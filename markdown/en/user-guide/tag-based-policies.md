# Attribute-based access control (ABAC) using tag-based policies

This topic provides an overview of attribute-based access control (ABAC) using tag-based data protection policies. With tag-based
policies, you can govern access using custom attributes or by bringing attributes from your external Active Directory (AD), such as
Microsoft Entra ID or Okta, using [Snowflake SCIM](/user-guide/scim-intro). A tag-based policy combines the
[object tagging](/user-guide/object-tagging/introduction) feature with data protection policies to allow a policy to be set on a
tag using an ALTER TAG command. When the tag is assigned to an object (database, schema, table, or column), the policy is automatically
applied to that object.

Tag-based policies simplify data protection management because objects that should be protected no longer need a policy manually applied.
Instead, you can define the policy once, assign it to a tag, and then apply the tag to objects that need protection. New objects that
inherit the tag are automatically protected.

## Supported tag-based policies

Snowflake supports the following tag-based data protection policies:

| Policy type | Description | Availability | Documentation |
| --- | --- | --- | --- |
| Masking policies | Protect column data by masking values based on conditions. | Generally available | [Tag-based masking policies](/user-guide/tag-based-masking-policies) |
| Aggregation policies | Require queries to aggregate data into groups of a minimum size. | Public preview | [Tag-based aggregation policies](/user-guide/tag-based-aggregation-policies) |
| Row access policies | Filter rows in a table or view based on conditions. | Public preview | [Tag-based row access policies](/user-guide/tag-based-row-access-policies) |
| Projection policies | Control whether a column can be projected (included) in query results. | Public preview | [Tag-based projection policies](/user-guide/tag-based-projection-policies) |
| Join policies | Control whether a column can be used as a join column. | Public preview | [Tag-based join policies](/user-guide/tag-based-join-policies) |

Expand

Show lessSee more

Tag-based aggregation, row access, projection, and join policies are in public preview:

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Benefits

Ease of use:
:   Assigning one or more policies to a tag is simple. Policy administrators can add or replace policies without breaking existing workflows.

Scalable:
:   Tag-based policies allow policy administrators to write a policy once, assign a policy to a tag once, and, depending on the
    [level](/user-guide/object-tagging/inheritance) at which the tag is set, have the policy apply to many objects. This significantly
    reduces the manual effort of assigning a single policy to individual objects every time a new object is created or replaced.

Comprehensive:
:   Policy administrators can create policies and assign them to a single tag. Once the tag is applied at the database, schema, or table
    level, objects within that scope are protected according to the policy conditions. Assigning a tag-based policy to a database, schema, or
    table automatically applies the policy to any new objects added to that scope.

Flexibility:
:   Tag-based policies offer an alternative to specifying the policy in DDL statements, which helps simplify object management. Administrators
    can choose to assign the policy either at object creation or by assigning the policy to the tag, which uses
    [tag inheritance](/user-guide/object-tagging/inheritance).

## Choose a database, schema, or table to assign the policy

Data engineers and data stewards can choose to assign the tag-based policy to a database, schema, table, or column.

Database and schema:
:   When you set a tag-based policy on a database or schema, you leverage [tag inheritance](/user-guide/object-tagging/inheritance) to
    protect tables and views in the schema or database.

    The main benefit of setting the tag-based policy on the database or schema is that objects in all newly added tables and views are
    automatically protected. This approach simplifies data protection management because it is no longer necessary to set tags on every table.
    The result is that the policy protects new data in Snowflake automatically.

Tables and views:
:   When you set a tag-based policy on a table or view, the tag is set on the object directly. Depending on the policy type, the protection
    applies to the entire object or its columns.

    When an object is protected by both a directly assigned policy and a tag-based policy of the same type, the directly assigned policy takes
    precedence. For aggregation policies, precedence applies only when the entity keys match; otherwise, both policies are enforced on the table
    or view.

## Understanding tag inheritance and propagation

If you apply a tag to a database or schema, the tag is inherited by all of the tables and views in the database or schema. This means that
a table or view is protected if the tag-based policy is set on its parent database or schema. For more information about tag inheritance,
see [Tag inheritance](/user-guide/object-tagging/inheritance).

When you define a tag, you can specify that you want the tag to be propagated to downstream objects. Propagation can occur when data moves
from an object to the downstream object or when the downstream object depends on a tagged object. If you configure your tag to propagate to
downstream objects, the tag-based policy protects those downstream objects automatically because they are associated with the same tag.
For more information about tag propagation, see [Tag propagation](/user-guide/object-tagging/propagation).

