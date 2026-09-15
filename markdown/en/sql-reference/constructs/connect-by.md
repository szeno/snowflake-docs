Categories:
:   [Query syntax](/sql-reference/constructs)

# CONNECT BY

Joins a table to itself to process hierarchical data in the table. The `CONNECT BY` subclause of the
[FROM](/sql-reference/constructs/from) clause iterates to process the data.

For example, you can create a query that shows a “parts explosion” to
recursively list a component and the sub-components of that component.

The Snowflake syntax for CONNECT BY is mostly compatible with the Oracle syntax.

See also:
:   [WITH](/sql-reference/constructs/with)

## Syntax

The general form of a statement with CONNECT BY is similar to the following
(some variations in order are allowed, but are not shown):

Copy code

```
SELECT <column_list> [ , <level_expression> ]
  FROM <data_source>
    START WITH <predicate>
    CONNECT BY [ PRIOR ] <col1_identifier> = [ PRIOR ] <col2_identifier>
           [ , [ PRIOR ] <col3_identifier> = [ PRIOR ] <col4_identifier> ]
           ...
  ...
```

## Parameters

`column_list`
:   This generally follows the rules for the projection clause of a [SELECT](/sql-reference/sql/select) statement.

`level_expression`
:   CONNECT BY queries allow some pseudo-columns.
    One of those pseudo-columns is `LEVEL`, which indicates the current level
    of the hierarchy (where level 1 represents the top of the hierarchy).
    The projection clause of the query can use LEVEL as a column.

`data_source`
:   The data source is usually a table, but can be another table-like data source, such as a view, UDTF, etc.

