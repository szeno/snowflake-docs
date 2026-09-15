# Load data into Apache Iceberg™ tables

Snowflake supports the following options for loading data into a Snowflake-managed Iceberg table:

- [INSERT](/sql-reference/sql/insert)
- [COPY INTO <table>](/sql-reference/sql/copy-into-table)
- [Snowpipe](/user-guide/data-load-snowpipe-intro)
- [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg)
- [Snowpipe Streaming Classic with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-iceberg)
- [Using the Snowflake Connector for Kafka with Apache Iceberg™ tables](/user-guide/kafka-connector/classic/iceberg)

## File formats

You can load data into an Iceberg table from files in any of the formats supported for loading into standard Snowflake tables.

For CSV, JSON, Avro, and ORC,
Snowflake converts the data from non-Parquet file formats into Iceberg Parquet files and stores the data in the base location of the Iceberg table. Only the default
`LOAD_MODE = FULL_INGEST` option is supported for these file format loading scenarios that require type conversion.

For Apache Parquet files, Snowflake loads the data directly into table columns and lets you choose from the following `LOAD_MODE` options:

- `FULL_INGEST`: Scans the files and rewrites the Parquet data under the base location of the Iceberg table.
- `ADD_FILES_COPY`: Binary copies the Iceberg-compatible Apache Parquet files that aren’t registered with an Iceberg catalog
  into the base location of the Iceberg table, then registers the files to the Iceberg table.

For more information, see [COPY INTO <table>](/sql-reference/sql/copy-into-table).

Important

Registering Parquet files by using ADD\_FILES\_COPY isn’t recommended if those files are already part of another Iceberg table.

The best practice for converting externally-managed Iceberg tables to Snowflake-managed Iceberg tables without rewriting files is to use
the [ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed) command.

## Considerations and limitations when you load data into Iceberg tables

- To load the row lineage metadata columns for Parquet files, which are `_row_id` and `_last_updated_sequence_number`, you
  must use the FULL\_INGEST option. The other LOAD\_MODE
  options aren’t supported. However, Parquet files that contain row lineage are likely already part of an Iceberg v3 table. For the best
  practice on how to handle Parquet files that are already part of another Iceberg table, see the [note above](#label-tables-iceberg-load-mode).

## Example: Load Iceberg-compatible Parquet files

This example shows how to create an Iceberg table, and then load data into it from
Iceberg-compatible Parquet data files on an external stage.

Important

Registering Parquet files by using ADD\_FILES\_COPY isn’t recommended if those files are already part of another Iceberg table. The best
practice for converting externally managed Iceberg tables to Snowflake-managed Iceberg tables without rewriting files is to use the
[ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed) command.

For demonstration purposes, this example uses the following resources:

- An external volume named `iceberg_ingest_vol`. To create
  an external volume, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).
- An external stage named `my_parquet_stage` with Iceberg-compatible Parquet files on it. To create an external stage, see
  [CREATE STAGE](/sql-reference/sql/create-stage).

1. Create a file format object that describes the staged Parquet files, using the required configuration for copying
   Iceberg-compatible Parquet data (`TYPE = PARQUET USE_VECTORIZED_SCANNER = TRUE`):

   Copy code

   ```
   CREATE OR REPLACE FILE FORMAT my_parquet_format
     TYPE = PARQUET
     USE_VECTORIZED_SCANNER = TRUE;
   ```
2. Create a Snowflake-managed Iceberg table, defining columns with data types that are compatible with the source Parquet file data types:

   This example uses case-sensitive column names. You must surround the column names in double quotes when you create the Iceberg table, and
   specify the column names exactly as they appear in your Parquet footer.

   Copy code

   ```
   CREATE OR REPLACE ICEBERG TABLE customer_iceberg_ingest (
     "c_custkey" INTEGER,
     "c_name" STRING,
     "c_address" STRING,
     "c_nationkey" INTEGER,
     "c_phone" STRING,
     "c_acctbal" INTEGER,
     "c_mktsegment" STRING,
     "c_comment" STRING
   )
     CATALOG = 'SNOWFLAKE'
     EXTERNAL_VOLUME = 'iceberg_ingest_vol'
     BASE_LOCATION = 'customer_iceberg_ingest/';
   ```

   Note

   The example statement specifies Iceberg data types that map to Snowflake data types. For more information,
   see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).
3. To load the data from the staged Parquet files, which are located directly under the stage URL path, into the Iceberg table, use a COPY INTO statement:

   In COPY INTO *<table>* statements with `LOAD_MODE = ADD_FILES_COPY`, only `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE` is supported.

   Copy code

   ```
   COPY INTO customer_iceberg_ingest
     FROM @my_parquet_stage
     FILE_FORMAT = 'my_parquet_format'
     LOAD_MODE = ADD_FILES_COPY
     PURGE = TRUE
     MATCH_BY_COLUMN_NAME = CASE_SENSITIVE;
   ```

   Note

   The example specifies `LOAD_MODE = ADD_FILES_COPY`, which tells Snowflake to copy the files into your external volume location,
   and then register the files to the table.

   This option avoids file charges, because Snowflake doesn’t scan the source Parquet files and rewrite the data into new Parquet files.

   Output:

   ```
   +---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
   | file                                                          | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
   |---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
   | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_008.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_006.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_005.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_002.parquet | LOADED |           5 |           5 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_010.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   +---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
   ```
