# ML Jobs in Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

ML Jobs enables collaborators to run complex, resource-intensive machine learning workflows within
[Collaboration Data Clean Rooms](/user-guide/cleanrooms/about). Instead of running Python code as UDFs or stored
procedures on a standard warehouse, ML Jobs runs full ML workloads in an isolated container environment. This enables
collaborators across advertising, retail media, and measurement to train models on combined data
without exposing raw user-level data to any party.

ML Jobs extends the existing collaboration specification and template submission workflow. Template providers stage
artifacts and register ML Jobs code specs, then submit templates for approval. Analysis runners review and approve the
templates, then run ML Jobs on their own compute pool.

### Benefits

- **Simplified development:** Stage Python scripts and specify pip dependencies. No need to build or manage Docker
  images.
- **Distributed training:** Run workloads across multiple nodes with GPU support for accelerated training and
  inference. Snowflake [distributed trainers](/developer-guide/snowflake-ml/distributed-training) for XGBoost,
  LightGBM, and PyTorch scale automatically across compute pool nodes.
- **Hyperparameter optimization:** Use the built-in [HPO API](/developer-guide/snowflake-ml/container-hpo)
  (`snowflake.ml.modeling.tune`) for Bayesian optimization, random search, and grid search. Run parallel trials
  with no additional dependencies.
- **Multi-file projects:** Stage entire project directories with multiple modules, libraries, and model artifacts.
- **Flexible compute:** Select the compute pool size and instance family to match the workload.
- **Job monitoring:** Track progress through container logs, status checks, and result retrieval.

For more information about ML Jobs capabilities, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

### Use cases

ML Jobs supports a range of use cases across advertising, retail media, financial services, and other industries:

- **Lookalike modeling:** Train classifiers on seed audiences and score users across impression and campaign data.
  Applicable to CTV, retail media networks (RMN), and digital advertising.
- **Measurement and incrementality:** Run sales lift studies and incrementality models by joining ad impressions with
  purchase or conversion data across collaborators. Use [distributed HPO](/developer-guide/snowflake-ml/container-hpo)
  to optimize uplift model hyperparameters for each campaign automatically.
- **Attribution modeling:** Build multi-touch attribution models across campaign logs, impressions, and conversion
  events from multiple data sources without exposing raw user-level data.
- **Propensity scoring:** Score user populations for purchase propensity, churn risk, or lifetime value using ad
  exposure, engagement, and transaction features from multiple parties.
- **Audience segmentation:** Cluster and segment users using ML techniques on combined impression logs, CRM data, and
  behavioral signals from publishers, advertisers, and data providers.
- **Distributed model training:** Train large models using Snowflake
  [distributed trainers](/developer-guide/snowflake-ml/distributed-training) (XGBoost, LightGBM, PyTorch) that
  automatically scale across multiple nodes and GPUs in the compute pool.
- **Custom ML workflows:** Run any containerized Python ML workload inside a secure clean room environment, including
  proprietary models, pre-trained model inference, and feature engineering on campaign and user data.

## Requirements

- Both accounts in the collaboration must have the latest version of the Snowflake Data Clean Rooms environment
  installed.
