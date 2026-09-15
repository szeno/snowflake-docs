# Using the Snowpark Python DB-API

With the Snowpark Python DB-API, Snowpark Python users can programmatically pull data from external databases into Snowflake. The DB-API includes:

- **Python DB-API support:** Connect to external databases using Python’s standard DB-API 2.0 drivers.
- **Streamlined setup:** Use `pip` to install the necessary drivers, with no need to manage additional dependencies.

With these APIs, you can seamlessly pull data into Snowflake tables and transform it using [Snowpark DataFrames](/developer-guide/snowpark/python/working-with-dataframes) for advanced analytics.

The [DB-API](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.dbapi) can be used in a similar way as the [Spark JDBC API](https://spark.apache.org/docs/3.5.4/sql-data-sources-jdbc.html). Most parameters are designed to be identical or similar for better parity. At the same time, Snowpark emphasizes a Python-first design with intuitive naming conventions that avoid JDBC-specific configurations. This provides Python developers with a familiar experience. For more information that compares the Snowpark Python DB-API with the Spark JDBC API, see the following table:

## DB-API parameters

| Parameter | Snowpark Python DB-API |
| --- | --- |
| `create_connection` | Function to create a Python DB-API connection |
| `table` | Specifies the table in the source database |
| `query` | SQL query wrapped as a subquery for reading data |
| `column` | Partitioning column for parallel reads |
| `lower_bound` | Lower bound for partitioning |
| `upper_bound` | Upper bound for partitioning |
| `num_partitions` | Number of partitions for parallelism |
| `query_timeout` | Timeout for SQL execution (in seconds) |
| `fetch_size` | Number of rows fetched per round trip |
| `custom_schema` | Custom schema for pulling data from external databases |
| `max_workers` | Number of workers for parallel fetching and pulling data from external databases |
| `predicates` | List of conditions for WHERE clause partitions |
| `session_init_statement` | Executes a SQL or PL/SQL statement upon session initialization |
| `udtf_configs` | Executes the workload using a Snowflake UDTF for better performance |
| `fetch_merge_count` | Number of fetched batches to be merged into a single Parquet file before it is uploaded |

Expand

Show lessSee more

## Understanding parallelism

The Snowpark Python DB-API has two underlying forms of ingestion mechanisms:

Local ingestion
:   In local ingestion, Snowpark first fetches data from external sources to your local environment, where the `dbapi()` function is called and
    converts them to Parquet files. Next, Snowpark uploads these Parquet files to a temporary Snowflake stage and copies them into a temporary
    table from the stage.

UDTF ingestion
:   In UDTF ingestion, all workloads run on the Snowflake server. Snowpark first creates a UDTF and executes it, and the UDTF directly
    ingests data into Snowflake and stores it in a temporary table.

The Snowpark Python DB-API also has two ways to parallelize and accelerate ingestion:

Partition column
:   This method divides source data into multiple partitions based on four parameters when users call `dbapi()`:

    - `column`
    - `lower_bound`
    - `upper_bound`
    - `num_partitions`

    These four parameters have to be set at the same time and `column` must be numeric or date type.

Predicates
:   This method divides source data into partitions based on parameter predicates, which are a list of expressions suitable for inclusion
    in `WHERE` clauses, where each expression defines a partition. Predicates provide a more flexible way of dividing partitions; for example,
    you can divide partitions on Boolean or non-numeric columns.

The Snowpark Python DB-API also allows the adjustment of parallelism level within a partition:

Fetch\_size
:   Within a partition, the API fetches rows in chunks defined by fetch\_size. These rows are written to Snowflake in parallel as they are
    fetched, which allows reading and writing to overlap and maximizes throughput.

By combining the listed methods of ingestion and parallelism, Snowflake has four ways of ingestion:

- **Local ingestion with partition column**

  Copy code

  ```
  df_local_par_column = session.read.dbapi(
   create_connection,
   table="target_table",
   fetch_size=100000,
   num_partitions=4,
   column="ID",  # Swap with the column you want your partition based on
   upper_bound=10000,
   lower_bound=0
  )
  ```
- **Local ingestion with predicates**

  Copy code

  ```
  df_local_predicates = session.read.dbapi(
   create_connection,
   table="target_table",
   fetch_size=100000,
   predicates=[
       "ID < 3",
       "ID >= 3"
   ]
  )
  ```
- **UDTF ingestion with partition column**

  Copy code

  ```
  udtf_configs = {
   "external_access_integration": "<your external access integration>"
  }
  df_udtf_par_column = session.read.dbapi(
   create_connection,
   table="target_table",
   udtf_configs=udtf_configs,
   fetch_size=100000,
   num_partitions=4,
   column="ID",  # Swap with the column you want your partition based on
   upper_bound=10000,
   lower_bound=0
  )
  ```
- **UDTF ingestion with predicates**

  Copy code

  ```
  udtf_configs = {
   "external_access_integration": "<your external access integration>"
  }

  df_udtf_predicates = session.read.dbapi(
   create_dbx_connection,
   table="target_table",
   udtf_configs=udtf_configs,
   fetch_size=100000,
   predicates=[
       "ID < 3",
       "ID >= 3"
   ]
  )
  ```

## SQL Server

To connect to SQL Server from Snowpark, you need the following three packages:

- Snowpark: [snowflake-snowpark-python[pandas]](https://pypi.org/project/snowflake-snowpark-python/)
- SQL Server ODBC Driver: [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server)

  By installing the driver, you agree to Microsoft’s EULA.
- The open source pyodbc library: [pyodbc](https://pypi.org/project/pyodbc/)

The following code examples show how to connect to SQL Server from a Snowpark client and a stored procedure.

### Use the DB-API to connect to SQL Server from a Snowpark client

1. Install the Python SQL Driver:

   Copy code

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   brew update
   HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql mssql-tools
   ```
2. Install `snowflake-snowpark-python[pandas]` and `pyodbc`:

   Copy code

   ```
   pip install snowflake-snowpark-python[pandas]
   pip install pyodbc
   ```
3. Define the factory method for creating a connection to SQL Server:

   Copy code

   ```
   def create_sql_server_connection():
    import pyodbc
    SERVER = "<your host name>"
    PORT = <your port>
    UID = "<your user name>"
    PWD = "<your password>"
    DATABASE = "<your database name>"
    connection_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER}:{PORT};"
        f"UID={UID};"
        f"PWD={PWD};"
        f"DATABASE={DATABASE};"
        "TrustServerCertificate=yes"
        "Encrypt=yes"
        # Optional to identify source of queries
        "APP=snowflake-snowpark-python;"
    )
    connection = pyodbc.connect(connection_str)
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_sql_server_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_sql_server_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_sql_server_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # Swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_sql_server_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )
   ```

### Use the DB-API to connect to SQL Server from a stored procedure

1. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
2. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   -- Configure a secret to allow egress to the source endpoint

   CREATE OR REPLACE SECRET mssql_secret
   TYPE = PASSWORD
   USERNAME = 'mssql_username'
   PASSWORD = 'mssql_password';

   -- Configure a network rule to allow egress to the source endpoint

   CREATE OR REPLACE NETWORK RULE mssql_network_rule
   MODE = EGRESS
   TYPE = HOST_PORT
   VALUE_LIST = ('mssql_host:mssql_port');

   -- Configure an external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mssql_access_integration
   ALLOWED_NETWORK_RULES = (mssql_network_rule)
   ALLOWED_AUTHENTICATION_SECRETS = (mssql_secret)
   ENABLED = true;
   ```
3. Use the DB-API to pull data from SQL Server in a Python stored procedure:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_mssql_dbapi()
    RETURNS TABLE()
    LANGUAGE PYTHON
    RUNTIME_VERSION='3.11'
    HANDLER='run'
    PACKAGES=('snowflake-snowpark-python', 'pyodbc', 'msodbcsql')
    EXTERNAL_ACCESS_INTEGRATIONS = (mssql_access_integration)
    SECRETS = ('cred' = mssql_secret )
   AS $$

   # Get user name and password from mssql_secret

   import _snowflake
   username_password_object = _snowflake.get_username_password('cred')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   # Define a method to connect to SQL Server_hostname
   from snowflake.snowpark import Session
   def create_sql_server_connection():
    import pyodbc

    host = "<your host>"
    port = <your port>
    username = USER
    password = PASSWORD
    database = "<your database name>"
    connection_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes"
        "Encrypt=yes"
        # Optional to identify source of queries
        "APP=snowflake-snowpark-python;"
    )

    connection = pyodbc.connect(connection_str)
    return connection

   def run(session: Session):
    # Feel free to combine local/udtf ingestion and partition column/predicates
    # as stated in the understanding parallelism section

    # Call dbapi to pull data from target table

    df = session.read.dbapi(
        create_sql_server_connection,
        table="target_table"
    )

    # Call dbapi to pull data from target query

    df_query = session.read.dbapi(
        create_sql_server_connection,
        query="select * from target_table"
    )

    # Pull data from target table with parallelism using partition column

    df_local_par_column = session.read.dbapi(
        create_sql_server_connection,
        table="target_table",
        fetch_size=100000,
        num_partitions=4,
        column="ID",  # swap with the column you want your partition based on
        upper_bound=10000,
        lower_bound=0
    )

    udtf_configs = {
        "external_access_integration": "<your external access integration>"
    }

    # Pull data from target table with udtf ingestion with parallelism using predicates

    df_udtf_predicates = session.read.dbapi(
        create_sql_server_connection,
        table="target_table",
        udtf_configs=udtf_configs,
        fetch_size=100000,
        predicates=[
            "ID < 3",
            "ID >= 3"
        ]
    )

    return df
   $$;

   CALL sp_mssql_dbapi();
   ```

### Use the DB-API to connect to SQL Server from a Snowflake notebook

1. From [Snowflake Notebook packages](/user-guide/ui-snowsight/notebooks-import-packages), select `snowflake-snowpark-python` and `pyodbc`.
2. In the **Files** pane, open the file `environment.yml`, and under **Dependencies**, add the following line of code after other entries:

   Copy code

   ```
   - msodbcsql
   ```
3. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   -- Configure a secret to allow egress to the source endpoint

   CREATE OR REPLACE SECRET mssql_secret
   TYPE = PASSWORD
   USERNAME = 'mssql_username'
   PASSWORD = 'mssql_password';

   ALTER NOTEBOOK mynotebook SET SECRETS = ('snowflake-secret-object' = mssql_secret);

   -- Configure a network rule to allow egress to the source endpoint

   CREATE OR REPLACE NETWORK RULE mssql_network_rule
   MODE = EGRESS
   TYPE = HOST_PORT
   VALUE_LIST = ('mssql_host:mssql_port');

   -- Configure an external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mssql_access_integration
   ALLOWED_NETWORK_RULES = (mssql_network_rule)
   ALLOWED_AUTHENTICATION_SECRETS = (mssql_secret)
   ENABLED = true;
   ```
