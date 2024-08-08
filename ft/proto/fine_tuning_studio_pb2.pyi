from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor


class DatasetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_TYPE_HUGGINGFACE: _ClassVar[DatasetType]
    DATASET_TYPE_PROJECT: _ClassVar[DatasetType]


class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_TYPE_HUGGINGFACE: _ClassVar[ModelType]
    MODEL_TYPE_PROJECT: _ClassVar[ModelType]
    MODEL_TYPE_MODEL_REGISTRY: _ClassVar[ModelType]


class ModelFrameworkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_FRAMEWORK_TYPE_PYTORCH: _ClassVar[ModelFrameworkType]
    MODEL_FRAMEWORK_TYPE_TENSORFLOW: _ClassVar[ModelFrameworkType]
    MODEL_FRAMEWORK_TYPE_ONNX: _ClassVar[ModelFrameworkType]


class AdapterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADAPTER_TYPE_PROJECT: _ClassVar[AdapterType]
    ADAPTER_TYPE_HUGGINGFACE: _ClassVar[AdapterType]
    ADAPTER_TYPE_MODEL_REGISTRY: _ClassVar[AdapterType]


class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_STATUS_SCHEDULED: _ClassVar[JobStatus]
    JOB_STATUS_RUNNING: _ClassVar[JobStatus]
    JOB_STATUS_SUCCESS: _ClassVar[JobStatus]
    JOB_STATUS_FAILURE: _ClassVar[JobStatus]


class PromptType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROMPT_TYPE_IN_PLACE: _ClassVar[PromptType]


class EvaluationJobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVALUATION_JOB_TYPE_MLFLOW: _ClassVar[EvaluationJobType]


DATASET_TYPE_HUGGINGFACE: DatasetType
DATASET_TYPE_PROJECT: DatasetType
MODEL_TYPE_HUGGINGFACE: ModelType
MODEL_TYPE_PROJECT: ModelType
MODEL_TYPE_MODEL_REGISTRY: ModelType
MODEL_FRAMEWORK_TYPE_PYTORCH: ModelFrameworkType
MODEL_FRAMEWORK_TYPE_TENSORFLOW: ModelFrameworkType
MODEL_FRAMEWORK_TYPE_ONNX: ModelFrameworkType
ADAPTER_TYPE_PROJECT: AdapterType
ADAPTER_TYPE_HUGGINGFACE: AdapterType
ADAPTER_TYPE_MODEL_REGISTRY: AdapterType
JOB_STATUS_SCHEDULED: JobStatus
JOB_STATUS_RUNNING: JobStatus
JOB_STATUS_SUCCESS: JobStatus
JOB_STATUS_FAILURE: JobStatus
PROMPT_TYPE_IN_PLACE: PromptType
EVALUATION_JOB_TYPE_MLFLOW: EvaluationJobType


class ListDatasetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListDatasetsResponse(_message.Message):
    __slots__ = ("datasets",)
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[DatasetMetadata]
    def __init__(self, datasets: _Optional[_Iterable[_Union[DatasetMetadata, _Mapping]]] = ...) -> None: ...


class GetDatasetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: DatasetMetadata
    def __init__(self, dataset: _Optional[_Union[DatasetMetadata, _Mapping]] = ...) -> None: ...


