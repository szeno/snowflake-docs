# DROP SNAPSHOT

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Removes a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). A snapshot is persisted data that the customer pays for. DROP SNAPSHOT tells Snowflake to delete that data. The data is no longer available for use as a snapshot and the customer no longer pays for it.

See also:
:   [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot) , [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot), [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot), [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots)

## Syntax

Copy code

```
DROP SNAPSHOT [ IF EXISTS ] <name>;
```

## Parameters

`name`
:   Specifies the identifier for the snapshot to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

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

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- Dropping a snapshot does not immediately remove it from the system. A version of the dropped snapshot is retained in [Time Travel](/user-guide/data-time-travel) for
  the number of days specified by the DATA\_RETENTION\_TIME\_IN\_DAYS parameter for the parent schema, database, or account:

  - Within the Time Travel retention period, a dropped snapshot can be restored using the UNDROP SNAPSHOT command.
  - After the Time Travel retention period, it is permanently removed; it must be recreated.

  For more information, see [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period).
- To immediately drop a snapshot without retention, set DATA\_RETENTION\_TIME\_IN\_DAYS to 0 at the schema level where the snapshot resides. This setting also affects the retention period for other objects within that schema.

## Examples

The following example drops the snapshot named `example_snapshot`:

Copy code

```
DROP SNAPSHOT example_snapshot;
```

```
+----------------------------------------+
| status                                 |
|----------------------------------------|
| EXAMPLE_SNAPSHOT successfully dropped. |
+----------------------------------------+
```
