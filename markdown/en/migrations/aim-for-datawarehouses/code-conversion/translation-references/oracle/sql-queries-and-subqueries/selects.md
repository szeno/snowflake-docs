# Oracle - Select

In this section you could find information about the select query syntax and its conversions.

Note

Some parts in the output codes are omitted for clarity reasons.

## Overall Select Translation

### Simple select

#### Oracle:

Copy code

```
select * from table1;
select col1 from schema1.table1;
```

#### Snowflake:

Copy code

```
select * from
table1;

select col1 from
schema1.table1;
```

### Where clause

#### Oracle:

Copy code

```
select col1 from schema1.table1 WHERE col1 = 1 and id > 0 or id < 1;
```

#### Snowflake:

Copy code

```
select col1 from
schema1.table1
WHERE col1 = 1 and id > 0 or id < 1;
```

### Order By clause

#### Oracle:

Copy code

```
select col1 from schema1.table1 order by id ASC;
```

#### Snowflake:

Copy code

```
select col1 from
schema1.table1
order by id ASC;
```

### Group by

#### Oracle:

Copy code

```
select col1 from schema1.table1 GROUP BY id;
```

#### Snowflake:

Copy code

```
select col1 from
schema1.table1
GROUP BY id;
```

### Model Clause

The model clause is not supported yet.

### Row Limiting Clause

#### Oracle:

Copy code

```
-- Using ONLY
select * from TableFetch1 FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 FETCH FIRST 20 percent ROWS ONLY;
select * from TableFetch1 order by col1 FETCH FIRST 2 ROWS with ties;
select * from TableFetch1 order by col1 FETCH FIRST 20 percent ROWS with ties;

-- Using OFFSET clause
select * from TableFetch1 offset 2 rows FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 offset 2 rows FETCH FIRST 60 percent rows ONLY;
select * from TableFetch1
order by col1 offset 2 rows FETCH NEXT 2 ROWs with ties;
select * from TableFetch1
order by col1 offset 2 rows FETCH FIRST 60 percent ROWs with ties;

-- Using WITH TIES clause
select * from TableFetch1 FETCH FIRST 2 ROWS with ties;
select * from TableFetch1 FETCH FIRST 20 percent ROWS with ties;
select * from TableFetch1 offset 2 rows FETCH NEXT 2 ROWs with ties;
select * from TableFetch1 offset 2 rows FETCH FIRST 60 percent ROWs with ties;

-- Using ORDER BY clause
select * from TableFetch1 order by col1 FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 order by col1 FETCH FIRST 20 percent ROWS ONLY;
select * from TableFetch1 order by col1 offset 2 rows FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1
order by col1 offset 2 rows FETCH FIRST 60 percent ROWS ONLY;

select * from TableFetch1 FETCH FIRST ROWS ONLY;

select * from TableFetch1 offset 2 rows;
```

#### Snowflake:

Copy code

```
-- Using ONLY
select * from
TableFetch1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
QUALIFY
RANK() OVER (
order by col1) <= 2;

select * from
TableFetch1
QUALIFY
(RANK() OVER (
order by col1) - 1) / COUNT(*) OVER () < 20 / 100;

-- Using OFFSET clause
select * from
TableFetch1
offset 2 rows FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

select * from
TableFetch1
QUALIFY
RANK() OVER (
order by col1) - 2 <= 2
LIMIT NULL OFFSET 2;

select * from
TableFetch1
QUALIFY
(RANK() OVER (
order by col1) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

-- Using WITH TIES clause
select * from
TableFetch1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
offset 2 rows FETCH NEXT 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

-- Using ORDER BY clause
select * from
TableFetch1
order by col1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
order by col1) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
order by col1 offset 2 rows FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
order by col1) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

select * from
TableFetch1
FETCH FIRST 1 ROWS ONLY;

select * from
TableFetch1
LIMIT NULL OFFSET 2;
```

Note

In Oracle, the `FETCH` / `OFFSET WITH TIES` is ignored when no `ORDER BY` is specified in the `SELECT`. This case will be transformed to a `FETCH` / `OFFSET` with the ONLY keyword in Snowflake, please note that in Snowflake the `ONLY` keyword has no effect in the results and is used just for readability.

## Pivot

Snowflake does not support the following statements:  
- Rename columns  
- Multiple Columns

### Oracle:

Copy code

```
select * from schema1.table1
PIVOT(count(*) as count1 FOR (column1, column2) IN (row1 as rowName));
```