class AddDatasetRequest(_message.Message):
    __slots__ = ("type", "huggingface_name", "location")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    type: DatasetType
    huggingface_name: str
    location: str
    def __init__(self, type: _Optional[_Union[DatasetType, str]] = ...,
                 huggingface_name: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...


class AddDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: DatasetMetadata
    def __init__(self, dataset: _Optional[_Union[DatasetMetadata, _Mapping]] = ...) -> None: ...


class RemoveDatasetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemoveDatasetResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListModelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListModelsResponse(_message.Message):
    __slots__ = ("Models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    Models: _containers.RepeatedCompositeFieldContainer[ModelMetadata]
    def __init__(self, Models: _Optional[_Iterable[_Union[ModelMetadata, _Mapping]]] = ...) -> None: ...


class GetModelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelMetadata
    def __init__(self, model: _Optional[_Union[ModelMetadata, _Mapping]] = ...) -> None: ...


class AddModelRequest(_message.Message):
    __slots__ = ("type", "huggingface_name", "model_registry_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_REGISTRY_ID_FIELD_NUMBER: _ClassVar[int]
    type: ModelType
    huggingface_name: str
    model_registry_id: str

    def __init__(self,
                 type: _Optional[_Union[ModelType,
                                        str]] = ...,
                 huggingface_name: _Optional[str] = ...,
                 model_registry_id: _Optional[str] = ...) -> None: ...


class AddModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelMetadata
    def __init__(self, model: _Optional[_Union[ModelMetadata, _Mapping]] = ...) -> None: ...


class ExportModelRequest(_message.Message):
    __slots__ = ("type", "model_id", "adapter_id", "model_name", "artifact_location", "model_description")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    MODEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    type: ModelType
    model_id: str
    adapter_id: str
    model_name: str
    artifact_location: str
    model_description: str

    def __init__(self,
                 type: _Optional[_Union[ModelType,
                                        str]] = ...,
                 model_id: _Optional[str] = ...,
                 adapter_id: _Optional[str] = ...,
                 model_name: _Optional[str] = ...,
                 artifact_location: _Optional[str] = ...,
                 model_description: _Optional[str] = ...) -> None: ...


class ExportModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelMetadata
    def __init__(self, model: _Optional[_Union[ModelMetadata, _Mapping]] = ...) -> None: ...


class RemoveModelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemoveModelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListAdaptersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListAdaptersResponse(_message.Message):
    __slots__ = ("Adapters",)
    ADAPTERS_FIELD_NUMBER: _ClassVar[int]
    Adapters: _containers.RepeatedCompositeFieldContainer[AdapterMetadata]
    def __init__(self, Adapters: _Optional[_Iterable[_Union[AdapterMetadata, _Mapping]]] = ...) -> None: ...


class GetAdapterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetAdapterResponse(_message.Message):
    __slots__ = ("adapter",)
    ADAPTER_FIELD_NUMBER: _ClassVar[int]
    adapter: AdapterMetadata
    def __init__(self, adapter: _Optional[_Union[AdapterMetadata, _Mapping]] = ...) -> None: ...


class AddAdapterRequest(_message.Message):
    __slots__ = ("type", "huggingface_name", "location")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    type: AdapterType
    huggingface_name: str
    location: str
    def __init__(self, type: _Optional[_Union[AdapterType, str]] = ...,
                 huggingface_name: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...


class AddAdapterResponse(_message.Message):
    __slots__ = ("adapter",)
    ADAPTER_FIELD_NUMBER: _ClassVar[int]
    adapter: AdapterMetadata
    def __init__(self, adapter: _Optional[_Union[AdapterMetadata, _Mapping]] = ...) -> None: ...


class RemoveAdapterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemoveAdapterResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListPromptsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListPromptsResponse(_message.Message):
    __slots__ = ("Prompts",)
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    Prompts: _containers.RepeatedCompositeFieldContainer[PromptMetadata]
    def __init__(self, Prompts: _Optional[_Iterable[_Union[PromptMetadata, _Mapping]]] = ...) -> None: ...


class GetPromptRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetPromptResponse(_message.Message):
    __slots__ = ("Prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    Prompt: PromptMetadata
    def __init__(self, Prompt: _Optional[_Union[PromptMetadata, _Mapping]] = ...) -> None: ...


class AddPromptRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: PromptType
    def __init__(self, type: _Optional[_Union[PromptType, str]] = ...) -> None: ...


class AddPromptResponse(_message.Message):
    __slots__ = ("Prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    Prompt: PromptMetadata
    def __init__(self, Prompt: _Optional[_Union[PromptMetadata, _Mapping]] = ...) -> None: ...


class RemovePromptRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemovePromptResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListFineTuningJobsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListFineTuningJobsResponse(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[FineTuningJobMetadata]
    def __init__(self, jobs: _Optional[_Iterable[_Union[FineTuningJobMetadata, _Mapping]]] = ...) -> None: ...


class GetFineTuningJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetFineTuningJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: FineTuningJobMetadata
    def __init__(self, job: _Optional[_Union[FineTuningJobMetadata, _Mapping]] = ...) -> None: ...


class StartFineTuningJobRequest(_message.Message):
    __slots__ = (
        "adapter_name",
        "base_model_id",
        "dataset_id",
        "prompt_id",
        "num_workers",
        "bits_and_bytes_config",
        "auto_add_adapter",
        "num_epochs",
        "learning_rate",
        "cpu",
        "gpu",
        "memory",
        "train_test_split",
        "finetuning_framework",
        "axolotl_train_config")
    ADAPTER_NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    BITS_AND_BYTES_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUTO_ADD_ADAPTER_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    TRAIN_TEST_SPLIT_FIELD_NUMBER: _ClassVar[int]
    FINETUNING_FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    AXOLOTL_TRAIN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    adapter_name: str
    base_model_id: str
    dataset_id: str
    prompt_id: str
    num_workers: int
    bits_and_bytes_config: BnbConfig
    auto_add_adapter: bool
    num_epochs: int
    learning_rate: float
    cpu: int
    gpu: int
    memory: int
    train_test_split: float
    finetuning_framework: str
    axolotl_train_config: AxolotlTrainConfig

    def __init__(self,
                 adapter_name: _Optional[str] = ...,
                 base_model_id: _Optional[str] = ...,
                 dataset_id: _Optional[str] = ...,
                 prompt_id: _Optional[str] = ...,
                 num_workers: _Optional[int] = ...,
                 bits_and_bytes_config: _Optional[_Union[BnbConfig,
                                                         _Mapping]] = ...,
                 auto_add_adapter: bool = ...,
                 num_epochs: _Optional[int] = ...,
                 learning_rate: _Optional[float] = ...,
                 cpu: _Optional[int] = ...,
                 gpu: _Optional[int] = ...,
                 memory: _Optional[int] = ...,
                 train_test_split: _Optional[float] = ...,
                 finetuning_framework: _Optional[str] = ...,
                 axolotl_train_config: _Optional[_Union[AxolotlTrainConfig,
                                                        _Mapping]] = ...) -> None: ...


class StartFineTuningJobResponse(_message.Message):
    __slots__ = ("FineTuningJob",)
    FINETUNINGJOB_FIELD_NUMBER: _ClassVar[int]
    FineTuningJob: FineTuningJobMetadata
    def __init__(self, FineTuningJob: _Optional[_Union[FineTuningJobMetadata, _Mapping]] = ...) -> None: ...


class RemoveFineTuningJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemoveFineTuningJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListEvaluationJobsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class ListEvaluationJobsResponse(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[EvaluationJobMetadata]
    def __init__(self, jobs: _Optional[_Iterable[_Union[EvaluationJobMetadata, _Mapping]]] = ...) -> None: ...


class GetEvaluationJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class GetEvaluationJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: EvaluationJobMetadata
    def __init__(self, job: _Optional[_Union[EvaluationJobMetadata, _Mapping]] = ...) -> None: ...


class StartEvaluationJobRequest(_message.Message):
    __slots__ = ("type", "base_model_id", "dataset_id", "adapter_id", "cpu", "gpu", "memory")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_ID_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    type: EvaluationJobType
    base_model_id: str
    dataset_id: str
    adapter_id: str
    cpu: int
    gpu: int
    memory: int

    def __init__(self,
                 type: _Optional[_Union[EvaluationJobType,
                                        str]] = ...,
                 base_model_id: _Optional[str] = ...,
                 dataset_id: _Optional[str] = ...,
                 adapter_id: _Optional[str] = ...,
                 cpu: _Optional[int] = ...,
                 gpu: _Optional[int] = ...,
                 memory: _Optional[int] = ...) -> None: ...


class StartEvaluationJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: EvaluationJobMetadata
    def __init__(self, job: _Optional[_Union[EvaluationJobMetadata, _Mapping]] = ...) -> None: ...


class RemoveEvaluationJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...


class RemoveEvaluationJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class GetAppStateRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...


class GetAppStateResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: AppState
    def __init__(self, state: _Optional[_Union[AppState, _Mapping]] = ...) -> None: ...


class DatasetMetadata(_message.Message):
    __slots__ = ("id", "type", "name", "description", "huggingface_name", "location", "features")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: DatasetType
    name: str
    description: str
    huggingface_name: str
    location: str
    features: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self,
                 id: _Optional[str] = ...,
                 type: _Optional[_Union[DatasetType,
                                        str]] = ...,
                 name: _Optional[str] = ...,
                 description: _Optional[str] = ...,
                 huggingface_name: _Optional[str] = ...,
                 location: _Optional[str] = ...,
                 features: _Optional[_Iterable[str]] = ...) -> None: ...


class RegisteredModelMetadata(_message.Message):
    __slots__ = ("cml_registered_model_id", "mlflow_experiment_id", "mlflow_run_id")
    CML_REGISTERED_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MLFLOW_EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MLFLOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    cml_registered_model_id: str
    mlflow_experiment_id: str
    mlflow_run_id: str

    def __init__(
        self,
        cml_registered_model_id: _Optional[str] = ...,
        mlflow_experiment_id: _Optional[str] = ...,
        mlflow_run_id: _Optional[str] = ...) -> None: ...


class ModelMetadata(_message.Message):
    __slots__ = ("id", "type", "framework", "name", "huggingface_model_name", "location", "registered_model")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_MODEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: ModelType
    framework: ModelFrameworkType
    name: str
    huggingface_model_name: str
    location: str
    registered_model: RegisteredModelMetadata

    def __init__(self,
                 id: _Optional[str] = ...,
                 type: _Optional[_Union[ModelType,
                                        str]] = ...,
                 framework: _Optional[_Union[ModelFrameworkType,
                                             str]] = ...,
                 name: _Optional[str] = ...,
                 huggingface_model_name: _Optional[str] = ...,
                 location: _Optional[str] = ...,
                 registered_model: _Optional[_Union[RegisteredModelMetadata,
                                                    _Mapping]] = ...) -> None: ...


class AdapterMetadata(_message.Message):
    __slots__ = (
        "id",
        "type",
        "name",
        "model_id",
        "location",
        "huggingface_name",
        "job_id",
        "prompt_id",
        "registered_model")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_MODEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: AdapterType
    name: str
    model_id: str
    location: str
    huggingface_name: str
    job_id: str
    prompt_id: str
    registered_model: RegisteredModelMetadata

    def __init__(self,
                 id: _Optional[str] = ...,
                 type: _Optional[_Union[AdapterType,
                                        str]] = ...,
                 name: _Optional[str] = ...,
                 model_id: _Optional[str] = ...,
                 location: _Optional[str] = ...,
                 huggingface_name: _Optional[str] = ...,
                 job_id: _Optional[str] = ...,
                 prompt_id: _Optional[str] = ...,
                 registered_model: _Optional[_Union[RegisteredModelMetadata,
                                                    _Mapping]] = ...) -> None: ...


class PromptMetadata(_message.Message):
    __slots__ = ("id", "name", "dataset_id", "prompt_template")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    dataset_id: str
    prompt_template: str

    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        prompt_template: _Optional[str] = ...) -> None: ...


class WorkerProps(_message.Message):
    __slots__ = ("num_cpu", "num_memory", "num_gpu")
    NUM_CPU_FIELD_NUMBER: _ClassVar[int]
    NUM_MEMORY_FIELD_NUMBER: _ClassVar[int]
    NUM_GPU_FIELD_NUMBER: _ClassVar[int]
    num_cpu: int
    num_memory: int
    num_gpu: int

    def __init__(
        self,
        num_cpu: _Optional[int] = ...,
        num_memory: _Optional[int] = ...,
        num_gpu: _Optional[int] = ...) -> None: ...


class FineTuningJobMetadata(_message.Message):
    __slots__ = (
        "job_id",
        "base_model_id",
        "dataset_id",
        "prompt_id",
        "num_workers",
        "cml_job_id",
        "adapter_id",
        "worker_props",
        "num_epochs",
        "learning_rate",
        "out_dir",
        "finetuning_framework",
        "axolotl_train_config")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    CML_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_PROPS_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    OUT_DIR_FIELD_NUMBER: _ClassVar[int]
    FINETUNING_FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    AXOLOTL_TRAIN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    base_model_id: str
    dataset_id: str
    prompt_id: str
    num_workers: int
    cml_job_id: str
    adapter_id: str
    worker_props: WorkerProps
    num_epochs: int
    learning_rate: float
    out_dir: str
    finetuning_framework: str
    axolotl_train_config: AxolotlTrainConfig

    def __init__(self,
                 job_id: _Optional[str] = ...,
                 base_model_id: _Optional[str] = ...,
                 dataset_id: _Optional[str] = ...,
                 prompt_id: _Optional[str] = ...,
                 num_workers: _Optional[int] = ...,
                 cml_job_id: _Optional[str] = ...,
                 adapter_id: _Optional[str] = ...,
                 worker_props: _Optional[_Union[WorkerProps,
                                                _Mapping]] = ...,
                 num_epochs: _Optional[int] = ...,
                 learning_rate: _Optional[float] = ...,
                 out_dir: _Optional[str] = ...,
                 finetuning_framework: _Optional[str] = ...,
                 axolotl_train_config: _Optional[_Union[AxolotlTrainConfig,
                                                        _Mapping]] = ...) -> None: ...


class BnbConfig(_message.Message):
    __slots__ = (
        "load_in_8bit",
        "load_in_4bit",
        "bnb_4bit_compute_dtype",
        "bnb_4bit_quant_type",
        "bnb_4bit_use_double_quant",
        "bnb_4bit_quant_storage",
        "quant_method")
    LOAD_IN_8BIT_FIELD_NUMBER: _ClassVar[int]
    LOAD_IN_4BIT_FIELD_NUMBER: _ClassVar[int]
    BNB_4BIT_COMPUTE_DTYPE_FIELD_NUMBER: _ClassVar[int]
    BNB_4BIT_QUANT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BNB_4BIT_USE_DOUBLE_QUANT_FIELD_NUMBER: _ClassVar[int]
    BNB_4BIT_QUANT_STORAGE_FIELD_NUMBER: _ClassVar[int]
    QUANT_METHOD_FIELD_NUMBER: _ClassVar[int]
    load_in_8bit: bool
    load_in_4bit: bool
    bnb_4bit_compute_dtype: str
    bnb_4bit_quant_type: str
    bnb_4bit_use_double_quant: bool
    bnb_4bit_quant_storage: str
    quant_method: str

    def __init__(
        self,
        load_in_8bit: bool = ...,
        load_in_4bit: bool = ...,
        bnb_4bit_compute_dtype: _Optional[str] = ...,
        bnb_4bit_quant_type: _Optional[str] = ...,
        bnb_4bit_use_double_quant: bool = ...,
        bnb_4bit_quant_storage: _Optional[str] = ...,
        quant_method: _Optional[str] = ...) -> None: ...


class EvaluationJobMetadata(_message.Message):
    __slots__ = (
        "job_id",
        "cml_job_id",
        "base_model_id",
        "dataset_id",
        "num_workers",
        "adapter_id",
        "worker_props",
        "evaluation_dir")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    CML_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_PROPS_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_DIR_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    cml_job_id: str
    base_model_id: str
    dataset_id: str
    num_workers: int
    adapter_id: str
    worker_props: WorkerProps
    evaluation_dir: str

    def __init__(self,
                 job_id: _Optional[str] = ...,
                 cml_job_id: _Optional[str] = ...,
                 base_model_id: _Optional[str] = ...,
                 dataset_id: _Optional[str] = ...,
                 num_workers: _Optional[int] = ...,
                 adapter_id: _Optional[str] = ...,
                 worker_props: _Optional[_Union[WorkerProps,
                                                _Mapping]] = ...,
                 evaluation_dir: _Optional[str] = ...) -> None: ...


class AppState(_message.Message):
    __slots__ = ("datasets", "models", "fine_tuning_jobs", "evaluation_jobs", "prompts", "adapters")
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    FINE_TUNING_JOBS_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_JOBS_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    ADAPTERS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[DatasetMetadata]
    models: _containers.RepeatedCompositeFieldContainer[ModelMetadata]
    fine_tuning_jobs: _containers.RepeatedCompositeFieldContainer[FineTuningJobMetadata]
    evaluation_jobs: _containers.RepeatedCompositeFieldContainer[EvaluationJobMetadata]
    prompts: _containers.RepeatedCompositeFieldContainer[PromptMetadata]
    adapters: _containers.RepeatedCompositeFieldContainer[AdapterMetadata]

    def __init__(self,
                 datasets: _Optional[_Iterable[_Union[DatasetMetadata,
                                                      _Mapping]]] = ...,
                 models: _Optional[_Iterable[_Union[ModelMetadata,
                                                    _Mapping]]] = ...,
                 fine_tuning_jobs: _Optional[_Iterable[_Union[FineTuningJobMetadata,
                                                              _Mapping]]] = ...,
                 evaluation_jobs: _Optional[_Iterable[_Union[EvaluationJobMetadata,
                                                             _Mapping]]] = ...,
                 prompts: _Optional[_Iterable[_Union[PromptMetadata,
                                                     _Mapping]]] = ...,
                 adapters: _Optional[_Iterable[_Union[AdapterMetadata,
                                                      _Mapping]]] = ...) -> None: ...


class AxolotlTrainConfig(_message.Message):
    __slots__ = (
        "base_model",
        "model_type",
        "tokenizer_type",
        "trust_remote_code",
        "tokenizer_use_fast",
        "tokenizer_legacy",
        "gptq",
        "load_in_8bit",
        "load_in_4bit",
        "bf16",
        "fp16",
        "tf32",
        "datasets",
        "shuffle_merged_datasets",
        "dataset_prepared_path",
        "val_set_size",
        "sequence_len",
        "pad_to_sequence_len",
        "sample_packing",
        "eval_sample_packing",
        "adapter",
        "lora_model_dir",
        "lora_r",
        "lora_alpha",
        "lora_dropout",
        "lora_target_modules",
        "lora_target_linear",
        "mlflow_tracking_uri",
        "mlflow_experiment_name",
        "hf_mlflow_log_artifacts",
        "output_dir",
        "gradient_accumulation_steps",
        "micro_batch_size",
        "num_epochs",
        "warmup_ratio",
        "learning_rate",
        "logging_steps",
        "evals_per_epoch",
        "save_safetensors",
        "train_on_inputs",
        "group_by_length",
        "gradient_checkpointing",
        "lr_scheduler",
        "optimizer",
        "weight_decay",
        "strict",
        "xformers_attention",
        "flash_attention")
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRUST_REMOTE_CODE_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_USE_FAST_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_LEGACY_FIELD_NUMBER: _ClassVar[int]
    GPTQ_FIELD_NUMBER: _ClassVar[int]
    LOAD_IN_8BIT_FIELD_NUMBER: _ClassVar[int]
    LOAD_IN_4BIT_FIELD_NUMBER: _ClassVar[int]
    BF16_FIELD_NUMBER: _ClassVar[int]
    FP16_FIELD_NUMBER: _ClassVar[int]
    TF32_FIELD_NUMBER: _ClassVar[int]
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    SHUFFLE_MERGED_DATASETS_FIELD_NUMBER: _ClassVar[int]
    DATASET_PREPARED_PATH_FIELD_NUMBER: _ClassVar[int]
    VAL_SET_SIZE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_LEN_FIELD_NUMBER: _ClassVar[int]
    PAD_TO_SEQUENCE_LEN_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_PACKING_FIELD_NUMBER: _ClassVar[int]
    EVAL_SAMPLE_PACKING_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_FIELD_NUMBER: _ClassVar[int]
    LORA_MODEL_DIR_FIELD_NUMBER: _ClassVar[int]
    LORA_R_FIELD_NUMBER: _ClassVar[int]
    LORA_ALPHA_FIELD_NUMBER: _ClassVar[int]
    LORA_DROPOUT_FIELD_NUMBER: _ClassVar[int]
    LORA_TARGET_MODULES_FIELD_NUMBER: _ClassVar[int]
    LORA_TARGET_LINEAR_FIELD_NUMBER: _ClassVar[int]
    MLFLOW_TRACKING_URI_FIELD_NUMBER: _ClassVar[int]
    MLFLOW_EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    HF_MLFLOW_LOG_ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DIR_FIELD_NUMBER: _ClassVar[int]
    GRADIENT_ACCUMULATION_STEPS_FIELD_NUMBER: _ClassVar[int]
    MICRO_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    WARMUP_RATIO_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    LOGGING_STEPS_FIELD_NUMBER: _ClassVar[int]
    EVALS_PER_EPOCH_FIELD_NUMBER: _ClassVar[int]
    SAVE_SAFETENSORS_FIELD_NUMBER: _ClassVar[int]
    TRAIN_ON_INPUTS_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    GRADIENT_CHECKPOINTING_FIELD_NUMBER: _ClassVar[int]
    LR_SCHEDULER_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZER_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_DECAY_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    XFORMERS_ATTENTION_FIELD_NUMBER: _ClassVar[int]
    FLASH_ATTENTION_FIELD_NUMBER: _ClassVar[int]
    base_model: str
    model_type: str
    tokenizer_type: str
    trust_remote_code: bool
    tokenizer_use_fast: bool
    tokenizer_legacy: bool
    gptq: bool
    load_in_8bit: bool
    load_in_4bit: bool
    bf16: str
    fp16: bool
    tf32: bool
    datasets: _containers.RepeatedCompositeFieldContainer[DatasetConfig]
    shuffle_merged_datasets: bool
    dataset_prepared_path: str
    val_set_size: float
    sequence_len: int
    pad_to_sequence_len: bool
    sample_packing: bool
    eval_sample_packing: bool
    adapter: str
    lora_model_dir: str
    lora_r: int
    lora_alpha: int
    lora_dropout: float
    lora_target_modules: _containers.RepeatedScalarFieldContainer[str]
    lora_target_linear: bool
    mlflow_tracking_uri: str
    mlflow_experiment_name: str
    hf_mlflow_log_artifacts: bool
    output_dir: str
    gradient_accumulation_steps: int
    micro_batch_size: int
    num_epochs: int
    warmup_ratio: float
    learning_rate: float
    logging_steps: int
    evals_per_epoch: int
    save_safetensors: bool
    train_on_inputs: bool
    group_by_length: bool
    gradient_checkpointing: bool
    lr_scheduler: str
    optimizer: str
    weight_decay: float
    strict: bool
    xformers_attention: bool
    flash_attention: bool

    def __init__(self,
                 base_model: _Optional[str] = ...,
                 model_type: _Optional[str] = ...,
                 tokenizer_type: _Optional[str] = ...,
                 trust_remote_code: bool = ...,
                 tokenizer_use_fast: bool = ...,
                 tokenizer_legacy: bool = ...,
                 gptq: bool = ...,
                 load_in_8bit: bool = ...,
                 load_in_4bit: bool = ...,
                 bf16: _Optional[str] = ...,
                 fp16: bool = ...,
                 tf32: bool = ...,
                 datasets: _Optional[_Iterable[_Union[DatasetConfig,
                                                      _Mapping]]] = ...,
                 shuffle_merged_datasets: bool = ...,
                 dataset_prepared_path: _Optional[str] = ...,
                 val_set_size: _Optional[float] = ...,
                 sequence_len: _Optional[int] = ...,
                 pad_to_sequence_len: bool = ...,
                 sample_packing: bool = ...,
                 eval_sample_packing: bool = ...,
                 adapter: _Optional[str] = ...,
                 lora_model_dir: _Optional[str] = ...,
                 lora_r: _Optional[int] = ...,
                 lora_alpha: _Optional[int] = ...,
                 lora_dropout: _Optional[float] = ...,
                 lora_target_modules: _Optional[_Iterable[str]] = ...,
                 lora_target_linear: bool = ...,
                 mlflow_tracking_uri: _Optional[str] = ...,
                 mlflow_experiment_name: _Optional[str] = ...,
                 hf_mlflow_log_artifacts: bool = ...,
                 output_dir: _Optional[str] = ...,
                 gradient_accumulation_steps: _Optional[int] = ...,
                 micro_batch_size: _Optional[int] = ...,
                 num_epochs: _Optional[int] = ...,
                 warmup_ratio: _Optional[float] = ...,
                 learning_rate: _Optional[float] = ...,
                 logging_steps: _Optional[int] = ...,
                 evals_per_epoch: _Optional[int] = ...,
                 save_safetensors: bool = ...,
                 train_on_inputs: bool = ...,
                 group_by_length: bool = ...,
                 gradient_checkpointing: bool = ...,
                 lr_scheduler: _Optional[str] = ...,
                 optimizer: _Optional[str] = ...,
                 weight_decay: _Optional[float] = ...,
                 strict: bool = ...,
                 xformers_attention: bool = ...,
                 flash_attention: bool = ...) -> None: ...


class ListOfString(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...


class DatasetConfig(_message.Message):
    __slots__ = ("path", "type", "train_on_split")
    PATH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAIN_ON_SPLIT_FIELD_NUMBER: _ClassVar[int]
    path: str
    type: str
    train_on_split: str

    def __init__(self, path: _Optional[str] = ..., type: _Optional[str]
                 = ..., train_on_split: _Optional[str] = ...) -> None: ...
