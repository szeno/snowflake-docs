# Tag-based projection policies

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A [projection policy](/user-guide/projection-policies) is a schema-level object that defines whether a column can be projected in the
output of a SQL query result. A [tag](/user-guide/object-tagging/introduction) is a schema-level object that can be assigned to
another object, including databases, schemas, tables, views, and columns. *Tag-based projection policies* combine the object tagging and
projection policy features to allow a projection policy to be set on a tag using an ALTER TAG command. When
a projection policy is set on a tag, a column is protected by the policy whenever the tag is set on the column.

You can create the body of the projection policy to allow or block projection based on the current user’s role (like a regular projection
policy) or you can control projection based on the value of the tag that is associated with the policy. For examples of these two
strategies, see [Extended examples](#label-tag-based-pp-examples).

For tag inheritance and propagation, see [Understanding tag inheritance and propagation](/user-guide/tag-based-policies#label-tag-based-policies-inheritance) in [Attribute-based access control (ABAC) using tag-based policies](/user-guide/tag-based-policies).

## Before you begin

Before you implement tag-based projection policies, you should determine how tags and projection policies are currently being used in your
account. Use the following steps:

1. Identify the existing tags and their string values in your Snowflake account.

   - Query the Account Usage [TAG REFERENCES](/sql-reference/account-usage/tag_references) view to obtain all tags and their assigned
     string values.
   - Optionally, query the Account Usage [TAGS](/sql-reference/account-usage/tags) view to obtain a list of tags to ensure that
     duplicate tag naming doesn’t occur later while using tag-based projection policies.
   - Optionally, compare the outputs from the TAG\_REFERENCES and TAGS queries to determine if there are any unassigned tags that can be used
     later.
2. Identify the existing policies and their definitions in your Snowflake account.

   - Run the [SHOW PROJECTION POLICIES](/sql-reference/sql/show-projection-policies) command to obtain a list of existing projection policies.
   - Decide whether these policies, in their current form, can be assigned to tags. If necessary, run the
     [DESCRIBE PROJECTION POLICY](/sql-reference/sql/desc-projection-policy) command to obtain the policy definition.

## Workflow for using a tag-based projection policy

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command or use an existing tag.
2. Create a projection policy using the [CREATE PROJECTION POLICY](/sql-reference/sql/create-projection-policy) command or use an existing policy.
3. Set the projection policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.

   For example:

   Copy code

   ```
   ALTER TAG my_tag SET PROJECTION POLICY proj_policy;
   ```
4. Set the tag on a column.

   For example:

   Copy code

   ```
   ALTER TABLE t1 MODIFY COLUMN email SET TAG my_tag = 'sensitive';
   ```

   You can also set the tag at the database, schema, or table level.
5. Query the data to verify that the tag-based projection policy protects the data as intended.

For end-to-end examples of this workflow, see [Extended examples](#label-tag-based-pp-examples).

## Remove a projection policy from a tag

To remove a projection policy from a tag, use the ALTER TAG statement with the UNSET PROJECTION POLICY clause.

Copy code

```
ALTER TAG security UNSET PROJECTION POLICY proj_policy_1;
```

## Replace a projection policy on a tag

You have two options to replace the projection policy for a tag-based policy with a different projection policy.

Option 1:
:   Unset the policy from a tag in one statement and then set a new policy on the tag in a different statement:

    Copy code

    ```
    ALTER TAG security UNSET PROJECTION POLICY proj_policy_1;

    ALTER TAG security SET PROJECTION POLICY proj_policy_2;
    ```

Option 2:
:   Use the `FORCE` keyword to replace the policy in a single statement.

    > Copy code
    >
    > ```
    > ALTER TAG security SET PROJECTION POLICY proj_policy_2 FORCE;
    > ```

Important

Exercise caution when replacing a projection policy on a tag.

Depending on the timing of the replacement and queries on the protected columns, choosing to replace the policy in two separate statements
could lead to a data leak because the column data is unprotected in the time interval between the UNSET and SET operations.

However, if the policy conditions in the replacement policy differ from those in the original policy, specifying the `FORCE` keyword
could lead to a lack of access because (previously) users could project the column and the replacement no longer allows projection.

Prior to replacing a policy, consult your internal data administrators to coordinate the best approach to protect data with tag-based
projection policies and replace projection policies as needed.

## Deleting tag-based projection policies

The following restrictions apply when attempting to delete a tag-based projection policy:

- A tag can’t be [dropped](/sql-reference/sql/drop-tag) if it is assigned to a projection policy.
- A projection policy can’t be [dropped](/sql-reference/sql/drop-projection-policy) if it is assigned to a tag.
- A database or schema can’t be dropped if it contains a tag with a projection policy.
- A database or schema can’t be dropped if it contains a projection policy that is set on a tag.

To delete either the tag or the projection policy, you must first run an ALTER TAG … UNSET PROJECTION POLICY command to remove the
association between the tag and policy.

## Update a tag value

If a schema owner (for example, `sch_role`) sets a tag on a schema and then a different role sets a projection policy on the same tag
(for example, `proj_admin_role`), the schema owner can’t change the tag value. Snowflake fails the ALTER SCHEMA … SET TAG operation for
the schema owner.

To change the tag value, you must do the following:

1. Using the `proj_admin_role`, unset the projection policy from the tag.
2. Using the `sch_role`, modify the tag value.
3. Reassign the projection policy to the tag using the `proj_admin_role`.

## Access control requirements

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Set a projection policy on a tag | APPLY PROJECTION POLICY on the account |  |
| Set a tag-based projection policy on a column, table, or view | One of the following:   - GRANT APPLY TAG on the account - GRANT APPLY on the tag |  |
| Set a tag-based projection policy on a database/schema | - APPLY PROJECTION POLICY on the account - One of the following:   - GRANT APPLY TAG on the account   - GRANT APPLY on the tag |  |
| Unset a projection policy from a tag | APPLY PROJECTION POLICY on the account |  |

Expand

Show lessSee more

### Privileges for tag owners

A tag owner must have the APPLY PROJECTION POLICY privilege to unset a projection policy from the tag.

In some cases, tag owners can work with tag-based projection policies without having the APPLY PROJECTION POLICY privilege. If your role has
the OWNERSHIP or APPLY privilege on a tag that has a projection policy set on it, you can apply the tag to your column, table, or view
without the APPLY PROJECTION POLICY privilege. However, you still need the APPLY PROJECTION POLICY privilege to apply the same tag to a
database or schema.

## Extended examples

- [Common assumptions with the examples](#common-assumptions-with-the-examples)
- [Example 1: Protect column data based on the projection policy assigned to the tag](#example-1-protect-column-data-based-on-the-projection-policy-assigned-to-the-tag)
- [Example 2: Protect column data based on the tag string value](#example-2-protect-column-data-based-on-the-tag-string-value)

### Common assumptions with the examples

The examples in this section make the following assumptions:

- The prerequisite steps were completed.
- The `tag_admin` custom role has the following privileges:

  - The schema-level CREATE TAG privilege.
  - The global APPLY TAG privilege.

  For more information, see [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `projection_admin` custom role has the following privileges:

  - The schema-level CREATE PROJECTION POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.projection_policies` schema.
  - The global APPLY PROJECTION POLICY privilege to assign projection policies to tags.
  - The global APPLY TAG privilege, to assign the tag (with the projection policies) to objects.

  For more information, see [projection policy privileges](/user-guide/projection-policies#label-projection-policy-ddl-privilege-summary).
- The `data_admin` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The `analyst` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and on the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The custom roles described above are granted to the appropriate users.

  For details, see [Configuring access control](/user-guide/security-access-control-configure).

### Example 1: Protect column data based on the projection policy assigned to the tag

This example assigns a projection policy to a tag and then assigns the tag to a column. The result is that the projection policy controls
whether a query can project the column.

The following steps create a tag-based projection policy to protect accounting data. For example, consider the table named
`finance.accounting.customers`, which has multiple columns including `CUSTOMER_NAME`, `EMAIL`, and `PHONE`.

> ```
> +----------------+----------------------+----------------+
> |  CUSTOMER_NAME | EMAIL                | PHONE          |
> +----------------+----------------------+----------------+
> |  Alice Johnson | alice@example.com    | 555-0123       |
> |  Bob Smith     | bob@globalcorp.com   | 555-0456       |
> +----------------+----------------------+----------------+
> ```

Create a tag-based projection policy to protect the EMAIL column as follows:

1. Create a tag named `data_protection` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG data_protection;
   ```
2. Create a projection policy that allows only the DATA\_ADMIN role to project the column.

   Copy code

   ```
   USE ROLE projection_admin;
   USE SCHEMA governance.projection_policies;

   CREATE OR REPLACE PROJECTION POLICY accounting_proj
   AS () RETURNS PROJECTION_CONSTRAINT ->
     CASE
    WHEN CURRENT_ROLE() = 'DATA_ADMIN' THEN PROJECTION_CONSTRAINT(ALLOW => true)
    ELSE PROJECTION_CONSTRAINT(ALLOW => false)
     END;
   ```
3. Assign the projection policy to the `data_protection` tag.

   Copy code

   ```
   ALTER TAG governance.tags.data_protection SET PROJECTION POLICY accounting_proj;
   ```
4. Assign the `data_protection` tag to the `EMAIL` column of the `finance.accounting.customers` table.

   Copy code

   ```
   ALTER TABLE finance.accounting.customers
     MODIFY COLUMN email SET TAG governance.tags.data_protection = 'protected';
   ```
5. Query the table to verify the tag-based projection policy protects the column as intended.

   Copy code

   ```
   USE ROLE analyst;
   SELECT * FROM finance.accounting.customers;
   ```

   The query fails because the analyst role is attempting to project the protected EMAIL column.

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM finance.accounting.customers;
   ```

   The query succeeds for the `data_admin` role, returning all columns including EMAIL.

### Example 2: Protect column data based on the tag string value

This example uses a tag-based projection policy to determine whether a column should be visible based upon the string value of the tag
assigned to a column. The projection policy dynamically evaluates the tag string value by calling the
[SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) function in the projection policy conditions.

The following steps create a tag-based projection policy to protect accounting data:

1. Create a tag named `sensitivity_level` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG sensitivity_level;
   ```
2. Create a projection policy that evaluates the tag string value. The column is visible when the current tag string value on the column is
   set to `'public'`. If the tag string value is set to `'restricted'`, then the user executing the query must also be using the
   `data_admin` role to project the column.

   > Copy code
   >
   > ```
   > USE ROLE projection_admin;
   > USE SCHEMA governance.projection_policies;
   >
   > CREATE PROJECTION POLICY sensitivity_proj
   > AS () RETURNS PROJECTION_CONSTRAINT ->
   >   CASE
   >  WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('governance.tags.sensitivity_level') = 'public'
   >    THEN PROJECTION_CONSTRAINT(ALLOW => true)
   >  WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('governance.tags.sensitivity_level') = 'restricted'
   >       AND CURRENT_ROLE() IN ('DATA_ADMIN')
   >    THEN PROJECTION_CONSTRAINT(ALLOW => true)
   >  ELSE PROJECTION_CONSTRAINT(ALLOW => false)
   >   END;
   > ```
   >
   > Note
   >
   > This policy uses the fully qualified name for the tag in the function argument. Snowflake returns an error at query runtime if the
   > system function argument in the policy conditions contains a tag name that is not sufficiently qualified.
   >
   > For more information, see [Object name resolution](/sql-reference/name-resolution).
3. Assign the projection policy to the `sensitivity_level` tag.

   Copy code

   ```
   ALTER TAG governance.tags.sensitivity_level SET PROJECTION POLICY sensitivity_proj;
   ```
4. Assign the `sensitivity_level` tag to the `EMAIL` column with the tag string value `'restricted'`.

   Copy code

   ```
   ALTER TABLE finance.accounting.customers
     MODIFY COLUMN email SET TAG governance.tags.sensitivity_level = 'restricted';
   ```
5. Query the table to ensure Snowflake returns the correct query result based on the tag value and current role.

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM finance.accounting.customers;
   ```

   Returns all columns including EMAIL (because tag value is ‘restricted’ and role is DATA\_ADMIN).
6. Change the tag value to `'public'` to allow all roles to project the column:

   Copy code

   ```
   ALTER TABLE finance.accounting.customers
     MODIFY COLUMN email SET TAG governance.tags.sensitivity_level = 'public';

   USE ROLE analyst;
   SELECT * FROM finance.accounting.customers;
   ```

   Returns all columns including EMAIL (because tag value is now ‘public’).

## Limitations and considerations

- If a projection policy already protects a column and a tag-based projection policy is also set on the same column, the directly assigned
  projection policy takes precedence over the projection policy assigned to the tag.
- A tag can have only one projection policy.
- A policy cannot be assigned to a system tag.
- A column can’t be associated with more than one tag-based projection policy.
- If a different type of data protection policy — for example, a masking policy — is assigned to a tag, you can’t attach a projection
  policy to the same tag.
- A tag-based projection policy can be applied to a table or column that is assigned other tag-based policies, for example, a tag-based row
  access policy. Query results reflect the cumulative effect of all policies when they are evaluated at runtime.
- Tag-based projection policies interact with other Snowflake features the same as other projection policies. See [projection policies](/user-guide/projection-policies#label-projection-policy-snowflake-features).
