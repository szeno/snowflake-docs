# Code Conversion - IBM DB2 Issues

## SSC-EWI-DB0001

WITH ROW ACCESS POLICY CLAUSE DOES NOT SUPPORT MULTIPLE DECLARATION

### Severity

Low

### Description

This message is shown whenever multiple security label column options are detected inside the same `CREATE TABLE` clause, the security label is translated to a row access policy clause and Snowflake does not support multiple row access policy declarations. Therefore, if more than one security labels are found they will be commented out with this EWI.

#### Code example

##### Input code:

Copy code

```
 CREATE TABLE T1
(
COL1 VARCHAR(10) COLUMN SECURED WITH securityLabel1,
COL2 VARCHAR(10) COLUMN SECURED WITH securityLabel2
);
```

##### Output code:

Copy code

```
CREATE TABLE T1
(
COL1 VARCHAR(10),
COL2 VARCHAR(10)
)
WITH ROW ACCESS POLICY securityLabel1 ON (
COL1
)
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0001 - WITH ROW ACCESS POLICY CLAUSE DOES NOT SUPPORT MULTIPLE DECLARATION IN SNOWFLAKE ***/!!!
WITH ROW ACCESS POLICY securityLabel2 ON (
COL2
)
;
```

### Recommendations

- Review your code and ensure that only one security label is inside the `CREATE TABLE` clause
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0003

PERIOD DEFINITION IS NOT SUPPORTED IN SNOWFLAKE.

### Severity

Medium

### Description

DB2 temporal tables do not have a functional equivalent in Snowflake. When an application-period or system-period temporal table declaration is found in the `CREATE TABLE` columns, that column is commented out from the resulting script. The behavior of the SELECT statement will differ from Snowflake because temporal tables are not part of the Snowflake solution and this causes the result to be different if the Select statement is migrated partially, see the example below for more information about this.

#### Select Query

Copy code

```
 SELECT
  ID,
  Start,
  END
FROM
  timetable
FOR system_time as of '2022-05-09-16.20.17.0';
```

##### Result

| ID | START | END |
| --- | --- | --- |
| 1001 | 19:45.3 | 22:39.5 |
| 1002 | 19:45.5 | 22:39.6 |
| 1003 | 19:45.6 | 22:39.8 |
| 1004 | 19:45.7 | 00:00.0 |
| 1005 | 19:45.8 | 00:00.0 |
| 1006 | 19:46.0 | 00:00.0 |
| 7 | 16:21.8 | 00:00.0 |

Expand

Show lessSee more

If the Select statement is migrated partially we get a very different result as shown below.

##### Select Query

Copy code

```
 SELECT
  ID,
  Start,
  END
FROM
  timetable
-- FOR system_time as of '2022-05-09-16.20.17.0';
```

##### Result

|  |  |  |
| --- | --- | --- |
| ID | START | END |
| 2001 | 22:39.5 | 00:00.0 |
| 2002 | 22:39.6 | 00:00.0 |
| 2003 | 22:39.8 | 00:00.0 |
| 1004 | 19:45.7 | 00:00.0 |
| 1005 | 19:45.8 | 00:00.0 |
| 1006 | 19:46.0 | 00:00.0 |
| 7 | 16:21.8 | 00:00.0 |

Expand

Show lessSee more

#### Code example

##### DB2

##### Create table

Copy code

```
CREATE TABLE TestTable (
COL1 DATE,
COL2 DATE,
PERIOD SYSTEM_TIME (COL1, COL2),
PERIOD BUSINESS_TIME (COL1, COL2)
```

##### Select Query

Copy code

```
SELECT
   *
FROM
   Table1
FOR SYSTEM_TIME AS of Value
```

##### Snowflake

##### Create Table

Copy code

```
CREATE TABLE TestTable (
COL1 DATE,
COL2 DATE,
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
PERIOD SYSTEM_TIME (COL1, COL2),
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
PERIOD BUSINESS_TIME (COL1, COL2)
)
```

