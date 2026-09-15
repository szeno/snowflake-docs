# Tag-based row access policies

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A [row access policy](/user-guide/security-row-intro) is used to control which rows are returned in a query result. It lets you filter
out rows based on the values in one or more columns of the table. A [tag](/user-guide/object-tagging/introduction) is a schema-level
object that can be assigned to another object, including databases, schemas, tables, and views. *Tag-based row access policies* combine the
object tagging and row access policy features to allow a row access policy to be set on a tag using an ALTER TAG command.

When a row access policy is set on a tag, a table or view is protected by the policy when the tag is set on the object or on a parent
database or schema. By default, Snowflake maps policy arguments to table columns when the name and data type match. You can optionally
define [signature aliases](#label-tag-based-rap-signature-aliases) when attaching the policy to the tag to map arguments to columns with
different names.

You can create the body of the row access policy to filter out rows based on the value of a column (like a regular row access
policy) or you can filter out rows based on the value of the tag that is associated with the policy. For examples of these two strategies,
see [Extended examples](#label-tag-based-rap-examples).

For tag inheritance and propagation, see [Understanding tag inheritance and propagation](/user-guide/tag-based-policies#label-tag-based-policies-inheritance) in [Attribute-based access control (ABAC) using tag-based policies](/user-guide/tag-based-policies).

## Before you begin

Before you implement tag-based row access policies, you should determine how tags and row access policies are currently being used in your
account. Use the following steps:

1. Identify the existing tags and their string values in your Snowflake account.

   - Query the Account Usage [TAG REFERENCES](/sql-reference/account-usage/tag_references) view to obtain all tags and their assigned
     string values.
   - Optionally, query the Account Usage [TAGS](/sql-reference/account-usage/tags) view to obtain a list of tags to ensure that
     duplicate tag naming doesn’t occur later while using tag-based row access policies.
   - Optionally, compare the outputs from the TAG\_REFERENCES and TAGS queries to determine if there are any unassigned tags that can be used
     later.
2. Identify the existing policies and their definitions in your Snowflake account.

   - Run the [SHOW ROW ACCESS POLICIES](/sql-reference/sql/show-row-access-policies) command to obtain a list of existing row access policies.
   - Decide whether these policies, in their current form, can be assigned to tags. If necessary, run the
     [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy) command to obtain the policy definition.

## Workflow for using a tag-based row access policy

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command or use an existing tag.
2. Create a row access policy using the [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) command or use an existing policy.
3. Set the row access policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.

   Copy code

   ```
   ALTER TAG [ IF EXISTS ] <tag_name> SET ROW ACCESS POLICY <policy_name>
     [ ON ( <arg_name> <data_type> [ , ... ] ) [ , ( <arg_name> <data_type> [ , ... ] ) ... ] ];
   ```

   For example:

   Copy code

   ```
   ALTER TAG my_tag SET ROW ACCESS POLICY rap_policy;
   ```

   If you omit the `ON` clause, Snowflake uses the argument names and data types from the policy signature. To map policy arguments to
   columns with different names, specify one or more signature aliases. For more information, see
   [Signature aliases](#label-tag-based-rap-signature-aliases) (in this topic).
4. Use one of the following commands to set the tag on an object:

   - [ALTER DATABASE](/sql-reference/sql/alter-database)
   - [ALTER SCHEMA](/sql-reference/sql/alter-schema)
   - [ALTER TABLE](/sql-reference/sql/alter-table)
   - [ALTER VIEW](/sql-reference/sql/alter-view)

   For example:

   Copy code

   ```
   ALTER TABLE t1 SET TAG my_tag = 'sensitive';
   ```
5. Query the data to verify that the tag-based row access policy protects the data as intended.

For end-to-end examples of this workflow, see [Extended examples](#label-tag-based-rap-examples).

## Signature aliases

When you attach a row access policy to a table directly, you specify which columns enforce the policy:

Copy code

```
ALTER TABLE t ADD ROW ACCESS POLICY rap ON (dept_code, region);
```

Tag-based attachment has no table-level column specification when you set the tag on an object. Signature aliases address this by letting
you reuse policies with generic argument names (for example, `col1` or `arg_1`) across tables whose column names differ, without creating
duplicate policies or views to rename columns.

When you attach a row access policy to a tag, optionally use the `ON` clause to supply one or more alias tuples for the entire policy
signature:

Copy code

```
ALTER TAG T SET ROW ACCESS POLICY RAP
  ON (id NUMBER, ssn STRING), (user_id NUMBER, social_security STRING);
```

When the tag is set on a table or view, Snowflake resolves signature aliases in the order you specified:

1. Snowflake tries to match the first alias tuple to columns on the table. In this example, Snowflake looks for `id` and `ssn` columns
   with the matching data types.
2. If at least one argument in that tuple can’t be resolved, Snowflake tries the next alias tuple (`user_id`, `social_security`).
3. If more than one alias tuple matches the same table, Snowflake returns a runtime error when a query runs on that table.
4. If no alias tuple matches, the policy isn’t enforced on that table.

## Remove a row access policy from a tag

To remove a row access policy from a tag, use the ALTER TAG statement with the UNSET ROW ACCESS POLICY clause:

Copy code

```
ALTER TAG [ IF EXISTS ] <tag_name> UNSET ROW ACCESS POLICY <policy_name>;
```

For example:

Copy code

```
ALTER TAG security UNSET ROW ACCESS POLICY row_policy_1;
```

## Replace a row access policy on a tag

You have two options to replace the row access policy for a tag-based policy with a different row access policy.

Option 1:
:   Unset the policy from a tag in one statement and then set a new policy on the tag in a different statement:

    Copy code

    ```
    ALTER TAG security UNSET ROW ACCESS POLICY rap_policy_1;

    ALTER TAG security SET ROW ACCESS POLICY rap_policy_2;
    ```

Option 2:
:   Use the `FORCE` keyword to replace the policy in a single statement.

    > Copy code
    >
    > ```
    > ALTER TAG security SET ROW ACCESS POLICY rap_policy_2 FORCE;
    > ```

Important

Exercise caution when replacing a row access policy on a tag.

Depending on the timing of the replacement and queries on the protected objects, choosing to replace the policy in two separate statements
could lead to a data leak because the table or view data is unprotected in the time interval between the UNSET and SET operations.

However, if the policy conditions in the replacement policy differ from those in the original policy, specifying the `FORCE` keyword
could lead to a lack of access because (previously) users could access data and the replacement no longer allows access.

Prior to replacing a policy, consult your internal data administrators to coordinate the best approach to protect data with tag-based row
access policies and replace row access policies as needed.

## Deleting tag-based row access policies

The following restrictions apply when attempting to delete a tag-based row access policy:

- A tag can’t be [dropped](/sql-reference/sql/drop-tag) if it is assigned to a row access policy.
- A row access policy can’t be [dropped](/sql-reference/sql/drop-row-access-policy) if it is assigned to a tag.
- A database or schema can’t be dropped if it contains a tag with a row access policy.
- A database or schema can’t be dropped if it contains a row access policy that is set on a tag.

To delete either the tag or the row access policy, you must first run an ALTER TAG … UNSET ROW ACCESS POLICY command to remove the
association between the tag and policy.

## Update a tag value

If a schema owner (for example, `sch_role`) sets a tag on a schema and then a different role sets a row access policy on the same tag
(for example, `rap_admin_role`), the schema owner can’t change the tag value. Snowflake fails the ALTER SCHEMA … SET TAG operation for
the schema owner.

To change the tag value, you must do the following:

1. Using the `rap_admin_role`, unset the row access policy from the tag.
2. Using the `sch_role`, modify the tag value.
3. Using the `rap_admin_role`, reassign the row access policy to the tag.

## Access control requirements

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Set a row access policy on a tag | APPLY ROW ACCESS POLICY on the account |  |
| Set a tag-based row access policy on a database/schema | - APPLY ROW ACCESS POLICY on the account - One of the following:   - GRANT APPLY TAG on the account   - GRANT APPLY on the tag |  |
| Set a tag-based row access policy on a table/view | One of the following:   - GRANT APPLY TAG on the account - GRANT APPLY on the tag |  |
| Unset a row access policy from a tag | APPLY ROW ACCESS POLICY on the account |  |

Expand

Show lessSee more

### Privileges for tag owners

A tag owner must have the APPLY ROW ACCESS POLICY privilege to unset a row access policy from the tag.

In some cases, tag owners can work with tag-based row access policies without having the APPLY ROW ACCESS POLICY privilege. If your role has
the OWNERSHIP or APPLY privilege on a tag that has a row access policy set on it, you can apply the tag to your table or view without the
APPLY ROW ACCESS POLICY privilege. However, you still need the APPLY ROW ACCESS POLICY privilege to apply the same tag to a database or
schema.

## Extended examples

- [Common assumptions with the examples](#common-assumptions-with-the-examples)
- [Example 1: Protect table data based on the row access policy assigned to the tag](#example-1-protect-table-data-based-on-the-row-access-policy-assigned-to-the-tag)
- [Example 2: Protect table data based on the tag string value](#example-2-protect-table-data-based-on-the-tag-string-value)

### Common assumptions with the examples

The examples in this section make the following assumptions:

- The prerequisite steps were completed.
- The `tag_admin` custom role has the following privileges:

  - The schema-level CREATE TAG privilege.
  - The global APPLY TAG privilege.

  For more information, see [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `row_access_admin` custom role has the following privileges:

  - The schema-level CREATE ROW ACCESS POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.row_access_policies` schema.
  - The global APPLY ROW ACCESS POLICY privilege to assign row access policies to tags.
  - The global APPLY TAG privilege, to assign the tag (with the row access policies) to objects.

  For more information, see [row access policy privileges](/user-guide/security-row-intro#label-security-row-privilege-command-summary).
- The `data_admin` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The `analyst` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and on the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The custom roles described above are granted to the appropriate users.

  For details, see [Configuring access control](/user-guide/security-access-control-configure).

### Example 1: Protect table data based on the row access policy assigned to the tag

This example assigns a row access policy to a tag and then assigns the tag to a table. The result is that the row access policy controls
which rows are visible in query results.

The following steps create a tag-based row access policy to protect accounting data. For example, consider the table named
`finance.accounting.transactions`, which has multiple columns including `ACCOUNT_NAME`, `TRANSACTION_DATE`, and `AMOUNT`.

> ```
> +---------------+------------------+----------+
> |  ACCOUNT_NAME | TRANSACTION_DATE | AMOUNT   |
> +---------------+------------------+----------+
> |  ACME         | 2026-01-15       | 50000.00 |
> |  GlobalCorp   | 2026-01-16       | 75000.00 |
> +---------------+------------------+----------+
> ```

Create a tag-based row access policy to protect the table as follows:

1. Create a tag named `data_protection` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG data_protection;
   ```
2. Create a row access policy that filters out all rows except the ones where the account name is `ACME`.

   Copy code

   ```
   USE ROLE row_access_admin;
   USE SCHEMA governance.row_access_policies;

   CREATE OR REPLACE ROW ACCESS POLICY accounting_rap
   AS (account_name string) RETURNS BOOLEAN ->
     CASE
    WHEN account_name = 'ACME' THEN TRUE
    ELSE FALSE
     END;
   ```
3. Assign the row access policy to the `data_protection` tag.

   Copy code

   ```
   ALTER TAG governance.tags.data_protection SET ROW ACCESS POLICY accounting_rap;
   ```
4. Assign the `data_protection` tag to the `finance.accounting.transactions` table.

   Copy code

   ```
   ALTER TABLE finance.accounting.transactions
     SET TAG governance.tags.data_protection = 'protected';
   ```
5. Query the table to verify the tag-based row access policy protects the data as intended.

   Copy code

   ```
   USE ROLE analyst;
   SELECT * FROM finance.accounting.transactions;
   ```

   Returns only the row where `ACCOUNT_NAME` is `ACME`:

   ```
   +---------------+------------------+----------+
   |  ACCOUNT_NAME | TRANSACTION_DATE | AMOUNT   |
   +---------------+------------------+----------+
   |  ACME         | 2026-01-15       | 50000.00 |
   +---------------+------------------+----------+
   ```

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM finance.accounting.transactions;
   ```

   Returns the same filtered result. The policy evaluates the `account_name` column value, not the current role, so only the ACME row is
   visible to both roles.

### Example 2: Protect table data based on the tag string value

This example uses a tag-based row access policy to determine whether rows should be visible based upon the string value of the tag assigned
to a table. The row access policy dynamically evaluates the tag string value by calling the [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag)
function in the row access policy conditions.

The following steps create a tag-based row access policy to protect accounting data:

1. Create a tag named `sensitivity_level` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG sensitivity_level;
   ```
2. Create a row access policy that evaluates the tag string value. All rows are visible when the tag string value on the table is
   `'public'`. When the tag string value is `'restricted'`, only rows where `account_name` is `'ACME'` are visible, regardless of role.

   > Copy code
   >
   > ```
   > USE ROLE row_access_admin;
   > USE SCHEMA governance.row_access_policies;
   >
   > CREATE ROW ACCESS POLICY sensitivity_rap
   > AS (account_name string) RETURNS BOOLEAN ->
   >   CASE
   >  WHEN SYSTEM$GET_TAG('governance.tags.sensitivity_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'TRANSACTIONS', 'TABLE') = 'public' THEN TRUE
   >  WHEN SYSTEM$GET_TAG('governance.tags.sensitivity_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'TRANSACTIONS', 'TABLE') = 'restricted'
   >       AND account_name = 'ACME' THEN TRUE
   >  ELSE FALSE
   >   END;
   > ```
   >
   > Note
   >
   > This policy uses the fully qualified name for the tag in the function argument. Snowflake returns an error at query runtime if the
   > system function argument in the policy conditions contains a tag name that is not sufficiently qualified.
   >
   > For more information, see [Object name resolution](/sql-reference/name-resolution).
3. Assign the row access policy to the `sensitivity_level` tag.

   Copy code

   ```
   ALTER TAG governance.tags.sensitivity_level SET ROW ACCESS POLICY sensitivity_rap;
   ```
4. Assign the `sensitivity_level` tag to the table with the tag string value `'restricted'`.

   Copy code

   ```
   ALTER TABLE finance.accounting.transactions
     SET TAG governance.tags.sensitivity_level = 'restricted';
   ```
5. Query the table to ensure Snowflake returns the correct query result based on the tag value.

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM finance.accounting.transactions;
   ```

   Returns only the row where `ACCOUNT_NAME` is `ACME` (because the tag value is `'restricted'`):

   ```
   +---------------+------------------+----------+
   |  ACCOUNT_NAME | TRANSACTION_DATE | AMOUNT   |
   +---------------+------------------+----------+
   |  ACME         | 2026-01-15       | 50000.00 |
   +---------------+------------------+----------+
   ```

   Copy code

   ```
   USE ROLE analyst;
   SELECT * FROM finance.accounting.transactions;
   ```

   Returns the same filtered result. The policy does not reference the current role.
6. Change the tag value to `'public'` to allow all roles to view all rows:

   Copy code

   ```
   ALTER TABLE finance.accounting.transactions
     SET TAG governance.tags.sensitivity_level = 'public';

   USE ROLE analyst;
   SELECT * FROM finance.accounting.transactions;
   ```

   Returns all rows (because the tag value is now `'public'`):

   ```
   +---------------+------------------+----------+
   |  ACCOUNT_NAME | TRANSACTION_DATE | AMOUNT   |
   +---------------+------------------+----------+
   |  ACME         | 2026-01-15       | 50000.00 |
   |  GlobalCorp   | 2026-01-16       | 75000.00 |
   +---------------+------------------+----------+
   ```

## Limitations and considerations

- If a row access policy already protects a table or view and a tag-based row access policy is also set on the same object, the directly
  assigned row access policy takes precedence over the row access policy assigned to the tag.
- By default, the name and data type of each policy argument must match a column on the table (case insensitive). If they don’t match and
  no signature alias resolves, the policy isn’t enforced. For more information, see
  [Signature aliases](#label-tag-based-rap-signature-aliases) (in this topic).
- A tag can have only one row access policy.
- A policy cannot be assigned to a system tag.
- A table can’t be associated with more than one tag-based row access policy.
- If a different type of data protection policy — for example, a masking policy — is assigned to a tag, you can’t attach a row access
  policy to the same tag.
- A tag-based row access policy can be applied to a table or view that is assigned other tag-based policies, for example, a tag-based
  projection policy. Query results reflect the cumulative effect of all policies when they are evaluated at runtime.
