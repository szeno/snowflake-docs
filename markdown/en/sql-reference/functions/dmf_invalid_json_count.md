Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_JSON\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not valid JSON. Use this function to validate columns that are expected to
contain JSON payloads.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_JSON_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are excluded from the count.

## Example

Measure the number of invalid JSON values in the `payload` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_JSON_COUNT(
  SELECT
    payload
  FROM events.tables.logs
);
```

The following example creates a table with sample JSON payloads, and then counts the values that aren’t valid JSON:

Copy code

```
CREATE OR REPLACE TABLE json_payloads (payload VARCHAR);

INSERT INTO json_payloads (payload) VALUES
  ('{"id": 1, "status": "active"}'),  -- valid JSON object
  ('[1, 2, 3]'),                      -- valid JSON array
  ('{"id": 2, "status": }'),          -- not valid JSON: missing value
  (NULL);                             -- NULL values aren't counted

SELECT SNOWFLAKE.CORE.INVALID_JSON_COUNT(
  SELECT
    payload
  FROM json_payloads
);
```

In this example, the function returns `1`, for the one value that isn’t valid JSON.
