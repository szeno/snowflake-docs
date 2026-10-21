Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SOURCE\_TARGET\_LAG (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns how far, in seconds, the latest timestamp in a target table trails the latest timestamp in a source table. Use this
function to monitor whether a table that is loaded from another table, such as a replica or the output of a pipeline, is keeping
up with its source.

You associate the function with the target table and specify the source table as a reference table argument.

## Syntax

To associate the function with a table:

Copy code

```
ALTER TABLE <target_table>
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.SOURCE_TARGET_LAG
    ON ( <target_column>, TABLE( <source_table>( <source_column> ) ) )
```

To call the function directly:

Copy code

```
SNOWFLAKE.CORE.SOURCE_TARGET_LAG( ( <target_query> ), ( <source_query> ) )
```

## Arguments

`target_column`
:   Specifies the timestamp column in the associated (target) table.

`TABLE(source_table(source_column))`
:   Specifies the source table and its timestamp column:

    - `source_table`: The fully qualified name of the source table (for example,
      `my_db.my_schema.my_table`).
    - `source_column`: The timestamp column in the source table.

`target_query`, `source_query`
:   Specifies two SQL queries, each enclosed in parentheses, when you call the function directly. Each query must project a single
    timestamp column. The first query reads the target, and the second query reads the source.

## Allowed data types

The target and source columns must have the same data type, which must be one of the following:

- `DATE`
- `TIMESTAMP_LTZ`
- `TIMESTAMP_NTZ`
- `TIMESTAMP_TZ`

## Returns

The function returns a `NUMBER` value: the latest source timestamp minus the latest target timestamp, in seconds.

- A positive value means that the target trails the source by that number of seconds.
- A negative value means that the target is ahead of the source.
- A value of 0 means that the latest timestamps are equal.

For `DATE` columns, the value is a whole number of days expressed in seconds. For example, a difference of two days returns
`172800`.

`NULL` values are ignored. The function returns `NULL` if either the target or the source has no non-`NULL` timestamp.

## Usage notes

- This function uses a reference-table argument, so you can’t use [FILTER](/user-guide/data-quality-filter) with it. You also
  can’t use [WITHIN GROUP](/user-guide/data-quality-group-by).
- The value is signed, so an expectation can tell a target that trails its source from one that is ahead of it. To allow a
  difference of up to `t` seconds in either direction, use an expectation such as
  `VALUE BETWEEN -t AND t`.
- To measure how long ago a single table was last updated, use [FRESHNESS](/sql-reference/functions/dmf_freshness).

## Examples

The examples use a source table of orders and a target table that is loaded from it:

Copy code

```
CREATE TABLE sales.raw.orders (updated_at TIMESTAMP_NTZ);
INSERT INTO sales.raw.orders VALUES
  ('2026-10-20 11:00:00'),
  ('2026-10-20 12:00:00');

CREATE TABLE sales.reporting.orders (loaded_at TIMESTAMP_NTZ);
INSERT INTO sales.reporting.orders VALUES
  ('2026-10-20 11:45:00');
```

Measure how far the target trails the source. The latest target timestamp is 15 minutes behind the latest source timestamp:

Copy code

```
SELECT SNOWFLAKE.CORE.SOURCE_TARGET_LAG(
  (SELECT loaded_at FROM sales.reporting.orders),
  (SELECT updated_at FROM sales.raw.orders)
) AS lag_seconds;
```

```
+-------------+
| LAG_SECONDS |
+-------------+
| 900         |
+-------------+
```

Associate the function with the target table, and define an expectation that is violated when the target trails or leads the
source by more than one hour:

Copy code

```
ALTER TABLE sales.reporting.orders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.SOURCE_TARGET_LAG
    ON (loaded_at, TABLE(sales.raw.orders(updated_at)))
    EXPECTATION within_one_hour (VALUE BETWEEN -3600 AND 3600);
```
