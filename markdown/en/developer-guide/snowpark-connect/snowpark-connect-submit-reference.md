# Snowpark Submit reference

With Snowpark Submit, you can use familiar Spark semantics to run non-interactive, batch-oriented Spark workloads on Snowflake.

Note

`snowpark-submit` supports much of the same functionality as `spark-submit`. However, some functionality has been
omitted because it is not needed when running Spark workloads on Snowflake.

## Syntax

Copy code

```
snowpark-submit
  --name <application_name>
  --exclude-packages <package_to_exclude> [, <package_to_exclude>, ...]
  --py-files <files_to_place_on_path>
  --conf <spark_config_property=value> [<spark_config_property=value> ...]
  --properties-file <path_to_properties_file>
  --help, -h
  --verbose, -v
  --version
  --account <snowflake_account>
  --user <snowflake_user>
  --authenticator <snowflake_authenticator>
  --token-file-path <snowflake_token_file_path>
  --password <snowflake_password>
  --role <snowflake_role>
  --host <snowflake_host>
  --database <snowflake_database_name>
  --schema <snowflake_schema_name>
  --warehouse <snowflake_warehouse_name>
  --compute-pool <snowflake_compute_pool>
  --comment <comment>
  --snowflake-stage <snowflake_stage>
  --external-access-integrations <snowflake_external_access_integrations> [, ...]
  --snowflake-log-level <snowflake_log_level>
  --snowflake-workload-name <snowflake_workload_name>
  --snowflake-connection-name <snowflake_connection_name>
  --snowflake-grpc-max-message-size <message_size>
  --snowflake-grpc-max-metadata-size <metadata_size>
  --workload-status
  --display-logs
  --wait-for-completion
  --jars <jar_files> [, <jar_files>, ...]
  --scala-version <scala_version>
  <application.jar | application.py> [<application_arguments>]
```

## Arguments

`{application.jar | application.py}`
:   Path to a file containing the application and dependencies.

`[{application arguments}]`
:   Application-specific arguments passed to the application’s main method.

## Options

`--class CLASS_NAME`
:   Your application’s main class (for Java and Scala applications). This option is required if the main class is not specified in the application JAR.

`--conf [PROP=VALUEPROP=VALUE ...]`
:   Arbitrary Spark configuration property.

`--exclude-packages [EXCLUDE_PACKAGES ...]`
:   Comma-separated list of groupId:artifactId pairs, to exclude while resolving the dependencies provided in `--packages` to avoid
    dependency conflicts.

`--help, -h`
:   Show help message and exit.

`--jars JAR`
:   Comma-separated list of `.jar` files to include. This can include the workload JAR itself, if a class finder is not used.

Note

The files are not automatically included in the classpath and need to be explicitly registered using `addArtifact`.

`--name NAME`
Name of your application.

`--properties-file FILE`
:   Path to a file from which to load extra properties. If not specified, this will look for conf/spark-defaults.conf.

`--py-files PY_FILES`
:   Comma-separated list of `.zip`, `.egg`, or `.py` files to place on the PYTHONPATH for Python apps.

`--verbose, -v`
:   Print additional debug output.

`--version`
:   Print the version of current Spark.

### Snowflake specific options

`--account SNOWFLAKE_ACCOUNT`
:   Snowflake account to use. Overrides the account in the `connections.toml` file if specified.

`--authenticator SNOWFLAKE_AUTHENTICATOR`
:   Authenticator for Snowflake login. Overrides the authenticator in the `connections.toml` file if specified. If not specified,
    defaults to user password authenticator.

`--comment COMMENT`
:   A message associated with the workload. Can be used to identify the workload in Snowflake.

`--compute-pool SNOWFLAKE_COMPUTE_POOL`
:   Snowflake compute pool for running the provided workload. Overrides the compute pool in the `connections.toml` file if specified.

`--database SNOWFLAKE_DATABASE_NAME`
:   Snowflake database to be used in the session. Overrides the database in the `connections.toml` file if specified.

`--display-logs`
:   Whether to print application logs to console when `--workload-status` is specified.

`--external-access-integrations [SNOWFLAKE_EXTERNAL_ACCESS_INTEGRATIONS ...]`
:   Snowflake external access integrations required by the workload.

`--host SNOWFLAKE_HOST`
:   Host for snowflake deployment. Overrides the host in the `connections.toml` file if specified.

`--password SNOWFLAKE_PASSWORD`
:   Password for the Snowflake user. Overrides the password in the `connections.toml` file if specified.

`--requirements-file REQUIREMENTS_FILE`
:   Path to a `requirements.txt` file containing Python package dependencies to install before running the workload. Requires
    external access integration for PyPI. This parameter will not function if you also specify the `--snowflake-stage` parameter.

