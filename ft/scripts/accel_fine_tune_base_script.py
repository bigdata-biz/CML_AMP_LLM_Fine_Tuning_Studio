import argparse
import sys
import datasets
import json
import os

from accelerate import Accelerator, notebook_launcher
from accelerate.commands import launch as accel_launch
from typing import Tuple
from ft.utils import attempt_hf_login
from ft.client import FineTuningStudioClient
from ft.api import *

# TODO: Make all FTS configs/settings loading come from an imported module
#       so scripts like this focus on fine-tuning loop only
try:
    # Launch workers when using CML
    from cml.workers_v1 import launch_workers, list_workers, await_workers
except ImportError:
    # Launch workers when using CDSW
    from cdsw import launch_workers


# Constants
DATA_TEXT_FIELD = "prediction"
DEFAULT_TRAIN_TEST_SPLIT = 0.9
DEFAULT_DATASET_FRACTION = 1.0
SEED = 42

# Parse arguments from environment variable
arg_string = os.environ.get('JOB_ARGUMENTS', '')

parser = argparse.ArgumentParser()

# Args from FTS framework
parser.add_argument("--prompt_id", help="ID of the prompt template to use.", required=True)
parser.add_argument("--base_model_id", help="Base model ID to use.", required=True)
parser.add_argument("--dataset_id", help="Dataset ID from the Fine Tuning Studio application", required=True)
parser.add_argument("--experimentid", help="UUID to use for experiment tracking", required=True)
parser.add_argument("--out_dir", help="Output directory for the fine-tuned model", required=True)
parser.add_argument("--train_out_dir", help="Output directory for the training runs", required=True)
parser.add_argument("--train_test_split", type=float, default=DEFAULT_TRAIN_TEST_SPLIT,
                    help="Split of the existing dataset between training and testing.")
parser.add_argument("--dataset_fraction", type=float, default=DEFAULT_DATASET_FRACTION,
                    help="Fraction of the dataset to downsample to.")
parser.add_argument("--bnb_config_id", default=None, help="ID of the BnB config in FT Studio's config store.")
parser.add_argument("--lora_config_id", default=None, help="ID of the Lora config in FT Studio's config store.")
parser.add_argument("--training_arguments_config_id", default=None,
                    help="ID of the training arguments in FT Studio's config store.")
parser.add_argument("--hf_token", help="Huggingface access token to use for gated models", default=None)
parser.add_argument("--adapter_name", help="Human friendly name of the adapter to train", default=None)
parser.add_argument(
    "--auto_add_adapter",
    action="store_true",
    help="Automatically add an adapter to database if training succeeds.")

parser.add_argument("--dist_num", help="Number of workers to distriibute across", default=1, type=int)
parser.add_argument("--dist_cpu", help="Num vCPU specified for the FT job (for distributed worker launching)", default=0, type=float)
parser.add_argument("--dist_mem", help="Num mem in GB size specified for the FT job (for distributed worker launching)", default=0, type=float)
parser.add_argument("--dist_gpu", help="Num GPU specified for the FT job (for distributed worker launching)", default=0, type=int)
parser.add_argument("--gpu_label_id", help=" GPU Label specified for the FT job (for distributed worker launching)", default='')
parser.add_argument(
    "--finetuning_framework_type",
    help="Finetuning frameowork to be used for Model training.",
    default=FineTuningFrameworkType.LEGACY)

args = parser.parse_args(arg_string.split())


# Determine node rank for distributed training
NODE_RANK = int(os.environ.get('CML_FTS_JOB_NODE_RANK', '0'))

# Determine if this is a main job pod or a worker
print("This host is a  %s" % os.getenv('CDSW_ENGINE_TYPE'))
IS_MASTER = os.getenv('CDSW_ENGINE_TYPE') != "worker" and NODE_RANK == 0

# Figure out the job master IP for distributed training
JOB_MASTER_IP = os.environ.get('CML_FTS_JOB_MASTER_IP', os.environ.get('CDSW_IP_ADDRESS'))

# test local single rank run
#args.dist_num=1

# Create a client connection to the FTS server
fts: FineTuningStudioClient = FineTuningStudioClient()

# Attempt log in to huggingface
attempt_hf_login(args.hf_token)

