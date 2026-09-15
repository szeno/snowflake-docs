# UNDROP SNAPSHOT

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Restores a previously removed [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). After Snowflake restores the snapshot, the data is available for use.

See also:
:   [Managing snapshots](/developer-guide/snowpark-container-services/block-storage-volume#label-snowpark-containers-block-storage-manage-snapshots), [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot), [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot)

## Syntax

Copy code

```
UNDROP SNAPSHOT { <name> | IDENTIFIER( <id> ) }
 [ RENAME TO <new_snapshot_name> ];
```

## Parameters

`name`
:   Specifies the name of the snapshot to restore. If you specify a snapshot name, the command restores the most recently dropped snapshot with that name.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`IDENTIFIER( id )`
:   Specifies the system-generated identifier for the snapshot to restore.

    If you have multiple dropped snapshots with the same name, you can query the [BLOCK\_STORAGE\_SNAPSHOTS view](/sql-reference/account-usage/block_storage_snapshots) to get the system-generated identifier of the dropped snapshot that you want to restore. Then, use the [IDENTIFIER keyword](/sql-reference/identifier-literal) to specify that you want to restore this snapshot. The restored snapshot keeps its original name.

    For an example of restoring a snapshot by system-generated identifier, see [Examples](#examples).

    Note

    You can only use the system-generated identifier with the IDENTIFIER() keyword when executing the UNDROP command for notebooks, tables, block storage snapshots, schemas, and databases.

`RENAME TO new_snapshot_name`
:   Specifies the name for the snapshot after it is restored. This lets you restore the snapshot to a different name.

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

- Snapshots can only be restored to the database and schema where the snapshot was located at the time of deletion. For example, if you
  create and drop a snapshot in schema `s1`, then change the current schema in your session to `s2` and attempt to undrop the
  snapshot, the snapshot will be restored in schema `s1`, not in the current schema `s2`.
- If a snapshot with the same name already exists, UNDROP SNAPSHOT returns an error.
  In this case, you have the option to specify a different name by using `RENAME TO` parameter.
- UNDROP SNAPSHOT relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be
  restored only if the object was deleted within the [data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period).
  The default retention period is 24 hours. After the data retention period has passed, you can’t restore the snapshot.

## Examples

### Restore snapshot using name

The following example restores a previously dropped snapshot named `example_snapshot`:

Copy code

```
UNDROP SNAPSHOT example_snapshot;
```

```
+--------------------------------------------------+
| status                                           |
|--------------------------------------------------|
| Snapshot EXAMPLE_SNAPSHOT successfully restored. |
+--------------------------------------------------+
```

### Restore snapshot using ID

Restore a dropped snapshot by ID using [IDENTIFIER()](/sql-reference/identifier-literal). You can find the snapshot ID of the specific snapshot to restore by using the snapshot\_id column in the [BLOCK\_STORAGE\_SNAPSHOTS view](/sql-reference/account-usage/block_storage_snapshots) view. For example, if you have multiple dropped snapshots named `MY_SNAPSHOT`, and you want to restore the second-to-last dropped snapshot `MY_SNAPSHOT`, follow these steps:

1. In the Account Usage BLOCK\_STORAGE\_SNAPSHOTS view, find the snapshot ID of the dropped snapshot:

   Copy code

   ```
   SELECT snapshot_id,
    snapshot_name,
    database_name,
    schema_name,
    created_on,
    deleted_on
     FROM SNOWFLAKE.ACCOUNT_USAGE.BLOCK_STORAGE_SNAPSHOTS
     WHERE database_name = 'TUTORIAL_DB'
    AND schema_name = 'DATA_SCHEMA'
    AND snapshot_name = 'MY_SNAPSHOT'
    AND deleted_on IS NOT NULL
     ORDER BY deleted_on;
   ```

   Example output:

   ```
   +-------------+---------------+---------------+-------------+-------------------------------+-------------------------------+
   | SNAPSHOT_ID | SNAPSHOT_NAME | DATABASE_NAME | SCHEMA_NAME | CREATED_ON                    | DELETED_ON                    |
   |-------------+---------------+---------------+-------------+-------------------------------+-------------------------------|
   |           1 | MY_SNAPSHOT   | TUTORIAL_DB   | DATA_SCHEMA | 2025-09-06 09:51:47.131 -0700 | 2025-09-15 14:21:49.683 -0700 |
   +-------------+---------------+---------------+-------------+-------------------------------+-------------------------------+
   ```
2. Undrop `MY_SNAPSHOT` by snapshot ID; to restore the second-to-last deleted snapshot, use snapshot ID 1 from the output of the previous statement.

   After you execute the following statement, the snapshot is restored with its original name, `MY_SNAPSHOT`:

   Copy code

   ```
   UNDROP SNAPSHOT IDENTIFIER(1);
   ```
