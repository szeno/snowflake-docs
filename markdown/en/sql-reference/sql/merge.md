# MERGE

Inserts, updates, and deletes values in a table that are based on values in a second table or a subquery. Merging can be
useful if the second table is a change log that contains new rows (to be inserted), modified rows (to be updated),
or marked rows (to be deleted) in the target table.

The command supports semantics for handling the following cases:

- Values that match (for updates and deletes).
- Values that don’t match (for inserts).

See also:
:   [DELETE](/sql-reference/sql/delete) , [UPDATE](/sql-reference/sql/update)

## Syntax

Copy code

```
MERGE INTO <target_table>
  USING <source>
  ON <join_expr>
  { matchedClause | notMatchedClause } [ ... ]
```

Where:

> Copy code
>
> ```
> matchedClause ::=
>   WHEN MATCHED
>     [ AND <case_predicate> ]
>     THEN { UPDATE { ALL BY NAME | SET <col_name> = <expr> [ , <col_name> = <expr> ... ] } | DELETE } [ ... ]
> ```
>
> Copy code
>
> ```
> notMatchedClause ::=
>    WHEN NOT MATCHED
>      [ AND <case_predicate> ]
>      THEN INSERT { ALL BY NAME | [ ( <col_name> [ , ... ] ) ] VALUES ( <expr> [ , ... ] ) }
> ```

## Parameters

`target_table`
:   Specifies the table to merge.

`source`
:   Specifies the table or subquery to join with the target table.

`join_expr`
:   Specifies the expression on which to join the target table and source.

### `matchedClause` (for updates or deletes)

`WHEN MATCHED ... AND case_predicate`
:   Optionally specifies an expression which, when true, causes the matching case to be executed.

    Default: No value (matching case is always executed)

`WHEN MATCHED ... THEN { UPDATE { ALL BY NAME | SET ... } | DELETE }`
:   Specifies the action to perform when the values match.

    `ALL BY NAME`
    :   Updates all columns in the target table with values from the source. Each column in
        the target table is updated with the values of the column with the same name from the source.

        The target table and source must have the same number of columns and the same names for all of the
        columns. However, the column order can be different between the target table and the source.

    `SET col_name = expr [ , col_name = expr ... ]`
    :   Updates the specified column in the target table by using the corresponding expression for the new column
        value (can refer to both the target and source relations).

        In a single `SET` subclause, you can specify multiple columns to update.

    `DELETE`
    :   Deletes the rows in the target table when they match the source.

### `notMatchedClause` (for inserts)

`WHEN NOT MATCHED ... AND case_predicate`
:   Optionally specifies an expression which, when true, causes the not-matching case to be executed.

    Default: No value (not-matching case is always executed)

`WHEN NOT MATCHED ... THEN INSERT` `{ ALL BY NAME | [ ( col_name [ , ... ] ) ] VALUES ( expr [ , ... ] ) }`
:   Specifies the action to perform when the values don’t match.

    `ALL BY NAME`
    :   Inserts all columns in the target table with values from the source. Each column in
        the target table is inserted with the values of the column with the same name from the source.

        The target table and source must have the same number of columns and the same names for all of the
        columns. However, the column order can be different between the target table and the source.

    `( col_name [ , ... ] )`
    :   Optionally specifies one or more columns in the target table to be inserted with values from the source.

        Default: No value (all columns in the target table are inserted)

    `VALUES ( expr [ , ... ] )`
    :   Specifies the corresponding expressions for the inserted column values (must refer to the source relations).

## Usage notes

- A single MERGE statement can include multiple matching and not-matching clauses (that is, `WHEN MATCHED ...` and
  `WHEN NOT MATCHED ...`).
- Any matching or not-matching clause that omits the `AND` subclause (default behavior) must be the last of its clause
  type in the statement (for example, a `WHEN MATCHED ...` clause can’t be followed by a `WHEN MATCHED AND ...` clause). Doing
  so results in an unreachable case, which returns an error.

