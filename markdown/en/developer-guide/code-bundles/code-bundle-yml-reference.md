# `code_bundle.yml` reference

The `code_bundle.yml` file defines how your Code Bundle runs, including the bundle type, compute type, runtime version, dependencies, secrets, environment variables, and other settings. Place the file in the root of your project directory.

Availability

Scheduling notebooks on compute pools (Snowpark Container Services), the capability previously delivered as Notebook Projects, is generally available. Running on warehouses and submitting Spark jobs (`type: spark`) are in Public Preview. For the full availability breakdown and background on the rename, see [Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

The following table summarizes the most common fields for `type: custom` Code Bundles and where they apply. For Spark bundle properties (`type: spark`), see [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

| Field | Warehouse | Compute pool (Snowpark Container Services) |
| --- | --- | --- |
| `compute_type` | `warehouse` | `compute_pool` |
| `compute_options.runtime_version` | Python version (for example, 3.11) | Container image version (for example, V2.9-CPU-PY3.12) |
| `compute_options.compute_pool` | N/A | Required |
| `compute_options.query_warehouse` | N/A | Optional (for SQL queries inside your script) |
| `properties.requirements_file` | Optional | Optional |
| `env_vars` | Optional | Optional |
| `secrets` | Optional | Optional |
| `external_access_integrations` | Optional | Optional |
| `stage_mounts` | Optional (read-only) | Optional (read and write) |
| `artifact_repositories` | Optional | Optional |

Expand

Show lessSee more

## bundle.type

The `type` property instructs Snowflake how to execute the bundle. The currently supported values are `custom` and `spark`. See [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle) for more details about `type: spark`.

## bundle.compute\_type

The `compute_type` property designates where the Code Bundle runs. The currently supported values are `warehouse` and `compute_pool`.

## bundle.language

The `language` property specifies the runtime language for the Code Bundle.

For `custom` Code Bundles running on the warehouse, the currently supported option is `python`. For `custom` Code Bundles running on compute pools, the currently supported option is `python`.

To run Spark workloads in Python, Scala, or Java using the `spark` bundle type, see [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle#supported-languages-and-runtimes).

## bundle.compute\_options

The `compute_options` object specifies the options of your `compute_type`, for example the compute pool and Python version to run on.

If your Code Bundle is configured to run on the warehouse (with `bundle.compute_type: warehouse`), the bundle is executed on the current warehouse for the session.

### bundle.compute\_options.runtime\_version

The `runtime_version` property specifies the version of the runtime `language` to use. Always quote the value. In YAML, an unquoted version like `3.10` is parsed as the number `3.1`, which can select the wrong runtime.

- The currently supported versions of Python on the warehouse are: `'3.10'`, `'3.11'`, `'3.12'`, `'3.13'`
- The currently supported versions of Python on compute pools follow the pattern `<runtime-version>-<accelerator>-PY<python-version>`. The supported versions are documented in [Snowflake Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases). For example: `V2.9-CPU-PY3.12`.

Use the latest available container runtime version for new Code Bundles. Older versions receive fewer updates, so check [Snowflake Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases) for the current version rather than copying a version from an example.

For `type: spark` bundles, `runtime_version` instead selects the Snowpark Connect for Spark client version, and the Python or Scala runtime is set with `language_version`. See [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

### bundle.compute\_options.compute\_pool

(Only applicable to Code Bundles with `compute_type: compute_pool`)

The `compute_pool` property specifies the compute pool to execute the Code Bundle on. For example: `MY_DB.MY_SCHEMA.MY_COMPUTE_POOL`.

### bundle.compute\_options.query\_warehouse

(Only applicable to Code Bundles with `compute_type: compute_pool`)

The `query_warehouse` property specifies the Snowflake virtual warehouse used for executing SQL and Snowpark queries from the Code Bundle. For example: `MY_DB.MY_SCHEMA.MY_WAREHOUSE`.

## bundle.properties

The `properties` object specifies type-specific properties for the Code Bundle. For example, specifying your `requirements.txt` or `pyproject.toml` file for Snowflake.

For Spark bundle properties (`spark_conf`, `java_dependencies`, `python_files`, and `python_dependencies`), see [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

### bundle.properties.requirements\_file

The `requirements_file` parameter specifies your `requirements.txt` or `pyproject.toml` file when using `type: custom` and `language: python`.

By default, packages are installed from the `snowflake.snowpark.pypi_shared_repository` [artifact repository](/developer-guide/udf/python/udf-python-packages). You can specify an alternate artifact repository under the `artifact_repositories` list.

For example:

Copy code

```
bundle:
  type: custom
  compute_type: compute_pool
  language: python

  compute_options:
    compute_pool: system_compute_pool_cpu
    query_warehouse: SNOWFLAKE_LEARNING_WH
    runtime_version: 'V2.9-CPU-PY3.12'

  properties:
    requirements_file: pyproject.toml
```

## bundle.artifact\_repositories

The `artifact_repositories` list specifies the artifact repository or repositories to use to install Python packages from.

On the warehouse (`compute_type: warehouse`), only one artifact repository can be specified (a list of one entry).

On compute pools (`compute_type: compute_pool`), the Anaconda repository (`snowflake.snowpark.anaconda_shared_repository`) can’t be used.

For example:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python

  compute_options:
    runtime_version: '3.12'

  properties:
    requirements_file: requirements.txt

  artifact_repositories:
    - snowflake.snowpark.anaconda_shared_repository
```

## bundle.external\_access\_integrations

The `external_access_integrations` list specifies one or more [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access) to attach to the Code Bundle.

For example:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python

  compute_options:
    runtime_version: '3.11'

  external_access_integrations:
    - my_db.my_schema.my_eai
```

## bundle.secrets

The `secrets` list specifies one or more [Snowflake secrets](/sql-reference/sql/create-secret) to attach to the Code Bundle.

For example:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python

  compute_options:
    runtime_version: '3.11'

  external_access_integrations:
    - my_db.my_schema.my_eai

  secrets:
    - my_db.my_schema.my_secret
```

## bundle.env\_vars

The `env_vars` property is a list of environment variable key/value pairs to set in the runtime environment. You can use this to configure application code or third-party libraries that fetch configuration settings from environment variables.

For example:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python

  compute_options:
    runtime_version: '3.11'

  env_vars:
    - API_ROOT: 'https://my_org.com/api/v3/'
    - TIMEOUT_MS: '100'
```

## bundle.stage\_mounts

The `stage_mounts` list specifies one or more [Snowflake stages](/sql-reference/sql/create-stage) to mount to the runtime environment. Each stage mount is a named YAML object that specifies the stage to mount and the location in the runtime environment to mount to.

Mounted stages behave differently depending on the compute type:

- On compute pools (`compute_type: compute_pool`), mounted stages are readable and writable.
- On warehouses (`compute_type: warehouse`), mounted stages are read-only.

For example:

Copy code

```
bundle:
  ...

  stage_mounts:
    my_stage:
      stage_url: '@db.schema.stage'
      mount_path: '/mnt/myStage/'

    my_other_stage:
      stage_url: '@db.schema.other_stage/subdir'
      mount_path: '/mnt/myOtherStage/'

    single_file_example:
      stage_url: '@db.schema.stage2/my-file.txt'
      mount_path: '/mnt/stage2/my-file.txt'
```

### stage\_mounts.<mount\_name>.stage\_url

The `stage_url` property specifies the stage path to mount to the corresponding `mount_path`. This can specify an entire stage, a subdirectory of a stage, or a single file.

### stage\_mounts.<mount\_name>.mount\_path

The target directory path inside the Code Bundle runtime to mount the stage to.