4. Query the table:

   Copy code

   ```
   SELECT
    c_custkey,
    c_name,
    c_mktsegment
     FROM customer_iceberg_ingest
     LIMIT 10;
   ```

   Output:

   ```
   +-----------+--------------------+--------------+
   | C_CUSTKEY | C_NAME             | C_MKTSEGMENT |
   |-----------+--------------------+--------------|
   |     75001 | Customer#000075001 | FURNITURE    |
   |     75002 | Customer#000075002 | FURNITURE    |
   |     75003 | Customer#000075003 | MACHINERY    |
   |     75004 | Customer#000075004 | AUTOMOBILE   |
   |     75005 | Customer#000075005 | FURNITURE    |
   |         1 | Customer#000000001 | BUILDING     |
   |         2 | Customer#000000002 | AUTOMOBILE   |
   |         3 | Customer#000000003 | AUTOMOBILE   |
   |         4 | Customer#000000004 | MACHINERY    |
   |         5 | Customer#000000005 | HOUSEHOLD    |
   +-----------+--------------------+--------------+
   ```

## Example: Load Iceberg-compatible Parquet files into the table created with INFER\_SCHEMA function

This example covers how to do the following:

1. Create an Apache Iceberg™ table by using the [INFER\_SCHEMA](/sql-reference/functions/infer_schema) function.
2. Load data into it from Iceberg-compatible Parquet data files on an external stage.

For demonstration purposes, this example uses the following resources:

- An external volume named `iceberg_ingest_vol`. To create
  an external volume, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).
- An external stage named `my_parquet_stage` with Iceberg-compatible Parquet files on it. To create an external stage, see
  [CREATE STAGE](/sql-reference/sql/create-stage).

1. Create a file format object that describes the staged Parquet files, using the required configuration for copying
   Iceberg-compatible Parquet data (`TYPE = PARQUET USE_VECTORIZED_SCANNER = TRUE`):

   Copy code

   ```
   CREATE OR REPLACE FILE FORMAT my_parquet_format
     TYPE = PARQUET
     USE_VECTORIZED_SCANNER = TRUE;
   ```
2. Retrieve the column definitions for Parquet files in the `my_parquet_stage` stage:

   Copy code

   ```
   SELECT *
     FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@my_parquet_stage/customer_iceberg/files-to-ingest/'
      , FILE_FORMAT=>'my_parquet_format'
      , KIND => 'ICEBERG'
      )
    );
   ```

   Output:

   ```
   +-------------+---------+----------+---------------------+------------------------------------------------------+----------+
   | COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                                            | ORDER_ID |
   |-------------+---------+----------+---------------------+------------------------------------------------------|----------+
   | id          | INT     | False    | $1:id::INT          | customer_iceberg/files-to-ingest/customers.parquet   | 0        |
   | custnum     | INT     | False    | $1:custnum::INT     | customer_iceberg/files-to-ingest/customers.parquet   | 1        |
   +-------------+---------+----------+---------------------+------------------------------------------------------+----------+
   ```
3. Create an Iceberg table using the detected schema.

   Copy code

   ```
   CREATE ICEBERG TABLE myicebergtable
     USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    WITHIN GROUP (ORDER BY order_id)
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@my_parquet_stage/customer_iceberg/files-to-ingest/',
          FILE_FORMAT=>'my_parquet_format',
          KIND => 'ICEBERG'
        )
      ))
    ... {rest of the ICEBERG options}
    ;
   ```

   Note

   Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 16MB. We
   recommend avoiding the use of `*` for larger result sets, and only using the required columns, `COLUMN NAME`, `TYPE`, and
   `NULLABLE`, for the query. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`.
4. Use a COPY INTO statement to load the data from the staged Parquet files into the Iceberg table:

   Copy code

   ```
   COPY INTO myicebergtable
     FROM @my_parquet_stage/customer_iceberg/files-to-ingest/
     FILE_FORMAT = 'my_parquet_format'
     LOAD_MODE = ADD_FILES_COPY
     MATCH_BY_COLUMN_NAME = CASE_SENSITIVE;
   ```

   Note

   The example specifies `LOAD_MODE = ADD_FILES_COPY`, which tells Snowflake to copy the files into your external volume location
   and then register the files to the table.

   This option avoids file charges, because Snowflake doesn’t scan the source Parquet files and rewrite the data into new Parquet files.

   Output:

   ```
   +---------------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
   | file                                                                | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
   |---------------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
   | my_parquet_stage/customer_iceberg/files-to-ingest/customers.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
   +---------------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
   ```
5. After loading the data, query the table:

   Copy code

   ```
   SELECT
    id,
    custnum
     FROM myicebergtable
     LIMIT 10;
   ```

   Output:

   ```
   +-----------+---------+
   | id        | custnum |
   |-----------+---------+
   |         1 |   75001 |
   |         2 |   75002 |
   |         3 |   75003 |
   |         4 |   75004 |
   |         5 |   75005 |
   |         6 |   75006 |
   |         7 |   75007 |
   |         8 |   75008 |
   |         9 |   75009 |
   |        10 |   75010 |
   +-----------+---------+
   ```
