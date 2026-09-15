Categories:
:   [Query syntax](/sql-reference/constructs)

# WHERE

The `WHERE` clause specifies a condition that acts as a filter. You can use the `WHERE` clause to:

- Filter the result of the [FROM](/sql-reference/constructs/from) clause in a [SELECT](/sql-reference/sql/select) statement.
- Specify which rows to operate on in an [UPDATE](/sql-reference/sql/update),
  [MERGE](/sql-reference/sql/merge), or [DELETE](/sql-reference/sql/delete) .

## Syntax

Copy code

```
...
WHERE <predicate>
[ ... ]
```

## Parameters

`predicate`
:   A [Boolean expression](/sql-reference/data-types-logical). The expression can include
    [logical operators](/sql-reference/operators-logical),
    such as `AND`, `OR`, and `NOT`.

## Usage notes

- Predicates in the WHERE clause behave as if they are evaluated after the [FROM](/sql-reference/constructs/from) clause (though the optimizer
  can reorder predicates if it does not impact the results). For example, if a predicate in the WHERE clause
  references columns of a table participating in an outer join in the FROM clause, the filter operates on the rows
  returned from the join (which might be padded with NULLs).
- Use care when creating expressions that might evaluate NULLs.

  - In most contexts, the Boolean expression `NULL = NULL` returns NULL, not TRUE. Consider using
    [IS [ NOT ] NULL](/sql-reference/functions/is-null) to compare NULL values.
  - In a `WHERE` clause, if an expression evaluates to NULL, the row for that expression is removed from the result
    set (that is, it is filtered out).
- The maximum number of expressions in a list is 200,000. For example, the limit applies to the number of expressions
  in the following SELECT statement:

  Copy code

  ```
  SELECT column_x
  FROM mytable
  WHERE column_y IN (<expr1>, <expr2>, <expr3> ...);
  ```

  To avoid reaching the limit, perform a join with a lookup table that contains the expression values, rather than specifying
  the values using the IN clause. For example, when the expression values in the previous example are added to a lookup table
  named `mylookuptable`, you can run the following query successfully even if the lookup table has more than 200,000 rows:

  Copy code

  ```
  SELECT column_x
    FROM mytable t
    JOIN mylookuptable l
    ON t.column_y = l.values_for_comparison;
  ```

## Joins in the WHERE clause

Although the `WHERE` clause is primarily for filtering, the `WHERE` clause can also be used to express many types
of joins. For conceptual information about joins, see [Working with joins](/user-guide/querying-joins).

A `WHERE` clause can specify a join by including join conditions, which are Boolean expressions that define which row(s) from one
side of the JOIN match row(s) from the other side of the join.

The following two equivalent queries show how to express an inner join in either the `WHERE` or [FROM](/sql-reference/constructs/from) clause:

> Copy code
>
> ```
> SELECT t1.c1, t2.c2
>     FROM t1, t2
>     WHERE t1.c1 = t2.c2;
>
> SELECT t1.c1, t2.c2
>     FROM t1 INNER JOIN t2
>         ON t1.c1 = t2.c2;
> ```

Outer joins can be specified by using either the `(+)` syntax in the `WHERE` clause or
the `OUTER JOIN` keywords in the [FROM](/sql-reference/constructs/from) clause.

When you specify an outer join with `(+)`, the WHERE clause applies `(+)` to each join column of the table that is
“inner” (defined below).

Note

The result of an outer join contains a copy of all rows from one table. In this topic, the table whose rows are preserved is
called the “outer” table, and the other table is called the “inner” table.

- In a LEFT OUTER JOIN, the left-hand table is the outer table and the right-hand table is the inner table.
- In a RIGHT OUTER JOIN, the right-hand table is the outer table and the left-hand table is the inner table.

The following queries show equivalent left outer joins, one of which specifies the join in the `FROM` clause and one of which
specifies the join in the `WHERE` clause:

> Copy code
>
> ```
> SELECT t1.c1, t2.c2
> FROM t1 LEFT OUTER JOIN t2
>         ON t1.c1 = t2.c2;
>
> SELECT t1.c1, t2.c2
> FROM t1, t2
> WHERE t1.c1 = t2.c2(+);
> ```

In the second query, the `(+)` is on the right hand side and identifies the inner table.

Sample output for both queries is below:

> Copy code
>
> ```
> +-------+-------+
> | T1.C1 | T2.C2 |
> |-------+-------|
> |     1 |     1 |
> |     2 |  NULL |
> |     3 |     3 |
> |     4 |  NULL |
> +-------+-------+
> ```

If you are joining a table on multiple columns, use the `(+)` notation
on each column in the inner table (`t2` in the example below):

