# Implementing entity-level privacy with aggregation policies

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Entity-level privacy strengthens the privacy protections provided by aggregation policies. With entity-level privacy, Snowflake
can ensure that each group contains a minimum number of unique entities, not just a minimum number of rows.

The majority of tasks and considerations related to aggregation policies are the same regardless of whether you are implementing
entity-level privacy. For general information about working with aggregation policies, see [Aggregation policies](/user-guide/aggregation-policies).

## About entity-level privacy

An *entity* refers to a set of attributes that belong to a logical object (for example, a user profile or household information). These
attributes can be used to identify an entity within a dataset. Entity-level privacy is a feature of privacy-enhancing technologies (PET)
that protects the privacy of an entity that is stored in a shared dataset. It ensures that queries cannot expose sensitive attributes of an
entity, even if those attributes are found in multiple records.

To achieve entity-level privacy, Snowflake allows you to specify which columns identify an entity (an *entity key*). This
lets Snowflake identify all of the records that belong to a particular entity within a dataset. For example, if the entity key is defined
as the column `email`, then Snowflake can determine that all records where `email=joe.smith@example.com` belong to the same entity.

When you define multiple entities for a table, the aggregation policy is evaluated separately for each entity key.

The policy is applied to a query even if the key columns do not appear in the query. For example, given a policy that applies to entity key (user\_id), the query `SELECT age FROM T1 GROUP BY age;` will still apply the `min_group_size` restriction for `user_id` in each group, although `user_id` does not appear in the query.

### Aggregation policies *without* entity-level privacy

By default, aggregation policies require analysts to run queries that aggregate data rather
than retrieving individual rows, thereby achieving *row-level privacy*. However, row-level privacy does not prevent a query from
exposing attributes of an entity when those attributes are found in multiple rows (for example, in a table containing transactional data).

For example, suppose a streaming service, ActonViz, has a transactional table that contains the email address (`user_id`) and household
(`household_id`) of each viewer as they watch shows.

| user\_id | household\_id | program\_id | watch\_time | start\_time |
| --- | --- | --- | --- | --- |
| [dave\_sr@example.com](mailto:dave_sr@example.com) | 12345 | 1 | 29 | 2023-09-12 09:00 |
| [mary@bazco.com](mailto:mary@bazco.com) | 23485 | 1 | 30 | 2023-09-12 09:00 |
| [dave\_sr@example.com](mailto:dave_sr@example.com) | 12345 | 6 | 18 | 2023-09-11 13:00 |
| [joe@jupiterlink.com](mailto:joe@jupiterlink.com) | 85456 | 6 | 25 | 2023-09-15 22:00 |
| [junior@example.com](mailto:junior@example.com) | 12345 | 5 | 30 | 2023-09-13 11:00 |

Expand

Show lessSee more

ActonViz can use an aggregation policy to force the advertisers to aggregate data into groups that contain at least 2 records. This prevents
the advertisers from retrieving data from an individual record (row-level privacy). If each viewer and household only appeared once in
the table, that would be enough to protect their privacy.

However, an advertiser’s query could still learn information about both viewers and their households. A query could create a group that
consists entirely of records from household `12345` or, even worse, a group that consisted entirely of records for viewer `dave_sr`.
In both cases, the number of records in the group would meet the requirements set by ActonViz (minimum of 2 records per group).

### Aggregation policies *with* entity-level privacy

To achieve entity-level privacy, Snowflake allows you to specify one or more entity keys when assigning an aggregation policy to a table or
view. After the entity key is defined, the groups returned by a query against an aggregation-constrained table or view must contain
at least the specified number of *entities*, not a specified number of *rows*.

In the preceding example, suppose ActonViz defines `household_id` as the entity key because it uniquely identifies each household. The
privacy of each household is now enhanced. Before the change, a group could consist entirely of records where `household_id = 12345`,
but now it must contain at least two distinct values of `household_id`.

