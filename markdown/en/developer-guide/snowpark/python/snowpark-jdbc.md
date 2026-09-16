[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

# Using the Snowpark Python JDBC

With the Snowpark Python JDBC, Snowpark Python users can programmatically pull data from external databases into Snowflake. This allows you to connect to external databases using JDBC drivers.

With these APIs, you can seamlessly pull data into Snowflake tables and transform it using [Snowpark DataFrames](/developer-guide/snowpark/python/working-with-dataframes) for advanced analytics.

The [JDBC](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.jdbc) can be used in a similar way as the Spark JDBC API. Most parameters are designed to be identical or similar for better parity. For more information that compares the Snowpark Python JDBC with the Spark JDBC API, see the following table:

## Snowpark JDBC parameters

| Parameter | Snowpark Python JDBC |
| --- | --- |
| `url` | A connection string used to connect to the external data source via the JDBC driver |
| `udtf_configs` | A dictionary containing the necessary configurations for the UDTF creation |
| `properties` | A dictionary containing the key-value pair that is needed during establishing JDBC connection |
| `table` | Table in the source database |
| `query` | SQL query wrapped as a subquery for reading data |
| `column` | Partitioning column for parallel reads |
| `lower_bound` | Lower bound for partitioning |
| `upper_bound` | Upper bound for partitioning |
| `num_partitions` | Number of partitions for parallelism |
| `query_timeout` | The timeout duration for SQL execution, measured in seconds. |
| `fetch_size` | Number of rows fetched per round trip |
| `custom_schema` | Custom schema for pulling data from external databases |
| `predicates` | List of conditions for WHERE clause partitions |
| `session_init_statement` | Executes a SQL or PL/SQL statement upon session initialization |

Expand

Show lessSee more

## Understanding parallelism

Snowpark Python JDBC currently has one form of underlying ingestion mechanism:

UDTF ingestion
:   All workloads run on the Snowflake server. Snowpark creates a Java UDTF and invoke it in parallel to ingest data into a Snowflake temporary table. Thus the `udtf_configs` parameter is required for this feature.

The Snowpark Python JDBC has two ways to parallelize and accelerate ingestion:

Partition column
:   This method divides source data into a number of partitions based on four parameters when users call `jdbc()`:

    - `column`
    - `lower_bound`
    - `upper_bound`
    - `num_partitions`

    These four parameters have to be set at the same time and the `column` must be numeric or date type.

Predicates
:   This method divides source data into partitions based on parameter predicates, which are a list of expressions suitable for inclusion in `WHERE` clauses, where each expression defines a partition. Predicates provide a more flexible way of dividing partitions; for example, you can divide partitions on boolean or non-numeric columns.

The Snowpark Python JDBC also allows adjusting parallelism level within a partition:

Fetch\_size
:   Within a partition, the API fetches rows in chunks defined by `fetch_size`. These rows are written to Snowflake in parallel as they are fetched, which allows reading and writing to overlap and maximizes throughput.

## Using JDBC to ingest data from external data source

### Using JDBC to ingest data from a Snowpark client

1. Upload the JDBC driver jar file to a Snowflake stage using Snowpark or Snowsight

   - Upload using Snowpark.
     In Snowpark, after creating a session, run the following code:

     Copy code

     ```
     session.file.put("<your directory>/<your file name>", "@<your stage name>/<stage path>")
     ```
   - Upload using Snowsight as described in the following steps.

     1. In Snowsight, click on **Catalog** -> **Explorer**.
     2. In the left search bar of databases, click on **[your database name]** -> **[your schema name]** -> **stages** -> **[your stage name]**.
     3. Click the **“+File”** button on the top right corner of the stage page.
2. Configure the secret, network rule, and external access integration.

   Copy code

   ```
   -- Configure a secret to allow egress to the source endpoint
   CREATE OR REPLACE SECRET <your secret>
    TYPE = PASSWORD
    USERNAME = '<your username>'
    PASSWORD = '<your password>';

   -- Configure a network rule to allow egress to the source endpoint
   CREATE OR REPLACE NETWORK RULE <your network rule>
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = ('<your host>:<your port>');

   -- Configure an external access integration
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION <your integration>
     ALLOWED_NETWORK_RULES = (<your network rule>)
     ALLOWED_AUTHENTICATION_SECRETS = (<your secret>)
     ENABLED = true;
   ```
3. Pull data from the target using Snowpark JDBC from a Snowpark client.

   Copy code

   ```
   connection_str=f"jdbc:<your dbms>://<your host>:<your port>/<your db>"
   udtf_configs = {
    "external_access_integration": "<your integration>",
    "secret": "<your secret>",
    "imports": ["<your stage path to jdbc jar file>"]
   }

   # Call jdbc to pull data from target table
   df_table = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
    )

   # Call jdbc to pull data from target query
   df_query = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        query="select * from <your table>",
    )

   # Pull data from target table with parallelism using partition column
   df_table_partition_column = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
        fetch_size=100000,
        num_partitions=4,
        column="ID",
        upper_bound=10000,
        lower_bound=0
    )

   # Pull data from target table with parallelism using predicates
   df_table_predicates = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
        fetch_size=100000,
        predicates = [
            "ID < 3",
            "ID >= 3"
        ]
    )
   ```

### Using JDBC to ingest data from a stored procedure

1. Upload JDBC driver jar file to Snowflake stage using Snowsight

   - In Snowsight, click on **Catalog** -> **Explorer**
   - In the left search bar of databases, click **[your database name]** -> **[your schema name]** -> **stages** -> **[your stage name]**.
   - Click the **“+File”** button on the top right corner of the stage page.
2. Configure secret, network rule, and external access integration.

   Copy code

   ```
   -- Configure a secret to allow egress to the source endpoint
   CREATE OR REPLACE SECRET <your secret>
    TYPE = PASSWORD
    USERNAME = '<your username>'
    PASSWORD = '<your password>';

   -- Configure a network rule to allow egress to the source endpoint
   CREATE OR REPLACE NETWORK RULE <your network rule>
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = ('<your host>:<your port>');

   -- Configure an external access integration
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION <your integration>
     ALLOWED_NETWORK_RULES = (<your network rule>)
     ALLOWED_AUTHENTICATION_SECRETS = (<your secret>)
     ENABLED = true;
   ```
3. Pull data from target using Snowpark JDBC from a stored procedure.

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE sp_jdbc()
   RETURNS STRING
   LANGUAGE PYTHON
   RUNTIME_VERSION = '3.10'
   PACKAGES = ('snowflake-snowpark-python')
   HANDLER = 'run'
   AS
   $$
   import time
   def run(session):
    connection_str=f"jdbc:<your dbms>://<your host>:<your port>/<your db>"
    udtf_configs = {
        "external_access_integration": "<your integration>",
        "secret": "<your secret>",
        "imports": ["<your stage path to jdbc jar file>"]
    }

    # Call jdbc to pull data from target table
    df_table = session.read.jdbc(
            url=connection_str,
            udtf_configs=udtf_configs,
            table="<your table>",
        )

    # Call jdbc to pull data from target query
    df_query = session.read.jdbc(
            url=connection_str,
            udtf_configs=udtf_configs,
            query="select * from <your table>",
        )

    # Pull data from target table with parallelism using partition column
    df_table_partition_column = session.read.jdbc(
            url=connection_str,
            udtf_configs=udtf_configs,
            table="<your table>",
            fetch_size=100000,
            num_partitions=4,
            column="ID",
            upper_bound=10000,
            lower_bound=0
        )

    # Pull data from target table with parallelism using predicates
    df_table_predicates = session.read.jdbc(
            url=connection_str,
            udtf_configs=udtf_configs,
            table="<your table>",
            fetch_size=100000,
            predicates = [
                "ID < 3",
                "ID >= 3"
            ]
        )
    df_table.write.save_as_table("snowflake_table", mode="overwrite")
    return f"success"

   $$
   ;

   call sp_jdbc();
   select * from snowflake_table ;
   ```

### Using JDBC to ingest data from a Snowflake notebook

1. Upload JDBC driver jar file to Snowflake stage using Snowsight

   - In Snowsight, click on **Catalog** -> **Explorer**
   - In the left search bar of databases, click **[your database name]** -> **[your schema name]** -> **stages** -> **[your stage name]**.
   - Click the **“+File”** button on the top right corner of the stage page.
2. Configure secret, network rule, and external access integration.

   Copy code

   ```
   -- Configure a secret to allow egress to the source endpoint
   CREATE OR REPLACE SECRET <your secret>
    TYPE = PASSWORD
    USERNAME = '<your username>'
    PASSWORD = '<your password>';

   -- Configure a network rule to allow egress to the source endpoint
   CREATE OR REPLACE NETWORK RULE <your network rule>
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = ('<your host>:<your port>');

   -- Configure an external access integration
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION <your integration>
     ALLOWED_NETWORK_RULES = (<your network rule>)
     ALLOWED_AUTHENTICATION_SECRETS = (<your secret>)
     ENABLED = true;
   ```
3. Pull data from target using Snowpark JDBC from a Snowflake notebook.

   Copy code

   ```
   import snowflake.snowpark.context
   session = snowflake.snowpark.context.get_active_session()
   connection_str=f"jdbc:<your dbms>://<your host>:<your port>/<your db>"
   udtf_configs = {
        "external_access_integration": "<your integration>",
        "secret": "<your secret>",
        "imports": ["<your stage path to jdbc jar file>"]
    }

   # Call jdbc to pull data from target table
   df_table = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
    )

   # Call jdbc to pull data from target query
   df_query = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        query="select * from <your table>",
    )

   # Pull data from target table with parallelism using partition column
   df_table_partition_column = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
        fetch_size=100000,
        num_partitions=4,
        column="ID",
        upper_bound=10000,
        lower_bound=0
    )

   # Pull data from target table with parallelism using predicates
   df_table_predicates = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
        fetch_size=100000,
        predicates = [
            "ID < 3",
            "ID >= 3"
        ]
    )
   ```

## Source tracing

### Source tracing when using Snowpark JDBC connect to MySQL

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   connection_str="jdbc:mysql://<your host>:<your port>/<your db>?applicationName=snowflake-snowpark-python"
   udtf_configs = {
    "external_access_integration": "<your integration>",
    "secret": "<your secret>",
    "imports": ["<your stage path to jdbc jar file>"]
   }

   # Call dbapi to pull data from target table
   df_table = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
    )
   ```
