# Snowpark Submit examples

This topic includes examples that use Snowpark Submit to submit production-ready Spark applications.
For installation, connection setup, and required privileges, see
[Using Snowpark Submit](/developer-guide/snowpark-connect/snowpark-connect-using-submit).

## Write and submit a simple Spark application

The following example shows how to write and submit a simple Spark application with no dependencies.

1. In your local IDE, create a new Python file called `app.py` with the following content:

   Copy code

   ```
   from pyspark.sql import SparkSession
   from pyspark.sql.functions import col, lit, upper, concat

   # Create Spark session
   spark = SparkSession.builder.appName("SimpleSession").getOrCreate()

   # Create a DataFrame from inline data
   data = [
    (1, "alice", "engineering", 95000),
    (2, "bob", "marketing", 72000),
    (3, "carol", "engineering", 105000),
    (4, "david", "sales", 68000),
    (5, "eva", "engineering", 88000),
   ]
   df = spark.createDataFrame(data, ["id", "name", "department", "salary"])

   # Add a new column
   df_with_bonus = df.withColumn("bonus", col("salary") * 0.1)
   df_with_bonus.show()

   # Filter and transform
   engineers = df.filter(col("department") == "engineering") \
    .withColumn("name_upper", upper(col("name"))) \
    .withColumn("greeting", concat(lit("Hello, "), col("name")))
   engineers.show()

   # Aggregate
   df.groupBy("department").avg("salary").show()

   # Stop the Spark session
   spark.stop()
   ```
2. To submit the application, use the following command:

   Copy code

   ```
   snowpark-submit \
     --snowflake-workload-name MY_JOB \
     --snowflake-connection-name MY_CONNECTION \
     /path/to/app.py
   ```

   You can use the `--wait-for-completion` option to wait for the job to complete, the `--workload-status` option to check the status of the job, and the `--display-logs` option to display the logs of the job. For a complete list of options, see [Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-connect-submit-reference).

## Deploy an application from a Snowflake stage

If the application has dependencies, like files it needs to read, you can deploy them from a Snowflake stage. The following example shows how to deploy an application and its dependencies from a Snowflake stage.

