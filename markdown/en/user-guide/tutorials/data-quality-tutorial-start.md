# Tutorial: Getting started with data metric functions

## Introduction

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can complete this tutorial using a worksheet in Snowsight or using a CLI client such as [SnowSQL](/user-guide/snowsql).
Simply paste the code examples and run them.

By the end of this tutorial, you will learn how to:

- Create a custom data metric function (DMF) to measure data quality.
- Manage the DMF to optimize serverless credit usage.
- Monitor the serverless credit usage associated with calling the scheduled DMF.

## Access control setup

To complete this tutorial, use a single custom role that has all of the required access, which includes the following:

- Creating a database, which subsequently allows creating a schema, creating a DMF in the schema, and creating a table in the schema
- Creating a warehouse to perform query operations
- Querying the view that contains the results of calling the scheduled DMF
- Querying the view that contains serverless compute usage information

Create the `dq_tutorial_role` role to use throughout the tutorial:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
> CREATE ROLE IF NOT EXISTS dq_tutorial_role;
> ```

Grant privileges, and grant the application role and database roles to the `dq_tutorial_role`:

> Copy code
>
> ```
> GRANT CREATE DATABASE ON ACCOUNT TO ROLE dq_tutorial_role;
> GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE dq_tutorial_role;
> GRANT APPLICATION ROLE SNOWFLAKE.DATA_QUALITY_MONITORING_VIEWER TO ROLE dq_tutorial_role;
> GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE dq_tutorial_role;
> GRANT DATABASE ROLE SNOWFLAKE.DATA_METRIC_USER TO ROLE dq_tutorial_role;
> ```

Create a warehouse to query the table that contains the data and grant the USAGE privilege on the role to the `dq_tutorial_role` role:

> Copy code
>
> ```
> CREATE WAREHOUSE IF NOT EXISTS dq_tutorial_wh;
> GRANT USAGE ON WAREHOUSE dq_tutorial_wh TO ROLE dq_tutorial_role;
> ```

Confirm the grants to the `dq_tutorial_role` role:

> Copy code
>
> ```
> SHOW GRANTS TO ROLE dq_tutorial_role;
> ```

Establish a role hierarchy and grant the role to a user who can complete this tutorial (replace the `jsmith` value):

> Copy code
>
> ```
> GRANT ROLE dq_tutorial_role TO ROLE SYSADMIN;
> GRANT ROLE dq_tutorial_role TO USER jsmith;
> ```

## Data setup

To facilitate managing the data and the DMF for this tutorial, create a dedicated database to contain these objects:

### Create a table

Copy code

```
USE ROLE dq_tutorial_role;
CREATE DATABASE IF NOT EXISTS dq_tutorial_db;
CREATE SCHEMA IF NOT EXISTS sch;

