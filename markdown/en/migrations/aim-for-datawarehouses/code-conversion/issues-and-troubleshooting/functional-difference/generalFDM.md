# Code Conversion - General Functional Differences

## SSC-FDM-0001

Views selecting all columns from a single table are not required in Snowflake

Note

Some parts of the output code are omitted for clarity reasons.

### Description

Views that only select all columns of a single table and do not have any filtering clauses are not required in Snowflake and may affect performance.

#### Code Example

##### Input Code (Oracle):

Copy code

```
 CREATE OR REPLACE VIEW simpleView1
AS
SELECT
*
FROM
simpleTable;

CREATE OR REPLACE VIEW simpleView2
AS
SELECT
*
FROM
simpleTable GROUP BY col1;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE VIEW simpleView1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
*
FROM
simpleTable;

CREATE OR REPLACE VIEW simpleView2
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
*
FROM
simpleTable
GROUP BY col1;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0002

Correlated Subquery May Have Functional Differences

### Description

This message is reported when a `Correlated Subquery` (subquery that refers to a column from the outer query) is located. This type of subqueries can, in some cases, present some functional differences in Snowflake ([Working with Subqueries](https://docs.snowflake.com/en/user-guide/querying-subqueries#correlated-vs-uncorrelated-subqueries)).

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE schema1.table1(column1 NVARCHAR(50), column2 NVARCHAR(50));
CREATE TABLE schemaA.tableA(columnA NVARCHAR(50), columnB NVARCHAR(50));

--Correlated Subquery
SELECT columnA FROM schemaA.tableA ta WHERE columnA = (SELECT SUM(column1) FROM schema1.table1 t1 WHERE t1.column1 = ta.columnA);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE schema1.table1 (
column1 VARCHAR(50),
column2 VARCHAR(50))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/11/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE schemaA.tableA (
columnA VARCHAR(50),
columnB VARCHAR(50))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/11/2024",  "domain": "test" }}'
;

--Correlated Subquery
SELECT
columnA
FROM
schemaA.tableA ta
WHERE
columnA =
          --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
          (SELECT
          SUM(column1) FROM
          schema1.table1 t1
          WHERE
          t1.column1 = ta.columnA
          );
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0003

Conversion Rate Inconsistency

### Description

This message is reported when a conversion rate inconsistency is found on the assessment field specified. These situations are resolved automatically, so this is just an informative warning.

Note

This Informative warning will only be visible in the assessment documents and not the output code

#### Best Practices

- Despite the issue being automatically fixed, you can still notify the support team by emailing [aim-support@snowflake.com](mailto:aim-support@snowflake.com) and specifying the issue.

## SSC-FDM-0004

External table translated to regular table

Note

This FDM is deprecated.

### Description

This warning is added to clauses related to external handling. Snowflake recommends that all data should be managed inside the Snowflake data storage. For more information on this subject, see the [Snowflake data storage considerations](https://docs.snowflake.com/en/user-guide/tables-storage-considerations.html#data-storage-considerations).

#### Code Example

##### Input Code:

Copy code

```
 CREATE EXTERNAL TABLE ext_csv_file (
    id INT,
    name TEXT,
    age INT,
    city TEXT
)
LOCATION (
    'gpfdist://192.168.1.100:8080/data/my_data.csv'
)
FORMAT 'CSV' (DELIMITER ',' HEADER);
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0004 - EXTERNAL TABLE TRANSLATED TO REGULAR TABLE **
CREATE TABLE ext_csv_file (
       id INT,
       name TEXT,
       age INT,
       city TEXT
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "07/09/2025",  "domain": "no-domain-provided" }}'
;
```

#### Best Practices

- The data stored in files of the external tables must be somehow moved into the Snowflake database.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0005

TIME ZONE not supported for time data type

### Description

The Time data type in Snowflake does not store Timezone values

> TIME internally stores “wallclock” time, and all operations on TIME values are performed without taking any time zone into consideration. For more information, see the [Snowflake TIME data type documentation](https://docs.snowflake.com/en/sql-reference/data-types-datetime#time).

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE TABLE_TIME_TYPE (
    COLNAME TIME (9) WITH TIME ZONE
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TABLE_TIME_TYPE (
    COLNAME TIME(9) /*** SSC-FDM-0005 - TIME ZONE NOT SUPPORTED FOR TIME DATA TYPE ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0006

Number type column may not behave similarly in Snowflake

### Description

This functional difference message appears when a `NUMBER` Type column is being created within a Table. The reason for this is due to arithmetic differences when performing operations related to the scales of intermediate values in Snowflake which could make some operations fail. For more information please refer to [Snowflake’s post on intermediate numbers in Snowflake](https://community.snowflake.com/s/question/0D50Z00008HhSHCSA3/sql-compilation-error-invalid-intermediate-datatype-number7148) and [Number out of representable range](https://community.snowflake.com/s/article/Number-out-of-representable-range-error-occurs-during-the-multiplication-of-numeric-values).

To avoid these arithmetic issues, you can run data samplings to verify the needed precision and scales for these operations.

#### Example Codes

#### Simple Table with Number Columns

##### Input Code (Oracle):

Copy code

```
 CREATE TABLE table1