4. [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access), and then restart the notebook session.
5. Use the DB-API to pull data from SQL Server in a Python cell of a Snowflake notebook:

   Copy code

   ```
   # Get user name and password from mssql_secret

   import _snowflake
   username_password_object = _snowflake.get_username_password('snowflake-secret-object')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()

   def create_sql_server_connection():
    import pyodbc
    SERVER = SQL_SERVER_CONNECTION_PARAMETERS["SERVER"]
    UID = SQL_SERVER_CONNECTION_PARAMETERS["UID"]
    PWD = SQL_SERVER_CONNECTION_PARAMETERS["PWD"]
    DATABASE = "test_query_history"
    connection_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};"
        f"UID={UID};"
        f"PWD={PWD};"
        f"DATABASE={DATABASE};"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
        # Optional to identify source of queries
        "APP=snowflake-snowpark-python;"
    )
    connection = pyodbc.connect(connection_str)
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_sql_server_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_sql_server_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_sql_server_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_sql_server_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )

   # Save data into sf_table
   df.write.mode("overwrite").save_as_table('sf_table')
   ```

### Source tracing when using the DB-API to connect to SQL Server

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   def create_sql_server_connection():
    import pyodbc
    SERVER = "<your host name>"
    PORT = <your port>
    UID = "<your user name>"
    PWD = "<your password>"
    DATABASE = "<your database name>"
    connection_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER}:{PORT};"
        f"UID={UID};"
        f"PWD={PWD};"
        f"DATABASE={DATABASE};"
        "TrustServerCertificate=yes"
        "Encrypt=yes"
        # include this parameter for source tracing
        "APP=snowflake-snowpark-python;"
    )
    connection = pyodbc.connect(connection_str)
    return connection
   ```
2. Run the following SQL in your data source to capture queries from Snowpark that are still live:

   Copy code

   ```
   SELECT
    s.session_id,
    s.program_name,
    r.status,
    t.text AS sql_text
   FROM sys.dm_exec_sessions s
   JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
   CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS t
   WHERE s.program_name = 'snowflake-snowpark-python';
   ```

## Oracle

To connect to Oracle from Snowpark, you need the following two packages:

- Snowpark: [snowflake-snowpark-python[pandas]](https://pypi.org/project/snowflake-snowpark-python/)
- The open source oracledb library: [oracledb](https://pypi.org/project/oracledb/)

The following code examples show how to connect to Oracle from a Snowpark client, stored procedures, and a Snowflake notebook.

### Use the DB-API to connect to Oracle from a Snowpark client

1. Install `snowflake-snowpark-python[pandas]` and `oracledb`:

   Copy code

   ```
   pip install snowflake-snowpark-python[pandas]
   pip install oracledb
   ```
2. Use the DB-API to pull data from Oracle and define the factory method for creating a connection to Oracle:

   Copy code

   ```
   def create_oracle_db_connection():
    import oracledb
    HOST = "<your host>"
    PORT = <your port>
    SERVICE_NAME = "<your service name>"
    USER = "<your user name>"
    PASSWORD = "your password"
    DSN = f"{HOST}:{PORT}/{SERVICE_NAME}"
    connection = oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN
    )
    # Optional: include this parameter for source tracing
    connection.clientinfo = "snowflake-snowpark-python"
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_oracle_db_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )
   ```

### Use the DB-API to connect to Oracle from a stored procedure

1. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
2. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   -- Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   CREATE OR REPLACE SECRET ora_secret
   TYPE = PASSWORD
   USERNAME = 'ora_username'
   PASSWORD = 'ora_password';

   -- configure a network rule to allow egress to the source endpoint

   CREATE OR REPLACE NETWORK RULE ora_network_rule
   MODE = EGRESS
   TYPE = HOST_PORT
   VALUE_LIST = ('ora_host:ora_port');

   -- configure an external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION ora_access_integration
   ALLOWED_NETWORK_RULES = (ora_network_rule)
   ALLOWED_AUTHENTICATION_SECRETS = (ora_secret)
   ENABLED = true;
   ```
