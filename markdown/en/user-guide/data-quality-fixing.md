# Remediation of data quality issues

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Data quality metrics (DMFs) let you identify how many records in a table might contain quality issues. For example, the
SNOWFLAKE.CORE.NULL\_COUNT DMF can identify how many records contain a NULL value in a specific column.

To help you fix these possible quality issues, you can call the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) system function to
return the individual records identified by the DMF as containing data that failed a data quality check. For example, if you pass the
NULL\_COUNT DMF into the SYSTEM$DATA\_METRIC\_SCAN function as an argument, then you can obtain the actual records that contain a NULL value,
not just the number of records that contain a NULL value.

## Supported DMFs

The SYSTEM$DATA\_METRIC\_SCAN function accepts a DMF as an argument to return the records identified by the DMF as containing problematic
data. The following system DMFs can be used as arguments:

> - [ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values)
> - [BLANK\_COUNT](/sql-reference/functions/dmf_blank_count)
> - [BLANK\_PERCENT](/sql-reference/functions/dmf_blank_percent)
> - [DUPLICATE\_COUNT](/sql-reference/functions/dmf_duplicate_count)
> - [NULL\_COUNT](/sql-reference/functions/dmf_null_count)
> - [NULL\_PERCENT](/sql-reference/functions/dmf_null_percent)

## Limitations and considerations

- You cannot use custom DMFs as an argument of the SYSTEM$DATA\_METRIC\_SCAN function.
- If a table is protected by a policy, such as a masking policy or row access policy, the SYSTEM$DATA\_METRIC\_SCAN function might return
  unexpected or incomplete data because results depend on the user’s role when executing the function.

## Calling the SYSTEM$DATA\_METRIC\_SCAN function

When you call the SYSTEM$DATA\_METRIC\_SCAN function, it analyses a table with a DMF to identify possible data quality issues. You must pass
in the following arguments to the SYSTEM$DATA\_METRIC\_SCAN function: the name of the table, the DMF, and any arguments being passed to the
DMF to help identify problematic records.

For example, given that the SNOWFLAKE.CORE.NULL\_COUNT system metric function returns the total number of NULL values in a particular column,
the following returns the rows of the `employeesTable` table that have NULL values in the `SSN` column.

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME  => 'governance.sch.employeesTable'
    ,METRIC_NAME  => 'snowflake.core.null_count'
    ,ARGUMENT_NAME => 'SSN'
    ,AT_TIMESTAMP => '2024-08-28 02:00:00 -0700'
  ));
```

To check the results of a DMF evaluation on the table or view in the past, you can pass the AT\_TIMESTAMP argument. The AT\_TIMESTAMP
argument allows you to use [Time Travel](/sql-reference/functions/to_timestamp) to cast the timestamp string to return only those
records that existed in the table at the ’2024-08-28 02:00:00 -0700’ timestamp.

### ACCEPTED\_VALUES DMF

You must specify an additional argument when calling the SYSTEM$DATA\_METRIC\_SCAN function to return records identified by the
[ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values) DMF as containing data quality issues. With this argument,
ARGUMENT\_EXPRESSION, you can specify a Boolean expression that determines which rows
to return. If a value in the column does *not* match the expression, the row is returned.

The following command returns the rows where the value of the `age` column is equal to or less than five (that is, the rows that *don’t*
match the condition specified by ARGUMENT\_EXPRESSION).

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME  => 'governance.sch.employeesTable',
    METRIC_NAME  => 'snowflake.core.accepted_values',
    ARGUMENT_NAME => 'age',
    ARGUMENT_EXPRESSION => 'age > 5'
  ));
```

## Using SYSTEM$DATA\_METRIC\_SCAN to fix data

The SYSTEM$DATA\_METRIC\_SCAN function is a [table function](/sql-reference/functions-table) that returns a set of rows. The output of
the function can be used within a DML statement to take action on the records that have been identified as containing data that failed a
data quality check.

Suppose you want to replace blank values in the `email` column of the `t` table with NULL values. Because the BLANK\_COUNT data metric
function identifies blank values, you could run the following statement:

Copy code

```
UPDATE T
  SET email = null
  WHERE T.ID IN (SELECT ID FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME => 't'
    ,METRIC_NAME => 'snowflake.core.blank_count'
    ,ARGUMENT_NAME => 'email'
  )));
```
