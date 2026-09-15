# Teradata - SQL to Snowflake Scripting (Procedures)

## ABORT and ROLLBACK

Translation reference to convert Teradata ABORT and ROLLBACK statements to Snowflake Scripting

### Description

Teradata’s `ABORT` and `ROLLBACK` statements are replaced by a `ROLLBACK` statement in Snowflake Scripting.

For more information on Teradata [ABORT](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/c6KYQ4ySu4QTCkKS4f5A2w) and for [ROLLBACK](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/ZddbA8dTQ1LNcHwmCn8BVg).

Copy code

```
 ABORT [abort_message] [FROM option] [WHERE abort_condition];

ROLLBACK [WORK] [abort_message] [FROM clause] [WHERE clause];
```

### Sample Source Patterns

#### Basic ABORT and ROLLBACK

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE procedureBasicAbort()
BEGIN
    ABORT;
    ROLLBACK;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureBasicAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        ROLLBACK;
        ROLLBACK;
    END;
$$;
```

#### Conditional ABORT and ROLLBACK

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE procedureWhereAbort(AnotherValueProc INTEGER)
BEGIN
    ABORT WHERE AValueProc > 2;

    ROLLBACK WHERE (AnotherValueProc > 2);
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureWhereAbort (ANOTHERVALUEPROC INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (AValueProc > 2) THEN
            ROLLBACK;
        END IF;
        IF (:AnotherValueProc > 2) THEN
            ROLLBACK;
        END IF;
    END;
$$;
```

#### ABORT and ROLLBACK with table references and FROM clause

##### Teradata

##### Query

Copy code

```
 CREATE TABLE  ReferenceTable
    (ColumnValue INTEGER);

CREATE TABLE  ReferenceTable2
    (ColumnValue INTEGER);

REPLACE PROCEDURE procedureFromAbort()
BEGIN
    ROLLBACK FROM ReferenceTable, ReferenceTable2
	WHERE ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
    ABORT FROM ReferenceTable, ReferenceTable2
        WHERE ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE TABLE ReferenceTable
(
	ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE TABLE ReferenceTable2
(
	ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE procedureFromAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		LET _ROW_COUNT FLOAT;
		SELECT
			COUNT(*)
		INTO
			_ROW_COUNT
			FROM
			ReferenceTable,
			ReferenceTable2
				WHERE
			ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
			IF (_ROW_COUNT > 0) THEN
			ROLLBACK;
			END IF;
			SELECT
			COUNT(*)
			INTO
			_ROW_COUNT
			FROM
			ReferenceTable,
			ReferenceTable2
			        WHERE
			ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
			IF (_ROW_COUNT > 0) THEN
			ROLLBACK;
			END IF;
	END;
$$;
```

#### ABORT and ROLLBACK with table references without FROM clause

##### Teradata

##### Query

Copy code

```
 CREATE TABLE  ReferenceTable
    (ColumnValue INTEGER);

REPLACE PROCEDURE procedureFromTableAbort()
BEGIN
    ROLLBACK WHERE ReferenceTable.ColumnValue > 2;
    ABORT WHERE ReferenceTable.ColumnValue > 4;
END;
```

##### Snowflake Scripting

##### Abort and rollback

Copy code

```
 CREATE OR REPLACE TABLE ReferenceTable
(
    ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE procedureFromTableAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET _ROW_COUNT FLOAT;
        SELECT
            COUNT(*)
        INTO
            _ROW_COUNT
        FROM
            ReferenceTable
            WHERE
            ReferenceTable.ColumnValue > 2;
            IF (_ROW_COUNT > 0) THEN
            ROLLBACK;
            END IF;
            SELECT
            COUNT(*)
            INTO
            _ROW_COUNT
            FROM
            ReferenceTable
            WHERE
            ReferenceTable.ColumnValue > 4;
            IF (_ROW_COUNT > 0) THEN
            ROLLBACK;
            END IF;
    END;
$$;
```

### Known Issues

#### 1. Custom Error Message

Even though the ROLLBACK AND ABORT are supported, using them with a custom error message is not supported.

##### Teradata

##### Error message

Copy code

```
 ABORT 'Error message for abort';
ROLLBACK  'Error message for rollback';
```

##### Snowflake Scripting

##### Error message

Copy code

```
 ABORT 'Error message for abort';
ROLLBACK  'Error message for rollback';
```

##### 2. Aggregate function

The use of the aggregate function combined with ABORT/ROLLBACK is not supported

##### Teradata

##### Aggregate function

Copy code

```
 ROLLBACK WHERE SUM(ATable.AValue) < 2;
ABORT WHERE SUM(ATable.AValue) < 2;
```

##### Snowflake Scripting

##### Aggregate function

Copy code

```
 ROLLBACK WHERE SUM(ATable.AValue) < 2;
ABORT WHERE SUM(ATable.AValue) < 2;
```

### Related EWIs

No related EWIs.

## ACTIVITY\_COUNT

Translation specification for the ACTIVITY\_COUNT status variable.

### Description

The `ACTIVITY_COUNT` status variable returns the number of rows affected by an SQL DML statement in an embedded SQL or stored procedure application. For more information, see the [Teradata ACTIVITY\_COUNT documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/Result-Code-Variables/ACTIVITY_COUNT).

There is no direct equivalent in Snowflake. However, there is a workaround to emulate the `ACTIVITY_COUNT`’s behavior. One must simply use the following query:

Copy code