`--role SNOWFLAKE_ROLE`
:   Snowflake role to use. Overrides the role in the `connections.toml` file if specified.

`--schema SNOWFLAKE_SCHEMA_NAME`
:   Snowflake schema to use in the session. Overrides the schema in the `connections.toml` file if specified.

`--snowflake-connection-name SNOWFLAKE_CONNECTION_NAME`
:   Name of the connection in `connections.toml` file to use as the base configuration. Command-line arguments override any
    values from the `connections.toml` file.

`--snowflake-grpc-max-message-size MESSAGE_SIZE`
:   Maximum message size, in bytes, for gRPC communication in Snowpark Submit.

`--snowflake-grpc-max-metadata-size METADATA_SIZE`
:   Maximum metadata size, in bytes, for gRPC communication in Snowpark Submit.

`--snowflake-log-level SNOWFLAKE_LOG_LEVEL`
:   Log level for Snowflake event table: `'INFO'`, `'ERROR'`, `'NONE'`. (Default: INFO).

`--snowflake-stage SNOWFLAKE_STAGE`
:   Snowflake stage where workload files are uploaded.

`--snowflake-workload-name SNOWFLAKE_WORKLOAD_NAME`
:   Name of the workload to be run in Snowflake.

`--token-file-path SNOWFLAKE_TOKEN_FILE_PATH`
:   Path to a file containing the OAuth token for Snowflake. Overrides the token file path in the `connections.toml` file if specified.

`--user SNOWFLAKE_USER`
:   Snowflake user to use. Overrides the user in the `connections.toml` file if specified.

`--wait-for-completion`
:   In cluster mode, when specified, run the workload in blocking mode and wait for completion.

`--warehouse SNOWFLAKE_WAREHOUSE_NAME`
:   Snowflake warehouse to use in the session. Overrides the warehouse in the `connections.toml` file if specified.

`--wheel-files WHEEL_FILES`
:   Comma-separated list of .whl files to install before running the Python workload. Used for private dependencies not available on PyPI.

`--workload-status`
:   Print the detailed status of the workload.

`--scala-version SCALA_VERSION`
:   Scala version to use. Can be `2.12` or `2.13`. The default value is `2.12`.

## Common option examples

### Application deployment

Snowflake’s Snowpark Container Services (SPCS) is the primary infrastructure for running your Spark applications. You need to have created
an SPCS compute pool in advance.

#### Basic Python application

To deploy a basic Python application in cluster mode:

Copy code

```
snowpark-submit \
  --snowflake-workload-name MY_PYTHON_JOB \
  --snowflake-connection-name MY_CONNECTION_CONFIG_NAME
  app.py arg1 arg2
```

#### Basic Scala application

To deploy a basic Scala application in cluster mode, use a command such as the following:

Copy code

```
snowpark-submit \
  --class com.example.MainClass \
  --snowflake-workload-name MY_SCALA_JOB \
  --snowflake-connection-name MY_CONNECTION_CONFIG_NAME
  app.jar arg1 arg2
```

You can omit the `--class` option if you specified the main class in the application JAR.

##### Specifying the Scala version

Scala 2.12 and 2.13 are supported, with the default version being 2.12. If the application is built with Scala 2.13, the Scala version must be specified in the CLI and the script.

Copy code

```
snowpark-submit \
  --scala-version 2.13 \
  --snowflake-workload-name MY_SCALA_JOB \
  --snowflake-connection-name MY_CONNECTION_CONFIG_NAME
  app.jar arg1 arg2
```

You must specify the Scala version in the application code:

Copy code

```
// Directly in the session builder
val spark = SparkSession.builder()
  .remote("sc://localhost:15002")
  .config("snowpark.connect.scala.version", "2.13")
  .getOrCreate()

// Via session configuration
spark.conf.set("snowpark.connect.scala.version", "2.13")
```

### Authentication

Snowpark Submit offers various methods for authenticating with Snowflake. You must use at least one method. Connection profile and
direct authentication can be used together or separately. The command-line option overrides corresponding fields in connection profile
when it is also present.

### Connection profile

To use a pre-configured Snowflake connection profile:

Copy code

```
snowpark-submit \
  --snowflake-connection-name my_connection \
  --snowflake-workload-name MY_JOB \
  app.py
```

### Direct authentication

#### Username and password

To provide authentication details directly in the command:

Copy code

```
snowpark-submit \
  --host myhost \
  --account myaccount \
  --user myuser \
  --password mypassword \
  --role myrole \
  --snowflake-workload-name MY_JOB \
  app.py
```

#### OAuth

To authenticate by using an OAuth token:

