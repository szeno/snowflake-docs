# Teradata - DML

In this section, you will find the documentation for the translation reference of Data Manipulation Language Elements.

## Delete Statement

> See [Delete statement](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/z8eO9bdxtjFRveHdDwwYPQ)

Teradata support calling more than one table in the`FROM`clause, Snowflake does not. Therefore, it is necessary to use the`USING`clause to refer to the extra tables involved in the condition.

**Teradata**

**Delete**

Copy code

```
DEL FROM MY_TABLE ALL;
DEL FROM MY_TABLE_2 WHERE COL1 > 50;
DELETE T1 FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE T1 FROM TABLE2 T2, TABLE1 T1 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 WHERE TABLE1.COLUMN1 = TABLE2.COLUMN2
```

**Snowflake**

**Delete**

Copy code

```
DELETE FROM
MY_TABLE;

DELETE FROM
MY_TABLE_2
WHERE
COL1 > 50;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1
WHERE
TABLE1.COLUMN1 = TABLE2.COLUMN2;
```

### Known Issues

#### 1. DEL abbreviation unsupported

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to DELETE.

### Related EWIs

No related EWIs.

## Set Operators

The SQL set operators manipulate the result sets of several queries combining the results of each query into a single result set.

Note

Some parts in the output code are omitted for clarity reasons.

