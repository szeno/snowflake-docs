# Tag-based join policies

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A [join policy](/user-guide/join-policies) is a schema-level object that controls the requirement to join a table when it is queried.
When a join policy is applied to a table, queries against that table either require or do not require a join. A
[tag](/user-guide/object-tagging/introduction) is a schema-level object that can be assigned to another object, including databases,
schemas, tables, and views. *Tag-based join policies* combine the object tagging and join policy features to allow a join policy to be set
on a tag using an ALTER TAG command.

When a join policy is set on a tag, a table or view is protected by the policy when the tag is set on the object or its parent object (like
a database or schema). Tables protected by a tag-based join policy require queries to include joins in the same way as tables with directly
assigned join policies.

You can create the body of the join policy to require joins based on the current user’s role (like a regular join policy) or you can control
join requirements based on the value of the tag that is associated with the policy. For examples of these two strategies, see
[Extended examples](#label-tag-based-join-examples).

For tag inheritance and propagation, see [Understanding tag inheritance and propagation](/user-guide/tag-based-policies#label-tag-based-policies-inheritance) in [Attribute-based access control (ABAC) using tag-based policies](/user-guide/tag-based-policies).

## Before you begin

Before you implement tag-based join policies, you should determine how tags and join policies are currently being used in your account. Use
the following steps:

1. Identify the existing tags and their string values in your Snowflake account.

   - Query the Account Usage [TAG REFERENCES](/sql-reference/account-usage/tag_references) view to obtain all tags and their assigned
     string values.
   - Optionally, query the Account Usage [TAGS](/sql-reference/account-usage/tags) view to obtain a list of tags to ensure that
     duplicate tag naming doesn’t occur later while using tag-based join policies.
   - Optionally, compare the outputs from the TAG\_REFERENCES and TAGS queries to determine if there are any unassigned tags that can be used
     later.
2. Identify the existing policies and their definitions in your Snowflake account.

   - Run the [SHOW JOIN POLICIES](/sql-reference/sql/show-join-policies) command to obtain a list of existing join policies.
   - Decide whether these policies, in their current form, can be assigned to tags. If necessary, run the
     [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy) command to obtain the policy definition.

## Workflow for using a tag-based join policy

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command or use an existing tag.
2. Create a join policy using the [CREATE JOIN POLICY](/sql-reference/sql/create-join-policy) command or use an existing policy.
3. Set the join policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.

   Copy code

   ```
   ALTER TAG [ IF EXISTS ] <tag_name> SET JOIN POLICY <policy_name> [ ALLOWED JOIN KEYS ( <col_name> [ , ... ] ) ];
   ```

   For example:

   Copy code

   ```
   ALTER TAG my_tag SET JOIN POLICY join_policy;
   ```

   Optionally, specify `ALLOWED JOIN KEYS` to define which columns can be used as joining columns when the tag-based join policy is in
   effect:

   Copy code

   ```
   ALTER TAG my_tag SET JOIN POLICY join_policy ALLOWED JOIN KEYS (customer_id, region);
   ```

   For more information, see [Restricting joins on specific columns](/user-guide/join-policies#label-join-policy-allowed-keys-test) in the
   join policies documentation.
4. Use one of the following commands to set the tag on an object:

   - [ALTER DATABASE](/sql-reference/sql/alter-database)
   - [ALTER SCHEMA](/sql-reference/sql/alter-schema)
   - [ALTER TABLE](/sql-reference/sql/alter-table)
   - [ALTER VIEW](/sql-reference/sql/alter-view)

   For example:

   Copy code

   ```
   ALTER TABLE t1 SET TAG my_tag = 'protected';
   ```
5. Query the data to verify that the tag-based join policy protects the data as intended.

For end-to-end examples of this workflow, see [Extended examples](#label-tag-based-join-examples).

## Remove a join policy from a tag

To remove a join policy from a tag, use the ALTER TAG statement with the UNSET JOIN POLICY clause:

Copy code

```
ALTER TAG [ IF EXISTS ] <tag_name> UNSET JOIN POLICY <policy_name>;
```

For example:

Copy code

```
ALTER TAG security UNSET JOIN POLICY join_policy_1;
```

## Replace a join policy on a tag

You have two options to replace the join policy for a tag-based policy with a different join policy.

Option 1:
:   Unset the policy from a tag in one statement and then set a new policy on the tag in a different statement:

    Copy code

    ```
    ALTER TAG security UNSET JOIN POLICY join_policy_1;

    ALTER TAG security SET JOIN POLICY join_policy_2;
    ```

Option 2:
:   Use the `FORCE` keyword to replace the policy in a single statement.

    > Copy code
    >
    > ```
    > ALTER TAG security SET JOIN POLICY join_policy_2 FORCE;
    > ```

Important

Exercise caution when replacing a join policy on a tag.

Depending on the timing of the replacement and queries on the protected objects, choosing to replace the policy in two separate statements
could lead to data exposure because the table or view data is unprotected in the time interval between the UNSET and SET operations.

However, if the policy conditions in the replacement policy differ from those in the original policy, specifying the `FORCE` keyword
could lead to a lack of access because (previously) users could access data and the replacement no longer allows access.

Prior to replacing a policy, consult your internal data administrators to coordinate the best approach to protect data with tag-based join
policies and replace join policies as needed.

## Deleting tag-based join policies

The following restrictions apply when attempting to delete a tag-based join policy:

- A tag can’t be [dropped](/sql-reference/sql/drop-tag) if it is assigned to a join policy.
- A join policy can’t be [dropped](/sql-reference/sql/drop-join-policy) if it is assigned to a tag.
- A database or schema can’t be dropped if it contains a tag with a join policy.
- A database or schema can’t be dropped if it contains a join policy that is set on a tag.

To delete either the tag or the join policy, you must first run an ALTER TAG … UNSET JOIN POLICY command to remove the association between
the tag and policy.

## Update a tag value

If a schema owner (for example, `sch_role`) sets a tag on a schema and then a different role sets a join policy on the same tag (for
example, `join_admin_role`), the schema owner can’t change the tag value. Snowflake fails the ALTER SCHEMA … SET TAG operation for the
schema owner.

To change the tag value, you must do the following:

1. Using the `join_admin_role`, unset the join policy from the tag.
2. Using the `sch_role`, modify the tag value.
3. Using the `join_admin_role`, reassign the join policy to the tag.

## Access control requirements

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Set a join policy on a tag | APPLY JOIN POLICY on the account |  |
| Set a tag-based join policy on a database/schema | - APPLY JOIN POLICY on the account - One of the following:   - GRANT APPLY TAG on the account   - GRANT APPLY on the tag |  |
| Set a tag-based join policy on a table/view | One of the following:   - GRANT APPLY TAG on the account - GRANT APPLY on the tag |  |
| Unset a join policy from a tag | APPLY JOIN POLICY on the account |  |

Expand

Show lessSee more

### Privileges for tag owners

A tag owner must have the APPLY JOIN POLICY privilege to unset a join policy from the tag.

In some cases, tag owners can work with tag-based join policies without having the APPLY JOIN POLICY privilege. If your role has the
OWNERSHIP or APPLY privilege on a tag that has a join policy set on it, you can apply the tag to your table or view without the APPLY JOIN
POLICY privilege. However, you still need the APPLY JOIN POLICY privilege to apply the same tag to a database or schema.

## Extended examples

- [Common assumptions with the examples](#common-assumptions-with-the-examples)
- [Example 1: Protect table data based on the join policy assigned to the tag](#example-1-protect-table-data-based-on-the-join-policy-assigned-to-the-tag)
- [Example 2: Protect table data based on the tag string value](#example-2-protect-table-data-based-on-the-tag-string-value)

### Common assumptions with the examples

The examples in this section make the following assumptions:

- The prerequisite steps were completed.
- The `tag_admin` custom role has the following privileges:

  - The schema-level CREATE TAG privilege.
  - The global APPLY TAG privilege.

  For more information, see [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `join_policy_admin` custom role has the following privileges:

  - The schema-level CREATE JOIN POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.join_policies` schema.
  - The global APPLY JOIN POLICY privilege to assign join policies to tags.
  - The global APPLY TAG privilege, to assign the tag (with the join policies) to objects.

  For more information, see [join policy privileges](/user-guide/join-policies#label-join-policy-ddl-privilege-summary).
- The `data_admin` custom role has the following privileges:

  - The USAGE privilege on the `partner` database and the `partner.shared_data` schema.
  - The SELECT privilege on tables in the `partner.shared_data` schema.
- The `analyst` custom role has the following privileges:

  - The USAGE privilege on the `partner` database and on the `partner.shared_data` schema.
  - The SELECT privilege on tables in the `partner.shared_data` schema.
- The custom roles described above are granted to the appropriate users.

  For details, see [Configuring access control](/user-guide/security-access-control-configure).

### Example 1: Protect table data based on the join policy assigned to the tag

This example assigns a join policy to a tag and then assigns the tag to a table. The result is that the join policy requires queries to
include joins when accessing the table.

The following steps create a tag-based join policy to protect shared partner data. For example, consider a provider’s table named
`partner.shared_data.customer_data`, which has columns including `CUSTOMER_ID`, `REGION`, and `PURCHASE_AMOUNT`.

> ```
> +-------------+--------+-----------------+
> | CUSTOMER_ID | REGION | PURCHASE_AMOUNT |
> +-------------+--------+-----------------+
> | C001        | WEST   | 1500.00         |
> | C002        | EAST   | 2300.00         |
> | C003        | WEST   | 890.00          |
> +-------------+--------+-----------------+
> ```

Create a tag-based join policy to protect the table as follows:

1. Create a tag named `shared_data_protection` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG shared_data_protection;
   ```
2. Create a join policy that requires a join for most users, but allows unrestricted access for the DATA\_ADMIN role.

   Copy code

   ```
   USE ROLE join_policy_admin;
   USE SCHEMA governance.join_policies;

   CREATE OR REPLACE JOIN POLICY partner_join_policy
   AS () RETURNS JOIN_CONSTRAINT ->
    CASE
    WHEN CURRENT_ROLE() = 'DATA_ADMIN' THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE)
    ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
    END;
   ```
3. Assign the join policy to the `shared_data_protection` tag.

   Copy code

   ```
   ALTER TAG governance.tags.shared_data_protection SET JOIN POLICY partner_join_policy;
   ```
4. Assign the `shared_data_protection` tag to the `partner.shared_data.customer_data` table.

   Copy code

   ```
   ALTER TABLE partner.shared_data.customer_data
     SET TAG governance.tags.shared_data_protection = 'protected';
   ```
5. Query the table to verify the tag-based join policy protects the data as intended.

   Copy code

   ```
   USE ROLE analyst;
   SELECT * FROM partner.shared_data.customer_data;
   ```

   The query fails because the analyst role must join the table with another table.

   Copy code

   ```
   USE ROLE analyst;
   SELECT cd.customer_id, cd.region, cd.purchase_amount
   FROM partner.shared_data.customer_data cd
   INNER JOIN local_db.my_schema.my_customers mc ON cd.customer_id = mc.customer_id;
   ```

   The query succeeds because it includes a join with another table.

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM partner.shared_data.customer_data;
   ```

   The query succeeds for the `data_admin` role, returning all rows without requiring a join.

### Example 2: Protect table data based on the tag string value

This example uses a tag-based join policy to determine join requirements based upon the string value of the tag assigned to a table. The
join policy dynamically evaluates the tag string value by calling the [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) function in the join
policy conditions.

The following steps create a tag-based join policy to protect data:

1. Create a tag named `access_level` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG access_level;
   ```
2. Create a join policy that evaluates the tag string value. Unrestricted access is allowed when the tag string value is `'open'`. If the
   tag string value is `'restricted'`, queries must include joins.

   > Copy code
   >
   > ```
   > USE ROLE join_policy_admin;
   > USE SCHEMA governance.join_policies;
   >
   > CREATE JOIN POLICY access_join_policy
   > AS () RETURNS JOIN_CONSTRAINT ->
   >  CASE
   >  WHEN SYSTEM$GET_TAG('governance.tags.access_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'CUSTOMER_DATA', 'TABLE') = 'open'
   >    THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE)
   >  WHEN SYSTEM$GET_TAG('governance.tags.access_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'CUSTOMER_DATA', 'TABLE') = 'restricted'
   >    THEN JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
   >  ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)
   >  END;
   > ```
   >
   > Note
   >
   > This policy uses the fully-qualified name for the tag in the function argument. Snowflake returns an error at query runtime if the
   > system function argument in the policy conditions contains a tag name that is not sufficiently qualified.
   >
   > For more information, see [Object name resolution](/sql-reference/name-resolution).
3. Assign the join policy to the `access_level` tag.

   Copy code

   ```
   ALTER TAG governance.tags.access_level SET JOIN POLICY access_join_policy;
   ```
4. Assign the `access_level` tag to the table with the tag string value `'restricted'`.

   Copy code

   ```
   ALTER TABLE partner.shared_data.customer_data
     SET TAG governance.tags.access_level = 'restricted';
   ```
5. Query the table to ensure Snowflake enforces join requirements based on the tag value.

   Copy code

   ```
   SELECT * FROM partner.shared_data.customer_data;
   ```

   The query fails because the tag value is ‘restricted’ and joins are required.
6. Change the tag value to `'open'` to allow unrestricted access:

   Copy code

   ```
   ALTER TABLE partner.shared_data.customer_data
     SET TAG governance.tags.access_level = 'open';

   SELECT * FROM partner.shared_data.customer_data;
   ```

   Now queries can return results without requiring joins because the tag value is ‘open’.

## Limitations and considerations

- If a join policy already protects a table or view and a tag-based join policy is also set on the same object, the directly assigned join
  policy takes precedence over the join policy assigned to the tag.
- A tag can have only one join policy.
- A policy cannot be assigned to a system tag.
- A table can’t be associated with more than one tag-based join policy.
- If a different type of data protection policy (for example, a masking policy) is assigned to a tag, you can’t attach a join policy to
  the same tag.
- A tag-based join policy can be applied to a table or view that is assigned other tag-based policies, for example, a tag-based projection
  policy. Query results reflect the cumulative effect of all policies when they are evaluated at runtime.
- Tag-based join policies interact with other Snowflake features the same as other join policies. See [join policies](/user-guide/join-policies#label-join-policy).
