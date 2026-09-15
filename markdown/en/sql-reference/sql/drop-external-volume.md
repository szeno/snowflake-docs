# DROP EXTERNAL VOLUME

Removes an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) from the account, but retains a version of the
external volume so that it can be recovered using [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume). For more information, see [Usage Notes](#usage-notes) (in this topic).

See also:
:   [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) , [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) , [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes) , [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume)

## Syntax

Copy code

```
DROP EXTERNAL VOLUME [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the external volume to drop. If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External volume | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t drop or replace an external volume if one or more Iceberg tables
  are associated with the external volume.

  To view the tables that depend on an external volume,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `external_volume_name` column.

  Note

  The column identifier (`external_volume_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "external_volume_name" = 'my_external_volume_1';
  ```
- Dropping an external volume does not permanently remove it from the system. Snowflake retains a version of the dropped external volume in
  [Time Travel](/user-guide/data-time-travel). You can restore a dropped external volume by using
  the [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume) command.
- After a dropped external volume has been purged, it cannot be recovered; it must be recreated.
- After dropping an external volume, creating an external volume with the same name creates a new version of the external volume.
  You can restore the dropped version of the previous external volume by following these steps:
  1. Rename the current version of the external volume.
  2. Use the [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume) command to restore the previous version.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops an external volume named `my_external_volume`:

> Copy code
>
> ```
> DROP EXTERNAL VOLUME my_external_volume;
> ```
