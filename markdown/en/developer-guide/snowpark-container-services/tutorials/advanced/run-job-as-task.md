# Tutorial: Run a Snowflake Container Services job as a Snowflake task

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## Introduction

When you run a Snowpark Container Services [job service](/developer-guide/snowpark-container-services/working-with-services) as a Snowflake task, the integration enables scenarios that leverage the robust containerization and scalability of Snowpark Container Services.

In this tutorial you create a task graph with the following two tasks:

1. A SQL task that creates a table (`sales_number`) and returns the table name as the return value for use by the dependent job service task.

   Note

   For simplicity, this SQL job only creates a table. In actual work, you use the table to perform more complex computations, such as model training.
2. A dependent job service task that queries the sales\_number table and returns results as JSON.

### Prerequisites

Complete the [Tutorial Common Setup](/developer-guide/snowpark-container-services/tutorials/common-setup) required for Snowpark Container Services tutorials provided in this guide.

## Step 1: Create example job service image

Save the sample code provided for the job service, build an image, and upload it to an image repository you created as part of common setup. This is the job service that you run as a Snowflake task in this tutorial.

### Save the code that is provided for the job service

Save the followng example job service code files to your local machine:

- `main.py`

  Copy code

  ```
  #!/usr/bin/env python3

  import json
  import logging
  import os
  import sys
  from snowflake.core.task.context import TaskContext
  from snowflake.snowpark import Session

  def get_logger(logger_name):
   """Set up logging for the application."""
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   handler = logging.StreamHandler(sys.stdout)
   handler.setLevel(logging.DEBUG)
   handler.setFormatter(
       logging.Formatter(
           '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
   logger.addHandler(handler)
   return logger

  logger = get_logger('job-in-task-graph')

  def run(session: Session):
   """
   Example job that reads the return value of the predecessor task
   and performs a simple query.
   """
   context = TaskContext(session)

   task_name = context.get_current_root_task_name()
   task_uuid = context.get_current_root_task_uuid()
   logger.info(f"Executing in task {task_name} with UUID {task_uuid}")

   # Fetch task graph configuration. It is equivalent to the following SQL
   # SELECT SYSTEM$GET_TASK_GRAPH_CONFIG('top_k')
   task_config = context.get_task_graph_config()
   top_k = task_config.get("top_k")

   # Fetch result of the predecessor task
   table_name = context.get_predecessor_return_value()

   # Select top k rows
   # In a real scenario, your code would use 'table_name' and
   # task graph configs to perform more complex computations
   # such as model training
   result = session.sql(f"""
       SELECT name FROM {table_name}
       ORDER BY total_sales DESC
       LIMIT {top_k}
   """).collect()
   names = [row[0] for row in result]

   # Set the return value for the task
   context.set_return_value(json.dumps(names))

  def get_login_token():
   """
   Read the login token supplied automatically by Snowflake. These tokens
   are short lived and should always be read right before creating any new connection.
   """
   with open("/snowflake/session/token", "r") as f:
       return f.read()

  def get_connection_params():
   """
   Construct Snowflake connection params from environment variables.
   """
   SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
   SNOWFLAKE_HOST = os.getenv("SNOWFLAKE_HOST")
   SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
   SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
   return {
           "account": SNOWFLAKE_ACCOUNT,
           "host": SNOWFLAKE_HOST,
           "database": SNOWFLAKE_DATABASE,
           "schema": SNOWFLAKE_SCHEMA,
           "authenticator": "oauth",
           "token": get_login_token(),
       }

  if __name__ == '__main__':
   with Session.builder.configs(get_connection_params()).create() as session:
       logger.info(f"Snowflake connection established (id={session.session_id})")
       run(session)
       logger.info("Job execution completed")
  ```
- `requirements.txt`

  Copy code

  ```
  snowflake-snowpark-python>=1.33.0
  snowflake-core
  ```