> > Copy code
> >
> > ```
> > SELECT t1.c1, t2.c2
> > FROM t1, t2
> > WHERE t1.c1 = t2.c2 (+)
> >   AND t1.c3 = t2.c4 (+);
> > ```
>
> Note
>
> There are many restrictions on where the `(+)` annotation can appear; [FROM](/sql-reference/constructs/from) clause outer joins are more expressive. Snowflake suggests using the
> `(+)` notation only when porting code that already uses that notation.
> New code should avoid that notation.
>
> The restrictions include:
>
> - You cannot use the `(+)` notation to create `FULL OUTER JOIN`; you
>   can only create `LEFT OUTER JOIN` and `RIGHT OUTER JOIN`.
>   The following is not valid. The statement causes the following error message:
>   `SQL compilation error: Outer join predicates form a cycle between 'T1' and 'T2'.`
>
>   Copy code
>
>   ```
>   -- NOT VALID
>   select t1.c1
>    from t1, t2
>    where t1.c1 (+) = t2.c2 (+);
>   ```
> - If a table participates in more than one join in a query, the `(+)` notation can specify the table as the inner table in only
>   one of those joins. The following is not valid because `t1` serves as the inner table in two joins.
>   The statement causes the following error message:
>   `SQL compilation error: Table 'T1' is outer joined to multiple tables: 'T3' and 'T2'.`
>
>   Copy code
>
>   ```
>   -- NOT VALID
>   select t1.c1
>    from t1, t2, t3
>    where t1.c1 (+) = t2.c2
>      and t1.c1 (+) = t3.c3;
>   ```
>
>   Note, however, that you can use `(+)` to identify different tables as
>   inner tables in different joins in the same SQL statement. The following
>   example joins three tables: `t1`, `t2`, and `t3`, two of which are
>   inner tables (in different joins). This statement performs:
>
>   - A LEFT OUTER JOIN between `t1` and `t2` (where `t2` is the inner table).
>   - A LEFT OUTER JOIN between `t2` and `t3` (where `t3` is the inner table).
>
>   Copy code
>
>   ```
>   select t1.c1
>    from t1, t2, t3
>    where t1.c1 = t2.c2 (+)
>      and t2.c2 = t3.c3 (+);
>   ```

The `(+)` may be immediately adjacent to the table and column name, or it may be separated by whitespace. Both of the following
are valid:

> Copy code
>
> ```
> where t1.c1 = t2.c2(+)
>
> where t1.c1 = t2.c2 (+)
> ```

A query can contain joins specified in both the `FROM ... ON ...` clause and the `WHERE` clause. However, specifying
joins in different clauses of the same query can make that query more difficult to read.

Support for joins in the `WHERE` clause is primarily for backwards compatibility with older queries that do not use
the `FROM ... ON ...` syntax. Snowflake recommends using `FROM ... ON ...` when writing new queries with joins.
For details, see [JOIN](/sql-reference/constructs/join).

## Examples

### Simple examples of filtering

The following show some simple uses of the WHERE clause:

> Copy code
>
> ```
> SELECT * FROM invoices
>   WHERE invoice_date < '2018-01-01';
>
> SELECT * FROM invoices
>   WHERE invoice_date < '2018-01-01'
>     AND paid = FALSE;
> ```

This example uses a subquery and shows all the invoices that have
smaller-than-average billing amounts:

> Copy code
>
> ```
> SELECT * FROM invoices
>     WHERE amount < (
>                    SELECT AVG(amount)
>                        FROM invoices
>                    )
>     ;
> ```

### Performing joins in the WHERE clause

To specify a join in the `WHERE` clause, list the tables to be joined in the `FROM clause`, separating the tables
with a comma. Specify the join condition as a filter in the `WHERE` clause, as shown in the following example:

> Copy code
>
> ```
> SELECT t1.col1, t2.col1
>     FROM t1, t2
>     WHERE t2.col1 = t1.col1
>     ORDER BY 1, 2;
> +------+------+
> | COL1 | COL1 |
> |------+------|
> |    2 |    2 |
> |    2 |    2 |
> |    3 |    3 |
> +------+------+
> ```

Note

The comma operator is older syntax for `INNER JOIN`. The following statement shows the recommended way to
perform a join using newer syntax. The query below is equivalent to the query above:

> Copy code
>
> ```
> SELECT t1.col1, t2.col1
>     FROM t1 JOIN t2
>         ON t2.col1 = t1.col1
>     ORDER BY 1, 2;
> +------+------+
> | COL1 | COL1 |
> |------+------|
> |    2 |    2 |
> |    2 |    2 |
> |    3 |    3 |
> +------+------+
> ```

This next section shows 3-table joins and shows the difference in behavior with 0, 1, or 2 `(+)` outer join
operators.