- The analysis runner must have a compute pool available for running ML Jobs. For GPU-accelerated
  workloads, a GPU compute pool is required. GPU availability varies by region: see
  [Compute pool errors](/user-guide/cleanrooms/v2/troubleshooting#ml-jobs) in the troubleshooting guide.

## ML Jobs code spec

An ML Jobs code spec defines one or more containerized ML workloads that run on a compute pool.
For the full field reference, including `stage_code_dir` requirements and `image_tag` options,
see [ML Jobs code specification](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-ml-jobs).

## User flow: template provider

The template provider defines and submits the ML Job spec and the template for execution in the collaboration.

### 1. Stage artifacts

Stage your code, model files, and private libraries into an internal stage. The stage must have directory enabled and
use Snowflake-managed encryption:

Copy code

```
CREATE STAGE IF NOT EXISTS my_db.public.ml_stage
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

Upload your Python scripts using SnowSQL or the Snowflake CLI:

Copy code

```
PUT file://train.py @my_db.public.ml_stage/ml_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://score.py @my_db.public.ml_stage/ml_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
```

After uploading, refresh the stage directory so that the collaboration can access the files:

Copy code

```
ALTER STAGE my_db.public.ml_stage REFRESH;
```

### 2. Register the ML Jobs code spec

Register an ML Jobs code spec that references the staged artifacts. The code spec must include an `ml_jobs` section
with at least one ML job definition:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_CODE_SPEC(
$$
api_version: 2.0.0
spec_type: code_spec
name: my_ml_model
version: V0
ml_jobs:
  - name: my_train_job
    entrypoint: train.py
    stage_code_dir: '@my_db.public.ml_stage/ml_project'
    image_tag: "2.9.0"
    pip_requirements:
      - pandas
      - xgboost
      - scikit-learn
$$);
```

Tip

The `image_tag` field is optional. If you omit it, the collaboration uses the latest available
runtime image. The image is re-evaluated when the code spec is added to a collaboration and on
each subsequent patch. To ensure your code spec runs against a stable, known
set of libraries, pin `image_tag` to a specific version. See
[Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases) for the
list of available versions, and
[ML Jobs code specification](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-ml-jobs)
for the full field reference.

For the full field reference, see
[ML Jobs code specification](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-ml-jobs).

### 3. Register templates

Register a template for each step in your pipeline. Each template calls the ML job procedure generated from the code
spec:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
$$
api_version: 2.0.0
spec_type: template
name: my_train_template
version: V0
type: sql_analysis
parameters:
  - name: compute_pool
    description: Name of the compute pool to run the ML job on.
    type: string
    required: true
code_specs:
  - <code_spec_id>
template: |
  call cleanroom.my_ml_model$my_train_job(
    {{ compute_pool }}, {{ num_instances | default(1) }}, {{ warehouse | default(\"APP_WH\") }},
    OBJECT_CONSTRUCT('source_table', ARRAY_CONSTRUCT({{ source_table[0] }}, {{ source_table[1] }}))::VARCHAR
  )
$$);
```

### 4. Submit the template for approval

Submit the template to the collaboration for approval using the standard template approval flow. The collaborator
validates the code and artifacts using hashes to ensure compliance.

### 5. Update code as needed

As the code evolves, update the ML Jobs code spec and resubmit for approval. To update a code
spec, change the `version` field and call `REGISTER_CODE_SPEC` again with the updated YAML.
Re-registration recomputes content hashes automatically.

Note

ML Jobs code specs registered before the
[June 18, 2026 release](/release-notes/2026/other/2026-06-18-dcr) (Clean Rooms API Version 16.3)
don’t have content hashes and can’t be added to a collaboration. For resolution steps, see
[ML Jobs troubleshooting](/user-guide/cleanrooms/v2/troubleshooting#ml-jobs).

## User flow: analysis runner

The analysis runner reviews, approves, and executes the ML Job within the collaboration.

### 1. Review and approve the template

Review the template approval request and inspect the artifacts. Validate the code and artifacts using hashes to ensure
compliance. Approve the pending template.

Note

If code review is needed, it should be done offline.

### 2. Set up the compute pool

ML Jobs runs in containers on a compute pool instead of a warehouse. Create a compute pool for the installed clean room
application:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE COMPUTE POOL my_ml_pool
    FOR APPLICATION <installed_app_name>
    MIN_NODES = 1
    MAX_NODES = 1
    INSTANCE_FAMILY = CPU_X64_XS  -- minimum size; increase for production workloads
    AUTO_RESUME = TRUE;

GRANT USAGE ON COMPUTE POOL my_ml_pool
    TO APPLICATION <installed_app_name>;
GRANT USAGE ON WAREHOUSE APP_WH
    TO APPLICATION <installed_app_name>;
```

### 3. Run the ML Job

Call `COLLABORATION.RUN` with the template and pass the compute pool name as a parameter. The call returns a job ID:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: analysis
    template: <template_id>
    template_configuration:
      arguments:
        compute_pool: my_ml_pool
    $$
);
```

The `template` value is the template ID, which is the template name and version joined by an underscore. For example,
if you registered a template named `my_train_template` with version `v1`, the template ID is `my_train_template_v1`.

### 4. Monitor the ML Job

Use `RUN_ML_JOB_ACTION` to check logs, status, and results. Pass a YAML specification with the job ID returned by
`COLLABORATION.RUN` and the action to perform:

Copy code

```
-- Check job status.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_status
    $$
);

-- Check container logs for progress.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_logs
    $$
);

