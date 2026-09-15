Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$ESTIMATE\_QUERY\_ACCELERATION

For a previously executed query, this function returns a JSON object that specifies if the query is eligible to benefit from the
[query acceleration service](/user-guide/query-acceleration-service). If the query is eligible for query acceleration, the output
includes the estimated query execution time for different query acceleration scale factors.

See also:
:   [QUERY\_ACCELERATION\_ELIGIBLE view](/sql-reference/account-usage/query_acceleration_eligible)

## Syntax

Copy code

```
SYSTEM$ESTIMATE_QUERY_ACCELERATION( '<query_id>' )
```

## Parameters

`query_id`
:   Query ID. Query ID must be for a query executed within the last 14 days; otherwise, the `status` is `invalid`.

## Output

The function returns a JSON object with the properties described below:

|  |  |
| --- | --- |
| `eligible` | The query can benefit from query acceleration. |
| `ineligible` | The query cannot benefit from query acceleration. |
| `accelerated` | The query has already been accelerated. |
| `invalid` | The query with the specified ID was not found. |

Expand

Show lessSee more

|  |  |  |
| --- | --- | --- |
| `eligible` | The query can benefit from query acceleration. |  |
| `ineligible` | The query cannot benefit from query acceleration. |  |
| `accelerated` | The query has already been accelerated. |  |
| `invalid` | The query with the specified ID was not found. | The query with the specified ID was not found. |
| `invalid` | The query with the specified ID was not found. | The query with the specified ID was not found. |
| `upperLimitScaleFactor` | Number of the highest query acceleration scale factor in the `estimatedQueryTimes` object. If the `status` for the query is  not `eligible` for query acceleration, this field is set to `0`. |  |

Expand

Show lessSee more

In the `estimatedQueryTimes` object, each name / value pair specifies a query acceleration [scale factor](/sql-reference/sql/create-warehouse#label-query-acceleration-max-scale-factor) and the estimated query execution time at that scale factor.

The following example lists the estimated query execution time for the scale factors `1`, `2`, `4` and
`8`:

Copy code

```
...
"estimatedQueryTimes" : {
  "1" : 171,
  "2": 152,
  "4": 133,
  "8": 120
}
...
```

## Usage notes

- Estimated query times are for analysis purposes only and are not guaranteed.
- Estimated query times are calculated based on the assumption that the query is serviced by all the compute resources allocated by the
  query acceleration service based on scale factor.
- Estimated query times do not factor in concurrency.

## Examples

For example queries, see [Identifying queries with the SYSTEM$ESTIMATE\_QUERY\_ACCELERATION function](/user-guide/query-acceleration-service#label-identify-queries-using-system-estimate-query-acceleration).