CREATE TABLE customers (
  account_number NUMBER(38,0),
  first_name VARCHAR(16777216),
  last_name VARCHAR(16777216),
  email VARCHAR(16777216),
  phone VARCHAR(16777216),
  created_at TIMESTAMP_NTZ(9),
  street VARCHAR(16777216),
  city VARCHAR(16777216),
  state VARCHAR(16777216),
  country VARCHAR(16777216),
  zip_code NUMBER(38,0)
);
```

### Insert values into a table

Add data to the table:

> Copy code
>
> ```
> USE WAREHOUSE dq_tutorial_wh;
>
> INSERT INTO customers (account_number, city, country, email, first_name, last_name, phone, state, street, zip_code)
>   VALUES (1589420, 'san francisco', 'usa', 'john.doe@', 'john', 'doe', 1234567890, null, null, null);
>
> INSERT INTO customers (account_number, city, country, email, first_name, last_name, phone, state, street, zip_code)
>   VALUES (8028387, 'san francisco', 'usa', 'bart.simpson@example.com', 'bart', 'simpson', 1012023030, null, 'market st', 94102);
>
> INSERT INTO customers (account_number, city, country, email, first_name, last_name, phone, state, street, zip_code)
>   VALUES
>     (1589420, 'san francisco', 'usa', 'john.doe@example.com', 'john', 'doe', 1234567890, 'ca', 'concar dr', 94402),
>     (2834123, 'san mateo', 'usa', 'jane.doe@example.com', 'jane', 'doe', 3641252911, 'ca', 'concar dr', 94402),
>     (4829381, 'san mateo', 'usa', 'jim.doe@example.com', 'jim', 'doe', 3641252912, 'ca', 'concar dr', 94402),
>     (9821802, 'san francisco', 'usa', 'susan.smith@example.com', 'susan', 'smith', 1234567891, 'ca', 'geary st', 94121),
>     (8028387, 'san francisco', 'usa', 'bart.simpson@example.com', 'bart', 'simpson', 1012023030, 'ca', 'market st', 94102);
> ```

## Create and work with DMFs

In the following sections, we will create a user-defined DMF to measure the count of invalid email addresses and subsequently do the
following:

- Schedule the DMF to run every 5 minutes.
- Check the DMF table references (find the tables the DMF is set on).
- Query a built-in view that contains the result of calling the scheduled DMF.
- Unset the DMF from the table to avoid unnecessary serverless credit usage.

### Create a DMF

Create a data metric function (DMF) to return the number of email addresses in a column that don’t match the specified regular expression:

> Copy code
>
> ```
> CREATE DATA METRIC FUNCTION IF NOT EXISTS
>   invalid_email_count (ARG_T table(ARG_C1 STRING))
>   RETURNS NUMBER AS
>   'SELECT COUNT_IF(FALSE = (
>     ARG_C1 REGEXP ''^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$''))
>     FROM ARG_T';
> ```

### Set the schedule on the table

The DMF schedule defines when all DMFs on the table run. Currently, 5 minutes is the shortest possible time interval:

> Copy code
>
> ```
> ALTER TABLE customers SET DATA_METRIC_SCHEDULE = '5 MINUTE';
> ```

Note

For the purpose of the tutorial, the schedule is set for 5 minutes. However, after you optimize your DMF use cases, experiment with the
other schedule settings, such as cron expressions or trigger events associated with DML operations that affect the table.

### Set the DMFs on the table and check the references

Associate the DMF to the table:

> Copy code
>
> ```
> ALTER TABLE customers ADD DATA METRIC FUNCTION
>   invalid_email_count ON (email);
> ```

Because the schedule is set for 5 minutes, we need to wait 5 minutes in order for Snowflake to call the DMF and process the results. For
now, we can check to see that the DMF is associated with the table by calling the
[DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) Information Schema table function:

> Copy code
>
> ```
> SELECT * FROM TABLE(INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
>   REF_ENTITY_NAME => 'dq_tutorial_db.sch.customers',
>   REF_ENTITY_DOMAIN => 'TABLE'));
> ```

### View the DMF results

The results of calling the scheduled DMF are stored in the DATA\_QUALITY\_MONITORING\_RESULTS view. To determine the number of invalid email
addresses, query the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) view to see the results
of calling the scheduled DMF:

> Copy code
>
> ```
> SELECT scheduled_time, measurement_time, table_name, metric_name, value
> FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS
> WHERE TRUE
> AND METRIC_NAME = 'INVALID_EMAIL_COUNT'
> AND METRIC_DATABASE = 'DQ_TUTORIAL_DB'
> LIMIT 100;
> ```

The results show that the `value` column contains `1`. This number corresponds to one improperly formatted email
address, which corresponds to the first INSERT statement in the [Insert values into a table](#label-data-quality-tutorial-insert-data) section.

### Unset the DMFs from the table

You have established that the DMF is working as expected based on the definition of the DMF, the schedule, and the expected results.

To avoid unnecessary serverless credit usage, unset the DMF from the table:

> Copy code
>
> ```
> ALTER TABLE customers DROP DATA METRIC FUNCTION
>   invalid_email_count ON (email);
> ```

## Use DMF to return failed records

In this section, you will return records that failed a data quality check because they had blank values.

The data quality metric function identifies rows that contain data that failed the quality check. You can run a data metric scan to
extract and return these records.

To return the rows identified by a DMF, follow these steps:

- Create a table.
- Add bad records to the table.
- Run the data metric scan to return records with blank values.
- View the scan results.
- Update records with a new value.

### Create a table

Paste and run the following statement to create a table.

> Copy code
>
> ```
> CREATE or REPLACE table dq_tutorial_db.sch.employeesTable (
>   id NUMBER,
>   name VARCHAR,
>   last_name VARCHAR,
>   email VARCHAR,
>   zip_code NUMBER
>  );
> ```

### Insert values into a table

Add data with a few bad records, such as blank values, to the table:

> Copy code
>
> ```
> INSERT INTO dq_tutorial_db.sch.employeesTable (id, name, last_name, email, zip_code)
> VALUES
>   (8, 'John', 'Doe', 'johndoe@example.com', 12345),
>   (23, '', 'Smith', 'smithj@example.com', 23456),
>   (1, NULL, 'Taylor', 'taylorj@example.com', 34567),
>   (99, 'Jane', 'Adams', 'jadams@example.com', 45678),
>   (50, 'Alice', 'Brown', '', 56789),
>   (51, NULL, 'Lee', 'lee@example.com', 67890),
>   (234, 'Michael', '', 'michael@example.com', 78901),
>   (56, 'Sara', 'Jones', 'sjones@example.com', 89012),
>   (11, '', NULL, 'blanklast@example.com', 90123),
>   (12, 'Tom', 'Harris', NULL, 10234);
> ```

### Return the number of blank values by running the BLANK\_COUNT data metric function

Execute the BLANK\_COUNT data metric function to return the number of blank values:

Copy code

```
SELECT snowflake.core.blank_count (SELECT name FROM dq_tutorial_db.sch.employeesTable)
```

### Return rows by running the SYSTEM$DATA\_METRIC\_SCAN function

To return the table rows containing blank values in the `name` column, execute the SYSTEM$DATA\_METRIC\_SCAN function on the `name`
column.

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
>     REF_ENTITY_NAME  => 'dq_tutorial_db.sch.employeesTable',
>     METRIC_NAME  => 'snowflake.core.blank_count',
>     ARGUMENT_NAME => 'name'
>    ));
> ```

