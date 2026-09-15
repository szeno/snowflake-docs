# Understanding Dynamic Data Masking

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides a general overview of the Dynamic Data Masking feature.

To learn more about using a masking policy with a tag, see [Tag-based masking policies](/user-guide/tag-based-masking-policies).

## What is Dynamic Data Masking?

Dynamic Data Masking is a Column-level Security feature that uses masking policies to selectively mask plain-text data in table and view columns at query time.

In Snowflake, masking policies are schema-level objects, which means a database and schema must exist in Snowflake before a masking policy can be applied to a column. Currently, Snowflake supports using Dynamic Data Masking on tables and views.

At query runtime, the masking policy is applied to the column at every location where the column appears. Depending on the masking policy conditions, the SQL execution context, and role hierarchy, Snowflake query operators may see the plain-text value, a partially masked value, or a fully masked value.

For more details about how masking policies work, including the query runtime behavior, creating a policy, usage with tables and views, and management approaches using masking policies, see: [Understanding Column-level Security](/user-guide/security-column-intro).

For more details on the effects of the SQL execution context and role hierarchy, see [Advanced Column-level Security topics](/user-guide/security-column-advanced).

## Dynamic Data Masking benefits

The following summarizes some of the key benefits of Dynamic Data Masking.

Ease of use:
:   You can write a policy once and have it apply to thousands of columns across databases and schemas.

Data administration and SoD:
:   A security or privacy officer decides which columns to protect, not the object owner. Masking policies are easy to manage and support centralized and decentralized administration models.

Data authorization and governance:
:   Contextual data access by role or custom entitlements.

    Supports data governance as implemented by security or privacy officers and can prohibit privileged users with the ACCOUNTADMIN or SECURITYADMIN role from unnecessarily viewing data.

Data sharing:
:   Easily mask data before sharing.

Change management:
:   Easily change masking policy content without having to reapply the masking policy to thousands of columns.

