Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS

Returns estimated costs associated with enabling [Automatic Clustering](/user-guide/tables-auto-reclustering) for a table. This
function is used to do the following:

- Estimate the cost of clustering a table for the first time.
- Estimate the cost of changing the cluster key of a table.
- Estimate, when possible, the cost associated with maintaining the table after it’s clustered around the specified key.
  Sometimes, a table might need more DML history to estimate future maintenance costs.

Important

The cost estimates returned by the SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS function are best efforts. The actual realized costs can vary by up to 100% (or, in rare cases, several times) from the estimated costs.

## Syntax

Copy code

```
SYSTEM$ESTIMATE_AUTOMATIC_CLUSTERING_COSTS( '<table_name>' ,
 [ '( <expr1> [ , <expr2> ... ] )' ] )
```

## Arguments

‘`table_name`’
:   Name of the table for which you want to return the estimated cost of clustering.

‘`(expr1 [ , expr2 ... ])`’
:   The proposed cluster key for the table is where each expression resolves to a table column. The function estimates the cost of
    clustering the table using these columns as the cluster key.

Even if only one column name or expression is passed, it must be inside parentheses.

This argument is required for a table with no clustering key. An error is returned if the argument is omitted.

This argument is optional for a table with a clustering key. If the argument is omitted, the function estimates the cost of
clustering the table using the table’s current clustering key.

## Returns

A value of type VARCHAR. The returned string is in JSON format and contains the following name/value pairs:

`warning`
:   Indicates whether conditions might affect the cost estimation accuracy or the impact of choosing a cluster key.

`reportTime`
:   Date when the function’s output was generated.

`clusteringKey`
:   Columns that make up the cluster key.

`initial`
:   Describes the predicted cost of clustering the table around the specified cluster key.
    The estimated cost of maintaining the table once it is clustered is not included.
    The `initial` JSON object contains the following name/value pairs.

    `unit`
    :   Indicates the units in which the initial cost is expressed.

    `value`
    :   Indicates the cost to cluster the table, expressed in `unit`.

    `comment`
    :   Interprets the initial cost of clustering.

`maintenance`
:   Describes the predicted costs of maintaining a well-clustered table after it is initially clustered.
    This prediction is based on recent DML activity because a table is reclustered as it changes.

    An empty object indicates that Snowflake was unable to provide a maintenance cost estimate. In most cases, Snowflake is unable to provide
    a maintenance estimate because the table did not have enough DML history available or did not have enough supported DML types in the
    past week to accurately predict costs.

    `unit`
    :   Indicates the units in which the cost is expressed.

    `value`
    :   Indicates how much it will cost to maintain the table after its initial clustering, expressed in `units` per day.

    `comment`
    :   Includes costs-incurring period and the time frame upon which the estimate is based.

## Access control requirements

The privileges needed to estimate costs are the same as those required to read the table and change the cluster key. You need the
following privileges:

- SELECT and INSERT privileges on the table, or OWNERSHIP privilege on the table.
- USAGE or OWNERSHIP privilege on the parent schema and database.

## Usage notes

- The cost estimates returned by the SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS function are based on sampling a subset of
  micro-partitions from your table and capturing the clustering execution time. Depending on sampled specific micro-partitions
  and the system speed, the cost estimates might differ between function executions.
- For the best possible accuracy, you can run SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS multiple times and average the results.
  The function uses sample clustering jobs and collects their execution time. The provided cost estimate might fluctuate depending
  on the system speed.
  Running the function multiple times and averaging the results can produce a more accurate cost estimate.
- The most common reason for an inaccurate maintenance cost estimate is that the past DML patterns based on the estimate did not
  match future DML patterns.
- Snowflake is able to provide a one-time cost estimate in the vast majority of cases and a maintenance cost estimate in some cases. If the
  function is unable to provide a maintenance cost estimate, Snowflake includes a reason in the output.

## Examples

Return the estimated costs associated with defining columns `day` and `tenantId` as the cluster key for table `myTable`.

Copy code

```
SELECT SYSTEM$ESTIMATE_AUTOMATIC_CLUSTERING_COSTS('myTable', '(day, tenantId)');
```

```
{
  "reportTime": "Fri, 12 Jul 2024 01:06:18 GMT",
  "clusteringKey": "LINEAR(day, tenantId)",
  "initial": {
    "unit": "Credits",
    "value": 98.2,
    "comment": "Total upper bound of one-time cost"
  },
  "maintenance": {
    "unit": "Credits",
    "value": 10.0,
    "comment": "Daily maintenance cost estimate provided based on DML history from the
    past seven days."
  }
}
```
