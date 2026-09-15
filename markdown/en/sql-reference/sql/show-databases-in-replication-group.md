# SHOW DATABASES IN REPLICATION GROUP

Lists databases in a [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

See also:
:   [SHOW SHARES IN REPLICATION GROUP](/sql-reference/sql/show-shares-in-replication-group)

## Syntax

Copy code

```
SHOW DATABASES IN REPLICATION GROUP <name>
```

## Parameters

`name`
:   Specifies the identifier for the replication group.

## Usage notes

- Executing this command requires a role with either the OWNERSHIP or MONITOR privilege on the replication group. The command
  returns results only for a role with the MONITOR privilege on a database.
- To retrieve the list of replication (and failover) groups in your organization, use [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups#label-show-replication-groups).

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

List the databases in the replication group `myrg`:

Copy code

```
SHOW DATABASES IN REPLICATION GROUP myrg;
```
