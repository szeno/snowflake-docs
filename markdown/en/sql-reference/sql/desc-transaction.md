# DESCRIBE TRANSACTION

Describes the [transaction](/sql-reference/transactions), including the start time and the state (running, committed, rolled
back).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CURRENT\_TRANSACTION](/sql-reference/functions/current_transaction) , [LAST\_TRANSACTION](/sql-reference/functions/last_transaction) , [BEGIN](/sql-reference/sql/begin) ,
    [COMMIT](/sql-reference/sql/commit) , [ROLLBACK](/sql-reference/sql/rollback) , [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions)

## Syntax

Copy code

```
{ DESC | DESCRIBE } TRANSACTION <transaction_id>
```

## Parameters

`transaction_id`
:   Specifies the identifier of the transaction to describe.

    `transaction_id` must be a literal, not a session variable.

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

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `id` | Unique identifier of the transaction. |
| `user` | The user ID of the user who ran the transaction. |
| `session name` | The ID of the user session in which the transaction was executed. |
| `started_on` | Date and time that the transaction was created. |
| `state` | The transaction’s completion status, e.g. committed, rolled back, or still running. |
| `ended_on` | Date and time that the transaction finished. |

Expand

Show lessSee more

## Examples

Copy code

```
DESC TRANSACTION 1651535571261000000;
```
