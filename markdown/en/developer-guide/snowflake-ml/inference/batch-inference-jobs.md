# Batch inference jobs

Note

Batch inference jobs require `snowflake-ml-python` version 2.0.0 or later. If you’re using
`snowflake-ml-python` 1.x, see
[Batch inference jobs (snowflake-ml-python 1.x, deprecated)](/developer-guide/snowflake-ml/inference/batch-inference-jobs-v1).

Use Snowflake batch inference to run efficient, large-scale model inference on static or
periodically updated datasets. The batch inference API runs on Snowpark Container Services (SPCS),
which provides a distributed compute layer optimized for throughput and cost efficiency.

You start a batch inference job by calling `ModelVersion.run_batch` on a model version in the
[Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview). The job builds an
inference image, provisions an SPCS job on the compute pool you name, runs inference, writes results
to a stage, and then winds the compute down so you don’t keep paying for idle capacity.

If the model depends on packages from a private PyPI repository, set `artifact_repository_map` when
you log the model. Snowflake installs those packages when it builds the inference image. You don’t
pass the repository to `run_batch`. For an explanation and example, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).

To run batch inference directly in SQL, use [EXECUTE INFERENCE JOB SERVICE](/sql-reference/sql/execute-inference-job-service).

## When to use batch inference

Use the `run_batch` method for workloads that:

- Process images, audio, or video files using multimodal models with unstructured data.
- Execute inference over millions or billions of rows.
- Run inference as a discrete, asynchronous stage in a pipeline.
- Integrate inference as a step within an Airflow DAG or a Snowflake task.

## Limitations

- The output stage must be a Snowflake internal stage.
- For multimodal use cases, only server-side encryption is supported.
- `partition_column` isn’t supported for Hugging Face pipeline models or for FUNCTION-type model
  methods.

## Get started

### Connect to the model registry

Connect to the Snowflake Model Registry and get a reference to the model version you want to run:

Copy code

```
from snowflake.ml.registry import Registry

registry = Registry(session=session, database_name="MY_DB", schema_name="MY_REGISTRY_SCHEMA")
mv = registry.get_model("my_model").version("my_version")  # returns a ModelVersion
```

### Run a batch inference job

Pass the input rows, a compute pool, and an output location. The call returns an `MLJob` handle:

Copy code

```
from snowflake.ml.model.batch_inference import OutputSpec, SaveMode

input_df = session.table("my_db.my_schema.my_input_table")

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(
        stage_location="@my_db.my_schema.my_stage/predictions/",
        mode=SaveMode.ERROR,
    ),
)

job.wait()  # optional: block until the job finishes
```

By default `run_batch` submits the job asynchronously (`async_=True`) and returns right away. Pass
`async_=False` if you’d rather have the call block until the job finishes.

### Job management

Use the ML Job APIs to list, inspect, cancel, and delete batch inference jobs:

Copy code

```
from snowflake.ml.jobs import delete_job, get_job, list_jobs

# view logs to troubleshoot
print(job.get_logs())

# cancel a running job
job.cancel()

# list all jobs
list_jobs().show()

# get the handle of an existing job
job = get_job("my_db.my_schema.my_job_name")

# delete a job you no longer need
delete_job(job)
```

Note

The `result` function in the ML Job APIs isn’t supported for batch inference jobs. Read the job’s
output from the output stage instead.

## Specify inference data

Provide exactly one of the following:

- `X`: a Snowpark DataFrame holding the input rows.
- `input_stage_location`: a stage path that already holds the input data.

Passing both, or neither, raises a `ValueError`.

### DataFrame input

When you pass `X`, Snowflake materializes the rows as Parquet files in a reserved subdirectory of
`output_spec.stage_location` before the job starts, then reads them from there.

Copy code

```
# from a table
X = session.table("my_db.my_schema.feature_table")

# from a query
X = session.sql(
    "SELECT id, feature_1, feature_2 FROM my_db.my_schema.feature_table WHERE feature_1 > 100"
)

# from Parquet files already in a stage
from snowflake.snowpark.functions import col

X = (
    session.read.option("pattern", ".*file.*\\.parquet")
    .parquet("@my_db.my_schema.my_stage/some/path")
    .select(col("id1").alias("id"), col("feature_1"), col("feature_2"))
    .filter(col("feature_1") > 100)
)
```

