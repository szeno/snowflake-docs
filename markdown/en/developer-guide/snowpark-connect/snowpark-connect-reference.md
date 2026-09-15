# Snowpark Connect for Spark package reference

This page documents the public Python API of the `snowpark-connect` package. It covers server
startup, session initialization, and Snowflake-specific session helpers.

Install the package from [PyPI](https://pypi.org/project/snowpark-connect/):

Copy code

```
pip install snowpark-connect
```

## Package exports

The `snowflake.snowpark_connect` package exports the following symbols:

| Export | Description |
| --- | --- |
| `init_spark_session` | Start the server and return a ready-to-use `SparkSession`. This is the most common entry point. |
| `start_session` | Start the gRPC server without creating a client session. |
| `get_session` | Return a `SparkSession` from an already-running server. |
| `skip_session_configuration` | Skip the automatic `ALTER SESSION SET` parameter bundle that Snowpark Connect for Spark applies at startup. |

Expand

Show lessSee more

## Server lifecycle

### init\_spark\_session

Initialize and return a `SparkSession` connected to Snowflake. This is the most common entry
point. It starts the Snowpark Connect for Spark server (if it isn’t already running) and returns a ready-to-use
session.

Copy code

```
def init_spark_session(
    conf: SparkConf = None,
    connection_parameters: dict[str, str] | None = None,
    app_name: str | None = None,
) -> SparkSession
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `conf` | `SparkConf` | `None` | Optional Spark configuration object. |
| `connection_parameters` | `dict` | `None` | Connection parameters for the Snowpark session (for example, `connection_name`, `account`, `user`, `password`, `host`, `warehouse`, `database`, `schema`). If not provided, the connection resolver determines which connection to use from `connections.toml`. Not supported inside `snowpark-submit` jobs. |
| `app_name` | `str` | `None` | Application name for the Snowflake session. If not provided, a default is derived from the caller’s filename and a timestamp. |

Expand

Show lessSee more

**Returns:** `SparkSession` connected to Snowflake.

### start\_session

Start the Snowpark Connect for Spark gRPC server. This is a no-op if the server is already running. Use this when
you need to control the server lifecycle separately from session creation, for example when running
a long-lived server process for Scala clients.

Copy code

```
def start_session(
    is_daemon: bool = True,
    remote_url: str | None = None,
    tcp_port: int | None = None,
    unix_domain_socket: str | None = None,
    stop_event: threading.Event = None,
    snowpark_session: snowpark.Session | None = None,
    connection_parameters: dict[str, str] | None = None,
    max_grpc_message_size: int = 134217728,
    app_name: str | None = None,
) -> threading.Thread | None
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `is_daemon` | `bool` | `True` | When `True`, the server shuts down automatically when the main program exits. Set to `False` for a standalone, long-running server. |
| `remote_url` | `str` | `None` | A `sc://` URL to start the server on. Mutually exclusive with `tcp_port` and `unix_domain_socket`. |
| `tcp_port` | `int` | `None` | TCP port for the gRPC server. Mutually exclusive with `remote_url` and `unix_domain_socket`. |
| `unix_domain_socket` | `str` | `None` | Path to a Unix domain socket for the gRPC server. Mutually exclusive with `remote_url` and `tcp_port`. |
| `stop_event` | `threading.Event` | `None` | When `set()` is called, the server shuts down. Only works when `is_daemon=True`. |
| `snowpark_session` | `snowpark.Session` | `None` | An existing Snowpark session to reuse (for example, from a stored procedure environment). Can’t be used together with `connection_parameters`. |
| `connection_parameters` | `dict` | `None` | Connection parameters for creating a Snowpark session. Can’t be used together with `snowpark_session`. |
| `max_grpc_message_size` | `int` | `134217728` | Maximum gRPC message size in bytes (default 128 MiB). |
| `app_name` | `str` | `None` | Application name registered with the Snowflake session. |

Expand

Show lessSee more

**Returns:** `threading.Thread` when `is_daemon=True`, or `None` when `is_daemon=False`
(blocks until the server stops).

### get\_session

Return a `SparkSession` connected to a running Snowpark Connect for Spark server. The server must already be
started via `start_session` or `init_spark_session`.

Copy code

```
def get_session(
    url: str | None = None,
    conf: SparkConf = None,
) -> SparkSession
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | `str` | `None` | Spark Connect server URL. Uses the default server URL if not provided. |
| `conf` | `SparkConf` | `None` | Optional Spark configuration object. |

Expand

Show lessSee more

**Returns:** `SparkSession`

**Raises:** `RuntimeError` if the server hasn’t been started.

### execute\_jar

Run a Java or Scala JAR inside the Snowpark Connect for Spark server process. This function manages the full
lifecycle: it sets up the classpath, starts the server and JVM, executes the JAR’s main class, and
shuts everything down when the application finishes.

Copy code

```
from snowflake.snowpark_connect.server import execute_jar

execute_jar(
    jar_path: str,
    main_class: str,
    jar_args: list[str] | None = None,
    additional_jars: list[str] | None = None,
    tcp_port: int | None = None,
    jvm_options: list[str] | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `jar_path` | `str` | (required) | Path to the application JAR file. |
| `main_class` | `str` | (required) | Fully qualified class name (for example, `com.example.MyApp`). |
| `jar_args` | `list[str]` | `None` | Arguments forwarded to the application’s `main` method. |
| `additional_jars` | `list[str]` | `None` | Dependency JARs or globs added to the classpath (for example, `["/path/to/gson.jar", "/path/to/lib/*.jar"]`). |
| `tcp_port` | `int` | `None` | gRPC server port (defaults to `15002`). |
| `jvm_options` | `list[str]` | `None` | JVM flags (for example, `["-Xmx4g", "-Xms1g"]`). |

Expand

Show lessSee more

Note

`execute_jar` isn’t exported from the top-level package. Import it directly from
`snowflake.snowpark_connect.server`.

### skip\_session\_configuration

Control whether Snowpark Connect for Spark runs `ALTER SESSION SET` for its standard parameter bundle at
startup. When set to `True`, you’re responsible for setting the required session parameters
manually. This is useful in restricted environments such as some Native App stored procedures.

Copy code

```
def skip_session_configuration(skip: bool) -> None
```

## SnowflakeSession

The `SnowflakeSession` class wraps a `SparkSession` to provide Snowflake SQL pass-through and
helper methods for switching database, schema, role, and warehouse. Use it when you need to run
Snowflake-specific SQL that Spark’s parser doesn’t support.

Copy code

```
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession
```

### Constructor

Copy code

```
sf = SnowflakeSession(spark_session: SparkSession)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `spark_session` | `SparkSession` | The Spark Connect session to wrap. |

Expand

Show lessSee more

### sql

Execute Snowflake-specific SQL directly against Snowflake. This bypasses the Spark SQL parser and
sends the statement directly to Snowflake, allowing Snowflake-specific syntax that Spark doesn’t
support.

Copy code

```
sf.sql(sql_stmt: str) -> DataFrame
```

| Parameter | Type | Description |
| --- | --- | --- |
| `sql_stmt` | `str` | The Snowflake SQL statement to execute. |

Expand

Show lessSee more

**Returns:** `pyspark.sql.DataFrame`

### use\_database

Switch the active database for the Snowflake session.

Copy code

```
sf.use_database(database: str, preserve_case: bool = False) -> DataFrame
```

### use\_schema

Switch the active schema for the Snowflake session.

Copy code

```
sf.use_schema(schema: str, preserve_case: bool = False) -> DataFrame
```

### use\_role

Switch the active role for the Snowflake session.

Copy code

```
sf.use_role(role: str, preserve_case: bool = False) -> DataFrame
```

### use\_warehouse

Switch the active warehouse for the Snowflake session.

Copy code

```
sf.use_warehouse(warehouse: str, preserve_case: bool = False) -> DataFrame
```

All four `use_*` methods accept a `preserve_case` parameter. When set to `True`, the
identifier is wrapped in double quotes to preserve its original casing. By default, Snowflake
uppercases unquoted identifiers.

## Examples

### Minimal setup

If your `~/.snowflake/connections.toml` has a default connection configured, no parameters
are needed:

Copy code

```
from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session()
df = spark.sql("SELECT 1 AS value")
df.show()
```

### Connecting with explicit credentials

Copy code

```
from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session(connection_parameters={
    "account": "myaccount",
    "user": "myuser",
    "password": "mypassword",
    "warehouse": "my_wh",
    "database": "my_db",
    "schema": "my_schema",
})
```

### Connecting with a named connection

Copy code

```
from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session(connection_parameters={
    "connection_name": "my_dev_connection",
})
```

### Setting an application name

The app name is registered as a query tag in Snowflake
(`Spark-Connect-App-Name=my-etl-pipeline`), making it easy to identify queries in the query
history.

Copy code

```
from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session(app_name="my-etl-pipeline")
```

### Passing Spark configuration

Copy code

```
from pyspark import SparkConf
from snowflake.snowpark_connect import init_spark_session

conf = SparkConf()
conf.set("spark.sql.session.timeZone", "UTC")
conf.set("spark.sql.ansi.enabled", "true")

spark = init_spark_session(conf=conf)
```

### Separate server and session lifecycle

Use this pattern when you want the server to outlive individual sessions, or when multiple sessions
share the same server:

Copy code

```
from snowflake.snowpark_connect import start_session, get_session

start_session(is_daemon=True, tcp_port=15002)

spark = get_session()
spark.sql("SELECT current_timestamp()").show()
```

### Long-running standalone server

This blocks the calling thread and is useful for running the server as a service:

Copy code

```
from snowflake.snowpark_connect import start_session

start_session(is_daemon=False, tcp_port=15002)
```

### Graceful shutdown with stop\_event

Copy code

```
import threading
from snowflake.snowpark_connect import start_session, get_session

stop = threading.Event()
start_session(is_daemon=True, tcp_port=15002, stop_event=stop)

spark = get_session()
spark.sql("SELECT 1").show()

stop.set()
```

### Using an existing Snowpark session

In stored procedure environments where a Snowpark session is already available:

Copy code

```
from snowflake.snowpark_connect import start_session, get_session

start_session(snowpark_session=existing_snowpark_session)
spark = get_session()
```

### Snowflake SQL pass-through

Execute Snowflake-specific SQL that Spark’s parser doesn’t support:

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession

spark = init_spark_session()
sf = SnowflakeSession(spark)

sf.sql("CREATE OR REPLACE TABLE test_table (id INT, name STRING)")
sf.sql("SHOW TABLES IN SCHEMA public").show()
sf.sql("DESCRIBE TABLE test_table").show()
```

### Switching database, schema, role, and warehouse

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession

spark = init_spark_session()
sf = SnowflakeSession(spark)

sf.use_database("analytics")
sf.use_schema("public")
sf.use_role("analyst_role")
sf.use_warehouse("compute_wh")

spark.sql("SELECT * FROM my_table").show()
```

### Preserving case in identifiers

Snowflake uppercases unquoted identifiers by default. Use `preserve_case=True` to wrap names in
double quotes:

Copy code

```
sf.use_database("MyMixedCaseDB", preserve_case=True)
sf.use_schema("camelCaseSchema", preserve_case=True)
```

### Running a Java or Scala JAR

Copy code

```
from snowflake.snowpark_connect.server import execute_jar

execute_jar(
    jar_path="my-spark-app.jar",
    main_class="com.example.MySparkApp",
    jar_args=["--input", "@my_stage/data", "--output", "@my_stage/results"],
    additional_jars=["/path/to/deps/*.jar"],
    jvm_options=["-Xmx4g", "-Xms1g"],
)
```

### Skipping automatic session configuration

Use this when you need full control over the Snowflake session parameters:

Copy code

```
from snowflake.snowpark_connect import skip_session_configuration, init_spark_session

skip_session_configuration(True)
spark = init_spark_session()
```
