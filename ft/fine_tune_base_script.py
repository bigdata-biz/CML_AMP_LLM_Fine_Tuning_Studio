from transformers import BitsAndBytesConfig
from pathlib import Path
from peft import LoraConfig
import json
import datasets
from ft import fine_tune, fine_tune_axolotl
import argparse
import os
from typing import Tuple
from ft.utils import attempt_hf_login

# Constants
NUM_EPOCHS = 3
LEARNING_RATE = 2e-4
DATA_TEXT_FIELD = "prediction"
TRAIN_TEST_SPLIT = 0.1
SEED = 42

# Parse arguments from environment variable
arg_string = os.environ.get('JOB_ARGUMENTS', '')

parser = argparse.ArgumentParser()

parser.add_argument(
    "--aggregateconfig",
    help="Path of the aggregate config containing: LoraConfig, BitsAndBytesConfig, prompt text, trainer arguments")
parser.add_argument("--loraconfig", help="Path of the LoRA config json")
parser.add_argument("--bnbconfig", help="Path of the BitsAndBytes config json")
parser.add_argument("--prompttemplate", help="Path of the PromptTemplate")
parser.add_argument("--trainerarguments", help="Path of the trainer arguments json")
parser.add_argument("--basemodel", help="Huggingface base model to use")
parser.add_argument("--dataset", help="Huggingface dataset to use")
parser.add_argument("--experimentid", help="UUID to use for experiment tracking", required=True)
parser.add_argument("--out_dir", help="Output directory for the fine-tuned model")
parser.add_argument("--num_epochs", type=int, default=NUM_EPOCHS, help="Epochs for fine tuning job")
parser.add_argument("--learning_rate", type=float, default=LEARNING_RATE, help="Learning rate for fine tuning job")
parser.add_argument("--train_test_split", type=float, default=TRAIN_TEST_SPLIT,
                    help="Split of the existing dataset between training and testing.")
parser.add_argument("--hf_token", help="Huggingface access token to use for gated models", default=None)
parser.add_argument(
    "--finetuning_framework",
    help="Framework to use for fine-tuning ('legacy' or 'axolotl')",
    required=True)
parser.add_argument("--axolotl_yaml_file_path", help="YAML file path for Axolotl training configuration")

args = parser.parse_args(arg_string.split())


def load_dataset(dataset_name: str, dataset_fraction: int = 100) -> datasets.Dataset:
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


def split_dataset(ds: datasets.Dataset, split_fraction: float = TRAIN_TEST_SPLIT,
                  seed: int = SEED) -> Tuple[datasets.Dataset, datasets.Dataset]:
    """
    Split a dataset into two datasets given a split size and a random seed.

    Parameters:
        split_fraction (float): the dataset split. The first dataset returned will be of size S*(1-split_fraction).
        seed (int): randomized seed for dataset splitting.

    Returns:
        Tuple[Dataset, Dataset], the two split datasets.
    """
    dataset_split = ds.train_test_split(test_size=split_fraction, shuffle=True, seed=seed)
    return dataset_split['train'], dataset_split['test']


def map_dataset_with_prompt_template(dataset: datasets.Dataset, prompt_template: str) -> datasets.Dataset:
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
            data[DATA_TEXT_FIELD] = prompt_template.format(**data) + finetuner.tokenizer.eos_token
        except KeyError as e:
            raise KeyError(f"Error formatting data with prompt template: {e}")
        return data

    return dataset.map(ds_map)


# Attempt log in to huggingface
attempt_hf_login(args.hf_token)

if args.finetuning_framework == 'legacy':
    # Load aggregate config file
    try:
        aggregate_config_file = Path(args.aggregateconfig).read_text()
        aggregate_config = json.loads(aggregate_config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error loading aggregate config file: {e}")

    # Initialize BitsAndBytesConfig
    try:
        bnb_config = BitsAndBytesConfig(**aggregate_config['bnb_config'])
    except KeyError as e:
        raise KeyError(f"Missing key in BitsAndBytesConfig: {e}")

    # Initialize the fine-tuner
    finetuner = fine_tune.AMPFineTuner(
        base_model=args.basemodel,
        ft_job_uuid=args.experimentid,
        bnb_config=bnb_config,
        auth_token=args.hf_token,
    )

    # Set LoRA training configuration
    finetuner.set_lora_config(
        LoraConfig(
            r=16,
            lora_alpha=32,
            # target_modules=["query_key_value", "xxx"],  # Customize as needed
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
    )

    # Set training arguments
    finetuner.training_args.num_train_epochs = args.num_epochs
    finetuner.training_args.warmup_ratio = 0.03
    finetuner.training_args.max_grad_norm = 0.3
    finetuner.training_args.learning_rate = args.learning_rate

    # Load and map dataset
    try:
        prompt_text = Path(args.prompttemplate).read_text()

        # Load the base dataset into memory
        dataset = load_dataset(args.dataset)

        # Split the above dataset into a training dataset and a testing dataset.
        ds_train, ds_eval = split_dataset(dataset, args.train_test_split)

        # Map both datasets with prompt templates
        ds_train = map_dataset_with_prompt_template(ds_train, prompt_text)
        ds_eval = map_dataset_with_prompt_template(ds_eval, prompt_text)

    except FileNotFoundError as e:
        raise RuntimeError(f"Error loading prompt template: {e}")

    # Start fine-tuning
    finetuner.train(
        train_dataset=ds_train,
        eval_dataset=ds_eval,
        dataset_text_field=DATA_TEXT_FIELD,
        output_dir=args.out_dir
    )

elif args.finetuning_framework == 'axolotl':
    if not args.axolotl_yaml_file_path:
        raise ValueError("YAML file path must be provided for Axolotl training configuration.")

    # Initialize the fine-tuner
    finetuner = fine_tune_axolotl.AxolotlFineTuner(
        ft_job_uuid=args.experimentid
    )

    # Start fine-tuning
    try:
        finetuner.train(yaml_file_path=args.axolotl_yaml_file_path)
    except FileNotFoundError as e:
        raise RuntimeError(f"Error loading Axolotl YAML configuration: {e}")
    except Exception as e:
        raise RuntimeError(f"Error during Axolotl fine-tuning: {e}")

else:
    raise ValueError("Finetuning framework not supported")