For a comparison of benefits between Dynamic Data Masking and External Tokenization, see: [Column-level Security Benefits](/user-guide/security-column-intro#label-security-column-benefits).

## Dynamic Data Masking limitations

For an overview of the limitations, see [Column-level Security Limitations](/user-guide/security-column-intro#label-security-column-limitations).

## Dynamic Data Masking considerations

For additional Dynamic Data Masking Considerations, see [Column-level Security Considerations](/user-guide/security-column-intro#label-security-column-considerations).

## Dynamic Data Masking privileges

The following table summarizes the privileges related to Dynamic Data Masking.

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a [masking policy](/user-guide/security-column-intro) on a column.  Note that granting the global APPLY MASKING POLICY privilege (i.e. APPLY MASKING POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views.  For syntax examples, see [Masking policy privileges](/user-guide/security-column-intro#label-security-column-privileges-masking-policies). |
| OWNERSHIP | Grants full control over the masking policy. Required to alter most properties of a masking policy. Only a single role can hold this privilege on a specific object at a time. |

Expand

Show lessSee more

Note

Operating on a masking policy also requires USAGE or any other privilege on the parent database and schema.

## Dynamic Data Masking DDL

Snowflake provides the following set of commands to manage Dynamic Data Masking policies.

- [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy)
- [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) (see also: [ALTER TABLE](/sql-reference/sql/alter-table), [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column), and [ALTER VIEW](/sql-reference/sql/alter-view))
- [DROP MASKING POLICY](/sql-reference/sql/drop-masking-policy)
- [SHOW MASKING POLICIES](/sql-reference/sql/show-masking-policies)
- [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy)

## Auditing Dynamic Data Masking

Snowflake provides two Account Usage views to obtain information about masking policies:

- The [MASKING\_POLICIES](/sql-reference/account-usage/masking_policies) view provides a list of all masking policies in your
  Snowflake account.
- The [POLICY\_REFERENCES](/sql-reference/account-usage/policy_references) view provides a list of all objects in which a masking
  policy is set.

The Information Schema table function [POLICY\_REFERENCES](/sql-reference/functions/policy_references) can be used to either:

- Return a list of all objects (i.e. tables, views) that have the masking policy set on a column.
- Return a list of policy associations that have the specified object name and object type.

Snowflake records the original query run by the user on the [History page](/user-guide/ui-snowsight-activity) (in the web interface). The query
is found in the **SQL Text** column.

The masking policy names that were used in a specific query can be found in the [Query Profile](/user-guide/ui-snowsight-activity).

The query history is specific to the Account Usage [QUERY\_HISTORY](/sql-reference/account-usage/query_history) view only. In this
view, the **Query Text** column contains the text of the SQL statement. Masking policy names are not included in the QUERY\_HISTORY
view.

## Troubleshooting Dynamic Data Masking

You can use error messages to help troubleshoot masking policy issues.

# Error Messages

The following table describes error messages Snowflake can return while using masking policies.

| Behavior | Error Message | Troubleshooting Action |
| --- | --- | --- |
| Cannot apply a masking policy to a Snowflake feature. | Unsupported feature `CREATE ON MASKING POLICY COLUMN`. | Masking policies are currently not applicable to this feature. |
| An active role cannot create or replace a masking policy. | SQL access control error: Insufficient privileges to operate on account <account\_name> | Grant the CREATE MASKING POLICY privilege to the specified role using `grant create masking policy on account to role role_name;`   Verify the role has the privilege using `show grants to role role_name`, and try the CREATE OR REPLACE masking statement again. |
| A given role cannot attach a masking policy to a table. | SQL compilation error: Database <database\_name> does not exist or not authorized. | Grant the APPLY MASKING POLICY privilege to the role using `grant apply masking policy on account to role role_name;` |
| A given role that does not own a masking policy on a table tries to apply a masking policy on a table they can use. | SQL compilation error: Masking policy <policy\_name> does not exist or not authorized. | Grant the given role usage on the masking policy using `grant apply on masking policy policy_name to role role_name;` |
| Cannot drop or remove a policy using `drop masking policy policy_name;` | SQL compilation error: Policy <policy\_name> cannot be dropped/replaced as it is associated with one or more entities. | Use an ALTER TABLE … MODIFY COLUMN or ALTER VIEW … MODIFY COLUMN statement to UNSET the policy first, then try the DROP statement again. |
| Restoring a dropped table produces a masking policy error. | SQL execution error: Column <column\_name> already attached to a masking policy that does not exist. Please contact the policy administrator. | Unset the currently attached masking policy with an ALTER Table/View MODIFY COLUMN statement and then reapply the masking policy to the column with a CREATE OR REPLACE statement. |
| Cannot apply a masking policy to a specific column, but the masking policy can be applied to a different column. | Specified column already attached to another masking policy.A column cannot be attached to multiple masking policies.please drop the current association in order to attach a new masking policy. | Decide which masking policy should apply to the column, update, and try again. |
| Updating a policy with an ALTER statement fails. | SQL compilation error: Masking policy <policy\_name> does not exist or not authorized. | Verify the policy name in the ALTER command matches an existing policy by executing `show masking policies;` |
| The role that owns the cloned table cannot unset a masking policy. | SQL access control error: Insufficient privileges to operate on ALTER TABLE UNSET MASKING POLICY ‘<policy\_name>’ | Grant the APPLY privilege to the role that owns the cloned table using `grant apply on masking policy policy_name to role role_name;`   Verify that the role that owns the cloned table has the grant using `show grants to role role_name;` and try the ALTER statement again. |
| Updating a policy using IF EXISTS returns a successful result but does not update the policy. | No error message returned; Snowflake returns Statement executed successfully. | Remove IF EXISTS from the ALTER statement and try again. |
| While creating or replacing a masking policy with CASE, the data types do not match (e.g. (VAL string) -> returns number). | SQL compilation error: Masking policy function argument and return type mismatch. | Update the masking policy using CASE with matching data types using a CREATE OR REPLACE statement or an ALTER MASKING POLICY statement. |
| Applying a masking policy to a virtual column. | SQL compilation error: Masking policy cannot be attached to a VIRTUAL\_COLUMN column. | Apply the masking policy to the column(s) in the source table. |
| Applying a masking policy to a materialized view. | SQL compilation error: syntax error line <number> at position <number> unexpected ‘modify’.   SQL compilation error: error line <number> at position <number> invalid identifier ‘<character>’   SQL execution error: One or more materialized views exist on the table. number of mvs=<number>, table name=<table\_name>. | Apply the masking policy to the column(s) in the source table. For more information, see [Limitations](/user-guide/security-column-intro#label-security-column-limitations). |
| Applying a masking policy to a table column used to create a materialized view. | SQL compilation error: Masking policy cannot be attached to a MATERIALIZED\_VIEW column. | To apply the masking policy to the table column, drop the materialized view. |
| Including a masked column while creating a materialized view. | Unsupported feature ‘CREATE ON MASKING POLICY COLUMN’. | Create the materialized view without including the masked columns or do not set any masking policies on the base table or views, create the materialized view, and then apply the masking policies to the materialized view columns. |
| Cannot create a masking policy with a user-defined function (UDF) in the masking policy body. | SQL access control error: Insufficient privileges to operate on function ‘<udf\_name>’ | Verify the role creating the masking policy has the USAGE privilege on the UDF. |

Expand

Show lessSee more

**Next Topics:**

- [Using Dynamic Data Masking](/user-guide/security-column-ddm-use)