#### Snowflake:

Copy code

```
select * from
schema1.table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
PIVOT (count(*)
                !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT MULTIPLE COLUMN NOT SUPPORTED ***/!!!
                FOR (column1, column2)
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
IN (row1 as rowName));
```

## Unpivot

Snowflake does not support the following statements:  
- INCLUDE / EXCLUDE NULLS

### Oracle:

Copy code

```
select * from schema1.table1
UNPIVOT INCLUDE NULLS (column1 FOR column2 IN (ANY, ANY));
```

#### Snowflake:

Copy code

```
select * from
schema1.table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT INCLUDE NULLS NOT SUPPORTED ***/!!!
UNPIVOT ( column1 FOR column2 IN (
ANY,
ANY));
```

## Transformation of JOIN (+) to ANSI Syntax

Danger

This translation is currently deactivated and it’s only meant for reference for translations done with previous tool versions. For the current translation check the section above.

The NON-ANSI special outer join (+) syntax is translated to ANSI outer join syntax. This subsection shows some examples:

### To LEFT OUTER JOIN

Example 1:

#### Oracle:

Copy code

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e
WHERE  d.department_id = e.department_id (+)
AND    d.department_id >= 30;
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON d.department_id = e.department_id
WHERE
       d.department_id >= 30;
```

Example 2:

#### Oracle:

Copy code

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e
WHERE  d.department_id(+)  = e.department_id
AND    d.department_id >= 30;
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name
FROM
       employees e
       LEFT OUTER JOIN
              departments d
              ON d.department_id = e.department_id
WHERE
       d.department_id >= 30;
```

Example 3: Multiple join

#### Oracle:

Copy code

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e, projects p
WHERE  e.department_id(+) = d.department_id
AND    p.department_id(+) = d.department_id
AND    d.department_id >= 30;
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON e.department_id = d.department_id
       LEFT OUTER JOIN
              projects p
              ON p.department_id = d.department_id
WHERE
       d.department_id >= 30;
```

Example 4: Join with other kinds of conditional

#### Oracle:

Copy code

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e
WHERE  d.department_id(+)  = e.department_id
AND    d.location(+) IN ('CHICAGO', 'BOSTON', 'NEW YORK')
AND    d.department_id >= 30;
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name
FROM
       employees e
       LEFT OUTER JOIN
              departments d
              ON d.department_id = e.department_id
              AND d.location IN ('CHICAGO', 'BOSTON', 'NEW YORK')
WHERE
       d.department_id >= 30;
```

Example 5: Join with (+) inside a function

#### Oracle:

Copy code

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e
WHERE SUBSTR(d.department_name, 1, NVL(e.department_id, 1) ) = e.employee_name(+);
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON SUBSTR(d.department_name, 1, NVL(e.department_id, 1) ) = e.employee_name;
```

Warning

Please be aware that some of the patterns that were translated to LEFT OUTER JOIN could retrieve the rows in a different order.

### To CROSS JOIN

Example 6: Complex case that requires the use of CROSS JOIN

#### Oracle:

Copy code

```
SELECT d.department_name,
       e.employee_name,
       p.project_name,
       c.course_name
FROM   departments d, employees e, projects p, courses c
WHERE
e.salary (+) >= 2000 AND
d.department_id = e.department_id (+)
AND p.department_id = e.department_id(+)
AND c.course_id  = e.department_id(+)
AND d.department_id >= 30;
```

#### Snowflake:

Copy code

```
SELECT d.department_name,
       e.employee_name,
       p.project_name,
       c.course_name
FROM
       departments d
       CROSS JOIN projects p
       CROSS JOIN courses c
       LEFT OUTER JOIN
              employees e
              ON
              e.salary >= 2000
              AND
              d.department_id = e.department_id
              AND p.department_id = e.department_id
              AND c.course_id  = e.department_id
WHERE
       d.department_id >= 30;
