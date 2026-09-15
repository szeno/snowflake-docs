# CREATE STORAGE LIFECYCLE POLICY

Creates a new [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) in the current or specified schema, or replaces
an existing policy.
The policy runs an expression on arguments that you specify to determine which rows to expire in the table that the policy is attached to.
The arguments in a policy refer to columns in your tables.

After you create a policy, use the [ALTER TABLE](/sql-reference/sql/alter-table) command to add the policy to a table.

See also:
:   [ALTER STORAGE LIFECYCLE POLICY](/sql-reference/sql/alter-storage-lifecycle-policy) , [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) , [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) , [SHOW STORAGE LIFECYCLE POLICIES](/sql-reference/sql/show-storage-lifecycle-policies)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] STORAGE LIFECYCLE POLICY [ IF NOT EXISTS ] <name>
  AS ( <arg_name> <arg_type> [ , ... ] )
  RETURNS BOOLEAN -> <body>
  [ ARCHIVE_TIER = { COOL | COLD } ]
  [ ARCHIVE_FOR_DAYS = <number_of_days> ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

## Required parameters

`name`
:   String that specifies the identifier for the storage lifecycle policy. This must be unique for the schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS ( arg_name arg_type [ , ... ] )`
:   The signature for the policy. You must include at least one argument in the signature.

    A signature specifies a set of attributes that must be considered to determine whether the row is ready for expiration. The attribute
    values come from the database object (table).

`RETURNS BOOLEAN -> body`
:   A storage lifecycle policy must evaluate to true or false. A user that queries a table protected by a storage lifecycle policy sees rows in the output
    based on how the `body` is written.

    `body`
    :   SQL expression that Snowflake uses to determine which rows to expire.

        To transform the data, you can use built-in functions such as [Conditional expression functions](/sql-reference/expressions-conditional) or
        [user-defined functions](/developer-guide/udf/udf-overview) (UDFs).

        Note

        Currently, only SQL and JavaScript UDFs are supported in the body of a storage lifecycle policy.

## Optional parameters

`ARCHIVE_TIER = { COOL | COLD }`
:   Specifies the type of storage tier to use for archiving rows. After you set the ARCHIVE\_TIER for a policy, you can’t modify it.
    For more information, see [Archive storage tiers](/user-guide/storage-management/storage-lifecycle-policies#label-slp-archive-tiers).

    If you don’t specify this parameter, the policy is an expiration policy that deletes rows without archiving them.

    - `COOL` requires that you set an archival period (ARCHIVE\_FOR\_DAYS) of 90 days or longer to enable archiving.
    - `COLD` requires that you set an archival period (ARCHIVE\_FOR\_DAYS) of 180 days or longer to enable archiving.

    For supported cloud providers, see [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).

    Default: No value

`ARCHIVE_FOR_DAYS = number_of_days`
:   Specifies the number of days to keep rows that match the policy expression in archive storage.
    If set, Snowflake moves the data into archive storage according
    to the value you select for ARCHIVE\_TIER. If unset, Snowflake expires the rows from the table without archiving the data.

    Values:

    - ARCHIVE\_TIER = COOL: `90` - `2147483647`
    - ARCHIVE\_TIER = COLD: `180` - `2147483647`

    Default: Unset

`COMMENT = 'string_literal'`
:   Specifies a comment for the storage lifecycle policy.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| [CREATE STORAGE LIFECYCLE POLICY](/user-guide/security-access-control-privileges#label-security-access-control-slp-privileges) | Schema | None |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

  - If you specify OR REPLACE and the policy is attached to any objects, the command fails.
  - You can’t use `OR REPLACE` and `IF NOT EXISTS` together for this command.
  - If you want to replace an existing storage lifecycle policy and need to see the current definition of the policy, call the
    [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) command.
- Including one or more [subqueries](/user-guide/querying-subqueries) in the policy body might cause errors. When possible, limit the
  number of subqueries, limit the number of JOIN operations, and simplify WHERE clause conditions.
- You cannot change the policy signature if the policy is attached to a table. If you need to change the signature, use the
  [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) command and create a new policy.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following lifecycle policy moves data from rows that correspond to closed accounts and are more than 60 days old into archive
storage (COOL tier).

Copy code

```
CREATE STORAGE LIFECYCLE POLICY example_policy
  AS (event_ts TIMESTAMP, account_id NUMBER)
  RETURNS BOOLEAN ->
    event_ts < DATEADD(DAY, -60, CURRENT_TIMESTAMP())
    AND EXISTS (
      SELECT 1 FROM closed_accounts
      WHERE id = account_id
    )
  ARCHIVE_TIER = COOL
  ARCHIVE_FOR_DAYS = 180;
```
