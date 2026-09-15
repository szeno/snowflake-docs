# Snowpark Connect for Spark Java/Scala client reference

This page documents the public Java API of the Snowpark Connect for Spark Java/Scala client library. It covers
session creation, Snowflake SQL pass-through, and environment configuration.

All classes are in the `com.snowflake.snowpark_connect.client` package.

Get the library from Maven Central:

- [snowpark-connect-java-client\_2.12](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.12)
- [snowpark-connect-java-client\_2.13](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.13)

## JVM module system arguments

On Java 9 and later, the module system restricts reflective access to internal APIs that Apache Arrow
(used by Spark Connect) requires. Add the following JVM arguments when running your application:

```
--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED
--add-opens=java.base/jdk.internal.misc=org.apache.arrow.memory.core,ALL-UNNAMED
--add-opens=jdk.unsupported/sun.misc=org.apache.arrow.memory.core,ALL-UNNAMED
```

## Package exports

The `com.snowflake.snowpark_connect.client` package exports the following public classes:

| Export | Description |
| --- | --- |
| `SnowparkConnectSession` | Entry point for building a `SparkSession`. Use `builder()` for configuration or `getOrCreate()` for a default singleton session. |
| `SnowflakeSession` | Wraps a `SparkSession` to provide Snowflake SQL pass-through and helpers for switching database, schema, role, and warehouse. |
| `SnowparkConnectServerException` | Runtime exception thrown when the server can’t be started or communicated with. |

Expand

Show lessSee more

## SnowparkConnectSession

Entry point for building a `SparkSession` connected to a Snowpark Connect for Spark server. This is the most
common entry point for Java and Scala applications.

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
```

### builder

Returns a new `SnowparkConnectSessionBuilder` for configuring the session.

Copy code

```
public static SnowparkConnectSessionBuilder builder()
```

**Returns:** `SnowparkConnectSessionBuilder`

### getOrCreate

Returns the singleton `SparkSession` with default configuration. Equivalent to
`SnowparkConnectSession.builder().getOrCreate()`.

Copy code

```
public static SparkSession getOrCreate()
```

**Returns:** `SparkSession`

**Throws:** `SnowparkConnectServerException` if the server can’t be started (local mode only).

## SnowparkConnectSessionBuilder

Builder that produces a `SparkSession` connected to a Snowpark Connect for Spark server. Handles environment
detection, automatic server creation, and Spark config forwarding.

Resolution order for the server URL:

1. `SPARK_REMOTE` environment variable is set: connect directly to that URL.
2. `SNOWPARK_SUBMIT_JOB=true`: connect to the sidecar server at `sc://localhost:15002`.
3. Auto mode: launch a Python server subprocess using the configured venv.

### appName

Set the application name, forwarded to `SparkSession.Builder.appName()`. The app name is
registered as a query tag in Snowflake (`Spark-Connect-App-Name=<name>`), making it easy to
identify queries in the query history.

Copy code

```
public SnowparkConnectSessionBuilder appName(String name)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `name` | `String` | `null` | Application name for the Snowflake session. |

Expand

Show lessSee more

### config

Set Spark configuration properties, forwarded to `SparkSession.Builder.config()`.

Copy code

```
public SnowparkConnectSessionBuilder config(String key, String value)
public SnowparkConnectSessionBuilder config(String key, long value)
public SnowparkConnectSessionBuilder config(String key, double value)
public SnowparkConnectSessionBuilder config(String key, boolean value)
public SnowparkConnectSessionBuilder config(Map<String, ?> map)
public SnowparkConnectSessionBuilder config(scala.collection.Map<String, ?> map)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `key` | `String` | (required) | Spark configuration property name. |
| `value` | `String`, `long`, `double`, or `boolean` | (required) | Spark configuration property value. |
| `map` | `Map<String, ?>` or `scala.collection.Map<String, ?>` | (required) | Multiple configuration properties at once. Both Java and Scala map types are accepted. |

Expand

Show lessSee more

### pythonVenv

Set the path to the Python virtual environment containing the `snowpark-connect` package. This
is forwarded to the server builder if no explicit server is provided and `SPARK_REMOTE` is not
set.