Note that the entity key is not always the same as the [primary key](/sql-reference/constraints-overview#label-constraints-supported-types) of a table. In this example,
the table might use `user_id` as the primary key because it uniquely identifies a viewer. But in this case, ActonViz wants to protect
the privacy of an entire household, which consists of multiple viewers, so they chose `household_id` as the entity key.

## About minimum group sizes

Every aggregation policy specifies a minimum group size. Without entity-level privacy, the minimum group size defines the
number of records that must be included in an aggregation group. When an entity key is specified, the minimum group size defines the minimum
number of *unique* entities that must appear in the group to allow it to appear in final results. Remember that aggregation functions such as
SUM and AVG return one group, whereas GROUP BY columns return one group per unique value in the grouped columns.

The following column-level policies do not affect how Snowflake calculates whether there are enough entities in an aggregation group:

- Projection policies are enforced after aggregation policies.
- Masking policies are enforced before aggregation policies. Any aggregation functions or policies work on masked data.

In cases where name references are used several times (for example, in JOIN or UNION operators), Snowflake enforces the minimum group size
for each name reference of each dataset separately. This applies even when the reference points to the same dataset several times.

## Enforce entity-level privacy with aggregation policies

To enforce entity-level privacy with aggregation policies, do the following:

1. When executing the CREATE AGGREGATION POLICY command to create the aggregation policy, [specify the number of entities](#label-agg-entity-privacy-create-agg) that must be included in each aggregation group.
2. [Define the entity key](#label-agg-entity-privacy-assign) when assigning the aggregation policy to a table or view.

### Specify the minimum number of entities

The syntax for creating an aggregation policy with
[CREATE AGGREGATION POLICY](/sql-reference/sql/create-aggregation-policy) does not change if you are using an entity key to achieve entity-level privacy. You
still use the MIN\_GROUP\_SIZE argument of the AGGREGATION\_CONSTRAINT function to specify a minimum group size. As soon as you
[define an entity key](#label-agg-entity-privacy-assign), the minimum group size changes from a requirement on the number
of records in a group to the number of entities in a group.

For example, the following code creates an aggregation policy that has a minimum group size of 5. As long as you define an entity key when
assigning the policy to a table, each aggregation group must contain at least 5 entities.

Copy code

```
CREATE AGGREGATION POLICY my_agg_policy
  AS () RETURNS AGGREGATION_CONSTRAINT ->
  AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);
```

For complete details about creating aggregation policies, including an example of a conditional aggregation policy that enforces different
restrictions under different circumstances, see [Create an aggregation policy](/user-guide/aggregation-policies#label-aggregation-policy-create).

### Define an entity key

You define an entity key for a table when you assign the aggregation policy to the table or view. You can define the entity key when
[creating a new table or view](#label-agg-entity-privacy-assign-new), or when
[updating an existing table or view](#label-agg-entity-privacy-assign-existing).

#### Define an entity key for existing tables and views

When executing the ALTER TABLE … SET AGGREGATION POLICY command or the ALTER VIEW … SET AGGREGATION POLICY command to assign the
aggregation policy, use the ENTITY KEY clause to specify which columns in the table or view contain the identifying attributes of an
entity (that is, the entity key).

For example, to create an entity key while assigning an aggregation policy `my_agg_policy` to a table `viewership_log`, execute:

Copy code

```
ALTER TABLE viewership_log
  SET AGGREGATION POLICY my_agg_policy
  ENTITY KEY (first_name,last_name);
```

Because columns `first_name` and `last_name` are the entity key, the aggregation policy can determine that all rows where
`first_name = joe` and `last_name = peterbilt` belong to the same entity.

##### Define multiple entity keys for existing tables and views

To define multiple entity keys for an existing table, you can either add new keys in multiple calls, or add multiple keys in a single call.
Defining a key on a table is additive; it does not overwrite or drop previously defined keys.

**Add two entity keys in two calls.** The first key comprises two columns.

Copy code

```
ALTER TABLE transactions ADD AGGREGATION POLICY ap ENTITY KEY (user_id, user_email);
ALTER TABLE transactions ADD AGGREGATION POLICY ap ENTITY KEY (vendor_id);
```

**Add two entity keys in one call**

Copy code

```
ALTER TABLE transactions ADD AGGREGATION POLICY ap ENTITY KEY (user_id) ENTITY KEY (vendor_id);
```

#### Define an entity key for new tables and views

When executing the CREATE TABLE … WITH AGGREGATION POLICY command or the CREATE VIEW … WITH AGGREGATION POLICY command to assign the
aggregation policy, use the ENTITY KEY clause to specify which columns in the table or view contain the identifying attributes of an entity.

For example, to create a new table `t1` while assigning an aggregation policy and defining an entity key, execute:

Copy code

```
CREATE TABLE t1
  WITH AGGREGATION POLICY my_agg_policy
  ENTITY KEY (first_name,last_name);
```

Because columns `first_name` and `last_name` are the entity key, the aggregation policy can determine that all rows where
`first_name = joe` and `last_name = peterbilt` belong to the same entity.

## Deferred aggregation policies

If a query has subqueries, Snowflake will attempt to enforce any entity aggregation policies on the innermost query. If that query has a
GROUP BY clause, and the GROUP BY columns match the entity key for an aggregation policy, that aggregation policy will not be applied to
that subquery but to the parent query of that subquery. This deferment continues up the chain until either a query is reached that doesn’t
have a set of GROUP BY columns that match the entity key of the policy, or until the top-level query is reached; in either case, the
aggregation policy will be applied to that query. An aggregation policy is applied only once in a query chain.

For example, suppose you have an aggregation policy `my_agg_policy` with entity key `(name, zipcode)`. In the following pseudo query, the inner query has a GROUP BY set that matches the entity key for `my_agg_policy`, and so the policy is deferred to its parent. The policy is applied at the parent because it is a top-level query, even though the GROUP BY columns also match the policy columns.

Copy code

```
SELECT age, name, zipcode FROM(                        -- Outermost query: my_agg_policy enforced.
  SELECT name, zipcode FROM T GROUP BY name, zipcode   -- Matches my_agg_policy entity key: my_agg_policy deferred
)
  GROUP BY age, name, zipcode;
```

Note that GROUP BY columns can be a superset of the entity key columns to trigger a deferment, and policies are deferred only when GROUP BY columns are matched; aggregation functions do not trigger deferment.

Each aggregation policy is applied separately to all query blocks in the query. A query comprised of multiple blocks through a [set operator](/sql-reference/operators-query) (such as UNION) will evaluate the aggregation policies separately for each query block.

Aggregation deferment has some useful effects, demonstrated in the following example.

### Deferment example

Imagine you want to aggregate users into two buckets, “low spenders” and “high spenders”, for entities defined as `(zipcode, email)`.
Deferment allows this to work as shown in the following example. Without deferment, the inner query would return NULL, because each group
would consist of one `(zipcode, email)` entity, which would be suppressed when *min\_group\_size* is set to any value greater than 1

Copy code

```
WITH bucketed AS (
  SELECT
    CASE
      WHEN SUM(transaction_amount) BETWEEN 0 AND 100 THEN 'low'
      WHEN SUM(transaction_amount) BETWEEN 101 AND 100000 THEN 'high'
    END AS transaction_bucket,
    zipcode,               -- zipcode and email need not appear in the select list, but this lets us compute entity_count below
    email
  FROM my_transactions
  GROUP BY zipcode, email  -- This would not work if it was only GROUP BY zipcode, since the entity key is (zipcode, email)
)
SELECT
  transaction_bucket,
  COUNT(DISTINCT zipcode, email) AS entity_count
FROM
  bucketed
GROUP BY transaction_bucket;
```

### Multiple policy deferment

If a table has multiple aggregation policies, each aggregation policy is evaluated, and possibly deferred, independently. If you have multiple aggregation policies on a table, design your queries carefully, as you can encounter unexpected results when different policies are applied at different query levels.

For example, here is a problem you might encounter if you try a nested query to bucket your users into high and low spender categories on a table with two separate aggregation policies:

**Table T:**

> ```
> user_id, vendor_id, zipcode, email,         transaction_amount
>    1     1001       90000    a@example.com        100
>    1     1001       90000    a@example.com         50
>    2     2001       90001    b@example.com         12
>    2     2001       90001    b@example.com          5
>    3     3001       90002    c@example.com         40
> ```

**Aggregation policies:**

> - `user_policy`: `min_group_size` = 3, entity key = `(user_id)`
> - `vendor_policy`: `min_group_size` = 2, entity key = `(vendor_id)`

**Query to bucket users as high or low spenders:**

> Copy code
>
> ```
> WITH amounts AS (
>   SELECT
>     user_id,
>     IFF(SUM(transaction_amount) > 50, 'high', 'low') AS bucket
>   FROM T
>   GROUP BY user_id -- user_policy is deferred, but vendor_policy is enforced
> )
> SELECT COUNT(*) FROM amounts GROUP BY bucket
> ```

**Unexpected results:**

In the inner query, `vendor_policy` is enforced. Each row is grouped by `user_id`, which has only one corresponding `vendor_id`, which violates the `vendor_policy` minimum group size, and the inner query will return NULL, even though three distinct customers belong in the “high” bucket.

## Removing entity key constraints

**To remove an aggregation policy for a single entity key:**

Copy code

```
-- Drop agg policy ap associated with entity key user_id
ALTER TABLE transactions DROP AGGREGATION POLICY ap ENTITY KEY (user_id)
```

**To remove an aggregation policy for multiple entity keys,** remove each policy separately:

Copy code

```
-- Drop the agg policies associated with two separate keys
ALTER TABLE transactions DROP AGGREGATION POLICY ap ENTITY KEY (user_id)
ALTER TABLE transactions DROP AGGREGATION POLICY ap ENTITY KEY (vendor_id)
```

**To remove an aggregation policy together with all its entities,** omit ENTITY KEY from the DROP statement:

Copy code

```
-- Drop agg policy ap from the table entirely
ALTER TABLE transactions DROP AGGREGATION POLICY ap
```

## Restrictions

The following restrictions apply when working with tables that have multiple entity keys or aggregation policies defined:

- An entity key may be associated with at most one policy. Attempting to assign another policy for an entity key that is already mapped to a policy will result in an error.
- A policy cannot be used for both row-level privacy and entity-level privacy.
- At most one policy may be used for row-level privacy. Attempting to assign another policy as the row-level aggregation policy will result in an error.

## Querying an aggregation-constrained table

The requirements for querying an aggregation-constrained table that has an entity key is the same as querying a table without one. For
information about what types of queries conform to these requirements, see [Query requirements](/user-guide/aggregation-policies#label-aggregation-policy-query-reqs).
