# Join policies

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A join policy is a schema-level object that controls the requirement to join a table when it is queried. When a join
policy is applied to a table, queries against that table either require or do not require a join. When joins
are required, they can be restricted to certain joining columns.

You can use this kind of policy to enforce joins for queries on certain tables and views, as a means of finding common information across shared tables. A table or view with a join policy assigned to it is said to be *protected* or *join-constrained*.

## Overview

A core feature of Snowflake is the ability to share data sets with other entities. Join policies allow a provider (data owner) to exercise control
over what can be done with their data even after it is shared with a consumer. Specifically, the provider can require a consumer of a table to join
the data to another table rather than retrieve records from a single table. This requirement facilitates data sharing among semi-trusted partners
that have common data sets. The selection of data from a single table is not generally useful; meaningful data is available when one owner’s table is
joined with a similar table owned by a consumer or partner.

After the join policy is applied to a table or view, a query must:

- Join the table or view to another table or view.
- Specify a supported [join type](/sql-reference/constructs/join).
- Specify a join condition with allowed joining columns.

At least one table or view participating in the join must be unprotected. This restriction prevents attackers from circumventing the join policy by joining two protected tables that are shared by the same organization and have matching key values.

While join policies control access to joined tables, they do not guarantee that a malicious actor could not use carefully constructed queries to obtain
sensitive data from a join-constrained table. With enough query attempts, a malicious actor could potentially work around the join requirements. Join
policies are best suited for use with partners and customers with whom you have an existing level of trust. In addition, providers should be vigilant
about potential misuses of their data (for example, reviewing the access history for their listings).

## Creating and implementing join policies

To create and implement a join policy:

1. Create the policy itself.
2. Apply the policy to a new or existing table or view.
3. Run some queries to verify the expected behavior of the policy.

These steps are explained in the following sections.

You might also want to modify an existing policy and verify that the expected behavior changes.

At any time, you can see the join policies in your account by using the [SHOW JOIN POLICIES](/sql-reference/sql/show-join-policies) and [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy) commands. To see the actual definition of a policy, query the [JOIN\_POLICIES](/sql-reference/account-usage/join_policies) view. To see which tables and views are attached to policies, query the [POLICY\_REFERENCES](/sql-reference/functions/policy_references) Information Schema table function.

