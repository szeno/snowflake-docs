# Using privacy policies for differential privacy

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes how a data provider uses privacy policies to implement
[differential privacy](/user-guide/diff-privacy/differential-privacy-overview).

## About privacy policies

With differential privacy, Snowflake must check each query to determine whether it will exceed the
[privacy budget](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-loss-budgets) associated with the user executing the query. Privacy policies make that possible.
A data provider creates a privacy policy that associates users with privacy budgets, and then assigns that policy to tables and views to
make them privacy-protected.

When an analyst executes a query against a table with a privacy policy, Snowflake evaluates the body of the policy and does one of the
following:

- If the policy associates the user with a privacy budget, Snowflake makes sure that the
  [privacy loss](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-loss-budgets) incurred by the query does not exceed that privacy budget. If the query is executed
  successfully, Snowflake adds the privacy loss incurred by the query to the cumulative privacy loss for the user so that subsequent queries
  don’t exceed the privacy budget.
- If the policy indicates that the user can query the table without restriction, then the results don’t contain
  [noise](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-noisy-aggregates), and Snowflake does not track the privacy loss incurred by the query.

### Privacy policy best practices

You can create a single privacy policy to protect a single entity, and then assign the privacy policy to all tables and views that contain
information for that entity. This groups all privacy budgets for that entity under one privacy policy. You don’t need to create separate
privacy policies for every table and view.

## Working with privacy policies

Implementing differential privacy for a schema is a three-step process:

