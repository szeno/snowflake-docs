# Using synthetic data in Snowflake

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This release introduces a new stored procedure, [GENERATE\_SYNTHETIC\_DATA](/sql-reference/stored-procedures/generate_synthetic_data), to generate synthetic data.

## Overview

Snowflake can generate *synthetic data* from a source table, producing a table with the same number of columns as the source
table, but with statistically similar artificial data. You can use synthetic data to share or test data that is too sensitive,
confidential, or otherwise restricted to share with others. The synthetic data set has the same characteristics as the source data set,
such as name, number, and data type of columns, and the same or fewer number of rows. You can use synthetic data to test and validate
workloads in Snowflake, particularly when the original data is sensitive and shouldn’t be accessible to unauthorized users. Synthetic data
appears in the [data lineage graph](/user-guide/ui-snowsight-lineage).

### Benefits

Statistical consistency:
:   A synthetic data set represents the statistical properties of the original data set, which helps data engineers to understand the
    statistical properties of the real data set. Subsequently, the data engineer can test and validate solutions that are based on the real
    data set.

Production validation:
:   A synthetic data set similar to a production data set enables production engineers to test and validate their production
    environment. The result is a more robust production environment.

### About the synthetic data algorithm

Snowflake uses an algorithm to generate synthetic data that is similar to the original data set. The algorithm uses the original data set
to generate synthetic data that has the same statistical properties as the original data set. Once this distribution is captured, the
synthetic data resembles the original data statistically but does not have a direct reference or link to any row from the original data.

## Generating synthetic data

