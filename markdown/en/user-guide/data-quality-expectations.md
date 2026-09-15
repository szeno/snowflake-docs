# Use SQL to work with expectations

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returning a value from a data metric function (DMF) provides useful information, but it might be hard to know whether it indicates a data
quality issue without knowing what you consider to be acceptable for your data. For example, you might consider tables that contain less
than 10 NULL values in a given column as passing the data quality check. In this case, you *expect* the value to be less than 10, and only
want to be notified if it exceeds that value.

An *expectation* lets you define criteria for whether data passes a data quality check performed by a DMF. When the DMF returns a value,
that value is compared to this criteria to determine whether the data passed or failed the check. Return values that fail are reported as
expectation violations so you can take appropriate action upon the data.

Note

This topic describes how to use SQL to set up and monitor expectations. To use a user interface to set up data quality checks consisting of
a DMF and an expectation, see [Use Snowsight to set up data quality checks](/user-guide/data-quality-ui-setup).

The following creates the expectation that the column `C1` contains less than 10 NULL values.

Copy code

```
ALTER VIEW v1
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT ON (C1)
  EXPECTATION my_exp ( VALUE < 10);
```

You can define expectations for both system DMFs and custom DMFs.

## Defining what meets the expectation

An expectation includes a Boolean expression that determines whether the expectation was met or not. When this expression
evaluates to TRUE it means that the DMF result matched your expectation.

Within an expression, the keyword `VALUE` represents the value returned by the DMF. For example, suppose you had the following
definition of an expectation:

Copy code

```
EXPECTATION my_exp (VALUE < 5)
```

Snowflake replaces `VALUE` with the value returned by the DMF when evaluating the expectation. If the DMF returned `3`, the expectation
would be met because the expression evaluates to TRUE.