- `DOCKERFILE`

  Copy code

  ```
  FROM python:3.10-slim

  # Set working directory
  WORKDIR /app

  # Copy requirements first for better layer caching
  COPY requirements.txt .

  # Install dependencies
  RUN pip install -U pip && \
   pip install -r requirements.txt

  # Copy application code
  COPY main.py .

  # Make the script executable
  RUN chmod +x main.py

  # Set the entrypoint
  ENTRYPOINT ["python3", "main.py"]
  ```

You should now have a directory with three files.

### Build image and upload to image repository

Build an image for the linux/amd64 platform that Snowpark Container Services supports, and then upload the image to the image
repository in your account. For more information, see [Common Setup](/developer-guide/snowpark-container-services/tutorials/common-setup).

You need the repository URL and the registry hostname before you can build and upload the image. For more information, see
[Registry and Repositories](/developer-guide/snowpark-container-services/working-with-registry-repository).

#### Get information about the repository

To get the repository URL, execute the [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories) SQL command:

Copy code

```
SHOW IMAGE REPOSITORIES;
```

- The `repository_url` column in the output provides the URL, as shown in the following example:

  ```
  <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
  ```
- The host name in the repository URL is registry host name. An example is shown:

  ```
  <orgname>-<acctname>.registry.snowflakecomputing.com
  ```

#### Build image and upload it to the repository

1. Open a terminal window, and then change your directory to the directory that contains the files that you saved.
2. To build a Docker image, execute the following `docker build` command by using the Docker CLI.

The command ends with a period (.) which specifies current working directory as the `PATH` for files to use for building the image.

> Copy code
>
> ```
> docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
> ```
>
> - For `image_name`, use `my_task_job_image:latest`.
>
> **Example**
>
> Copy code
>
> ```
> docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_task_job_image:latest .
> ```

