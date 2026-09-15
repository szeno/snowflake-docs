Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ABORT\_TRANSACTION

Aborts the specified transaction, if it is running. If the transaction has already been committed or rolled back, then the state of the
transaction is not altered.

For more information, see [Transactions](/sql-reference/transactions).

## Syntax

Copy code

```
SYSTEM$ABORT_TRANSACTION(<transaction_id>)
```

## Arguments

`transaction_id`
:   Identifier for the transaction to abort. To obtain transaction IDs,
    you can use the [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions) or
    [SHOW LOCKS](/sql-reference/sql/show-locks) commands.

## Usage notes

- This function is supported for explicit/multi-statement transactions only. Autocommit transactions can be aborted by aborting the associated job.
- Note that DDL statements, including “CREATE TABLE AS SELECT …” will implicitly commit an open transaction. After the implicit commit finishes, the previously open transaction cannot be aborted.
- Transactions can be aborted only by the user who started the transaction or an account administrator.

## Examples

> Copy code
>
> ```
> SHOW LOCKS IN ACCOUNT;
>
> --------------+--------+---------------+---------------------------------+---------+---------------------------------+--------------------------------------+
>    session    | table  |  transaction  |     transaction_started_on      | status  |           acquired_on           |               query_id               |
> --------------+--------+---------------+---------------------------------+---------+---------------------------------+--------------------------------------+
>  103079321618 | ORDERS | 1442254688149 | Mon, 14 Sep 2015 11:18:08 -0700 | HOLDING | Mon, 14 Sep 2015 11:18:16 -0700 | 6a478582-9e8c-4603-b5bf-89b14c042e1a |
>  103079325702 | ORDERS | 1442255439400 | Mon, 14 Sep 2015 11:30:39 -0700 | WAITING | [NULL]                          | 82fea8a6-a679-4de1-b6e9-7a80905831cf |
> --------------+--------+---------------+---------------------------------+---------+---------------------------------+--------------------------------------+
>
> SELECT SYSTEM$ABORT_TRANSACTION(1442254688149);
>
> -----------------------------------------+
>  SYSTEM$ABORT_TRANSACTION(1442254688149) |
> -----------------------------------------+
>  Aborted transaction id: 1442254688149   |
> -----------------------------------------+
> ```