-- Get the result once the job completes.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_result
    $$
);
```

The `action` field is case-insensitive. Valid actions are:

`get_status`
:   Returns the current execution status of the job. Possible values: `PENDING`, `RUNNING`,
    `DONE`, `FAILED`. Poll this action to know when the job completes.

`get_logs`
:   Returns the container’s stdout/stderr output. Use this to monitor progress, debug errors, or
    view script print statements. Only available if `allow_monitoring` is `true` in the code
    spec **and** the collaboration owner has not disabled `ALLOW_ML_JOBS_MONITORING`.

    `get_logs` retrieves output through [`SYSTEM$GET_SERVICE_LOGS`](/sql-reference/functions/system_get_service_logs),
    which returns only the most recent container output (up to 100 KB of the most recent log lines
    by default). The beginning of a long-running job’s logs may therefore be missing, and logs
    can become unavailable after the job’s service expires.

    To retrieve the complete, persisted logs, query the account event table, where Snowflake stores all
    container stdout/stderr. See
    [Publishing and accessing container logs](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs)
    and the [event table columns](/developer-guide/logging-tracing/event-table-columns) reference.

`get_result`
:   Returns the job’s return value after completion. For scripts that write to cleanroom tables
    rather than returning data directly, this returns NULL. Check `get_status` first to confirm
    the job is `DONE` before calling `get_result`.

These actions map to the underlying Snowflake ML Jobs management API. For more details on job
lifecycle and status values, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

Note

Log access (`get_logs`) is controlled by the `ALLOW_ML_JOBS_MONITORING` collaboration configuration, which is
`true` (enabled) by default. Only the collaboration owner can change it, and only the owner’s setting applies to the
collaboration. To disable or re-enable log access, the owner calls
[SET\_CONFIGURATION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-set-configuration-reference):

Copy code

```
-- Disable ML Jobs log access for the collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.SET_CONFIGURATION(
  'my_collaboration',
  'ALLOW_ML_JOBS_MONITORING',
  'false'
);
```

When disabled, `get_logs` returns an error, but `get_status` and `get_result` still work.

### 5. Activate results

Activate the output audiences or measurement metrics back to collaborators or third parties using the standard
activation template flow.

## Examples

- [Lookalike audience modeling (ML Jobs option)](/user-guide/cleanrooms/collab-lookalike-modeling#option-2-ml-jobs)
- [Multi-party incrementality measurement with automated HPO](/user-guide/cleanrooms/collab-mljobs-rmn-hpo)

## Tips and patterns

For troubleshooting common ML Jobs errors (template call pattern, compute pool issues), see
[Troubleshooting Collaboration Data Clean Rooms — ML Jobs](/user-guide/cleanrooms/v2/troubleshooting#ml-jobs).

### Runtime image upgrades and patching

When a collaboration patch runs, the default ML runtime image reflects the current Snowflake Data Clean Rooms API release.
All pinned `image_tag` values are preserved unchanged.

- **Unspecified `image_tag`:** Uses the latest available runtime image, resolved when the code
  spec is added to a collaboration. To pick up a new default image on an existing code spec,
  re-add the code spec to the collaboration.
- **Pinned `image_tag`:** Your pin is always preserved unchanged across patches. Pin `image_tag`
  to run against a stable, known set of libraries.

See [ML Jobs code specification](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-ml-jobs)
for the `image_tag` field reference and
[Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases) for the
list of available versions.

### Development workflow

You can build and test the full ML Job workflow outside Snowflake Data Clean Rooms in a standard
Snowflake environment using the same Python scripts and container runtime. You can then iterate
quickly in your normal development environment without pushing each change through the
collaboration’s template approval workflow.

Once you’ve built and tested your scripts, bring them into the collaboration using a code spec with
a pinned `image_tag`. Pinning the image version locks down the exact set of dependencies you
developed and tested with, so the workload runs identically inside the collaboration. See
[ML Jobs code specification](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-ml-jobs)
for the `image_tag` field reference.

### Accessing collaborator data

Unlike UDF or procedure templates that execute inline SQL, ML Jobs scripts can’t reference `cleanroom.source_table_0` directly because that view is not created for ML Jobs execution.

Instead, pass source table references into the container through the args parameter using `OBJECT_CONSTRUCT`:

Copy code

```
template: |
  call cleanroom.my_ml_model$my_train_job(
    {{ compute_pool }}, {{ num_instances | default(1) }}, {{ warehouse | default("APP_WH") }},
    OBJECT_CONSTRUCT('source_table', ARRAY_CONSTRUCT({{ source_table[0] }}, {{ source_table[1] }}))::VARCHAR
  )