### View the system metric scan results

The results show the rows of the `employeeTable` table that contain blank values.

```
+-----+-------+--------------+-----------------------+-----------+------- --+
| ID  | NAME  | LAST_NAME    | EMAIL                 | CREATEDAT | ZIP_CODE |
|-----+-------+--------------+-----------------------+----------------------|
| 23  |       |   Smith      | smith@example.com     | null      | 23456    |
| 11  |       |   null       | blanklast@example.com | null      | 90123    |
+-----+-------+--------------+-----------------------+-----------+----------+
```

### Update records with a new value

To replace the blank values in the `name` column, run a query on the target table that includes the SYSTEM$DATA\_METRIC\_SCAN function.
It sets the blank values in the `name` column to NULL by running the UPDATE command on each of the rows returned by the system
function:

Copy code

```
UPDATE dq_tutorial_db.sch.employeesTable
  SET name = null
  WHERE dq_tutorial_db.sch.employeesTable.ID IN (
    select ID from table(system$data_metric_scan(
  REF_ENTITY_NAME => 'dq_tutorial_db.sch.employeesTable',
  METRIC_NAME => 'snowflake.core.blank_count',
  ARGUMENT_NAME => 'name'
  )));
```

After you update the values, running the following returns 0:

Copy code

```
SELECT snowflake.core.blank_count (SELECT name FROM dq_tutorial_db.sch.employeesTable)
```

In this section, you extracted records with data that failed the quality check. In the next section, you will learn how to view your
serverless credit consumption.

## View your serverless credit consumption

Calling scheduled data metric functions (DMFs) requires [serverless compute resources](/user-guide/cost-understanding-compute). You
can query the Account Usage view
[DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY](/sql-reference/account-usage/data_quality_monitoring_usage_history) to view the
[DMF serverless compute cost](/user-guide/data-quality-intro#label-data-quality-cost).

Because the view has a latency of 1-2 hours, wait for that time to pass before querying the view. You can come back to this step later.

Query the view and filter the results to include the time interval of your scheduled DMF:

> Copy code
>
> ```
> USE ROLE dq_tutorial_role;
> SELECT *
> FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_QUALITY_MONITORING_USAGE_HISTORY
> WHERE TRUE
> AND START_TIME >= CURRENT_TIMESTAMP - INTERVAL '3 days'
> LIMIT 100;
> ```

## Clean up, summary, and additional resources

Congratulations! You’ve completed this tutorial.

Take a few minutes to review the summary and the key points covered in this tutorial.

Consider cleaning up by dropping the objects you created in this tutorial. Learn more by reviewing other topics in the Snowflake
documentation.

### Summary and key points

In summary, you learned how to do the following:

- Create a custom DMF to measure data quality and manage the DMF to optimize serverless credit usage.
- Monitor the serverless credit usage associated with calling the scheduled DMF.

### Drop the tutorial objects

If you plan to repeat the tutorial, you can keep the objects that you created.

Otherwise, drop the tutorial objects as follows:

Copy code

```
USE ROLE ACCOUNTADMIN;
DROP DATABASE dq_tutorial_db;
DROP WAREHOUSE dq_tutorial_wh;
DROP ROLE dq_tutorial_role;
```

### What’s next?

Continue learning about Snowflake using the following resources:

- Learn more about DMFs by starting with [Introduction to data quality checks](/user-guide/data-quality-intro).
- Complete the other tutorials provided by Snowflake in the [Tutorials to get started with Snowflake](/learn-tutorials) topic.
