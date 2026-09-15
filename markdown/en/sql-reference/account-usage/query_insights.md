Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUERY\_INSIGHTS view

This Account Usage view displays a row for each [insight produced for a query](/user-guide/query-insights).

## Columns

| Column name | Type | Description |
| --- | --- | --- |
| `start_time` | TIMESTAMP\_LTZ | Start time of the query. |
| `end_time` | TIMESTAMP\_LTZ | End time of the query. |
| `total_elapsed_time` | NUMBER | Total elapsed time of the query (in milliseconds). |
| `query_id` | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| `query_hash` | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| `query_parameterized_hash` | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| `warehouse_id` | VARCHAR | Internal/system-generated identifier for the warehouse that was used. |
| `warehouse_name` | VARCHAR | Warehouse that the query executed on, if any. |
| `insight_instance_id` | NUMBER | Internal/system-generated identifier for the insight. |
| `insight_type_id` | VARCHAR | Identifier of the [insight type](/user-guide/query-insights#label-query-insights-types). |
| `message` | VARIANT | Structured information and details about the insight. |
| `suggestions` | ARRAY | Array of strings, each containing a recommended action for the insight. |
| `is_opportunity` | BOOLEAN | If `true`, the insight includes suggestions to improve query performance. For example:   - For an insight with the type ID `QUERY_INSIGHT_NO_FILTER_ON_TOP_OF_TABLE_SCAN`, this column contains `true` because   the insight includes suggestions for improving performance. - For an insight with the type ID `QUERY_INSIGHT_FILTER_WITH_CLUSTERING_KEY`, this column contains `false` because the   insight does not include suggestions for improving performance. |
| `insight_topic` | VARCHAR | Label that identifies the type of performance impact detected by this insight. For the list of labels, see `Insight topics`\_. |

Expand

Show lessSee more

### Insight topics

For the `insight_topic` column, the label can be one of the following:

- `TABLE_SCAN`: Insights about the efficiency of accessing tables. This label applies to the following types of insights:

  - [QUERY\_INSIGHT\_NO\_FILTER\_ON\_TOP\_OF\_TABLE\_SCAN](/user-guide/query-insights#label-query-insight-no-filter-on-top-of-table-scan)
  - [QUERY\_INSIGHT\_INAPPLICABLE\_FILTER\_ON\_TABLE\_SCAN](/user-guide/query-insights#label-query-insight-inapplicable-filter-on-table-scan)
  - [QUERY\_INSIGHT\_UNSELECTIVE\_FILTER](/user-guide/query-insights#label-query-insight-unselective-filter)
  - [QUERY\_INSIGHT\_LIKE\_WITH\_LEADING\_WILDCARD](/user-guide/query-insights#label-query-insight-like-with-leading-wildcard)
  - [QUERY\_INSIGHT\_FILTER\_WITH\_CLUSTERING\_KEY](/user-guide/query-insights#label-query-insight-filter-with-clustering-key)
  - [QUERY\_INSIGHT\_SEARCH\_OPTIMIZATION\_USED](/user-guide/query-insights#label-query-insight-search-optimization-used)
  - [QUERY\_INSIGHT\_SNOWFLAKE\_OPTIMA](/user-guide/query-insights#label-query-insight-snowflake-optima)
  - [QUERY\_INSIGHT\_SEARCH\_OPTIMIZATION\_AND\_SNOWFLAKE\_OPTIMA](/user-guide/query-insights#label-query-insight-search-optimization-and-snowflake-optima)
- `QUERY`: Insights about the efficiency of query execution plans. This label applies to the following types of insights:

  - [QUERY\_INSIGHT\_SNOWFLAKE\_OPTIMA\_PLANNING\_USED](/user-guide/query-insights#label-query-insight-optima-planning-used)
  - [QUERY\_INSIGHT\_SNOWFLAKE\_OPTIMA\_PLANNING\_OPPORTUNITY](/user-guide/query-insights#label-query-insight-snowflake-optima-planning-opportunity)
- `JOIN`: Insights about the efficiency of JOIN operations in the query. This label applies to the following types of insights:

  - [QUERY\_INSIGHT\_JOIN\_WITH\_NO\_JOIN\_CONDITION](/user-guide/query-insights#label-query-insight-join-with-no-join-condition)
  - [QUERY\_INSIGHT\_INEFFICIENT\_JOIN\_CONDITION](/user-guide/query-insights#label-query-insight-inefficient-join-condition)
  - [QUERY\_INSIGHT\_NESTED\_EXPLODING\_JOIN](/user-guide/query-insights#label-query-insight-nested-exploding-join)
  - [QUERY\_INSIGHT\_EXPLODING\_JOIN](/user-guide/query-insights#label-query-insight-exploding-join)
- `AGGREGATE`: Insights about the efficiency of aggregate operations in the query. This label applies to the following types of
  insights:

  - [QUERY\_INSIGHT\_INEFFICIENT\_AGGREGATE](/user-guide/query-insights#label-query-insight-inefficient-aggregate)
- `UNION`: Insights about the efficiency of UNION operations in the query. This label applies to the following types of
  insights:

  - [QUERY\_INSIGHT\_UNNECESSARY\_UNION\_DISTINCT](/user-guide/query-insights#label-query-insight-unnecessary-union-distinct)
- `WAREHOUSE`: Insights about the warehouse used for the query. This label applies to the following types of insights:

  - [QUERY\_INSIGHT\_REMOTE\_SPILLAGE](/user-guide/query-insights#label-query-insight-remote-spillage)
  - [QUERY\_INSIGHT\_QUEUED\_OVERLOAD](/user-guide/query-insights#label-query-insight-queued-overload)

## Usage notes

- Latency for the view may be up to 90 minutes.

## Examples

The following example returns the query insights for the query with the ID
`01bd3a9d-0910-8327-0000-09717704c032`:

Copy code

```
SELECT query_id, insight_type_id, message, suggestions
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_INSIGHTS
  WHERE query_id = '01bd3a9d-0910-8327-0000-09717704c032';
```

The following example returns the query insights for queries that have the same
[hash of parameterized query text](/user-guide/query-hash). These are queries that use the same SELECT statement except for
the literals specified in the statement.

Copy code

```
SELECT query_id, insight_type_id, message, suggestions
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_INSIGHTS
  WHERE query_parameterized_hash = '4bb66effc1a3c8b4e94a728f7caaa736';
```

The following example returns the query insights for queries that ran during the past week:

Copy code

```
SELECT query_id, insight_type_id, message, suggestions
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_INSIGHTS
  WHERE start_time > TO_DATE(DATEADD(DAY, -7, CURRENT_DATE()));
```

The following example returns the query insights for queries that ran during the past week and took more than an hour to complete:

Copy code

```
SELECT query_id, insight_type_id, message, suggestions
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_INSIGHTS
  WHERE start_time > TO_DATE(DATEADD(DAY, -7, CURRENT_DATE()))
    AND total_duration > 3600000;
```

The following example returns the query insights for queries that ran during the past week, took more than an hour to complete,
and used the warehouse with the ID `84412315`:

Copy code

```
SELECT query_id, insight_type_id, message, suggestions
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_INSIGHTS
  WHERE start_time > TO_DATE(DATEADD(DAY, -7, CURRENT_DATE()))
    AND total_duration > 3600000
    AND warehouse_id = 84412315;
```