1. To upload files to a stage from the terminal, you can use the Snowflake CLI. Note that SnowSQL is the legacy CLI and if you are already using it, you can use that as well to upload files to a stage. If you have not already installed the Snowflake CLI, you can install it by following the instructions in [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
2. Create a new CSV file in your local IDE called `sample_employees.csv` with the following content:

   ```
   employee_id,name,department,salary,years_employed
   1,Alice Johnson,Engineering,95000,5
   2,Bob Smith,Marketing,72000,3
   3,Carol Williams,Engineering,105000,8
   4,David Brown,Sales,68000,2
   5,Eva Martinez,Engineering,88000,4
   6,Frank Wilson,Marketing,75000,6
   7,Grace Lee,Sales,92000,7
   8,Henry Taylor,Engineering,110000,10
   9,Ivy Chen,Marketing,65000,1
   10,Jack Davis,Sales,78000,4
   11,Karen White,Engineering,98000,6
   12,Leo Harris,Marketing,71000,3
   13,Maria Garcia,Sales,85000,5
   14,Nathan Clark,Engineering,102000,9
   15,Olivia Moore,Marketing,69000,2
   ```

   Upload your dependency files to a stage by using the following command, where *my\_stage* is the name of a stage in your account. (If you do not have a stage created, you can use [*snow stage create*](/developer-guide/snowflake-cli/command-reference/stage-commands/create).)

   Copy code

   ```
   snow stage copy sample_employees.csv @<database>.<schema>.<stage>/sample_employees.csv -c MY_CONNECTION
   ```

   To verify that the file uploaded successfully, you can use the following command to list the files in the stage:

   Copy code

   ```
   snow sql -c MY_CONNECTION -q "ls @<database>.<schema>.<stage>"
   ```

   You should see the file `sample_employees.csv` in the list.
3. In your local IDE, create a new Python file called `app.py` with the following content:

   Copy code

   ```
   from pyspark.sql import SparkSession

   # Create Spark session
   spark = SparkSession.builder.appName("SimpleStageExample").getOrCreate()

   # Load data from stage (adjust stage name to match yours)
   df = spark.read.csv("/app/<YOUR_STAGE>/sample_employees.csv", header=True, inferSchema=True)
   df.show()

   # Filter: Engineering department only
   engineers = df.filter(df["department"] == "Engineering")
   engineers.show()

   # Filter: Salary > 80000 and years_employed > 3
   senior_high_earners = df.filter((df["salary"] > 80000) & (df["years_employed"] > 3))
   senior_high_earners.show()

   # Aggregate: Average salary by department
   df.groupBy("department").avg("salary").show()

   # Select specific columns
   result = senior_high_earners.select("name", "department", "salary")
   result.show()

   # Stop the Spark session
   spark.stop()
   ```

   To submit the application which uses the files you uploaded to the stage, use the following command:

   Copy code

   ```
   snowpark-submit \
     --snowflake-connection-name MY_CONNECTION \
     --snowflake-workload-name MY_JOB \
     --snowflake-stage @<database>.<schema>.<stage> \
     /path/to/app.py
   ```

   Note that a compute pool is required to run the application and must be either specified in the `connections.toml` file or on the command line using the `--compute-pool` option. For more information, see [Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-connect-submit-reference).

## Monitor with wait and logs

The following example shows how to submit a job, wait for its completion, and then retrieve logs.

1. Submit the job and wait for completion by using the following command:

   Copy code

   ```
   snowpark-submit \
     --snowflake-workload-name MY_JOB \
     --wait-for-completion \
     --snowflake-connection-name MY_CONNECTION \
     /path/to/app.py
   ```
2. If the job fails, check the detailed logs by using the following command:

   Copy code

   ```
   snowpark-submit
     --snowflake-workload-name MY_JOB \
     --workload-status \
     --display-logs \
     --snowflake-connection-name MY_CONNECTION
   ```

## Use Snowpark Submit in an Apache Airflow DAG

You can submit a Spark job to Snowflake via Snowpark Connect for Spark. You can use `snowpark-submit` in cluster mode to leverage a
compute pool to run the job.

When you use Apache Airflow in this way, ensure that the Docker service or Snowpark Container Services container that runs Apache Airflow
has proper access to Snowflake and the required files in the Snowflake stage.

The code in the following example performs the following tasks:

- Creates a Python virtual environment at `/tmp/myenv`.

  In the `create_venv` task, the code uses `pip` to install the `snowpark-submit` package by using a `.whl` file.
- Generates a secure `connections.toml` file with Snowflake connection credentials and an OAuth token.

  In the `create_connections_toml` task, the code creates the `/app/.snowflake` directory, creates the `.toml` file,
  and then changes file permissions to allow only the owner (user) to have read and write access.
- Runs a Spark job by using the `snowpark-submit` command.

  In the `run_snowpark_script` task, the code does the following things:

  - Activates the virtual environment.
  - Runs the Spark job by using the `snowpark-submit` command.
  - Deploys to Snowflake by using cluster mode.
  - Uses the Snowpark Connect for Spark remote URI sc://localhost:15002.
  - Specifies the Spark application class `org.example.SnowparkConnectApp`.
  - Pulls the script from the @snowflake\_stage stage.
  - Blocks deployment until the job finishes by using `--wait-for-completion`.

Copy code

```
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
  'start_date': airflow.utils.dates.days_ago(1),
  'retries': 0,
}

with DAG(
  'run_sparkconnect_python_script',
  default_args=default_args,
  schedule_interval=None,
  catchup=False,
) as dag:

  create_venv = BashOperator(
      task_id='create_venv',
      bash_command="""
      python3 -m venv /tmp/myenv &&
      source /tmp/myenv/bin/activate &&
      export PIP_USER=false &&
      pip install --upgrade pip &&
      pip install --no-cache-dir grpcio-tools>=1.48.1 &&
      pip install /app/snowpark_submit-<version>.whl
      """
  )

  create_connections_toml = BashOperator(
      task_id='create_connections_toml',
      bash_command="""
      mkdir -p /app/.snowflake
      echo "${SNOWFLAKE_USER}"
      cat <<EOF > /app/.snowflake/connections.toml

[snowpark-submit]
host = "${SNOWFLAKE_HOST}"
port = "${SNOWFLAKE_PORT}"
protocol = "https"
account = "${SNOWFLAKE_ACCOUNT}"
authenticator = "oauth"
token = "$(cat /snowflake/session/token)"
warehouse = "airflow_wh"
database = "${SNOWFLAKE_DATABASE}"
schema = "${SNOWFLAKE_SCHEMA}"
client_session_keep_alive = true
EOF
  chmod 600 /app/.snowflake/connections.toml
  """
  )

  run_script = BashOperator(
      task_id='run_snowpark_script',
      bash_command="""
      set -e
      echo "Using SNOWFLAKE_HOME: $SNOWFLAKE_HOME"

      echo "Running Python script with Snowpark..."
      source /tmp/myenv/bin/activate &&
      snowpark-submit --deploy-mode cluster --class org.example.SnowparkConnectApp --compute-pool="snowparksubmit" --snowflake-workload-name="spcstest" --snowflake-stage="@AIRFLOW_APP_FILES" --wait-for-completion "@AIRFLOW_APP_FILES/transformation.py" --snowflake-connection-name snowpark-submit
      """,
      env={
          'SNOWFLAKE_HOME': '/app/.snowflake'
      }
  )

create_venv >> create_connections_toml >> run_script
```

You can monitor the DAG by using the Apache Airflow user interface’s Graph View or Tree View. Inspect the task logs for the following items:

- Environment setup
- Status of Snowpark Connect for Spark
- `snowpark-submit` job output

You can also monitor for jobs that ran in Snowflake from the logs stored in Snowflake stage or from event tables.
