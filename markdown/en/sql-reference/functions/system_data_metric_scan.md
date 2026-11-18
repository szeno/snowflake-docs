Categories:
:   [System functions](/sql-reference/functions-system), [Table functions](/sql-reference/functions-table)

# SYSTEM$DATA\_METRIC\_SCAN

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the rows identified by a [data quality metric](/user-guide/data-quality-intro) as containing data that fails a data quality
check. For example, if you use the NULL\_COUNT data metric function as an argument, the function returns the rows in the table that contain a
NULL value in a specific column.

## Syntax

Copy code

```
SYSTEM$DATA_METRIC_SCAN(
  REF_ENTITY_NAME  => '<object>'
  , METRIC_NAME  => '<data_metric_function>'
  , ARGUMENT_NAME => '<column> [ , <column> ... ]'
  [ , ARGUMENT_EXPRESSION => '<boolean-expression>' ]
  [ , AT_TIMESTAMP => '<timestamp>' ]
  [ , WITHIN_GROUP_VALUES => '<json_object>' ]
)
```

## Arguments

**Required:**

`REF_ENTITY_NAME => 'object'`
:   Name of the table or view on which the specified data metric function will run. The function returns rows from this object.

`METRIC_NAME => 'data_metric_function'`
:   Name of the system data metric that you want to run to evaluate the specified table or view. Only the following system functions are
    supported:

    > - SNOWFLAKE.CORE.ACCEPTED\_VALUES
    > - SNOWFLAKE.CORE.ACCEPTED\_VALUES\_PERCENT
    > - SNOWFLAKE.CORE.BLANK\_COUNT
    > - SNOWFLAKE.CORE.BLANK\_PERCENT
    > - SNOWFLAKE.CORE.DUPLICATE\_COUNT
    > - SNOWFLAKE.CORE.NULL\_COUNT
    > - SNOWFLAKE.CORE.NULL\_PERCENT

`ARGUMENT_NAME => 'column [ , column ... ]'`
:   Name of the columns in the specified table or view that are being passed as arguments to the specified data metric function.

**Optional:**

`ARGUMENT_EXPRESSION => 'boolean-expression'`
:   Required if the specified data metric function is [ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values) or
    [ACCEPTED\_VALUES\_PERCENT](/sql-reference/functions/dmf_accepted_values_percent). Disallowed for all other DMFs.

    Specifies a Boolean expression used to evaluate whether a record passes or fails the ACCEPTED\_VALUES or ACCEPTED\_VALUES\_PERCENT data quality check. The
    SYSTEM$DATA\_METRIC\_SCAN function returns records that do *not* match the Boolean expression. The expression can include the following
    operators and functions:

    - [Comparison operators](/sql-reference/operators-comparison)
    - [Logical operators](/sql-reference/operators-logical)
    - [[ NOT ] LIKE](/sql-reference/functions/like)
    - [[ NOT ] IN](/sql-reference/functions/in)
    - [IS [ NOT ] NULL](/sql-reference/functions/is-null)

    The column in the Boolean expression must be the same column specified in the ARGUMENT\_NAME argument.

    If the ACCEPTED\_VALUES or ACCEPTED\_VALUES\_PERCENT DMF is [associated with the object](/user-guide/data-quality-working#label-dmf-associate) specified by
    REF\_ENTITY\_NAME, the SYSTEM$DATA\_METRIC\_SCAN function ignores the Boolean expression that was specified when the DMF was associated
    with the object.

`AT_TIMESTAMP => 'timestamp'`
:   Timestamp string specifying the historical snapshot to scan. The function uses [Time Travel](/user-guide/data-time-travel) to
    evaluate the specified DMF against the table or view data at that time. It does not retrieve stored evaluation results.

    The requested time must be within the Time Travel retention period of the queried tables and must not precede their creation.

    The string is converted using [TO\_TIMESTAMP](/sql-reference/functions/to_timestamp). Its format must match the
    [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) session parameter, which defaults to `AUTO`.
    The resulting timestamp type depends on the
    [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter:

    - With the default `TIMESTAMP_NTZ` mapping, any timezone offset in the string is discarded. Time Travel interprets the resulting
      clock time as UTC. Supply a UTC timestamp string. For example, use the format `YYYY-MM-DD HH24:MI:SS.FF3` when
      `TIMESTAMP_INPUT_FORMAT` is `AUTO`.
    - With `TIMESTAMP_LTZ` or `TIMESTAMP_TZ` mapping, an explicit timezone offset is honored. If the string has no offset, the
      [TIMEZONE](/sql-reference/parameters#label-timezone) session parameter determines the timezone.

    To scan data from a past DMF measurement, use `MEASUREMENT_TIME` from
    [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results). For an example, see
    [Calling the SYSTEM$DATA\_METRIC\_SCAN function](/user-guide/data-quality-fixing#label-data-quality-scan-historical-data).

`WITHIN_GROUP_VALUES => 'json_object'`
:   For an association created with a WITHIN GROUP clause, a JSON object that maps grouping column names to the specific group values to
    scan. For example: `'{"REGION": "US", "PRODUCT_CATEGORY": "Electronics"}'`. If you omit this argument, the scan returns all rows
    regardless of group.

    Only string and numeric values are supported in the JSON object.

    For more information, see [Apply data quality checks by group](/user-guide/data-quality-group-by).

## Returns

Rows from the specified table or view.

## Access control privileges

Executing this function requires the following privileges:

- SELECT on the specified table.
- USAGE on the specified data metric function.

## Usage notes

- This function does not support user-defined metrics.
- If the specified table is protected by a policy, such as a masking policy or row access policy, the function might return unexpected or
  incomplete data because results depend on the user’s role when executing the function.

## Examples

Given that the SNOWFLAKE.CORE.NULL\_COUNT system metric returns the total number of NULL values in a particular column, the following returns
the rows of the `employeesTable` table that have NULL values in the `SSN` column.

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME  => 'governance.sch.employeesTable',
    METRIC_NAME  => 'snowflake.core.null_count',
    ARGUMENT_NAME => 'SSN'
  ));
```

Given that the SNOWFLAKE.CORE.DUPLICATE\_COUNT system metric returns the count of duplicate values, the following returns
the rows of the `employeesTable` table that had duplicate values in both the `first_name` and `last_name` columns.

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME  => 'governance.sch.employeesTable',
    METRIC_NAME  => 'snowflake.core.duplicate_count',
    ARGUMENT_NAME => 'first_name, last_name'
  ));
```

Return the rows where the value of the `age` column is *not* equal to five (that is, the rows that *don’t* match the condition specified by
ARGUMENT\_EXPRESSION).

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME  => 'governance.sch.employeesTable',
    METRIC_NAME  => 'snowflake.core.accepted_values',
    ARGUMENT_NAME => 'age',
    ARGUMENT_EXPRESSION => 'age = 5'
  ));
```

For an association created with a WITHIN GROUP clause, return only the NULL rows in the `name` column for a specific group (the
`US` region):

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
    REF_ENTITY_NAME     => 'governance.sch.customer_data',
    METRIC_NAME         => 'snowflake.core.null_count',
    ARGUMENT_NAME       => 'name',
    WITHIN_GROUP_VALUES => '{"REGION": "US"}'
  ));
```

For more information, see [Apply data quality checks by group](/user-guide/data-quality-group-by).
