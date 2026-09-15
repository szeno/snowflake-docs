# ALTER STORAGE LIFECYCLE POLICY

Modifies the properties of an existing [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies).

Attention

Changes to a storage lifecycle policy can have significant impact on all associated tables.
Use the QUERY\_HISTORY view in the ACCOUNT\_USAGE schema to audit policy changes regularly.
For more information, see [QUERY\_HISTORY view](/sql-reference/account-usage/query_history).

See also:
:   [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy) , [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) , [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) , [SHOW STORAGE LIFECYCLE POLICIES](/sql-reference/sql/show-storage-lifecycle-policies)

## Syntax

Copy code

```
ALTER STORAGE LIFECYCLE POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER STORAGE LIFECYCLE POLICY [ IF EXISTS ] <name> SET

  BODY -> <expression_on_arg_name>
  | ARCHIVE_TIER = { COOL | COLD }
  | ARCHIVE_FOR_DAYS = <number_of_days>
  | COMMENT = '<string_literal>'
  | TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER STORAGE LIFECYCLE POLICY [ IF EXISTS ] <name> UNSET
  ARCHIVE_FOR_DAYS
  | COMMENT
  | TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the policy; must be unique for your schema.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies one or more properties to set for the policy:

    `BODY -> expression_on_arg_name`
    :   SQL expression that determines the rows to expire.

        To transform the data, you can use built-in functions such as [Conditional expression functions](/sql-reference/expressions-conditional) or
        [user-defined functions](/developer-guide/udf/udf-overview) (UDFs).

        Note

        Currently, only SQL and JavaScript UDFs are supported in the body of a storage lifecycle policy.

    `ARCHIVE_TIER = { COOL | COLD }`
    :   Specifies a storage tier to convert an expiration policy where ARCHIVE\_FOR\_DAYS is unset into an archival policy.

        - `COOL` requires that you set an archival period (ARCHIVE\_FOR\_DAYS) of 90 days or longer.
        - `COLD` requires that you set an archival period (ARCHIVE\_FOR\_DAYS) of 180 days or longer.

        For supported cloud providers, see [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).

    `ARCHIVE_FOR_DAYS = number_of_days`
    :   Specifies the number of days to keep rows that match the policy expression in archive storage.
        If set, Snowflake moves the data into archive storage according
        to the value you select for ARCHIVE\_TIER. If unset, Snowflake expires the rows from the table without archiving the data.

        Values:

        - ARCHIVE\_TIER = COOL: `90` - `2147483647`
        - ARCHIVE\_TIER = COLD: `180` - `2147483647`

        Default: Unset

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the policy.

        Default: No value

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies properties to unset for the policy, which resets the properties to their defaults:

    - `ARCHIVE_FOR_DAYS`
    - `COMMENT`
    - `TAG tag_name [ , tag_name ... ]`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Storage lifecycle policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If you want to update an existing policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) command.
- You can’t change the policy signature with this command. To change the signature, use the [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) command and then create a new policy.
- After you set the ARCHIVE\_TIER for a policy, you can’t change it. For example, you can’t use this command to change the ARCHIVE\_TIER for a policy from COOL to COLD.
- If you unset ARCHIVE\_FOR\_DAYS for a policy, the storage tier doesn’t change. If you later re-enable archival storage for the policy, you can’t modify the storage tier.
- Including one or more [subqueries](/user-guide/querying-subqueries) in the policy body might cause errors. When possible, limit the
  number of subqueries, limit the number of JOIN operations, and simplify WHERE clause conditions.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example updates the storage lifecycle policy to expire closed accounts after 30 days.

Copy code

```
ALTER STORAGE LIFECYCLE POLICY expire_storage_for_closed_accounts
  SET BODY ->
    event_ts < DATEADD(DAY, -30, CURRENT_TIMESTAMP())
    AND EXISTS (
      SELECT 1 FROM closed_accounts
      WHERE id = account_id
    );
```
