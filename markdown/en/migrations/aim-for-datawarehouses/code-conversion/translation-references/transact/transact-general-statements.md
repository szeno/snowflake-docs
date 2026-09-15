# SQL Server-Azure Synapse - General Language Elements

In this section you could find information about general statements of Transact-SQL.

## COLLATE

Applies to

- SQL Server
- Azure Synapse Analytics

The transformation of the collate depends on its value, since it can be supported or not supported.

Currently, these are the languages that are supported for the transformation, if they are found in the collate, they will be transformed into its Snowflake equivalent.

| SQL Server | Snowflake |
| --- | --- |
| Latin1\_General | EN |
| Modern\_Spanish | ES |
| French | FR |

Expand

Show lessSee more

If the language is not one of the above, the collate will be commented.

The collate in SQL Server comes with additional specifications, such as **CI, CS, AI,** and **AS**. If there are additional specifications that are unsupported, they will be commented in the result.

### Source

Copy code

```
:force:
SELECT 'a' COLLATE Latin1_General_CI_AS;

SELECT 'a' COLLATE Modern_Spanish_CI_AS;

SELECT 'a' COLLATE French_CI_AS;

SELECT 'a' COLLATE Albanian_BIN;

SELECT 'a' COLLATE Latin1_General_CI_AS_WS;

SELECT 'a' COLLATE Latin1_General_CI_AS_KS_WS;

SELECT 'a' COLLATE Albanian_CI_AI;
```

### Expected

Copy code

```
:force:
SELECT 'a' COLLATE 'EN-CI-AS';

SELECT 'a' COLLATE 'ES-CI-AS';

SELECT 'a' COLLATE 'FR-CI-AS';

SELECT 'a'
--           !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATION Albanian_BIN NOT SUPPORTED ***/!!!
-- COLLATE Albanian_BIN
                     ;

SELECT 'a' COLLATE 'EN-CI-AS' /*** SSC-FDM-TS0002 - COLLATION FOR VALUE WS NOT SUPPORTED ***/;

SELECT 'a' COLLATE 'EN-CI-AS' /*** SSC-FDM-TS0002 - COLLATION FOR VALUES KS,WS NOT SUPPORTED ***/;

SELECT 'a'
--           !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATION Albanian_CI_AI NOT SUPPORTED ***/!!!
-- COLLATE Albanian_CI_AI
                       ;
```

Let’s see an example of collate in a Create Table

### Source

Copy code