```

## Hierarchical Queries

Hierarchical queries in Snowflake allow you to organize and retrieve data in a tree-like structure, typically using the [`CONNECT BY`](https://docs.snowflake.com/en/sql-reference/constructs/connect-by) clause. This clause joins a table to itself to process hierarchical data in the table.

### Sample Source Patterns

#### Oracle:

Copy code

```
SELECT employee_ID, manager_ID, title
FROM employees
START WITH manager_ID = 1
CONNECT BY manager_ID = PRIOR employee_id;
```

#### Snowflake:

Copy code

```
SELECT employee_ID, manager_ID, title
FROM
employees
START WITH manager_ID = 1
CONNECT BY
manager_ID = PRIOR employee_id;
```

### Related EWIs

1. [SSC-EWI-0015](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0015): Pivot/Unpivot multiple functions not supported.

## Select Flashback Query

### Description

**Oracle**

The flashback query claused in Oracle retrieves past data from a table, view, or materialized view. In Oracle, the uses can include:

- Restoring deleted data or undoing an incorrect commit, comparing current data with the corresponding data at an earlier time, checking the state of transactional data at a particular time, and reporting generation tools to past data, among others. ([Oracle Flashback query documentation](https://docs.oracle.com/cd/E11882_01/appdev.112/e41502/adfns_flashback.htm#ADFNS01003)).

**Snowflake**

The equivalent mechanism in Snowflake to query data from the past is the `AT | BEGIN` query. Notice that the only equivalent is for the `AS OF` statements.

Furthermore, Snowflake has complete “Time Travel” documentation that allows querying data to clone objects such as tables, views, and schemas. There are limitations on the days to access the past or deleted data (90 days before passing to Fail-safe status). For more information, review the [Snowflake Time Travel Documentation](https://docs.snowflake.com/en/user-guide/data-time-travel).

**Oracle syntax**

Copy code

```
{ VERSIONS BETWEEN
  { SCN | TIMESTAMP }
  { expr | MINVALUE } AND { expr | MAXVALUE }
| AS OF { SCN | TIMESTAMP } expr
}
```

**Snowflake Syntax**

Copy code

```
SELECT ...
FROM ...
  {
   AT( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) |
   BEFORE( STATEMENT => <id> )
  }
[ ... ]
```

Note

Notice that the query ID must reference a query executed within 14 days. If the query ID references a query over 14 days old, the following error is returned: `Error: statement <query_id> not found`. To work around this limitation, use the time stamp for the referenced query. ([Snowflake AT | Before documentation](https://docs.snowflake.com/en/sql-reference/constructs/at-before#syntax))

### Sample Source Patterns

The following data is used in the following examples to generate the query outputs.

#### Oracle

Copy code

```
CREATE TABLE Employee (
    EmployeeID NUMBER PRIMARY KEY,
    FirstName VARCHAR2(50),
    LastName VARCHAR2(50),
    EmailAddress VARCHAR2(100),
    HireDate DATE,
    SalaryAmount NUMBER(10, 2)
);

INSERT INTO Employee VALUES (1, 'Bob', 'SampleNameA', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (2, 'Bob', 'SampleNameB', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (3, 'Bob', 'SampleNameC', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (4, 'Bob', 'SampleNameD', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (5, 'Bob', 'SampleNameE', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Employee (
       EmployeeID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
       FirstName VARCHAR(50),
       LastName VARCHAR(50),
       EmailAddress VARCHAR(100),
       HireDate TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
       SalaryAmount NUMBER(10, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
   ;

   INSERT INTO Employee
   VALUES (1, 'Bob', 'SampleNameA', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (2, 'Bob', 'SampleNameB', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (3, 'Bob', 'SampleNameC', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (4, 'Bob', 'SampleNameD', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (5, 'Bob', 'SampleNameE', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
```

#### 1. AS OF with TIMESTAMP case

##### Oracle

Copy code

```
SELECT * FROM employees
AS OF TIMESTAMP
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

##### Snowflake

Copy code

```
SELECT * FROM
employees
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0135 - DATA RETENTION PERIOD MAY PRODUCE NO RESULTS ***/!!!
AT (TIMESTAMP =>
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS'))
WHERE last_name = 'SampleName';
```

#### 2. AS OF with SCN case

##### Oracle

Copy code

```
SELECT * FROM employees
AS OF SCN
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

##### Snowflake

Copy code

```
SELECT * FROM
employees
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'FLASHBACK QUERY' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
AS OF SCN
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

### Known Issues

1. The option when it is using SCN is not supported.
2. The VERSION statement is not supported in Snowflake.

### Related EWIs

1. [SSC-EWI-0040](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040): Statement Not Supported.
2. [SSC-EWI-OR0135](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0135): Current of clause is not supported in Snowflake.
3. [SSC-FDM-0006](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.
4. [SSC-FDM-OR0042](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.
