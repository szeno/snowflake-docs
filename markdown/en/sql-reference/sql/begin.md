# BEGIN

Begins a transaction in the current session.

START TRANSACTION is a synonym for BEGIN.

See also:
:   [COMMIT](/sql-reference/sql/commit) , [ROLLBACK](/sql-reference/sql/rollback) , [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions) , [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction)

## Syntax

Copy code

```
BEGIN [ { WORK | TRANSACTION } ] [ NAME <name> ]

START TRANSACTION [ NAME <name> ]
```

## Parameters

`WORK | TRANSACTION`
:   Optional keywords that provide compatibility with other database systems.

`NAME name`
:   Optional string that assigns a name to the transaction. A name helps identify a transaction, but is not required and does not need to be unique.

## Usage notes

- All transactions have a system-generated internal ID. The transaction ID is a signed 64-bit (long) integer. The range of values is
  -9,223,372,036,854,775,808 (-2 63) to 9,223,372,036,854,775,807 (2 63 - 1).
- If you specify a name for a transaction, the NAME keyword is required.
- If a name is not specified, a system-generated name is assigned to the transaction.
- To complete a transaction, a COMMIT or ROLLBACK command must be explicitly executed. Until one of these commands is executed, the transaction
  remains open.
- When a SQL statement queries a stream within an explicit transaction, the stream is queried at the stream advance point (i.e. the timestamp)
  when the transaction began rather than when the statement was run. This behavior pertains both to DML statements and
  CREATE TABLE … AS SELECT (CTAS) statements that populate a new table with rows from an existing stream.
- If two BEGIN statements in a row are executed (within the same [scope](/sql-reference/transactions#label-scoped-transactions)), the second one is ignored. For
  example, in the following code, the second and third BEGINs have no effect; the existing open transaction continues.

  Copy code

  ```
  BEGIN;
  BEGIN;    -- Ignored!
  INSERT INTO table1 ...;
  BEGIN;    -- Ignored!
  INSERT INTO table2 ...;
  COMMIT;
  ```

  The rules can be more complex if you are using
  [autonomous scoped transactions and stored procedures](/sql-reference/transactions#label-transactions-stored-procedures-and-transactions).

## Examples

Note

These examples do not include the necessary commands for completing the transactions. For examples of complete transactions, see [COMMIT](/sql-reference/sql/commit) or [ROLLBACK](/sql-reference/sql/rollback).

Begin a transaction:

> Copy code
>
> ```
> BEGIN;
>
> SHOW TRANSACTIONS;
>
> +---------------+--------+--------------+--------------------------------------+-------------------------------+---------+
> |            id | user   |      session | name                                 | started_on                    | state   |
> |---------------+--------+--------------+--------------------------------------+-------------------------------+---------|
> | 1530042321085 | USER1  | 223347060798 | 56cb9163-77a3-4223-b3e0-aa24a20540a3 | 2018-06-26 12:45:21.085 -0700 | running |
> +---------------+--------+--------------+--------------------------------------+-------------------------------+---------+
>
> SELECT CURRENT_TRANSACTION();
>
> +-----------------------+
> | CURRENT_TRANSACTION() |
> |-----------------------|
> | 1530042321085         |
> +-----------------------+
> ```
>
> Note the system-assigned name, `56cb9163-77a3-4223-b3e0-aa24a20540a3`, for the transaction.

Begin a transaction with a specified name:

> Copy code
>
> ```
> BEGIN NAME T1;
>
> SHOW TRANSACTIONS;
>
> +---------------+--------+--------------+------+-------------------------------+---------+
> |            id | user   |      session | name | started_on                    | state   |
> |---------------+--------+--------------+------+-------------------------------+---------|
> | 1530042377426 | USER1  | 223347060798 | T1   | 2018-06-26 12:46:17.426 -0700 | running |
> +---------------+--------+--------------+------+-------------------------------+---------+
>
> SELECT CURRENT_TRANSACTION();
>
> +-----------------------+
> | CURRENT_TRANSACTION() |
> |-----------------------|
> | 1530042377426         |
> +-----------------------+
> ```

This example is the same as the previous example, but uses START TRANSACTION instead of BEGIN:

> Copy code
>
> ```
> START TRANSACTION NAME T2;
>
> SHOW TRANSACTIONS;
>
> +---------------+--------+--------------+------+-------------------------------+---------+
> |            id | user   |      session | name | started_on                    | state   |
> |---------------+--------+--------------+------+-------------------------------+---------|
> | 1530042467963 | USER1  | 223347060798 | T2   | 2018-06-26 12:47:47.963 -0700 | running |
> +---------------+--------+--------------+------+-------------------------------+---------+
>
> SELECT CURRENT_TRANSACTION();
>
> +-----------------------+
> | CURRENT_TRANSACTION() |
> |-----------------------|
> | 1530042467963         |
> +-----------------------+
> ```