3. Use the Snowpark Python DB-API to pull data from Oracle in a Python stored procedure:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_ora_dbapi()
    RETURNS TABLE()
    LANGUAGE PYTHON
    RUNTIME_VERSION='3.11'
    HANDLER='run'
    PACKAGES=('snowflake-snowpark-python', 'oracledb')
    EXTERNAL_ACCESS_INTEGRATIONS = (ora_access_integration)
    SECRETS = ('cred' = ora_secret )
   AS $$

   # Get user name and password from ora_secret
   import _snowflake
   username_password_object = _snowflake.get_username_password('cred')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   # Define the factory method for creating a connection to Oracle

   from snowflake.snowpark import Session

   def create_oracle_db_connection():
    import oracledb
    host = "ora_host"
    port = "ora_port"
    service_name = "ora_service"
    user = USER
    password = PASSWORD
    DSN = f"{host}:{port}/{service_name}"
    connection = oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN
    )
    # Optional: include this parameter for source tracing
    connection.clientinfo = "snowflake-snowpark-python"
    return connection

   def run(session: Session):
    # Feel free to combine local/udtf ingestion and partition column/predicates
    # as stated in the understanding parallelism section

    # Call dbapi to pull data from target table

    df = session.read.dbapi(
        create_oracle_db_connection,
        table="target_table"
    )

    # Call dbapi to pull data from target query

    df_query = session.read.dbapi(
        create_oracle_db_connection,
        query="select * from target_table"
    )

    # Pull data from target table with parallelism using partition column

    df_local_par_column = session.read.dbapi(
        create_oracle_db_connection,
        table="target_table",
        fetch_size=100000,
        num_partitions=4,
        column="ID",  # swap with the column you want your partition based on
        upper_bound=10000,
        lower_bound=0
    )

    udtf_configs = {
        "external_access_integration": "<your external access integration>"
    }

    # Pull data from target table with udtf ingestion with parallelism using predicates

    df_udtf_predicates = session.read.dbapi(
        create_oracle_db_connection,
        table="target_table",
        udtf_configs=udtf_configs,
        fetch_size=100000,
        predicates=[
            "ID < 3",
            "ID >= 3"
        ]
    )
    return df
   $$;

   CALL sp_ora_dbapi();
   ```

### Use the DB-API to connect to Oracle from a Snowflake notebook

1. From [Snowflake Notebook packages](/user-guide/ui-snowsight/notebooks-import-packages), select `snowflake-snowpark-python` and `oracledb`.
2. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
3. Configure the secret, a network rule, and EAI to allow egress to the source endpoint:

   Copy code

   ```
   -- Configure the secret, a network rule to allow egress to the source endpoint, and EAI:
   CREATE OR REPLACE SECRET mysql_secret
    TYPE = PASSWORD
    USERNAME = 'mysql_username'
    PASSWORD = 'mysql_password';
   ALTER NOTEBOOK mynotebook SET SECRETS = ('snowflake-secret-object' = mysql_secret);

   -- configure a network rule to allow egress to the source endpoint

   CREATE OR REPLACE NETWORK RULE mysql_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('mysql_host:mysql_port');

   -- configure an external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mysql_access_integration
    ALLOWED_NETWORK_RULES = (mysql_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (mysql_secret)
    ENABLED = true;
   ```
4. [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access), and then restart the notebook session.
5. Use the DB-API to pull data from Oracle in a Python cell of a Snowflake notebook:

   Copy code

   ```
   # Get user name and password from ora_secret

   import _snowflake
   username_password_object = _snowflake.get_username_password('snowflake-secret-object')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()

   # Define the factory method for creating a connection to Oracle

   def create_oracle_db_connection():
    import oracledb
    host = "ora_host"
    port = "ora_port"
    service_name = "ora_service"
    user = USER
    password = PASSWORD
    DSN = f"{host}:{port}/{service_name}"
    connection = oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN,
    )
    # Optional: include this parameter for source tracing
    connection.clientinfo = "snowflake-snowpark-python"
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_oracle_db_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_oracle_db_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )

   # Save data into sf_table

   df_udtf_predicates.write.mode("overwrite").save_as_table('sf_table')
   ```

### Source tracing when using the DB-API to connect to Oracle

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   def create_oracle_db_connection():
    import oracledb
    HOST = "myhost"
    PORT = "myport"
    SERVICE_NAME = "myservice"
    USER = "myuser"
    PASSWORD = "mypassword"
    DSN = f"{HOST}:{PORT}/{SERVICE_NAME}"
    connection = oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN,
    )
    # include this parameter for source tracing
    connection.clientinfo = "snowflake-snowpark-python"
    return connection
   ```
