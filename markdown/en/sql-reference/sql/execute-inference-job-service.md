# EXECUTE INFERENCE JOB SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Runs batch inference on a model in the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) as a Snowpark Container Services (SPCS) job. This command is the SQL equivalent of the `run_batch` method in the `snowflake-ml-python` API. For more information, see [Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs).

You provide a compute pool, a batch inference job specification, an input data source (a query or a stage), and the model to run. Snowflake runs inference over the input and writes the results to the output stage that you specify in the specification. When all containers exit, the job is done.

By default, the job runs asynchronously; the command returns while the job runs in the background. (If the model’s container image must be built first, the command waits for the image build to finish before returning.) You can use the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command to poll for job completion and then call the [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) function to wait for the job to complete. To run the job synchronously, so that the command finishes only after all containers exit, specify `ASYNC = FALSE`.

After a job service completes, Snowflake automatically cleans up the resources allocated to the job service to help reduce costs. You can still access job metadata for up to 30 days by using the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) and [SHOW SERVICES](/sql-reference/sql/show-services) commands. After 30 days, Snowflake automatically deletes the job.

Note that the command parameters must be specified in a specific order. For more information, see [Usage notes](#usage-notes).

See also:
:   [EXECUTE JOB SERVICE](/sql-reference/sql/execute-job-service) , [SYSTEM$GET\_SERVICE\_STATUS — Deprecated](/sql-reference/functions/system_get_service_status) , [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs)

## Syntax

Copy code

```
EXECUTE INFERENCE JOB SERVICE
  IN COMPUTE POOL <compute_pool_name>
  WITH SPECIFICATION <specification_text>
  FROM { ( <subquery> ) | @[<namespace>.]<stage_name>[/<path>] }
  MODEL = [<db>.<schema>.]<model_name>
  [ VERSION = <version_or_alias> ]
  [ FUNCTION = '<function_name>' ]
  [ NAME = [<db>.<schema>.]<name> ]
  [ ASYNC = { TRUE | FALSE } ]
  [ REPLICAS = <num> ]
```

## Required parameters

`IN COMPUTE POOL compute_pool_name`
:   Specifies the name of the compute pool in your account on which to run the inference job.

`WITH SPECIFICATION specification_text`
:   Specifies the batch inference job specification, as inline YAML. You can use a
    [pair of dollar signs](/sql-reference/data-types-text#label-dollar-quoted-string-constants) (`$$`) to delimit the beginning and ending of the
    specification string. For the fields you can set, see [Specification](#specification).

`FROM { ( subquery ) | @[namespace.]stage_name[/path] }`
:   Specifies the input data for inference, as one of the following:

    - A subquery that produces the input rows; for example, `( SELECT id, feature_1 FROM my_table )`.
    - A stage path that references the input files; for example, `@my_db.my_schema.my_stage/data/`. Use a stage
      path for file-based input.

`MODEL = [db.schema.]model_name`
:   Specifies the model in the Snowflake Model Registry to run inference with. If you omit the database and schema, Snowflake uses the current database and schema for the session.

## Optional parameters

`VERSION = version_or_alias`
:   Specifies the model version (or a version alias) to use.

    Default: The model’s default version.

`FUNCTION = 'function_name'`
:   Specifies the name of the model function (method) to invoke, for example `'predict'`. To list the functions
    available for a model version, run `SHOW FUNCTIONS IN MODEL <model_name> VERSION <version>`.

    Default: For a model that exposes a single function, that function.

`NAME = [db.schema.]name`
:   The name (that is, the identifier) for the service that executes like a job; it must be unique for the schema in
    which the service is created.

    Quoted names for special characters or case-sensitive names are not supported. The same constraint also applies to
    database and schema names where you create a service. That is, database and schema names without quotes are valid
    when creating a service.

    Default: If not specified, Snowflake generates a name for the service in the format
    `<db>.<schema>.BATCH_INFERENCE_<UUID>`.

`ASYNC = { TRUE | FALSE }`
:   Specifies whether to execute the job asynchronously. When `TRUE`, the command returns while the job runs (after
    waiting for the image build, if one is needed). When `FALSE`, the command finishes only after all containers exit.

    Default: TRUE

`REPLICAS = num`
:   Specifies the number of job replicas to run. For more information,
    see [Run multiple replicas of a job service (batch jobs)](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-batch-jobs).

    Default: 1.

## Specification

The specification is a YAML document that configures how the batch inference job runs and where it writes results. It
supports the following top-level sections. Only `output` is required.

`output`
:   Required. Configures where the job writes results.

    - `stage_location` (required): The base stage location for results. Snowflake writes each job’s output to a per-job
      subdirectory of this location, `<stage_location>/<job_name>/`, where `<job_name>` is the job’s unqualified name
      (from the `NAME` parameter, or auto-generated in the format `BATCH_INFERENCE_<UUID>` if you don’t specify one).
    - `mode`: What happens when the output location already contains files. `error` (the default) fails the job;
      `overwrite` removes the existing files first.

`resources`
:   Configures the compute resources requested for the job containers.

    - `cpu_requests`: The CPU limit for CPU-based inference, as an integer, fractional, or string value. If omitted, the
      job uses all of the node’s vCPUs.
    - `memory_requests`: The memory limit, as an integer or fractional value with a unit (for example, `8GiB` or
      `512MiB`). If omitted, the job uses all of the node’s memory.
    - `gpu_requests`: The GPU count for GPU-based inference, as an integer or string value. If omitted, the job runs on
      CPU.

`inference`
:   Tunes inference execution.

    - `num_workers`: The number of workers per service instance that process requests in parallel. Defaults to
      `2 * vCPU + 1` for CPU-based inference and `1` for GPU-based inference.
    - `max_batch_rows`: The maximum number of rows to process in a single batch. Auto-determined if omitted; larger
      values can improve throughput.
    - `engine_options`: Inference engine settings:
      - `engine`: The inference engine, one of `DEFAULT`, `VLLM`, or `PYTHON_GENERIC`.
      - `engine_args_override`: A list of engine arguments to override (for example, `--max-model-len=18048` for vLLM).

`input`
:   Configures how the input rows are processed.

    - `params`: A dictionary of model inference parameters (for example, `temperature` or `top_k` for LLMs). These are
      passed as keyword arguments to the model function.
    - `column_handling`: Maps an input column to file-handling options, so the model receives the file’s contents instead
      of the stage path string. For each column name, provide:
      - `input_format`: How to interpret the column value. Supported value: `full_stage_path` (the value is a full stage
        path to a file).
      - `convert_to`: The encoding in which the file contents are passed to the model, one of `raw_bytes`, `base64`, or
        `base64_data_url`.
    - `partition_column`: The name of a column to partition the input by. Each partition is processed independently, which
      is useful for [partitioned models](/developer-guide/snowflake-ml/model-registry/partitioned-models).

`image_build`
:   Configures the container image build for the job.

    - `image_repo`: The image repository to use for the job’s container image. If omitted, the job uses the default
      repository.
    - `force_rebuild`: Whether to rebuild the container image even if a cached image exists. Default: `false`.

For example:

Copy code

```
output:
  stage_location: "@my_db.my_schema.my_stage/results/"
resources:
  cpu_requests: "2"
  memory_requests: "8GiB"
inference:
  num_workers: 2
  max_batch_rows: 2048
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SERVICE | Schema | Schema in which the job service is created. |
| USAGE | Compute pool |  |
| USAGE | Model | Model referenced by the `MODEL` clause. |
| READ | Stage | Input stage and the stage where the specification is stored. |
| WRITE | Stage | Output stage where results are written (the specification’s `output.stage_location`). |
| READ | Image Repository | Repository of images referenced by the specification. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When calling EXECUTE INFERENCE JOB SERVICE, specify the parameters in the order shown in [Syntax](#syntax): compute
  pool, specification, input source (`FROM`), model, and then the remaining optional properties.
- To mark completion, the job writes a `_SUCCESS` completion file to the output directory. To avoid reading partial
  results, read the output only after this file is present.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Run batch inference from a query

Run inference asynchronously (the default) over rows produced by a subquery, using a specific model version and
function.

Copy code

```
EXECUTE INFERENCE JOB SERVICE
  IN COMPUTE POOL my_compute_pool
  WITH SPECIFICATION $$
  output:
    stage_location: "@my_db.my_schema.my_stage/results/"
  $$
  FROM ( SELECT id, review_text FROM my_db.my_schema.reviews WHERE lang = 'en' )
  MODEL = my_db.my_schema.sentiment_model
  VERSION = v1
  FUNCTION = 'predict';
```

The command doesn’t specify the `ASYNC` parameter, so the job runs asynchronously and the command returns immediately.

### Run batch inference from a stage on GPUs

Run inference synchronously over files in a stage, requesting a GPU and using the vLLM inference engine.

Copy code

```
EXECUTE INFERENCE JOB SERVICE
  IN COMPUTE POOL my_gpu_pool
  WITH SPECIFICATION $$
  resources:
    gpu_requests: "1"
  inference:
    engine_options:
      engine: VLLM
  output:
    stage_location: "@my_db.my_schema.my_stage/results/"
  $$
  FROM @my_db.my_schema.input_stage/images/
  MODEL = my_db.my_schema.image_classifier
  ASYNC = FALSE;
```

### Run a batch inference job with multiple replicas

Run 3 replicas of an inference job with a named job service, tuning the number of workers and batch size in the
specification.

Copy code

```
EXECUTE INFERENCE JOB SERVICE
  IN COMPUTE POOL my_pool
  WITH SPECIFICATION $$
  inference:
    num_workers: 2
    max_batch_rows: 2048
  output:
    stage_location: "@my_db.my_schema.my_stage/results/"
  $$
  FROM ( SELECT * FROM my_db.my_schema.input_table )
  MODEL = my_db.my_schema.my_model
  NAME = my_db.my_schema.my_inference_job
  REPLICAS = 3;
```

Use the [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service) command to find the status of each replica.

Copy code

```
SHOW SERVICE INSTANCES IN SERVICE my_db.my_schema.my_inference_job;
```

In the output, the `instance_id` and `status` columns show the replica number and its status.

### Run multimodal inference with column handling

Run multimodal inference on files (such as images, audio, or video) that are referenced by stage path. Each input row
carries a full stage path to a file, and `input.column_handling` tells Snowflake to read that file and pass its
contents to the model. For the handled column, set `input_format` to `full_stage_path` and `convert_to` to the
encoding your model expects (`raw_bytes`, `base64`, or `base64_data_url`). The `column_handling` key matches the input
column name.

In this example, the `IMAGES` column produced by the `FROM` subquery holds full stage paths such as
`@my_db.my_schema.my_stage/data/cat.jpeg`.

Copy code

```
EXECUTE INFERENCE JOB SERVICE
  IN COMPUTE POOL my_compute_pool
  WITH SPECIFICATION $$
  input:
    column_handling:
      IMAGES:
        input_format: full_stage_path
        convert_to: raw_bytes
  output:
    stage_location: "@my_db.my_schema.my_stage/results/"
  $$
  FROM ( SELECT images FROM my_db.my_schema.pet_images )
  MODEL = my_db.my_schema.image_classifier;
```
