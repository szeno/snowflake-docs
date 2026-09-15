# Tag-based masking policies

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides concepts about tag-based masking policies and examples of tag-based masking policies to protect column data.

## Overview

A tag-based masking policy combines the object tagging and masking policy features to allow a masking policy to be set on a tag using an
ALTER TAG command. When the data type in the masking policy signature and the data type of the column match, the tagged column is
automatically protected by the conditions in the masking policy. This simplifies the data protection efforts because column data that
should be protected no longer needs a masking policy manually applied to the column to protect the data. You can set a tag-based masking
policy on a database, schema, or table.

The tag can support one masking policy for each [data type](/sql-reference-data-types) that Snowflake supports. To simplify the
initial column data protection efforts, create a generic masking policy for each data type (e.g. STRING, NUMBER, TIMESTAMP\_LTZ) that allows
authorized roles to see the raw data and unauthorized roles to see a fixed masked value.

The masking policy conditions can be written to protect the column data based on the policy assigned to the tag or protect the column data
based on the tag string value of the tag assigned to the column, depending upon the decisions of the policy administrator, tag
administrator, and data steward.

## Choose a database, schema, or table to assign the policy

Data engineers and data stewards can choose to assign the tag-based masking policy to a database, schema, table, or column.

Database & Schema:
:   When you set a tag-based masking policy on a database or schema, you leverage [tag inheritance](#label-tag-based-masking-lineage) to
    protect table and view columns in the schema or database. Setting a tag-based masking policy on the database or schema protects the
    columns in that database or schema when the data type of the column matches the data type of the masking policy that is
    set on the tag.

    The main benefit of setting the tag-based masking policy on the database or schema is that the columns in all newly added tables and
    views are automatically protected when the column data type matches the masking policy data type. This approach simplifies data
    protection management because it is no longer necessary to set tags on every table. The result is that the policy protects new data in
    Snowflake until a data protection officer decides to assign either a masking policy to the column directly or a row
    access policy to the table or view.

Tables:
:   When you set a tag-based masking policy on a table, the tag is set on all columns in the table. The masking policy protects the column
    data when the data type of the column matches the data type of the masking policy.

    A column can be protected by a masking policy directly assigned to the column and a tag-based masking policy. If both policies protect the
    same column, the masking policy that is directly assigned to the column takes precedence over the tag-based masking policy.

For examples of tag-based masking policies, refer to the [Use Tag-Based Masking Policies](#use-tag-based-masking-policies) section (in this topic).

## Benefits

Ease of Use:
:   Assigning one or more masking policies to a tag is simple. Policy administrators can add or replace policies without breaking
    existing workflows.

Scalable:
:   Tag-based policies allow policy administrators to write a policy once, assign a policy to a tag once, and, depending on the
    [level](/user-guide/object-tagging/inheritance#label-object-tagging-lineage) at which the tag is set, have the policy apply to many objects. This results in the vast
    reduction of manually assigning a single policy to a single column every time a new column is created or replaced.

Comprehensive:
:   Policy administrators can create a policy for each data type and assign all of those policies to a single tag. Once the tag is applied at
    the table level, all columns in the table are protected, provided that the column data type matches the data type specified in the policy.

Protect future objects:
:   Assigning a tag-based masking policy to a table automatically applies the masking policy to any new table columns. This behavior is
    analogous to [future grants](/sql-reference/sql/grant-privilege).

Flexibility:
:   Tag-based masking policies offer an alternative to specifying the masking policy in a [CREATE TABLE](/sql-reference/sql/create-table) statement,
    which helps to simplify table DDL management. Administrators can choose to assign the masking policy either at table creation or by
    assigning the policy to the tag, which uses [tag inheritance](/user-guide/object-tagging/inheritance#label-object-tagging-lineage).

## Considerations

- For a tag-based masking policy where the tag is stored in a different schema than the masking policy and table, cloning the schema
  containing the masking policy and table results in the cloned table being protected by the masking policy in the source schema not the
  cloned schema.

  However, for a tag-based masking policy where the tag, masking policy, and table all exist in the schema, cloning the schema results in the
  table being protected by the masking policy in the cloned schema, not the source schema.

  If the table is cloned or moved to a different schema or database and was originally protected by a tag-based masking policy set on the
  schema or database, the table is not protected by the tag-based masking policy set on the source schema or database. The table is
  protected by the tag-based masking policy set on the target schema or database, if there is a tag-based masking policy set on the target
  schema or database.

- Regarding replication and tag-based masking policies, see
  [policy replication considerations](/user-guide/database-replication-considerations#label-database-replication-considerations-masking-row-policies).
- For details about [Secure Data Sharing](/user-guide/data-sharing-gs) and this feature, see:
  - [Masking Policies & Data Sharing](/user-guide/security-column-intro#label-security-column-intro-data-sharing)
  - [Object Tagging & Data Sharing](/user-guide/object-tagging/interaction#label-object-tagging-data-sharing)

## Limitations

All of the existing [masking policy limitations](/user-guide/security-column-intro#label-security-column-limitations) apply to tag-based masking policies.

Note the following additional limitations when using tag-based masking policies:

Data types:
:   A tag can support one masking policy for each data type. For example, if a tag already has a masking policy for the NUMBER data type, you
    cannot assign another masking policy with the NUMBER data type to the same tag.

System tags:
:   A masking policy cannot be assigned to a [system tag](/user-guide/classify-intro#label-classify-classification-tags).

Dropping objects:
:   Neither the masking policy nor the tag can be dropped if the masking policy is assigned to a tag. Similarly, the parent schema and
    database containing the tag and the masking policy cannot be dropped if the policy is assigned to a tag. For more information,
    see [Assign a masking policy to a tag](#label-tag-masking-assignment) (in this topic).

Materialized views:
:   A materialized view cannot be created if the underlying table is protected by a tag-based masking policy. For additional details,
    see [masking policies and materialized views](/user-guide/security-column-intro#label-security-column-intro-mv).

    If a materialized view exists and a tag-based masking policy is added to the underlying table later, the materialized view cannot
    be queried; the materialized view is now invalidated. To continue using the materialized view, unset the tag-based masking
    policy, recreate or [resume](/sql-reference/sql/alter-materialized-view), and then query the materialized view.

Semantic views:
:   Tag-based masking policies are not supported for tags directly applied to semantic views and attributes of those views (logical
    tables, dimensions, facts, and metrics).

    To use a tag-based masking policy on a semantic view, set the tag on the base table or on a column in the base table.

    For example, suppose that you have assigned a masking policy `my_masking_policy` to the tag `security`:

    Copy code

    ```
    ALTER TAG security SET MASKING POLICY my_masking_policy;
    ```

    Suppose that you have a semantic view that uses a logical table containing data or a column that you want to mask:

    Copy code

    ```
    CREATE OR REPLACE SEMANTIC VIEW sv_mask_example
      TABLES (
        my_logical_table AS my_base_table
      )
      METRICS (
        my_logical_table.my_col_count AS SUM(my_logical_table.my_col)
      );
    ```

    To apply the tag-based masking policy to the semantic view, apply the tag to the base table or a column in the base table:

    Copy code

    ```
    ALTER TABLE my_base_table SET TAG security = 'tag-based policies';
    ```

    Copy code

    ```
    ALTER TABLE my_base_table
      MODIFY COLUMN my_col SET TAG security = 'tag-based policies';
    ```

Row access policies:
:   A given table or view column can be specified in either a masking policy signature or a row access policy signature.
    In other words, the same column cannot be specified in both a masking policy signature and a row access policy signature at the same time.

Conditional columns:
:   A masked column cannot be used as a conditional column in a masking policy.

Mapping tables:
:   A table containing a column protected by a tag-based masking policy cannot be used as a mapping table.

Snowflake Native App Framework:
:   For details about using tag-based masking policies with a Snowflake Native App, see:

    - [Restrictions on sharing data content that contains policies](/developer-guide/native-apps/preparing-data-content#label-native-apps-share-policy-protected-data).
    - [Define policies on proxy views](/developer-guide/native-apps/preparing-data-content#label-native-apps-policies-proxy-views).
    - [Blocked context functions](/developer-guide/native-apps/redacted-content#label-native-apps-context-function-limitations).

## Manage tag-based masking policies

The existing privileges for masking policies and tags, along with the commands to manage masking policies and tags, apply to tag-based
masking policies.

### Privilege

There are different privilege requirements depending on whether you choose to set the tag-based masking policy on a
database, schema, or table.

With tag-based masking on a database or schema, the current role or a role in the current role hierarchy must inherit the privileges as
shown in either of the following two options.

Option 1:
:   The role must have both the global APPLY MASKING POLICY and the global APPLY TAG privileges. For example, grant these privileges to the
    `data_engineer` custom role:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;

    GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE data_engineer;

    GRANT APPLY TAG ON ACCOUNT TO ROLE data_engineer;
    ```

    This is the most [centralized approach](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary) to protect columns with a tag-based masking policy
    in a schema or database.

Option 2:
:   A schema owner (i.e. a role with the OWNERSHIP privilege on the schema) can have the global APPLY MASKING POLICY privilege and the
    APPLY privilege on the tag. For example, if the tag is named `governance.tags.schema_mask` and the custom role that owns the schema
    is `schema_owner`:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;

    GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE schema_owner;

    GRANT APPLY ON TAG governance.tags.schema_mask TO ROLE schema_owner;
    ```

    This approach provides more flexibility by delegating column protection to schema owners.

With tag-based masking on tables and views, a role with the global APPLY MASKING POLICY privilege can assign and replace a masking policy
on a tag.

For example, grant the global APPLY MASKING POLICY privilege to the `tag_admin` custom role:

> Copy code
>
> ```
> USE ROLE SECURITYADMIN;
>
> GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE tag_admin;
> ```

#### Privileges for tag owners

A tag owner must have the APPLY MASKING POLICY privilege to unset a masking policy from the tag.

In some cases, tag owners can work with tag-based masking policies without having the APPLY MASKING POLICY privilege. If your role has the
OWNERSHIP or APPLY privilege on a tag that has a masking policy set on it, then you can apply the tag to your table or view without the
APPLY MASKING POLICY privilege. However, you’d still need the APPLY MASKING POLICY privilege to apply the same tag to a database or schema.

### Assign a masking policy to a tag

Assigning a tag-based masking policy on a schema or database follows the same procedure as setting a tag-based masking policy on a
table:

1. Create a tag using the [CREATE TAG](/sql-reference/sql/create-tag) command.
2. Create a masking policy using the [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy) command.

   You can optionally use the [SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) and
   [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table) system functions in the masking policy conditions.
3. Set the masking policy on the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) command.
4. Set the tag on the object based on how you want to protect your data using one of the following commands:

   - [ALTER DATABASE](/sql-reference/sql/alter-database)
   - [ALTER SCHEMA](/sql-reference/sql/alter-schema)
   - [ALTER TABLE](/sql-reference/sql/alter-table)

Tip

To avoid conflicts with tags and masking policies when setting a tag-based masking policy on a schema or database, prior to
assigning the tag-based masking policy:

- Query the Account Usage TAG\_REFERENCES view to verify the existing tags set on a table or a column in a table.
- Query the Account Usage POLICY\_REFERENCES view to determine if a tag-based masking policy is set on a table or a column. For details,
  refer to [Tag and policy discovery](#label-tag-based-masking-discovery).

In addition to the ALTER TAG usage notes, note the following:

- A tag can have only one masking policy per data type. For example, one policy for the STRING data type, one policy for NUMBER data type,
  and so on.
- If a masking policy already protects a column and a tag-based masking policy is also set on the same column, the directly assigned masking
  policy takes precedence over the masking policy assigned to the tag.
- A tag cannot be [dropped](/sql-reference/sql/drop-tag) if it is assigned to a masking policy.
- A masking policy cannot be [dropped](/sql-reference/sql/drop-masking-policy) if it is assigned to a tag.

For more information on managing masking policies and tags, see:

- [Managing Column-level Security](/user-guide/security-column-intro#label-security-column-manage)
- [Access control privileges](/user-guide/object-tagging/work#label-object-tags-privileges)

### Replace a masking policy on a tag

After setting a masking policy on a tag, there are two different pathways to replace the masking policy on the tag with a different
masking policy. The ALTER TAG statement must specify the masking policy name as shown in the following options.

Option 1:
:   Unset the policy from a tag in one statement and then set a new policy on the tag in a different statement:

    Copy code

    ```
    ALTER TAG security UNSET MASKING POLICY ssn_mask;

    ALTER TAG security SET MASKING POLICY ssn_mask_2;
    ```

Option 2:
:   Use the `FORCE` keyword to replace the policy in a single statement.

    Note that using the `FORCE` keyword replaces the policy when a policy of the same [data type](/sql-reference-data-types) is
    already set on the tag.

    > Copy code
    >
    > ```
    > ALTER TAG security SET MASKING POLICY ssn_mask_2 FORCE;
    > ```

The option you select in the [Privilege](#label-tag-based-masking-privilege) section and the order of operations in the
[Assign a masking policy to a tag](#label-tag-masking-assignment) section can impact tag management if you need to replace or unset a tag on a database or schema.

If a schema owner sets a tag on a schema and then a different role sets a masking policy on the same tag, the schema owner cannot unset
the tag from the schema unless the schema owner is granted the global APPLY MASKING POLICY privilege. Snowflake fails the
[ALTER SCHEMA … UNSET TAG](/sql-reference/sql/alter-schema) operation for the schema owner. This scenario ensures that column data
that is protected by a tag-based masking policy stays protected. To avoid this scenario, use option 1 in the
[Privilege](#label-tag-based-masking-privilege) section.

> Important
>
> Exercise caution when replacing a masking policy on a tag.
>
> Depending on the timing of the replacement and the query on the column, choosing to replace the policy in two separate statements could
> lead to a data leak because the column data is unprotected in the time interval between the UNSET and SET operations.
>
> However, if the policy conditions are different in the replacement policy, specifying the `FORCE` keyword could lead to a lack of
> access because (previously) users could access data and the replacement no longer allows access.
>
> Prior to replacing a policy, consult your internal data administrators to coordinate the best approach to protect data with tag-based
> masking policies and replace masking policies as needed.

### Update a tag value

If a schema owner (i.e. `sch_role`) sets a tag on a schema and then a different role sets a masking policy on the same tag
(i.e. `masking_admin_role`), the schema owner cannot change the tag value. Snowflake fails the ALTER SCHEMA … SET TAG operation for
the schema owner.

To change the tag value:

1. Using the `masking_admin_role`, unset the masking policy from the tag.
2. Using the `sch_role`, modify the tag value.
3. Reassign the masking policy to the tag using the `masking_admin_role`.

### Parent database and schema

You cannot perform DROP and REPLACE operations on the database and schema when:

- The tag and masking policy are in the same schema.
- The table or view is in a different schema.
- The protected column in the table or view exists in a different schema than the schema that contains the masking policy and tag.

These four commands refer to DROP and replace operations on the database and schema:

- DROP DATABASE
- DROP SCHEMA
- CREATE OR REPLACE DATABASE
- CREATE OR REPLACE SCHEMA

### Conditional arguments

A [conditional masking policy](/user-guide/security-column-intro#label-security-column-intro-cond-cols) can be assigned to a tag. After assigning the tag to a column,
the conditional arguments map to a column in the table by name if the data type of the argument matches with the data type of the column.

A query will fail if a conditional masking policy is assigned to a column in the following cases:

- The table does not have a column with the same name as a conditional argument of the policy.
- The table has a column that matches the name of the conditional argument of the policy but the data type doesn’t match.

For more information on these errors, see [Troubleshoot Tag-based Masking Policies](#troubleshoot-tag-based-masking-policies) (in this topic).

### Tag inheritance

The tag with the masking policy can be assigned to all base table objects, or the tag can be assigned to a column in a base table.
When the tag-based masking policy is assigned to a base table, the columns are protected by the policy provided that the column
data type matches the data type in the masking policy signature.

Since the masking policy protects the base table columns, view columns that are derived from the underlying base table columns are also
protected, based on the current [limitations](/user-guide/security-column-intro#label-security-column-limitations),
[considerations](/user-guide/security-column-intro#label-security-column-considerations), and [behaviors](/user-guide/security-column-intro#label-security-column-intro-tables-views) regarding
masking policies with tables and views.

### Data Sharing

Tag-based masking policies that are set on a shared schema or shared database in the provider account are enforced in the consumer account.
This scenario ensures protected data that is shared remains protected, even if a consumer creates a new database from the share.

Additionally, note the following:

- Tag inheritance is preserved in the consumer account.

  When the provider sets a tag-based masking policy on their database and shares that database, Snowflake references the shared provider
  database in the consumer account in terms of the database that contains the tag.
- Snowflake does not honor tag inheritance with shared objects when the tags and tag-based masking policies originate in the consumer account.

  Tags and tag-based masking policies from the consumer account are not enforced on any shared objects.

### Snowsight

You can monitor and assign tag-based masking policies in Snowsight. For details, see:

- [Monitor tags with Snowsight](/user-guide/object-tagging/monitor#label-object-tagging-snowsight)
- [Monitor masking policies with Snowsight](/user-guide/security-column-intro#label-security-column-intro-snowsight)

## Use tag-based masking policies

The subsections below provide the following information:

- A common procedure to use with tag-based masking policies for data protection and validation.
- Prerequisite steps to complete before implementing tag-based masking policies.
- A list of common assumptions for the examples.
- Representative examples of tag-based masking policy usage, including the usage of the following system functions:
  - [SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column)
  - [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table)

### Tag and policy discovery

The Information Schema table function [POLICY\_REFERENCES](/sql-reference/functions/policy_references) and the Account Usage
[POLICY\_REFERENCES](/sql-reference/account-usage/policy_references) view can help determine whether a masking policy and a tag
reference each other by looking at the following columns:

- TAG\_DATABASE
- TAG\_SCHEMA
- TAG\_NAME
- POLICY\_STATUS

The POLICY\_STATUS column can have four possible values:

`ACTIVE`
:   Specifies that the column (i.e. REF\_COLUMN\_NAME) is only associated with a single policy.

`MULTIPLE_MASKING_POLICY_ASSIGNED_TO_THE_COLUMN`
:   Specifies that multiple masking policies are assigned to the same column.

`COLUMN_IS_MISSING_FOR_SECONDARY_ARG`
:   Specifies that the policy (i.e. POLICY\_NAME) is a conditional masking policy and the table (i.e. REF\_ENTITY\_NAME) does not have a
    column with the same name.

`COLUMN_DATATYPE_MISMATCH_FOR_SECONDARY_ARG`
:   Specifies that the policy is a conditional masking policy and the table has a column with the same name but a different data type than
    the data type in the masking policy signature.

For details on related error messages with the possible values in the POLICY\_STATUS column, refer to
[Troubleshoot Tag-Based Masking Policies](#troubleshoot-tag-based-masking-policies) (in this topic).

### Data protection and validation steps

Generally, Snowflake recommends the following approach when using tag-based masking policies:

1. Create any tags that are needed for tag-based masking policies.
2. Create one masking policy for each data type based on the table columns that you intend to protect with the tag-based masking policies.
3. Assign the masking policies to the tag.
4. Assign the tag with the masking policies to the table column directly or to the table.
5. Check the Information Schema to verify the tag-based policy is assigned to the columns.
6. Query the data to verify the tag-based masking policy protects the data as intended.

### Prerequisite steps

1. Identify the existing tags and their string values in your Snowflake account.

   - Query the Account Usage [TAG REFERENCES](/sql-reference/account-usage/tag_references) view to obtain all tags and their assigned
     string values.
   - Optionally:
     - Query the Account Usage [TAGS](/sql-reference/account-usage/tags) view (i.e. the *tag catalog*) to obtain a list of
       tags to ensure that duplicate tag naming does not occur later while using tag-based masking policies.
     - Compare the outputs from the TAG\_REFERENCES and TAGS queries to determine if there are any unassigned tags that can be used later.
     - Create any tags that will be needed later using the [CREATE TAG](/sql-reference/sql/create-tag) command. Otherwise, create tags as needed.
2. Identify the existing policies and their definitions in your Snowflake account.

   - Execute the [SHOW MASKING POLICIES](/sql-reference/sql/show-masking-policies) command to obtain a list of existing masking policies.
   - Decide whether these policies, in their current form, can be assigned to tags. If necessary, execute the
     [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) command to obtain the policy definition. Otherwise, plan to create new policies to
     assign to tags.
3. Determine how to protect the column data with the masking policy in terms of whether the policy conditions should evaluate the tag
   string value that is set on the table column.

### Common assumptions with the examples

The examples make the following assumptions:

- The prerequisite steps were completed.
- The `tag_admin` custom role has the following privileges:

  - The schema-level CREATE TAG privilege.
  - The global APPLY TAG privilege.

  For more information, see [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `masking_admin` custom role has the following privileges:

  - The schema-level CREATE MASKING POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.masking_policies` schema.
  - The global APPLY MASKING POLICY privilege to assign masking policies to tags (see [Privilege](#privilege) in this topic).
  - The global APPLY TAG privilege, to assign the tag (with the masking policies) to objects.

  For details, see, [tag privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- The `row_access_admin` custom role has the following privileges:

  - The schema-level CREATE ROW ACCESS POLICY privilege.
  - The USAGE privilege on the `governance` database and the `governance.row_access_policies` schema.
  - The global APPLY ROW ACCESS POLICY privilege.

  For more information, see [row access policy privileges](/user-guide/security-row-intro#label-security-row-privilege-command-summary).
- The `accounting_admin` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and the `finance.accounting` schema.
  - The SELECT privilege on tables in the `finance.accounting` schema.
- The `analyst` custom role has the following privileges:

  - The USAGE privilege on the `finance` database and on the `finance.accounting` schema.
  - The SELECT privilege on the `finance.accounting.name_number` table.
- The custom roles described above are granted to the appropriate users.

  For details, see [Configuring access control](/user-guide/security-access-control-configure).

### Example 1: Protect column data based on the masking policy directly assigned to the tag

This example assigns two masking policies to a tag and then assigns the same tag to a table. The result is that the masking policies
protect all table columns whose data types match the data types in the policies.

The following steps create a tag-based masking policy to mask accounting data. For example, consider the table named
`finance.accounting.name_number`, which has two columns, `ACCOUNT_NAME` and `ACCOUNT_NUMBER`. The data types in these columns are
STRING and NUMBER, respectively.

> ```
> ---------------+----------------+
>   ACCOUNT_NAME | ACCOUNT_NUMBER |
> ---------------+----------------+
>   ACME         | 1000           |
> ---------------+----------------+
> ```

Create a tag-based masking policy to protect the ACCOUNT\_NAME and ACCOUNT\_NUMBER columns as follows:

1. Create a tag named `accounting` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE OR REPLACE TAG accounting;
   ```
2. Create different masking policies to protect the ACCOUNT\_NAME and ACCOUNT\_NUMBER columns. In each of these policies, only the
   `ACCOUNTING_ADMIN` custom role can view the raw data.

   Account name policy:

   Copy code

   ```
   USE ROLE masking_admin;
   USE SCHEMA governance.masking_policies;

   CREATE OR REPLACE MASKING POLICY account_name_mask
   AS (val string) RETURNS string ->
     CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTING_ADMIN') THEN val
    ELSE '***MASKED***'
     END;
   ```

   Account number policy:

   Copy code

   ```
   CREATE OR REPLACE MASKING POLICY account_number_mask
   AS (val number) RETURNS number ->
     CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTING_ADMIN') THEN val
    ELSE -1
     END;
   ```
3. Assign both masking policies to the `accounting` tag. Note that both policies can be assigned to the tag in a single statement.

   Copy code

   ```
   ALTER TAG governance.tags.accounting SET
     MASKING POLICY account_name_mask,
     MASKING POLICY account_number_mask;
   ```
4. Assign the `accounting` tag to the `finance.accounting.name_number` table.

   Copy code

   ```
   ALTER TABLE finance.accounting.name_number
     SET TAG governance.tags.accounting = 'tag-based policies';
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
     REF_ENTITY_NAME => 'governance.accounting.name_number' )
   );
   ```

   Returns (note the updated columns):

   ```
   -------------+------------------+---------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+------------+---------------+
     POLICY_DB  | POLICY_SCHEMA    | POLICY_NAME         | POLICY_KIND    | REF_DATABASE_NAME | REF_SCHEMA_NAME | REF_ENTITY_NAME | REF_ENTITY_DOMAIN | REF_COLUMN_NAME | REF_ARG_COLUMN_NAMES | TAG_DATABASE | TAG_SCHEMA | TAG_NAME   | POLICY_STATUS |
   -------------+------------------+---------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+------------+---------------+
     GOVERNANCE | MASKING_POLICIES | ACCOUNT_NAME_MASK   | MASKING_POLICY | FINANCE           | ACCOUNTING      | NAME_NUMBER     | TABLE             | ACCOUNT_NAME    | NULL                 | GOVERNANCE   | TAGS       | ACCOUNTING | ACTIVE        |
     GOVERNANCE | MASKING_POLICIES | ACCOUNT_NUMBER_MASK | MASKING_POLICY | FINANCE           | ACCOUNTING      | NAME_NUMBER     | TABLE             | ACCOUNT_NUMBER  | NULL                 | GOVERNANCE   | TAGS       | ACCOUNTING | ACTIVE        |
   -------------+------------------+---------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+------------+---------------+
   ```
6. Query the table columns with authorized and unauthorized roles to ensure Snowflake returns the correct query result.

   Authorized:

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

   Unauthorized:

   Copy code

   ```
   USE ROLE analyst;
   SELECT * FROM finance.accounting.name_number;
   ```

   Returns:

   ```
   ---------------+----------------+
     ACCOUNT_NAME | ACCOUNT_NUMBER |
   ---------------+----------------+
     ***MASKED*** | -1             |
   ---------------+----------------+
   ```

### Example 2: Protect column data based on the column tag string value

This example uses a tag-based masking policy to determine whether data should be masked based upon the tag string value of the tag assigned
to a column. The masking policy dynamically evaluates the tag string value by calling the
[SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) function into the masking policy conditions and writing the masking policy
conditions to match the tag string value.

The following steps create a tag-based masking policy to mask accounting data. For brevity, the table columns have two data types,
STRING and NUMBER, respectively. For example, a table named `finance.accounting.name_number`:

> ```
> ---------------+----------------+
>   ACCOUNT_NAME | ACCOUNT_NUMBER |
> ---------------+----------------+
>   ACME         | 1000           |
> ---------------+----------------+
> ```

Create a tag-based masking policy to protect the `ACCOUNT_NAME` and `ACCOUNT_NUMBER` columns as follows:

1. Create a tag named `accounting_col_string` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG accounting_col_string;
   ```
2. Create different masking policies to protect the ACCOUNT\_NAME and ACCOUNT\_NUMBER columns. In each of these policies, the raw data is
   visible only when the current tag string value on the column is set to `'visible'`.

   Account name policy:

   Copy code

   ```
   USE ROLE masking_admin;
   USE SCHEMA governance.masking_policies;

   CREATE MASKING POLICY account_name_mask_tag_string
   AS (val string) RETURNS string ->
     CASE
    WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tags.accounting_col_string') = 'visible' THEN val
    ELSE '***MASKED***'
     END;
   ```

   Account number policy:

   > Copy code
   >
   > ```
   > CREATE MASKING POLICY account_number_mask_tag_string
   > AS (val number) RETURNS number ->
   >   CASE
   >  WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tags.accounting_col_string') = 'visible' THEN val
   >  ELSE -1
   >   END;
   > ```
   >
   > Note
   >
   > These policies use the `schema_name.tag_name` object name format in the function argument because the `tags` schema and the
   > `masking_policies` schema both exist in the `governance` database. Alternatively, you can also use the fully-qualified name
   > for the tag in the function argument.
   >
   > Snowflake returns an error at query runtime on a column protected by a tag-based masking policy if the system function argument
   > in the policy conditions contains a tag name that is not sufficiently qualified. For example, the argument uses the tag name as
   > `accounting_col_string` only, without specifying the schema name or the database name.
   >
   > For more information, see [Object name resolution](/sql-reference/name-resolution).
3. Assign both masking policies to the `accounting_col_string` tag. Note that both policies can be assigned to the tag in a single
   statement.

   Copy code

   ```
   ALTER TAG accounting_col_string SET
     MASKING POLICY account_name_mask_tag_string,
     MASKING POLICY account_number_mask_tag_string;
   ```
4. Assign the `accounting_col_string` tag to each table column. In this example, the tag string value on the `ACCOUNT_NAME` column is
   `'visible'`, however, the tag string value on the `ACCOUNT_NUMBER` column is set to `'protect'`.

   Copy code

   ```
   ALTER TABLE finance.accounting.name_number MODIFY COLUMN
     account_name SET TAG governance.tags.accounting_col_string = 'visible',
     account_number SET TAG governance.tags.accounting_col_string = 'protect';
   ```
5. Verify the `ACCOUNT_NAME` and `ACCOUNT_NUMBER` table columns are protected by the tag-based masking policy by calling the
   Information Schema [POLICY\_REFERENCES](/sql-reference/functions/policy_references) table function.

   For each protected column, the row in the query result should specify the appropriate values for the column name, policy name, and tag
   name.

   Copy code

   ```
   SELECT *
   FROM TABLE(
    governance.INFORMATION_SCHEMA.POLICY_REFERENCES(
   REF_ENTITY_DOMAIN => 'TABLE',
   REF_ENTITY_NAME => 'finance.accounting.name_number'
   )
   );
   ```

   Returns (note the updated columns):

   ```
   ------------+----------------+--------------------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+-----------------------+---------------+
    POLICY_DB  | POLICY_SCHEMA  | POLICY_NAME                    |  POLICY_KIND   | REF_DATABASE_NAME | REF_SCHEMA_NAME | REF_ENTITY_NAME | REF_ENTITY_DOMAIN | REF_COLUMN_NAME | REF_ARG_COLUMN_NAMES | TAG_DATABASE | TAG_SCHEMA | TAG_NAME              | POLICY_STATUS |
   ------------+----------------+--------------------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+-----------------------+---------------+
    GOVERNANCE | MASKING_POLICY | ACCOUNT_NAME_MASK_TAG_STRING   | MASKING_POLICY | FINANCE           | ACCOUNTING      | NAME_NUMBER     | TABLE             | ACCOUNT_NAME    | NULL                 | GOVERNANCE   | TAGS       | ACCOUNTING_COL_STRING | ACTIVE        |
    GOVERNANCE | MASKING_POLICY | ACCOUNT_NUMBER_MASK_TAG_STRING | MASKING_POLICY | FINANCE           | ACCOUNTING      | NAME_NUMBER     | TABLE             | ACCOUNT_NUMBER  | NULL                 | GOVERNANCE   | TAGS       | ACCOUNTING_COL_STRING | ACTIVE        |
   ------------+----------------+--------------------------------+----------------+-------------------+-----------------+-----------------+-------------------+-----------------+----------------------+--------------+------------+-----------------------+---------------+
   ```
6. Query the table columns to ensure Snowflake returns the correct query result, which should only mask the value in the `ACCOUNT_NUMBER`
   column.

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
     ACME         | -1             |
   ---------------+----------------+
   ```

### Example 3: Protect a table based on the table tag string value

This example uses a row access policy to protect a table based on a tag string value assigned to the table and a tag-based masking policy
to protect the columns in the table. For simplicity, this example uses one tag, assigns the masking policies to the tag, and assigns the
tag to the table. The columns in the table will automatically have the same tag and its string value because of
[tag inheritance](/user-guide/object-tagging/inheritance#label-object-tagging-lineage).

The row access policy dynamically evaluates the tag string value of the tag assigned to the table by calling the
[SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table) function in the row access policy conditions. As with the previous example,
the masking policy conditions call the [SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) function to evaluate the tag
string value on the table columns.

Important

Note that you cannot assign a row access policy to the tag.

Instead, assign the row access policy to the table directly using an [ALTER TABLE](/sql-reference/sql/alter-table) command.

The table `finance.accounting.name_number` has two columns, which have the data types STRING and NUMBER:

> ```
> ---------------+----------------+
>   ACCOUNT_NAME | ACCOUNT_NUMBER |
> ---------------+----------------+
>   ACME         | 1000           |
> ---------------+----------------+
> ```

Protect the table and its columns with a row access policy and a tag-based masking policy as follows:

1. [Create a row access policy](/sql-reference/sql/create-row-access-policy) that calls the
   [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table) function in the policy conditions:

   Copy code

   ```
   USE ROLE row_access_admin;
   USE SCHEMA governance.row_access_policies;

   CREATE ROW ACCESS POLICY rap_tag_value
   AS (account_number number)
   RETURNS BOOLEAN ->
   SYSTEM$GET_TAG_ON_CURRENT_TABLE('tags.accounting_row_string') = 'visible'
   AND
   'accounting_admin' = CURRENT_ROLE();
   ```

   The policy specifies that Snowflake return rows in the query result only when the `accounting_row_string` tag is assigned to
   the table with a string value as `'visible'` and the role executing the query on the table or its columns is the
   `accounting_admin` custom role.

   Snowflake does not return rows in the query result if any of the following are true:

   - The `accounting_row_string` tag is not set on the table.
   - The `accounting_row_string` tag is set on the table but with a different string value.
   - The role executing a query on the table or its columns is not the `accounting_admin` custom role.
2. [Assign](/sql-reference/sql/alter-table) the row access policy to the table:

   Copy code

   ```
   ALTER TABLE finance.accounting.name_number
     ADD ROW ACCESS POLICY rap_tag_value ON (account_number);
   ```

   Note that at this point in the procedure, a query on the table should not return any rows in the query result for any role in
   Snowflake because the `accounting_row_string` tag is not assigned to the table. So, the expected result from a query on the table
   should be:

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
               |                |
   ---------------+----------------+
   ```

   By choosing to assign the row access policy to the table before assigning the tag-based masking policy to the table, all of the table
   data is protected as early as possible.
3. Create a tag named `accounting_row_string` in the schema named `governance.tags`.

   Copy code

   ```
   USE ROLE tag_admin;
   USE SCHEMA governance.tags;
   CREATE TAG accounting_row_string;
   ```
4. Create different masking policies to protect the ACCOUNT\_NAME and ACCOUNT\_NUMBER columns. In each of these policies, the raw data is
   visible only when the current tag string value on the column is set to `'visible'`.

   Account name policy:

   Copy code

   ```
   USE ROLE masking_admin;
   USE SCHEMA governance.masking_policies;

   CREATE MASKING POLICY account_name_mask AS (val string) RETURNS string ->
     CASE
    WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tags.accounting_row_string') = 'visible' THEN val
    ELSE '***MASKED***'
     END;
   ```

   Account number policy:

   Copy code

   ```
   CREATE MASKING POLICY account_number_mask AS (val number) RETURNS number ->
     CASE
    WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tags.accounting_row_string') = 'visible' THEN val
    ELSE -1
     END;
   ```
5. Assign both masking policies to the `accounting_row_string` tag. Note that both policies can be assigned to the tag in a single
   statement.

   Copy code

   ```
   ALTER TAG governance.tags.accounting_row_string SET
     MASKING POLICY account_name_mask,
     MASKING POLICY account_number_mask;
   ```
6. Assign the `accounting_row_string` tag to the table with the tag string value `'visible'`:

   Copy code

   ```
   ALTER TABLE finance.accounting.name_number
     SET TAG governance.tags.accounting_row_string = 'visible';
   ```

   Now that the tag is assigned to the table with a string value of `visible`, only the `accounting_admin` custom role can view the
   table data; a query made by a user with any other role should result in no rows being returned as shown earlier in this example. In
   other words, the conditions of the row access policy now evaluate to true.

   Similarly, the table columns also have the tag string value of `visible` tag because the columns inherit the tag and its string value
   through tag inheritance. The result is that when a user with the `accounting_admin` custom role queries the table, Snowflake returns
   unmasked data:

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
7. To mask data in either column, update the tag string value for the column directly. For example, to mask the data in the ACCOUNT\_NUMBER
   column:

   Copy code

   ```
   ALTER TABLE finance.accounting.name_number MODIFY COLUMN
     account_number SET TAG governance.tags.accounting_row_string = 'protect';
   ```

   Now when a user with the `accounting_admin` custom role queries the table or the ACCOUNT\_NUMBER column, Snowflake returns masked data:

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
     ACME         | -1             |
   ---------------+----------------+
   ```

## Enforce tag-based masking policies on Apache Iceberg tables queried from Apache Spark™

Snowflake supports enforcing tag-based masking policies on Apache Iceberg tables that you query from Apache Spark™ through Snowflake Horizon
Catalog. For more information,
see [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

## Troubleshoot tag-based masking policies

The following table lists some error messages that Snowflake can return when using tag-based masking policies:

| Behavior | Error message | Troubleshooting action |
| --- | --- | --- |
| Cannot query a column: too many policies. | SQL execution error: Column <col\_name> is mapped to multiple masking policies by tags.Please contact your local administrator to fix the issue. | A given column can be protected by only one masking policy.  Call the [POLICY\_REFERENCES](/sql-reference/functions/policy_references) function to identify the masking policies set on the column. Modify the tags by unsetting the masking policy from the tag so that the column is protected by only one policy. |
| Cannot query a column: no conditional column. | SQL execution error: Column <col\_name> is mapped to a masking policy where the table doesn’t have a column for a secondary argument name of the policy.Please contact your local administrator to fix the issue. | A masking policy that uses [conditional arguments](/user-guide/security-column-intro#label-security-column-intro-cond-cols) must have all of the specified columns in the same table or view. Do one of the following to protect the column data:   - Assign a different policy to the column [directly](/user-guide/security-column-intro#label-security-column-intro-apply-to-column). - Modify the tag by [assigning](#label-tag-masking-assignment) a different masking policy to the tag. |
| Column data is not masked due to a data type mismatch for the column and the policy. | SQL execution error: Column <col\_name> is mapped to a masking policy where the table has a column with different data-type for a secondary argument name.Please contact your local administrator to fix the issue. | To mask the column data, the data type for the column and the data type in the masking policy signature must match. Do one of the following to protect the column data:   - Assign a different policy to the column [directly](/user-guide/security-column-intro#label-security-column-intro-apply-to-column). - [Assign](#label-tag-masking-assignment) a masking policy to the tag, making sure that the data type for the policy and the   data type for the column match. |

Expand

Show lessSee more
