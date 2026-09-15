# Develop with a local IDE

You can run Spark workloads interactively from Jupyter Notebooks, VS Code, IntelliJ, or any
Python/Java/Scala interface without needing to manage a Spark cluster. The workloads run on the
Snowflake infrastructure.

To connect, install the `snowpark-connect` Python package, which is required for all languages
(Python, Java, and Scala). For Java and Scala projects, also add the `snowpark-connect-java-client`
Maven dependency. For establishing a connection, use a TOML connection file. This approach handles
server lifecycle, authentication, and session management automatically.

You can run your workload interactively (for example, from a notebook, an IDE, or the PySpark shell),
or you can run a packaged Java or Scala application JAR directly with the
`snowpark-connect-execute-jar` command-line tool. For more information, see
[Running Java or Scala workloads](#label-snowpark-connect-execute-jar-cli).

## Prerequisites

- You have a Snowflake account with access to Snowpark Connect for Spark.
- Python 3.10 or later (earlier than 3.13) is installed. Confirm your version by running `python3 --version`.
- Ensure that your Java and Python installations use the same CPU architecture. For example, if Python is arm64,
  install an arm64 build of Java (not x86\_64).

## Connection configuration

Snowpark Connect for Spark connects to Snowflake using a TOML connection file. You can create this file manually or by using
Snowflake CLI.

If you have Snowflake CLI installed, you can use it to define a connection. Otherwise, you can manually write connection parameters in a `config.toml` file.

### Add a connection by using Snowflake CLI

You can use Snowflake CLI to add connection properties that Snowpark Connect for Spark uses to connect to Snowflake. Your changes are saved to a
`config.toml` file.

1. Run the following command to add a connection:

   Copy code

   ```
   snow connection add
   ```
2. Follow the prompts to define a connection.

   Specify `spark-connect` as the connection name.

   This command adds a connection to your `config.toml` file:

   Copy code

   ```
   [connections.spark-connect]
   host = "example.snowflakecomputing.com"
   port = 443
   account = "example"
   user = "test_example"
   password = "password"
   protocol = "https"
   warehouse = "example_wh"
   database = "example_db"
   schema = "public"
   ```
3. Confirm the connection works:

   Copy code

   ```
   snow connection list
   snow connection test --connection spark-connect
   ```

### Add a connection manually

You can write or update a `connections.toml` file so that your code can connect to Snowpark Connect for Spark on Snowflake.

1. Ensure that the file permissions allow only the owner to read and write:

   Copy code

   ```
   chmod 0600 ~/.snowflake/connections.toml
   ```
2. Edit the file to contain a `[spark-connect]` connection with your specifics:

   Copy code

   ```
   [spark-connect]
   host="my_snowflake_account.snowflakecomputing.com"
   account="my_snowflake_account"
   user="my_user"
   password="&&&&&&&&"
   warehouse="my_wh"
   database="my_db"
   schema="public"
   ```

## Install Snowpark Connect for Spark

Note

The Snowpark Connect for Spark package runs a local gRPC server process that connects to Snowflake using
a single session. Each developer or isolated workload should use its own server process.

PythonJavaScala

Create a Python virtual environment and install the Snowpark Connect for Spark package:

Copy code

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade --force-reinstall 'snowpark-connect[jdk]'
pip install pyspark==3.5.6
```

Note

The Snowpark Connect for Spark package includes a vendored copy of PySpark. However, the vendored copy
doesn’t support IDE features like IntelliSense and requires that you import Snowpark Connect for Spark
before any PySpark imports in your code. To avoid these limitations, install PySpark 3.5.6
as shown above.

The Java/Scala client library manages the Snowpark Connect for Spark Python gRPC server as a child process. You
need both the library and a Python virtual environment with `snowpark-connect` installed.

1. Create a Python virtual environment:

   Copy code

   ```
   python3 -m venv /path/to/scos-venv
   /path/to/scos-venv/bin/pip install snowpark-connect
   ```
2. Add the following dependencies to your `pom.xml`:

   Copy code

   ```
   <!-- Snowpark Connect Java client (Scala 2.12) -->
   <dependency>
    <groupId>com.snowflake</groupId>
    <artifactId>snowpark-connect-java-client_2.12</artifactId>
    <version>1.0.0</version>
   </dependency>

   <!-- Spark Connect client (must be provided separately) -->
   <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-connect-client-jvm_2.12</artifactId>
    <version>3.5.6</version>
   </dependency>
   ```

   The library is available on Maven Central:
   [snowpark-connect-java-client\_2.12](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.12),
   [snowpark-connect-java-client\_2.13](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.13).
3. On Java 9+, add the required `--add-opens` JVM arguments for Apache Arrow compatibility.
   See [JVM module system arguments](/developer-guide/snowpark-connect/snowpark-connect-jvm-reference#label-snowpark-connect-jvm-module-args) for the full list and how to configure them
   in Maven, IntelliJ, or on the command line.
4. Point the library to the venv using one of these methods (in order of precedence):

   - **Code API**: `.pythonVenv("/path/to/scos-venv")` on the session builder
   - **Environment variable**: `SNOWPARK_CONNECT_PYTHON_VENV=/path/to/scos-venv`

   If neither is set, the library falls back to system `python3` (or `python` on Windows)
   and checks whether `snowpark-connect` is importable.

The Java/Scala client library manages the Snowpark Connect for Spark Python gRPC server as a child process. You
need both the library and a Python virtual environment with `snowpark-connect` installed.

1. Create a Python virtual environment:

   Copy code

   ```
   python3 -m venv /path/to/scos-venv
   /path/to/scos-venv/bin/pip install snowpark-connect
   ```
2. Add the following dependencies to your `build.sbt`:

   Copy code

   ```
   libraryDependencies ++= Seq(
     "com.snowflake" %% "snowpark-connect-java-client" % "1.0.0",
     "org.apache.spark" %% "spark-connect-client-jvm" % "3.5.6"
   )
   ```

   The library is available on Maven Central:
   [snowpark-connect-java-client\_2.12](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.12),
   [snowpark-connect-java-client\_2.13](https://central.sonatype.com/artifact/com.snowflake/snowpark-connect-java-client_2.13).
3. On Java 9+, add the required `--add-opens` JVM arguments for Apache Arrow compatibility.
   See [JVM module system arguments](/developer-guide/snowpark-connect/snowpark-connect-jvm-reference#label-snowpark-connect-jvm-module-args) for the full list and how to configure them
   in sbt, IntelliJ, or on the command line.
4. Point the library to the venv using one of these methods (in order of precedence):

   - **Code API**: `.pythonVenv("/path/to/scos-venv")` on the session builder
   - **Environment variable**: `SNOWPARK_CONNECT_PYTHON_VENV=/path/to/scos-venv`

   If neither is set, the library falls back to system `python3` (or `python` on Windows)
   and checks whether `snowpark-connect` is importable.

## Start a session and run code

Once you have Snowpark Connect for Spark installed and an authenticated connection in place, start a session and
run Spark code.

PythonJavaScala

Start the Snowpark Connect for Spark server and create a session:

Copy code

```
from snowflake import snowpark_connect
spark = snowpark_connect.init_spark_session()
```

Then run Spark DataFrame code:

Copy code

```
from pyspark.sql import Row

df = spark.createDataFrame([
    Row(id=1, name="Alice", age=25),
    Row(id=2, name="Bob", age=30),
    Row(id=3, name="Charlie", age=35),
])

df.show()
df.filter(df.age > 28).show()
print(df.count())
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

public class SnowparkConnectExample {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .pythonVenv("/path/to/scos-venv")
            .appName("My App")
            .getOrCreate();

        Dataset<Row> df = spark.sql("SELECT 1 AS id, 'Alice' AS name, 25 AS age "
            + "UNION ALL SELECT 2, 'Bob', 30 "
            + "UNION ALL SELECT 3, 'Charlie', 35");

        df.show();
        df.filter("age > 28").show();
        System.out.println(df.count());

        spark.stop();
    }
}
```

Compile and run:

Copy code

```
mvn compile exec:java -Dexec.mainClass="SnowparkConnectExample"
```

**UDF support**

When using user-defined functions or custom code with Java, do one of the following:

- Register a class finder to monitor and upload class files.

  Copy code

  ```
  import org.apache.spark.sql.connect.client.REPLClassDirMonitor;

  REPLClassDirMonitor classFinder = new REPLClassDirMonitor("/absolute/path/to/target/classes");
  spark.registerClassFinder(classFinder);
  ```
- Upload JAR dependencies. You can include the workload JAR itself if a class finder isn’t used.

  Copy code

  ```
  spark.addArtifact("/absolute/path/to/dependency.jar");
  ```
- Use a staged JAR.

  Copy code

  ```
  spark.conf().set("snowpark.connect.udf.java.imports",
   "[@mystage/dependency.jar, @db.schema.stage/other_dependency.jar]");
  ```

**Using Scala 2.13**

By default, Snowpark Connect for Spark uses Scala 2.12. If your dependencies are built with Scala 2.13, you
must specify the Scala version using the `snowpark.connect.scala.version` configuration option.

Copy code

```
SparkSession spark = SnowparkConnectSession.builder()
    .appName("My App")
    .config("snowpark.connect.scala.version", "2.13")
    .getOrCreate();
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession

