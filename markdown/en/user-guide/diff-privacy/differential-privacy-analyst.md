# Querying data protected by differential privacy

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic helps an analyst run queries against data protected by differential privacy (that is, privacy-protected tables and views), and
understand and adjust the results returned by the queries.

To execute a query against a privacy-protected table, a user must have the SELECT privilege on the table.

**Limitations**

- Differential privacy supports a subset of Snowflake data types, operators, query syntax, and functions. For a list of supported SQL that
  you can use in a query, see [Differential privacy SQL reference](/user-guide/diff-privacy/differential-privacy-sql-reference).
- Queries against privacy-protected tables take longer because Snowflake must run additional computations to determine how much
  noise to add. For basic queries, this latency is at least 7 seconds. Complex
  queries, such as the following, can take much longer:

  - Queries with many joins and sub-queries.
  - Queries that output multiple rows in the result, for example, when using GROUP BY clauses that result in hundreds or thousands of
    groups.
- In tables protected by differential privacy, fields in the outermost SELECT clause can only have aggregation, GROUP BY, or
  DP\_INTERVAL\_LOW/HIGH applied. Other actions, such as math and concatenation, are not allowed. Examples:

  - `SELECT key, COUNT(*) AS 'c', DP_INTERVAL_LOW('c') FROM T GROUP BY key`

    **Succeeds:** No unsupported actions taken on `key`, `COUNT(*)`, or `c`.
  - `SELECT key, 1 + COUNT(*) AS 'c', DP_INTERVAL_LOW('c') FROM T GROUP BY key`

    **Fails:** `1 + COUNT(*)` is specified on a field in the outermost SELECT clause.
  - `SELECT key, COUNT(1 + x) AS 'cnt', DP_INTERVAL_LO('cnt') FROM T GROUP BY key`

    **Succeeds:** `COUNT`, a permitted aggregation, happens after `1 + x` in the outermost SELECT clause.
  - `SELECT key, COUNT(x) AS 'c', DP_INTERVAL_LOW('c') FROM (SELECT key, 1 + income AS x FROM table) GROUP BY key`

    **Succeeds:** `1 + income` is applied in a nested SELECT clause, which is allowed.

## Query Fundamentals

This section discusses the basic components of a query that will succeed when run against a privacy-protected table. It includes:

