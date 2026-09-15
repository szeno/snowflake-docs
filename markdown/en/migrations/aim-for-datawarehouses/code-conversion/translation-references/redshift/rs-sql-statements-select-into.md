# Redshift - SELECT INTO

## Description

> Returns rows from tables, views, and user-defined functions and inserts them into a new table. ([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

## Grammar Syntax

Copy code

```
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number ] [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...]
INTO [ TEMPORARY | TEMP ] [ TABLE ] new_table
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ GROUP BY expression [, ...] ]
[ HAVING condition [, ...] ]
[ { UNION | INTERSECT | { EXCEPT | MINUS } } [ ALL ] query ]
[ ORDER BY expression
[ ASC | DESC ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

For more information please refer to each of the following links:

1. [WITH clause](rs-sql-statements-select#with-clause)
2. [SELECT list](rs-sql-statements-select#select-list)
3. [FROM clause](rs-sql-statements-select#from-clause)
4. [WHERE clause](rs-sql-statements-select#where-clause)
5. [CONNECT BY clause](rs-sql-statements-select#connect-by-clause)
6. [GROUP BY clause](rs-sql-statements-select#group-by-clause)
7. [HAVING clause](rs-sql-statements-select#having-clause)
8. [QUALIFY clause](rs-sql-statements-select#qualify-clause)
9. [UNION, INTERSECT, and EXCEPT](rs-sql-statements-select#union-intersect-and-except)
10. [ORDER BY clause](rs-sql-statements-select#order-by-clause)
11. [LIMIT and OFFSET clauses](#limit-and-offset-clauses)
12. [Local Variables and Parameters](#local-variables-and-parameters)

## FROM clause

### Description

> The `FROM` clause in a query lists the table references (tables, views, and subqueries) that data is selected from. If multiple table references are listed, the tables must be joined, using appropriate syntax in either the `FROM` clause or the `WHERE` clause. If no join criteria are specified, the system processes the query as a cross-join. ([Redshift SQL Language Reference FROM Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html))

Warning

The [FROM clause](https://docs.snowflake.com/en/sql-reference/constructs/from) is partially supported in Snowflake. [Object unpivoting](https://docs.aws.amazon.com/redshift/latest/dg/query-super.html#unpivoting) is not currently supported.

### Grammar Syntax

Copy code

```
 FROM table_reference [, ...]

<table_reference> ::=
with_subquery_table_name [ table_alias ]
table_name [ * ] [ table_alias ]
( subquery ) [ table_alias ]
table_reference [ NATURAL ] join_type table_reference
   [ ON join_condition | USING ( join_column [, ...] ) ]
table_reference PIVOT (
   aggregate(expr) [ [ AS ] aggregate_alias ]
   FOR column_name IN ( expression [ AS ] in_alias [, ...] )
) [ table_alias ]
table_reference UNPIVOT [ INCLUDE NULLS | EXCLUDE NULLS ] (
   value_column_name
   FOR name_column_name IN ( column_reference [ [ AS ]
   in_alias ] [, ...] )
) [ table_alias ]
UNPIVOT expression AS value_alias [ AT attribute_alias ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE department (
    id INT,
    name VARCHAR(50),
    manager_id INT
);

INSERT INTO department(id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

SELECT e.name AS employee_name, d.name AS department_name
INTO employees_in_department
FROM employee e
INNER JOIN department d ON e.manager_id = d.manager_id;
```

##### Results

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Sofía | Engineering |

Expand

Show lessSee more

##### Output Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE department (
    id INT,
    name VARCHAR(50),
    manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO department (id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

CREATE TABLE IF NOT EXISTS employees_in_department AS
  SELECT e.name AS employee_name, d.name AS department_name
  FROM
    employee e
  INNER JOIN
      department d ON e.manager_id = d.manager_id;
```

##### Results

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Sofía | Engineering |

### Known Issues

There are no known issues.

### Related EWIs.

See [SELECT](rs-sql-statements-select#select) transformation for related EWIs.

## GROUP BY clause

### Description

> The `GROUP BY` clause identifies the grouping columns for the query. Grouping columns must be declared when the query computes aggregates with standard functions such as `SUM`, `AVG`, and `COUNT`. ([Redshift SQL Language Reference GROUP BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_GROUP_BY_clause.html))

Note

:class: tip
The [GROUP BY clause](https://docs.snowflake.com/en/sql-reference/constructs/group-by) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 GROUP BY expression [, ...]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT
    manager_id,
    COUNT(id) AS total_employees
INTO manager_employees
FROM employee
GROUP BY manager_id
ORDER BY manager_id;
```

##### Results

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
|  | 1 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE IF NOT EXISTS manager_employees AS
  SELECT
      manager_id,
      COUNT(id) AS total_employees
  FROM
      employee
  GROUP BY manager_id
  ORDER BY manager_id;
```

##### Results

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
|  | 1 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## HAVING clause

### Description

> The `HAVING` clause applies a condition to the intermediate grouped result set that a query returns. ([Redshift SQL Language Reference HAVING Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_HAVING_clause.html))

Note

:class: tip
The [HAVING clause](https://docs.snowflake.com/en/sql-reference/constructs/having) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 [ HAVING condition ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT manager_id, COUNT(id) AS total_employees
INTO manager_employees
FROM
employee
GROUP BY manager_id
HAVING COUNT(id) > 2
ORDER BY manager_id;
```

##### Results

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE IF NOT EXISTS manager_employees AS
  SELECT manager_id, COUNT(id) AS total_employees
  FROM
    employee
  GROUP BY manager_id
  HAVING COUNT(id) > 2
  ORDER BY manager_id;
```

##### Results

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## LIMIT and OFFSET clauses

### Description

> The LIMIT and OFFSET clauses retrieves and skips the number of rows specified in the number.

Note

:class: tip
The [LIMIT and OFFSET](https://docs.snowflake.com/en/sql-reference/constructs/limit) clauses are fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 [ LIMIT { number | ALL } ]
[ OFFSET start ]
```

### Sample Source Patterns

#### LIMIT number

##### Input Code:

##### Redshift

Copy code

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
LIMIT 5;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT 5;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |

Expand

Show lessSee more

#### LIMIT ALL

##### Input Code:

##### Redshift

Copy code

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
LIMIT ALL;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT NULL;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

#### OFFSET without LIMIT

Snowflake doesn’t support OFFSET without LIMIT. The LIMIT is added after transformation with NULL, which is the default LIMIT.

##### Input Code:

##### Redshift

Copy code

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
OFFSET 5;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT NULL
OFFSET 5;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## Local Variables and Parameters

### Description

> Redshift also allows SELECT INTO variables when the statement is executed inside stored procedures.

Note

:class: tip
This pattern is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 SELECT [ select_expressions ] INTO target [ select_expressions ] FROM ...;
```

### Sample Source Patterns

#### SELECT INTO with expressions at the left

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE test_sp1(out param1 int)
AS $$
DECLARE
    var1 int;
BEGIN
     select 10, 100 into param1, var1;
END;
$$ LANGUAGE plpgsql;
```

##### Results

| param1 |
| --- |
| 10 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE test_sp1 (param1 OUT int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            var1 int;
BEGIN
     select 10, 100 into
                : param1,
                : var1;
END;
$$;
```

##### Results

| TEST\_SP1 |
| --- |
| { “param1”: 10 } |

Expand

Show lessSee more

#### SELECT INTO with expressions at the right

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE test_sp1(out param1 int)
AS $$
DECLARE
    var1 int;
BEGIN
     select into param1, var1 10, 100;
END;
$$ LANGUAGE plpgsql;
```

##### Results

| param1 |
| --- |
| 10 |

Expand

Show lessSee more

##### Output Code:

Since Snowflake doesn’t support this grammar for SELECT INTO, the expressions are moved to the left of the INTO.

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE test_sp1 (param1 OUT int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            var1 int;
BEGIN
     select
                10, 100
            into
                : param1,
                : var1;
END;
$$;
```

##### Results

| TEST\_SP1 |
| --- |
| { “param1”: 10 } |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## ORDER BY clause

### Description

> The `ORDER BY` clause sorts the result set of a query. ([Redshift SQL Language Reference Order By Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html))

Note

:class: tip
The [ORDER BY clause](https://docs.snowflake.com/en/sql-reference/constructs/order-by) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 [ ORDER BY expression [ ASC | DESC ] ]
[ NULLS FIRST | NULLS LAST ]
[ LIMIT { count | ALL } ]
[ OFFSET start ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
    id INT,
    name VARCHAR(20),
    manager_id INT,
    salary DECIMAL(10, 2)
);

INSERT INTO employee (id, name, manager_id, salary) VALUES
(100, 'Carlos', NULL, 120000.00),
(101, 'John', 100, 90000.00),
(102, 'Jorge', 101, 95000.00),
(103, 'Kwaku', 101, 105000.00),
(104, 'Paulo', 102, 110000.00),
(105, 'Richard', 102, 85000.00),
(106, 'Mateo', 103, 95000.00),
(107, 'Liu', 103, 108000.00),
(108, 'Zhang', 104, 95000.00);

SELECT id, name, manager_id, salary
INTO salaries
FROM employee
ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
LIMIT 5
OFFSET 2;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee (
    id INT,
    name VARCHAR(20),
    manager_id INT,
    salary DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id, salary) VALUES
(100, 'Carlos', NULL, 120000.00),
(101, 'John', 100, 90000.00),
(102, 'Jorge', 101, 95000.00),
(103, 'Kwaku', 101, 105000.00),
(104, 'Paulo', 102, 110000.00),
(105, 'Richard', 102, 85000.00),
(106, 'Mateo', 103, 95000.00),
(107, 'Liu', 103, 108000.00),
(108, 'Zhang', 104, 95000.00);

CREATE TABLE IF NOT EXISTS salaries AS
    SELECT id, name, manager_id, salary
    FROM
        employee
    ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
    LIMIT 5
    OFFSET 2;
```

##### Results

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## SELECT list

### Description

> The SELECT list names the columns, functions, and expressions that you want the query to return. The list represents the output of the query. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

Note

:class: tip
The [query start options](https://docs.snowflake.com/en/sql-reference/sql/select) are fully supported in Snowflake. Just keep in mind that in Snowflake the `DISTINCT` and `ALL` options must go at the beginning of the query.

Note

In Redshift, if your application allows foreign keys or invalid primary keys, it can cause queries to return incorrect results. For example, a SELECT DISTINCT query could return duplicate rows if the primary key column does not contain all unique values. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

### Grammar Syntax

Copy code

```
 SELECT
[ TOP number ]
[ ALL | DISTINCT ] * | expression [ AS column_alias ] [, ...]
```

### Sample Source Patterns

#### Top clause

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT TOP 5 id, name, manager_id
INTO top_employees
FROM employee;

SELECT * FROM top_employees;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee
(
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE IF NOT EXISTS top_employees AS
SELECT TOP 5 id, name, manager_id
  FROM
    employee;

SELECT * FROM
  top_employees;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

Expand

Show lessSee more

#### ALL

##### Input Code:

##### Redshift

Copy code

```
:force:
SELECT ALL manager_id
INTO manager
FROM employee;
```

##### Results

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 101 |
| 101 |
| 102 |
| 103 |
| 103 |
| 103 |
| 104 |
| 104 |
| 102 |
| 104 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS manager AS
SELECT ALL manager_id
FROM
employee;
```

##### Results

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 101 |
| 101 |
| 102 |
| 103 |
| 103 |
| 103 |
| 104 |
| 104 |
| 102 |
| 104 |

Expand

Show lessSee more

#### DISTINCT

##### Input Code:

##### Redshift

Copy code

```
:force:
SELECT DISTINCT manager_id
INTO manager
FROM employee;
```

##### Results

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS manager AS
SELECT DISTINCT manager_id
FROM
employee;
```

##### Results

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## UNION, INTERSECT, and EXCEPT

### Description

> The `UNION`, `INTERSECT`, and `EXCEPT` *set operators* are used to compare and merge the results of two separate query expressions. ([Redshift SQL Language Reference Set Operators](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html))

Note

:class: tip
[Set operators](https://docs.snowflake.com/en/sql-reference/operators-query) are fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 query
{ UNION [ ALL ] | INTERSECT | EXCEPT | MINUS }
query
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 SELECT id, name, manager_id
INTO some_employees
FROM
employee
WHERE manager_id = 101

UNION

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 102

UNION ALL

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

INTERSECT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 103

EXCEPT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 104;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 102 | Jorge | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS some_employees AS
SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

UNION

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 102

UNION ALL

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

INTERSECT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 103

EXCEPT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 104;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## WHERE clause

### Description

> The `WHERE` clause contains conditions that either join tables or apply predicates to columns in tables. ([Redshift SQL Language Reference WHERE Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WHERE_clause.html))

Note

:class: tip
The [WHERE clause](https://docs.snowflake.com/en/sql-reference/constructs/where) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 [ WHERE condition ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT id, name, manager_id
INTO employee_names
FROM employee
WHERE name LIKE 'J%';
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE IF NOT EXISTS employee_names AS
  SELECT id, name, manager_id
  FROM
    employee
  WHERE name LIKE 'J%' ESCAPE '\\';
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## WITH clause

### Description

> A `WITH` clause is an optional clause that precedes the SELECT INTO in a query. The `WITH` clause defines one or more *common\_table\_expressions*. Each common table expression (CTE) defines a temporary table, which is similar to a view definition. You can reference these temporary tables in the `FROM` clause. ([Redshift SQL Language Reference WITH Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html))

Note

:class: tip
The [WITH clause](https://docs.snowflake.com/en/sql-reference/constructs/with) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]

--Where common_table_expression can be either non-recursive or recursive.
--Following is the non-recursive form:
CTE_table_name [ ( column_name [, ...] ) ] AS ( query )

--Following is the recursive form of common_table_expression:
CTE_table_name (column_name [, ...] ) AS ( recursive_query )
```

### Sample Source Patterns

#### Non-Recursive form

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);

INSERT INTO orders (order_id, customer_id, order_date, total_amount)
VALUES
(1, 101, '2024-02-01', 250.00),
(2, 102, '2024-02-02', 600.00),
(3, 103, '2024-02-03', 150.00),
(4, 104, '2024-02-04', 750.00),
(5, 105, '2024-02-05', 900.00);

WITH HighValueOrders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM orders
    WHERE total_amount > 500
)
SELECT * INTO high_value_orders FROM HighValueOrders;

SELECT * FROM high_value_orders;
```

##### Results

| ORDER\_ID | CUSTOMER\_ID | ORDER\_DATE | TOTAL\_AMOUNT |
| --- | --- | --- | --- |
| 2 | 102 | 2024-02-02 | 600.00 |
| 4 | 104 | 2024-02-04 | 750.00 |
| 5 | 105 | 2024-02-05 | 900.00 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';

INSERT INTO orders (order_id, customer_id, order_date, total_amount)
VALUES
(1, 101, '2024-02-01', 250.00),
(2, 102, '2024-02-02', 600.00),
(3, 103, '2024-02-03', 150.00),
(4, 104, '2024-02-04', 750.00),
(5, 105, '2024-02-05', 900.00);

CREATE TABLE IF NOT EXISTS high_value_orders AS
WITH HighValueOrders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM
        orders
    WHERE total_amount > 500
    )
    SELECT *
    FROM
    HighValueOrders;

SELECT * FROM
    high_value_orders;
```

##### Results

| ORDER\_ID | CUSTOMER\_ID | ORDER\_DATE | TOTAL\_AMOUNT |
| --- | --- | --- | --- |
| 2 | 102 | 2024-02-02 | 600.00 |
| 4 | 104 | 2024-02-04 | 750.00 |
| 5 | 105 | 2024-02-05 | 900.00 |

Expand

Show lessSee more

#### Recursive form

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE employee (
   id INT,
   name VARCHAR(20),
   manager_id INT
);

INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

WITH RECURSIVE john_org(id, name, manager_id, level)
AS
(
   SELECT id, name, manager_id, 1 AS level
   FROM employee
   WHERE name = 'John'
   UNION ALL
   SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
   FROM employee e, john_org j
   WHERE e.manager_id = j.id and level < 4
)
SELECT DISTINCT id, name, manager_id into new_org FROM john_org ORDER BY manager_id;

SELECT * FROM new_org;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 103 | Kwaku | 101 |
| 102 | Jorge | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 105 | Richard | 103 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE employee (
   id INT,
   name VARCHAR(20),
   manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);
CREATE TABLE IF NOT EXISTS new_org AS
WITH RECURSIVE john_org(id, name, manager_id, level)
AS
(
   SELECT id, name, manager_id, 1 AS level
   FROM
         employee
   WHERE name = 'John'
   UNION ALL
   SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
   FROM
         employee e,
         john_org j
   WHERE e.manager_id = j.id and level < 4
   )
   SELECT DISTINCT id, name, manager_id
   FROM
   john_org
   ORDER BY manager_id;
SELECT * FROM
   new_org;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 103 | Kwaku | 101 |
| 102 | Jorge | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 105 | Richard | 103 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.