## General workflow for using tag-based policies

The general workflow for implementing tag-based policies is as follows:

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command or use an existing tag.
2. Create a policy using the appropriate CREATE command (for example, CREATE MASKING POLICY, CREATE ROW ACCESS POLICY).
3. Set the policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.

   For example:

   Copy code

   ```
   ALTER TAG my_tag SET MASKING POLICY my_masking_policy;
   ```
4. Set the tag on an object using one of the following commands:

   - [ALTER DATABASE](/sql-reference/sql/alter-database)
   - [ALTER SCHEMA](/sql-reference/sql/alter-schema)
   - [ALTER TABLE](/sql-reference/sql/alter-table)
   - [ALTER VIEW](/sql-reference/sql/alter-view)

   For example:

   Copy code

   ```
   ALTER TABLE my_table SET TAG my_tag = 'protected';
   ```
5. Query the data to verify that the tag-based policy protects the data as intended.

For detailed examples for each policy type, see the documentation for the specific tag-based policy.

## Example: Protect schema columns when an agent is active

This example assigns a masking policy that calls [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) to a tag and then assigns
the tag to a schema. Tag inheritance protects all table and view columns in the schema whose data types match the data types in the
policies. When an AI agent is active in the execution context, Snowflake masks the protected column values even if the user’s role would
otherwise allow viewing unmasked data.

Assume the following table exists:

> ```
> ---------------+----------------+
>   ACCOUNT_NAME | ACCOUNT_NUMBER |
> ---------------+----------------+
>   ACME         | 1000           |
> ---------------+----------------+
> ```

Protect the schema columns as follows:

1. Create a tag named `ai_governance` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG ai_governance;
   ```
2. Create different masking policies to protect the ACCOUNT\_NAME and ACCOUNT\_NUMBER columns. In each of these policies, Snowflake returns
   a masked value when an agent is active in the execution context. When no agent is active, only the `ACCOUNTING_ADMIN` custom role can
   view the raw data.

   Account name policy:

   Copy code

   ```
   USE ROLE masking_admin;
   USE SCHEMA governance.masking_policies;

   CREATE OR REPLACE MASKING POLICY account_name_agent_mask
   AS (val string) RETURNS string ->
     CASE
    WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE THEN NULL
    WHEN CURRENT_ROLE() IN ('ACCOUNTING_ADMIN') THEN val
    ELSE '***MASKED***'
     END;
   ```

   Account number policy:

   Copy code

   ```
   CREATE OR REPLACE MASKING POLICY account_number_agent_mask
   AS (val number) RETURNS number ->
     CASE
    WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE THEN NULL
    WHEN CURRENT_ROLE() IN ('ACCOUNTING_ADMIN') THEN val
    ELSE -1
     END;
   ```
3. Assign both masking policies to the `ai_governance` tag. Note that both policies can be assigned to the tag in a single statement.

   Copy code

   ```
   ALTER TAG governance.tags.ai_governance SET
     MASKING POLICY account_name_agent_mask,
     MASKING POLICY account_number_agent_mask;
   ```
4. Assign the `ai_governance` tag to the `finance.accounting` schema. Tag inheritance protects the columns in all tables and views in
   the schema when the column data type matches the data type in the masking policy.

   Copy code

   ```
   ALTER SCHEMA finance.accounting
     SET TAG governance.tags.ai_governance = 'agent-aware masking';
   ```
5. Verify the `ACCOUNT_NAME` and `ACCOUNT_NUMBER` table columns are protected by the tag-based masking policy by calling the
   Information Schema [POLICY\_REFERENCES](/sql-reference/functions/policy_references) table function.

   For each protected column, the row in the query result should specify the appropriate values for the column name, policy name, and tag
   name:

   Copy code

   ```
   USE ROLE masking_admin;
   SELECT *
   FROM TABLE (governance.INFORMATION_SCHEMA.POLICY_REFERENCES(
     REF_ENTITY_DOMAIN => 'TABLE',
     REF_ENTITY_NAME => 'finance.accounting.name_number' )
   );
   ```
6. Query the table columns to verify the tag-based masking policy protects the data as intended.

   When no agent is active, users with the `ACCOUNTING_ADMIN` custom role see unmasked data and users with other roles see masked data:

   Copy code

   ```
   USE ROLE accounting_admin;
   SELECT * FROM finance.accounting.name_number;
   ```

   Returns:

   ```
   ---------------+----------------+
     ACCOUNT_NAME | ACCOUNT_NUMBER |
   ---------------+----------------+
     ACME         | 1000           |
   ---------------+----------------+
   ```

   When an agent is active in the execution context, Snowflake returns `NULL` for both columns even when the query runs with the
   `ACCOUNTING_ADMIN` custom role.

For more about using agent identity in data protection policies, see
[Data protection policies for agentic interactions](/user-guide/data-protection-policies-snowsight#label-data-protection-policies-agentic).

## Tag and policy discovery

The Information Schema table function [POLICY\_REFERENCES](/sql-reference/functions/policy_references) can help determine whether a
policy and a tag reference each other by looking at the following columns:

- TAG\_DATABASE
- TAG\_SCHEMA
- TAG\_NAME
- POLICY\_STATUS

The POLICY\_STATUS column indicates the status of the tag-based policy assignment.

You can use the Account Usage [TAG\_REFERENCES](/sql-reference/account-usage/tag_references) view to identify all tags and their
assigned string values.

### Query tag-based policy assignments

To verify tag-based policy assignments for a table, call the POLICY\_REFERENCES table function:

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_DOMAIN => 'TABLE',
  REF_ENTITY_NAME => 'my_database.my_schema.my_table'
));
```

