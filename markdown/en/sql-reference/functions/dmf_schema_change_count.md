Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SCHEMA\_CHANGE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the number of schema change operations (column add, drop, rename, or type change) detected on the associated table since
the previous evaluation of the function. On the first run, the function records a baseline snapshot of the table’s columns and
returns `0`.

In addition to the aggregate count written to
[DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results), this function writes one row per
detected change to the [DATA\_QUALITY\_MONITORING\_LOGS](/sql-reference/local/data_quality_monitoring_logs) view, correlated by
`run_id`.

## Syntax

Not applicable.

## Returns

The function returns a scalar value with a NUMBER data type.

## Usage notes

You can’t call this function directly. To learn how to associate the function with a table or view so it runs at regular
intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).
