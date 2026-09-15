# SHOW LOCKS

Lists all running transactions that have locks on resources. The command can be used to show locks for the current user in all the
user’s sessions or all users in the account.

For information about transactions and resource locking, see [Transactions](/sql-reference/transactions).

See also:
:   [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions)

## Syntax

Copy code

```
SHOW LOCKS [ IN ACCOUNT ]
```

## Parameters

`IN ACCOUNT`
:   Returns all locks across all users in the account. This parameter only applies when executed by users with the ACCOUNTADMIN role
    (account administrators).

    For all other roles, the function only shows locks across all sessions for the current user.

## Output

The command output shows lock metadata in the following columns:

| Column | Description |
| --- | --- |
| `resource` | A fully qualified table name or a transaction ID. |
| `type` | `PARTITIONS` (for standard table locks) or `ROW` (for hybrid table locks). |
| `transaction` | Transaction ID (a signed 64-bit integer). |
| `transaction_started_on` | Timestamp that specifies when the transaction started executing. |
| `status` | Current status of the transaction: `HOLDING` or `WAITING`. |
| `acquired_on` | Timestamp that specifies when the lock was acquired. |
| `query_id` | Internal/system-generated identifier for the SQL statement. |
| `session` | Session ID (visible to users with the ACCOUNTADMIN role only). |

Expand

Show lessSee more

## Usage notes

- The command output includes the IDs for all running transactions that have locks on resources. These IDs can be used as input for
  [SYSTEM$ABORT\_TRANSACTION](/sql-reference/functions/system_abort_transaction) to abort a specified transaction.
- For hybrid tables, this command displays a lock only if a transaction is blocked, or is blocking another transaction.

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

In this example, a transaction is holding a lock on the specified standard table (the table named in the `resource` column).

Copy code

```
SHOW LOCKS;
```

```
+---------------------------+------------+---------------------+-------------------------------+---------+-------------------------------+--------------------------------------+
| resource                  | type       |         transaction | transaction_started_on        | status  | acquired_on                   | query_id                             |
|---------------------------+------------+---------------------+-------------------------------+---------+-------------------------------+--------------------------------------|
| CALIBAN_DB.PUBLIC.WEATHER | PARTITIONS | 1721330303831000000 | 2024-07-18 12:18:23.831 -0700 | HOLDING | 2024-07-18 12:18:49.832 -0700 | 01b5c1c6-0002-8691-0000-a9950068a0c6 |
+---------------------------+------------+---------------------+-------------------------------+---------+-------------------------------+--------------------------------------+
```

In this example, a transaction is holding a row-level lock on a hybrid table. Another transaction is waiting on
that lock.

Copy code

```
SHOW LOCKS;
```

```
+---------------------+------+---------------------+-------------------------------+---------+-------------+--------------------------------------+
| resource            | type |         transaction | transaction_started_on        | status  | acquired_on | query_id                             |
|---------------------+------+---------------------+-------------------------------+---------+-------------+--------------------------------------|
| 1721165584820000000 | ROW  | 1721165584820000000 | 2024-07-16 14:33:04.820 -0700 | HOLDING | NULL        |                                      |
| 1721165584820000000 | ROW  | 1721165674582000000 | 2024-07-16 14:34:34.582 -0700 | WAITING | NULL        | 01b5b715-0002-852b-0000-a99500665352 |
+---------------------+------+---------------------+-------------------------------+---------+-------------+--------------------------------------+
```