> Before executing the queries, create and load the tables to use in the joins:
>
> > Copy code
> >
> > ```
> > create table departments (
> >     department_ID INTEGER,
> >     department_name VARCHAR,
> >     location VARCHAR
> >     );
> > insert into departments (department_id, department_name, location) values
> >     (10, 'CUSTOMER SUPPORT', 'CHICAGO'),
> >     (40, 'RESEARCH', 'BOSTON'),
> >     (80, 'Department with no employees yet', 'CHICAGO'),
> >     (90, 'Department with no projects or employees yet', 'EREHWON')
> >     ;
> >
> > create table projects (
> >     project_id integer,
> >     project_name varchar,
> >     department_id integer
> >     );
> > insert into projects (project_id, project_name, department_id) values
> >     (4000, 'Detect fake product reviews', 40),
> >     (4001, 'Detect false insurance claims', 10),
> >     (9000, 'Project with no employees yet', 80),
> >     (9099, 'Project with no department or employees yet', NULL)
> >     ;
> >
> > create table employees (
> >     employee_ID INTEGER,
> >     employee_name VARCHAR,
> >     department_id INTEGER,
> >     project_id INTEGER
> >     );
> > insert into employees (employee_id, employee_name, department_id, project_id)
> >   values
> >     (1012, 'May Aidez', 10, NULL),
> >     (1040, 'Devi Nobel', 40, 4000),
> >     (1041, 'Alfred Mendeleev', 40, 4001)
> >     ;
> > ```
>
> Execute a 3-way inner join. This does not use `(+)` (or the OUTER keyword) and is therefore an inner join. The
> output includes only rows for which there is a department, project, and employee:
>
> > Copy code
> >
> > ```
> > SELECT d.department_name, p.project_name, e.employee_name
> >     FROM  departments d, projects p, employees e
> >     WHERE
> >             p.department_id = d.department_id
> >         AND
> >             e.project_id = p.project_id
> >     ORDER BY d.department_id, p.project_id, e.employee_id;
> > +------------------+-------------------------------+------------------+
> > | DEPARTMENT_NAME  | PROJECT_NAME                  | EMPLOYEE_NAME    |
> > |------------------+-------------------------------+------------------|
> > | CUSTOMER SUPPORT | Detect false insurance claims | Alfred Mendeleev |
> > | RESEARCH         | Detect fake product reviews   | Devi Nobel       |
> > +------------------+-------------------------------+------------------+
> > ```
>
> Perform an outer join. This is similar to the preceding statement except that this uses `(+)` to make the
> second join a right outer join. The effect is that if a department is included in the output, then all of that
> department’s projects are included, even if those projects have no employees:
>
> > Copy code
> >
> > ```
> > SELECT d.department_name, p.project_name, e.employee_name
> >     FROM  departments d, projects p, employees e
> >     WHERE
> >             p.department_id = d.department_id
> >         AND
> >             e.project_id(+) = p.project_id
> >     ORDER BY d.department_id, p.project_id, e.employee_id;
> > +----------------------------------+-------------------------------+------------------+
> > | DEPARTMENT_NAME                  | PROJECT_NAME                  | EMPLOYEE_NAME    |
> > |----------------------------------+-------------------------------+------------------|
> > | CUSTOMER SUPPORT                 | Detect false insurance claims | Alfred Mendeleev |
> > | RESEARCH                         | Detect fake product reviews   | Devi Nobel       |
> > | Department with no employees yet | Project with no employees yet | NULL             |
> > +----------------------------------+-------------------------------+------------------+
> > ```
>
> Perform two outer joins.
> This is the same as the preceding statement except that this uses `(+)` to make both joins into
> outer joins. The effect is that all departments are included (even if they have no projects or employees yet) and
> all projects associated with departments are included (even if they have no employees yet). Note that the output
> excludes projects that have no department.
>
> > Copy code
> >
> > ```
> > SELECT d.department_name, p.project_name, e.employee_name
> >     FROM  departments d, projects p, employees e
> >     WHERE
> >             p.department_id(+) = d.department_id
> >         AND
> >             e.project_id(+) = p.project_id
> >     ORDER BY d.department_id, p.project_id, e.employee_id;
> > +----------------------------------------------+-------------------------------+------------------+
> > | DEPARTMENT_NAME                              | PROJECT_NAME                  | EMPLOYEE_NAME    |
> > |----------------------------------------------+-------------------------------+------------------|
> > | CUSTOMER SUPPORT                             | Detect false insurance claims | Alfred Mendeleev |
> > | RESEARCH                                     | Detect fake product reviews   | Devi Nobel       |
> > | Department with no employees yet             | Project with no employees yet | NULL             |
> > | Department with no projects or employees yet | NULL                          | NULL             |
> > +----------------------------------------------+-------------------------------+------------------+
> > ```

(Remember, however, that Snowflake recommends using the `OUTER` keyword in the `FROM` clause rather than using
the `(+)` operator in the `WHERE` clause.)