```
:force:
CREATE TABLE TABLECOLLATE
(
    COL1 VARCHAR COLLATE Latin1_General_CI_AS
);
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLECOLLATE
(
    COL1 VARCHAR COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

As you can see, the transformation of Collate inside a Select or a Table is the same.

### Related EWIs

1. [SSC-EWI-TS0077](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0077): This message is shown when there is a collate clause that is not supported in Snowflake.
2. [SSC-FDM-TS0002](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0002): This message is shown when there is a collate clause that is not supported in Snowflake.
3. [SSC-PRF-0002](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0002): Case-insensitive columns can decrease the performance of queries.

## COMPUTED COLUMN

The computed expression could not be transformed.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The expression of a computed column could not be transformed.

#### Code Example

##### Input Code:

Copy code

```
:force:
CREATE TABLE [TestTable](
    [Col1] AS (CONVERT ([REAL], ExpressionValue))
);
```

##### Output Code:

Copy code

```
:force:
CREATE OR REPLACE TABLE TestTable (
    Col1 REAL AS (CAST(ExpressionValue AS REAL)) /*** SSC-FDM-TS0014 - COMPUTED COLUMN WAS TRANSFORMED TO ITS SNOWFLAKE EQUIVALENT, FUNCTIONAL EQUIVALENCE VERIFICATION PENDING. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

#### Recommendations

- Add manual changes to the not-transformed expression.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

1. [SSC-FDM-TS0014](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0014): Computed column transformed.

## OUTER APPLY

Outer apply statement equivalence translation.

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

When OUTER APPLY is specified, one row is produced for each row of the left rowset even when the right-side rowset expression returns an empty rowset for that row. ([OUTER APPLY Definition](https://learn.microsoft.com/en-us/u-sql/statements-and-expressions/select/from/select-selecting-from-cross-apply-and-outer-apply))

### Syntax

Copy code

```
   Apply_Operator :=
       'CROSS' 'APPLY'
  |    'OUTER' 'APPLY'.
```

### Snowflake equivalence

Despite the unsupported statement OUTER APPLY in Snowflake, there is an equivalent statement, which is LATERAL. Hence, the translation for the statement is conducted to get the same functionality through the use of alternative solutions.

Nevertheless, the LATERAL statement in Snowflake has two variations in syntax. In fact, the INNER JOIN LATERAL variation is used in this specific translation.

The INNER JOIN LATERAL grammar from Snowflake is the following:

Copy code

```
 SELECT ...
FROM <left_hand_table_expression> INNER JOIN LATERAL ( <inline_view> )
...
```

Note

*&lt;inline\_view>* must not be a table name.

And, the single LATERAL statement is shown below:

Copy code

```
 SELECT ...
FROM <left_hand_table_expression>, LATERAL ( <inline_view> )
...
```

### Sample source

The following example shows a general translation between OUTER APPLY and INNER JOIN LATERAL:

#### SQL Server

Copy code

```
SELECT  p.ProjectName, e.ProjectName, e.FirstName
FROM Project p
OUTER APPLY (
    SELECT
        ProjectName,
        FirstName,
        LastName
    FROM Employees e
) e;
```

#### Output

| p.ProjectName | e.ProjectName | FirstName |
| --- | --- | --- |
| Project A | Project A | John |
| Project A | Project A | Jane |
| Project A | Project B | Michael |
| Project B | Project A | John |
| Project B | Project A | Jane |
| Project B | Project B | Michael |
| Project C | Project A | John |
| Project C | Project A | Jane |
| Project C | Project B | Michael |

Expand

Show lessSee more

#### Snowflake

Copy code

```
 SELECT
    p.ProjectName,
    e.ProjectName,
    e.FirstName
FROM
    Project p
    INNER JOIN
        LATERAL (
                   SELECT
                       ProjectName,
                       FirstName,
                       LastName
                   FROM
                       Employees e
               ) e;
```

#### Output

| PROJECTNAME | PROJECTNAME\_2 | FIRSTNAME |
| --- | --- | --- |
| Project A | Project A | John |
| Project A | Project A | Jane |
| Project A | Project B | Michael |
| Project B | Project A | John |
| Project B | Project A | Jane |
| Project B | Project B | Michael |
| Project C | Project A | John |
| Project C | Project A | Jane |
| Project C | Project B | Michael |

Expand

Show lessSee more

### Known issues

Since the translation is an equivalence from the input, there are some limitations.

- TOP and WHERE statements may be reviewed for optimal behavior.
- A correlation name at the end of the statement may be needed. In Snowflake, the query does not represent a problem if the correlation name is not in the query, but functionality may change and does not form part of the accepted pattern in SQL Server.

#### SQL Server

Copy code

```
SELECT
    SATT.UNIVERSAL_NAME
FROM
SAMPLE_ATLAS AS SATT
OUTER APPLY (
    SELECT
        TOP 1 UNIVERSAL_NAME,
        INTERNATIONAL_NAME,
        CODE_IDENTIFIER
    FROM
        SAMPLE_GLOBE AS SG
    WHERE
        SG.GLOBE_KEY = SATT.MbrPersGenKey
    ORDER BY
        GLOBE_KEY
);
```

##### Translation output

Copy code

```
SELECT
            UNIVERSAL_NAME
FROM
            SAMPLE_ATLAS
            AS SATT
            OUTER APPLY
                        /*** MSC-ERROR - MSCCP0001 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/ (SELECT TOP 1
                                                UNIVERSAL_NAME,
                                                INTERNATIONAL_NAME,
                                                CODE_IDENTIFIER
                                    FROM
                                                SAMPLE_GLOBE AS SG
                                    WHERE
                                                SG.GLOBE_KEY = SATT.MbrPersGenKey
                                    ORDER BY GLOBE_KEY
                        );
```

- Specific statements that are not supported may comment out all the block code (example taken from: [JSON Example](https://learn.microsoft.com/en-us/sql/relational-databases/json/validate-query-and-change-json-data-with-built-in-functions-sql-server?view=sql-server-ver16)).

##### SQL Server

Copy code

```
SELECT
    SATT.UNIVERSAL_NAME
FROM
SAMPLE_ATLAS AS SATT
INNER JOIN LATERAL (
    SELECT
        TOP 1 UNIVERSAL_NAME,
        INTERNATIONAL_NAME,
        CODE_IDENTIFIER
    FROM
        SAMPLE_GLOBE AS SG
    WHERE
        SG.GLOBE_KEY = SATT.MbrPersGenKey
    ORDER BY
        GLOBE_KEY
);
```

##### Translation output

Copy code

```
SELECT
	familyName,
	c.givenName AS childGivenName,
	c.firstName AS childFirstName,
	p.givenName AS petName
FROM
	Families f
	LEFT OUTER JOIN
		OPENJSON(f.doc) /*** MSC-WARNING - MSCEWI4030 - Equivalence from CROSS APPLY to LEFT OUTER JOIN must be checked. ***/;
-- ** MSC-ERROR - MSCEWI1001 - UNRECOGNIZED TOKEN ON LINE 7 OF THE SOURCE CODE. **
--		WITH (familyName nvarchar(100), children nvarchar(max) AS JSON)
--		CROSS APPLY OPENJSON(children)
--		WITH (givenName nvarchar(100), firstName nvarchar(100), pets nvarchar(max) AS JSON) as c
--			OUTER APPLY OPENJSON (pets)
--			WITH (givenName nvarchar(100))  as p
```

### Related EWIs

No related EWIs.

## USE

Transact-SQL USE statement Snowflake equivalence.

Applies to

- SQL Server

The [USE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/use-transact-sql?view=sql-server-ver15) statement has its own equivalent in Snowflake. The statement will be translated to the [USE DATABASE](https://docs.snowflake.com/en/sql-reference/sql/use-database.html) statement in Snowflake.

### Translation Examples

#### Source

Copy code

```
:force:
USE [MY DATABASE]
```

#### Output

Copy code

```
:force:
USE DATABASE "MY DATABASE";
```

#### Database name

The `database name` specified in the `USE` statement, could have a change if it comes inside *Square Brackets* **`([ ])`**. The first bracket and the last bracket will be replaced with *quotes.* Example:

##### Source

Copy code

```
:force:
[MYDATABASE]
[[[MYDATABASE]]
```

##### Output

Copy code

```
:force:
"MYDATABASE"
"[[MYDATABASE]"
```

#### User Defined Database

If a user specifies to the Conversion Tool a custom database name to be applied to all the objects by using the `-d` parameter, and wants the USE statements to be transformed, the Database name should be applied just to the `USE` statement and not to the objects. This will override the specified database from the use statement. Example:

##### Source

Copy code

```
:force:
-- Additional Params: -d MYCUSTOMDB
USE [MY DATABASE]

CREATE TABLE [TableName1].[TableName2](
	[ColumnName1] varchar NULL
);
```

##### Output

Copy code

```
:force:
-- Additional Params: -d MYCUSTOMDB
USE DATABASE MYCUSTOMDB;

CREATE OR REPLACE TABLE MYCUSTOMDB.TableName1.TableName2 (
	ColumnName1 VARCHAR NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## EXECUTE

Applies to

- SQL Server
- Azure Synapse Analytics

The translation for **Exec** or **Execute** Statements is not supported in Snowflake, but it will be translated to **CALL** statement.

Note

Some parts in the output code are omitted for clarity reasons.

### Input

Copy code

```
:force:
Exec db.sp1
```

### Output

Copy code

```
:force:
CALL db.sp1();
```

For more information about Execute visit: [Execute inside Procedures](./transact-create-procedure#exec--execute)

## PRINT

Applies to

- SQL Server
- Azure Synapse Analytics
  

The **Print** statement is not directly supported in Snowflake, but it will be translated to its closest equivalent, the **SYSTEM$LOG\_INFO** built-in function.

### Input

Copy code

```
:force:
PRINT 'My message';
```

### Output (Inside SnowScript)

Copy code

```
:force:
SYSTEM$LOG_INFO('My message');
```

### Output (Outside of SnowScript)

When the **Print** statement is used outside of a stored procedure, it is required to be called from a UDP.

Copy code

```
:force:
CALL PUBLIC.LOG_INFO_UDP('My message');
```

Before you can begin logging messages, you must set up an event table. For more information, see: [Logging messages in Snowflake Scripting](/developer-guide/logging-tracing/logging-snowflake-scripting)

## System Stored Procedures

## SP\_EXECUTESQL

Translation specification for the system procedure SP\_EXECUTESQL.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The SP\_EXECUTESQL system stored procedure is used to execute a Transact-SQL statement or batch that can be reused many times, or one that is built dynamically. The statement or batch can contain embedded parameters.

This functionality can be emulated in Snowflake through the EXECUTE IMMEDIATE statement and with a user-defined function (UDF) for embedded parameters.

For more information about the user-defined function (UDF) used for this translation,
check [TRANSFORM\_SP\_EXECUTE\_SQL\_STRING\_UDF(STRING, STRING, ARRAY, ARRAY)](../../function-references/sql-server#transform_sp_execute_sql_string_udfstring-string-array-array).

#### Syntax

##### Transact

Copy code

```
 sp_executesql [ @stmt = ] N'statement'
[
    [ , [ @params = ] N'@parameter_name data_type [ { OUT | OUTPUT } ] [ , ...n ]' ]
    [ , [ @param1 = ] 'value1' [ , ...n ] ]
]
```

### Sample Source Patterns

All patterns will transform SP\_EXECUTESQL into Snowflake’s EXECUTE IMMEDIATE statement and only modify the SQL string to be executed when using embedded parameters.

Warning

[SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030) (Usage of Dynamic SQL) will be added for all patterns. Even though the translation for SP\_EXECUTESQL is equivalent to Snowflake, in this context, this EWI indicates that the SQL string might require manual fixes for the translation to execute as intended.

#### Setup Data

##### Transact

Copy code

```
 CREATE TABLE PERSONS(
  NAME VARCHAR(25),
  ID INT,
  AGE INT
);

-- DATA
INSERT INTO PERSONS VALUES ('John Smith', 1, 24);
INSERT INTO PERSONS VALUES ('John Doe', 2, 21);
INSERT INTO PERSONS VALUES ('Mary Keller', 3, 32);
INSERT INTO PERSONS VALUES ('Mundane Man', 4, 18);
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE PERSONS (
  NAME VARCHAR(25),
  ID INT,
  AGE INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
;

-- DATA
INSERT INTO PERSONS VALUES ('John Smith', 1, 24);
INSERT INTO PERSONS VALUES ('John Doe', 2, 21);
INSERT INTO PERSONS VALUES ('Mary Keller', 3, 32);
INSERT INTO PERSONS VALUES ('Mundane Man', 4, 18);
```

#### Without embedded parameters

When no embedded parameters are being used, the SP\_EXECUTESQL is transformed into an EXECUTE IMMEDIATE statement and use the SQL string without modifications.

##### Transact

Copy code

```
 CREATE PROCEDURE SIMPLE_SINGLE_QUERY
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    SET @SQLString = N'SELECT * FROM PERSONS';
    EXECUTE sp_executesql @SQLString;
END

GO

EXEC SIMPLE_SINGLE_QUERY;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE SIMPLE_SINGLE_QUERY ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQLSTRING VARCHAR(500);
    ProcedureResultSet RESULTSET;
  BEGIN

    SQLSTRING := 'SELECT
   *
FROM
   PERSONS;';
    ProcedureResultSet := (
      !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
      EXECUTE IMMEDIATE :SQLSTRING
    );
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL SIMPLE_SINGLE_QUERY();
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |

Expand

Show lessSee more

#### With embedded parameters for data binding

For embedded parameters for data binding, the SP\_EXECUTESQL is transformed into an EXECUTE IMMEDIATE statement, and the SQL string is modified through the `TRANSFORM_SP_EXECUTE_SQL_STRING_UDF`.

The result of the EXECUTE IMMEDIATE is assigned to the `ProcedureResultSet` variable and later returned as `TABLE(ProcedureResultSet)`.

##### Transact

Copy code

```
 CREATE PROCEDURE QUERY_WITH_DATA_BINDING_PARAMS
AS
BEGIN
    DECLARE @IntVariable INT;
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);

    SET @IntVariable = 21;
    SET @SQLString = N'SELECT * FROM PERSONS WHERE AGE = @age';
    SET @ParmDefinition = N'@age INT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @age = @IntVariable;
END

GO

EXEC QUERY_WITH_DATA_BINDING_PARAMS;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Doe | 2 | 21 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE QUERY_WITH_DATA_BINDING_PARAMS ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    INTVARIABLE INT;
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    ProcedureResultSet RESULTSET;
  BEGIN

    INTVARIABLE := 21;
    SQLSTRING := 'SELECT
   *
FROM
   PERSONS
WHERE
   AGE = @age;';
    PARMDEFINITION := '@age INT';
    ProcedureResultSet := (
      !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
      EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('AGE'), ARRAY_CONSTRUCT(:INTVARIABLE))
    );
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL QUERY_WITH_DATA_BINDING_PARAMS();
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Doe | 2 | 21 |

Expand

Show lessSee more

#### With embedded OUTPUT parameters

For embedded OUTPUT parameters, the SP\_EXECUTESQL is transformed into an EXECUTE IMMEDIATE statement, and the SQL string is modified through the `TRANSFORM_SP_EXECUTE_SQL_STRING_UDF`.

Additionally, a `SELECT $1, ..., $n INTO :outputParam1, ..., :outputParamN FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))` is added to the result of each column to the corresponding OUTPUT parameter.

Warning

SSC-FDM-TS0028 is added to the SELECT INTO statement. It is essential for the parameters in the INTO clause to appear in the same order as they were assigned in the original SQL String.

Otherwise, manual changes are required to meet this requirement.

##### Transact

Copy code

```
CREATE PROCEDURE QUERY_WITH_OUTPUT_PARAMS
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParamDefinition NVARCHAR(500);
    DECLARE @MaxAge INT;

    SET @SQLString = N'SELECT @MaxAgeOUT = max(AGE) FROM PERSONS';
    SET @ParamDefinition = N'@MaxAgeOUT INT OUTPUT';
    EXECUTE sp_executesql @SQLString, @ParamDefinition, @MaxAgeOUT = @MaxAge OUTPUT;

    SELECT @MaxAge;
END

GO

EXEC QUERY_WITH_OUTPUT_PARAMS;
```

##### Results

| &lt;anonymous> |
| --- |
| 32 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE QUERY_WITH_OUTPUT_PARAMS ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/27/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        SQLSTRING VARCHAR(500);
        PARAMDEFINITION VARCHAR(500);
        MAXAGE INT;
        ProcedureResultSet RESULTSET;
    BEGIN

        SQLSTRING := 'SELECT
   MAX(AGE) FROM
   PERSONS;';
        PARAMDEFINITION := '@MaxAgeOUT INT OUTPUT';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARAMDEFINITION, ARRAY_CONSTRUCT('MAXAGEOUT'), ARRAY_CONSTRUCT(:MAXAGE));
        --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
        SELECT
            $1
        INTO
            :MAXAGE
        FROM
            TABLE(RESULT_SCAN(LAST_QUERY_ID()));
        ProcedureResultSet := (
        SELECT
            :MAXAGE);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;

CALL QUERY_WITH_OUTPUT_PARAMS();
```

##### Results

| :MAXAGE::NUMBER(38,0) |
| --- |
| 32 |

Expand

Show lessSee more

#### With both embedded OUTPUT parameters and data binding

The translation is the same as for only OUTPUT parameters.

##### Transact

Copy code

```
CREATE PROCEDURE QUERY_WITH_BOTH_PARAMS
AS
BEGIN
    DECLARE @AgeVariable INT;
    DECLARE @IdVariable INT;
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    SET @AgeVariable = 30;
    SET @IdVariable = 100;
    SET @SQLString = N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE AGE < @age AND ID < @id;';
    SET @ParmDefinition = N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @age = @AgeVariable, @id = @IdVariable, @MaxAgeOUT = @MaxAge OUTPUT, @MaxIdOUT = @MaxId OUTPUT;

    SELECT @MaxAge, @MaxId;
END

GO

EXEC QUERY_WITH_BOTH_PARAMS;
```

##### Results

| &lt;anonymous> | &lt;anonymous> |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE QUERY_WITH_BOTH_PARAMS ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    AGEVARIABLE INT;
    IDVARIABLE INT;
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    MAXAGE INT;
    MAXID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    AGEVARIABLE := 30;
    IDVARIABLE := 100;
    SQLSTRING := 'SELECT
   MAX(AGE),
   MAX(ID) FROM
   PERSONS
WHERE
   AGE < @age AND ID < @id;';
    PARMDEFINITION := '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('AGE', 'ID', 'MAXAGEOUT', 'MAXIDOUT'), ARRAY_CONSTRUCT(:AGEVARIABLE, :IDVARIABLE, :MAXAGE, :MAXID));
    --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
    SELECT
      $1,
      $2
    INTO
      :MAXAGE,
      :MAXID
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    ProcedureResultSet := (
    SELECT
      :MAXAGE,
      :MAXID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL QUERY_WITH_BOTH_PARAMS();
```

##### Results

| :MAXAGE::NUMBER(38,0) | :MAXID::NUMBER(38,0) |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

#### Parameters not in order of definition

This pattern follows the same rules as the previous patterns. `TRANSFORM_SP_EXECUTE_SQL_STRING_UDF` replaces the parameter values in the correct order.

##### Transact

Copy code

```
CREATE PROCEDURE QUERY_PARAMS_NOT_IN_ORDER_OF_DEF
AS
BEGIN
    DECLARE @AgeVariable INT;
    DECLARE @IdVariable INT;
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    SET @AgeVariable = 30;
    SET @IdVariable = 100;
    SET @SQLString = N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE AGE < @age AND ID < @id;';
    SET @ParmDefinition = N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @id = @IdVariable, @MaxAgeOUT = @MaxAge OUTPUT, @age = @AgeVariable, @MaxIdOUT = @MaxId OUTPUT;

    SELECT @MaxAge, @MaxId;
END

GO

EXEC QUERY_PARAMS_NOT_IN_ORDER_OF_DEF;

CREATE PROCEDURE QUERY_PARAMS_NOT_IN_ORDER_OF_DEF_2
AS
BEGIN
    DECLARE @AgeVariable INT;
    DECLARE @IdVariable INT;
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    SET @AgeVariable = 30;
    SET @IdVariable = 100;
    SET @SQLString = N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE AGE < @age AND ID < @id;';
    SET @ParmDefinition = N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @AgeVariable, @MaxAgeOUT = @MaxAge OUTPUT, @id = @IdVariable, @MaxIdOUT = @MaxId OUTPUT;

    SELECT @MaxAge, @MaxId;
END

GO

EXEC QUERY_PARAMS_NOT_IN_ORDER_OF_DEF_2;
```

##### Results

| &lt;anonymous> | &lt;anonymous> |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

| &lt;anonymous> | &lt;anonymous> |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE QUERY_PARAMS_NOT_IN_ORDER_OF_DEF ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    AGEVARIABLE INT;
    IDVARIABLE INT;
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    MAXAGE INT;
    MAXID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    AGEVARIABLE := 30;
    IDVARIABLE := 100;
    SQLSTRING := 'SELECT
   MAX(AGE),
   MAX(ID) FROM
   PERSONS
WHERE
   AGE < @age AND ID < @id;';
    PARMDEFINITION := '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('ID', 'MAXAGEOUT', 'AGE', 'MAXIDOUT'), ARRAY_CONSTRUCT(:IDVARIABLE, :MAXAGE, :AGEVARIABLE, :MAXID));
    --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
    SELECT
      $1,
      $2
    INTO
      :MAXAGE,
      :MAXID
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    ProcedureResultSet := (
    SELECT
      :MAXAGE,
      :MAXID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL QUERY_PARAMS_NOT_IN_ORDER_OF_DEF();

CREATE OR REPLACE PROCEDURE QUERY_PARAMS_NOT_IN_ORDER_OF_DEF_2 ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    AGEVARIABLE INT;
    IDVARIABLE INT;
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    MAXAGE INT;
    MAXID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    AGEVARIABLE := 30;
    IDVARIABLE := 100;
    SQLSTRING := 'SELECT
   MAX(AGE),
   MAX(ID) FROM
   PERSONS
WHERE
   AGE < @age AND ID < @id;';
    PARMDEFINITION := '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('', 'MAXAGEOUT', 'ID', 'MAXIDOUT'), ARRAY_CONSTRUCT(:AGEVARIABLE, :MAXAGE, :IDVARIABLE, :MAXID));
    --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
    SELECT
      $1,
      $2
    INTO
      :MAXAGE,
      :MAXID
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    ProcedureResultSet := (
    SELECT
      :MAXAGE,
      :MAXID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL QUERY_PARAMS_NOT_IN_ORDER_OF_DEF_2();
```

##### Results

| :MAXAGE::NUMBER(38,0) | :MAXID::NUMBER(38,0) |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

| :MAXAGE::NUMBER(38,0) | :MAXID::NUMBER(38,0) |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

#### Execute direct values

This translation also handles the cases where the values are directly assigned instead of using variables.

##### Transact

Copy code

```
CREATE PROCEDURE QUERY_WITH_DIRECT_PARAMS_VALUES_ALL
AS
BEGIN
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    EXECUTE sp_executesql
        N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE ID < @id AND AGE < @age;',
        N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT',
        30,
        100,
        @MaxAge OUTPUT,
        @MaxId OUTPUT;

    SELECT @MaxAge, @MaxId;
END

GO

EXEC QUERY_WITH_DIRECT_PARAMS_VALUES_ALL;
```

##### Results

| &lt;anonymous> | &lt;anonymous> |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE QUERY_WITH_DIRECT_PARAMS_VALUES_ALL ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/07/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    MAXAGE INT;
    MAXID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF('SELECT
   MAX(AGE),
   MAX(ID) FROM
   PERSONS
WHERE
   ID < @id AND AGE < @age;', '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT', ARRAY_CONSTRUCT('', '', '', ''), ARRAY_CONSTRUCT(
    30,
    100, :MAXAGE, :MAXID));
    --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
    SELECT
      $1,
      $2
    INTO
      :MAXAGE,
      :MAXID
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    ProcedureResultSet := (
    SELECT
      :MAXAGE,
      :MAXID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL QUERY_WITH_DIRECT_PARAMS_VALUES_ALL();
```

##### Results

| :MAXAGE::NUMBER(38,0) | :MAXID::NUMBER(38,0) |
| --- | --- |
| 24 | 4 |

Expand

Show lessSee more

#### SQL string dynamically built

This pattern follows the same rules as the previous patterns. However, assigning the result of the EXECUTE IMMEDIATE statement might not be added if the SQL string is not a simple single query with or without embedded parameters.

Furthermore, the SQL string must start with the literal value `'SELECT'` for the conversion to correctly identify that a SELECT statement is going to be executed.

##### Transact

Copy code

```
CREATE PROCEDURE DYNAMIC_WITH_PARAMS
AS
BEGIN
    DECLARE @IntVariable INT;
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);
    DECLARE  @where_clause nvarchar(100);

    SET @where_clause = 'WHERE AGE = @age';
    SET @IntVariable = 21;
    SET @SQLString = N'SELECT * FROM PERSONS ' + @where_clause;
    SET @ParmDefinition = N'@age INT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @age = @IntVariable;
END

GO

EXEC DYNAMIC_WITH_PARAMS;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Doe | 2 | 21 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE DYNAMIC_WITH_PARAMS ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    INTVARIABLE INT;
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    WHERE_CLAUSE VARCHAR(100);
    ProcedureResultSet RESULTSET;
  BEGIN

    WHERE_CLAUSE := 'WHERE AGE = @age';
    INTVARIABLE := 21;
    SQLSTRING := 'SELECT
   *
FROM
   PERSONS ' || :WHERE_CLAUSE || ';';
    PARMDEFINITION := '@age INT';
    ProcedureResultSet := (
      !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
      EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('AGE'), ARRAY_CONSTRUCT(:INTVARIABLE))
    );
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL DYNAMIC_WITH_PARAMS();
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Doe | 2 | 21 |

Expand

Show lessSee more

#### Returning multiple result sets

Snowflake Scripting procedures only allow one result set to be returned per procedure.

To replicate Transact-SQL behavior, when two or more result sets are to be returned, they are stored in temporary tables. The Snowflake Scripting procedure will return an array containing the names of the temporary tables. For more information, check [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020).

##### Transact

Copy code

```
CREATE PROCEDURE WITH_MULTIPLE_RETURNS
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @ParmDefinition NVARCHAR(500);

    SET @SQLString = N'SELECT * FROM PERSONS WHERE AGE = @age';
    SET @ParmDefinition = N'@age INT';
    EXECUTE sp_executesql @SQLString, @ParmDefinition, @age = 21;

    SET @SQLString = N'INSERT INTO PERSONS VALUES (''INSERT FIRST'', 1200, 230);';
    EXECUTE sp_executesql @SQLString;

    SET @SQLString = N'SELECT * FROM PERSONS';
    EXECUTE sp_executesql @SQLString;
END

GO

EXECUTE WITH_MULTIPLE_RETURNS;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Doe | 2 | 21 |

Expand

Show lessSee more

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |
| INSERT FIRST | 1200 | 230 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE WITH_MULTIPLE_RETURNS ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/07/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQLSTRING VARCHAR(500);
    PARMDEFINITION VARCHAR(500);
    ProcedureResultSet1 VARCHAR;
    ProcedureResultSet2 VARCHAR;
    return_arr ARRAY := array_construct();
  BEGIN

    SQLSTRING := 'SELECT
   *
FROM
   PERSONS
WHERE
   AGE = @age;';
    PARMDEFINITION := '@age INT';
    ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(:SQLSTRING, :PARMDEFINITION, ARRAY_CONSTRUCT('AGE'), ARRAY_CONSTRUCT(21));
    CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
      SELECT
        *
      FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    return_arr := array_append(return_arr, :ProcedureResultSet1);
    SQLSTRING := 'INSERT INTO PERSONS VALUES ('INSERT FIRST', 1200, 230);';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :SQLSTRING;
    SQLSTRING := 'SELECT
   *
FROM
   PERSONS;';
    ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :SQLSTRING;
    CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
      SELECT
        *
      FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    return_arr := array_append(return_arr, :ProcedureResultSet2);
    --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
    RETURN return_arr;
  END;
$$;

CALL WITH_MULTIPLE_RETURNS();
```

##### Results

| WITH\_MULTIPLE\_RETURNS |
| --- |
| [ “RESULTSET\_88C35D7A\_1E5B\_455D\_97A4\_247806E583A5”, “RESULTSET\_B2345B61\_A015\_43CB\_BA11\_6D3E013EF262” ] |

Expand

Show lessSee more

### Known Issues

#### 1. Invalid code is detected

`SP_EXECUTESQL` can execute more than one SQL statement inside the SQL string. Snowflake also supports executing multiple SQL statements, but need to be enclosed in a `BEGIN ... END` block.
Furthermore, when executing multiple statements from a `BEGIN ... END` block, the `EXECUTE IMMEDIATE` will not return a resultset.
The translation for these cases is not yet supported.
For more information, check [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030).

Thus, when this case is detected, in the translated code, the `EXECUTE IMMEDIATE` will not be assigned to the `ProcedureResultSet`.

##### Transact

Copy code

```
CREATE PROCEDURE WITH_INVALID_CODE_DETECTED
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    SET @SQLString = N'INSERT INTO PERSONS VALUES (''INSERT FIRST'', 1200, 230); SELECT * FROM PERSONS;';
    EXECUTE sp_executesql @SQLString;
END

GO

EXEC WITH_INVALID_CODE_DETECTED;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |
| INSERT FIRST | 1200 | 230 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE WITH_INVALID_CODE_DETECTED ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQLSTRING VARCHAR(500);
  BEGIN

    SQLSTRING := 'INSERT INTO PERSONS VALUES ('INSERT FIRST', 1200, 230); SELECT
   *
FROM
   PERSONS;';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :SQLSTRING;
  END;
$$;

CALL WITH_INVALID_CODE_DETECTED();
```

##### Results

Copy code

```
000006 (0A000): Uncaught exception of type 'STATEMENT_ERROR' on line 10 at position 4 : Multiple SQL statements in a single API call are not supported; use one API call per statement instead.
```

#### 2. Valid or Invalid code is not detected

When the SQL string is built dynamically through concatenations, it might not be detectable what statement is going to be executed. Thus, in the translated code, the `EXECUTE IMMEDIATE` will not be assigned to the `ProcedureResultSet`.

##### Transact

Copy code

```
CREATE PROCEDURE WITH_INVALID_CODE_NOT_DETECTED
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    DECLARE @SQLInsert NVARCHAR(500);
    SET @SQLInsert = N'INSERT INTO PERSONS VALUES (''INSERT FIRST'', 1200, 230)';
    SET @SQLString = @SQLInsert + N'SELECT * FROM PERSONS;';
    EXECUTE sp_executesql @SQLString;
END

GO

EXEC WITH_INVALID_CODE_NOT_DETECTED;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |
| INSERT FIRST | 1200 | 230 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE WITH_INVALID_CODE_NOT_DETECTED ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQLSTRING VARCHAR(500);
    SQLINSERT VARCHAR(500);
  BEGIN

    SQLINSERT := 'INSERT INTO PERSONS VALUES ('INSERT FIRST', 1200, 230);';
    SQLSTRING := :SQLINSERT || 'SELECT * FROM PERSONS;';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE :SQLSTRING;
  END;
$$;

CALL WITH_INVALID_CODE_NOT_DETECTED();
```

##### Results

Copy code

```
000006 (0A000): Uncaught exception of type 'STATEMENT_ERROR' on line 10 at position 4 : Multiple SQL statements in a single API call are not supported; use one API call per statement instead.
```

#### 3. Invalid code is mistaken as valid

If the SQL string starts with a SELECT statement and is followed by more statements, this will be detected as valid code and an attempt will be made to assign the result of the `EXECUTE IMMEDIATE` to the `ProcedureResultSet`. This leads to a compilation error.
For more information, check [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030).

##### Transact

Copy code

```
CREATE PROCEDURE WITH_INVALID_CODE_MISTAKEN_AS_VALID
AS
BEGIN
    DECLARE @SQLString NVARCHAR(500);
    SET @SQLString = N'SELECT * FROM PERSONS; SELECT * FROM PERSONS;';
    EXECUTE sp_executesql @SQLString;
END

GO

EXEC WITH_INVALID_CODE_MISTAKEN_AS_VALID;
```

##### Results

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |

Expand

Show lessSee more

| Name | ID | AGE |
| --- | --- | --- |
| John Smith | 1 | 24 |
| John Doe | 2 | 21 |
| Mary Keller | 3 | 32 |
| Mundane Man | 4 | 18 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE WITH_INVALID_CODE_MISTAKEN_AS_VALID ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQLSTRING VARCHAR(500);
    ProcedureResultSet RESULTSET;
  BEGIN

    SQLSTRING := 'SELECT
   *
FROM
   PERSONS; SELECT
   *
FROM
   PERSONS;';
    ProcedureResultSet := (
      !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
      EXECUTE IMMEDIATE :SQLSTRING
    );
    RETURN TABLE(ProcedureResultSet);
  END;
$$;

CALL WITH_INVALID_CODE_MISTAKEN_AS_VALID();
```

##### Results

Copy code

```
000006 (0A000): Uncaught exception of type 'STATEMENT_ERROR' on line 10 at position 4 : Multiple SQL statements in a single API call are not supported; use one API call per statement instead.
```

### Related EWIs

1. [SSC-EWI-0030](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030): The statement below has usages of dynamic SQL
2. [SSC-FDM-TS0028](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0028): Output parameters must have the same order as they appear in the executed code.
3. [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables.

## SP\_RENAME

Stored Procedure to Rename certain objects in SQL Server

Applies to

- SQL Server
- Azure Synapse Analytics

The SP\_RENAME system store procedure can be emulated in Snowflake in certain scenarios. In general, the equivalent is the EXECUTE IMMEDIATE using a dynamic statement with the ALTER TABLE and the original parameters.

### Translation Examples for Tables

#### Source

Copy code

```
:force:
EXEC sp_rename 'TABLE1', 'TABLENEW1'
```

#### Output

Copy code

```
:force:
EXECUTE IMMEDIATE 'ALTER TABLE TABLE1 RENAME TO TABLENEW1';
```

##### Source

Copy code

```
:force:
DECLARE @varname1 nvarchar(50) = 'previous_name'
DECLARE @varname2 nvarchar(50) = 'newer_name'
EXEC sp_rename @varname1, @varname2
```

##### Output

Copy code

```
:force:
DECLARE
VARNAME1 VARCHAR(50) := 'previous_name';
VARNAME2 VARCHAR(50) := 'newer_name';
BEGIN
EXECUTE IMMEDIATE 'ALTER TABLE ' || :VARNAME1 || ' RENAME TO ' || :VARNAME2;
END;
```

#### Translation Examples for Columns

##### Source

Copy code

```
:force:
EXEC sp_rename 'sample_BACKUP_2.column_old', 'column_new', 'COLUMN'
EXEC sp_rename 'database1.sample_BACKUP_3.column_old', 'column_new', 'COLUMN'
```

##### Output

Copy code

```
:force:
EXECUTE IMMEDIATE 'ALTER TABLE sample_BACKUP_2 RENAME COLUMN column_old TO column_new';

EXECUTE IMMEDIATE 'ALTER TABLE database1.sample_BACKUP_3 RENAME COLUMN column_old TO column_new';
```

##### Source

Copy code

```
:force:
DECLARE @oldColumnName nvarchar(50) = 'previous_name'
DECLARE @newColumnName nvarchar(50) = 'newer_name'
DECLARE @tableName nvarchar(50) = 'TABLE'
EXEC sp_rename @objname = @tableName + '.' + @oldColumnName, @newname = @newColumnName, @objtype = 'COLUMN';
```

##### Output

Copy code

```
:force:
DECLARE
OLDCOLUMNNAME VARCHAR(50) := 'previous_name';
NEWCOLUMNNAME VARCHAR(50) := 'newer_name';
TABLENAME VARCHAR(50) := 'TABLE';
BEGIN
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0075 - TRANSLATION FOR BUILT-IN PROCEDURE 'SP_RENAME' IS NOT CURRENTLY SUPPORTED. ***/!!!
EXEC sp_rename OBJNAME = :TABLENAME || '.' || :OLDCOLUMNNAME, NEWNAME = :NEWCOLUMNNAME, OBJTYPE = 'COLUMN';
END;
```

### Related EWIs

1. [SSC-EWI-TS0075](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0075):
   Translation for Built-In Procedure Is Not Currently Supported.

## WAITFOR DELAY

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

In SQL Server, [`WAITFOR DELAY`](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/waitfor-transact-sql?view=sql-server-ver16) pauses execution for a specified duration. `WAITFOR DELAY` statements are transformed to Snowflake’s [`CALL SYSTEM$WAIT()`](https://docs.snowflake.com/en/sql-reference/functions/system_wait) function, which provides equivalent delay functionality.

The time string is parsed and converted to seconds (or milliseconds for sub-second precision). Variables and parameters are passed through directly with an EWI warning, since `SYSTEM$WAIT` expects a numeric value rather than a time string.

Note

`WAITFOR TIME` (which pauses until a specific time of day) has no Snowflake equivalent and remains flagged with SSC-EWI-0073.

### Translation Examples

#### WAITFOR DELAY with literal time

##### Input Code:

Copy code

```
 CREATE PROCEDURE proc1()
AS
BEGIN
  WAITFOR DELAY '00:00:30';
END
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    CALL SYSTEM$WAIT(30);
  END;
$$;
```

#### WAITFOR DELAY with sub-second precision

##### Input Code:

Copy code

```
 CREATE PROCEDURE proc1()
AS
BEGIN
  WAITFOR DELAY '00:00:00.500';
END
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    CALL SYSTEM$WAIT(500, 'MILLISECONDS');
  END;
$$;
```

#### WAITFOR DELAY with variable

##### Input Code:

Copy code

```
 CREATE PROCEDURE proc1(@WaitTime INT)
AS
BEGIN
  WAITFOR DELAY @WaitTime;
END
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 (WAITTIME INT)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0094 - WAITFOR DELAY WITH VARIABLE ':WAITTIME' WAS CONVERTED TO SYSTEM$WAIT, BUT THE VARIABLE MAY CONTAIN A TIME STRING IN 'HH:MM:SS' FORMAT. SYSTEM$WAIT EXPECTS A NUMERIC VALUE IN SECONDS. ***/!!!
    CALL SYSTEM$WAIT(:WAITTIME);
  END;
$$;
```

#### WAITFOR DELAY at script level

##### Input Code:

Copy code

```
 WAITFOR DELAY '00:00:30';
```

##### Generated Code:

Copy code

```
 CALL SYSTEM$WAIT(30);
```

### Known Limitations

- `WAITFOR TIME` (pause until a specific time of day) has no Snowflake equivalent and is flagged with SSC-EWI-0073.
- When a variable is used, SSC-EWI-TS0094 is emitted because `SYSTEM$WAIT` expects a numeric value but the variable may contain a time string in `'HH:MM:SS'` format.

### Related EWIs

1. [SSC-EWI-TS0094](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0094): WAITFOR DELAY variable may contain a time string incompatible with SYSTEM$WAIT.
2. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending functional equivalence review (emitted for WAITFOR TIME).

## CREATE STATISTICS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

`CREATE STATISTICS` statements are commented out because Snowflake automatically collects optimizer statistics and does not require this statement.

### Translation Example

#### Input Code:

Copy code

```
CREATE STATISTICS Stats1 ON dbo.Table1(col1);
```

#### Generated Code:

Copy code

```
----** SSC-FDM-0037 - CREATE STATISTICS NOT NEEDED. SNOWFLAKE AUTOMATICALLY COLLECTS STATISTICS. **
--CREATE STATISTICS Stats1 ON dbo.Table1 (
--  col1
--);
```

### Additional Example

#### Input Code:

Copy code

```
CREATE STATISTICS NamePurchase ON AdventureWorks2022.Person.Person(BusinessEntityID, EmailPromotion) WITH FULLSCAN, NORECOMPUTE;
```

#### Generated Code:

Copy code

```
----** SSC-FDM-0037 - CREATE STATISTICS NOT NEEDED. SNOWFLAKE AUTOMATICALLY COLLECTS STATISTICS. **
--CREATE STATISTICS NamePurchase ON AdventureWorks2022.Person.Person (
--  BusinessEntityID,
--  EmailPromotion
--) WITH FULLSCAN, NORECOMPUTE ;
```

### Known Limitations

- Any operational process that explicitly creates or refreshes statistics in SQL Server should be reviewed, because Snowflake manages optimizer statistics automatically.

### Related Issues

1. [SSC-FDM-0037](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0037): Statistics function not needed in Snowflake.

## CREATE SYNONYM

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Snowflake does not support synonyms. `CREATE SYNONYM` statements are commented out with the `SSC-FDM-TS0059` marker and all references to the synonymn are replaced with the original base object name, so the generated Snowflake code is functionally equivalent.

### Translation Example

#### Input Code:

Copy code

```
CREATE SYNONYM MyProduct FOR inventory.product;
```

#### Generated Code:

Copy code

```
----** SSC-FDM-TS0059 - SYNONYMS ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES TO THIS SYNONYM HAVE BEEN REPLACED WITH THE ORIGINAL OBJECT NAME. **
--CREATE SYNONYM MyProduct FOR inventory.product;
```

### Additional Example

When a synonym is used as a table reference in a query, it is replaced with the original object name.

#### Input Code:

Copy code

```
CREATE SYNONYM MyProduct FOR inventory.product;
GO
SELECT * FROM MyProduct;
```

#### Generated Code:

Copy code

```
----** SSC-FDM-TS0059 - SYNONYMS ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES TO THIS SYNONYM HAVE BEEN REPLACED WITH THE ORIGINAL OBJECT NAME. **
--CREATE SYNONYM MyProduct FOR inventory.product;

SELECT
  *
FROM
  inventory.product;
```

### Related Issues

1. [SSC-FDM-TS0059](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0059): Synonyms are not supported in Snowflake. References to this synonym have been replaced with the original object name.