`predicate`
:   The predicate is an expression that selects the first “level” of the
    hierarchy (e.g. the president of the company or the top-level component in
    a parts explosion). The predicate should look similar to a
    [WHERE](/sql-reference/constructs/where) clause, but without the keyword `WHERE`.

    See the [Examples](#examples) section (in this topic) for predicate examples.

`colN_identifier`
:   The CONNECT BY clause should contain one or more expressions similar to those
    used in joins. Specifically, a column in the “current” level of the table
    should refer to a column in the “prior” (higher) level of the table.

    For example, in a manager/employee hierarchy, the clause might look similar to:

    > Copy code
    >
    > ```
    > ... CONNECT BY manager_ID = PRIOR employee_ID ...
    > ```

    The keyword PRIOR indicates that the value should be taken from the
    prior (higher/parent) level.

    In this example, the current employee’s `manager_ID` should match the prior level’s `employee_ID`.

    The CONNECT BY clause can contain more than one such expression, for example:

    > Copy code
    >
    > ```
    > ... CONNECT BY y = PRIOR x AND b = PRIOR a ...
    > ```

    Each expression similar to the following should have exactly one occurrence of the keyword PRIOR:

    > Copy code
    >
    > ```
    > CONNECT BY <col_1_identifier> = <col_2_identifier>
    > ```
    >
    > The keyword PRIOR may be on either the left-hand or right-hand side of the `=` sign. For example:
    >
    > Copy code
    >
    > ```
    > CONNECT BY <col_1_identifier> = PRIOR <col_2_identifier>
    > ```
    >
    > or
    >
    > Copy code
    >
    > ```
    > CONNECT BY PRIOR <col_1_identifier> = <col_2_identifier>
    > ```

## Usage notes

- A CONNECT BY clause always joins a table to itself, not to another table.
- Some variations within the projection clause are valid. Although the syntax shows `level_expression`
  occurring after the `column_list`, the level expression(s) can occur in any order.
- The keyword `PRIOR` should occur exactly once in each CONNECT BY expression. `PRIOR` can occur on either
  the left-hand side or the right-hand side of the expression, but not on both.
- A query with CONNECT BY may also contain one or both of the following:

  - Filters in a [WHERE](/sql-reference/constructs/where) clause.
  - [JOINs](/sql-reference/constructs/join) (which may be in either a [FROM](/sql-reference/constructs/from) clause or
    a [WHERE](/sql-reference/constructs/where) clause).

  The order of evaluation is:

  1. JOINs (regardless of whether specified in the WHERE clause or the FROM clause).
  2. CONNECT BY
  3. Filters (other than JOIN filters).

  For example, filters in a WHERE clause are processed after the CONNECT BY.
- The Snowflake implementation of CONNECT BY is mostly compatible with the Oracle implementation; however,
  Snowflake does not support:

  - NOCYCLE
  - CONNECT\_BY\_ISCYCLE
  - CONNECT\_BY\_ISLEAF

- Snowflake supports the function `SYS_CONNECT_BY_PATH` when used with the `CONNECT BY` clause.
  `SYS_CONNECT_BY_PATH` returns a string that contains the path from the root to the current element.
  An example is included in the [Examples](#examples) section below.

- Snowflake supports the `CONNECT_BY_ROOT` operator when used with the `CONNECT BY` clause. The `CONNECT_BY_ROOT`
  operator allows the current level to use information from the root level of the hierarchy, even if the root level
  is not the immediate parent of the current level.
  An example is included in the [Examples](#examples) section below.
- The `CONNECT BY` clause can iterate as many times as necessary to process the data. Constructing a query improperly can cause
  an infinite loop. In these cases, the query continues to run until the query succeeds, the query times out (e.g. exceeds the
  number of seconds specified by the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) parameter), or you
  [cancel the query](/user-guide/querying-cancel-statements).

  For information on how infinite loops can occur and for guidelines on how to avoid this problem, see
  [Troubleshooting a Recursive CTE](/user-guide/queries-cte#label-recursive-common-table-expression-troubleshoot).

## Examples

This example uses a CONNECT BY to show the management hierarchy in a table
of employee information. The table and data are shown below:

> > Copy code
> >
> > ```
> > CREATE OR REPLACE TABLE employees (title VARCHAR, employee_ID INTEGER, manager_ID INTEGER);
> > ```
> >
> > Copy code
> >
> > ```
> > INSERT INTO employees (title, employee_ID, manager_ID) VALUES
> >     ('President', 1, NULL),  -- The President has no manager.
> >         ('Vice President Engineering', 10, 1),
> >             ('Programmer', 100, 10),
> >             ('QA Engineer', 101, 10),
> >         ('Vice President HR', 20, 1),
> >             ('Health Insurance Analyst', 200, 20);
> > ```
>
> The query and output are shown below:
>
> > Copy code
> >
> > ```
> > SELECT employee_ID, manager_ID, title
> >   FROM employees
> >     START WITH title = 'President'
> >     CONNECT BY
> >       manager_ID = PRIOR employee_id
> >   ORDER BY employee_ID;
> > +-------------+------------+----------------------------+
> > | EMPLOYEE_ID | MANAGER_ID | TITLE                      |
> > |-------------+------------+----------------------------|
> > |           1 |       NULL | President                  |
> > |          10 |          1 | Vice President Engineering |
> > |          20 |          1 | Vice President HR          |
> > |         100 |         10 | Programmer                 |
> > |         101 |         10 | QA Engineer                |
> > |         200 |         20 | Health Insurance Analyst   |
> > +-------------+------------+----------------------------+
> > ```

This example uses the `SYS_CONNECT_BY_PATH` function to show the hierarchy from the President down to the
current employee:

> Copy code
>
> ```
> SELECT SYS_CONNECT_BY_PATH(title, ' -> '), employee_ID, manager_ID, title
>   FROM employees
>     START WITH title = 'President'
>     CONNECT BY
>       manager_ID = PRIOR employee_id
>   ORDER BY employee_ID;
> +----------------------------------------------------------------+-------------+------------+----------------------------+
> | SYS_CONNECT_BY_PATH(TITLE, ' -> ')                             | EMPLOYEE_ID | MANAGER_ID | TITLE                      |
> |----------------------------------------------------------------+-------------+------------+----------------------------|
> |  -> President                                                  |           1 |       NULL | President                  |
> |  -> President -> Vice President Engineering                    |          10 |          1 | Vice President Engineering |
> |  -> President -> Vice President HR                             |          20 |          1 | Vice President HR          |
> |  -> President -> Vice President Engineering -> Programmer      |         100 |         10 | Programmer                 |
> |  -> President -> Vice President Engineering -> QA Engineer     |         101 |         10 | QA Engineer                |
> |  -> President -> Vice President HR -> Health Insurance Analyst |         200 |         20 | Health Insurance Analyst   |
> +----------------------------------------------------------------+-------------+------------+----------------------------+
> ```

This example uses the `CONNECT_BY_ROOT` keyword to display information from the top of the hierarchy in each row
of output:

> Copy code
>
> ```
> SELECT
> employee_ID, manager_ID, title,
> CONNECT_BY_ROOT title AS root_title
>   FROM employees
>     START WITH title = 'President'
>     CONNECT BY
>       manager_ID = PRIOR employee_id
>   ORDER BY employee_ID;
> +-------------+------------+----------------------------+------------+
> | EMPLOYEE_ID | MANAGER_ID | TITLE                      | ROOT_TITLE |
> |-------------+------------+----------------------------+------------|
> |           1 |       NULL | President                  | President  |
> |          10 |          1 | Vice President Engineering | President  |
> |          20 |          1 | Vice President HR          | President  |
> |         100 |         10 | Programmer                 | President  |
> |         101 |         10 | QA Engineer                | President  |
> |         200 |         20 | Health Insurance Analyst   | President  |
> +-------------+------------+----------------------------+------------+
> ```

This example uses a CONNECT BY to show a “parts explosion”:

> Here is the data:
>
> > Copy code
> >
> > ```
> > -- The components of a car.
> > CREATE TABLE components (
> >     description VARCHAR,
> >     quantity INTEGER,
> >     component_ID INTEGER,
> >     parent_component_ID INTEGER
> >     );
> >
> > INSERT INTO components (description, quantity, component_ID, parent_component_ID) VALUES
> >     ('car', 1, 1, 0),
> >        ('wheel', 4, 11, 1),
> >           ('tire', 1, 111, 11),
> >           ('#112 bolt', 5, 112, 11),
> >           ('brake', 1, 113, 11),
> >              ('brake pad', 1, 1131, 113),
> >        ('engine', 1, 12, 1),
> >           ('piston', 4, 121, 12),
> >           ('cylinder block', 1, 122, 12),
> >           ('#112 bolt', 16, 112, 12)   -- Can use same type of bolt in multiple places
> >     ;
> > ```
>
> Here are the query and output:
>
> > Copy code
> >
> > ```
> > SELECT
> >   description,
> >   quantity,
> >   component_id,
> >   parent_component_ID,
> >   SYS_CONNECT_BY_PATH(component_ID, ' -> ') AS path
> >   FROM components
> >     START WITH component_ID = 1
> >     CONNECT BY
> >       parent_component_ID = PRIOR component_ID
> >   ORDER BY path
> >   ;
> > +----------------+----------+--------------+---------------------+----------------------------+
> > | DESCRIPTION    | QUANTITY | COMPONENT_ID | PARENT_COMPONENT_ID | PATH                       |
> > |----------------+----------+--------------+---------------------+----------------------------|
> > | car            |        1 |            1 |                   0 |  -> 1                      |
> > | wheel          |        4 |           11 |                   1 |  -> 1 -> 11                |
> > | tire           |        1 |          111 |                  11 |  -> 1 -> 11 -> 111         |
> > | #112 bolt      |        5 |          112 |                  11 |  -> 1 -> 11 -> 112         |
> > | brake          |        1 |          113 |                  11 |  -> 1 -> 11 -> 113         |
> > | brake pad      |        1 |         1131 |                 113 |  -> 1 -> 11 -> 113 -> 1131 |
> > | engine         |        1 |           12 |                   1 |  -> 1 -> 12                |
> > | #112 bolt      |       16 |          112 |                  12 |  -> 1 -> 12 -> 112         |
> > | piston         |        4 |          121 |                  12 |  -> 1 -> 12 -> 121         |
> > | cylinder block |        1 |          122 |                  12 |  -> 1 -> 12 -> 122         |
> > +----------------+----------+--------------+---------------------+----------------------------+
> > ```
