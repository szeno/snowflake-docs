# COMMIT

Commits an open transaction in the current session.

See also:
:   [BEGIN](/sql-reference/sql/begin) , [ROLLBACK](/sql-reference/sql/rollback) , [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions) , [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction)

## Syntax

Copy code

```
COMMIT [ WORK ]
```

## Parameters

`WORK`
:   Optional keyword that provides compatibility with other database systems.

## Usage notes

- If two COMMIT statements in a row are executed (within the same [scope](/sql-reference/transactions#label-scoped-transactions)), the
  second one is ignored. For example, in the following code, the second COMMIT has no effect; there is no open
  transaction to commit.

  Copy code

  ```
  BEGIN;
  INSERT INTO table1 ...;
  COMMIT;
  COMMIT;  -- Ignored!
  ```

  The rules can be more complex if you are using
  [autonomous scoped transactions and stored procedures](/sql-reference/transactions#label-transactions-stored-procedures-and-transactions).

## Examples

Begin a transaction, insert some values into a table, then complete the transaction by committing it:

Copy code

```
SELECT COUNT(*) FROM A1;

+----------+
| COUNT(*) |
|----------+
|        0 |
+----------+

BEGIN NAME T3;

SELECT CURRENT_TRANSACTION();

+-----------------------+
| CURRENT_TRANSACTION() |
|-----------------------+
| 1432071497832         |
+-----------------------+

INSERT INTO A1 VALUES (1), (2);

+-------------------------+
| number of rows inserted |
|-------------------------+
|                       2 |
+-------------------------+

COMMIT;

SELECT CURRENT_TRANSACTION();

+-----------------------+
| CURRENT_TRANSACTION() |
|-----------------------+
| [NULL]                |
+-----------------------+

SELECT LAST_TRANSACTION();

+--------------------+
| LAST_TRANSACTION() |
|--------------------+
| 1432071497832      |
+--------------------+

SELECT COUNT(*) FROM A1;

+----------+
| COUNT(*) |
|----------+
|        2 |
+----------+
```
