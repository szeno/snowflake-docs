Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# DATA\_METRIC\_SCHEDULED\_TIME (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the timestamp for when a DMF is scheduled to run or the current timestamp if the function is called manually.

You can use this DMF to define custom metrics to measure the freshness of your data or to define incremental metrics in
conjunction with DMFs that already exist.

## Syntax

Copy code

```
SNOWFLAKE.CORE.DATA_METRIC_SCHEDULED_TIME()
```

## Arguments

None.

## Returns

The function returns a scalar value with a TIMESTAMP\_LTZ data type.

## Usage notes

Calling this function manually in a SELECT query returns the same value as the [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) function.

## Example

Create a custom data metric function to determine the data freshness on a table in the last hour:

> Copy code
>
> ```
> CREATE OR REPLACE DATA METRIC FUNCTION data_freshness_hour(
>   ARG_T TABLE (ARG_C TIMESTAMP_LTZ))
>   RETURNS NUMBER AS
>   'SELECT TIMEDIFF(
>      minute,
>      MAX(ARG_C),
>      SNOWFLAKE.CORE.DATA_METRIC_SCHEDULED_TIME())
>    FROM ARG_T';
> ```

Call the data metric function manually:

> Copy code
>
> ```
> SELECT data_freshness_hour(SELECT last_updated FROM hr.tables.empl_info) < 60;
> ```
>
> The statement returns `True` if there are no updates to the table in the last hour (60 minutes).
>
> The statement returns `False` if there were updates to the table that took place more than one hour ago.
