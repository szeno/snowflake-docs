Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$ESTIMATE\_SEARCH\_OPTIMIZATION\_COSTS

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the estimated costs of adding [search optimization](/user-guide/search-optimization-service) to a given table and
configuring specific columns for search optimization.

Important

Cost estimates returned by the SYSTEM$ESTIMATE\_SEARCH\_OPTIMIZATION\_COSTS function are best efforts. The actual realized
costs can vary by up to 50% (or, in rare cases, by several times) from the estimated costs.

- Build and storage cost estimates are based on sampling a subset of the rows in the table
- Maintenance cost estimates are based on recent create, delete, and update activity in the table

## Syntax

Copy code

```
SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('<table_name>' [ , '<search_method_with_target>' ])
```

## Arguments

**Required:**

`table_name`
:   Table for which you want to estimate the search optimization costs.

    If the table name is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the function looks for the table in the current schema for the session.

    The entire name must be enclosed in single quotes.

**Optional:**

`search_method_with_target`
:   Specifies a [search method and target](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-search-method-target) for a
    [column configuration](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding) similar to what can be
    specified in the ON clause of the [ALTER TABLE](/sql-reference/sql/alter-table) … [ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command.

    This entire argument must be enclosed in single quotes. Within this string, use double quotes around column names
    [where required](/sql-reference/identifiers-syntax#label-delimited-identifier).

## Output

The function returns a JSON object with the properties described below:

| Property | Description |
| --- | --- |
| `tableName` | Name of the table. |
| `searchOptimizationEnabled` | `true` if search optimization is enabled for the table or any columns in it; `false` otherwise. |
| `costPositions` | Array of objects that describe the predicted costs of adding search optimization to the table or its columns. |

Expand

Show lessSee more

Each object in the `costPositions` array represents a different type of cost estimate:

Copy code

```
...
"costPositions" : [
  {
    "name" : "BuildCosts",
    ...
  }, {
    "name" : "StorageCosts",
    ...
  }, {
    "name" : "Benefit",
    ...
  }, {
    "name" : "MaintenanceCosts",
    ...
  }
]
...
```

The `name` property identifies the type of cost represented by the object. `name` can be one of the following:

| `name` of object in `costPositions` | Description |
| --- | --- |
| `BuildCosts` | This object describes the predicted costs of building the search access path for the table. If search optimization has already been added to the table or to all the specified columns, this object contains no cost information. |
| `StorageCosts` | This object describes the predicted amount of storage space (in TB) needed for the search access path for the table. |
| `Benefit` | This object appears only when the table has search optimization enabled. It does not contain information at this time. |
| `MaintenanceCosts` | This object describes the predicted costs of maintaining the search access path for the table when rows are inserted, deleted, or modified. If the table has been created recently, no cost information is reported. |

Expand

Show lessSee more

Each object in the `costPositions` array can have the following properties:

| Property | Description |
| --- | --- |
| `name` | [Name](/sql-reference/functions/system_estimate_search_optimization_costs#label-costpositions-object-names) that identifies the type of cost information represented by this object. |
| `costs` | Object that describes the predicted costs in terms of the following properties: |
| `value` | Amount of the predicted cost. |
| `unit` | Unit of measure for the cost (e.g., “Credits” for compute costs, “TB” for storage costs, etc.). |
| `perTimeUnit` | For maintenance costs, the unit of time that the estimated cost covers (for example, `"MONTH"` for the cost per month). |
| `computationMethod` | Method used to estimate the costs, if multiple methods are available. |
| `comment` | Additional information about the estimated cost. |

Expand

Show lessSee more

## Usage notes

- The `searchOptimizationEnabled` property is `true` when the table or any column in it has search optimization enabled.
- For the build cost, this function returns an approximation based on building search access paths for a sample of the data in the
  specified table.
- For the maintenance cost, this function bases the estimates on recent changes made to the table (the changes to bytes over
  time).
- In order to call the function, you must have a warehouse in use. If no warehouse is currently in use, the function reports the
  following error:

  Copy code

  ```
  No active warehouse selected in the current session.
  Select an active warehouse with the 'use warehouse' command.
  ```

  The [warehouse size](/user-guide/warehouses-overview#label-warehouse-size) has no effect on the performance of this function, so you can use an
  X-Small warehouse.
- Because the function uses a warehouse, you are billed for warehouse usage for this function.
- The function can take somewhere in the range of 20 seconds to 10 minutes to complete. Using a larger warehouse does
  not result in faster execution.

## Examples

The following example shows the estimated costs of adding search optimization to a table:

> Copy code
>
> ```
> SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_without_search_opt')
>   AS estimate_for_table_without_search_optimization;
> ```
>
> ```
> +---------------------------------------------------------------------------+
> | ESTIMATE_FOR_TABLE_WITHOUT_SEARCH_OPTIMIZATION                            |
> |---------------------------------------------------------------------------|
> | {                                                                         |
> |   "tableName" : "TABLE_WITHOUT_SEARCH_OPT",                               |
> |   "searchOptimizationEnabled" : false,                                    |
> |   "costPositions" : [ {                                                   |
> |     "name" : "BuildCosts",                                                |
> |     "costs" : {                                                           |
> |       "value" : 11.279,                                                   |
> |       "unit" : "Credits"                                                  |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "StorageCosts",                                              |
> |     "costs" : {                                                           |
> |       "value" : 0.070493,                                                 |
> |       "unit" : "TB"                                                       |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "MaintenanceCosts",                                          |
> |     "costs" : {                                                           |
> |       "value" : 30.296,                                                   |
> |       "unit" : "Credits",                                                 |
> |       "perTimeUnit" : "MONTH"                                             |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "Estimated from historic change rate over last ~11 days." |
> |   } ]                                                                     |
> | }                                                                         |
> +---------------------------------------------------------------------------+
> ```

The following example shows the output of this function for a table that already has search optimization enabled. You
can see that no build cost information is available in this case. Also, the `Benefit` property is included (but
it does not contain any information).

> Copy code
>
> ```
> SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_with_search_opt')
>   AS estimate_for_table_with_search_optimization;
> ```
>
> ```
> +---------------------------------------------------------------------------+
> | ESTIMATE_FOR_TABLE_WITH_SEARCH_OPTIMIZATION                               |
> |---------------------------------------------------------------------------|
> | {                                                                         |
> |   "tableName" : "TABLE_WITH_SEARCH_OPT",                                  |
> |   "searchOptimizationEnabled" : true,                                     |
> |   "costPositions" : [ {                                                   |
> |     "name" : "BuildCosts",                                                |
> |     "computationMethod" : "NotAvailable",                                 |
> |     "comment" : "Search optimization is already enabled."                 |
> |   }, {                                                                    |
> |     "name" : "StorageCosts",                                              |
> |     "costs" : {                                                           |
> |       "value" : 0.052048,                                                 |
> |       "unit" : "TB"                                                       |
> |     },                                                                    |
> |     "computationMethod" : "Measured"                                      |
> |   }, {                                                                    |
> |     "name" : "Benefit",                                                   |
> |     "computationMethod" : "NotAvailable",                                 |
> |     "comment" : "Currently not supported."                                |
> |   }, {                                                                    |
> |     "name" : "MaintenanceCosts",                                          |
> |     "costs" : {                                                           |
> |       "value" : 30.248,                                                   |
> |       "unit" : "Credits",                                                 |
> |       "perTimeUnit" : "MONTH"                                             |
> |     },                                                                    |
> |     "computationMethod" : "EstimatedUpperBound",                          |
> |     "comment" : "Estimated from historic change rate over last ~11 days." |
> |   } ]                                                                     |
> | }                                                                         |
> +---------------------------------------------------------------------------+
> ```

The following example shows the output of this function for estimating search optimization on three specific columns of
a table using the EQUALITY search method (that is, the estimate is for enabling search optimization only for equality
comparisons on these columns). Neither the table nor any of its columns already have any type of search optimization enabled.

> Copy code
>
> ```
> SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_without_search_opt', 'EQUALITY(C1, C2, C3)')
>   AS estimate_for_columns_without_search_optimization;
> ```
>
> ```
> +---------------------------------------------------------------------------+
> | ESTIMATE_FOR_COLUMNS_WITHOUT_SEARCH_OPTIMIZATION                          |
> |---------------------------------------------------------------------------|
> | {                                                                         |
> |   "tableName" : "TABLE_WITHOUT_SEARCH_OPT",                               |
> |   "searchOptimizationEnabled" : false,                                    |
> |   "costPositions" : [ {                                                   |
> |     "name" : "BuildCosts",                                                |
> |     "costs" : {                                                           |
> |       "value" : 10.527,                                                   |
> |       "unit" : "Credits"                                                  |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "StorageCosts",                                              |
> |     "costs" : {                                                           |
> |       "value" : 0.040323,                                                 |
> |       "unit" : "TB"                                                       |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "MaintenanceCosts",                                          |
> |     "costs" : {                                                           |
> |       "value" : 22.821,                                                   |
> |       "unit" : "Credits",                                                 |
> |       "perTimeUnit" : "MONTH"                                             |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "Estimated from historic change rate over last ~7 days."  |
> |   } ]                                                                     |
> | }                                                                         |
> +---------------------------------------------------------------------------+
> ```

If a similar query is run on a table where search optimization is already enabled for any of the specified columns, the
output includes a build cost estimate that covers adding search optimization to the specified columns where it is
not already enabled. This is different from the earlier example where we were estimating search optimization on a whole
table where search optimization was already enabled, which resulted in no build cost estimate since there was no build
work to be done.

The storage estimate here includes only the actual search access path size for the columns where search optimization is
already enabled.

The maintenance estimate covers all of the specified columns regardless of whether they already have search optimization
enabled.

> Copy code
>
> ```
> SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_with_search_opt', 'EQUALITY(C1, C2, C3)')
>   AS estimate_for_columns_with_search_optimization;
> ```
>
> ```
> +---------------------------------------------------------------------------+
> | ESTIMATE_FOR_COLUMNS_WITH_SEARCH_OPTIMIZATION                             |
> |---------------------------------------------------------------------------|
> | {                                                                         |
> |   "tableName" : "TABLE_WITH_SEARCH_OPT",                                  |
> |   "searchOptimizationEnabled" : true,                                     |
> |   "costPositions" : [ {                                                   |
> |     "name" : "BuildCosts",                                                |
> |     "costs" : {                                                           |
> |       "value" : 8.331,                                                    |
> |       "unit" : "Credits"                                                  |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "StorageCosts",                                              |
> |     "costs" : {                                                           |
> |       "value" : 0.040323,                                                 |
> |       "unit" : "TB"                                                       |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "estimated via sampling"                                  |
> |   }, {                                                                    |
> |     "name" : "Benefit",                                                   |
> |     "computationMethod" : "NotAvailable",                                 |
> |     "comment" : "Currently not supported."                                |
> |   }, {                                                                    |
> |     "name" : "MaintenanceCosts",                                          |
> |     "costs" : {                                                           |
> |       "value" : 22.821,                                                   |
> |       "unit" : "Credits",                                                 |
> |       "perTimeUnit" : "MONTH"                                             |
> |     },                                                                    |
> |     "computationMethod" : "Estimated",                                    |
> |     "comment" : "Estimated from historic change rate over last ~7 days."  |
> |   } ]                                                                     |
> | }                                                                         |
> +---------------------------------------------------------------------------+
> ```
