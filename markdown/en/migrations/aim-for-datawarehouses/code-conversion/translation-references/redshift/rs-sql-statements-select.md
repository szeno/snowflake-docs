# Redshift - SELECT

## SELECT

### Description

Returns rows from tables, views, and user-defined functions. ([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

### Grammar Syntax

Copy code

```
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number | [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...] ]
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ [ START WITH expression ] CONNECT BY expression ]
[ GROUP BY expression [, ...] ]
[ HAVING condition ]
[ QUALIFY condition ]
[ { UNION | ALL | INTERSECT | EXCEPT | MINUS } query ]
[ ORDER BY expression [ ASC | DESC ] ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

For more information please refer to each of the following links:

1. [WITH clause](#with-clause)
2. [SELECT list](#select-list)
3. [FROM clause](#from-clause)
4. [WHERE clause](#where-clause)
5. [CONNECT BY clause](#connect-by-clause)
6. [GROUP BY clause](#group-by-clause)
7. [HAVING clause](#having-clause)
8. [QUALIFY clause](#qualify-clause)
9. [UNION, INTERSECT, and EXCEPT](#union-intersect-and-except)
10. [ORDER BY clause](#order-by-clause)

## CONNECT BY clause

### Description

The `CONNECT BY` clause specifies the relationship between rows in a hierarchy. You can use `CONNECT BY` to select rows in a hierarchical order by joining the table to itself and processing the hierarchical data. ([Redshift SQL Language Reference CONNECT BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_CONNECT_BY_clause.html))

Note

:class: tip
The [CONNECT BY clause](https://docs.snowflake.com/en/sql-reference/constructs/connect-by) is supported in Snowflake.

### Grammar Syntax

Copy code

```
 [START WITH start_with_conditions]
CONNECT BY connect_by_conditions
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

SELECT COUNT(*)
FROM
Employee "start"
CONNECT BY PRIOR id = manager_id
START WITH name = 'John';
```

##### Results

| COUNT(\*) |
| --- |
| 12 |

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

SELECT
  COUNT(*)
FROM
  Employee "start"
CONNECT BY PRIOR id = manager_id
START WITH name = 'John';
```

##### Results

| COUNT(\*) |
| --- |
| 12 |

Expand

Show lessSee more

### Related EWIs

There are no known issues.

## FROM clause

### Description

The `FROM` clause in a query lists the table references (tables, views, and subqueries) that data is selected from. If multiple table references are listed, the tables must be joined, using appropriate syntax in either the `FROM` clause or the `WHERE` clause. If no join criteria are specified, the system processes the query as a cross-join. ([Redshift SQL Language Reference FROM Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html))

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

#### Join types

Snowflake supports all types of joins. For more information, see [the JOIN documentation.](https://docs.snowflake.com/en/sql-reference/constructs/join)

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
FROM employee e
INNER JOIN department d ON e.manager_id = d.manager_id;

SELECT e.name AS employee_name, d.name AS department_name
FROM employee e
LEFT JOIN department d ON e.manager_id = d.manager_id;

SELECT d.name AS department_name, e.name AS manager_name
FROM department d
RIGHT JOIN employee e ON d.manager_id = e.id;

SELECT e.name AS employee_name, d.name AS department_name
FROM employee e
FULL JOIN department d ON e.manager_id = d.manager_id;
```

##### Results

##### Inner Join

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

##### Left Join

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

Expand

Show lessSee more

##### Right Join

| DEPARTMENT\_NAME | MANAGER\_NAME |
| --- | --- |
| HR | Carlos |
| Sales | John |
| Engineering | Jorge |
| Marketing | Kwaku |
| null | Liu |
| null | Mateo |
| null | Nikki |
| null | Paulo |
| null | Richard |
| null | Saanvi |
| null | Shirley |
| null | Sofía |
| null | Zhang |

Expand

Show lessSee more

##### Full Join

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO department (id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
INNER JOIN
  department d ON e.manager_id = d.manager_id;

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
LEFT JOIN
  department d ON e.manager_id = d.manager_id;

SELECT d.name AS department_name, e.name AS manager_name
FROM
department d
RIGHT JOIN
  employee e ON d.manager_id = e.id;

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
FULL JOIN
  department d ON e.manager_id = d.manager_id;
```

##### Results

##### Inner Join

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

##### Left Join

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

Expand

Show lessSee more

##### Right Join

| DEPARTMENT\_NAME | MANAGER\_NAME |
| --- | --- |
| HR | Carlos |
| Sales | John |
| Engineering | Jorge |
| Marketing | Kwaku |
| null | Liu |
| null | Mateo |
| null | Nikki |
| null | Paulo |
| null | Richard |
| null | Saanvi |
| null | Shirley |
| null | Sofía |
| null | Zhang |

Expand

Show lessSee more

##### Full Join

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

Expand

Show lessSee more

#### Pivot Clause

Note

Column aliases cannot be used in the IN clause of the PIVOT query in Snowflake.

##### Input Code:

##### Redshift

Copy code

```
 SELECT *
FROM
    (SELECT e.manager_id, d.name AS department, e.id AS employee_id
     FROM employee e
     JOIN department d ON e.manager_id = d.manager_id) AS SourceTable
PIVOT
    (
     COUNT(employee_id)
     FOR department IN ('HR', 'Sales', 'Engineering', 'Marketing')
    ) AS PivotTable;
```

##### Results

| MANAGER\_ID | ‘HR’ | ‘Sales’ | ‘Engineering’ | ‘Marketing’ |
| --- | --- | --- | --- | --- |
| 100 | 1 | 0 | 0 | 0 |
| 101 | 0 | 3 | 0 | 0 |
| 102 | 0 | 0 | 2 | 0 |
| 103 | 0 | 0 | 0 | 3 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 SELECT *
FROM
    (SELECT e.manager_id, d.name AS department, e.id AS employee_id
     FROM
     employee e
     JOIN
         department d ON e.manager_id = d.manager_id) AS SourceTable
PIVOT
    (
     COUNT(employee_id)
     FOR department IN ('HR', 'Sales', 'Engineering', 'Marketing')
    ) AS PivotTable;
```

##### Results

| MANAGER\_ID | ‘HR’ | ‘Sales’ | ‘Engineering’ | ‘Marketing’ |
| --- | --- | --- | --- | --- |
| 100 | 1 | 0 | 0 | 0 |
| 101 | 0 | 3 | 0 | 0 |
| 102 | 0 | 0 | 2 | 0 |
| 103 | 0 | 0 | 0 | 3 |

Expand

Show lessSee more

#### Unpivot Clause

Note

Column aliases cannot be used in the IN clause of the UNPIVOT query in Snowflake.

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE count_by_color (quality VARCHAR, red INT, green INT, blue INT);

INSERT INTO count_by_color VALUES ('high', 15, 20, 7);
INSERT INTO count_by_color VALUES ('normal', 35, NULL, 40);
INSERT INTO count_by_color VALUES ('low', 10, 23, NULL);

SELECT *
FROM (SELECT red, green, blue FROM count_by_color) UNPIVOT (
    cnt FOR color IN (red, green, blue)
);

SELECT *
FROM (SELECT red, green, blue FROM count_by_color) UNPIVOT (
    cnt FOR color IN (red r, green as g, blue)
);
```

##### Results

| COLOR | CNT |
| --- | --- |
| RED | 15 |
| RED | 35 |
| RED | 10 |
| GREEN | 20 |
| GREEN | 23 |
| BLUE | 7 |
| BLUE | 40 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE count_by_color (quality VARCHAR, red INT, green INT, blue INT)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO count_by_color
VALUES ('high', 15, 20, 7);
INSERT INTO count_by_color
VALUES ('normal', 35, NULL, 40);
INSERT INTO count_by_color
VALUES ('low', 10, 23, NULL);

SELECT *
FROM (SELECT red, green, blue FROM
            count_by_color
    ) UNPIVOT (
    cnt FOR color IN (red, green, blue)
);

SELECT *
FROM (SELECT red, green, blue FROM
            count_by_color
) UNPIVOT (
    cnt FOR color IN (red
                          !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - SNOWCONVERT AI TRANSLATION FOR COLUMN ALIASES IN THE PIVOT/UNPIVOT IN CLAUSE IS PENDING. ***/!!!
 r, green
          !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - SNOWCONVERT AI TRANSLATION FOR COLUMN ALIASES IN THE PIVOT/UNPIVOT IN CLAUSE IS PENDING. ***/!!!
 as g, blue)
);
```

##### Results

| COLOR | CNT |
| --- | --- |
| RED | 15 |
| GREEN | 20 |
| BLUE | 7 |
| RED | 35 |
| BLUE | 40 |
| RED | 10 |
| GREEN | 23 |

Expand

Show lessSee more

### Related EWIs

1. [SSC-EWI-RS0005](../../issues-and-troubleshooting/conversion-issues/redshiftEWI#ssc-ewi-rs0005): Translation for column aliases in the PIVOT/UNPIVOT IN clause is pending.

## GROUP BY clause

### Description

The `GROUP BY` clause identifies the grouping columns for the query. Grouping columns must be declared when the query computes aggregates with standard functions such as `SUM`, `AVG`, and `COUNT`. ([Redshift SQL Language Reference GROUP BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_GROUP_BY_clause.html))

Note

:class: tip
The [GROUP BY clause](https://docs.snowflake.com/en/sql-reference/constructs/group-by) is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 GROUP BY group_by_clause [, ...]

group_by_clause := {
    expr |
    GROUPING SETS ( () | group_by_clause [, ...] ) |
    ROLLUP ( expr [, ...] ) |
    CUBE ( expr [, ...] )
    }
```

### Sample Source Patterns

#### Grouping sets

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

SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM employee
GROUP BY GROUPING SETS
    ((manager_id), ())
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
| null | 1 |
| null | 13 |

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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

SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY GROUPING SETS
    ((manager_id), ())
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
| null | 1 |
| null | 13 |

Expand

Show lessSee more

#### Group by Cube

##### Input Code:

##### Redshift

Copy code

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY CUBE(manager_id)
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
| null | 1 |
| null | 13 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY CUBE(manager_id)
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
| null | 1 |
| null | 13 |

Expand

Show lessSee more

#### Group by Rollup

##### Input Code:

##### Redshift

Copy code

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY ROLLUP(manager_id)
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
| null | 1 |
| null | 13 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY ROLLUP(manager_id)
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
| null | 1 |
| null | 13 |

Expand

Show lessSee more

### Related EWIs

There are no known issues.

## HAVING clause

### Description

The `HAVING` clause applies a condition to the intermediate grouped result set that a query returns. ([Redshift SQL Language Reference HAVING Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_HAVING_clause.html))

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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

### Related EWIs

There are no known issues.

## ORDER BY clause

### Description

The `ORDER BY` clause sorts the result set of a query. ([Redshift SQL Language Reference Order By Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html))

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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

### Related EWIs

There are no known issues.

## QUALIFY clause

### Description

The `QUALIFY` clause filters results of a previously computed window function according to user‑specified search conditions. You can use the clause to apply filtering conditions to the result of a window function without using a subquery. ([Redshift SQL Language Reference QUALIFY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_QUALIFY_clause.html))

Note

:class: tip
The [QUALIFY clause](https://docs.snowflake.com/en/sql-reference/constructs/qualify) is supported in Snowflake.

### Grammar Syntax

Copy code

```
 QUALIFY condition
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE store_sales
(
    ss_sold_date DATE,
    ss_sold_time TIME,
    ss_item TEXT,
    ss_sales_price FLOAT
);

INSERT INTO store_sales VALUES ('2022-01-01', '09:00:00', 'Product 1', 100.0),
                               ('2022-01-01', '11:00:00', 'Product 2', 500.0),
                               ('2022-01-01', '15:00:00', 'Product 3', 20.0),
                               ('2022-01-01', '17:00:00', 'Product 4', 1000.0),
                               ('2022-01-01', '18:00:00', 'Product 5', 30.0),
                               ('2022-01-02', '10:00:00', 'Product 6', 5000.0),
                               ('2022-01-02', '16:00:00', 'Product 7', 5.0);

SELECT *
FROM store_sales ss
WHERE ss_sold_time > time '12:00:00'
QUALIFY row_number()
OVER (PARTITION BY ss_sold_date ORDER BY ss_sales_price DESC) <= 2;
```

##### Results

| SS\_SOLD\_DATE | SS\_SOLD\_TIME | SS\_ITEM | SS\_SALES\_PRICE |
| --- | --- | --- | --- |
| 2022-01-01 | 17:00:00 | Product 4 | 1000 |
| 2022-01-01 | 18:00:00 | Product 5 | 30 |
| 2022-01-02 | 16:00:00 | Product 7 | 5 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE TABLE store_sales
(
    ss_sold_date DATE,
    ss_sold_time TIME,
    ss_item TEXT,
    ss_sales_price FLOAT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO store_sales
VALUES ('2022-01-01', '09:00:00', 'Product 1', 100.0),
                               ('2022-01-01', '11:00:00', 'Product 2', 500.0),
                               ('2022-01-01', '15:00:00', 'Product 3', 20.0),
                               ('2022-01-01', '17:00:00', 'Product 4', 1000.0),
                               ('2022-01-01', '18:00:00', 'Product 5', 30.0),
                               ('2022-01-02', '10:00:00', 'Product 6', 5000.0),
                               ('2022-01-02', '16:00:00', 'Product 7', 5.0);

SELECT *
FROM
    store_sales ss
WHERE ss_sold_time > time '12:00:00'
QUALIFY
    ROW_NUMBER()
OVER (PARTITION BY ss_sold_date ORDER BY ss_sales_price DESC) <= 2;
```

##### Results

| SS\_SOLD\_DATE | SS\_SOLD\_TIME | SS\_ITEM | SS\_SALES\_PRICE |
| --- | --- | --- | --- |
| 2022-01-02 | 16:00:00 | Product 7 | 5 |
| 2022-01-01 | 17:00:00 | Product 4 | 1000 |
| 2022-01-01 | 18:00:00 | Product 5 | 30 |

Expand

Show lessSee more

### Related EWIs

There are no known issues.

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
FROM employee;
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
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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

SELECT TOP 5 id, name, manager_id
FROM
    employee;
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
:force:
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

### Related EWIs

There are no known issues.

## UNION, INTERSECT, and EXCEPT

### Description

The `UNION`, `INTERSECT`, and `EXCEPT` *set operators* are used to compare and merge the results of two separate query expressions. ([Redshift SQL Language Reference Set Operators](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html))

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

### Related EWIs

There are no known issues.

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

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

### Related EWIs

There are no known issues.

## WITH clause

### Description

A `WITH` clause is an optional clause that precedes the SELECT list in a query. The `WITH` clause defines one or more *common\_table\_expressions*. Each common table expression (CTE) defines a temporary table, which is similar to a view definition. You can reference these temporary tables in the `FROM` clause. ([Redshift SQL Language Reference WITH Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html))

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

WITH RECURSIVE john_org(id, name, manager_id, level) AS
( SELECT id, name, manager_id, 1 AS level
  FROM employee
  WHERE name = 'John'
  UNION ALL
  SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
  FROM employee e, john_org j
  WHERE e.manager_id = j.id and level < 4
)
SELECT DISTINCT id, name, manager_id FROM john_org ORDER BY manager_id;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 110 | Liu | 101 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 201 | Sofía | 102 |
| 106 | Mateo | 102 |
| 105 | Richard | 103 |
| 104 | Paulo | 103 |
| 110 | Nikki | 103 |
| 205 | Zhang | 104 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |

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

WITH RECURSIVE john_org(id, name, manager_id, level) AS
( SELECT id, name, manager_id, 1 AS level
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
SELECT DISTINCT id, name, manager_id FROM
  john_org
ORDER BY manager_id;
```

##### Results

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 105 | Richard | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

Expand

Show lessSee more

#### Non recursive form

##### Input Code:

##### Redshift

Copy code

```
 WITH ManagerHierarchy AS (
    SELECT id AS employee_id, name AS employee_name, manager_id
    FROM employee
)
SELECT e.employee_name AS employee, m.employee_name AS manager
FROM ManagerHierarchy e
LEFT JOIN ManagerHierarchy m ON e.manager_id = m.employee_id;
```

##### Results

| EMPLOYEE | MANAGER |
| --- | --- |
| Carlos | null |
| John | Carlos |
| Jorge | John |
| Kwaku | John |
| Liu | John |
| Mateo | Jorge |
| Sofía | Jorge |
| Nikki | Kwaku |
| Paulo | Kwaku |
| Richard | Kwaku |
| Saanvi | Paulo |
| Shirley | Paulo |
| Zhang | Paulo |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 WITH ManagerHierarchy AS (
    SELECT id AS employee_id, name AS employee_name, manager_id
    FROM
    employee
)
SELECT e.employee_name AS employee, m.employee_name AS manager
FROM
    ManagerHierarchy e
LEFT JOIN
    ManagerHierarchy m ON e.manager_id = m.employee_id;
```

##### Results

| EMPLOYEE | MANAGER |
| --- | --- |
| John | Carlos |
| Jorge | John |
| Kwaku | John |
| Liu | John |
| Mateo | Jorge |
| Sofía | Jorge |
| Nikki | Kwaku |
| Paulo | Kwaku |
| Richard | Kwaku |
| Saanvi | Paulo |
| Shirley | Paulo |
| Zhang | Paulo |
| Carlos | null |

Expand

Show lessSee more

### Related EWIs

There are no known issues.
