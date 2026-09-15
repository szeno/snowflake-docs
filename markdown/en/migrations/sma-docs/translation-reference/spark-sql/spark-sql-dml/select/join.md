description:
:   Join the fun! Use the SMA today!

# Snowpark Migration Accelerator: Join

## Description

Merges rows from two [table references](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-table-reference.html) using specified join conditions. For more details, see the [Databricks SQL Language Reference JOIN](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-join.html).

A `JOIN` combines data from two sources (such as tables or views) into a single result set. Each row in the result contains columns from both sources based on a specified condition. For a detailed explanation of joins, see [Working with Joins](https://docs.snowflake.com/en/user-guide/querying-joins). ([Snowflake SQL Language Reference JOIN](https://docs.snowflake.com/en/sql-reference/constructs/join))

### Syntax

```
left_table_reference { [ join_type ] JOIN right_table_reference join_criteria |
           NATURAL join_type JOIN right_table_reference |
           CROSS JOIN right_table_reference }

join_type
  { [ INNER ] |
    LEFT [ OUTER ] |
    [ LEFT ] SEMI |
    RIGHT [ OUTER ] |
    FULL [ OUTER ] |
    [ LEFT ] ANTI |
    CROSS }

join_criteria
  { ON boolean_expression |
    USING ( column_name [, ...] ) }
```

Copy code

```
SELECT ...
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ ON <condition> ]
[ ... ]

SELECT *
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ USING( <column_list> ) ]
[ ... ]

SELECT ...
FROM <object_ref1> [
                     {
                       | NATURAL [ { LEFT | RIGHT | FULL } [ OUTER ] ]
                       | CROSS
                     }
                   ]
                   JOIN <object_ref2>
[ ... ]
```

## Sample Source Patterns

### Setup data

#### Databricks

Copy code

```
-- Use employee and department tables to demonstrate different type of joins.
CREATE TEMP VIEW employee(id, name, deptno) AS
     VALUES(105, 'Chloe', 5),
           (103, 'Paul', 3),
           (101, 'John', 1),
           (102, 'Lisa', 2),
           (104, 'Evan', 4),
           (106, 'Amy', 6);

CREATE TEMP VIEW department(deptno, deptname) AS
    VALUES(3, 'Engineering'),
          (2, 'Sales'      ),
          (1, 'Marketing'  );
```

#### Snowflake

Copy code

```
-- Use employee and department tables to demonstrate different type of joins.
CREATE TEMPORARY TABLE employee(id, name, deptno) AS
SELECT id, name, deptno
  FROM (VALUES (105, 'Chloe', 5),
           (103, 'Paul' , 3),
           (101, 'John' , 1),
           (102, 'Lisa' , 2),
           (104, 'Evan' , 4),
           (106, 'Amy'  , 6)) AS v1 (id, name, deptno);

CREATE TEMP VIEW department(deptno, deptname) AS
SELECT deptno, deptname
  FROM (VALUES(3, 'Engineering'),
          (2, 'Sales'      ),
          (1, 'Marketing'  )) AS v1 (deptno, deptname);
```

### Pattern code

#### Databricks

Copy code

```
-- 1. Use employee and department tables to demonstrate inner join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   INNER JOIN department ON employee.deptno = department.deptno;

-- 2. We will use the employee and department tables to show how a left join works. This example will help you understand how to combine data from two tables while keeping all records from the left (first) table.
SELECT id, name, employee.deptno, deptname
   FROM employee
   LEFT JOIN department ON employee.deptno = department.deptno;

-- 3. Demonstrate a RIGHT JOIN using employee and department tables. This query retrieves all departments and matching employees.
SELECT id, name, employee.deptno, deptname
    FROM employee
    RIGHT JOIN department ON employee.deptno = department.deptno;

-- 4. Demonstrate a FULL JOIN operation using the employee and department tables.
SELECT id, name, employee.deptno, deptname
    FROM employee
    FULL JOIN department ON employee.deptno = department.deptno;

-- 5. Demonstrate a cross join operation using the employee and department tables. This query returns all possible combinations of employees and departments.
SELECT id, name, employee.deptno, deptname
    FROM employee
    CROSS JOIN department;

-- 6. This example shows how to use a semi join between employee and department tables. A semi join returns records from the first table (employee) where there is a matching record in the second table (department).
```{code} sql
SELECT *
    FROM employee
    SEMI JOIN department ON employee.deptno = department.deptno;
```

1. We will use two sample tables - “employee” and “department” - to show how an inner join works. An inner join combines rows from both tables where there is a match between specified columns.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |

Expand

Show lessSee more

---

1. We will use the employee and department tables to show how a left join works. This example will help you understand how to combine data from two tables while keeping all records from the left (first) table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a RIGHT JOIN works in SQL.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 102 | Lisa | 2 | Sales |
| 101 | John | 1 | Marketing |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a full join works. A full join combines all records from both tables, including unmatched rows from either table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 103 | Paul | 3 | Engineering |
| 104 | Evan | 4 | null |
| 105 | Chloe | 5 | null |
| 106 | Amy | 6 | null |

Expand

Show lessSee more

---

1. Create a cross join between the employee and department tables to show how to combine every row from one table with every row from another table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | Engineering |
| 105 | Chloe | 5 | Sales |
| 105 | Chloe | 5 | Marketing |
| 103 | Paul | 3 | Engineering |
| 103 | Paul | 3 | Sales |
| 103 | Paul | 3 | Marketing |
| 101 | John | 1 | Engineering |
| 101 | John | 1 | Sales |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Engineering |
| 102 | Lisa | 2 | Sales |
| 102 | Lisa | 2 | Marketing |
| 104 | Evan | 4 | Engineering |
| 104 | Evan | 4 | Sales |
| 104 | Evan | 4 | Marketing |
| 106 | Amy | 6 | Engineering |
| 106 | Amy | 6 | Sales |
| 106 | Amy | 6 | Marketing |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a semi join works. A semi join returns records from the first table where there is a matching record in the second table.

| id | name | deptno |
| --- | --- | --- |
| 103 | Paul | 3 |
| 101 | John | 1 |
| 102 | Lisa | 2 |

Expand

Show lessSee more

#### Snowflake

Copy code

```
-- 1. Use employee and department tables to demonstrate inner join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   INNER JOIN department ON employee.deptno = department.deptno;

-- 2. Use employee and department tables to demonstrate left join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   LEFT JOIN department ON employee.deptno = department.deptno;

-- 3. Use employee and department tables to demonstrate right join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    RIGHT JOIN department ON employee.deptno = department.deptno;

-- 4. Use employee and department tables to demonstrate full join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    FULL JOIN department ON employee.deptno = department.deptno;

-- 5. Use employee and department tables to demonstrate cross join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    CROSS JOIN department;

-- 6. Use employee and department tables to demonstrate semi join.
SELECT e.*
    FROM employee e, department d
    WHERE e.deptno = d.deptno;
```

1. We will use two sample tables - “employee” and “department” - to show how an inner join works. An inner join combines records from both tables where there is a matching value in the specified columns.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |

Expand

Show lessSee more

---

1. Use employee and department tables to demonstrate left join.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a right join works.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 102 | Lisa | 2 | Sales |
| 101 | John | 1 | Marketing |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a full join works. A full join combines all records from both tables, including unmatched rows from either table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

Expand

Show lessSee more

---

1. Create a cross join between the employee and department tables to show how each employee can be paired with every department. This example demonstrates how cross joins work by combining all possible combinations of rows from both tables.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | Engineering |
| 105 | Chloe | 5 | Sales |
| 105 | Chloe | 5 | Marketing |
| 103 | Paul | 3 | Engineering |
| 103 | Paul | 3 | Sales |
| 103 | Paul | 3 | Marketing |
| 101 | John | 1 | Engineering |
| 101 | John | 1 | Sales |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Engineering |
| 102 | Lisa | 2 | Sales |
| 102 | Lisa | 2 | Marketing |
| 104 | Evan | 4 | Engineering |
| 104 | Evan | 4 | Sales |
| 104 | Evan | 4 | Marketing |
| 106 | Amy | 6 | Engineering |
| 106 | Amy | 6 | Sales |
| 106 | Amy | 6 | Marketing |

Expand

Show lessSee more

---

1. Let’s use the employee and department tables to show how a semi join works. A semi join returns records from the first table where there is a matching record in the second table.

| id | name | deptno |
| --- | --- | --- |
| 103 | Paul | 3 |
| 101 | John | 1 |
| 102 | Lisa | 2 |

Expand

Show lessSee more

### Known Issues

No issues were found

### Related EWIs

No related EWIs