> See [Set operators](https://docs.teradata.com/r/b8dd8xEYJnxfsq4uFRrHQQ/Q8qU3AO1RXLNFCPOGTX73g)

Set Operators in both Teradata and Snowflake have the same syntax and supported scenarios `EXCEPT`, `INTERSECT`, and `UNION` except for the clause `ALL` in the `INTERSECT ALL`, which is not supported in Snowflake, resulting in the portion of the `ALL` as a commented code after the conversion.

**Teradata**

### Intersect

Copy code

```
 SELECT LastName, FirstName FROM employees
INTERSECT
SELECT FirstName, LastName FROM contractors;

SELECT LastName, FirstName FROM employees
INTERSECT ALL
SELECT FirstName, LastName FROM contractors;
```

**Snowflake**

#### Intersect

Copy code

```
 SELECT
LastName,
FirstName FROM
employees
INTERSECT
SELECT
FirstName,
LastName FROM
contractors;

SELECT
LastName,
FirstName FROM
employees
INTERSECT
        !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'INTERSECT ALL QUANTIFIER' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!! ALL
SELECT
FirstName,
LastName FROM
contractors;
```

### Known Issues

#### 1. INTERSECT ALL unsupported

The INTERSECT ALL is unsupported in Snowflake and then the part ALL will be commented.

### Related EWIs

1. [SSC-EWI-0040](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040): Statement Not Supported.

## Update Statement

### Description

> Modifies column values in existing rows of a table. ([Teradata SQL Language Reference UPDATE](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/k6fC7ozmhIZZXa315VjJAw))

### Sample Source Patterns

#### Basic case

**Teradata**

**Update**

Copy code

```
 UPDATE CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

**Snowflake**

**Update**

Copy code

```
UPDATE CRASHDUMPS.TABLE1 AS i
 SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

#### UPDATE with forward alias

Teradata supports referencing an alias before it is declared, but Snowflake does not. The transformation for this scenario is to take the referenced table and change the alias for the table name it references.

**Teradata**

**Update**

Copy code

```
 UPDATE i
 FROM CRASHDUMPS.TABLE2, CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

**Snowflake**

**Update**

Copy code

```
UPDATE CRASHDUMPS.TABLE1 AS i
  SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
  FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

#### UPDATE with target table in the FROM clause

Teradata supports having the target table defined in the FROM clause, this is removed in Snowflake to avoid duplicate alias and ambiguous column reference errors.

**Teradata**

**Update**

Copy code

```
UPDATE some_table
FROM some_table
SET Code = Code + 100
WHERE Name = 'A';
```

**Snowflake**

**Update**

Copy code

```
UPDATE some_table
  SET Code = Code + 100
  WHERE
  UPPER(RTRIM( Name)) = UPPER(RTRIM('A'));
```

### Related EWIs

No related EWIs.

## With Modifier

Select statement that uses the WITH modifier with a list of several named queries also known as common table expressions (CTEs).

> See [With Modifier](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Manipulation-Language/July-2021/SELECT-Statements/WITH-Modifier)

Snowflake supports Teradata’s `WITH` modifier on a SELECT statement that has several `CTEs` (Common Table Expressions). Teradata supports any order of CTE definition, regardless of whether it is referenced before it is declared or not, but Snowflake requires that if a CTE calls another CTE, it must be defined before it is called. Then the converted sequence of CTEs within the WITH will be reordered into the unreferenced CTEs, then the CTE that calls the next CTE, and so on.

Where there is a cycle detected in the WITH calling sequence, it will be left as the original, without any changes to the sequence as detailed in an example of the [SSC-EWI-TD0077](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0077).

In the example below, there are two CTEs named n1 and n2, the n1 referring to n2. Then the n2 must be defined first in Snowflake as the corresponding converted code.

Note

Some parts of the output code are omitted for clarity reasons.

**Teradata**

### With Modifier

Copy code

```
 WITH recursive n1(c1) as (select c1, c3 from t2, n1),
     n2(c2) as (select c2 from tablex)
     SELECT * FROM t1;
```

**Snowflake**

#### With Modifier

Copy code

```
 WITH RECURSIVE n1(c1) AS
(
     SELECT
          c1,
          c3 from
          t2, n1
),
n2(c2) AS
(
     SELECT
          c2 from
          tablex
)
SELECT
     * FROM
     t1;
```

### Known Issues

#### 1. Impossible to reorder when cycles were found

When the CTEs references are analyzed and there is a cycle between the calls of the CTEs, the CTEs will not be ordered.

### Related EWIs

No related EWIs.

## Insert Statement

SQL statement that adds new rows to a table.

Note

Some parts in the output code are omitted for clarity reasons.

> See [Insert statement](https://docs.teradata.com/r/0I5vemahub4iSU2bk5WA1A/SQ4EQb1a8WMHn3tbrcvW9Q)

In Teradata, there is an alternate`INSERT`syntax that assigns the value for each table column inline. This alternate structure requires a special transformation to be supported in Snowflake. The inline assignment of the values is separated and placed inside the `VALUES(...)` part of the Snowflake `INSERT INTO` statement.

**Teradata**

### Insert

Copy code

```
 INSERT INTO appDB.logTable (
    process_name = 'S2F_BOOKS_LOAD_NEW'
    , session_id = 105678989
    , message_txt = ''
    , message_ts = '2019-07-23 00:00:00'
    , Insert_dt = CAST((CURRENT_TIMESTAMP(0)) AS DATE FORMAT 'YYYY-MM-DD'));
```

**Snowflake**

#### Insert

Copy code

```
 INSERT INTO appDB.logTable (
process_name, session_id, message_txt, message_ts, Insert_dt)
VALUES ('S2F_BOOKS_LOAD_NEW', 105678989, '', '2019-07-23 00:00:00', TO_DATE((CURRENT_TIMESTAMP(0))));
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## LOGGING ERRORS

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is** <mark style=”background-color:red;”>**removed from the migration**</mark> **because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description

Statement to log errors when using statements as `INSERT...SELECT.` Please review the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Statement-Syntax/INSERT/INSERT-...-SELECT/INSERT/INSERT-...-SELECT-Examples/Example-Logging-Errors-with-INSERT-...-SELECT).

### Sample Source Patterns

#### LOGGING ERRORS

In this example, notice that `LOGGING ERRORS` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata

Copy code

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS;
```

##### Snowflake

Copy code

```
INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ALL ERRORS

In this example, notice that `LOGGING ALL ERRORS` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata

Copy code

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ALL ERRORS;
```

##### Snowflake

Copy code

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ERRORS WITH NO LIMIT

In this example, notice that `LOGGING ERRORS WITH NO LIMIT` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata

Copy code

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH NO LIMIT;
```

##### Snowflake

Copy code

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ERRORS WITH LIMIT OF

In this example, notice that `LOGGING ERRORS WITH LIMIT OF` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata

Copy code

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH LIMIT OF 100;
```

##### Snowflake

Copy code

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## Select Statement

> See [Select statement](https://docs.teradata.com/reader/b8dd8xEYJnxfsq4uFRrHQQ/kH97CTRIXdd~i1yLemdvKw)

Snowflake supports Teradata’s `SELECT` syntax with a few exceptions. Primarily, it does not support the `SEL` abbreviation.​

**Teradata**

**Sel**

Copy code

```
SEL DISTINCT col1, col2 FROM table1
```

**Snowflake**

**Select**

Copy code

```
SELECT DISTINCT col1,
col2 FROM
table1;
```

Teradata supports referencing an alias before it is declared, but Snowflake does not. The transformation for this scenario is to take the referenced column and change the alias for the column name it references.

**Teradata**

**Alias**

Copy code

```
SELECT
my_val, sum(col1),
col2 AS my_val FROM table1
```

**Snowflake**

**Alias**

Copy code

```
SELECT
my_val,
SUM(col1),
col2 AS my_val FROM
table1;
```

### Removed clause options

The following clause options are not relevant to Snowflake, therefore they are removed during the migration.

| Teradata | Snowflake |
| --- | --- |
| Expand on | Unsupported |
| Normalize | Unsupported |
| With check option (Query) | Unsupported |

Expand

Show lessSee more

### Known Issues

#### 1. SEL abbreviation unsupported

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to SELECT.

### Related EWIs

No related EWIs.

## ANY Predicate

Warning

This is a work in progress, changes may be applied in the future.

### Description

In Teradata enables quantification in a comparison operation or IN/NOT IN predicate. The comparison of expression and at least one value in the set of values returned by subquery is true. Please review the following [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Logical-Predicates/ANY/ALL/SOME) for more information.

**Teradata syntax**

Copy code

```
 { expression quantifier ( literal [ {, | OR} ... ] ) |
  { expression | ( expression [,...] ) } quantifier ( subquery )
}
```

Where quantifier:

Copy code

```
 { comparison_operator [ NOT ] IN } { ALL |ANY | SOME }
```

**Snowflake syntax**

Note

:class: tip
In subquery form, IN is equivalent to `= ANY` and NOT IN is equivalent to `<> ALL`. Review the following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions/in) for more information.

To compare individual values:

Copy code

```
 <value> [ NOT ] IN ( <value_1> [ , <value_2> ...  ] )
```

To compare *row constructors* (parenthesized lists of values):

Copy code

```
 ( <value_A> [, <value_B> ... ] ) [ NOT ] IN (  ( <value_1> [ , <value_2> ... ] )  [ , ( <value_3> [ , <value_4> ... ] )  ...  ]  )
```

To compare a value to the values returned by a subquery:

Copy code

```
 <value> [ NOT ] IN ( <subquery> )
```

### Sample Source Patterns

#### Sample data

##### Teradata

##### Query

Copy code

```
 CREATE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "01/14/2025",  "domain": "test" }}'
;

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

#### Equal ANY predicate in WHERE clause

**Teradata**

##### Input

Copy code

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo = ANY(100,300,500) ;
```

##### Output

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

Expand

Show lessSee more

**Snowflake**

##### Input

Copy code

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

##### Output

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

Expand

Show lessSee more

#### Other comparison operators in WHERE clause

When there are other comparison operators, there equivalent translation is to add a subquery with the required logic.

**Teradata**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY(100,300,500) ;
```

##### Output

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

Expand

Show lessSee more

**Snowflake**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY
(SELECT DeptNo
FROM Employee
WHERE DeptNo > 100
OR DeptNo > 300
OR DeptNo > 500);
```

##### Output

| NAME | DEPTNO |
| --- | --- |
| Alice | 100 |
| Eve | 100 |
| Bob | 300 |
| David | 200 |

Expand

Show lessSee more

#### IN ANY in WHERE clause

**Teradata**

##### Input

Copy code

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN ANY(100,300,500) ;
```

##### Output

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

Expand

Show lessSee more

**Snowflake**

##### Input

Copy code

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

##### Output

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

Expand

Show lessSee more

#### NOT IN ALL in WHERE clause

**Teradata**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ALL(100, 200);
```

##### Output

| Name | DeptNo |
| --- | --- |
| Charlie | 500 |
| Bob | 300 |

Expand

Show lessSee more

**Snowflake**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN (100, 200);
```

##### Output

| Name | DeptNo |
| --- | --- |
| Charlie | 500 |
| Bob | 300 |

Expand

Show lessSee more

### Known Issues

#### NOT IN ANY in WHERE clause

**Teradata**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ANY(100, 200);
```

##### Output

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Charlie | 500 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

Expand

Show lessSee more

**Snowflake**

##### Input

Copy code

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo IN (100, 200)
   OR DeptNo NOT IN (100, 200);
```

##### Output

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Charlie | 500 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

Expand

Show lessSee more

### Related EWIs

No related EWIs.

## Expand On Clause

Translation reference to convert Teradata Expand On functionality to Snowflake

### Description

> The Expand On clause expands a column having a **period** data type, creating a regular time series of rows based on the period value in the input row. For more information about Expand On clause, see the [Teradata documentation](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/542VMPPqGwHBhF98pnTz9w).

### Sample Source Patterns

Note

Some parts in the output code are omitted for clarity reasons.

#### Sample data

##### Teradata

Copy code

```
 CREATE TABLE table1 (id INTEGER, pd PERIOD (TIMESTAMP));

INSERT INTO
    table1
VALUES
    (
        1,
        PERIOD(
            TIMESTAMP '2022-05-23 10:15:20.00009',
            TIMESTAMP '2022-05-23 10:15:25.000012'
        )
    );
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE table1 (
    id INTEGER,
    pd VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO table1
VALUES (
1, PUBLIC.PERIOD_UDF(
            TIMESTAMP '2022-05-23 10:15:20.00009',
            TIMESTAMP '2022-05-23 10:15:25.000012'
        ) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);
```

#### Expand On Clause

Suppose you want to expand the period column by seconds, for this Expand On clause has anchor period expansion and interval literal expansion.

##### Anchor Period Expansion

##### Teradata

Copy code

```
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY ANCHOR ANCHOR_SECOND;
```

##### Result

| id | BEGIN (bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |
| 1 | 2022-05-23 10:15:25.0000 |

Expand

Show lessSee more

Snowflake doesn’t support Expand On clause. To reproduce the same results and functionality, the Teradata SQL code will be contained in a CTE block, with an **EXPAND\_ON\_UDF** and **TABLE** function, using **FLATTEN** function to return multiple rows, **ROW\_COUNT\_UDF** and **DIFF\_TTIME\_PERIOD\_UDF** to indicate how many rows are needed and returning **VALUE** to help the EXPAND\_ON\_UDF to calculate the different regular time series. This CTE block returns the same expand columns alias as in the Expand On clause, so the result can be used in any usage of period datatype.

##### Snowflake

Copy code

```
 WITH ExpandOnCTE AS
(
    SELECT
        PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, pd) bg
    FROM
        table1,
        TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', pd))))
)
SELECT
    id,
    PUBLIC.PERIOD_BEGIN_UDF(bg) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
FROM
    table1,
    ExpandOnCTE;
```

##### Result

| id | PERIOD\_BEGIN\_UDF(bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |
| 1 | 2022-05-23 10:15:25.0000 |

Expand

Show lessSee more

### Known Issues

The Expand On clause can use interval literal expansion, for this case, an error will be added that this translation is planned.

#### Interval literal expansion

##### Teradata

Copy code

```
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

##### Result

| id | BEGIN(bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:20.0000 |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 SELECT
    id,
    PUBLIC.PERIOD_BEGIN_UDF(bg) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
FROM
    table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'EXPAND ON' NODE ***/!!!
EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

### Related EWIs

1. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-EWI-TD0053](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Normalize

Translation reference to convert Teradata Normalize functionality to Snowflake

### Description

> NORMALIZE specifies that period values in the first-period column that meet or overlap are combined to form a period that encompasses the individual period values. For more information about Normalize clause, see the [Teradata documentation](https://docs.teradata.com/r/2_MC9vCtAJRlKle2Rpb0mA/UuxiA0mklFgv~33X5nyKMA).

### Sample Source Patterns

Note

Some parts in the output code are omitted for clarity reasons.

#### Sample data

##### Teradata

Copy code

```
 CREATE TABLE project (
    emp_id INTEGER,
    project_name VARCHAR(20),
    dept_id INTEGER,
    duration PERIOD(DATE)
);

INSERT INTO project
VALUES
    (
        10,
        'First Phase',
        1000,
        PERIOD(DATE '2010-01-10', DATE '2010-03-20')
    );

INSERT INTO project
VALUES
    (
        10,
        'First Phase',
        2000,
        PERIOD(DATE '2010-03-20', DATE '2010-07-15')
    );

INSERT INTO project
VALUES
    (
        10,
        'Second Phase',
        2000,
        PERIOD(DATE '2010-06-15', DATE '2010-08-18')
    );

INSERT INTO project
VALUES
    (
        20,
        'First Phase',
        2000,
        PERIOD(DATE '2010-03-10', DATE '2010-07-20')
    );

INSERT INTO project
VALUES
    (
        20,
        'Second Phase',
        1000,
        PERIOD(DATE '2020-05-10', DATE '2020-09-20')
    );
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE project (
    emp_id INTEGER,
    project_name VARCHAR(20),
    dept_id INTEGER,
    duration VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO project
VALUES (
10,
        'First Phase',
        1000, PUBLIC.PERIOD_UDF(DATE '2010-01-10', DATE '2010-03-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
10,
        'First Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-03-20', DATE '2010-07-15') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
10,
        'Second Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-06-15', DATE '2010-08-18') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
20,
        'First Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-03-10', DATE '2010-07-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
20,
        'Second Phase',
        1000, PUBLIC.PERIOD_UDF(DATE '2020-05-10', DATE '2020-09-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);
```

#### Normalize Clause

Suppose you want to use Normalize clause with the employee id.

##### Teradata

Copy code

```
 SELECT
    NORMALIZE emp_id,
    duration
FROM
    project;
```

##### Result

| EMP\_ID | DURATION |
| --- | --- |
| 20 | (2010-03-10, 2010-07-20) |
| 10 | (2010-01-10, 2010-08-18) |
| 20 | (2020-05-10, 2010-09-20) |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TD0079 - THE REQUIRED PERIOD TYPE COLUMN WAS NOT FOUND ***/!!!
WITH NormalizeCTE AS
(
    SELECT
        T1.*,
        SUM(GroupStartFlag)
        OVER (
        PARTITION BY
            emp_id, duration
        ORDER BY
            PeriodColumn_begin
        ROWS UNBOUNDED PRECEDING) GroupID
    FROM
        (
            SELECT
                emp_id,
                duration,
                PUBLIC.PERIOD_BEGIN_UDF(PeriodColumn) PeriodColumn_begin,
                PUBLIC.PERIOD_END_UDF(PeriodColumn) PeriodColumn_end,
                (CASE
                    WHEN PeriodColumn_begin <= LAG(PeriodColumn_end)
                    OVER (
                    PARTITION BY
                        emp_id, duration
                    ORDER BY
                        PeriodColumn_begin,
                        PeriodColumn_end)
                        THEN 0
                    ELSE 1
                END) GroupStartFlag
            FROM
                project
        ) T1
)
SELECT
    emp_id,
    duration,
    PUBLIC.PERIOD_UDF(MIN(PeriodColumn_begin), MAX(PeriodColumn_end))
FROM
    NormalizeCTE
GROUP BY
    emp_id,
    duration,
    GroupID;
```

##### Result

| EMP\_ID | PUBLIC.PERIOD\_UDF(MIN(START\_DATE), MAX(END\_DATE)) |
| --- | --- |
| 20 | 2020-05-10\*2010-09-20 |
| 20 | 2010-03-10\*2010-07-20 |
| 10 | 2010-01-10\*2010-08-18 |

Expand

Show lessSee more

### Known Issues

Normalize clause can use **ON MEETS OR OVERLAPS**, **ON OVERLAPS** or **ON OVERLAPS OR MEETS,** for these cases an error will be added that this translation is planned for the future.

#### Teradata

Copy code

```
 SELECT NORMALIZE ON MEETS OR OVERLAPS emp_id, duration FROM table1;
```

##### Snowflake

Copy code

```
 SELECT
       !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NORMALIZE SET QUANTIFIER' NODE ***/!!!
       NORMALIZE ON MEETS OR OVERLAPS emp_id,
duration FROM
table1;
```

### Related EWIs

1. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-EWI-TD0079](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0079): The required period type column was not found.
3. [SSC-EWI-TD0053](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Reset When

### Description

> Reset When determines the partition on which an SQL window function operates based on some specific condition. If the condition evaluates to True, a new dynamic sub partition is created within the existing window partition. For more information about Reset When, see the [Teradata documentation](https://docs.teradata.com/reader/1DcoER_KpnGTfgPinRAFUw/b7wL86OoMTPno6hrSPNdDg).

### Sample Source Patterns

#### Sample data

##### Teradata

**Query**

Copy code

```
CREATE TABLE account_balance
(
  account_id INTEGER NOT NULL,
  month_id INTEGER,
  balance INTEGER
)
UNIQUE PRIMARY INDEX (account_id, month_id);

INSERT INTO account_balance VALUES (1, 1, 60);
INSERT INTO account_balance VALUES (1, 2, 99);
INSERT INTO account_balance VALUES (1, 3, 94);
INSERT INTO account_balance VALUES (1, 4, 90);
INSERT INTO account_balance VALUES (1, 5, 80);
INSERT INTO account_balance VALUES (1, 6, 88);
INSERT INTO account_balance VALUES (1, 7, 90);
INSERT INTO account_balance VALUES (1, 8, 92);
INSERT INTO account_balance VALUES (1, 9, 10);
INSERT INTO account_balance VALUES (1, 10, 60);
INSERT INTO account_balance VALUES (1, 11, 80);
INSERT INTO account_balance VALUES (1, 12, 10);
```

**Result**

| account\_id | month\_id | balance |
| --- | --- | --- |
| 1 | 1 | 60 |
| 1 | 2 | 99 |
| 1 | 3 | 94 |
| 1 | 4 | 90 |
| 1 | 5 | 80 |
| 1 | 6 | 88 |
| 1 | 7 | 90 |
| 1 | 8 | 92 |
| 1 | 9 | 10 |
| 1 | 10 | 60 |
| 1 | 11 | 80 |
| 1 | 12 | 10 |

Expand

Show lessSee more

##### Snowflake

**Query**

Copy code

```
CREATE OR REPLACE TABLE account_balance (
  account_id INTEGER NOT NULL,
  month_id INTEGER,
  balance INTEGER,
  UNIQUE (account_id, month_id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO account_balance
VALUES (1, 1, 60);

INSERT INTO account_balance
VALUES (1, 2, 99);

INSERT INTO account_balance
VALUES (1, 3, 94);

INSERT INTO account_balance
VALUES (1, 4, 90);

INSERT INTO account_balance
VALUES (1, 5, 80);

INSERT INTO account_balance
VALUES (1, 6, 88);

INSERT INTO account_balance
VALUES (1, 7, 90);

INSERT INTO account_balance
VALUES (1, 8, 92);

INSERT INTO account_balance
VALUES (1, 9, 10);

INSERT INTO account_balance
VALUES (1, 10, 60);

INSERT INTO account_balance
VALUES (1, 11, 80);

INSERT INTO account_balance
VALUES (1, 12, 10);
```

**Result**

| account\_id | month\_id | balance |
| --- | --- | --- |
| 1 | 1 | 60 |
| 1 | 2 | 99 |
| 1 | 3 | 94 |
| 1 | 4 | 90 |
| 1 | 5 | 80 |
| 1 | 6 | 88 |
| 1 | 7 | 90 |
| 1 | 8 | 92 |
| 1 | 9 | 10 |
| 1 | 10 | 60 |
| 1 | 11 | 80 |
| 1 | 12 | 10 |

Expand

Show lessSee more

#### Reset When

For each account, suppose you want to analyze the sequence of consecutive monthly balance increases. When the balance of one month is less than or equal to the balance of the previous month, the requirement is to reset the counter to zero and restart.

To analyze this data, Teradata SQL uses a window function with a nested aggregate and a Reset When statement, as follows:

##### Teradata

**Query**

Copy code

```
SELECT
   account_id,
   month_id,
   balance,
   (
     ROW_NUMBER() OVER (
       PARTITION BY account_id
       ORDER BY
         month_id RESET WHEN balance <= SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         )
     ) -1
   ) AS balance_increase
FROM account_balance
ORDER BY 1, 2;
```

**Result**

| account\_id | month\_id | balance | balance\_increase |
| --- | --- | --- | --- |
| 1 | 1 | 60 | 0 |
| 1 | 2 | 99 | 1 |
| 1 | 3 | 94 | 0 |
| 1 | 4 | 90 | 0 |
| 1 | 5 | 80 | 0 |
| 1 | 6 | 88 | 1 |
| 1 | 7 | 90 | 2 |
| 1 | 8 | 92 | 3 |
| 1 | 9 | 10 | 0 |
| 1 | 10 | 60 | 1 |
| 1 | 11 | 80 | 2 |
| 1 | 12 | 10 | 0 |

##### Snowflake

Snowflake does not support the Reset When clause in window functions. To reproduce the same result, the Teradata SQL code must be translated using native SQL syntax and nested subqueries, as follows:

**Query**

Copy code

```
SELECT
   account_id,
   month_id,
   balance,
   (
     ROW_NUMBER() OVER (
   PARTITION BY
      account_id, new_dynamic_part
   ORDER BY
         month_id
     ) -1
   ) AS balance_increase
FROM
   (
      SELECT
   account_id,
   month_id,
   balance,
   previous_value,
   SUM(dynamic_part) OVER (
           PARTITION BY account_id
           ORDER BY month_id
   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS new_dynamic_part
      FROM
   (
      SELECT
         account_id,
         month_id,
         balance,
         SUM(balance) OVER (
                 PARTITION BY account_id
                 ORDER BY month_id
                 ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
               ) AS previous_value,
         (CASE
            WHEN balance <= previous_value
               THEN 1
            ELSE 0
         END) AS dynamic_part
      FROM
         account_balance
   )
   )
ORDER BY 1, 2;
```

**Result**

| account\_id | month\_id | balance | balance\_increase |
| --- | --- | --- | --- |
| 1 | 1 | 60 | 0 |
| 1 | 2 | 99 | 1 |
| 1 | 3 | 94 | 0 |
| 1 | 4 | 90 | 0 |
| 1 | 5 | 80 | 0 |
| 1 | 6 | 88 | 1 |
| 1 | 7 | 90 | 2 |
| 1 | 8 | 92 | 3 |
| 1 | 9 | 10 | 0 |
| 1 | 10 | 60 | 1 |
| 1 | 11 | 80 | 2 |
| 1 | 12 | 10 | 0 |

Two nested sub-queries are needed to support the Reset When functionality in Snowflake.

In the inner sub-query, a dynamic partition indicator (dynamic\_part) is created and populated. dynamic\_part is set to 1 if one month’s balance is less than or equal to the preceding month’s balance; otherwise, it’s set to 0.

In the next layer, a new\_dynamic\_part attribute is generated as the result of a SUM window function.

Finally, a new\_dynamic\_part is added as a new partition attribute (dynamic partition) to the existing partition attribute (account\_id) and applies the same ROW\_NUMBER() window function as in Teradata.

After these changes, Snowflake generates the same output as Teradata.

#### Reset When when conditional window function is a column

Same example as above, except that now the window function used in the RESET WHEN condition is defined as a column called `previous`. This variation changes the transformation slightly since it is no longer necessary to define the `previous_value` as in the previous example. It is the same workaround.

##### Teradata

**Query**

Copy code

```
SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   (
     ROW_NUMBER() OVER (
       PARTITION BY account_id
       ORDER BY
         month_id RESET WHEN balance <= previous
     )
   ) AS balance_increase
FROM account_balance
ORDER BY 1, 2;
```

**Result**

| account\_id | month\_id | balance | previous | balance\_increase |
| --- | --- | --- | --- | --- |
| 1 | 1 | 60 |  | 0 |
| 1 | 2 | 99 | 60 | 1 |
| 1 | 3 | 94 | 99 | 0 |
| 1 | 4 | 90 | 94 | 0 |
| 1 | 5 | 80 | 90 | 0 |
| 1 | 6 | 88 | 80 | 1 |
| 1 | 7 | 90 | 88 | 2 |
| 1 | 8 | 92 | 90 | 3 |
| 1 | 9 | 10 | 92 | 0 |
| 1 | 10 | 60 | 10 | 1 |
| 1 | 11 | 80 | 60 | 2 |
| 1 | 12 | 10 | 80 | 0 |

##### Snowflake

**Query**

Copy code

```
SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   (
     ROW_NUMBER() OVER (
   PARTITION BY
      account_id, new_dynamic_part
   ORDER BY
         month_id
     )
   ) AS balance_increase
FROM
   (
      SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   SUM(dynamic_part) OVER (
           PARTITION BY account_id
           ORDER BY month_id
   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS new_dynamic_part
      FROM
   (
      SELECT
         account_id,
         month_id,
         balance,
         SUM(balance) OVER (
                 PARTITION BY account_id
                 ORDER BY month_id
                 ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
               ) AS previous,
         (CASE
            WHEN balance <= previous
               THEN 1
            ELSE 0
         END) AS dynamic_part
      FROM
         account_balance
   )
   )
ORDER BY 1, 2;
```

**Untitled**

| account\_id | month\_id | balance | previous | balance\_increase |
| --- | --- | --- | --- | --- |
| 1 | 1 | 60 |  | 0 |
| 1 | 2 | 99 | 60 | 1 |
| 1 | 3 | 94 | 99 | 0 |
| 1 | 4 | 90 | 94 | 0 |
| 1 | 5 | 80 | 90 | 0 |
| 1 | 6 | 88 | 80 | 1 |
| 1 | 7 | 90 | 88 | 2 |
| 1 | 8 | 92 | 90 | 3 |
| 1 | 9 | 10 | 92 | 0 |
| 1 | 10 | 60 | 10 | 1 |
| 1 | 11 | 80 | 60 | 2 |
| 1 | 12 | 10 | 80 | 0 |

### Known Issues

The RESET WHEN clause could have some variations such as its condition. Currently, only binary conditions (<=, >=, <> or =) are supported, in any other type, as `IS NOT NULL`, the RESET WHEN clause will be removed and an error message added since it is not supported in Snowflake, as shown in the following example.

#### Teradata

**Query**

Copy code

```
SELECT
    account_id,
    month_id,
    balance,
    ROW_NUMBER() OVER (
        PARTITION BY account_id
        ORDER BY month_id
        RESET WHEN balance IS NOT NULL
        ROWS UNBOUNDED PRECEDING
    ) as balance_increase
FROM account_balance
ORDER BY 1,2;
```

#### Snowflake

**Query**

Copy code

```
SELECT
    account_id,
    month_id,
    balance,
    ROW_NUMBER() OVER (
        PARTITION BY account_id
    !!!RESOLVE EWI!!! /*** SSC-EWI-TD0077 - RESET WHEN CLAUSE IS NOT SUPPORTED IN THIS SCENARIO DUE TO ITS CONDITION ***/!!!
        ORDER BY month_id
        ROWS UNBOUNDED PRECEDING
    ) as balance_increase
FROM
    account_balance
ORDER BY 1,2;
```

### Related EWIs

- [SSC-EWI-TD0077](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0077): RESET WHEN clause is not supported in this scenario due to its condition.

## SAMPLE clause

### Description

The SAMPLE clause in Teradata reduces the number of rows to be processed and it returns one or more samples of rows as a list of fractions or as a list of numbers of rows. The clause is used in the SELECT query. Please review the following [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/SELECT-Statements/SAMPLE-Clause) for more information.

**Teradata syntax**

Copy code

```
SAMPLE
  [ WITH REPLACEMENT ]
  [ RANDOMIZED LOCALIZATION ]
  { { fraction_description | count_description } [,...] |
    when_clause ]
  }
```

**Snowflake syntax**

Review the following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/constructs/sample) for more information. `SAMPLE` and `TABLESAMPLE` are synonymous.

Copy code

```
SELECT ...
FROM ...
  { SAMPLE | TABLESAMPLE } [ samplingMethod ]
[ ... ]
```

Where:

Copy code

```
samplingMethod ::= {
{ BERNOULLI | ROW } ( { <probability> | <num> ROWS } ) |
{ SYSTEM | BLOCK } ( <probability> ) [ { REPEATABLE | SEED } ( <seed> ) ] }
```

- In Snowflake, the following keywords can be used interchangeably:

  > - `SAMPLE | TABLESAMPLE`
  > - `BERNOULLI | ROW`
  > - `SYSTEM | BLOCK`
  > - `REPEATABLE | SEED`

Review the following table to check on key differences.

| SAMPLE behavior | Teradata | Snowflake |
| --- | --- | --- |
| Sample by probability | Also known as fraction description. It must be a fractional number between 0,1 and 1. | Decimal number between 0 and 100. |
| Fixed number of rows | Also known as count description. It is a positive integer that determines the number of rows to be sampled. | It specifies the number of rows (up to 1,000,000) to sample from the table. Can be any integer between `0` (no rows selected) and `1000000` inclusive. |
| Repeated rows | It is known as `WITH REPLACEMENT.` This is used to query more samples than there are rows in the table. | It is known as `REPEATABLE` or `SEED`. This is used to make the query deterministic. It means that the same set of rows will be the same for each query run. |
| Sampling methods | *Proportional* and `RANDOMIZED ALLOCATION.` | `BERNOULLI` or `SYSTEM`. |

Expand

Show lessSee more

### Sample Source Patterns

#### Sample data

##### Teradata

**Query**

Copy code

```
CREATE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

##### Snowflake

**Query**

Copy code

```
CREATE OR REPLACE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "01/14/2025",  "domain": "test" }}'
;

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

#### SAMPLE clause

##### Fixed number of rows

Notice that for this example, the number of rows are a fixed number but not necessarily are the same result for each run.

**Teradata**

**Input**

Copy code

```
SELECT * FROM Employee SAMPLE 2;
```

**Output**
2 rows.

**Snowflake**

**Input**

Copy code

```
SELECT * FROM Employee SAMPLE (2 ROWS);
```

**Output**
2 rows.

##### Rows number based on probability

This option will return a variety of rows depending on the probability set.

**Teradata**

**Input**

Copy code

```
SELECT * FROM Employee SAMPLE 0.25;
```

**Output**
25% of probability for each row: 1 output row.

**Snowflake**

**Input**

Copy code

```
SELECT * FROM Employee SAMPLE (25);
```

**Output**
25% of probability for each row: 1 output row.

### Known Issues

#### Fixed number of rows with replacement

This option will return a fixed number of rows and will allows the repetition of the rows. In Snowflake, it is not possible to request more samples than rows in a table.

**Teradata sample**

**Input**

Copy code

```
SELECT * FROM Employee SAMPLE WITH REPLACEMENT 8;
```

**Output**

| EmpNo | Name | DeptNo |
| --- | --- | --- |
| 5 | Eve | 100 |
| 5 | Eve | 100 |
| 5 | Eve | 100 |
| 4 | David | 200 |
| 4 | David | 200 |
| 3 | Charlie | 500 |
| 1 | Alice | 100 |
| 1 | Alice | 100 |

Expand

Show lessSee more

#### SAMPLEID related functionality

In Teradata, it is possible to assign a unique ID to each sample that is specified. It helps to identify which belongs to which sample. This is not ANSI grammar, instead it is an extension of Teradata.

**Teradata sample**

**Input**

Copy code

```
SELECT name, SAMPLEID FROM employee SAMPLE 0.5, 0.25, 0.25;
```

**Output**

| Name | SampleId |
| --- | --- |
| Eve | 3 |
| Charlie | 1 |
| Alice | 1 |
| David | 2 |
| Bob | 1 |

Expand

Show lessSee more

In Snowflake, there is not a SAMPLEID function. A possible workaround may be the following, but it has to be adapted to each single case:

**Snowflake possible workaround**

**Input**

Copy code

```
WITH sampled_data AS (
    -- Sample 100% of the rows from the Employee table
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY EmpNo) AS row_num,
           COUNT(*) OVER () AS total_rows  -- Get the total row count to calculate sample size
    FROM Employee
)
SELECT Name,
       CASE
           -- First 50% of the rows
           WHEN row_num <= total_rows * 0.5 THEN 1
           -- Next 25% of the rows
           WHEN row_num <= total_rows * 0.75 THEN 2
           -- Remaining 25% of the rows
           ELSE 3
       END AS sample_id
FROM sampled_data
ORDER BY sample_id, row_num;  -- Order by sample_id and row_num for consistency
```

**Output**

| Name | SAMPLE\_ID |
| --- | --- |
| Alice | 1 |
| Bob | 1 |
| Charlie | 2 |
| David | 3 |
| Eve | 3 |

Expand

Show lessSee more

#### Conditional sampling

In Snowflake there is not conditional sampling. This can be achieve by using CTE’s.

**Teradata sample**

**Input**

Copy code

```
SELECT * FROM employee
SAMPLE WHEN DeptNo > 100 then 0.9
ELSE 0.1 END;
```

**Output**

| EmpNo | Name | DeptNo |
| --- | --- | --- |
| 3 | Charlie | 500 |
| 4 | David | 200 |
| 2 | Bob | 300 |

Expand

Show lessSee more

### Related EWIs

[SSC-EWI-0021](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0021): Syntax not supported in Snowflake.

## Column-level FORMAT Clause in DML Statements

Translation reference for how Teradata column FORMAT clauses affect DML statement conversion to Snowflake.

### Description

In Teradata, the `FORMAT` clause on a column definition controls how date, timestamp, and time values are parsed from string literals. For example, if a column is defined as `DATE FORMAT 'MM-DD-YYYY'`, writing `WHERE hire_date = '03-30-2026'` means Teradata reads the string using that format.

Snowflake does not have this feature. To preserve the same behavior:

1. The `FORMAT` clause is **commented out** in the `CREATE TABLE` output (see [DDL reference](ddl-teradata)).
2. **Conversion functions** (`TO_DATE`, `TO_TIMESTAMP`, or `TO_TIME`) are **added** around string literals in DML statements that reference the formatted column, using the equivalent Snowflake format string.

Note

When the FORMAT matches Snowflake’s default output format for the column type (`'YYYY-MM-DD'` for `DATE`, `'HH:MI:SS'` for `TIME`, `'YYYY-MM-DDBHH:MI:SS'` for `TIMESTAMP`), the FORMAT clause is **silently removed** from the DDL and no conversion functions are added to DML statements. These formats are natively handled by Snowflake. The conversion functions described below only apply to non-standard formats.

Important

For this to work, the `CREATE TABLE` that defines the `FORMAT` clause **must be included** in the conversion input. The FORMAT value and column type are read from the `CREATE TABLE` statement and stored internally so that DML statements referencing those columns can be converted correctly. If the `CREATE TABLE` is missing, the conversion functions will not be added. Always verify that the converted code behaves correctly when FORMAT clauses are present.

### Supported DML Contexts

The following contexts are handled when the target column has a translatable datetime FORMAT:

| Context | Teradata Pattern | Snowflake Result |
| --- | --- | --- |
| WHERE equality | `WHERE col = '03-30-2026'` | `WHERE col = TO_DATE('03-30-2026', 'MM-DD-YYYY')` |
| WHERE comparison | `WHERE col > '01-01-2026'` | `WHERE col > TO_DATE('01-01-2026', 'MM-DD-YYYY')` |
| WHERE BETWEEN | `WHERE col BETWEEN '...' AND '...'` | Both bounds converted |
| WHERE IN | `WHERE col IN ('...', '...')` | All values converted |
| INSERT VALUES | `VALUES ('03-30-2026')` | `VALUES (TO_DATE('03-30-2026', 'MM-DD-YYYY'))` |
| UPDATE SET | `SET col = '03-30-2026'` | `SET col = TO_DATE('03-30-2026', 'MM-DD-YYYY')` |
| MERGE UPDATE | `UPDATE SET col = '...'` | Conversion function added |
| MERGE INSERT | `INSERT (col) VALUES ('...')` | Conversion function added |
| JOIN ON | `ON col = '03-30-2026'` | `ON col = TO_DATE('03-30-2026', 'MM-DD-YYYY')` |

Expand

Show lessSee more

### Sample Source Patterns

#### WHERE Equality with Date FORMAT

**Teradata**

Copy code

```
CREATE TABLE employee (
  id INTEGER,
  hire_date DATE FORMAT 'MM-DD-YYYY'
);

SELECT * FROM employee WHERE hire_date = '03-30-2026';
```

**Snowflake**

Copy code

```
CREATE OR REPLACE TABLE employee (
  id INTEGER,
  hire_date DATE
--                 --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'MM-DD-YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                 FORMAT 'MM-DD-YYYY'
)
;

SELECT
  *
FROM
  employee
WHERE
  hire_date = TO_DATE('03-30-2026', 'MM-DD-YYYY');
```

#### WHERE with TIME FORMAT

**Teradata**

Copy code

```
CREATE TABLE shift_log (
  id INTEGER,
  shift_start TIME FORMAT 'HH.MI.SS'
);

SELECT * FROM shift_log WHERE shift_start = '08.30.00';
```

**Snowflake**

Copy code

```
CREATE OR REPLACE TABLE shift_log (
  id INTEGER,
  shift_start TIME
--                   --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'HH.MI.SS' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                   FORMAT 'HH.MI.SS'
)
;

SELECT
  *
FROM
  shift_log
WHERE
  shift_start = TO_TIME('08.30.00', 'HH.MI.SS');
```

#### JOIN ON with Date FORMAT

**Teradata**

Copy code

```
CREATE TABLE event_log (
  id INTEGER,
  event_date DATE FORMAT 'MM-DD-YYYY'
);

CREATE TABLE event_source (
  id INTEGER
);

SELECT * FROM event_log e JOIN event_source s ON e.event_date = '03-30-2026' AND e.id = s.id;
```

**Snowflake**

Copy code

```
CREATE OR REPLACE TABLE event_log (
  id INTEGER,
  event_date DATE
--                  --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'MM-DD-YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                  FORMAT 'MM-DD-YYYY'
)
;

CREATE OR REPLACE TABLE event_source (
  id INTEGER
)
;

SELECT
  *
FROM
  event_log e
  JOIN event_source s
    ON e.event_date = TO_DATE('03-30-2026', 'MM-DD-YYYY')
    AND e.id = s.id;
```

### Best Practices

- Always include the `CREATE TABLE` statements that define `FORMAT` clauses in the conversion input. Without them, conversion functions cannot be added to DML statements.
- After conversion, verify that the converted code behaves correctly when these formats are present, especially for edge cases such as `INSERT ... SELECT` statements or columns with untranslatable format strings.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

1. [SSC-FDM-TD0040](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0040): Column-level FORMAT clause is not supported in Snowflake. Conversion functions are used in DML statements as a workaround.
2. [SSC-FDM-TD0041](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0041): Column-level display-only FORMAT clause is not supported in Snowflake. No action needed.
3. [SSC-EWI-TD0040](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0040): Column-level FORMAT clause cannot be automatically converted to Snowflake.