For information about managing policies, including setup of a custom policy administration role, see [Managing join policies](#label-join-policy-manage).

### Creating a join policy

The simplest form of join policy requires users to always join a table or view to some other table or view. In other words,
queries against a single table, without a join specification, are disallowed. For example, create a policy named `jp1`:

Copy code

```
CREATE JOIN POLICY jp1
  AS () RETURNS JOIN_CONSTRAINT -> JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE);
```

For the complete syntax of this command and its JOIN\_CONSTRAINT function, see [CREATE JOIN POLICY](/sql-reference/sql/create-join-policy).

### Applying a join policy to a table or view

Having created a join policy, you implement it by assigning it to a specific table or view:

- Use an ALTER TABLE or ALTER VIEW command if the table or view already exists.
- Use a CREATE TABLE or CREATE VIEW command for a new table or view.

In either case, specify the JOIN POLICY parameter to identify the join policy itself. For example, the following
command assigns the policy `jp` to the table `join_table`:

Copy code

```
CREATE OR REPLACE TABLE join_table (
  col1 INT,
  col2 VARCHAR,
  col3 NUMBER )
  JOIN POLICY jp1;
```

Optionally, you can also specify the ALLOWED JOIN KEYS parameter if you want to restrict joins to use specific joining columns. See [Restricting joins on specific columns](#label-join-policy-allowed-keys-test).

A table or view can have only one join policy assigned to it at any given time. See [Replacing a join policy](#label-join-policy-replace).

### Testing the join policy by running some queries

The following queries demonstrate the expected behavior when the `jp1` policy is in effect for the table `join_table`. This table does not
need to be loaded; an empty table is sufficient to demonstrate the expected behavior.

A query without a join returns an expected error:

Copy code

```
SELECT * FROM join_table;
```

```
506037 (23001): SQL compilation error: Join Policy violation, please contact the policy admin for details
```

A query with an explicit inner join on `col1` returns results:

Copy code

```
SELECT * FROM join_table jt1 INNER JOIN join_table_2 jt2 ON jt1.col1=jt2.col1;
```

```
+------+------+------+------+------+------+
| COL1 | COL2 | COL3 | COL1 | COL2 | COL3 |
|------+------+------+------+------+------|
+------+------+------+------+------+------+
```

A query with an explicit inner join on `col2` also returns results:

Copy code

```
SELECT * FROM join_table jt1 INNER JOIN join_table_2 jt2 ON jt1.col2=jt2.col2;
```

```
+------+------+------+------+------+------+
| COL1 | COL2 | COL3 | COL1 | COL2 | COL3 |
|------+------+------+------+------+------|
+------+------+------+------+------+------+
```

### Restricting joins on specific columns

To further test join policy behavior, detach (unset) the policy from the table, drop and recreate the join policy,
then recreate `join_table` with DDL that includes the ALLOWED JOIN KEYS parameter.

Copy code

```
ALTER TABLE join_table UNSET JOIN POLICY;

DROP JOIN POLICY jp1;

CREATE JOIN POLICY jp1
  AS () RETURNS JOIN_CONSTRAINT -> JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE);

CREATE OR REPLACE TABLE join_table (
  col1 INT,
  col2 VARCHAR,
  col3 NUMBER )
  JOIN POLICY jp1 ALLOWED JOIN KEYS (col1);
```

Now try one of the previous queries again, with `col2` as the joining column. The query fails
because `col2` is not an allowed join key.

Copy code

```
SELECT * FROM join_table jt1 INNER JOIN join_table_2 jt2 ON jt1.col2=jt2.col2;
```

```
506038 (23001): SQL compilation error: Join Policy violation, invalid join condition with reason: Disallowed join key used.
```

The same query with `jt1.col1=jt2.col1` as the join condition would succeed. A natural join of these two tables would fail
because it would attempt to join over `col1` *and* `col2`.

### Showing and describing join policies

You can use [SHOW JOIN POLICIES](/sql-reference/sql/show-join-policies) and [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy) commands to get basic information about existing join policies in your account. To return more detailed information about join policies, see [Monitoring join policies](#label-monitor-join-policies-vew).

Copy code

```
SHOW JOIN POLICIES;
```

```
+-------------------------------+------+---------------+----------------+-------------+--------------+---------+-----------------+---------+
| created_on                    | name | database_name | schema_name    | kind        | owner        | comment | owner_role_type | options |
|-------------------------------+------+---------------+----------------+-------------+--------------+---------+-----------------+---------|
| 2024-12-04 15:15:49.591 -0800 | JP1  | POLICY1_DB    | POLICY1_SCHEMA | JOIN_POLICY | POLICY1_ROLE |         | ROLE            |         |
+-------------------------------+------+---------------+----------------+-------------+--------------+---------+-----------------+---------+
```

Copy code

```
DESCRIBE JOIN POLICY jp1;
```

```
+------+-----------+-----------------+----------------------------------------+
| name | signature | return_type     | body                                   |
|------+-----------+-----------------+----------------------------------------|
| JP1  | ()        | JOIN_CONSTRAINT | JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE) |
+------+-----------+-----------------+----------------------------------------+
```

### Creating and applying conditional join policies

Policy administrators can define the SQL expression of a join policy so different queries have different restrictions based on
factors such as the role of the user executing the query. This strategy can allow one user to query a table without restriction while requiring others to use joins.

For example, the following join policy gives users with the roles `ACCOUNTADMIN`, `FINANCE_ROLE`, or `HR_ROLE` unrestricted access to a table while requiring all other users to specify a join.

> Copy code
>
> ```
> CREATE JOIN POLICY my_join_policy
>   AS () RETURNS JOIN_CONSTRAINT ->
>     CASE
>       WHEN CURRENT_ROLE() = 'ACCOUNTADMIN'
>           OR CURRENT_ROLE() = 'FINANCE_ROLE'
>           OR CURRENT_ROLE() = 'HR_ROLE'
>         THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE)
>       ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
>     END;
> ```
>
> Tip
>
> You can use the following strategies when using context functions such as [CURRENT\_ROLE](/sql-reference/functions/current_role) in a conditional
> policy:
>
> - Context functions return strings, so comparisons using them are case-sensitive. You can use
>   [LOWER](/sql-reference/functions/lower) to convert strings to all lowercase if you’d like to do a case-insensitive comparison.
> - The [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function helps you evaluate whether a policy body is returning the correct value
>   when a context function or [SYS\_CONTEXT](/sql-reference/functions/sys_context) property returns a certain value. The
>   POLICY\_CONTEXT function simulates query results based upon a specified value of one or more context functions or SYS\_CONTEXT
>   namespace properties, such as activated roles and agent types.

When an agent is active in the execution context, you can use [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) in a join
policy to require a join even when the user’s role would otherwise allow queries without a join. When no agent is active, the ACCOUNTADMIN
role can query without a join:

> Copy code
>
> ```
> CREATE OR REPLACE JOIN POLICY join_when_agent AS ()
>   RETURNS JOIN_CONSTRAINT ->
>   CASE
>     WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE
>       THEN JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
>     WHEN CURRENT_ROLE() = 'ACCOUNTADMIN'
>       THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE)
>     ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
>   END;
> ```

## Join query requirements

Queries against a join-constrained table or view must conform to the following requirements in order
for a join policy to take effect:

Supported [join](/sql-reference/constructs/join) types
:   The following explicit join types are supported for join-constrained tables:

    - INNER JOIN (with the optional INNER keyword; JOIN is required)
    - LEFT OUTER JOIN and RIGHT OUTER JOIN, where the join-constrained table is the “opposite” table. If the
      join-constrained table is the first or “left” table, the outer join must be a RIGHT OUTER JOIN. If the
      join-constrained table is the second or “right” table, the outer join must be a LEFT OUTER JOIN.
    - NATURAL JOIN (inner join over columns with common names)

    Inner and outer joins must be specified explicitly within the FROM clause, with ON or USING join conditions. These joins can’t be specified in the WHERE clause.

Unsupported join types
:   The following join types are not supported:

    - FULL OUTER JOIN
    - ASOF JOIN
    - LATERAL joins
    - Implicit joins in the WHERE clause
    - Cross-joins (Cartesian product)

Joins with multiple join-constrained tables
:   If both (or all) tables in a join query have been assigned a join policy, the query fails with an error. In a join of two tables, only one can be join-constrained.

[UNION, INTERSECT, and EXCEPT](/sql-reference/operators-query)

> - UNION and UNION ALL set operations are not supported in queries against join-constrained tables.
> - INTERSECT set operations are supported because they are semantically equivalent to inner joins.
> - MINUS and EXCEPT set operations are supported only when the join-constrained table is on the filtered side of the operator (that is, in the
>   second query block).

Data type conversions
:   A query that includes a data type conversion function in the SELECT statement must use the TRY version of the function. For example, the
    TRY\_CAST function is allowed, but the CAST function is prohibited. The following data type conversion functions are allowed for numeric
    types:

    - [TRY\_CAST](/sql-reference/functions/try_cast)
    - [TRY\_TO\_DECFLOAT](/sql-reference/functions/try_to_decfloat)
    - [TRY\_TO\_DECIMAL](/sql-reference/functions/try_to_decimal)
    - [TRY\_TO\_DOUBLE](/sql-reference/functions/try_to_double)
    - [TRY\_TO\_NUMBER](/sql-reference/functions/try_to_decimal)
    - [TRY\_TO\_NUMERIC](/sql-reference/functions/try_to_decimal)

## Expected errors for queries against join-constrained tables

The following examples show some of the cases where queries are expected to fail because a join policy is applied to a table or view. For background information, see [Join query requirements](#label-join-policy-query-reqs). The tables in these queries do
not contain any rows, so queries return either an empty result (success) or an error (failure).

### Queries without joins fail

When a join policy is assigned to `join_table`, simple queries without joins fail. The following query returns an error.

Copy code

```
SELECT col1, col2 FROM join_table;
```

### WHERE clause joins are prohibited

If `join_table` (alias `jt1`) is a join-constrained table, the following WHERE clause join returns an error:

Copy code

```
SELECT *
  FROM join_table jt1, join_table_2 jt2
  WHERE jt1.col1=jt2.col1;
```

### Left and right outer joins depend on the order of tables

The following examples show the expected behavior with outer joins, where `join_table` (alias `jt1`) is the join-constrained table. The first query returns an error.

Copy code

```
SELECT * FROM join_table jt1
  LEFT OUTER JOIN join_table_2 jt2 ON jt1.col1=jt2.col1;
```

The second query returns results.

Copy code

```
SELECT * FROM join_table jt1
  RIGHT OUTER JOIN join_table_2 jt2 ON jt1.col1=jt2.col1;
```

### Joining two join-constrained tables is not supported

If `join_table` and `join_table_2` both have a join policy assigned, the following join query returns an error:

Copy code

```
SELECT * FROM join_table jt1 JOIN join_table_2 jt2 ON jt1.col1=jt2.col1;
```

### UNION set operations are disallowed, but INTERSECT operations are allowed

In these examples, `join_table` has a join policy but `join_table_3` does not. The UNION query fails, but a similar INTERSECT query succeeds.

Copy code

```
SELECT * FROM JOIN_TABLE
UNION
SELECT * FROM JOIN_TABLE_3;
```

Copy code

```
SELECT * FROM JOIN_TABLE
INTERSECT
SELECT * FROM JOIN_TABLE_3;
```

### EXCEPT behavior depends on the order of query blocks

The EXCEPT behavior depends on the order of query blocks. Note that the
first query selects from the join-constrained table first and returns an error.

Copy code

```
SELECT * FROM JOIN_TABLE
EXCEPT
SELECT * FROM JOIN_TABLE_3;
```

The second query succeeds.

Copy code

```
SELECT * FROM JOIN_TABLE_3
EXCEPT
SELECT * FROM JOIN_TABLE;
```

### A view on a join-constrained table is also protected

Assume that `join_table` has been assigned join policy `jp1`. Create a view on the table:

Copy code

```
CREATE VIEW join_table_view AS
  SELECT * FROM join_table;
```

Now query the view without specifying a join:

Copy code

```
SELECT * FROM join_table_view;
```

The query fails because it violates the policy on `join_table`. The query on the view must contain a join. For
more information about join policy behavior with views, see [Views and materialized views](#label-views-and-materialized-views).

## Managing join policies

You can modify, replace, detach, describe, and monitor join policies. The following sections cover these management
tasks.

### Modifying a join policy

You can use the [ALTER JOIN POLICY](/sql-reference/sql/alter-join-policy) command to modify join policy rules. You can also
rename a policy or change its comment.

Before modifying a join policy, run the [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy) command or
[GET\_DDL](/sql-reference/functions/get_ddl) function to review the policy’s current SQL expression.

For example, run the following command to update the SQL expression of the join policy `jp3` so that joins are not
required:

Copy code

```
ALTER JOIN POLICY jp3 SET BODY -> JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE);
```

### Replacing a join policy

The recommended method to replace a join policy is to use the `FORCE` parameter in an ALTER TABLE statement,
which detaches the existing policy and assigns a new one in a single command. This approach allows you to atomically replace the old policy, leaving no gap in protection.

For example, to assign a new join policy to a table that is already join-constrained:

Copy code

```
ALTER TABLE join_table SET JOIN POLICY jp2 FORCE;
```

You can also detach the policy from a table or view in one statement (using UNSET JOIN POLICY), then set a new policy
in a different statement (using SET JOIN POLICY). If you choose this method, the table is not protected by a join policy in the interim between the two operations. A query could potentially access sensitive data during this time.

### Detaching a join policy

Use the UNSET JOIN POLICY clause of an ALTER TABLE or ALTER VIEW command to detach a join policy from a table or view. The name of the policy is not required because an object can’t have more than one policy. For example:

Copy code

```
ALTER VIEW join_view UNSET JOIN POLICY;
```

### Monitoring join policies

You can monitor join policy usage in the following ways:

- Query the [JOIN\_POLICIES](/sql-reference/account-usage/join_policies) view in the Account Usage schema of the
  shared SNOWFLAKE database. This view is a *catalog* for all join policies in your Snowflake account.
- Query the [POLICY\_REFERENCES](/sql-reference/functions/policy_references) Information Schema table function to identify join
  policy references and find out which tables and views currently have policies applied to them.

#### Getting information about join policies

To get information about existing join policies, query the [JOIN\_POLICIES](/sql-reference/account-usage/join_policies) view in the Account Usage schema of the shared SNOWFLAKE database. This view is a *catalog* for all join policies in your Snowflake account. For example, you can return the policy body for a specific join policy:

Copy code

```
SELECT policy_name, policy_body, created
  FROM SNOWFLAKE.ACCOUNT_USAGE.JOIN_POLICIES
  WHERE policy_name='JP2' AND created LIKE '2024-11-26%';
```

```
+-------------+----------------------------------------------------------+-------------------------------+
| POLICY_NAME | POLICY_BODY                                              | CREATED                       |
|-------------+----------------------------------------------------------+-------------------------------|
| JP2         | CASE                                                     | 2024-11-26 11:22:54.848 -0800 |
|             |           WHEN CURRENT_ROLE() = 'ACCOUNTADMIN'           |                               |
|             |             THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE) |                               |
|             |           ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)    |                               |
|             |         END                                              |                               |
+-------------+----------------------------------------------------------+-------------------------------+
```

#### Getting information about tables and views attached to join policies

The [POLICY\_REFERENCES](/sql-reference/functions/policy_references) Information Schema table function returns information about tables
and views attached to existing join policies. You can use two different syntax options:

- Return a row for each object (table or view) that has the specified join policy set:

  Copy code

  ```
  USE DATABASE my_db;
  USE SCHEMA INFORMATION_SCHEMA;
  SELECT
   policy_name,
   policy_kind,
   ref_entity_name,
   ref_entity_domain,
   ref_column_name,
   ref_arg_column_names,
   policy_status
    FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(policy_name => 'my_db.my_schema.jp1'));
  ```

- Return information about the policy that is assigned to `join_table`:

  Copy code

  ```
  USE DATABASE my_db;
  USE SCHEMA INFORMATION_SCHEMA;
  SELECT
   policy_name,
   policy_kind,
   ref_entity_name,
   ref_entity_domain,
   ref_column_name,
   ref_arg_column_names,
   policy_status
    FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(ref_entity_name => 'my_db.my_schema.join_table', ref_entity_domain => 'table'));
  ```

  ```
  +-------------+-------------+-----------------+-------------------+-----------------+----------------------+---------------+
  | POLICY_NAME | POLICY_KIND | REF_ENTITY_NAME | REF_ENTITY_DOMAIN | REF_COLUMN_NAME | REF_ARG_COLUMN_NAMES | POLICY_STATUS |
  |-------------+-------------+-----------------+-------------------+-----------------+----------------------+---------------|
  | JP1         | JOIN_POLICY | JOIN_TABLE      | TABLE             | NULL            | [ "COL1" ]           | ACTIVE        |
  +-------------+-------------+-----------------+-------------------+-----------------+----------------------+---------------+
  ```

### Best practices for policy administration

Creating a join policy and assigning the policy to a table requires the same general procedure as creating and assigning
other policies, such as masking, projection, and aggregation policies:

1. If you are using a centralized management approach, create a custom role (such as `join_policy_admin`) to manage the policy. Alternatively, you can use an existing role.
2. Grant this role the privileges to create and assign a join policy.
3. Create the join policy.
4. Create or alter a table to assign the policy to the table and to allow joining columns (ALLOWED JOIN KEYS).
5. Test some join and non-join queries on the table.

Successful queries against the table must join its data to another table or view and must join on the allowed columns.

Access control administrator tasks
:   1. Create a custom role to manage the join policy. You could also re-use an existing role.

       Copy code

       ```
       USE ROLE USERADMIN;

       CREATE ROLE join_policy_admin;
       ```
    2. Grant the `join_policy_admin` custom role the privileges to create a join policy in a schema and assign the policy
       to a table or view in the Snowflake account.

       This step assumes the join policy will be stored in a database and schema named `privacy.join_policies` and that this database and
       schema already exist:

       Copy code

       ```
       GRANT USAGE ON DATABASE privacy TO ROLE join_policy_admin;
       GRANT USAGE ON SCHEMA privacy.join_policies TO ROLE join_policy_admin;

       GRANT CREATE JOIN POLICY
         ON SCHEMA privacy.join_policies TO ROLE join_policy_admin;

       GRANT APPLY JOIN POLICY ON ACCOUNT TO ROLE join_policy_admin;
       ```

       The `join_policy_admin` role can now be assigned to one or more users.

       For information about the privileges needed to work with join policies, refer to [Managing join policies](#label-join-policy-manage)
       (in this topic).

Join policy administrator tasks
:   - Create a join policy:

      Copy code

      ```
      USE ROLE join_policy_admin;
      USE SCHEMA privacy.join_policies;

      CREATE OR REPLACE JOIN POLICY jp1
        AS () RETURNS JOIN_CONSTRAINT -> JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE);
      ```

## Interaction of join policies with other Snowflake features

The following sections summarize how join policies interact with other Snowflake features and services.

### Other policies

This section describes how a join policy interacts with other policies, including
[masking policies](/user-guide/security-column-intro),
[row access policies](/user-guide/security-row-intro), [aggregation policies](/user-guide/aggregation-policies),
and [projection policies](/user-guide/projection-policies).

You can attach other policies to a join-constrained table. A successful query against the table must meet the requirements of all
policies.

If a row access policy is assigned to a join-constrained table, a row excluded from the query results based on the row
access policy is not included when calculating the results of the join.

The body of a masking policy, row access policy, aggregation policy, or projection policy cannot reference a join-constrained table, including its
columns.

### Views and materialized views

You can assign a join policy to both views and materialized views. When a join policy is applied to a view, the underlying
table does not become join-constrained. This base table can still be queried without restriction.

Whether you can create a view from a join-constrained table depends on the type of view:

> - You can create a regular view from one or more join-constrained tables; however, queries against that view must join data in
>   a way that meets the restrictions of those base tables. You cannot circumvent a join policy on a protected table by creating a view on the table. The policy for the table is respected and enforced for queries against the view. For an example, see [A view on a join-constrained table is also protected](#label-join-policy-on-view).
> - You cannot create a materialized view based on a join-constrained table or view, nor can you assign a join policy to a
>   table or view upon which a materialized view is based.

### Cloned objects

The following approach helps to safeguard data from users with the SELECT privilege on a cloned table or view that is stored in the cloned
database or schema:

- Cloning an individual join policy object is not supported.
- Cloning a database results in the cloning of all join policies within the database.
- Cloning a schema results in the cloning of all join policies within the schema.
- A cloned table maps to the same join policies as the source table.
  - When a table is cloned in the context of its parent schema being cloned, if the source table has a reference to a join policy in the
    same parent schema (that is, a local reference), the cloned table will have a reference to the cloned join policy.
  - If the source table refers to a join policy in a different schema (that is, a foreign reference), the cloned table retains the
    foreign reference.

For more information, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

### Replication

Join policies and their assignments can be replicated using database replication and replication groups.

For [database replication](/user-guide/database-replication-considerations), the replication operation fails if either of the
following conditions is true:

- The primary database is in an Enterprise (or higher) account and contains a policy but one or more of the accounts approved for
  replication are on lower editions.
- A table or view contained in the primary database has a [dangling reference](/user-guide/database-replication-considerations#label-database-replication-dangling-references) to a policy in another database.

The dangling reference behavior for database replication can be avoided when replicating multiple databases in a
[replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

## Privileges and commands

The following subsections provide information to help manage join policies.

### Join policy privileges

Snowflake supports the following privileges on the join policy object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Usage |
| --- | --- |
| APPLY | Enables the set and unset operations for a join policy on a table. |
| OWNERSHIP | Transfers ownership of the join policy, which grants full control over the policy. Required to alter most properties of a join policy. |

Expand

Show lessSee more

For information, see [Summary of DDL commands, operations, and privileges](#label-join-policy-ddl-privilege-summary).

### Join policy DDL reference

Snowflake supports the following DDL commands to create and manage join policies.

- [CREATE JOIN POLICY](/sql-reference/sql/create-join-policy)
- [ALTER JOIN POLICY](/sql-reference/sql/alter-join-policy)
- [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy)
- [DROP JOIN POLICY](/sql-reference/sql/drop-join-policy)
- [SHOW JOIN POLICIES](/sql-reference/sql/show-join-policies)

### Summary of DDL commands, operations, and privileges

The following table summarizes the relationship between join policy privileges and DDL operations.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Operation | Privilege required |
| --- | --- |
| Create join policy. | A role with the CREATE JOIN POLICY privilege in the same schema. |
| Alter join policy. | The role with the OWNERSHIP privilege on the join policy. |
| Describe join policy | One of the following:   - A role with the global APPLY JOIN POLICY privilege. - A role with the OWNERSHIP privilege on the join policy. - A role with the APPLY privilege on the join policy. |
| Drop join policy. | A role with the OWNERSHIP privilege on the join policy. |
| Show join policies. | One of the following:   - A role with the USAGE privilege on the schema in which the join policy exists. - A role with the APPLY JOIN POLICY on the account. |
| Set or unset a join policy on a table. | One of the following:   - A role with the APPLY JOIN POLICY privilege on the account. - A role with the APPLY privilege on the join policy and the OWNERSHIP privilege on the table or view. |

Expand

Show lessSee more

Snowflake supports different permissions to create and set a join policy on an object.

1. For a centralized policy management approach in which the `join_policy_admin` custom role creates and sets
   join policies on all tables, the following permissions are necessary:

   Copy code

   ```
   USE ROLE securityadmin;
   GRANT USAGE ON DATABASE mydb TO ROLE join_policy_admin;
   GRANT USAGE ON SCHEMA mydb.schema TO ROLE join_policy_admin;
   GRANT CREATE JOIN POLICY ON SCHEMA mydb.schema TO ROLE join_policy_admin;
   GRANT APPLY ON JOIN POLICY ON ACCOUNT TO ROLE join_policy_admin;
   ```
2. In a hybrid management approach, a single role has the CREATE JOIN POLICY privilege to ensure join policies are named
   consistently and individual teams or roles have the APPLY privilege for a specific join policy.

   For example, the custom role `finance_role` can be granted the permission to set the join policy `cost_center` on tables
   and views the role owns (that is, the role has the OWNERSHIP privilege on the table or view):

   Copy code

   ```
   USE ROLE securityadmin;
   GRANT CREATE JOIN POLICY ON SCHEMA mydb.schema TO ROLE join_policy_admin;
   GRANT APPLY ON JOIN POLICY cost_center TO ROLE finance_role;
   ```
