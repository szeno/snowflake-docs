# Apply data quality checks by group

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When you associate a data metric function (DMF) with a table or view, the DMF evaluates your data
and returns a single scalar value for the entire column or table, which is useful for tracking data
health at a global level. Some use cases require the same metric broken down by a dimension, such
as null counts per region or duplicate counts per product category.

The WITHIN GROUP clause lets you specify one or more columns to segment data when you create a DMF
association, so each group gets its own metric result.

## Overview

When you create a DMF association with a WITHIN GROUP clause, the DMF is evaluated separately for
each distinct combination of values in the grouping columns. Results are written as one row per
group to the data quality monitoring results view, which makes it easier to identify quality issues
within specific segments.

For example, if your `customer_data` table has data for multiple regions and you want to track
null counts per region, you can group the NULL\_COUNT DMF by the `region` column. Instead of
getting a single count across all regions, you get one row per region in the results.

## Supported DMFs

The WITHIN GROUP clause is supported for most system DMFs in the SNOWFLAKE.CORE schema (including
NULL\_COUNT, DUPLICATE\_COUNT, and ROW\_COUNT) and for most custom DMFs.

The following system DMFs aren’t supported with WITHIN GROUP:

- FRESHNESS, because it operates on the table as a whole and doesn’t take column arguments.
- REFERENTIAL\_INTEGRITY\_COUNT, because it joins across two tables and can’t be evaluated within a
  single group.

Note

Some metrics aren’t additive across groups. For example, AVG and STDDEV per group can’t be
combined to derive a table-level equivalent. Keep this in mind when interpreting grouped results.

### Custom DMF compatibility

Custom DMFs are supported when the DMF body uses a straightforward SQL structure. The following
table summarizes compatibility by structure type:

| DMF body structure | Supported |
| --- | --- |
| Single table query | Yes |
| Subquery | Yes |
| FLATTEN | Yes |
| JOIN | No |
| Common table expressions (CTEs) | No |
| UNION or UNION ALL | No |
| DISTINCT | No |
| Window functions | No |

Expand

Show lessSee more

If you try to use WITHIN GROUP with an unsupported custom DMF structure, an error is returned at
association creation time.

Tip

If your custom DMF uses a CTE, UNION, JOIN, DISTINCT, or window function pattern, consider
rewriting it as a subquery, or migrate to an equivalent system DMF where possible.

## Create an association with grouping

To add a DMF association with group-level results, use the [ALTER TABLE](/sql-reference/sql/alter-table)
command with the WITHIN GROUP clause. The clause is added to the same ADD DATA METRIC FUNCTION
syntax that you use for non-grouped associations, so all of the existing association properties
(such as EXPECTATION and EXECUTE AS ROLE) remain available:

Copy code

```
ALTER TABLE <table_name>
  ADD DATA METRIC FUNCTION <dmf_name>
    ON ( <argument_column> [ , ... ] )
    WITHIN GROUP ( <group_col1> [ , <group_col2> ... ] )
    [ GROUP LIMIT <integer> ]
    [ ADD EXPECTATION <expectation_name> ( <expression> ) [ , ... ] ]
    [ EXECUTE AS ROLE <role_name> ]
```

The `GROUP LIMIT` clause is two keywords without an equals sign, and it must follow the
`WITHIN GROUP` clause directly.