Copy code

```
snowpark-submit \
  --host myhost \
  --account myaccount \
  --authenticator oauth \
  --token-file-path /path/to/token.txt \
  --snowflake-workload-name MY_JOB \
  --compute-pool MY_COMPUTE_POOL \
  app.py
```

### Snowflake resources

To specify the Snowflake database, schema, warehouse, and compute pool for your job:

Copy code

```
snowpark-submit \
  --database MY_DB \
  --schema MY_SCHEMA \
  --warehouse MY_WH \
  --snowflake-workload-name MY_JOB \
  --snowflake-connection-name MY_CONNECTION \
  app.py
```

### Snowflake stages

You can use Snowpark Submit to store and access files directly on a Snowflake stage.

To submit a job using a file on a Snowflake stage:

Copy code

```
snowpark-submit \
  --snowflake-stage @my_stage \
  --snowflake-workload-name MY_JOB \
  --snowflake-connection-name MY_CONNECTION \
  @my_stage/app.py
```

### Dependencies management

You can manage your application’s dependencies.

#### Python dependencies

To specify additional Python files or archives that are needed by your application:

Copy code

```
snowpark-submit \
  --py-files dependencies.zip,module.py \
  --snowflake-workload-name MY_PYTHON_JOB \
  --snowflake-connection-name MY_CONNECTION \
  app.py
```

#### Java or Scala dependencies

To include external JAR files for Java or Scala applications:

Copy code

```
snowpark-submit \
  --jars dep1.jar,dep2.jar \
  --snowflake-workload-name MY_SCALA_JOB \
  --snowflake-connection-name MY_CONNECTION \
  --compute-pool MY_COMPUTE_POOL \
  app.jar
```

When you add dependencies via the `--jars` option, you must explicitly register them using `addArtifact`.

Copy code

```
spark.addArtifact("dep1.jar")
spark.addArtifact("dep2.jar")
```

It’s also possible to use staged JAR files. These files do not have to be specified in the `--jars` option.

Copy code

```
spark.conf.set("snowpark.connect.udf.java.imports", "[@mystage/dep1.jar, @mystage/dep2.jar]")
```

### Monitoring and control

You can monitor and control your Snowpark Submit jobs effectively.

#### Waiting for job completion

By default, Snowpark Submit starts the job and returns immediately. To run in blocking mode and wait for the job to finish:

Copy code

```
snowpark-submit \
  --snowflake-connection-name my_connection \
  --snowflake-workload-name MY_JOB \
  --wait-for-completion \
  app.py
```

The `wait-for-completion` flag causes the command to block until the job completes (either successfully or with failure), showing
periodic status updates. This is useful for workflows where you need to ensure a job completes before proceeding with other tasks,
such as when you use Apache Airflow.

#### Checking workload status

Check the status of a workload (running or completed).

Copy code

```
snowpark-submit --snowflake-connection-name my_connection --snowflake-workload-name MY_JOB --workload-status
```

This command returns the following information about the workload:

- Current state (`DEPLOYING`, `RUNNING`, `SUCCEEDED`, `FAILED`)
- Start time and duration
- Service details

#### Viewing application logs

To view detailed logs along with the workload status:

Copy code

```
snowpark-submit --snowflake-connection-name my_connection --snowflake-workload-name MY_JOB --workload-status --display-logs
```

The `display-logs` flag will fetch and print the application’s output logs to the console. Using these logs, you can perform the
following tasks:

- Debug application errors
- Monitor execution progress
- View application output

Note

There is a small latency, from a few seconds to a minute, for logs to be ready for fetching. When an event table is not used to
store log data, logs are retained for a short period of time, such as five minutes or less.

### Advanced configuration

Fine-tune your Snowpark Submit jobs with advanced configurations.

#### External access integration

Connect to external services from your Spark application:

Copy code

```
snowpark-submit \
  --external-access-integrations "MY_NETWORK_RULE,MY_STORAGE_INTEGRATION" \
  --snowflake-workload-name MY_JOB \
  --snowflake-connection-name my_connection \
  app.py
```

#### Logging level configuration

Control the logging level for your application to the Snowflake event table:

Copy code

```
snowpark-submit \
  --snowflake-log-level INFO \
  --snowflake-workload-name MY_JOB \
  --snowflake-connection-name MY_CONNECTION \
  app.py
```

Options for –snowflake-log-level: INFO, ERROR, NONE.

#### Adding job context

Add a descriptive comment for easier workload identification in Snowflake:

Copy code

```
snowpark-submit \
  --comment "Daily data processing job" \
  --snowflake-workload-name MY_JOB \
  --snowflake-connection-name my_connection \
  app.py
```