## Duplicate join behavior

When multiple rows in the source table match a single row in the target table, the results can be deterministic or nondeterministic.
This section describes MERGE behavior for these use cases.

### Nondeterministic results for UPDATE and DELETE

When a merge joins a row in the target table against multiple rows in the source, the following join conditions produce nondeterministic
results (that is, the system is unable to determine the source value to use to update or delete the target row):

- A target row is selected to be updated with multiple values (for example, `WHEN MATCHED ... THEN UPDATE`).
- A target row is selected to be both updated and deleted (for example, `WHEN MATCHED ... THEN UPDATE` , `WHEN MATCHED ... THEN DELETE`).

In this situation, the outcome of the merge depends on the value specified for the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](/sql-reference/parameters#label-error-on-nondeterministic-merge) session
parameter:

- If TRUE (default value), the merge returns an error.
- If FALSE, one row from among the duplicates is selected to perform the update or delete; the row selected is not defined.

### Deterministic results for UPDATE and DELETE

Deterministic merges always complete without error. A merge is deterministic if it meets *at least one* of the following conditions
for each target row:

- One or more source rows satisfy the `WHEN MATCHED ... THEN DELETE` clauses, and no other source rows satisfy any
  `WHEN MATCHED` clauses
- Exactly one source row satisfies a `WHEN MATCHED ... THEN UPDATE` clause, and no other source rows satisfy any
  `WHEN MATCHED` clauses.

This makes MERGE semantically equivalent to the [UPDATE](/sql-reference/sql/update) and [DELETE](/sql-reference/sql/delete) commands.

Note

To avoid errors when multiple rows in the data source (that is, the source table or subquery) match the target table based on the ON
condition, use [GROUP BY](/sql-reference/constructs/group-by) in the source clause to ensure that each target row joins against one row
(at most) in the source.

In the following example, assume `src` includes multiple rows with the same `k` value. It’s ambiguous which values (`v`) will
be used to update rows in the target row with the same value of `k`. By using the MAX function and GROUP BY, the query clarifies exactly
which value of `v` from `src` is used:

Copy code

```
MERGE INTO target
  USING (SELECT k, MAX(v) AS v FROM src GROUP BY k) AS b
  ON target.k = b.k
  WHEN MATCHED THEN UPDATE SET target.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);
```

### Deterministic results for INSERT

Deterministic merges always complete without error.

If the MERGE statement contains a `WHEN NOT MATCHED ... THEN INSERT` clause, and if there are no matching rows in the target, and if the
source contains duplicate values, then the target gets one copy of the row for *each* copy in the source. For an example,
see [Perform a merge with source duplicates](#label-merge-example-source-duplicates).

## Examples

The following examples use the MERGE command:

- [Perform a basic merge that updates values](#label-merge-example-basic-updates)
- [Perform a basic merge with multiple operations](#label-merge-example-basic-multiple-operations)
- [Perform a merge by using ALL BY NAME](#label-merge-example-all)
- [Perform a merge with source duplicates](#label-merge-example-source-duplicates)
- [Perform a merge with deterministic and nondeterministic results](#label-merge-example-deterministic-nondeterministic)
- [Perform a merge based on DATE values](#label-merge-example-date-values)

### Perform a basic merge that updates values

The following example performs a basic merge that updates values in the target table by using values from the source
table. Create and load two tables:

Copy code

```
CREATE OR REPLACE TABLE merge_example_target (id INTEGER, description VARCHAR);

INSERT INTO merge_example_target (id, description) VALUES
  (10, 'To be updated (this is the old value)');

CREATE OR REPLACE TABLE merge_example_source (id INTEGER, description VARCHAR);

INSERT INTO merge_example_source (id, description) VALUES
  (10, 'To be updated (this is the new value)');
```

Display the values in the tables:

Copy code

```
SELECT * FROM merge_example_target;
```

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the old value) |
+----+---------------------------------------+
```

Copy code

```
SELECT * FROM merge_example_source;
```

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

Run the MERGE statement:

Copy code

```
MERGE INTO merge_example_target
  USING merge_example_source
  ON merge_example_target.id = merge_example_source.id
  WHEN MATCHED THEN
    UPDATE SET merge_example_target.description = merge_example_source.description;
```

```
+------------------------+
| number of rows updated |
|------------------------|
|                      1 |
+------------------------+
```

Display the new values in the target table (the source table is unchanged):

Copy code

```
SELECT * FROM merge_example_target;
```

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

Copy code

```
SELECT * FROM merge_example_source;
```

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

### Perform a basic merge with multiple operations

Perform a basic merge with a mix of operations (INSERT, UPDATE, and DELETE).

Create and load two tables:

Copy code

```
CREATE OR REPLACE TABLE merge_example_mult_target (
  id INTEGER,
  val INTEGER,
  status VARCHAR);

INSERT INTO merge_example_mult_target (id, val, status) VALUES
  (1, 10, 'Production'),
  (2, 20, 'Alpha'),
  (3, 30, 'Production');

CREATE OR REPLACE TABLE merge_example_mult_source (
  id INTEGER,
  marked VARCHAR,
  isnewstatus INTEGER,
  newval INTEGER,
  newstatus VARCHAR);

INSERT INTO merge_example_mult_source (id, marked, isnewstatus, newval, newstatus) VALUES
  (1, 'Y', 0, 10, 'Production'),
  (2, 'N', 1, 50, 'Beta'),
  (3, 'N', 0, 60, 'Deprecated'),
  (4, 'N', 0, 40, 'Production');
```

Display the values in the tables:

Copy code

```
SELECT * FROM merge_example_mult_target;
```

```
+----+-----+------------+
| ID | VAL | STATUS     |
|----+-----+------------|
|  1 |  10 | Production |
|  2 |  20 | Alpha      |
|  3 |  30 | Production |
+----+-----+------------+
```

Copy code

```
SELECT * FROM merge_example_mult_source;
```

```
+----+--------+-------------+--------+------------+
| ID | MARKED | ISNEWSTATUS | NEWVAL | NEWSTATUS  |
|----+--------+-------------+--------+------------|
|  1 | Y      |           0 |     10 | Production |
|  2 | N      |           1 |     50 | Beta       |
|  3 | N      |           0 |     60 | Deprecated |
|  4 | N      |           0 |     40 | Production |
+----+--------+-------------+--------+------------+
```

The following merge example performs the following actions on the `merge_example_mult_target` table:

- Deletes the row with `id` set to `1` because the `marked` column for the row with the same `id` is
  `Y` in `merge_example_mult_source`.
- Updates the `val` and `status` values in the row with `id` set to `2` with values in the row with the same
  `id` in `merge_example_mult_source`, because `isnewstatus` is set to `1` for the same row in
  `merge_example_mult_source`.
- Updates the `val` value in the row with `id` set to `3` with the value in the row with the same
  `id` in `merge_example_mult_source`. The MERGE statement doesn’t update the `status` value in `merge_example_mult_target`
  because `isnewstatus` is set to `0` for this row in `merge_example_mult_source`.
- Inserts the row with `id` set to `4` because the row exists in `merge_example_mult_source` and there is no
  matching row in `merge_example_mult_target`.

Copy code

```
MERGE INTO merge_example_mult_target
  USING merge_example_mult_source
  ON merge_example_mult_target.id = merge_example_mult_source.id
  WHEN MATCHED AND merge_example_mult_source.marked = 'Y'
    THEN DELETE
  WHEN MATCHED AND merge_example_mult_source.isnewstatus = 1
    THEN UPDATE SET val = merge_example_mult_source.newval, status = merge_example_mult_source.newstatus
  WHEN MATCHED
    THEN UPDATE SET val = merge_example_mult_source.newval
  WHEN NOT MATCHED
    THEN INSERT (id, val, status) VALUES (
      merge_example_mult_source.id,
      merge_example_mult_source.newval,
      merge_example_mult_source.newstatus);
```

```
+-------------------------+------------------------+------------------------+
| number of rows inserted | number of rows updated | number of rows deleted |
|-------------------------+------------------------+------------------------|
|                       1 |                      2 |                      1 |
+-------------------------+------------------------+------------------------+
```

To see the results of the merge, display the values in the `merge_example_mult_target` table:

Copy code

```
SELECT * FROM merge_example_mult_target ORDER BY id;
```

```
+----+-----+------------+
| ID | VAL | STATUS     |
|----+-----+------------|
|  2 |  50 | Beta       |
|  3 |  60 | Production |
|  4 |  40 | Production |
+----+-----+------------+
```

### Perform a merge by using ALL BY NAME

The following example performs a merge that inserts and updates values in the target table by using values from the
source table. The example uses the `WHEN MATCHED ... THEN ALL BY NAME` and
`WHEN NOT MATCHED ... THEN ALL BY NAME` subclauses to specify that the merge applies to all columns.

Create two tables with the same number of columns and the same names for the columns,
but with a different order for two of the columns:

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_all (
  id INTEGER,
  x INTEGER,
  y VARCHAR);

CREATE OR REPLACE TABLE merge_example_source_all (
  id INTEGER,
  y VARCHAR,
  x INTEGER);
```

Load the tables:

Copy code

```
INSERT INTO merge_example_target_all (id, x, y) VALUES
  (1, 10, 'Skiing'),
  (2, 20, 'Snowboarding');

INSERT INTO merge_example_source_all (id, y, x) VALUES
  (1, 'Skiing', 10),
  (2, 'Snowboarding', 25),
  (3, 'Skating', 30);
```

Display the values in the tables:

Copy code

```
SELECT * FROM merge_example_target_all;
```

```
+----+----+--------------+
| ID |  X | Y            |
|----+----+--------------|
|  1 | 10 | Skiing       |
|  2 | 20 | Snowboarding |
+----+----+--------------+
```

Copy code

```
SELECT * FROM merge_example_source_all;
```

```
+----+--------------+----+
| ID | Y            |  X |
|----+--------------+----|
|  1 | Skiing       | 10 |
|  2 | Snowboarding | 25 |
|  3 | Skating      | 30 |
+----+--------------+----+
```

Run the MERGE statement:

Copy code

```
MERGE INTO merge_example_target_all
  USING merge_example_source_all
  ON merge_example_target_all.id = merge_example_source_all.id
  WHEN MATCHED THEN
    UPDATE ALL BY NAME
  WHEN NOT MATCHED THEN
    INSERT ALL BY NAME;
```

```
+-------------------------+------------------------+
| number of rows inserted | number of rows updated |
|-------------------------+------------------------|
|                       1 |                      2 |
+-------------------------+------------------------+
```

Display the new values in the target table:

Copy code

```
SELECT *
  FROM merge_example_target_all
  ORDER BY id;
```

```
+----+----+--------------+
| ID |  X | Y            |
|----+----+--------------|
|  1 | 10 | Skiing       |
|  2 | 25 | Snowboarding |
|  3 | 30 | Skating      |
+----+----+--------------+
```

### Perform a merge with source duplicates

Perform a merge in which the source has duplicate values and the target has no matching values. All copies of the source
record are inserted into the target. For more information, see [Deterministic results for INSERT](#label-merge-deterministic-results-for-insert).

Truncate both tables and load new rows into the source table that include duplicates:

Copy code

```
TRUNCATE table merge_example_target;

TRUNCATE table merge_example_source;

INSERT INTO merge_example_source (id, description) VALUES
  (50, 'This is a duplicate in the source and has no match in target'),
  (50, 'This is a duplicate in the source and has no match in target');
```

The `merge_example_target` has no values. Display the values in the
`merge_example_source` table:

Copy code

```
SELECT * FROM merge_example_source;
```

```
+----+--------------------------------------------------------------+
| ID | DESCRIPTION                                                  |
|----+--------------------------------------------------------------|
| 50 | This is a duplicate in the source and has no match in target |
| 50 | This is a duplicate in the source and has no match in target |
+----+--------------------------------------------------------------+
```

Run the MERGE statement:

Copy code

```
MERGE INTO merge_example_target
  USING merge_example_source
  ON merge_example_target.id = merge_example_source.id
  WHEN MATCHED THEN
    UPDATE SET merge_example_target.description = merge_example_source.description
  WHEN NOT MATCHED THEN
    INSERT (id, description) VALUES
      (merge_example_source.id, merge_example_source.description);
```

```
+-------------------------+------------------------+
| number of rows inserted | number of rows updated |
|-------------------------+------------------------|
|                       2 |                      0 |
+-------------------------+------------------------+
```

Display the new values in the target table:

Copy code

```
SELECT * FROM merge_example_target;
```

```
+----+--------------------------------------------------------------+
| ID | DESCRIPTION                                                  |
|----+--------------------------------------------------------------|
| 50 | This is a duplicate in the source and has no match in target |
| 50 | This is a duplicate in the source and has no match in target |
+----+--------------------------------------------------------------+
```

### Perform a merge with deterministic and nondeterministic results

Merge records by using joins that produce nondeterministic and deterministic results.

Create and load two tables:

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_orig (k NUMBER, v NUMBER);

INSERT INTO merge_example_target_orig VALUES (0, 10);

CREATE OR REPLACE TABLE merge_example_src (k NUMBER, v NUMBER);

INSERT INTO merge_example_src VALUES (0, 11), (0, 12), (0, 13);
```

When you perform the merge in the following example, multiple updates conflict with each other. If
the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](/sql-reference/parameters#label-error-on-nondeterministic-merge) session parameter is set to `true`, the MERGE statement
returns an error. Otherwise, the MERGE statement updates `merge_example_target_clone.v` with a value
(for example, `11`, `12`, or `13`) from one of the duplicate rows (row not defined):

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_clone
  CLONE merge_example_target_orig;

MERGE INTO  merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Updates and deletes conflict with each other. If the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](/sql-reference/parameters#label-error-on-nondeterministic-merge) session
parameter is set to `true`, the MERGE statement returns an error. Otherwise, the MERGE statement either deletes the row
or updates `merge_example_target_clone.v` with a value (for example, `12` or `13`) from one of the
duplicate rows (row not defined):

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_clone
  CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v = 11 THEN DELETE
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Multiple deletes don’t conflict with each other. Joined values that don’t match any clause don’t prevent
the delete (`merge_example_src.v = 13`). The MERGE statement succeeds and the target row is deleted:

Copy code

```
CREATE OR REPLACE TABLE target CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v <= 12 THEN DELETE;
```

Joined values that don’t match any clause don’t prevent an update (`merge_example_src.v = 12, 13`).
The MERGE statement succeeds and the target row is set to `target.v = 11`:

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_clone CLONE target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v = 11
    THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Use GROUP BY in the source clause to ensure that each target row joins against one row
in the source:

Copy code

```
CREATE OR REPLACE TABLE merge_example_target_clone CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING (SELECT k, MAX(v) AS v FROM merge_example_src GROUP BY k) AS b
  ON merge_example_target_clone.k = b.k
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);
```

### Perform a merge based on DATE values

In the following example, the `members` table stores the names, addresses, and current fees (`members.fee`) paid to a
local gym. The `signup` table stores each member’s signup date (`signup.date`). The MERGE statement applies a standard
$40 fee to members who joined the gym more than 30 days ago, after the free trial expired:

Copy code

```
MERGE INTO members m
  USING (SELECT id, date
    FROM signup
    WHERE DATEDIFF(day, CURRENT_DATE(), signup.date::DATE) < -30) s
  ON m.id = s.id
  WHEN MATCHED THEN UPDATE SET m.fee = 40;
```
