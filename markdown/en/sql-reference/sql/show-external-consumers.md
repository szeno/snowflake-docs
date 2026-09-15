# SHOW EXTERNAL CONSUMERS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the external consumers defined in the account.

See also:
:   [CREATE EXTERNAL CONSUMER](/sql-reference/sql/create-external-consumer) ,
    [ALTER EXTERNAL CONSUMER](/sql-reference/sql/alter-external-consumer) ,
    [DROP EXTERNAL CONSUMER](/sql-reference/sql/drop-external-consumer) ,
    [DESCRIBE EXTERNAL CONSUMER](/sql-reference/sql/desc-external-consumer)

## Syntax

Copy code

```
SHOW EXTERNAL CONSUMERS [ LIKE '<pattern>' ]
```

## Parameters

`LIKE 'pattern'`
:   `LIKE 'pattern'`
    :   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
        wildcard characters (`%` and `_`).

        For example, the following patterns return the same results:

        `... LIKE '%testing%' ...`
        `... LIKE '%TESTING%' ...`

        Default: No value (no filtering is applied to the output).

## Access control requirements

Any role can execute this command. Results are filtered to show only the external consumers that the current role has privileges to view.

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

## Examples

List all external consumers in the account:

Copy code

```
SHOW EXTERNAL CONSUMERS;
```

List external consumers whose names match a pattern:

Copy code

```
SHOW EXTERNAL CONSUMERS LIKE 'acme%';
```