# Get the configurations.
lora_config_dict = json.loads(
    fts.GetConfig(
        GetConfigRequest(
            id=args.lora_config_id
        )
    ).config.config
)

bnb_config_dict = json.loads(
    fts.GetConfig(
        GetConfigRequest(
            id=args.bnb_config_id
        )
    ).config.config
)

training_args_dict = json.loads(
    fts.GetConfig(
        GetConfigRequest(
            id=args.training_arguments_config_id
        )
    ).config.config
)

# Call the FTS server
# to extract metadata information about the dataset. Right now,
# only huggingface datasets are supported for fine tuning jobs.
dataset_id = args.dataset_id
dataset_metadata: DatasetMetadata = fts.GetDataset(
    GetDatasetRequest(
        id=dataset_id
    )
).dataset
assert dataset_metadata.type == DatasetType.HUGGINGFACE

# Extract other fields like base model and prompt.
base_model_md: ModelMetadata = fts.GetModel(
    GetModelRequest(
        id=args.base_model_id
    )
).model

# Extract prompt template information.
prompt_md: PromptMetadata = fts.GetPrompt(
    GetPromptRequest(
        id=args.prompt_id
    )
).prompt


# Data mapping functions for this style of finetuning
def load_dataset(dataset_name, dataset_fraction=100):
    """
    Loads a dataset from Huggingface, optionally sampling a fraction of it.

    Parameters:
        dataset_name (str): The name of the Huggingface dataset to load.
        dataset_fraction (int): The percentage of the dataset to load. Defaults to 100.

    Returns:
        datasets.Dataset: The loaded dataset.
    """
    try:
        return datasets.load_dataset(dataset_name, split=f'train[:{dataset_fraction}%]')
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")


def split_dataset(ds: datasets.Dataset, split_fraction: float = DEFAULT_TRAIN_TEST_SPLIT,
                  seed: int = SEED) -> Tuple[datasets.Dataset, datasets.Dataset]:
    """
    Split a dataset into two datasets given a split size and a random seed. This is
    primarily used to create a train dataset and an evaluation dataset.

    Parameters:
        split_fraction (float): the dataset split. The first dataset returned will be of size S*split_fraction.
        seed (int): randomized seed for dataset splitting.

    Returns:
        Tuple[Dataset, Dataset], the two split datasets.
    """
    dataset_split = ds.train_test_split(test_size=(1.0 - split_fraction), shuffle=True, seed=SEED)
    return dataset_split['train'], dataset_split['test']


def map_dataset_with_prompt_template(dataset, prompt_template, eos_token):
    """
    Maps a dataset with a given prompt template.

    Parameters:
        dataset (datasets.Dataset): The dataset to map.
        prompt_template (str): The prompt template to apply to the dataset.

    Returns:
        datasets.Dataset: The mapped dataset.
    """
    def ds_map(data):
        try:
            data[DATA_TEXT_FIELD] = prompt_template.format(**data) + eos_token
        except KeyError as e:
            raise KeyError(f"Error formatting data with prompt template: {e}")
        return data

    return dataset.map(ds_map)

