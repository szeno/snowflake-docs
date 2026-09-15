# Code Conversion - SQL Server-Azure Synapse Functional Differences

Applies to

- SQL Server
- Azure Synapse Analytics

## SSC-FDM-TS0001

Note

This FDM is deprecated, please refer to [SSC-EWI-TS0077](../conversion-issues/sqlServerEWI#ssc-ewi-ts0077) documentation

### Description

This message is shown when there is a collate clause that is not supported in Snowflake.

#### Code example

##### Input Code:

Copy code

```
 SELECT 'a' COLLATE Albanian_BIN;

SELECT 'a' COLLATE Albanian_CI_AI;

CREATE TABLE ExampleTable (
    ID INT,
    Name VARCHAR(50) COLLATE collateName
);
```

##### Generated Code:

Copy code

```
 SELECT 'a'
--           --** SSC-FDM-TS0001 - COLLATION Albanian_BIN NOT SUPPORTED **
--           COLLATE Albanian_BIN
                               ;

SELECT 'a'
--           --** SSC-FDM-TS0001 - COLLATION Albanian_CI_AI NOT SUPPORTED **
--           COLLATE Albanian_CI_AI
                                 ;

CREATE OR REPLACE TABLE ExampleTable (
    ID INT,
    Name VARCHAR(50)
--                     --** SSC-FDM-TS0001 - COLLATION collateName NOT SUPPORTED **
--                     COLLATE collateName
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0002

### Description

This message is shown when there is a collate clause that is not supported in Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 SELECT 'a' COLLATE Latin1_General_CI_AS_WS;
```

##### Generated Code:

Copy code

```
 SELECT 'a' COLLATE 'EN-CI-AS' /*** SSC-FDM-TS0002 - COLLATION FOR VALUE WS NOT SUPPORTED ***/;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0003

XP\_LOGININFO mapped to custom UDF

### Description

This message is shown when the XP\_LOGININFO procedure is executed and returns the following set of columns ([See SQL SERVER documentation for more info](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-logininfo-transact-sql?view=sql-server-ver16))

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| account name | type | privilege | mapped login name | permission path |

To replicate this behavior, there is a query that select the columns from the APPLICABLE\_ROLES view in Snowflake, which returns the following set of columns ([See Snowflake documentation for more info](https://docs.snowflake.com/en/sql-reference/info-schema/applicable_roles.html))

| GRANTEE | ROLE\_NAME | ROLE\_OWNER | IS\_GRANTABLE |
| --- | --- | --- | --- |

Expand

Show lessSee more

SQL Server original columns are mapped as shown in the next table. They may be not completely equivalent.

| SQL Server | Snowflake |  |
| --- | --- | --- |
| account name | GRANTEE |  |
| type | ROLE\_OWNER |  |
| privilege | ROLE\_NAME |  |
| mapped login name | GRANTEE |  |
| permission path | NULL |  |

#### Example code

##### Input code:

Copy code

```
 EXEC xp_logininfo

EXEC xp_logininfo 'USERNAME'
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-TS0003 - XP_LOGININFO MAPPED TO CUSTOM UDF XP_LOGININFO_UDF AND MIGHT HAVE DIFFERENT BEHAVIOR **
SELECT
*
FROM
TABLE(XP_LOGININFO_UDF());

--** SSC-FDM-TS0003 - XP_LOGININFO MAPPED TO CUSTOM UDF XP_LOGININFO_UDF AND MIGHT HAVE DIFFERENT BEHAVIOR **
SELECT
*
FROM
TABLE(XP_LOGININFO_UDF('USERNAME'));
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0004

### Description

This message is shown when a `BULK INSERT` was transformed and a `PUT` command is added to the output code. It happens because the `PUT` command cannot be executed using the SnowSQL Web UI. To successfully execute it, any user should have the SnowCLI installed before.

#### Code Example

##### Input Code:

Copy code

```
 BULK INSERT #temptable FROM 'path/to/file.txt'  
WITH
(
   FIELDTERMINATOR ='\t',  
   ROWTERMINATOR ='\n'
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE FILE FORMAT FILE_FORMAT_638466175888203490
FIELD_DELIMITER = '\t'
RECORD_DELIMITER = '\n';

CREATE OR REPLACE STAGE STAGE_638466175888203490
FILE_FORMAT = FILE_FORMAT_638466175888203490;

--** SSC-FDM-TS0004 - PUT STATEMENT IS NOT SUPPORTED ON WEB UI. YOU SHOULD EXECUTE THE CODE THROUGH THE SNOWFLAKE CLI **
PUT file://path/to/file.txt @STAGE_638466175888203490 AUTO_COMPRESS = FALSE;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "#temptable" **
COPY INTO T_temptable FROM @STAGE_638466175888203490/file.txt;
```

#### Best Practices

- Install SnowCLI.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0005

TRY\_CONVERT/TRY\_CAST could not be converted to TRY\_CAST

Note

This FDM is deprecated.

### Description

This FDM is added when a TRY\_CONVERT or TRY\_CAST cannot be converted to a TRY\_CAST in Snowflake.

[Snowflake’s TRY\_CAST](https://docs.snowflake.com/en/sql-reference/functions/try_cast) function has a limitation as it only allows the conversion of string expressions. However, Transact’s `TRY_CONVERT` and `TRY_CAST` functions allow any data type expression.

Currently, the transformation from `TRY_CONVERT` or `TRY_CAST` to Snowflake’s `TRY_CAST` is only performed for string expressions or expressions that the tool can identify as strings in its context.

#### Code Example

##### Input Code:

Copy code

```
 SELECT TRY_CAST(14.85 AS INT);
SELECT TRY_CONVERT(VARCHAR, 1234);
SELECT TRY_CONVERT(CHAR, 1);
SELECT TRY_CONVERT(SQL_VARIANT, '2017-01-01 12:00:00');
SELECT TRY_CONVERT(GEOGRAPHY, 'LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

##### Generated Code:

Copy code

```
 SELECT
CAST(14.85 AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/;
SELECT
TO_VARCHAR(1234);
SELECT
TO_CHAR(1);
SELECT
TO_VARIANT('2017-01-01 12:00:00');
SELECT
TO_GEOGRAPHY('LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0006

EXECUTE AS ‘user\_name’ clause does not exist in Snowflake and the user calling the procedure should have all the required privileges.

### Description

This message is shown when a procedure with an `EXECUTE AS 'user_name'` clause is found. This is not supported in Snowflake, so it is changed `EXECUTE AS CALLER.`

This clause specifies the security context under which to execute the procedure.

Note

For more details see the [documentation](https://learn.microsoft.com/en-us/sql/t-sql/statements/execute-as-clause-transact-sql?view=sql-server-ver16&tabs=sqlserver) about the clause functionality.

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROCEDURE SelectAllCustomers
WITH EXECUTE AS 'user_name'
AS
BEGIN
      SELECT * FROM Customers;
END;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "Customers" **
CREATE OR REPLACE PROCEDURE SelectAllCustomers ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
--** SSC-FDM-TS0006 - EXECUTE AS 'user_name' CLAUSE DOES NOT EXIST IN SNOWFLAKE AND THE USER CALLING THE PROCEDURE SHOULD HAVE ALL THE REQUIRED PRIVILEGES **
AS
$$
      DECLARE
            ProcedureResultSet RESULTSET;
      BEGIN
            ProcedureResultSet := (
            SELECT
                  *
            FROM
                  Customers);
            RETURN TABLE(ProcedureResultSet);
      END;
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0007

FOR REPLICATION clause does not exist in Snowflake.

### Description

This message is shown when a procedure with a `FOR REPLICATION` clause is found. This is not supported in Snowflake, so it is removed.

This clause specifies that the procedure is created for replication. Consequently, it can’t be executed on the Subscriber.

Note

For more details see the [documentation](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver16#for-replication) about the clause functionality.

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROCEDURE SelectAllCustomers
WITH FOR REPLICATION
AS
BEGIN
      SELECT * FROM Customers;
END;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "Customers" **
CREATE OR REPLACE PROCEDURE SelectAllCustomers ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
--** SSC-FDM-TS0007 - FOR REPLICATION CLAUSE DOES NOT EXIST IN SNOWFLAKE **
AS
$$
      DECLARE
            ProcedureResultSet RESULTSET;
      BEGIN
            ProcedureResultSet := (
            SELECT
                  *
            FROM
                  Customers);
            RETURN TABLE(ProcedureResultSet);
      END;
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0008

FORMATMESSAGE function was converted to UDF

### Description

This Warning is added because the `FORMATMESSAGE` function is being used and it was replaced by `FORMATMESSAGE_UDF`. The reason to add the warning is because the `FORMATMESSAGE_UDF` used to replace the `FORMATMESSAGE` does not handle properly all kinds of formats and it may throw an error on certain conditions.

Unsigned numerical values that are given as negative will preserve the sign instead of converting the value. Also, the `%I64d` placeholder is not supported by the UDF so it will throw an error when it is used.

In the FORMATMESSAGE\_UDF, an error will happen if the given number of arguments is different than the number of placeholders.

This UDF does not support using message number IDs.

#### Code Example

##### Input Code:

Copy code

```
 SELECT FORMATMESSAGE('Unsigned int %u, %u', 50, -50); -- Unsigned int 50, 4294967246
SELECT FORMATMESSAGE('Unsigned octal %o, %o', 50, -50); -- Unsigned octal 62, 37777777716
SELECT FORMATMESSAGE('Unsigned hexadecimal %X, %x', -11, -50); -- Unsigned hexadecimal FFFFFFF5, ffffffce
SELECT FORMATMESSAGE('Unsigned octal with prefix: %#o', -50); -- Unsigned octal with prefix: 037777777716
SELECT FORMATMESSAGE('Unsigned hexadecimal with prefix: %#X, %x', -11,-50); -- Unsigned hexadecimal with prefix: 0XFFFFFFF5, ffffffce
SELECT FORMATMESSAGE('Bigint %I64d', 3000000000); -- Bigint 3000000000
SELECT FORMATMESSAGE('My message: %s %s %s', 'Hello', 'World'); -- My message: Hello World (null)
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Unsigned int %u, %u', ARRAY_CONSTRUCT(50, -50)); -- Unsigned int 50, 4294967246
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Unsigned octal %o, %o', ARRAY_CONSTRUCT(50, -50)); -- Unsigned octal 62, 37777777716
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Unsigned hexadecimal %X, %x', ARRAY_CONSTRUCT(-11, -50)); -- Unsigned hexadecimal FFFFFFF5, ffffffce
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Unsigned octal with prefix: %#o', ARRAY_CONSTRUCT(-50)); -- Unsigned octal with prefix: 037777777716
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Unsigned hexadecimal with prefix: %#X, %x', ARRAY_CONSTRUCT(-11, -50)); -- Unsigned hexadecimal with prefix: 0XFFFFFFF5, ffffffce
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('Bigint %I64d', ARRAY_CONSTRUCT(3000000000)); -- Bigint 3000000000
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('My message: %s %s %s', ARRAY_CONSTRUCT('Hello', 'World')); -- My message: Hello World (null)
```

#### Best Practices

- Avoid using `%I64d` placeholder in the message.
- Use directly the message as a string instead of using a message ID for the first argument.
- Make sure the number of placeholders is the same as the number of arguments after the message.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0009

Encrypted with not supported in Snowflake.

### Description

This warning is added when there is an `ENCRYPTED WITH` used in a Column Definition. Since this is not supported in Snowflake, it is being removed and a warning is added.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE [SCHEMA1].[TABLE1] (
    [COL1] NVARCHAR(60)
        ENCRYPTED WITH (
            COLUMN_ENCRYPTION_KEY = MyCEK,
            ENCRYPTION_TYPE = RANDOMIZED,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
        )
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE SCHEMA1.TABLE1 (
    COL1 VARCHAR(60)
--    --** SSC-FDM-TS0009 - ENCRYPTED WITH NOT SUPPORTED IN SNOWFLAKE **
--           ENCRYPTED WITH (
--               COLUMN_ENCRYPTION_KEY = MyCEK,
--               ENCRYPTION_TYPE = RANDOMIZED,
--               ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
--           )
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
   ;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0010

CURRENT\_DATABASE function has different behavior in certain cases.

### Description

This EWI is added when the function DB\_NAME is transformed to CURRENT\_DATABASE because Snowflake does not support the database\_id parameter and the CURRENT\_DATABASE function will always return the current database name.

#### Code Example

##### Input Code:

Copy code

```
 SELECT DB_NAME(someId);
```

##### Generated Code:

Copy code

```
 SELECT
CURRENT_DATABASE() /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0011

Default value not allowed in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-TS0078](../conversion-issues/sqlServerEWI#ssc-ewi-ts0078) documentation

### Description

This error is added to the code when expressions like function calls, variable names, or named constants follow the default option.

Snowflake only supports explicit constants like numbers or strings.

#### Code Example

##### Input Code:

Copy code

```
 ALTER TABLE
    T_ALTERTABLETEST
ADD
    COLUMN COL10 INTEGER DEFAULT RANDOM(10);
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "T_ALTERTABLETEST", "RANDOM" **
ALTER TABLE IF EXISTS T_ALTERTABLETEST
ADD
    COLUMN COL10 INTEGER
--                         --** SSC-FDM-TS0011 - DEFAULT OPTION NOT ALLOWED IN SNOWFLAKE **
--                         DEFAULT RANDOM(10)
                                           ;
```

##### 

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0012

Information for the column was not found. STRING used to match CAST operation

### Description

This EWI is added in Table-Valued User Defined Functions where the return type of a column can not be determined during the conversion. `STRING` is used as a default to match the `CAST` operation in the `SELECT` statement

#### Code Example

##### Input Code:

Copy code

```
 CREATE FUNCTION GetDepartmentInfo()
RETURNS TABLE
AS
RETURN
(
  SELECT DepartmentID, Name, GroupName
  FROM HumanResources.Department
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE FUNCTION GetDepartmentInfo ()
RETURNS TABLE(
  DepartmentID STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN DepartmentID WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  Name STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN Name WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  GroupName STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN GroupName WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
$$
    SELECT
    CAST(DepartmentID AS STRING),
    CAST(Name AS STRING),
    CAST(GroupName AS STRING)
    FROM
    HumanResources.Department
$$;
```

#### Best Practices

- The user should check which is the correct data type that could not be found and change it in the `RETURNS TABLE` statement definition.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0013

Snowflake Scripting cursor rows are not modifiable.

### Description

This EWI is added when Cursors are open to modification in the input code. Snowflake Scripting does not allow modifying cursor rows.

#### Example Code:

##### Input Code:

Copy code

```
 CREATE OR ALTER PROCEDURE modifiablecursorTest
AS
BEGIN
    -- Should be marked with SSC-FDM-TS0013
    DECLARE CursorVar CURSOR
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar2 INSENSITIVE CURSOR
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar3 CURSOR KEYSET SCROLL_LOCKS
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar4 CURSOR DYNAMIC OPTIMISTIC
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar6 CURSOR STATIC
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar7 CURSOR READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    -- Shouid not be marked
    DECLARE CursorVar5 CURSOR STATIC READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    RETURN 'DONE';
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE modifiablecursorTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		-- Should be marked with SSC-FDM-TS0013
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar2 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar3 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar4 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar6 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		CursorVar7 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		-- Shouid not be marked
		CursorVar5 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
	BEGIN
		RETURN 'DONE';
	END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0014

Computed column transformed

Note

This FDM is deprecated; please refer to [SSC-EWI-TS0089](../conversion-issues/sqlServerEWI#ssc-ewi-ts0089) for the replacement issue identified by `IssueResources.json`.

### Description

This warning is added when an SQL Server computed column is transformed to its Snowflake equivalent. It is added because, in some cases, the functional equivalence could be affected.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE [TestTable](
    [Col1] AS (CONVERT ([REAL], ExpressionValue))
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TestTable (
    Col1 REAL AS (CAST(ExpressionValue AS REAL)) /*** SSC-FDM-TS0014 - COMPUTED COLUMN WAS TRANSFORMED TO ITS SNOWFLAKE EQUIVALENT, FUNCTIONAL EQUIVALENCE VERIFICATION PENDING. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

#### Best Practices

- No additional user actions are required; it is just informative.
- Add manual changes to the not-transformed expression.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0016

XML columns in Snowflake might have a different format

### Description

This warning is added when an SQL Server FOR XML clause with a non-empty path is transformed to its Snowflake equivalent using `FOR_XML_UDF`. It is added because columns in XML could be different.

Note

`FOR XML PATH('')` (empty path without a `ROOT` clause) is a common SQL Server string concatenation pattern and is **not** an XML generation scenario. These cases are transformed to `LISTAGG` instead of `FOR_XML_UDF`, and this FDM is not emitted. See the [SELECT FOR](../../translation-references/transact/transact-dmls#select-for) section for details.

#### Code Example

Given the following table called `employee` as an example.

| Id | Name | Hint |
| --- | --- | --- |
| 1 | Kinslee Park | Developer |
| 2 | Ezra Mata | Developer |
| 3 | Aliana Quinn | Manager |

Expand

Show lessSee more

##### Input Code:

##### Code

Copy code

```
 SELECT
  	e.id,
  	e.name as full_name,
  	e.hint
  FROM
  	employee e
  FOR XML PATH;
```

##### Output

Copy code

```
 <row>
    <id>1</id>
    <full_name>Kinslee Park</full_name>
    <hint>Developer</hint>
</row>
<row>
    <id>2</id>
    <full_name>Ezra Mata</full_name>
    <hint>Developer</hint>
</row>
<row>
    <id>3</id>
    <full_name>Aliana Quinn</full_name>
    <hint>Manager</hint>
</row>
```

##### Generated Code:

##### Code

Copy code

```
 SELECT
	--** SSC-FDM-TS0016 - XML COLUMNS IN SNOWFLAKE MIGHT HAVE A DIFFERENT FORMAT **
	FOR_XML_UDF(OBJECT_CONSTRUCT('id', e.id, 'full_name', e.name, 'hint', e.hint), 'row')
FROM
	employee e;
```

##### Output

Copy code

```
 <row type="OBJECT">
    <full_name type="VARCHAR">Kinslee Park</full_name>
    <hint type="VARCHAR">Developer</hint>
    <id type="INTEGER">1</id>
</row>
<row type="OBJECT">
    <full_name type="VARCHAR">Ezra Mata</full_name>
    <hint type="VARCHAR">Developer</hint>
    <id type="INTEGER">2</id>
</row>
<row type="OBJECT">
    <full_name type="VARCHAR">Aliana Quinn</full_name>
    <hint type="VARCHAR">Manager</hint>
    <id type="INTEGER">3</id>
</row>
```

#### Best Practices

- No additional user actions are required; it is just informative.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0017

CURRENT\_USER function does not support a user ID as a parameter.

### Description

This EWI is added when functions like `SUSER_NAME` or `SUSER_SNAME` contain the user identifier as a parameter because this last one is not supported in the CURRENT\_USER function in Snowflake.

#### Input Code:

Copy code

```
 SELECT SUSER_NAME(0x010500000000000515000000a065cf7e784b9b5fe77c87705a2e0000);
```

##### Generated Code:

Copy code

```
 SELECT
CURRENT_USER() /*** SSC-FDM-TS0017 - User ID parameter used in SUSER_NAME function is not supported in CURRENT_USER function and it was removed. ***/;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0018

Database console command is not supported

Note

This FDM is deprecated, please refer to [SSC-EWI-TS0079](../conversion-issues/sqlServerEWI#ssc-ewi-ts0079) documentation

### Description

This FDM is added when a DBCC statement is found inside the input code.  
Most DBCC statements are not supported in Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 DBCC CHECKIDENT(@a, RESEED, @b) WITH NO_INFOMSGS
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-TS0018 - DATABASE CONSOLE COMMAND 'CHECKIDENT' IS NOT SUPPORTED. **
--DBCC CHECKIDENT(@a, RESEED, @b) WITH NO_INFOMSGS
```

#### Best Practices

- No additional user actions are required; it is just informative.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0019

RAISERROR Error Message may differ because of the SQL Server string format.

### Description

This EWI is added to notify that the RAISERROR Error Message may differ because of the SQL Server string format.

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROCEDURE RAISERROR_PROCEDURE 
AS
BEGIN
RAISERROR ('This is a sample error message with the first parameter %d and the second parameter %*.*s',
           10, 
           1,
           123,
	   7,
	   7,
	   'param2');
END
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE RAISERROR_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		--** SSC-FDM-TS0019 - RAISERROR ERROR MESSAGE MAY DIFFER BECAUSE OF THE SQL SERVER STRING FORMAT **
		SELECT
			RAISERROR_UDF('This is a sample error message with the first parameter %d and the second parameter %*.*s',
			10,
			1, array_construct(
			123,
7,
7,
'param2'));
	END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0020

Default constraint was commented out and may have been added to a table definition.

### Description

This FDM is added when the default constraint is present in an Alter Table statement.

Currently, support for that constraint is unavailable. A workaround to transform it is to define the table before using Alter Table. This allows the references to be identified, and the default constraint is consolidated in the table definition. Otherwise, the constraint is only commented out.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE table1(
  col1 integer,
  col2 varchar collate Latin1_General_CS,
  col3 date
);

ALTER TABLE table1
ADD col4 integer,
  CONSTRAINT col1_constraint DEFAULT 50 FOR col1,
  CONSTRAINT col1_constraint DEFAULT (getdate()) FOR col1;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE table1 (
  col1 INTEGER DEFAULT 50,
  col2 VARCHAR COLLATE 'EN-CS',
  col3 DATE
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

ALTER TABLE table1
ADD col4 INTEGER;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD
--CONSTRAINT col1_constraint DEFAULT 50 FOR col1
                                              ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD
--CONSTRAINT col1_constraint DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP) FOR col1
                                                                              ;
```

#### Known Issues

- When different default constraints are declared over the same column, only the first will be reflected on the Create Table Statement.
- When a default constraint is declared on a missing column, the transformation cannot be performed due to the lack of dependencies.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0021

A MASKING POLICY was created as a substitute for MASKED WITH.

Note

Some parts of the output code are omitted for clarity reasons.

### Description

This EWI is added when the Alter Table statement contains a MASKED WITH clause. The reason this is added is to inform that an approximate MASKING POLICY was created as a substitute for the MASKED WITH function.

#### Code Example

##### Input Code:

Copy code

```
 ALTER TABLE table_name
ALTER COLUMN column_name
ADD MASKED WITH (FUNCTION = 'default()');
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-TS0022 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER **
CREATE OR REPLACE MASKING POLICY "default" AS
(val STRING)
RETURNS STRING ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE 'xxxxx'
END;

ALTER TABLE IF EXISTS table_name MODIFY COLUMN column_name/*** SSC-FDM-TS0021 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/  SET MASKING POLICY "default";
```

Note

The MASKING POLICY will be created previous to the ALTER TABLE statement. And it is expected to have an approximate behavior. Some tweaks might be needed in regard to roles and user privileges.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0022

The user must previously define the masking role.

Note

Some parts of the output code are omitted for clarity reasons.

### Description

This is EWI occurs when a MASKING POLICY is created and a role or privilege must be linked to it so the data masking could work properly.

#### Code Example

##### Input code

Copy code

```
 ALTER TABLE tableName
ALTER COLUMN columnName
ADD MASKED WITH (FUNCTION = 'partial(1, "xxxxx", 1)');
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-TS0022 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER **
CREATE OR REPLACE MASKING POLICY "partial_1_xxxxx_1" AS
(val STRING)
RETURNS STRING ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE LEFT(val, 1) || 'xxxxx' || RIGHT(val, 1)
END;

ALTER TABLE IF EXISTS tableName MODIFY COLUMN columnName/*** SSC-FDM-TS0021 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/  SET MASKING POLICY "partial_1_xxxxx_1";
```

Note

As shown on line 6, there is a placeholder where the defined roles can be placed. There is room for one or several values separated by commas. Also, here, the use of single quotes is mandatory for each of the values.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0023

Error function could be different in Snowflake

### Description

This EWI is added in the transformation of the following ERRORs functions due to the corresponding behavior change.

- **ERROR\_MESSAGE** The message of SQLERRM could be different in Snowflake.
- **ERROR\_STATE** The target SQLSTATE property could return a different number due to platform differences.
- **ERROR\_PROCEDURE** Transformation changed to return the stored procedure where the function is called.

#### Input Code:

Copy code

```
CREATE PROCEDURE ProcError
AS
BEGIN
Declare @ErrorState INT = ERROR_STATE();
Declare @ErrorMessage INT = ERROR_MESSAGE();
Declare @ErrorProc INT = ERROR_PROCEDURE();
Select 1;
END;
```

#### Generated Code

Copy code

```
CREATE OR REPLACE PROCEDURE ProcError ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
DECLARE
ERRORSTATE INT := SQLSTATE /*** SSC-FDM-TS0023 - ERROR STATE COULD BE DIFFERENT IN SNOWFLAKE ***/;
ERRORMESSAGE INT := SQLERRM /*** SSC-FDM-TS0023 - ERROR MESSAGE COULD BE DIFFERENT IN SNOWFLAKE ***/;
ERRORPROC INT := 'ProcError' /*** SSC-FDM-TS0023 - ERROR PROCEDURE NAME COULD BE DIFFERENT IN SNOWFLAKE ***/;
ProcedureResultSet RESULTSET;
BEGIN
 
 
 
ProcedureResultSet := (
Select 1);
RETURN TABLE(ProcedureResultSet);
END;
$$;
```

#### Recommendation

If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-TS0024

CURRENT\_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases.

### Description

This FDM is added when the `At Time Zone` has the `CURRENT_TIMESTAMP`. This is because the result might differ in some instances.

The main difference is that in SQL Server, CURRENT\_TIMESTAMP returns the current system date and time in the server time zone and in Snowflake CURRENT\_TIMESTAMP returns the current date and time in the UTC (Coordinated Universal Time) time zone.

#### Input Code:

##### Sql Server

Copy code

```
 SELECT current_timestamp at time zone 'Hawaiian Standard Time';
```

##### Result

`2024-02-08 16:52:55.317 -10:00`

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
CONVERT_TIMEZONE('Pacific/Honolulu', CURRENT_TIMESTAMP() /*** SSC-FDM-TS0024 - CURRENT_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases ***/);
```

##### Result

`2024-02-08 06:53:46.994 -1000`

#### Best Practices

This is an example if you want to keep the same format in Snowflake.

##### SQL Server

Copy code

```
 SELECT current_timestamp at time zone 'Hawaiian Standard Time';
```

##### Result

`2024-02-08 16:33:49.143 -10:00`

In Snowflake you can use [ALTER SESSION](https://docs.snowflake.com/en/sql-reference/sql/alter-session) to change the default time zone. For example:

##### Snowflake

Copy code

```
 ALTER SESSION SET TIMEZONE = 'Pacific/Honolulu';

SELECT
CONVERT_TIMEZONE('Pacific/Honolulu', 'UTC', CURRENT_TIMESTAMP());
```

##### Result

`2024-02-08 16:33:49.143`

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0025

DB\_ID\_UDF may have a different behavior in certain cases.

### Description

This FDM is added to clarify that the DB\_ID\_UDF tries to emulate the [DB\_ID](https://learn.microsoft.com/en-us/sql/t-sql/functions/db-id-transact-sql?view=sql-server-ver16) SqlServer function as well as possible. In SqlServer, the identifier assigned to a database is unique, and if the database is deleted, this ID won’t ever be used again; otherwise, in Snowflake, this identifier corresponds to the number assigned to the database when it is created; it is also unique, but it is a consecutive number which means that if this database is deleted, this number is going to be assigned to the database that was created after the deleted one.

#### Input Code:

##### Sql Server

Copy code

```
 SELECT DB_ID('my_database');
```

##### Result

`6`

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
DB_ID_UDF('my_database') /*** SSC-FDM-TS0025 - DB_ID_UDF MAY HAVE A DIFFERENT BEHAVIOR IN CERTAIN CASES ***/;
```

##### Result

`6`

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0026

DELETE case is not being considered in the temporary table

### Description

There is an INSERT statement pattern that requires a specific transformation, which involves the creation of a temporary table. This FDM notifies that the DELETE case is not considered in the transformation mentioned. Please visit [INSERT with Table DML Factor with MERGE as DML](../../translation-references/transact/transact-dmls#insert) to get more information about this pattern.

#### Input Code:

##### Sql Server

Copy code

```
 INSERT INTO T3
SELECT
	col1,
  col2
FROM (
  MERGE T1 USING T2
  	ON T1.col1 = T2.col1
  WHEN NOT MATCHED THEN
    INSERT VALUES ( T2.col1, T2.col2 )
  WHEN MATCHED THEN
    UPDATE SET T1.col2 = t2.col2
  OUTPUT
  	$action ACTION_OUT,
    T2.col1,
    T2.col2
) AS MERGE_OUT
 WHERE ACTION_OUT='UPDATE';
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-TS0026 - DELETE CASE IS NOT BEING CONSIDERED, PLEASE CHECK IF THE ORIGINAL MERGE PERFORMS IT **
CREATE OR REPLACE TEMPORARY TABLE MERGE_OUT AS
	SELECT
		CASE
			WHEN T1.$1 IS NULL
				THEN 'INSERT'
			ELSE 'UPDATE'
		END ACTION_OUT,
		T2.col1,
		T2.col2
	FROM
		T2
		LEFT JOIN
			T1
			ON T1.col1 = T2.col1;

MERGE INTO T1
USING T2
ON T1.col1 = T2.col1
WHEN NOT MATCHED THEN
	   INSERT VALUES (T2.col1, T2.col2)
WHEN MATCHED THEN
	UPDATE SET
		T1.col2 = t2.col2
		!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - OUTPUT CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
		OUTPUT
			$action ACTION_OUT,
		  T2.col1,
		  T2.col2 ;

		INSERT INTO T3
		SELECT
	col1,
	col2
		FROM
	MERGE_OUT
		WHERE
	ACTION_OUT ='UPDATE';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0027

SET ANSI\_NULLS ON statement may have a different behavior in Snowflake

### Description

This FDM notifies that the SET ANSI\_NULLS ON statement may behave differently in Snowflake. For more information about this statement,
go to the [ANSI\_NULLS](../../translation-references/transact/transact-ansi-nulls) article.

#### Input Code

Copy code

```
 SET ANSI_NULLS ON;
```

##### Generated Code

Copy code

```
 ----** SSC-FDM-TS0027 - SET ANSI_NULLS ON STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE **
--SET ANSI_NULLS ON
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0028

Output parameters must have the same order as they appear in the executed code

### Description

This FDM notifies that the output parameters in the SP\_EXECUTESQL statement must be in the same order as they appear in the SQL string to execute. Otherwise, the output values will not be correctly assigned.

### Code Example

#### Correct case

As can be seen, `@MaxAgeOUT` and `@MaxIdOU`T appear in the same order in both the SQL string and the output parameters.

Thus, when converting the code, the `SELECT $1, $2 INTO :MAXAGE, :MAXID FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))` will assign the values correctly.

##### Transact

Copy code

```
 CREATE PROCEDURE CORRECT_OUTPUT_PARAMS_ORDER
AS
BEGIN
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    EXECUTE sp_executesql
        N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE ID < @id AND AGE < @age;',
        N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT',
        30,
        100,
        @MaxAgeOUT = @MaxAge OUTPUT,
        @MaxIdOut = @MaxId OUTPUT;

    SELECT @MaxAge, @MaxId;
END
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE CORRECT_OUTPUT_PARAMS_ORDER ()
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
   ID < @id AND AGE < @age;', '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT', ARRAY_CONSTRUCT('', '', 'MAXAGEOUT', 'MAXIDOUT'), ARRAY_CONSTRUCT(
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
```

#### Problematic case

As can be seen, `@MaxAgeOUT` and `@MaxIdOUT` in the output parameters appear in a different order compared to the SQL string.

Thus, when converting the code, the `SELECT $1, $2 INTO :MAXID, :MAXAGE FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))` will assign the values incorrectly. `Max(AGE)` will be assigned to `:MAXID` and `Max(ID)` to `:MAXAGE`.

This needs to be manually fixed by either changing the order of the output parameters in the SELECT INTO statement or by changing the order in the SQL string.

##### Transact

Copy code

```
 CREATE PROCEDURE INCORRECT_OUTPUT_PARAMS_ORDER
AS
BEGIN
    DECLARE @MaxAge INT;
    DECLARE @MaxId INT;

    EXECUTE sp_executesql
        N'SELECT @MaxAgeOUT = max(AGE), @MaxIdOut = max(ID) FROM PERSONS WHERE ID < @id AND AGE < @age;',
        N'@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT',
        30,
        100,
        @MaxIdOut = @MaxId OUTPUT,
        @MaxAgeOUT = @MaxAge OUTPUT;

    SELECT @MaxAge, @MaxId;
END
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE INCORRECT_OUTPUT_PARAMS_ORDER ()
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
   ID < @id AND AGE < @age;', '@age INT, @id INT, @MaxAgeOUT INT OUTPUT, @MaxIdOUT INT OUTPUT', ARRAY_CONSTRUCT('', '', 'MAXIDOUT', 'MAXAGEOUT'), ARRAY_CONSTRUCT(
    30,
    100, :MAXID, :MAXAGE));
    --** SSC-FDM-TS0028 - OUTPUT PARAMETERS MUST HAVE THE SAME ORDER AS THEY APPEAR IN THE EXECUTED CODE **
    SELECT
      $1,
      $2
    INTO
      :MAXID,
      :MAXAGE
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    ProcedureResultSet := (
    SELECT
      :MAXAGE,
      :MAXID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

### Best Practices

- Make sure the OUTPUT parameters are in the same order as they appear in the SQL string.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0029

SET NOCOUNT statement is commented out, which is not applicable in Snowflake.

### Description

When a `SET NOCOUNT` statement is encountered, this FDM is added and the statement is commented out because it is not relevant in the Snowflake environment.

### Code example

#### Input Code:

Copy code

```
 SET NOCOUNT ON;
```

##### Generated Code

Copy code

```
 ----** SSC-FDM-TS0029 - SET NOCOUNT STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--SET NOCOUNT ON
```

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0030

SET ANSI\_PADDING ON statement is commented out, which is equivalent in Snowflake.

### Description

Snowflake always preserves trailing spaces in string values when they are inserted into columns. This behavior is equivalent to `SET ANSI_PADDING ON` in SQL Server. Therefore, when a `SET ANSI_PADDING ON` statement is encountered, this FDM is added and the statement is commented out.

Note

When `SET ANSI_PADDING OFF` is encountered instead, [SSC-EWI-TS0002](../conversion-issues/sqlServerEWI#ssc-ewi-ts0002) is raised because `ANSI_PADDING OFF` behavior cannot be replicated in Snowflake. In SQL Server, `ANSI_PADDING` is a column-level storage property set at column creation time, not a session-level behavior. See SSC-EWI-TS0002 for details on the limitations and recommended manual remediation steps.

### Code example

#### Input Code:

Copy code

```
 SET ANSI_PADDING ON;
```

##### Generated Code

Copy code

```
 ----** SSC-FDM-TS0030 - SET ANSI_PADDING ON STATEMENT IS COMMENTED OUT, WHICH IS EQUIVALENT IN SNOWFLAKE. **
--SET ANSI_PADDING ON
```

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0031

SET ANSI\_WARNINGS ON statement is commented out because Snowflake generally adheres to ANSI-standard behaviors.

### Description

Snowflake generally behaves as if `ANSI_WARNINGS` is `ON` by default, especially concerning error handling for arithmetic overflow, division by zero, and string truncation. You typically don’t need to explicitly “set” an equivalent to `ANSI_WARNINGS` in Snowflake. Therefore, when a `SET ANSI_WARNINGS ON` statement is encountered, this FDM is added and the statement is commented out.

### Code example

#### Input Code:

Copy code

```
 SET ANSI_WARNINGS ON;
```

##### Generated Code

Copy code

```
 ----** SSC-FDM-TS0031 - SET ANSI_WARNINGS ON STATEMENT IS COMMENTED OUT, WHICH SNOWFLAKE GENERALLY ADHERES TO ANSI-STANDARD BEHAVIORS. **
--SET ANSI_WARNINGS ON
```

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0032

IDENTITY column property not supported in CREATE TABLE AS STATEMENT, emulated using ROW\_NUMBER().

### Description

Snowflake does not have a direct way to perform a CREATE TABLE AS with an identity column. Although SnowConvert adds a ROW\_NUMBER column instead of the IDENTITY to simulate the enumeration of the identity. This transformation does not create an identity column, which means rows inserted after creation won’t be automatically incremented.

### Code example

#### Input Code:

Copy code

```
with peers as
(
    select
    *
    from (
    values
        ('Luis', 'Miguel'),
        ('Cory', 'Wong'),
        ('Steve', 'Vai'),
        ('John', 'Petrucci'),
        ('Paul', 'Gilbert')
    ) as info(name, lastname)
)
select
    rowm = IDENTITY(int,1,1),
    *
into #MYTABLE
from peers;
```

##### Generated Code

Copy code

```
:force: 

--** SSC-FDM-TS0032 - IDENTITY COLUMN PROPERTY NOT SUPPORTED IN CREATE TABLE AS STATEMENT, EMULATED WITH USING ROW_NUMBER **
CREATE OR REPLACE TEMPORARY TABLE T_MYTABLE AS
     WITH peers as
(
    select
     *
    from (
    values
        ('Luis', 'Miguel'),
        ('Cory', 'Wong'),
        ('Steve', 'Vai'),
        ('John', 'Petrucci'),
        ('Paul', 'Gilbert')
    ) as info (
      name,
      lastname
     )
)
     SELECT
    ROW_NUMBER()
    OVER (
    ORDER BY
     NULL) AS rowm,
    *
from
    peers;
```

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0033

SET QUOTED\_IDENTIFIER STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE.

### Description

**SQL Server Behavior**

In SQL Server, SET QUOTED\_IDENTIFIER ON is a syntax setting that is separate from collation. The database’s or column’s collation (for example, \_CI for Case-Insensitive or \_CS for Case-Sensitive) dictates whether quoted identifiers are case-sensitive or not. If a database has a \_CI collation, then “MyColumn” and “mycolumn” are treated as the same.

**Snowflake Behavior**

In Snowflake, the behavior is simpler and more strict:

Unquoted Identifiers: Automatically stored and resolved in all uppercase, making them case-insensitive (mytable is the same as MYTABLE).

Quoted Identifiers: By default, identifiers enclosed in double quotes (“MyColumn”) are case-sensitive. They are stored exactly as you typed them.

### Code example

#### Input Code:

Copy code

```
SET QUOTED_IDENTIFIER ON
GO

-- the table is defined as "Products Test"
-- this query will work because the case is ignored.
select
*
from [products test];

SET QUOTED_IDENTIFIER OFF

-- this query will fail because the case is preserved
select
*
from [products test];
GO
```

##### Generated Code

Copy code

```
:force: 

----** SSC-FDM-TS0033 - SET QUOTED_IDENTIFIER STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE **
--SET QUOTED_IDENTIFIER ON

-- the table is defined as "Products Test"
-- this query will work because the case is ignored.
select
  *
from
  "products test";

----** SSC-FDM-TS0033 - SET QUOTED_IDENTIFIER STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE **
--SET QUOTED_IDENTIFIER OFF

-- this query will fail because the case is preserved
select
  *
from
  "products test";
```

**How to Achieve Equivalence in Snowflake**

To get the same case-insensitive behavior for quoted identifiers as in SQL Server, you can set the QUOTED\_IDENTIFIERS\_IGNORE\_CASE session parameter to TRUE in Snowflake.

Copy code

```
-- This will make quoted identifiers case-insensitive for the session
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE;

-- Now, this query will succeed
select
  *
from
  "products test";
```

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0034

### Description

This FDM is generated when a `DATA_COMPRESSION` clause is encountered in a `CREATE TABLE` or `ALTER TABLE` statement. In SQL Server, `DATA_COMPRESSION` is used to specify whether data should be compressed (using ROW or PAGE compression) to reduce storage space and improve I/O performance. **Snowflake automatically handles data compression** using its proprietary compression algorithms, making the `DATA_COMPRESSION` clause unnecessary and unsupported. SnowConvert comments out the `DATA_COMPRESSION` clause during conversion.

### Example Code

#### Input (SQL Server):

Copy code

```
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Department NVARCHAR(50),
    Salary DECIMAL(10, 2)
)
WITH (DATA_COMPRESSION = PAGE);
```

#### Output (Snowflake):

Copy code

```
CREATE OR REPLACE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Department NVARCHAR(50),
    Salary DECIMAL(10, 2)
)
--WITH (
----  --** SSC-FDM-TS0034 - DATA_COMPRESSION IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--  DATA_COMPRESSION = PAGE
--)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/06/2025",  "domain": "no-domain-provided",  "migrationid": "sFmaAZAnCnm6VvGeJrE4BQ==" }}'
;
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0035

Triggers are not supported in Snowflake. ENABLE/DISABLE trigger operation is out of translation scope.

### Description

Triggers are not supported in Snowflake. In SQL Server, ENABLE TRIGGER and DISABLE TRIGGER operations control whether a trigger fires when its triggering event occurs. Since Snowflake does not have an equivalent trigger mechanism, these operations are out of translation scope. When an `ALTER TABLE ... ENABLE TRIGGER` or `ALTER TABLE ... DISABLE TRIGGER` statement is encountered, the entire statement is commented out and this issue is generated.

#### Code Example

##### Input Code:

Copy code

```
ALTER TABLE Employees
ENABLE TRIGGER AuditEmployeeChanges;
GO
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TS0035 - TRIGGERS ARE NOT SUPPORTED IN SNOWFLAKE. ENABLE TRIGGER OPERATION IS OUT OF THE TRANSLATION SCOPE OF SNOWCONVERT AI. **
--ALTER TABLE IF EXISTS Employees ENABLE TRIGGER
--  AuditEmployeeChanges
        ;
```

#### Best Practices

- **Review trigger dependencies:** Identify all triggers that were enabled or disabled in the source SQL Server code and document their business logic. Determine whether that logic should be implemented as Snowflake streams and tasks, stored procedures, or application-layer logic.
- **Consider Snowflake streams and tasks:** Snowflake’s [streams](https://docs.snowflake.com/en/user-guide/streams-intro) capture change data on tables, and [tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) can be scheduled to process that data — together they provide event-driven behavior similar to SQL Server triggers.
- **Remove commented-out statements:** After migrating the trigger logic to Snowflake-native constructs, remove the commented-out ENABLE/DISABLE TRIGGER statements to keep the codebase clean.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0036

HOST\_NAME replaced with CURRENT\_IP\_ADDRESS, which returns the client IP address instead of the workstation name.

### Description

This FDM is generated when the `HOST_NAME()` function is encountered. In SQL Server, `HOST_NAME()` returns the workstation name of the client connection. Snowflake does not have a direct equivalent; `CURRENT_IP_ADDRESS()` is used as the closest alternative, but it returns the client’s IP address rather than the hostname. This is a functional difference because the returned values have different formats and semantics.

#### Code Example

##### Input Code:

Copy code

```
SELECT HOST_NAME();
```

##### Generated Code:

Copy code

```
SELECT
    CURRENT_IP_ADDRESS() /*** SSC-FDM-TS0036 - HOST_NAME REPLACED WITH CURRENT_IP_ADDRESS, WHICH RETURNS THE CLIENT IP ADDRESS INSTEAD OF THE WORKSTATION NAME ***/;
```

#### Best Practices

- If your application uses `HOST_NAME()` for auditing or logging, verify that the IP address provides sufficient information for your use case.
- If the workstation name is required, consider passing it as a session parameter via `ALTER SESSION SET` or storing it in a context variable.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0037

SET statement is not applicable in Snowflake as it has equivalent default behavior.

### Description

This FDM is generated when a `SET` statement whose specified value matches Snowflake’s default behavior is encountered. For example, `SET CONCAT_NULL_YIELDS_NULL ON` is the default in Snowflake (NULL concatenation yields NULL), `SET NUMERIC_ROUNDABORT OFF` matches Snowflake’s default of not raising errors on precision loss, and `SET ARITHABORT ON/OFF` has no behavioral impact in Snowflake. Since the setting is already the default, the statement is commented out.

#### Code Example

##### Input Code:

Copy code

```
SET CONCAT_NULL_YIELDS_NULL ON;
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TS0037 - SET CONCAT_NULL_YIELDS_NULL ON STATEMENT IS NOT APPLICABLE IN SNOWFLAKE AS IT HAS EQUIVALENT DEFAULT BEHAVIOR. **
--SET CONCAT_NULL_YIELDS_NULL ON;
```

#### Best Practices

- No action is required — the commented-out statement reflects behavior that is already the default in Snowflake.
- If the non-default value of the same option is used elsewhere (e.g., `SET CONCAT_NULL_YIELDS_NULL OFF`), that will generate a separate EWI (SSC-EWI-TS0089) because the non-default behavior cannot be replicated.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

- [SSC-EWI-TS0089](../conversion-issues/sqlServerEWI#ssc-ewi-ts0089): SET statement not supported in Snowflake (for non-default values).

## SSC-FDM-TS0038

Agent Job migrated to Snowflake Task orchestration.

### Description

This FDM is generated when an `sp_add_job` call is encountered that creates a SQL Server Agent Job containing SSIS package steps. The Agent Job definition is migrated to a Snowflake Task orchestration model. The original `sp_add_job` call is commented out and replaced with generated orchestration files in the `ETL/AGENTJOBS/` output directory. The generated output includes Snowflake Task definitions, orchestrator stored procedures, and schedule mappings.

#### Code Example

##### Input Code:

Copy code

```
DECLARE @jobId BINARY(16);
EXEC msdb.dbo.sp_add_job
    @job_name = N'ETL_Nightly_Load',
    @enabled = 1,
    @job_id = @jobId OUTPUT;
```

##### Generated Code:

Copy code

```
DECLARE
  JOBID BINARY(16);
BEGIN
--  --** SSC-FDM-TS0038 - AGENT JOB 'ETL_Nightly_Load' MIGRATED TO SNOWFLAKE TASK ORCHESTRATION. GENERATED OUTPUT IN ETL/AGENTJOBS/. **
--  EXEC msdb.dbo.sp_add_job @job_name = N'ETL_Nightly_Load', @enabled = 1, @job_id = @jobId OUTPUT
                                                                                                 ;
END;
```

#### Best Practices

- Review the generated files in the `ETL/AGENTJOBS/` output directory. These include Snowflake Task definitions and orchestrator stored procedures that replace the Agent Job.
- Validate the task scheduling and step ordering match your original Agent Job configuration.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0039

Agent Job schedule mapped to CRON expression in Snowflake Task.

### Description

This FDM is generated when an `sp_add_jobschedule` or `sp_add_schedule`/`sp_attach_schedule` call is encountered that defines a schedule for a SQL Server Agent Job. The schedule parameters (`freq_type`, `freq_interval`, `active_start_time`) are mapped to a CRON expression for use in the corresponding Snowflake Task definition. The original schedule call is commented out.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_add_jobschedule
    @job_id = @jobId,
    @name = N'Nightly_2AM',
    @enabled = 1,
    @freq_type = 4,
    @freq_interval = 1,
    @active_start_time = 020000;
```

##### Generated Code:

Copy code

```
--  --** SSC-FDM-TS0039 - AGENT JOB SCHEDULE 'Nightly_2AM' MAPPED TO CRON EXPRESSION IN SNOWFLAKE TASK. **
--  EXEC msdb.dbo.sp_add_jobschedule @job_id = @jobId, @name = N'Nightly_2AM', @enabled = 1, @freq_type = 4, @freq_interval = 1, @active_start_time = 020000
                                                                                                                                                          ;
```

#### Best Practices

- Verify the generated CRON expression in the Snowflake Task definition matches your intended schedule. Complex SQL Server schedules (e.g., monthly on specific days, bi-weekly) may need manual adjustment.
- Review the `ETL/AGENTJOBS/` output for the generated `CREATE TASK ... SCHEDULE = 'USING CRON ...'` statement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0040

Agent Job step migrated to orchestrator Stored Procedure.

### Description

This FDM is generated when an `sp_add_jobstep` call is encountered for an Agent Job step with a `TSQL` or `SSIS` subsystem. The step is migrated to an orchestrator stored procedure that is generated in the `ETL/AGENTJOBS/` output directory. The original `sp_add_jobstep` call is commented out. For SSIS steps, the SSIS package is also processed through the ETL-to-dbt pipeline.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_add_jobstep
    @job_name = N'ETL_Nightly_Load',
    @step_name = N'LoadSalesData',
    @step_id = 1,
    @subsystem = N'SSIS',
    @command = N'/ISSERVER "SalesETL.dtsx"';
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TS0040 - AGENT JOB STEP 'LoadSalesData' (SSIS) MIGRATED TO ORCHESTRATOR STORED PROCEDURE. GENERATED OUTPUT IN ETL/AGENTJOBS/. **
--EXEC msdb.dbo.sp_add_jobstep @job_name = N'ETL_Nightly_Load', @step_name = N'LoadSalesData', @step_id = 1, @subsystem = N'SSIS', @command = N'/ISSERVER "SalesETL.dtsx"'
```

#### Best Practices

- Review the generated orchestrator stored procedure in `ETL/AGENTJOBS/` to ensure the step logic is correctly translated.
- For SSIS steps, also review the generated dbt models and SQL files produced by the ETL-to-dbt pipeline.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0041

sp\_delete\_job translated to DROP TASK IF EXISTS.

### Description

This FDM is generated when an `sp_delete_job` call is encountered for a SQL Server Agent Job that has been migrated to a Snowflake Task. The `sp_delete_job` call is translated to a `DROP TASK IF EXISTS` statement targeting the corresponding Snowflake Task. The task name is derived from the original job name with a `TASK_` prefix and uppercase formatting.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_delete_job
    @job_name = N'ETL_Nightly_Load';
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TS0041 - SP_DELETE_JOB FOR AGENT JOB 'ETL_Nightly_Load' TRANSLATED TO DROP TASK IF EXISTS. **
DROP TASK IF EXISTS TASK_ETL_NIGHTLY_LOAD;
```

#### Best Practices

- Verify that the task name `TASK_{JOB_NAME}` matches the task created by the Agent Job migration (SSC-FDM-TS0038).
- Note that dropping a task in Snowflake also removes its schedule. If the task has dependent tasks, those must be updated separately.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0042

sp\_start\_job translated to EXECUTE TASK.

### Description

This FDM is generated when an `sp_start_job` call is encountered for a SQL Server Agent Job that has been migrated to a Snowflake Task. The call is translated to an `EXECUTE TASK` statement that triggers the corresponding Snowflake Task immediately, regardless of its schedule.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_start_job
    @job_name = N'ETL_Nightly_Load';
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TS0042 - SP_START_JOB FOR AGENT JOB 'ETL_Nightly_Load' TRANSLATED TO EXECUTE TASK. **
EXECUTE TASK TASK_ETL_NIGHTLY_LOAD;
```

#### Best Practices

- `EXECUTE TASK` triggers a single immediate run of the task. It does not affect the task’s schedule or resume/suspend state.
- Ensure the task has been created and is in a `STARTED` state if you also need it to run on schedule.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0043

sp\_stop\_job translated to ALTER TASK SUSPEND.

### Description

This FDM is generated when an `sp_stop_job` call is encountered for a SQL Server Agent Job that has been migrated to a Snowflake Task. The call is translated to `ALTER TASK ... SUSPEND`, which prevents future scheduled runs of the task. Note that `ALTER TASK SUSPEND` does not stop an already-running execution — it only prevents future runs from being triggered.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_stop_job
    @job_name = N'ETL_Nightly_Load';
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TS0043 - SP_STOP_JOB FOR AGENT JOB 'ETL_Nightly_Load' TRANSLATED TO ALTER TASK SUSPEND. NOTE: THIS PREVENTS FUTURE RUNS BUT CANNOT STOP AN IN-PROGRESS EXECUTION. **
EXECUTE IMMEDIATE 'ALTER TASK TASK_ETL_NIGHTLY_LOAD SUSPEND';
```

#### Best Practices

- Be aware that `ALTER TASK SUSPEND` only prevents future scheduled executions. If the task is currently running, the in-progress execution will complete.
- In SQL Server, `sp_stop_job` attempts to cancel an in-progress job step. This capability does not exist in Snowflake’s Task model.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0044

sp\_update\_job @enabled translated to ALTER TASK RESUME or SUSPEND.

### Description

This FDM is generated when an `sp_update_job` call is encountered with the `@enabled` parameter for a SQL Server Agent Job that has been migrated to a Snowflake Task. When `@enabled=1`, the call is translated to `ALTER TASK ... RESUME` (starts the task’s schedule). When `@enabled=0`, it is translated to `ALTER TASK ... SUSPEND` (pauses the task’s schedule).

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_update_job
    @job_name = N'ETL_Nightly_Load',
    @enabled = 0;
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TS0044 - SP_UPDATE_JOB @ENABLED FOR AGENT JOB 'ETL_Nightly_Load' TRANSLATED TO ALTER TASK RESUME/SUSPEND. **
EXECUTE IMMEDIATE 'ALTER TASK TASK_ETL_NIGHTLY_LOAD SUSPEND';
```

#### Best Practices

- Verify that `RESUME` and `SUSPEND` map correctly to your intended enable/disable behavior.
- If `sp_update_job` is called with parameters other than `@enabled` (e.g., `@description`), those calls will generate SSC-EWI-TS0093 instead, as metadata updates are not applicable in Snowflake’s Task model.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0046

Rowversion/timestamp data type auto-generates unique values in SQL Server but not in Snowflake.

#### Description

This FDM is generated when a column with the [`ROWVERSION`](https://learn.microsoft.com/en-us/sql/t-sql/data-types/rowversion-transact-sql?view=sql-server-ver16) or `TIMESTAMP` data type is encountered (they are synonyms in SQL Server). In SQL Server, these data types automatically generate unique binary values on every `INSERT` and `UPDATE`, providing a mechanism for optimistic concurrency control. The type is mapped to `BINARY(8)`, which preserves the storage format but does not replicate the auto-generation behavior.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    RowVer ROWVERSION
);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Orders (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    RowVer BINARY(8) /*** SSC-FDM-TS0046 - ROWVERSION/TIMESTAMP DATA TYPE AUTO-GENERATES UNIQUE VALUES ON INSERT AND UPDATE IN SQL SERVER. THIS BEHAVIOR IS NOT REPLICATED IN SNOWFLAKE BINARY(8). ***/
)
;
```

#### Best Practices

- If your application uses `ROWVERSION` for optimistic concurrency control, implement an alternative pattern in Snowflake. Options include:
  - A `NUMBER` column with a Snowflake sequence, updated via a stream/task or stored procedure on each modification.
  - A `TIMESTAMP_NTZ` column set to `CURRENT_TIMESTAMP()` on insert/update using a default value and a stream-triggered task.
- If the column is only used for auditing (not concurrency), a `TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()` column may suffice.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0047

SET IDENTITY\_INSERT commented out.

#### Description

In SQL Server, [`SET IDENTITY_INSERT`](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-identity-insert-transact-sql?view=sql-server-ver16) controls whether explicit values can be inserted into the identity column of a table. When set to `ON`, it allows explicit inserts; when set to `OFF` (the default), it prevents them.

In Snowflake, there is no equivalent statement because explicit inserts into `IDENTITY` / `AUTOINCREMENT` columns are **always allowed by default**. However, unlike SQL Server, the underlying sequence counter in Snowflake does not adjust to account for explicitly inserted values, which may lead to duplicate key conflicts on subsequent inserts.

The `SET IDENTITY_INSERT` statement is commented out and this FDM is attached with a context-specific reason depending on whether the original statement was `ON` or `OFF`.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SET IDENTITY_INSERT dbo.MyTable ON;

SET IDENTITY_INSERT dbo.MyTable OFF;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0047 - SET IDENTITY_INSERT COMMENTED OUT. SNOWFLAKE ALLOWS EXPLICIT INSERTS INTO IDENTITY/AUTOINCREMENT COLUMNS BY DEFAULT, BUT THE SEQUENCE COUNTER DOES NOT ADJUST TO EXPLICITLY INSERTED VALUES. **
--SET IDENTITY_INSERT dbo.MyTable ON;

----** SSC-FDM-TS0047 - SET IDENTITY_INSERT COMMENTED OUT. SNOWFLAKE DOES NOT SUPPORT RESTRICTING EXPLICIT INSERTS INTO IDENTITY/AUTOINCREMENT COLUMNS. **
--SET IDENTITY_INSERT dbo.MyTable OFF;
```

#### Best Practices

- After migration, verify that any tables with `IDENTITY` / `AUTOINCREMENT` columns do not experience duplicate key conflicts caused by the sequence counter not reflecting explicitly inserted values.
- After explicitly inserting values into an identity column in Snowflake, manually adjust the underlying sequence to avoid conflicts: `ALTER SEQUENCE seq_name SET START = <max_inserted_value + increment>`.
- If you rely on toggling `IDENTITY_INSERT` in batch load scripts, remove the `SET` statements and add a sequence adjustment step at the end of the batch.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0048

SP\_ADD\_CATEGORY translated to Snowflake TAG definition.

#### Description

This FDM indicates that SnowConvert AI translated a SQL Server Agent Job category with class `JOB` into a Snowflake tag definition.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
EXEC msdb.dbo.sp_add_category @class=N'JOB', @type=N'LOCAL', @name=N'Data Collector';
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0048 - SP_ADD_CATEGORY TRANSLATED TO SNOWFLAKE TAG DEFINITION. **
--EXEC msdb.dbo.sp_add_category @class = N'JOB', @type = N'LOCAL', @name = N'Data Collector'
                                                                                          ;

EXECUTE IMMEDIATE 'CREATE TAG IF NOT EXISTS JOB_CATEGORY ALLOWED_VALUES 'Data Collector'';
```

#### Best Practices

- Review the generated tag name and allowed values against your Snowflake governance model.
- Grant the required tag privileges before running the generated statement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0049

SP\_SEND\_DBMAIL translated to SNOWFLAKE NOTIFICATION. Requires a NOTIFICATION INTEGRATION to be configured.

#### Description

This FDM indicates that SnowConvert AI translated `sp_send_dbmail` to `SYSTEM$SEND_SNOWFLAKE_NOTIFICATION`. The generated call requires a configured Snowflake email notification integration.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
EXEC msdb.dbo.sp_send_dbmail
  @recipients=N'admin@company.com',
  @subject=N'ETL Failed',
  @body=N'Pipeline failed.';
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0049 - SP_SEND_DBMAIL TRANSLATED TO SNOWFLAKE NOTIFICATION. REQUIRES A NOTIFICATION INTEGRATION TO BE CONFIGURED. **
--EXEC msdb.dbo.sp_send_dbmail @recipients = N'admin@company.com', @subject = N'ETL Failed', @body = N'Pipeline failed.';

CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('Pipeline failed.'),
  SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG('<your_email_notification_integration>', 'ETL Failed', ARRAY_CONSTRUCT('admin@company.com')));
```

#### Best Practices

- Replace the notification-integration placeholder with a configured integration.
- Validate recipient restrictions, message content, and error handling in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0050

@BODY\_FORMAT=’HTML’ translated to SNOWFLAKE.NOTIFICATION.TEXT\_HTML. HTML rendering may differ between SQL Server Database Mail and Snowflake email notifications.

#### Description

This FDM indicates that an HTML Database Mail body was translated to `SNOWFLAKE.NOTIFICATION.TEXT_HTML`. Email-client rendering and supported HTML may differ from SQL Server Database Mail.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
EXEC msdb.dbo.sp_send_dbmail
  @recipients=N'admin@company.com',
  @subject=N'Report',
  @body=N'<h1>Report</h1>',
  @body_format=N'HTML';
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0050 - @BODY_FORMAT='HTML' TRANSLATED TO SNOWFLAKE.NOTIFICATION.TEXT_HTML. HTML RENDERING MAY DIFFER BETWEEN SQL SERVER DATABASE MAIL AND SNOWFLAKE EMAIL NOTIFICATIONS. **
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_HTML('<h1>Report</h1>'),
  SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG('<your_email_notification_integration>', 'Report', ARRAY_CONSTRUCT('admin@company.com')));
```

#### Best Practices

- Send a test notification and verify rendering in supported email clients.
- Keep the HTML body self-contained and avoid features unsupported by email clients.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0051

Agent Job ‘Cleanup\_Temp\_Tables’ recognized but no SSIS steps found. No Snowflake Task orchestration generated.

#### Description

This FDM indicates that SnowConvert AI recognized a SQL Server Agent Job but found no SSIS steps from which to generate Snowflake Task orchestration.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
DECLARE @jobId BINARY(16);
EXEC msdb.dbo.sp_add_job @job_name=N'Cleanup_Temp_Tables', @enabled=1, @job_id=@jobId OUTPUT;
EXEC msdb.dbo.sp_add_jobstep @job_id=@jobId, @step_name=N'Step1', @subsystem=N'TSQL', @command=N'SELECT 1';
```

##### Output Code:

##### Snowflake

Copy code

```
DECLARE
  JOBID BINARY(16);
BEGIN
--  --** SSC-FDM-TS0051 - AGENT JOB 'Cleanup_Temp_Tables' RECOGNIZED BUT NO SSIS STEPS FOUND. NO SNOWFLAKE TASK ORCHESTRATION GENERATED. **
--  EXEC msdb.dbo.sp_add_job @job_name = N'Cleanup_Temp_Tables', @enabled = 1, @job_id = @jobId OUTPUT
  ;
  CALL msdb.dbo.sp_add_jobstep(:JOBID, 'Step1', 'TSQL', 'SELECT 1');
END;
```

#### Best Practices

- Inventory the job’s non-SSIS steps and migrate them to Snowflake tasks, procedures, or external orchestration.
- Confirm that omitting task generation does not leave an operational dependency unresolved.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0052

sp\_send\_dbmail parameters not translated: @query, @attach\_query\_result\_as\_file. These parameters have no equivalent in Snowflake SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION.

#### Description

This FDM indicates that SnowConvert AI dropped one or more `sp_send_dbmail` parameters because `SYSTEM$SEND_SNOWFLAKE_NOTIFICATION` has no equivalent options. `@recipients`, `@subject`, `@body`, and `@body_format` drive the generated notification call; `@profile_name` and `@importance` are not reported. Every other parameter of the original call is listed in this message and dropped.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
EXEC msdb.dbo.sp_send_dbmail
  @recipients=N'admin@company.com',
  @subject=N'Daily Report',
  @body=N'See attached results.',
  @query=N'SELECT COUNT(*) FROM dbo.Orders',
  @attach_query_result_as_file=1;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0049 - SP_SEND_DBMAIL TRANSLATED TO SNOWFLAKE NOTIFICATION. REQUIRES A NOTIFICATION INTEGRATION TO BE CONFIGURED. **
----** SSC-FDM-TS0052 - SP_SEND_DBMAIL PARAMETERS NOT TRANSLATED: @query, @attach_query_result_as_file. THESE PARAMETERS HAVE NO EQUIVALENT IN SNOWFLAKE SYSTEM$SEND_SNOWFLAKE_NOTIFICATION. **
--EXEC msdb.dbo.sp_send_dbmail
--  @recipients=N'admin@company.com',
--  @subject=N'Daily Report',
--  @body=N'See attached results.',
--  @query=N'SELECT COUNT(*) FROM dbo.Orders',
--  @attach_query_result_as_file=1
                                ;

CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('See attached results.'), SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG('<your_email_notification_integration>', 'Daily Report', ARRAY_CONSTRUCT('admin@company.com')));
```

#### Best Practices

- Review the listed parameters and reproduce any required behavior in surrounding Snowflake or orchestration logic.
- Validate priority, attachments, query-result formatting, and profile-dependent behavior separately.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0053

WITH CHECK clause removed. Snowflake constraints are informational only and not enforced.

### Description

This message is shown when an `ALTER TABLE ... WITH CHECK ADD CONSTRAINT ... FOREIGN KEY ...` statement is converted. The `WITH CHECK` clause is removed because Snowflake constraints are informational and are not enforced, so the validation semantics do not apply.

#### Code Example

##### Input Code:

Copy code

```
ALTER TABLE dAccount
WITH CHECK ADD CONSTRAINT testFK
FOREIGN KEY (account_id) REFERENCES dInvoiceAccounts (account_id);
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TS0053 - WITH CHECK CLAUSE REMOVED, SNOWFLAKE CONSTRAINTS ARE INFORMATIONAL ONLY AND NOT ENFORCED **
ALTER TABLE dAccount ADD CONSTRAINT testFK FOREIGN KEY (account_id) REFERENCES dInvoiceAccounts (account_id);
```

#### Best Practices

- Review whether the source workflow depended on SQL Server validating existing data when the constraint was added.
- If validation is required after migration, implement an explicit data-quality check in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0054

CHECK/NOCHECK CONSTRAINT statement removed. Enabling or disabling constraints is not applicable in Snowflake.

### Description

This message is shown when `ALTER TABLE ... CHECK CONSTRAINT ...` or `ALTER TABLE ... NOCHECK CONSTRAINT ...` is converted. The statement is commented out because Snowflake does not support enabling or disabling constraints in the same way SQL Server does.

#### Code Example

##### Input Code:

Copy code

```
ALTER TABLE dbo.FactPoolSummary CHECK CONSTRAINT DimPoolFKFactPoolSummary01;
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TS0054 - CHECK CONSTRAINT STATEMENT REMOVED, ENABLING/DISABLING CONSTRAINTS IS NOT APPLICABLE IN SNOWFLAKE **
--ALTER TABLE IF EXISTS dbo.FactPoolSummary CHECK CONSTRAINT DimPoolFKFactPoolSummary01;
```

#### Best Practices

- Review any operational process that temporarily disables constraints during bulk loads or maintenance.
- If the source process relied on constraint state transitions, redesign that workflow explicitly for Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0055

Label statement commented out. No GOTO references this label so it is not required in Snowflake.

### Description

This message is shown when a labeled statement in a stored procedure has no corresponding `GOTO` that references it. Since the label serves no control flow purpose, it is commented out. The statements that follow the label are preserved and execute normally.

#### Code Example

In this example, the `Cleanup` label exists in the procedure body but no `GOTO Cleanup` references it, so the label is commented out while the `RETURN` statement beneath it is preserved:

##### Input Code:

Copy code

```
CREATE PROCEDURE dbo.UpdateCustomerStatus
AS
BEGIN
    DECLARE @ErrorCode INT = 0
    SET @ErrorCode = 1
Cleanup:
    RETURN @ErrorCode
END
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.UpdateCustomerStatus ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ERRORCODE INT := 0;
  BEGIN
    ERRORCODE := 1;

--    --** SSC-FDM-TS0055 - LABEL STATEMENT COMMENTED OUT. NO GOTO REFERENCES THIS LABEL SO IT IS NOT REQUIRED IN SNOWFLAKE. **
--    Cleanup:
    RETURN :ERRORCODE;
  END;
$$;
```

#### Best Practices

- No action is required. The label had no effect on control flow and was safely removed.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

- [SSC-EWI-TS0045](../conversion-issues/sqlServerEWI#ssc-ewi-ts0045): Labeled statement is not supported in Snowflake Scripting.

## SSC-FDM-TS0056

CREATE USER statement commented out, database-scoped user management is not applicable in Snowflake.

### Description

In SQL Server, `CREATE USER` creates a database-scoped user that is typically tied to a SQL Server login (`FOR LOGIN`) or a Windows domain account, and may include a `DEFAULT_SCHEMA` assignment. Snowflake does not have an equivalent concept — users are managed at the account level rather than within individual databases, so there is no direct translation. The entire statement is commented out and this FDM marker is added. All variants are handled, including `FOR LOGIN`, `WITH DEFAULT_SCHEMA`, and combinations of both.

#### Code Example

##### Input Code:

Copy code

```
CREATE USER [CORP\DEV-LA] FOR LOGIN [CORP\DEV-LA]
CREATE USER [Corp\IceService] FOR LOGIN [CORP\IceService] WITH DEFAULT_SCHEMA=[dbo]
CREATE USER [CORP\GOLDEV] WITH DEFAULT_SCHEMA=[dbo]
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TS0056 - CREATE USER STATEMENT COMMENTED OUT, DATABASE-SCOPED USER MANAGEMENT IS NOT APPLICABLE IN SNOWFLAKE **
--CREATE USER [CORP\DEV-LA] FOR LOGIN [CORP\DEV-LA]

----** SSC-FDM-TS0056 - CREATE USER STATEMENT COMMENTED OUT, DATABASE-SCOPED USER MANAGEMENT IS NOT APPLICABLE IN SNOWFLAKE **
--CREATE USER [Corp\IceService] FOR LOGIN [CORP\IceService] WITH DEFAULT_SCHEMA = [dbo]

----** SSC-FDM-TS0056 - CREATE USER STATEMENT COMMENTED OUT, DATABASE-SCOPED USER MANAGEMENT IS NOT APPLICABLE IN SNOWFLAKE **
--CREATE USER [CORP\GOLDEV] WITH DEFAULT_SCHEMA = [dbo]
```

#### Best Practices

- Review the commented-out `CREATE USER` statements and recreate the users at the Snowflake account level using `CREATE USER` with Snowflake’s syntax.
- Map SQL Server logins and Windows domain accounts to Snowflake’s identity providers (SSO, SCIM, or key-pair authentication).
- Default schema assignments can be configured per user in Snowflake using `ALTER USER ... SET DEFAULT_NAMESPACE`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0057

DEALLOCATE is not required in Snowflake Scripting. Cursors are automatically deallocated when they go out of scope.

### Description

In SQL Server, `DEALLOCATE` releases the data structures and locks held by a cursor. In Snowflake Scripting, cursors are automatically deallocated when they go out of scope, so there’s no functional need for an explicit `DEALLOCATE` statement. The statement is commented out and this FDM marker is added to indicate no user action is required.

#### Code Example

##### Input Code:

Copy code

```
CREATE PROCEDURE dbo.SimpleCursorProc
AS
BEGIN
    DECLARE @ItemId INT

    DECLARE item_curs CURSOR FOR
        SELECT ItemId FROM dbo.Items

    OPEN item_curs

    FETCH NEXT FROM item_curs INTO @ItemId

    CLOSE item_curs
    DEALLOCATE item_curs
END
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.SimpleCursorProc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ITEMID INT;
    --** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
    item_curs CURSOR
    FOR
      SELECT
        ItemId
      FROM
        dbo.Items;
  BEGIN
    OPEN item_curs;
    FETCH
      item_curs
    INTO
      :ITEMID;
    CLOSE item_curs;
--    --** SSC-FDM-TS0057 - DEALLOCATE IS NOT REQUIRED IN SNOWFLAKE SCRIPTING. CURSORS ARE AUTOMATICALLY DEALLOCATED WHEN THEY GO OUT OF SCOPE. **
--    DEALLOCATE item_curs
  END;
$$;
```

#### Best Practices

- No additional user actions are required. The commented-out `DEALLOCATE` statement can safely be left as is or removed entirely.
- Snowflake automatically deallocates cursors when the procedure or block scope ends.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0058

Waiting until a specific hour of the day is not supported by Snowflake.

#### Description

This FDM indicates that SnowConvert AI commented out `WAITFOR TIME`. Snowflake can wait for a duration with `SYSTEM$WAIT`, but it has no equivalent statement that waits until a wall-clock time.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
WAITFOR TIME '22:30:00';
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0058 - WAITING UNTIL A SPECIFIC HOUR OF THE DAY IS NOT SUPPORTED BY SNOWFLAKE **
--WAITFOR
--TIME '22:30:00';
```

#### Best Practices

- Replace wall-clock waiting with a scheduled Snowflake task or an external orchestrator.
- Account for the task’s configured time zone and daylight-saving changes.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0059

Synonym references renamed to original object name.

#### Description

This message is shown when a `CREATE SYNONYM` statement is converted. Snowflake does not support synonyms, so The `CREATE SYNONYM` statement is commented out and all references to the synonym are replaced with the original object name.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE SYNONYM MyProduct FOR inventory.product;
GO
SELECT * FROM MyProduct;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0059 - SYNONYMS ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES TO THIS SYNONYM HAVE BEEN REPLACED WITH THE ORIGINAL OBJECT NAME. **
--CREATE SYNONYM MyProduct FOR inventory.product;

SELECT
  *
FROM
  inventory.product;
```

#### Best Practices

- Only synonym references found within the converted scripts are replaced. Any external code that references the synonym — such as ETL pipelines, application queries, or stored procedures in other scripts — must be updated manually to use the original object name.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0060

The database\_id parameter in OBJECT\_SCHEMA\_NAME is not supported in Snowflake and has been removed.

### Description

SQL Server’s `OBJECT_SCHEMA_NAME` function accepts an optional second parameter `database_id` that allows cross-database schema lookups:

Copy code

```
OBJECT_SCHEMA_NAME(object_id, database_id)
```

Snowflake’s `INFORMATION_SCHEMA` views are scoped to the current database by default and do not support a numeric `database_id` parameter. When the two-argument form is encountered, the function is converted to `OBJECT_SCHEMA_NAME_UDF` using only the first argument and drops the `database_id` parameter, adding this FDM to indicate the behavioral difference.

#### Code Example

##### Input Code:

Copy code

```
SELECT OBJECT_SCHEMA_NAME(1, 1);
```

##### Generated Code:

Copy code

```
SELECT
PUBLIC.OBJECT_SCHEMA_NAME_UDF(1) /*** SSC-FDM-TS0060 - THE DATABASE_ID PARAMETER IN OBJECT_SCHEMA_NAME IS NOT SUPPORTED IN SNOWFLAKE AND HAS BEEN REMOVED ***/;
```

##### Input Code (dynamic database\_id):

Copy code

```
SELECT OBJECT_SCHEMA_NAME(object_id, DB_ID()) FROM sys.objects;
```

##### Generated Code:

Copy code

```
SELECT
   PUBLIC.OBJECT_SCHEMA_NAME_UDF(object_id) /*** SSC-FDM-TS0060 - THE DATABASE_ID PARAMETER IN OBJECT_SCHEMA_NAME IS NOT SUPPORTED IN SNOWFLAKE AND HAS BEEN REMOVED ***/
FROM
   sys.objects;
```

#### Best Practices

- If the original query targets a different database, you may need to manually qualify the UDF call or switch database context using `USE DATABASE`.
- For single-database migrations, the removed `database_id` parameter typically has no impact since `INFORMATION_SCHEMA` queries default to the current database.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0063

ISDATE result depends on the session date format; set DATE\_INPUT\_FORMAT if a specific format is needed.

### Description

The T-SQL `ISDATE(expr)` function returns `1` if `expr` is a valid date value and `0` otherwise. Its validation behavior is driven by the session `DATEFORMAT` and `LANGUAGE` settings, which have no direct equivalent in Snowflake.

`ISDATE(expr)` is replaced with an inline `IFF(... IS NOT NULL, 1, 0)` expression built from one or more `TRY_TO_DATE` (and optionally `TRY_TO_TIMESTAMP_NTZ`) calls. When the argument is a string literal, SnowConvert infers the format from the literal value and collapses the expression to a single call. For ambiguous literals or non-literal expressions (column references, variables), it generates a multi-branch `OR` chain covering all common date formats plus a timestamp fallback for inputs that contain a time component.

#### Code Example

##### Input Code:

Copy code

```
SELECT ISDATE('2026-02-20');
```

##### Generated Code:

Copy code

```
SELECT
IFF(TRY_TO_DATE('2026-02-20') IS NOT NULL, 1, 0) /*** SSC-FDM-TS0063 - ISDATE DEPENDS ON THE SESSION DATEFORMAT/LANGUAGE; SET DATE_INPUT_FORMAT IF A SPECIFIC FORMAT IS NEEDED. ***/;
```

##### Input Code (column reference):

Copy code

```
SELECT ISDATE(date_column) FROM my_table;
```

##### Generated Code (column reference):

Copy code

```
SELECT
IFF(TRY_TO_DATE(date_column) IS NOT NULL OR TRY_TO_DATE(date_column, 'YYYY/MM/DD') IS NOT NULL OR TRY_TO_DATE(date_column, 'MM.DD.YYYY') IS NOT NULL OR TRY_TO_DATE(date_column, 'MM/YYYY/DD') IS NOT NULL OR TRY_TO_DATE(date_column, 'MM-DD-YYYY') IS NOT NULL OR TRY_TO_TIMESTAMP_NTZ(date_column) IS NOT NULL, 1, 0) /*** SSC-FDM-TS0063 - ISDATE DEPENDS ON THE SESSION DATEFORMAT/LANGUAGE; SET DATE_INPUT_FORMAT IF A SPECIFIC FORMAT IS NEEDED. ***/
FROM
my_table;
```

#### Best Practices

- If your data uses a consistent date format, set `DATE_INPUT_FORMAT` at the session or warehouse level so a single `TRY_TO_DATE` call suffices.
- The multi-branch expression generated for column references can be expensive on large tables. If the column always contains ISO-formatted dates, simplify to `IFF(TRY_TO_DATE(date_column) IS NOT NULL, 1, 0)`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0064

OPTION LABEL removed, not supported in Snowflake.

### Description

The T-SQL `OPTION (LABEL = '...')` hint attaches a string label to a query for workload management and monitoring (visible in Azure Synapse Dedicated Pool DMVs). Snowflake has no equivalent query-level label hint; workload monitoring is handled via `QUERY_TAG` session parameters or resource monitors.

When an `OPTION` clause that contains a `LABEL` hint is encountered, the entire `OPTION (...)` clause is commented out and this FDM marker is emitted. `OPTION` clauses that contain only optimizer hints without a `LABEL` (e.g., `OPTION (HASH JOIN, RECOMPILE)`) are silently dropped.

#### Code Example

##### Input Code:

Copy code

```
SELECT region, SUM(amount) AS total
FROM dbo.Sales
WHERE region = @region
GROUP BY region
OPTION (LABEL = 'DailySalesReport:RegionalAggregation');
```

##### Generated Code:

Copy code

```
SELECT
  region,
  SUM(amount) AS total
FROM
  dbo.Sales
WHERE
  region = @region
GROUP BY
  region
----** SSC-FDM-TS0064 - OPTION LABEL REMOVED, NOT SUPPORTED IN SNOWFLAKE. **
--OPTION (
--  LABEL = 'DailySalesReport:RegionalAggregation')
                                                 ;
```

##### Input Code (mixed OPTION hints):

Copy code

```
SELECT COUNT(*)
FROM dbo.DimCustomer a
INNER JOIN dbo.FactInternetSales b ON (a.CustomerKey = b.CustomerKey)
OPTION (LABEL = 'CustJoin', HASH JOIN, MERGE JOIN);
```

##### Generated Code (mixed OPTION hints):

Copy code

```
SELECT
  COUNT(*)
FROM
  dbo.DimCustomer a
  INNER JOIN
    dbo.FactInternetSales b
    ON (a.CustomerKey = b.CustomerKey)
----** SSC-FDM-TS0064 - OPTION LABEL REMOVED, NOT SUPPORTED IN SNOWFLAKE. **
--OPTION (
--  LABEL = 'CustJoin',
--  HASH JOIN,
--  MERGE JOIN)
             ;
```

#### Best Practices

- Use `ALTER SESSION SET QUERY_TAG = 'your-label'` before the query to attach a searchable tag visible in Snowflake’s `QUERY_HISTORY` view.
- If many queries share the same label pattern, apply `QUERY_TAG` at the warehouse or session level rather than per statement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0065

System table was mapped to an approximate Snowflake equivalent

#### Description

This FDM indicates that SnowConvert AI mapped a SQL Server system table to an approximate Snowflake metadata view. SQL Server database-scoped security metadata and Snowflake account-scoped metadata are not fully equivalent.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT name FROM sys.database_principals;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT name
FROM
  --** SSC-FDM-TS0065 - SYSTEM TABLE 'sys.database_principals' WAS MAPPED TO 'SNOWFLAKE.ACCOUNT_USAGE.USERS' (APPROXIMATE EQUIVALENT). SNOWFLAKE SECURITY MODEL IS ACCOUNT-LEVEL, NOT DATABASE-SCOPED. MANUAL REVIEW REQUIRED **
  SNOWFLAKE.ACCOUNT_USAGE.USERS;
```

#### Best Practices

- Review column meanings, row visibility, and account-level scope before relying on the result.
- Update filters and joins to use Snowflake metadata keys.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0066

External table AUTO\_REFRESH set to false

#### Description

This FDM indicates that SnowConvert AI generated an external table with `AUTO_REFRESH = false`. Snowflake defaults this property to `true`, but automatic refresh requires a compatible notification integration.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE EXTERNAL TABLE silver.Items (id INT)
WITH (DATA_SOURCE = DataLakeSource, LOCATION = N'Silver/Items', FILE_FORMAT = ParquetFormat);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0066 - AUTO_REFRESH WAS SET TO FALSE. SNOWFLAKE DEFAULTS EXTERNAL TABLES TO AUTO_REFRESH = TRUE; ENABLE IT WITH A NOTIFICATION INTEGRATION IF AUTOMATIC METADATA REFRESH IS REQUIRED. **
CREATE EXTERNAL TABLE silver.Items (id INT)
LOCATION = @DataLakeSource/Silver/Items
FILE_FORMAT = ParquetFormat
AUTO_REFRESH = false;
```

#### Best Practices

- Configure event notifications and enable automatic refresh when new files must become queryable without manual refresh.
- Otherwise schedule explicit metadata refreshes and monitor their completion.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0067

DATENAME with TZOFFSET was converted to TO\_CHAR; a zero UTC offset renders as ‘Z’ instead of ‘+00:00’ in Snowflake.

#### Description

This FDM indicates that `DATENAME(TZOFFSET, ...)` was converted to `TO_CHAR`. Snowflake may render a zero UTC offset as `Z`, while SQL Server returns `+00:00`.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT DATENAME(tzoffset, GETDATE());
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
TO_CHAR(CURRENT_TIMESTAMP() :: TIMESTAMP, 'TZH:TZM') /*** SSC-FDM-TS0067 - DATENAME WITH TZOFFSET WAS CONVERTED TO TO_CHAR. A ZERO UTC OFFSET RENDERS AS 'Z' INSTEAD OF '+00:00' IN SNOWFLAKE. ***/;
```

#### Best Practices

- Normalize `Z` to `+00:00` if downstream code requires SQL Server’s exact text format.
- Prefer timestamp values over formatted offset strings for comparisons.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0068

External file format option was dropped because it has no Snowflake equivalent.

#### Description

This FDM indicates that SnowConvert AI dropped a Synapse external file format option that has no Snowflake file-format equivalent.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE EXTERNAL FILE FORMAT CsvWithEncoding
WITH (FORMAT_TYPE = DELIMITEDTEXT, FORMAT_OPTIONS (FIELD_TERMINATOR = '|', ENCODING = 'UTF8'));
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0068 - FILE FORMAT OPTION 'ENCODING' WAS NOT TRANSLATED BECAUSE IT HAS NO SNOWFLAKE EQUIVALENT AND MAY CAUSE A FUNCTIONAL DIFFERENCE. **
CREATE FILE FORMAT IF NOT EXISTS CsvWithEncoding
TYPE = CSV
FIELD_DELIMITER = '|'
COMPRESSION = AUTO;
```

#### Best Practices

- Confirm that Snowflake reads the source files with the intended encoding and parsing behavior.
- Preprocess files or adjust upstream export settings when the dropped option is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0069

SERVERPROPERTY has no exact Snowflake equivalent and the result may differ from the original value.

#### Description

SQL Server’s `SERVERPROPERTY` function returns instance-level metadata such as the product version, edition, and server name. Snowflake has no single function that exposes the same server properties, so the most commonly used property literals are translated to the closest Snowflake scalar and this functional-difference marker is attached, because the returned value won’t match the original SQL Server output.

The property literal is matched case-insensitively, and both regular (`'...'`) and national (`N'...'`) string literals are supported. The following properties are mapped:

| `SERVERPROPERTY` property | Snowflake replacement |
| --- | --- |
| `ProductVersion` | `CURRENT_VERSION()` |
| `ServerName`, `MachineName`, `InstanceName` | `CURRENT_ACCOUNT()` |
| `Edition` | `'Snowflake'` (string literal) |

Expand

Show lessSee more

Any other property literal, or a non-literal argument (such as a column or variable that can’t be resolved at conversion time), has no scalar equivalent. In those cases the original `SERVERPROPERTY` call is preserved and flagged with [SSC-EWI-0073](../conversion-issues/generalEWI#ssc-ewi-0073) for manual functional-equivalence review.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT SERVERPROPERTY('ProductVersion');

SELECT SERVERPROPERTY('EngineEdition');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
CURRENT_VERSION() /*** SSC-FDM-TS0069 - SERVERPROPERTY HAS NO EXACT SNOWFLAKE EQUIVALENT AND THE RESULT MAY DIFFER FROM THE ORIGINAL VALUE. ***/;

SELECT
SERVERPROPERTY('EngineEdition') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SERVERPROPERTY' NODE ***/!!!;
```

#### Best Practices

- Review every translated `SERVERPROPERTY` call: the Snowflake scalar returns Snowflake-specific values (for example, `CURRENT_VERSION()` returns the Snowflake version, not a SQL Server build number), so any logic that parses or compares the original result may need to be adjusted.
- For calls flagged with `SSC-EWI-0073`, replace the call with the Snowflake metadata that best fits your use case, or remove it if it isn’t applicable in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0070

A storage integration and stage scaffold were generated from the external data source; provide the credentials before use.

#### Description

This FDM indicates that SnowConvert AI generated a Snowflake storage integration and stage scaffold from a Synapse external data source. Credential placeholders must be configured before use.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE EXTERNAL DATA SOURCE DataLakeSource
WITH (LOCATION = 'https://example.dfs.core.windows.net/sales');
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0070 - A STORAGE INTEGRATION AND STAGE SCAFFOLD WERE GENERATED FROM THE EXTERNAL DATA SOURCE. PROVIDE AZURE_TENANT_ID AND CONFIGURE THE CREDENTIALS VIA A CORTEX SECRET BEFORE USE. **
CREATE STORAGE INTEGRATION IF NOT EXISTS DataLakeSource_INTEGRATION
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'AZURE'
  ENABLED = TRUE
  AZURE_TENANT_ID = '<TODO_AZURE_TENANT_ID>'
  STORAGE_ALLOWED_LOCATIONS = ('azure://example.blob.core.windows.net/sales/');
CREATE STAGE IF NOT EXISTS DataLakeSource
  STORAGE_INTEGRATION = DataLakeSource_INTEGRATION
  URL = 'azure://example.blob.core.windows.net/sales/';
```

#### Best Practices

- Supply the Azure tenant ID, allowed locations, and credentials through approved secret-management procedures.
- Test stage access with the least privileges required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0071

Database Collation Scope Differs From Default DDL Collation

#### Description

This FDM indicates that only the source database’s default column collation was mapped to `DEFAULT_DDL_COLLATION`. Other database-collation effects are not reproduced in Snowflake.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE DATABASE SalesDb COLLATE Latin1_General_CI_AS;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE DATABASE IF NOT EXISTS SalesDb
DEFAULT_DDL_COLLATION='EN-CI-AS' /*** SSC-FDM-TS0071 - ONLY THE DEFAULT COLUMN COLLATION IS APPLIED; OTHER EFFECTS OF THE SOURCE DATABASE COLLATION ARE NOT SUPPORTED ***/;
```

#### Best Practices

- Review identifier, comparison, sorting, and expression behavior that depended on database collation.
- Apply explicit collations where the default DDL collation is insufficient.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0072

System column value has not been translated to its Snowflake equivalent

#### Description

This FDM indicates that a SQL Server system-column value has no known Snowflake equivalent. SnowConvert AI maps the column but preserves the value for manual review.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT [type] FROM sys.tables WHERE [type] = 'V';
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'V' /*** SSC-FDM-TS0072 - SYSTEM COLUMN VALUE 'V' FOR BUILT-IN OBJECT 'SYS.TABLES' HAS NOT BEEN TRANSLATED TO ITS SNOWFLAKE EQUIVALENT. MANUAL REVIEW REQUIRED ***/;
```

#### Best Practices

- Replace the preserved value with the value used by the mapped Snowflake metadata view.
- Confirm the query’s expected object types and row set.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0073

SET TRANSACTION ISOLATION LEVEL statement is commented out, which is not applicable in Snowflake.

#### Description

This FDM indicates that SnowConvert AI commented out `SET TRANSACTION ISOLATION LEVEL`. Snowflake uses its own multiversion concurrency-control isolation behavior and does not expose SQL Server’s isolation-level choices.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0073 - SET TRANSACTION ISOLATION LEVEL STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

#### Best Practices

- Review workflows that depended on dirty reads, blocking, or lock duration.
- Redesign concurrency-sensitive logic for Snowflake transaction semantics.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0074

Parameter was renamed because its converted name conflicts with another identifier in the function.

#### Description

This FDM indicates that SnowConvert AI renamed a function parameter because its converted identifier conflicts with another identifier in the function.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE FUNCTION dbo.CountByStatus(@status INT)
RETURNS INT
AS
BEGIN
  RETURN (SELECT COUNT(*) FROM dbo.Orders WHERE Status = @status);
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION dbo.CountByStatus (
  P_STATUS INT /*** SSC-FDM-TS0074 - PARAMETER '@status' WAS RENAMED TO 'P_STATUS' BECAUSE ITS CONVERTED NAME CONFLICTS WITH ANOTHER IDENTIFIER IN THE FUNCTION ***/)
RETURNS INT
LANGUAGE SQL
AS
$$
  SELECT COUNT(*) FROM dbo.Orders WHERE Status = P_STATUS
$$;
```

#### Best Practices

- Update named-argument calls and external references to use the generated parameter name.
- Verify that every parameter reference was renamed consistently.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0075

String literal was not reformatted to an unambiguous date format; Snowflake may read it as an epoch offset.

#### Description

This FDM indicates that SnowConvert AI could not safely reformat a compact date string. Snowflake may interpret the preserved numeric-looking string as an epoch offset instead of a calendar date.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT * FROM Orders WHERE OrderDate = '970101';
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT * FROM Orders
WHERE OrderDate = '970101' /*** SSC-FDM-TS0075 - STRING LITERAL '970101' WAS NOT REFORMATTED TO AN UNAMBIGUOUS DATE FORMAT. IF IT IS COMPARED AGAINST A DATE VALUE, SNOWFLAKE MAY INTERPRET IT AS AN EPOCH OFFSET INSTEAD OF A CALENDAR DATE. ADD AN EXPLICIT CAST IF NEEDED. ***/;
```

#### Best Practices

- Replace compact or two-digit-year strings with ISO dates or an explicit `TO_DATE` format.
- Define the intended century rather than relying on session defaults.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0076

SET DEADLOCK\_PRIORITY statement is commented out, which is not applicable in Snowflake.

#### Description

This FDM indicates that SnowConvert AI commented out `SET DEADLOCK_PRIORITY`. Snowflake does not expose an equivalent session setting.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SET DEADLOCK_PRIORITY HIGH;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0076 - SET DEADLOCK_PRIORITY STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--SET DEADLOCK_PRIORITY HIGH;
```

#### Best Practices

- Remove logic that assumes a session can control deadlock-victim selection.
- Use idempotent operations and retry handling for concurrency failures.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0077

DATETIMEFROMPARTS is not supported in Snowflake. TIMESTAMP\_NTZ\_FROM\_PARTS is used as a workaround.

#### Description

This FDM indicates that `DATETIMEFROMPARTS` was translated to `TIMESTAMP_NTZ_FROM_PARTS`. Milliseconds are scaled to Snowflake nanoseconds.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT DATETIMEFROMPARTS(2024, 1, 15, 10, 30, 45, 999);
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
TIMESTAMP_NTZ_FROM_PARTS(2024, 1, 15, 10, 30, 45, 999 * 1000000) /*** SSC-FDM-TS0077 - DATETIMEFROMPARTS IS NOT SUPPORTED IN SNOWFLAKE. TIMESTAMP_NTZ_FROM_PARTS IS USED AS A WORKAROUND. ***/;
```

#### Best Practices

- Validate timestamp precision and out-of-range input behavior.
- Confirm that a timezone-free timestamp matches the source requirement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0078

APP\_NAME was replaced with CURRENT\_CLIENT, whose client identity may differ from the SQL Server application name.

#### Description

This FDM indicates that `APP_NAME()` was replaced with `CURRENT_CLIENT()`. The Snowflake client identity can differ from the SQL Server application-name connection property.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT APP_NAME();
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CURRENT_CLIENT() /*** SSC-FDM-TS0078 - APP_NAME WAS REPLACED WITH CURRENT_CLIENT, WHOSE CLIENT IDENTITY MAY DIFFER FROM THE SQL SERVER APPLICATION NAME. ***/;
```

#### Best Practices

- Do not use the returned client value as a stable application identifier without validation.
- Pass an explicit application tag or set `QUERY_TAG` when auditing requires a controlled value.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0079

Index metadata for standard tables is not supported in Snowflake. INFORMATION\_SCHEMA.INDEXES is used as a workaround for hybrid tables.

#### Description

This FDM indicates that `sys.indexes` was mapped to `INFORMATION_SCHEMA.INDEXES`. That Snowflake view describes indexes on hybrid tables and is not equivalent to SQL Server index metadata for standard tables.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT i.[name], i.[object_id] FROM sys.indexes i WHERE i.[name] = 'IX_EXAMPLE';
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT i.NAME, i.TABLE_NAME
FROM
  --** SSC-FDM-TS0079 - INDEX METADATA FOR STANDARD TABLES IS NOT SUPPORTED IN SNOWFLAKE. INFORMATION_SCHEMA.INDEXES IS USED AS A WORKAROUND FOR HYBRID TABLES. **
  INFORMATION_SCHEMA.INDEXES i
WHERE i.NAME = 'IX_EXAMPLE';
```

#### Best Practices

- Determine whether the migrated tables are standard or hybrid tables before relying on the view.
- Remove SQL Server index-maintenance logic that has no Snowflake equivalent.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0080

COLLATE DATABASE\_DEFAULT was removed because the source database default collation is not part of the converted code.

#### Description

This FDM indicates that SnowConvert AI removed `COLLATE DATABASE_DEFAULT`. Without source database-default metadata, the expression falls back to Snowflake’s binary collation.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT Name FROM Customers WHERE Name COLLATE DATABASE_DEFAULT = 'alice';
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT Name FROM Customers
WHERE Name
-- --** SSC-FDM-TS0080 - COLLATE DATABASE_DEFAULT REMOVED - THE SOURCE DATABASE DEFAULT COLLATION IS NOT PART OF THE CONVERTED CODE, SO THE COMPARISON FALLS BACK TO SNOWFLAKE'S BINARY COLLATION. ADD AN EXPLICIT COLLATE IF A CASE OR ACCENT INSENSITIVE COMPARISON IS REQUIRED. **
-- COLLATE DATABASE_DEFAULT
= 'alice';
```

#### Best Practices

- Add an explicit Snowflake collation when case- or accent-insensitive comparison is required.
- Test sorting and equality behavior with representative data.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0081

Snowflake does not expose SQL Server physical database-file properties. Review dependent logic.

#### Description

This FDM indicates that `FILEPROPERTY` was replaced with `NULL` because Snowflake does not expose SQL Server physical database-file properties.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT FILEPROPERTY('master', 'SpaceUsed');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT null /*** SSC-FDM-TS0081 - SNOWFLAKE DOES NOT EXPOSE SQL SERVER PHYSICAL DATABASE-FILE PROPERTIES. REVIEW DEPENDENT LOGIC. ***/;
```

#### Best Practices

- Replace file-level capacity or state checks with Snowflake storage, billing, or account-usage views appropriate to the goal.
- Update null-sensitive downstream logic explicitly.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0082

CURSOR\_STATUS is not supported in Snowflake. Manual cursor state tracking is required.

#### Description

This FDM is generated when SnowConvert AI encounters the SQL Server `CURSOR_STATUS` function. Snowflake does not provide an equivalent function, so the call is preserved and marked for manual cursor state tracking.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT CURSOR_STATUS('global', 'test_cursor');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CURSOR_STATUS('global', 'test_cursor') /*** SSC-FDM-TS0082 - CURSOR_STATUS IS NOT SUPPORTED IN SNOWFLAKE. MANUAL CURSOR STATE TRACKING IS REQUIRED. ***/;
```

#### Best Practices

- Track cursor lifecycle state explicitly in the migrated procedure.
- Review each branch that depends on `CURSOR_STATUS` before deployment.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0084

SQL Server DATEFORMAT order-only behavior is not supported in Snowflake; DATE\_INPUT\_FORMAT is used as a workaround.

#### Description

This FDM is generated when SnowConvert AI converts a SQL Server `SET DATEFORMAT` statement. Snowflake requires a concrete `DATE_INPUT_FORMAT`, so the generated session format uses slash separators and a four-digit year as a narrower workaround.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SET DATEFORMAT mdy;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0084 - SQL SERVER DATEFORMAT ORDER-ONLY BEHAVIOR IS NOT SUPPORTED IN SNOWFLAKE. DATE_INPUT_FORMAT WITH SLASH SEPARATORS AND A FOUR-DIGIT YEAR IS USED AS A WORKAROUND. ** ALTER SESSION SET DATE_INPUT_FORMAT = 'MM/DD/YYYY';
```

#### Best Practices

- Verify that incoming date strings use the generated separator and four-digit year.
- Set a more appropriate explicit `DATE_INPUT_FORMAT` when source inputs use another shape.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TS0085

CHECKPOINT is not supported in Snowflake. The statement is commented out.

#### Description

This FDM indicates that SnowConvert AI commented out `CHECKPOINT`. Snowflake manages durable storage and recovery without a user-issued checkpoint statement.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CHECKPOINT 60;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-FDM-TS0085 - CHECKPOINT IS NOT SUPPORTED IN SNOWFLAKE. THE STATEMENT IS COMMENTED OUT. **
--CHECKPOINT 60;
```

#### Best Practices

- Remove checkpoint scheduling and monitoring logic after migration.
- Review surrounding maintenance workflows for other SQL Server-specific recovery operations.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
