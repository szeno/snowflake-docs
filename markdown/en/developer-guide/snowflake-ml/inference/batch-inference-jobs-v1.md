# Batch inference jobs (snowflake-ml-python 1.x, deprecated)

Important

This page documents how `ModelVersion.run_batch` works in `snowflake-ml-python` 1.x (version 1.39.0
or later). This 1.x `run_batch` API is deprecated and will no longer be supported. The method still
exists in version 2.0.0 and later, but the API has changed. Snowflake recommends upgrading to
version 2.0.0 or later. For the current API, see
[Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs).

Use Snowflake Batch Inference to enable efficient, large-scale model inference on static or periodically updated datasets. The Batch Inference API uses Snowpark Container Services (SPCS) to provide a distributed compute layer optimized for massive throughput and cost-efficiency.

If the model depends on packages from a private PyPI repository, set `artifact_repository_map` when you log the
model. Snowflake installs those packages when it builds the inference image. You don’t pass the repository to
`run_batch`. For an explanation and example, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).

To run batch inference directly in SQL, use [EXECUTE INFERENCE JOB SERVICE](/sql-reference/sql/execute-inference-job-service).

## When to use batch inference

Use the `run_batch` method for workloads to:

- Process images, audio, or video files using multimodal models with unstructured data.
- Execute inference over millions or billions of rows.
- Run inference as a discrete, asynchronous stage in a pipeline.
- Integrate inference as a step within an Airflow DAG or Snowflake Task.

## Limitations

- For multi-modal use cases, encryption is only supported on the server side.

## Get started

### Connect to Model Registry

Connect to the Snowflake Model Registry and retrieve the model reference as:

Copy code

```
from snowflake.ml.registry import Registry

registry = Registry(session=session, database_name=DATABASE, schema_name=REGISTRY_SCHEMA)
mv = registry.get_model('my_model').version('my_version')  # returns ModelVersion
```

### Execute batch job

This API uses a Snowpark Container Services (SPCS) job to launch the inference workload. After running inference, the compute automatically winds down to prevent you from incurring additional charges. At a high level, this API looks like the following:

Copy code

```
from snowflake.ml.model.batch import OutputSpec

# how to run a batch job
job = mv.run_batch(
    compute_pool = "my_compute_pool",
    X = session.table("my_table"),
    output_spec = OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
)

job.wait() # Optional: Blocking until the job finishes
```

### Job management

You can get a list of jobs, cancel a job, get a job’s handle, or delete a job using the methods below:

Copy code

```
from snowflake.ml.jobs import list_jobs, delete_job, get_job

# view logs to troubleshoot
job.get_logs()

# cancel a job
job.cancel()

# list to see all jobs
list_jobs().show()

# get the handle of a job
job = get_job("my_db.my_schema.job_name")

# delete a job that you no longer wish to run
delete_job(job)
```

Note

The `result` function in the ML Job APIs is not supported for batch inference jobs.

## Specify inference data

You can use structured data or unstructured data for batch inference. To use structured data for your workflow, you can either provide a SQL query or a dataframe to the run\_batch method.

For unstructured data, you can reference your files from a Snowflake stage. To reference your files, create a dataframe with the file paths.

You provide your dataframe to the `run_batch` method, which provides the content of the files to the model.

### Structured input

The following are examples illustrating the range of input possibilities:

Copy code

```
# providing input from a query
X = session.sql("SELECT id, feature_1, feature_2 FROM feature_table WHERE feature_1 > 100"),

# reading from parquet files
X = session.read.option("pattern",".*file.*\\.parquet")
    .parquet("@DB.SCHEMA.STAGE/some/path")
    .select(col("id1").alias("id"), col("feature_1"), col("feature_2"))).filter(col("feature_1") > 100)
```

### Unstructured input (multi-modal)

For unstructured data, the `run_batch` method can read the files from the fully qualified stage paths provided in the input dataframe. The following example shows you how to specify unstructured input data:

Copy code

```
# Process a list of files
# The file paths have to be in the form of a full stage path as below
data = [
    ["@DB.SCHEMA.STAGE/dataset/files/file1"],
    ["@DB.SCHEMA.STAGE/dataset/files/file2"],
    ["@DB.SCHEMA.STAGE/dataset/files/file3"],
]
column_names = ["image"]
X = session.create_dataframe(data, schema=column_names)
```

To automatically list all files in a stage as dataframe, use code like the following:

Copy code

