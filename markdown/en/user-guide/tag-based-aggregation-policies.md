# Tag-based aggregation policies

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

An [aggregation policy](/user-guide/aggregation-policies) is a schema-level object that controls what type of query can access data from
a table or view. When an aggregation policy is applied to a table, queries against that table must aggregate data into groups of a minimum
size in order to return results. A [tag](/user-guide/object-tagging/introduction) is a schema-level object that can be assigned to
another object, including databases, schemas, tables, and views. *Tag-based aggregation policies* combine the object tagging and
aggregation policy features to allow an aggregation policy to be set on a tag using an ALTER TAG command.

When an aggregation policy is set on a tag, a table or view is protected by the policy when the tag is set on the object or on a parent
database or schema. Tables protected by a tag-based aggregation policy require queries to aggregate data in the same way as tables with
directly assigned aggregation policies.

You can create the body of the aggregation policy to require aggregation based on the current user’s role (like a regular aggregation
policy) or you can control aggregation requirements based on the value of the tag that is associated with the policy. For examples of these
two strategies, see [Extended examples](#label-tag-based-agg-examples).

For tag inheritance and propagation, see [Understanding tag inheritance and propagation](/user-guide/tag-based-policies#label-tag-based-policies-inheritance) in [Attribute-based access control (ABAC) using tag-based policies](/user-guide/tag-based-policies).

## Before you begin

Before you implement tag-based aggregation policies, you should determine how tags and aggregation policies are currently being used in your
account. Use the following steps:

1. Identify the existing tags and their string values in your Snowflake account.

   - Query the Account Usage [TAG REFERENCES](/sql-reference/account-usage/tag_references) view to obtain all tags and their assigned
     string values.
   - Optionally, query the Account Usage [TAGS](/sql-reference/account-usage/tags) view to obtain a list of tags to ensure that
     duplicate tag naming doesn’t occur later while using tag-based aggregation policies.
   - Optionally, compare the outputs from the TAG\_REFERENCES and TAGS queries to determine if there are any unassigned tags that can be used
     later.
2. Identify the existing policies and their definitions in your Snowflake account.

   - Run the [SHOW AGGREGATION POLICIES](/sql-reference/sql/show-aggregation-policies) command to obtain a list of existing aggregation policies.
   - Decide whether these policies, in their current form, can be assigned to tags. If necessary, run the
     [DESCRIBE AGGREGATION POLICY](/sql-reference/sql/desc-aggregation-policy) command to obtain the policy definition.

## Workflow for using a tag-based aggregation policy

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command or use an existing tag.
2. Create an aggregation policy using the [CREATE AGGREGATION POLICY](/sql-reference/sql/create-aggregation-policy) command or use an existing policy.
3. Set the aggregation policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.

   Copy code

   ```
   ALTER TAG [ IF EXISTS ] <tag_name> SET AGGREGATION POLICY <policy_name>
     [ ENTITY KEY ( <col_name> [ , ... ] ) ] ... ;
   ```

   For example:

   Copy code

   ```
   ALTER TAG sensitive_data SET AGGREGATION POLICY privacy_policy;
   ```

   When you apply the tag to a table, any query that groups rows from that table must return at least the minimum group size defined in the
   policy. Smaller groups are suppressed.

   Optionally, specify one or more `ENTITY KEY` clauses when you attach the policy to define which columns Snowflake counts distinct values
   for. For more information, see [Entity keys](#label-tag-based-agg-entity-keys) (in this topic).
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
5. Query the data to verify that the tag-based aggregation policy protects the data as intended.

For end-to-end examples of this workflow, see [Extended examples](#label-tag-based-agg-examples).

## Remove an aggregation policy from a tag

To remove an aggregation policy from a tag, use the ALTER TAG statement with the UNSET AGGREGATION POLICY clause:

Copy code

```
ALTER TAG [ IF EXISTS ] <tag_name> UNSET AGGREGATION POLICY <policy_name>;
```

For example:

Copy code

```
ALTER TAG sensitive_data UNSET AGGREGATION POLICY privacy_policy;
```

The policy is removed from the tag. Tables that carry this tag no longer enforce the policy unless they have a directly assigned
aggregation policy.

## Entity keys

An entity key specifies which column or columns Snowflake uses to count distinct values in each aggregation group, in addition to the row
count threshold defined in the policy. For example, instead of requiring at least five rows per group, a policy can require at least five
distinct `user_id` values per group. For general background on entity keys, see
[Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy).

When you attach an aggregation policy to a tag, use the optional `ENTITY KEY` clause on the `ALTER TAG ... SET AGGREGATION POLICY`
statement to define one or more entity keys for that attachment.

### Single-column entity key

The following example attaches a policy that requires a minimum group size of five and defines `user_id` as the entity key:

Copy code

```
CREATE AGGREGATION POLICY user_privacy
  AS () RETURNS AGGREGATION_CONSTRAINT ->
    AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);

ALTER TAG sensitive_data SET AGGREGATION POLICY user_privacy ENTITY KEY (user_id);

ALTER TABLE transactions SET TAG sensitive_data = 'user_pii';
```

When you query `transactions`, each result group must contain at least five distinct `user_id` values. If a table doesn’t have a
`user_id` column, the policy doesn’t enforce on that table.

### Composite entity key

To require distinct combinations of multiple columns, specify those columns in a single `ENTITY KEY` clause:

Copy code

```
ALTER TAG campaign_tag SET AGGREGATION POLICY user_privacy
  ENTITY KEY (user_id, campaign_id);
```

Groups must contain at least five distinct (`user_id`, `campaign_id`) pairs. Both columns must exist on the table for the policy to
enforce.

### Multiple entity keys in one statement

You can specify multiple `ENTITY KEY` clauses in a single `ALTER TAG` statement:

Copy code

```
ALTER TAG multi_dim SET AGGREGATION POLICY privacy_policy
  ENTITY KEY (user_id)
  ENTITY KEY (campaign_id);
```

For the policy to enforce on a table, **all** entity key columns from **all** clauses must exist on that table. If the table has only
`user_id` and not `campaign_id`, the policy doesn’t enforce on that table at all, including the `user_id` dimension.

To allow tables with only some of the columns to still receive protection, use separate tags with separate attachments:

Copy code

```
ALTER TAG user_tag SET AGGREGATION POLICY privacy_policy ENTITY KEY (user_id);
ALTER TAG campaign_tag SET AGGREGATION POLICY privacy_policy ENTITY KEY (campaign_id);
```

Tables with only `user_id` enforce the user dimension. Tables with both columns can carry both tags to enforce both dimensions. See
[Cross-tag behavior](#label-tag-based-agg-cross-tag) (in this topic).

## Cross-tag behavior

A table or view can inherit multiple tags, each with its own tag-based aggregation policy attachment. Snowflake evaluates unique
combinations of policy and entity key when more than one tag applies to the same object.

### Same policy and entity key on multiple tags

If the same aggregation policy is attached to multiple tags with the same entity key, and all of those tags are set on the same table,
Snowflake enforces the policy once. Deduplication is based on the unique tuple of policy and entity keys.

Copy code

```
ALTER TAG tag1 SET AGGREGATION POLICY privacy_policy ENTITY KEY (user_id);
ALTER TAG tag2 SET AGGREGATION POLICY privacy_policy ENTITY KEY (user_id);

ALTER TABLE sales SET TAG tag1 = 'v1';
ALTER TABLE sales SET TAG tag2 = 'v2';
```

The policy enforces once on `sales`, not twice.

### Different policies with the same entity key

If different aggregation policies are attached to different tags but use the same entity key tuple, and all of those tags apply to the same
table, Snowflake returns a runtime error at query time because it can’t determine which policy’s threshold applies:

Copy code

```
ALTER TAG tag1 SET AGGREGATION POLICY policy_min3 ENTITY KEY (user_id);
ALTER TAG tag2 SET AGGREGATION POLICY policy_min5 ENTITY KEY (user_id);

ALTER TABLE sales SET TAG tag1 = 'v1';
ALTER TABLE sales SET TAG tag2 = 'v2';
```

To avoid this error, use the same policy object on both tags, or use different entity keys.

### Different entity keys on multiple tags

When different tags specify different entity keys for the same policy, Snowflake enforces each entity key constraint conjunctively:

Copy code

```
ALTER TAG tag1 SET AGGREGATION POLICY privacy_policy ENTITY KEY (user_id);
ALTER TAG tag2 SET AGGREGATION POLICY privacy_policy ENTITY KEY (campaign_id);

ALTER TABLE sales SET TAG tag1 = 'v1';
ALTER TABLE sales SET TAG tag2 = 'v2';
```

Result groups must satisfy both constraints: at least five distinct `user_id` values and at least five distinct `campaign_id` values.

## Replace an aggregation policy on a tag

You have two options to replace the aggregation policy for a tag-based policy with a different aggregation policy.

Option 1:
:   Unset the policy from a tag in one statement and then set a new policy on the tag in a different statement:

    Copy code

    ```
    ALTER TAG security UNSET AGGREGATION POLICY agg_policy_1;

    ALTER TAG security SET AGGREGATION POLICY agg_policy_2;
    ```

Option 2:
:   Use the `FORCE` keyword to replace the policy in a single statement.

    > Copy code
    >
    > ```
    > ALTER TAG security SET AGGREGATION POLICY agg_policy_2 FORCE;
    > ```

Important

Exercise caution when replacing an aggregation policy on a tag.

Depending on the timing of the replacement and queries on the protected objects, choosing to replace the policy in two separate statements
could lead to data exposure because the table or view data is unprotected in the time interval between the UNSET and SET operations.

However, if the policy conditions in the replacement policy differ from those in the original policy, specifying the `FORCE` keyword
could lead to a lack of access because (previously) users could access data and the replacement no longer allows access.

Prior to replacing a policy, consult your internal data administrators to coordinate the best approach to protect data with tag-based
aggregation policies and replace aggregation policies as needed.

## Deleting tag-based aggregation policies

The following restrictions apply when attempting to delete a tag-based aggregation policy:

- A tag can’t be [dropped](/sql-reference/sql/drop-tag) if it is assigned to an aggregation policy.
- An aggregation policy can’t be [dropped](/sql-reference/sql/drop-aggregation-policy) if it is assigned to a tag.
- A database or schema can’t be dropped if it contains a tag with an aggregation policy.
- A database or schema can’t be dropped if it contains an aggregation policy that is set on a tag.

To delete either the tag or the aggregation policy, you must first run an ALTER TAG … UNSET AGGREGATION POLICY command to remove the
association between the tag and policy.

## Update a tag value

If a schema owner (for example, `sch_role`) sets a tag on a schema and then a different role sets an aggregation policy on the same tag
(for example, `agg_admin_role`), the schema owner can’t change the tag value. Snowflake fails the ALTER SCHEMA … SET TAG operation for
the schema owner.

To change the tag value, you must do the following:

1. Using the `agg_admin_role`, unset the aggregation policy from the tag.
2. Using the `sch_role`, modify the tag value.
3. Using the `agg_admin_role`, reassign the aggregation policy to the tag.

## Access control requirements

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Set an aggregation policy on a tag | APPLY AGGREGATION POLICY on the account |  |
| Set a tag-based aggregation policy on a database/schema | - APPLY AGGREGATION POLICY on the account - One of the following:   - GRANT APPLY TAG on the account   - GRANT APPLY on the tag |  |
| Set a tag-based aggregation policy on a table/view | One of the following:   - GRANT APPLY TAG on the account - GRANT APPLY on the tag |  |
| Unset an aggregation policy from a tag | APPLY AGGREGATION POLICY on the account |  |

Expand

Show lessSee more

### Privileges for tag owners

A tag owner must have the APPLY AGGREGATION POLICY privilege to unset an aggregation policy from the tag.

In some cases, tag owners can work with tag-based aggregation policies without having the APPLY AGGREGATION POLICY privilege. If your role has
the OWNERSHIP or APPLY privilege on a tag that has an aggregation policy set on it, you can apply the tag to your table or view without the
APPLY AGGREGATION POLICY privilege. However, you still need the APPLY AGGREGATION POLICY privilege to apply the same tag to a database or
schema.

## Extended examples

- [Common assumptions with the examples](#common-assumptions-with-the-examples)
- [Example 1: Protect table data based on the aggregation policy assigned to the tag](#example-1-protect-table-data-based-on-the-aggregation-policy-assigned-to-the-tag)
- [Example 2: Protect table data based on the tag string value](#example-2-protect-table-data-based-on-the-tag-string-value)

### Common assumptions with the examples

The examples in this section make the following assumptions:

- The prerequisite steps were completed.
- The `tag_admin` custom role has the following privileges:

  - The schema-level CREATE TAG privilege.
  - The global APPLY TAG privilege.

  For more information, see [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `aggregation_admin` custom role has the following privileges:

  - The schema-level CREATE AGGREGATION POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.aggregation_policies` schema.
  - The global APPLY AGGREGATION POLICY privilege to assign aggregation policies to tags.
  - The global APPLY TAG privilege, to assign the tag (with the aggregation policies) to objects.

  For more information, see [aggregation policy privileges](/user-guide/aggregation-policies#label-aggregation-policy-ddl-privilege-summary).
- The `data_admin` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The `analyst` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and on the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The custom roles described above are granted to the appropriate users.

  For details, see [Configuring access control](/user-guide/security-access-control-configure).

### Example 1: Protect table data based on the aggregation policy assigned to the tag

This example assigns an aggregation policy to a tag and then assigns the tag to a table. The result is that the aggregation policy requires
queries to aggregate data into groups of a minimum size.

The following steps create a tag-based aggregation policy to protect employee data. For example, consider the table named
`hr.employees.salaries`, which has multiple columns including `DEPARTMENT`, `EMPLOYEE_ID`, and `SALARY`.

> ```
> +------------+-------------+--------+
> | DEPARTMENT | EMPLOYEE_ID | SALARY |
> +------------+-------------+--------+
> | Engineering| 1001        | 95000  |
> | Engineering| 1002        | 98000  |
> | Engineering| 1003        | 92000  |
> | Sales      | 2001        | 85000  |
> | Sales      | 2002        | 88000  |
> +------------+-------------+--------+
> ```

Create a tag-based aggregation policy to protect the table as follows:

1. Create a tag named `privacy_protection` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG privacy_protection;
   ```
2. Create an aggregation policy that requires a minimum group size of 3 for most users, but allows unrestricted access for the DATA\_ADMIN
   role.

   Copy code

   ```
   USE ROLE aggregation_admin;
   USE SCHEMA governance.aggregation_policies;

   CREATE OR REPLACE AGGREGATION POLICY employee_agg_policy
   AS () RETURNS AGGREGATION_CONSTRAINT ->
    CASE
    WHEN CURRENT_ROLE() = 'DATA_ADMIN' THEN NO_AGGREGATION_CONSTRAINT()
    ELSE AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 3)
    END;
   ```
3. Assign the aggregation policy to the `privacy_protection` tag.

   Copy code

   ```
   ALTER TAG governance.tags.privacy_protection SET AGGREGATION POLICY employee_agg_policy;
   ```
4. Assign the `privacy_protection` tag to the `hr.employees.salaries` table.

   Copy code

   ```
   ALTER TABLE hr.employees.salaries
     SET TAG governance.tags.privacy_protection = 'protected';
   ```
5. Query the table to verify the tag-based aggregation policy protects the data as intended.

   Copy code

   ```
   USE ROLE analyst;
   SELECT department, AVG(salary) AS avg_salary
   FROM hr.employees.salaries
   GROUP BY department;
   ```

   Returns aggregated results where each group has at least 3 rows. The Engineering department has 3 employees, so its average is returned
   directly. The Sales department has only 2 employees, so it may be combined into a remainder group.

   Copy code

   ```
   USE ROLE data_admin;
   SELECT * FROM hr.employees.salaries;
   ```

   The query succeeds for the `data_admin` role, returning all rows without aggregation requirements.

### Example 2: Protect table data based on the tag string value

This example uses a tag-based aggregation policy to determine aggregation requirements based on the string value of the tag assigned
to a table. The aggregation policy dynamically evaluates the tag string value by calling the [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag)
function in the aggregation policy conditions.

The following steps create a tag-based aggregation policy to protect data:

1. Create a tag named `sensitivity_level` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG sensitivity_level;
   ```
2. Create an aggregation policy that evaluates the tag string value. Unrestricted access is allowed when the tag string value is `'public'`.
   If the tag string value is `'confidential'`, queries must aggregate with a minimum group size of 5.

   > Copy code
   >
   > ```
   > USE ROLE aggregation_admin;
   > USE SCHEMA governance.aggregation_policies;
   >
   > CREATE AGGREGATION POLICY sensitivity_agg_policy
   > AS () RETURNS AGGREGATION_CONSTRAINT ->
   >  CASE
   >  WHEN SYSTEM$GET_TAG('governance.tags.sensitivity_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'SALARIES', 'TABLE') = 'public'
   >    THEN NO_AGGREGATION_CONSTRAINT()
   >  WHEN SYSTEM$GET_TAG('governance.tags.sensitivity_level',
   >                      CURRENT_DATABASE() || '.' || CURRENT_SCHEMA() || '.' ||
   >                      'SALARIES', 'TABLE') = 'confidential'
   >    THEN AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5)
   >  ELSE AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 3)
   >  END;
   > ```
   >
   > Note
   >
   > This policy uses the fully-qualified name for the tag in the function argument. Snowflake returns an error at query runtime if the
   > system function argument in the policy conditions contains a tag name that is not sufficiently qualified.
   >
   > For more information, see [Object name resolution](/sql-reference/name-resolution).
3. Assign the aggregation policy to the `sensitivity_level` tag.

   Copy code

   ```
   ALTER TAG governance.tags.sensitivity_level SET AGGREGATION POLICY sensitivity_agg_policy;
   ```
4. Assign the `sensitivity_level` tag to the table with the tag string value `'confidential'`.

   Copy code

   ```
   ALTER TABLE hr.employees.salaries
     SET TAG governance.tags.sensitivity_level = 'confidential';
   ```
5. Query the table to ensure Snowflake returns the correct query result based on the tag value.

   Copy code

   ```
   SELECT department, AVG(salary) AS avg_salary
   FROM hr.employees.salaries
   GROUP BY department;
   ```

   Queries must aggregate data with a minimum group size of 5 because the tag value is ‘confidential’.
6. Change the tag value to `'public'` to allow unrestricted access:

   Copy code

   ```
   ALTER TABLE hr.employees.salaries
     SET TAG governance.tags.sensitivity_level = 'public';

   SELECT * FROM hr.employees.salaries;
   ```

   Now queries can return results without aggregation requirements because the tag value is ‘public’.

## Limitations and considerations

- If an aggregation policy already protects a table or view and a tag-based aggregation policy is also set on the same object, the
  directly assigned aggregation policy takes precedence only when its entity keys are identical to those of the tag-based policy. If the
  entity keys differ, both policies can be enforced on the table or view.
- A tag can have only one aggregation policy. You can’t attach a second aggregation policy to the same tag, even with a different entity
  key.
- A policy can’t be assigned to a system tag.
- When multiple tags with tag-based aggregation policies apply to the same table or view, see
  [Cross-tag behavior](#label-tag-based-agg-cross-tag) (in this topic).
- If a different type of data protection policy (for example, a masking policy) is assigned to a tag, you can’t attach an aggregation
  policy to the same tag.
- A tag-based aggregation policy can be applied to a table or view that is assigned other tag-based policies, for example, a tag-based
  projection policy. Query results reflect the cumulative effect of all policies when they are evaluated at runtime.
- Tag-based aggregation policies interact with other Snowflake features the same as other aggregation policies. See [aggregation policies](/user-guide/aggregation-policies#label-aggregation-policies).
