# SQL Server-Azure Synapse - CREATE PROCEDURE (Snowflake Scripting)

## BEGIN and COMMIT Transaction

Translation reference to convert Transact-SQL BEGIN and COMMIT transaction to Snowflake SQL

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Snowflake SQL, a transaction can be started explicitly by executing a BEGIN statement. Snowflake supports the synonyms `BEGIN WORK` and `BEGIN TRANSACTION`. Snowflake recommends using `BEGIN TRANSACTION`.

A transaction can be ended explicitly by executing COMMIT. For more information, see the [Snowflake Transactions documentation](https://docs.snowflake.com/en/sql-reference/transactions.html).

### Sample Source Patterns

The following examples detail the BEGIN and COMMIT transaction statements.

#### Transact-SQL

##### BEGIN/COMMIT TRANSACTION

Copy code

```
CREATE PROCEDURE TestTransaction
AS
BEGIN
    DROP TABLE IF EXISTS NEWTABLE;
    CREATE TABLE NEWTABLE(COL1 INT, COL2 VARCHAR);
      BEGIN TRANSACTION;
         INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
         INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
      COMMIT TRANSACTION;
END
```

##### Begin/Commit transaction with label

Copy code

```
CREATE PROCEDURE TestTransaction
AS
BEGIN
    DROP TABLE IF EXISTS NEWTABLE;
    CREATE TABLE NEWTABLE(COL1 INT, COL2 VARCHAR);
      BEGIN TRANSACTION LabelA;
        INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
        INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
      COMMIT TRANSACTION LabelA;
END
```

##### Snowflake SQL

##### BEGIN/COMMIT

Copy code

```
CREATE OR REPLACE PROCEDURE TestTransaction ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DROP TABLE IF EXISTS NEWTABLE;
        CREATE OR REPLACE TABLE NEWTABLE (
            COL1 INT,
            COL2 VARCHAR
        );
            BEGIN TRANSACTION;
            INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
         INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
            COMMIT;
    END;
$$;
```

##### BEGIN/COMMIT transaction with label

Copy code

```
 CREATE OR REPLACE PROCEDURE TestTransaction ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DROP TABLE IF EXISTS NEWTABLE;
        CREATE OR REPLACE TABLE NEWTABLE (
            COL1 INT,
            COL2 VARCHAR
        );
            BEGIN TRANSACTION
            !!!RESOLVE EWI!!! /*** SSC-EWI-0101 - COMMENTED OUT TRANSACTION LABEL NAME BECAUSE IS NOT APPLICABLE IN SNOWFLAKE ***/!!!
            LabelA;
            INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
        INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
            COMMIT;
    END;
$$;
```

### Known Issues

1. Nested transactions are not supported in Snowflake. Review the following documentation for more information: <https://docs.snowflake.com/en/sql-reference/transactions>

### Related EWIs

1. [SSC-EWI-0101](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0101): Commented out transaction label name because is not applicable in Snowflake.

## CALL

Translation reference for CALL statement

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The CALL statement is not supported in Snowflake Scripting since this is part of the ODBC API and not a SQL statement, therefore this statement is not translated.

## CASE

Translation reference to convert Transact-SQL Case expression to Snowflake Scripting

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Transact-SQL has two possible formats of the Case expression. both of them for the purpose of evaluating expressions and conditionally obtaining results. The first one refers to a Simple Case Expression that will evaluate if an input\_expression matches one or more of the when\_expression. The second one will evaluate each Boolean\_expression independently. The else clause is supported in both formats.

According to the official Transact-SQL Case documentation:

CASE can be used in any statement or clause that allows a valid expression. For example, you can use CASE in statements such as SELECT, UPDATE, DELETE and SET, and in clauses such as select\_list, IN, WHERE, ORDER BY, and HAVING.

For more information, see the [Transact-SQL CASE documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver15).

Copy code

```
 -- Simple CASE expression:
CASE input_expression
     WHEN when_expression THEN result_expression [ ...n ]
     [ ELSE else_result_expression ]
END

-- Searched CASE expression:
CASE
     WHEN boolean_expression THEN result_expression [ ...n ]
     [ ELSE else_result_expression ]
END
```

Note: Transact-SQL allows to optionally encapsulate the input\_expression and the boolean\_expression in parentheses; Snowflake Scripting too.

### Sample Source Patterns

The following examples detail two scenarios where the Case expression can be used and their differences from Snowflake Scripting.

#### Select using Case

##### Transact-SQL

##### Simple CASE

Copy code

```
CREATE OR ALTER PROCEDURE SelectCaseDemoProcedure
AS
      SELECT TOP 10
          LOGINID,
          CASE (MARITALSTATUS)
              WHEN 'S' THEN 'SINGLE'
              WHEN 'M' THEN 'MARIED'
              ELSE 'OTHER'
          END AS status
      FROM HUMANRESOURCES.EMPLOYEE;
GO

EXEC SelectCaseDemoProcedure;
```

##### Searched CASE

Copy code

```
CREATE OR ALTER PROCEDURE SelectCaseDemoProcedure
AS
      SELECT TOP 10
          LOGINID,
          CASE
              WHEN MARITALSTATUS = 'S' THEN 'SINGLE'
              WHEN MARITALSTATUS = 'M' THEN 'MARIED'
              ELSE 'OTHER'
          END AS status
      FROM HUMANRESOURCES.EMPLOYEE;
GO

EXEC SelectCaseDemoProcedure;
```

##### Result

| sqlLOGINID | status |
| --- | --- |
| adventure-works\ken0 | SINGLE |
| adventure-works\terri0 | SINGLE |
| adventure-works\roberto0 | MARIED |
| adventure-works\rob0 | SINGLE |
| adventure-works\gail0 | MARIED |
| adventure-works\jossef0 | MARIED |
| adventure-works\dylan0 | MARIED |
| adventure-works\diane1 | SINGLE |
| adventure-works\gigi0 | MARIED |
| adventure-works\michael6 | MARIED |

Expand

Show lessSee more

##### Snowflake Scripting

Note that in this scenario there are no differences regarding the Case expression itself.

Warning

The declaration and assignment of the `res` variable is to demonstrate the functional equivalence between both languages. It does not appear in the actual output.

##### Simple CASE

Copy code

```
:force:

CREATE OR REPLACE PROCEDURE SelectCaseDemoProcedure ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
      DECLARE
            ProcedureResultSet RESULTSET;
      BEGIN
            ProcedureResultSet := (
            SELECT TOP 10
                  LOGINID,
                CASE (MARITALSTATUS)
                    WHEN 'S' THEN 'SINGLE'
                    WHEN 'M' THEN 'MARIED'
                    ELSE 'OTHER'
                END AS status
            FROM
                  HUMANRESOURCES.EMPLOYEE);
            RETURN TABLE(ProcedureResultSet);
      END;
$$;

CALL SelectCaseDemoProcedure();
```

##### Searched CASE

Copy code

```
CREATE OR REPLACE PROCEDURE SelectCaseDemoProcedure ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
      DECLARE
            ProcedureResultSet RESULTSET;
      BEGIN
            ProcedureResultSet := (
            SELECT TOP 10
                  LOGINID,
                CASE
                    WHEN MARITALSTATUS = 'S' THEN 'SINGLE'
                    WHEN MARITALSTATUS = 'M' THEN 'MARIED'
                    ELSE 'OTHER'
                END AS status
            FROM
                  HUMANRESOURCES.EMPLOYEE);
            RETURN TABLE(ProcedureResultSet);
      END;
$$;

CALL SelectCaseDemoProcedure();
```

##### Result

| LOGINID | STATUS |
| --- | --- |
| adventure-worksken0 | SINGLE |
| adventure-works erri0 | SINGLE |
| adventure-worksoberto0 | MARIED |
| adventure-worksob0 | SINGLE |
| adventure-worksgail0 | MARIED |
| adventure-worksjossef0 | MARIED |
| adventure-worksdylan0 | MARIED |
| adventure-worksdiane1 | SINGLE |
| adventure-worksgigi0 | MARIED |
| adventure-worksmichael6 | MARIED |

Expand

Show lessSee more

#### Set using Case

The AdventureWorks2019 database was used in both languages to obtain the same results.

##### Transact-SQL

##### Simple Case

Copy code

```
CREATE OR ALTER PROCEDURE SetCaseDemoProcedure
AS
    DECLARE @value INT;
    DECLARE @result INT;
    SET @value = 5;

    SET @result =
        CASE @value
            WHEN 1 THEN @value * 10
            WHEN 3 THEN @value * 20
            WHEN 5 THEN @value * 30
            WHEN 7 THEN @value * 40
            ELSE -1
        END;

    RETURN @result
GO

DECLARE @result INT;
EXEC @result = SetCaseDemoProcedure;
PRINT @result;
```

##### Searched Case

Copy code

```
CREATE OR ALTER PROCEDURE SetCaseDemoProcedure
AS
    DECLARE @value INT;
    DECLARE @result INT;
    SET @value = 5;

    SET @result =
        CASE
            WHEN @value = 1 THEN @value * 10
            WHEN @value = 3 THEN @value * 20
            WHEN @value = 5 THEN @value * 30
            WHEN @value = 7 THEN @value * 40
            ELSE -1
        END;

    RETURN @result
GO

DECLARE @result INT;
EXEC @result = SetCaseDemoProcedure;
PRINT @result;
```

##### Result

| result |
| --- |
| 150 |

Expand

Show lessSee more

##### Snowflake Scripting

Warning

Snowflake Scripting does not allow setting a case expression directly to a variable. Both Transact-SQL Case expression formats translate to the following grammar in Snowflake Scripting.

##### SimpleCase

Copy code

```
CREATE OR REPLACE PROCEDURE SetCaseDemoProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        VALUE INT;
        RESULT INT;
    BEGIN

        VALUE := 5;
        CASE (:VALUE)
            WHEN 1 THEN
                RESULT := :VALUE * 10;
            WHEN 3 THEN
                RESULT := :VALUE * 20;
            WHEN 5 THEN
                RESULT := :VALUE * 30;
            WHEN 7 THEN
                RESULT := :VALUE * 40;
            ELSE
                RESULT := -1;
        END;
        RETURN :RESULT;
    END;
$$;

DECLARE
    RESULT INT;
BEGIN
    CALL SetCaseDemoProcedure();
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Print' NODE ***/!!!
    PRINT @result;
END;
```

##### Searched Case

Copy code

```
CREATE OR REPLACE PROCEDURE SetCaseDemoProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        VALUE INT;
        RESULT INT;
    BEGIN

        VALUE := 5;
        CASE
            WHEN :VALUE = 1 THEN
                RESULT := :VALUE * 10;
            WHEN :VALUE = 3 THEN
                RESULT := :VALUE * 20;
            WHEN :VALUE = 5 THEN
                RESULT := :VALUE * 30;
            WHEN :VALUE = 7 THEN
                RESULT := :VALUE * 40;
            ELSE
                RESULT := -1;
        END;
        RETURN :RESULT;
    END;
$$;

DECLARE
    RESULT INT;
BEGIN
    CALL SetCaseDemoProcedure();
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Print' NODE ***/!!!
    PRINT @result;
END;
```

##### Result

| result |
| --- |
| 150 |

Expand

Show lessSee more

### Related EWIs

1. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

## CREATE PROCEDURE

Translation reference to convert Transact-SQL CREATE PROCEDURE clauses to Snowflake

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

The create procedure statement allows the creation of stored procedures that can:

- Accept input parameters and return multiple values in the form of output parameters to the calling procedure or batch.
- Contain programming statements that perform operations in the database, including calling other procedures.
- Return a status value to a calling procedure or batch to indicate success or failure (and the reason for failure).

For more information, see the [Transact-SQL CREATE PROCEDURE documentation](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver15).

Copy code

```
CREATE [ OR ALTER ] { PROC | PROCEDURE }
    [schema_name.] procedure_name [ ; number ]
    [ { @parameter [ type_schema_name. ] data_type }
        [ VARYING ] [ = default ] [ OUT | OUTPUT | [READONLY]
    ] [ ,...n ]
[ WITH <procedure_option> [ ,...n ] ]
[ FOR REPLICATION ]
AS { [ BEGIN ] sql_statement [;] [ ...n ] [ END ] }
[;]
```

### Sample Source Patterns

#### Stored procedure without body

A stored procedure without a body is an unusual scenario that is allowed in Transact-SQL. Snowflake Scripting does not allow defining procedures without a body, but the following example shows the equivalence.

##### Transact-SQL

##### Procedure

Copy code

```
CREATE PROC SampleProcedure AS;
```

##### Snowflake Scripting

Copy code

```
:force:

CREATE OR REPLACE PROCEDURE SampleProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      RETURN '';
   END;
$$;
```

#### Basic stored procedure

The following example details a simple stored procedure that will include a new Privacy department into the AdventureWorks2019 database.

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE Add_Privacy_Department
AS
EXECUTE ('INSERT INTO HumanResources.Department VALUES (''Privacy'', ''Executive General and Administration'', default)');
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE Add_Privacy_Department ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE 'INSERT INTO HumanResources.Department VALUES ('Privacy', 'Executive General and Administration', default);';
  END;
$$;
```

#### Alter procedure

The transformation for the ALTER procedure is equivalent to the basic procedure.

##### Transact-SQL

Copy code

```
ALTER PROCEDURE procedureName
AS
SELECT 1 AS ThisDB;
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE procedureName ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
ProcedureResultSet RESULTSET;
BEGIN
ProcedureResultSet := (
SELECT 1 AS ThisDB);
RETURN TABLE(ProcedureResultSet);
END;
$$;
```

#### Using parameters

You can use parameters to drive your logic or construct dynamic SQL statements inside your stored procedure. In the following example a simple SetNewPrice stored procedure is constructed, which sets a new product price based on the arguments sent by the caller.

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE SetNewPrice @ProductID INT, @NewPrice MONEY
AS
  BEGIN
    DECLARE @dynSqlStatement AS VARCHAR(300);
    SET @dynSqlStatement = 'UPDATE Production.ProductListPriceHistory SET ListPrice = ' + CAST(@NewPrice AS VARCHAR(10)) + ' WHERE ProductID = ' + CAST(@ProductID AS VARCHAR(10)) + ' AND EndDate IS NULL';
    EXECUTE (@dynSqlStatement);
  END;
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE SetNewPrice (PRODUCTID INT, NEWPRICE NUMBER(38, 4))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    DYNSQLSTATEMENT VARCHAR(300);
  BEGIN

    DYNSQLSTATEMENT := 'UPDATE Production.ProductListPriceHistory
   SET
      ListPrice = ' || CAST(:NEWPRICE AS VARCHAR(10)) || '
   WHERE
      ProductID = ' || CAST(:PRODUCTID AS VARCHAR(10)) || '
      AND EndDate IS NULL;';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :DYNSQLSTATEMENT;
  END;
$$;
```

#### Output Parameters

Transact-SQL output keyword indicates that the parameter is an output parameter, whose value will be returned to the stored procedure caller. For example, the following procedure will return the number of vacation hours of a specific employee.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE GetVacationHours
   @employeeId INT,
   @vacationHours INT OUTPUT
AS
BEGIN
   SELECT @vacationHours = VacationHours
   FROM HumanResources.Employee
   WHERE NationalIDNumber = @employeeID
END;
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE GetVacationHours (EMPLOYEEID INT, VACATIONHOURS OUT INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      SELECT
         VacationHours
      INTO
         :VACATIONHOURS
      FROM
         HumanResources.Employee
      WHERE
         NationalIDNumber = :EMPLOYEEID;
   END;
$$;
```

#### Optional Parameters

A parameter is considered optional if the parameter has a default value specified when it is declared. It is not necessary to provide a value for an optional parameter in a procedure call.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE OPTIONAL_PARAMETER @VAR1 INT = 1, @VAR2 INT = 2
AS
    BEGIN
        RETURN NULL;
    END

GO

EXEC OPTIONAL_PARAMETER @VAR2 = 4
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE OPTIONAL_PARAMETER (VAR1 INT DEFAULT 1, VAR2 INT DEFAULT 2)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        RETURN NULL;
    END;
$$;

CALL OPTIONAL_PARAMETER(VAR2 => 4);
```

#### EXECUTE AS

Transact-SQL’s EXECUTE AS clause defines the execution context of the stored procedure, specifying which user account the Database Engine uses to validate permissions on objects that are referenced within the procedure. For example, we can modify the previous GetVacationHours procedure to define different execution contexts.

- Owner (default in Snowflake Scripting)

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE GetVacationHours
   @employeeId INT,
   @vacationHours INT OUTPUT
WITH EXECUTE AS OWNER
AS
BEGIN
   SELECT @vacationHours = VacationHours
   FROM HumanResources.Employee
   WHERE NationalIDNumber = @employeeID
END;
```

##### Snowflake Scripting

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "HumanResources.Employee" **
CREATE OR REPLACE PROCEDURE GetVacationHours (EMPLOYEEID INT, VACATIONHOURS OUT INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS OWNER
AS
$$
   BEGIN
      SELECT
         VacationHours
      INTO
         :VACATIONHOURS
      FROM
         HumanResources.Employee
      WHERE
         NationalIDNumber = :EMPLOYEEID;
   END;
$$;
```

#### Caller

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE GetVacationHours
   @employeeId INT,
   @vacationHours INT OUTPUT
WITH EXECUTE AS CALLER
AS
BEGIN
   SELECT @vacationHours = VacationHours
   FROM HumanResources.Employee
   WHERE NationalIDNumber = @employeeID
END;
```

##### Snowflake Scripting

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "HumanResources.Employee" **
CREATE OR REPLACE PROCEDURE GetVacationHours (EMPLOYEEID INT, VACATIONHOURS OUT INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      SELECT
         VacationHours
      INTO
         :VACATIONHOURS
      FROM
         HumanResources.Employee
      WHERE
         NationalIDNumber = :EMPLOYEEID;
   END;
$$;
```

Warning

SELF and specific user (‘user\_name’) execution contexts are not supported in Snowflake Scripting.

#### READONLY AND VARYING PARAMETERS

Snowflake does not support `READONLY` and `VARYING` parameter types, an FDM is added instead.

##### Transact-SQL

Copy code

```
 CREATE OR ALTER PROCEDURE GetVacationHours
   @Param1 INT READONLY,
   @Param2 INT VARYING
AS
BEGIN
   SELECT * FROM Table1;
END;
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE GetVacationHours (PARAM1 INT !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'READONLY PARAMETERS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!, PARAM2 INT !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'VARYING PARAMETERS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!)
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      ProcedureResultSet RESULTSET;
   BEGIN
      ProcedureResultSet := (
      SELECT
         *
      FROM
         Table1);
      RETURN TABLE(ProcedureResultSet);
   END;
$$;
```

### Known Issues

#### Unsupported Optional Arguments

- [VARYING] Applies only to **cursor** parameters.Specifies the result set supported as an output parameter. This parameter is dynamically constructed by the procedure and its contents may vary. Snowflake scripting does not support CURSOR as a valid return data type.
- [= default] Makes a parameter optional through the definition of a default value. Snowflake scripting does not natively supports default parameter values.
- [READONLY] Indicates that the parameter cannot be updated or modified within the body of the procedure. Currently unsupported in Snowflake Scripting.
- [WITH RECOMPILE] Forces the database engine to compile the stored procedure’s query plan each time it is executed. Currently unsupported in Snowflake Scripting.
- [WITH ENCRYPTION] Used to encrypt the text of a stored procedure. Only users with access to system tables or database files (such as sysadmin users) will be able to access the procedure text after its creation. Currently unsupported in Snowflake Scripting.
- [FOR REPLICATION] Restricts the stored procedure to be executed only during replication. Currently unsupported in Snowflake Scripting.

### Related EWIs

1. [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030): The statement below has usages of dynamic SQL.
2. [SSC-EWI-0058](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.

## CURSOR

Translation reference to convert Transact-SQL CURSOR statement to Snowflake Scripting

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Transact-SQL statements produce a complete result set, but there are times when the results are best processed one row at a time. Opening a cursor on a result set allows processing the result set one row at a time. You can assign a cursor to a variable or parameter with a **cursor** data type. For more information, see the [Transact-SQL Cursors documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/cursors-transact-sql?view=sql-server-ver15).

Copy code

```
 //ISO Syntax
DECLARE cursor_name [ INSENSITIVE ] [ SCROLL ] CURSOR
     FOR select_statement
     [ FOR { READ ONLY | UPDATE [ OF column_name [ ,...n ] ] } ]
[;]

//Transact-SQL Extended Syntax
DECLARE cursor_name CURSOR [ LOCAL | GLOBAL ]
     [ FORWARD_ONLY | SCROLL ]
     [ STATIC | KEYSET | DYNAMIC | FAST_FORWARD ]
     [ READ_ONLY | SCROLL_LOCKS | OPTIMISTIC ]
     [ TYPE_WARNING ]
     FOR select_statement
     [ FOR UPDATE [ OF column_name [ ,...n ] ] ]
[;]
```

Copy code

```
 FETCH
          [ [ NEXT | PRIOR | FIRST | LAST
                    | ABSOLUTE { n | @nvar }
                    | RELATIVE { n | @nvar }
               ]
               FROM
          ]
{ { [ GLOBAL ] cursor_name } | @cursor_variable_name }
[ INTO @variable_name [ ,...n ] ]
```

Copy code

```
OPEN { { [ GLOBAL ] cursor_name } | cursor_variable_name }
```

Copy code

```
CLOSE { { [ GLOBAL ] cursor_name } | cursor_variable_name }
```

Copy code

```
DEALLOCATE { { [ GLOBAL ] cursor_name } | @cursor_variable_name }
```

### Sample Source Patterns

#### Transact-SQL

Notice that the following parameters are inherently supported by Snowflake Scripting.

- [LOCAL].
- [FORWARD\_ONLY].
- [FAST\_FORWARD] Specifies a FORWARD\_ONLY (FETCH NEXT only) and READ\_ONLY
- [READ\_ONLY] the WHERE CURRENT OF does not exist in Snowflake Scripting.

##### Cursor

Copy code

```
CREATE TABLE vEmployee   (
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255),
);

INSERT INTO vEmployee(PersonID, LastName, FirstName)
VALUES
    (1, 'AA', 'A'),
    (2, 'BB', 'B'),
    (3, 'CC', 'C'),
    (4, 'DD', 'D'),
    (5, 'EE', 'E'),
    (6, 'FF', 'F'),
    (7, 'GG', 'G');

CREATE OR ALTER PROCEDURE CursorExample
AS
    DECLARE
        @CursorVar CURSOR,
	@firstName VARCHAR;

    SET @CursorVar = CURSOR LOCAL FORWARD_ONLY STATIC READ_ONLY
	FOR
	SELECT FirstName
	FROM vEmployee;

    OPEN @CursorVar;

    FETCH NEXT FROM @CursorVar INTO @firstName;
    FETCH NEXT FROM @CursorVar INTO @firstName;

    CLOSE @CursorVar;

    SELECT @firstName;
GO
```

##### Result

Copy code

```
B
```

##### Snowflake Scripting

##### Cursor

Copy code

```
CREATE OR REPLACE TABLE vEmployee (
	PersonID INT,
	LastName VARCHAR(255),
	FirstName VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES
    (1, 'AA', 'A'),
    (2, 'BB', 'B'),
    (3, 'CC', 'C'),
    (4, 'DD', 'D'),
    (5, 'EE', 'E'),
    (6, 'FF', 'F'),
    (7, 'GG', 'G');

CREATE OR REPLACE PROCEDURE CursorExample ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		CURSORVAR CURSOR
		FOR
			SELECT FirstName
			FROM vEmployee;
		FIRSTNAME VARCHAR;
		ProcedureResultSet RESULTSET;
	BEGIN

		OPEN CURSORVAR;
		FETCH
			CURSORVAR
		INTO
			:FIRSTNAME;
		FETCH
			CURSORVAR
		INTO
			:FIRSTNAME;
		CLOSE CURSORVAR;
		ProcedureResultSet := (
		SELECT
			:FIRSTNAME);
		RETURN TABLE(ProcedureResultSet);
	END;
$$;
```

##### Result

Copy code

```
B
```

### Known Issues

The following parameters are not supported:

DECLARE CURSOR

- [ GLOBAL ] Allows referencing the cursor name in any stored procedure or batch executed by the connection. Snowflake Scripting only allows the use of the cursor locally.
- [ SCROLL ] Snowflake Scripting only support FETCH NEXT.
- [ KEYSET | DYNAMIC ] If after opening a cursor and update to the table is made, these options may display some of the changes when fetching the cursor, Snowflake scripting only supports STATIC, in other words, after the cursor is opened the changes to the table are not detected by the cursor.
- [SCROLL\_LOCKS] Specifies that positioned updates or deletes made through the cursor are guaranteed to succeed, Snowflake Scripting cannot guarantee it.
- [OPTIMISTIC] When an update or delete is made through the cursor it uses comparisons of timestamp column values, or a checksum value if the table has no timestamp column, to determine whether the row was modified after it was read into the cursor. Snowflake Scripting does not have an internal process to replicate it.
- [TYPE\_WARNING]

FETCH

- [PRIOR | FIRST | LAST] Snowflake Scripting only support NEXT.
- [ABSOLUTE] Snowflake Scripting only supports NEXT but the behavior can be replicated.
- [RELATIVE] Snowflake Scripting but the behavior can be replicated.
- [ GLOBAL ] Allows referencing the cursor name in any stored procedure or batch executed by the connection. Snowflake Scripting only allows the use of the cursor locally.
- FETCH without INTO is not supported.
- When the FETCH statement is located inside a loop it is considered a complex pattern as it may have an impact on the Snowflake translated code performance. Check the related issues section for more information.

#### Fetch inside loop sample

##### SQL Server

Copy code

```
CREATE OR ALTER PROCEDURE cursor_procedure1
AS
BEGIN
DECLARE cursor1 CURSOR FOR SELECT col1 FROM my_table;
WHILE 1=0
   BEGIN
      FETCH NEXT FROM @cursor1 INTO @variable1;
   END
END;
```

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE cursor_procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      --** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
      cursor1 CURSOR
      FOR
         SELECT
            col1
         FROM
            my_table;
   BEGIN

      WHILE (1=0) LOOP
         --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
         FETCH
            CURSOR1
            INTO
            :VARIABLE1;
      END LOOP;
   END;
$$;
```

#### OPEN

- [ GLOBAL ] Allows referencing the cursor name in any stored procedure or batch executed by the connection. Snowflake Scripting only allows the use of the cursor locally.

CLOSE

- [ GLOBAL ] Allows referencing the cursor name in any stored procedure or batch executed by the connection. Snowflake Scripting only allows the use of the cursor locally.

DEALLOCATE removes a cursor reference. Snowflake Scripting doesn’t require explicit deallocation because cursors are automatically deallocated when they go out of scope. The statement is commented out with [SSC-FDM-TS0057](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0057).

WHERE CURRENT OF the use of this statement is not supported, for example:

Copy code

```
:force:

CREATE OR ALTER PROCEDURE CursorWithCurrent
AS
    DECLARE
        @CursorVar CURSOR;

    SET @CursorVar = CURSOR
	FOR
	SELECT FirstName
	FROM vEmployee;

    OPEN @CursorVar;

    FETCH NEXT FROM @CursorVar;
    FETCH NEXT FROM @CursorVar;

    UPDATE vEmployee SET LastName = 'Changed' WHERE CURRENT OF @CursorVar;

    CLOSE @CursorVar;
GO
```

Environment variables

- @@CURSOR\_ROWS
- @@FETCH\_STATUS

### Related EWIs

1. [SSC-FDM-TS0013](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0013): Snowflake Scripting cursor rows are not modifiable.
2. [SSC-PRF-0003](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003): Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.

## DECLARE

Translation reference to convert Transact-SQL DECLARE statement to Snowflake Scripting

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Transact-SQL DECLARE statement allows the creation of variables that can be used in the scope of the batch or a stored procedure. For more information, see the [Transact-SQL DECLARE documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/declare-local-variable-transact-sql?view=sql-server-ver15).

Copy code

```
:force:
-- Syntax for SQL Server and Azure SQL Database

DECLARE
{
    { @local_variable [AS] data_type  [ = value ] }
  | { @cursor_variable_name CURSOR }
} [,...n]
| { @table_variable_name [AS] <table_type_definition> }

<table_type_definition> ::=
     TABLE ( { <column_definition> | <table_constraint> } [ ,...n] )

<column_definition> ::=
     column_name { scalar_data_type | AS computed_column_expression }
     [ COLLATE collation_name ]
     [ [ DEFAULT constant_expression ] | IDENTITY [ (seed ,increment ) ] ]
     [ ROWGUIDCOL ]
     [ <column_constraint> ]

<column_constraint> ::=
     { [ NULL | NOT NULL ]
     | [ PRIMARY KEY | UNIQUE ]
     | CHECK ( logical_expression )
     | WITH ( <index_option > )
     }

<table_constraint> ::=
     { { PRIMARY KEY | UNIQUE } ( column_name [ ,...n] )
     | CHECK ( search_condition )
     }
```

### Sample Source Patterns

#### Declare variables

Variables can be created in different ways. Variables may or may not have a default value and several variables can be declared in the same line.

Notice that Snowflake Scripting does not allow creating more than one variable per line.

##### Transact-SQL

Copy code

```
:force:
DECLARE @find VARCHAR(30);
DECLARE @find2 VARCHAR(30) = 'Default';
DECLARE @var VARCHAR(5), @var2 varchar(5);
```

##### Snowflake Scripting

Copy code

```
:force:
DECLARE
    FIND VARCHAR(30);
    FIND2 VARCHAR(30) := 'Default';
    VAR VARCHAR(5);
    VAR2 VARCHAR(5);
BEGIN
    RETURN '';
END;
```

#### Declare table variables

Transact-SQL allows the creation of table variables that can be used as regular tables. Snowflake scripting does not support this, instead, a table can be created and then dropped at the end of the procedure.

##### Transact-SQL

Copy code

```
:force:
DECLARE @MyTableVar TABLE(
    column1 varchar(10));
```

##### Snowflake Scripting

Copy code

```
:force:
BEGIN
    DECLARE
        T_MYTABLEVAR TABLE(
            column1 VARCHAR(10));
END;
```

#### DECLARE statement outside routines (functions and procedures)

Unlike Transact-SQL, Snowflake does not support executing isolated statements like DECLARE outside routines like functions or procedures. For this scenario, the statement should be encapsulated in an anonymous block, as shown in the following examples. This statement is usually used before a [`SET STATEMENT`](#set).

##### Transact-SQL

Copy code

```
:force:
DECLARE @Group nvarchar(50), @Sales MONEY;
SET @Group = N'North America';
SET @Sales = 2000000;
```

##### Snowflake Scripting

Copy code

```
:force:
DECLARE
    _GROUP VARCHAR(50);
    SALES NUMBER(38, 4);
BEGIN
    _GROUP := 'North America';
    SALES := 2000000;
END;
```

If there is a scenario with only DECLARE statements, the BEGIN…END block should have a RETURN NULL statement to avoid errors, since this block can’t be empty.

##### Transact-SQL

Copy code

```
:force:
DECLARE @Group nvarchar(50), @Sales MONEY;
```

##### Snowflake Scripting

Copy code

```
:force:
DECLARE
    _GROUP VARCHAR(50);
    SALES NUMBER(38, 4);
BEGIN
    RETURN '';
END;
```

## EXECUTE

Translation reference to convert Transact-SQL Execute statement to Snowflake

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Transact-SQL EXECUTE statement allows the execution of a command string or character string within a Transact-SQL batch, a scalar-valued user-defined function, or a stored procedure. For more information, see the [Transact-SQL EXECUTE documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver15).

Copy code

```
 -- Execute a character string
{ EXEC | EXECUTE }
    ( { @string_variable | [ N ]'tsql_string' } [ + ...n ] )
    [ AS { LOGIN | USER } = ' name ' ]
[;]

-- Execute a stored procedure or function
[ { EXEC | EXECUTE } ]
    {
      [ @return_status = ]
      { module_name [ ;number ] | @module_name_var }
        [ [ @parameter = ] { value
                           | @variable [ OUTPUT ]
                           | [ DEFAULT ]
                           }
        ]
      [ ,...n ]
      [ WITH <execute_option> [ ,...n ] ]
    }
[;]
```

### Sample Source Patterns

#### Execution of character string

EXECUTE can be used to perform SQL operations passed directly as literals. In the following example it is used within a stored procedure that will insert a new privacy department into the AdventureWorks2019 database.

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE AddPrivacyDepartment
AS
EXECUTE ('INSERT INTO HumanResources.Department VALUES (''Privacy'', ''Executive General and Administration'', default)');
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE AddPrivacyDepartment ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
BEGIN
!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
EXECUTE IMMEDIATE 'INSERT INTO HumanResources.Department VALUES ('Privacy', 'Executive General and Administration', default);';
END;
$$;
```

#### Execution of stored procedure

EXECUTE can also be used to call an existing stored procedure. The following example will call the AddPrivacyDepartment procedure that was created above. It will then run a SELECT to verify that the new department was successfully included.

##### Transact-SQL

Copy code

```
EXECUTE AddPrivacyDepartment;
SELECT DepartmentID, Name, GroupName FROM HumanResources.Department;
```

##### Result

| DepartmentID | Name | GroupName | ModifiedDate |
| --- | --- | --- | --- |
| 1 | Engineering | Research and Development | 2008-04-30 00:00:00.000 |
| 2 | Tool Design | Research and Development | 2008-04-30 00:00:00.000 |
| 3 | Sales | Sales and Marketing | 2008-04-30 00:00:00.000 |
| 4 | Marketing | Sales and Marketing | 2008-04-30 00:00:00.000 |
| 5 | Purchasing | Inventory Management | 2008-04-30 00:00:00.000 |
| 6 | Research and Development | Research and Development | 2008-04-30 00:00:00.000 |
| 7 | Production | Manufacturing | 2008-04-30 00:00:00.000 |
| 8 | Production Control | Manufacturing | 2008-04-30 00:00:00.000 |
| 9 | Human Resources | Executive General and Administration | 2008-04-30 00:00:00.000 |
| 1 0 | Finance | Executive General and Administration | 2008-04-30 00:00:00.000 |
| 1 1 | Information Services | Executive General and Administration | 2008-04-30 00:00:00.000 |
| 1 2 | Document Control | Quality Assurance | 2008-04-30 00:00:00.000 |
| 1 3 | Quality Assurance | Quality Assurance | 2008-04-30 00:00:00.000 |
| 1 4 | Facilities and Maintenance | Executive General and Administration | 2008-04-30 00:00:00.000 |
| 1 5 | Shipping and Receiving | Inventory Management | 2008-04-30 00:00:00.000 |
| 1 6 | Executive | Executive General and Administration | 2008-04-30 00:00:00.000 |
| 1 7 | Privacy | Executive General and Administration | 2021-11-17 12:42:54.640 |

Expand

Show lessSee more

##### Snowflake Scripting

Copy code

```
 CALL AddPrivacyDepartment();

SELECT
DepartmentID,
Name,
GroupName
FROM
HumanResources.Department;
```

##### Result

| DEPARTMENTID | NAME | GROUPNAME | MODIFIEDDATE |
| --- | --- | --- | --- |
| 1 | Engineering | Research and Development | 2021-11-17 10:29:36.963 |
| 2 | Tool Design | Research and Development | 2021-11-17 10:29:37.463 |
| 3 | Sales | Sales and Marketing | 2021-11-17 10:29:38.192 |
| 4 | Marketing | Sales and Marketing | 2021-11-17 10:29:38.733 |
| 5 | Purchasing | Inventory Management | 2021-11-17 10:29:39.298 |
| 6 | Research and Development | Research and Development | 2021-11-17 10:31:53.770 |
| 7 | Production | Manufacturing | 2021-11-17 10:31:55.082 |
| 8 | Production Control | Manufacturing | 2021-11-17 10:31:56.638 |
| 9 | Human Resources | Executive General and Administration | 2021-11-17 10:31:57.507 |
| 10 | Finance | Executive General and Administration | 2021-11-17 10:31:58.473 |
| 11 | Information Services | Executive General and Administration | 2021-11-17 10:34:35.200 |
| 12 | Document Control | Quality Assurance | 2021-11-17 10:34:35.741 |
| 13 | Quality Assurance | Quality Assurance | 2021-11-17 10:34:36.277 |
| 14 | Facilities and Maintenance | Executive General and Administration | 2021-11-17 10:34:36.832 |
| 15 | Shipping and Receiving | Inventory Management | 2021-11-17 10:34:37.373 |
| 16 | Executive | Executive General and Administration | 2021-11-17 10:34:37.918 |
| 17 | Privacy | Executive General and Administration | 2021-11-17 10:46:43.345 |

Expand

Show lessSee more

#### Execution of local variable and use of parameters

A common use case for the EXECUTE statement is when dynamic SQL statements are needed. In this cases instead of executing a string literal, the statement could be constructed dynamically and assigned to a local variable, which will then be executed. A set of arguments can be sent to the called stored procedure to construct the dynamic SQL command.

In the following example a simple SetNewPrice stored procedure is constructed, which uses the EXECUTE statement to set a new product price based on the arguments sent by the caller. Lastly a SELECT is performed to confirm the new product price.

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE SetNewPrice @ProductID INT, @NewPrice MONEY
AS
  DECLARE @dynSqlStatement AS VARCHAR(300);
  SET @dynSqlStatement = 'UPDATE Production.ProductListPriceHistory SET ListPrice = ' + CAST(@NewPrice AS VARCHAR(10)) + ' WHERE ProductID = ' + CAST(@ProductID AS VARCHAR(10)) + ' AND EndDate IS NULL';
  EXECUTE (@dynSqlStatement);
GO

EXECUTE Set_New_Price @ProductID = 707, @NewPrice = 34.99;
SELECT ListPrice FROM Production.ProductListPriceHistory WHERE ProductID = 707 AND EndDate IS NULL;
```

##### Result

| ListPrice |
| --- |
| 34.9900 |

Expand

Show lessSee more

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE SetNewPrice (PRODUCTID INT, NEWPRICE NUMBER(38, 4))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    DYNSQLSTATEMENT VARCHAR(300);
  BEGIN

    DYNSQLSTATEMENT := 'UPDATE Production.ProductListPriceHistory
   SET
      ListPrice = ' || CAST(:NEWPRICE AS VARCHAR(10)) || '
   WHERE
      ProductID = ' || CAST(:PRODUCTID AS VARCHAR(10)) || '
      AND EndDate IS NULL;';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :DYNSQLSTATEMENT;
  END;
$$;

CALL Set_New_Price(707, 34.99);

SELECT
  ListPrice
FROM
  Production.ProductListPriceHistory
WHERE
  ProductID = 707 AND EndDate IS NULL;
```

##### Result

| LISTPRICE |
| --- |
| 34.9900 |

Expand

Show lessSee more

### Known Issues

#### Using return codes

Transact-SQL EXECUTE syntax contains the @return\_status optional argument, which allows creating a scalar variable to store the return status of a scalar-valued user defined function.

It can also be used in stored procedures although the returning status will be limited to integer data type.

To represent this functionality, we could slightly modify the above example and create a user defined function to calculate the new product price as an average of the historical prices. Instead of passing it to the stored procedure, we could now call the CalculateAveragePrice function to obtain the new price, and store it in the return variable to construct the dynamic SQL.

##### Transact-SQL

##### Execute

Copy code

```
CREATE OR ALTER FUNCTION CalculateAveragePrice(@pid INT)
RETURNS MONEY
AS
BEGIN
  DECLARE @average AS MONEY;
  SELECT @average = AVG(LISTPRICE) FROM Production.ProductListPriceHistory WHERE ProductID = @pid;
  RETURN @average;
END;
GO

CREATE OR ALTER PROCEDURE SetNewPrice @ProductID INT
AS
  DECLARE @averageHistoricalPrice MONEY;
  EXECUTE @averageHistoricalPrice = [dbo].Calculate_Average_Price @pid=@ProductID;
  UPDATE Production.ProductListPriceHistory SET ListPrice = @averageHistoricalPrice WHERE ProductID =  @ProductID AND EndDate IS NULL;
GO

EXECUTE Set_New_Price @ProductID = 707;
SELECT ListPrice FROM Production.ProductListPriceHistory WHERE ProductID = 707 AND EndDate IS NULL;
```

##### Result

| ListPrice |
| --- |
| 34.0928 |

Expand

Show lessSee more

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE FUNCTION CalculateAveragePrice (PID INT)
RETURNS NUMBER(38, 4)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
  WITH CTE1 AS
  (
    SELECT
      AVG(LISTPRICE) AS AVERAGE FROM
      Production.ProductListPriceHistory
    WHERE
      ProductID = PID
  )
  SELECT
    AVERAGE
  FROM
    CTE1
$$;

CREATE OR REPLACE PROCEDURE SetNewPrice (PRODUCTID INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    AVERAGEHISTORICALPRICE NUMBER(38, 4);
  BEGIN

    CALL dbo.Calculate_Average_Price(:PRODUCTID);
    UPDATE Production.ProductListPriceHistory
      SET
        ListPrice = :AVERAGEHISTORICALPRICE
      WHERE
        ProductID = :PRODUCTID
        AND EndDate IS NULL;
  END;
$$;

CALL Set_New_Price(707);

SELECT
  ListPrice
FROM
  Production.ProductListPriceHistory
WHERE
  ProductID = 707 AND EndDate IS NULL;
```

#### Unsupported Optional arguments

- @return\_status
- ;number
- @module\_\_name\_v\_ar
- WITH RECOMPILE, WITH RESULT SETS NONE, WITH &lt;result set definition>

### Related EWIs

1. [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030): The statement below has usages of dynamic SQL.

## IF

Translation reference to convert Transact-SQL IF..ELSE clauses to Snowflake Scripting

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The IF clause allows an SQL statement or a block of statements to be conditionally executed as long as the Boolean expression is true; otherwise, the statements in the optional ELSE clause will be executed. Transact-SQL also supports embedding multiple IF… ELSE clauses in case multiple conditions are required, or the CASE clause can also be used.

For more information, see the [Transact-SQL IF…ELSE documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/if-else-transact-sql?view=sql-server-ver15).

Copy code

```
 IF Boolean_expression
     { sql_statement | statement_block }
[ ELSE
     { sql_statement | statement_block } ]
```

Note: To define a statement block, use the control-of-flow keywords `BEGIN` and `END`.

### Sample Source Patterns

#### Transact-SQL

The following code refers to an IF… ELSE in Transact-SQL that conditions the variable @value to identify if it is less than 5, if it is between 5 and 10, or if it has any other value. Since @value is initialized as 7, the second condition must be true and the result must be 200.

##### IF…ELSE

Copy code

```
CREATE OR ALTER PROCEDURE IfElseDemoProcedure
AS
    DECLARE @value INT;
    SET @value = 7;

    IF @value < 5
        SET @value = 100;
    ELSE IF @value >= 5 AND @value < 10
        BEGIN
            SET @value = 300;
            SET @value = @value - 100;
        END;
    ELSE
        SET @value = -1;

    RETURN @value
GO

DECLARE @result INT;
EXEC @result = IfElseDemoProcedure;
PRINT @result;
```

##### Result

| result |
| --- |
| 200 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

Notice that in Snowflake Scripting, the embedded IF… ELSE condition is called ELSEIF.

Besides, the Boolean condition is encapsulated in parentheses and the clause always ends with the END IF expression.

In addition, in Snowflake Scripting it is not necessary to use the BEGIN and END keywords to define a statement block, however it can be used if required.

##### IF…ELSE

Copy code

```
CREATE OR REPLACE PROCEDURE IfElseDemoProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        VALUE INT;
    BEGIN

        VALUE := 7;
        IF (:VALUE < 5) THEN
            VALUE := 100;
        ELSEIF (:VALUE >= 5 AND :VALUE < 10) THEN
            BEGIN
                VALUE := 300;
                VALUE := :VALUE - 100;
            END;
        ELSE
            VALUE := -1;
        END IF;
        RETURN :VALUE;
    END;
$$;

DECLARE
    RESULT INT;
BEGIN
    CALL IfElseDemoProcedure();
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Print' NODE ***/!!!
    PRINT @result;
END;
```

##### Result

| result |
| --- |
| 200 |

Expand

Show lessSee more

#### IF statement outside routines (functions and procedures)

Unlike Transact-SQL, Snowflake does not support executing isolated statements like IF…ELSE outside routines like functions or procedures. For this scenario, the statement should be encapsulated in an anonymous block, as shown in the following example.
You can read more about how to correctly return the output values in the [SELECT section](./transact-select).

##### Transact-SQL

Copy code

```
DECLARE @maxWeight FLOAT, @productKey INTEGER
SET @maxWeight = 100.00
SET @productKey = 424
IF @maxWeight <= 99
    SELECT @productKey,  'This product is too heavy to ship and is only available for pickup.'
ELSE
    SELECT @productKey, 'This product is available for shipping or pickup.'
```

##### Snowflake Scripting

Copy code

```
DECLARE
    MAXWEIGHT FLOAT;
    PRODUCTKEY INTEGER;
    BlockResultSet1 VARCHAR;
    BlockResultSet2 VARCHAR;
    return_arr ARRAY := array_construct();
BEGIN
    MAXWEIGHT := 100.00;
    PRODUCTKEY := 424;
    IF (:MAXWEIGHT <= 99) THEN
        BlockResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
        CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:BlockResultSet1) AS
            SELECT
                :PRODUCTKEY,  'This product is too heavy to ship and is only available for pickup.';
        return_arr := array_append(return_arr, :BlockResultSet1);
    ELSE
        BlockResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
        CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:BlockResultSet2) AS
            SELECT
                :PRODUCTKEY, 'This product is available for shipping or pickup.';
        return_arr := array_append(return_arr, :BlockResultSet2);
    END IF;
    --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
    RETURN return_arr;
END;
```

### Related EWIs

1. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables.

## LABEL and GOTO

Translation reference for LABEL and GOTO statements in Transact-SQL.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

T-SQL supports `GOTO` for unconditional jumps to labeled statements within a procedure. Snowflake Scripting does not support `GOTO` or labeled jump targets natively.

When GOTO/Label patterns appear inside a stored procedure with **forward-only** jumps to **top-level** labels, they are automatically transformed using a **nested procedure decomposition** approach. The procedure body is split into sections at each label declaration, and each section becomes its own nested procedure — code before the first label is placed in a nested procedure called `SC_PROCESS`, while each labeled section becomes a nested procedure named after its label. Every `GOTO label` is then replaced with `CALL label(); RETURN 'PROCESS FINISHED';`, which transfers control to the target section and exits the current one. To preserve sequential execution when no `GOTO` is taken, each section automatically calls the next one at its end (fall-through). All local variable declarations are moved up to the parent procedure’s `DECLARE` block so that every nested procedure can access them through Snowflake’s lexical scoping. Any `RETURN @value` inside a label section is translated to an assignment `SC_EXIT_CODE := :expr;`, and the outer procedure body simply calls `SC_PROCESS()` and then returns the exit code.

When the pattern **cannot** be transformed, the original `GOTO` and label statements are preserved with EWI markers. This happens with **backward GOTOs** (where the target label appears before the GOTO in source order, which would require recursive nested calls), **GOTO/Label in anonymous blocks or UDFs** (which do not support nested procedure definitions), and **labels inside nested control flow** such as `IF`, `WHILE`, or `TRY` blocks (which cannot be extracted into top-level nested procedures).

### Sample Source Patterns

#### Forward GOTO with single label (transformed)

A common T-SQL pattern uses `GOTO` to skip to a cleanup or exit section when an error is detected. This is transformed by wrapping the main logic and the cleanup label into separate nested procedures.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE dbo.ValidateOrderInput
AS
BEGIN
    DECLARE @ErrorCode INT = 0
    IF @ErrorCode = 0
    BEGIN
        SET @ErrorCode = 1
        GOTO Cleanup
    END
    SET @ErrorCode = -1
Cleanup:
    RETURN @ErrorCode
END
```

##### Snowflake SQL

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.ValidateOrderInput ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SC_EXIT_CODE VARCHAR;
    ERRORCODE INT := 0;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        IF (:ERRORCODE = 0) THEN
          BEGIN
            ERRORCODE := 1;
            BEGIN
              CALL Cleanup();
              RETURN 'PROCESS FINISHED';
            END;
          END;
        END IF;
        ERRORCODE := -1;
        CALL Cleanup();
      END;
    Cleanup PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        SC_EXIT_CODE := :ERRORCODE;
      END;
  BEGIN
    CALL SC_PROCESS();
    RETURN :SC_EXIT_CODE;
  END;
$$;
```

#### Multiple labels with fall-through (transformed)

When a procedure has multiple labeled sections, sequential fall-through is preserved by having each nested procedure call the next one at its end. A `GOTO` can also skip ahead to any label, bypassing intermediate sections.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE dbo.ProcessShipment @Status VARCHAR(100) OUTPUT
AS
BEGIN
    SET @Status = 'Received'
    IF @Status = 'skip' GOTO Ship
Validate:
    SET @Status = 'Validated'
Pack:
    SET @Status = 'Packed'
Ship:
    SET @Status = 'Shipped'
    RETURN 0
END
```

##### Snowflake SQL

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.ProcessShipment (STATUS OUT STRING)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SC_EXIT_CODE VARCHAR;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        STATUS := 'Received';
        IF (:STATUS = 'skip') THEN
          BEGIN
            CALL Ship();
            RETURN 'PROCESS FINISHED';
          END;
        END IF;
        CALL Validate();
      END;
    Validate PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        STATUS := 'Validated';
        CALL Pack();
      END;
    Pack PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        STATUS := 'Packed';
        CALL Ship();
      END;
    Ship PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        STATUS := 'Shipped';
        SC_EXIT_CODE := 0;
      END;
  BEGIN
    CALL SC_PROCESS();
    RETURN :SC_EXIT_CODE;
  END;
$$;
```

#### GOTO inside nested IF (transformed)

`GOTO` statements inside nested `IF` or `BEGIN...END` blocks are also transformed. The `CALL`/`RETURN` pair exits from any depth of nesting, effectively reproducing the jump-out behavior of the original `GOTO`.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE dbo.ApproveExpenseReport @ManagerApproved INT, @BudgetAvailable INT
AS
BEGIN
    DECLARE @ApprovalStatus INT = 0
    IF @ManagerApproved = 1
    BEGIN
        IF @BudgetAvailable = 1
            GOTO Finalize
        SET @ApprovalStatus = 1
    END
    SET @ApprovalStatus = 2
Finalize:
    RETURN 0
END
```

##### Snowflake SQL

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.ApproveExpenseReport (MANAGERAPPROVED INT, BUDGETAVAILABLE INT)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SC_EXIT_CODE VARCHAR;
    APPROVALSTATUS INT := 0;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        IF (:MANAGERAPPROVED = 1) THEN
          BEGIN
            IF (:BUDGETAVAILABLE = 1) THEN
              BEGIN
                CALL Finalize();
                RETURN 'PROCESS FINISHED';
              END;
            END IF;
            APPROVALSTATUS := 1;
          END;
        END IF;
        APPROVALSTATUS := 2;
        CALL Finalize();
      END;
    Finalize PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        SC_EXIT_CODE := 0;
      END;
  BEGIN
    CALL SC_PROCESS();
    RETURN :SC_EXIT_CODE;
  END;
$$;
```

#### Backward GOTO — not transformed (EWI kept)

When a `GOTO` targets a label that appears *before* the `GOTO` in the source (a backward jump), the nested procedure decomposition cannot be applied because it would require recursive calls, which Snowflake does not support for nested procedures. In these cases, the `GOTO` and label are preserved with EWI markers for manual resolution.

##### Transact-SQL

Copy code

```
CREATE PROCEDURE dbo.RetryDatabaseConnection
AS
BEGIN
    DECLARE @Attempts INT = 0
RetryConnection:
    SET @Attempts = @Attempts + 1
    IF @Attempts < 3
        GOTO RetryConnection
    RETURN 0
END
```

##### Snowflake SQL

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.RetryDatabaseConnection ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ATTEMPTS INT := 0;
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0045 - LABELED STATEMENT IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
    RetryConnection:
    ATTEMPTS := :ATTEMPTS + 1;
    IF (:ATTEMPTS < 3) THEN
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0087 - GOTO IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
      GOTO RetryConnection
    END IF;
    RETURN 0;
  END;
$$;
```

#### LABEL and GOTO outside stored procedures (not transformed)

When `GOTO` and labels appear in batch scripts outside of a stored procedure, the nested procedure decomposition cannot be applied because Snowflake anonymous blocks do not support nested procedure definitions. The statements are preserved with EWI markers.

##### Transact-SQL

Copy code

```
CREATE TABLE AuditLog(EventID INT);
GOTO InsertSecond
InsertFirst:
    INSERT INTO AuditLog VALUES (1);
InsertSecond:
    INSERT INTO AuditLog VALUES (2);
```

##### Snowflake Scripting

Copy code

```
BEGIN
    CREATE OR REPLACE TABLE AuditLog (
        EventID INT
    );
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0087 - GOTO IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
    GOTO InsertSecond;
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0045 - LABELED STATEMENT IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
    InsertFirst:
    INSERT INTO AuditLog VALUES (1);

    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0045 - LABELED STATEMENT IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
    InsertSecond:
    INSERT INTO AuditLog VALUES (2);
END;
```

### Related EWIs

1. [SSC-EWI-TS0045](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0045): Labeled Statement is not supported in Snowflake Scripting.
2. [SSC-EWI-TS0087](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0087): GOTO is not supported in Snowflake.
3. [SSC-EWI-TS0103](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0103): GOTO targeting a label inside a nested block is not supported in Snowflake.
4. [SSC-FDM-TS0055](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0055): Label statement commented out (no GOTO references the label).

## OUTPUT PARAMETERS

This article is about the current transformation of the output parameters and how their functionality is being emulated.

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

An **output parameter** is a parameter whose value is passed out of the stored procedure, back to the calling SQL block. Since the output parameters are not supported by Snowflake Scripting, a solution has been implemented to emulate their functionality.

### Sample Source Patterns

#### Single OUT parameter

The most basic scenario for OUT parameters is when the procedure only has one. In this case, we simply return the OUT parameter at the end of the procedure body.

The EXEC procedure has to be translated as well, for this a CALL is created, the parameters are passed without any modifier (“OUT” is removed), and subsequently, an assignment is done so the parameter is associated with it’s respective resulting value.

##### Transact-SQL

Copy code

```
 -- Procedure with output parameter
CREATE PROCEDURE dbo.outmain
@name VARCHAR (255) OUTPUT
AS
SET @name = 'Jane';

GO

-- Auxiliary procedure that calls the main procedure
CREATE PROCEDURE dbo.outaux
AS
DECLARE @name VARCHAR (255);
EXEC dbo.outmain
    @name = @name OUTPUT;
```

##### Snowflake Scripting

Copy code

```
 -- Procedure with output parameter
CREATE OR REPLACE PROCEDURE dbo.outmain (NAME OUT STRING)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NAME := 'Jane';
    END;
$$;

-- Auxiliary procedure that calls the main procedure
CREATE OR REPLACE PROCEDURE dbo.outaux ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        NAME VARCHAR(255);
    BEGIN

        CALL dbo.outmain(:NAME);
    END;
$$;
```

#### Multiple OUT parameters

When more than one OUT parameters are found, the RETURNS clause of the procedure changes to VARIANT. This is to accommodate the OBJECT\_CONSTRUCT that is going to be used to store the values of the OUT parameters.

On top of that, a RETURN statement is added to the end of the procedure’s body. This is where the OBJECT\_COSNTRUCT is created and all the OUT parameter values are stored within it. This object will then be used by the caller to assign the parameters value to the corresponding result.

##### Transact-SQL

Copy code

```
CREATE OR ALTER PROCEDURE basicProc (
    @col1 INT OUT,
    @col2 VARCHAR(10) OUT
) AS
BEGIN
    SET @col1 = 4;
    SET @col2 = 'test';
END;

GO

CREATE OR ALTER PROCEDURE basicProcCall AS
BEGIN
    DECLARE @var1 INT = 0;
    DECLARE @var2 VARCHAR(10) = 'EMPTY';

    EXEC basicProc @var1 OUT, @var2 OUT;
    INSERT INTO TABLE1(col1, col2) VALUES (@var1, @var2);
END;

GO

EXEC basicProcCall;
```

##### Snowflake Scripting

Copy code

```
CREATE OR REPLACE PROCEDURE basicProc (COL1 OUT INT, COL2 OUT STRING)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        COL1 := 4;
        COL2 := 'test';
    END;
$$;

CREATE OR REPLACE PROCEDURE basicProcCall ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        VAR1 INT := 0;
        VAR2 VARCHAR(10) := 'EMPTY';
    BEGIN

        CALL basicProc(:VAR1, :VAR2);
        INSERT INTO TABLE1 (col1, col2) VALUES (:VAR1, :VAR2);
    END;
$$;

CALL basicProcCall();
```

#### OUT parameters and return values

Transact-SQL allows procedures to have return values. When a procedure has both a return value and OUT parameter(s), a similar approach to the [Multiple OUT parameters](#multiple-out-parameters) scenario is followed. The original return value is treated as an OUT parameter would be treated, so it’s stored within the OBJECT\_CONSTRUCT and extracted inside the caller procedure.

##### Transact-SQL

Copy code

```
 -- Procedure with multiple output parameters
CREATE PROCEDURE dbo.outmain
@name VARCHAR (255) OUTPUT
AS
SET @name = 'Jane';
RETURN 0;

GO

-- Auxiliary procedure that calls the main procedure
CREATE PROCEDURE dbo.outaux
AS
DECLARE @name VARCHAR (255);
DECLARE @returnValue INT;
EXEC @returnValue = dbo.outmain
    @name = @name OUTPUT;
```

##### Snowflake Scripting

##### Query

Copy code

```
 -- Procedure with multiple output parameters
CREATE OR REPLACE PROCEDURE dbo.outmain (NAME OUT STRING)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NAME := 'Jane';
        RETURN 0;
    END;
$$;

-- Auxiliary procedure that calls the main procedure
CREATE OR REPLACE PROCEDURE dbo.outaux ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        NAME VARCHAR(255);
        RETURNVALUE INT;
    BEGIN

        CALL dbo.outmain(:NAME);
    END;
$$;
```

#### Customer data type OUT parameters

when the output parameter is a custom type, the process is similar to a regular data type.

##### Transact-SQL

Copy code

```
 CREATE PROCEDURE procedure_udtype_out_params(
  @p_employee_id INT,
  @p_phone [dbo].[PhoneNumber] OUTPUT
) AS
BEGIN
  SELECT @p_phone = phone
  FROM employees
  WHERE employee_id = @p_employee_id;
END;
```

##### Snowflake Scripting

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "[dbo].[PhoneNumber]", "employees" **
CREATE OR REPLACE PROCEDURE procedure_udtype_out_params (P_EMPLOYEE_ID INT, P_PHONE OUT VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE DBO.PHONENUMBER IS NOT SUPPORTED IN SNOWFLAKE ***/!!! NOT NULL)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    SELECT
      phone
    INTO
      :P_PHONE
    FROM
      employees
    WHERE
      employee_id = :P_EMPLOYEE_ID;
  END;
$$;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-EWI-TS0015](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0015): Data type is not supported in Snowflake.

## SET

Translation reference to convert Transact-SQL SET statement to Snowflake

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Sets the specified local variable, previously created by using the DECLARE @*local\_variable* statement, to the specified value. For more information, see the [Transact-SQL SET documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/set-local-variable-transact-sql?view=sql-server-ver15).

There are four SET cases that are the following:

Copy code

```
SET
{ @local_variable
    [ . { property_name | field_name } ] = { expression | udt_name { . | :: } method_name }
}
|
{ @SQLCLR_local_variable.mutator_method
}
|
{ @local_variable
    {+= | -= | *= | /= | %= | &= | ^= | |= } expression
}
|
  { @cursor_variable =
    { @cursor_variable | cursor_name
    | { CURSOR [ FORWARD_ONLY | SCROLL ]
        [ STATIC | KEYSET | DYNAMIC | FAST_FORWARD ]
        [ READ_ONLY | SCROLL_LOCKS | OPTIMISTIC ]
        [ TYPE_WARNING ]
    FOR select_statement
        [ FOR { READ ONLY | UPDATE [ OF column_name [ ,...n ] ] } ]
      }
    }
}
```

### Sample Source Patterns

#### Transact-SQL

##### Case 1

Copy code

```
CREATE OR ALTER PROCEDURE SetProcedure
AS
    DECLARE @MyCounter INT;
    DECLARE @FloatCounter FLOAT;

    --Numerical operators
    SET @MyCounter = 3;
    SET @MyCounter += 1;  --@MyCounter has 4
    SET @MyCounter -= 1;  --@MyCounter has 3
    SET @MyCounter *= 2;  --@MyCounter has 6

    SET @MyCounter /= 3;  --@MyCounter has 2
    SET @MyCounter = 6;
    SET @MyCounter /= 5;  --@MyCounter has 1
    SET @MyCounter = 6;
    SET @MyCounter /= 7;  --@MyCounter has 0
    SET @FloatCounter = 10;
    SET @FloatCounter /= 4;  --@FloatCounter has 2.5

    SET @MyCounter = 6;
    SET @MyCounter %= 4;  --@MyCounter has 2

    --Logical operators
    SET @MyCounter &= 3;  --@MyCounter has 2
    SET @MyCounter ^= 2;  --@MyCounter has 0
    SET @MyCounter |= 0;  --@MyCounter has 0

    RETURN @MyCounter;
GO

DECLARE @result INT;
EXEC @result = SetProcedure;
PRINT @result;
```

##### Case 2

Copy code

```
CREATE TABLE vEmployee (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255)
);

CREATE OR ALTER PROCEDURE SetCursor
AS
    DECLARE @CursorVar CURSOR;

    SET @CursorVar = CURSOR SCROLL DYNAMIC
        FOR
	SELECT LastName, FirstName
	FROM vEmployee
	WHERE LastName like 'B%';
GO
```

##### Result 1

| Result |
| --- |
| 0 |

Expand

Show lessSee more

##### Snowflake Scripting

##### Case 1

Copy code

```
CREATE OR REPLACE PROCEDURE SetProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        MYCOUNTER INT;
        FLOATCOUNTER FLOAT;
    BEGIN

        --Numerical operators
        MYCOUNTER := 3;
        MYCOUNTER := MYCOUNTER + 1;  --@MyCounter has 4

        MYCOUNTER := MYCOUNTER - 1;  --@MyCounter has 3

        MYCOUNTER := MYCOUNTER * 2;  --@MyCounter has 6

        MYCOUNTER := MYCOUNTER / 3;  --@MyCounter has 2

        MYCOUNTER := 6;
        MYCOUNTER := MYCOUNTER / 5;  --@MyCounter has 1

        MYCOUNTER := 6;
        MYCOUNTER := MYCOUNTER / 7;  --@MyCounter has 0

        FLOATCOUNTER := 10;
        FLOATCOUNTER := FLOATCOUNTER / 4;  --@FloatCounter has 2.5

        MYCOUNTER := 6;
        MYCOUNTER := MYCOUNTER % 4;  --@MyCounter has 2

    --Logical operators
        MYCOUNTER := BITAND(MYCOUNTER, 3);  --@MyCounter has 2

        MYCOUNTER := BITXOR(MYCOUNTER, 2);  --@MyCounter has 0

        MYCOUNTER := BITOR(MYCOUNTER, 0);  --@MyCounter has 0

        RETURN :MYCOUNTER;
    END;
$$;

DECLARE
    RESULT INT;
BEGIN
    CALL SetProcedure();
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Print' NODE ***/!!!
    PRINT @result;
END;
```

##### Case 2

Copy code

```
CREATE OR REPLACE TABLE vEmployee (
	PersonID INT,
	LastName VARCHAR(255),
	FirstName VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

CREATE OR REPLACE PROCEDURE SetCursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		!!!RESOLVE EWI!!! /*** SSC-EWI-TS0037 - SNOWFLAKE SCRIPTING CURSORS ARE NON-SCROLLABLE, ONLY FETCH NEXT IS SUPPORTED ***/!!!
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CURSORVAR CURSOR
		FOR
			SELECT LastName, FirstName
			FROM vEmployee
			WHERE LastName like 'B%';
	BEGIN

		RETURN '';
	END;
$$;
```

##### Result 1

| Result |
| --- |
| 0 |

Expand

Show lessSee more

#### SET statement outside routines (functions and procedures)

Unlike Transact-SQL, Snowflake does not support executing isolated statements like SET outside routines like functions or procedures. For this scenario, the statement should be encapsulated in an anonymous block, as shown in the following examples. This statement is usually used after a [DECLARE STATEMENT](#declare).

##### Transact-SQL

Copy code

```
DECLARE @Group nvarchar(50), @Sales MONEY;
SET @Group = N'North America';
SET @Sales = 2000000;
```

##### Snowflake Scripting

Copy code

```
DECLARE
    _GROUP VARCHAR(50);
    SALES NUMBER(38, 4);
BEGIN
    _GROUP := 'North America';
    SALES := 2000000;
END;
```

If there is a scenario with only SET statements, the DECLARE block is not necessary. Probably this scenario will produce runtime errors if there is an attempt of setting a value to a variable that is not declared.

##### Transact-SQL

Copy code

```
SET @Group = N'North America';
```

##### Snowflake Scripting

Copy code

```
BEGIN
    _GROUP := 'North America';
END;
```

### Known Issues

#### 1. SET of a local variable with property name

This type of set is not currently supported by Snowflake scripting.

Copy code

```
 // TSQL custom data type with properties example
DECLARE @p Point;
SET @p.X = @p.X + 1.1;
```

##### 2. SET of a local variable with mutator method

This type of set is not currently supported by Snowflake scripting.

Copy code

```
 // TSQL custom data type with mutator method
SET @p.SetXY(22, 23);
```

### Related EWIs

1. [SSC-EWI-TS0037](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0037): Snowflake Scripting Cursors are non-scrollable.
2. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
3. [SSC-FDM-TS0013](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0013): Snowflake Scripting cursor rows are not modifiable.

## TRY CATCH

Translation reference for TRY CATCH statement in Transact-SQL.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Implements error handling for Transact SQL. A group of Transact-SQL statements can be enclosed in a TRY block. If an error occurs in the TRY block, control is usually passed to another group of statements that is enclosed in a CATCH block.

### Sample Source Patterns

The following example details the transformation for TRY CATCH inside procedures.

#### Transact-SQL

Copy code

```
CREATE PROCEDURE ERROR_HANDLING_PROC
AS
BEGIN
    BEGIN TRY
        -- Generate divide-by-zero error.
        SELECT 1/0;
    END TRY
    BEGIN CATCH
        -- Execute error retrieval routine.
        SELECT 'error';
    END CATCH;
END;
```

#### Output

Copy code

```
|   error    |
```

##### Snowflake SQL

Copy code

```
CREATE OR REPLACE PROCEDURE ERROR_HANDLING_PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        BEGIN
            -- Generate divide-by-zero error.
            SELECT
                TRUNC( 1/0);
        EXCEPTION
            WHEN OTHER THEN
                -- Execute error retrieval routine.
                SELECT 'error';
        END;
    END;
$$;
```

##### Output

Copy code

```
|    error    |
```

#### Try catch outside routines (functions and procedures)

##### Transact-SQL

Copy code

```
 BEGIN TRY
    SELECT 1/0;
END TRY
BEGIN CATCH
    SELECT 'error';
END CATCH;
```

##### Snowflake Scripting

Copy code

```
DECLARE
    BlockResultSet1 VARCHAR;
    BlockResultSet2 VARCHAR;
    return_arr ARRAY := array_construct();
BEGIN
    BEGIN
        BlockResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
        CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:BlockResultSet1) AS
            SELECT
                TRUNC( 1/0);
        return_arr := array_append(return_arr, :BlockResultSet1);
    EXCEPTION
        WHEN OTHER THEN
            BlockResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
            CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:BlockResultSet2) AS
                SELECT 'error';
            return_arr := array_append(return_arr, :BlockResultSet2);
    END;
    --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
    RETURN return_arr;
END;
```

### Related EWIs

1. [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables.

## WHILE

Translation reference to convert Transact-SQL While Statement to Snowflake Scripting

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The While statement allows an SQL statement or a block of statements to be repeatedly executed as long as the specified condition is true. The execution of statements in the WHILE loop can be controlled from inside the loop with the `BREAK` and `CONTINUE` keywords.

For more information, see the [Transact-SQL WHILE documentation](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/while-transact-sql?view=sql-server-ver15).

Copy code

```
 WHILE Boolean_expression
     { sql_statement | statement_block | BREAK | CONTINUE }
```

Note: To define a statement block, use the control-of-flow keywords `BEGIN` and `END`.

### Sample Source Patterns

#### Basic source pattern code

##### Transact-SQL

The following code refers to a While Loop in Transact-SQL that iterates the @Iteration variable and controls the flow of the loop to terminate when the value of @Iteration equals 10.

Note

Statements after the `CONTINUE` keyword will not be executed.

##### While

Copy code

```
CREATE OR ALTER PROCEDURE WhileDemoProcedure
AS
    DECLARE @iteration INT;
    SET @iteration = 1;

    WHILE @iteration < 100
    BEGIN
        IF @iteration = 10
            BREAK;
        ELSE
            BEGIN
                SET @iteration = @iteration + 1;
                CONTINUE;
                SET @iteration = 2 * @iteration;
            END;
    END;
    RETURN @iteration;
GO

DECLARE @result INT;
EXEC @result = WhileDemoProcedure;
PRINT @result;
```

##### Result

| iteration |
| --- |
| 10 |

Expand

Show lessSee more

##### Snowflake Scripting

Note

As well as Transact-SQL, in Snowflake Scripting the statements after the `CONTINUE` keyword will not be executed.

Notice that in Snowflake Scripting it is not necessary to use the BEGIN and END keywords to define a statement block, however it can be used if required.

##### While

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE WhileDemoProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ITERATION INT;
    BEGIN

        ITERATION := 1;
        WHILE (:ITERATION &#x3C; 100) LOOP
            IF (:ITERATION = 10) THEN
                BREAK;
            ELSE
                BEGIN
                    ITERATION := :ITERATION + 1;
                    CONTINUE;
                    ITERATION := 2 * :ITERATION;
                END;
            END IF;
        END LOOP;
        RETURN :ITERATION;
    END;
$$;

DECLARE
    RESULT INT;
BEGIN
    CALL WhileDemoProcedure();
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Print' NODE ***/!!!
    PRINT @result;
END;
```

##### Loop keyword

Snowflake Scripting allows to use `LOOP` keyword instead of `DO` and the `END LOOP` expression instead of `END WHILE` .

Copy code

```
WHILE (Boolean_expression) LOOP
    -- statement or statement block
END LOOP;
```

##### Result

| Iteration |
| --- |
| 10 |

Expand

Show lessSee more

#### While with empty body Source Pattern

##### Transact-SQL

Note

Please note this example was written while the IF ELSE statement was not supported, the differences in the results should disappear when support for the statement is implemented.

Copy code

```
CREATE OR ALTER PROCEDURE WhileEmptyBodyProc
AS
BEGIN
    DECLARE @MyVar INT;
    SET @MyVar = 1;
    WHILE (@MyVar < 100)
        BEGIN
            IF @MyVar < 50
                SET @MyVar *= 5;
            ELSE
                SET @MyVar *= 3;
        END;
    RETURN @MyVar;
END;

DECLARE @result INT;
EXEC @result = WhileEmptyBodyProc;
PRINT @result;
```

##### Result

| result |
| --- |
| 125 |

Expand

Show lessSee more

##### Snowflake Scripting

This statement can not have an empty body in Snowflake Scripting, to solve this cases a default BREAK statement is added when an empty body is detected.

Copy code

```
CREATE OR REPLACE PROCEDURE WhileEmptyBodyProc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        MYVAR INT;
        RESULT INT;
    BEGIN
        BEGIN

            MYVAR := 1;
            WHILE (:MYVAR < 100) LOOP
                IF (:MYVAR < 50) THEN
                    MYVAR := MYVAR * 5;
                ELSE
                    MYVAR := MYVAR * 3;
                END IF;
            END LOOP;
            RETURN :MYVAR;
        END;

        CALL WhileEmptyBodyProc();
        !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PRINT' NODE ***/!!!
        PRINT @result;
    END;
$$;
```

##### Result

| result |
| --- |
| 1 |

Expand

Show lessSee more

#### WHILE statement outside routines (functions and procedures)

Unlike Transact-SQL, Snowflake does not support executing isolated statements like WHILE outside routines like functions or procedures. For this scenario, the statement should be encapsulated in an anonymous block, as shown in the following example.

##### Transact-SQL

Copy code

```
DECLARE @iteration INT;
SET @iteration = 1;

WHILE @iteration < 100
BEGIN
    IF @iteration = 10
        BREAK;
    ELSE
        BEGIN
            SET @iteration = @iteration + 1;
            CONTINUE;
            SET @iteration = 2 * @iteration;
        END;
    END;
```

##### Snowflake Scripting

Copy code

```
DECLARE
    ITERATION INT;
BEGIN
    ITERATION := 1;
    WHILE (:ITERATION < 100) LOOP
        IF (:ITERATION = 10) THEN
            BREAK;
        ELSE
            BEGIN
                ITERATION := :ITERATION + 1;
                CONTINUE;
                ITERATION := 2 * :ITERATION;
            END;
        END IF;
    END LOOP;
END;
```

### Related EWIs

1. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