# Single Training loop function to use with accelerate launchers
def training_loop():
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        DataCollatorForLanguageModeling,
    )
    import torch
    import mlflow

    from transformers import BitsAndBytesConfig, TrainingArguments
    from peft import LoraConfig, get_peft_model

    from trl import SFTTrainer

    accelerator = Accelerator()
    accelerator.print(accelerator.distributed_type)

    mlflow.set_experiment(args.experimentid)

    # Override the training args based on the provided output dir. The reason
    # this happens within the job (rather than passing the training job dir as part
    # of the output config) is that we set the training config BEFORE we have this
    # desired job ID field available. This is a side effect of using the UI.
    training_args_dict["output_dir"] = args.train_out_dir + "/" + str(NODE_RANK)

    print("Load the base model and tokenizer...\n")
    tokenizer = AutoTokenizer.from_pretrained(base_model_md.huggingface_model_name, use_auth_token=args.hf_token)
    tokenizer.pad_token = tokenizer.eos_token
    compute_dtype = getattr(torch, "float16")

    model = AutoModelForCausalLM.from_pretrained(
        base_model_md.huggingface_model_name,
        quantization_config=BitsAndBytesConfig(**bnb_config_dict),
        device_map={"": accelerator.process_index},
        token=args.hf_token,
    )

    # Set LORA Config
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

    model = get_peft_model(model, LoraConfig(**lora_config_dict))

    # Load and map dataset
    try:
        prompt_text = prompt_md.prompt_template
        with accelerator.main_process_first():
            dataset = load_dataset(dataset_metadata.huggingface_name, dataset_fraction=int(100 * args.dataset_fraction))

        # Split the above dataset into a training dataset and a testing dataset.
        ds_train, ds_eval = split_dataset(dataset, args.train_test_split)

        # Map both datasets with prompt templates
        ds_train = map_dataset_with_prompt_template(ds_train, prompt_text, tokenizer.eos_token)
        ds_eval = map_dataset_with_prompt_template(ds_eval, prompt_text, tokenizer.eos_token)
    except FileNotFoundError as e:
        raise RuntimeError(f"Error loading prompt template: {e}")

    accelerator.print("Total rows to be trained on: %d" % len(ds_train))
    trainer = accelerator.prepare(SFTTrainer(
        model=model,
        train_dataset=ds_train,
        eval_dataset=ds_eval,
        peft_config=LoraConfig(**lora_config_dict),
        tokenizer=tokenizer,
        dataset_text_field=DATA_TEXT_FIELD,
        packing=True,
        max_seq_length=512,
        args=TrainingArguments(**training_args_dict),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
       callbacks=[],
    ))

    trainer.train()
    print("Training Complete on this Worker!")

    # Save the model and the tokenizer.
    # This should only execute on the master worker in distributed mode
    trainer.save_model(args.out_dir)

    
print("This training should occur across %d workers" % args.dist_num)

## TODO: BEGIN Remove this monkeypatch when a PR is approved to fix the single gpu machines issue
# HF notebook_launcher implementation does not support 1 gpu machines in multi-node training
# https://github.com/huggingface/accelerate/blob/v0.32.0-release/src/accelerate/launchers.py#L165
# Implementing trainer_launcher to achieve this until this is fixed

import os
import torch
from accelerate.utils import (
    PrecisionType,
    PrepareForLaunch,
    check_cuda_p2p_ib_support,
    is_torch_version,
    patch_environment,
)
from accelerate.utils.constants import ELASTIC_LOG_LINE_PREFIX_TEMPLATE_PYTORCH_VERSION

def notebook_launcher_single_gpu_dist(
    function,
    args=(),
    num_processes=None,
    mixed_precision="no",
    use_port="29500",
    master_addr="127.0.0.1",
    node_rank=0,
    num_nodes=1,
    rdzv_backend="static",
    rdzv_endpoint="",
    rdzv_conf=None,
    rdzv_id="none",
    max_restarts=0,
    monitor_interval=0.1,
    log_line_prefix_template=None,
):

    if num_processes*num_nodes > 1:
        # Multi-GPU launch across nodes or gpu or both
        from torch.distributed.launcher.api import LaunchConfig, elastic_launch
        from torch.multiprocessing import start_processes
        from torch.multiprocessing.spawn import ProcessRaisedException

        patched_env = dict(
            nproc=num_processes,
            node_rank=node_rank,
            world_size=num_nodes * num_processes,
            master_addr=master_addr,
            master_port=use_port,
            mixed_precision=mixed_precision,
        )
        # Check for CUDA P2P and IB issues
        if not check_cuda_p2p_ib_support():
            patched_env["nccl_p2p_disable"] = "1"
            patched_env["nccl_ib_disable"] = "1"
        with patch_environment(**patched_env):
            launcher = PrepareForLaunch(function, distributed_type="MULTI_GPU")
            print(f"Launching training on {num_processes} GPUs.")
            try:
                if rdzv_conf is None:
                    rdzv_conf = {}
                if rdzv_backend == "static":
                    rdzv_conf["rank"] = node_rank
                    if not rdzv_endpoint:
                        rdzv_endpoint = f"{master_addr}:{use_port}"
                launch_config_kwargs = dict(
                    min_nodes=num_nodes,
                    max_nodes=num_nodes,
                    nproc_per_node=num_processes,
                    run_id=rdzv_id,
                    rdzv_endpoint=rdzv_endpoint,
                    rdzv_backend=rdzv_backend,
                    rdzv_configs=rdzv_conf,
                    max_restarts=max_restarts,
                    monitor_interval=monitor_interval,
                    start_method="fork",
                )
                if is_torch_version(">=", ELASTIC_LOG_LINE_PREFIX_TEMPLATE_PYTORCH_VERSION):
                    launch_config_kwargs["log_line_prefix_template"] = log_line_prefix_template
                elastic_launch(config=LaunchConfig(**launch_config_kwargs), entrypoint=function)(*args)
            except ProcessRaisedException as e:
                if "Cannot re-initialize CUDA in forked subprocess" in e.args[0]:
                    raise RuntimeError(
                        "CUDA has been initialized before the `notebook_launcher` could create a forked subprocess. "
                        "Check training loop wrapper function to make sure there is not a rogue import"
                    ) from e
                else:
                    raise RuntimeError(f"An issue was found when launching the training: {e}") from e

    else:
        # Non-distributed launch
        if torch.cuda.is_available():
            print("Launching training on one GPU.")
        else:
            print("Launching training on CPU.")
        function(*args)