```
from snowflake.ml.utils.stage_file import list_stage_files

# get all files under a path
X = list_stage_files(session, "@db.schema.my_stage/path")

# get all files under a path ending with ".jpg"
X = list_stage_files(session, "@db.schema.my_stage/path", pattern=".*\\.jpg")

# get all files under a path ending with ".jpg" and return the dataframe with a column_name "IMAGES"
X = list_stage_files(session, "@db.schema.my_stage/path", pattern=".*\\.jpg", column_name="IMAGES")
```

### Stage support

Supported configurations for input:

- **Internal stages**: all types of internal stages are supported.
- **External stages**: Amazon S3 only, must use server-side encryption. Azure Blob Storage and Google Cloud Storage are not supported.

Input rows can reference different stages in the same DataFrame, mixing external and internal paths. Each path is resolved independently at read time.

External stages require a one-time admin setup (S3 storage integration and IAM permissions on the bucket). For details, see [CREATE STAGE](/sql-reference/sql/create-stage#external-stage-parameters) and [Bulk loading from Amazon S3](/user-guide/data-load-s3). The role running the batch inference job must have `USAGE` on the external stage.

The output stage specified by `OutputSpec(stage_location=...)` must be an **internal** stage.

### Expressing type of data

`run_batch` automatically converts your files to model-compatible formats.

Your model can accept data in one of the following formats:

- RAW\_BYTES
- BASE64

For example, if you have images stored in PNG format in your stage and your model accepts RAW\_BYTES, you can use the `input_spec` argument to specify how Snowflake converts your data.

The following example code converts files in your stage to RAW\_BYTES:

Copy code

```
mv.run_batch(
    X,
    input_spec=InputSpec(
 # we need to provide column_handling in the InputSpec to perform the necessary conversion
 # FULL_STAGE_PATH: fully qualified path (@db.schema.stage/path) to a file
 # RAW_BYTES: download and convert the file from the stage path to bytes
        column_handling={
            "path": {"input_format": InputFormat.FULL_STAGE_PATH, "convert_to": FileEncoding.RAW_BYTES}
        }
    ),
    ...
)
```

The `column_handling` argument tells the framework that the path column of X contains a full stage path, and calls the model with raw bytes from that file.

### Output (`output_spec`)

Specify a stage directory to store the file output, as shown here:

Copy code

```
mv.run_batch(
    ...
    output_spec = OutputSpec(stage_location="@db.schema.stage/path/"),
)
```

Snowflake currently supports models that output text and store them as parquet files. You can convert the parquet files to a Snowpark data frame as follows:

Copy code

```
session.read.option("pattern", ".*\\.parquet").parquet("@db.schema.stage/output_path/")
```

### Passing parameters

If the model’s signature includes parameters defined with
[ParamSpec](/developer-guide/snowflake-ml/model-registry/model-signature), you can pass parameter values at
inference time using the `params` argument in `InputSpec`. Any parameter not included in the dictionary uses its
default value from the signature.

Copy code

```
from snowflake.ml.model.batch import InputSpec, OutputSpec

mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    input_spec=InputSpec(
        params={"temperature": 0.9, "max_tokens": 512}
    ),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
)
```

### Partitioned models

Note

This feature requires `snowflake-ml-python` version 1.33.0 or later.

You can run batch inference jobs with partitioned models by passing the `partition_column`
argument in `InputSpec`. Each partition is processed independently, which is useful for
models that train or predict per group.

Copy code

```
from snowflake.ml.model.batch import InputSpec, OutputSpec

job = model_version.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    input_spec=InputSpec(partition_column="STORE_NUMBER"),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/results/"),
)
```

For more information about partitioned models, see
[Partitioned models](/developer-guide/snowflake-ml/model-registry/partitioned-models).

## Job specification

To configure job-level settings for your batch inference workload (such as the number of workers, resource allocation, and execution parameters),
pass a `JobSpec` instance as the `job_spec` argument of the `run_batch` method. An example is shown below:

Copy code

```
from snowflake.ml.model.batch import JobSpec, OutputSpec

job_spec = JobSpec(
    job_name="my_inference_job",
    cpu_requests="2",
    memory_requests="8GiB",
    max_batch_rows=2048,
    replicas=2,
)

job = mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
    job_spec=job_spec,
)
```

## Best practices

### Using a sentinel file

A job can fail midway for various reasons. The output directory can therefore end up having partial data. To mark completion of the job, run\_batch writes a completion file \_SUCCESS in the output directory.

To avoid having partial or incorrect output:

- Read output data only after the sentinel file is found.
- Provide an empty directory to begin with.
- Run run\_batch with mode = SaveMode.ERROR.

## Run batch inference in a Snowflake task DAG

Note

This feature requires the `snowflake.core` package.

Use `BatchInferenceTask` to run a batch inference job inside a [Snowflake task DAG](/developer-guide/snowpark/python/managing-tasks-with-python-api). This is useful for scheduled or recurring batch inference, multi-step DAGs that include batch inference, and downstream tasks that read the inference output.

Construct `BatchInferenceTask` inside a `with DAG(...)` block (or pass `dag=` explicitly) and chain it with other tasks using `>>`. Each scheduled run submits a new SPCS batch inference job and writes results to a per-run output subdirectory.

Copy code

```
from datetime import timedelta
from snowflake.core import Root
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask
from snowflake.ml.model.batch import BatchInferenceTask, JobSpec, OutputSpec

api_root = Root(session)
schema_ref = api_root.databases["my_db"].schemas["my_schema"]

dag = DAG(
    "my_inference_dag",
    schedule=timedelta(days=1),
    stage_location="@my_db.my_schema.my_stage",  # DAG metadata stage
)

with dag:
    data_prep = DAGTask("data_preparation", definition="<PREP_SQL>")
    batch_inf = BatchInferenceTask(
        "batch_inference",
        model_version=mv,
        X=input_df,
        compute_pool="my_compute_pool",
        output_spec=OutputSpec(
            base_stage_location="@my_db.my_schema.my_stage/",
        ),
        job_spec=JobSpec(function_name="predict"),
    )
    post = DAGTask("post_process", definition="<POST_SQL>")
    data_prep >> batch_inf >> post

DAGOperation(schema_ref).deploy(dag)
DAGOperation(schema_ref).run(dag)
```

When you use `base_stage_location` in `OutputSpec`, each run writes to its own subdirectory under the base path (default form `BATCH_INFERENCE_<UUID>/`), so repeated runs don’t clobber each other.

A successor task can read the predecessor batch inference task’s output directory using `SYSTEM$GET_PREDECESSOR_RETURN_VALUE()`:

Copy code

```
SELECT PARSE_JSON(SYSTEM$GET_PREDECESSOR_RETURN_VALUE()):output_stage_location::VARCHAR
```

For more information about Snowflake tasks, see [Introduction to tasks](/user-guide/tasks-intro).

## Examples

### Using a custom model

Copy code

```
from transformers import pipeline
from snowflake.ml.model import custom_model
from snowflake.ml.model import target_platform
from snowflake.ml.model.batch import InputSpec, OutputSpec, FileEncoding, InputFormat
from snowflake.ml.model.model_signature import core

# first we must define the schema, we'll expect audio file input as base64 string
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

# defining the custom model, we decode the input from base64 to bytes and
# use whisper to perform the transcription
class CustomTranscriber(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)
        self.model = self.context.model_ref("my_model")

    @custom_model.inference_api
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        import base64
        audio_b64_list = df["audio"].tolist()
        audio_bytes_list = [base64.b64decode(audio_b64) for audio_b64 in audio_b64_list]
        temp_res = [self.model(audio_bytes) for audio_bytes in audio_bytes_list]
        return pd.DataFrame({"outputs": temp_res})

# creating an instance of our transcriber for logging
transcriber = CustomTranscriber(
    custom_model.ModelContext(
        models={
            "my_model": pipeline(
                task="automatic-speech-recognition", model="openai/whisper-small"
            )
        }
    )
)

# log the model
mv = reg.log_model(
    transcriber,
    model_name="custom_transcriber",
    version_name="v1",
    signatures={"predict": signature},
)

# input dataframe
data = [
    ["@DB.SCHEMA.STAGE/dataset/audio/audio1.mp3"],
    ["@DB.SCHEMA.STAGE/dataset/audio/audio2.mp3"],
    ["@DB.SCHEMA.STAGE/dataset/audio/audio3.mp3"],
]
column_names = ["audio"] # This column was defined in the signature above
input_df = session.create_dataframe(data, schema=column_names)

job = mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
    input_spec=InputSpec(
# we need to provide column_handling in the InputSpec to perform the necessary conversion
# FULL_STAGE_PATH: fully qualified path (db.schema.stage/path) to a file
# BASE64: download and convert the file from the stage path to base64 string
        column_handling={
            "audio": {"input_format": InputFormat.FULL_STAGE_PATH, "convert_to": FileEncoding.BASE64}
        }
    )
)
```

### Using Hugging Face Model

Copy code

```
from transformers import pipeline
from snowflake.ml.model import target_platform
from snowflake.ml.model.batch import InputSpec, OutputSpec, FileEncoding, InputFormat

# supported Hugging Face tasks will have their signatures auto-inferred
classifier = pipeline(task="image-classification", model="google/vit-base-patch16-224")

# log the model
mv = reg.log_model(
    classifier,
    model_name="image_classifier",
    version_name="v1",
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
    pip_requirements=[
        "pillow" # dependency for image classification
    ],
    # To install pip packages from a private index, add:
    # artifact_repository_map={"pip": "my_db.my_schema.my_python_repo"},
)

# input dataframe
data = [
    ["@DB.SCHEMA.STAGE/dataset/image/image1.jpg"],
    ["@DB.SCHEMA.STAGE/dataset/image/image2.jpg"],
    ["@DB.SCHEMA.STAGE/dataset/image/image3.jpg"],
]
# this column was defined in the auto-inferred signature
# you can view the signature by calling 'mv.show_functions()'
column_names = ["images"]
input_df = session.create_dataframe(data, schema=column_names)

mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location=f"@my_db.my_schema.my_stage/path/"),
    input_spec=InputSpec(
# we need to provide column_handling in the InputSpec to perform the necessary conversion
# FULL_STAGE_PATH: fully qualified path (db.schema.stage/path) to a file
# RAW_BYTES: download and convert the file to bytes (matching the predefined signature)
        column_handling={
            "IMAGES": {"input_format": InputFormat.FULL_STAGE_PATH, "convert_to": FileEncoding.RAW_BYTES}
        }
    )
)
```

### Using Hugging Face Model with vLLM

#### Task: text generation

Copy code

```
import json

from snowflake.ml.model import target_platform
from snowflake.ml.model.batch import InputSpec, OutputSpec, FileEncoding, InputFormat

# it's a large model so we remotely log it
model = huggingface.TransformersPipeline(model="Qwen/Qwen2.5-0.5B-Instruct", task="text-generation")

mv = reg.log_model(
    model,
    model_name="qwenw_5",
    version_name="v1",
    options={"cuda_version": "12.4"},
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
)

# constructing OpenAI chat/completions API compatible messages
messages = [[
    {"role": "system", "content": [{"type": "text", "text": "You are an expert on cats and kitchens."}]},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "How many breeds of cats are there?"},
        ]
    }
]]
schema = ["messages"]
data = [(json.dumps(m)) for m in messages]
input_df = session.create_dataframe(data, schema=schema)

mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
    inference_engine_options={
 # set vLLM as the inference backend
        "engine": InferenceEngine.VLLM,
    },
)
```

#### Task: image text to text

Copy code

```
import json

from snowflake.ml.model import target_platform
from snowflake.ml.model.batch import InputSpec, OutputSpec

# it's a large model so we remotely log it
model = huggingface.TransformersPipeline(model="Qwen/Qwen2-VL-2B-Instruct", task="image-text-to-text")

mv = reg.log_model(
    model,
    model_name="qwen2_vl_2b",
    version_name="v1",
    options={"cuda_version": "12.4"},
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
)

# constructing OpenAI chat/completions API compatible messages
messages = [[
    {"role": "system", "content": [{"type": "text", "text": "You are an expert on cats and kitchens."}]},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What breed of cat is this?"},
            {
                "type": "image_url",
                "image_url": {
                    # run_batch will download and convert the file to the format that vLLM can handle
                    "url": f"@db.schema.stage/path/cat.jpeg",
                }
            }
     # you can also pass video and audio like below
            # {
            #     "type": "video_url",
            #     "video_url": {
            #         "url": "@db.schema.stage/path/video.avi",
            #     }
            # }
            # {
            #     "type": "input_audio",
            #     "input_audio": {
            #         "data": "@db.schema.stage/path/audio.mp3",
            #         "format": "mp3",
            #     }
            # }
        ]
    }
]]

schema = ["messages"]
data = [(json.dumps(m)) for m in messages]
input_df = session.create_dataframe(data, schema=schema)

mv.run_batch(
    X=input_df,
    compute_pool="my_compute_pool",
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
    inference_engine_options={
 # set vLLM as the inference backend
        "engine": InferenceEngine.VLLM,
    },
)
```

### Sample notebooks

For end-to-end runnable examples, see the
[batch inference sample notebooks](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/ml/model_serving/batch_inference)
on GitHub.

## Troubleshooting

### Get metrics

To get metrics for a batch inference job, use one of the following approaches depending on whether the job still exists.

**If the job hasn’t been deleted**, use the [SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics) function, which returns container metrics for the job’s underlying SPCS service:

Copy code

```
SELECT * FROM TABLE(<DB>.<SCHEMA>.<JOB_NAME>!SPCS_GET_METRICS());
```

**If the job has been deleted**, query your event table directly. The event table retains historical metrics even after the service is dropped:

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

Replace `<JOB_NAME>` with the job name specified in `JobSpec`, or the auto-generated name if you didn’t specify one.
