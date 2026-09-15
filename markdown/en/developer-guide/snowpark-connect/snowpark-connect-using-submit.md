# Using Snowpark Submit

Snowpark Submit lets you run batch-oriented Spark workloads directly on Snowflake’s infrastructure. You package your application as a
Python script or a Scala/Java JAR, then use the Snowpark Submit CLI to submit it. The job runs in cluster mode on Snowpark Container Services with no external
Spark cluster required.

## Prerequisites

On the machine that submits the job, you need:

- **Python 3.10 or later** (earlier than 3.13). The Snowpark Submit CLI is written in Python, but your application itself can be Python,
  Java, or Scala.
- **Snowflake CLI** (`snow`). Used to manage connections and upload files to stages. For installation instructions, see
  [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
- **A Snowflake warehouse**. The virtual warehouse on which your Spark job executes. The role you use for Snowpark Submit needs USAGE
  privilege on that warehouse.
- **A Snowflake compute pool**. An SPCS compute pool that hosts the Spark driver. If you don’t have one, create it in
  [Step 3](#label-snowpark-submit-compute-pool).

For Scala or Java jobs, you also need:

- A **JDK** (Java 11 or later) to compile your application.
- **sbt** (Scala) or **Maven** (Java) to build the JAR.

### Required privileges

The role you use with Snowpark Submit must have the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Database | The parent database of the schema where the job runs. |
| USAGE | Schema | The parent schema where the job service is created. |
| CREATE SERVICE | Schema | The schema where the job service is created. |
| USAGE | Compute pool | The pool specified with `--compute-pool` or in `connections.toml`. |
| USAGE | Warehouse | The virtual warehouse on which the Spark job executes. |
| READ | Stage | The stage where workload files are stored (if using `--snowflake-stage`). |
| READ | Image repository | The repository containing images referenced by the job spec. |

Expand

Show lessSee more

## Step 1: Prepare your application

PythonJavaScala

Create a Python file with your Spark application. Use `SparkSession.builder` to obtain a session; Snowpark Submit handles the
connection to the Snowflake-managed Spark server automatically.

Copy code

```
# app.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

spark = SparkSession.builder.appName("MyApp").getOrCreate()

data = [
    (1, "alice", "engineering", 95000),
    (2, "bob", "marketing", 72000),
    (3, "carol", "engineering", 105000),
]
df = spark.createDataFrame(data, ["id", "name", "department", "salary"])

df.withColumn("name", upper(col("name"))).show()

spark.stop()
```

Add the Snowpark Connect for Spark Java client and Spark Connect client dependencies to your `pom.xml`:

Copy code

```
<dependency>
  <groupId>com.snowflake</groupId>
  <artifactId>snowpark-connect-java-client_2.12</artifactId>
  <version>1.0.0</version>
</dependency>
<dependency>
  <groupId>org.apache.spark</groupId>
  <artifactId>spark-connect-client-jvm_2.12</artifactId>
  <version>3.5.6</version>
  <scope>provided</scope>
</dependency>
```

Write your application entry point using `SnowparkConnectSession`:

Copy code

```
package com.example;

import com.snowflake.snowpark_connect.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

public class HelloSnowparkSubmit {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("MyJavaJob")
            .getOrCreate();

        Dataset<Row> df = spark.sql("SELECT 1 AS id, 'hello' AS message");
        df.show();

        spark.stop();
    }
}
```

Build a fat JAR (uber JAR) that bundles all dependencies into a single file. Snowpark Submit uploads
this JAR to Snowflake, so all classes must be included. Add the Maven Shade Plugin to your
`pom.xml`:

Copy code

```
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-shade-plugin</artifactId>
  <version>3.5.1</version>
  <executions>
    <execution>
      <phase>package</phase>
      <goals><goal>shade</goal></goals>
    </execution>
  </executions>
</plugin>
```

Then build:

Copy code

```
mvn package
```

For details on the Java client API, see
[Snowpark Connect for Spark Java/Scala client reference](/developer-guide/snowpark-connect/snowpark-connect-jvm-reference).

Scala 2.12 is the default. Add the Snowpark Connect for Spark Java client and Spark Connect client dependencies
to your `build.sbt`:

Copy code

```
libraryDependencies += "com.snowflake" %% "snowpark-connect-java-client" % "1.0.0"
libraryDependencies += "org.apache.spark" %% "spark-connect-client-jvm" % "3.5.6" % Provided
```

Write your application entry point using `SnowparkConnectSession`:

Copy code

```
package com.example

import com.snowflake.snowpark_connect.SnowparkConnectSession

object HelloSnowparkSubmit {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("MyScalaJob")
      .getOrCreate()

    val df = spark.sql("SELECT 1 AS id, 'hello' AS message")
    df.show()

    spark.stop()
  }
}
```

Build a fat JAR (uber JAR) that bundles all dependencies into a single file. Snowpark Submit uploads
this JAR to Snowflake, so all classes must be included. Add the sbt-assembly plugin to
`project/plugins.sbt`:

Copy code

```
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "2.2.0")
```

Then build:

Copy code

```
sbt assembly
```

For details on the Java client API, see
[Snowpark Connect for Spark Java/Scala client reference](/developer-guide/snowpark-connect/snowpark-connect-jvm-reference).

**If you must use Scala 2.13**, two changes are required:

- Pass `--scala-version 2.13` when submitting (Step 5).
- Set `snowpark.connect.scala.version` in your application code:

  Copy code

  ```
  val spark = SnowparkConnectSession.builder()
    .config("snowpark.connect.scala.version", "2.13")
    .getOrCreate()
  ```

## Step 2: Install the Snowpark Submit CLI

Snowpark Submit is a Python package that acts as the submission CLI. Your application still runs as Python, Java, or Scala on
Snowflake.

Copy code

```
pip install snowpark-submit
```

Verify the installation:

Copy code

```
snowpark-submit -h
```

Optionally, install it inside a Python virtual environment to keep it isolated from your system Python:

Copy code

```
python3 -m venv ~/.venvs/snowpark-submit
source ~/.venvs/snowpark-submit/bin/activate
pip install --upgrade pip
pip install snowpark-submit
```

## Step 3: Set up a compute pool

If you already have a compute pool, skip to Step 4.

Create a compute pool in Snowsight or with the Snowflake CLI using a role that has the CREATE COMPUTE POOL privilege (for
example, ACCOUNTADMIN). For testing, you can start with the smallest CPU instance family and scale up later. For more
information, see [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

Copy code

```
CREATE COMPUTE POOL MY_SPARK_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_SUSPEND_SECS = 300
  AUTO_RESUME = TRUE;
```

Note

- AUTO\_SUSPEND\_SECS and AUTO\_RESUME mean the pool suspends itself when idle and resumes on the next submit, so you don’t pay
  for idle nodes between runs. Expect around 30-60 seconds of cold-start latency on a resumed pool.
- If your job needs more memory, step up to `CPU_X64_S` (3 vCPU, 13 GiB) or `CPU_X64_M` (6 vCPU, 28 GiB). Use
  `SHOW COMPUTE POOL INSTANCE FAMILIES;` to list all available sizes.
- The role that runs Snowpark Submit needs USAGE on the compute pool. If it’s a different role from the one that created the pool,
  grant it:

  Copy code

  ```
  GRANT USAGE ON COMPUTE POOL MY_SPARK_POOL TO ROLE <your_role>;
  ```

## Step 4: Configure your Snowflake connection

Snowpark Submit reads the [connections.toml](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml) file used by the Snowflake Python connector and
Snowflake CLI. The Snowflake CLI provides an interactive onboarding experience for adding connections and a
dedicated command for testing them. For details, see
[Configuring Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli).

You can create or update a connection with the Snowflake CLI:

Copy code

```
snow connection add
```

Or edit `connections.toml` directly. An example entry using OAuth:

Copy code

```
[snowpark-submit]
account = "<account>"
user = "<user>"
authenticator = "OAUTH_AUTHORIZATION_CODE"
client_store_temporary_credential = true
warehouse = "<warehouse>"
database = "<database>"
schema = "<schema>"
compute_pool = "<compute_pool>"
```

Password authentication is also supported. Replace the `authenticator` and `client_store_temporary_credential` lines with
`password = "<password>"`.

The compute pool can either be set here as `compute_pool` or passed at submit time with `--compute-pool` (see Step 5).

Verify that the connection works:

Copy code

```
snow connection test --connection snowpark-submit
```

## Step 5: Submit the job

See the [Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-connect-submit-reference) for the full list of CLI flags.

PythonJavaScala

Copy code

```
snowpark-submit \
  --snowflake-workload-name MY_PYTHON_JOB \
  --snowflake-connection-name snowpark-submit \
  --compute-pool MY_SPARK_POOL \
  --wait-for-completion \
  path/to/app.py
```

Copy code

```
snowpark-submit \
  --class com.example.HelloSnowparkSubmit \
  --snowflake-workload-name MY_JAVA_JOB \
  --snowflake-connection-name snowpark-submit \
  --compute-pool MY_SPARK_POOL \
  --wait-for-completion \
  path/to/your-app.jar
```

Copy code

```
snowpark-submit \
  --class com.example.HelloSnowparkSubmit \
  --snowflake-workload-name MY_SCALA_JOB \
  --snowflake-connection-name snowpark-submit \
  --compute-pool MY_SPARK_POOL \
  --wait-for-completion \
  path/to/your-app.jar
```

For Scala 2.13 JARs, add `--scala-version 2.13`.

Common flags:

- `--class` – required for Java/Scala if the main class isn’t set in the JAR manifest.
- `--compute-pool` – the SPCS compute pool that hosts the Spark driver. Can also be set in `connections.toml`.
- `--wait-for-completion` – blocks until the workload finishes. Without it, Snowpark Submit starts the job and returns immediately.
- `--scala-version 2.13` – required only if the JAR is built against Scala 2.13.
- `--jars` – comma-separated list of additional JAR dependencies. These must also be registered with `spark.addArtifact()`
  in your application code.

## Step 6: Check status and logs

The submit command from Step 5 prints two things you need for status lookups:

- **Snowflake Workload Name** – the full workload name with the timestamp suffix the CLI appends (for example,
  `MY_SCALA_JOB_260417_200531`). Status lookups only work with this suffixed name.
- **Job History URL** – a Snowsight link for the workload, which is the fastest way to see status and logs in the UI.

To check status and logs from the CLI, pass the suffixed name:

Copy code

```
snowpark-submit \
  --snowflake-connection-name snowpark-submit \
  --snowflake-workload-name MY_SCALA_JOB_260417_200531 \
  --workload-status --display-logs
```

`--workload-status` returns the current state (`DEPLOYING`, `RUNNING`, `SUCCEEDED`, or `FAILED`), start time, duration,
and service details. `--display-logs` prints the application logs.

Note

There is a small latency, from a few seconds to a minute, before logs are available for fetching. When an event table isn’t
used to store log data, logs are retained for a short period of time, such as five minutes or less.

For production monitoring and detailed log configuration, see [Monitoring Snowpark Connect for Spark workloads](/developer-guide/snowpark-connect/snowpark-connect-monitoring).