2. Run the following SQL in your data source to capture queries from Snowpark that are still live:

   Copy code

   ```
   SELECT
    s.sid,
    s.serial#,
    s.username,
    s.module,
    q.sql_id,
    q.sql_text,
    q.last_active_time
   FROM
    v$session s
    JOIN v$sql q ON s.sql_id = q.sql_id
   WHERE
    s.client_info = 'snowflake-snowpark-python'
   ```

## PostgreSQL

To connect to PostgreSQL from Snowpark, you need the following two packages:

- Snowpark: [snowflake-snowpark-python[pandas]](https://pypi.org/project/snowflake-snowpark-python/)
- The open source psycopg2 library: [psycopg2](https://pypi.org/project/psycopg2/)

The following code examples show how to connect to PostgreSQL from a Snowpark client, stored procedures, and a Snowflake notebook.

### Use the DB-API to connect to PostgreSQL from a Snowpark client

1. Install `psycopg2`:

   Copy code

   ```
   pip install psycopg2
   ```
2. Define the factory method for creating a connection to PostgreSQL:

   Copy code

   ```
   def create_pg_connection():
    import psycopg2
    connection = psycopg2.connect(
        host="pg_host",
        port=pg_port,
        dbname="pg_dbname",
        user="pg_user",
        password="pg_password",
        # Optional: include this parameter for source tracing
        application_name="snowflake-snowpark-python"
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_pg_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_pg_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_pg_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # Swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_pg_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )
   ```

### Use the DB-API to connect to PostgreSQL from a stored procedure

1. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
2. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   -- configure a secret

   CREATE OR REPLACE SECRET pg_secret
    TYPE = PASSWORD
    USERNAME = 'pg_username'
    PASSWORD = 'pg_password';

   -- configure a network rule.

   CREATE OR REPLACE NETWORK RULE pg_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('pg_host:pg_port');

   -- configure an external access integration.

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pg_access_integration
    ALLOWED_NETWORK_RULES = (pg_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (pg_secret)
    ENABLED = true;
   ```
3. Use the Snowpark Python DB-API to pull data from PostgreSQL in a Python stored procedure:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_pg_dbapi()
    RETURNS TABLE()
    LANGUAGE PYTHON
    RUNTIME_VERSION='3.11'
    HANDLER='run'
    PACKAGES=('snowflake-snowpark-python', 'psycopg2')
    EXTERNAL_ACCESS_INTEGRATIONS = (pg_access_integration)
    SECRETS = ('cred' = pg_secret )
   AS $$

   # Get user name and password from pg_secret

   import _snowflake
   username_password_object = _snowflake.get_username_password('cred')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   # Define the factory method for creating a connection to PostgreSQL

   from snowflake.snowpark import Session

   def create_pg_connection():
    import psycopg2
    connection = psycopg2.connect(
        host="pg_host",
        port=pg_port,
        dbname="pg_dbname",
        user=USER,
        password=PASSWORD,
        # Optional: include this parameter for source tracing
        application_name="snowflake-snowpark-python"
    )
    return connection

   def run(session: Session):

    # Feel free to combine local/udtf ingestion and partition column/predicates
    # as stated in the understanding parallelism section

    # Call dbapi to pull data from target table

    df = session.read.dbapi(
        create_pg_connection,
        table="target_table"
    )

    # Call dbapi to pull data from target query

    df_query = session.read.dbapi(
        create_pg_connection,
        query="select * from target_table"
    )

    # Pull data from target table with parallelism using partition column

    df_local_par_column = session.read.dbapi(
        create_pg_connection,
        table="target_table",
        fetch_size=100000,
        num_partitions=4,
        column="ID",  # swap with the column you want your partition based on
        upper_bound=10000,
        lower_bound=0
    )

    udtf_configs = {
        "external_access_integration": "<your external access integration>"
    }

    # Pull data from target table with udtf ingestion with parallelism using predicates

    df_udtf_predicates = session.read.dbapi(
        create_pg_connection,
        table="target_table",
        udtf_configs=udtf_configs,
        fetch_size=100000,
        predicates=[
            "ID < 3",
            "ID >= 3"
        ]
    )
    return df

   $$;
   CALL sp_pg_dbapi();
   ```

### Use the DB-API to connect to PostgreSQL from a Snowflake notebook

1. From [Snowflake Notebook packages](/user-guide/ui-snowsight/notebooks-import-packages), select `snowflake-snowpark-python` and `psycopg2`.
2. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
3. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   -- Configure the secret

   CREATE OR REPLACE SECRET pg_secret
    TYPE = PASSWORD
    USERNAME = 'pg_username'
    PASSWORD = 'pg_password';

   ALTER NOTEBOOK pg_notebook SET SECRETS = ('snowflake-secret-object' = pg_secret);

   -- Configure the network rule to allow egress to the source endpoint

   CREATE OR REPLACE NETWORK RULE pg_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('pg_host:pg_port');

   -- Configure external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pg_access_integration
    ALLOWED_NETWORK_RULES = (pg_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (pg_secret)
    ENABLED = true;
   ```
4. [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access), and then restart the notebook session.
5. Use the DB-API to pull data from PostgreSQL in a Python cell of a Snowflake notebook:

   Copy code

   ```
   # Get the user name and password from :code:`pg_secret`

   import _snowflake
   username_password_object = _snowflake.get_username_password('snowflake-secret-object')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()

   # Define the factory method for creating a connection to PostgreSQL

   def create_pg_connection():
    import psycopg2
    connection = psycopg2.connect(
        host="pg_host",
        port=pg_port,
        dbname="pg_dbname",
        user=USER,
        password=PASSWORD,
        # Optional: include this parameter for source tracing
        application_name="snowflake-snowpark-python"
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_pg_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_pg_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_pg_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_pg_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )

   # Save data into sf_table

   df.write.mode("overwrite").save_as_table('sf_table')
   # Get the user name and password from :code:`pg_secret`
   ```

### Source tracing when using the DB-API to connect to PostgreSQL

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   def create_pg_connection():
    import psycopg2
    connection = psycopg2.connect(
        host="pg_host",
        port=pg_port,
        dbname="pg_dbname",
        user="pg_user",
        password="pg_password",
        # Include this parameter for source tracing
        application_name="snowflake-snowpark-python"
    )
    return connection
   ```
2. Run the following SQL in your data source to capture queries from Snowpark that are still live:

   Copy code

   ```
   SELECT
    pid,
    usename AS username,
    datname AS database,
    application_name,
    client_addr,
    state,
    query_start,
    query
   FROM
    pg_stat_activity
   WHERE
    application_name = 'snowflake-snowpark-python';
   ```

## MySQL

To connect to MySQL from Snowpark, you need the following two packages:

- Snowpark: [snowflake-snowpark-python[pandas]](https://pypi.org/project/snowflake-snowpark-python/)
- The open source pymysql library: [PyMySQL](https://pypi.org/project/PyMySQL/)

The following code examples show how to connect to MySQL from a Snowpark client, stored procedures, and a Snowflake notebook.

### Use the DB-API to connect to MySQL from a Snowpark client

1. Install pymysql:

   Copy code

   ```
   pip install snowflake-snowpark-python[pandas]
   pip install pymysql
   ```
2. Define the factory method for creating a connection to MySQL:

   Copy code

   ```
   def create_mysql_connection():
    import pymysql
    connection = pymysql.connect(
        host="mysql_host",
        port=mysql_port,
        database="mysql_db",
        user="mysql_user",
        password="mysql_password",
        # Optional: include this parameter for source tracing
        init_command="SET @program_name='snowflake-snowpark-python';"
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_mysql_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_mysql_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_mysql_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_mysql_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )
   ```

### Use the DB-API to connect to MySQL from a stored procedure

1. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
2. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   CREATE OR REPLACE SECRET mysql_secret
    TYPE = PASSWORD
    USERNAME = 'mysql_username'
    PASSWORD = 'mysql_password';

   -- configure a network rule.

   CREATE OR REPLACE NETWORK RULE mysql_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('mysql_host:mysql_port');

   -- configure an external access integration

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mysql_access_integration
    ALLOWED_NETWORK_RULES = (mysql_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (mysql_secret)
        ENABLED = true;
   ```
3. Use the Snowpark Python DB-API to pull data from MySQL in a Python stored procedure:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_mysql_dbapi()
    RETURNS TABLE()
    LANGUAGE PYTHON
    RUNTIME_VERSION='3.11'
    HANDLER='run'
    PACKAGES=('snowflake-snowpark-python', 'pymysql')
    EXTERNAL_ACCESS_INTEGRATIONS = (mysql_access_integration)
    SECRETS = ('cred' = mysql_secret )
   AS $$

   # Get user name and password from mysql_secret

   import _snowflake
   username_password_object = _snowflake.get_username_password('cred')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   # Define the factory method for creating a connection to MySQL

   from snowflake.snowpark import Session

   def create_mysql_connection():
    import pymysql
    connection = pymysql.connect(
        host="mysql_host",
        port=mysql_port,
        dbname="mysql_dbname",
        user=USER,
        password=PASSWORD,
        # Optional: include this parameter for source tracing
        init_command="SET @program_name='snowflake-snowpark-python';"
    )
    return connection

   # Using Snowpark Python DB-API to pull data from MySQL in a Python stored procedure.

   def run(session: Session):
    # Feel free to combine local/udtf ingestion and partition column/predicates
    # as stated in the understanding parallelism section

    # Call dbapi to pull data from target table

    df = session.read.dbapi(
        create_mysql_connection,
        table="target_table"
    )

    # Call dbapi to pull data from target query

    df_query = session.read.dbapi(
        create_mysql_connection,
        query="select * from target_table"
    )

    # Pull data from target table with parallelism using partition column

    df_local_par_column = session.read.dbapi(
        create_mysql_connection,
        table="target_table",
        fetch_size=100000,
        num_partitions=4,
        column="ID",  # swap with the column you want your partition based on
        upper_bound=10000,
        lower_bound=0
    )

    udtf_configs = {
        "external_access_integration": "<your external access integration>"
    }

    # Pull data from target table with udtf ingestion with parallelism using predicates

    df_udtf_predicates = session.read.dbapi(
        create_mysql_connection,
        table="target_table",
        udtf_configs=udtf_configs,
        fetch_size=100000,
        predicates=[
            "ID < 3",
            "ID >= 3"
        ]
    )
    return df
   $$;

   CALL sp_mysql_dbapi();
   ```

### Use the DB-API to connect to MySQL from a Snowflake notebook

1. From [Snowflake Notebook packages](/user-guide/ui-snowsight/notebooks-import-packages), select `snowflake-snowpark-python` and `pymysql`.
2. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
3. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   CREATE OR REPLACE SECRET mysql_secret
    TYPE = PASSWORD
    USERNAME = 'mysql_username'
    PASSWORD = 'mysql_password';

   ALTER NOTEBOOK mynotebook SET SECRETS = ('snowflake-secret-object' = mysql_secret);

   -- configure a network rule.
   CREATE OR REPLACE NETWORK RULE mysql_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('mysql_host:mysql_port');

   -- configure an EAI
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mysql_access_integration
    ALLOWED_NETWORK_RULES = (mysql_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (mysql_secret)
    ENABLED = true;
   ```
4. [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access), and then restart the notebook session.
5. Use the DB-API to pull data from MySQL in a Python cell of a Snowflake notebook:

   Copy code

   ```
   # Get user name and password from mysql_secret
   import _snowflake
   username_password_object = _snowflake.get_username_password('snowflake-secret-object')
   USER = username_password_object.username
   PASSWORD = username_password_object.password

   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()

   # Define the factory method for creating a connection to MySQL

   def create_mysql_connection():
    import pymysql
    connection = pymysql.connect(
        host="mysql_host",
        port=mysql_port,
        dbname="mysql_dbname",
        user=USER,
        password=PASSWORD,
        # Optional: include this parameter for source tracing
        init_command="SET @program_name='snowflake-snowpark-python';"
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_mysql_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_mysql_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_mysql_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_mysql_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )

   # Save data into sf_table

   df.write.mode("overwrite").save_as_table('sf_table')
   ```

### Source tracing when using the DB-API to connect to MySQL

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   def create_mysql_connection():
    import pymysql
    connection = pymysql.connect(
        host="mysql_host",
        port=mysql_port,
        database="mysql_db",
        user="mysql_user",
        password="mysql_password",
        # include this parameter for source tracing
        init_command="SET @program_name='snowflake-snowpark-python';"
    )
    return connection
   ```
2. Run the following SQL in your data source to capture queries from Snowpark:

   Copy code

   ```
   SELECT *
   FROM performance_schema.events_statements_history_long
   WHERE THREAD_ID = (
    SELECT THREAD_ID
    FROM performance_schema.events_statements_history_long
    WHERE SQL_TEXT = "SET @program_name='snowflake-snowpark-python'"
    ORDER BY EVENT_ID DESC
    LIMIT 1
   )
   ```

## Databricks

To connect to Databricks from Snowpark, you need the following two packages:

- Snowpark: [snowflake-snowpark-python[pandas]](https://pypi.org/project/snowflake-snowpark-python/)
- The open source psycopg2 library: [databricks-sql-connector](https://pypi.org/project/databricks-sql-connector/)

The following code examples show how to connect to Databricks from a Snowpark client, stored procedures, and a Snowflake notebook.

### Use the DB-API to connect to Databricks from a Snowpark client

1. Install databricks-sql-connector:

   Copy code

   ```
   pip install snowflake-snowpark-python[pandas]
   pip install databricks-sql-connector
   ```
2. Define the factory method for creating a connection to Databricks:

   Copy code

   ```
   def create_dbx_connection():
    import databricks.sql
    connection = databricks.sql.connect(
        server_hostname=HOST,
        http_path=PATH,
        access_token=ACCESS_TOKEN
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_dbx_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_dbx_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_dbx_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_dbx_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )
   ```

### Use the DB-API to connect to Databricks from a stored procedure

1. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
2. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   CREATE OR REPLACE SECRET dbx_secret
    TYPE = GENERIC_STRING
    SECRET_STRING = 'dbx_access_token';

   CREATE OR REPLACE NETWORK RULE dbx_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('dbx_host:dbx_port');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbx_access_integration
    ALLOWED_NETWORK_RULES = (dbx_network_rule)
    ALLOWED_AUTHENTICATION_SECRETS = (dbx_secret)
    ENABLED = true;
   ```
3. Use the Snowpark Python DB-API to pull data from Databricks in a Python stored procedure:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_dbx_dbapi()
    RETURNS TABLE()
    LANGUAGE PYTHON
    RUNTIME_VERSION='3.11'
    HANDLER='run'
    PACKAGES=('snowflake-snowpark-python', 'databricks-sql-connector')
    EXTERNAL_ACCESS_INTEGRATIONS = (dbx_access_integration)
    SECRETS = ('cred' = dbx_secret )
   AS $$

   # Get user name and password from dbx_secret

   import _snowflake
   ACCESS_TOKEN = _snowflake.get_generic_secret_string('cred')

   from snowflake.snowpark import Session

   # Define the method for creating a connection to Databricks
   def create_dbx_connection():
    import databricks.sql
    connection = databricks.sql.connect(
        server_hostname="dbx_host",
        http_path="dbx_path",
        access_token=ACCESS_TOKEN,
    )
    return connection

   # Using Snowpark Python DB-API to pull data from Databricks in a Python stored procedure.

   def run(session: Session):
    # Feel free to combine local/udtf ingestion and partition column/predicates
    # as stated in the understanding parallelism section

    # Call dbapi to pull data from target table

    df = session.read.dbapi(
        create_dbx_connection,
        table="target_table"
    )

    # Call dbapi to pull data from target query

    df_query = session.read.dbapi(
        create_dbx_connection,
        query="select * from target_table"
    )

    # Pull data from target table with parallelism using partition column

    df_local_par_column = session.read.dbapi(
        create_dbx_connection,
        table="target_table",
        fetch_size=100000,
        num_partitions=4,
        column="ID",  # swap with the column you want your partition based on
        upper_bound=10000,
        lower_bound=0
    )

    udtf_configs = {
        "external_access_integration": "<your external access integration>"
    }

    # Pull data from target table with udtf ingestion with parallelism using predicates

    df_udtf_predicates = session.read.dbapi(
        create_dbx_connection,
        table="target_table",
        udtf_configs=udtf_configs,
        fetch_size=100000,
        predicates=[
            "ID < 3",
            "ID >= 3"
        ]
    )
    return df

   $$;

   CALL sp_dbx_dbapi();
   ```

### Use the DB-API to connect to Databricks from a Snowflake notebook

1. From [Snowflake Notebook packages](/user-guide/ui-snowsight/notebooks-import-packages), select `snowflake-snowpark-python` and `databricks-sql-connector`.
2. Configure an external access integration (EAI), which is required to allow Snowflake to connect to the source endpoint.

   Note

   [PrivateLink](/user-guide/admin-security-privatelink#label-aws-privatelink-connect) is recommended for secure data transfer, especially when you’re dealing with
   sensitive information. Ensure that your Snowflake account has the necessary PrivateLink privileges enabled and that the
   PrivateLink feature is configured and active in your Snowflake Notebook environment.
3. Configure the secret, a network rule to allow egress to the source endpoint, and EAI:

   Copy code

   ```
   CREATE OR REPLACE SECRET dbx_secret
   TYPE = GENERIC_STRING
   SECRET_STRING = 'dbx_access_token';

   ALTER NOTEBOOK mynotebook SET SECRETS = ('snowflake-secret-object' = dbx_secret);

   CREATE OR REPLACE NETWORK RULE dbx_network_rule
   MODE = EGRESS
   TYPE = HOST_PORT
   VALUE_LIST = ('dbx_host:dbx_port');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbx_access_integration
   ALLOWED_NETWORK_RULES = (dbx_network_rule)
   ALLOWED_AUTHENTICATION_SECRETS = (dbx_secret)
   ENABLED = true;
   ```
4. [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access), and then restart the notebook session.
5. Use the DB-API to pull data from Databricks in a Python cell of a Snowflake notebook:

   Copy code

   ```
   # Get user name and password from dbx_secret

   import _snowflake
   ACCESS_TOKEN = _snowflake.get_generic_secret_string('cred')

   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()

   # Define the factory method for creating a connection to Databricks

   def create_dbx_connection():
    import databricks.sql
    connection = databricks.sql.connect(
        server_hostname="dbx_host",
        http_path="dbx_path",
        access_token=ACCESS_TOKEN,
    )
    return connection

   # Feel free to combine local/udtf ingestion and partition column/predicates as
   # stated in the understanding parallelism section

   # Call dbapi to pull data from target table

   df = session.read.dbapi(
    create_dbx_connection,
    table="target_table"
   )

   # Call dbapi to pull data from target query

   df_query = session.read.dbapi(
    create_dbx_connection,
    query="select * from target_table"
   )

   # Pull data from target table with parallelism using partition column

   df_local_par_column = session.read.dbapi(
    create_dbx_connection,
    table="target_table",
    fetch_size=100000,
    num_partitions=4,
    column="ID",  # swap with the column you want your partition based on
    upper_bound=10000,
    lower_bound=0
   )

   udtf_configs = {
    "external_access_integration": "<your external access integration>"
   }

   # Pull data from target table with udtf ingestion with parallelism using predicates

   df_udtf_predicates = session.read.dbapi(
    create_dbx_connection,
    table="target_table",
    udtf_configs=udtf_configs,
    fetch_size=100000,
    predicates=[
        "ID < 3",
        "ID >= 3"
    ]
   )

   # Save data into sf_table

   df.write.mode("overwrite").save_as_table('sf_table')
   ```

### Source tracing when using the DB-API to connect to Databricks

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   def create_dbx_connection():
    import databricks.sql
    connection = databricks.sql.connect(
        server_hostname=HOST,
        http_path=PATH,
        access_token=ACCESS_TOKEN,
        # include this parameter for source tracing
        user_agent_entry="snowflake-snowpark-python"
    )
    return connection
   ```
2. Navigate to query history on the Databricks console and search for the query whose source is `snowflake-snowpark-python`.

## Limitations

The Snowpark Python DB-API supports only Python DB-API 2.0–compliant drivers (for example, `pyodbc` or *oracledb*). JDBC drivers are not supported in this release.
