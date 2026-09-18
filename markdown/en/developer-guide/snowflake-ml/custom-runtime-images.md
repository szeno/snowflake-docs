# Custom Runtime Images

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Custom runtime images let you use your own container images for machine learning workloads on Container Runtime,
including [Snowflake Notebooks](/developer-guide/snowflake-ml/notebooks-on-spcs) and
[ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview). You can extend the Snowflake-provided base images provided they meet platform compatibility requirements.

## Overview

While the Container Runtime image is convenient for interactive use with Notebooks and ad-hoc execution with ML Jobs, using only
the Snowflake-provided image can create challenges for enterprise customers, particularly those in regulated
industries or with mature MLOps practices.

Custom runtime images address the following needs:

- **Compliance and security**: Strict IT and security policies often mandate the use of pre-scanned and allowlisted
  images for production ML pipelines. Custom images let regulated customers integrate fully security-scanned and
  approved images into Snowflake workloads.
- **CI/CD integration**: Custom images can be built, tested, scanned, and validated as part of existing CI/CD
  pipelines, enabling automated validation and faster iteration when deploying to Snowflake.
- **Reproducibility**: Data scientists can create consistent Docker images that encapsulate exact package and version
  requirements, ensuring reproducibility across development, staging, and production environments.
- **Package control**: Organizations that don’t have external access integrations to PyPI repositories can use
  org-approved and managed images without needing PyPI access at runtime.
- **Persistent environments**: Custom images eliminate the need for manual `pip install` commands in every Notebook
  session, providing persistent package installations that are shareable and reproducible across Notebooks.

### How it works

You can create custom images by extending the base image: Build on one of the Snowflake-provided base ML runtime images, adding your own packages and configuration on top.

After building a custom image, you push it to a Snowflake image repository, validate it, and register it as a
Custom Runtime Environment (CRE). You can then reference the CRE when running ML Jobs or Notebooks.

## Workflow: Create and use a custom runtime image

To use a Custom Runtime Environment in ML Jobs or Notebooks, you need to build a custom container image, validate it,
push it to Snowflake, and register it. The following steps outline the complete end-to-end workflow. Before you begin, make sure to install [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index).

### Step 1: Authenticate with the image registry

Before pulling the base image or pushing to the Snowflake repository, authenticate the local Docker client with the
Snowflake image registry using the Snowflake CLI.

Copy code

```
snow spcs image-registry login
```

For more information, see [snow spcs image-registry login](/developer-guide/snowflake-cli/command-reference/spcs/image-registry/login).

### Step 2: Select and pull a base image

All custom images must be derived from an official Snowflake ML runtime base image. Base images are specific to the
hardware type (CPU or GPU) and Python version.

1. Identify the appropriate base image from the [Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases).
2. Pull the base image locally using Docker.

Copy code

```
docker pull <registry_url>/snowflake/images/snowflake_images/container_runtime/cpu_x86_64:2.7.2
```

### Step 3: Author the Dockerfile

Create a Dockerfile that uses the selected Snowflake base image. Specify any additional system packages, Python
libraries, or organizational configuration required for your workloads.

Copy code

```
FROM <registry_url>/snowflake/images/snowflake_images/container_runtime/cpu_x86_64:2.7.2

RUN uv pip install --system --break-system-packages \
    xgboost==2.0.3 \
    scikit-learn==1.3.2
```

### Step 4: Build the custom image

Build the custom image locally using standard Docker tooling. Build for the `linux/amd64` platform to ensure
compatibility with Snowflake’s execution environment.

Copy code

```
docker build --platform linux/amd64 -t my-custom-image:v1 .
```

### Step 5: Validate the image locally (pre-push)

Before pushing the image to Snowflake, validate it locally to ensure it meets runtime requirements. This
advisory step helps prevent failures during the server-side registration process.

Copy code

```
snow custom-image validate my-custom-image:v1
```

Resolve any missing dependencies, conflicting packages, or configuration errors flagged by the validation report.

