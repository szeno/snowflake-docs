# Snowflake ML Jobs

Use Snowflake ML Jobs to run machine learning (ML) workflows inside Snowflake ML container runtimes.
You can run them from any development environment. You don’t need to run the code in a Snowflake worksheet or notebook. Use jobs to leverage Snowflake’s infrastructure to run resource-intensive tasks within your development workflow. For information about setting up Snowflake ML locally, see [Using Snowflake ML Locally](/developer-guide/snowflake-ml/snowpark-ml#label-snowpark-ml-get-started).

Important

Snowflake ML Jobs are available in `snowflake-ml-python` version 1.26.0 and later.

Snowflake ML Jobs enable you to do the following:

- Run ML workloads on Snowflake Compute Pools, including GPU and high-memory CPU instances.
- Use your preferred development environment such as VS Code or Jupyter notebooks.
- Install and use custom Python packages within your runtime environment.
- Use Snowflake’s distributed APIs to optimize data loading, training, and hyperparameter tuning.
- Integrate with orchestration tools, such as Apache Airflow.
- Monitor and manage jobs through Snowflake’s APIs.

You can use these capabilities to do the following:

- Execute resource-intensive training on large datasets requiring GPU acceleration or significant compute resources.
- Productionize ML workflows by moving ML code from development to production with programmatic execution through pipelines.
- Retain your existing development environment while leveraging Snowflake’s compute resources.
- Lift and shift OSS ML workflows with minimal code changes.
- Work directly with large Snowflake datasets to reduce data movement and avoid expensive data transfers.

## Prerequisites

1. Install the Snowflake ML Python package.

   Copy code

   ```
   pip install snowflake-ml-python>=1.26.0
   ```
2. The default compute pool size uses the CPU\_X64\_S instance family. The minimum number of nodes is 1 and the maximum is 25. You can use the following SQL command to create a custom compute pool:

   Copy code

   ```
   CREATE COMPUTE POOL IF NOT EXISTS MY_COMPUTE_POOL
     MIN_NODES = <MIN_NODES>
     MAX_NODES = <MAX_NODES>
     INSTANCE_FAMILY = <INSTANCE_FAMILY>;
   ```
3. Snowflake ML Jobs require a Snowpark Session. Use the following code to create it:

   Copy code

   ```
   from snowflake.snowpark import Session
   from snowflake.ml.jobs import list_jobs

   ls = list_jobs() # This will fail! You must create a session first.

   # Requires valid ~/.snowflake/config.toml file
   session = Session.builder.getOrCreate()

   ls = list_jobs(session=session)
   ls = list_jobs() # Infers created session from context
   ```

   For information about creating a session, see [Creating a Session](/developer-guide/snowpark/python/creating-session#label-snowpark-python-creating-session).

## Run a Snowflake ML job

You can run a Snowflake ML Job in one of the following ways:

- Using a function decorator within your code.
- Submitting entire files or directories using the Python API.

### Run a Python function as a Snowflake ML Job

Use Function Dispatch to run individual Python functions remotely on Snowflake’s compute resources with the `@remote` decorator.

Using `@remote`, you can:

- Serializate the function and its dependencies.
- Upload it to a specified Snowflake stage.
- Execute it within a specific Container Runtime.

The following example Python code uses the `@remote` decorator to submit a function call as a Snowflake ML Job:

Copy code

```
from snowflake.ml.jobs import remote

@remote("MY_COMPUTE_POOL", stage_name="payload_stage", session=session)
def train_model(data_table: str):
  # Provide your ML code here, including imports and function calls
  ...

job = train_model("my_training_data")
```

Note

Submitting a job requires an existing Snowpark `Session`; See [Prerequisites](#label-snowflake-ml-jobs-prerequisites) for details.

Invoking a `@remote` decorated function returns a Snowflake `MLJob` object that can be used to manage and monitor the job execution. For more information, see [Ray Dashboard in ML Jobs](#label-snowflake-ml-job-management).

### Run a Python file as a Snowflake ML Job

Run Python files or project directories on Snowflake compute resources. This is useful when:

- You have complex ML projects with multiple modules and dependencies.
- You want to maintain separation between local development and production code.
- You need to run scripts that use command-line arguments.
- You’re working with existing ML projects that weren’t specifically designed for execution on Snowflake compute.

The Snowflake Job API offers three main methods for submitting file-based payloads:

- `submit_file`: For running single Python files
- `submit_directory`: For running Python projects spanning multiple files and resources
- `submit_from_stage`: For running Python projects saved on a Snowflake stage

Both methods support:

- Command-line argument passing
- Environment variable configuration
- Custom dependency specification
- Project asset management through Snowflake stages

File Dispatch is particularly useful for productionizing existing ML workflows and maintaining clear separation between development and execution environments.

The following Python code submits a file as a Snowflake ML Job:

Copy code

```
from snowflake.ml.jobs import submit_file

# Run a single file
job1 = submit_file(
  "train.py",
  "MY_COMPUTE_POOL",
  stage_name="payload_stage",
  args=["--data-table", "my_training_data"],
  session=session,
)
```

The following Python code submits a directory as a Snowflake ML Job:

Copy code

```
from snowflake.ml.jobs import submit_directory

# Run from a directory
job2 = submit_directory(
  "./ml_project/",
  "MY_COMPUTE_POOL",
  entrypoint="train.py",
  stage_name="payload_stage",
  session=session,
)
```

The following Python code submits a directory from a Snowflake Stage as a Snowflake ML Job:

Copy code

```
from snowflake.ml.jobs import submit_from_stage

# Run from a directory
job3 = submit_from_stage(
  "@source_stage/ml_project/"
  "MY_COMPUTE_POOL",
  entrypoint="@source_stage/ml_project/train.py",
  stage_name="payload_stage",
  session=session,
)

# Entrypoint may also be a relative path
job4 = submit_from_stage(
  "@source_stage/ml_project/",
  "MY_COMPUTE_POOL",
  entrypoint="train.py",  # Resolves to @source_stage/ml_project/train.py
  stage_name="payload_stage",
  session=session,
)
```

Submitting a file or directory returns a Snowflake `MLJob` object that can be used to manage and monitor the job execution. For more information, see [Ray Dashboard in ML Jobs](#label-snowflake-ml-job-management).

### Run a Snowflake ML Job on a specific container runtime

The `@remote` decorator, as well as the functions `submit_directory`, `submit_from_stage`, and `submit_file` all support the `runtime_environment` keyword. When you don’t provide this keyword in your decorator or function call, Snowflake automatically uses the latest available version of the Snowflake Container Runtime on your compute pool.

To specify a container runtime for your ML Job, use the `runtime_environment` keyword with the full Container Runtime version string. For example, use `2.3.0`. See [Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases) for the full list of available versions and what’s contained in these environments by default.

The following example shows how to pin a function with the `@remote` decorator to Snowflake Container Runtime version `2.3.0`:

Copy code

```
from snowflake.ml.jobs import remote

@remote("MY_COMPUTE_POOL", stage_name="payload_stage", session=session, runtime_environment="2.3.0")
def train_model(data_table: str):
  # Provide your ML code here, including imports and function calls
  ...
```

### Custom runtime

You can build and register your own custom container images to use as the runtime environment for ML Jobs. Custom
images let you include specific packages, meet compliance requirements, and ensure reproducibility across environments.
To use a custom image, reference it with the `runtime_environment="cre@<name>"` format.

For more information, see [Custom runtime images](/developer-guide/snowflake-ml/custom-runtime-images).

### Supporting Additional Payloads in Submissions

When submitting a file, directory, or from a stage, additional payloads are supported for use during job execution.
The import path can be specified explicitly; otherwise, it will be inferred from the location of the additional payload.

Important

You can only load single Python files from a stage.

Copy code

```
# Run from a file
 job1 = submit_file(
   "train.py",
   "MY_COMPUTE_POOL",
   stage_name="payload_stage",
   session=session,
   imports=[
     ("src/utils/", "utils"), # the import path is utils
   ],
 )

 # Run from a directory
 job2 = submit_directory(
   "./ml_project/",
   "MY_COMPUTE_POOL",
   entrypoint="train.py",
   stage_name="payload_stage",
   session=session,
   imports=[
     ("src/utils/"), # the import path is utils
   ],
 )

 # Run from a stage
 job3 = submit_from_stage(
   "@source_stage/ml_project/",
   "MY_COMPUTE_POOL",
   entrypoint="@source_stage/ml_project/train.py",
   stage_name="payload_stage",
   session=session,
   imports=[
     ("@source_stage/src/utils/sub_utils/", "utils.sub_utils"),
   ],
 )
```

### Accessing Snowpark Session in ML Jobs

When running ML Jobs on Snowflake, a Snowpark Session is automatically available in the execution context.
You can access the Session object from within your ML Job payload using the following approaches:

Copy code

```
from snowflake.ml.jobs import remote
from snowflake.snowpark import Session

@remote("MY_COMPUTE_POOL", stage_name="payload_stage")
def my_function():
  # This approach works for all payload types, including file and directory payloads
  session = Session.builder.getOrCreate()
  print(session.sql("SELECT CURRENT_VERSION()").collect())

@remote("MY_COMPUTE_POOL", stage_name="payload_stage")
def my_function_with_injected_session(session: Session):
  # This approach works only for function dispatch payloads
  # The session is injected automatically by the Snowflake ML Job API
  print(session.sql("SELECT CURRENT_VERSION()").collect())
```

The Snowpark Session can be used to access Snowflake tables, stages, and other database objects inside your ML Job.

### Returning results from ML Jobs

Snowflake ML Jobs support returning execution results back to the client environment.
This enables you to retrieve computed values, trained models, or any other artifacts produced by your job payloads.

For function dispatch, simply return a value from your decorated function.
The returned value will be serialized and made available through the `result()` method.

Copy code

```
from snowflake.ml.jobs import remote

@remote("MY_COMPUTE_POOL", stage_name="payload_stage")
def train_model(data_table: str):
  # Your ML code here
  model = XGBClassifier()
  model.fit(data_table)
  return model

job1 = train_model("my_training_data")
```

For file-based jobs, use the special `__return__` variable to specify the return value.

Copy code

```
# Example: /path/to/repo/my_script.py
def main():
    # Your ML code here
    model = XGBClassifier()
    model.fit(data_table)
    return model

if __name__ == "__main__":
    __return__ = main()
```

Copy code

```
from snowflake.ml.jobs import submit_file

job2 = submit_file(
    "/path/to/repo/my_script.py",
    "MY_COMPUTE_POOL",
    stage_name="payload_stage",
    session=session,
)
```

You can retrieve the job execution result using the `MLJob.result()` API.
The API blocks the calling thread until the job reaches a terminal state, then returns the payload’s return value or, if execution failed, raises an exception.
If the payload does not define a return value, the result will be `None` on success.

Copy code

```
# These will block until the respective job is done and return the trained model
model1 = job1.result()
model2 = job2.result()
```

## ML Job Definitions

An ML Job Definition captures the reusable components of an ML Job—payload location, compute pool, and related configuration.
This allows you to submit multiple jobs from the same payload with different arguments without re-uploading
the payload.

Note

ML Job Definitions are available in `snowflake-ml-python` version 1.26 and later.

To create an ML Job Definition, use the `MLJobDefinition` class.
The API closely mirrors the job-creation APIs. All optional parameters supported for job creation are also supported when creating job definitions.

Use Function Dispatch to register individual Python functions with the `@remote` decorator.

Copy code

```
from snowflake.ml.jobs import remote

compute_pool = "MY_COMPUTE_POOL"
@remote(compute_pool, stage_name="payload_stage")
def hello_world(name: str = "world"):
    from datetime import datetime

    print(f"{datetime.now()} Hello {name}!")

# this is a definition handle
definition = hello_world

job1 = hello_world()
```

Use `register()` to create job definitions from a local file, a local directory, or a stage directory.

Copy code

```
from snowflake.ml.jobs import MLJobDefinition

# create a job definition from a stage directory
job_definition1 = MLJobDefinition.register(
    entrypoint ='@tmp_stage/my_project/xgb.py',
    source = '@tmp_stage/my_project',
    stage_name = "payload_stage",
    compute_pool = compute_pool
)

# create a job definition from local file
job_definition2 = MLJobDefinition.register(
    source ='/path/to/script.py',
    stage_name = "payload_stage",
    compute_pool = compute_pool
)

# create a job definition from the directory
job_definition3 = MLJobDefinition.register(
    entrypoint ='/path/to/directory/script.py',
    source = '/path/to/directory',
    stage_name = "payload_stage",
    compute_pool = compute_pool
)
```

Create a job from a job definition, with support for passing different parameters to generate distinct jobs.

Copy code

```
from snowflake.ml.jobs import remote

# create a job definition using the remote decorator
compute_pool = "MY_COMPUTE_POOL"
@remote(compute_pool, stage_name="payload_stage")
def hello_world(name: str = "world"):
    from datetime import datetime

    print(f"{datetime.now()} Hello {name}!")

definition = hello_world

job1 = definition()

job2 = definition(name="ML Job Definition") # pass in the different parameter
```

The `register` function takes `runtime_environment` as an optional keyword argument to select the container image that runs on your selected compute pool. By default, your job definition uses the latest available version of the Snowflake Container Runtime.

To specify a container runtime for your ML Job, use the `runtime_environment` keyword with the full Container Runtime version string. For example, use `2.3.0`. See [Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases) for the full list of available versions and what’s contained in these environments by default.

Support integration with Tasks. Jobs executed from a Task do not run within a stored procedure. Refer to [ML Jobs Task Integration samples](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/ml/ml_jobs/e2e_task_graph) for examples of using Snowflake ML Job Definitions in Tasks.

Copy code

```
from snowflake.ml.jobs import remote

compute_pool = "MY_COMPUTE_POOL"
@remote(COMPUTE_POOL, stage_name="payload_stage")
def train_model(input_data: DataSource) -> Optional[str]:
    ...

train_model_task = DAGTask("TRAIN_MODEL", definition=train_model) # train_model is a job definition created by the @remote decorator
```

## Ray Dashboard in ML Jobs

ML Job now supports the ray dashboard for the running jobs in *snowflake-ml-python* version 1.30 and later.

Note

The Ray Dashboard is not supported on the `CPU_X64_XS` compute pool instance family. The dashboard is only available while the job is running.

Copy code

```
from snowflake.ml.jobs import remote

@remote("MY_COMPUTE_POOL", stage_name="payload_stage", session=session)
def train_model(data_table: str):
  # Provide your ML code here, including imports and function calls
  ...

job = train_model("my_training_data")
ray_dashboard_url = job.get_ray_dashboard_url() # copy and paste this url in browser to log in then to see the ray dashboard
```

## Managing ML Jobs

When you submit a Snowflake ML Job, the API creates an `MLJob` instance. You can use it to do the following:

- Track job progress through status updates
- Debug issues using detailed execution logs
- Retrieve the execution result (if any)

You can use the `get_job` API to retrieve an `MLJob` object by its ID. The following Python code shows how to retrieve an `MLJob` object:

Copy code

```
from snowflake.ml.jobs import MLJob, get_job, list_jobs, delete_job

# Get a list of the 10 most recent jobs as a Pandas DataFrame
jobs_df = list_jobs(limit=10)
print(jobs_df)  # Display list in table format

# Retrieve an existing job based on ID
job = get_job("<job_id>")  # job is an MLJob instance

# Retrieve status and logs for the retrieved job
print(job.status)  # PENDING, RUNNING, FAILED, DONE
print(job.get_logs())

# Clean up the job
delete_job(job)
```

## Managing dependencies

The Snowflake ML Job API runs payloads inside the [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml) environment. The environment has the most commonly used Python packages for machine learning and data science.
Most use cases should work “out of the box” without additional configuration.
If you need custom dependencies, you can use `pip_requirements` to install them.

Snowflake ML Jobs support two ways to install packages:

- **External Access Integration (EAI)**: lets the job reach an external package index, such as PyPI or a private feed, over the network.
- **Artifact repository**: serves packages to the job from a Snowflake `ARTIFACT REPOSITORY` object governed by role-based access control (RBAC), so the job doesn’t need external network access for package installs.

Use one of these for a given job. If you specify both, the artifact repositories take effect and packages are installed only from those repositories.

### Using an External Access Integration

To install custom dependencies from an external package index, you must enable external network access using an External Access Integration. You can use the following SQL example command to provide access:

Copy code

```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION PYPI_EAI
  ALLOWED_NETWORK_RULES = (snowflake.external_access.pypi_rule)
  ENABLED = true;
```

For more information about external access integrations, see [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

After you’ve provided external network access, you can use the `pip_requirements` and `external_access_integrations` parameters to configure custom dependencies. You can use packages that aren’t available in the container runtime environment or if you need specific versions of the packages.

The following Python code shows how to specify custom dependencies to the `remote` decorator:

Copy code

```
@remote(
  "MY_COMPUTE_POOL",
  stage_name="payload_stage",
  pip_requirements=["custom-package"],
  external_access_integrations=["PYPI_EAI"],
  session=session,
)
def my_function():
  # Your code here
```

The following Python code shows how to specify custom dependencies for the `submit_file()` method:

Copy code

```
from snowflake.ml.jobs import submit_file

# Can include version specifier to specify version(s)
job = submit_file(
  "/path/to/repo/my_script.py",
  compute_pool,
  stage_name="payload_stage",
  pip_requirements=["custom-package==1.0.*"],
  external_access_integrations=["pypi_eai"],
  session=session,
)
```

### Private package feeds

Snowflake ML Jobs also support loading packages from private feeds such as JFrog Artifactory and Sonatype Nexus Repository. These feeds are commonly used to distribute internal and proprietary packages, maintain control over dependency versions, and ensure security/compliance.

To install packages from a private feed, you must do the following:

1. Create a Network Rule to allow access to the private feed’s URL.

   1. For sources which use basic authentication, you can simply create a network rule.

      Copy code

      ```
      CREATE OR REPLACE NETWORK RULE private_feed_nr
      MODE = EGRESS
      TYPE = HOST_PORT
      VALUE_LIST = ('<your-repo>.jfrog.io');
      ```
   2. To configure access to a source using private connectivity (i.e. Private Link), follow the steps in [Network egress using private connectivity](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress-private).
2. Create an External Access Integration using the network rule. Grant permission to use the EAI to the role that will be submitting jobs.

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION private_feed_eai
   ALLOWED_NETWORK_RULES = (PRIVATE_FEED_NR)
   ENABLED = true;

   GRANT USAGE ON INTEGRATION private_feed_eai TO ROLE <role_name>;
   ```
3. Specify the private feed URL, External Access Integration, and package(s) when submitting the job

   Copy code

   ```
   # Option 1: Specify private feed URL in pip_requirements
   job = submit_file(
     "/path/to/script.py",
     compute_pool="MY_COMPUTE_POOL",
     stage_name="payload_stage",
     pip_requirements=[
    "--index-url=https://your.private.feed.url",
    "internal-package==1.2.3"
     ],
     external_access_integrations=["PRIVATE_FEED_EAI"]
   )
   ```

   Copy code

   ```
   # Option 2: Specify private feed URL by environment variable
   job = submit_directory(
     "/path/to/code/",
     compute_pool="MY_COMPUTE_POOL",
     entrypoint="script.py",
     stage_name="payload_stage",
     pip_requirements=["internal-package==1.2.3"],
     external_access_integrations=["PRIVATE_FEED_EAI"],
     env_vars={'PIP_INDEX_URL': 'https://your.private.feed.url'},
   )
   ```

If your private feed URL contains sensitive information like authentication tokens, manage the URL by creating a Snowflake Secret.
Use the [CREATE SECRET](/sql-reference/sql/create-secret) to create a secret. Configure secrets during job submission with the `spec_overrides` argument.

Note

When using `spec_overrides`, Snowflake only supports and validates secrets in the `secrets` field within container definitions. Snowflake does not support or validate other fields, such as `args`, `volumes`, and `endpoints`.

Copy code

```
# Create secret for private feed URL with embedded auth token
feed_url = "<your-repo>.jfrog.io/artifactory/api/pypi/test-pypi/simple"
user = "<auth_user>"
token = "<auth_token>"
session.sql(f"""
CREATE SECRET IF NOT EXISTS PRIVATE_FEED_URL_SECRET
 TYPE = GENERIC_STRING
 SECRET_STRING = 'https://{auth_user}:{auth_token}@{feed_url}'
""").collect()

# Prepare service spec override for mounting secret into job execution
spec_overrides = {
 "spec": {
  "containers": [
    {
     "name": "main",  # Primary container name is always "main"
     "secrets": [
      {
        "snowflakeSecret": "PRIVATE_FEED_URL_SECRET",
        "envVarName": "PIP_INDEX_URL",
        "secretKeyRef": "secret_string"
      },
     ],
    }
  ]
 }
}

# Load private feed URL from secret (e.g. if URL includes auth token)
job = submit_file(
  "/path/to/script.py",
  compute_pool="MY_COMPUTE_POOL",
  stage_name="payload_stage",
  pip_requirements=[
    "internal-package==1.2.3"
  ],
  external_access_integrations=["PRIVATE_FEED_EAI"],
  spec_overrides=spec_overrides,
)
```

For more information about the `container.secrets`, see [`containers.secrets` field](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-ref-containers-secrets).

### Using artifact repositories

Snowflake’s default PyPI artifact repository lets you install PyPI packages with support for [package policies](/developer-guide/udf/python/packages-policy) in your jobs. The Snowflake PyPI repo is a schema-level, RBAC-governed object: `snowflake.snowpark.pypi_shared_repository`. Because packages are served through this object, your job doesn’t need external network access to install them.

You can also use a customer-hosted artifact repository as the package source for a job: for example, a Nexus, JFrog, Azure DevOps, Google Cloud Artifact Registry, or AWS CodeArtifact repository registered as a Snowflake `ARTIFACT REPOSITORY` object. To configure your own repository, see [Integrate customer-hosted Python artifact repositories](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).

Note

Artifact repository support in Snowflake ML Jobs is available in `snowflake-ml-python` version 1.51.0 and later.

#### Privilege requirements

By default, the `PUBLIC` role has access to the Snowflake PyPI repo. To manage privileges, use the following commands:

Copy code

```
-- To revoke access from the PUBLIC role:
REVOKE DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER FROM ROLE PUBLIC;

-- To grant access to specific roles:
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE <your_user_role>;
```

To use a customer-hosted repository, the role that submits the job needs the `USAGE` privilege on that artifact repository. For more information, see [Integrate customer-hosted Python artifact repositories](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).

#### Submitting a job with an artifact repository

Pass the fully qualified repository name to the `artifact_repositories` parameter, along with the packages you want in `pip_requirements`. The parameter accepts a list, so you can specify more than one repository.

The following Python code shows how to use an artifact repository with the `remote` decorator. The same parameter works the same way with `submit_file()`, `submit_directory()`, `submit_from_stage()`, and `MLJobDefinition.register()`.

Copy code

```
@remote(
  "MY_COMPUTE_POOL",
  stage_name="payload_stage",
  artifact_repositories=["snowflake.snowpark.pypi_shared_repository"],
  pip_requirements=["catboost"],
  session=session,
)
def my_function():
  # Your code here
```

To install internal packages from a customer-hosted repository, specify that repository. You can list it alongside the Snowflake PyPI repo if your payload also needs public packages:

Copy code

```
artifact_repositories=[
  "my_db.my_schema.my_python_repo",
  "snowflake.snowpark.pypi_shared_repository",
],
pip_requirements=["internal-package==1.2.3", "catboost"],
```

#### How multiple repositories are resolved

When you specify more than one repository, all of them are exposed to the container. The package installer that runs inside the container, not the ML Job itself, determines which repository a package comes from:

- If your code runs `pip install foo`, `pip` queries all configured artifact repositories and selects the best matching package version.
- If your code runs `uv pip install foo`, `uv` checks the repositories in the configured order and uses the first repository that contains `foo`.

Because the installer resolves conflicts, the same set of repositories can produce different results depending on which installer you use. For example, if both repository A and repository B contain `foo`, `uv` uses A when A is listed first, while `pip` might choose the highest compatible version across both. To make resolution predictable, list your repositories in priority order and pin package versions in `pip_requirements`.

## Examples

See [ML Jobs Code Samples](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/ml/ml_jobs) for examples of how to use Snowflake ML Jobs.

## Cost considerations

Snowflake ML Jobs run on Snowpark Container Services and are billed based on usage. For information about compute costs, see [Snowpark Container Services costs](/developer-guide/snowpark-container-services/accounts-orgs-usage-views).

Job payloads are uploaded to the stage specified with the `stage_name` argument. To avoid additional charges, you must clean them up. For more information, see [Understanding storage cost](/user-guide/cost-understanding-data-storage) and [Exploring storage cost](/user-guide/cost-exploring-data-storage) to learn more about costs associated with stage storage.
