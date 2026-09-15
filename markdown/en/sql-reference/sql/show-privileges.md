# SHOW PRIVILEGES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the privileges granted to an application.

## Syntax

Copy code

```
SHOW PRIVILEGES IN APPLICATION <name>
```

## Parameters

`name`
:   Specifies the name of the application.

## Output

Specifies the privileges granted to an application.

| Column | Description |
| --- | --- |
| privilege | The name of the privilege as specified in the manifest file. |
| description | A description of the privilege, which is specified in the manifest file. For details, refer to [Access control privileges](/user-guide/security-access-control-privileges). |
| is\_granted | Specifies if the consumer has granted the privilege. |
| is\_grantable | Specifies if the user running the command has an [activated role](/user-guide/security-access-control-overview#label-access-control-role-enforcement) that can grant this privilege |

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