#### Validation requirements

To pass the local validation, your image must meet the following criteria:

- **Entrypoint**: The image must use the exact entrypoint path `/usr/local/bin/entrypoint.sh`.
- **Required environment variables**: The image must expose the dashboard port by including the environment
  variable `DASHBOARD_PORT=12003`.
- **Mandatory Python packages**: The image must contain the following packages:
  - snowflake-ml-python
  - snowflake-snowpark-python[pandas]
  - ray
  - jupyter-server
  - notebook
  - ipykernel
  - ipython
  - sqlparse
  - jinja2
  - psutil
- **Healthy package dependencies**: The Python environment must have a fully resolved dependency tree with no
  package conflicts.
- **Optional vulnerability scanning**: The validation tool can also scan for vulnerabilities (CVEs) in your
  image’s packages or base layers. While fixing high-severity vulnerabilities is strongly recommended, this check
  isn’t required to pass validation.

Copy code

```
snow custom-image validate my-custom-image:v1 --scan-vulnerabilities
```

### Step 6: Tag and push to the image repository

Tag the locally built, validated image with the fully qualified URL of the Snowflake image repository, then push it.

1. Tag the image:

   Copy code

   ```
   docker tag my-custom-image:v1 <registry_url>/<database>/<schema>/<image_repo>/my-custom-image:v1
   ```
2. Push the image:

   Copy code

   ```
   docker push <registry_url>/<database>/<schema>/<image_repo>/my-custom-image:v1
   ```

The `registry_url` will look something like `<your_account>.registry.snowflakecomputing.com`.

### Step 7: Create the Custom Runtime Environment

With the image stored in the Snowflake repository, run the DDL command to register the Custom Runtime Environment.
During this step, Snowflake performs a server-side validation check to confirm the image executes correctly. The CRE
is only created if this check passes.

Copy code

```
CREATE CUSTOM RUNTIME ENVIRONMENT my_cre
    IMAGE_PATH = '/<database>/<schema>/<image_repo>/my-custom-image:v1'
    BASE_IMAGE_TYPE = CPU;
```

Once this command completes successfully, the Custom Runtime Environment is in the RESOLVED state and is ready to be
referenced in ML Jobs and Notebooks.

## Use custom runtime images in ML Jobs

Once your custom image is registered, you can use it to run ML Jobs. This ensures your code executes in your
specialized environment with all your required dependencies.

When submitting an ML Job using the Snowflake ML Python SDK, configure the environment using the
`runtime_environment` parameter. Reference an admin-approved Custom Runtime Environment using the `cre@<name>` format.

### Prerequisites

- **Required package**: snowflake-ml-python version 1.37.0 or higher.
- **Role privileges**: The active role must hold the USAGE privilege on the target Custom Runtime Environment,
  along with access to the underlying image repository.
- **Environment status**: The Custom Runtime Environment must be in the RESOLVED state. Environments marked as
  DEPRECATED can’t be used for new jobs.

### Usage notes

- When using a CRE alias, the system verifies the image’s SHA digest at runtime. If the underlying image in
  the repository was modified after the CRE was registered, the job submission is rejected to ensure
  reproducibility. In this case, you must recreate the CRE.

### Example

Copy code

```
from snowflake.ml import jobs

@jobs.remote(
    "MY_COMPUTE_POOL",
    stage_name="payload_stage",
    runtime_environment="cre@my_cre"
)
def test_function():
    ...

job = test_function()
```

## Use custom runtime images in Notebooks

Once your custom image is registered, you can use it to run Notebook services. This ensures your code executes in
your specialized environment with all your required dependencies.

Registered custom images can be selected from advanced settings when creating, editing, and scheduling a
notebook in the workspaces UI. You can also use a custom image when executing a Code Bundle using SQL with the
`RUNTIME` parameter. Reference an admin-approved Custom Runtime Environment using the `cre@<name>` format.

### Prerequisites