```

In your Python script, read the source table references from the args JSON:

Copy code

```
import argparse, json
from snowflake.snowpark.context import get_active_session

parser = argparse.ArgumentParser()
parser.add_argument("--args", type=str, default="{}")
args = json.loads(parser.parse_args().args)

session = get_active_session()
source_tables = args.get("source_table", [])
df = session.table(source_tables[0]).to_pandas()
```

### Writing results for activation

For activation to work, the scoring script must write results to a cleanroom table that the activation template reads.
Use `session.create_dataframe(df).write.save_as_table("cleanroom.<table_name>", mode="overwrite")` in the scoring
script, and reference the same table in the activation template:

Copy code

```
template: |
  BEGIN
      CREATE OR REPLACE TABLE cleanroom.activation_data_<results> AS
          SELECT <columns>
          FROM cleanroom.<table_written_by_score>;
      RETURN '<results>';
  END;
```

### Scaling with distributed training

For large datasets (tens of millions of rows or more), use Snowflake
[distributed trainers](/developer-guide/snowflake-ml/distributed-training) instead of single-node training. The
ML Jobs container runtime includes a Ray cluster that distributed trainers use automatically.

**When to use distributed training:**

Distributed training helps scale out to multiple nodes when the memory or compute requirements to
train a model are beyond what can be supported in a single compute pool node, covering either a
high memory CPU node or a large GPU node.

**Code change: replace raw XGBoost with the distributed trainer:**

Copy code

```
# Instead of:
import xgboost
model = xgboost.train(params, dtrain, num_rounds)

# Use the distributed trainer:
from snowflake.ml.modeling.distributors import XGBoostDistributor
from snowflake.ml.data.data_connector import DataConnector

train_connector = DataConnector.from_dataframe(session.table(source_tables[0]))

distributor = XGBoostDistributor(
    params={"objective": "binary:logistic", "max_depth": 6, "eta": 0.1},
    num_boost_round=100,
    label_column="LABEL",
)
model = distributor.train(train_connector)
```

**Template change: increase `num_instances` for multi-node:**

Copy code

```
template: |
  call cleanroom.my_ml_model$my_train_job(
    {{ compute_pool }},
    {{ num_instances | default(2) }},
    {{ warehouse | default("APP_WH") }},
    OBJECT_CONSTRUCT('source_table', ARRAY_CONSTRUCT({{ source_table[0] }}))::VARCHAR
  )
```

The `num_instances` parameter controls how many compute pool nodes the job runs across. The distributed trainer
automatically discovers and uses all available nodes. Size the compute pool accordingly:

Copy code

```
CREATE COMPUTE POOL my_distributed_pool
    FOR APPLICATION <installed_app_name>
    MIN_NODES = 4
    MAX_NODES = 4
    INSTANCE_FAMILY = GPU_NV_S  -- or CPU_X64_L for CPU training
    AUTO_RESUME = TRUE;
```

For more information, see [Distributed training](/developer-guide/snowflake-ml/distributed-training).