For the full set of clauses supported by ADD DATA METRIC FUNCTION (including ANOMALY\_DETECTION,
SENSITIVITY, and chaining additional DMFs in a single statement), see
[Data metric function actions (`dataMetricFunctionAction`)](/sql-reference/sql/alter-table#label-alter-table-data-metric-function-action).

### Parameters specific to grouping

| Parameter | Description |
| --- | --- |
| `WITHIN GROUP ( col [ , col ... ] )` | One or more columns to group by. Each distinct combination of values in these columns produces a separate result row. |
| `GROUP LIMIT integer` | Optional. The maximum number of groups allowed per evaluation. Valid values are 1 through 1000 (default: 1000). If the number of distinct groups at evaluation time exceeds this limit, the evaluation fails with an error. |

Expand

Show lessSee more

Note

You can only have one association per DMF, table, and column combination. If an association
already exists for a given metric and column combination, you can’t create a second one with a
different grouping.

ANOMALY\_DETECTION is automatically disabled when a WITHIN GROUP clause is present. For details,
see [Limitations](#label-data-quality-group-by-limitations).

### Examples

The following example tracks null counts in the `name` column of the `customer_data` table,
broken down by `region`:

Copy code

```
ALTER TABLE customer_data
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (name)
    WITHIN GROUP (region);
```

To also group by product category and allow up to 500 groups:

Copy code

```
ALTER TABLE customer_data
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (name)
    WITHIN GROUP (region, product_category)
    GROUP LIMIT 500;
```

## Modify or drop a grouped association

You can use the existing `ALTER TABLE ... MODIFY ...` command to update other properties of a
grouped association, such as suspending or resuming it, or changing the expectation. The WITHIN
GROUP clause is set at association creation time and can’t be modified after the fact.

To change the grouping on an existing association, drop the association and re-create it.

To drop a grouped association, use the standard drop syntax. No changes are needed:

Copy code

```
ALTER TABLE customer_data
  DROP DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (name);
```

## View grouped results

Grouped DMF results are available in the same views as standard DMF results. When an association
uses WITHIN GROUP, each evaluation produces one result row per group.

### DATA\_QUALITY\_MONITORING\_RESULTS view

Use the [DATA\_QUALITY\_MONITORING\_RESULTS view](/sql-reference/local/data_quality_monitoring_results) view to query evaluation
results. Grouped results include a new `GROUP_BY_INFO` column that identifies the group each row
corresponds to.

| Column | Type | Description |
| --- | --- | --- |
| `GROUP_BY_INFO` | ARRAY | An array of objects, each describing one grouping column and its value for this row. Each object contains `id`, `name`, and `value`. Empty array for non-grouped associations. |

Expand

Show lessSee more

**Example: Query null counts by region**

Copy code

```
SELECT metric_name,
       value,
       group_by_info
  FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS
  WHERE table_name = 'CUSTOMER_DATA'
    AND metric_name = 'NULL_COUNT'
  ORDER BY measurement_time DESC;
```

Example output:

```
+-------------+-------+----------------------------------------------------+
| METRIC_NAME | VALUE | GROUP_BY_INFO                                      |
+-------------+-------+----------------------------------------------------+
| NULL_COUNT  |    42 | [{"id":"7","name":"REGION","value":"US"}]          |
| NULL_COUNT  |     5 | [{"id":"7","name":"REGION","value":"EU"}]          |
| NULL_COUNT  |     3 | [{"id":"7","name":"REGION","value":"APAC"}]        |
+-------------+-------+----------------------------------------------------+
```

**Example: Filter results for a specific group**

Copy code

```
SELECT metric_name, value, measurement_time
  FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS,
       LATERAL FLATTEN(input => group_by_info) f
  WHERE table_name = 'CUSTOMER_DATA'
    AND f.value:name::STRING = 'REGION'
    AND f.value:value::STRING = 'US';
```

**Example: Compare results across groups from the same evaluation**

All rows from a single evaluation share the same `reference_id` (the association ID) and
`measurement_time`. Use both columns to scope results to one evaluation run:

Copy code

```
SELECT f.value:name::STRING AS group_column,
       f.value:value::STRING AS group_value,
       value
  FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS,
       LATERAL FLATTEN(input => group_by_info) f
  WHERE reference_id = '<your_reference_id>'
    AND measurement_time = '<measurement_time>';
```

## View grouping configuration

### DATA\_METRIC\_FUNCTION\_REFERENCES table function

The [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) table function exposes
grouping details for each association through its `PROPERTIES` VARIANT column. The two keys
that are specific to WITHIN GROUP are:

| Field | Description |
| --- | --- |
| `properties:within_group` | A JSON-encoded string representing the array of column references used in the WITHIN GROUP clause, in the format `"[{\"domain\":\"COLUMN\",\"id\":\"<id>\",\"name\":\"<col_name>\"}]"`. Apply `PARSE_JSON()` to convert the string into a queryable array. NULL if no grouping is configured. |
| `properties:group_limit` | The maximum group limit for this association, or NULL if no grouping is configured. |

Expand

Show lessSee more

For the full list of keys included in the `PROPERTIES` column, see
[DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references).

For example:

Copy code

```
SELECT ref_entity_name,
       metric_name,
       PARSE_JSON(properties:within_group::STRING) AS within_group,
       properties:group_limit::NUMBER AS group_limit
  FROM TABLE(INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
    REF_ENTITY_NAME => 'CUSTOMER_DATA',
    REF_ENTITY_DOMAIN => 'TABLE'));
```

Example output:

```
+-----------------+-------------+-------------------------------------------------+-------------+
| REF_ENTITY_NAME | METRIC_NAME | WITHIN_GROUP                                    | GROUP_LIMIT |
+-----------------+-------------+-------------------------------------------------+-------------+
| CUSTOMER_DATA   | NULL_COUNT  | [{"domain":"COLUMN","id":"7","name":"REGION"}]  |        1000 |
+-----------------+-------------+-------------------------------------------------+-------------+
```

The [DATA\_METRIC\_FUNCTION\_REFERENCES view](/sql-reference/account-usage/data_metric_function_references) view exposes the same
`PROPERTIES` column.

## Extract error rows for a specific group

When a grouped DMF flags a quality issue, you might want to inspect the raw rows that contributed
to a specific group’s result. The [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function
accepts an optional `WITHIN_GROUP_VALUES` argument that filters the scan to a specific group:

Copy code

```
SELECT * FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
  REF_ENTITY_NAME     => '<table_or_view>',
  METRIC_NAME         => '<dmf_name>',
  ARGUMENT_NAME       => '<column>',
  [ AT_TIMESTAMP      => '<timestamp>', ]
  [ WITHIN_GROUP_VALUES => '<json_object>' ]
));
```

### Arguments

| Argument | Description |
| --- | --- |
| `WITHIN_GROUP_VALUES` | A JSON object that maps grouping column names to the specific group values you want to scan. For example: `'{"REGION": "US", "PRODUCT_CATEGORY": "Electronics"}'`. Only string and numeric values are supported. If you omit this argument, the scan returns all rows regardless of group. |

Expand

Show lessSee more

**Example: View null rows in the US region**

Copy code

```
SELECT * FROM TABLE(SYSTEM$DATA_METRIC_SCAN(
  REF_ENTITY_NAME     => 'CUSTOMER_DATA',
  METRIC_NAME         => 'snowflake.core.null_count',
  ARGUMENT_NAME       => 'NAME',
  WITHIN_GROUP_VALUES => '{"REGION": "US"}'));
```

This returns all rows where `name IS NULL` and `region = 'US'`.

## Use expectations with grouped associations

Expectations work with grouped DMF associations. When an expectation is defined on a grouped
association, it’s evaluated independently for each group, and a per-group result is written to
the event table. To inspect per-group expectation results, query the
[DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view](/sql-reference/local/data_quality_monitoring_expectation_status) view, which includes a
`GROUP_BY_INFO` column that identifies the group for each row.

Notifications behave differently from per-group results. For a single evaluation, Snowflake fires
at most one notification, based on the worst-group value (the maximum metric value across all
groups). If at least one group violates the expectation, you receive one notification for that
evaluation. Per-group violation details are still recorded in the event table for follow-up
analysis.

To evaluate expectations on demand, use
[SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations). For a grouped association,
this function evaluates every group and returns one row per group, with each group identified in
the `GROUP_BY_VALUES` output column. To inspect the underlying rows for a specific group value,
use [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) with the `WITHIN_GROUP_VALUES` argument
(see [Extract error rows for a specific group](#label-data-quality-group-by-extract-errors)).

For more information about expectations, see [Use SQL to work with expectations](/user-guide/data-quality-expectations).

## Limitations

- **Custom DMF compatibility.** The WITHIN GROUP clause isn’t supported for custom DMFs that use
  CTEs, `UNION`, `UNION ALL`, `JOIN`, `DISTINCT`, or window functions. For details, see
  [Supported DMFs](#label-data-quality-group-by-supported-dmfs).
- **Schema-level associations.** WITHIN GROUP isn’t supported on schema-level DMF associations
  (`ALTER SCHEMA ... ADD DATA METRIC FUNCTION`). To group by a column, create the association at
  the table or view level.
- **One association per DMF, table, and column combination.** Because only one association is
  allowed per metric, table, and column combination, you can only have one grouping configuration
  per combination.
- **Group limit.** Valid values for `GROUP LIMIT` are 1 through 1000, with a default of 1000. If
  the number of distinct groups at evaluation time exceeds the configured limit, the evaluation
  fails and no results are written for that run. Reduce cardinality in your grouping column, or
  raise `GROUP LIMIT` up to the maximum of 1000 to avoid this error.
- **Immutable grouping configuration.** The grouping columns and group limit can’t be changed
  after an association is created. Drop and re-create the association to change the grouping.
- **Anomaly detection.** The per-association `ANOMALY_DETECTION` property and the system
  anomaly DMFs in the `SNOWFLAKE.CORE` schema (such as `ROW_COUNT` and `FRESHNESS` with
  anomaly detection enabled) aren’t supported with WITHIN GROUP. The `ANOMALY_DETECTION`
  property is automatically disabled when a WITHIN GROUP clause is present. Full anomaly detection
  support for groups is planned for a future release.