```
 SELECT $1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

This query retrieves and returns the first column of the result set from the last executed query in the current session. Furthermore, `$1` can be replaced by `"number of rows inserted"`, `"number of rows updated"` or `"number of rows deleted"` based on the query type.

As expected, this translation behaves like its Teradata counterpart only when no other queries besides the SQL DML statement are executed before calling `LAST_QUERY_ID`.

### Sample Source Patterns

#### Setup data

##### Teradata

##### Query

Copy code

```
 CREATE TABLE employees (
    employee_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10,2),
    PRIMARY KEY (employee_id)
);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (1, 'John', 'Doe', 10, 60000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (2, 'Johny', 'Doey', 10, 65000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (3, 'Max', 'Smith', 10, 70000.00);

DROP TABLE activity_log;
CREATE TABLE activity_log (
    log_id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    operation VARCHAR(200),
    row_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id)
);
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE TABLE employees (
    employee_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10,2),
    PRIMARY KEY (employee_id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (1, 'John', 'Doe', 10, 60000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (2, 'Johny', 'Doey', 10, 65000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (3, 'Max', 'Smith', 10, 70000.00);

CREATE OR REPLACE TABLE activity_log (
    log_id INT DEFAULT activity_log_log_id.NEXTVAL NOT NULL,
    operation VARCHAR(200),
    row_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (log_id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
;
```

#### Supported usage

##### *Teradata*

##### Query

Copy code

```
 REPLACE PROCEDURE UpdateEmployeeSalaryAndLog ()
BEGIN
    DECLARE row_count1 INT;

    UPDATE employees
    SET salary = 80000
    WHERE department_id = 10;

    -- Get the ACTIVITY_COUNT
    SET row_count1 = ACTIVITY_COUNT;

    -- Insert the ACTIVITY_COUNT into the activity_log table
    INSERT INTO activity_log (operation, row_count)
    VALUES ('UPDATE WHERE dept=10', row_count1);
END;

CALL UpdateEmployeeSalaryAndLog();

SELECT * FROM ACTIVITY_LOG;
```

##### Result

Copy code

```
LOG_ID | OPERATION    	      | ROW_COUNT | LOG_TIMESTAMP              |
-------+----------------------+-----------+----------------------------+
1      | UPDATE WHERE dept=10 |	3         | 2024-07-10 15:58:46.490000 |
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE UpdateEmployeeSalaryAndLog ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        row_count1 INT;
    BEGIN

        UPDATE employees
    SET salary = 80000
    WHERE department_id = 10;

    -- Get the ACTIVITY_COUNT
        row_count1 := (
    SELECT
        $1
    FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;

        -- Insert the ACTIVITY_COUNT into the activity_log table
        INSERT INTO activity_log (operation, row_count)
        VALUES ('UPDATE WHERE dept=10', :row_count1);
    END;
$$;

CALL UpdateEmployeeSalaryAndLog();

SELECT
    * FROM
    ACTIVITY_LOG;
```

##### Result

Copy code

```
LOG_ID | OPERATION    	      | ROW_COUNT | LOG_TIMESTAMP            |
-------+----------------------+-----------+--------------------------+
102    | UPDATE WHERE dept=10 |	3         | 2024-07-11T12:42:35.280Z |
```

### Known Issues

1. If `ACTIVITY_COUNT` is called twice or more times before executing a DML statement, the transformation might not return the expected values. See [SSC-FDM-TD0033](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0033).
2. If `ACTIVITY_COUNT` is called after a non DML statement was executed, the transformation will not return the expected values. See [SSC-FDM-TD0033](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0033).
3. `ACTIVITY_COUNT` requires manual fixing when inside a `SELECT/SET INTO VARIABLE` statement and was not able to be identified as a column name. See [SSC-EWI-TD0003](../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0003).

### Related EWIs

1. [SSC-FDM-TD0033](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0033): ‘ACTIVITY\_COUNT’ TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS.

## BEGIN END

Translation reference to convert Teradata BEGIN END clause to Snowflake Scripting

### BEGIN END TRANSACTION

#### Description

> Defines the beginning of an explicit logical transaction in Teradata session mode.

For more information, see the [Teradata BEGIN END Transaction documentation](https://docs.teradata.com/r/2_MC9vCtAJRlKle2Rpb0mA/EhQtM73NDooSYqTcaZEHzQ).

Copy code

```
 [ BEGIN TRANSACTION | BT ]
     statement
     [ statement ]... ]
[ END TRANSACTION | ET ];
```

#### Sample Source Pattern

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    BEGIN TRANSACTION
        SET HELLOSTRING = 'HELLO WORLD';
    END TRANSACTION;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN

        BEGIN TRANSACTION;
        HELLOSTRING := 'HELLO WORLD';
        COMMIT;
    END;
$$;
```

### BEGIN END REQUEST

#### Description

> Delimits a SQL multistatement request

For more information, see the [Teradata BEGIN END Request documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Definition-Language-Syntax-and-Examples/March-2019/Procedure-Statements/CREATE-PROCEDURE-and-REPLACE-PROCEDURE-SQL-Form/Syntax-Elements/Statement-Options/BEGIN-REQUEST).

Copy code

```
 BEGIN REQUEST
     statement
     [ statement ]... ]
END REQUEST;
```

#### Sample Source Pattern

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    BEGIN REQUEST
        SET HELLOSTRING = 'HELLO WORLD';
    END REQUEST;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN

        BEGIN
            HELLOSTRING := 'HELLO WORLD';
            COMMIT;
        EXCEPTION
            WHEN OTHER THEN
                ROLLBACK;
        END;
    END;
$$;
```

### BEGIN END COMPOUND

#### Description

> Delimits a compound statement in a stored procedure.

For more information, see the [Teradata BEGIN END Compound documentation](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/BEGIN-...-END).

Copy code

```
 label_name: BEGIN
     statement
     [ statement ]... ]
END label_name;
```

#### Sample Source Pattern

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    label_name: BEGIN
        SET HELLOSTRING = 'HELLO WORLD';
    END label_name;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN

        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'label_name LABEL' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        label_name:
        BEGIN
            HELLOSTRING := 'HELLO WORLD';
        END;
    END;
$$;
```

### Known Issues

#### 1. Labels not supported in outer BEGIN END blocks

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE procedureLabelSingle()
label_name: BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    SET HELLOSTRING = 'HELLO WORLD';
END label_name;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureLabelSingle ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'label_name LABEL' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
    label_name:
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN

        HELLOSTRING := 'HELLO WORLD';
    END;
$$;
```

### Related EWIs

1. [SSC-EWI-0058](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.

## CASE

Translation reference to convert Teradata CASE statement to Snowflake Scripting

### Description

> Provides conditional execution of statements based on the evaluation of the specified conditional expression or equality of two operands.
>
> The CASE statement is different from the SQL CASE expression\_,\_ which returns the result of an expression.

For more information, see the [Teradata CASE documentation](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/3nWOY~VPjk9_5FJXaKQNFg).

Copy code

```
 -- Simple CASE
CASE operant_1
[ WHEN operant_2 THEN
     statement
     [ statement ]... ]...
[ ELSE
     statement
     [ statement ]... ]
END CASE;

-- Searched CASE
CASE
[ WHEN conditional_expression THEN
     statement
     [ statement ]... ]...
[ ELSE
     statement
     [ statement ]... ]
END CASE;
```

### Sample Source Patterns

#### Sample auxiliary table

##### Teradata

Copy code

```
 CREATE TABLE case_table(col varchar(30));
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE case_table (
col varchar(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Simple Case

##### Teradata

##### Query

Copy code

```
 CREATE  PROCEDURE caseExample1 ( grade NUMBER )
BEGIN
    CASE grade
        WHEN 10 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Excellent');
        WHEN 9 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Very Good');
        WHEN 8 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Good');
        WHEN 7 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Fair');
        WHEN 6 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Poor');
        ELSE INSERT INTO CASE_TABLE(COL) VALUES ('No such grade');
    END CASE;
END;

CALL caseExample1(6);
CALL caseExample1(4);
CALL caseExample1(10);
SELECT * FROM CASE_TABLE;
```

##### Result

Copy code

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE caseExample1 (GRADE NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CASE (grade)
            WHEN 10 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Excellent');
            WHEN 9 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Very Good');
            WHEN 8 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Good');
            WHEN 7 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Fair');
            WHEN 6 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Poor');
            ELSE
                INSERT INTO CASE_TABLE (COL)
                VALUES ('No such grade');
        END CASE;
    END;
$$;

CALL caseExample1(6);
CALL caseExample1(4);
CALL caseExample1(10);
SELECT * FROM CASE_TABLE;
```

##### Result

Copy code

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

#### Searched Case

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE caseExample2 ( grade NUMBER )
BEGIN
    CASE
        WHEN grade = 10 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Excellent');
        WHEN grade = 9 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Very Good');
        WHEN grade = 8 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Good');
        WHEN grade = 7 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Fair');
        WHEN grade = 6 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Poor');
        ELSE INSERT INTO CASE_TABLE(COL) VALUES ('No such grade');
    END CASE;
END;

CALL caseExample2(6);
CALL caseExample2(4);
CALL caseExample2(10);
SELECT * FROM CASE_TABLE;
```

##### Result

Copy code

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

##### Snowflake Scripting

##### Query

Copy code

```
CREATE OR REPLACE PROCEDURE caseExample2 (GRADE NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CASE
            WHEN :grade = 10 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Excellent');
            WHEN :grade = 9 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Very Good');
            WHEN :grade = 8 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Good');
            WHEN :grade = 7 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Fair');
            WHEN :grade = 6 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Poor');
                ELSE
                INSERT INTO CASE_TABLE (COL)
                VALUES ('No such grade');
        END CASE;
    END;
$$;

CALL caseExample2(6);

CALL caseExample2(4);

CALL caseExample2(10);

SELECT
    * FROM
    CASE_TABLE;
```

##### Result

Copy code

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## CURSOR

Translation reference to convert Teradata CURSOR statement to Snowflake Scripting

### Description

A cursor is a data structure that is used by stored procedures at runtime to point to a resultset returned by an SQL query. For more information, see the [Teradata SQL Cursor Control and DML Statements documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Cursor-Control-and-DML-Statements).

Copy code

```
 DECLARE cursor_name [ SCROLL | NO SCROLL ] CURSOR
     [
          WITHOUT RETURN
          |
          WITH RETURN [ ONLY ] [ TO [ CALLER | CLIENT ] ]
     ]
     FOR
     cursor_specification [ FOR [ READ ONLY | UPDATE ] ]
     |
     statement_name
;
```

Copy code

```
 FETCH [ [ NEXT | FIRST ] FROM ] cursor_name INTO
    [ variable_name | parameter_name ] [ ,...n ]
;
```

Copy code

```
 OPEN cursor_name
    [ USING [ SQL_identifier | SQL_paramenter ] [ ,...n ] ]
;
```

Copy code

```
 CLOSE cursor_name ;
```

### Sample Source Patterns

#### Setup Data

The following code is necessary to execute the sample patterns present in this section.

##### Teradata

Copy code

```
 CREATE TABLE vEmployee(
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255)
);

CREATE TABLE ResTable(
    Column1 VARCHAR(255)
);

INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (1, 'Smith', 'Christian');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (2, 'Johnson', 'Jhon');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (3, 'Brown', 'William');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (4, 'Williams', 'Gracey');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (5, 'Garcia', 'Julia');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (6, 'Miller', 'Peter');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (7, 'Davis', 'Jannys');

CREATE TABLE TEST_TABLE (
    ColumnA NUMBER,
    ColumnB VARCHAR(8),
    ColumnC VARCHAR(8));

SELECT * FROM TEST_TABLE;
INSERT INTO TEST_TABLE VALUES (1, '1', '1');
INSERT INTO TEST_TABLE VALUES (2, '2', '2');
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE vEmployee (
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE TABLE ResTable (
    Column1 VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (1, 'Smith', 'Christian');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (2, 'Johnson', 'Jhon');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (3, 'Brown', 'William');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (4, 'Williams', 'Gracey');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (5, 'Garcia', 'Julia');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (6, 'Miller', 'Peter');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (7, 'Davis', 'Jannys');

CREATE OR REPLACE TABLE TEST_TABLE (
    ColumnA NUMBER(38, 18),
    ColumnB VARCHAR(8),
    ColumnC VARCHAR(8))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT
    * FROM
    TEST_TABLE;

    INSERT INTO TEST_TABLE
    VALUES (1, '1', '1');

    INSERT INTO TEST_TABLE
    VALUES (2, '2', '2');
```

#### Basic Cursor

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE CursorsTest()
BEGIN
    DECLARE val1 VARCHAR(255);
    DECLARE empcursor CURSOR FOR
        SELECT LastName
        FROM vEmployee
        ORDER BY PersonID;

    OPEN empcursor;
    FETCH NEXT FROM empcursor INTO val1;
    FETCH NEXT FROM empcursor INTO val1;
    INSERT INTO ResTable(Column1) VALUES (val1);
    CLOSE empcursor;
END;

CALL CursorsTest();
SELECT * FROM ResTable;
```

##### Result

Copy code

```
Johnson
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 CREATE OR REPLACE PROCEDURE CursorsTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        val1 VARCHAR(255);
    BEGIN

        LET empcursor CURSOR
        FOR
            SELECT
                LastName
                   FROM
                vEmployee
                   ORDER BY PersonID;
        OPEN empcursor;
        FETCH NEXT FROM empcursor INTO val1;
            FETCH NEXT FROM empcursor INTO val1;
        INSERT INTO ResTable (Column1)
        VALUES (:val1);
            CLOSE empcursor;
    END;
$$;

CALL CursorsTest();

SELECT
    * FROM
    ResTable;
```

##### Result

Copy code

```
Johnson
```

#### Single Returnable Cursor

The following procedure is intended to return one result set since it has the `DYNAMIC RESULT SETS 1` property in the header, the cursor has the `WITH RETURN` property and is being opened in the body.

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE spSimple ()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE result_set CURSOR WITH RETURN ONLY FOR
    SELECT *
    FROM vEmployee;

    OPEN result_set;
END;

CALL spSimple();
```

##### Result

Copy code

```
PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 CREATE OR REPLACE PROCEDURE spSimple ()
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET result_set CURSOR FOR
            SELECT * FROM vEmployee;
        OPEN result_set;
        RETURN TABLE(resultset_from_cursor(result_set));
    END;
$$;

CALL spSimple();
```

##### Result

Copy code

```
PERSONID|LASTNAME|FIRSTNAME|
--------+--------+---------+
       1|Smith   |Christian|
       2|Johnson |Jhon     |
       3|Brown   |William  |
       4|Williams|Gracey   |
       5|Garcia  |Julia    |
       6|Miller  |Peter    |
       7|Davis   |Jannys   |
```

#### Multiple Returnable Cursors

The following procedure is intended to return multiple results when `DYNAMIC RESULT SETS` property in the header is greater than 1, the procedure has multiple cursors with the `WITH RETURN` property and these same cursors are being opened in the body.

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE spTwoOrMore()
DYNAMIC RESULT SETS 2
BEGIN
    DECLARE result_set CURSOR WITH RETURN ONLY FOR
        SELECT * FROM SampleTable2;

    DECLARE result_set2 CURSOR WITH RETURN ONLY FOR
	SELECT Column11 FROM SampleTable1;
    OPEN result_set2;
    OPEN result_set;
END;

CALL spTwoOrMore();
```

##### Result

Copy code

```
ColumnA|ColumnB|ColumnC|
-------+-------+-------+
      2|2      |2      |
      1|1      |1      |

PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "SampleTable2", "SampleTable1" **
CREATE OR REPLACE PROCEDURE spTwoOrMore ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		tbl_result_set VARCHAR;
		tbl_result_set2 VARCHAR;
		return_arr ARRAY := array_construct();
	BEGIN
		tbl_result_set := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set) AS
			SELECT
				* FROM
				SampleTable2;
		LET result_set CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
		tbl_result_set2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set2) AS
			SELECT
				Column11 FROM
				SampleTable1;
		LET result_set2 CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
		OPEN result_set2 USING (tbl_result_set2);
		return_arr := array_append(return_arr, :tbl_result_set2);
		OPEN result_set USING (tbl_result_set);
		return_arr := array_append(return_arr, :tbl_result_set);
		--** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
		RETURN return_arr;
	END;
$$;

CALL spTwoOrMore();
```

##### Results

Copy code

```
[
  "RESULTSET_B5B0005D_1602_48B7_9EE4_62E1A28B000C",
  "RESULTSET_1371794D_7B77_4DA9_B42E_7981F35CEA9C"
]

ColumnA|ColumnB|ColumnC|
-------+-------+-------+
      2|2      |2      |
      1|1      |1      |

PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

#### Cursors With Binding Variables

The following cursor uses binding variables as the were condition to perform the query.

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE TestProcedure (IN param1 NUMBER, param2 VARCHAR(8), param3 VARCHAR(8))
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE cursorExample CURSOR WITH RETURN ONLY FOR
        SELECT * FROM  TEST_TABLE
   	WHERE ColumnA = param1 AND ColumnB LIKE param2 and ColumnC LIKE param3;

    OPEN cursorExample;
END;
```

##### Result

Copy code

```
|ColumnA|ColumnB|ColumnC|
+-------+-------+-------+
|      2|2      |2      |
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TEST_TABLE" **
CREATE OR REPLACE PROCEDURE TestProcedure (PARAM1 NUMBER(38, 18), PARAM2 VARCHAR(8), PARAM3 VARCHAR(8))
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      LET cursorExample CURSOR
      FOR
         SELECT
            * FROM
            TEST_TABLE
           	WHERE ColumnA = ?
            AND ColumnB ILIKE ?
            and ColumnC ILIKE ?;
      OPEN cursorExample USING (param1, param2, param3);
      RETURN TABLE(resultset_from_cursor(cursorExample));
   END;
$$;
```

##### Result

Copy code

```
|ColumnA|ColumnB|ColumnC|
+-------+-------+-------+
|      2|2      |2      |
```

#### Cursor For Loop

It is a type of loop that uses a cursor to fetch rows from a SELECT statement and then performs some processing on each row.

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE TestProcedure ()
DYNAMIC RESULT SETS 1
BEGIN
    FOR fUsgClass AS cUsgClass CURSOR FOR
        SELECT columnA FROM  TEST_TABLE
    DO
        INSERT INTO ResTable(Column1) VALUES (fUsgClass.columnA);
    END FOR;
END;

CALL TestProcedure();
SELECT * FROM ResTable;
```

##### Result

Copy code

```
|Column1|
+-------+
|      1|
|      2|
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "TEST_TABLE", "ResTable" **
CREATE OR REPLACE PROCEDURE TestProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0110 - TRANSFORMATION NOT PERFORMED DUE TO MISSING DEPENDENCIES ***/!!!
        temp_fUsgClass_columnA;
    BEGIN
        LET cUsgClass CURSOR
        FOR
            SELECT
                columnA FROM
                TEST_TABLE;
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR fUsgClass IN cUsgClass DO
            temp_fUsgClass_columnA := fUsgClass.columnA;
            INSERT INTO ResTable (Column1)
            VALUES (:temp_fUsgClass_columnA);
        END FOR;
    END;
$$;

CALL TestProcedure();

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "ResTable" **
SELECT
    * FROM
    ResTable;
```

##### Result

Copy code

```
|Column1|
+-------+
|      1|
|      2|
```

#### Cursor Fetch inside a Loop

It allows one to retrieve rows from a result set one at a time and perform some processing on each row.

##### Teradata

##### Cursor Code

Copy code

```
 REPLACE PROCEDURE teradata_fetch_inside_loop()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE col_name VARCHAR(255);
    DECLARE col_int INTEGER DEFAULT 1;
    DECLARE cursor_var CURSOR FOR SELECT columnA FROM TEST_TABLE;
    WHILE (col_int <> 0) DO
        FETCH cursor_var INTO col_name;
        INSERT INTO ResTable(Column1) VALUES (cursor_var.columnA);
        SET col_int = 0;
    END WHILE;
END;

CALL teradata_fetch_inside_loop();
SELECT * FROM ResTable;
```

##### Result

Copy code

```
|Column1|
+-------+
|      2|
```

##### Snowflake Scripting

##### Cursor Code

Copy code

```
 CREATE OR REPLACE PROCEDURE teradata_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        col_name VARCHAR(255);
        col_int INTEGER DEFAULT 1;
    BEGIN

        LET cursor_var CURSOR
        FOR
            SELECT
                columnA FROM
                TEST_TABLE;
                WHILE (:col_int <> 0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH cursor_var INTO col_name;
            INSERT INTO ResTable (Column1)
            VALUES (cursor_var.columnA);
            col_int := 0;
                END LOOP;
    END;
$$;

CALL teradata_fetch_inside_loop();

SELECT
    * FROM
    ResTable;
```

##### Result

Copy code

```
|Column1|
+-------+
|      2|
```

### Known Issues

The following parameters are not applicable in Snowflake Scripting.

#### 1. Declare

[ SCROLL/NO SCROLL ] Snowflake Scripting only supports FETCH NEXT.

[ READ-ONLY ] This is the default in Snowflake Scripting.

[ UPDATE ].

##### 2. Fetch

[ NEXT ] This is the default behavior in Snowflake Scripting.

[ FIRST ].

### Related EWIs

1. [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables.
2. [SSC-PRF-0003](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003): Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.
3. [SSC-PRF-0004](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0004): This statement has usages of cursor for loop.

## DECLARE CONTINUE HANDLER

Translation reference to convert Teradata DECLARE CONTINUE handler to Snowflake Scripting

### Description

> Handle completion conditions and exception conditions not severe enough to affect the flow of control.

For more information, see the [Teradata DECLARE CONTINUE handler documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/Condition-Handling/DECLARE-HANDLER-CONTINUE-Type).

Copy code

```
 DECLARE CONTINUE HANDLER FOR
  {
    { sqlstate_state_spec | condition_name } [,...] |

    { SQLEXCEPTION | SQLWARNING | NOT FOUND } [,...]

  } handler_action_statement ;
```

### Sample Source Patterns

#### DECLARE CONTINUE HANDLER

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE PURGING_ADD_TABLE
(
 IN inDatabaseName     	VARCHAR(30),
 IN inTableName    		VARCHAR(30)
)
BEGIN
 DECLARE vCHAR_SQLSTATE CHAR(5);
 DECLARE vSUCCESS       CHAR(5);

  DECLARE CONTINUE HANDLER FOR SQLSTATE 'T5628'
  BEGIN
     SET vCHAR_SQLSTATE = SQLCODE;
     SET vSUCCESS    = SQLCODE;
  END;

  SELECT 1;

END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE PURGING_ADD_TABLE
(INDATABASENAME VARCHAR(30), INTABLENAME VARCHAR(30)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  vCHAR_SQLSTATE CHAR(5);
  vSUCCESS       CHAR(5);
 BEGIN

  BEGIN
   SELECT
    1;
  EXCEPTION
   WHEN statement_error THEN
    LET errcode := :sqlcode
    LET sqlerrmsg := :sqlerrm
    IF (errcode = '904'
    AND contains(sqlerrmsg, 'invalid value')) THEN
     BEGIN
      vCHAR_SQLSTATE := SQLCODE;
      vSUCCESS := SQLCODE;
     END;
    ELSE
     RAISE
    END IF
  END
 END;
$$;
```

### Known Issues

#### DECLARE CONTINUE HANDLER FOR SQLSTATE

The support of declaring continue handlers for some SQLSTATE values is not currently supported by Snowflake Scripting.

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE declareConditionExample2 ( )
BEGIN
   DECLARE CONTINUE HANDLER FOR SQLSTATE 'UNSUPPORTED'
     BEGIN
       SET vCHAR_SQLSTATE = SQLCODE;
       SET vSUCCESS    = SQLCODE;
    END;
END;
```

##### Snowflake Scripting

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE declareConditionExample2 ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      !!!RESOLVE EWI!!! /*** SSC-EWI-TD0004 - NOT SUPPORTED SQL EXCEPTION ON CONTINUE HANDLER ***/!!!
      DECLARE CONTINUE HANDLER FOR SQLSTATE 'UNSUPPORTED'
      BEGIN
         vCHAR_SQLSTATE := SQLCODE;
         vSUCCESS := SQLCODE;
      END;
   END;
$$;
```

### Related EWIs

1. [SSC-EWI-TD0004](../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0004): Not supported SQL Exception on continue handler.

## DECLARE CONDITION HANDLER

Translation reference to convert Teradata DECLARE CONDITION handler to Snowflake Scripting

### Description

> Assign a name to an SQLSTATE code, or declare a user-defined condition.

For more information, see the [Teradata DECLARE CONDITION handler documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Condition-Handling/DECLARE-CONDITION).

Copy code

```
 DECLARE condition_name CONDITION
    [ FOR SQLSTATE [ VALUE ] sqlstate_code ] ;
```

### Sample Source Patterns

#### DECLARE CONDITION

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE declareConditionExample ( )
BEGIN
    DECLARE DB_ERROR CONDITION;
    ...
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE declareConditionExample ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        DB_ERROR EXCEPTION;
    BEGIN
    END;
$$;
```

### Known Issues

#### DECLARE CONDITION FOR SQLSTATE

The support of declaring conditions for SQLSTATE values is not currently supported by Snowflake Scripting.

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE declareConditionExample2 ( )
BEGIN
    DECLARE ERROR_EXISTS CONDITION FOR SQLSTATE VALUE '42000';
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE declareConditionExample2 ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ERROR_EXISTS EXCEPTION;
    BEGIN
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'SET EXCEPTION DETAILS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
-- ERROR_EXISTS CONDITION FOR SQLSTATE VALUE '42000';
    END;
$$;
```

### Related EWIs

1. [SSC-EWI-0058:](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058) Functionality is not currently supported by Snowflake Scripting.

## DECLARE

Translation reference to convert Teradata DECLARE statement to Snowflake Scripting

### Description

> Declares one or more local variables.

For more information, see the [Teradata DECLARE documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Control-Statements/DECLARE).

Copy code

```
 DECLARE variable_name [, variable_name ]... DATA_TYPE [ DEFAULT default_value]
```

### Sample Source Patterns

#### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE declareExample ( )
BEGIN
    DECLARE COL_NAME, COL_TYPE VARCHAR(200) DEFAULT '' ;
    DECLARE COL_COUNT, COL_LEN INTEGER;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE declareExample ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        COL_NAME VARCHAR(200) DEFAULT '';
        COL_TYPE VARCHAR(200) DEFAULT '';
        COL_COUNT INTEGER;
        COL_LEN INTEGER;
    BEGIN

        RETURN 1;
    END;
$$;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## DML and DDL Objects

### Description

DML and DDL objects are translated in the same way regardless of whether they are inside stored procedures or not. For further information check the following links.

### Translation References

- [data-types.md](sql-translation-reference/data-types "mention"): Compare Teradata data types and their equivalents in Snowflake.
- [ddl](sql-translation-reference/ddl-teradata "mention"): Explore the translation of the Data Definition Language.
- [dml](sql-translation-reference/dml-teradata "mention"): Explore the translation of the Data Manipulation Language.
- [built-in-functions](sql-translation-reference/teradata-built-in-functions "mention"): Compare functions included in the runtime of both languages.

## EXCEPTION HANDLERS

Translation reference to convert Teradata EXCEPTION HANDLERS clause to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Teradata’s single and multiple Exception Handlers are replaced by its equivalent handlers in Snowflake Scripting.

For more information, see the [Teradata EXCEPTION HANDLERS documentation](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/gH3xxgeVDpIqVBjEQfppyQ).

Copy code

```
 DECLARE < handler_type > HANDLER
  FOR  < condition_value_list > < handler_action > ;
```

### Sample Source Patterns

#### SQLEXCEPTION HANDLER

##### Teradata

##### Single handler

Copy code

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlException');
    SELECT * FROM Proc_Error_Table;
END;
```

##### Multiple handlers

Copy code

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE ConditionByUser1 CONDITION;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlException');
    DECLARE EXIT HANDLER FOR ConditionByUser1
        INSERT INTO Proc_Error_Table ('procSample', 'Failed ConditionByUser1');
    SELECT * FROM Proc_Error_Table;
END;
```

##### Snowflake Scripting

##### Single handler

Copy code

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN

        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN other THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed SqlException');
    END;
$$;
```

##### Multiple handlers

Copy code

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ConditionByUser1 EXCEPTION;
    BEGIN

        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN ConditionByUser1 THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed ConditionByUser1');
            WHEN other THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed SqlException');
    END;
$$;
```

#### User-Defined Handlers

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR Custom1, Custom2, Custom3
      BEGIN
        SET Message1 = 'custom1 and custom2 and custom3';
      END;
    SELECT * FROM Proc_Error_Table;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN

        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN Custom1 OR Custom2 OR Custom3 THEN
            BEGIN
                    Message1 := 'custom1 and custom2 and custom3';
            END;
    END;
$$;
```

### Known Issues

#### CONTINUE Handler

Danger

A ‘CONTINUE’ handler in Teradata allows the execution to be resumed after executing a statement with errors. This is not supported by the exception blocks in Snowflake Scripting. [Condition Handler Teradata reference documentation.](https://docs.teradata.com/r/CeAGk~BNtx~axcR0ed~5kw/EN6T2zEDlgBRvSKjw7shUg)

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('spSample4', 'Failed SqlException');
    SELECT * FROM Proc_Error_Table;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-TD0004 - NOT SUPPORTED SQL EXCEPTION ON CONTINUE HANDLER ***/!!!
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table
        VALUES ('spSample4', 'Failed SqlException');
        SELECT
            * FROM
            Proc_Error_Table;
    END;
$$;
```

#### Other not supported handlers

Danger

Handlers for SQLSTATE, SQLWARNING, and NOT FOUND are not supported

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '42002', SQLWARNING, NOT FOUND
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlState or SqlWarning or Not Found');
    SELECT * FROM Proc_Error_Table;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/04/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'SQLSTATE, SQLWARNING, NOT-FOUND TYPES HANDLER' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        DECLARE EXIT HANDLER FOR SQLSTATE '42002', SQLWARNING, NOT FOUND
--            INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlState or SqlWarning or Not Found');
        SELECT
            * FROM
            Proc_Error_Table;
    END;
$$;
```

### Related EWIs

1. [SSC-EWI-0058](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-TD0004](../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0004): Not supported SQL Exception on continue handler.

## EXECUTE/EXEC

Translation reference to convert Teradata EXECUTE or EXEC statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

The Teradata `EXECUTE`statement allows the execution prepared dynamic SQL or macros, on the other hand exec only allows macros.

For more information regarding Teradata EXECUTE/EXEC, check [Macro Form](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Manipulation-Language/June-2017/Statement-Syntax/EXECUTE-Macro-Form) and [Dynamic SQL Form](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/Dynamic-Embedded-SQL-Statements/Dynamic-SQL-Statement-Syntax/EXECUTE-Dynamic-SQL-Form)

Copy code

```
 -- EXECUTE macro syntax
{EXECUTE | EXEC } macro_identifier [ (<parameter_definition>[, ...n] ) ] [;]

<parameter_definition>:= {parameter_name = constant_expression | constant_expresion}

-- EXECUTE prepared dynamic SQL syntax
EXECUTE prepare_indentifier [<using>|<usingDescriptor>]

<using>:= USING < host_variable >[, ...n]
<host_variable>:= [:] host_variable_name [[INDICATOR] :host_indicator_name]
<usingDescriptor>:= USING DESCRIPTOR [:] descript_area
```

### Sample Source Patterns

#### Setup data

The following code is necessary to execute the sample patterns present in this section.

##### Teradata

Copy code

```
 -- Additional Params: -t JavaScript
CREATE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
);

CREATE MACRO dummyMacro AS(
  SELECT * FROM INVENTORY;
);
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE inventory (
  product_name VARCHAR(50),
  price INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE dummyMacro ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  INSERT_TEMP(`SELECT
   *
  FROM
   INVENTORY`,[]);
  return tablelist;
$$;
```

#### Execute prepared statement

##### Teradata

##### Execute

Copy code

```
 CREATE PROCEDURE InsertProductInInventory(IN productName VARCHAR(50), IN price INTEGER)
BEGIN
    DECLARE dynamicSql CHAR(200);
    SET dynamicSql = 'INSERT INTO INVENTORY VALUES( ?, ?)';
    PREPARE preparedSql FROM dynamicSql;
    EXECUTE preparedSql USING productName, price;

END;

CALL InsertProductInInventory('''Chocolate''', 75);
CALL InsertProductInInventory('''Sugar''', 65);
CALL InsertProductInInventory('''Rice''', 100);
```

##### Snowflake Scripting

##### Execute

Copy code

```
 CREATE OR REPLACE PROCEDURE InsertProductInInventory (PRODUCTNAME VARCHAR(50), PRICE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        dynamicSql CHAR(200);
    BEGIN

        dynamicSql := 'INSERT INTO INVENTORY
VALUES (?, ?)';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PREPARE STATEMENT' NODE ***/!!!
            PREPARE preparedSql FROM dynamicSql;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE dynamicSql;
    END;
$$;

CALL InsertProductInInventory('''Chocolate''', 75);

CALL InsertProductInInventory('''Sugar''', 65);

CALL InsertProductInInventory('''Rice''', 100);
```

#### Execute macro statement

##### Teradata

##### Execute

Copy code

```
 EXECUTE dummyMacro;
```

##### Result

Copy code

```
+---------------+-------+
| product_name  | price |
+---------------+-------+
| 'Chocolate'   | 75    |
+---------------+-------+
| 'Sugar'       | 65    |
+---------------+-------+
| 'Rice'        | 100   |
+---------------+-------+
```

##### Snowflake Scripting

##### Execute

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
EXECUTE IMMEDIATE dummyMacro;
```

#### PREPARE with cursor pattern and USING clause

When a `PREPARE` statement is used with a cursor that is opened with a `USING` clause, the pattern is transformed into `EXECUTE IMMEDIATE` with the USING clause bound at execution time.

##### Teradata

##### Query

Copy code

```
REPLACE PROCEDURE fetch_cursor_with_using(OUT result INTEGER)
BEGIN
    DECLARE SQL_string VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTable WHERE col1 = ?';
    DECLARE filter_value INTEGER DEFAULT 5;

    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string;
    OPEN C1 USING filter_value;
    FETCH C1 INTO result;
    CLOSE C1;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
CREATE OR REPLACE PROCEDURE fetch_cursor_with_using (RESULT OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQL_string VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTable
WHERE col1 = ?';
    filter_value INTEGER DEFAULT 5;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
    prepareQuery_aux_sql := SQL_string;
    --** SSC-FDM-TD0044 - USING VARIABLES BOUND AT EXECUTE IMMEDIATE TIME INSTEAD OF OPEN CURSOR TIME. CURSOR IS FIXED AT LET CURSOR FOR RESULTSET DECLARATION; REASSIGNING THE RESULTSET VARIABLE OR RE-EXECUTING PREPARE IN A LOOP WILL NOT UPDATE THE CURSOR. **
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql USING (filter_value)
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      result;
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;
```

**Transformation details:**

1. **PREPARE statement** is converted to `EXECUTE IMMEDIATE` with the USING clause
2. **Cursor declaration** is transformed to `LET CURSOR ... FOR resultset`
3. **OPEN USING** clause is moved to the EXECUTE IMMEDIATE statement
4. **Cursor instances** receive unique names (e.g., `CURSOR_S1_INSTANCE_V0`) when reused in loops

**Behavioral note:** In Teradata, the USING variables are bound when `OPEN` is called. In Snowflake, they are bound when `EXECUTE IMMEDIATE` runs (at PREPARE time). See [SSC-FDM-TD0044](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0044) for implications.

### Related EWIs

1. [SSC-EWI-0030:](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030) The statement below has usages of dynamic SQL.
2. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
3. [SSC-FDM-TD0044](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0044): PREPARE with USING variables bound at EXECUTE IMMEDIATE time instead of OPEN CURSOR time.
4. [SSC-EWI-TD0098](../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0098): PREPARE with USING clause containing non-variable expressions cannot be automatically migrated.

## EXECUTE IMMEDIATE

Translation reference to convert Teradata EXECUTE IMMEDIATE statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

The Teradata `EXECUTE IMMEDIATE` statement allows the execution of dynamic SQL contained on variables or string literals.

For more information, see the [Teradata EXECUTE IMMEDIATE documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Dynamic-Embedded-SQL-Statements/Dynamic-SQL-Statement-Syntax/EXECUTE-IMMEDIATE).

Copy code

```
 -- EXECUTE IMMEDIATE syntax
EXECUTE IMMEDIATE <dynamic_statement>

<dynamic_statement> := {string_literal | string_variable}
```

### Sample Source Patterns

#### Setup data

The following code is necessary to execute the sample patterns present in this section.

##### Teradata

Copy code

```
 CREATE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
);
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Execute Example

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE InsertProductInInventory(IN productName VARCHAR(50), IN price INTEGER)
BEGIN
	DECLARE insertStatement VARCHAR(100);
	SET insertStatement = 'INSERT INTO INVENTORY VALUES(' || productName || ', ' || price || ')';
    EXECUTE IMMEDIATE insertStatement;
END;

CALL InsertProductInInventory('''Chocolate''', 75);
CALL InsertProductInInventory('''Sugar''', 65);
CALL InsertProductInInventory('''Rice''', 100);

SELECT product_name, price FROM inventory;
```

##### Result

Copy code

```
+--------------+-------+
| product_name | price |
+--------------+-------+
| Chocolate    | 75    |
+--------------+-------+
| Sugar        | 65    |
+--------------+-------+
| Rice         | 100   |
+--------------+-------+
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE InsertProductInInventory (PRODUCTNAME VARCHAR(50), PRICE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		insertStatement VARCHAR(100);
	BEGIN

		insertStatement := 'INSERT INTO INVENTORY
VALUES (' || productName || ', ' || price || ')';
		!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
		EXECUTE IMMEDIATE insertStatement;
	END;
$$;

CALL InsertProductInInventory('''Chocolate''', 75);

CALL InsertProductInInventory('''Sugar''', 65);

CALL InsertProductInInventory('''Rice''', 100);

SELECT
	product_name,
	price FROM
	inventory;
```

##### Result

Copy code

```
+--------------+-------+
| PRODUCT_NAME | PRICE |
+--------------+-------+
| Chocolate    | 75    |
+--------------+-------+
| Sugar        | 65    |
+--------------+-------+
| Rice         | 100   |
+--------------+-------+
```

##### Result

Copy code

```
column1|column2                  |column3|
-------+-------------------------+-------+
      3|Mundo3                   |    3.3|
```

### Related EWIs

1. [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030): The statement below has usages of dynamic SQL.

## FUNCTION OPTIONS OR DATA ACCESS

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is**<mark style=”background-color:red;”>**removed from the migration**</mark>**because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description

Functions options or data access options are statements used in functions on the declaration part to specify certain characteristics. These can be:

- `CONTAINS SQL`
- `SQL SECURITY DEFINER`
- `COLLATION INVOKER`
- `SPECIFIC FUNCTION_NAME`

### Sample Source Patterns

#### Function Options

Notice that in this example the function options have been removed because they are not required in Snowflake.

##### Teradata

Copy code

```
 CREATE FUNCTION sumValues(A INTEGER, B INTEGER)
   RETURNS INTEGER
   LANGUAGE SQL
   CONTAINS SQL
   SQL SECURITY DEFINER
   SPECIFIC sumTwoValues
   COLLATION INVOKER
   INLINE TYPE 1
   RETURN A + B;
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE FUNCTION sumValues (A INTEGER, B INTEGER)
   RETURNS INTEGER
   LANGUAGE SQL
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
   AS
   $$
      A + B
   $$;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## GET DIAGNOSTICS EXCEPTION

Translation reference to convert Teradata GET DIAGNOSTICS EXCEPTION statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> GET DIAGNOSTICS retrieves information about successful, exception, or completion conditions from the Diagnostics Area.

For more information, see the [Teradata GET DIAGNOSTICS documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Condition-Handling/GET-DIAGNOSTICS).

Copy code

```
 GET DIAGNOSTICS
{
  [ EXCEPTION < condition_number >
    [ < parameter_name | variable_name > = < information_item > ]...
  ]
  |
  [ < parameter_name | variable_name > = < information_item > ]...
}
```

### Sample Source Patterns

#### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE getDiagnosticsSample ()
BEGIN
    DECLARE V_MESSAGE, V_CODE VARCHAR(200);
    DECLARE V_Result INTEGER;

    SELECT c1 INTO V_Result FROM tab1;
    GET DIAGNOSTICS EXCEPTION 1
        V_MESSAGE = Message_Text,
        V_CODE = RETURNED_SQLSTATE;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE getDiagnosticsSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        V_MESSAGE VARCHAR(200);
        V_CODE VARCHAR(200);
        V_Result INTEGER;
    BEGIN

        SELECT
            c1 INTO
            :V_Result
        FROM
            tab1;
            V_MESSAGE := SQLERRM;
            V_CODE := SQLSTATE;
    END;
$$;
```

### Known Issues

#### CLASS\_ORIGIN, CONDITION\_NUMBER

Danger

The use of GET DIAGNOSTICS for CLASS\_ORIGIN, CONDITION\_NUMBER is not supported

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE getDiagnosticsSample ()
BEGIN
    DECLARE V_MESSAGE, V_CODE VARCHAR(200);
    DECLARE V_Result INTEGER;

    SELECT c1 INTO V_Result FROM tab1;
    GET DIAGNOSTICS EXCEPTION 5
        V_CLASS = CLASS_ORIGIN,
        V_COND = CONDITION_NUMBER;
END;
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE getDiagnosticsSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        V_MESSAGE VARCHAR(200);
        V_CODE VARCHAR(200);
        V_Result INTEGER;
    BEGIN

        SELECT
            c1 INTO
            :V_Result
        FROM
            tab1;
--            V_CLASS = CLASS_ORIGIN
                                  !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'GET DIAGNOSTICS DETAIL FOR CLASS_ORIGIN' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

--            V_COND = CONDITION_NUMBER
                                     !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'GET DIAGNOSTICS DETAIL FOR CONDITION_NUMBER' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

    END;
$$;
```

### Related EWIs

1. [SSC-EWI-0058](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.

## IF

Translation reference to convert Teradata IF statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> Provides conditional execution based on the truth value of a condition.

For more information, see the [Teradata IF documentation](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/BER5lYjGTnRKex5a8eznnA).

Copy code

```
 IF conditional_expression THEN
     statement
     [ statement ]...
[ ELSEIF conditional_expression THEN
     statement
     [ statement ]... ]...
[ ELSE
     statement
     [ statement ]... ]
END IF;
```

### Sample Source Patterns

#### Sample auxiliary table

##### Teradata

Copy code

```
 CREATE TABLE if_table(col1 varchar(30));
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE if_table (
col1 varchar(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Possible IF variations

##### Teradata

##### Code 1

Copy code

```
 CREATE PROCEDURE ifExample1 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   END IF;
END;

CALL ifExample1(1);
SELECT * FROM if_table;
```

##### Code 2

Copy code

```
 CREATE PROCEDURE ifExample2 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSE
      INSERT INTO if_table(col1) VALUES ('Unexpected input.');
   END IF;
END;

CALL ifExample2(2);
SELECT * FROM if_table;
```

##### Code 3

Copy code

```
 CREATE PROCEDURE ifExample3 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSEIF flag = 2 THEN
      INSERT INTO if_table(col1) VALUES ('two');
   ELSEIF flag = 3 THEN
      INSERT INTO if_table(col1) VALUES ('three');
   END IF;
END;

CALL ifExample3(3);
SELECT * FROM if_table;
```

##### Code 4

Copy code

```
 CREATE PROCEDURE ifExample4 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSEIF flag = 2 THEN
      INSERT INTO if_table(col1) VALUES ('two');
   ELSEIF flag = 3 THEN
      INSERT INTO if_table(col1) VALUES ('three');
   ELSE
      INSERT INTO if_table(col1) VALUES ('Unexpected input.');
   END IF;
END;

CALL ifExample4(4);
SELECT * FROM if_table;
```

##### Result 1

Copy code

```
|COL1|
|----|
|one |
```

##### Result 2

Copy code

```
|COL1             |
|-----------------|
|Unexpected input.|
```

##### Result 3

Copy code

```
|COL1 |
|-----|
|three|
```

##### Result 4

Copy code

```
|COL1             |
|-----------------|
|Unexpected input.|
```

##### Snowflake Scripting

##### Query 1

Copy code

```
 CREATE OR REPLACE PROCEDURE ifExample1 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      END IF;
   END;
$$;

CALL ifExample1(1);

SELECT
   * FROM
   if_table;
```

##### Query 2

Copy code

```
 CREATE OR REPLACE PROCEDURE ifExample2 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSE
         INSERT INTO if_table (col1)
         VALUES ('Unexpected input.');
      END IF;
   END;
$$;

CALL ifExample2(2);

SELECT
   * FROM
   if_table;
```

##### Query 3

Copy code

```
 CREATE OR REPLACE PROCEDURE ifExample3 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSEIF (:flag = 2) THEN
         INSERT INTO if_table (col1)
         VALUES ('two');
      ELSEIF (:flag = 3) THEN
         INSERT INTO if_table (col1)
         VALUES ('three');
      END IF;
   END;
$$;

CALL ifExample3(3);

SELECT
   * FROM
   if_table;
```

##### Query 4

Copy code

```
 CREATE OR REPLACE PROCEDURE ifExample4 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSEIF (:flag = 2) THEN
         INSERT INTO if_table (col1)
         VALUES ('two');
      ELSEIF (:flag = 3) THEN
         INSERT INTO if_table (col1)
         VALUES ('three');
      ELSE
         INSERT INTO if_table (col1)
         VALUES ('Unexpected input.');
      END IF;
   END;
$$;

CALL ifExample4(4);

SELECT
   * FROM
   if_table;
```

##### Result 1

Copy code

```
|COL1|
|----|
|one |
```

##### Result 2

Copy code

```
|COL1             |
|-----------------|
|Unexpected input.|
```

##### Result 3

Copy code

```
|COL1 |
|-----|
|three|
```

##### Result 4

Copy code

```
|COL1             |
|-----------------|
|Unexpected input.|
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## LOCKING FOR ACCESS

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is**<mark style=”background-color:red;”>**removed from the migration**</mark>**because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description

The functionality of locking a row in Teradata is related to the access and the privileges. Review the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Statement-Syntax/LOCKING-Request-Modifier/Usage-Notes/Using-LOCKING-ROW) to know more.

### Sample Source Patterns

#### Locking row

Notice that in this example the `LOCKING ROW FOR ACCESS` has been deleted. This is because Snowflake handles accesses with roles and privileges. The statement is not required.

##### Teradata

Copy code

```
 REPLACE VIEW SCHEMA2.VIEW1
AS
LOCKING ROW FOR ACCESS
SELECT * FROM SCHEMA1.TABLE1;
```

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "SCHEMA1.TABLE1" **
CREATE OR REPLACE VIEW SCHEMA2.VIEW1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
SCHEMA1.TABLE1;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-0001](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0001): Views selecting all columns from a single table are not required in Snowflake.
2. [SSC-FDM-0007](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007): Element with missing dependencies.

## LOOP

Translation reference to convert Teradata LOOP statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Teradata’s `LOOP` statement is translated to Snowflake Scripting `LOOP` syntax.

For more information, see the [Teradata LOOP documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Control-Statements/LOOP).

Copy code

```
 [label_name:] LOOP
    { sql_statement }
END LOOP [label_name];
```

### Sample Source Patterns

#### Teradata

##### Loop

Copy code

```
 CREATE PROCEDURE loopProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;

    customeLabel: LOOP
    	SET counter = counter + 1;
	IF counter = 10 THEN
	    LEAVE customeLabel;
	END IF;
    END LOOP customeLabel;

    SET resultCounter = counter;
END;

CALL loopProcedure(:?);
```

##### Result

Copy code

```
 |resultCounter|
|-------------|
|10           |
```

##### Snowflake Scripting

##### Loop

Copy code

```
 CREATE OR REPLACE PROCEDURE loopProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		counter INTEGER DEFAULT 0;
	BEGIN

		LOOP
			counter := counter + 1;
			IF (:counter = 10) THEN
				BREAK CUSTOMELABEL;
			END IF;
		END LOOP CUSTOMELABEL;
		resultCounter := counter;
	END;
$$;

CALL loopProcedure(:?);
```

##### Result

Copy code

```
 |LOOPPROCEDURE|
|-------------|
|10           |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## OUTPUT PARAMETERS

This article is about the current transformation of the output parameters and how their functionality is being emulated.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

An **output parameter** is a parameter whose value is passed out of the stored procedure, back to the calling statement. Snowflake has direct support for output parameters.

### Sample Source Patterns

#### Single out parameter

##### Teradata

Copy code

```
CREATE PROCEDURE demo.proc_with_single_output_parameters(OUT param1 NUMBER)
BEGIN
 SET param1 = 100;
END;

REPLACE PROCEDURE demo.proc_calling_proc_with_single_output_parameters ()
BEGIN
  DECLARE mytestvar NUMBER;
  CALL demo.proc_with_single_output_parameters(mytestvar);
  INSERT INTO demo.TABLE20 VALUES(mytestvar,432);
END;
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE demo.proc_with_single_output_parameters (PARAM1 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  param1 := 100;
 END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "demo.TABLE20" **
CREATE OR REPLACE PROCEDURE demo.proc_calling_proc_with_single_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  mytestvar NUMBER(38, 18);
 BEGIN

  CALL demo.proc_with_single_output_parameters(:mytestvar);
  INSERT INTO demo.TABLE20
  VALUES (:mytestvar,432);
 END;
$$;
```

#### Multiple out parameter

##### Teradata

Copy code

```
 CREATE PROCEDURE demo.proc_with_multiple_output_parameters(OUT param1 NUMBER, INOUT param2 NUMBER)
BEGIN
  SET param1 = param2;
  SET param2 = 32;
END;

CREATE PROCEDURE demo.proc_calling_proc_with_multiple_output_parameters ()
BEGIN
    DECLARE var1  NUMBER;
    DECLARE var2  NUMBER;
    SET var2 = 34;
    CALL demo.proc_with_multiple_output_parameters(var1, var2);
    INSERT INTO demo.TABLE20 VALUES(var1,var2);
END;
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE demo.proc_with_multiple_output_parameters (PARAM1 OUT NUMBER(38, 18), PARAM2 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    param1 := param2;
    param2 := 32;
  END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "demo.TABLE20" **
CREATE OR REPLACE PROCEDURE demo.proc_calling_proc_with_multiple_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1 NUMBER(38, 18);
    var2 NUMBER(38, 18);
  BEGIN

    var2 := 34;
    CALL demo.proc_with_multiple_output_parameters(:var1, :var2);
    INSERT INTO demo.TABLE20
    VALUES (:var1, :var2);
  END;
$$;
```

### Related EWIs

No related EWIs.

## PREPARE

Translation specification to convert Teradata PREPARE statement to Snowflake Scripting. This section review the PREPARE pattern related to a cursor logic.

### Description

> Prepares the dynamic DECLARE CURSOR statement to allow the creation of different result sets. Allows dynamic parameter markers.

For more information, please review the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/SQL-Cursor-Control-and-DML-Statements/PREPARE).

**Teradata syntax**:

Copy code

```
 PREPARE statement_name FROM { 'statement_string' | statement_string_variable } ;
```

Where:

- **statement\_name** is the same identifier as `statement_name` in a **DECLARE CURSOR** statement.
- **statement\_string** is the SQL text that is to be executed dynamically.
- **statement\_string\_variable** is the name of an SQL local variable, or an SQL parameter or string variable, that contains the SQL text string to be executed dynamically.

Note

<mark style=”color:blue;”>**Important information**</mark>

**For this transformation, the cursors are renamed since they cannot be dynamically updated.**

### Sample Source Patterns

#### Data setting for examples

For this example, please use the following complementary queries in the case that you want to run each case.

##### Teradata

Copy code

```
 CREATE TABLE MyTemporaryTable(
    Col1  INTEGER
);

INSERT INTO MyTemporaryTable(col1) VALUES (1);
SELECT * FROM databaseTest.MyTemporaryTable;

CREATE TABLE MyStatusTable (
    Col1  VARCHAR(2)
);
SELECT * FROM MyStatusTable;
```

##### Snowflake

Copy code

```
 CREATE TABLE MyTemporaryTable (
    Col1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

INSERT INTO MyTemporaryTable (col1) VALUES (1);

SELECT * FROM MyTemporaryTable;

    CREATE TABLE MyStatusTable (
    Col1 VARCHAR(2)
   )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT * FROM MyStatusTable;
```

#### Simple scenario

This example reviews the functionality for the cases where a single cursor is being used one single time.

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE simple_scenario()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable';
    DECLARE procedure_result INTEGER DEFAULT 0;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);
    CLOSE C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_scenario ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable';
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN

    -- Actual Cursor usage

    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

#### Simple scenario with RETURN ONLY

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE simple_scenario()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable';
    DECLARE procedure_result VARCHAR(100);
    DECLARE C1 CURSOR WITH RETURN ONLY FOR S1;

    SET procedure_result = '';
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_scenario ()
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable';
    procedure_result VARCHAR(100);
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN

    procedure_result := '';
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    RETURN TABLE(resultset_from_cursor(CURSOR_S1_INSTANCE_V0));
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

#### Reused cursor case

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE fetch_simple_reused_cursor(OUT procedure_result INTEGER)
BEGIN
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';

    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;

    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;
END;
```

##### Output

Copy code

```
No returning information.
```

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_simple_reused_cursor (
--                                                        OUT
                                                            PROCEDURE_RESULT INTEGER)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
        S1 RESULTSET;
        prepareQuery_aux_sql VARCHAR;
    BEGIN

        prepareQuery_aux_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE prepareQuery_aux_sql
        );
        LET CURSOR_S1_INSTANCE_V0 CURSOR
        FOR
            S1;
        OPEN CURSOR_S1_INSTANCE_V0;
            FETCH
            CURSOR_S1_INSTANCE_V0
        INTO procedure_result;
            CLOSE CURSOR_S1_INSTANCE_V0;
        prepareQuery_aux_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE prepareQuery_aux_sql
        );
        LET CURSOR_S1_INSTANCE_V1 CURSOR
        FOR
            S1;
        OPEN CURSOR_S1_INSTANCE_V1;
            FETCH
            CURSOR_S1_INSTANCE_V1
        INTO procedure_result;
            CLOSE CURSOR_S1_INSTANCE_V1;
        RETURN procedure_result;
    END;
$$;
```

##### Output

Copy code

```
No returning information.
```

#### Modified query before usage

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE fetch_modified_query_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE procedure_result INTEGER DEFAULT 0;
    -- Actual Cursor usages
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;

    -- This modification does not take effect since S1 is already staged for the Cursor
    SET SQL_string_sel = 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 0';
    OPEN C1;
    FETCH C1 INTO procedure_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);
    CLOSE C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_modified_query_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN

    -- Actual Cursor usages

    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    -- This modification does not take effect since S1 is already staged for the Cursor
    SQL_string_sel := 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 0';
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

#### Simple cursor combined with no PREPARE pattern

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE fetch_cursor_ignored_query_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE intermediate_result INTEGER;
    DECLARE procedure_result INTEGER DEFAULT 0;
    DECLARE C2 CURSOR FOR SELECT col1 FROM MyTemporaryTable WHERE col1 = 1;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO intermediate_result;
    CLOSE C1;
    SET procedure_result = intermediate_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);

    OPEN C2;
    FETCH C2 INTO intermediate_result;
    CLOSE C2;
    SET procedure_result = procedure_result + intermediate_result;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_cursor_ignored_query_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable
WHERE col1 = 1';
    intermediate_result INTEGER;
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN

    -- Actual Cursor usage
    LET C2 CURSOR
    FOR
      SELECT
        col1
      FROM
        MyTemporaryTable
      WHERE
        col1 = 1;
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      intermediate_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
    procedure_result := intermediate_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    OPEN C2;
    FETCH
      C2
    INTO
      intermediate_result;
    CLOSE C2;
    procedure_result := procedure_result + intermediate_result;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| 1 |

Expand

Show lessSee more

#### Prepare combined with nested cursors

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE fetch_nested_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE intermediate_result INTEGER;
    DECLARE C2 CURSOR FOR SELECT col1 FROM MyTemporaryTable WHERE col1 = 1;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    OPEN C2;
    FETCH C2 INTO intermediate_result;

    CLOSE C2;
    FETCH C1 INTO intermediate_result;
    CLOSE C1;
END;
```

##### Output

Copy code

```
No returning information.
```

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_nested_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    intermediate_result INTEGER;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN

    -- Actual Cursor usage
    LET C2 CURSOR
    FOR
      SELECT
        col1
      FROM
        MyTemporaryTable
      WHERE
        col1 = 1;
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    OPEN C2;
    FETCH
      C2
    INTO
      intermediate_result;
    CLOSE C2;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      intermediate_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;
```

##### Output

Copy code

```
No returning information.
```

#### Variable markers without variable reordering

Warning

**This case is not supported yet.**

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE PREPARE_ST_TEST()
BEGIN
    DECLARE ctry_list VARCHAR(100);
    DECLARE SQL_string_sel VARCHAR(255);
    DECLARE col_value NUMBER;

    DECLARE C1 CURSOR FOR S1;

    SET ctry_list = '';
    SET col_value = 1;
    SET SQL_string_sel = 'SELECT * FROM databaseTest.MyTemporaryTable where Col1 = ?';
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1 USING col_value;
    FETCH C1 INTO ctry_list;
    IF (ctry_list <> '') THEN
        INSERT INTO databaseTest.MyStatusTable(col1) VALUES ('ok');
    END IF;
    CLOSE C1;
END;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

##### Output

| Col1 |
| --- |
| ok |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE PREPARE_ST_TEST_MARKERS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        p1 RESULTSET;
        p1_sql VARCHAR DEFAULT '';

    BEGIN
        LET ctry_list VARCHAR(100);
        LET SQL_string_sel VARCHAR(255);
        LET col_value NUMBER(38, 18);
        LET S1 RESULTSET;

        ctry_list := '';

        col_value := 1;

        SQL_string_sel := 'SELECT * FROM MyTemporaryTable WHERE Col1 = ?';

        p1_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE p1_sql USING (col_value)
        );
        LET C1 CURSOR FOR S1;

        OPEN C1;
            FETCH C1 INTO ctry_list;
        IF (RTRIM(ctry_list) <> '') THEN
            INSERT INTO MyStatusTable (col1)
            VALUES ('ok');
        END IF;
            CLOSE C1;
    END;
$$;
```

##### Output

| Col1 |
| --- |
| ok |

Expand

Show lessSee more

#### Variable markers with variable reordering

Warning

**This case is not supported yet.**

Note

When there are variables setting the value into different ones between the `PREPARE` statement and `OPEN` cursor in Teradata, It is necessary to move this variable before the `EXECUTE IMMEDIATE` in Snowflake. So, the dynamic variable information is updated at the moment of running the dynamic query.

##### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE PREPARE_ST_TEST()
BEGIN
    DECLARE ctry_list VARCHAR(100);
    DECLARE SQL_string_sel VARCHAR(255);
    DECLARE col_name NUMBER;

    DECLARE C1 CURSOR FOR S1;

    SET ctry_list = '';
    SET col_name = 1;
    SET SQL_string_sel = 'SELECT * FROM databaseTest.MyTemporaryTable where Col1 = ?';
    PREPARE S1 FROM SQL_string_sel;
    SET col_name = 2; // change value before open cursor
    OPEN C1 USING col_name;
    FETCH C1 INTO ctry_list;
    IF (ctry_list <> '') THEN
        INSERT INTO databaseTest.MyStatusTable(col1) VALUES ('ok');
    END IF;
    CLOSE C1;
END;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

##### Output

Copy code

```
"MyStatusTable" should be empty.
```

##### Snowflake Scripting

Note

Usages for cursors must be renamed and declared again.

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE PREPARE_ST_TEST_MARKERS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        p1 RESULTSET;
        p1_sql VARCHAR DEFAULT '';

    BEGIN
        LET ctry_list VARCHAR(100);
        LET SQL_string_sel VARCHAR(255);
        LET col_value NUMBER(38, 18);
        LET S1 RESULTSET;

        ctry_list := '';

        col_value := 1;

        SQL_string_sel := 'SELECT * FROM MyTemporaryTable WHERE Col1 = ?';

        p1_sql := SQL_string_sel;

        col_value:= 2; // Move variable setting before the EXECUTE IMMEDIATE

        S1 := (
            EXECUTE IMMEDIATE p1_sql USING (col_value)
        );

        LET C1 CURSOR FOR S1;

        OPEN C1;
            FETCH C1 INTO ctry_list;
        IF (RTRIM(ctry_list) <> '') THEN
            INSERT INTO MyStatusTable (col1)
            VALUES ('ok');
        END IF;
            CLOSE C1;
    END;
$$;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

##### Output

Copy code

```
"MyStatusTable" should be empty.
```

#### Anonymous blocks - Declaration outside the block

Warning

**This case is not supported yet.**

##### Teradata

##### Query

Copy code

```
 REPLACE PROCEDURE anonymous_blocks_case(OUT procedure_result INTEGER)
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    DECLARE C2 CURSOR FOR S2;

    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;

    BEGIN
        PREPARE S2 FROM SQL_string_sel;
        OPEN C2;
        FETCH C2 INTO procedure_result;
        CLOSE C2;
    END;

    OPEN C1;
    CLOSE C1;
END;
```

##### Output

Copy code

```
No returning information.
```

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE anonymous_blocks_case (
--                                                   OUT
                                                       PROCEDURE_RESULT INTEGER)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "none",  "convertedOn": "01/01/0001" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
    S2 RESULTSET;
  BEGIN
    -- Actual Cursor usage

    prepareQuery_aux_sql := SQL_string_sel
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    CLOSE CURSOR_S1_INSTANCE_V0;

    BEGIN
      prepareQuery_aux_sql := SQL_string_sel
      S2 := (
        EXECUTE IMMEDIATE prepareQuery_aux_sql
      );
      LET CURSOR_S2_INSTANCE_V# CURSOR
      FOR
        S1;
      OPEN CURSOR_S2_INSTANCE_V#;
      FETCH
        CURSOR_S2_INSTANCE_V#
      INTO
        procedure_result;
      CLOSE CURSOR_S2_INSTANCE_V#;
    END;

    OPEN CURSOR_S1_INSTANCE_V0; -- NAME REMAINS AS NEEDED IN LOGIC
    CLOSE CURSOR_S1_INSTANCE_V0;
    RETURN null;
  END;
$$;
```

##### Output

Copy code

```
No returning information.
```

### Known Issues

- Review carefully nested cursors and conditionals, if that is the case.

### Related EWIs

No related EWIs.

## REPEAT

Translation reference to convert Teradata REPEAT statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Teradata’s `REPEAT` statement is translated to Snowflake Scripting `REPEAT` syntax.

For more information, see the [Teradata REPEAT documentation](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/REPEAT).

Copy code

```
 [label_name:] REPEAT
    { sql_statement }
    UNTIL conditional_expression
END REPEAT [label_name];
```

### Sample Source Patterns

#### Teradata

##### Repeat

Copy code

```
 CREATE PROCEDURE repeatProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;

    customeLabel: REPEAT
    	SET counter = counter + 1;
	UNTIL 10 < counter
    END REPEAT customeLabel;

    SET resultCounter = counter;
END;

CALL repeatProcedure(:?);
```

##### Result

Copy code

```
|resultCounter|
|-------------|
|11           |
```

##### Snowflake Scripting

##### Repeat

Copy code

```
 CREATE OR REPLACE PROCEDURE repeatProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		counter INTEGER DEFAULT 0;
	BEGIN

		REPEAT
			counter := counter + 1;
		UNTIL (10 < :counter)
		END REPEAT CUSTOMELABEL;
		resultCounter := counter;
	END;
$$;

CALL repeatProcedure(:?);
```

##### Result

Copy code

```
|REPEATPROCEDURE|
|---------------|
|1             |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## SET

Translation reference to convert Teradata SET statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> Assigns a value to a local variable or parameter in a stored procedure.

For more information, see the [Teradata SET documentation](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/7wwpafjC_5JfF~I2zpTsQQ).

Copy code

```
 SET assigment_target = assigment_source ;
```

### Sample Source Patterns

#### Teradata

##### Query

Copy code

```
 CREATE PROCEDURE setExample ( OUT PARAM1 INTEGER )
BEGIN
    DECLARE COL_COUNT INTEGER;
    SET COL_COUNT = 3;
    SET PARAM1 = COL_COUNT + 1;
END;
```

##### Result

Copy code

```
|PARAM1 |
|-------|
|4      |
```

##### Snowflake Scripting

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE setExample (PARAM1 OUT INTEGER )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        COL_COUNT INTEGER;
    BEGIN

        COL_COUNT := 3;
        PARAM1 := COL_COUNT + 1;
    END;
$$;
```

##### Result

Copy code

```
|PARAM1 |
|-------|
|4      |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## SYSTEM\_DEFINED

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is**<mark style=”background-color:red;”>**removed from the migration**</mark>**because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description

Property in Teradata that can be after a `CREATE` statement in cases such as `JOIN INDEX`.

### Sample Source Patterns

Notice that SYSTEM\_DEFINED has been removed from the source code because it is a non-relevant syntax in Snowflake.

#### Teradata

Copy code

```
 CREATE SYSTEM_DEFINED JOIN INDEX MY_TESTS.MYPARTS_TJI004 ,FALLBACK ,CHECKSUM = DEFAULT, MAP = TD_MAP1 AS
CURRENT TRANSACTIONTIME
SELECT
    MY_TESTS.myParts.ROWID,
    MY_TESTS.myParts.part_id,
    MY_TESTS.part_duration
FROM MY_TESTS.myParts
UNIQUE PRIMARY INDEX (part_id);
```

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "MY_TESTS.myParts" **
CREATE OR REPLACE DYNAMIC TABLE MY_TESTS.MYPARTS_TJI004
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/01/2024" }}'
AS
--    --** SSC-FDM-TD0025 - TEMPORAL FORMS ARE NOT SUPPORTED IN SNOWFLAKE **
--    CURRENT TRANSACTIONTIME
                            SELECT
        MY_TESTS.myParts.ROWID,
        MY_TESTS.myParts.part_id,
        MY_TESTS.part_duration
    FROM
        MY_TESTS.myParts;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-0007](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007): Element with missing dependencies.
2. [SSC-FDM-TD0025](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0025): Teradata Database Temporal Table is not supported in Snowflake.
3. [SSC-FDM-0031](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0031): Dynamic Table required parameters set by default

## WHILE

Translation reference to convert Teradata WHILE statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Teradata’s `WHILE` statement is translated to Snowflake Scripting`WHILE` syntax.

For more information, see the [Teradata WHILE documentation](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/WHILE).

Copy code

```
 [label_name:] WHILE conditional_expression DO
    { sql_statement }
END WHILE [label_name];
```

### Sample Source Patterns

#### Teradata

##### While

Copy code

```
 REPLACE PROCEDURE whileProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;
    customeLabel: WHILE counter < 10 DO
        SET counter = counter + 1;
    END WHILE customeLabel;
    SET resultCounter = counter;
END;

CALL whileProcedure(:?);
```

##### Result

Copy code

```
 |resultCounter|
|-------------|
|10           |
```

##### Snowflake Scripting

##### While

Copy code

```
 CREATE OR REPLACE PROCEDURE whileProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        counter INTEGER DEFAULT 0;
    BEGIN

        WHILE (:counter < 10) LOOP
            counter := counter + 1;
        END LOOP CUSTOMELABEL;
        resultCounter := counter;
    END;
$$;

CALL whileProcedure(:?);
```

##### Result

Copy code

```
 |WHILEPROCEDURE|
|--------------|
|10            |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.
