# Querying Hierarchical Data

This topic describes how to store and query hierarchical data using:

- JOINs
- Recursive CTEs (common table expressions)
- CONNECT BY

See also:
:   [CONNECT BY](/sql-reference/constructs/connect-by) , [the recursive CTE portion of the WITH command](/sql-reference/constructs/with) , [Working with CTEs (Common Table Expressions)](/user-guide/queries-cte) , [Tabular SQL UDFs (UDTFs)](/developer-guide/udf/sql/udf-sql-tabular-functions)

## Storing Hierarchical Data

Many types of data are best represented as a hierarchy, such as a tree.

For example, employees are usually organized in a hierarchy, with a company President at the top of the hierarchy.

Another example of a hierarchy is a “parts explosion”. For example, a car contains an engine; an engine contains a
fuel pump; and a fuel pump contains a hose.

You can store hierarchical data in:

- A hierarchy of tables.
- A single table with one (or more) columns representing the hierarchy (e.g. indicating each employee’s direct manager).

Both techniques are described below.

Note

This topic focuses on hierarchical data stored as *structured* data. Hierarchical data can also be stored as semi-structured
data (e.g. JSON data can be stored in ARRAY, OBJECT, or VARIANT data types). For information about semi-structured data, see:

> - [Introduction to loading semi-structured data](/user-guide/semistructured-intro)
> - [Querying Semi-structured Data](/user-guide/querying-semistructured)

### Hierarchical Data Across Multiple Tables

Relational databases often store hierarchical data by using different tables. For example, one table might
contain “parent” data and another table might contain “child” data. When the entire hierarchy is known in advance,
one table can be created for each layer in the hierarchy.

For example, consider a Human Resources database that stores employee information and manager information. If the
company is small, then there might be only two levels, for example, one manager and two employees.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE managers  (title VARCHAR, employee_ID INTEGER);
> ```
>
> Copy code
>
> ```
> CREATE OR REPLACE TABLE employees (title VARCHAR, employee_ID INTEGER, manager_ID INTEGER);
> ```
>
> Copy code
>
> ```
> INSERT INTO managers (title, employee_ID) VALUES
>     ('President', 1);
> INSERT INTO employees (title, employee_ID, manager_ID) VALUES
>     ('Vice President Engineering', 10, 1),
>     ('Vice President HR', 20, 1);
> ```

### Hierarchical Data in a Single Table

In some situations, the number of levels in the hierarchy might change.

For example, a company that started with a two-level hierarchy (President and other employees) might increase the
number of levels as the company grows. The company might expand to include a President, Vice Presidents, and regular
employees.

If the number of levels is unknown, so that it is not possible to create a hierarchy with a known number of tables,
then in some cases the hierarchical data can be stored in one table. For example, a single table can contain all
employees, and can include a column that stores each employee’s manager\_ID, which points to another employee in that
same table. For example:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE employees (title VARCHAR, employee_ID INTEGER, manager_ID INTEGER);
> ```
>
> Copy code
>
> ```
> INSERT INTO employees (title, employee_ID, manager_ID) VALUES
>     ('President', 1, NULL),  -- The President has no manager.
>         ('Vice President Engineering', 10, 1),
>             ('Programmer', 100, 10),
>             ('QA Engineer', 101, 10),
>         ('Vice President HR', 20, 1),
>             ('Health Insurance Analyst', 200, 20);
> ```

Storing an entire hierarchy of data in one table works best if all levels
of the hierarchy store the same data – in our example, employee ID, title, etc.
If the data at different levels doesn’t fit the same record structure, then
storing all the data in one table might not be practical.

## Using Joins to Query Hierarchical Data

In a two-level hierarchy (for example, managers and employees), the data can be queried with a two-way join:

> Copy code
>
> ```
> SELECT 
>         employees.title, 
>         employees.employee_ID, 
>         managers.employee_ID AS MANAGER_ID, 
>         managers.title AS "MANAGER TITLE"
>     FROM employees, managers
>     WHERE employees.manager_ID = managers.employee_ID
>     ORDER BY employees.title;
> +----------------------------+-------------+------------+---------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MANAGER TITLE |
> |----------------------------+-------------+------------+---------------|
> | Vice President Engineering |          10 |          1 | President     |
> | Vice President HR          |          20 |          1 | President     |
> +----------------------------+-------------+------------+---------------+
> ```

In a three-level hierarchy, you can use a 3-way join:

> Copy code
>
> ```
> SELECT
>      emps.title,
>      emps.employee_ID,
>      mgrs.employee_ID AS MANAGER_ID, 
>      mgrs.title AS "MANAGER TITLE"
>   FROM employees AS emps LEFT OUTER JOIN employees AS mgrs
>     ON emps.manager_ID = mgrs.employee_ID
>   ORDER BY mgrs.employee_ID NULLS FIRST, emps.employee_ID;
> +----------------------------+-------------+------------+----------------------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MANAGER TITLE              |
> |----------------------------+-------------+------------+----------------------------|
> | President                  |           1 |       NULL | NULL                       |
> | Vice President Engineering |          10 |          1 | President                  |
> | Vice President HR          |          20 |          1 | President                  |
> | Programmer                 |         100 |         10 | Vice President Engineering |
> | QA Engineer                |         101 |         10 | Vice President Engineering |
> | Health Insurance Analyst   |         200 |         20 | Vice President HR          |
> +----------------------------+-------------+------------+----------------------------+
> ```