(
column1 NUMBER,
column2 NUMBER (20, 4)
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE table1
(
column1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
column2 NUMBER(20, 4) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Arithmetic Issue Examples

The next examples show how the arithmetic issues can happen when using Number columns:

##### Snowflake Code with Division Error:

Copy code

```
 CREATE OR REPLACE TABLE number_table( column1 NUMBER(38, 19) );

INSERT INTO number_table VALUES (1);

SELECT column1 / column1 FROM number_table;
```

##### Snowflake Code with Multiplication Error:

Copy code

```
 CREATE OR REPLACE TABLE number_table( column1 NUMBER(38, 20) );

INSERT INTO number_table VALUES (1);

SELECT column1 * column1 FROM number_table;
```

When running either `SELECT` statements Snowflake will return an error:

`Number out of representable range: type FIXEDSB16{nullable}, value 1.0000000000000000000`

This is due to the intermediate operation’s result overflowing Snowflake’s maximum capacity; reducing the number scales by 1 on each example will fix the error and work normally:

##### Snowflake Code with Division:

Copy code

```
 CREATE OR REPLACE TABLE number_table( column1 NUMBER(38, 18) );

INSERT INTO number_table VALUES (1);

SELECT column1 / column1 FROM number_table;
```

##### Snowflake Code with Multiplication:

Copy code

```
 CREATE OR REPLACE TABLE numbertable( column1 NUMBER(38, 19) );

INSERT INTO number_table VALUES (1);

SELECT column1 * column1 FROM number_table;
```

For this reason, the default scale of Numbers is set to 18, minimizing the number of errors when migrating.

#### Best Practices

- Verify that your operations’ intermediate values don’t exceed a scale of 37, as that is Snowflake’s maximum.
- Run Data Samplings on your data, to make sure you have the required precision and scales before running any operations.
- In most cases, after doing some data sampling or discussing with the business you might come to the conclusion that the precision can be different. For example, for `MONEY` columns a typical precision is `NUMBER(20,4)`. In snowflake you cannot easily alter a column data type, you can check this [post on our forum](https://www.mobilize.net/blog/how-to-alter-column-datatype-in-snowflake) which provides some guidance on how to alter your columns data types and preserve your data.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0007

Element with missing dependencies

Note

Some parts of the output code are omitted for clarity reasons

### Description

There is a missing dependency for an object, Snow Convert could not resolve some data types. Also there exists a possibility to have a deployment error if the dependency was not in the source code.

#### Example Code

##### Input Code:

Copy code

```
 CREATE VIEW VIEW01 AS SELECT * FROM TABLE1;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE VIEW VIEW01
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
TABLE1;
```

Note

Note that the TABLE1 definition is missing.

#### Best Practices

- Make sure all the dependencies of the objects are in the source code.
- If not, find the references to the object in the code and check if the operations are well managed.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0008

On Commit not supported

Note

Some parts of the output code are omitted for clarity reasons.

### Description

The ON COMMIT clauses in your CREATE TABLE statement have been commented out. Snowflake does not support the ON COMMIT clause, as it’s typically used for temporary tables in other SQL dialects. If you need to manage transaction-specific behavior, consider using Snowflake’s transactions or temporary tables with explicit TRUNCATE or DROP statements instead.

#### Example Code

##### Input Code

Copy code

```
CREATE TEMPORARY TABLE TABLE02 (COLNAME VARCHAR(20)) ON COMMIT DELETE ROWS
```

##### Generated Code

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE TABLE02 (
COLNAME VARCHAR(20))
----** SSC-FDM-0008 - ON COMMIT (DELETE ROWS) IS NOT SUPPORTED **
--ON COMMIT DELETE ROWS
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "09/22/2025",  "domain": "no-domain-provided" }}'
;
```

## SSC-FDM-0009

GLOBAL TEMPORARY TABLE functionality not supported.

### Description

Global temporary tables are considered a complex pattern, due to the fact they can come in several variations, as indicated in [Snowflake’s documentation](https://docs.snowflake.com/en/sql-reference/sql/create-table#variant-syntax).

#### Example Code

##### Input Code

Copy code

```
 CREATE OR REPLACE GLOBAL TEMPORARY TABLE GLOBAL_TEMP_TABLE
(
    col3 INTEGER,
    col4 VARCHAR(50)
);
```

##### Generated Code

Copy code

```
 --** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE GLOBAL_TEMP_TABLE
    (
        col3 INTEGER,
        col4 VARCHAR(50)
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0010

Type changed to Date.

### Description

This message is shown when a DEFAULT SYSDATE is found and the data type is NOT a DATE or TIMESTAMP datatype. In this case, the data type is changed to DATE.

#### Example Code

##### Input Code

Copy code

```
 CREATE TABLE "SYSDATE_DEFAULT_TEST_TABLE_1"( 
 "COLUMN1" VARCHAR2(30 BYTE) DEFAULT SYSDATE
);
```

##### Generated Code

Copy code

```
 CREATE OR REPLACE TABLE "SYSDATE_DEFAULT_TEST_TABLE_1" (
  "COLUMN1" TIMESTAMP DEFAULT CURRENT_TIMESTAMP() /*** SSC-FDM-0010 - CONVERTED FROM VARCHAR2 TO DATE FOR CURRENT_DATE DEFAULT ***/
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0011

Column Name Is Snowflake Reserved Keyword.

Note

This FDM is deprecated, please refer to [SSC-EWI-0045](../conversion-issues/generalEWI#ssc-ewi-0045) documentation.

### Description

Column names that are valid for the source language but are reserved keywords in Snowflake.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE TABLE T1
(
    LOCALTIME VARCHAR,
    CURRENT_USER VARCHAR
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE T1
    (
    --** SSC-FDM-0011 - COLUMN NAME 'LOCALTIME' IS A SNOWFLAKE RESERVED KEYWORD **
    "LOCALTIME" VARCHAR,
    --** SSC-FDM-0011 - COLUMN NAME 'CURRENT_USER' IS A SNOWFLAKE RESERVED KEYWORD **
    "CURRENT_USER" VARCHAR
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Best Practices

- Consider renaming the columns that use names that are not supported in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0012

Constraint Name in some constraints is not Supported.

### Description

This message is added when a constraint is of type Null, Not Null, or default and was defined with a name. Snowflake does not support the name in those constraints. For that, it will be removed and the comment added.

#### Example Code

##### Input Code

Copy code

```
 CREATE TABLE TABLE1 ( 
COL1 VARCHAR (10) CONSTRAINT constraintName DEFAULT ('0') NOT NULL 
);
```

##### Generated Code

Copy code

```
 CREATE OR REPLACE TABLE TABLE1 (
COL1 VARCHAR(10) DEFAULT ('0') /*** SSC-FDM-0012 - CONSTRAINT NAME 'constraintName' IN DEFAULT EXPRESSION CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE ***/ NOT NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0013

Timezone expression could not be mapped

### Description

This FDM message is added to indicate scenarios where the actual value of a timezone expression cannot be determined, and therefore, the translated results might be different. When the timezone value used is a literal string, it can be mapped to its corresponding timezone value in Snowflake. However, when this value is specified by an expression, the timezone value that will be used at runtime cannot be determined and, therefore, cannot be mapped to its corresponding Snowflake equivalent.

#### Example Code

##### Input Code (Oracle)

Copy code

```
 SELECT TIMESTAMP '1998-12-25 09:26:50.12' AT TIME ZONE SESSIONTIMEZONE FROM DUAL;
SELECT TIMESTAMP '1998-12-25 09:26:50.12' AT TIME ZONE Expression FROM DUAL;
```

##### Generated Code

Copy code

```
 SELECT
--** SSC-FDM-0013 - TIMEZONE EXPRESSION COULD NOT BE MAPPED, RESULTS MAY BE DIFFERENT **
TO_TIMESTAMP_LTZ( TIMESTAMP '1998-12-25 09:26:50.12')
FROM DUAL;

SELECT
--** SSC-FDM-0013 - TIMEZONE EXPRESSION COULD NOT BE MAPPED, RESULTS MAY BE DIFFERENT **
CONVERT_TIMEZONE(Expression, TIMESTAMP '1998-12-25 09:26:50.12')
FROM DUAL;
```

##### Input Code (Teradata)

Copy code

```
 select TIMESTAMP '1998-12-25 09:26:50.12' AT TIME ZONE SESSIONTIMEZONE;
select current_timestamp at time zone CONCAT(' America ', ' Pacific'); 
select current_timestamp at time zone (SELECT COL1 FROM TABLE1 WHERE COL2 = 2);
```

##### Generated Code

Copy code

```
 SELECT
CONVERT_TIMEZONE(SESSIONTIMEZONE, TIMESTAMP '1998-12-25 09:26:50.12') /*** SSC-FDM-0013 - TIMEZONE EXPRESSION COULD NOT BE MAPPED, RESULTS MAY BE DIFFERENT ***/;

SELECT
CONVERT_TIMEZONE(CONCAT(' America ', ' Pacific'), CURRENT_TIMESTAMP) /*** SSC-FDM-0013 - TIMEZONE EXPRESSION COULD NOT BE MAPPED, RESULTS MAY BE DIFFERENT ***/;

SELECT
CONVERT_TIMEZONE((
SELECT
COL1 FROM
TABLE1
WHERE COL2 = 2), CURRENT_TIMESTAMP) /*** SSC-FDM-0013 - TIMEZONE EXPRESSION COULD NOT BE MAPPED, RESULTS MAY BE DIFFERENT ***/;
```

#### 

Note

##### Timezone Compatibility in Oracle

The majority of timezone name expressions in Oracle are directly supported in Snowflake, when this is the case, the migration will run without issues. Additionally, here is a list of which ones are not supported by Snowflake at the moment, and therefore will include the functional difference message.

- Africa/Doula
- Asia/Ulaanbaator
- Asia/Yetaterinburg
- Canada/East-Saskatchewan
- CST
- PST
- US/Pacific-New

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0014

Check statement not supported.

Note

This FDM is deprecated, please refer to [SSC-EWI-0035](../conversion-issues/generalEWI#ssc-ewi-0035) documentation.

### Description

***CHECK*** constraint is not supported by Snowflake but it does not affect functionally.

#### Example Code

##### Input Code Oracle :

Copy code

```
 CREATE TABLE "Schema"."BaseTable"(
  "COLUMN1" VARCHAR2(255),
  CHECK ( COLUMN1 IS NOT NULL )
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE "Schema"."BaseTable" (
    "COLUMN1" VARCHAR(255)
--                          ,
--    --** SSC-FDM-0014 - CHECK STATEMENT NOT SUPPORTED **
--    CHECK ( COLUMN1 IS NOT NULL )
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
  ;
```

##### Input Code Teradata:

Copy code

```
 CREATE TABLE TABLE1,
    NO FALLBACK,
    NO BEFORE JOURNAL,
    NO AFTER JOURNAL
(
    COL0 BYTEINT,
    CONSTRAINT constraint_name CHECK (COL1 < COL2)
)
```

##### Generated Code:

Copy code

```
 CREATE TABLE TABLE1
(
    COL0 BYTEINT
--                ,
--    --** SSC-FDM-0014 - CHECK STATEMENT NOT SUPPORTED **
--    CONSTRAINT constraint_name CHECK (COL1 < COL2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

##### Input Code SqlServer

Copy code

```
 ALTER TABLE table_name2
ADD column_name VARCHAR(255)
CONSTRAINT constraint_name 
CHECK NOT FOR REPLICATION (column_name > 1);
```

##### Generated Code:

Copy code

```
 ALTER TABLE IF EXISTS table_name2
ADD column_name VARCHAR(255)
----** SSC-FDM-0014 - CHECK STATEMENT NOT SUPPORTED **
--CONSTRAINT constraint_name
--CHECK NOT FOR REPLICATION (column_name > 1)
                                           ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0015

​Referenced custom type in query not found.

### Description

This error happens when the definition for a Custom Type was not found or an Oracle built-in data type was not recognized by SnowConvert.

#### Example code

##### Input Code (Oracle):

Copy code

```
 --Type was never defined
--CREATE TYPE type1;

CREATE TABLE table1
(
column1 type1
);
```

##### Generated Code:

Copy code

```
 --Type was never defined
--CREATE TYPE type1;

CREATE OR REPLACE TABLE table1
(
column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE TYPE1 IS NOT SUPPORTED IN SNOWFLAKE ***/!!! NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}}'
;
```

#### Best Practices

- Verify that the type that the referenced data type was defined in the input code.
- Check the Snowflake data types [documentation](https://docs.snowflake.com/en/sql-reference/data-types.html) to find an equivalent for the data type.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0016

Constants are not supported by Snowflake Scripting. It was transformed to a variable.

### Description

Snowflake Scripting does not support constants. Therefore, all constants inside procedures are being transformed into variables when the Snowflake Scripting flag is active.

#### Example code

##### Oracle:

Copy code

```
 CREATE OR REPLACE PROCEDURE p_constants
AS
my_const1 CONSTANT NUMBER := 40;
my_const2 CONSTANT NUMBER NOT NULL := 40;
BEGIN
NULL;
END;
```

##### Snowflake Scripting:

Copy code

```
 CREATE OR REPLACE PROCEDURE p_constants ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
--** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
my_const1 NUMBER(38, 18) := 40;
--** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
--** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE **
my_const2 NUMBER(38, 18) := 40;
BEGIN
NULL;
END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0017

WITH SYSTEM VERSIONING clause is not supported by Snowflake

### Description

The `WITH SYSTEM VERSIONING` clause in ANSI SQL is used to enable system versioning for a table, allowing you to maintain a history of changes to the table’s data over time. This clause is not supported by Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE t1 (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    SysStartTime TIMESTAMP,
    SysEndTime TIMESTAMP
) WITH SYSTEM VERSIONING;
```

##### Generated Code:

Copy code

```
 CREATE TABLE t1 (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    SysStartTime TIMESTAMP,
    SysEndTime TIMESTAMP
)
----** SSC-FDM-0017 - WITH SYSTEM VERSIONING CLAUSE IS NOT SUPPORTED BY SNOWFLAKE. **
--WITH SYSTEM VERSIONING
                      ;
```

#### Best Practices

- You can use [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel) in Snowflake, Time Travel enables accessing historical data (that is, data that has been changed or deleted) at any point within a defined period. It serves as a powerful tool for performing the following tasks:
  - Restoring data-related objects (tables, schemas, and databases) that might have been accidentally or intentionally deleted.
  - Duplicating and backing up data from key points in the past.
  - Analyzing data usage/manipulation over specified periods of time.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0018

CHARACTER SET clause is not supported by Snowflake.

### Description

The column option CHARACTER SET determines the allowed set of characters that can be stored in the column, this clause is not supported by Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE TABLE01(
    COLNAME VARCHAR(20) CHARACTER SET character_specification
);
```

##### Generated Code:

Copy code

```
 CREATE TABLE TABLE01 (
    COLNAME VARCHAR(20)
--                        --** SSC-FDM-0018 - CHARACTER SET CLAUSE IS NOT SUPPORTED BY SNOWFLAKE. **
--                        CHARACTER SET character_specification
);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0019

Semantic information could not be loaded.

### Description

This warning lets the user know that semantic information for a specific object could not be loaded. This is most likely caused because if there is a duplicated object with the same name, the semantic information of this object could not be loaded to complete the analysis.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE T1
(
    COL1 INTEGER
);

CREATE TABLE T1
(
    COL2 INTEGER
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE T1
(
    COL1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR T1. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE TABLE T1
(
    COL2 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- Check for duplicate objects in the input code since this may affect the loading of semantic information.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0020

Multiple result sets are returned in temporary tables

### Description

Snowflake Scripting procedures only allow one result set to be returned per procedure.

To replicate Teradata behavior, when there are two or more result sets to return, they are stored in temporary tables. The Snowflake Scripting procedure will return an array containing the name of the temporary tables.

#### Example code

##### Input Code (Teradata):

Copy code

```
 REPLACE MACRO sampleMacro AS 
(
    SELECT CURRENT_DATE AS DT;
    SELECT CURRENT_DATE AS DT_TWO;
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE sampleMacro ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        return_arr ARRAY := array_construct();
        tbl_nm VARCHAR;
    BEGIN
        tbl_nm := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
        CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_nm) AS
            SELECT
                CURRENT_DATE() AS DT;
        return_arr := array_append(return_arr, :tbl_nm);
        tbl_nm := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
        CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_nm) AS
            SELECT
                CURRENT_DATE() AS DT_TWO;
        return_arr := array_append(return_arr, :tbl_nm);
        --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
        RETURN return_arr;
    END;
$$;
```

#### Best Practices

- To obtain the result sets, it is necessary to run a SELECT query with the name of the temporary tables returned by the procedure.
- As much as possible, avoid procedures that return multiple result sets; instead, make them single-responsibility for more direct results.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0021

Create Index Not Supported

### Description

Due to architectural reasons, Snowflake does not support indexes so, all the code related to the creation of indexes will be commented out. Snowflake automatically creates micro-partitions for every table that help speed up the performance of DML operations, the user does not have to worry about creating or managing these micro-partitions.

Usually, this is enough to have a very good query performance however, there are ways to improve it by creating data clustering keys. [Snowflake’s official page](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html) provides more information about micro-partitions and data clustering.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE INDEX index1
ON table1(column1);
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-0021 - CREATE INDEX IS NOT SUPPORTED BY SNOWFLAKE **
----** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
--CREATE INDEX index1
--ON table1(column1)
                  ;
```

#### Best Practices

- Data clustering might be a way to speed up query performance on tables.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0022

Window frame unit was changed to Rows

### Severity

Low

### Description

This warning is added when an unsupported Window Frame Unit was changed into Rows, leading to output differences. One example of this is the GROUPS unit, which is not supported by Snowflake.

Please note that this message is also used in cases where a Window Frame Unit is **partially** unsupported leading to it being changed, like the RANGE unit.

#### Example Code

Given the following data as an example to explain it.

| C\_NAME | C\_BIRTH\_DAY |
| --- | --- |
| USA | 1 |
| USA | 4 |
| Poland | 9 |
| Canada | 10 |
| USA | 5 |
| Canada | 12 |
| Costa Rica | 3 |
| Poland | 4 |
| USA | 2 |
| Costa Rica | 7 |
| Costa Rica | 10 |

Expand

Show lessSee more

##### Oracle:

##### Code

Copy code

```
SELECT
    C_NAME,
    SUM(C_BIRTH_DAY)
    OVER (ORDER BY C_BIRTH_DAY
    RANGE BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS MAX1
FROM WINDOW_TABLE;
```

##### Result

| C\_NAME | MAX1 |
| --- | --- |
| USA | - |
| USA | 1 |
| Costa Rica | 3 |
| USA | 6 |
| Poland | 6 |
| USA | 14 |
| Costa Rica | 19 |
| Poland | 26 |
| Canada | 35 |
| Costa Rica | 35 |
| Canada | 55 |

Expand

Show lessSee more

##### Snowflake:

##### Code

Copy code

```
 SELECT
    C_NAME,
    SUM(C_BIRTH_DAY)
    OVER (ORDER BY C_BIRTH_DAY ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING /*** SSC-FDM-0022 - WINDOW FRAME UNIT 'RANGE' WAS CHANGED TO ROWS ***/) AS MAX1
    FROM
WINDOW_TABLE;
```

##### Result

| C\_NAME | MAX1 |
| --- | --- |
| USA | - |
| USA | 1 |
| Costa Rica | 3 |
| USA | 6 |
| Poland | 10 |
| USA | 14 |
| Costa Rica | 19 |
| Poland | 26 |
| Canada | 35 |
| Costa Rica | 45 |
| Canada | 55 |

Expand

Show lessSee more

#### Best Practices

- Ensure deterministic ordering for rows to ensure deterministic outputs when running in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0023

A Global Temporary Table is being referenced.

### Severity

Medium

### Description

Global Temporary tables are transformed into regular Create Table. References to these tables may behave different than expected.

#### Code example

##### Input

Copy code

```
 create global temporary table t1 
    (col1 varchar); 
create view view1 as 
    select col1 from t1;
```

##### Output

Copy code

```
 --** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE t1
    (col1 varchar)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW view1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
select col1 from
    --** SSC-FDM-0023 - A Global Temporary Table is being referenced **
    t1;
```

#### Related Issues

- [SSC-FDM-0009](#ssc-fdm-0009): GLOBAL TEMPORARY TABLE functionality not supported.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0024

Functionality is not currently supported by Snowflake Scripting

Note

This `FDM` is deprecated, please refer to [SSC-EWI-0058](../conversion-issues/generalEWI#ssc-ewi-0058) documentation.

### Description

This error happens when a statement used in a create procedure is not currently supported by Snowflake Scripting.

#### Example code

##### Input Code (Oracle):

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC01
IS
  number_variable INTEGER;
BEGIN
  EXECUTE IMMEDIATE 'SELECT 1 FROM DUAL' INTO number_variable;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC01 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    number_variable INTEGER;
  BEGIN
    EXECUTE IMMEDIATE 'SELECT 1 FROM DUAL'
--                                           --** SSC-FDM-0024 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING **
--                                           INTO number_variable
                                                               ;
  END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0025

Unexpected end of statement

### Description

This message is reported when an unexpected end of statement is encountered during conversion. This typically occurs when the parser reaches the end of the source code while still expecting additional tokens to complete a statement. The EWI includes the line number of the original source code where the issue was detected.

#### Example Code

##### Input Code:

Copy code

```
 UPDATE orders
SET total = 100
WHERE order_id = 1
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0025 - UNEXPECTED END OF STATEMENT. PLEASE CHECK THE LINE 5 OF ORIGINAL SOURCE CODE. **
UPDATE orders
SET total = 100
WHERE order_id = 1;
```

#### Best Practices

- Check the specified line in the original source code for missing semicolons or incomplete statements.
- Ensure all statements are properly terminated.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0026

Type not supported by Snowflake

Note

This `FDM` is deprecated, please refer to [SSC-EWI-0028](../conversion-issues/generalEWI#ssc-ewi-0028) documentation.

### Description

This message appears when a type is not supported in Snowflake.

#### Example

##### Input Code (Oracle):

Copy code

```
 CREATE TABLE MYTABLE
(
    COL1 SYS.ANYDATASET
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE MYTABLE
    (
    --** SSC-FDM-0026 - TYPE NOT SUPPORTED BY SNOWFLAKE **
        COL1 SYS.ANYDATASET
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0027

Removed next statement, not applicable in Snowflake.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This message appears when a specific statement is not applicable in Snowflake, it means that there is no Snowflake equivalent for this statement and it is no longer needed, and for that reason, it is removed from the source code. However, the original statement is kept as part of the comment at the end.

#### Example Code

##### Input Code:

Copy code

```
 .LOGTABLE tduser.Employee_log;  
   .BEGIN MLOAD TABLES Employee_Stg;  
      .LAYOUT Employee;  
      .FIELD in_EmployeeNo * VARCHAR(10);  
      .FIELD in_FirstName * VARCHAR(30); 
      .FIELD in_LastName * VARCHAR(30);  
      .FIELD in_BirthDate * VARCHAR(10); 
      .FIELD in_JoinedDate * VARCHAR(10);  
      .FIELD in_DepartmentNo * VARCHAR(02);

      .dml label EmpLabel
  IGNORE DUPLICATE INSERT ROWS; 
      INSERT INTO Employee_Stg (
         EmployeeNo,
         FirstName,
         LastName,
         BirthDate,
         JoinedDate,
         DepartmentNo
      )  
      VALUES (
         :in_EmployeeNo,
         :in_FirstName,
         :in_Lastname,
         :in_BirthDate,
         :in_JoinedDate,
         :in_DepartmentNo
      );
      .IMPORT INFILE employee.txt  
      FORMAT VARTEXT ','
      LAYOUT Employee
      APPLY EmpLabel;  
   .END MLOAD;  
LOGOFF;
```

##### Generated Code:

Copy code

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
// SnowConvert AI Helpers Code section is omitted.
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #.LOGTABLE tduser.Employee_log
   
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #.BEGIN MLOAD TABLES Employee_Stg
   
  Employee_TableName = "Employee_TEMP_TABLE"
  Employee_Columns = """in_EmployeeNo VARCHAR(10), 
in_FirstName VARCHAR(30), 
in_LastName VARCHAR(30), 
in_BirthDate VARCHAR(10), 
in_JoinedDate VARCHAR(10), 
in_DepartmentNo VARCHAR(02)"""
  Employee_Conditions = """in_EmployeeNo AS in_EmployeeNo, in_FirstName AS in_FirstName, in_LastName AS in_LastName, in_BirthDate AS in_BirthDate, in_JoinedDate AS in_JoinedDate, in_DepartmentNo AS in_DepartmentNo"""
  def EmpLabel(tempTableName, queryConditions = ""):
    exec(f"""INSERT INTO Employee_Stg (EmployeeNo, FirstName, LastName, BirthDate, JoinedDate, DepartmentNo)
SELECT
   SRC.in_EmployeeNo,
   SRC.in_FirstName,
   :in_Lastname,
   SRC.in_BirthDate,
   SRC.in_JoinedDate,
   SRC.in_DepartmentNo
FROM {tempTableName} SRC {queryConditions}""")
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #.IMPORT INFILE employee.txt FORMAT VARTEXT ',' LAYOUT Employee APPLY EmpLabel
   
  snowconvert.helpers.import_file_to_temptable(fr"employee.txt", Employee_TableName, Employee_Columns, Employee_Conditions, ',')
  EmpLabel(Employee_TableName)
  exec(f"""DROP TABLE {Employee_TableName}""")

  if con is not None:
    con.close()
    con = None
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0028

Not supported.

Note

This `FDM` is deprecated, please refer to [SSC-EWI-0021](../conversion-issues/generalEWI#ssc-ewi-0021) documentation.

### Description

This message appears when a specific node or statement from the source code is not supported in Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 WITH my_av ANALYTIC VIEW AS
(USING sales_av HIERARCHIES(time_hier) ADD MEASURES(lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1 )))) 
SELECT aValue from my_av;
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-0028 - SubavFactoring NOT SUPPORTED IN SNOWFLAKE **
--WITH my_av ANALYTIC VIEW AS
--(USING sales_av HIERARCHIES(time_hier) ADD MEASURES(lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1 ))))
--SELECT aValue from my_av
                        ;
```

#### Best Practices

- If this error happens, it is because there is no Snowflake equivalent for the node that is being converted.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0029

User defined function was transformed to a Snowflake procedure.

Warning

This EWI is deprecated, please refer to [SSC-EWI-0068](../conversion-issues/generalEWI#ssc-ewi-0068) documentation

### Severity

Low

### Description

Snowflake user defined functions do not support the same features as Oracle or SQL Server. To maintain the functional equivalence the function is transformed to a Snowflake stored procedure. This will affect their usage in queries.

#### Example Code

##### SQL Server:

##### Input Code

Copy code

```
 CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS INT
AS
BEGIN
    DECLARE @i int = 0, @p int;
    Select @p = COUNT(*) FROM PURCHASING.VENDOR
    
    WHILE (@p < 1000)
    BEGIN
        SET @i = @i + 1
        SET @p = @p + @i
    END
        
    IF (@i = 6)
        RETURN 1
    
    RETURN @p
END;
```

##### Generated Code

Copy code

```
 --** SSC-FDM-0029 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE **
CREATE OR REPLACE PROCEDURE PURCHASING.FOO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I INT := 0;
        P INT;
    BEGIN
         
        Select
            COUNT(*)
        INTO
            :P
 FROM
            PURCHASING.VENDOR;
        WHILE (:P < 1000) LOOP
            I := :I + 1;
            P := :P + :I;
        END LOOP;
        IF ((:I = 6)) THEN
            RETURN 1;
        END IF;
        RETURN :P;
    END;
$$;
```

##### Oracle:

##### Input Code

Copy code

```
 CREATE FUNCTION employee_function (param1 in NUMBER) RETURN NUMBER is
  var1    employees.employee_ID%TYPE;
  var2    employees.manager_ID%TYPE;
  var3    employees.title%TYPE;
BEGIN
  SELECT employee_ID, manager_ID, title
  INTO var1, var2, var3
  FROM employees
    START WITH manager_ID = param1
    CONNECT BY manager_ID = PRIOR employee_id;
  RETURN var1;
EXCEPTION
   WHEN no_data_found THEN RETURN param1;
END employee_function;
```

##### Generated Code

Copy code

```
 --** SSC-FDM-0029 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE **
CREATE OR REPLACE PROCEDURE employee_function (param1 NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1    employees.employee_ID%TYPE;
    var2    employees.manager_ID%TYPE;
    var3    employees.title%TYPE;
  BEGIN
    SELECT employee_ID, manager_ID, title
    INTO
      :var1,
      :var2,
      :var3
    FROM
      employees
      START WITH manager_ID = :param1
    CONNECT BY
      manager_ID = PRIOR employee_id;
    RETURN :var1;
  EXCEPTION
     WHEN no_data_found THEN
      RETURN :param1;
  END;
$$;
```

### Best Practices

- Separate the inside queries to maintain the same logic.
- The source code may need to be restructured to fit with the Snowflake user-defined functions [approach](https://docs.snowflake.com/en/sql-reference/user-defined-functions.html#udfs-user-defined-functions).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0030

Replaced invalid characters for new identifier

### Description

The given identifier has invalid characters for the output language. Those characters were replaced with their UTF-8 codes.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE PROCEDURE PROC1
AS
    "VAR0" INT;
    "VAR`/1ͷ" VARCHAR(20);
    "o*/o" FLOAT;
    " . " INT;
    ". ." INT;
    "123Name" INT;
    "return" INT;
    yield INT;
    ident#10 INT;
BEGIN
    NULL;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        "VAR0" INT;
        --** SSC-FDM-0030 - IDENTIFIER '"VAR`/1ͷ"' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES **
        VAR_u60_u2F1_uCD_B7 VARCHAR(20);
        --** SSC-FDM-0030 - IDENTIFIER '"o*/o"' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES **
        o_u2A_u2Fo FLOAT;
        --** SSC-FDM-0030 - IDENTIFIER '" . "' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES **
        _u20_u2E_u20 INT;
        --** SSC-FDM-0030 - IDENTIFIER '". ."' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES **
        _u2E_u20_u2E INT;
        "123Name" INT;
        "return" INT;
        yield INT;
        IDENT_HASHTAG_10 INT;
    BEGIN
        NULL;
    END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0031

Dynamic Table required parameters set by default

### Description

Materialized Views (and Join Indexes in the case of Teradata) are migrated to Dynamic Tables in Snowflake. Dynamic Tables require two parameters to be set: TARGET\_LAG and WAREHOUSE.

If these parameters are not set in the configuration options, they are set by default during conversion.

Read more about the [required Dynamic Tables parameters here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table#required-parameters).

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE MATERIALIZED VIEW mv1
AS SELECT * FROM table1;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE DYNAMIC TABLE mv1
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT * FROM
table1;
```

#### Best Practices

- Configure the dynamic table required parameters according to your needs.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0032

Parameter is not a literal value, transformation could not be fully applied

### Description

For multiple transformations, validating the contents of a parameter is sometimes required, which is only possible if the parameter is a literal value.

This message is generated to warn the user that the value of the parameter could not be retrieved because it was passed by reference, causing the transformation of the function or statement to not be completed.

#### Example Code

##### Input Code (Redshift):

Copy code

```
 SELECT TO_CHAR(DATE '2001-01-01', 'YYY/MM/DD'),
TO_CHAR(DATE '2001-01-01', f)
FROM (SELECT 'YYY/MM/DD' as f);
```

##### Generated Code:

Copy code

```
 SELECT
PUBLIC.YEAR_PART_UDF(DATE '2001-01-01', 3) || TO_CHAR(DATE '2001-01-01', '/MM/DD'),
--** SSC-FDM-0032 - PARAMETER 'format_string' IS NOT A LITERAL VALUE, TRANSFORMATION COULD NOT BE FULLY APPLIED **
TO_CHAR(DATE '2001-01-01', f)
FROM (SELECT 'YYY/MM/DD' as f);
```

#### Best Practices

- Try to provide the specified parameter as a literal value.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0033

Sample clause behaves differently in Snowflake.

### Description

This message is generated to showcase the functional difference while sampling rows in Snowflake. The differences are related to the quantity of rows retrieved. When in Teradata there is the same quantity of rows in the non-deterministic output, it may change in Snowflake and return a few rows more or less. This is because a probability related topic and it is expected to behaves like that in Snowflake.

If there is a requirement of retrieving the same values and the same quantity, a deterministic output, it is recommended to use a seed in the Snowflake query.

#### Example Code

##### Input Code (Teradata):

Copy code

```
 SELECT * FROM Employee SAMPLE 2;
SELECT * FROM Employee SAMPLE 0.25;
```

##### Generated Code:

Copy code

```
 SELECT
    * FROM
    Employee
--** SSC-FDM-0033 - SAMPLE CLAUSE BEHAVES DIFFERENTLY IN SNOWFLAKE **
SAMPLE(2 ROWS);

SELECT
    * FROM
    Employee
--** SSC-FDM-0033 - SAMPLE CLAUSE BEHAVES DIFFERENTLY IN SNOWFLAKE **
SAMPLE(25);
```

#### Best Practices

- Try to use the seed part of the query when it is required a deterministic output.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0034

Struct converted to VARIANT. Some of its usages might have functional differences.

### Description

Snowflake does not natively support the STRUCT data type. STRUCT is automatically converted to VARIANT. When used in INSERT statements, STRUCT data will be handled using `OBJECT_CONSTRUCT`. Be aware that this conversion may introduce functional differences in some use cases.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE test.structTypes
(
  COL1 STRUCT<sc1 INT64>,
  COL2 STRUCT<sc2 STRING(10)>,
  COL3 STRUCT<sc3 STRUCT<sc31 INT64, sc32 INT64>>,
  COL4 STRUCT<sc4 ARRAY<INT64>>,
  COL5 STRUCT<sc5 INT64, sc51 INT64>,
  COL7 STRUCT<sc7 INT64 OPTIONS(description = "A repeated STRING field"), sc71 BOOL>,
  COL8 STRUCT<sc8 INT64 NOT NULL, sc81 BOOL NOT NULL OPTIONS(description = "A repeated STRING field")>
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE test.structTypes
(
  COL1 VARIANT /*** SSC-FDM-0034 - STRUCT<INT64> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL2 VARIANT /*** SSC-FDM-0034 - STRUCT<STRING(10)> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL3 VARIANT /*** SSC-FDM-0034 - STRUCT<STRUCT<INT64, INT64>> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL4 VARIANT /*** SSC-FDM-0034 - STRUCT<ARRAY<INT64>> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL5 VARIANT /*** SSC-FDM-0034 - STRUCT<INT64, INT64> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL7 VARIANT /*** SSC-FDM-0034 - STRUCT<INT, BOOL> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL8 VARIANT /*** SSC-FDM-0034 - STRUCT<INT64, BOOLEAN> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/
  )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "05/30/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0035

The INFER\_SCHEMA function requires a file path without wildcards to generate the table template, replace the FILE\_PATH placeholder with it

### Description

The [INFER\_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) function is used in Snowflake to generate the columns definition of a table based on the structure of a file, it requires a LOCATION parameter that specifies the path to a file or folder that will be used to construct the table columns, however, this path does not support regex, meaning that the wildcard `*` character is not supported.

When the table has no columns, all URIs are checked to find one that does not use wildcards and use it in the INFER\_SCHEMA function, when no URI meets such criteria this FDM and a FILE\_PATH placeholder will be generated, the placeholder has to be replaced with the path of one of the files referenced by the external table to generate the table columns.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2
OPTIONS(
  FORMAT='JSON',
  URIS=['gs://sc_external_table_bucket/folder_with_json/*']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2 USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-0035 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_json/.*'
FILE_FORMAT = (TYPE = JSON);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0036

The transformed numeric/date format may have a different behavior in Snowflake.

### Description

The transformed numeric formats to Snowflake use {ref}`Fixed position formats <label-fixed-position-numeric-formats>`. The transformed format can fail and generate a different output when there are more digits in the integer part of the number than there are digit positions in the format; all digits are printed as # to indicate overflow.

For date/time custom format specifiers, some SQL Server specifiers are mapped to Snowflake equivalents that may produce slightly different output. For example, `dddd` (full day name) maps to `DY` (abbreviated day name), uppercase `F`–`FFFFFFF` (fractional seconds without trailing zeros) map to `F1`–`F7` (Snowflake always includes trailing zeros), and `z` (UTC offset hours only) maps to `TZH`. These differences are flagged with this FDM marker so you can verify the output matches your requirements.

#### Code Example — Numeric Formats

##### Input Code:

##### Sql Server

Copy code

```
SELECT
 FORMAT(value, '00.00') as formatted,
 FORMAT(value, '#,##0') as formatSource
 FROM MY_TABLE;
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
 TO_CHAR(value, 'FM9999999999900.00') /*** SSC-FDM-0036 - TRANSFORMATION OF '00.00' FORMAT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ as formatted,
 TO_CHAR(value, 'FM9,999,999,999,990') /*** SSC-FDM-0036 - TRANSFORMATION OF '#,##0' FORMAT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ as formatSource
 FROM
 MY_TABLE;
```

##### Result

Copy code

```
#############
```

#### Code Example — Date/Time Custom Format Specifiers

##### Input Code:

##### Sql Server

Copy code

```
SELECT FORMAT(CAST('12/12/2024' as datetime), 'dddd, MMMM dd yyyy HH:mm:ss.FFF');
```

##### Snowflake

Copy code

```
SELECT
 TO_CHAR(TO_TIMESTAMP_NTZ('12/12/2024'), 'DY, MMMM DD YYYY HH24:MI:SS.F3') /*** SSC-FDM-0036 - TRANSFORMATION OF dddd, MMMM dd yyyy HH:mm:ss.FFF FORMAT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/;
```

Tip

The generated `TO_TIMESTAMP_NTZ('12/12/2024')` relies on Snowflake’s `TIMESTAMP_INPUT_FORMAT` session parameter for date parsing. If your session uses a non-default format, you may need to set it explicitly (e.g., `ALTER SESSION SET TIMESTAMP_INPUT_FORMAT = 'MM/DD/YYYY'`).

Note

The following date/time format specifiers are translated with this FDM marker due to behavioral differences between SQL Server and Snowflake:

| SQL Server Specifier | Snowflake Equivalent | Difference |
| --- | --- | --- |
| `dddd` (full day name) | `DY` (abbreviated day name) | Snowflake `DY` returns abbreviated names (e.g., “Mon”) instead of full names (e.g., “Monday”) |
| `F` through `FFFFFFF` (fractional seconds, no trailing zeros) | `F1` through `F7` | Snowflake `F1`–`F7` always include trailing zeros, unlike SQL Server uppercase `F` specifiers which suppress them |
| `z` (UTC offset hours) | `TZH` | Formatting differences in timezone offset representation |

Expand

Show lessSee more

#### Best Practices

- If the numeric digit does not fit in the format, please update the format by adding more digits based on the possible input data values.
- For date/time formats flagged with this FDM, review the Snowflake output to verify it matches your application’s expected format. You may need to apply additional string manipulation to achieve the exact SQL Server behavior.

## SSC-FDM-0037

Statistics function not needed in Snowflake.

### Description

DROP, COLLECT, or HELP statistics are not needed in Snowflake. Snowflake already collects statistics used for automatic query optimization.

#### Example Code

##### Input Code:

Copy code

```
  HELP STATISTICS TestName;
```

##### Generated Code

Copy code

```
  ----** SSC-FDM-0037 - HELP STATISTICS NOT NEEDED. SNOWFLAKE AUTOMATICALLY COLLECTS STATISTICS. **
  --HELP STATISTICS TestName
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0038

Micro-partitioning is automatically performed on all Snowflake tables.

### Description

This message is added to the CREATE TABLE statement when a PARTITION BY clause is present. The PARTITION BY clause, which controls table partitioning in some databases, is not supported in Snowflake.

In Snowflake, all tables are automatically divided into micro-partitions—contiguous units of storage ranging from 50 MB to 500 MB of uncompressed data. This architecture enables highly granular pruning of large tables, which may consist of millions of micro-partitions.

Snowflake automatically stores metadata for each micro-partition, including:

- The range of values for each column in the micro-partition.
- The number of distinct values.
- Additional properties used for optimization and efficient query processing.

Tables are transparently partitioned based on the order of data as it is inserted or loaded. For more details, see the [Benefits of Micro-partitioning](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions#benefits-of-micro-partitioning).

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE orders 
    (
      storeid INTEGER NOT NULL,
      productid INTEGER NOT NULL,
      orderdate DATE FORMAT 'yyyy-mm-dd' NOT NULL,
      totalorders INTEGER NOT NULL)
      PRIMARY INDEX (storeid, productid) 
      PARTITION BY (RANGE_N(totalorders BETWEEN *, 100, 1000 AND *),RANGE_N(orderdate BETWEEN *, '2005-12-31' AND *) );
```

##### Generated Code

Copy code

```
CREATE OR REPLACE TABLE orders
(
 storeid INTEGER NOT NULL,
 productid INTEGER NOT NULL,
 orderdate DATE NOT NULL,
 totalorders INTEGER NOT NULL)
-- --** SSC-FDM-0038 - MICRO-PARTITIONING IS AUTOMATICALLY HANDLED ON ALL SNOWFLAKE TABLES **
-- PARTITION BY (RANGE_N(totalorders BETWEEN *, 100, 1000 AND *)
--              ,RANGE_N(orderdate BETWEEN *, '2005-12-31' AND *) )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "09/17/2025",  "domain": "no-domain-provided" }}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0039

SQLWARNING may not be captured as an exception in Snowflake.

### Description

In source databases such as Teradata, SQLWARNING can be caught in exception handlers. Snowflake’s exception handling may not capture SQLWARNING in the same way. When a handler is configured to catch SQLWARNING, it is translated, but the behavior in Snowflake may differ.

#### Example Code

##### Input Code:

Copy code

```
 UPDATE orders SET status = 'processed';
DECLARE sqlwarning CONDITION FOR SQLSTATE '01000';
DECLARE EXIT HANDLER FOR sqlwarning
  INSERT INTO log_table VALUES ('Warning occurred');
```

##### Generated Code:

Copy code

```
 UPDATE orders SET status = 'processed';
DECLARE sqlwarning CONDITION FOR SQLSTATE '01000';
DECLARE EXIT HANDLER FOR
  --** SSC-FDM-0039 - SQLWARNING MAY NOT BE CAPTURED AS AN EXCEPTION IN SNOWFLAKE. **
  sqlwarning
  INSERT INTO log_table VALUES ('Warning occurred');
```

#### Best Practices

- Review exception handling logic that catches SQLWARNING; the handler may not be invoked in Snowflake for the same conditions.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0040

REGEXP\_SUBSTR / REGEXP\_INSTR function may fail if regex argument is not POSIX

### Description

When translating regex-based functions (such as REGEXP\_SUBSTR, REGEXP\_INSTR) from source dialects to Snowflake, the regex argument must be valid POSIX syntax. Source dialects may support extended regex features that Snowflake does not. If the regex pattern uses non-POSIX syntax, the function may fail at runtime or produce different results.

#### Example Code

##### Input Code:

Copy code

```
 SELECT REGEXP_INSTR(product_name, format_pattern) FROM products;
```

##### Generated Code:

Copy code

```
 SELECT
  --** SSC-FDM-0040 - REGEXP_INSTR FUNCTION MAY FAIL IF REGEX ARGUMENT IS NOT POSIX **
  REGEXP_INSTR(product_name, format_pattern)
FROM products;
```

#### Best Practices

- Ensure regex patterns use POSIX-compliant syntax.
- Test regex functions with sample data after conversion.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0041

Default parameters were reordered to the end of the parameter list.

### Description

Snowflake requires all parameters with default values to appear after all non-default parameters. When a procedure whose default parameters are not at the end of the parameter list is detected, they are automatically reordered. Code that uses positional arguments may need to be updated to match the new parameter order.

Note

This FDM replaces the deprecated [SSC-EWI-0002](../conversion-issues/generalEWI#ssc-ewi-0002), which previously only warned about the issue without performing the reorder.

#### Example Code

##### Input Code (SQL Server):

Copy code

```
 CREATE PROCEDURE dbo.TestProc (@Param1 INT = 10, @Param2 VARCHAR(50))
AS
BEGIN
   SET @Param1 = @Param1;
END
```

##### Generated Code (SQL Server):

Copy code

```
 CREATE OR REPLACE PROCEDURE dbo.TestProc
--** SSC-FDM-0041 - DEFAULT PARAMETERS WERE REORDERED TO THE END OF THE PARAMETER LIST TO MATCH SNOWFLAKE REQUIREMENTS. CALLERS USING POSITIONAL ARGUMENTS MAY NEED TO BE UPDATED **
(PARAM2 STRING, PARAM1 INT DEFAULT 10)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    PARAM1 := :PARAM1;
  END;
$$;
```

##### Input Code (Oracle):

Copy code

```
 CREATE OR REPLACE PROCEDURE TestProc (param1 IN NUMBER DEFAULT 10, param2 IN VARCHAR2)
IS
BEGIN
   param1 := param1;
END;
```

##### Generated Code (Oracle):

Copy code

```
 CREATE OR REPLACE PROCEDURE TestProc
--** SSC-FDM-0041 - DEFAULT PARAMETERS WERE REORDERED TO THE END OF THE PARAMETER LIST TO MATCH SNOWFLAKE REQUIREMENTS. CALLERS USING POSITIONAL ARGUMENTS MAY NEED TO BE UPDATED **
(param2 VARCHAR, param1 NUMBER(38, 18) DEFAULT 10)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    param1 := :param1;
  END;
$$;
```

##### Positional Call Site Conversion

When callers use positional arguments and the parameters have been reordered, they are automatically converted to named arguments:

Copy code

```
 CREATE PROCEDURE dbo.CallerProc
AS
BEGIN
   EXEC dbo.TestProc 5, 'hello';
END
```

Copy code

```
 CREATE OR REPLACE PROCEDURE dbo.CallerProc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    CALL dbo.TestProc(PARAM1 => 5, PARAM2 => 'hello');
  END;
$$;
```

#### Best Practices

- Review all callers of the affected procedure. If positional arguments are used, update them to match the new parameter order or convert them to named arguments.
- Consider using named arguments (e.g., `param1 => value`) instead of positional arguments to avoid issues with parameter ordering.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0042

Interval qualifier changed to DAY TO SECOND, Snowflake does not support mixing year to month and day to second time parts.

### Description

This FDM is emitted when the `--UseIntervalDatatype` preview flag is enabled in the SnowConvert AI Desktop application and a source INTERVAL type is converted to `INTERVAL DAY TO SECOND` regardless of its original qualifier. This applies to languages such as BigQuery, PostgreSQL, Greenplum, and Netezza, where **all** INTERVAL types (whether unqualified, `DAY TO SECOND`, or `YEAR TO MONTH`) are normalized to `INTERVAL DAY TO SECOND`.

The reason for this transformation is that these languages allow mixing intervals from the `YEAR TO MONTH` and `DAY TO SECOND` families in all kinds of operations (addition, subtraction, inserts, updates, and so on). This behavior breaks the ANSI SQL standard for the INTERVAL data type, which Snowflake’s implementation is based on. To avoid runtime errors caused by mixing the two interval families, `DAY TO SECOND` is forced across the entire migration. This approach ensures there are no exceptions related to mixed interval families while minimizing the precision loss inherent to such a type change.

For languages that enforce explicit qualifiers and do not allow mixing (such as Oracle and Teradata), the original qualifier is preserved and this FDM is not emitted.

For more details on how interval types are handled across languages, see the [Interval Data Types](../../translation-references/general/interval-data-types) translation reference.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE intervals (
    COL1 INTERVAL
);
```

##### Generated Code (BigQuery):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE intervals (
    COL1 INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/
)
;
```

##### Input Code (PostgreSQL):

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  CAST(someColumn AS INTERVAL YEAR TO MONTH),
  someColumn::INTERVAL YEAR TO MONTH
FROM someTable;
```

##### Generated Code (PostgreSQL):

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  CAST(someColumn AS INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/),
  someColumn :: INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/
FROM someTable;
```

#### Best Practices

- Review all converted INTERVAL columns and expressions in the migrated code. Because the source language allows mixing `YEAR TO MONTH` and `DAY TO SECOND` interval families, every INTERVAL is normalized to `DAY TO SECOND` to prevent runtime errors in Snowflake. Verify that this choice is acceptable for your data.
- If any source columns store year-to-month durations exclusively (for example, subscription lengths or contract terms), the `DAY TO SECOND` normalization may lose semantic meaning. Consider manually changing those specific columns to `INTERVAL YEAR TO MONTH` after migration, but only after confirming that they are never mixed with `DAY TO SECOND` intervals in your queries.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0043

Array size limit removed. Snowflake arrays are dynamically sized.

### Severity

None (functional difference)

### Description

Several source dialects let you bind a fixed maximum size to an array-style user-defined type — for example Oracle `VARRAY(n) OF <type>` and Db2 `<type> ARRAY[n]`. Snowflake `ARRAY` is a single, dynamically-sized type and does not preserve a maximum cardinality at the type level, so the size argument is dropped and this FDM is emitted to flag the behavioral difference.

This issue is dialect-agnostic and is emitted by both the Oracle (`CREATE TYPE … AS VARRAY(n) OF …`) and Db2 (`CREATE [DISTINCT] TYPE … AS <type> ARRAY[n]`) `CREATE TYPE` translators. It supersedes the previous Oracle-specific issue [SSC-FDM-OR0051](./oracleFDM#ssc-fdm-or0051).

#### Example Code

##### Input Code (Oracle):

Copy code

```
CREATE TYPE PhoneNumbers AS VARRAY(10) OF VARCHAR2(20);
```

##### Generated Code (Oracle):

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '10' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE PhoneNumbers AS ARRAY ( VARCHAR(20) );
```

##### Input Code (Db2):

Copy code

```
CREATE TYPE INT_ARRAY AS INTEGER ARRAY[100];
```

##### Generated Code (Db2):

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '100' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE INT_ARRAY AS ARRAY ( INTEGER );
```

#### Best Practices

- If application logic depends on a maximum array size, enforce the limit outside the type definition — for example with a check constraint or application-level validation — because Snowflake will silently accept values that exceed the original cardinality.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0044

CHECK constraint added inside procedural object will not validate existing data in Snowflake

### Description

This FDM is emitted when an `ALTER TABLE ... ADD CONSTRAINT CHECK` statement appears inside a stored procedure or user-defined function. In Snowflake, CHECK constraints added via `ALTER TABLE` do **not** validate existing data in the table — they only apply to new inserts and updates after the constraint is created. This differs from some source databases where adding a CHECK constraint may validate existing rows.

When the constraint is defined inside a procedural object (stored procedure or UDF), it is especially important to understand this behavior because:

- The constraint may not be enforced against data that was already in the table before the procedure was executed
- Application logic may incorrectly assume that all existing data meets the constraint after the procedure runs

The FDM annotation identifies the type of procedural object (e.g., “STORED PROCEDURE” or “USER-DEFINED FUNCTION”) to help you locate and review the logic.

#### Example Code

##### Example 1: CHECK Constraint Added Inside Stored Procedure

###### Input Code (SQL Server):

Copy code

```
CREATE PROCEDURE TestProc AS
BEGIN
  ALTER TABLE MyTable ADD CONSTRAINT CHK_Price CHECK (Price > 0);
END;
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE TestProc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-0044 - CHECK CONSTRAINT ADDED INSIDE STORED PROCEDURE WILL NOT VALIDATE EXISTING DATA IN SNOWFLAKE **
    ALTER TABLE MyTable
    ADD CONSTRAINT CHK_Price CHECK (Price > 0);
  END;
$$;
```

##### Example 2: CHECK Constraint Added Inside User-Defined Function

###### Input Code (SQL Server):

Copy code

```
CREATE FUNCTION TestFunc() RETURNS INT AS
BEGIN
  ALTER TABLE MyTable ADD CONSTRAINT CHK_Age CHECK (Age >= 18);
  RETURN 1;
END;
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE FUNCTION TestFunc ()
RETURNS INT
LANGUAGE SQL
AS
$$
  BEGIN
    --** SSC-FDM-0044 - CHECK CONSTRAINT ADDED INSIDE USER-DEFINED FUNCTION WILL NOT VALIDATE EXISTING DATA IN SNOWFLAKE **
    ALTER TABLE MyTable
    ADD CONSTRAINT CHK_Age CHECK (Age >= 18);
    RETURN 1;
  END;
$$;
```

##### Example 3: CHECK Constraint at Top Level (No FDM)

When the `ALTER TABLE ... ADD CONSTRAINT CHECK` statement appears at the top level (outside any procedural object), the FDM is **not** emitted because the behavioral difference is less surprising in that context.

###### Input Code (SQL Server):

Copy code

```
ALTER TABLE MyTable ADD CONSTRAINT CHK_Price CHECK (Price > 0);
```

###### Generated Code:

Copy code

```
ALTER TABLE MyTable
ADD CONSTRAINT CHK_Price CHECK (Price > 0);
```

#### Best Practices

- **Validate existing data explicitly**: After adding a CHECK constraint in a stored procedure, consider adding a `SELECT` statement to audit existing rows that violate the constraint:

  Copy code

  ```
  -- Add the constraint
  ALTER TABLE MyTable ADD CONSTRAINT CHK_Price CHECK (Price > 0);

  -- Audit existing violations
  SELECT * FROM MyTable WHERE NOT (Price > 0);
  ```
- **Fix violations before adding constraint**: If you expect all existing data to meet the constraint, update or delete non-compliant rows before adding the constraint
- **Document the limitation**: Add comments in your migrated code explaining that the constraint only applies to new data, not existing rows
- **Consider refactoring**: If the procedural object’s purpose is to enforce data quality, consider alternative approaches such as:
  - Adding the CHECK constraint during table creation (in DDL scripts) rather than in a procedure
  - Using streams and tasks to continuously validate data
  - Implementing validation logic in the application layer before data reaches Snowflake
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0045

DISABLE/ENABLE CONSTRAINT is not supported in Snowflake. DROP/ADD CONSTRAINT is used as a workaround.

#### Description

Snowflake does not support enabling or disabling a constraint, so SnowConvert AI uses `DROP CONSTRAINT` or `ADD CONSTRAINT` as a workaround. Review the generated operation because dropping or recreating a constraint does not preserve its source enabled state.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
ALTER TABLE dbo.FactPoolSummary NOCHECK CONSTRAINT DimPoolFKFactPoolSummary01;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-0045 - DISABLE/ENABLE CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE. DROP/ADD CONSTRAINT IS USED AS A WORKAROUND. **
ALTER TABLE IF EXISTS dbo.FactPoolSummary DROP CONSTRAINT DimPoolFKFactPoolSummary01 ;
```

#### Best Practices

- Review the generated `DROP CONSTRAINT` or `ADD CONSTRAINT` operation because it does not preserve the source constraint’s enabled/disabled state.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0046

Unsupported check constraint clause removed

### Description

This FDM is emitted when Oracle-specific state clauses are removed from CHECK constraints during conversion. Snowflake CHECK constraints do not support constraint state options such as `DEFERRABLE`, `RELY`, `INITIALLY`, `ENABLE`, or `DISABLE`. These clauses control when and how constraints are validated in Oracle, but have no equivalent in Snowflake.

The removed clauses include:

- **`[NOT] DEFERRABLE`**: Controls whether constraint validation can be deferred until transaction commit. Snowflake always validates CHECK constraints immediately on insert/update.
- **`[NOT] RELY`**: Hints to the Oracle optimizer whether the constraint is trusted. Snowflake does not have this optimization concept for CHECK constraints.
- **`INITIALLY IMMEDIATE` / `INITIALLY DEFERRED`**: Sets the default validation timing for deferrable constraints. Not applicable in Snowflake.
- **`ENABLE` / `DISABLE`**: Controls whether the constraint is actively enforced. Snowflake CHECK constraints are always enforced once created (use `ALTER TABLE DROP CONSTRAINT` to remove them entirely).

When multiple state clauses are present, they are all removed and the FDM annotation lists them together (e.g., “UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] DEFERRABLE, [NOT] RELY”).

#### Example Code

##### Example 1: NOT DEFERRABLE Clause Removed (Column-Level)

###### Input Code (Oracle):

Copy code

```
CREATE TABLE MyTable (
  col1 NUMBER CONSTRAINT chk1 CHECK (col1 > 0) NOT DEFERRABLE
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE MyTable (
  col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
                                                                                                         --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] DEFERRABLE **
                                                                                                         CONSTRAINT chk1 CHECK (col1 > 0)
)
;
```

##### Example 2: RELY Clause Removed (Column-Level)

###### Input Code (Oracle):

Copy code

```
CREATE TABLE MyTable (
  col1 NUMBER CONSTRAINT chk1 CHECK (col1 > 0) RELY
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE MyTable (
  col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
                                                                                                         --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] RELY **
                                                                                                         CONSTRAINT chk1 CHECK (col1 > 0)
)
;
```

##### Example 3: Multiple State Clauses Removed

###### Input Code (Oracle):

Copy code

```
CREATE TABLE MyTable (
  col1 NUMBER CONSTRAINT chk1 CHECK (col1 > 0) NOT DEFERRABLE RELY
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE MyTable (
  col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
                                                                                                         --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] DEFERRABLE, [NOT] RELY **
                                                                                                         CONSTRAINT chk1 CHECK (col1 > 0)
)
;
```

##### Example 4: NOT DEFERRABLE in Table-Level Constraint

###### Input Code (Oracle):

Copy code

```
CREATE TABLE accounts (
  account_id NUMBER NOT NULL,
  balance NUMBER(15, 2),
  CONSTRAINT chk_balance CHECK (balance >= -1000) NOT DEFERRABLE
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE accounts (
  account_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ NOT NULL,
  balance NUMBER(15, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] DEFERRABLE **
  CONSTRAINT chk_balance CHECK(balance >= -1000)
)
;

#### Best Practices

* **Immediate validation**: Understand that all Snowflake CHECK constraints validate immediately on insert/update. If your Oracle code relied on deferred validation to allow intermediate constraint violations within a transaction, you may need to adjust your transaction logic or remove the constraint.
* **RELY optimization**: The Oracle `RELY` clause signals that the optimizer can trust the constraint without validating it. Snowflake's query optimizer does not currently use CHECK constraints for optimization, so this is not a functional loss.
* **DISABLE clause**: If a CHECK constraint was marked `DISABLE` in Oracle, it will be converted to Snowflake but will be **enforced** (since Snowflake has no "disabled constraint" concept). Review disabled constraints and consider:
  - Commenting them out entirely if they should not be enforced
  - Dropping them after migration with `ALTER TABLE DROP CONSTRAINT`
  - Fixing any data that would violate the constraint before enabling it
* **Transaction boundaries**: If your Oracle code used `SET CONSTRAINT ... DEFERRED`, you may need to refactor the transaction logic to avoid intermediate violations
* If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0047

Error logging clause removed; base table not in migration scope

### Description

This FDM is emitted when Oracle's `DBMS_ERRLOG.CREATE_ERROR_LOG()` call or Teradata's `CREATE ERROR TABLE ... FOR` statement is found **without** the corresponding base table's `CREATE TABLE` in scope. In Snowflake, error logging is enabled via the `ERROR_LOGGING = TRUE` table property rather than through a separate error-log table.

When the base table is in scope, SnowConvert automatically adds `ERROR_LOGGING = TRUE` to the migrated `CREATE TABLE` and removes the Oracle/Teradata construct silently (no FDM). When the base table is **not** in scope, SnowConvert cannot apply that property automatically, so it comments out the construct and emits this FDM with guidance for manual follow-up.

The same FDM is also emitted for DML statements that carry an error-logging clause (Oracle `INSERT`/`UPDATE`/`MERGE` with `LOG ERRORS INTO`; Teradata `INSERT`/`MERGE` with `LOGGING [ALL] ERRORS`) when the base table is not in scope.

#### Example Code

##### Example 1: Oracle — DBMS_ERRLOG.CREATE_ERROR_LOG without base table in scope

###### Input Code (Oracle):

{/* code title="IN -> Oracle_01.sql" */}
```sql

EXEC DBMS_ERRLOG.CREATE_ERROR_LOG('SALES.ORDERS', 'ERR$_ORDERS');
```

###### Generated Code:

Copy code

```
----** SSC-FDM-0047 - ERROR LOG CLAUSE REMOVED; BASE TABLE NOT IN MIGRATION SCOPE. TO ENABLE ERROR LOGGING, EXECUTE 'ALTER TABLE SALES.ORDERS SET ERROR_LOGGING = TRUE'. READ ERRORS WITH 'ERROR_TABLE(SALES.ORDERS)'. **
--DBMS_ERRLOG.CREATE_ERROR_LOG('SALES.ORDERS', 'ERR$_ORDERS')
```

##### Example 2: Teradata — CREATE ERROR TABLE without base table in scope

###### Input Code (Teradata):

Copy code

```
CREATE ERROR TABLE err_sales_orders FOR sales_orders;
```

###### Generated Code:

Copy code

```
----** SSC-FDM-0047 - ERROR LOG CLAUSE REMOVED; BASE TABLE NOT IN MIGRATION SCOPE. TO ENABLE ERROR LOGGING, EXECUTE 'ALTER TABLE sales_orders SET ERROR_LOGGING = TRUE'. READ ERRORS WITH 'ERROR_TABLE(sales_orders)'. **
--CREATE ERROR TABLE err_sales_orders FOR sales_orders ;
```

#### Best Practices

- Run `ALTER TABLE <base_table> SET ERROR_LOGGING = TRUE` in Snowflake to enable error logging on the target table before executing DML that previously relied on the error-log table.
- Read captured errors with `SELECT * FROM ERROR_TABLE(<base_table>)` — no separate error table object is required.
- If the base table’s `CREATE TABLE` can be added to the migration input, SnowConvert will handle the `ERROR_LOGGING = TRUE` property automatically and suppress this FDM.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0048

Unsupported virtual columns, view created as a workaround.

### Description

Snowflake virtual columns must use deterministic expressions. When a source table defines a computed / virtual / generated column whose expression Snowflake cannot represent inline — a non-deterministic function (e.g. `GETDATE()`, `NEWID()`, `RAND()` in SQL Server; `SYS_GUID()`, `USERENV()`, `SYS_CONTEXT()` in Oracle; `RAND()`, `GENERATE_UNIQUE()`, `IDENTITY_VAL_LOCAL()` in DB2; `RANDOM()`, `GEN_RANDOM_UUID()`, `CLOCK_TIMESTAMP()` in PostgreSQL), a user-defined function, or a SnowConvert UDF-helper function — That column is removed from the `CREATE TABLE` and a compensating view named `<table>_View` is created in a separate view file. The view re-projects the base columns together with the unsupported expression(s), so the original column set remains available. `SELECT` statements that reference the original table are repointed to the generated view. This FDM is emitted on the `CREATE TABLE`, listing the reason(s) the workaround was required.

Supported computed columns — deterministic expressions such as `price * quantity` — are preserved inline as Snowflake virtual columns and do not trigger this FDM.

#### Example Code

##### Example 1: SQL Server — computed column using GETDATE()

###### Input Code (SQL Server):

Copy code

```
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY,
    created_at DATETIME DEFAULT GETDATE(),
    age_in_days AS (DATEDIFF(DAY, created_at, GETDATE()))
);
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0048 - UNSUPPORTED VIRTUAL COLUMN(S), VIEW audit_log_View CREATED AS A WORKAROUND. REASON(S): Non-deterministic functions. **
CREATE OR REPLACE TABLE audit_log (
    log_id INT PRIMARY KEY,
    created_at TIMESTAMP_NTZ(3) DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP_NTZ(3)
)
;
```

##### Example 2: Oracle — virtual column using SYS\_GUID()

###### Input Code (Oracle):

Copy code

```
CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    order_guid VARCHAR2(36) GENERATED ALWAYS AS (SYS_GUID()) VIRTUAL
);
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0048 - UNSUPPORTED VIRTUAL COLUMN(S), VIEW orders_View CREATED AS A WORKAROUND. REASON(S): Non-deterministic functions. **
CREATE OR REPLACE TABLE orders (
  order_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY
)
;
```

##### Example 3: DB2 — generated column using RAND()

###### Input Code (DB2):

Copy code

```
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    random_value DOUBLE GENERATED ALWAYS AS (RAND())
);
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0048 - UNSUPPORTED VIRTUAL COLUMN(S), VIEW orders_View CREATED AS A WORKAROUND. REASON(S): Non-deterministic functions. **
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY
)
;
```

##### Example 4: PostgreSQL — generated column using GEN\_RANDOM\_UUID()

###### Input Code (PostgreSQL):

Copy code

```
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    guid_col UUID GENERATED ALWAYS AS (GEN_RANDOM_UUID()) STORED
);
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0048 - UNSUPPORTED VIRTUAL COLUMN(S), VIEW audit_log_View CREATED AS A WORKAROUND. REASON(S): Non-deterministic functions. **
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY
)
;
```

##### Example 5: SQL Server — queries are repointed to the generated view

###### Input Code (SQL Server):

Copy code

```
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY,
    created_at DATETIME DEFAULT GETDATE(),
    age_in_days AS (DATEDIFF(DAY, created_at, GETDATE()))
);

SELECT * FROM audit_log;
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0048 - UNSUPPORTED VIRTUAL COLUMN(S), VIEW audit_log_View CREATED AS A WORKAROUND. REASON(S): Non-deterministic functions. **
CREATE OR REPLACE TABLE audit_log (
    log_id INT PRIMARY KEY,
    created_at TIMESTAMP_NTZ(3) DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP_NTZ(3)
)
;

SELECT
    *
FROM
    audit_log_View;
```

#### Best Practices

- The compensating `<table>_View` is written to a separate view file in the output. Deploy that view alongside the migrated table so queries that reference the unsupported columns continue to work.
- Where possible, replace non-deterministic computed columns with application logic or scheduled processes that populate a regular column, since their values are evaluated per row rather than recomputed on read.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0049

DELETE with error logging clause: Snowflake DELETE has no row-level validation

### Description

This FDM is emitted when a `DELETE` statement contains a `LOG ERRORS INTO` clause. Snowflake’s `DELETE` statement does not have row-level error capture — it either succeeds or fails atomically — so there is no direct equivalent for this clause. SnowConvert comments out the `LOG ERRORS INTO` clause and emits this FDM to alert the user that manual error-handling logic may be required.

#### Example Code

##### Example 1: DELETE with LOG ERRORS INTO clause

###### Input Code (Oracle):

Copy code

```
DELETE FROM delete_table
LOG ERRORS INTO error_log_my_table12 ('something') REJECT LIMIT UNLIMITED;
```

###### Generated Code:

Copy code

```
DELETE FROM
  delete_table
----** SSC-FDM-0049 - SNOWFLAKE DELETE HAS NO ROW-LEVEL VALIDATION; LOG ERRORS HAS NO DIRECT EQUIVALENT. MANUAL ERROR HANDLING MAY BE REQUIRED. **
--LOG ERRORS INTO error_log_my_table12 ('something') REJECT LIMIT UNLIMITED
;
```

#### Best Practices

- Consider wrapping the `DELETE` in a stored procedure that uses a `TRY … CATCH` (or `EXCEPTION` block in Snowpark) to handle failures and log them manually.
- If auditing deleted rows is required, capture them with a `SELECT INTO` before the `DELETE` and insert them into a dedicated log table.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0050

Error logging table removed; not required in Snowflake

### Description

This FDM is emitted when SnowConvert detects a `CREATE TABLE` statement that represents an Oracle or Teradata error-logging table. These tables are commented out because Snowflake’s built-in `ERROR_TABLE()` function replaces their role — no physical error-log table needs to exist.

SnowConvert identifies Oracle error-logging tables by:

- A table name beginning with `ERR$_` (Oracle-generated by `DBMS_ERRLOG.CREATE_ERROR_LOG`)
- The presence of Oracle error-logging system columns (`ORA_ERR_NUMBER$`, `ORA_ERR_MESG$`, `ORA_ERR_ROWID$`, `ORA_ERR_OPTYP$`)

The FDM template argument is the **base table name** that the error table was associated with. Read errors with `SELECT * FROM ERROR_TABLE(<base_table>)`.

#### Example Code

##### Example 1: Table with ERR$\_ prefix (Oracle)

###### Input Code (Oracle):

Copy code

```
CREATE TABLE ERR$_employees (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$   VARCHAR2(2000),
    ORA_ERR_ROWID$  ROWID,
    ORA_ERR_OPTYP$  VARCHAR2(2),
    ORA_ERR_TAG$    VARCHAR2(2000),
    emp_id          VARCHAR2(4000)
);
```

###### Generated Code:

Copy code

```
----** SSC-FDM-0050 - EXPLICIT ERROR LOGGING TABLE REMOVED; NOT REQUIRED IN SNOWFLAKE. READ ERRORS WITH 'SELECT * FROM ERROR_TABLE(employees)'. **
--CREATE TABLE ERR$_employees (
--  ORA_ERR_NUMBER$ NUMBER,
--  ORA_ERR_MESG$ VARCHAR2(2000),
--  ORA_ERR_ROWID$ ROWID,
--  ORA_ERR_OPTYP$ VARCHAR2(2),
--  ORA_ERR_TAG$ VARCHAR2(2000),
--  emp_id VARCHAR2(4000)
--);
```

##### Example 2: Table identified by ORA\_ERR\_\* columns

###### Input Code (Oracle):

Copy code

```
CREATE TABLE table_for_errors (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$   VARCHAR2(2000),
    ORA_ERR_ROWID$  ROWID,
    ORA_ERR_OPTYP$  VARCHAR2(2),
    ORA_ERR_TAG$    VARCHAR2(2000),
    emp_id          VARCHAR2(4000)
);
```

###### Generated Code:

Copy code

```
----** SSC-FDM-0050 - EXPLICIT ERROR LOGGING TABLE REMOVED; NOT REQUIRED IN SNOWFLAKE. READ ERRORS WITH 'SELECT * FROM ERROR_TABLE(table_for_errors)'. **
--CREATE TABLE table_for_errors (
--  ORA_ERR_NUMBER$ NUMBER,
--  ORA_ERR_MESG$ VARCHAR2(2000),
--  ORA_ERR_ROWID$ ROWID,
--  ORA_ERR_OPTYP$ VARCHAR2(2),
--  ORA_ERR_TAG$ VARCHAR2(2000),
--  emp_id VARCHAR2(4000)
--);
```

#### Best Practices

- The commented-out `CREATE TABLE` is preserved as a migration trace. Do not recreate these tables in Snowflake — they are not needed.
- Query captured errors using Snowflake’s built-in `ERROR_TABLE()` function: `SELECT * FROM ERROR_TABLE(<base_table>)`.
- `ERROR_TABLE()` is available only on tables that have `ERROR_LOGGING = TRUE` enabled. Ensure the base table was migrated with that property (or apply it manually with `ALTER TABLE <base_table> SET ERROR_LOGGING = TRUE`).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0051

Table looks like an error logging table but base table cannot be determined.

### Description

This FDM is emitted when SnowConvert detects a `CREATE TABLE` that resembles an Oracle error-logging table — either by the `ERR$_` prefix convention or by the presence of multiple `ORA_ERR_*` system columns — but cannot determine the associated base table name. This happens when:

- The table name starts with `ERR$_` but no `LOG ERRORS INTO` clause in the file references it (so the base table cannot be inferred from context)
- The table has Oracle error-system columns but lacks the canonical `ERR$_` prefix and no `LOG ERRORS INTO` reference exists

In this situation SnowConvert does **not** comment out the `CREATE TABLE` (because it cannot confirm the table is an error-log table with certainty) and instead emits this FDM as a warning for manual review.

#### Example Code

##### Example 1: ERR$\_-prefix table with no LOG ERRORS INTO reference

###### Input Code (Oracle):

Copy code

```
CREATE TABLE ERR$_employees (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$   VARCHAR2(2000),
    ORA_ERR_ROWID$  ROWID,
    ORA_ERR_OPTYP$  VARCHAR2(2),
    ORA_ERR_TAG$    VARCHAR2(2000),
    emp_id          VARCHAR2(4000)
);

SELECT * FROM ERR$_employees;
```

###### Generated Code:

Copy code

```
--** SSC-FDM-0051 - THIS TABLE LOOKS LIKE AN ERROR LOGGING TABLE BUT THE BASE TABLE CANNOT BE DETERMINED. REVIEW MANUALLY. **
CREATE OR REPLACE TABLE "ERR$_EMPLOYEES" (
  "ORA_ERR_NUMBER$" NUMBER(38, 18),
  "ORA_ERR_MESG$" VARCHAR(2000),
  "ORA_ERR_ROWID$" VARCHAR(18),
  "ORA_ERR_OPTYP$" VARCHAR(2),
  "ORA_ERR_TAG$" VARCHAR(2000),
  emp_id VARCHAR(4000)
)
;

SELECT
  *
FROM
  "ERR$_EMPLOYEES";
```

#### Best Practices

- Search the codebase for `LOG ERRORS INTO <table_name>` to confirm whether this table is indeed an error-log table and identify its base table.
- If the base table is confirmed, add a `LOG ERRORS INTO` reference so SnowConvert can resolve the association and emit `SSC-FDM-0050` with the correct base table name.
- If the table is unrelated to error logging, you can safely ignore this FDM.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0052

EXECUTE IMMEDIATE commented out because all of its dynamic SQL branches were commented out.

#### Description

SnowConvert AI comments out `EXECUTE IMMEDIATE` when every dynamic SQL branch that can reach it was also commented out. No executable statement remains, so replace the commented source-specific SQL with valid Snowflake SQL before running the procedure.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE PROC01
AS
BEGIN
  EXECUTE IMMEDIATE 'bad statement goes here';
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE PROC01 ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN -- --** SSC-FDM-0052 - EXECUTE IMMEDIATE COMMENTED OUT BECAUSE ALL OF ITS DYNAMIC SQL BRANCHES WERE COMMENTED OUT; NO EXECUTABLE STATEMENT REMAINS. ** -- EXECUTE IMMEDIATE 'bad statement goes here' NULL; END; $$;
```

#### Best Practices

- Replace the commented dynamic SQL with a valid Snowflake statement before invoking the procedure.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0053

Some dynamic SQL branches reaching this EXECUTE IMMEDIATE were commented out.

#### Description

SnowConvert AI emits this issue when one or more branches feeding `EXECUTE IMMEDIATE` were commented out during conversion. If a commented branch is selected at runtime, the statement can be empty, so review and replace every affected branch with valid Snowflake SQL.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
REPLACE PROCEDURE comment_exec_imm_mixed (IN flag INTEGER)
BEGIN
  DECLARE STATSSQL VARCHAR(500);
  IF flag = 1 THEN
    SET STATSSQL = 'COLLECT STATISTICS COLUMN(col1) ON db.tbl;';
  ELSE
    SET STATSSQL = 'SELECT 1;';
  END IF;
  EXECUTE IMMEDIATE STATSSQL;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE comment_exec_imm_mixed (FLAG INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    STATSSQL VARCHAR(500);
  BEGIN

    IF (flag = 1) THEN
      STATSSQL := '--COLLECT STATISTICS COLUMN (col1) ON db.tbl';
    ELSE
      STATSSQL := 'SELECT 1;';
    END IF;
    --** SSC-FDM-0053 - ONE OR MORE DYNAMIC SQL BRANCHES OF THIS EXECUTE IMMEDIATE WERE COMMENTED OUT; IF ONE OF THOSE BRANCHES IS SELECTED AT RUNTIME, EXECUTE IMMEDIATE WILL FAIL WITH AN EMPTY-STATEMENT ERROR. **
    --** SSC-FDM-0037 - COLLECT STATISTICS NOT NEEDED. SNOWFLAKE AUTOMATICALLY COLLECTS STATISTICS. **
    EXECUTE IMMEDIATE :STATSSQL;
  END;
$$;
```

#### Best Practices

- Review every branch that can assign the executed statement and replace commented branches with valid Snowflake SQL.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0054

Unicode replacement character (U+FFFD) detected and removed from source.

#### Description

SnowConvert AI treats a Unicode replacement character (`U+FFFD`) as whitespace because the original source character cannot be recovered. Compare identifiers and string literals near the marker with correctly encoded source text and restore any missing content.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT 1 AS �ABC FROM T1;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  1 AS /*** SSC-FDM-0054 - ENCODING ARTIFACT (U+FFFD) WAS DETECTED IN THE SOURCE AND TREATED AS WHITESPACE. THE ORIGINAL CHARACTER COULD NOT BE RECOVERED. VERIFY IDENTIFIERS AND STRING LITERALS NEAR THIS LOCATION IN THE CONVERTED OUTPUT. ***/ ABC
FROM
  T1;
```

#### Best Practices

- Compare the flagged location with the original source encoding and restore any missing identifier or string content manually.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0055

Alter Index is not applicable in Snowflake. Standard tables do not use user-managed indexes.

#### Description

SnowConvert AI comments out `ALTER INDEX` because standard Snowflake tables do not use user-managed indexes. Review the workload and use Snowflake clustering or search optimization only if the converted queries require it.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
ALTER INDEX index_name UNUSABLE;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-0055 - ALTER INDEX IS NOT APPLICABLE IN SNOWFLAKE. STANDARD TABLES DO NOT USE USER-MANAGED INDEXES. **
--ALTER INDEX index_name UNUSABLE
```

#### Best Practices

- Remove dependencies on user-managed indexes and evaluate Snowflake clustering or search optimization only when query performance requires it.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0130

SELECT \* over a remapped system object may return a different set of columns

#### Description

A `SELECT *` reads from a source system object that SnowConvert AI remapped to a Snowflake system object exposing a different set of columns, so the expanded column list may differ at runtime. In the example below `SYS.TABLES` is remapped to `INFORMATION_SCHEMA.TABLES`, and the emitted message is `'*' OVER SYSTEM OBJECT 'SYS.TABLES' MAY RETURN A DIFFERENT SET OF COLUMNS IN SNOWFLAKE. MANUAL REVIEW REQUIRED`.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
SELECT * FROM SYS.TABLES;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  * /*** SSC-FDM-0130 - '*' OVER SYSTEM OBJECT 'SYS.TABLES' MAY RETURN A DIFFERENT SET OF COLUMNS IN SNOWFLAKE. MANUAL REVIEW REQUIRED ***/
FROM
  INFORMATION_SCHEMA.TABLES;
```

#### Best Practices

- Replace `*` with the explicit source columns consumed downstream and review positional dependencies.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0131

Dynamic SQL code could not be parsed

#### Description

SnowConvert AI emits this issue when it cannot parse dynamic SQL and therefore leaves the statement unchanged for runtime execution. Validate the preserved statement in Snowflake and replace any remaining source-dialect syntax.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE PROCEDURE drop_col_tab(p_tab VARCHAR2) IS
BEGIN
  EXECUTE IMMEDIATE 'alter table ' || p_tab || ' drop column old_col';
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE drop_col_tab (p_tab VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-0131 - THE DYNAMIC SQL CODE COULD NOT BE PARSED, SO IT WAS LEFT UNCHANGED AND WILL BE EXECUTED AS-IS AT RUNTIME. PLEASE REVIEW THE GENERATED CODE. **
    EXECUTE IMMEDIATE 'alter table ' || NVL(:P_TAB :: STRING, '') || ' drop column old_col';
  END;
$$;
```

#### Best Practices

- Validate the preserved statement directly in Snowflake and rewrite any source-dialect syntax before deployment.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0133

TEMPORARY keyword removed for Hybrid Table

#### Description

Snowflake does not support temporary hybrid tables, so SnowConvert AI removes the `TEMPORARY` keyword. The generated hybrid table persists beyond the source table lifecycle, so review its cleanup and retention requirements.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE TABLE #orders_temp (
  order_id INT NOT NULL,
  customer_id INT,
  CONSTRAINT pk_orders_temp PRIMARY KEY (order_id)
);
```

##### Output Code:

##### Snowflake

```
HybridTablesSelected: 1
Issue code: SSC-FDM-0133
```

#### Best Practices

- Review lifecycle and cleanup requirements after the table becomes a permanent hybrid table.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0134

CLUSTER BY clause removed for Hybrid Table

#### Description

Snowflake hybrid tables do not support `CLUSTER BY`, so SnowConvert AI removes the clause. Review representative query performance and determine whether hybrid-table indexes provide the required access paths.

#### Code Example

##### Input Code:

##### Hive

Copy code

```
CREATE TABLE orders (
  order_id INT NOT NULL,
  bucket_id INT,
  CONSTRAINT pk_orders PRIMARY KEY (order_id)
)
CLUSTERED BY (bucket_id)
INTO 10 BUCKETS;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-0134 - CLUSTER BY IS NOT SUPPORTED ON HYBRID TABLES IN SNOWFLAKE. THE CLUSTER BY CLAUSE IS REMOVED AS A WORKAROUND. **
CREATE HYBRID TABLE orders (
   order_id INT NOT NULL,
   bucket_id INT,
   CONSTRAINT pk_orders PRIMARY KEY (order_id)
 )
;
```

#### Best Practices

- Test representative queries after migration and review whether hybrid-table indexes provide the required access paths.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0135

COLLATE clause removed from indexed column for Hybrid Table

#### Description

Snowflake hybrid tables do not support custom collation on indexed columns, so SnowConvert AI removes the `COLLATE` clause. Verify that comparisons, uniqueness, and sorting still match the source behavior.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE TABLE dbo.orders (
  order_id INT COLLATE Latin1_General_CI_AS NOT NULL,
  customer_id INT,
  CONSTRAINT pk_orders PRIMARY KEY (order_id)
)
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE HYBRID TABLE dbo.orders (
  --** SSC-FDM-0135 - CUSTOM COLLATION ON INDEXED COLUMNS IS NOT SUPPORTED ON HYBRID TABLES IN SNOWFLAKE. THE COLLATE CLAUSE IS REMOVED AS A WORKAROUND. **
  order_id INT NOT NULL,
  customer_id INT,
  CONSTRAINT pk_orders PRIMARY KEY (order_id)
)
;
```

#### Best Practices

- Verify sorting and comparison results for the indexed column under Snowflake’s resulting collation behavior.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0137

Multiple writers to the same target combined with UNION ALL.

#### Description

SnowConvert AI combines multiple writers to the same target with `UNION ALL` in one query. This does not preserve source-specific write order or intermediate target state, so review the model when writer order affects the final result.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<component
  refId="Package\Simple Data Flow\OLE DB Destination"
  componentClassID="Microsoft.OLEDBDestination"
  name="OLE DB Destination">
  <properties>
    <property name="OpenRowset">[dbo].[TargetTable]</property>
    <property name="AccessMode" typeConverter="AccessMode">3</property>
  </properties>
</component>
<component
  refId="Package\Simple Data Flow\OLE DB Destination 2"
  componentClassID="Microsoft.OLEDBDestination"
  name="OLE DB Destination 2">
  <properties>
    <property name="OpenRowset">[dbo].[TargetTable]</property>
    <property name="AccessMode" typeConverter="AccessMode">3</property>
  </properties>
</component>
```

##### Output Code:

##### Snowflake

Copy code

```
{{ config(
    alias='TargetTable'
) }}
--** SSC-FDM-0137 - MULTIPLE WRITERS TO THE SAME TARGET ARE COMBINED WITH UNION ALL IN A SINGLE QUERY. SOURCE-SPECIFIC WRITE ORDER OR INTERMEDIATE TARGET STATE IS NOT PRESERVED. REVIEW THE GENERATED MODEL IF WRITER ORDER AFFECTS THE FINAL RESULT. **
WITH source_1 AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      {{ ref('int_multicast') }}
),
source_2 AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      {{ ref('int_multicast') }}
)
SELECT
   sd.Id AS Id,
   sd.Name AS Name,
   sd.Value AS Value
FROM
   source_1 AS sd
UNION ALL
SELECT
   sd.Id AS Id,
   sd.Name AS Name,
   sd.Value AS Value
FROM
   source_2 AS sd
```

#### Best Practices

- Review whether writer order or intermediate target state affects results; split the generated model when order-dependent behavior must be preserved.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0138

Unresolved objects are assumed to be Hybrid Tables

#### Description

This FDM is generated when SnowConvert AI creates an inline stored procedure in Hybrid Table conversion mode and cannot resolve a referenced table’s type. The generated procedure assumes that each unresolved reference is a Snowflake Hybrid Table and identifies the affected object in the marker.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE update_order_status(p_order_id NUMBER, p_status VARCHAR2)
AS
BEGIN
  UPDATE orders SET status = p_status WHERE order_id = p_order_id;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-0138 - INLINE STORED PROCEDURE GENERATION ASSUMES THAT UNRESOLVED TABLE REFERENCES ARE SNOWFLAKE HYBRID TABLES: orders. VERIFY THE REFERENCED OBJECT TYPES BEFORE DEPLOYMENT. **
CREATE OR REPLACE INLINE PROCEDURE update_order_status (p_order_id NUMBER(38, 18), p_status VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
  BEGIN ATOMIC
    UPDATE orders
      SET
        status = p_status
      WHERE
        order_id = p_order_id;
  END;
$$;
```

#### Best Practices

- Verify that every object named in the marker is a Snowflake Hybrid Table.
- Resolve and convert referenced objects before relying on inline procedure generation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-0139

Inline Stored Procedure generation was not applied

#### Description

This FDM is generated when SnowConvert AI cannot create an inline stored procedure because the source procedure contains an unsupported feature. The marker identifies the blocking feature, and a standard Snowflake procedure is generated instead.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE commit_order(p_order_id NUMBER)
AS
BEGIN
  UPDATE orders SET status = 'DONE' WHERE order_id = p_order_id;
  COMMIT;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-0139 - INLINE STORED PROCEDURE GENERATION WAS NOT APPLIED BECAUSE THE PROCEDURE CONTAINS UNSUPPORTED FEATURES: explicit transaction control. A STANDARD SNOWFLAKE PROCEDURE IS GENERATED. **
CREATE OR REPLACE PROCEDURE commit_order (p_order_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    UPDATE orders
      SET
        status = 'DONE'
      WHERE
        order_id = p_order_id;
    --** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
    COMMIT;
  END;
$$;
```

#### Best Practices

- Review the unsupported feature named in the marker and decide whether the procedure can be redesigned for inline execution.
- Validate the generated standard procedure and its transaction behavior before deployment.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
