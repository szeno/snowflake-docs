# Working with Subqueries

A subquery is a query within another query. Subqueries in a [FROM](/sql-reference/constructs/from) or [WHERE](/sql-reference/constructs/where)
clause are used to provide data that will be used to limit or compare/evaluate the data returned by the containing query.

## Types of Subqueries

### Correlated vs. Uncorrelated Subqueries

Subqueries can be categorized as *correlated* or *uncorrelated*:

- A correlated subquery refers to one or more columns from outside of
  the subquery. (The columns are typically referenced inside the `WHERE`
  clause of the subquery.) A correlated subquery can be thought of as a filter
  on the table that it refers to, as if the subquery were evaluated on each
  row of the table in the outer query.
- An uncorrelated subquery has no such external column references. It
  is an independent query, the results of which are returned to and used by
  the outer query once (not per row).

For example:

> Copy code
>
> ```
> -- Uncorrelated subquery:
> SELECT c1, c2
>   FROM table1 WHERE c1 = (SELECT MAX(x) FROM table2);
>
> -- Correlated subquery:
> SELECT c1, c2
>   FROM table1 WHERE c1 = (SELECT x FROM table2 WHERE y = table1.c2);
> ```

### Scalar vs. Non-scalar Subqueries

Subqueries can also be categorized as *scalar* or *non-scalar*:

- A scalar subquery returns a single value (one column of one row).
  If no rows qualify to be returned, the subquery returns NULL.
- A non-scalar subquery returns 0, 1, or multiple rows, each of which
  may contain 1 or multiple columns. For each column, if there is no value to
  return, the subquery returns NULL. If no rows qualify to be returned, the
  subquery returns 0 rows (not NULLs).

### Types Supported by Snowflake

Snowflake currently supports the following types of subqueries:

- Uncorrelated scalar subqueries in any place that a value expression can be used.
- Correlated scalar subqueries in [WHERE](/sql-reference/constructs/where) clauses.
- EXISTS, ANY / ALL, and IN subqueries in [WHERE](/sql-reference/constructs/where) clauses. These subqueries can be correlated or uncorrelated.

## Subquery Operators

[Subquery operators](/sql-reference/operators-subquery) operate on nested query expressions. They can be used to compute values that are:

- Returned in a [SELECT](/sql-reference/sql/select) list.
- Grouped in a [GROUP BY](/sql-reference/constructs/group-by) clause.
- Compared with other expressions in the [WHERE](/sql-reference/constructs/where) or [HAVING](/sql-reference/constructs/having) clause.

## Differences Between Correlated and Non-Correlated Subqueries

The following query demonstrates an uncorrelated subquery in a [WHERE](/sql-reference/constructs/where) clause.
The subquery gets the per capita GDP of Brazil, and the outer query
selects all the jobs (in any country) that pay less than the
per-capita GDP of Brazil. The subquery is uncorrelated because the value
that it returns does not depend upon any column of the outer query. The
subquery only needs to be called once during the entire execution of the
outer query.

> Copy code
>
> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p
>   WHERE p.annual_wage < (SELECT per_capita_GDP
>                            FROM international_GDP
>                            WHERE name = 'Brazil');
> ```

The next query demonstrates a correlated subquery in a [WHERE](/sql-reference/constructs/where) clause.
The query lists jobs where the annual pay of the job is less than the
per-capita GDP in that country.
This subquery is correlated because it is called once for each row in the
outer query and is passed a value, `p.country` (country name), from the row.

> Copy code
>
> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p
>   WHERE p.annual_wage < (SELECT MAX(per_capita_GDP)
>                            FROM international_GDP i
>                            WHERE p.country = i.name);
> ```

Note

The [MAX](/sql-reference/functions/max) aggregate function is not logically necessary in this case because the
`international_GDP` table has only one row per country; however, because the server doesn’t know that, and because the server
requires that the subquery return no more than one row, the query uses the aggregate function to force the server to recognize that the
subquery will return only one row each time that the subquery is executed.

The functions [MIN](/sql-reference/functions/min) and [AVG](/sql-reference/functions/avg) also work because
applying either of these to a single value returns that value unchanged.

## Scalar Subqueries

A scalar subquery is a subquery that returns at most one row. A scalar subquery can appear anywhere that a value expression can appear, including
the [SELECT](/sql-reference/sql/select) list, [GROUP BY](/sql-reference/constructs/group-by) clause, or as an argument to a function in a
[WHERE](/sql-reference/constructs/where) or [HAVING](/sql-reference/constructs/having) clause.

### Usage Notes

- A scalar subquery can contain only one item in the [SELECT](/sql-reference/sql/select) list.
- If a scalar subquery returns more than one row, a runtime error is generated.
- Correlated scalar subqueries are currently supported only if they can be statically determined to return one row (e.g. if the
  [SELECT](/sql-reference/sql/select) list contains an aggregate function with no [GROUP BY](/sql-reference/constructs/group-by)).
- Uncorrelated scalar subqueries are supported anywhere that a value expression is allowed.
- Subqueries with a correlation inside of [FLATTEN](/sql-reference/functions/flatten) are currently unsupported.
- The [LIMIT / FETCH](/sql-reference/constructs/limit) clause is allowed only in uncorrelated scalar subqueries.

### Examples

This example shows a basic uncorrelated subquery in a WHERE clause:

> Copy code
>
> ```
> SELECT employee_id
> FROM employees
> WHERE salary = (SELECT max(salary) FROM employees);
> ```

This example shows an uncorrelated subquery in a FROM clause; this basic subquery
returns a subset of the information in the `international_GDP` table.
The overall query lists jobs in “high-wage” countries where the annual pay
of the job is the same as the per\_capita\_GDP in that country.

> Copy code
>
> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p INNER JOIN (SELECT name, per_capita_GDP
>                               FROM international_GDP
>                               WHERE per_capita_GDP >= 10000.0) AS pcg
>     ON pcg.per_capita_GDP = p.annual_wage AND p.country = pcg.name;
> ```

## Limitations

Although subqueries can contain a wide range of SELECT statements, they have the following limitations:

- Some clauses are not allowed inside of ANY/ALL/NOT EXISTS subqueries.
- The only type of subquery that allows a
  [LIMIT / FETCH](/sql-reference/constructs/limit) clause is an uncorrelated scalar
  subquery. Also, because an uncorrelated scalar subquery returns only 1 row,
  the LIMIT clause has little or no practical value inside a subquery.
