# Using the Query Hash to Identify Patterns and Trends in Queries

To identify, group, and analyze similar queries in the query history, you can use a hash of the query text. For example, you can:

- Group queries by the query hash to identify patterns in expensive queries.
- Determine the effects of performance improvements (for example, changes to clustering keys) on repeated queries.

In the following views and table functions, you can use the `query_hash` and `query_parameterized_hash` columns to get the
hash of the query text:

- ACCOUNT\_USAGE views (1 year retention)

  - [QUERY\_HISTORY view](/sql-reference/account-usage/query_history)
  - [QUERY\_ACCELERATION\_ELIGIBLE view](/sql-reference/account-usage/query_acceleration_eligible)
  - [TASK\_HISTORY view](/sql-reference/account-usage/task_history)
- INFORMATION\_SCHEMA table functions (7 days retention)

  - [QUERY\_HISTORY](/sql-reference/functions/query_history) table function
  - [TASK\_HISTORY](/sql-reference/functions/task_history) table function

You can use this hash to analyze repeated queries.

## Using the Hash of the Query (`query_hash`)

The `query_hash` column contains a hash value that is computed, based on the canonicalized text of the SQL statement. Repeated
queries that have exactly the same query text have the same `query_hash` values.

Repeated queries also have the same `query_hash` if their query text differs only in:

- Case insensitive identifier, session variable, and stage name

  Note that this does not include identifiers specified using IDENTIFIER() with bind variables. Bind variables with different
  values produce different query hashes.
- White space
- Comments

If any other part of the query text of two queries differ, those queries have different `query_hash` values.

For example, the following queries have the same `query_hash` value because they have exactly the same query text.

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'TIM'
```

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'TIM'
```

You can use the `query_hash` value to find patterns in query performance that might not be obvious otherwise. For example,
although a query might not be excessively expensive during any single execution, a frequently repeated query could lead to high
costs, based on the number of times it runs. You can use the `query_hash` value to identify the queries to focus on optimizing
first.

For example, the following query uses the `query_hash` value to identify the query IDs for the 100 longest-running queries:

Copy code

```
SELECT
    query_hash,
    COUNT(*),
    SUM(total_elapsed_time),
    ANY_VALUE(query_id)
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE warehouse_name = 'MY_WAREHOUSE'
    AND DATE_TRUNC('day', start_time) >= CURRENT_DATE() - 7
  GROUP BY query_hash
  ORDER BY SUM(total_elapsed_time) DESC
  LIMIT 100;
```

## Using the Hash of the Parameterized Query (`query_parameterized_hash`)

`query_parameterized_hash` contains a hash value that is computed based on the parameterized query, which means the version of
the query after literals are parameterized. These literals must be used in the query predicate and must be used with one of the
following [comparison operators](/sql-reference/operators-comparison):

- `=` (equal to)
- `!=` (not equal to)
- `>=` (greater than or equal to)
- `<=` (less than or equal to)

Repeated queries (including those with different parameter values) have the same `query_parameterized_hash` value.

Repeated queries also have the same `query_parameterized_hash` if their query text differs only in:

- Case insensitive identifier, session variable, and stage name

  Note that this does not include identifiers specified using IDENTIFIER() with bind variables. Bind variables with different
  values produce different query hashes.
- White space
- Comments

Queries that have the same `query_hash` value also have the same `query_parameterized_hash` value, but not vice versa.

For example, the following queries have the same `query_parameterized_hash` value because the literal values are the
only difference between the queries:

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'TIM'
```

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'AIHUA'
```

As is the case with the `query_hash` value, you can use the `query_parameterized_hash` value to find patterns in query
performance that might not be obvious otherwise.

The following statement computes the average `total_elapsed_time` each day for all queries with a specific
`query_parameterized_hash` value (`cbd58379a88c37ed6cc0ecfebb053b03`):

Copy code

```
SELECT
    DATE_TRUNC('day', start_time),
    SUM(total_elapsed_time),
    ANY_VALUE(query_id)
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE query_parameterized_hash = 'cbd58379a88c37ed6cc0ecfebb053b03'
    AND DATE_TRUNC('day', start_time) >= CURRENT_DATE() - 30
  GROUP BY DATE_TRUNC('day', start_time);
```

## Checking the Version That Was Used to Generate the Hash

Over time, the logic used by Snowflake to generate the query hash can change. Changes to this logic can result in different
hashes produced for the same query. For example, for a given query, the hash generated by version 1 of the logic might differ
from the hash generated by version 2 of the logic.

The views and table function output that include the `query_hash` and `query_parameterized_hash` columns also include the
following columns that specify the version of the logic used to produce the hashes:

- `query_hash_version`
- `query_parameterized_hash_version`

The version number in these columns is a NUMBER (for example, `1` for the first version of the logic, `2` for the second
version of the logic, etc.).

If these columns contain different version numbers for different periods of time, you can use these version columns to identify
the different hashes for the same query. For example:

Copy code

```
...
WHERE (query_hash = 'hash_from_v1' AND query_hash_version = 1)
  OR (query_hash = 'hash_from_v2' AND query_hash_version = 2)
```