##### Select Query

Copy code

```
SELECT
   *
FROM
Table1
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
FOR SYSTEM_TIME AS of Value
```

### Recommendations

- Snowflake allows the storage of historical table data for up to 90 days, to know more about this see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel.html).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0004

OUTER TABLE REFERENCE NOT APPLICABLE IN SNOWFLAKE

### Severity

Low

### Description

This message is shown when an OUTER table reference is found in a FROM clause inside of a SELECT statement. This clause is used to include from subtables in the intermediate result table of the SELECT statement. Subtables are related to [typed tables](https://www.ibm.com/docs/en/db2/9.7?topic=tables-creating-typed) in the DB2 database, that are created with the [OF clause](https://docs.mobilize.net/snowconvert-limited-access/-MUuBuIkrrZbtDaKcru_/for-ibm-db2/translation-reference/statements/create-table/content-source/of-type) of the CREATE TABLE statement, which is also not supported in Snowflake.

#### Code example

##### Input code:

Copy code

```
Select * from OUTER(ATable);
Select * from ONLY(ATable);
```

##### Output code:

Copy code

```
Select * from
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0004 - OUTER TABLE REFERENCE IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
OUTER(ATable) AS AliasName;

Select * from
ATable;
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0005

MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED

### Severity

Medium

### Description

This message is shown when it is found in a CREATE VIEW a node or clause that is related to the data manipulation of rows in a CREATE VIEW. Note that in DB2 you can insert or update rows directly from a VIEW meanwhile in Snowflake this is not supported, because of this, nodes or clauses related to this functionality are commented and an EWI is added.

#### Code example

##### Input code:

Copy code

```
CREATE VIEW TestTableId2 AS Select * from TestTableId1 WITH ROW MOVEMENT;
```

##### Output code:

Copy code

```
 CREATE VIEW TestTableId2
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/02/2025",  "domain": "no-domain-provided" }}'
 AS Select * from
  TestTableId1
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0005 - MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED. ***/!!!
 WITH ROW MOVEMENT;
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0006

INTERMEDIATE RESULT TABLE IS NOT SUPPORTED

### Severity

Medium

### Description

This message is shown when a DATA CHANGE TABLE REFERENCE is found in a FROM Clause. A DATA CHANGE TABLE REFERENCE specifies an intermediate table, which consists of the rows that are changed by an UPDATE, DELETE or INSERT statement included in the DATA CHANGE TABLE REFERENCE.

In Snowflake, this is not supported, since it can’t modify the rows and return a result set of table at the same time, hence the Select is commented.

#### Code example

##### DB2 Input code:

##### Select statement

Copy code

```
 SELECT
   *
FROM
   OLD Table(UPDATE T1 SET NAME = 'Tony' where ID = 4)
```

##### Update statement

Copy code

```
 UPDATE (SELECT EMPNO, SALARY, COMM,
     AVG(SALARY) OVER (PARTITION BY WORKDEPT),
     AVG(COMM) OVER (PARTITION BY WORKDEPT)
     FROM EMPLOYEE E) AS E(EMPNO, SALARY, COMM, AVGSAL, AVGCOMM)
   SET (SALARY, COMM) = (AVGSAL, AVGCOMM)
   WHERE EMPNO = '000120';

 UPDATE TABLE5
INCLUDE (col1 INT, col2 Varchar(10))
SET Column1 = 1;
```

##### Snowflake Output code:

##### Select statement

Copy code

```
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0006 - INTERMEDIATE RESULT TABLE IS NOT SUPPORTED. ***/!!!
   OLD Table(UPDATE T1 SET NAME = 'Tony' where ID = 4)
```

##### Update statement

Copy code

```
UPDATE
       !!!RESOLVE EWI!!! /*** SSC-EWI-DB0006 - INTERMEDIATE RESULT TABLE IS NOT SUPPORTED. ***/!!!
 (SELECT EMPNO, SALARY, COMM,
       AVG(SALARY) OVER (PARTITION BY WORKDEPT),
       AVG(COMM) OVER (PARTITION BY WORKDEPT)
       FROM EMPLOYEE E) AS E(EMPNO, SALARY, COMM, AVGSAL, AVGCOMM)
       SET
       SALARY = AVGSAL,
       COMM = AVGCOMM
WHERE EMPNO = '000120';

UPDATE TABLE5
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0006 - INTERMEDIATE RESULT TABLE IS NOT SUPPORTED. ***/!!!
INCLUDE (col1 INT, col2 Varchar(10))
SET Column1 = 1;
```

#### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0007

QUERY AS INSERT TARGET NAME IS NOT SUPPORTED.

### Severity

Medium

### Description

Unlike DB2, Snowflake does not allow using SELECT query results as the target of an INSERT statement, requiring instead that data be inserted directly into tables or materialized views.

#### Code example

##### DB2

##### Query

Copy code

```
 INSERT INTO
   (SELECT * FROM SOMEOTHERTABLE)
VALUES
   (DEFAULT);
```

##### Snowflake

##### Query

Copy code

```
 INSERT INTO
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0007 - QUERY AS INSERT TARGET NAME IS NOT SUPPORTED ***/!!!
   (SELECT * FROM SOMEOTHERTABLE)
VALUES
   (DEFAULT);
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0008

DELETE FROM SELECT STATEMENT IS NOT SUPPORTED.

### Severity

Medium

### Description

Snowflake does not support the use of select queries in the From clause of a Delete statement. If the Delete statement is migrated partially we get an incomplete statement as the From clause will be empty.

#### Code example

##### DB2

##### Select Query

Copy code

```
 DELETE FROM (
SELECT * FROM table1
)
```

##### Snowflake

##### Select Query

Copy code

```
DELETE FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0008 - DELETE FROM SELECT STATEMENT IS NOT SUPPORTED. ***/!!!
 (
SELECT * FROM table1
)
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0009

POSITIONED STATEMENT IS NOT SUPPORTED.

### Severity

Medium

### Description

Snowflake does not support the use of cursors as part of the Delete statement and Update statement. If the statement is migrated partially, we will get rid of the where clause in which the cursor is forming part, making it dangerous to delete or update the whole table.

#### Code example

##### DB2

##### Delete statement

Copy code

```
 DELETE FROM table1
WHERE CURRENT OF cursor1
```

##### Update statement

Copy code

```
 UPDATE table1
     SET col1 = 1
     WHERE CURRENT OF cursor1
```

##### Snowflake

##### Delete statement

Copy code

```
DELETE FROM
table1
WHERE
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0009 - POSITIONED CURRENT OF IS NOT SUPPORTED. ***/!!! CURRENT OF cursor1
```

##### Update statement

Copy code

```
UPDATE TABLE1
SET Column1 = 1
WHERE
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0009 - POSITIONED CURRENT OF IS NOT SUPPORTED. ***/!!!
 CURRENT OF cursor1;
```

### Recommendations

- For additional support, contact SnowConvert support at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-DB0010

ATTRIBUTE NAME IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Medium

### Description

This message is displayed when specifying the attribute of a structured type that is being set (called an attribute assignment). A structured type can be a subtype that allows attributes to be inherited from a supertype.

Snowflake does not support these types of structures.

For more information, see the [DB2 CREATE TYPE (structured) documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-type-structured).

#### Code Example

##### DB2

Copy code

```
 UPDATE CIRCLES
     SET C..CENTER..X = C..CENTER..Y,
       C..CENTER..Y = C..CENTER..X
     WHERE ID = 999;
```

##### Snowflake

Copy code

```
UPDATE CIRCLES
     SET
          !!!RESOLVE EWI!!! /*** SSC-EWI-DB0010 - ATTRIBUTE NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!! C..CENTER..X =
          !!!RESOLVE EWI!!! /*** SSC-EWI-DB0010 - ATTRIBUTE NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!! C..CENTER..Y,
          !!!RESOLVE EWI!!! /*** SSC-EWI-DB0010 - ATTRIBUTE NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
       C..CENTER..Y =
                      !!!RESOLVE EWI!!! /*** SSC-EWI-DB0010 - ATTRIBUTE NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!! C..CENTER..X
     WHERE ID = 999
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0011

ASSIGNMENT CLAUSE TYPE IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Medium

### Description

This message is displayed when the assignment clause contains an expression not supported by Snowflake

### Cases

#### Update Statement

When an assignment clause presents a multi-column assignment of a row selection, an example of this can be found in the Code example section.

#### Code Example

##### DB2

Copy code

```
 UPDATE EMPLOYEE EU
    SET (EU.COM, EU.SALARY) = (SELECT ES.SALARY FROM EMPLOYEE ES WHERE ES.WORKDEPT = EU.WORKDEPT)
    WHERE EU.EMPNO = '000120';
```

##### Snowflake

Copy code

```
UPDATE EMPLOYEE EU
    SET
        !!!RESOLVE EWI!!! /*** SSC-EWI-DB0011 - ASSIGNMENT CLAUSE TYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
 (EU.COM, EU.SALARY) = (SELECT ES.SALARY FROM
         EMPLOYEE ES WHERE ES.WORKDEPT = EU.WORKDEPT)
    WHERE EU.EMPNO = '000120';
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0012

INVALID NAME AS INSERTION TARGET, USE OF VIEW NAME IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Medium

### Description

Snowflake does not support the use of view name in the insert target name statement.

#### Code Example

##### DB2

Copy code

```
 CREATE VIEW VIEW1 AS SELECT * FROM T;
INSERT INTO VIEW1 (COL1, COL2) VALUES (NULL, DEFAULT);
```

##### Snowflake

Copy code

```
 CREATE VIEW PUBLIC.VIEW1
AS SELECT * FROM
PUBLIC.T;

!!!RESOLVE EWI!!! /*** SSC-EWI-DB0012 - INVALID NAME AS INSERTION TARGET, USE OF VIEW NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INSERT INTO VIEW1 (COL1, COL2) VALUES (NULL,DEFAULT);
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0013

INVALID NAME AS DELETE TARGET, USE OF VIEW NAME IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Medium

### Description

Snowflake does not support the use of view name in the delete target name statement. For this reason, the result query could not be valid

#### Code Example

##### DB2

Copy code

```
 CREATE VIEW VIEW1 AS SELECT * FROM T;
DELETE FROM VIEW1
```

##### Snowflake

Copy code

```
 CREATE VIEW PUBLIC.VIEW1
AS SELECT * FROM
PUBLIC.T;

DELETE FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0013 - INVALID NAME AS DELETE TARGET, USE OF VIEW NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
 VIEW1
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0014

THE USE OF EXTERNAL TABLE REFERENCES IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Medium

### Description

Snowflake does not support the use of external tables in the Select statement. For this reason, the result query could not be valid

#### Code Example

##### DB2

Copy code

```
 SELECT
   *
FROM
   EXTERNAL SOMENAME AS T1 LIKE TABLE2 USING(COMPRESS NO)
```

##### Snowflake

Copy code

```
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0014 - THE USE OF EXTERNAL TABLE REFERENCES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
   EXTERNAL SOMENAME AS T1 LIKE TABLE2 USING(COMPRESS NO)
```

### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0015

The use of Create View Of Type is not supported in Snowflake

### Severity

High

### Description

This message is shown when a `CREATE VIEW` statement that uses the `OF type` clause is detected. In DB2, typed views are created with the `OF type MODE DB2SQL` syntax and are based on structured types for object-relational modeling. Snowflake does not support typed views or structured types, so the view definition is marked with this EWI and marked as invalid.

#### Code Example

##### DB2

Copy code

```
CREATE VIEW testView
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM testTable;
```

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0015 - CREATE VIEW OF TYPE IS NOT SUPPORTED ***/!!!
CREATE VIEW testView
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM testTable;
```

### Recommendations

- Refactor the typed view into a standard view or materialized view that selects from the underlying table(s)
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0016

The use of Unnest Function is not supported in Snowflake

### Severity

High

### Description

This message is shown when the `UNNEST` or `TABLE` function in a `FROM` clause is detected. In DB2, these table functions expand arrays or collections into rows (optionally with `WITH ORDINALITY` for row numbering). Snowflake has different syntax and semantics for array unnesting—`FLATTEN` is the equivalent—so the DB2 `UNNEST`/`TABLE` usage is marked as not supported.

#### Code Example

##### DB2

Copy code

```
SELECT
   *
FROM
   UNNEST(arrray) WITH ORDINALITY
```

##### Snowflake

Copy code

```
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0016 - UNNEST FUNCTION IS NOT SUPPORTED ***/!!!
   UNNEST(arrray) WITH ORDINALITY;
```

### Recommendations

- Replace DB2 `UNNEST` or `TABLE` with Snowflake `FLATTEN` to expand arrays into rows. Use `FLATTEN(input => array_column)` with appropriate column references
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0017

The use of Typed Tables is not supported in Snowflake

### Severity

High

### Description

This message is shown when a `CREATE TABLE` statement that uses the `OF type` or `UNDER` clause is detected. In DB2, typed tables are defined with a structured type hierarchy (e.g., `OF Student_t UNDER Person`) and support inheritance. Snowflake does not support typed tables or structured types, so the table definition is marked with this EWI.

#### Code Example

##### DB2

Copy code

```
CREATE TABLE Student OF Student_t UNDER Person
INHERIT SELECT PRIVILEGES;
```

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0017 - TYPED TABLES ARE NOT SUPPORTED ***/!!!
CREATE TABLE Student OF Student_t UNDER Person
INHERIT SELECT PRIVILEGES;
```

### Recommendations

- Refactor typed tables into standard tables. Model the type hierarchy with separate tables and foreign keys if inheritance relationships need to be preserved
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0018

The use of Staging Tables is not supported in Snowflake

### Severity

High

### Description

This message is shown when a `CREATE TABLE` statement that defines a staging table using the `FOR` clause (e.g., `CREATE TABLE emp_summary_s FOR emp_summary PROPAGATE IMMEDIATE`) is detected. In DB2, staging tables are used for materialized query table propagation. Snowflake does not support this construct, so the table definition is marked with this EWI.

#### Code Example

##### DB2

Copy code

```
CREATE TABLE emp_summary_s FOR emp_summary PROPAGATE IMMEDIATE;
```

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0018 - STAGING TABLES ARE NOT SUPPORTED ***/!!!
CREATE TABLE emp_summary_s FOR emp_summary PROPAGATE IMMEDIATE;
```

### Recommendations

- Use Snowflake streams and tasks, or materialized views with refresh logic, to achieve similar incremental propagation behavior
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0019

The use of Analyze Table Factor is not supported in Snowflake

### Severity

Low

### Description

This message is shown when an `ANALYZE_TABLE` table factor in a `FROM` clause is detected. In DB2, `ANALYZE_TABLE` invokes external analytics (e.g., SAS routines) inline in a query. Snowflake does not support this DB2-specific analytics integration, so the table reference is marked with this EWI.

#### Code Example

##### DB2

Copy code

```
SELECT
   *
FROM v1 ANALYZE_TABLE(
   IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;')
ORDER BY 1;
```

##### Snowflake

Copy code

```
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0019 - ANALYZE TABLE FACTOR IS NOT SUPPORTED ***/!!!
   v1 ANALYZE_TABLE(
   IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;')
ORDER BY 1;
```

### Recommendations

- Implement the analytics logic in Snowflake using Snowpark (Python/Java), stored procedures, or external functions, and restructure the query accordingly
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0020

The use of Data Capture is not supported in Snowflake

### Severity

High

### Description

This message is shown when the `DATA CAPTURE CHANGES` (or `DATA CAPTURE NONE`) clause in a `CREATE TABLE` statement is detected. In DB2, this clause controls whether changed data is captured for replication (e.g., Q Replication). Snowflake does not support this DB2-specific clause, so it is marked with this EWI.

#### Code Example

##### DB2

Copy code

```
CREATE TABLE TestTable
(
   COL1 INT
) DATA CAPTURE CHANGES;
```

##### Snowflake

Copy code

```
CREATE TABLE TestTable
(
   COL1 INT
)
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0020 - DATA CAPTURE IS NOT SUPPORTED ***/!!!
 DATA CAPTURE CHANGES
;
```

### Recommendations

- For change data capture in Snowflake, use [Streams](https://docs.snowflake.com/en/user-guide/streams-intro) to track changes on tables
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0021

The use of Materialized Query is not supported in Snowflake

### Severity

Low

### Description

This message is shown when a `CREATE TABLE ... AS` statement with materialized query options such as `DATA INITIALLY DEFERRED`, `REFRESH DEFERRED`, `MAINTAINED BY SYSTEM`, or `ENABLE QUERY OPTIMIZATION` is detected. In DB2, these options define a refreshable materialized query table. Snowflake materialized views use different syntax and semantics, so these options are marked with this EWI.

#### Code Example

##### DB2

Copy code

```
CREATE TABLE TRANSCNT (ACCTID, LOCID, YEAR, CNT) AS
  (SELECT ACCOUNTID, LOCATIONID, YEAR, COUNT(*)
     FROM TRANS
     GROUP BY ACCOUNTID, LOCATIONID, YEAR )
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION;
```

##### Snowflake

Copy code

```
CREATE TABLE TRANSCNT (ACCTID, LOCID, YEAR, CNT) AS
  (SELECT ACCOUNTID, LOCATIONID, YEAR, COUNT(*)
     FROM TRANS
     GROUP BY ACCOUNTID, LOCATIONID, YEAR )
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0021 - MATERIALIZED QUERY IS NOT SUPPORTED ***/!!!
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION
;
```

### Recommendations

- Convert to a Snowflake [materialized view](https://docs.snowflake.com/en/user-guide/views-materialized) if you need automatic refresh. Use `CREATE MATERIALIZED VIEW` with appropriate refresh settings
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-DB0022

The use of With Select Analyzed Table is not supported in Snowflake

### Severity

High

### Description

This message is shown when a `WITH` (CTE) query in which the main `SELECT` references a table using the `ANALYZE_TABLE` table factor is detected. DB2 allows inline analytics (e.g., SAS routines) via `ANALYZE_TABLE` in such contexts. Snowflake does not support this, so the entire `WITH` query is marked with this EWI.

#### Code Example

##### DB2

Copy code

```
WITH sas_score_in (c1,c2) AS
  (SELECT c1,c2 FROM t1)
  SELECT *
    FROM sas_score_in ANALYZE_TABLE(
    IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;');
```

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0022 - WITH SELECT ANALYZED TABLE IS NOT SUPPORTED ***/!!!
WITH sas_score_in (c1,c2) AS
  (SELECT c1,c2 FROM t1)
  SELECT *
    FROM sas_score_in ANALYZE_TABLE(
    IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;');
```

### Recommendations

- Refactor the query to remove `ANALYZE_TABLE`. Implement the analytics logic in Snowflake using Snowpark, stored procedures, or external functions, then integrate results via a separate step or view
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
