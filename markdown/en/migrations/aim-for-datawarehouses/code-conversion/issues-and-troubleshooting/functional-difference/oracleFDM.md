# Code Conversion - Oracle Functional Differences

## SSC-FDM-OR0001

Note

This FDM was added for an old version and is currently deprecated.

### Description

This error is related to the ***Assessment*** report file. It appears when an error occurs while writing the assessment details report file.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0002

The sequence start value exceeds the max value allowed by Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0068](../conversion-issues/oracleEWI#ssc-ewi-or0068) documentation

### Description

This error appears when the `START WITH` statement value exceeds the maximum value allowed by Snowflake. What Snowflake said about the start value is: *Specifies the first value returned by the sequence. Supported values are any value that can be represented by a 64-bit two’s compliment integer (from `-2^63` to `2^63-1`)*. So according to the previously mentioned, the max value allowed is **9223372036854775807** for positive numbers and **9223372036854775808** for negative numbers.

#### Example Code

##### Input Code:

Copy code

```
 CREATE SEQUENCE SEQUENCE1
START WITH 9223372036854775808;
```

Copy code

```
 CREATE SEQUENCE SEQUENCE2
START WITH -9223372036854775809;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE SEQUENCE SEQUENCE1
--** SSC-FDM-OR0002 - SEQUENCE START VALUE EXCEEDS THE MAX VALUE ALLOWED BY SNOWFLAKE. **
START WITH 9223372036854775808
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';
```

Copy code

```
 CREATE OR REPLACE SEQUENCE SEQUENCE2
--** SSC-FDM-OR0002 - SEQUENCE START VALUE EXCEEDS THE MAX VALUE ALLOWED BY SNOWFLAKE. **
START WITH -9223372036854775809
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';
```

#### Best Practices

- It can be recommended to just reset the sequence and modify its usage too. **NOTE**: the target column must have enough space for holding this value.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0003

Search clause removed from the with element statement.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0038](../conversion-issues/oracleEWI#ssc-ewi-or0038) documentation

### Description

The [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142) is employed to define the order in which rows are processed in a SELECT statement. This functionality allows for a customized traversal of the data, ensuring that the results are returned in a specific sequence based on the specified criteria. It is important to note, however, that this behavior, characterized by the [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142), is not supported in Snowflake.

In databases such as Oracle, the [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142) is commonly used in conjunction with recursive queries or common table expressions (CTEs) to influence the sequence in which hierarchical data is explored. By designating a particular column or set of columns in the [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142), you can control the depth-first or breadth-first traversal of the hierarchy, impacting the order in which rows are processed.

In Snowflake, [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142) message will be generated, and the [`search_clause`](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2077142) is subsequently eliminated.

#### Example Code

##### Input Code:

Copy code

```
 WITH dup_hiredate(eid, emp_last, mgr_id, reportLevel, hire_date, job_id) AS 
(SELECT aValue from atable) SEARCH DEPTH FIRST BY hire_date SET order1 SELECT aValue from atable;
```

##### Generated Code:

Copy code

```
 WITH dup_hiredate(eid, emp_last, mgr_id, reportLevel, hire_date, job_id) AS
(
SELECT aValue from
atable
) /*** SSC-FDM-OR0003 - SEARCH CLAUSE REMOVED FROM THE WITH ELEMENT STATEMENT ***/
SELECT aValue from
atable;
```

#### Recommendation

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0004

Siblings keyword removed from the order by clause because Snowflake does not support it.

### Description

In Oracle, the [ORDER BY SIBLINGS](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2171079) clause can be used in hierarchical queries to preserve the order of the data given by the hierarchy, while applying a reorder of the values that are siblings in the same hierarchy. This is not supported in Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 SELECT LEVEL,
       LPAD(' ', 2 * (LEVEL - 1)) || NAME AS FORMATTED_NAME,
       JOB_TITLE
FROM EMPLOYEES
START WITH MANAGER_ID IS NULL
CONNECT BY PRIOR EMPLOYEE_ID = MANAGER_ID
ORDER SIBLINGS BY NAME;
```

##### Generated Code:

Copy code

```
 SELECT LEVEL,
       NVL(
       LPAD(' ', 2 * (
                      !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!LEVEL - 1)) :: STRING, '') || NVL(NAME :: STRING, '') AS FORMATTED_NAME,
       JOB_TITLE
FROM
       EMPLOYEES
START WITH MANAGER_ID IS NULL
CONNECT BY
       PRIOR EMPLOYEE_ID = MANAGER_ID
ORDER BY
       NAME /*** SSC-FDM-OR0004 - SIBLINGS KEYWORD REMOVED FROM ORDER BY CLAUSE BECAUSE SNOWFLAKE DOES NOT SUPPORT IT ***/;
```

- While the exact same ordering achieved with the SIBLINGS clause might not be accessible, there are a few alternatives to get a similar result.
  - Embed the query within an outer query that applies the desired sorting using `ORDER BY`.
  - Create a CTE with the hierarchical query using `CONNECT BY` and reference the CTE in a subsequent query to apply `ORDER BY` for sibling sorting (rows at the same level).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0005

Synonyms are not supported in Snowflake but references to this synonym were changed by the original object name.

### Description

Synonyms are not supported in Snowflake. The synonyms are replaced by the original name.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE TABLE1
(
    COLUMN1 NUMBER
);

CREATE OR REPLACE SYNONYM B.TABLE1_SYNONYM FOR TABLE1;
SELECT * FROM B.TABLE1_SYNONYM WHERE B.TABLE1_SYNONYM.COLUMN1 = 20;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TABLE1
    (
        COLUMN1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;

--    --** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **

--    CREATE OR REPLACE SYNONYM B.TABLE1_SYNONYM FOR TABLE1
                                                         ;
SELECT * FROM
    TABLE1
    WHERE
    TABLE1.COLUMN1 = 20;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0006

Constraint state removed from not null inline constraint.

### Description

This warning occurs when the not null column constraint contains one of the following Oracle constraint states as part of the column inline definition:

Copy code

```
 [ RELY | NORELY | RELY DISABLE | RELY ENABLE | VALIDATE | NOVALIDATE ]
```

Snowflake does not support these states; therefore, they will be removed from the `NOT NULL` inline constraint.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE Table1(
  col1 INT NOT NULL RELY
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE Table1 (
    col1 INT NOT NULL /*** SSC-FDM-OR0006 - CONSTRAINT STATE RELY REMOVED FROM NOT NULL INLINE CONSTRAINT ***/
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
  ;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0007

Snowflake does not support the versioning of objects. Developers should consider alternate approaches for code versioning.

### Description

Snowflake doesn’t support the versioning of objects. The modifier EDITIONABLE or NONEDITIONABLE is removed in the converted code and a warning is added.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE EDITIONABLE PROCEDURE FUN1 (n number)is
l_result number;
begin
    DELETE FROM employees;
end;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-OR0007 - SNOWFLAKE DOESN'T SUPPORT VERSIONING OF OBJECTS. DEVELOPERS SHOULD CONSIDER ALTERNATE APPROACHES FOR CODE VERSIONING. **
CREATE OR REPLACE PROCEDURE FUN1 (n NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        l_result NUMBER(38, 18);
    BEGIN
        DELETE FROM
            employees;
    END;
$$;
```

#### Best Practices

- The user should consider alternate approaches for code versioning.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0008

Set Quantifier Not Supported

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0071](../conversion-issues/oracleEWI#ssc-ewi-or0071) documentation

### Description

Quantifier ‘all’ is not supported in Snowflake. The modifier is removed from the source code, and a warning is added; the resulting code may behave unexpectedly.

#### Example Code

##### Input Code:

Copy code

```
 SELECT location_id  FROM locations 
MINUS ALL 
SELECT location_id  FROM departments;
```

##### Generated Code:

Copy code

```
 SELECT location_id  FROM
locations
--** SSC-FDM-OR0008 - QUANTIFIER 'ALL' NOT SUPPORTED FOR THIS SET OPERATOR, RESULTS MAY DIFFER **
MINUS
SELECT location_id  FROM
departments;
```

In Snowflake, the `INTERSECT` and `MINUS/EXCEPT` operators will always remove duplicate values.

#### Best Practices

- Check alternatives in Snowflake to emulate the functionality of the “all” quantifier.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0009

SQL implicit cursor values may differ.

### Description

Note

Generate Procedures and Macros using JavaScript as the target language adding the following flag `-t JavaScript` or `--PLTargetLanguage JavaScript`

Note

Some parts in the output code are omitted for clarity reasons.

This EWI is shown when SQL implicit cursor value is used. This is because Oracle uses different values depending on the type of query. For example, for `SELECT` the value used to set SQL implicit cursor values are the number of rows returned by the query. When the query type is `UPDATE/CREATE/DELETE/INSERT` the value used is the number of rows affected, this is the main reason why this EWI is displayed.

#### Example Code

##### Input Code:

Copy code

```
-- Additional Params: -t JavaScript
--Transformation for implicit cursor
CREATE OR REPLACE PROCEDURE SP_SAMPLE AUTHID DEFINER IS
  stmt_no  POSITIVE;
BEGIN
  IF SQL%ROWCOUNT = 0 THEN
   EXIT ;
  END IF;
  IF SQL%ISOPEN THEN
   EXIT ;
  END IF;
  IF SQL%FOUND THEN
   EXIT ;
  END IF;
  IF SQL%NOTFOUND THEN
   EXIT ;
  END IF;
END;
```

##### Generated Code:

Copy code

```
 -- Additional Params: -t JavaScript
--Transformation for implicit cursor
CREATE OR REPLACE PROCEDURE SP_SAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
  !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PlInvokerRightsClause' NODE ***/!!!
  //AUTHID DEFINER
  null
  // SnowConvert AI Helpers Code section is omitted.

  let STMT_NO = new POSITIVE();
  if (SQL.ROWCOUNT /*** SSC-FDM-OR0009 - SQL IMPLICIT CURSOR VALUES MAY DIFFER ***/ == 0) {
    break;
  }
  if (SQL.ISOPEN) {
    break;
  }
  if (SQL.FOUND) {
    break;
  }
  if (SQL.NOTFOUND) {
    break;
  }
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0010

NUMBER datatype smaller precision was increased to match scale.

### Description

The `NUMBER` data type stores fixed and floating-point numbers. This data is portable among different operating systems running the Oracle Database. The `NUMBER` data type is recommended for most cases in which you must store numeric data. The syntax is the following `NUMBER (X, Y)`, where ***X*** is the precision and ***Y*** is the scale.

For example, `NUMBER(5, 3)` is a number that has ***2*** digits before the decimal and ***3*** digits after the decimal, just like the following:

Copy code

```
12.345
```

Another important considerations:

1. Scale ***Y*** specifies the maximum number of digits to the right of the decimal point.
2. Scale-Precision ***Y-X*** specifies the minimum number of zeros present after the decimal point.

This message is shown when a `NUMBER` has a smaller precision than its scale. Snowflake does not support this feature, and this message is used to indicate that the precision’s value was increased to maintain equivalence.

Note

:class: tip
Please consider that there are cases where this issue can either stack alongside other known transformations or not happen at all. For example, cases where the scale is replaced by nineteen and the former precision is greater than nineteen; will NOT show this message.

#### Example Code

##### Input Code:

##### Queries

Copy code

```
 CREATE TABLE SampleNumberTable(Col1 NUMBER(4, 5));

INSERT INTO SampleNumberTable (Col1)
VALUES (0.00009);

INSERT INTO SampleNumberTable (Col1)
VALUES (0.000021);

INSERT INTO SampleNumberTable (Col1)
VALUES (0.012678912);

SELECT * FROM SampleNumberTable;
```

##### Result

Copy code

```
Col1   |
-------+
0.00009|
0.00002|
0.01268|
```

##### Generated Code:

##### Queries

Copy code

```
 CREATE OR REPLACE TABLE SampleNumberTable (Col1 NUMBER(5, 5) /*** SSC-FDM-OR0010 - NUMBER DATATYPE SMALLER PRECISION WAS INCREASED TO MATCH SCALE ***/ /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO SampleNumberTable(Col1)
VALUES (0.00009);

INSERT INTO SampleNumberTable(Col1)
VALUES (0.000021);

INSERT INTO SampleNumberTable(Col1)
VALUES (0.012678912);

SELECT * FROM
SampleNumberTable;
```

##### Result

Copy code

```
Col1   |
-------+
0.00009|
0.00002|
0.01268|
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0011

The boolean argument was removed because the “add to stack” options is not supported.

### Description

This warning is displayed when the third optional argument of *RAISE\_APPLICATION\_ERROR* was removed during the migration. This functionality is not supported by Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE FUNCTION TEST(SAMPLE_A      IN NUMBER DEFAULT NULL,
                               SAMPLE_B       IN NUMBER DEFAULT NULL)
  RETURN NUMBER
 AS
BEGIN
    raise_application_error(-20001, 'First exception message', FALSE);
  RETURN 1;
END TEST;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE TEST (SAMPLE_A NUMBER(38, 18) DEFAULT NULL,
                               SAMPLE_B NUMBER(38, 18) DEFAULT NULL)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  FIRST_EXCEPTION_MESSAGE_EXCEPTION_CODE_0 EXCEPTION (-20001, 'FIRST EXCEPTION MESSAGE');
 BEGIN
  --** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT FALSE WAS REMOVED. **
  RAISE FIRST_EXCEPTION_MESSAGE_EXCEPTION_CODE_0;
  RETURN 1;
 END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0012

COMMIT and ROLLBACK statements require adequate setup to perform as intended.

### Description

COMMIT and ROLLBACK statements require adequate setup to perform as intended in Snowflake. The following instruction needs to be executed in Snowflake to simulate the correct functionality of these statements:

Copy code

```
 ALTER SESSION SET AUTOCOMMIT = false;
```

#### Example Code

##### Input Code

Copy code

```
 COMMIT;
ROLLBACK;
```

##### Generated Code

Copy code

```
 --** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
COMMIT;

--** SSC-FDM-OR0012 - ROLLBACK REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
ROLLBACK;
```

#### Best Practices

- Execute the query mentioned in the description section before you start to execute your code.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-OR0013

The cycle clause is not supported in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0039](../conversion-issues/oracleEWI#ssc-ewi-or0039) documentation.

### Description

This message is shown when a query with a CYCLE clause is found. It is not supported in Snowflake, so it is commented out from the code.

This clause marks when there is a recursion.

For more details see the [documentation](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/SELECT.html#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__GUID-8EE64250-3C9A-40C7-A81D-46695F8B2EB9) about the clause functionality.

#### Example Code

#### Connect By

##### Input Code:

Copy code

```
 CREATE OR REPLACE FORCE NONEDITIONABLE VIEW VIEW01 AS
SELECT
      UNIQUE A.*
FROM
      TABLITA A
WHERE
      A.X = A.C CONNECT BY NOCYCLE A.C = 0 START WITH A.B = 1
HAVING
      X = 1
GROUP BY
      A.C;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE VIEW VIEW01
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT DISTINCT
      A.*
FROM
      TABLITA A
WHERE
      A.X = A.C
GROUP BY
      A.C
HAVING
      X = 1
--** SSC-FDM-OR0013 - CYCLE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE **
CONNECT BY
      A.C = 0 START WITH A.B = 1;
```

#### Best Practices

- If there are cycles in the data hierarchy, you can review this [article](https://docs.snowflake.com/en/user-guide/queries-cte#cause-1-cyclic-data-hierarchy) to deal with them.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0014

Foreign key data type mismatch.

### Description

This error happens when there is a mismatch in a foreign key data type.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE "MyDb"."MyTable"
(
    "COL1" NUMBER,
    CONSTRAINT "PK" PRIMARY KEY ("COL1")
);

CREATE TABLE "MyDb"."MyTable1"
(   
    "COL1" NUMBER(*,0),
    CONSTRAINT "FK1" FOREIGN KEY ("COL1") REFERENCES "MyDb"."MyTable" ("COL1")
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE "MyDb"."MyTable"
    (
        "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
        CONSTRAINT "PK" PRIMARY KEY ("COL1")
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    CREATE OR REPLACE TABLE "MyDb"."MyTable1"
    (
        "COL1" NUMBER(38) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    ALTER TABLE "MyDb"."MyTable1"
    ADD
    --** SSC-FDM-OR0014 - FOREIGN KEY DATA TYPE MISMATCH **
    CONSTRAINT "FK1" FOREIGN KEY ("COL1") REFERENCES "MyDb"."MyTable" ("COL1");
```

Note

Note that “MyDb”.”MyTable1”.COL1 and “MyDb”.”MyTable”.COL1 are of different types and the ERROR is displayed.

#### Best Practices

- If there are cycles in the data hierarchy, you can review this [article](https://docs.snowflake.com/en/user-guide/queries-cte#cause-1-cyclic-data-hierarchy) to deal with them.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0015

LENGTHB transformed to OCTET\_LENGTH results may vary due to memory management of DBMS.

### Description

This issue happens when there is an invocation to [LENGTHB](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/LENGTH.html#GUID-8F97F652-5AE8-4457-AFD7-7A6F25551E0C) function that returns the size of a column or literal in bytes. This function is transformed into [OCTET\_LENGTH](https://docs.snowflake.com/en/sql-reference/functions/octet_length.html) Snowflake’s function.

When the parameter to the function is a column, the result will be the size of the value that the column has, this size may vary from Oracle to Snowflake, the type of the column plays an important role in the result returned by the function.

#### Example Code

##### Input Code:

##### Queries

Copy code

```
 CREATE TABLE char_table
(
	char_column1 CHAR(15)
);

INSERT INTO char_table VALUES ('Hello world');

SELECT char_column1, LENGTHB(char_column1), LENGTH('Hello world') FROM char_table;
```

##### Result

Copy code

```
|CHAR_COLUMN1   |LENGTHB(CHAR_COLUMN1)|LENGTH('HELLOWORLD')|
|---------------|---------------------|--------------------|
|Hello world    |15                   |11                  |
```

##### Generated Code:

##### Queries

Copy code

```
CREATE OR REPLACE TABLE char_table
(
	char_column1 CHAR(15)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO char_table
VALUES ('Hello world');

SELECT char_column1,
OCTET_LENGTH(char_column1) /*** SSC-FDM-OR0015 - LENGTHB TRANSFORMED TO OCTET_LENGTH RESULTS MAY VARY DUE TO MEMORY MANAGEMENT OF DBMS ***/, LENGTH('Hello world') FROM
char_table;
```

##### Result

Copy code

```
|CHAR_COLUMN1|OCTET_LENGTH(CHAR_COLUMN1)|LENGTH('HELLO WORLD')|
|------------|--------------------------|---------------------|
|Hello world |11                        |11                   |
```

#### Best Practices

- Manually check the data types used.
- Check the encoding of the columns used because OCTET\_LENGTH can return bigger sizes when the string contains Unicode code points.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0016

COMMIT and ROLLBACK options were removed because Snowflake does not require them

### Description

COMMIT and ROLLBACK statement options are being removed because Snowflake does not require them.

#### Example Code

##### Input Code

Copy code

```
 COMMIT WORK FORCE '22.57.53';
ROLLBACK WORK FORCE '22.57.53';
```

##### Generated Code

Copy code

```
 --** SSC-FDM-OR0016 - COMMIT OPTIONS REMOVED BECAUSE SNOWFLAKE DOES NOT REQUIRE THEM **
--** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
COMMIT WORK;

--** SSC-FDM-OR0016 - ROLLBACK OPTIONS REMOVED BECAUSE SNOWFLAKE DOES NOT REQUIRE THEM **
--** SSC-FDM-OR0012 - ROLLBACK REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
ROLLBACK WORK;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0017

DBTimezone was removed to use the default value of the Timestamp.

### Description

DBTIMEZONE keyword was removed from the AT TIME ZONE expression.

#### Example Code

##### Input Code:

Copy code

```
 SELECT TIMESTAMP '1998-12-25 09:26:50.12' AT TIME ZONE DBTIMEZONE FROM DUAL;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0017 - DBTIMEZONE WAS REMOVED TO USE THE DEFAULT VALUE OF THE TIMESTAMP **
TO_TIMESTAMP_LTZ( TIMESTAMP '1998-12-25 09:26:50.12')
FROM DUAL;
```

#### Best Practices

- You may need to set the TIMEZONE session parameter to get equal results.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0018

Merge statement may not work as expected

### Description

This warning is used to indicate that the Snowflake merge statement may have some functional differences compared to Oracle.

#### Example Code

##### Input Code:

Copy code

```
 MERGE INTO people_target pt 
USING people_source ps 
ON    (pt.person_id = ps.person_id) 
WHEN MATCHED THEN UPDATE 
  SET pt.first_name = ps.first_name, 
      pt.last_name = ps.last_name, 
      pt.title = ps.title 
  DELETE where pt.title  = 'Mrs.' 
WHEN NOT MATCHED THEN INSERT 
  (pt.person_id, pt.first_name, pt.last_name, pt.title) 
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title) 
  WHERE ps.title = 'Mr';
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-OR0018 - SNOWFLAKE MERGE STATEMENT MAY HAVE SOME FUNCTIONAL DIFFERENCES COMPARED TO ORACLE **
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "people_target", "people_source" **
MERGE INTO people_target pt
USING people_source ps
ON    (pt.person_id = ps.person_id)
      WHEN MATCHED AND pt.title  = 'Mrs.' THEN
        DELETE
      WHEN MATCHED THEN
        UPDATE SET
          pt.first_name = ps.first_name,
               pt.last_name = ps.last_name,
               pt.title = ps.title
      WHEN NOT MATCHED AND ps.title = 'Mr' THEN
        INSERT
        (pt.person_id, pt.first_name, pt.last_name, pt.title)
        VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);
```

#### Best Practices

- If you are getting different results compared to Oracle, consider the following:
  - For execution order prioritization, go to the next [link](https://docs.snowflake.com/en/sql-reference/sql/merge.html#usage-notes) to get more information.
    - Execute the skipped DML statements outside (before or after accordingly) the merge statement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0019

Window frame output may not be equivalent

### Description

This warning is added when a ROWS window frame unit is found within the source code.

ROWS works by using physical row numbers for its computing, which may differ once it is migrated to the target platform. Manually adding extra ORDER BY clauses can help mitigate or remove this issue.

Note

Note that as the [Oracle documentation](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Analytic-Functions.html) states:  
”The value returned by an analytic function with a logical offset is always deterministic. However, the value returned by an analytic function with a physical offset may produce nondeterministic results unless the ordering expression results in a unique ordering. You may have to specify multiple columns in the `order_by_clause` to achieve this unique ordering.”

According to this is recommended to check if the function returned deterministic results beforehand to avoid any issues.

#### Example Code

##### Input Code:

Copy code

```
 SELECT
SUM(C_BIRTH_DAY)
OVER (
    ORDER BY C_BIRTH_COUNTRY
    ROWS UNBOUNDED PRECEDING) AS MAX1
FROM WINDOW_TABLE;
```

##### Generated Code:

Copy code

```
 SELECT
SUM(C_BIRTH_DAY)
OVER (
    ORDER BY C_BIRTH_COUNTRY ROWS UNBOUNDED PRECEDING /*** SSC-FDM-OR0019 - WINDOW FRAME OUTPUT MAY NOT BE EQUIVALENT ***/) AS MAX1
FROM
WINDOW_TABLE;
```

#### Best Practices

- Ensure deterministic ordering for rows to ensure deterministic outputs when running in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0020

PRAGMA EXCEPTION\_INIT is not supported.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0051](../conversion-issues/oracleEWI#ssc-ewi-or0051) documentation.

### Description

This warning is added when PRAGMA EXCEPTION\_INIT function is invoked within a procedure. Exception Name and SQL Code of the exceptions are set in the RAISE function. When it is converted to Snowflake Scripting, the SQL Code is added to the Exception declaration, however, some code values may be invalid in Snowflake Scripting.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE EXCEPTION_DECLARATION_SAMPLE AUTHID DEFINER IS
  NEW_EXCEPTION EXCEPTION;
  PRAGMA EXCEPTION_INIT(NEW_EXCEPTION, -63);
  NEW_EXCEPTION2 EXCEPTION;
  PRAGMA EXCEPTION_INIT ( NEW_EXCEPTION2, -20100 );
BEGIN

  IF true THEN
    RAISE NEW_EXCEPTION;
  END IF;

EXCEPTION
    WHEN NEW_EXCEPTION THEN
        --Handle Exceptions
        NULL;
END;
/
```

##### Generated Code:

##### Snowflake Scription

Copy code

```
 CREATE OR REPLACE PROCEDURE EXCEPTION_DECLARATION_SAMPLE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0097 - PROCEDURE PROPERTIES ARE NOT SUPPORTED IN SNOWFLAKE PROCEDURES ***/!!!
AS
$$
  DECLARE
    --** SSC-FDM-OR0023 - EXCEPTION CODE NUMBER EXCEEDS SNOWFLAKE SCRIPTING LIMITS **
    NEW_EXCEPTION EXCEPTION;
    --** SSC-FDM-OR0020 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED **
    PRAGMA EXCEPTION_INIT(NEW_EXCEPTION, -63);
    NEW_EXCEPTION2 EXCEPTION (-20100, '');
    --** SSC-FDM-OR0020 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED **
  PRAGMA EXCEPTION_INIT ( NEW_EXCEPTION2, -20100 );
  BEGIN
    IF (true) THEN
      RAISE NEW_EXCEPTION;
    END IF;
    EXCEPTION
        WHEN NEW_EXCEPTION THEN
            --Handle Exceptions
            NULL;
    END;
$$;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0021

For Loop With Float Number As Bound May Not Behave Correctly In Snowflake Scripting

### Description

Snowflake Scripting only allows an `INTEGER` or an expression that evaluates to an `INTEGER` as a bound for the `FOR LOOP` condition. Floating numbers will be rounded up or down and alter the original bound.

The lower bound will be rounded to the closest integer number. For example:

**3.1 -> 3**, **6.7 -> 7**, **4.5 -> 5**

However the upper bound will be truncated to the closest lower integer. For example:

**3.1 -> 3**, **6.7 -> 6**, **4.5 -> 4**

#### Snowflake Scripting

Copy code

```
 CREATE OR REPLACE PROCEDURE p1()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        var1 VARCHAR DEFAULT '';
        var2 VARCHAR DEFAULT '';
        var3 VARCHAR DEFAULT '';
    BEGIN
        --Loop 1
        FOR i IN 1.2 TO 5.2 DO
            var1 := var1 || ' ' || i::VARCHAR;
        END FOR;
        
        --Loop 2
        FOR i IN 1.7 TO 5.5 DO
            var2 := var2 || ' ' || i::VARCHAR;
        END FOR;
        
        --Loop 3
        FOR i IN 1.5 TO 5.8 DO
            var3 := var3 || ' ' || i::VARCHAR;
        END FOR;
        RETURN  ' Loop1: ' || var1 ||
                ' Loop2: ' || var2 ||
                ' Loop3: ' || var3;
    END;
$$;

CALL p1();
```

##### Result

Copy code

```
P1                                                |
--------------------------------------------------+
 Loop1:  1 2 3 4 5                                |
 Loop2:  2 3 4 5                                  |
 Loop3:  2 3 4 5                                  |
```

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE p1
AS
BEGIN
FOR i NUMBER(5,1) IN 1.2 .. 5.7 LOOP
    NULL;
END LOOP;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE p1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0021 - FOR LOOP WITH FLOAT NUMBER AS LOWER OR UPPER BOUND MAY NOT BEHAVE CORRECTLY IN SNOWFLAKE SCRIPTING **
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN 1.2 TO 5.7
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
                                   NULL;
END LOOP;
    END;
$$;
```

#### Best Practices

- Rewrite the FOR LOOP condition so it uses integers.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0022

For Loop With Multiple Conditions Is Currently Not Supported By Snowflake Scripting. Only First Condition Is Used

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0100](../conversion-issues/oracleEWI#ssc-ewi-or0100) documentation.

### Description

Oracle allows multiple conditions in a single `FOR LOOP` however, Snowflake Scripting only allows one condition per `FOR LOOP`. Only the first condition is migrated and the others are ignored during transformation.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE P3
AS
BEGIN
FOR i IN REVERSE 1..3,
REVERSE i+5..i+7
LOOP
    NULL;
END LOOP; 
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE P3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0022 - FOR LOOP WITH MULTIPLE CONDITIONS IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING **
        FOR i IN REVERSE 1 TO 3 LOOP
            NULL;
        END LOOP;
    END;
$$;
```

#### Best Practices

- Separate the `FOR LOOP` into different loops or rewrite the condition.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0023

The exception code exceeds the Snowflake Scripting limit

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0099](../conversion-issues/oracleEWI#ssc-ewi-or0099) documentation.

### Description

This warning appears when an exception declaration error code exceeds the Snowflake Scripting exception number limits. The number must be an integer between -20000 and -20999.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure_exception
IS
my_exception EXCEPTION;
PRAGMA EXCEPTION_INIT ( my_exception, -19000 );
BEGIN
    NULL; 
END;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE procedure_exception ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-FDM-OR0023 - EXCEPTION CODE NUMBER EXCEEDS SNOWFLAKE SCRIPTING LIMITS **
        my_exception EXCEPTION;
        --** SSC-FDM-OR0020 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED **
        PRAGMA EXCEPTION_INIT ( my_exception, -19000 );
    BEGIN
        NULL;
    END;
$$;
```

#### Best Practices

- Check if the exception code is between the limits allowed by Snowflake Scripting, if not change it for another exception number available.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0024

Columns from expression not found

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0002](../conversion-issues/oracleEWI#ssc-ewi-or0002) documentation.

### Description

This error happens when the columns of a Select Expression were unable to be resolved, usually when it either refers to a Type Access whose reference wasn’t resolved or a column with a User Defined Type whose columns haven’t been defined; such as a Type Without Body or Object Type with no columns.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE record_unknown_table_proc
AS
    unknownTable_variable_rowtype unknownTable%ROWTYPE;
BEGIN
    INSERT INTO MyTable values unknownTable_variable_rowtype;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE record_unknown_table_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        unknownTable_variable_rowtype OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    BEGIN
        INSERT INTO MyTable
        SELECT
            null /*** SSC-FDM-OR0024 - COLUMNS FROM EXPRESSION unknownTable%ROWTYPE NOT FOUND ***/;
    END;
$$;
```

#### Related EWIs

1. [SSC-EWI-0036](../conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.

#### Best Practices

- Verify that the type definition that was referenced does have columns within it.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0025

Not Null constraint is not supported in Snowflake Procedures

### Description

The Oracle variable declaration `NOT NULL` constraint is not supported in variable declarations inside procedures in Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC04
IS
 var3 FLOAT NOT NULL := 100;
BEGIN
NULL;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC04 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  var3 FLOAT := 100 /*** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE ***/;
 BEGIN
  NULL;
 END;
$$;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0026

Type not supported in cast operation.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0045](../conversion-issues/oracleEWI#ssc-ewi-or0045) documentation.

### Description

This error happens when a type is not supported in a cast operation.

#### Example

##### Input Code:

Copy code

```
 select cast(' $123.45' as number, 'L999.99') from dual;
```

##### Generated Code:

Copy code

```
 select
--** SSC-FDM-OR0026 - CAST TYPE NOT SUPPORTED **
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0011 - THE FORMAT PARAMETER ' $123.45' IS NOT SUPPORTED ***/!!!
 cast(' $123.45' as NUMBER(38, 18) , 'L999.99') from dual;
```

### Related EWIs

1. SSC-EWI-OR0011: The format parameter is not supported.

#### Best Practices

- The cast is converted to a user-defined function (UDF/Stub), so you can modify it to emulate the behavior of the cast function.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0027

DEFAULT ON CONVERSION ERROR is not supported.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0029](../conversion-issues/oracleEWI#ssc-ewi-or0029) documentation

### Description

Default on conversion error not supported in Snowflake

#### Example Code

##### Input Code:

Copy code

```
 SELECT TO_NUMBER('2,00' DEFAULT 0 ON CONVERSION ERROR) "Value" FROM DUAL;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0027 - DEFAULT ON CONVERSION ERROR NOT SUPPORTED IN SNOWFLAKE IN SNOWFLAKE **
TO_NUMBER('2,00') "Value" FROM DUAL;
```

#### Best Practices

- You might create UDF to emulate the behavior of `DEFAULT` value `ON CONVERSION ERROR`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0028

SYS\_CONTEXT parameter is not supported.

Note

This FDM is deprecated, please refer to SSC-EWI-OR0031 documentation.

### Description

This error happens when a SYS\_CONTEXT function parameter is not supported.

#### Example Code

##### Input Code:

Copy code

```
 SELECT SYS_CONTEXT ('USERENV', 'NLS_SORT') FROM DUAL;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0028 - 'NLS_SORT' SYS_CONTEXT PARAMETER NOT SUPPORTED IN SNOWFLAKE **
SYS_CONTEXT ('USERENV', 'NLS_SORT') FROM DUAL;
```

#### Best Practices

- The function is converted to a user defined function(stub), so you can modify it to emulate the behavior of the SYS\_CONTEXT parameter.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0029

This ALTER SESSION configuration is not supported in Snowflake.

### Description

A clause or configuration of the ALTER SESSION statement is not currently supported.

#### Example Code

##### Input Code:

Copy code

```
 ALTER SESSION SET SQL_TRACE TRUE;
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-OR0029 - THIS ALTER SESSION CONFIGURATION IS NOT SUPPORTED IN SNOWFLAKE **
--ALTER SESSION SET SQL_TRACE TRUE
                                ;
```

#### Best Practices

- For session variables, you can check the Snowflake [documentation](https://docs.snowflake.com/en/sql-reference/parameters.html) to find an equivalent.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0030

ROWID pseudocolumn is not supported in Snowflake

### Description

When ROWID is used as a pseudocolumn in a query it is transformed to null to avoid runtime errors and the EWI is added. There is still no transformation to emulate the functionality.

#### Example Code

##### Input Code Oracle:

Copy code

```
 SELECT ROWID FROM T1;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
'' AS ROWID
FROM
T1;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0031

The error logging clause in DML statements is not supported by Snowflake

### Description

This error is used to advise that the error\_logging clause in Oracle’s DML statements is not supported by Snowflake’s DML statements.

#### Example Code

##### Input Code:

Copy code

```
 MERGE INTO people_target pt 
USING people_source ps ON (pt.person_id = ps.person_id) 
WHEN MATCHED THEN UPDATE 
  SET pt.first_name = ps.first_name, 
      pt.last_name = ps.last_name, 
      pt.title = ps.title
LOG ERRORS;
```

##### Generated Code:

Copy code

```
 MERGE INTO people_target pt
USING people_source ps ON (pt.person_id = ps.person_id)
  WHEN MATCHED THEN
    UPDATE
    SET pt.first_name = ps.first_name,
        pt.last_name = ps.last_name,
        pt.title = ps.title
--  --** SSC-FDM-OR0031 - THE ERROR LOGGING CLAUSE IN DML STATEMENTS IS NOT SUPPORTED BY SNOWFLAKE **
--LOG ERRORS
          ;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0032

StandardHash function with input non-string parameter generates a different result in Snowflake.

### Description

This warning is used when `STANDARD_HASH` function in Oracle with input non-string parameter generates a different result in Snowflake.

Note

When the algorithm parameter is a dynamic expression (not a string literal), the function cannot be converted and [SSC-EWI-OR0138](../conversion-issues/oracleEWI#ssc-ewi-or0138) is emitted instead.

#### Example Code

##### Input Code:

##### Query

Copy code

```
 SELECT STANDARD_HASH(1+1) FROM DUAL;
```

##### Result

Copy code

```
 STANDARD_HASH(1+1)                               |
--------------------------------------------------+
 E39323970701D93598FC1D357F4BF04578CE3242         |
```

##### Generated Code:

##### Query

Copy code

```
SELECT
--** SSC-FDM-OR0032 - STANDARD HASH FUNCTION WITH INPUT NON-STRING PARAMETER GENERATES A DIFFERENT RESULT IN SNOWFLAKE **
SHA1(1+1)
FROM DUAL;
```

##### Result

Copy code

```
SHA1(1+1)                                        |
--------------------------------------------------+
 da4b9237bacccdf19c0760cab7aec4a8359010b0         |
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0033

DBMS\_RANDOM.VALUE Built-In Package precision is lower in Snowflake

Description

This message is shown when a DBMS\_RANDOM.VALUE Oracle built-in package function*.* is migrated. This warning indicates that the UDF added to emulate the functionality has lower precision than the original function*.*

### Example code

#### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE built_in_package_proc
IS
var1 NUMBER;
BEGIN
    SELECT DBMS_RANDOM.VALUE() INTO var1 FROM DUAL;

    SELECT DBMS_RANDOM.VALUE(2,10) INTO var1 FROM DUAL; 
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE built_in_package_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 NUMBER(38, 18);
    BEGIN
        SELECT
            --** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
            DBMS_RANDOM.VALUE_UDF() INTO
            :var1
        FROM DUAL;

        SELECT
            --** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
            DBMS_RANDOM.VALUE_UDF(2,10) INTO
            :var1
        FROM DUAL;
    END;
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0034

Sequence start value with ‘LIMIT VALUE’ is not supported by Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0001](../conversion-issues/oracleEWI#ssc-ewi-or0001) documentation.

### Description

This error appears when the `START WITH` statement value is `LIMIT VALUE`.

In Oracle this clause is used only in ALTER TABLE

> - `START` `WITH` `LIMIT VALUE`, which is specific to `identity_options`, can only be used with `ALTER` `TABLE` `MODIFY`. If you specify `START` `WITH` `LIMIT VALUE`, then Oracle Database locks the table and finds the maximum identity column value in the table (for increasing sequences) or the minimum identity column value (for decreasing sequences) and assigns the value as the sequence generator’s high water mark. The next value returned by the sequence generator will be the high water mark + `INCREMENT` `BY` `integer` for increasing sequences, or the high water mark - `INCREMENT` `BY` `integer` for decreasing sequences.

#### [ALTER TABLE ORACLE](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-TABLE.html#GUID-552E7373-BF93-477D-9DA3-B2C9386F2877)

#### Example Code

##### Input Code:

Copy code

```
 CREATE SEQUENCE SEQUENCE1
  START WITH LIMIT VALUE;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE SEQUENCE SEQUENCE1
  --** SSC-FDM-OR0034 - SEQUENCE START VALUE WITH 'LIMIT VALUE' IS NOT SUPPORTED BY SNOWFLAKE. **
  START WITH LIMIT VALUE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0035

DBMS\_OUTPUT.PUTLINE check UDF implementation

### Description

This message is shown when a `DBMS_OUTPUT.PUT_LINE` Oracle built-in package function*.* is migrated. This warning tells you to check the added UDF*.*

This EWI exists to tell the user to review the `DBMS_OUTPUT.PUT_LINE_UDF` implementation where the following information will be found:

Warning

Performance may be affected by using this UDF. If you want to start logging information, please uncomment the implementation. Note that this is using a temporary table, if you want the data to persist after a session ends, please remove TEMPORARY from the CREATE TABLE.

Once the calls of `DBMS_OUTPUT.PUT_LINE_UDF` has been done, please use the following query to read all the logs: `SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG.`

#### Example code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE builtin_package_call
IS
BEGIN
	DBMS_OUTPUT.PUT_LINE(1);
	DBMS_OUTPUT.PUT_LINE("Test");
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE builtin_package_call ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		--** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
		CALL DBMS_OUTPUT.PUT_LINE_UDF(1);
		--** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
		CALL DBMS_OUTPUT.PUT_LINE_UDF("Test");
	END;
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0036

Unnecessary built-in packages parameters

### Description

This message is displayed when an Oracle built-in package procedure or function is migrated and some of the arguments are removed from the call.

Some of the original parameters may not have an equivalent in Snowflake or may not be needed in the transformed version, those parameters are removed from the produced code but are preserved in the EWI message so the user can still track them.

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE built_in_package_proc
IS
w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.txt','W',32760);
    UTL_FILE.PUT_LINE(w_file,'New line');    
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE built_in_package_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        w_file OBJECT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'UTL_FILE.FILE_TYPE' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := OBJECT_CONSTRUCT();
    BEGIN
        --** SSC-FDM-OR0036 - PARAMETERS: 'LOCATION, MAX_LINESIZE_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
        CALL UTL_FILE.FOPEN_UDF('test.txt', 'W');
        SELECT
            *
        INTO
            w_file
        FROM
            TABLE(RESULT_SCAN(LAST_QUERY_ID()));
        --** SSC-FDM-OR0036 - PARAMETERS: 'AUTOFLUSH_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
        CALL UTL_FILE.PUT_LINE_UDF(:w_file, 'New line');
    END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0037

The used syntax in select is not supported in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0004](../conversion-issues/oracleEWI#ssc-ewi-or0004) documentation

Note

Some parts of the output code are omitted for clarity reasons.

### Description

This warning happens when a clause in a select is not supported in Snowflake. The not supported clauses are:

- CONTAINERS
- SUBQUERY RESTRICTION
- HIERARCHIES
- EXTERNAL MODIFY
- DBLINK
- SHARDS
- PARTITION
- SUBPARTITION
- HIERARCHICAL

#### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM TABLE1 EXTERNAL MODIFY (LOCATION 'file.csv' REJECT LIMIT UNLIMITED);
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
SELECT * FROM
TABLE1
--       --** SSC-FDM-OR0037 - THE 'OPTIONAL MODIFIED EXTERNAL' SYNTAX IN SELECT IS NOT SUPPORTED IN SNOWFLAKE **
--       EXTERNAL MODIFY (LOCATION 'file.csv' REJECT LIMIT UNLIMITED)
                                                                   ;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0038

Boolean cursor attribute is not supported.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0128](../conversion-issues/oracleEWI#ssc-ewi-or0128) documentation.

### Description

This message is used to indicate that a boolean cursor attribute is not supported in SnowScript or that there is no transformation that emulates its functionality in SnowScript. The following table shows the boolean cursor attributes that can be emulated:

| Boolean Cursor Attribute | Status |
| --- | --- |
| `%FOUND` | <mark style=”color:green;”>Can be emulated</mark> |
| `%NOTFOUND` | <mark style=”color:green;”>Can be emulated</mark> |
| `%ISOPEN` | <mark style=”color:red;”>Not Supported</mark> |

Expand

Show lessSee more

#### Example Code

##### Input Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_attributes_proc
IS
    is_open_attr BOOLEAN;
    found_attr BOOLEAN;
    my_record table1%ROWTYPE;
    CURSOR my_cursor IS SELECT * FROM table1;
BEGIN
    OPEN my_cursor;
    LOOP
        FETCH my_cursor INTO my_record;
        EXIT WHEN my_cursor%NOTFOUND;
        is_open_attr := my_cursor%ISOPEN;
        found_attr := my_cursor%FOUND;
    END LOOP;
    CLOSE my_cursor;
END;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
CREATE OR REPLACE PROCEDURE cursor_attributes_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        is_open_attr BOOLEAN;
        found_attr BOOLEAN;
        my_record OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
        my_cursor CURSOR
        FOR
            SELECT
                OBJECT_CONSTRUCT( *) sc_cursor_record FROM
                table1;
    BEGIN
        OPEN my_cursor;
        LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH my_cursor INTO
                :my_record;
            IF (my_record IS NULL) THEN
                EXIT;
            END IF;
            is_open_attr := null /*my_cursor%ISOPEN*/ /*** SSC-FDM-OR0038 - BOOLEAN CURSOR ATTRIBUTE %ISOPEN IS NOT SUPPORTED IN SNOWFLAKE ***/;
            found_attr := my_record IS NOT NULL;
        END LOOP;
        CLOSE my_cursor;
    END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0039

Create Type Not Supported in Snowflake

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0007](../conversion-issues/oracleEWI#ssc-ewi-or0007) documentation

### Description

This message is added when a Create Type statement not supported by Snowflake is used.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE TYPE type6 UNDER type5(COL1 INTEGER);
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-OR0039 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE **
--CREATE TYPE type6 UNDER type5(COL1 INTEGER)
                                           ;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0040

Numeric characters cannot be altered in Snowflake. The decimal separator in Snowflake is the dot character.

### Description

Numeric characters cannot be altered in Snowflake. The decimal separator in Snowflake is the dot character. The ALTER session statement is commented and a warning is added.

#### Example Code

##### Oracle:

Copy code

```
 ALTER SESSION SET NLS_NUMERIC_CHARACTERS = ',.';
```

##### Snowflake Scripting:

Copy code

```
 ----** SSC-FDM-OR0040 - NUMERIC CHARACTERS CANNOT BE ALTERED IN SNOWFLAKE. THE DECIMAL SEPARATOR IN SNOWFLAKE IS THE DOT CHARACTER. **
--ALTER SESSION SET NLS_NUMERIC_CHARACTERS = ',.'
                                               ;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0041

Built In Package Not Supported.

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0076](../conversion-issues/oracleEWI#ssc-ewi-or0076) documentation

### Description

Translation for built-in packages is not currently supported.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 SELECT
UTL_RAW.CAST_TO_RAW('some magic here'),
DBMS_UTILITY.GET_TIME
FROM DUAL;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0041 - TRANSLATION FOR BUILT-IN PACKAGE 'UTL_RAW.CAST_TO_RAW' IS NOT CURRENTLY SUPPORTED. **
'' AS CAST_TO_RAW,
--** SSC-FDM-OR0041 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_UTILITY.GET_TIME' IS NOT CURRENTLY SUPPORTED. **
'' AS GET_TIME
FROM DUAL;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0042

Date Type Transformed To Timestamp Has A Different Behavior

### Description

Date type is being transformed to either Date or Timestamp type depending on flag [–disableDateAsTimestamp](/migrations/aim-for-datawarehouses/manual-migration/oracle#--disabledateastimestamp), because Date type in Snowflake has a different behavior than Oracle.

#### Key Differences

|  | Oracle DATE | Snowflake DATE |
| --- | --- | --- |
| Functionality | Stores date and time information | Stores only date information (year, month, day) |
| Internal Storage | Binary number representing seconds since epoch | Compact format optimized for dates |
| Use Cases | General-purpose date and time storage | Scenarios where only date information is needed |
| Advantages | Supports both date and time | More efficient storage for dates |
| Limitations | Can’t store date and time components separately. | Doesn’t store time information |

Expand

Show lessSee more

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE TABLE "PUBLIC"."TABLE1"
(
    "CREATED_DATE" DATE,
    "UPDATED_DATE" DATE
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE "PUBLIC"."TABLE1"
    (
        "CREATED_DATE" TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
        "UPDATED_DATE" TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

Copy code

```
 -- Additional Params: --disableDateAsTimestamp
CREATE OR REPLACE TABLE "PUBLIC"."TABLE1"
    (
        "CREATED_DATE" DATE /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
        "UPDATED_DATE" DATE /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0043

BFILE/BLOB parameters are considered binary. A format may be needed.

### Description

This error happens when a TO\_CLOB is converted to a TO\_VARCHAR function. A format may be needed for BFILE/BLOB parameters.

#### Example Code

##### Input Code:

Copy code

```
 SELECT TO_CLOB('Lorem ipsum dolor sit amet') FROM DUAL;
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-OR0043 - BFILE/BLOB PARAMETERS ARE CONSIDERED BINARY, FORMAT MAY BE NEEDED. **
TO_VARCHAR('Lorem ipsum dolor sit amet')
FROM DUAL;
```

#### Best Practices

- Check if outputs in the input code and converted code are equivalent and add a format parameter if needed.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0044

REGEXP\_LIKE\_UDF match parameter may not behave correctly

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This warning appears when the Oracle `REGEXP_LIKE`condition comes with the third parameter (match parameter)*.* The reason to add the warning is that the `REGEXP_LIKE_UDF`used to replace the `REGEXP_LIKE`does not recognize all the characters used by the match parameter, so the result of the query in Snowflake may not be equivalent to Oracle.

#### Example Code

##### Input Code Oracle:

Copy code

```
 SELECT last_name
FROM hr.employees
WHERE REGEXP_LIKE (last_name, '([aeiou])\1', 'i')
ORDER BY last_name;
```

##### Generated Code:

Copy code

```
 SELECT last_name
FROM
hr.employees
WHERE
--** SSC-FDM-OR0044 - REGEXP_LIKE_UDF MATCH PARAMETER MAY HAVE SOME FUNCTIONAL DIFFERENCES COMPARED TO ORACLE **
PUBLIC.REGEXP_LIKE_UDF(last_name, '([aeiou])\\1', 'i')
ORDER BY last_name;
```

- When the `REGEXP_LIKE`condition comes with one of the characters that are not supported by the user-defined function, maybe a possible solution is to change the regular expression to simulate the behavior of the missing character in the match parameter. To know more about the character not supported go to [REGEXP\_LIKE\_UDF](../../translation-references/oracle/functions/README) documentation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0045

Partitions Clauses are Handled by Snowflake

Note

This FDM is deprecated, please refer to [SSC-EWI-OR0010](../conversion-issues/oracleEWI#ssc-ewi-or0010) documentation

### Description

This warning appears when the `PARTITION` and `SUBPARTITION` clauses appear within a query. Snowflake handle partitions automatically

#### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM TABLITA PARTITION(col1);
```

##### Generated Code:

Copy code

```
 SELECT * FROM
TABLITA
--        --** SSC-FDM-OR0045 - PARTITIONS CLAUSES ARE HANDLED BY SNOWFLAKE **
--        PARTITION(col1)
                       ;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0046

The Subquery Restriction is not Possible in Snowflake

Note

Some parts of the output code are omitted for clarity reasons.

### Description

This warning happens when a Subquery Restriction appears in a `SELECT` Statement.

#### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM LATERAL(SELECT * FROM TABLITA WITH READ ONLY CONSTRAINT T);
```

##### Generated Code:

Copy code

```
 SELECT * FROM LATERAL(SELECT * FROM
TABLITA
--        --** SSC-FDM-OR0046 - THE SUBQUERY RESTRICTION IS NOT POSSIBLE IN SNOWFLAKE **
--        WITH READ ONLY CONSTRAINT T
                                   );
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0047

It may be needed to set a TimeStampOutput format.

### Description

TIMESTAMP\_OUTPUT\_FORMAT session parameter may need to be set to ‘DD-MON-YY HH24.MI.SS.FF AM TZH:TZM’ for timestamp output equivalence.

#### Example Code

##### Input Code:

Copy code

```
 SELECT SYSTIMESTAMP FROM DUAL;
```

##### Example of default TIMESTAMP output in Oracle

Note

:class: tip
13-JAN-21 04.18.37.288656 PM +00:00

##### Generated Code:

Copy code

```
 SELECT
CURRENT_TIMESTAMP() /*** SSC-FDM-OR0047 - YOU MAY NEED TO SET TIMESTAMP OUTPUT FORMAT ('DD-MON-YY HH24.MI.SS.FF AM TZH:TZM') ***/
FROM DUAL;
```

##### Example of default TIMESTAMP output in Snowflake

Note

:class: tip
2021-01-13 08:18:19.720 -080

#### Best Practices

- To change the timestamp output format in Snowflake use the following query:

  Copy code

ALTER SESSION SET TIMESTAMP\_OUTPUT\_FORMAT = ‘DD-MON-YY HH24.MI.SS.FF AM TZH:TZM’;

Copy code

```
* If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0048

Date or timestamp output format has to be set

### Description

When a DATE or TIMESTAMP is transformed to VARCHAR (for example, in a DEFAULT clause using SYSDATE or TRUNC(CURRENT_DATE())), the output depends on the OUTPUT_FORMAT and TIMESTAMP_OUTPUT_FORMAT session parameters. These may not match Oracle's default format. Set the session parameters to match the Oracle values for equivalent output.

#### Example Code

##### Input Code:

{/* code title="IN -> Oracle_01.sql" */}
```sql

 CREATE TABLE orders (
   order_id INT,
   created_date VARCHAR(30) DEFAULT TO_CHAR(TRUNC(SYSDATE))
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE orders (
   order_id INT,
   created_date VARCHAR(30) DEFAULT TO_VARCHAR(TRUNC(CURRENT_TIMESTAMP(), 'DD')) /*** SSC-FDM-OR0048 - TRANSFORMATION OF DATE/TIMESTAMP TO VARCHAR DEPENDS ON THE OUTPUT_FORMAT SESSION PARAMETERS, SET THEM TO MATCH THE ORACLE VALUES ***/
);
```

#### Best Practices

- Set TIMESTAMP\_OUTPUT\_FORMAT and OUTPUT\_FORMAT session parameters to match Oracle’s NLS format (e.g., ‘DD-MON-YY HH24.MI.SS.FF AM TZH:TZM’).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0049

LAG function might fail if default value type differs from the expression type.

### Description

In Oracle, the `LAG` function automatically converts the default value’s data type to match the expression’s type. Snowflake, however, does not perform this implicit conversion. Therefore, a warning is issued to indicate that the `LAG` function may fail if the data types are incompatible.

#### Example Code

##### Input Code:

Copy code

```
 SELECT 
    LAG(salary, 2, '0') OVER (ORDER BY salary) AS salary_two_steps_back
FROM 
    employees;
```

##### Generated Code:

Copy code

```
 SELECT
    --** SSC-FDM-OR0049 - LAG FUNCTION MIGHT FAIL IF DEFAULT VALUE TYPE DIFFERS FROM THE EXPRESSION TYPE. **
    LAG(salary, 2, '0')
    OVER (ORDER BY salary) AS salary_two_steps_back
FROM
    employees;
```

#### Best Practices

- Verify that the data type of the default value matches the data type of the expression in the `LAG` function. If they differ, explicitly cast the default value to the expression’s data type.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0050

Exceptions with `NOCOPY` parameters may lead to data inconsistency.

### Description

In Oracle PL/SQL, the `NOCOPY` keyword is an optimization hint for `OUT` and `IN OUT` procedure parameters. By default, Oracle passes these parameters by value, creating an expensive copy of the data during the call and copying it back upon completion. This can cause significant performance overhead for large data structures.

`NOCOPY` instructs Oracle to pass by reference instead, allowing the procedure to directly modify the original data. This eliminates copying overhead and improves performance. However, changes are immediate and are not implicitly rolled back if an unhandled exception occurs within the procedure.

Therefore, we will remove the NOCOPY parameters option and add this FDM. This is because procedure execution terminates upon hitting an exception, preventing the `RETURN` statement from being reached. As a result, the variable in the caller’s declare block retains its initial values, as the procedure fails to successfully return a new value for assignment.

#### Example Code

##### Input Code:

Copy code

```
CREATE OR REPLACE PROCEDURE calculate_division_with_nocopy (
    p_numerator IN NUMBER,
    p_denominator IN NUMBER,
    p_result OUT NOCOPY NUMBER
)
IS
    PROCEDURE calculate_division(result OUT NOCOPY NUMBER)
    AS
    BEGIN
    result := 20;
    result := p_numerator / p_denominator;
    END calculate_division;
BEGIN
    calculate_division(p_result);
        EXCEPTION
        WHEN OTHERS THEN
            p_result := p_result;
END calculate_division_with_nocopy;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE calculate_division_with_nocopy (p_numerator NUMBER(38, 18), p_denominator NUMBER(38, 18), p_result OUT NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/23/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        calculate_division PROCEDURE(result
        --** SSC-FDM-OR0050 - EXCEPTIONS WITH NOCOPY PARAMETERS MAY LEAD TO DATA INCONSISTENCY. **
        NUMBER(38, 18))
        RETURNS NUMBER
        AS
            BEGIN
                result := 20;
                result := :p_numerator / :p_denominator;
                RETURN result;
            END;
        call_results NUMBER;
    BEGIN
        call_results := (
            CALL
            calculate_division(:p_result)
        );
        p_result := :call_results;
        EXCEPTION
        WHEN OTHER THEN
            p_result := :p_result;
        END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0051

Array size limit removed. Snowflake arrays are dynamically sized.

Note

**Deprecated.** This issue has been replaced by the dialect-agnostic [SSC-FDM-0043](generalFDM#ssc-fdm-0043), which now covers the same behavior for both Oracle `VARRAY` and Db2 array type definitions. New conversions emit `SSC-FDM-0043` instead. The example code below is preserved for historical reference.

### Severity

None (functional difference)

### Description

When an Oracle `VARRAY` type is converted to a Snowflake `ARRAY` type, any **fixed maximum size** on the varray is not preserved because Snowflake arrays grow dynamically. SnowConvert emits this FDM to document that behavioral difference.

#### Example Code

##### Oracle:

Copy code

```
CREATE TYPE PhoneNumbers AS VARRAY(10) OF VARCHAR2(20);
```

##### Snowflake:

Copy code

```
--** SSC-FDM-OR0051 - ARRAY SIZE LIMIT '10' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE PhoneNumbers AS ARRAY ( VARCHAR(20) );
```

#### Best Practices

- If application logic relies on a maximum number of elements, enforce it in application code or with constraints outside the type definition.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0052

Collection EXISTS index adjusted from 1-based to 0-based indexing.

### Description

Oracle nested table and collection APIs often use **1-based** indexing; Snowflake `ARRAY` indexing is **0-based**. SnowConvert may adjust `EXISTS` index expressions and emits this FDM when that adjustment applies.

#### Best Practices

- Review all collection index arithmetic after migration.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0053

Embedded collection type definition removed. Collection variables are transformed to ARRAY.

### Description

PL/SQL **nested collection types** declared inside a block are not kept as separate type definitions in Snowflake Scripting; variables are migrated toward `ARRAY` usage. This FDM documents that the embedded type definition was removed as part of that transformation.

#### Best Practices

- Validate runtime behavior for nested collections and associative arrays after conversion.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0054

Embedded record type definition removed. Record variables are transformed to OBJECT.

### Description

PL/SQL **RECORD** types declared inside a procedure or block are inlined or replaced with Snowflake Scripting `OBJECT`-style handling; the original embedded `TYPE ... IS RECORD` definition may be commented or removed with this FDM.

#### Best Practices

- Review accesses to record fields and default initialization after migration.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0055

TRIM on BINARY data requires explicit cast.

### Description

Oracle `TRIM`, `LTRIM`, and `RTRIM` functions can operate directly on `RAW` (binary) columns. Snowflake does not support trimming on `BINARY` data types. To preserve functionality, SnowConvert wraps the argument with `TO_VARCHAR(expr, 'HEX')` before trimming and wraps the result with `TO_BINARY(NULLIF(..., ''), 'HEX')` to convert back to binary.

This pattern applies to all trim variants: `TRIM`, `LTRIM`, `RTRIM`, and `TRIM` with `LEADING`, `TRAILING`, or `BOTH` specifications.

#### Example Code

##### Oracle:

Copy code

```
CREATE TABLE test_table (raw_col RAW(16), varchar_col VARCHAR2(100));

SELECT TRIM(raw_col) FROM test_table;
```

##### Snowflake:

Copy code

```
CREATE OR REPLACE TABLE test_table (
  raw_col BINARY,
  varchar_col VARCHAR(100)
)
;

SELECT
--** SSC-FDM-OR0055 - TRIM/LTRIM/RTRIM IS NOT SUPPORTED ON BINARY DATA TYPES IN SNOWFLAKE. THE ARGUMENT HAS BEEN WRAPPED WITH TO_VARCHAR/TO_BINARY TO PRESERVE FUNCTIONALITY. **
  TO_BINARY(NULLIF(TRIM(TO_VARCHAR(raw_col, 'HEX')), ''), 'HEX')
FROM
  test_table;
```

##### Oracle (TRIM with LEADING specification):

Copy code

```
SELECT TRIM(LEADING '0' FROM raw_col) FROM test_table;
```

##### Snowflake:

Copy code

```
SELECT
--** SSC-FDM-OR0055 - TRIM/LTRIM/RTRIM IS NOT SUPPORTED ON BINARY DATA TYPES IN SNOWFLAKE. THE ARGUMENT HAS BEEN WRAPPED WITH TO_VARCHAR/TO_BINARY TO PRESERVE FUNCTIONALITY. **
  TO_BINARY(NULLIF(LTRIM(TO_VARCHAR(raw_col, 'HEX'), '0'), ''), 'HEX')
FROM
  test_table;
```

##### Oracle (LTRIM):

Copy code

```
SELECT LTRIM(raw_col) FROM test_table;
```

##### Snowflake:

Copy code

```
SELECT
--** SSC-FDM-OR0055 - TRIM/LTRIM/RTRIM IS NOT SUPPORTED ON BINARY DATA TYPES IN SNOWFLAKE. THE ARGUMENT HAS BEEN WRAPPED WITH TO_VARCHAR/TO_BINARY TO PRESERVE FUNCTIONALITY. **
  TO_BINARY(NULLIF(LTRIM(TO_VARCHAR(raw_col, 'HEX')), ''), 'HEX')
FROM
  test_table;
```

#### Best Practices

- Review generated code to ensure the `TO_VARCHAR`/`TO_BINARY` wrapping preserves the expected binary semantics for your application.
- Non-RAW columns used with `TRIM`, `LTRIM`, or `RTRIM` are not affected by this transformation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-OR0056

Oracle package-level cursor used in FOR…IN loop was converted to RESULTSET pattern.

#### Description

SnowConvert AI bounds the package cursor to the `FOR...IN` loop, opening it on entry and closing it on exit, so it behaves as a local `RESULTSET`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
        CREATE OR REPLACE PACKAGE BODY schema_test.pkg_test AS
            PROCEDURE process_employees IS
            BEGIN
                FOR rec IN pkg_test.c_emp_above_salary_70k LOOP
                    DBMS_OUTPUT.PUT_LINE(rec.emp_name);
                END LOOP;
            END process_employees;
        END pkg_test;
```

##### Output Code:

##### Snowflake

Copy code

```
        CREATE OR REPLACE PROCEDURE SCHEMA_TEST_PKG_TEST.process_employees ()
        RETURNS VARCHAR
        LANGUAGE SQL
        EXECUTE AS CALLER
        AS
        $$
          BEGIN
            LET "SCHEMA_TEST_PKG_TEST.C_EMP_ABOVE_SALARY_70K.for_1" RESULTSET;
            "SCHEMA_TEST_PKG_TEST.C_EMP_ABOVE_SALARY_70K.for_1" := (
              EXECUTE IMMEDIATE PACKAGE_CURSOR.GET_CURSOR_DEFINITION('"SCHEMA_TEST_PKG_TEST.C_EMP_ABOVE_SALARY_70K"')
            );
            --** SSC-FDM-OR0056 - ORACLE PACKAGE-LEVEL CURSOR 'C_EMP_ABOVE_SALARY_70K' IS BOUNDED TO THE FOR...IN LOOP BLOCK (OPENS ON ENTRY, CLOSES ON EXIT), SO IT BEHAVES AS A LOCAL CURSOR AND WAS CONVERTED ACCORDINGLY. **
            FOR rec IN "SCHEMA_TEST_PKG_TEST.C_EMP_ABOVE_SALARY_70K.for_1" DO
              CALL DBMS_OUTPUT.PUT_LINE(rec.emp_name);
            END FOR;
          END;
        $$;
```

#### Best Practices

- Verify cursor parameters, row shape, and lifecycle.

## SSC-FDM-OR0057

Package cursor OPEN uses PACKAGE\_CURSOR.OPEN\_CURSOR helper — verify UDF implementation.

#### Description

Package-cursor `OPEN` uses the generated `PACKAGE_CURSOR.OPEN_CURSOR` helper.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
        CREATE OR REPLACE PACKAGE BODY schema_test.pkg_test AS
            CURSOR c_emp_by_dept (p_dept VARCHAR2) IS
                SELECT emp_id FROM employees WHERE dept = p_dept;
            PROCEDURE process_eng IS
            BEGIN
                OPEN c_emp_by_dept(p_dept => 'ENG');
            END process_eng;
        END pkg_test;
```

##### Output Code:

##### Snowflake

Copy code

```
        CALL PACKAGE_CURSOR.CREATE_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP_BY_DEPT"', 'SELECT emp_id FROM schema_test.employees WHERE dept = @@p_dept@@', 'SELECT emp_id, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS _row_num FROM schema_test.employees WHERE dept = @@p_dept@@');

        CREATE OR REPLACE PROCEDURE SCHEMA_TEST_PKG_TEST.process_eng ()
        RETURNS VARCHAR
        LANGUAGE SQL
        EXECUTE AS CALLER
        AS
        $$
          BEGIN
            --** SSC-FDM-OR0057 - CHECK UDF IMPLEMENTATION FOR PACKAGE_CURSOR.OPEN_CURSOR. **
            CALL PACKAGE_CURSOR.OPEN_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP_BY_DEPT"', OBJECT_CONSTRUCT('p_dept', 'ENG'));
          END;
        $$;
```

#### Best Practices

- Review and deploy the helper before running converted cursor code.

## SSC-FDM-OR0059

Snowflake does not support ordering a DISTINCT array aggregation by a non-aggregated expression; the ORDER BY was dropped.

#### Description

SnowConvert AI keeps `DISTINCT` but removes an unsupported `ORDER BY` from the converted `ARRAY_AGG`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT COLLECT(DISTINCT cust_last_name ORDER BY cust_id) FROM dual;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ARRAY_AGG(DISTINCT cust_last_name)
  /*** SSC-FDM-OR0059 - SNOWFLAKE DOES NOT SUPPORT ORDERING A DISTINCT ARRAY AGGREGATION BY A NON-AGGREGATED EXPRESSION; THE ORDER BY WAS DROPPED. ***/
FROM dual;
```

#### Best Practices

- Order by the aggregated expression or sort the resulting array downstream.

## SSC-FDM-OR0060

NULL values are excluded by Snowflake’s ARRAY\_AGG whereas Oracle COLLECT retains them.

#### Description

Oracle `COLLECT` retains null elements, while Snowflake `ARRAY_AGG` excludes them.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT COLLECT(cust_last_name ORDER BY cust_id) FROM dual;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ARRAY_AGG(cust_last_name) WITHIN GROUP (ORDER BY cust_id)
  /*** SSC-FDM-OR0060 - NULL VALUES ARE EXCLUDED BY SNOWFLAKE'S ARRAY_AGG, WHEREAS ORACLE COLLECT RETAINS THEM. ***/
FROM dual;
```

#### Best Practices

- Validate downstream element counts and preserve null placeholders explicitly when required.

## SSC-FDM-OR0061

Built-in package call not required in Snowflake

#### Description

SnowConvert AI comments out Oracle package lifecycle or resource-management calls that are unnecessary in Snowflake.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE xmlstore_proc
IS
    l_ctx NUMBER;
BEGIN
    DBMS_XMLSTORE.setUpdateColumn(l_ctx, 'PROJ_ID');
    DBMS_XMLSTORE.setRowTag(l_ctx, 'XMLDATA');
    DBMS_XMLSTORE.closeContext(l_ctx);
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE xmlstore_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    l_ctx NUMBER(38, 18);
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_XMLSTORE.setUpdateColumn' IS NOT CURRENTLY SUPPORTED. ***/!!!
    DBMS_XMLSTORE.setUpdateColumn(:l_ctx, 'PROJ_ID');
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_XMLSTORE.setRowTag' IS NOT CURRENTLY SUPPORTED. ***/!!!
    DBMS_XMLSTORE.setRowTag(:l_ctx, 'XMLDATA');
--    --** SSC-FDM-OR0061 - BUILT-IN PACKAGE 'DBMS_XMLSTORE.closeContext' IS NOT REQUIRED IN SNOWFLAKE AND WAS REMOVED. **
--    DBMS_XMLSTORE.closeContext(:l_ctx)
  END;
$$;
```

#### Best Practices

- Verify that the removed call had no application-visible side effect.

## SSC-FDM-OR0062

XMLTYPE parsed as VARIANT via PARSE\_XML.

#### Description

SnowConvert AI translates `XMLTYPE` to `PARSE_XML`, producing a `VARIANT` whose downstream behavior can differ from Oracle `XMLType`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT XMLTYPE('<root><val>1</val></root>') FROM DUAL;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0062 - XMLTYPE PARSED AS A VARIANT VIA PARSE_XML. RESULTS MAY DIFFER FOR DOWNSTREAM XMLTYPE METHOD CALLS. **
  PARSE_XML('<root><val>1</val></root>')
FROM DUAL;
```

#### Best Practices

- Review member operations applied to the parsed value.

## SSC-FDM-OR0063

EXTRACTVALUE translated to GET/XMLGET for a plain element path.

#### Description

Plain element paths are translated to `GET` and `XMLGET`; namespaces, axes, and predicates are not handled by this rewrite.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT EXTRACTVALUE(xml_col, '/root/val') FROM t;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0063 - EXTRACTVALUE TRANSLATED TO GET/XMLGET FOR A PLAIN ELEMENT PATH. NAMESPACES, AXES AND PREDICATES ARE NOT SUPPORTED. **
  GET(XMLGET(PARSE_XML(TO_VARCHAR(xml_col)), 'val'), '$')::STRING
FROM t;
```

#### Best Practices

- Rework complex XPath expressions against Snowflake’s semi-structured representation.

## SSC-FDM-OR0064

XMLELEMENT translated to string concatenation.

#### Description

SnowConvert AI constructs the element with string concatenation, which does not XML-escape dynamic values.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT XMLELEMENT("EmpName", emp_name) FROM employees;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0064 - XMLELEMENT TRANSLATED TO STRING CONCATENATION. SPECIAL CHARACTERS IN VALUES MAY PRODUCE INVALID XML. **
  '<EmpName>' || COALESCE(emp_name::STRING, '') || '</EmpName>'
FROM employees;
```

#### Best Practices

- Escape special characters before concatenation.

## SSC-FDM-OR0065

XMLFOREST translated to string concatenation.

#### Description

SnowConvert AI translates `XMLFOREST` to concatenation and omits null-valued elements, but does not XML-escape values.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT XMLFOREST(emp_name AS "Name", salary AS "Salary") FROM employees;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0065 - XMLFOREST TRANSLATED TO STRING CONCATENATION. NULL COLUMNS ARE OMITTED FROM OUTPUT (ORACLE BEHAVIOR PRESERVED). SPECIAL CHARACTERS IN VALUES MAY PRODUCE INVALID XML. **
  IFF(emp_name IS NULL, '', '<Name>' || emp_name || '</Name>')
  || IFF(salary IS NULL, '', '<Salary>' || salary || '</Salary>')
FROM employees;
```

#### Best Practices

- Validate null handling and escape special characters.

## SSC-FDM-OR0066

XMLAGG translated to LISTAGG.

#### Description

SnowConvert AI translates `XMLAGG` to `LISTAGG`; the resulting string is limited to 16 MB.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT XMLAGG(xml_col ORDER BY id) FROM t;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0066 - XMLAGG TRANSLATED TO LISTAGG. RESULT IS CAPPED AT 16MB. **
  LISTAGG(TO_VARCHAR(xml_col), '') WITHIN GROUP (ORDER BY id)
FROM t;
```

#### Best Practices

- Use another aggregation strategy when the result can exceed 16 MB.

## SSC-FDM-OR0067

STRTOK\_SPLIT\_TO\_TABLE returns XML special characters unencoded

#### Description

The converted split does not XML-encode values or guarantee row order.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT
   trim(COLUMN_VALUE) currency
FROM
   my_table,
   xmltable(('"' || REPLACE(my_table.currency, ',', '","') || '"'));
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  NULLIF(trim(COLUMN_VALUE), '') currency
FROM
  my_table,
  --** SSC-FDM-OR0067 - STRTOK_SPLIT_TO_TABLE DOES NOT XML-ENCODE SPECIAL CHARACTERS OR GUARANTEE ROW ORDER (USE ORDER BY INDEX), UNLIKE ORACLE'S XMLTABLE. **
  TABLE(STRTOK_SPLIT_TO_TABLE(my_table.currency, ',')) AS COLUMN_VALUE_TABLE (
    SEQ,
    INDEX,
    COLUMN_VALUE
  );
```

#### Best Practices

- Order by `INDEX` and validate values containing XML special characters.

## SSC-FDM-OR0068

SPLIT\_TO\_TABLE keeps empty tokens dropped by the Oracle XMLTABLE string-split

#### Description

`SPLIT_TO_TABLE` keeps empty tokens, does not XML-encode values, and does not guarantee row order.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT
   COLUMN_VALUE
FROM
   my_table,
   xmltable(('"' || REPLACE(my_table.currency, ', ', '", "') || '"'));
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  COLUMN_VALUE
FROM
  my_table,
  --** SSC-FDM-OR0068 - SPLIT_TO_TABLE KEEPS EMPTY TOKENS, DOES NOT XML-ENCODE SPECIAL CHARACTERS, AND DOES NOT GUARANTEE ROW ORDER (USE ORDER BY INDEX), UNLIKE ORACLE'S XMLTABLE. **
  TABLE(SPLIT_TO_TABLE(my_table.currency, ', ')) AS COLUMN_VALUE_TABLE (
    SEQ,
    INDEX,
    COLUMN_VALUE
  );
```

#### Best Practices

- Filter empty values when required and order by `INDEX`.

## SSC-FDM-OR0069

%ROWTYPE variable represented as OBJECT.

#### Description

SnowConvert AI represents `%ROWTYPE` as `OBJECT`; writes use `OBJECT_INSERT` and reads use semi-structured access.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE RowtypeTypeProc
AS
	record_rowtype_variable record_table%ROWTYPE;
BEGIN
	record_rowtype_variable := null;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE RowtypeTypeProc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
	DECLARE
		--** SSC-FDM-OR0069 - %ROWTYPE VARIABLE REPRESENTED AS OBJECT. FIELD ASSIGNMENTS EMIT OBJECT_INSERT; FIELD READS EMIT SEMI-STRUCTURED ACCESS. **
		record_rowtype_variable OBJECT := OBJECT_CONSTRUCT();
	BEGIN
		record_rowtype_variable := null;
	END;
$$;
```

#### Best Practices

- Validate field names, value types, and missing-field behavior.

## SSC-FDM-OR0070

INSERT column list inferred from %ROWTYPE field assignments.

#### Description

When the target schema is unresolved, SnowConvert AI infers the `INSERT` columns from record field assignments.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE record_unknown_table_proc
AS
    unknownTable_variable_rowtype unknownTable%ROWTYPE;
BEGIN
    unknownTable_variable_rowtype.binds_html_table_capt := NULL;
    INSERT INTO MyTable values unknownTable_variable_rowtype;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE record_unknown_table_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-FDM-OR0069 - %ROWTYPE VARIABLE REPRESENTED AS OBJECT. FIELD ASSIGNMENTS EMIT OBJECT_INSERT; FIELD READS EMIT SEMI-STRUCTURED ACCESS. **
        unknownTable_variable_rowtype OBJECT := OBJECT_CONSTRUCT();
    BEGIN
        unknownTable_variable_rowtype := OBJECT_INSERT(unknownTable_variable_rowtype, 'BINDS_HTML_TABLE_CAPT', NULL, true);
        INSERT INTO MyTable
        --** SSC-FDM-OR0070 - INSERT COLUMN LIST INFERRED FROM %ROWTYPE FIELD ASSIGNMENTS BECAUSE THE TARGET TABLE SCHEMA COULD NOT BE RESOLVED. VERIFY THE INFERRED COLUMN ORDERING MATCHES THE TARGET TABLE. **
        SELECT
            :unknownTable_variable_rowtype:BINDS_HTML_TABLE_CAPT;
    END;
$$;
```

#### Best Practices

- Verify the inferred column order against the target table.

## SSC-FDM-OR0071

DBMS\_SESSION.SET\_IDENTIFIER translated to QUERY\_TAG

#### Description

The call becomes `ALTER SESSION SET QUERY_TAG`; Oracle VPD/RLS and auditing semantics are not preserved.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE set_id_literal_proc
IS
BEGIN
    DBMS_SESSION.SET_IDENTIFIER('my-app-user');
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE set_id_literal_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-OR0071 - TRANSLATED 'DBMS_SESSION.SET_IDENTIFIER' TO 'ALTER SESSION SET QUERY_TAG'. ORACLE'S SESSION CLIENT IDENTIFIER FEEDS VPD/RLS POLICIES AND AUDITING — THE DROPPED VALUE IS NOT RECOVERABLE IN SNOWFLAKE. **
    ALTER SESSION SET QUERY_TAG = 'my-app-user';
  END;
$$;
```

#### Best Practices

- Update policies and auditing that depended on the client identifier.

## SSC-FDM-OR0072

Ref cursor type definition inlined. Ref cursor variables are transformed to RESULTSET.

#### Description

The type definition is commented out and variables become `RESULTSET`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
               CREATE OR REPLACE PROCEDURE p_strong
               IS
                   TYPE rc IS REF CURSOR RETURN cursortable1%ROWTYPE;
                   c rc;
               BEGIN
                   OPEN c FOR SELECT col1 FROM cursortable1;
                   CLOSE c;
               END;
```

##### Output Code:

##### Snowflake

Copy code

```
                   CREATE OR REPLACE PROCEDURE p_strong ()
                   RETURNS VARCHAR
                   LANGUAGE SQL
                   EXECUTE AS CALLER
                   AS
                   $$
                     DECLARE
                   --    --** SSC-FDM-OR0072 - REF CURSOR TYPE DEFINITION 'PL REF CURSOR TYPE DEFINITION' IS INLINED. REF CURSOR VARIABLES OF THIS TYPE ARE TRANSFORMED TO RESULTSET AND THEIR OPEN FOR/FETCH/CLOSE USAGE IS HANDLED BY OTHER RULES, SO THE TYPE DEFINITION LINE ITSELF IS COMMENTED OUT. **
                   --    TYPE rc IS REF CURSOR RETURN cursortable1%ROWTYPE;
                       c_res RESULTSET;
                     BEGIN
                       LET c CURSOR
                       FOR
                         SELECT
                           col1
                         FROM
                           cursortable1;
                       OPEN c;
                       CLOSE c;
                     END;
                   $$;
```

#### Best Practices

- Validate the result-set schema and cursor lifecycle.

## SSC-FDM-OR0073

PRAGMA EXCEPTION\_INIT inlined onto the exception declaration. Snowflake matches handlers by exception name, not by error code.

#### Description

The handler catches errors raised through the exception name, not every error sharing the Oracle number.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE SC3973837_HANDLER_READS_SQLCODE (p_table IN varchar2, p_msg OUT varchar2) as
  NO_SUCH_TABLE exception;
  pragma exception_init (NO_SUCH_TABLE, -942);
begin
  execute immediate 'drop table "' || upper(p_table) || '"';
  p_msg := 'OK';
exception
  when NO_SUCH_TABLE then
    p_msg := 'ERR ' || to_char(SQLCODE) || ' ' || substr(SQLERRM, 1, 40);
end;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE SC3973837_HANDLER_READS_SQLCODE (p_table VARCHAR, p_msg OUT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0099 - EXCEPTION CODE NUMBER IS OUTSIDE THE SNOWFLAKE SCRIPTING RANGE (-20998 TO -20001). REMAP IT INTO THAT RANGE IF YOU CONTROL ALL REFERENCES, OR USE 'WHEN OTHER' WITH A SQLCODE CHECK. ***/!!!
    NO_SUCH_TABLE EXCEPTION;
--    --** SSC-FDM-OR0073 - PRAGMA EXCEPTION_INIT 'NO_SUCH_TABLE' IS INLINED: THE NEW EXCEPTION WILL ONLY CATCH ERRORS RAISED THROUGH THAT NAME - NOT OTHER ERRORS THAT SHARE THE SAME ORACLE ERROR NUMBER. **
--    pragma exception_init(NO_SUCH_TABLE, -942);
  BEGIN
    EXECUTE IMMEDIATE 'drop table "' || NVL(NVL(upper(p_table) :: STRING, '') :: STRING, '') || '"';
    p_msg := 'OK';
  exception
    when NO_SUCH_TABLE then
      p_msg := 'ERR ' || NVL(to_char(SQLCODE) /*** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR SQLCODE. CHECK IF THE NAME IS INVALID OR DUPLICATED. ***/ :: STRING, '') || ' ' || NVL(substr(SQLERRM, 1, 40) :: STRING, '');
  END;
$$;
```

#### Best Practices

- Review every raising site and avoid error-number-only assumptions.

## SSC-FDM-OR0074

PL/JSON to\_char translated to TO\_JSON; serialized output may differ

#### Description

Snowflake may order keys alphabetically and does not preserve PL/JSON pretty printing.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE p (vjson IN CLOB)
IS
    jsonobj  pljson;
    vd       pljson;
    vtext    VARCHAR2(4000);
    vsize    NUMBER;
BEGIN
    jsonobj := pljson(vjson);
    vd := jsonobj.get('d');
    vtext := jsonobj.to_char();
    vsize := jsonobj.count;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p (vjson VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    jsonobj VARIANT;
    vd VARIANT;
    vtext VARCHAR(4000);
    vsize NUMBER(38, 18);
  BEGIN
    jsonobj := PARSE_JSON(:vjson);
    vd := :jsonobj:"d";
    vtext := TO_JSON(:jsonobj) /*** SSC-FDM-OR0074 - PLJSON TO_CHAR TRANSLATED TO TO_JSON. SNOWFLAKE SERIALIZES OBJECT KEYS ALPHABETICALLY AND WITHOUT PRETTY-PRINTING, SO THE OUTPUT STRING MAY DIFFER FROM ORACLE PL/JSON. ***/;
    vsize := ARRAY_SIZE(OBJECT_KEYS(:jsonobj));
  END;
$$;
```

#### Best Practices

- Compare parsed JSON values rather than serialized formatting.

## SSC-FDM-OR0075

Collection FIRST/LAST translated assuming a dense array; differs for an empty collection.

#### Description

The translation assumes dense indexing and can differ because Oracle returns null for an empty collection.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE p_loop
AS
TYPE num_tab IS TABLE OF NUMBER;
v_arr num_tab := num_tab(10, 20, 30);
v_x NUMBER;
BEGIN
  FOR i IN v_arr.FIRST..v_arr.LAST LOOP
    v_x := v_arr(i);
  END LOOP;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p_loop ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
--    --** SSC-FDM-OR0053 - EMBEDDED COLLECTION TYPE DEFINITION 'PL COLLECTION TYPE DEFINITION' WAS REMOVED. COLLECTION VARIABLES ARE TRANSFORMED TO ARRAY BY OTHER RULES. **
--    TYPE num_tab IS TABLE OF NUMBER;
    v_arr ARRAY /*** SSC-FDM-OR0084 - COLLECTION TYPE 'num_tab' WAS MAPPED TO A SNOWFLAKE ARRAY; ELEMENT INDEXING WAS ADJUSTED FROM 1-BASED TO 0-BASED. ***/ := ARRAY_CONSTRUCT(10, 20, 30);
    v_x NUMBER(38, 18);
  BEGIN
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    FOR i IN 1 /*** SSC-FDM-OR0075 - COLLECTION 'FIRST' WAS TRANSLATED ASSUMING A DENSE ARRAY. ORACLE 'FIRST' RETURNS NULL FOR AN EMPTY COLLECTION WHILE THE SNOWFLAKE EQUIVALENT DOES NOT. ***/ TO ARRAY_SIZE(:v_arr) /*** SSC-FDM-OR0075 - COLLECTION 'LAST' WAS TRANSLATED ASSUMING A DENSE ARRAY. ORACLE 'LAST' RETURNS NULL FOR AN EMPTY COLLECTION WHILE THE SNOWFLAKE EQUIVALENT DOES NOT. ***/
                                                                                                                                                                                                                                                                                                                                                                                                       --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                                                                                                                                                                                                                                                                                                                                                                                       LOOP
                                                                                                                                                                                                                                                                                                                                                                                                         v_x := :v_arr[:i - 1];
                                                                                                                                                                                                                                                                                                                                                                                                       END LOOP;
  END;
$$;
```

#### Best Practices

- Add explicit empty-array handling and review sparse indexes.

## SSC-FDM-OR0076

DBMS\_UTILITY.FORMAT\_ERROR\_STACK translated to SQLERRM.

#### Description

`SQLERRM` preserves only the top-most message; chained messages and Oracle backtrace lines are dropped.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT DBMS_UTILITY.FORMAT_ERROR_STACK() FROM DUAL;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
SQLERRM /*** SSC-FDM-OR0076 - 'FORMAT_ERROR_STACK' WAS TRANSLATED TO SQLERRM, WHICH RETURNS ONLY THE TOP-MOST ERROR MESSAGE; ANY CHAINED MESSAGES AND ORA-06512 BACKTRACE LINES FROM THE ORACLE ERROR STACK ARE DROPPED. ***/
FROM
DUAL;
```

#### Best Practices

- Add application logging when the full error stack is required.

## SSC-FDM-OR0077

FLATTEN may drop NULL scalar elements, so row counts can differ from Oracle

#### Description

Snowflake `FLATTEN` can skip null scalar elements and return fewer rows than Oracle `TABLE()`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
DECLARE
  v DBMS_SQL.VARCHAR2A;
  n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM TABLE(v);
END;
```

##### Output Code:

##### Snowflake

Copy code

```
DECLARE
  v ARRAY /*** SSC-FDM-OR0084 - COLLECTION TYPE 'DBMS_SQL.VARCHAR2A' WAS MAPPED TO A SNOWFLAKE ARRAY; ELEMENT INDEXING WAS ADJUSTED FROM 1-BASED TO 0-BASED. ***/;
  n NUMBER(38, 18);
BEGIN
  SELECT
    COUNT(*)
  INTO
    :n
  FROM
    --** SSC-FDM-OR0077 - SNOWFLAKE'S FLATTEN SILENTLY SKIPS NULL SCALAR ELEMENTS OF THE COLLECTION, SO THIS UNNEST MAY RETURN FEWER ROWS THAN ORACLE'S TABLE() WHEN THE COLLECTION CONTAINS NULL ELEMENTS. **
    (
      SELECT
        VALUE :: VARCHAR AS COLUMN_VALUE
      FROM
        TABLE(FLATTEN(INPUT => :v))
    );
END;
```

#### Best Practices

- Test null-containing collections and preserve placeholders when row counts matter.

## SSC-FDM-OR0079

Partition-extension clause replaced with an equivalent WHERE predicate.

#### Description

SnowConvert AI derives a predicate from known partition boundaries.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE S.PART_RANGE (id NUMBER, amt NUMBER)
PARTITION BY RANGE (amt)
(PARTITION p_low VALUES LESS THAN (100),
 PARTITION p_mid VALUES LESS THAN (200),
 PARTITION p_max VALUES LESS THAN (MAXVALUE));
SELECT * FROM S.PART_RANGE PARTITION(p_low);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE S.PART_RANGE (
  id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  amt NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
;

SELECT
  --** SSC-FDM-OR0079 - PARTITION TARGETING IS NOT SUPPORTED IN SNOWFLAKE AND WAS REPLACED WITH AN EQUIVALENT WHERE PREDICATE DERIVED FROM THE TABLE'S PARTITION BOUNDARIES. VERIFY IT TARGETS THE INTENDED ROWS. **
  *
FROM
  S.PART_RANGE
WHERE
  amt < 100;
```

#### Best Practices

- Verify that the predicate selects exactly the intended rows.

## SSC-FDM-OR0080

Partition-extension clause removed.

#### Description

The Oracle partition-extension clause is removed when no equivalent predicate can be recovered.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
INSERT INTO SALES PARTITION (P_JAN) VALUES (1, 100);
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT INTO SALES
-- --** SSC-FDM-OR0080 - PARTITION-EXTENSION CLAUSE IS NOT SUPPORTED IN SNOWFLAKE AND WAS REMOVED. IF IT RESTRICTED THE AFFECTED ROWS, VERIFY THE WHERE CLAUSE COVERS THE INTENDED PARTITION. **
-- PARTITION (P_JAN)
VALUES (1, 100);
```

#### Best Practices

- Confirm the remaining predicate restricts rows as intended.

## SSC-FDM-OR0081

Cross-schema reference auto-bound through a synonym

#### Description

SnowConvert AI resolves the reference through an Oracle cross-schema synonym.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE "WH_FL"."FL_ACR_BOOKING" ("BOOKING_STATUS" VARCHAR2(10));
CREATE OR REPLACE SYNONYM "COM_WH"."FL_ACR_BOOKING" FOR "WH_FL"."FL_ACR_BOOKING";
SELECT es.booking_status FROM fl_acr_booking es;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "WH_FL"."FL_ACR_BOOKING" (
  "BOOKING_STATUS" VARCHAR(10)
)
;

----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM "COM_WH"."FL_ACR_BOOKING" FOR "WH_FL"."FL_ACR_BOOKING"

SELECT
   es.booking_status
FROM
   --** SSC-FDM-OR0081 - 'fl_acr_booking' WAS AUTO-BOUND TO 'WH_FL.FL_ACR_BOOKING' THROUGH A CROSS-SCHEMA SYNONYM. VERIFY 'WH_FL.FL_ACR_BOOKING' IS THE INTENDED OBJECT. **
   WH_FL.FL_ACR_BOOKING es;
```

#### Best Practices

- Verify the inferred schema and object.

## SSC-FDM-OR0082

Exception code is not supported in Snowflake and a supported code is used as a workaround.

#### Description

A Snowflake-supported code replaces the Oracle code while preserving its message.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE TEST
AS
  v_msg VARCHAR2(100);
BEGIN
  raise_application_error(-20000, 'First message');
  raise_application_error(-20001, 'Second message');
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE = -20000 THEN
      v_msg := 'matched';
    END IF;
END TEST;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE TEST ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    v_msg VARCHAR(100);
    FIRST_MESSAGE_EXCEPTION_CODE_0 EXCEPTION (-20002, 'FIRST MESSAGE');
    SECOND_MESSAGE_EXCEPTION_CODE_1 EXCEPTION (-20001, 'SECOND MESSAGE');
  BEGIN
    --** SSC-FDM-OR0082 - EXCEPTION CODE -20000 IS NOT SUPPORTED IN SNOWFLAKE. CODE -20002 IS USED AS A WORKAROUND WITH THE ORIGINAL MESSAGE PRESERVED, SO UPDATE ANY CODE THAT COMPARES SQLCODE TO -20000. **
    RAISE FIRST_MESSAGE_EXCEPTION_CODE_0;
    RAISE SECOND_MESSAGE_EXCEPTION_CODE_1;
  EXCEPTION
    WHEN OTHER THEN
      IF (SQLCODE = -20000) THEN
        v_msg := 'matched';
      END IF;
  END;
$$;
```

#### Best Practices

- Update logic that compares `SQLCODE` to the original number.

## SSC-FDM-OR0083

Associative array variable represented as OBJECT.

#### Description

Writes use `OBJECT_INSERT`, reads use `GET`, and missing keys return null instead of raising `NO_DATA_FOUND`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE p_assoc_ctor
AS
TYPE str_map IS TABLE OF VARCHAR2(100) INDEX BY VARCHAR2(50);
v_map str_map := str_map();
BEGIN
  NULL;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p_assoc_ctor ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
--    --** SSC-FDM-OR0053 - EMBEDDED COLLECTION TYPE DEFINITION 'PL COLLECTION TYPE DEFINITION' WAS REMOVED. COLLECTION VARIABLES ARE TRANSFORMED TO ARRAY BY OTHER RULES. **
--    TYPE str_map IS TABLE OF VARCHAR2(100)
--      INDEX BY VARCHAR2(50);
    --** SSC-FDM-OR0083 - ASSOCIATIVE ARRAY VARIABLE REPRESENTED AS OBJECT. ELEMENT WRITES EMIT OBJECT_INSERT; ELEMENT READS EMIT GET. MISSING-KEY READS RETURN NULL IN SNOWFLAKE (ORACLE RAISES NO_DATA_FOUND). **
    v_map OBJECT := OBJECT_CONSTRUCT();
  BEGIN
    NULL;
  END;
$$;
```

#### Best Practices

- Add explicit missing-key checks where Oracle exception behavior is required.

## SSC-FDM-OR0084

Collection represented as a Snowflake ARRAY; element indexing adjusted from 1-based to 0-based.

#### Description

The Oracle collection becomes `ARRAY` and indexes change from one-based to zero-based.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE p_desc_tab4 (pv IN DBMS_SQL.DESC_TAB4) IS
BEGIN
  NULL;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p_desc_tab4 (pv ARRAY /*** SSC-FDM-OR0084 - COLLECTION TYPE 'DBMS_SQL.DESC_TAB4' WAS MAPPED TO A SNOWFLAKE ARRAY; ELEMENT INDEXING WAS ADJUSTED FROM 1-BASED TO 0-BASED. ***/)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    NULL;
  END;
$$;
```

#### Best Practices

- Review index arithmetic and loop bounds.

## SSC-FDM-OR0085

XMLPI translated to string concatenation.

#### Description

The generated concatenation does not automatically XML-escape values.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT XMLPI(NAME "xml-stylesheet", 'type="text/xsl"') FROM dual;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-OR0085 - XMLPI TRANSLATED TO STRING CONCATENATION. SPECIAL CHARACTERS IN VALUES MAY PRODUCE INVALID XML. **
  IFF('type="text/xsl"' IS NULL, NULL, '<?xml-stylesheet ' || 'type="text/xsl"' || '?>')
FROM
  dual;
```

#### Best Practices

- Escape dynamic names and values.

## SSC-FDM-OR0086

Deduplication DELETE by MIN(ROWID) rewritten as INSERT OVERWRITE.

#### Description

The Oracle deduplication pattern becomes `INSERT OVERWRITE` with `ROW_NUMBER()`.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
DELETE FROM dedup_t WHERE ROWID NOT IN (SELECT MIN(ROWID) FROM dedup_t GROUP BY k);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-OR0086 - DEDUPLICATION BY MIN(ROWID) WAS REWRITTEN AS INSERT OVERWRITE WITH ROW_NUMBER() OVER (PARTITION BY k). ONE ROW PER GROUP IS KEPT AS IN ORACLE, BUT WHICH DUPLICATE SURVIVES IS NOT GUARANTEED. ADD A DETERMINISTIC ORDER BY IF A SPECIFIC ROW MUST WIN. **
INSERT OVERWRITE INTO dedup_t
SELECT * FROM dedup_t
QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY NULL) = 1;
```

#### Best Practices

- Add deterministic ordering when a specific duplicate must win.

## SSC-FDM-OR0087

ORDER BY ROWID sort key removed.

#### Description

Snowflake has no physical `ROWID` equivalent, so row and tie order are not guaranteed.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
SELECT c1 FROM t1 t ORDER BY t.ROWID;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-OR0087 - ORDER BY ROWID IS NOT SUPPORTED IN SNOWFLAKE AND THE ROWID SORT KEY WAS REMOVED. ORACLE'S PHYSICAL ROW ORDER HAS NO SNOWFLAKE EQUIVALENT; ROW ORDER (OR TIE ORDER AMONG THE REMAINING KEYS) IS NOT GUARANTEED - ADD A DETERMINISTIC KEY IF ORDER MATTERS. **
SELECT
  c1
FROM
  t1 t;
```

#### Best Practices

- Add stable business-key ordering.

## SSC-FDM-OR0088

ALTER TYPE attribute evolution folded into CREATE TYPE

#### Description

Supported changes are folded into `CREATE OR REPLACE TYPE`; Snowflake does not cascade them to dependent columns.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TYPE booking_t AS OBJECT (amount NUMBER, currency VARCHAR2(3));
ALTER TYPE booking_t ADD ATTRIBUTE (incentive NUMBER(5,2)) CASCADE NOT INCLUDING TABLE DATA;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-OR0088 - ALTER TYPE ATTRIBUTE CHANGES WERE FOLDED INTO THE CREATE TYPE ATTRIBUTE LIST. SNOWFLAKE DOES NOT SUPPORT ALTER TYPE AND DOES NOT CASCADE TYPE CHANGES TO DEPENDENT TABLE COLUMNS. **
CREATE OR REPLACE TYPE booking_t AS OBJECT (amount NUMBER(38, 18), currency VARCHAR(3), incentive NUMBER(5, 2));
```

#### Best Practices

- Migrate dependent table columns explicitly.

## SSC-FDM-OR0157

XMLSERIALIZE translated to TO\_VARCHAR.

#### Description

Indentation and Oracle `DOCUMENT` versus `CONTENT` distinctions are not preserved.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE demo_xmlserialize AS
  v_doc_data_xmltype XMLTYPE;
  v_doc_data_clob    CLOB;
BEGIN
  SELECT XMLSERIALIZE(
           CONTENT v_doc_data_xmltype.extract('/*') AS CLOB INDENT
         )
    INTO v_doc_data_clob
    FROM dual;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE demo_xmlserialize ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    v_doc_data_xmltype VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XMLTYPE DATA TYPE CONVERTED TO VARIANT ***/!!!;
    v_doc_data_clob VARCHAR;
  BEGIN
    SELECT
      --** SSC-FDM-OR0157 - XMLSERIALIZE TRANSLATED TO TO_VARCHAR. INDENT PRETTY-PRINTING AND DOCUMENT/CONTENT DISTINCTIONS ARE NOT PRESERVED. **
      TO_VARCHAR(
                  !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - V_DOC_DATA_XMLTYPE.EXTRACT FUNCTION NOT SUPPORTED ***/!!!
                  v_doc_data_xmltype.extract('/*'))
    INTO
      v_doc_data_clob
    FROM
      dual;
  END;
$$;
```

#### Best Practices

- Validate serialized text and apply presentation formatting separately.

## SSC-FDM-OR0158

Pipelined function converted to a UDTF; PIPE ROW side effects and emission timing not preserved.

#### Description

The UDTF preserves query results, but not `PIPE ROW` side effects or emission timing.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
      CREATE OR REPLACE FUNCTION one_row RETURN obj_tab PIPELINED IS
      BEGIN
          pipe row (obj(1, 'A'));
          RETURN;
      END;
```

##### Output Code:

##### Snowflake

Copy code

```
                     --** SSC-FDM-OR0158 - PIPELINED FUNCTION CONVERTED TO A TABLE FUNCTION (UDTF); PIPE ROW SIDE EFFECTS AND EMISSION TIMING ARE NOT PRESERVED. **
                     CREATE OR REPLACE FUNCTION one_row ()
                     RETURNS TABLE (
                       COLUMN1 NUMBER(38, 18),
                       COLUMN2 STRING
                     )
                     LANGUAGE SQL
                     AS
                     $$
                       SELECT
                         1,
                         'A'
                     $$;
```

#### Best Practices

- Validate row content and move side effects outside the UDTF.

## SSC-FDM-OR0160

DBMS\_UTILITY call-stack/backtrace member replaced with SQLERRM.

#### Description

Snowflake preserves only the error message, not the PL/SQL call stack or backtrace.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
                        SELECT DBMS_UTILITY.FORMAT_ERROR_BACKTRACE() FROM DUAL;
```

##### Output Code:

##### Snowflake

Copy code

```
                            SELECT
                            SQLERRM /*** SSC-FDM-OR0160 - 'FORMAT_ERROR_BACKTRACE' WAS REPLACED WITH SQLERRM; SNOWFLAKE HAS NO PL/SQL BACKTRACE / CALL STACK, SO ONLY THE ERROR MESSAGE IS PRESERVED. ***/
                            FROM
                            DUAL;
```

#### Best Practices

- Add explicit tracing when stack details are required.

## SSC-FDM-OR0161

ROWID/UROWID is not a native Snowflake type

#### Description

SnowConvert AI stores the value as `VARCHAR`, not as a physical row locator.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE t_rowid_col (rid ROWID);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE t_rowid_col (
  rid VARCHAR(18) /*** SSC-FDM-OR0161 - ROWID IS NOT A NATIVE SNOWFLAKE TYPE. THE VALUE IS STORED AS VARCHAR AND IS A STRING, NOT A PHYSICAL ROW LOCATOR. ***/
);
```

#### Best Practices

- Replace locator logic with stable primary or surrogate keys.

## SSC-FDM-OR0162

Binary-equivalent collation removed.

#### Description

The collation is removed because it matches Snowflake’s default binary comparison.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE NLSCOMP_T2 (INTEGRATION_ID VARCHAR2(200 BYTE) COLLATE USING_NLS_COMP);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-OR0162 - COLLATE REMOVED - MATCHES SNOWFLAKE'S DEFAULT BINARY COMPARISON. FOR CASE/ACCENT-INSENSITIVE OR LINGUISTIC COMPARISON, ADD AN EXPLICIT COLLATION LIKE COLLATE 'EN-CI'. **
CREATE OR REPLACE TABLE NLSCOMP_T2 (INTEGRATION_ID VARCHAR(200));
```

#### Best Practices

- Add a collation only when different comparison rules are required.

## SSC-FDM-OR0163

Oracle collation has no Snowflake equivalent.

#### Description

The unsupported collation is removed and default binary comparison applies.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE NLSCOMP_T6E (C1 VARCHAR2(40 BYTE) COLLATE GENERIC_M);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE NLSCOMP_T6E (
  C1 VARCHAR(40)
  -- --** SSC-FDM-OR0163 - COLLATE GENERIC_M REMOVED - NO SNOWFLAKE EQUIVALENT; COLUMN USES DEFAULT BINARY COMPARISON. ADD AN EXPLICIT COLLATION IF NEEDED. **
  -- COLLATE GENERIC_M
);
```

#### Best Practices

- Select and test the closest supported Snowflake collation.

## SSC-FDM-OR0164

Statement-level DEFAULT COLLATION is not supported.

#### Description

Snowflake has no table-wide or view-wide equivalent, so the clause is removed.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE NLSCOMP_T5C (
  C1 VARCHAR2(20 BYTE),
  C2 VARCHAR2(20 BYTE)
) DEFAULT COLLATION BINARY_CI;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-OR0164 - DEFAULT COLLATION BINARY_CI REMOVED - SNOWFLAKE HAS NO TABLE/VIEW-WIDE DEFAULT COLLATION; COLUMNS USE DEFAULT BINARY COMPARISON. ADD PER-COLUMN COLLATE IF NEEDED. **
CREATE OR REPLACE TABLE NLSCOMP_T5C (
  C1 VARCHAR(20),
  C2 VARCHAR(20)
);
```

#### Best Practices

- Apply supported collations to individual columns or expressions.

## SSC-FDM-OR0165

PRAGMA AUTONOMOUS\_TRANSACTION commented out. This routine owns BEGIN TRANSACTION … COMMIT as a scoped transaction.

#### Description

SnowConvert AI emits a scoped transaction when the routine has a matching commit.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE PROCEDURE mf_autotxn_multi IS
  PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
  INSERT INTO audit_tbl VALUES (1);
  COMMIT;
  INSERT INTO audit_tbl VALUES (2);
  ROLLBACK;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE mf_autotxn_multi ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
--  --** SSC-FDM-OR0165 - PRAGMA AUTONOMOUS_TRANSACTION WAS COMMENTED OUT. THIS ROUTINE OWNS BEGIN TRANSACTION ... COMMIT SO IT RUNS AS A SCOPED TRANSACTION THAT SURVIVES THE CALLER'S ROLLBACK. **
--  PRAGMA AUTONOMOUS_TRANSACTION;
  BEGIN
    BEGIN TRANSACTION;
    INSERT INTO audit_tbl
    VALUES (1);
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO audit_tbl
    VALUES (2);
    ROLLBACK;
  END;
$$;
```

#### Best Practices

- Verify transaction ownership and failure behavior independently from the caller.

## SSC-FDM-OR0166

PRAGMA AUTONOMOUS\_TRANSACTION commented out. No COMMIT or ROLLBACK was present to pair with a scoped transaction.

#### Description

No scoped transaction is generated, so transaction control affects the caller’s session.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE pragma_proc
AS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    NULL;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE pragma_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
--  --** SSC-FDM-OR0166 - PRAGMA AUTONOMOUS_TRANSACTION WAS COMMENTED OUT. A COMMIT OR ROLLBACK HERE AFFECTS THE CALLER'S SESSION TRANSACTION. IF THE WORK MUST BE INDEPENDENT, MOVE IT TO A SEPARATE SESSION OR JOB. **
--  PRAGMA AUTONOMOUS_TRANSACTION;
  BEGIN
    NULL;
  END;
$$;
```

#### Best Practices

- Move independent work to a separate session or job.

## SSC-FDM-OR0167

Oracle SELECT INTO enforces single-row results. Snowflake cursor FETCH does not.

#### Description

The generated cursor fetch does not reproduce Oracle’s single-row cardinality check.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE PROC01
IS
  number_variable INTEGER;
BEGIN
  EXECUTE IMMEDIATE 'SELECT 1 FROM DUAL' INTO number_variable;
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
  DECLARE
    number_variable INTEGER;
  BEGIN
    LET execute_immediate_query_1 VARCHAR := 'SELECT 1 FROM DUAL';
    LET execute_immediate_result_1 RESULTSET := (
      EXECUTE IMMEDIATE :execute_immediate_query_1
    );
    LET execute_immediate_cursor_1 CURSOR
    FOR
      execute_immediate_result_1;
    OPEN execute_immediate_cursor_1;
    --** SSC-FDM-OR0167 - ORACLE SELECT INTO ENFORCES SINGLE-ROW RESULTS. SNOWFLAKE CURSOR FETCH DOES NOT. **
    FETCH execute_immediate_cursor_1 INTO number_variable;
    CLOSE execute_immediate_cursor_1;
  END;
$$;
```

#### Best Practices

- Add an explicit check when zero or multiple rows must raise an error.

## SSC-FDM-OR0168

DBMS\_SESSION.FREE\_UNUSED\_USER\_MEMORY is a no-op in Snowflake.

#### Description

The original call is commented out because Snowflake manages session memory.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
DBMS_SESSION.FREE_UNUSED_USER_MEMORY;
```

##### Output Code:

##### Snowflake

Copy code

```
--    --** SSC-FDM-OR0168 - DBMS_SESSION.FREE_UNUSED_USER_MEMORY IS NOT SUPPORTED IN SNOWFLAKE. THE CALL IS A NO-OP AND THE ORIGINAL STATEMENT WAS COMMENTED OUT. **
--    DBMS_SESSION.FREE_UNUSED_USER_MEMORY
```

#### Best Practices

- Remove dependencies on manual session-memory release.

## SSC-FDM-OR0169

DBMS\_SESSION.SWITCH\_CURRENT\_CONSUMER\_GROUP is not supported in Snowflake.

#### Description

The call is commented out because Snowflake assigns compute through warehouses.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
DBMS_SESSION.SWITCH_CURRENT_CONSUMER_GROUP('DBA_GROUP', old_group, FALSE);
```

##### Output Code:

##### Snowflake

Copy code

```
--    --** SSC-FDM-OR0169 - DBMS_SESSION.SWITCH_CURRENT_CONSUMER_GROUP IS NOT SUPPORTED IN SNOWFLAKE. CONFIGURE THE WAREHOUSE ON THE JOB OR TASK; THE ORIGINAL STATEMENT WAS COMMENTED OUT. **
--    DBMS_SESSION.SWITCH_CURRENT_CONSUMER_GROUP('DBA_GROUP', old_group, FALSE)
```

#### Best Practices

- Configure the warehouse on the invoking job or task.

## SSC-FDM-OR0170

DBMS\_SESSION.CLOSE\_DATABASE\_LINK is not supported in Snowflake.

#### Description

The call is commented out because Snowflake does not use Oracle database links.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
DBMS_SESSION.CLOSE_DATABASE_LINK('MY_LINK');
```

##### Output Code:

##### Snowflake

Copy code

```
--    --** SSC-FDM-OR0170 - DBMS_SESSION.CLOSE_DATABASE_LINK IS NOT SUPPORTED IN SNOWFLAKE. SNOWFLAKE DOES NOT USE ORACLE DATABASE LINKS; THE ORIGINAL STATEMENT WAS COMMENTED OUT. **
--    DBMS_SESSION.CLOSE_DATABASE_LINK('MY_LINK')
```

#### Best Practices

- Replace database-link dependencies with supported connectivity.

## SSC-FDM-OR0171

DBMS\_SESSION.SET\_NLS is not supported in Snowflake. ALTER SESSION is used as a workaround.

#### Description

SnowConvert AI maps supported behavior to a Snowflake session parameter.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PROCEDURE dbms_session_set_nls_proc
IS
BEGIN
    DBMS_SESSION.SET_NLS('nls_date_format', '''dd/mm/yyyy HH:MI:SS AM''');
    DBMS_SESSION.SET_NLS('NLS_TIMESTAMP_FORMAT', '''yyyy-mm-dd HH24:MI:SS.FF''');
    DBMS_SESSION.SET_NLS('NLS_TIMESTAMP_TZ_FORMAT', '''yyyy-mm-dd HH:MI:SS.FF AM TZH:TZM''');
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE dbms_session_set_nls_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-OR0171 - DBMS_SESSION.SET_NLS IS NOT SUPPORTED IN SNOWFLAKE. ALTER SESSION IS USED AS A WORKAROUND. **
    ALTER SESSION SET DATE_INPUT_FORMAT = 'DD/MM/YYYY HH12:MI:SS AM';
    --** SSC-FDM-OR0171 - DBMS_SESSION.SET_NLS IS NOT SUPPORTED IN SNOWFLAKE. ALTER SESSION IS USED AS A WORKAROUND. **
    ALTER SESSION SET TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
    --** SSC-FDM-OR0171 - DBMS_SESSION.SET_NLS IS NOT SUPPORTED IN SNOWFLAKE. ALTER SESSION IS USED AS A WORKAROUND. **
    ALTER SESSION SET TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH12:MI:SS.FF AM TZH:TZM';
  END;
$$;
```

#### Best Practices

- Verify the mapped parameter’s parsing and formatting effects.

## SSC-FDM-OR0172

Snowflake does not preserve Oracle constraint enforcement state, so this ALTER TABLE clause was removed; review the resulting enforcement behavior.

#### Description

SnowConvert AI removes Oracle constraint-state clauses that Snowflake does not preserve.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE t (val NUMBER CONSTRAINT nn_val NOT NULL DISABLE);
ALTER TABLE t DISABLE CONSTRAINT nn_val;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE t (val NUMBER(38, 18));

----** SSC-FDM-OR0172 - SNOWFLAKE DOES NOT PRESERVE ORACLE CONSTRAINT ENFORCEMENT STATE, SO THIS ALTER TABLE CLAUSE WAS REMOVED. REVIEW THE RESULTING ENFORCEMENT BEHAVIOR. **
--ALTER TABLE t DISABLE CONSTRAINT nn_val
```

#### Best Practices

- Review resulting enforcement and validation behavior.

## SSC-FDM-OR0173

Triggers live outside the table definition in Snowflake, so this ALTER TABLE clause that enables or disables triggers was removed.

#### Description

SnowConvert AI removes the table-level trigger state clause.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
ALTER TABLE SOMENAME DISABLE ALL TRIGGERS;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-OR0173 - TRIGGERS LIVE OUTSIDE THE TABLE DEFINITION IN SNOWFLAKE, SO THIS ALTER TABLE CLAUSE THAT ENABLES OR DISABLES TRIGGERS WAS REMOVED. **
--ALTER TABLE SOMENAME
--DISABLE ALL TRIGGERS
```

#### Best Practices

- Redesign trigger behavior with tasks, streams, or application logic.

## SSC-FDM-OR0174

Snowflake manages physical storage automatically, so this ALTER TABLE clause that sets a physical or storage property was removed.

#### Description

SnowConvert AI removes Oracle physical-storage properties.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
ALTER TABLE SOMENAME SHRINK SPACE COMPACT CASCADE;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-OR0174 - SNOWFLAKE MANAGES PHYSICAL STORAGE AUTOMATICALLY, SO THIS ALTER TABLE CLAUSE THAT SETS A PHYSICAL OR STORAGE PROPERTY WAS REMOVED. **
--ALTER TABLE SOMENAME
--SHRINK SPACE COMPACT CASCADE
```

#### Best Practices

- Consider clustering only when workload evidence shows poor pruning.

## SSC-FDM-OR0175

A named NOT NULL disable was converted to ALTER … DROP NOT NULL. The constraint definition is not kept.

#### Description

The generated statement drops `NOT NULL`; the named constraint definition is not retained.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE t (val NUMBER CONSTRAINT nn_val NOT NULL);
ALTER TABLE t DISABLE CONSTRAINT nn_val;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE t (val NUMBER(38, 18) NOT NULL);

--** SSC-FDM-OR0175 - A NAMED NOT NULL DISABLE WAS CONVERTED TO ALTER ... DROP NOT NULL. THE CONSTRAINT DEFINITION IS NOT KEPT. **
ALTER TABLE t ALTER val DROP NOT NULL;
```

#### Best Practices

- Preserve required metadata separately and verify nullability.

## SSC-FDM-OR0176

Generated SELECT INTO collection write-back does not validate its integer OBJECT key.

#### Description

The generated `OBJECT` write-back omits Oracle validation for null, subtype-range, and 32-bit-range indexes.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE FUNCTION frf_probe RETURN NUMBER IS
  TYPE typ_ids IS TABLE OF NUMBER INDEX BY BINARY_INTEGER;
  t_ids typ_ids;
  ii NUMBER := 1;
BEGIN
  SELECT 1 INTO t_ids(ii) FROM DUAL;
  RETURN t_ids(ii);
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION frf_probe ()
RETURNS NUMBER(38, 18)
LANGUAGE SQL
AS
$$
  DECLARE
--    --** SSC-FDM-OR0053 - EMBEDDED COLLECTION TYPE DEFINITION 'PL COLLECTION TYPE DEFINITION' WAS REMOVED. COLLECTION VARIABLES ARE TRANSFORMED TO ARRAY BY OTHER RULES. **
--    TYPE typ_ids IS TABLE OF NUMBER
--      INDEX BY BINARY_INTEGER;
    --** SSC-FDM-OR0083 - ASSOCIATIVE ARRAY VARIABLE REPRESENTED AS OBJECT. ELEMENT WRITES EMIT OBJECT_INSERT; ELEMENT READS EMIT GET. MISSING-KEY READS RETURN NULL IN SNOWFLAKE (ORACLE RAISES NO_DATA_FOUND). **
    t_ids OBJECT := OBJECT_CONSTRUCT();
    ii NUMBER(38, 18) := 1;
  BEGIN
    LET SELECT_INTO_TEMP_1 VARIANT := null;
    SELECT_INTO_TEMP_1 := 1;
    --** SSC-FDM-OR0176 - THE GENERATED SELECT INTO COLLECTION WRITE-BACK USES A SNOWFLAKE OBJECT KEY, WHICH DOES NOT REPRODUCE ORACLE'S INTEGER INDEX VALIDATION FOR NULL, SUBTYPE RANGE, OR 32-BIT RANGE. **
    t_ids := OBJECT_INSERT(COALESCE(t_ids, OBJECT_CONSTRUCT()), TO_VARCHAR(CAST(ii AS INTEGER)), SELECT_INTO_TEMP_1, true);
    RETURN NULLIF(GET(:t_ids, TO_VARCHAR(CAST(:ii AS INTEGER))), PARSE_JSON('null'));
  END;
$$;
```

#### Best Practices

- Validate collection indexes explicitly before write-back.