### Stage input

If your input is already staged as Parquet, point `input_stage_location` at it. Snowflake reads
those files in place and doesn’t copy them:

Copy code

```
from snowflake.ml.model.batch_inference import OutputSpec

job = mv.run_batch(
    input_stage_location="@my_db.my_schema.input_stage/batch_01/",
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/predictions/"),
)
```

Important

`input_stage_location` must not sit inside `output_spec.stage_location`. Keep the input and output
paths separate so the job doesn’t read its own output.

### Unstructured input (multimodal)

For unstructured data, reference the files by their fully qualified stage paths in the input
DataFrame. The job reads each file and passes its content to the model:

Copy code

```
# the file paths must be full stage paths, as shown here
data = [
    ["@my_db.my_schema.my_stage/dataset/files/file1"],
    ["@my_db.my_schema.my_stage/dataset/files/file2"],
    ["@my_db.my_schema.my_stage/dataset/files/file3"],
]
X = session.create_dataframe(data, schema=["image"])
```

To list all files under a stage path as a DataFrame, use `list_stage_files`:

Copy code

```
from snowflake.ml.utils.stage_file import list_stage_files

# all files under a path
X = list_stage_files(session, "@my_db.my_schema.my_stage/path")

# only files ending with ".jpg"
X = list_stage_files(session, "@my_db.my_schema.my_stage/path", pattern=".*\\.jpg")

# same, but name the resulting column "IMAGES"
X = list_stage_files(
    session, "@my_db.my_schema.my_stage/path", pattern=".*\\.jpg", column_name="IMAGES"
)
```

### Stage support

Supported configurations for input:

- **Internal stages**: all types of internal stages are supported.
- **External stages**: Amazon S3 only, and the stage must use server-side encryption. Azure Blob
  Storage and Google Cloud Storage aren’t supported.

Input rows can reference different stages in the same DataFrame, mixing external and internal paths.
Each path is resolved independently at read time.