If an expression evaluates to FALSE, Snowflake reports it as an expectation violation. For information about tracking these violations, see [Identify expectation violations](#label-dmf-expectations-identify-violations).

An expression can include the following types of operators:

- [Logical operators](/sql-reference/operators-logical)
- [Comparison operators](/sql-reference/operators-comparison)

An expression cannot reference other tables or views, or user-defined functions (UDFs).

## Create an expectation

Each association between a DMF and an object can have one or more expectations.

You can add an expectation when you associate the DMF with the table or view, or you can add it to the association later. You can also
modify an existing expectation.

After you add an expectation, you can [manually test](#label-dmf-expectations-test) it without having to wait until the DMF
runs based on its schedule.

### Add an expectation when associating a DMF

You use an ALTER TABLE or ALTER VIEW command to associate a DMF with a table or view. You can add expectations to the association in the
same SQL statement that creates the association.

For example, the syntax to add expectations when associating a DMF with a table is as follows. Views use a similar syntax.

Copy code

```
ALTER TABLE <table>
  ADD DATA METRIC FUNCTION <dmf>
    ON (<col_name> [ , ... ] [ , TABLE<table_name>( <col_name> [ , ... ] ) )
    [ EXPECTATION <expectation_name> ( <expression> )
      [, <expectation_name> ( <expression> ) [ , ... ] ] ]
```

Where:

- `expectation_name` is a string that’s used to identify the expectation. You can create expectations with the same name as
  long as they belong to different associations.
- `expression` is a Boolean expression that determines whether the DMF returned an expected value. See
  [Defining what meets the expectation](#label-dmf-expectation-expression).

Example: Add single expectation
:   Suppose you’re associating the MAX system DMF with view `v1` in order to check the maximum value in the column `c1`. You expect the
    maximum value to be between 25 and 50.

    Copy code

    ```
    ALTER VIEW v1
      ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.MAX ON (C1)
        EXPECTATION my_exp ( 25 < VALUE AND VALUE < 50);
    ```

    If the MAX DMF returns a value outside this range of expected values, then Snowflake records it as an expectation violation.

Example: Add multiple expectations
:   Suppose you wanted to be notified when a table hasn’t been updated within five minutes, then again when it hasn’t been updated for 30
    minutes. You could add the following expectations, then check when those expectations were violated.

    Copy code

    ```
    ALTER TABLE emp
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS ON (last_updated)
      EXPECTATION lessThan5Mins (VALUE < 300), lessThan30Mins (VALUE < 1800);
    ```

### Add an expectation to an existing association

You use an ALTER TABLE or ALTER VIEW command to add an expectation to an existing association between a DMF and the table or view.

For example, the syntax to add expectations to an association between a table and a DMF is as follows. Views use a similar syntax.

Copy code

```
ALTER TABLE <table>
  MODIFY DATA METRIC FUNCTION <dmf>
    ON (<col_name> [ , ... ] [ , TABLE<table_name>( <col_name> [ , ... ] ) )
    [ ADD EXPECTATION <expectation_name> ( <expression> )
      [, <expectation_name> ( <expression> ) [ , ... ] ] ]
```

Where:

- `expectation_name` is a string that’s used to identify the expectation. You can create expectations with the same name as
  long as they belong to different associations.
- `expression` is a Boolean expression that determines whether the DMF returned an expected value. See
  [Defining what meets the expectation](#label-dmf-expectation-expression).

Example
:   Suppose you previously associated the NULL\_COUNT system DMF with the column `c1` in the table `my_table`. To add an expectation so you
    can be notified when there are 10 or more NULL values in the column `c1`, run the following statement:

    Copy code

    ```
    ALTER TABLE my_table
      MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT ON (c1)
        ADD EXPECTATION my_exp (VALUE < 10);
    ```

    If the result of NULL\_COUNT is 15, it’s reported as an expectation violation.

### Modify an existing expectation

You use a MODIFY EXPECTATION clause to change the expression of an expectation that you previously added to an association.

For example, suppose you previously added the expectation `my_exp` to the association between table `t1` and the NULL\_COUNT DMF. To
modify the expectation so it’s violated when there are 15 or more NULL values in column `c1`, run the following statement:

Copy code

```
ALTER TABLE t1
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT ON (c1)
    MODIFY EXPECTATION my_exp (VALUE < 15);
```

The previous expression of the expectation is replaced with `VALUE < 15`.

## Test an expectation

After you add expectations, you can call the [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations) system function to
ensure that they were added correctly and to determine whether these expectations are currently violated.

For example, suppose you added at least one expectation to the association between a DMF and table `t1`. To see whether these expectations
are currently violated, run the following statement:

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS(
      REF_ENTITY_NAME => 'my_db.sch.t1'));
```

## Drop an expectation

Use a DROP EXPECTATION clause to remove an expectation from an association and remove it from the system.

For example, suppose you previously added the expectation `my_exp` to the association between the column `c1` in the table `t1`
and the NULL\_COUNT DMF. To remove the `my_exp` from the association and the DMF, run the following code:

Copy code

```
ALTER TABLE t1
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT on (c1)
    DROP EXPECTATION my_exp;
```

## Identify expectation violations

You can identify expectation violations using the following:

- [SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW](#label-dmf-expectations-monitor-event-table) — A dedicated event table that records raw data quality results.
- [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view](#label-dmf-expectations-monitor-local-view) — View in the SNOWFLAKE.LOCAL schema that contains flattened results.
- [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS function](#label-dmf-expectations-monitor-function) — Table function that returns expectations results.

### SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW

Data quality results are recorded in the dedicated event table SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW.

If the association between an object and a DMF has an expectation, two rows are added to the table every time Snowflake computes the result
of the DMF. The first row records information about the object the DMF is associated with, the DMF itself, and the result of the data
quality check. The second row records information related to the expectation set on the DMF association, including whether the expectation
was met or violated. If there are multiple expectations, there is a row for each expectation.

The `snow.data_metric.record_type` field in the `resource_attribute` column indicates whether a row corresponds to an
expectation. This field has two possible values:

- `EXPECTATION_VIOLATION_STATUS` - Indicates that the row corresponds to an expectation.
- `EVALUATION_RESULT` - Indicates that the row corresponds to the evaluation of the DMF.

If the row corresponds to an expectation, the `resource_attribute` column also contains the following fields related to expectations:

- `snow.data_metric.expectation_id` - System-generated identifier.
- `snow.data_metric.expectation_name`- Name of the expectation when it was added to the association.
- `snow.data_metric.expectation_expression` - Expectation’s expression.

After you have determined that a row corresponds to the evaluation of an expectation, you can check the `value` column to determine
whether the expectation was violated. If TRUE, the expectation was violated.

### DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view

The [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view](/sql-reference/local/data_quality_monitoring_expectation_status), which exists in the SNOWFLAKE.LOCAL schema, flattens the
information in the event table to make it easier to access DMF results.

### DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS function

The [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS](/sql-reference/functions/data_quality_monitoring_expectation_status) table function returns rows that provide the
same information that is available in the DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view. The function uses a different access control
model than the view.

## Track the use of expectations

Snowflake keeps track of all of the expectations in your account. You can [run a function](#label-expectations-monitor-function) or
[query an ACCOUNT\_USAGE view](#label-expectations-monitor-view) to monitor the use of expectations, including performing the following
tasks:

- Monitor which objects have an expectation defined for their association with a DMF.
- Monitor which DMFs have an expectation defined for their association with an object.
- Discover whether there is an expectation defined for a specific association between an object and a DMF.
- Determine the Boolean expression of an expectation to better understand a data quality check.

### Run a function to track expectations

You can run the [DATA\_METRIC\_FUNCTION\_EXPECTATIONS](/sql-reference/functions/data_metric_function_expectations) function to output expectations defined for a specific
object, a specific DMF, or the association between an object and a DMF.

**Example:** Expectations that exist for a specific object

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      REF_ENTITY_NAME => 'my_table',
      REF_ENTITY_DOMAIN => 'table'));
```

**Example:** Expectations that exist for a specific DMF

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      METRIC_NAME => 'SNOWFLAKE.CORE.NULL_COUNT'));
```

**Example:** Expectations that exist for a specific association between an object and a DMF

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      METRIC_NAME => 'SNOWFLAKE.CORE.NULL_COUNT',
      REF_ENTITY_NAME => 'my_table',
      REF_ENTITY_DOMAIN => 'table'));
```

### Query a view to track expectations

The [DATA\_METRIC\_FUNCTION\_EXPECTATIONS view](/sql-reference/account-usage/data_metric_function_expectations) in the ACCOUNT\_USAGE schema contains all of the expectations in
your account. You can query the view to track the use of expectations within your account and determine the Boolean expression of each
expectation.

**Example:** Return all expectations for your Snowflake account

Copy code

```
SELECT * FROM snowflake.account_usage.data_metric_function_expectations
  ORDER BY expectation_name;
```

**Example:** Identify expectations for a specific data metric function

Copy code

```
SELECT expectation_name,
    ref_database_name as object_database,
    ref_schema_name as object_schema,
    ref_entity_name as object_name
  FROM snowflake.account_usage.data_metric_function_expectations
  WHERE
    metric_database_name = 'SNOWFLAKE' AND
    metric_schema_name = 'CORE' AND
    metric_name = 'ROW_COUNT'
  ORDER BY expectation_name;
```
