# Using lateral joins

In a [FROM](/sql-reference/constructs/from) clause, the [LATERAL](/sql-reference/constructs/join-lateral) construct allows an inline view to reference columns from preceding table expressions.

For example, if the inline view is a [subquery](/user-guide/querying-subqueries), the subquery can process rows from the table to the left of the subquery. For example:

Copy code

```
SELECT ...
  FROM left_hand_table_expression AS lhte,
    LATERAL (SELECT col_1 FROM table_2 AS t2 WHERE t2.col_1 = lhte.col_1);
```

This behavior is somewhat similar to a [correlated subquery](/user-guide/querying-subqueries#label-correlated-vs-uncorrelated-subqueries).
The subquery after the LATERAL keyword is similar to the correlated subquery itself, and the `left_hand_table_expression` is similar to the
outer query. A lateral join, unlike a correlated subquery, can return multiple rows, each of which can have multiple columns.

Other types of joins do not directly pass the left-hand table expression’s rows to the right-hand table
expression for processing.

A common use for a lateral join is to combine it with a call to the [FLATTEN](/sql-reference/functions/flatten) table function to
process a complex data structure, such as an ARRAY or VARIANT data type, and extract the values. For an example, see
[LATERAL](/sql-reference/constructs/join-lateral).

Unlike the output of other types of joins, the output from a lateral join includes only the rows
generated from the inline view (the subquery); after the rows from the subquery are generated, they are not cross-joined
to all the rows from the table on the left-hand side.

## Terminology

Consider the following code fragment:

Copy code

```
... FROM te1, LATERAL iv1 ...
```

The left-hand side of the lateral join is a table expression (`te1`).
The right-hand side of the lateral join is an inline view (`iv1`).

- *Table expression*: In this topic, the table expression on the left-hand side of a lateral join,
  such as the table expression above named `te1`, can be almost any valid
  expression that evaluates to a table. For example:

  - A table.
  - A view.
  - A subquery.
  - The output of a table function.
  - The result of an earlier join (a lateral join or other type of join).
- *Inline view*: In this topic, the expression on the right-hand side of a lateral join (in this case, `iv1`)
  is referred to as an “inline view.” In this context, a valid inline view can be one of the following:

  - A view that is defined within the statement, and valid only for the duration of the statement.
  - A subquery.
  - A table function: either a built-in table function such as FLATTEN or a user-defined table function (UDTF).

  The inline view cannot be a table.
- *Cross join*: In this topic, the term “cross join” refers not only to explicit cross joins, but also to
  inner joins and outer joins, including all variations (natural joins, left/right/full outer joins, and so on).

## A refresher on joins

A join is a two-step process. First, the server pairs up two rows,
which are usually in different tables, and which are almost always related in some way.
Second, the server joins the columns of each row in the pair into a single row.

Many of the example queries use the data shown below:

Copy code

```
CREATE TABLE departments (department_id INTEGER, name VARCHAR);
CREATE TABLE employees (employee_ID INTEGER, last_name VARCHAR,
  department_ID INTEGER, project_names ARRAY);

INSERT INTO departments (department_ID, name) VALUES
  (1, 'Engineering'),
  (2, 'Support');
INSERT INTO employees (employee_ID, last_name, department_ID) VALUES
  (101, 'Richards', 1),
  (102, 'Paulson',  1),
  (103, 'Johnson',  2);
```

Here’s a simple inner join (this is not a lateral join):

Copy code

```
SELECT *
  FROM departments AS d, employees AS e
  WHERE e.department_ID = d.department_ID
  ORDER BY employee_ID;
```

```
+---------------+-------------+-------------+-----------+---------------+---------------+
| DEPARTMENT_ID | NAME        | EMPLOYEE_ID | LAST_NAME | DEPARTMENT_ID | PROJECT_NAMES |
|---------------+-------------+-------------+-----------+---------------+---------------|
|             1 | Engineering |         101 | Richards  |             1 | NULL          |
|             1 | Engineering |         102 | Paulson   |             1 | NULL          |
|             2 | Support     |         103 | Johnson   |             2 | NULL          |
+---------------+-------------+-------------+-----------+---------------+---------------+
```

As you can see, the rows are paired based on matching department IDs.

The join takes the columns from two corresponding (“paired”) input rows and generates one output row that contains all
the columns from both input rows. (Of course, by modifying the SELECT list, you can change the columns; however,
in the simplest case, all input columns are included in the output.)

A lateral join pairs rows differently. However, the second half of the process, the “join” of paired rows, is similar:
the output row will (almost always) contain one or more columns from each member of the pair of input rows.

## How a lateral join pairs rows

A lateral join behaves differently from other types of joins. A lateral join behaves as if the server executed a loop
similar to the following:

Copy code

```
for each row in left_hand_table LHT:
  execute right_hand_subquery RHS using the values from the current row in the LHT
```

This section focuses on the “pairing” part of the process, which is different for lateral joins.

The LATERAL construct allows an inline view on the right-hand side of the lateral join to reference columns from a
table expression that is outside the view. (In the example below, the “inline view” is actually a subquery.)

Copy code

```
SELECT *
  FROM departments AS d,
    LATERAL (SELECT * FROM employees AS e WHERE e.department_ID = d.department_ID) AS iv2
  ORDER BY employee_ID;
```

```
+---------------+-------------+-------------+-----------+---------------+---------------+
| DEPARTMENT_ID | NAME        | EMPLOYEE_ID | LAST_NAME | DEPARTMENT_ID | PROJECT_NAMES |
|---------------+-------------+-------------+-----------+---------------+---------------|
|             1 | Engineering |         101 | Richards  |             1 | NULL          |
|             1 | Engineering |         102 | Paulson   |             1 | NULL          |
|             2 | Support     |         103 | Johnson   |             2 | NULL          |
+---------------+-------------+-------------+-----------+---------------+---------------+
```

In this example, the WHERE clause in the subquery on the right refers to a value from the table on the left.

The differences between a lateral join and a cross join are much greater than simply access to columns.
The next several paragraphs contrast these two types of joins, starting with the traditional cross join.

A cross join combines each row of the table on the left with each row of the table on the right. The result is a
Cartesian product.

Conceptually, a cross join is similar to a nested loop, as in the pseudo-code below:

Copy code

```
for each row in left_hand_table LHT:
  for each row in right_hand_table RHT:
    concatenate the columns of the RHT to the columns of the LHT
```

If the table on the left has *n* rows and the table on the right has *m* rows,
the result of the cross join has *n x m* rows. For example, if the table on the left
has 1000 rows and the table on the right has 100 rows, the result of
the inner join is 100,000 rows. This is just what you would expect from
nested loops; if the outer loop executes 1000 times and the inner loop
executes 100 times *per iteration of the outer loop*, the innermost statement executes 100,000 times.
(Of course, SQL programmers rarely write pure cross joins without any join conditions in the
FROM clause or WHERE clause.)

A lateral join pairs records very differently. Here’s the pseudo-code for the
implementation of a lateral join:

Copy code

```
for each row in left_hand_table LHT:
  execute right_hand_subquery RHS using the values from the LHT row,
    and concatenate LHT columns to RHS columns
```

The lateral join has only one loop, not two nested loops, which changes the output.

For the cross join, the output was 100,000 rows. For a lateral join with
the same 1000-row table on the left-hand side, and using a right-hand inline view (such as a subquery)
that emits one output row per input row, the output of the lateral join
will be 1000 rows, not 100,000 rows.

You can think of a lateral join as follows: For each input row from the left-hand table, the inline view on the right produces
0 or more rows. Each of those output rows from the subquery is then joined to the input row (*not* to the entire table on the
left-hand side) to produce a row that contains the columns selected from the subquery and the columns from the LHT input row.

The inline view on the right-hand side of a lateral join does not necessarily produce exactly one output row for each
input row. For any one input row, the output from the right-hand side might be 0 rows, 1 row, or multiple rows. Each
of those output rows will be joined to the columns of the original input row.

If the subquery does not produce exactly one output row for each input row, the lateral join does not necessarily
produce exactly as many rows as there are in the left-hand table. If the left-hand table has 1000 rows, and the
inline view produces 2 output rows for each input row, the result of the lateral join is 2000 rows.

In each of the lateral join examples so far, there was no ON clause or WHERE clause in the outer query to pair up
records. The pairing (if any) is done by the inline view based on the individual row passed into the inline view.
This is reasonably clear when the inline view is a subquery with a WHERE clause. It is not necessarily as obvious in
other cases, such as when the right-hand expression is a table function rather than a subquery. (A later example
shows a right-hand expression that uses the FLATTEN table function instead of a subquery.)

Readers who are fluent with correlated subqueries or with joins of table
functions might find the following comparisons helpful in understanding how
lateral joins differ from cross joins. Readers not familiar with correlated
subqueries or joining table functions can skip these sections.

## Similarities between correlated subqueries and lateral joins

A lateral join is similar to a correlated subquery:

- In a correlated subquery, the subquery is executed once for each row in the outer query.
- In a lateral join, the right-hand subquery (inline view) is executed once for each row in the
  left-hand table expression.

However, correlated subqueries and lateral joins are not the same. One difference is that
in a lateral join the subquery can generate more than one output row per input row,
and each output row can contain multiple columns. Correlated subqueries return only
one output row per input row, and each output row must contain only one column.

## Similarities between joining table functions and lateral joins

A lateral join is similar to a “join” between a table and a user-defined table function (UDTF).
For example, consider the following SQL statement:

Copy code

```
SELECT *
  FROM t1, TABLE(udtf2(t1.col1))
  ...
  ;
```

The pseudo-code for implementing the join between the table and the UDTF is:

Copy code

```
for each row in left_hand_table LHT:
  udtf2(row) -- that is, call udtf2() with the value(s) from the LHT row.
```

This is essentially identical to the code for implementing a lateral join:

Copy code

```
for each row in left_hand_table LHT:
  execute right_hand_subquery RHS using the values from the LHT row
```

## Example: Using a lateral join with the FLATTEN table function

Lateral joins are frequently used with the built-in [FLATTEN](/sql-reference/functions/flatten) table function. The FLATTEN function is
often used with data types that can store multiple values (such as ARRAY, VARIANT, and OBJECT). For example, an array typically
contains multiple values. Similarly, a VARIANT column can contain a JSON data value, which might contain a dictionary (hash) or list.
(And that, in turn, might contain other values.)

You can create ARRAY values as follows:

Copy code

```
UPDATE employees SET project_names = ARRAY_CONSTRUCT('Materialized Views', 'UDFs')
  WHERE employee_ID = 101;
UPDATE employees SET project_names = ARRAY_CONSTRUCT('Materialized Views', 'Lateral Joins')
  WHERE employee_ID = 102;
```

The FLATTEN function can extract values from inside those values. The function takes a single expression of type VARIANT, OBJECT,
or ARRAY, and extracts the values from that expression into a set of rows (0 or more rows, each of which contains 1 or more columns).
This set of rows is equivalent to a view or a table. This view exists only for the duration of the statement in which it is
defined, so it is commonly referred to as an “inline view”.

The following example uses FLATTEN to extract values from an array (*without using a lateral join*):

Copy code

```
SELECT index, value AS project_name
  FROM TABLE(FLATTEN(INPUT => ARRAY_CONSTRUCT('project1', 'project2')));
```

```
+-------+--------------+
| INDEX | PROJECT_NAME |
|-------+--------------|
|     0 | "project1"   |
|     1 | "project2"   |
+-------+--------------+
```

The inline view generated by FLATTEN can be (but is not required to be) used with the LATERAL keyword. For example:

Copy code

```
SELECT * FROM table1, LATERAL FLATTEN(...);
```

When used with the LATERAL keyword, the inline view can contain a reference to columns in a table that precedes it:

Copy code

```
SELECT emp.employee_ID, emp.last_name, index, value AS project_name
  FROM employees AS emp,
    LATERAL FLATTEN(INPUT => emp.project_names) AS proj_names
  ORDER BY employee_ID;
```

```
+-------------+-----------+-------+----------------------+
| EMPLOYEE_ID | LAST_NAME | INDEX | PROJECT_NAME         |
|-------------+-----------+-------+----------------------|
|         101 | Richards  |     0 | "Materialized Views" |
|         101 | Richards  |     1 | "UDFs"               |
|         102 | Paulson   |     0 | "Materialized Views" |
|         102 | Paulson   |     1 | "Lateral Joins"      |
+-------------+-----------+-------+----------------------+
```
