# SHOW EXTERNAL VOLUMES

Lists the [external volumes](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) in your account for which you have access privileges.

The output returns external volume metadata and properties.

See also:
:   [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) , [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) , [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) , [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume)

## Syntax

Copy code

```
SHOW EXTERNAL VOLUMES [ LIKE '<pattern>' ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | External volume | To see a particular external volume in the output for SHOW EXTERNAL VOLUMES, a role must have the USAGE privilege on that external volume. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the external volume. |
| `allow_writes` | Signifies whether Snowflake can write files to the storage location(s). |
| `comment` | Comment for the external volume. |

Expand

Show lessSee more

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

## Examples

Show all external volumes:

> Copy code
>
> ```
> SHOW EXTERNAL VOLUMES;
> ```

Show all the external volumes whose name starts with `aws` that you have privileges to view:

> Copy code
>
> ```
> SHOW EXTERNAL VOLUMES LIKE 'aws%';
> ```
