# Develop in Snowflake Workspaces

You can run Spark workloads interactively from Snowflake Notebooks without needing to manage a Spark cluster. The workloads run on the
Snowflake infrastructure.

To use Snowflake Notebooks as a client for developing Spark workloads to run on Snowflake:

1. Launch Snowflake Notebooks.
2. Within the notebook, start a Spark session.
3. Write PySpark code to load, transform, and analyze data.

## Use a Snowflake Notebook in a workspace

For more information about Snowflake Notebooks in Workspaces, see [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview).

The `snowpark-connect` package is preinstalled in the Notebooks in Workspaces base image, so you don’t need to
install it for basic use.

1. Set the database and schema for the session.

   Notebooks in Workspaces don’t automatically set a database or schema, and Snowpark Connect for Spark requires you to set
   the context before you initialize the session. In a SQL cell, set the context before you run the cell that
   starts the session:

   Copy code

   ```
   USE DATABASE <database>;
   USE SCHEMA <schema>;
   ```

   For more information, see [Set the execution context](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-execution-context).
2. Start the `snowpark_connect` server using `init_spark_session()`:

   Copy code

   ```
   import snowflake.snowpark_connect

   spark = snowflake.snowpark_connect.init_spark_session()
   ```
3. Run your Spark code, as shown in the following example:

   Copy code

   ```
   from pyspark.sql.connect.functions import *
   from pyspark.sql.connect.types import *
   from pyspark.sql import Row

   # Sample nested data
   data = [(1, ("Alice", 30))]
   schema = "id INT, info STRUCT<name:STRING, age:INT>"

   df = spark.createDataFrame(data, schema=schema)
   df.show()

   spark.sql("show databases").show()
   ```

To install a specific version of `snowpark-connect`, or to add other packages, use the Snowflake PyPI artifact
repository. By default, the PUBLIC role has access to the Snowflake PyPI repo, so you don’t need an external
access integration. For more information, see [Using artifact repositories](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-artifact-repositories).

1. When you edit or create the notebook service, select `snowflake.snowpark.pypi_shared_repository` for
   **Artifact Repository**, and then select **Create and connect**.
2. Install the package in a Python cell:

   Copy code

   ```
   !pip install snowpark-connect[jdk]
   ```
3. Restart the kernel. From the **Connect** button, select **Restart kernel**.

## Use a Snowflake Notebook on a warehouse

For more information about Snowflake Notebooks, see [Create a notebook](/user-guide/ui-snowsight/notebooks-create).

1. Create a Snowflake Notebook by completing the following steps:

   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
   2. At the top of the navigation menu, select [![Add a dashboard tile](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png)](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png) (**Create**) » **Notebook** » **New Notebook**.
   3. In the **Create notebook** dialog, enter a name, database, and schema for the new notebook.

      For more information, see [Create a notebook](/user-guide/ui-snowsight/notebooks-create).
   4. For **Runtime**, select **Run on warehouse**.
   5. For **Runtime version**, select **Snowflake Warehouse Runtime 2.0**.

      When you select version 2.0, you ensure that you have the dependency support you need, including Python 3.10. For more information,
      see [Legacy Notebook runtimes](/user-guide/ui-snowsight/notebooks#label-notebook-runtime-descriptions).
   6. For **Query warehouse** and **Notebook warehouse**, select warehouses for running query code and kernel and Python code,
      as described in [Create a notebook](/user-guide/ui-snowsight/notebooks-create).
   7. Select **Create**.
   8. In the notebook you created, under **Packages**, ensure that you have the following packages listed to support code in your
      notebook:

      - Python, version 3.10 or later
      - snowpark-connect, latest version

        If you need to add these packages, use the following steps:

        1. Under **Anaconda Packages**, type the packages name in the search box.
        2. Select the package name.
        3. Select **Save**.
2. To connect to the Snowpark Connect for Spark server and test the connection, copy the following code and paste it in the Python cell of the
   notebook you created:

   Copy code

   ```
   from snowflake import snowpark_connect

   spark = snowpark_connect.init_spark_session()
   df = spark.sql("show schemas").limit(10)
   df.show()
   ```