This concept can be extended to as many levels as needed, as long as you know how many levels are needed. But if
the number of levels changes, the queries need to change.

## Using CONNECT BY or Recursive CTEs to Query Hierarchical Data

Snowflake provides two ways to query hierarchical data in which the number of levels is not known in advance:

- Recursive CTEs (common table expressions).
- `CONNECT BY` clauses.

A recursive CTE allows you to create a [WITH](/sql-reference/constructs/with) clause that can refer to itself. This lets
you iterate through each level of your hierarchy and accumulate results.

A `CONNECT BY` clause allows you to create a type of `JOIN` operation that processes the hierarchy one level
at a time, and allows each level to refer to data in the prior level.

For more details, see:

- [WITH](/sql-reference/constructs/with) and [Working with CTEs (Common Table Expressions)](/user-guide/queries-cte).
- [CONNECT BY](/sql-reference/constructs/connect-by).

## Differences between Self-Join, Recursive CTE, and CONNECT BY

`CONNECT BY` allows only self-joins. Recursive CTEs are more flexible and allow a table to be joined to one
or more other tables.

A `CONNECT BY` clause has most of the power of a recursive CTE. However,
a recursive CTE can do some things that a `CONNECT BY` cannot.

For example, if you look at the recursive CTE examples, you see that one
of the queries indents the output and also sorts the output so that each
“child” appears underneath the corresponding “parent”. The sorting is done
by creating a sort key that contains the chain of IDs from the top all the
way down to the current level. In the manager/employee example, the chain
contains the President’s ID, followed by the Vice President’s ID, etc.
This sort key groups rows in a way that looks similar to a sideways tree.
The `CONNECT BY` syntax doesn’t support this because the
“START WITH” clause does not allow the code to specify additional columns
(beyond those in the table itself), such as the sort\_key. Contrast the two
code snippets below:

Copy code

```
SELECT indent(LEVEL) || employee_ID, manager_ID, title
  FROM employees
    -- This sub-clause specifies the record at the top of the hierarchy,
    -- but does not allow additional derived fields, such as the sort key.
    START WITH TITLE = 'President'
    CONNECT BY ...

WITH RECURSIVE current_layer
   (employee_ID, manager_ID, sort_key) AS (
     -- This allows us to add columns, such as sort_key, that are not part
     -- of the employees table.
     SELECT employee_ID, manager_ID, employee_ID AS sort_key
     ...
     )
```

You can, however, use the `SYS_CONNECT_BY_PATH` function to achieve a similar effect with the
`CONNECT BY` clause.

Although the `CONNECT BY` clause version is limited because the START WITH
clause cannot add columns to those already in the row (even derived columns
based on values already in the row), it also has some advantages:

- You have access to all columns of each row without specifying those columns
  in a column list. In a recursive CTE, the recursive clause
  does not have access to columns that are not explicitly specified in the CTE.
- In a recursive CTE, you must specify the columns in the
  CTE, and the projection lists of the selects in the anchor clause and the
  recursive clause, must both match the columns in the CTE. If the order of
  the columns in the various projection clauses does not match, you can
  cause problems such as infinite loops.
- The `CONNECT BY` syntax supports convenient pseudo-columns such as `LEVEL`,
  `CONNECT_BY_ROOT`, and `CONNECT_BY_PATH`

A minor difference between `CONNECT BY` and recursive CTE is that in `CONNECT BY`
you use the keyword `PRIOR` to indicate which column values should be taken
from the previous iteration, whereas in a recursive CTE you use the table
name and the CTE name to indicate which values are taken from the current
iteration and which are taken from the previous iteration. (In a recursive CTE,
you can also distinguish between current and previous iterations by using
different column names in the CTE column list than in the source table or table
expression.)

## Non-Contiguous Hierarchies

This topic described hierarchies and how parent-child relationships
can be used by recursive CTEs (common table expressions) and `CONNECT BY`
clauses. In all of this topic’s examples, as well as all the examples in the
`CONNECT BY` documentation and the recursive CTE documentation, the hierarchies are
contiguous. None of the examples has a parent and a grandchild without having a corresponding child between them.

For example, if you do a “parts explosion” of a car, you’re not going to have
a component for the car, and a component for the tire, without having a
component for the wheel that contains the tire (and that is contained by the
car).

However, there can be cases where data is incomplete. For example, in an
employee/manager hierarchy, suppose that the Vice President of Engineering
retires and the company doesn’t hire a replacement immediately. If the
VP’s employee record is deleted, then employees below that VP are “cut off”
from the rest of the hierarchy, so the employees table no longer contains a single contiguous hierarchy.

If you use recursive CTEs or `CONNECT BY` to process data, you need to think about whether the data in your table
represents a single, contiguous tree. You can use recursive CTEs and `CONNECT BY` on
a single table that contains multiple trees, but you can only
query one tree at a time, and that tree must be contiguous.