1. Upload the image to the repository in your Snowflake account. In order for Docker to upload an image on your behalf to your repository,
   you must first [authenticate Docker with the registry](/developer-guide/snowpark-container-services/working-with-registry-repository#label-registry-and-repository-authentication).
   1. For Docker to upload an image on your behalf to your repository,
      first [authenticate Docker with the registry](/developer-guide/snowpark-container-services/working-with-registry-repository#label-registry-and-repository-authentication).

      1. We recommend by using [Snowflake CLI](/developer-guide/snowflake-cli/index)
         to authenticate your local Docker instance with the image
         registry for your Snowflake account. Make sure that you configured Snowflake CLI to connect to Snowflake. For more information,
         see [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).
      2. To authenticate, execute the following Snowflake CLI command:

         Copy code

         ```
         snow spcs image-registry login
         ```
   2. To upload the image, execute the following command:

      Copy code

      ```
      docker push <repository_url>/<image_name>
      ```

      **Example**

      Copy code

      ```
      docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_task_job_image:latest
      ```

## Step 2: Create and execute a task graph

To create a task graph, run the following SQL code:

Copy code

```
use role accountadmin;
grant execute managed task on account to role test_role;

use role test_role;
use database tutorial_db;
use schema data_schema;

CREATE OR REPLACE TASK step1_prepare_data
CONFIG = '{"top_k": 3}'
AS BEGIN
    create or replace table sales_number (date timestamp, id number, name string, total_sales number)
    as select '2026-01-01' as date, 1 as id, 'Alice' as name, 100 as total_sales
    union all
    select '2026-01-01' as date, 2 as id, 'Bob' as name, 200 as total_sales;
    CALL SYSTEM$SET_RETURN_VALUE('sales_number');
END;

CREATE OR REPLACE TASK step2_execute_spcs_job
AFTER step1_prepare_data
AS
    EXECUTE JOB SERVICE
    IN COMPUTE POOL tutorial_compute_pool
    QUERY_WAREHOUSE=TUTORIAL_WAREHOUSE
    FROM SPECIFICATION $$
    spec:
        containers:
        - image: /tutorial_db/data_schema/tutorial_repository/my_task_job_image:latest
          name: main
    $$

;

-- Tasks you created are initially suspended state. So you first resume the tasks and run.
select SYSTEM$TASK_DEPENDENTS_ENABLE ('step1_prepare_data');
ALTER TASK step1_prepare_data RESUME;

-- now run the task graph
EXECUTE TASK step1_prepare_data;
```

In the next step, you can view the task and job details in Snowsight.

### Python code equivalent to the preceding SQL code

The following Snowflake Python code is the equivalent of the preceding SQL code to create the task graph:

Copy code

```
# DEFINE VARIABLES
from snowflake.snowpark.context import get_active_session
session = get_active_session()

STAGE_NAME = "TUTORIAL_DB.DATA_SCHEMA.TUTORIAL_STAGE"
WAREHOUSE_NAME = "TUTORIAL_WAREHOUSE"
DATABASE_NAME = "TUTORIAL_DB"
SCHEMA_NAME = "DATA_SCHEMA"
COMPUTE_POOL_NAME = "TUTORIAL_COMPUTE_POOL"
TEST_ROLE = "TEST_ROLE"

session.use_schema(f"{DATABASE_NAME}.{SCHEMA_NAME}")
session.use_role(f"{TEST_ROLE}")

# Create a task (only creates a task definition).
# Then you run the tasks

from datetime import timedelta

from snowflake.core import CreateMode, Root
from snowflake.core.task.context import TaskContext
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask
from snowflake.snowpark import Session

def prepare_dataset_task(session: Session)-> str:
    table_name = f"{DATABASE_NAME}.{SCHEMA_NAME}.daily_agg"
    session.sql(f"""
        create or replace table {table_name} (date timestamp, id number, name string, total_sales number)
        as select '2026-01-01' as date, 1 as id, 'Alice' as name, 100 as total_sales
        union all
        select '2026-01-01' as date, 2 as id, 'Bob' as name, 200 as total_sales
    """).collect()
    return table_name

def execute_spcs_job() -> str:
    return f"""
    EXECUTE JOB SERVICE
    IN COMPUTE POOL {COMPUTE_POOL_NAME}
    QUERY_WAREHOUSE={WAREHOUSE_NAME}
    FROM SPECIFICATION $$
    spec:
        containers:
        - image: /tutorial_db/data_schema/tutorial_repository/my_task_job_image:latest
          name: main
    $$
    """

def create_dag(name: str) -> DAG:
    with DAG(
        name,
        warehouse=WAREHOUSE_NAME,
        schedule=timedelta(minutes=100),
        use_func_return_value=True,
        stage_location=STAGE_NAME,
        packages=["snowflake-snowpark-python"],
        config={
            "top_k": 3,
        },
    ) as dag:
        # Step1 passes a function object to DAGTask and
        # the task, when run, executes the function object.
        step1 = DAGTask("step1", prepare_dataset_task)
        # In contrast, for step2 you execute the execute_spcs_job function
        # that returns a SQL string that is passed  to DAGTask.
        step2 = DAGTask("step2", execute_spcs_job())

        # Build the DAG
        step1 >> step2

    return dag

root = Root(session)
schema = root.databases[DATABASE_NAME].schemas[SCHEMA_NAME]
# *************** start code execution below **********
# Python API call (data_schema)
op = DAGOperation(schema)

# Directed acyclic graph. Create DAG definition. See function above.
# you can use "test_task_graph" to reference the task later.
dag = create_dag("test_task_graph")

# Create graph in Snowflake
op.deploy(dag, mode=CreateMode.or_replace)

# runs the code in both tasks.
op.run(dag)
```

## Step 3: View task and job details in Snowsight

To view the job service details in task history, perform the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. In the Horizon Catalog Explorer, locate the database and schema that contain the tasks that you want to view.
4. For the selected schema, select **Tasks**.
5. Select a specific task.

   The task details appear, with additional **Graph**, and **Run History** tabs.
6. To view the ID of the job service that you executed as part of the task run, select the **Run History** tab.

To view the task details in job history, perform the following steps:

1. In the navigation menu, select **Monitoring** » **Services & jobs**.
2. Select the **Jobs** tab.
3. Select the job that you want to view.

   The job details page appears. The **Overview** tab displays the task name if the task ran a job service.
4. To view the task details, select the task name.
5. To view the ID of the job service that you executed as part of the task run, select the **Run History** tab.