object SnowparkConnectExample {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .pythonVenv("/path/to/scos-venv")
      .appName("My App")
      .getOrCreate()

    try {
      import spark.implicits._

      val df = spark.createDataFrame(Seq(
        (1, "Alice", 25),
        (2, "Bob", 30),
        (3, "Charlie", 35)
      )).toDF("id", "name", "age")

      df.show()
      df.filter($"age" > 28).show()
      println(df.count())

    } finally {
      spark.stop()
    }
  }
}
```

Compile and run:

Copy code

```
sbt "runMain SnowparkConnectExample"
```

**UDF support**

When using user-defined functions or custom code with Scala, do one of the following:

- Register a class finder to monitor and upload class files.

  Copy code

  ```
  import org.apache.spark.sql.connect.client.REPLClassDirMonitor

  val classFinder = new REPLClassDirMonitor("/absolute/path/to/target/scala-2.12/classes")
  spark.registerClassFinder(classFinder)
  ```
- Upload JAR dependencies. You can include the workload JAR itself if a class finder isn’t used.

  Copy code

  ```
  spark.addArtifact("/absolute/path/to/dependency.jar")
  ```
- Use a staged JAR.

  Copy code

  ```
  spark.conf.set("snowpark.connect.udf.java.imports",
   "[@mystage/dependency.jar, @db.schema.stage/other_dependency.jar]")
  ```

**Using Scala 2.13**

By default, Snowpark Connect for Spark uses Scala 2.12. Workloads built with Scala 2.13 must specify the Scala
version using the `snowpark.connect.scala.version` configuration option.

Copy code

```
val spark = SnowparkConnectSession.builder()
  .appName("My App")
  .config("snowpark.connect.scala.version", "2.13")
  .getOrCreate()