2. Run the following SQL in your data source to capture queries from Snowpark that are still live:

   Copy code

   ```
   SELECT *
   FROM performance_schema.events_statements_history_long
   WHERE THREAD_ID = (
     SELECT THREAD_ID, NAME FROM performance_schema.threads WHERE NAME LIKE '%snowflake-snowpark-python%';
   )
   ```

### Source tracing when using Snowpark JDBC to connect to SQL Server

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   connection_str="jdbc:mssql://<your host>:<your port>/<your db>?applicationName=snowflake-snowpark-python"
   udtf_configs = {
   "external_access_integration": "<your integration>",
   "secret": "<your secret>",
   "imports": ["<your stage path to jdbc jar file>"]
   }
   # Call dbapi to pull data from target table
   df_table = session.read.jdbc(
      url=connection_str,
      udtf_configs=udtf_configs,
      table="<your table>",
     )
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

### Source tracing when using Snowpark JDBC to connect to PostgresSQL

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   connection_str="jdbc:postgres://<your host>:<your port>/<your db>?applicationName=snowflake-snowpark-python"
   udtf_configs = {
   "external_access_integration": "<your integration>",
   "secret": "<your secret>",
   "imports": ["<your stage path to jdbc jar file>"]
   }

   # Call dbapi to pull data from target table
   df_table = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
    )
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