Copy code

```
public SnowparkConnectSessionBuilder pythonVenv(String path)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `path` | `String` | `null` | Path to a Python virtual environment. If not set, falls back to the `SNOWPARK_CONNECT_PYTHON_VENV` environment variable, then to system Python. |

Expand

Show lessSee more

### getOrCreate

Returns a `SparkSession` connected to a Snowpark Connect for Spark server. Delegates to the open source
`SparkSession.Builder.getOrCreate()`, which caches sessions by connection configuration.

Copy code

```
public SparkSession getOrCreate()
```

**Returns:** `SparkSession`

**Throws:** `SnowparkConnectServerException` if the server can’t be started (local mode only).

## SnowflakeSession

The `SnowflakeSession` class wraps a `SparkSession` to provide Snowflake SQL pass-through and
helper methods for switching database, schema, role, and warehouse. Use it when you need to run
Snowflake-specific SQL that Spark’s parser doesn’t support.

Copy code

```
import com.snowflake.snowpark_connect.client.SnowflakeSession;
```

### Constructor

Copy code

```
SnowflakeSession sf = new SnowflakeSession(sparkSession);
```

| Parameter | Type | Description |
| --- | --- | --- |
| `sparkSession` | `SparkSession` | The Spark Connect session to wrap. Must not be null. |

Expand

Show lessSee more

### sql

Execute Snowflake-specific SQL directly against Snowflake. This bypasses the Spark SQL parser and
sends the statement directly to Snowflake, allowing Snowflake-specific syntax that Spark doesn’t
support.

Copy code

```
public Dataset<Row> sql(String sqlStmt)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `sqlStmt` | `String` | The Snowflake SQL statement to execute. Must not be null. |

Expand

Show lessSee more

**Returns:** `Dataset<Row>`

### useDatabase

Switch the active database for the Snowflake session.

Copy code

```
public Dataset<Row> useDatabase(String database)
public Dataset<Row> useDatabase(String database, boolean preserveCase)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `database` | `String` | (required) | The database name. |
| `preserveCase` | `boolean` | `false` | If `true`, the name is double-quoted to preserve case. |

Expand

Show lessSee more

### useSchema

Switch the active schema for the Snowflake session.

Copy code

```
public Dataset<Row> useSchema(String schema)
public Dataset<Row> useSchema(String schema, boolean preserveCase)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `schema` | `String` | (required) | The schema name. |
| `preserveCase` | `boolean` | `false` | If `true`, the name is double-quoted to preserve case. |

Expand

Show lessSee more

### useRole

Switch the active role for the Snowflake session.

Copy code

```
public Dataset<Row> useRole(String role)
public Dataset<Row> useRole(String role, boolean preserveCase)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `role` | `String` | (required) | The role name. |
| `preserveCase` | `boolean` | `false` | If `true`, the name is double-quoted to preserve case. |

Expand

Show lessSee more

### useWarehouse

Switch the active warehouse for the Snowflake session.

Copy code

```
public Dataset<Row> useWarehouse(String warehouse)
public Dataset<Row> useWarehouse(String warehouse, boolean preserveCase)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `warehouse` | `String` | (required) | The warehouse name. |
| `preserveCase` | `boolean` | `false` | If `true`, the name is double-quoted to preserve case. |

Expand

Show lessSee more

All four `use*` methods pass identifiers unquoted by default, so Snowflake uppercases them. Set
`preserveCase` to `true` to wrap the identifier in double quotes and preserve its original
casing.

## SnowparkConnectServerException

Runtime exception thrown when the Snowpark Connect for Spark server can’t be started, configured, or communicated
with.

Copy code

```
public class SnowparkConnectServerException extends RuntimeException
```

## How it works

The library detects the execution environment at startup:

- If the `SPARK_REMOTE` environment variable is set, the library connects directly to the
  pre-existing server. No Python venv is needed.
- Otherwise, it resolves the Python venv, locates `start_server.py` from the installed
  `snowpark-connect` package, starts a server subprocess on a random free port, and connects
  to it.