External stages require a one-time admin setup: an S3 storage integration and IAM permissions on the
bucket. For details, see
[CREATE STAGE](/sql-reference/sql/create-stage#external-stage-parameters) and
[Bulk loading from Amazon S3](/user-guide/data-load-s3). The role running the batch inference job
must have `USAGE` on the external stage.

The output stage specified by `OutputSpec(stage_location=...)` must be an internal stage.

### Convert files to a model-compatible format

Your model can accept file content in one of the following encodings:

- `FileEncoding.RAW_BYTES`
- `FileEncoding.BASE64`
- `FileEncoding.BASE64_DATA_URL`

Use the `column_handling` field of `InputSpec` to tell the job which columns hold stage paths and
what encoding the model expects. Each entry is a `ColumnHandlingOptions` mapping with an
`input_format` and a `convert_to` value.

Copy code

```
from snowflake.ml.model.batch_inference import (
    ColumnHandlingOptions,
    FileEncoding,
    InputFormat,
    InputSpec,
    OutputSpec,
)

job = mv.run_batch(
    X,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/predictions/"),
    input_spec=InputSpec(
        # FULL_STAGE_PATH: the column holds a fully qualified path (@db.schema.stage/path) to a file
        # RAW_BYTES: download the file and hand its bytes to the model
        column_handling={
            "path": ColumnHandlingOptions(
                input_format=InputFormat.FULL_STAGE_PATH,
                convert_to=FileEncoding.RAW_BYTES,
            )
        }
    ),
)
```

## Output

`OutputSpec.stage_location` is a base path, not the final directory. Each job writes its results to
a per-job subdirectory named for the unqualified job name:

```
<stage_location>/<job_name>/
```

The unqualified job name is the trailing identifier of the fully qualified `job.id`, so you can
build the output path from the job handle:

Copy code

```
from snowflake.ml.model.batch_inference import OutputSpec, SaveMode

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(
        stage_location="@my_db.my_schema.my_stage/predictions/",
        mode=SaveMode.ERROR,
    ),
)
job.wait()

job_name = job.id.split(".")[-1].strip('"')
output_location = f"@my_db.my_schema.my_stage/predictions/{job_name}/"

results = session.read.option("pattern", ".*\\.parquet").parquet(output_location)
results.show()
```

Results are written as Parquet files. Set `job_name` on `run_batch` if you want a predictable output
directory instead of a server-generated one.

### Save mode

`OutputSpec.mode` controls what happens when files already exist at the output location:

| Value | Behavior |
| --- | --- |
| `SaveMode.ERROR` | Fail if the output directory already contains files. This is the default. |
| `SaveMode.OVERWRITE` | Replace any existing files at the output directory. |

Expand

Show lessSee more

## Pass model parameters

If the model’s signature includes parameters defined with
[ParamSpec](/developer-guide/snowflake-ml/model-registry/model-signature), pass values at inference
time through `InputSpec.params`. Any parameter you leave out uses its default from the signature.

Copy code

```
from snowflake.ml.model.batch_inference import InputSpec, OutputSpec

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    input_spec=InputSpec(params={"temperature": 0.9, "max_tokens": 512}),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/predictions/"),
)
```

## Partitioned models

Run batch inference on a partitioned model by setting `InputSpec.partition_column`. Each partition
is processed independently, which is useful for models that train or predict per group.

Copy code

```
from snowflake.ml.model.batch_inference import InputSpec, OutputSpec

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    input_spec=InputSpec(partition_column="STORE_NUMBER"),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/results/"),
)
```

`run_batch` raises a `ValueError` if you set `partition_column` for a Hugging Face pipeline model or
a FUNCTION-type method, or if the partition column collides with a column in the partitioned model’s
output signature.

For more information about partitioned models, see
[Partitioned models](/developer-guide/snowflake-ml/model-registry/partitioned-models).

## Configure the job

Job settings are split into three optional blocks that you pass to `run_batch`.

### Resources

`ResourcesSpec` sets the per-node compute limits for the inference containers:

| Field | Description |
| --- | --- |
| `cpu_requests` | CPU limit for CPU-based inference. Accepts an integer, a fraction, or a string. If omitted, the job tries to use all vCPUs on the node. |
| `memory_requests` | Memory limit. Accepts an integer or a fraction, but requires a unit such as `GiB` or `MiB`. If omitted, the job tries to use all memory on the node. |
| `gpu_requests` | GPU limit for GPU-based inference. Accepts an integer or a string. If omitted, the job runs on CPU. |

Expand

Show lessSee more

### Inference

`InferenceSpec` tunes how the model is served inside the job:

| Field | Description |
| --- | --- |
| `num_workers` | Number of workers that handle requests in parallel within one service instance. Determined automatically if omitted. |
| `max_batch_rows` | Maximum number of rows processed in a single batch. Determined automatically if omitted. Larger values can improve throughput. |
| `engine_options` | An `EngineOptions` instance that selects a custom inference engine. |

Expand

Show lessSee more

`EngineOptions` takes an `engine` value and an optional `engine_args_override` list of command-line
arguments for that engine. The `engine` value accepts an `InferenceEngine` enum member or a
case-insensitive string such as `"vllm"` or `"python_generic"`.

### Image build

`ImageBuildSpec` controls the container image build:

| Field | Description |
| --- | --- |
| `image_repo` | Image repository for the inference image. Uses a default repository if omitted. |
| `force_rebuild` | Whether to rebuild the image even if a matching one already exists. Defaults to `False`. |

Expand

Show lessSee more

### Putting the blocks together

Copy code

```
from snowflake.ml.model.batch_inference import (
    EngineOptions,
    ImageBuildSpec,
    InferenceSpec,
    InputSpec,
    OutputSpec,
    ResourcesSpec,
    SaveMode,
)
from snowflake.ml.model.inference_engine import InferenceEngine

job = mv.run_batch(
    input_df,
    compute_pool="my_gpu_pool",
    output_spec=OutputSpec(
        stage_location="@my_db.my_schema.my_stage/predictions/",
        mode=SaveMode.OVERWRITE,
    ),
    input_spec=InputSpec(params={"temperature": 0.7, "top_k": 50}),
    resources_spec=ResourcesSpec(cpu_requests="2", memory_requests="8GiB", gpu_requests="1"),
    inference_spec=InferenceSpec(
        num_workers=4,
        max_batch_rows=2048,
        engine_options=EngineOptions(engine=InferenceEngine.VLLM),
    ),
    image_build_spec=ImageBuildSpec(image_repo="my_db.my_schema.my_image_repo"),
    function_name="predict",
    job_name="my_db.my_schema.my_inference_job",
    replicas=2,
)
```

`function_name` selects the model function to call. If you omit it, Snowflake resolves it against
the model’s function list. Use `mv.show_functions()` to see the available functions.

## Best practices

### Use the sentinel file

A job can fail midway for many reasons, which can leave partial data in the output directory. To
mark completion, the job writes a `_SUCCESS` file to the output directory.

To avoid reading partial or incorrect output:

- Read output data only after the `_SUCCESS` file appears.
- Start from an empty output directory.
- Use `OutputSpec(mode=SaveMode.ERROR)` so the job fails instead of silently overwriting data.

### Other recommendations

- Keep `input_stage_location` outside the output base path.
- Use a fully qualified `job_name` when a downstream step needs to know the output path in advance.
- Set `force_rebuild=True` only when you need it. Reusing a cached image makes jobs start faster.

## Run batch inference in a Snowflake task DAG

Note

This feature requires the `snowflake.core` package.

Use `BatchInferenceTask` to run a batch inference job inside a
[Snowflake task DAG](/developer-guide/snowpark/python/managing-tasks-with-python-api). This is
useful for scheduled or recurring batch inference, for multi-step DAGs that include inference, and
for downstream tasks that read the inference output.

Construct `BatchInferenceTask` inside a `with DAG(...)` block, or pass `dag=` explicitly, and chain
it with other tasks using `>>`. The task differs from `run_batch` in a few ways:

- Supply the input with `query` or `input_stage_location`, exactly one of the two. The task doesn’t
  accept a DataFrame.
- The job runs synchronously, so the DAG step completes when the job does.
- The DAG must supply a warehouse, either through `DAG(warehouse=...)` or `warehouse=` on the task.
  Serverless DAGs aren’t supported.
- Each run gets a server-generated job name and writes results under
  `<output_spec.stage_location>/<job_name>/`, so repeated runs don’t overwrite each other.

Use fully qualified stage paths. An unqualified path resolves against the session namespace when the
task is built, but against the task owner’s namespace when it runs.

Copy code

```
from datetime import timedelta

from snowflake.core import Root
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask
from snowflake.ml.model.batch_inference import (
    BatchInferenceTask,
    InferenceSpec,
    OutputSpec,
    ResourcesSpec,
)

api_root = Root(session)
schema_ref = api_root.databases["my_db"].schemas["my_schema"]

dag = DAG(
    "my_inference_dag",
    schedule=timedelta(days=1),
    warehouse="my_warehouse",
    stage_location="@my_db.my_schema.my_stage",  # DAG metadata stage
)

with dag:
    data_prep = DAGTask("data_preparation", definition="<PREP_SQL>")
    batch_inference = BatchInferenceTask(
        "batch_inference",
        model_version=mv,
        compute_pool="my_compute_pool",
        query="SELECT id, feature_1, feature_2 FROM my_db.my_schema.feature_table",
        output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/predictions/"),
        resources_spec=ResourcesSpec(cpu_requests="2", memory_requests="8GiB"),
        inference_spec=InferenceSpec(max_batch_rows=2048),
        function_name="predict",
        replicas=2,
    )
    post_process = DAGTask("post_process", definition="<POST_SQL>")
    data_prep >> batch_inference >> post_process

DAGOperation(schema_ref).deploy(dag)
DAGOperation(schema_ref).run(dag)
```

The task publishes its output directory as the task return value, so a successor can read the path
instead of hardcoding it:

Copy code

```
SELECT PARSE_JSON(SYSTEM$GET_PREDECESSOR_RETURN_VALUE()):output_stage_location::VARCHAR;
```

For more information about Snowflake tasks, see [Introduction to tasks](/user-guide/tasks-intro).

## Examples

### Use a custom model

This example transcribes audio files from a stage with a custom model that wraps a Whisper pipeline.

Copy code

```
import base64

import pandas as pd
from transformers import pipeline

from snowflake.ml.model import custom_model
from snowflake.ml.model.batch_inference import (
    ColumnHandlingOptions,
    FileEncoding,
    InputFormat,
    InputSpec,
    OutputSpec,
)
from snowflake.ml.model.model_signature import core

# define the signature first: the model expects audio file content as a base64 string
signature = core.ModelSignature(
    inputs=[
        core.FeatureSpec(name="audio", dtype=core.DataType.STRING),
    ],
    outputs=[
        core.FeatureGroupSpec(
            name="outputs",
            specs=[
                core.FeatureSpec(name="text", dtype=core.DataType.STRING),
                core.FeatureGroupSpec(
                    name="chunks",
                    specs=[
                        core.FeatureSpec(
                            name="timestamp", dtype=core.DataType.DOUBLE, shape=(2,)
                        ),
                        core.FeatureSpec(name="text", dtype=core.DataType.STRING),
                    ],
                    shape=(-1,),
                ),
            ],
        ),
    ],
)

# the custom model decodes the base64 input to bytes and runs Whisper on it
class CustomTranscriber(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)
        self.model = self.context.model_ref("my_model")

    @custom_model.inference_api
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        audio_b64_list = df["audio"].tolist()
        audio_bytes_list = [base64.b64decode(audio_b64) for audio_b64 in audio_b64_list]
        transcriptions = [self.model(audio_bytes) for audio_bytes in audio_bytes_list]
        return pd.DataFrame({"outputs": transcriptions})

transcriber = CustomTranscriber(
    custom_model.ModelContext(
        models={
            "my_model": pipeline(
                task="automatic-speech-recognition", model="openai/whisper-small"
            )
        }
    )
)

mv = registry.log_model(
    transcriber,
    model_name="custom_transcriber",
    version_name="v1",
    signatures={"predict": signature},
)

# input rows: one fully qualified stage path per audio file
data = [
    ["@my_db.my_schema.my_stage/dataset/audio/audio1.mp3"],
    ["@my_db.my_schema.my_stage/dataset/audio/audio2.mp3"],
    ["@my_db.my_schema.my_stage/dataset/audio/audio3.mp3"],
]
input_df = session.create_dataframe(data, schema=["audio"])  # matches the signature above

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/transcriptions/"),
    input_spec=InputSpec(
        # FULL_STAGE_PATH: the column holds a fully qualified path to a file
        # BASE64: download the file and hand it to the model as a base64 string
        column_handling={
            "audio": ColumnHandlingOptions(
                input_format=InputFormat.FULL_STAGE_PATH,
                convert_to=FileEncoding.BASE64,
            )
        }
    ),
)
job.wait()
```

### Use a Hugging Face model

Supported Hugging Face tasks have their signatures inferred automatically.

Copy code

```
from transformers import pipeline

from snowflake.ml.model import target_platform
from snowflake.ml.model.batch_inference import (
    ColumnHandlingOptions,
    FileEncoding,
    InputFormat,
    InputSpec,
    OutputSpec,
)

classifier = pipeline(task="image-classification", model="google/vit-base-patch16-224")

mv = registry.log_model(
    classifier,
    model_name="image_classifier",
    version_name="v1",
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
    pip_requirements=[
        "pillow"  # dependency for image classification
    ],
    # to install pip packages from a private index, add:
    # artifact_repository_map={"pip": "my_db.my_schema.my_python_repo"},
)

data = [
    ["@my_db.my_schema.my_stage/dataset/image/image1.jpg"],
    ["@my_db.my_schema.my_stage/dataset/image/image2.jpg"],
    ["@my_db.my_schema.my_stage/dataset/image/image3.jpg"],
]
# this column name comes from the inferred signature; check it with mv.show_functions()
input_df = session.create_dataframe(data, schema=["images"])

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/classifications/"),
    input_spec=InputSpec(
        # RAW_BYTES matches the inferred signature for image classification
        column_handling={
            "IMAGES": ColumnHandlingOptions(
                input_format=InputFormat.FULL_STAGE_PATH,
                convert_to=FileEncoding.RAW_BYTES,
            )
        }
    ),
)
job.wait()
```

### Use a Hugging Face model with vLLM

Select vLLM through `InferenceSpec(engine_options=EngineOptions(engine=...))`.

#### Text generation

Copy code

```
import json

from snowflake.ml.model.models import huggingface
from snowflake.ml.model import target_platform
from snowflake.ml.model.batch_inference import EngineOptions, InferenceSpec, OutputSpec
from snowflake.ml.model.inference_engine import InferenceEngine

# this is a large model, so log it remotely rather than loading it locally
model = huggingface.TransformersPipeline(
    model="Qwen/Qwen2.5-0.5B-Instruct", task="text-generation"
)

mv = registry.log_model(
    model,
    model_name="qwen2_5",
    version_name="v1",
    options={"cuda_version": "12.4"},
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
)

# messages follow the OpenAI chat completions format
messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert on cats and kitchens."}],
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "How many breeds of cats are there?"}],
        },
    ]
]
input_df = session.create_dataframe([(json.dumps(m),) for m in messages], schema=["messages"])

job = mv.run_batch(
    input_df,
    compute_pool="my_gpu_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/generations/"),
    inference_spec=InferenceSpec(
        engine_options=EngineOptions(engine=InferenceEngine.VLLM),
    ),
)
job.wait()
```

#### Image text to text

Copy code

```
import json

from snowflake.ml.model.models import huggingface
from snowflake.ml.model import target_platform
from snowflake.ml.model.batch_inference import EngineOptions, InferenceSpec, OutputSpec
from snowflake.ml.model.inference_engine import InferenceEngine

model = huggingface.TransformersPipeline(
    model="Qwen/Qwen2-VL-2B-Instruct", task="image-text-to-text"
)

mv = registry.log_model(
    model,
    model_name="qwen2_vl_2b",
    version_name="v1",
    options={"cuda_version": "12.4"},
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
)

messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert on cats and kitchens."}],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What breed of cat is this?"},
                {
                    "type": "image_url",
                    # the job downloads the file and converts it to a format vLLM can handle
                    "image_url": {"url": "@my_db.my_schema.my_stage/path/cat.jpeg"},
                },
                # you can pass video and audio the same way:
                # {"type": "video_url",
                #  "video_url": {"url": "@my_db.my_schema.my_stage/path/video.avi"}},
                # {"type": "input_audio",
                #  "input_audio": {"data": "@my_db.my_schema.my_stage/path/audio.mp3",
                #                  "format": "mp3"}},
            ],
        },
    ]
]
input_df = session.create_dataframe([(json.dumps(m),) for m in messages], schema=["messages"])

job = mv.run_batch(
    input_df,
    compute_pool="my_gpu_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/vl_outputs/"),
    inference_spec=InferenceSpec(
        engine_options=EngineOptions(
            engine=InferenceEngine.VLLM,
            engine_args_override=["--max-model-len=4096"],
        ),
    ),
)
job.wait()
```

## Troubleshooting

### Get job logs

Copy code

```
print(job.get_logs())
```

### Get metrics

To get metrics for a batch inference job, use one of the following approaches, depending on whether
the job still exists.

If the job hasn’t been deleted, use the
[SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics) function, which returns container
metrics for the job’s underlying SPCS service:

Copy code

```
SELECT * FROM TABLE(<DB>.<SCHEMA>.<JOB_NAME>!SPCS_GET_METRICS());
```

If the job has been deleted, query your event table directly. The event table retains historical
metrics even after the service is dropped:

Copy code

```
SELECT RESOURCE_ATTRIBUTES, VALUE
FROM <EVENT_TABLE_NAME>
WHERE timestamp > DATEADD('day', -1, CURRENT_TIMESTAMP())
  AND RESOURCE_ATTRIBUTES:"snow.database.name" = '<DB>'
  AND RESOURCE_ATTRIBUTES:"snow.schema.name" = '<SCHEMA>'
  AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<JOB_NAME>'
  AND RESOURCE_ATTRIBUTES:"snow.service.container.instance" = '0'
  AND RESOURCE_ATTRIBUTES:"snow.service.container.name" != 'snowflake-ingress'
ORDER BY timestamp ASC;
```

Replace `<JOB_NAME>` with the `job_name` you passed to `run_batch`, or with the server-generated name
if you didn’t specify one. You can get the generated name from `job.id`.

### Common errors

| Symptom | Likely cause |
| --- | --- |
| `ValueError` about `X` and `input_stage_location` | You passed both or neither. Pass exactly one. |
| Job fails because output files already exist | The output directory isn’t empty and `mode` is `SaveMode.ERROR`. Use a new directory or `SaveMode.OVERWRITE`. |
| `ValueError` about `partition_column` | The model is a Hugging Face pipeline or a FUNCTION-type method, or the partition column collides with the model’s output signature. |
| Output looks truncated | The job may not have finished. Check for the `_SUCCESS` file before reading results. |

Expand

Show lessSee more