### Source tracing when using Snowpark JDBC to connect to Oracle

1. Include a tag of Snowpark in your create connection function:

   Copy code

   ```
   connection_str="jdbc:oracle://<your host>:<your port>/<your db>?applicationName=snowflake-snowpark-python"
   udtf_configs = {
   "external_access_integration": "<your integration>",
   "secret": "<your secret>",
   "imports": ["<your stage path to jdbc jar file>"]
   }
   # Call dbapi to pull data from target table
   df_table = session.read.jdbc(
        url=connection_str,
        udtf_configs=udtf_configs,
        table="<your table>",
    )
   ```
2. Run the following SQL in your data source to capture queries from Snowpark that are still live:

   Copy code

   ```
   SELECT
     sid,
     serial#,
     username,
     program,
     module,
     action,
     client_identifier,
     client_info,
     osuser,
     machine
   FROM v$session
   WHERE program = 'snowflake-snowpark-python';
   ```

## Common DBMS and Type Support

The following is a certified list of data types of different DBMS systems. If your source data involves other data types, Snowpark Python JDBC will try to map them to best-effort Snowflake data types, or fall back to strings.

### Oracle

- INTEGER
- NUMBER
- BINARY\_FLOAT
- BINARY\_DOUBLE
- VARCHAR2
- CHAR
- CLOB
- NCHAR
- NVARCHAR2
- NCLOB
- DATE
- TIMESTAMP
- TIMESTAMP WITH TIME ZONE
- TIMESTAMP WITH LOCAL TIME ZONE
- RAW

### PostgresSQL

- BIGINT
- BIGSERIAL
- BIT
- BIT VARYING
- BOOLEAN
- BOX
- BYTEA
- CHAR
- VARCHAR
- CIDR
- CIRCLE
- DATE
- DOUBLE PRECISION
- INET
- INTEGER
- INTERVAL
- JSON
- JSONB
- LINE
- LSEG
- MACADDR
- POINT
- POLYGON
- REAL
- SMALLINT
- SMALLSERIAL
- SERIAL
- TEXT
- TIME
- TIMESTAMP
- TIMESTAMPTZ
- TSQUERY
- TSVECTOR
- TXID\_SNAPSHOT
- UUID
- XML

### MySQL

- INT
- DECIMAL
- INT
- TINYINT
- SMALLINT
- MEDIUMINT
- BIGINT
- YEAR
- FLOAT
- DOUBLE
- CHAR
- VARCHAR
- TINYTEXT
- TEXT
- MEDIUMTEXT
- LONGTEXT
- ENUM
- SET
- BIT
- BINARY
- VARBINARY
- TINYBLOB
- BLOB
- MEDIUMBLOB
- LONGBLOB
- DATE
- DATETIME
- TIMESTAMP
- TIME
- JSON

### SQL Server

- INT
- BIGINT
- INT
- SMALLINT
- TINYINT
- BIT
- DECIMAL
- NUMERIC
- MONEY
- SMALLMONEY
- FLOAT
- REAL
- DATE
- TIME
- DATETIME
- DATETIME2
- SMALLDATETIME
- CHAR
- VARCHAR
- VARCHAR(MAX)
- TEXT
- NCHAR
- NVARCHAR
- NVARCHAR(MAX)
- NTEXT
- BINARY
- VARBINARY
- VARBINARY(MAX)
- IMAGE
- UNIQUEIDENTIFIER
- TIMESTAMP

### Databricks

Connecting to Databricks using Snowpark Python JDBC is currently not supported.
