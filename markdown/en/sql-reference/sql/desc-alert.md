# DESCRIBE ALERT

Describes the properties of an [alert](/user-guide/alerts).

See also:
:   [CREATE ALERT](/sql-reference/sql/create-alert) , [ALTER ALERT](/sql-reference/sql/alter-alert), [DROP ALERT](/sql-reference/sql/drop-alert) , [SHOW ALERTS](/sql-reference/sql/show-alerts) , [EXECUTE ALERT](/sql-reference/sql/execute-alert)

## Syntax

Copy code

```
DESC[RIBE] ALERT <name>
```

## Required parameters

`name`
:   Identifier for the alert to describe. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR, OPERATE, or OWNERSHIP | Alert | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command provides the same output as [SHOW ALERTS](/sql-reference/sql/show-alerts).

## Usage notes

- Only returns rows for an alert owner (i.e. the role with the OWNERSHIP privilege on an alert) or a role with the OPERATE
  privilege on an alert.

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

See [Viewing details about an alert](/user-guide/alerts#label-alerts-show-desc).