- [Aggregating data](#label-diff-privacy-aggregating-data)
- [Using joins](#label-diff-privacy-joins)
- [Querying data protected by entity-level privacy](#label-diff-privacy-entity-level-queries)

### Aggregating data

All queries against a privacy-protected table must aggregate results rather than retrieve individual records. Not every part of a query
needs to use an aggregation function as long as the final result is aggregated.

With the exception of a COUNT function, a query cannot aggregate a column unless the column has a
[privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains).

For a list of supported aggregations, see [Functions](/user-guide/diff-privacy/differential-privacy-sql-reference#label-diff-privacy-sql-support-aggregate).

### Using joins

The following sections provide guidelines for using joins in a differentially private query:

- [Join operators](#label-diff-privacy-joins-operators)
- [Supported joins](#label-diff-privacy-joins-supported)
- [Using entity keys in joins](#label-diff-privacy-joins-entity-keys)
- [Data types and privacy domains](#label-diff-privacy-joins-data-types)
- [Uniqueness requirement](#label-diff-privacy-joins-no-duplicates)

To learn about the implications that joining two privacy-protected tables has on privacy domains, see
[Privacy domains and joins](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-joins).

#### Join operators

Each join must be an equi join that uses a single operator. For example, `t1.c1 == t2.c1` is supported, but `col1 > col2` and
`col1 + 10 = col2` are not. Unconditioned joins are not supported.

Joins must use the JOIN operator. The WHERE syntax for joins is not supported. For more information about join
syntax, see [Implementing joins](/user-guide/querying-joins#label-querying-join-implement).

#### Supported joins

Joins in a differentially private query must be one of the following:

- INNER
- { LEFT | RIGHT | FULL } OUTER
- NATURAL

Both sides of the join must have the same query pattern. For example, the following joins are supported:

**Both sides are identifiers**

> Copy code
>
> ```
> SELECT COUNT(*)
> FROM t1 INNER JOIN t2 ON t1.a=t2.a;
> ```

**Both sides are subqueries**

> Copy code
>
> ```
> SELECT COUNT(*)
> FROM (SELECT a, COUNT(b) FROM t1 GROUP BY a) AS g1
>     INNER JOIN (SELECT * FROM t2) AS g2
>     ON g1.a=g2.a;
> ```

Joining an identifier with a subquery is currently not supported.

For information about the supported query syntax related to joins, see [Query syntax](/user-guide/diff-privacy/differential-privacy-sql-reference#label-diff-privacy-sql-support-syntax).

#### Using entity keys in joins

When working with tables protected with [entity-level privacy](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy), you can minimize the amount
of noise by including the entity key column as part of the join key, especially if it doesn’t semantically change the query.

For example, consider the following tables where the entity is customers:

> | Table | Description |
> | --- | --- |
> | `customers` | Customer directory, where each row is a customer and has a `customer_id`. |
> | `transactions` | Customer transactions, where each customer can have multiple transactions. |
> | `transaction_lines` | Unique items that were purchased in a transaction. There can be multiple rows in a single transaction. |
>
> Expand
>
> Show lessSee more

If they are following best practices, the data provider has structured the data so that each of these tables has the entity key
`customer_id`. For this data schema, each transaction line can only belong to one transaction, and each transaction can only belong to
one customer. This relationship is not evident from the data itself, so without additional information the amount of noise added for
differential privacy will be higher than it needs to be.

You can minimize the amount of noise by including the entity key `customer_id` as part of the join key, even if it is redundant. For
example, joining the table `transactions` with `transaction_lines` typically only requires the join key `transaction_id`. However,
joining on both `transaction_id` and `customer_id` will result in a lower amount of noise.

#### Data types and privacy domains

When joining two tables, the data types of the join key columns from either side must be the same. For differential privacy, the data type
of a column includes whether or not it has a [privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains).

For example, if you had a privacy-protected table `transactions` and an unprotected table `product_lookup`, and you wanted to join them
on `product_id`, the `product_id` column in both tables must be the same data type (for example, a string) and must each have a privacy
domain.

To meet this requirement, the administrator for the analyst might need to define a privacy domain just like the data provider defines them.
For information on how to set a privacy domain for a table, see [Setting a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin#label-diff-privacy-admin-privacy-domains-create).

#### Uniqueness requirement

Joins can potentially duplicate rows of data, which can cause the amount of noise added to a query result to become unbounded. To ensure
that privacy-protected data is not duplicated in a join, the join key (that is, the columns on which the tables are joined) for
privacy-protected tables must match only one record in the other table. This means that when joining with a privacy-protected table, the
join key on the opposite side must be de-duplicated.

Important

The uniqueness requirement for joins doesn’t always apply to queries against tables that are protected by [entity-level privacy](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy). For entity-level privacy, queries must de-duplicate on the entity key before the aggregation.
As long as this is done after a join but before the aggregation, the join doesn’t need to be on de-duplicated data. For more
information about meeting these requirements, see [Querying data protected by entity-level privacy](#label-diff-privacy-entity-level-queries).

To satisfy the uniqueness requirement for joins, the query can use a GROUP BY on a subset of the join columns to group duplicate rows into
one result.

For example, suppose the `patients` table is protected by differential privacy and the `geo_lookup` table is not. The analyst wants to
join these two tables on `zip_code` so that they can filter the `patients` table on `State`. In order to ensure that the records in
the privacy-protected `patients` table are not duplicated, the query must de-duplicate the `zip_code` table on the join key. This must
be done explicitly even if the `geo_lookup` table is already unique on `zip_code`. This ensures that Snowflake can correctly account
for privacy.

Copy code

```
SELECT COUNT(*)
  FROM patients
  LEFT JOIN (SELECT zip_code, ANY_VALUE(state) AS residence_state
            FROM geo_lookup
            GROUP BY zip_code)
  USING zip_code
  WHERE birth_state = residence_state;
```

### Querying data protected by entity-level privacy

Most data providers use an entity key to implement [entity-level privacy](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy) when configuring
differential privacy. When a table is protected by entity-level privacy, Snowflake does not allow aggregates on fields if there might be an
unbounded number of rows per entity. This means queries must meet the following requirements:

- At some point in the query, the privacy-protected table must be deduplicated on the entity key. Operations that can be used to deduplicate
  data are:

  - COUNT( DISTINCT <entity\_key\_column> )
  - GROUP BY <entity\_key\_column>
  - UNION (but not UNION ALL) when only the entity key is projected.
- If a join uses a join key other than the entity key column, that join cannot occur between the deduplication and the final SELECT clause
  with aggregation.

Note

If the data provider implemented row-level privacy, the deduplication requirement for joins is different. For more information about these
requirements, see [Uniqueness requirement](#label-diff-privacy-joins-no-duplicates).

To help illustrate the requirements for entity-level privacy, suppose you have a privacy-protected table `patients` with the entity key
column `patient_id`. You also have a non-sensitive, unprotected table `geo_lookup`. The following examples show a query that fails
followed by a re-written version that succeeds.

Example: Deduplication
:   The following query fails because it doesn’t meet the deduplication requirement. Even though the table `patients` might already be
    unique on `patient_id`, the query fails because it does not explicitly deduplicate.

    Copy code

    ```
    SELECT COUNT(*)
      FROM patients
      WHERE insurance_type = 'Commercial';
    ```

    To re-write the query so it succeeds, include a distinct count on the entity key column in order to explicitly deduplicate on the entity
    key. For example:

    Copy code

    ```
    SELECT COUNT(DISTINCT patient_id)
      FROM patients
      WHERE insurance_type = 'Commercial';
    ```

Example: Location of join
:   The following query fails even though it is using a GROUP BY clause to meet the deduplication requirement. It fails because the table is
    being joined with another table using a column that is not the entity key column.

    Copy code

    ```
    SELECT COUNT(bmi)
      FROM (SELECT patient_id, ANY_VALUE(zip_code) AS zip_code
        FROM patients
        GROUP BY patient_id) AS p
      JOIN geo_lookup AS g
        ON p.zip_code = g.zip_code
      WHERE state='CA';
    ```

    To re-write the query so it succeeds, use the GROUP BY clause *after* the join. The join cannot occur in between the deduplication and
    the SELECT clause with aggregation.

    Copy code

    ```
    SELECT COUNT(bmi)
      FROM (SELECT patient_id, ANY_VALUE(bmi) as bmi, ANY_VALUE(state) as state
          FROM patients AS p
          JOIN geo_lookup AS g
            ON p.zip_code = g.zip_code
          GROUP BY patient_id)
      WHERE state='CA';
    ```

#### Executing transaction-level queries

The deduplication requirement for entity-level differential privacy does not prevent you from executing transaction-level queries. However,
you must first group the data to the entity-level, and then count those groups.

For example, suppose you have a table `doctor_visits` and that the data provider has defined an entity key `patient_id` to implement
entity-level privacy. A transaction-level query might be: “How many doctor visits weren’t for a regular checkup?” The following is an
example of how to write this query:

Copy code

```
SELECT COUNT(num_visits)
  FROM (SELECT COUNT((visit_reason<>'Regular checkup')::INT) AS num_visits
        WHERE visit_reason IS NOT NULL
        GROUP BY patient_id)
  WHERE num_visits > 0 AND num_visits < 20;
```

- The subquery groups by `patient_id` to deduplicate the data.
- The aggregate column `num_visits` captures the number of visits per patient that were not for a regular checkup.
- The query then aggregates again on that per-patient column to get the total number of visits.
- The WHERE clause on the outer query is required in order to
  [specify a privacy domain on the data](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst).

Note

While not a requirement, a best practice when joining tables protected by entity-level differential privacy is to include the entity key
column as part of the join key (if it doesn’t semantically change the query). For more information, see
[Using entity keys in joins](#label-diff-privacy-joins-entity-keys).

## Understanding query results

Queries against a privacy-protected table don’t return the exact value of an aggregation. Differential privacy introduces
[noise](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-noisy-aggregates) into the result so it becomes an approximation of the actual value. The returned value
differs enough from the actual value to conceal whether an individual’s data is included in the aggregation. This applies to all queries
except for a query that returns the total number of rows in the privacy-protected table, for example, `SELECT COUNT(*) FROM t`.

An analyst needs to be able to determine whether the noise introduced into the result has decreased the usefulness of the query. Snowflake
uses a *noise interval* to help analysts interpret the results. A noise interval is a closed mathematical interval that, in most cases,
includes the actual value of the aggregation. There is a 95% chance that the actual result of a query falls within the noise interval.

Adding the following functions to a query allows the analyst to use the noise interval to make decisions about the utility of a query:

- [DP\_INTERVAL\_LOW](/sql-reference/functions/dp_interval_low) — Returns the lower bound of the noise interval. The actual value is most
  likely to be equal to or larger than this number.
- [DP\_INTERVAL\_HIGH](/sql-reference/functions/dp_interval_high) — Returns the upper bound of the noise interval. The actual value is most
  likely to be equal to or smaller than this number.

To use these functions, pass in the alias of an aggregated column in the main query. For example, the following query returns the count of
the `num_claims` column along with the noise interval for that aggregation:

Copy code

```
SELECT COUNT(num_claims) AS count_claims,
    DP_INTERVAL_LOW(count_claims),
    DP_INTERVAL_HIGH(count_claims)
FROM t1;
```

The output might be:

```
+----------------+----------------------------------+----------------------------------+
|  count_claims  |  dp_interval_low("count_claims") |  dp_interval_high("count_claims")|
|----------------+----------------------------------+----------------------------------+
|  50            |  35                              |    75                            |
+----------------+----------------------------------+----------------------------------+
```

In this case, the return value is a count of 50. But the analyst has also determined with 95% certainty that the actual value of the
aggregation is between 35 and 75.

Tip

For information about techniques that can potentially reduce noise in results, see

- [Narrowing a privacy domain to improve results](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domains-improve-results)
- [Using entity keys in joins](#label-diff-privacy-joins-entity-keys)

## Tracking privacy budget spending

You can use the [ESTIMATE\_REMAINING\_DP\_AGGREGATES](/sql-reference/functions/estimate_remaining_dp_aggregates) function to estimate how many more queries you can run
within the current budget window (that is, until the cumulative privacy loss is reset to 0). The estimate is based on the number of
aggregates, not queries. For example, the query `SELECT COUNT(a), COUNT(b) FROM T` contains two aggregate functions: `COUNT(a)` and
`COUNT(b)`.

When executing the ESTIMATE\_REMAINING\_DP\_AGGREGATES function, be sure to use the exact conditions you’re using to execute queries, for
example, the same user, role, and account.

If you’re running a query that uses multiple tables, you should run ESTIMATE\_REMAINING\_DP\_AGGREGATES once per table, then use the lowest
`NUMBER_OF_REMAINING_DP_AGGREGATES` value as the estimated usage cap.

The following example shows how a series of queries affect how much of the privacy budget’s limit has been spent (that is, the cumulative
privacy loss of the queries) and the estimated number of remaining aggregates.

**1. Initial check**

Let’s look at privacy budget numbers on the table `my_table`. You’ve never run any queries on this table.

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('my_table'));
```

No budget used so far:

```
+-----------------------------------+--------------+---------------+--------------+
| NUMBER_OF_REMAINING_DP_AGGREGATES | BUDGET_LIMIT | BUDGET_WINDOW | BUDGET_SPENT |
|-----------------------------------+--------------+---------------+--------------|
|                 996               |     233      |     WEEKLY    |     0.0      |
+-----------------------------------+--------------+---------------+--------------+
```

**2. Run a query**

Let’s run a query with one aggregate function and check our numbers again:

Copy code

```
SELECT COUNT(salary) FROM my_table;

-- results omitted ...

SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('my_table'));
```

Estimate of remaining aggregate calls has dropped by one and the cumulative privacy loss (budget spent) has increased.

```
+-----------------------------------+--------------+---------------+--------------+
| NUMBER_OF_REMAINING_DP_AGGREGATES | BUDGET_LIMIT | BUDGET_WINDOW | BUDGET_SPENT |
|-----------------------------------+--------------+---------------+--------------|
|                 995               |     233      |     WEEKLY    |     0.6      |
+-----------------------------------+--------------+---------------+--------------+
```

**3. Run another query with two aggregate functions**

Copy code

```
SELECT COUNT(salary), COUNT(age) FROM my_table GROUP BY STATE;

-- results omitted ...

SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('my_table'));
```

Estimated remaining queries has dropped by two. Remember, this is an estimate.

```
+-----------------------------------+--------------+---------------+--------------+
| NUMBER_OF_REMAINING_DP_AGGREGATES | BUDGET_LIMIT | BUDGET_WINDOW | BUDGET_SPENT |
|-----------------------------------+--------------+---------------+--------------|
|                 993               |     233      |     WEEKLY    |     1.8      |
+-----------------------------------+--------------+---------------+--------------+
```

**4. Rerun a query**

Let’s rerun a previous query to show that privacy budget is always charged, even on identical queries. A duplicate query incurs the same
privacy loss each time it runs (that is, it spends the same amount of privacy budget).

Copy code

```
SELECT COUNT(salary), COUNT(age) FROM T GROUP BY STATE;

-- results omitted ...

SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('my_table'));
```

Same charge for the query as before: 1.2 units of privacy loss.

```
+-----------------------------------+--------------+---------------+--------------+
| NUMBER_OF_REMAINING_DP_AGGREGATES | BUDGET_LIMIT | BUDGET_WINDOW | BUDGET_SPENT |
|-----------------------------------+--------------+---------------+--------------|
|                 991               |     233      |     WEEKLY    |     3.0      |
+-----------------------------------+--------------+---------------+--------------+
```
