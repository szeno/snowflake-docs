# Understanding External Tokenization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides a general overview of the External Tokenization feature.

Note that an external tokenization masking policy can be assigned to a tag to provide tag-based external tokenization. For details about
assigning a masking policy to a tag, see [Tag-based masking policies](/user-guide/tag-based-masking-policies).

Important

External tokenization requires [Writing external functions](/sql-reference/external-functions), which are included in the Snowflake [Overview of editions](/user-guide/intro-editions#label-snowflake-editions-standard), and you can use external functions with a tokenization provider.

However, if you choose to integrate your tokenization provider with Snowflake External Tokenization, you must upgrade to
[Enterprise Edition](/user-guide/intro-editions#label-snowflake-editions-enterprise) or higher.

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## What is External Tokenization?

External Tokenization enables accounts to tokenize data before loading it into Snowflake and detokenize the data at query runtime. Tokenization is the process of removing sensitive data by replacing it with an undecipherable token. External Tokenization makes use of masking policies with [external functions](/sql-reference/external-functions).

In Snowflake, masking policies are schema-level objects, which means a database and schema must exist in Snowflake before a masking policy can be applied to a column. Currently, Snowflake supports using Dynamic Data Masking on tables and views.

At query runtime, the masking policy is applied to the column at every location where the column appears. Depending on the masking policy conditions, the SQL execution context, and role hierarchy, Snowflake query operators may see the plain-text value, a partially masked value, or a fully masked value.

For more details about how masking policies work, including the query runtime behavior, creating a policy, usage with tables and views, and management approaches using masking policies, see: [Understanding Column-level Security](/user-guide/security-column-intro).

For more details on the effects of the SQL execution context and role hierarchy, see [Advanced Column-level Security topics](/user-guide/security-column-advanced).

Tokenizing data before loading into Snowflake ensures that sensitive data is never exposed unnecessarily. Using masking policies with external functions ensures that only the appropriate audiences can view de-tokenized data at query runtime.

## External Tokenization benefits

The following summarizes some of the key benefits of External Tokenization.

Pre-load Tokenized Data:
:   Using a tokenization provider, tokenized data is pre-loaded into Snowflake. Therefore, even without applying a masking policy to a column in a table or view, users never see the real data value. This provides enhanced data security to the most sensitive data in your organization.

Ease of use:
:   You can write a policy once and have it apply to thousands of columns across databases and schemas.

Data administration and SoD:
:   A security or privacy officer decides which columns to protect, not the object owner. Masking policies are easy to manage and support centralized and decentralized administration models.

Data authorization and governance:
:   Contextual data access by role or custom entitlements.

    Supports data governance as implemented by security or privacy officers and can prohibit privileged users with the ACCOUNTADMIN or SECURITYADMIN role from unnecessarily viewing data.

Change management:
:   Easily change masking policy content without having to reapply the masking policy to thousands of columns.

For a comparison of benefits between Dynamic Data Masking and External Tokenization, see: [Column-level Security Benefits](/user-guide/security-column-intro#label-security-column-benefits).

## External Tokenization limitations

For an overview on the limitations, see [Column-level Security Limitations](/user-guide/security-column-intro#label-security-column-limitations).

## External Tokenization considerations

For additional External Tokenization Considerations, see [Column-level Security Considerations](/user-guide/security-column-intro#label-security-column-considerations).

## External Tokenization privileges and dependencies

The following table summarizes the privileges related to External Tokenization masking policies.

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a [masking policy](/user-guide/security-column-intro) on a column.  Note that granting the global APPLY MASKING POLICY privilege (i.e. APPLY MASKING POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views.  For syntax examples, see [Masking policy privileges](/user-guide/security-column-intro#label-security-column-privileges-masking-policies). |
| OWNERSHIP | Grants full control over the masking policy. Required to alter most properties of a masking policy. Only a single role can hold this privilege on a specific object at a time. |

Expand

Show lessSee more

Note

Operating on a masking policy also requires USAGE or any other privilege on the parent database and schema.

Since the external tokenization masking policy requires an external function that depends on an API integration, the following table summarizes the privileges the custom role (e.g. MASKING\_ADMIN) must have on Snowflake objects. Note that these privileges apply to the custom role only and are not necessary for the role of the user querying the column with a masking policy.

| Custom role | Privilege | Object |
| --- | --- | --- |
| External tokenization policy owner | USAGE | External function |
| External function owner (i.e. the role with the OWNERSHIP privilege on the external function) | USAGE | Any API integration objects that are referenced by the external function. |

Expand

Show lessSee more

## External Tokenization DDL

Snowflake provides the following set of commands to manage External Tokenization policies.

- [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy)
- [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) (see also: [ALTER TABLE](/sql-reference/sql/alter-table), [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column), and [ALTER VIEW](/sql-reference/sql/alter-view))
- [DROP MASKING POLICY](/sql-reference/sql/drop-masking-policy)
- [SHOW MASKING POLICIES](/sql-reference/sql/show-masking-policies)
- [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy)

## Auditing External Tokenization

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

## Troubleshooting External Tokenization

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

- [Using External Tokenization](/user-guide/security-column-ext-token-use)
- [Using Conditional Tokenization](/user-guide/security-column-intro#label-security-column-intro-cond-cols)
  (For an external tokenization policy example with conditional columns, see [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy).)