Each JVM gets its own server on its own port, so multiple IDE windows work simultaneously without
port collisions. The server process is cleaned up automatically through a JVM shutdown hook.

The same application code runs unchanged whether launched from a local IDE (where the library
starts the Python server automatically) or inside a `snowpark-submit` job (where the server
already exists in a sibling container).

## Environment variables

Only `SNOWPARK_CONNECT_PYTHON_VENV` can be overridden by the public code API.

| Variable | Description | Default |
| --- | --- | --- |
| `SNOWPARK_CONNECT_PYTHON_VENV` | Path to a Python virtual environment containing the `snowpark-connect` package. Overridden by `.pythonVenv()` in code. | (none) |
| `SNOWPARK_CONNECT_VERBOSE` | Set to `true` for verbose server logging. | `false` |
| `SNOWPARK_CONNECT_START_TIMEOUT_SECONDS` | Server startup timeout in seconds. | `60` |
| `SPARK_REMOTE` | Spark Connect URL of a pre-existing server. When set, the library connects directly and doesn’t start a subprocess. Set automatically by `snowpark-submit` and `snowpark-connect-execute-jar`. | (none) |

Expand

Show lessSee more

## Examples

### Minimal setup

If your `~/.snowflake/connections.toml` has a default connection configured, no parameters
are needed:

JavaScala

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;

public class MinimalExample {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("My ETL Job")
            .getOrCreate();

        spark.sql("SELECT * FROM my_table").show();
        spark.stop();
    }
}
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession

object MinimalExample {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("My ETL Job")
      .getOrCreate()

    spark.sql("SELECT * FROM my_table").show()
    spark.stop()
  }
}
```

### Specifying a Python venv

JavaScala

Copy code

```
SparkSession spark = SnowparkConnectSession.builder()
    .pythonVenv("/path/to/scos-venv")
    .appName("My App")
    .getOrCreate();
```

Copy code

```
val spark = SnowparkConnectSession.builder()
  .pythonVenv("/path/to/scos-venv")
  .appName("My App")
  .getOrCreate()
```

Alternatively, set `SNOWPARK_CONNECT_PYTHON_VENV=/path/to/scos-venv` and omit the
`.pythonVenv()` call. This keeps your code environment-independent.

### Passing Spark configuration

JavaScala

Copy code

```
SparkSession spark = SnowparkConnectSession.builder()
    .appName("Configured App")
    .config("spark.sql.caseSensitive", "true")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate();
```

Copy code

```
val spark = SnowparkConnectSession.builder()
  .appName("Configured App")
  .config("spark.sql.caseSensitive", "true")
  .config("spark.sql.session.timeZone", "UTC")
  .getOrCreate()
```

### Switching database, schema, role, and warehouse

JavaScala

Copy code

```
SnowflakeSession sf = new SnowflakeSession(spark);

sf.useDatabase("ANALYTICS");
sf.useSchema("PUBLIC");
sf.useRole("ANALYST_ROLE");
sf.useWarehouse("COMPUTE_WH");

spark.sql("SELECT * FROM my_table").show();
```

Copy code

```
val sf = new SnowflakeSession(spark)

sf.useDatabase("ANALYTICS")
sf.useSchema("PUBLIC")
sf.useRole("ANALYST_ROLE")
sf.useWarehouse("COMPUTE_WH")

spark.sql("SELECT * FROM my_table").show()
```

### Preserving case in identifiers

Snowflake uppercases unquoted identifiers by default. Use `preserveCase` to wrap names in double
quotes:

JavaScala

Copy code

```
sf.useDatabase("MyMixedCaseDB", true);
sf.useSchema("camelCaseSchema", true);
```

Copy code

```
sf.useDatabase("MyMixedCaseDB", true)
sf.useSchema("camelCaseSchema", true)
```

### Default session

The simplest way to get a session with default configuration:

JavaScala

Copy code

```
SparkSession spark = SnowparkConnectSession.getOrCreate();
```

Copy code

```
val spark = SnowparkConnectSession.getOrCreate()
```
