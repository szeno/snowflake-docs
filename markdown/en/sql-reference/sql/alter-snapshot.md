# ALTER SNAPSHOT

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Modifies the properties of an existing [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume).

See also:
:   [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot) , [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot), [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot), [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots)

## Syntax

Copy code

```
ALTER SNAPSHOT [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'
```

## Parameters

`name`
:   Specifies the identifier for the snapshot to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Sets one or more specified properties or parameters for the snapshot:

    `COMMENT = string-literal`
    :   Specifies a comment for the snapshot.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Snapshot | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example sets a comment on the `example_snapshot` snapshot.

Copy code

```
ALTER SNAPSHOT example_snapshot SET COMMENT = 'sample comment.';
```
