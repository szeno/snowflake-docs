Categories:
:   [Query syntax](/sql-reference/constructs)

# LATERAL

In a [FROM](/sql-reference/constructs/from) clause, the LATERAL keyword allows an inline view to reference columns
from a table expression that precedes that inline view.

A lateral join behaves more like a correlated subquery than a typical join. A lateral join
behaves as if the server executed a loop similar to the following:

Copy code

```
for each row in left_hand_table LHT:
    execute right_hand_subquery RHS using the values from the current row in the LHT
```

Unlike the output of a non-lateral join, the output from a lateral join includes only the rows
generated from the inline view. There is no need for an explicit ON clause to join rows from the left-hand
side to the right-hand side; the relationship is already established because the inline view
references columns from the left-hand table expression.

See also: [Using lateral joins](/user-guide/lateral-join-using).

## When to use LATERAL

LATERAL is a valuable tool for the following use cases:

- **Chaining table functions on nested data**: When you need to flatten arrays within arrays or
  navigate multiple levels of nested JSON, each subsequent table function call must reference
  the output of the previous one. Lateral joins make this possible.
- **Calling table functions with row-specific arguments**: When a table function (such as a UDTF)
  needs to receive different input values for each row from the left-hand table.

For simple cases such as flattening a single-level array, using `TABLE(FLATTEN(...))` without
a lateral join produces the same result. Lateral joins are necessary only when the inline view must reference
columns that are only available from a preceding expression in the FROM clause.

## Syntax

Copy code

```
SELECT ...
  FROM <left_hand_table_expression>, LATERAL ( <inline_view> )
...
```

## Parameters

`left_hand_table_expression`
:   This is a source of rows, such as:

    > - A table.
    > - A view.
    > - A subquery.
    > - A table function.
    > - The result of an earlier join.

`inline_view`
:   The `inline_view` can be:

    > - An inline view: a view defined within the statement, and valid only for the duration of the statement.
    > - A subquery.
    > - A table function: either a built-in table function such as FLATTEN or a user-defined table function (UDTF).

    The `inline_view` can’t be a plain table reference. It must be an expression that
    can process or filter rows based on values from the left-hand table expression, such as a
    subquery with a WHERE clause or a table function call.

## Usage notes

- The inline view after the keyword LATERAL can reference columns only from the inline view itself and from
  tables to the left of the inline view in the [FROM](/sql-reference/constructs/from) clause.

  Copy code

  ```
  SELECT *
    FROM table_reference_me, LATERAL (...), table_do_not_reference_me ...
  ```
- Although the inline view typically references one or more columns from the `left_hand_table_expression`, it
  is not required to do so.
- Just as INNER JOIN syntax can use either the comma or the keywords INNER JOIN,
  a lateral join can also use the comma or the keywords INNER JOIN. For example:

  Copy code

  ```
  FROM departments AS d INNER JOIN LATERAL (...)
  ```
- You can’t specify the ON, USING, or NATURAL JOIN clause in:

  - A lateral table function (other than a SQL UDTF)
  - An outer lateral join to a table function (other than a SQL UDTF)

  For details, see [the usage notes in the JOIN topic](/sql-reference/constructs/join#label-join-usage-notes).
- The `left_hand_table_expression` can’t be an UNPIVOT result set. Attempting to
  reference an UNPIVOT alias in a LATERAL join causes an error. As a workaround, materialize
  the UNPIVOT result into a temporary table first, then use that table as the left-hand expression.
  For more information, see [UNPIVOT](/sql-reference/constructs/unpivot).

## Examples

See also [Example: Using a lateral join with the FLATTEN table function](/user-guide/lateral-join-using#label-lateral-flatten-example) and [Using FLATTEN to Filter the Results in a WHERE Clause](/user-guide/querying-semistructured#label-using-flatten-where-clause).

The following example uses these tables:

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

The following query is a lateral join with a subquery:

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

The following SQL statement is equivalent and produces the same output. It uses the keywords
INNER JOIN instead of the comma in the FROM clause.

Copy code

```
SELECT *
  FROM departments AS d INNER JOIN
    LATERAL (SELECT * FROM employees AS e WHERE e.department_ID = d.department_ID) AS iv2
  ORDER BY employee_ID;
```

### Chaining LATERAL FLATTEN for nested data

LATERAL is required when you need to chain multiple [FLATTEN](/sql-reference/functions/flatten)
calls to access nested data structures. In the following example, the second FLATTEN must reference
the output of the first FLATTEN, which is only possible with LATERAL.

Copy code

```
CREATE OR REPLACE TABLE persons AS
  SELECT column1 AS id, PARSE_JSON(column2) AS c
    FROM VALUES
      (12712555,
       '{ "name": { "first": "John", "last": "Smith" },
          "contact": [{ "business": [
            { "type": "phone", "content": "555-1234" },
            { "type": "email", "content": "j.smith@example.com" }
          ]}]}'),
      (98127771,
       '{ "name": { "first": "Jane", "last": "Doe" },
          "contact": [{ "business": [
            { "type": "phone", "content": "555-1236" },
            { "type": "email", "content": "j.doe@example.com" }
          ]}]}');
```

The following query uses two LATERAL FLATTEN calls. The first call flattens the `contact` array, and
the second flattens the `business` array within each contact. The second FLATTEN call references
`f.value`, which comes from the output of the first FLATTEN call.

Copy code

```
SELECT id,
    f1.value:type::STRING AS contact_type,
    f1.value:content::STRING AS contact_details
  FROM persons p,
    LATERAL FLATTEN(INPUT => p.c, PATH => 'contact') f,
    LATERAL FLATTEN(INPUT => f.value:business) f1;
```

```
+----------+--------------+---------------------+
|       ID | CONTACT_TYPE | CONTACT_DETAILS     |
|----------+--------------+---------------------|
| 12712555 | phone        | 555-1234            |
| 12712555 | email        | j.smith@example.com |
| 98127771 | phone        | 555-1236            |
| 98127771 | email        | j.doe@example.com   |
+----------+--------------+---------------------+
```

This query can’t be written without LATERAL because the second FLATTEN call depends on the output
of the first FLATTEN call.

## LATERAL versus other approaches

The following table summarizes when to use LATERAL compared to other approaches:

| Use case | Recommendation |
| --- | --- |
| Flatten a single-level array | `TABLE(FLATTEN(...))` without LATERAL works the same. LATERAL is optional. |
| Flatten nested arrays (arrays within arrays) | LATERAL is required to chain FLATTEN calls. |
| Filter rows from another table based on the current row | Either a correlated subquery in the SELECT list or LATERAL works. LATERAL can return multiple rows and columns; a correlated subquery in SELECT can’t do this. |
| Call a table function with row-specific input | LATERAL allows the table function to receive different arguments for each row. |

Expand

Show lessSee more
