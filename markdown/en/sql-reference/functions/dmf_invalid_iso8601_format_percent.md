Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_ISO8601\_FORMAT\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not laid out as an ISO 8601 date or timestamp. The percentage is computed
over the
total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_ISO8601_FORMAT_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be a date in the form `YYYY-MM-DD`, optionally followed by a time. A time that follows an uppercase `T` can be
  hours alone, hours and minutes, or hours, minutes, and seconds. A time that follows a space must have at least hours and
  minutes.
  Seconds can have a fraction that uses a period or a comma.
- A time can end with a UTC offset of `Z`, `+hh`, `+hhmm`, or `+hh:mm` (or the same forms with `-`). An offset is accepted
  only after a time, so a date followed by `Z` is counted.
- The basic format without hyphens (`20261013`), week dates, ordinal dates, and lowercase `t` or `z` separators are counted.
- The function checks the layout only, so a value such as `2026-13-45` is not counted. To check whether values can be parsed
  as a
  timestamp, use [INVALID\_TIMESTAMP\_STRING\_PERCENT](/sql-reference/functions/dmf_invalid_timestamp_string_percent).

## Example

Measure the percentage of values that are not in ISO 8601 layout in the `event_time_text` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_ISO8601_FORMAT_PERCENT(
  SELECT
    event_time_text
  FROM events.tables.raw_events
);
```