Call [GENERATE\_SYNTHETIC\_DATA](/sql-reference/stored-procedures/generate_synthetic_data) to generate synthetic data from one or more tables. Snowflake creates
synthetic data tables with ownership granted to the role that calls the stored procedure. The output tables have the same number of columns
as the input tables, with the same column names and data types. The output generally has the same number of rows, unless you enable the
[privacy filter](#label-sdg-privacy-filter), in which case the output tables might have fewer rows.

### Generated data values

Snowflake generates synthetic data for non-join-key columns according to the source data type:

- **Statistical data:** Data of type number, boolean, date, time, or timestamp. Generated data is the same type, with similar values to
  the source data.
- **Categorical string:** A string column with *few* unique values‡. Generated data uses actual values from the source data.
- **Non-categorical string:** A string column with *many* unique values‡. Redacted in the output unless you specify an output
  format with the `replace` option in GENERATE\_SYNTHETIC\_DATA.

You can explicitly designate a non-join-key string column as categorical or non-categorical by providing a `categorical` value to
GENERATE\_SYNTHETIC\_DATA. Join key columns must be non-categorical strings or statistical.

Generated data in each table maintains the approximate distributions and correlations present in the original table.

Columns designated as join keys can be of any data type, and will result in synthetic data of the same type and consistent, but artificial,
values.

‡ *Few unique values* means that the number of unique values is less than half the row count. *Many unique values* means that the
number of unique values is more than half the row count.

### Maintaining join key consistency in synthetic data

If you plan to run join queries on your synthetic data, designate every column that you will join on as a *join key*. You can designate
any numeric, boolean, or non-categorical column as a join key by assigning the `join_key` value in GENERATE\_SYNTHETIC\_DATA. A consistent
synthetic value is generated in the output data for the same value in the source data for all join keys in all tables during a single run.
This enables you to run join queries and get similar results as you would when running the same query against the source data.

To maintain join consistency between tables, be sure that the same join key column in each table has the same arguments. That is,
if you expect `cust_id` to be joinable across tables, provide the same set of arguments and values in the `columns` description in each
dataset object:

Copy code

```
'datasets':[
  {
    'input_table': 'd.s.orders',
    'output_table': 'd.s.orders_synth',
    'columns': {'cust_id': {'join_key': True, 'replace': 'uuid'}, ...}
  },
  {
    'input_table': 'd.s.customers',
    'output_table': 'd.s.customers_synth',
    'columns' : {'cust_id': {'join_key': True, 'replace':'uuid'}, ...}

  }
]
```

If you provide a [symmetric string secret](/sql-reference/sql/create-secret#label-symmetric-secret) to `consistency_secret` in GENERATE\_SYNTHETIC\_DATA, join key
values will be consistent across tables and multiple runs. If you do not specify a secret, then the join key values will be consistent
across all tables in a single run, but not across multiple runs. Multi-run consistency is supported only for string columns.

Note

If you provide a SECRET object to GENERATE\_SYNTHETIC\_DATA, you need the READ or OWNERSHIP privilege on that SECRET.

**Example: Single-run join key consistency**

Copy code

```
CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
  'datasets':[
      {
        'input_table': 'CLINICAL_DB.PUBLIC.PATIENTS1',
        'output_table': 'MY_DB.PUBLIC.PATIENTS1',
        'columns': { 'patient_id': {'join_key': TRUE}, 'age':{'join_key': TRUE}}
      },
      {
        'input_table': 'CLINICAL_DB.PUBLIC.PATIENTS2',
        'output_table': 'MY_DB.PUBLIC.PATIENTS2',
        'columns': { 'patient_id': {'join_key': TRUE}, 'age':{'join_key': TRUE}}
      }
    ],
    'replace_output_tables': TRUE
});
```

**Example: Multi-run join key consistency**

Copy code

```
-- Generate consistent join keys across multiple runs by
-- providing a symmetric key secret.
CREATE OR REPLACE SECRET my_db.public.my_consistency_secret
  TYPE=SYMMETRIC_KEY
  ALGORITHM=GENERIC;

CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
  'datasets':[
      {
        'input_table': 'CLINICAL_DB.PUBLIC.BASE_TABLE',
        'output_table': 'MY_DB.PUBLIC.PATIENTS1',
        'columns': { 'patient_id': {'join_key': TRUE}}
      }
    ],
    'consistency_secret': SYSTEM$REFERENCE('SECRET', 'MY_CONSISTENCY_SECRET', 'SESSION', 'READ')::STRING,
    'replace_output_tables': TRUE
});

CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
  'datasets':[
      {
        'input_table': 'CLINICAL_DB.PUBLIC.SECOND_TABLE',
        'output_table': 'MY_DB.PUBLIC.PATIENTS2',
        'columns': { 'patient_id': {'join_key': TRUE}}
      }
    ],
    'consistency_secret': SYSTEM$REFERENCE('SECRET', 'MY_CONSISTENCY_SECRET', 'SESSION', 'READ')::STRING,
    'replace_output_tables': TRUE
});
```

### Enhancing privacy

When you call the GENERATE\_SYNTHETIC\_DATA stored procedure, you can optionally set the `'similarity_filter': True` configuration
option to apply a privacy filter to the output table. The privacy filter removes rows from the output table if the rows are too similar to
the input data set. The privacy threshold uses the nearest neighbor distance ratio (NNDR) and distance to closest record (DCR) values to
determine whether a row should be removed from the output table.

When using a similarity filter, all non-string columns must have values for all rows. A NULL value in a non-string column will cause the
procedure to fail.

## Requirements

### Input table requirements

Both tables and views are supported as source data. You can specify up to five input tables per procedure call.

To generate synthetic data, *each* input table or view must meet the following requirements:

- Minimum 20 distinct rows
- Maximum 100 columns
- Maximum 14M rows
- The following input table types are supported:

  - Regular, temporary, dynamic, and transient tables
  - Regular, materialized, secure, and secure materialized views
- The following input table types are not supported:

  - External, Apache Iceberg™, and hybrid tables
  - Streams
- The following column types are supported. Columns of an unsupported data type return NULL for all values in
  the column.

  - All numeric types (NUMBER, DECIMAL, FLOAT, INTEGER, and so on)
  - BOOLEAN
  - All date and time types (DATE, DATETIME, TIME, TIMESTAMP, and so on) except TIMESTAMP\_TZ.
    However, timestamps earlier than `1677-09-21 00:12:43.145224193` or later than `2262-04-11 23:47:16.854775807` in the source
    data are coerced to `1677-09-21 00:12:43.145224193` or `2262-04-11 23:47:16.854775807` respectively when generating synthetic data.
  - STRING, VARCHAR, CHAR, CHARACTER, TEXT

    If more than half of the values in a STRING column are unique values, Snowflake replaces the
    value with a redacted value in the output table due to privacy concerns.

### Access control requirements

To generate synthetic data, you must use a role with each the following grants:

- USAGE on the warehouse that you want to use for queries.
- SELECT on the input table from which you want to generate synthetic data.
- USAGE on the database and schema that contain the input table, and on the database that contains the output table.
- CREATE TABLE on the schema that contains the output table.
- OWNERSHIP on the output tables. The simplest way to do this is by granting OWNERSHIP to the schema where the output table is
  generated. (However, if someone has applied a FUTURE GRANT on this schema, table ownership will be silently overridden – that is,
  `GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA db.my_schema TO ROLE some_role` will automatically grant OWNERSHIP to `some_role` on any
  new tables created in schema `my_schema`.)

All users can access the SNOWFLAKE.DATA\_PRIVACY.GENERATE\_SYNTHETIC\_DATA stored procedure. Access is made available using the
SNOWFLAKE.CORE\_VIEWER database role, which is granted to the PUBLIC role.

### Other requirements

You must [accept the Anaconda terms and conditions](/developer-guide/udf/python/udf-python-packages#label-accept-anaconda-terms) in your Snowflake account in order to enable this
feature.

## Recommendations

- Use a medium [Snowpark-optimized warehouse](/user-guide/warehouses-snowpark-optimized).
- While `GENERATE_SYNTHETIC_DATA` is running, do not run any other queries in that warehouse.

## Example: Synthetic data from multiple tables

This example uses the [Snowflake Sample Data database SNOWFLAKE\_SAMPLE\_DATA](/user-guide/sample-data-using). If you don’t see it in
your account, you can copy it with the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE or REPLACE DATABASE SNOWFLAKE_SAMPLE_DATA from share SFC_SAMPLES.SAMPLE_DATA;
```

Follow these steps to generate synthetic data from multiple input tables:

1. Create and configure the access control for the `data_engineer` role to allow them to create all of the necessary objects:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE OR REPLACE ROLE data_engineer;
   CREATE OR REPLACE DATABASE syndata_db;
   CREATE OR REPLACE WAREHOUSE syndata_wh;

   GRANT OWNERSHIP ON DATABASE syndata_db TO ROLE data_engineer;
   GRANT USAGE ON WAREHOUSE syndata_wh TO ROLE data_engineer;
   GRANT ROLE data_engineer TO USER jsmith; -- Or whoever you want to run this example. Or skip this line to run it yourself.
   ```
2. Create two views from the Snowflake Sample Data database:

   Copy code

   ```
   - Sign in as user with data_engineer role. Then...
   CREATE SCHEMA syndata_db.sch;
   CREATE OR REPLACE VIEW syndata_db.sch.TPC_ORDERS_5K as (
    SELECT * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
    LIMIT 5000
   );
   CREATE OR REPLACE VIEW syndata_db.sch.TPC_CUSTOMERS_5K as (
    SELECT * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER
    LIMIT 5000
   );
   ```
3. Query the input tables to view the data and confirm that each table has 5,000 rows:

   Copy code

   ```
   USE WAREHOUSE syndata_wh;
   SELECT TOP 20 * FROM syndata_db.sch.TPC_ORDERS_5K;
   SELECT COUNT(*) FROM syndata_db.sch.TPC_ORDERS_5K;
   select count(distinct o_clerk), count(*) from syndata_db.sch.TPC_ORDERS_5K;

   SELECT TOP 20 * FROM syndata_db.sch.TPC_CUSTOMERS_5K;
   SELECT COUNT(*) FROM syndata_db.sch.TPC_CUSTOMERS_5K;
   ```
4. Call the [GENERATE\_SYNTHETIC\_DATA](/sql-reference/stored-procedures/generate_synthetic_data) stored procedure to generate the synthetic data into two output
   tables. Designate join keys, because you will join on those keys later.

   Copy code

   ```
   CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
    'datasets':[
        {
          'input_table': 'syndata_db.sch.TPC_ORDERS_5K',
          'output_table': 'syndata_db.sch.TPC_ORDERS_5K_SYNTHETIC',
          'columns': {'O_CUSTKEY': {'join_key': True}}
        },
        {
          'input_table': 'syndata_db.sch.TPC_CUSTOMERS_5K',
          'output_table': 'syndata_db.sch.TPC_CUSTOMERS_5K_SYNTHETIC',
          'columns' : {'C_CUSTKEY': {'join_key': True}}

        }
      ],
      'replace_output_tables':True
     });
   ```
5. Query the output table to view the synthetic data:

   Copy code

   ```
   SELECT TOP 20 * FROM syndata_db.sch.TPC_ORDERS_5K_SYNTHETIC;
   SELECT COUNT(*) FROM syndata_db.sch.TPC_ORDERS_5K_SYNTHETIC;

   SELECT TOP 20 * FROM syndata_db.sch.TPC_CUSTOMERS_5K_SYNTHETIC;
   SELECT COUNT(*) FROM syndata_db.sch.TPC_CUSTOMERS_5K_SYNTHETIC;
   ```
6. Clean up all the objects

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   DROP DATABASE syndata_db;
   DROP ROLE data_engineer;
   DROP WAREHOUSE syndata_wh;
   ```