# Monkey-patch imported notebook_launcher
notebook_launcher = notebook_launcher_single_gpu_dist
## TODO: END Remove this monkeypatch when a PR is approved to fix the single gpu machines issue


# Script launching logic do handle all training loop launching and workers spinup
if IS_MASTER: 
    # Parent workload needs to handle launching additional workers and then launch a finetuning loop itself
    for i in reversed(range(args.dist_num)):
        print("Handling rank number %d" % i)
        if i == 0:
            print(" - Launching master finetuning process")
            notebook_launcher(training_loop,
                              master_addr=JOB_MASTER_IP,
                              node_rank=NODE_RANK,
                              num_nodes=int(args.dist_num),
                              num_processes=int(args.dist_gpu)
                            )
        else:
            print(" - Launching worker %d for data distributed finetuning" % i)
            print(" - master_addr = %s" % JOB_MASTER_IP)
            # Setting up Worker ENVs to ensure pass through of args from the top of the script
            worker_envs = {}
            worker_envs['CML_FTS_JOB_MASTER_IP'] = JOB_MASTER_IP
            worker_envs['JOB_ARGUMENTS'] = os.environ.get('JOB_ARGUMENTS', '')
            worker_envs['CML_FTS_JOB_NODE_RANK'] = str(i)

            # This is to support compatibility with old workspaces without heterogeneous gpu support
            if args.gpu_label_id != -1 :
                launch_workers(n=1, cpu=args.dist_cpu, memory=args.dist_mem,
                            nvidia_gpu=args.dist_gpu,
                            script="/home/cdsw/ft/scripts/accel_fine_tune_base_script.py",
                            env=worker_envs,
                            accelerator_label_id=args.gpu_label_id
                            )
            else: 
                launch_workers(n=1, cpu=args.dist_cpu, memory=args.dist_mem,
                            nvidia_gpu=args.dist_gpu,
                            script="/home/cdsw/ft/scripts/accel_fine_tune_base_script.py",
                            env=worker_envs,
                            )
            print("Launched woker for rank %d" % i)
    if (args.dist_num > 1): 
        # Wait for all workers to complete
        worker_statuses = await_workers(ids = list_workers(), wait_for_completion=True)
        print(worker_statuses)
        if len(worker_statuses["failures"]) >= 1:
            sys.exit("A worker failed. Exiting training")
    # Upon completion, add the adapter to metadata if it's
    # requested to do so.
    print("Adding adapter to the FTS metadata")
    fts.AddAdapter(
        AddAdapterRequest(
            type=AdapterType.PROJECT,
            name=args.adapter_name,
            model_id=base_model_md.id,
            location=args.out_dir,
            fine_tuning_job_id=args.experimentid,
            prompt_id=prompt_md.id
        )
    )
else:
    # This is a worker, launch the training loop with notebook_launcher
    print("Launching worker finetuning process with node_rank=%d and num_nodes=%d" % (NODE_RANK, int(args.dist_num)))
    print(" - master_addr = %s" % JOB_MASTER_IP)
    notebook_launcher(training_loop, master_addr=JOB_MASTER_IP, node_rank=NODE_RANK,
                      num_nodes=int(args.dist_num), num_processes=int(args.dist_gpu))
    
print("Exiting job finetuning script.")