For each protected object or column, the row in the query result specifies the policy name, tag name, and policy status.

### Query tag assignments

To view all tags assigned to objects in your account, query the TAG\_REFERENCES view:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
WHERE TAG_NAME = 'my_tag';
```

## Access control requirements

The following general privileges apply to tag-based policies:

| Task | Required privileges |
| --- | --- |
| Create a tag | CREATE TAG on the schema |
| Create a policy | CREATE <POLICY\_TYPE> on the schema (for example, CREATE MASKING POLICY) |
| Set a policy on a tag | APPLY <POLICY\_TYPE> on the account (for example, APPLY MASKING POLICY) |
| Set a tag on a database or schema | APPLY TAG on the account, or APPLY on the specific tag |
| Set a tag on a table or view | APPLY TAG on the account, or APPLY on the specific tag |
| Unset a policy from a tag | APPLY <POLICY\_TYPE> on the account |

Expand

Show lessSee more

For detailed access control requirements for each policy type, see:

- [Tag-based masking policies: Privilege](/user-guide/tag-based-masking-policies#privilege)
- [Tag-based aggregation policies: Access control requirements](/user-guide/tag-based-aggregation-policies#label-tag-based-agg-access-control)
- [Tag-based row access policies: Access control requirements](/user-guide/tag-based-row-access-policies#label-tag-based-rap-access-control)
- [Tag-based projection policies: Access control requirements](/user-guide/tag-based-projection-policies#label-tag-based-pp-access-control)
- [Tag-based join policies: Access control requirements](/user-guide/tag-based-join-policies#label-tag-based-join-access-control)

## General considerations

The following considerations apply to all tag-based policies:

- If an object or column is protected by both a directly assigned policy and a tag-based policy, the directly assigned policy takes
  precedence.
- For aggregation policies, the directly assigned policy takes precedence only when its entity keys match those of the tag-based policy;
  otherwise, both policies are enforced on the table or view.
- A tag cannot be [dropped](/sql-reference/sql/drop-tag) if a policy is assigned to it.
- A policy cannot be dropped if it is assigned to a tag.
- A database or schema cannot be dropped if it contains a tag with a policy, or if it contains a policy that is set on a tag.
- A policy cannot be assigned to a [system tag](/user-guide/classify-intro#label-classify-classification-tags).

For policy-specific considerations and limitations, see the documentation for each tag-based policy type.

## Next steps

To learn more about specific tag-based policy types, see:

- [Tag-based masking policies](/user-guide/tag-based-masking-policies) — Protect column data by masking values.
- [Tag-based aggregation policies](/user-guide/tag-based-aggregation-policies) — Require queries to aggregate data into groups.
- [Tag-based row access policies](/user-guide/tag-based-row-access-policies) — Filter rows based on conditions.
- [Tag-based projection policies](/user-guide/tag-based-projection-policies) — Control whether columns can be projected.
- [Tag-based join policies](/user-guide/tag-based-join-policies) — Control whether columns can be used as join columns.
