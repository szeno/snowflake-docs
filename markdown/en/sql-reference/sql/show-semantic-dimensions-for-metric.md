# SHOW SEMANTIC DIMENSIONS FOR METRIC

Lists the dimensions that you can return when querying a specific metric in a
[semantic view](/user-guide/views-semantic/overview).

When you specify a dimension and a metric in a semantic view query, the logical table for the dimension must be related to the
logical table for the metric. In addition, the logical table for the dimension must have an equal or lower level of granularity
than the logical table for the metric.

To determine which dimensions meet this criteria, you can run this command.

For details, see [Choosing the dimensions that you can return for a given metric](/user-guide/views-semantic/querying#label-semantic-views-query-dimensions-metrics).

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) , [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) , [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) , [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

## Syntax

Copy code

```
SHOW SEMANTIC DIMENSIONS [ LIKE '<pattern>' ]
                         IN <semantic_view_name>
                         FOR METRIC <metric_name>
                         [ STARTS WITH '<name_string>' ]
                         [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN semantic_view_name`
:   Specifies the name of the semantic view containing the dimensions and metric.

`FOR METRIC metric_name`
:   Specifies the name of the metric for which to show associated dimensions.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `table_name` | Name of the logical table for the dimension. |
| `name` | Name of the dimension. |
| `data_type` | Data type of the dimension. |
| `required` | Indicates whether the dimension is required for the metric. |
| `synonyms` | Alternative names or synonyms for the dimension. |
| `comment` | Comment about the dimension. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | Semantic view |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists the dimensions that you can specify in a query for the `order_average_value` metric in the
`tpch_rev_analysis` semantic view:

Copy code

```
SHOW SEMANTIC DIMENSIONS IN tpch_rev_analysis FOR METRIC order_average_value;
```

```
+------------+---------------+-------------+----------+-------------------+--------------------------------+
| table_name | name          | data_type   | required | synonyms          | comment                        |
|------------+---------------+-------------+----------+-------------------+--------------------------------|
| CUSTOMERS  | CUSTOMER_NAME | VARCHAR(25) | false    | ["customer name"] | Name of the customer           |
| ORDERS     | ORDER_DATE    | DATE        | false    | NULL              | Date when the order was placed |
| ORDERS     | ORDER_YEAR    | NUMBER(4,0) | false    | NULL              | Year when the order was placed |
+------------+---------------+-------------+----------+-------------------+--------------------------------+
```

The following example lists the dimensions that are required when you query a window function metric.

This example uses the semantic view that you defined in [Defining window function metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-window-defining). The example returns
the dimensions that you can specify in the query for the `avg_7_days_sales_quantity` metric.

Copy code

```
SHOW SEMANTIC DIMENSIONS IN sv_window_function_example FOR METRIC avg_7_days_sales_quantity;
```

```
+------------+-----------+--------------+----------+----------+---------+
| table_name | name      | data_type    | required | synonyms | comment |
|------------+-----------+--------------+----------+----------+---------|
| DATE       | DATE      | DATE         | true     | NULL     | NULL    |
| DATE       | D_DATE_SK | NUMBER(38,0) | false    | NULL     | NULL    |
| DATE       | YEAR      | NUMBER(38,0) | true     | NULL     | NULL    |
+------------+-----------+--------------+----------+----------+---------+
```

Note that the `required` column contains `true` for the `date` and `year` dimensions. This is because the definition of
the `avg_7_days_sales_quantity` metric specifies the `date` and `year` dimensions in PARTITION BY EXCLUDING:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW sv_window_function_example
  ...
  METRICS (
    ...
      store_sales.avg_7_days_sales_quantity as AVG(total_sales_quantity)
        OVER (PARTITION BY EXCLUDING date.date, date.year ORDER BY date.date
          RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)
        WITH SYNONYMS = ('Running 7-day average of total sales quantity'),
```

Because of this, the `date` and `year` dimensions are required in any query of the `avg_7_days_sales_quantity` metric. You
must specify these dimensions in the query:

Copy code

```
SELECT * FROM SEMANTIC_VIEW (
  sv_window_function_example
  DIMENSIONS date.date, date.year
  METRICS store_sales.avg_7_days_sales_quantity
);
```
