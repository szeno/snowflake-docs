# SHOW TRANSACTIONS

List all running transactions. The command can be used to show transactions for the current user or all users in the account.

See also:
:   [SHOW LOCKS](/sql-reference/sql/show-locks)

## Syntax

Copy code

```
SHOW TRANSACTIONS [ IN ACCOUNT ]
```

## Parameters

`IN ACCOUNT`
:   Shows all transactions across all users in the account. It can only be used by users with the ACCOUNTADMIN role (i.e. account administrators).

## Output

The command output shows transaction metadata in the following columns:

| Column | Description |
| --- | --- |
| `id` | Transaction ID (a signed 64-bit integer). |
| `user` | Current user. |
| `session` | Session ID. |
| `name` | User-defined name or system-generated name (UUID) for the transaction. |
| `started_on` | Timestamp that specifies when the transaction started executing. |
| `state` | Transaction state: `running`. |
| `scope` | ID of the operation that created a stored procedure in a scoped transaction. `0` for non-scoped transactions. |

Expand

Show lessSee more

## Usage notes

- The command output includes the IDs for all running transactions. These IDs can be used as input for
  [SYSTEM$ABORT\_TRANSACTION](/sql-reference/functions/system_abort_transaction) to abort a specified transaction.
- A stored procedure that contains a transaction can be called from within another transaction. These
  transactions are separate but “scoped.” The values in the `scope` column are useful for discovering whether two transactions are in the same scope.
  For more information, see [Scoped transactions](/sql-reference/transactions#label-scoped-transactions).

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

## Example

In this example, two sessions are being run by the same user, with one transaction in progress for each session.

Copy code

```
SHOW TRANSACTIONS;
```

```
+---------------------+---------+-----------------+--------------------------------------+-------------------------------+---------+-------+
|                  id | user    |         session | name                                 | started_on                    | state   | scope |
|---------------------+---------+-----------------+--------------------------------------+-------------------------------+---------+-------|
| 1721165674582000000 | CALIBAN | 186457423713330 | 551f494d-90ed-438d-b32b-1161396c3a22 | 2024-07-16 14:34:34.582 -0700 | running |     0 |
| 1721165584820000000 | CALIBAN | 186457423749354 | a092aa44-9a0a-4955-9659-123b35c0efeb | 2024-07-16 14:33:04.820 -0700 | running |     0 |
+---------------------+---------+-----------------+--------------------------------------+-------------------------------+---------+-------+
```
