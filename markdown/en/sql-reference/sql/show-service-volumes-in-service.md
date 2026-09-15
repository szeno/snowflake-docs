# SHOW SERVICE VOLUMES IN SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the storage volumes for all instances of a [service](/developer-guide/snowpark-container-services/working-with-services).
For each mounted volume, the output includes a line for every
container mounting that volume. The output shows only volumes that are mounted to at least one container
in the service; volumes specified but unused by any container aren’t included.

See also:
:   [Snowpark Container Services overview](/developer-guide/snowpark-container-services/overview),
    [CREATE SERVICE](/sql-reference/sql/create-service), [SHOW SERVICES](/sql-reference/sql/show-services),
    [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service), [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service),
    [SHOW <objects>](/sql-reference/sql/show)

## Syntax

Copy code

```
SHOW SERVICE VOLUMES IN SERVICE <name>
```

## Parameters

`name`
:   Specifies the name of the service for which to display the list of mounted volumes.

    Quoted names for special characters or case-sensitive names aren’t supported.

## Output

The command output provides properties of service volumes in the following columns:

| Column | Description |
| --- | --- |
| `volume_name` | Name of the volume |
| `instance_id` | ID of the service instance, which is the index of the service instance starting from 0. |
| `container_name` | Name of the container to which a volume is mounted. |
| `volume_type` | Type of the volume. This can be one of the following types:   - `block` - `stage` - `local` - `memory`   For a detailed description of volume types, see [service specification](/developer-guide/snowpark-container-services/specification-reference). |
| `size` | Size of the volume in the format of `numberGi`. |
| `iops` | Only applicable to block volumes. Shows the configured input/output operations per second for each block volume. |
| `throughput` | Only applicable to block volumes. Shows the configured throughput for each block volume. |
| `encryption` | Only applicable to stage and block volumes. In the case of block volumes, it shows the configured volume encryption type. For a detailed description of block volumes encryption types, see [Encryption Support for block storage volumes](/developer-guide/snowpark-container-services/block-storage-volume). In the case of stage volumes, it shows the encryption type of the underlying stage. USAGE or OWNERSHIP privilege on a stage for the caller is required to get the stage encryption information. |
| `snapshot_used` | Only applicable to block volumes. Shows which snapshot was used to create the volume. The snapshot is listed in this column only if you are using a role that has been granted to the USAGE or OWNERSHIP privilege on the snapshot. |
| `stage_source` | Only applicable to stage volumes. Shows the fully qualified name for a stage that is used for the stage volume. |
| `volume_mounts` | Comma-separated list of paths where the volume is mounted in the given container. |

Expand

Show lessSee more

If a field is applicable to specific volume types, it is populated with NULL for every other volume type.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MONITOR | Service | None |
| OWNERSHIP or USAGE | Snapshot | Without access to a block storage snapshot, Snowflake populates the `snapshot_used` field with an authorization error, but the command doesn’t fail. |
| OWNERSHIP or USAGE | Stage | Without access to a stage, Snowflake populates the encryption field with an authorization error for stage volumes, but the command doesn’t fail. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists the volumes for the `echo_service` service:

Copy code

```
SHOW SERVICE VOLUMES IN SERVICE echo_service;
```

Sample output:

```
+----------------+-------------+----------------+-------------+--------+--------+------------+----------------+---------------+--------------+---------------------------+
| volume_name    | instance_id | container_name | volume_type |  size  |  iops  | throughput |   encryption   | snapshot_used | stage_source |       volume_mounts       |
+----------------+-------------+----------------+-------------+--------+--------+------------+----------------+---------------+--------------+---------------------------+
| block-volume-1 | 0           | main           | block       | 1Gi    | 3000   | 125        | SNOWFLAKE_SSE  | [NULL]        | [NULL]       | /tmp/block1               |
| block-volume-1 | 0           | secondary      | block       | 1Gi    | 3000   | 125        | SNOWFLAKE_SSE  | [NULL]        | [NULL]       | /data/shared              |
| block-volume-2 | 0           | main           | block       | 50Gi   | 3500   | 150        | SNOWFLAKE_FULL | [NULL]        | [NULL]       | /tmp/block2               |
| local-volume   | 0           | main           | local       | [NULL] | [NULL] | [NULL]     | [NULL]         | [NULL]        | [NULL]       | /tmp/local                |
| memory-volume  | 0           | main           | memory      | 512Mi  | [NULL] | [NULL]     | [NULL]         | [NULL]        | [NULL]       | /tmp/memory, /tmp/memory2 |
| memory-volume  | 0           | secondary      | memory      | 512Mi  | [NULL] | [NULL]     | [NULL]         | [NULL]        | [NULL]       | /cache/memory             |
+----------------+-------------+----------------+-------------+--------+--------+------------+----------------+---------------+--------------+---------------------------+
```