- **Role privileges**: The active role must hold the USAGE privilege on the target Custom Runtime Environment,
  along with access to the underlying image repository.
- **Environment status**: The Custom Runtime Environment must be in the RESOLVED state. Environments marked as
  DEPRECATED can’t be used for new Notebooks.

### Usage notes

- When using a CRE alias, the system verifies the image’s SHA digest at runtime. If the underlying image in
  the repository was modified after the CRE was registered, the service submission is rejected to ensure
  reproducibility. In this case, you must recreate the CRE.

### Example

Using the `CODE BUNDLE` grammar, set the custom runtime image through the specification:

Copy code

```
EXECUTE CODE BUNDLE DB.SCHEMA.MY_CODE_BUNDLE
    ENTRYPOINT = 'proj.ipynb'
    WITH SPECIFICATION
    $$
    bundle:
      type: custom
      compute_type: compute_pool
      language: python
      compute_options:
        compute_pool: SYSTEM_COMPUTE_POOL_CPU
        query_warehouse: MY_WH
        runtime_version: 'cre@my_custom_env'
    $$;
```

Using the `NOTEBOOK PROJECT` grammar, which is still supported:

Copy code

```
EXECUTE NOTEBOOK PROJECT DB.SCHEMA.MY_NOTEBOOK_PROJECT
    MAIN_FILE = 'proj.ipynb'
    COMPUTE_POOL = 'SYSTEM_COMPUTE_POOL_CPU'
    RUNTIME = 'cre@my_custom_env'
    QUERY_WAREHOUSE = 'MY_WH';
```

## Custom Runtime Environments SQL reference

A Custom Runtime Environment (CRE) is a Snowflake object that references a custom container image stored in an
SPCS image repository. Use the following SQL commands to create, modify, view, and delete custom runtime environments.

### CREATE CUSTOM RUNTIME ENVIRONMENT

Creates a new custom runtime environment in your account.

#### Syntax

Copy code

```
CREATE [ OR REPLACE ] CUSTOM RUNTIME ENVIRONMENT <name>
    IMAGE_PATH = '<image_path_in_repository>'
    BASE_IMAGE_TYPE = { CPU | GPU }
```

#### Required parameters

**name**

String that specifies the identifier (the name) for the custom runtime environment; it must
be unique for your account. Quoted names for special characters or case-sensitive names aren’t
supported.

**IMAGE\_PATH = ‘<image\_path>’**

Specifies the logical path to the image in the Snowflake image repository (for example,
`'/db/schema/repo/image:tag'`).

**BASE\_IMAGE\_TYPE = { CPU | GPU }**

Specifies the hardware optimization of the image. This must match the hardware requirements
of the base image used to build the custom image.

#### Access control requirements

| Privilege | Object |
| --- | --- |
| Create Custom Runtime Environment | Account |

Expand

Show lessSee more

#### Usage notes

- Executing this command triggers an automated server-side validation job. If the validation fails, the custom
  runtime environment isn’t created.