1. [Create a privacy policy](#label-diff-privacy-admin-create) that associates privacy budgets with users based on conditions like
   name, role, or account.
2. [Assign that privacy policy](#label-diff-privacy-admin-assign) to a table or view to ensure that a query or set of queries against
   the data don’t exceed the privacy budget associated with the user who is executing the query.
3. Grant SELECT privileges on the privacy-protected data. Don’t grant privileges before assigning a privacy policy to the table or view
   because the analyst would have full access to the data.

As you manage your differential privacy environment, you can also:

- [Modify an existing privacy policy](#label-diff-privacy-admin-modify).
- [Replace a privacy policy](#label-diff-privacy-admin-replace) that is currently assigned to a table or view with another policy.
- [Detach a privacy policy](#label-diff-privacy-admin-detach) from a table or view.

### Create a privacy policy

The most basic syntax for creating a new privacy policy is:

Copy code

```
CREATE PRIVACY POLICY  <name>
  AS ( ) RETURNS PRIVACY_BUDGET -> <body>
```

Where:

- `name` is the name of the privacy policy.
- `AS ( ) RETURNS PRIVACY_BUDGET` is the signature and return type of the policy. The signature doesn’t accept any arguments
  and the return type is PRIVACY\_BUDGET, which is an internal data type. All privacy policies have the same signature and return
  type.
- `body` is a SQL expression that determines whether the privacy policy returns a privacy budget, and if it does, which one.

  The SQL expression of the body calls two functions to control the return value of the policy:

  `NO_PRIVACY_POLICY`
  :   Use the body’s expression to call the NO\_PRIVACY\_POLICY function when you want a query to have unrestricted access to the table or view
      to which the privacy policy is assigned.

  `PRIVACY_BUDGET`
  :   Use the body’s expression to call the PRIVACY\_BUDGET function when you want to return a privacy budget from the policy.

For the complete syntax for the NO\_PRIVACY\_POLICY and PRIVACY\_BUDGET functions, see [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy).

#### Example privacy policies

Single privacy budget without conditions
:   Create a privacy policy `my_priv_policy` that always returns a privacy budget named `analysts`:

    > Copy code
    >
    > ```
    > CREATE PRIVACY POLICY my_priv_policy
    >   AS ( ) RETURNS PRIVACY_BUDGET ->
    >   PRIVACY_BUDGET(BUDGET_NAME=> 'analysts');
    > ```

Conditional privacy policy
:   Create a privacy policy `my_priv_policy` that gives `admin` unrestricted access to the privacy-protected table or view while
    associating all other users with the privacy budget `analysts`:

    > Copy code
    >
    > ```
    > CREATE PRIVACY POLICY my_priv_policy
    >   AS () RETURNS PRIVACY_BUDGET ->
    >     CASE
    >       WHEN CURRENT_USER() = 'ADMIN'
    >         THEN NO_PRIVACY_POLICY()
    >       ELSE PRIVACY_BUDGET(BUDGET_NAME => 'analysts')
    >     END;
    > ```

Conditional privacy policy for cross-account sharing
:   Create a privacy policy `my_priv_policy` that does the following:

    - Gives `admin` unrestricted access to the privacy-protected table or view.
    - Associates the privacy budget `analysts` to users in the same account.
    - Names the privacy budget associated with external account users so it can be easily identified. Privacy budgets are automatically
      namespaced to a specific external account, but using a descriptive naming scheme can help manage the privacy budgets.

    Copy code

    ```
    CREATE PRIVACY POLICY my_priv_policy
      AS () RETURNS PRIVACY_BUDGET ->
        CASE
          WHEN CURRENT_USER() = 'ADMIN'
            THEN NO_PRIVACY_POLICY()
          WHEN CURRENT_ACCOUNT() = 'YE74187'
            THEN PRIVACY_BUDGET(BUDGET_NAME => 'analysts')
          ELSE PRIVACY_BUDGET(BUDGET_NAME => 'external.' || CURRENT_ACCOUNT())
        END;
    ```

#### Using context functions in the policy body

You can include [context functions](/sql-reference/functions-context) in the body of a privacy policy so its behavior depends on the
context in which the differentially private query is executed.

You can use the following context functions in the body of a privacy policy:

| Context function | Description |
| --- | --- |
| [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) | Returns the account locator in use for the user’s current session. |
| [CURRENT\_DATABASE](/sql-reference/functions/current_database) | Returns the database that contains the table that is protected by the privacy policy. |
| [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name) | Returns the name of the organization in use for user’s the current session. |
| [CURRENT\_ROLE](/sql-reference/functions/current_role) | Returns the name of the role in use for the current session. |
| [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) | Returns the schema that contains the table that is protected by the privacy policy. |
| [CURRENT\_USER](/sql-reference/functions/current_user) | Returns the name of the user executing the query. |
| [INVOKER\_ROLE](/sql-reference/functions/invoker_role) | Returns the name of the executing role. |
| [INVOKER\_SHARE](/sql-reference/functions/invoker_share) | Returns the name of the share that directly accessed the table or view where the INVOKER\_SHARE function is invoked. |

Expand

Show lessSee more

Tip

Context functions like [CURRENT\_USER](/sql-reference/functions/current_user) return strings,
so comparisons using them are case-sensitive. You can use [LOWER](/sql-reference/functions/lower) to convert strings to all lowercase
if you’d like to do a case-insensitive comparison.

### Modify a privacy policy

Use the [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) command to modify a privacy policy. You can rename the policy, change its body, or
modify a comment.

For example, to replace the existing body of a privacy policy `my_priv_policy` with a new body that always returns a budget
`external_analysts`, execute:

Copy code

```
ALTER PRIVACY POLICY my_priv_policy SET BODY ->
  PRIVACY_BUDGET(BUDGET_NAME => 'external_analysts');
```

### Assign a privacy policy

A privacy policy can be applied to one or more tables or views to protect them with differential privacy. A table or view can have only one privacy policy assigned to it.

Use the ADD PRIVACY POLICY clause of an [ALTER TABLE](/sql-reference/sql/alter-table) or [ALTER VIEW](/sql-reference/sql/alter-view) command to assign
a privacy policy to the table or view. The syntax is:

> Copy code
>
> ```
> ALTER { TABLE | [ MATERIALIZED ] VIEW } <name>
>   ADD PRIVACY POLICY <policy_name>
>   { NO ENTITY KEY | ENTITY KEY ( <column_name> ) }
> ```

Where:

- `name` specifies the name of the table or view.
- `policy_name` specifies the name of the privacy policy.
- `column_name` specifies the entity key for the table or view. The [entity key](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy) is a
  column that uniquely identifies an entity within the table or view.

In most cases, you’ll want to define an entity key in order to implement entity-level privacy, though you can use the NO ENTITY KEY clause
to protect individual rows without considering whether data belonging to an entity could exist in multiple rows. For more information, see [About entity-level privacy](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy).

For example, to assign the policy `my_priv_policy` to the table `t1` where the entity key is the `email` column, execute:

> Copy code
>
> ```
> ALTER TABLE t1 ADD PRIVACY POLICY my_priv_policy ENTITY KEY (email);
> ```

### Replace a privacy policy or entity key

The recommended method of replacing a privacy policy or entity key is to use both the ADD and DROP clauses in the same ALTER TABLE or ALTER
VIEW command. This allows you to atomically make the change because both operations take place in the same transaction, leaving no gap in
protection.

To keep the same policy but change the entity key, you need to drop the policy, then add it again with the new entity key.

For example, to assign a new privacy policy to a table that is already protected by a privacy policy:

Copy code

```
ALTER TABLE finance.accounting.customers
  DROP PRIVACY POLICY priv_policy_1,
  ADD PRIVACY POLICY priv_policy_2 ENTITY KEY (email);
```

You can also detach the privacy policy from a table or view in one statement and then set a new policy
on the table or view in a different statement. If you choose this method, the table is not protected by a privacy policy in between
detaching one policy and assigning another. A query could potentially access sensitive data during this time if the users still have SELECT
privileges on the data.

### Detach a privacy policy

Use the DROP PRIVACY POLICY clause of an ALTER TABLE or ALTER VIEW command to detach a privacy policy from a table or
view. After executing this command, the table or view is no longer privacy-protected. The syntax is:

> Copy code
>
> ```
> ALTER { TABLE | [ MATERIALIZED ] VIEW } <name> DROP PRIVACY POLICY <policy_name>
> ```

Where:

- `name` specifies the name of the table or view.
- `policy_name` specifies the name of the privacy policy.

For example, to detach the privacy policy `my_priv_policy` from the `finance.accounting.customers` table:

> Copy code
>
> ```
> ALTER TABLE finance.accounting.customers
>   DROP PRIVACY POLICY my_priv_policy;
> ```

## Monitor privacy policies

To help monitor the use of privacy policies, you can list all of the privacy policies in your account, determine which tables and views are
protected by a particular privacy policy, or list all policies currently assigned to a table or view.

### List all privacy policies

You can use the [PRIVACY\_POLICIES](/sql-reference/account-usage/privacy_policies) view in the Account Usage schema of the shared
SNOWFLAKE database. This view is a *catalog* for all privacy policies in your Snowflake account. For example:

> Copy code
>
> ```
> SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.PRIVACY_POLICIES
>   ORDER BY POLICY_NAME;
> ```

### Identify privacy policy references

The [POLICY\_REFERENCES](/sql-reference/functions/policy_references) Information Schema table function can identify which tables and views are protected by
privacy policies. There are two different syntax options:

1. Return a row for each object (that is, table or view) that has the specified privacy policy set on it:

   Copy code

   ```
   USE DATABASE my_db;
   USE SCHEMA information_schema;
   SELECT policy_name,
       policy_kind,
       ref_entity_name,
       ref_entity_domain,
       ref_column_name,
       ref_arg_column_names,
       policy_status
   FROM TABLE(information_schema.policy_references(policy_name => 'my_db.my_schema.privpolicy'));
   ```
2. Return a row for each policy assigned to the table named `my_table`. Use the POLICY\_KIND column to identify which policies are privacy
   policies.

   Copy code

   ```
   USE DATABASE my_db;
   USE SCHEMA information_schema;
   SELECT policy_name,
       policy_kind,
       ref_entity_name,
       ref_entity_domain,
       ref_column_name,
       ref_arg_column_names,
       policy_status
   FROM TABLE(information_schema.policy_references(ref_entity_name => 'my_db.my_schema.my_table', ref_entity_domain => 'table'));
   ```

## Privileges and commands

The following subsections provide information to help manage privacy policies.

### Privacy policy privileges

Snowflake supports the following privileges on the privacy policy object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Usage |
| --- | --- |
| APPLY | Lets you assign a privacy policy to, or detach a privacy policy from, a table or view. |
| OWNERSHIP | Required to alter most properties of a privacy policy. Ownership of the privacy policy can be transferred, which grants full control over the privacy policy. |

Expand

Show lessSee more

### Privacy policy DDL reference

Snowflake supports the following DDL to create and manage privacy policies.

- [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy)
- [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy)
- [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy)
- [DROP PRIVACY POLICY](/sql-reference/sql/drop-privacy-policy)
- [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies)

### Summary of DDL commands, operations, and privileges

The following table summarizes the relationship between privacy policy privileges and DDL operations.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Operation | Privilege required |
| --- | --- |
| Create privacy policy | A role with the CREATE PRIVACY POLICY privilege in the same schema. |
| Alter privacy policy | The role with the OWNERSHIP privilege on the privacy policy. |
| Describe privacy policy | **One** of the following:   - A role with the global APPLY PRIVACY POLICY privilege. - A role with the OWNERSHIP privilege on the privacy policy. - A role with the APPLY privilege on the privacy policy. |
| Drop privacy policy. | A role with the OWNERSHIP privilege on the privacy policy. |
| Show privacy policies. | **One** of the following:   - A role with the USAGE privilege on the schema in which the privacy policy exists. - A role with the APPLY PRIVACY POLICY on the account. |
| Assign a privacy policy to, or detach a privacy policy from, a table or view. | **One** of the following:   - A role with the APPLY PRIVACY POLICY privilege on the account. - A role with the APPLY privilege on the privacy policy and the OWNERSHIP privilege on the table or view. |

Expand

Show lessSee more
