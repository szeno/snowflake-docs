# Apply data quality checks to a subset of rows

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When you associate a data metric function (DMF) with a table or view, the DMF evaluates all rows
in the column or table by default. Some use cases require running a metric against only a specific
subset of rows, such as active records, rows for a particular region, or rows within a date range.

The FILTER clause lets you attach a row predicate to a DMF association so that the metric is
evaluated only on rows that satisfy the condition. The DMF definition itself doesn’t change; the
filter is stored in the association and applied automatically at evaluation time.

## Overview

When you create or modify a DMF association with a FILTER clause, the predicate is saved with the
association. Each time the DMF runs, it evaluates only the rows that satisfy the predicate and
ignores the rest, returning the same kind of value it normally would for the filtered subset.

For example, if your `customer_data` table contains both active and inactive records and you only
want to track null counts for active customers, you can associate the NULL\_COUNT DMF with a filter
instead of pre-filtering the data or creating a view.

## Supported DMFs

The FILTER clause is supported for most system DMFs in the `SNOWFLAKE.CORE` schema and for custom
DMFs.

The following DMFs aren’t supported with FILTER:

- `FRESHNESS`, because it operates on the table as a whole and doesn’t take column arguments.
- DMFs with reference tables (multi-table associations), because the filter can only target a single
  table.

### Custom DMF compatibility

FILTER works with both system DMFs and custom DMFs, with no special requirements on how a custom
DMF is written.

If an incompatible DMF is specified (such as a multi-table DMF), an error is returned at
association creation time.

## Create an association with a filter

To add a DMF association with a row filter, use the [ALTER TABLE](/sql-reference/sql/alter-table) command
with the FILTER clause. The clause is added to the same ADD DATA METRIC FUNCTION syntax used for
standard associations, so all other association properties (such as EXPECTATION and EXECUTE AS
ROLE) remain available:

Copy code

```
ALTER TABLE <table_name>
  ADD DATA METRIC FUNCTION <dmf_name>
    ON ( <argument_column> [ , ... ] )
    FILTER ( <predicate> )
    [ ADD EXPECTATION <expectation_name> ( <expression> ) [ , ... ] ]
    [ EXECUTE AS ROLE <role_name> ]
    [ ANOMALY_DETECTION = { TRUE | FALSE } ]
    [ SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' } ]
```

The `<predicate>` is any valid SQL scalar expression that can appear in a WHERE clause. It can
reference columns in the table the DMF is associated with.

### Parameters specific to filtering

| Parameter | Description |
| --- | --- |
| `FILTER ( predicate )` | A boolean expression that rows must satisfy to be included in the DMF evaluation. The expression can use column references, comparison operators, AND, OR, NOT, and scalar functions. Subqueries aren’t supported. |

Expand

Show lessSee more

Note

You can only have one association per DMF, table, and column combination. If an association already
exists for a given metric and column combination, you can’t create a second one with a different
filter.

### Examples

Track null counts in the `email` column only for customers with `status = 'ACTIVE'`:

Copy code

```
ALTER TABLE customer_data
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (email)
    FILTER (status = 'ACTIVE');
```

Use multiple conditions in the filter:

Copy code

```
ALTER TABLE orders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (order_id)
    FILTER (region = 'US' AND order_date >= '2024-01-01');
```

Combine FILTER with an expectation:

Copy code

```
ALTER TABLE customer_data
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (email)
    FILTER (status = 'ACTIVE')
    ADD EXPECTATION no_active_nulls (value = 0);
```

## Modify or drop a filtered association

Use `ALTER TABLE` or `ALTER VIEW` with `MODIFY DATA METRIC FUNCTION ... FILTER` to set, replace, or
clear the filter on an existing association without dropping it. The association identity stays the
same.

Set or replace the filter:

Copy code

```
ALTER TABLE customer_data
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (email)
    FILTER (status = 'ACTIVE');
```

You can also add a filter to an association that was created without one.

Clear the filter so the DMF evaluates all rows:

Copy code

```
ALTER TABLE customer_data
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (email)
    FILTER ();
```

You can still use `ALTER TABLE ... MODIFY` to update other properties of a filtered association,
such as suspending or resuming it, or changing an expectation. You can’t combine FILTER with those
actions in the same statement.

To remove the association, use `DROP DATA METRIC FUNCTION` with the DMF and its columns. A filter on
the association doesn’t change the drop statement:

Copy code

```
ALTER TABLE customer_data
  DROP DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (email);
```

## View results

Filtered DMF results appear in the same views as standard DMF results. There’s no separate column
for filter results; the metric value reflects only the rows that satisfied the FILTER predicate.

For more information about querying results, see [View results of a data metric function](/user-guide/data-quality-results).

## View filter configuration

### DATA\_METRIC\_FUNCTION\_REFERENCES table function

The [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) table function exposes the
filter predicate for each association through the `PROPERTIES` VARIANT column using the `filter`
key:

| Field | Description |
| --- | --- |
| `properties:filter` | The filter predicate stored as a string, exactly as it was specified in the ADD or MODIFY DATA METRIC FUNCTION statement. NULL if no filter is configured. |

Expand

Show lessSee more

For example:

Copy code

```
SELECT ref_entity_name,
       metric_name,
       properties:filter::STRING AS filter_predicate
  FROM TABLE(INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
    REF_ENTITY_NAME => 'CUSTOMER_DATA',
    REF_ENTITY_DOMAIN => 'TABLE'));
```

Example output:

```
+-----------------+------------+----------------------+
| REF_ENTITY_NAME | METRIC_NAME | FILTER_PREDICATE    |
+-----------------+------------+----------------------+
| CUSTOMER_DATA   | NULL_COUNT  | status = 'ACTIVE'   |
+-----------------+------------+----------------------+
```

The [DATA\_METRIC\_FUNCTION\_REFERENCES view](/sql-reference/account-usage/data_metric_function_references) view exposes the same
`PROPERTIES` column.

## Limitations

- **Supported actions.** The FILTER clause is supported when adding an association (`ADD DATA METRIC FUNCTION`) and when modifying an association (`MODIFY DATA METRIC FUNCTION`). Empty
  parentheses (`FILTER ()`) are valid only with MODIFY, to clear the filter. FILTER isn’t valid in
  a DROP statement.
- **Schema-level associations.** FILTER isn’t supported on schema-level DMF associations
  (`ALTER SCHEMA ... ADD DATA METRIC FUNCTION`). To filter rows, create the association at the
  table or view level.
- **FRESHNESS DMF.** FILTER isn’t supported for the FRESHNESS DMF, because it operates on the
  table as a whole and doesn’t take column arguments.
- **Multi-table DMFs.** FILTER isn’t supported for DMFs with a reference table (two-table
  associations), because the filter expression can only target a single table.
- **WITHIN GROUP.** FILTER and WITHIN GROUP can’t be combined on the same association. Create
  separate associations if you need both row filtering and group-level results.
- **Subqueries.** The filter predicate can’t contain subqueries (including `IN (SELECT ...)` or
  `EXISTS (...)`).
- **One action per MODIFY.** You can’t combine `FILTER` with `SUSPEND`, `RESUME`, `EXPECTATION`, or `SET` in
  the same `MODIFY` statement.