- To avoid failures during creation, validate your image locally using client-side validation before running this
  command. See [Client-side image validation](#label-client-side-image-validation).
- All custom images must be derived from an official Snowflake ML base image.

#### Examples

Copy code

```
CREATE CUSTOM RUNTIME ENVIRONMENT my_cre
    IMAGE_PATH = '/mydb/myschema/my_repo/sklearn_custom:v1'
    BASE_IMAGE_TYPE = CPU;
```

### ALTER CUSTOM RUNTIME ENVIRONMENT

Updates the lifecycle status of an existing custom runtime environment.

#### Syntax

Copy code

```
ALTER CUSTOM RUNTIME ENVIRONMENT <name> SET
    CRE_STATUS = { RESOLVED | DEPRECATED }
```

#### Parameters

**name**

Specifies the identifier for the custom runtime environment to alter. Quoted names for special characters or case-sensitive names aren’t
supported.

**CRE\_STATUS = { RESOLVED | DEPRECATED }**

Updates the availability of the environment.

- **RESOLVED**: The environment is active and can be used in ML Jobs or Notebooks.
- **DEPRECATED**: The environment remains visible but can no longer be used for new ML Job submissions or Notebooks.

#### Access control requirements

| Privilege | Object |
| --- | --- |
| MODIFY | Custom Runtime Environment |

Expand

Show lessSee more

#### Examples

Copy code

```
ALTER CUSTOM RUNTIME ENVIRONMENT my_cre SET CRE_STATUS = DEPRECATED;
```

### DESCRIBE CUSTOM RUNTIME ENVIRONMENT

Retrieves detailed information about a specific custom runtime environment.

#### Syntax

Copy code

```
DESC[RIBE] CUSTOM RUNTIME ENVIRONMENT <name>
```

#### Parameters

**name**

Specifies the identifier for the custom runtime environment to describe. Quoted names for special characters or case-sensitive names aren’t
supported.

#### Output

| Column | Description |
| --- | --- |
| name | Custom runtime environment name. |
| image\_name | Image name. |
| tag | Image tag. |
| digest | SHA256 digest of the image. |
| created\_on | Date and time when the custom runtime environment was created. |
| updated\_on | Date and time when the custom runtime environment was last updated using ALTER CUSTOM RUNTIME ENVIRONMENT. |
| owner | Role that owns the custom runtime environment. |
| cre\_status | State of the custom runtime environment. |
| base\_image\_type | The hardware type (CPU or GPU). |
| image | Image path in the image repository. |

Expand

Show lessSee more

#### Access control requirements

| Privilege | Object |
| --- | --- |
| MONITOR | Custom Runtime Environment |

Expand

Show lessSee more

#### Examples

Copy code

```
DESCRIBE CUSTOM RUNTIME ENVIRONMENT my_sklearn_env;
```

### SHOW CUSTOM RUNTIME ENVIRONMENTS

Lists the custom runtime environments that you have access to.

#### Syntax

Copy code

```
SHOW CUSTOM RUNTIME ENVIRONMENTS;
```

#### Output

| Column | Description |
| --- | --- |
| name | Custom runtime environment name. |
| image\_name | Image name. |
| tag | Image tag. |
| digest | SHA256 digest of the image. |
| created\_on | Date and time when the custom runtime environment was created. |
| updated\_on | Date and time when the custom runtime environment was last updated using ALTER CUSTOM RUNTIME ENVIRONMENT. |
| owner | Role that owns the custom runtime environment. |
| cre\_status | State of the custom runtime environment. |
| base\_image\_type | The hardware type (CPU or GPU). |
| image | Image path in the image repository. |

Expand

Show lessSee more

#### Access control requirements

| Privilege | Object |
| --- | --- |
| Any one of: OWNERSHIP, USAGE, or MONITOR | Custom Runtime Environment |

Expand

Show lessSee more

#### Usage notes

- The command only returns objects for which the current role has been granted at least one access privilege.
- The command returns a maximum of 10,000 records for the specified object type, as dictated by the access privileges
  for the role used to execute the command. Records above the 10,000-record limit aren’t returned, even with a
  filter applied.

#### Examples

Copy code

```
SHOW CUSTOM RUNTIME ENVIRONMENTS;
```

### DROP CUSTOM RUNTIME ENVIRONMENT

Removes a custom runtime environment from the account.

#### Syntax

Copy code

```
DROP CUSTOM RUNTIME ENVIRONMENT [ IF EXISTS ] <name>
```

#### Parameters

**name**

Specifies the identifier for the custom runtime environment to drop. Quoted names for special characters or case-sensitive names aren’t
supported.

#### Access control requirements

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Custom Runtime Environment |

Expand

Show lessSee more

#### Usage notes

- Dropping a custom runtime environment only removes the Snowflake metadata object. The actual underlying container
  image remains in your SPCS image repository.
- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

#### Examples

Copy code

```
DROP CUSTOM RUNTIME ENVIRONMENT my_sklearn_env;
```
