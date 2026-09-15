# Snowpark Connect for Spark execute-jar CLI reference

If you already have a Spark application packaged as a JAR, you can run it against Snowflake without
changing its code by using the `snowpark-connect-execute-jar` command-line tool. This tool is
installed with the `snowpark-connect` package (see [Install Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide-install)).

When you run the tool, it does the following:

1. Adds your application JAR (and any dependency JARs) to the classpath.
2. Starts the local Snowpark Connect for Spark server, which connects to Snowflake using your TOML connection file.
3. Sets the `SPARK_REMOTE` environment variable so that a standard
   `SparkSession.builder().getOrCreate()` call in your application connects to that server
   automatically. No code changes are required.
4. Invokes the `public static void main(String[] args)` method of the class that you specify.
5. Shuts down the server when your application exits.

The required Apache Arrow `--add-opens` JVM arguments are added for you, so you don’t need to
configure them manually.

## Prerequisites

- The `snowpark-connect` package is installed, which provides the `snowpark-connect-execute-jar`
  command. See [Install Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide-install).
- A Java runtime (JDK) is available. Installing `snowpark-connect[jdk]` provides one. Otherwise,
  make sure that a compatible JDK is installed and that it uses the same CPU architecture as Python
  (see [Prerequisites](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide-prereq)).
- A connection is configured in your TOML connection file. See
  [Set up your environment](/developer-guide/snowpark-connect/snowpark-connect-workloads-jupyter#label-snowpark-connect-client-env-setup). The tool uses the `spark-connect` connection if it
  exists. Otherwise, it uses the connection specified by the `SNOWFLAKE_DEFAULT_CONNECTION_NAME`
  environment variable, the `default_connection_name` value in your `connections.toml` file, or a
  connection named `default`.
- Your application is packaged as a JAR that contains a class with a `main(String[] args)` method.
  In that class, obtain the session with the standard Spark builder so that no code changes are
  needed:

  Copy code

  ```
  val spark = SparkSession.builder().getOrCreate()
  ```

## Command options

| Option | Description |
| --- | --- |
| `--jar-file` | Required. Path to the JAR file that contains your main class. |
| `--main-class` | Required. Fully qualified name of the class to run (for example, `com.example.MyApp`). |
| `--jars` | Comma-separated list of additional dependency JARs or glob patterns to add to the classpath. Use this option for a thin JAR whose dependencies aren’t bundled. Separate entries with commas and no spaces. |
| `--port` | TCP port for the local gRPC server. The default is `15002`. Change it if that port is already in use. |
| `--jvm-options` | Additional JVM options, such as heap settings (for example, `--jvm-options="-Xmx4g -Xms1g"`). |
| `--scala-version` | Scala binary version of your JAR, either `2.12` or `2.13`. The default is `2.12`. |
| `--verbose` | Enable verbose (DEBUG) logging. |

Expand

Show lessSee more

Any arguments that you provide after `--` are passed to your application’s `main` method.

## Examples

JavaScala

Build an uber JAR that bundles your dependencies (for example, with the
[Maven Shade plugin](https://maven.apache.org/plugins/maven-shade-plugin/)), then run it:

Copy code

```
mvn package
snowpark-connect-execute-jar \
    --jar-file target/my-app-1.0.0.jar \
    --main-class com.example.MyApp
```

If you build a thin JAR instead, pass its dependency JARs with `--jars`:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file target/my-app-1.0.0.jar \
    --main-class com.example.MyApp \
    --jars /path/to/gson-2.10.1.jar,/path/to/commons-math3-3.6.1.jar
```

Build an uber JAR that bundles your dependencies (for example, with the
[sbt-assembly](https://github.com/sbt/sbt-assembly) plugin), then run it:

Copy code

```
sbt assembly
snowpark-connect-execute-jar \
    --jar-file target/scala-2.12/my-app-assembly-1.0.0.jar \
    --main-class com.example.MyApp
```

If you build a thin JAR instead (for example, with `sbt package`), pass its dependency JARs with
`--jars`:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file target/scala-2.12/my-app_2.12-1.0.0.jar \
    --main-class com.example.MyApp \
    --jars /path/to/gson-2.10.1.jar,/path/to/commons-math3-3.6.1.jar
```

Use a different port when the default (`15002`) is already in use:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file app.jar \
    --main-class com.example.MyApp \
    --port 15010
```

Tune the JVM (for example, heap size):

Copy code

```
snowpark-connect-execute-jar \
    --jar-file app.jar \
    --main-class com.example.MyApp \
    --jvm-options="-Xmx4g -Xms1g"
```

Pass arguments to your application’s `main` method after `--`:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file app.jar \
    --main-class com.example.MyApp \
    -- --input-table MY_TABLE --output-table RESULTS
```

Run a JAR that was built with Scala 2.13:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file target/scala-2.13/my-app_2.13-1.0.0.jar \
    --main-class com.example.MyApp \
    --scala-version 2.13
```

Enable verbose (DEBUG) logging to troubleshoot startup or connection issues:

Copy code

```
snowpark-connect-execute-jar \
    --jar-file app.jar \
    --main-class com.example.MyApp \
    --verbose
```
