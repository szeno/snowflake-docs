Categories:
:   [Query syntax](/sql-reference/constructs)

# FOR UPDATE

Locks the rows that the query selects until the transaction that contains the query commits or
aborts.

This clause is supported for use with hybrid tables only, and is useful for transactional
workloads in which multiple transactions attempt to access the same rows at the same time.
Rows are locked for update in the sense that other transactions cannot write data to these
rows until the transaction doing the locking has been fully committed or rolled back.
However, other transactions can read the locked rows, and other rows in the same table can be
read, updated, or deleted.

Copy code

```
SELECT ...
  FROM ...
  [ ... ]
  FOR UPDATE [ NOWAIT | WAIT <wait_time> ]
```

## Parameters

`NOWAIT`
:   Returns an error if the transaction cannot lock the selected rows immediately.
    NOWAIT is the default.

`WAIT wait_time`
:   Specifies the maximum time (in seconds) that the query waits to acquire row-level locks. If
    the wait time expires, the query returns an error.

## Restrictions

The FOR UPDATE clause:

- Cannot be used with [AUTOCOMMIT transactions](/sql-reference/parameters#label-autocommit).
- Must be the last clause in the [SELECT statement](/sql-reference/constructs).
- Cannot be used in a [CTAS statement](/sql-reference/sql/create-table#label-ctas-syntax).
- Cannot be used inside [subqueries](/user-guide/querying-subqueries).
- Cannot select from [multiple tables (joins)](/sql-reference/constructs/join) or
  [set operations](/sql-reference/operators-query).
- Cannot be used when the query contains:
  - [DISTINCT](/user-guide/querying-distinct-counts)
  - [Aggregation functions](/sql-reference/functions-aggregation)
  - [GROUP BY](/sql-reference/constructs/group-by)
  - [HAVING](/sql-reference/constructs/having)
  - [Sequences](/user-guide/querying-sequences)

## Usage notes

Because hybrid tables support the READ COMMITTED isolation level, FOR UPDATE clauses do not
guarantee read stability. For example, assume that a table `T` with a single column named `ID`
contains two rows with values `5` and `10`.

1. The following query is run in transaction `T1`:

   Copy code

   ```
   SELECT * FROM T WHERE ID < 20 FOR UPDATE;
   ```

   The query returns the values `5` and `10` and locks those two rows.
2. Another transaction, `T2`, runs the following DELETE operation:

   Copy code

   ```
   DELETE FROM T WHERE ID = 5;
   ```

   Transaction `T2` has to wait until `T1` completes (that is, until it commits or rolls back).
3. However, a third transaction, `T3`, can complete the following INSERT operation:

   Copy code

   ```
   INSERT INTO T VALUES 12;
   ```
4. A subsequent query in `T1` now returns three values (rows), not two: `5`, `10`, and `12`:

   Copy code

   ```
   SELECT * FROM T WHERE ID < 20;
   ```

## Examples

Open a new transaction, select all of the rows from a hybrid table (`ht`), and lock those
rows until the transaction commits. Update some selected rows and run another query before
committing the transaction.

Copy code

```
BEGIN;
...
SELECT * FROM ht ORDER BY c1 FOR UPDATE;
...
UPDATE ht set c1 = c1 + 10 WHERE c1 = 0;
...
SELECT ... ;
...
COMMIT;
```

Apply a maximum wait time of 60 seconds for row locking:

Copy code

```
BEGIN;
...
SELECT * FROM ht FOR UPDATE WAIT 60;
...
COMMIT;
```