```

## Running Java or Scala workloads

For Java and Scala workloads, Snowpark Connect for Spark provides two approaches. Choose the one that matches how
you build and run your application.

**`snowpark-connect-java-client` library**: Use this approach for interactive development, when you
build and run your application from source in an IDE, Jupyter notebook, or REPL. You add the client
as a Maven or sbt dependency so that it becomes part of your build. The library starts and manages a
local Snowpark Connect for Spark server for you and ties the server’s lifecycle to your application’s JVM process,
so your session connects to Snowflake without additional setup while you develop. For the API
reference and examples, see [Snowpark Connect for Spark Java/Scala client reference](/developer-guide/snowpark-connect/snowpark-connect-jvm-reference).

**`snowpark-connect-execute-jar` CLI**: Use this approach to run an application that’s already
packaged as a JAR, without modifying or rebuilding it. The command-line tool runs your existing JAR
against Snowflake, managing the local server and the connection for you and shutting everything down
when the application exits. Because it requires no code changes, it’s a good fit for running built
artifacts, scheduled batch jobs, or applications that you can’t or don’t want to recompile. For
prerequisites, command options, and examples, see
[Snowpark Connect for Spark execute-jar CLI reference](/developer-guide/snowpark-connect/snowpark-connect-execute-jar-reference).

## Common installation issues

Use the following checks to resolve common Snowpark Connect for Spark installation issues.

- Ensure that Java and Python are [based on the same architecture](#label-snowpark-connect-local-ide-prereq).
- Use the most recent Snowpark Connect for Spark package, as described in [Install Snowpark Connect for Spark](#label-snowpark-connect-local-ide-install).
- Confirm that the `python` command with PySpark code is working correctly for local execution without Snowflake connectivity.

  For example, execute a command such as the following:

  Copy code

  ```
  python your_pyspark_file.py
  ```
