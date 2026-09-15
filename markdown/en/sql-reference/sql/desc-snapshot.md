# DESCRIBE SNAPSHOT

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Describes the properties of a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot) , [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot), [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot), [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots)

## Syntax

Copy code

```
{ DESC | DESCRIBE } SNAPSHOT <name>
```

## Parameters

`name`
:   Specifies the identifier for the snapshot to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the snapshot. |
| `state` | One of the following values, which indicates the current status of the snapshot:   - INITIALIZED: The snapshot creation is in progress. - CREATED: The snapshot is created and can be used to create a volume. - ERROR: Snapshot creation failed. |
| `database_name` | Database in which the snapshot is created. |
| `schema_name` | Schema in which the snapshot is created. |
| `service_name` | Fully qualified service name from which the snapshot is created. |
| `volume_name` | Volume from the specified service instance for which the snapshot is created. |
| `instance` | ID of the service instance. |
| `size` | Size (in GB) of the snapshot. |
| `comment` | General comment about the snapshot. |
| `owner` | Role that owns the snapshot. |
| `owner_role_type` | The type of role that owns the object, either ROLE or DATABASE\_ROLE. |
| `created_on` | Date and time when the snapshot was created. |
| `encryption` | Encryption type configured for the volume, from which the snapshot was created. Possible values include `SNOWFLAKE_SSE` and `SNOWFLAKE_FULL`. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | Snapshot | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

## Examples

The following example describes the snapshot named `my_snapshot`:

Copy code

```
DESC SNAPSHOT my_snapshot;
```

Output:

```
+-------------+---------+---------------+-------------+----------------------------------------------------+-------------+----------+------+--------------+-----------+-----------------+-------------------------------+-------------------------------+---------------+
| name        | state   | database_name | schema_name | service_name                                       | volume_name | instance | size | comment      | owner     | owner_role_type | created_on                    | updated_on                    | encryption    |
|-------------+---------+---------------+-------------+----------------------------------------------------+-------------+----------+------+--------------+-----------+-----------------+-------------------------------+-------------------------------+---------------|
| MY_SNAPSHOT | CREATED | TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_DB.DATA_SCHEMA.MY_SERVICE_WITH_EBS_VOLUME | block-vol1  | 0        |   10 | new snapshot | TEST_ROLE | ROLE            | 2024-05-09 21:36:58.502 -0700 | 2024-05-09 21:38:03.424 -0700 | SNOWFLAKE_SSE |
+-------------+---------+---------------+-------------+----------------------------------------------------+-------------+----------+------+--------------+-----------+-----------------+-------------------------------+-------------------------------+---------------+
```
