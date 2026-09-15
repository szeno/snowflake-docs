# Code Conversion - SQL Server-Azure Synapse Issues

Applies to

- SQL Server
- Azure Synapse Analytics
- Sybase

## SSC-EWI-TS0001

User defined function body not generated

### Severity

Critical

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI appears when a critical exception is handled that causes the function body not to be generated during its translation.

#### Example Code

##### SQL Server

Copy code

```
 CREATE FUNCTION func1 ()
RETURNS VARCHAR
SELECT
   *
FROM
   TABLE1
```

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE FUNCTION func1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0001 - THE BODY WAS NOT GENERATED FOR FUNCTION 'func1' ***/!!!
AS
$$

$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0002

The ANSI\_PADDING OFF is not supported in Snowflake.

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

In SQL Server, `SET ANSI_PADDING` controls how trailing blanks are stored in `CHAR`, `VARCHAR`, `BINARY`, and `VARBINARY` columns. When `SET ANSI_PADDING OFF` is active during a `CREATE TABLE` or `ALTER TABLE` statement, SQL Server records this setting as a **column-level property** on each column defined in that scope. This means the trimming behavior is permanently associated with the column definition, regardless of the session setting at the time data is inserted.

Specifically, when a column is created with `ANSI_PADDING OFF`:

- `VARCHAR` columns have trailing blanks trimmed on insert.
- `VARBINARY` columns have trailing zeros trimmed on insert.
- `CHAR` columns are trimmed of trailing blanks (instead of being right-padded to the defined length).

Snowflake has no equivalent column-level property. Snowflake always preserves trailing spaces in string values (equivalent to `ANSI_PADDING ON`). There is no way to configure a Snowflake column to automatically trim trailing blanks on insert.

Since this is a storage-level semantic difference that cannot be automatically translated, the statement is flagged with this EWI.

#### Example Code

##### SQL Server

Copy code

```
 SET ANSI_PADDING OFF;
```

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0002 - THE ANSI_PADDING OFF IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
SET ANSI_PADDING OFF;
```

#### Limitations

Snowflake does not support `ANSI_PADDING OFF` semantics at any level (session, database, or column).

- **Wrapping inserts with `RTRIM`**: This only handles explicit `INSERT` statements in the migrated code. It does not cover data loaded through ETL pipelines, external tools, or application code that also relied on the column’s `ANSI_PADDING OFF` property.
- **Session-level setting**: Snowflake has no session parameter equivalent to `SET ANSI_PADDING`.
- **Column-level constraint or default**: Snowflake does not allow defining a column property that automatically trims trailing spaces.

To fully replicate `ANSI_PADDING OFF` behavior in Snowflake, manual intervention is required at the data pipeline level for every affected column.

#### Best Practices

- Identify all columns that were created under `SET ANSI_PADDING OFF` in the source SQL Server database. You can query `sys.columns` with `is_ansi_padded = 0` to find them.
- For each affected column, ensure that all data insertion paths (SQL scripts, ETL pipelines, application code) apply `RTRIM` before inserting into the corresponding Snowflake column.
- Consider creating a Snowflake stored procedure or UDF wrapper that enforces trimming for the affected columns.
- Review whether the trimming behavior is actually relied upon by downstream consumers. In some cases, `ANSI_PADDING OFF` was set by default in legacy scripts without the application depending on the trimming behavior.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0003

The ANSI\_WARNINGS OFF is not supported in Snowflake.

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

In Transact-SQL, the statement `SET ANSI_WARNINGS OFF` disables warnings such as Division by Zero or arithmetic overflow. Since `SET ANSI_WARNINGS OFF` is not a directly configurable setting in Snowflake, this EWI will be generated.

#### Example Code

##### SQL Server

Copy code

```
 SET ANSI_WARNINGS OFF;
```

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0003 - THE ANSI_WARNINGS OFF IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
SET ANSI_WARNINGS OFF;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0009

The following transaction may contain nested transactions and this is considered a complex pattern not supported in Snowflake.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

High

#### Description

This error is added to indicate when a transaction may contain nested transactions. In SQL Server, transactions can be nested. This means that it is possible to start a new transaction within an existing transaction. If after the first BEGIN statement, we execute another one, a new transaction will be opened and the current transaction count will be increased by one.\

On the other hand this is not supported in Snowflake, what will happen is that the second BEGIN statement will be ignored and we will still have only one transaction. For more information please refer to [SQL Server Transactions](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/transactions-transact-sql?view=sql-server-ver16).

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROC transactionsTest
AS
BEGIN TRANSACTION 
   SELECT @@TRANCOUNT AS TransactionCount_AfterFirstTransaction 
   INSERT INTO TESTSCHEMA.TESTTABLE(ID) VALUES (1), (2) 
   BEGIN TRANSACTION 
      SELECT @@TRANCOUNT AS TransactionCount_AfterSecondTransaction 
      INSERT INTO TESTSCHEMA.TESTTABLE(ID) VALUES (3), (4) 
   COMMIT;
   SELECT @@TRANCOUNT AS TransactionCount_AfterFirstCommit  
COMMIT;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE transactionsTest ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  ProcedureResultSet1 VARCHAR;
  ProcedureResultSet2 VARCHAR;
  ProcedureResultSet3 VARCHAR;
  return_arr ARRAY := array_construct();
 BEGIN
  !!!RESOLVE EWI!!! /*** SSC-EWI-TS0009 - THE FOLLOWING TRANSACTION MAY CONTAIN NESTED TRANSACTIONS WHICH ARE NOT SUPPORTED IN SNOWFLAKE. ***/!!!
  BEGIN TRANSACTION;
  ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
  CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
   SELECT
    :TRANCOUNT AS TransactionCount_AfterFirstTransaction;
  return_arr := array_append(return_arr, :ProcedureResultSet1);
  INSERT INTO TESTSCHEMA.TESTTABLE (ID) VALUES (1), (2);
  BEGIN TRANSACTION;
  ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
  CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
   SELECT
    :TRANCOUNT AS TransactionCount_AfterSecondTransaction;
  return_arr := array_append(return_arr, :ProcedureResultSet2);
  INSERT INTO TESTSCHEMA.TESTTABLE (ID) VALUES (3), (4);
  COMMIT;
  ProcedureResultSet3 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
  CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet3) AS
   SELECT
    :TRANCOUNT AS TransactionCount_AfterFirstCommit;
  return_arr := array_append(return_arr, :ProcedureResultSet3);
  COMMIT;
  --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
  RETURN return_arr;
 END;
$$;
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '12' COLUMN '1' OF THE SOURCE CODE STARTING AT 'END'. EXPECTED 'BATCH' GRAMMAR. **
--END
   ;
```

#### Best Practices

- In Snowflake nested transactions will not cause compilation errors, they will simply be ignored. You can access the assessment reports to check if nested transactions are present.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWI

1. [SSC-FDM-0020](../functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables
2. [SSC-EWI-0001](./generalEWI#ssc-ewi-0001): Unrecognized token on the line of the source code.
3. [SSC-EWI-0040](./generalEWI#ssc-ewi-0040): Statement Not Supported.

## SSC-EWI-TS0010

Common table expression in view not supported in Snowflake.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

High

#### Description

This error is added when an invalid CTE is inside a view since views are materialized representations of queries, which means that they only define how data is retrieved and presented, not how it is manipulated.

#### Code Example

##### Input Code:

Copy code

```
 Create View viewName
as
with commonTableExpressionName (
   columnName
) as
(
   select
      1
)
((select
   1 as col2)
union
(
   select
      1 as col3
));
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0010 - COMMON TABLE EXPRESSION IN VIEW NOT SUPPORTED IN SNOWFLAKE. ***/!!!
CREATE OR REPLACE VIEW viewName
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - WITH CTE NOT SUPPORTED IN SNOWFLAKE ***/!!!
with commonTableExpressionName (
   columnName
) as
(
   select
      1
)
((select
   1 as col2)
union
(
   select
      1 as col3
));
```

### Related EWI

1. [SSC-EWI-0021](./generalEWI#ssc-ewi-0021): Not supported.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0013

Computed column transformed

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0013](../functional-difference/sqlServerFDM#ssc-fdm-ts0013) documentation

### Severity

Low

#### Description

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
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

#### Best Practices

- No additional user actions are required; it is just informative.
- Add manual changes to the not-transformed expression.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0015

Data type is not supported in Snowflake

### Severity

Medium

### Description

This warning is added when an SQL Server column has an unsupported type in Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE table1
(
    column1 customType,
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE table1
(
    column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE CUSTOMTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

#### Best Practices

- Check the Snowflake data types [documentation](https://docs.snowflake.com/en/sql-reference/data-types.html) to find an equivalent for the data type.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0016

Translation for ODBC Scalar function pending

Note

Some parts of the output code are omitted for clarity reasons.

### Description

This EWI is added when an ODBC Scalar function is found inside the input code.  
User-defined functions are not supported in ODBC Scalar Function.

#### Code Example

##### Input Code:

Copy code

```
 SELECT {fn CURRENT_DATE_UDF()};
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "CURRENT_DATE_UDF" **
SELECT
CURRENT_DATE_UDF() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'CURRENT_DATE_UDF' NODE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-TS0016 - USER DEFINED FUNCTIONS ARE NOT SUPPORTED IN ODBC SCALAR FUNCTION. ***/!!!;
```

### Related EWI

1. [SSC-EWI-0073](./generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

#### Best Practices

- No additional user actions are required; it is just informative.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0017

Masking not supported

### Severity

Low

#### Description

This EWI is added when a masked column is found inside a `CREATE TABLE` statement. This functionality doesn’t work by adding the option in the column declaration. Manual effort is needed to have the same behavior as SQL Server.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE TABLE1
( 
  [COL1] nvarchar MASKED WITH (FUNCTION = 'default()') NULL,
  [COL2] varchar(100) MASKED WITH (FUNCTION = 'partial(1, "xxxxx", 1)') NULL,
  [COL3] varchar(100) MASKED WITH (FUNCTION = 'email()') NOT NULL,
  [COL4] smallint MASKED WITH (FUNCTION = 'random(1, 100)') NULL
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TABLE1
(
  COL1 VARCHAR
               !!!RESOLVE EWI!!! /*** SSC-EWI-TS0017 - COLUMN MASKING NOT SUPPORTED IN CREATE TABLE ***/!!!
               MASKED WITH (FUNCTION = 'default()') NULL,
  COL2 VARCHAR(100)
                    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0017 - COLUMN MASKING NOT SUPPORTED IN CREATE TABLE ***/!!!
 MASKED WITH (FUNCTION = 'partial(1, "xxxxx", 1)') NULL,
  COL3 VARCHAR(100)
                    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0017 - COLUMN MASKING NOT SUPPORTED IN CREATE TABLE ***/!!!
 MASKED WITH (FUNCTION = 'email()') NOT NULL,
  COL4 SMALLINT
                !!!RESOLVE EWI!!! /*** SSC-EWI-TS0017 - COLUMN MASKING NOT SUPPORTED IN CREATE TABLE ***/!!!
                MASKED WITH (FUNCTION = 'random(1, 100)') NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

#### Best Practices

`MASKING POLICIES` are not generated in the current version, so they have to be created manually. E.g.:

The first step is to create a masking policy administrator role.

Copy code

```
 create role masking_admin;
```

The second one is to grant the necessary privileges to the created role.

Copy code

```
 grant create masking policy on schema PUBLIC to role masking_admin;
allow table_owner role to set or unset the ssn_mask masking policy -- (optional)
grant apply on masking policy ssn_mask to role table_owner;
```

The next step is to create the masking policy functions.

Copy code

```
 -- default mask
create or replace masking policy default_mask as (val string) returns string ->
case
when current_role() in ('ANALYST') then val
else 'xxxx'
end;

-- partial mask
create or replace masking policy partial_mask as (val string) returns string ->
case
when current_role() in ('ANALYST') then val
else LEFT(val,1) || 'xxxxx' || RIGHT(val,1)
end;

-- email mask
create or replace masking policy email_mask as (val string) returns string ->
case
when current_role() in ('ANALYST') then val
else LEFT(val,1) || 'XXX@XXX.com'
end;

-- random mask
create or replace masking policy random_mask as (val smallint) returns smallint ->
case
when current_role() in ('ANALYST') then val
else UNIFORM(1,100,RANDOM())::SMALLINT
end;
```

Note

For sample purposes, we are taking some examples of masking functions in SQL Server, and manually translating it into its equivalent in Snowflake.

The final step is to add the masking policy to the column that originally had the masking option in SQL Server.

Copy code

```
 alter table if exists TABLE1 modify column COL1 set masking policy default_mask;
alter table if exists TABLE1 modify column COL2 set masking policy partial_mask;
alter table if exists TABLE1 modify column COL3 set masking policy email_mask;
alter table if exists TABLE1 modify column COL4 set masking policy random_mask;
```

If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0023

Bulk option not supported

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when some option in a `BULK INSERT` could not be mapped. The translated bulk options should be reflected as `FILE FORMAT` options.

#### Code Example

##### Input Code:

Copy code

```
 BULK INSERT #PCE FROM 'E:\PCE_Look-up_table.txt'  
WITH   
(  
   FIELDTERMINATOR ='\t',
   ROWTERMINATOR ='\n',
   FIRE_TRIGGERS 
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE FILE FORMAT FILE_FORMAT_638461199649565070
FIELD_DELIMITER = '\t'
RECORD_DELIMITER = '\n'
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0023 - 'FIRE_TRIGGERS' BULK OPTION COULD NOT BE TRANSFORMED TO ANY OF THE EXISTING FILE FORMAT OPTIONS ***/!!!
FIRE_TRIGGERS;

CREATE OR REPLACE STAGE STAGE_638461199649565070
FILE_FORMAT = FILE_FORMAT_638461199649565070;

--** SSC-FDM-TS0004 - PUT STATEMENT IS NOT SUPPORTED ON WEB UI. YOU SHOULD EXECUTE THE CODE THROUGH THE SNOWFLAKE CLI **
PUT file://E:\PCE_Look-up_table.txt @STAGE_638461199649565070 AUTO_COMPRESS = FALSE;

COPY INTO T_PCE FROM @STAGE_638461199649565070/PCE_Look-up_table.txt;
```

#### Best Practices

- Visit the SnowSQL CLI [user guide](https://docs.snowflake.com/en/user-guide/snowsql.html).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWI

1. [SSC-FDM-TS0004](../functional-difference/sqlServerFDM#ssc-fdm-ts0004): PUT statement not supported on UI.

## SSC-EWI-TS0024

Incomplete transformation for Bulk Insert

### Severity

Low

#### Description

This EWI is added when a `BULK INSERT` inside a stored procedure was not identified at all, so the dependencies for the complete transformation will not be generated. Also the transformed `COPY INTO` retrieves the file from a `tempStage` that needs to be created manually.

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROCEDURE BULK_PROC2
AS
BULK INSERT dbo.table1 FROM 'E:\test.txt'  
WITH   
(  
   FIELDTERMINATOR ='\t',
   ROWTERMINATOR ='\n'
); 

GO
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE FILE FORMAT FILE_FORMAT_638461207064166040
FIELD_DELIMITER = '\t'
RECORD_DELIMITER = '\n';

CREATE OR REPLACE STAGE STAGE_638461207064166040
FILE_FORMAT = FILE_FORMAT_638461207064166040;

--** SSC-FDM-TS0004 - PUT STATEMENT IS NOT SUPPORTED ON WEB UI. YOU SHOULD EXECUTE THE CODE THROUGH THE SNOWFLAKE CLI **
PUT file://E:\test.txt @STAGE_638461207064166040 AUTO_COMPRESS = FALSE;

CREATE OR REPLACE PROCEDURE BULK_PROC2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   // REGION SnowConvert AI Helpers Code
   // END REGION

   EXEC(`COPY INTO dbo.table1 FROM @STAGE_638461207064166040/test.txt`);
$$
```

#### Best Practices

- To retrieve the file, manually create a [STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) and a [FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0025

ERROR\_SEVERITY function transformed

### Severity

Low

Note

Generate Procedures and Macros using JavaScript as the target language adding the following flag -t JavaScript or –PLTargetLanguage JavaScript

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when [ERROR\_SEVERITY](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-severity-transact-sql?view=sql-server-ver15) built-in function is translated. By default, the function will return 16 as it is the most common severity in SQL Server. The generated UDF should retrie

#### Code Example

##### Input Code:

Copy code

```
 -- Additional Params: -t JavaScript
CREATE procedure proc1()
as
BEGIN TRY  
    -- Generate a divide-by-zero error.  
    SELECT 1/0 from table1;  
END TRY  
BEGIN CATCH  
    return ERROR_SEVERITY();  
END CATCH;  
GO
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    try {
        EXEC(`    -- Generate a divide-by-zero error.  
    SELECT
       TRUNC( 1/0) from
       table1`);
    } catch(error) {
        return SELECT(`   !!!RESOLVE EWI!!! /*** SSC-EWI-TS0025 - CUSTOM UDF 'ERROR_SEVERITY_UDF' INSERTED FOR ERROR_SEVERITY FUNCTION. ***/!!!
   ERROR_SEVERITY_UDF()`);
    }
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0026

With Delete Query turned to Create Table.

### Severity

Low

#### Description

This EWI is added when a Common Table Expression With a Delete From is transformed to a Create or Replace Table.

#### Code Example

##### Input Code:

Copy code

```
 WITH Duplicated AS (
SELECT *, ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ID) AS RN
FROM WithQueryTest
)
DELETE FROM Duplicated
WHERE Duplicated.RN > 1
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0026 - WITH DELETE QUERY TURNED TO CREATE TABLE ***/!!!
CREATE OR REPLACE TABLE WithQueryTest AS
SELECT
*
FROM
WithQueryTest
QUALIFY
ROW_NUMBER()
OVER (PARTITION BY
ID
ORDER BY ID) = 1;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0032

Bulk Insert Partially Translated

Warning

The EWI is only generated when Javascript is the target language for Stored Procedures. This is a deprecated translation feature, as Snowflake Scripting is the recommended target language for Stored Procedures.

### Severity

High

Note

Generate Procedures and Macros using JavaScript as the target language adding the following flag -t JavaScript or –PLTargetLanguage JavaScript

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added to a literal that was originally a concatenation, when the contained code had a `BULK INSERT` statement. The `PUT` command resulting from the `BULK INSERT` translation is not supported when executing code that was originally Dynamic SQL.

For this reason, the `PUT` command must be extracted from the output code and executed manually outside of the procedure that contains it. Keep in mind that if there are many `BULK INSERT` statements in Dynamic SQL sentences within the procedure, it is advised to split this procedure to be able to manually execute the corresponding `PUT` command for each translated `BULK INSERT`.

#### Code Example

##### Input Code:

Copy code

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE  [dbo].[Load_FuelMgtMasterData]
AS
    BEGIN
        SET NOCOUNT ON;

        DECLARE
            @SQLString VARCHAR(500)
        ,   @ImportName VARCHAR(200)
        ,   @Today DATE
        ,   @Yesterday DATE
        ,   @SourceAffiliates VARCHAR(200);

        SET @Today = GETDATE();
        SET @Yesterday = DATEADD(DAY, -1, @Today);
        TRUNCATE TABLE dbo.SourceFM_Affiliates;
        SET @ImportName = '\\' + +@@ServerName
            + '\WorkA\merchantportal\affiliates.txt';
        SET @SQLString = 'BULK INSERT ' + @SourceAffiliates + ' FROM '''
            + @ImportName + '''';
        EXEC (@SQLString);
    END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE dbo.Load_FuelMgtMasterData ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    /*** SSC-EWI-0040 - THE 'SET' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
    /*        SET NOCOUNT ON*/
    ;
    let SQLSTRING;
    let IMPORTNAME;
    let TODAY;
    let YESTERDAY;
    let SOURCEAFFILIATES;
    TODAY = SELECT(`   CURRENT_TIMESTAMP() :: TIMESTAMP`);
    YESTERDAY = SELECT(`   DATEADD(DAY, -1, ?)`,[TODAY]);
    EXEC(`        TRUNCATE TABLE dbo.SourceFM_Affiliates`);
    IMPORTNAME = `\\` + SERVERNAME + `\WorkA\merchantportal\affiliates.txt`;
    SQLSTRING =
        // ** SSC-EWI-TS0032 - THE BULK INSERT WAS PART OF A DYNAMIC SQL, WHICH MAKES SOME OF THE TRANSLATED ELEMENTS INVALID UNLESS EXECUTED OUTSIDE DYNAMIC CODE. **
        `CREATE OR REPLACE FILE FORMAT FILE_FORMAT_638923328992788100;

CREATE OR REPLACE STAGE STAGE_638923328992788100
FILE_FORMAT = FILE_FORMAT_638923328992788100;

PUT file://${IMPORTNAME} @STAGE_638923328992788100 AUTO_COMPRESS = FALSE;

COPY INTO ${SOURCEAFFILIATES}
FROM @STAGE_638923328992788100/${IMPORTNAME}`;
    EXEC(`${SQLSTRING}`);
$$;
```

#### Best Practices

- Extract the `PUT` command that resulted from the Dynamic `BULK INSERT` statement, and execute it before calling the procedure.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0034

RETURNS clause incomplete due to missing symbols

### Severity

High

#### Description

This EWI is added to the output code when the `RETURNS TABLE` clause of a `CREATE FUNCTION` could not be properly generated. This happens when the columns that must be specified in the resulting `RETURNS TABLE` clause cannot be inferred, thus leaving the `RETURNS TABLE` clause empty.

#### Code Example

##### Input Code:

Copy code

```
 CREATE FUNCTION Sales.ufn_SalesByStore2()
RETURNS TABLE
AS
RETURN
(
  WITH CTE AS (
  SELECT DepartmentID, Name, GroupName
  FROM HumanResources.Department
  )
  SELECT tab.* FROM CTE tab
);

GO

SELECT * FROM GetDepartmentInfo();
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "HumanResources.Department" **
CREATE OR REPLACE FUNCTION Sales.ufn_SalesByStore2 ()
RETURNS TABLE(
  DepartmentID STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN DepartmentID WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  Name STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN Name WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  GroupName STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN GroupName WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
AS
$$
  --** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
    WITH CTE AS (
    SELECT
      DepartmentID,
      Name,
      GroupName
    FROM
      HumanResources.Department
    )
    SELECT tab.* FROM
    CTE tab
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "GetDepartmentInfo" **

SELECT
    *
FROM
    TABLE(GetDepartmentInfo());
```

#### Best Practices

- The causes for this issue may vary. Be sure to include all the objects that your code needs. If the issue persists even though the migration has access to all the necessary objects, please do contact us with information about your specific scenario.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0035

Declaring a Cursor Variable that it is never initialized is not supported.

### Severity

Medium

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

Currently, a Cursor Variable that is declared but never initialized is not supported by Snowflake. Thus, the EWI is added, and the code commented out.

#### Code Example

##### Input Code:

Copy code

```
 CREATE OR ALTER PROCEDURE notInitializedCursorTest
AS
BEGIN
    -- Should be marked with SSC-EWI-TS0035
    DECLARE @MyCursor CURSOR, @MyCursor2 CURSOR;
    -- Should not be marked
    DECLARE cursorVar CURSOR FORWARD_ONLY STATIC READ_ONLY
        FOR
        SELECT someCol
        FROM someTable;
    RETURN 'DONE';
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE notInitializedCursorTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        -- Should be marked with SSC-EWI-TS0035
        !!!RESOLVE EWI!!! /*** SSC-EWI-TS0035 - CURSOR VARIABLE DECLARED BUT NEVER INITIALIZED, THIS IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
        MYCURSOR CURSOR;
        !!!RESOLVE EWI!!! /*** SSC-EWI-TS0035 - CURSOR VARIABLE DECLARED BUT NEVER INITIALIZED, THIS IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
        MYCURSOR2 CURSOR;
        -- Should not be marked
        cursorVar CURSOR
        FOR
            SELECT
                someCol
            FROM
                someTable;
    BEGIN
         
         
        RETURN 'DONE';
    END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0036

Snowflake Scripting only supports Local Cursors.

### Severity

Medium

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when Cursors other than Local Cursors are identified. Currently, Snowflake Scripting only supports Local Cursors. Thus, all Cursors are translated as Local Cursors.

#### Code Example

##### Input Code:

Copy code

```
 CREATE OR ALTER PROCEDURE globalCursorTest
AS
BEGIN
    -- Should be marked with SSC-EWI-TS0036
    DECLARE MyCursor CURSOR GLOBAL STATIC READ_ONLY
        FOR
        SELECT *
        FROM exampleTable;
    -- Should not be marked
    DECLARE MyCursor2 CURSOR LOCAL STATIC READ_ONLY
        FOR
        SELECT testCol
        FROM myTable;
    RETURN 'DONE';
END;
```

Copy code

```
 CREATE OR REPLACE PROCEDURE globalCursorTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        -- Should be marked with SSC-EWI-TS0036
        !!!RESOLVE EWI!!! /*** SSC-EWI-TS0036 - SNOWFLAKE SCRIPTING ONLY SUPPORTS LOCAL CURSORS ***/!!!
        MyCursor CURSOR
        FOR
            SELECT
                *
            FROM
                exampleTable;
        -- Should not be marked
        MyCursor2 CURSOR
        FOR
            SELECT
                testCol
            FROM
                myTable;
    BEGIN
         
         
        RETURN 'DONE';
    END;
$$;
```

Copy code

```

```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0037

Snowflake Scripting Cursors are non-scrollable.

### Severity

Medium

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

Snowflake Scripting Cursors are non-scrollable. Currently, only FETCH NEXT is supported.

#### Code Example

##### Input Code:

Copy code

```
 CREATE OR ALTER PROCEDURE scrollablecursorTest
AS
BEGIN
    -- Should be marked with SSC-EWI-TS0037
    DECLARE CursorVar CURSOR SCROLL STATIC READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    -- Should not be marked
    DECLARE CursorVar2 CURSOR STATIC READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE CursorVar3 CURSOR FORWARD_ONLY STATIC READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    RETURN 'DONE';
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE scrollablecursorTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		-- Should be marked with SSC-EWI-TS0037
		!!!RESOLVE EWI!!! /*** SSC-EWI-TS0037 - SNOWFLAKE SCRIPTING CURSORS ARE NON-SCROLLABLE, ONLY FETCH NEXT IS SUPPORTED ***/!!!
		CursorVar CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		-- Should not be marked
		CursorVar2 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		CursorVar3 CURSOR
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

## SSC-EWI-TS0039

Multiple SET Statements for the same cursor found.

### Severity

Medium

#### Description

This EWI is added when multiple SET Statements for the same cursor are found; All additional SET Statements are also commented out. This happens because having multiple SET Statements for the same cursor is not valid in Snowflake Scripting.

#### Example Code:

##### This EWI is added when multiple SET Statements for the same cursor are found; All additional SET Statements are also commented out. This happens because having multiple SET Statements for the same cursor is not valid in Snowflake Scripting.

#### Example Code:

##### Input Code:

Copy code

```
 CREATE OR ALTER PROCEDURE multipleSetExample
AS
BEGIN
    DECLARE @MyCursor CURSOR;
    DECLARE @MyCursor2 CURSOR STATIC READ_ONLY
	FOR  
	SELECT FirstName
	FROM vEmployee;
    DECLARE @MyCursor3 CURSOR;
    
    SET @MyCursor = CURSOR STATIC READ_ONLY
        FOR
        SELECT col3
        FROM defaultTable;
        
    SET @MyCursor3 = CURSOR STATIC READ_ONLY
    FOR
    SELECT *
    FROM someTable;
    
    SET @MyCursor = CURSOR DYNAMIC
        FOR
        SELECT col2
        FROM exampleTable;
        
    SET @MyCursor2 = CURSOR STATIC READ_ONLY
        FOR
        SELECT col3
        FROM defaultTable;
        
    RETURN 'DONE';
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE multipleSetExample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		MYCURSOR CURSOR
		FOR
			SELECT col3
			FROM defaultTable;
		MYCURSOR2 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		MYCURSOR3 CURSOR
		FOR
			SELECT *
			FROM someTable;
	BEGIN
		 
		 
		 
		 
		 
		DECLARE
		MYCURSOR CURSOR
		FOR
			SELECT col3
			FROM defaultTable;
		MYCURSOR2 CURSOR
		FOR
			SELECT
				FirstName
			FROM
				vEmployee;
		MYCURSOR3 CURSOR
		FOR
			SELECT *
			FROM someTable;
	BEGIN
		 
		 
		 
		 
		 
		!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SET CURSOR' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-TS0039 - CURSOR VARIABLE MYCURSOR SET MULTIPLE TIMES, THIS IS NOT VALID IN SNOWFLAKE SCRIPTING ***/!!!

		SET @MyCursor = CURSOR DYNAMIC
		    FOR
		    SELECT col2
		    FROM exampleTable;
		!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SET CURSOR' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-TS0039 - CURSOR VARIABLE MYCURSOR2 SET MULTIPLE TIMES, THIS IS NOT VALID IN SNOWFLAKE SCRIPTING ***/!!!

    SET @MyCursor2 = CURSOR STATIC READ_ONLY
        FOR
        SELECT col3
        FROM defaultTable;
		RETURN 'DONE';
	END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0041

XML data type methods are not supported in Snowflake.

### Severity

Medium

#### Description

This EWI is added for the following [XML data type methods](https://docs.microsoft.com/en-us/sql/t-sql/xml/xml-data-type-methods?view=sql-server-ver15) that are not supported in Snowflake SQL:

- Value
- Query
- Exist
- Modify
- Nodes

#### Code Example

##### Input Code:

Copy code

```
 CREATE PROCEDURE xml_procedure
    @inUserGroupsXML XML
AS
BEGIN
    SELECT  entities.entity.value('TypeID[1]', 'VARCHAR(100)') AS TypeID
        ,entities.entity.value('Name[1]', 'VARCHAR(100)') AS Name
    INTO  #tmpUserGroups
    FROM  @inUserGroupsXML.nodes('/entities/entity') entities(entity)
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE xml_procedure (INUSERGROUPSXML TEXT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CREATE OR REPLACE TEMPORARY TABLE T_tmpUserGroups AS
            SELECT
                XMLGET(entity, '$') :: VARCHAR(100) AS TypeID
                ,
                XMLGET(entity, '$') :: VARCHAR(100) AS Name
            FROM
                !!!RESOLVE EWI!!! /*** SSC-EWI-TS0041 - XML TYPE METHOD nodes IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                T_inUserGroupsXML('/entities/entity') entities (
                    entity
                );
    END;
$$;
```

#### Best Practices

- Consider using UDFs to emulate the behavior of the source code
- You can [check this documentation](https://medium.com/snowflake/working-with-xml-in-snowflake-part-ii-774b4d32399) and review some possible approaches to work with XML datatypes in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0043

WITH XMLNAMESPACES is not supported in Snowflake.

### Severity

Medium

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added for the [WITH XMLNAMESPACES](https://docs.microsoft.com/en-us/sql/relational-databases/xml/add-namespaces-to-queries-with-with-xmlnamespaces?view=sql-server-ver15) clause which is not supported in Snowflake SQL

#### Code Example

##### Input Code:

Copy code

```
 WITH XMLNAMESPACES ('uri' as ns1)
SELECT ProductID as 'ns1:ProductID',
Name      as 'ns1:Name',
Color     as 'ns1:Color'
FROM Production.Product
WHERE ProductID = 316
FOR XML RAW, ELEMENTS XSINIL
```

##### Generated Code:

Copy code

```
 --** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
WITH
     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0043 - WITH XMLNAMESPACES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
 XMLNAMESPACES ('uri' as VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE NS1 IS NOT SUPPORTED IN SNOWFLAKE ***/!!! NOT NULL)
SELECT
ProductID AS "ns1:ProductID",
Name AS "ns1:Name",
Color AS "ns1:Color"
FROM
Production.Product
WHERE
ProductID = 316
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0044 - FOR XML RAW CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FOR XML RAW, ELEMENTS XSINIL;
```

#### Best Practices

- Consider using UDFs to emulate the behavior of the source code. The following code provides suggestions of UDFs that can be used to achieve recreating the original behavior:

##### SQL Server

Copy code

```
 CREATE  TABLE PRODUCT (ProductID INTEGER, Name VarChar(20), Color VarChar(20));
INSERT INTO PRODUCT(PRODUCTID, NAME, COLOR) VALUES(1,'UMBRELLA','RED');
INSERT INTO PRODUCT(PRODUCTID, NAME, COLOR) VALUES(2,'SHORTS','BLUE');
INSERT INTO PRODUCT(PRODUCTID, NAME, COLOR) VALUES(3,'BALL','YELLOW');

WITH XMLNAMESPACES ('uri' as ns1)  
SELECT ProductID as 'ns1:ProductID',  
       Name      as 'ns1:Name',  
       Color     as 'ns1:Color'  
FROM Product  
FOR XML RAW
```

##### Snowflake SQL

Copy code

```
 CREATE OR REPLACE TABLE PRODUCT (
       ProductID INTEGER,
       Name VARCHAR(20),
       Color VARCHAR(20))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/12/2024" }}'
;

INSERT INTO PRODUCT (PRODUCTID, NAME, COLOR) VALUES(1,'UMBRELLA','RED');
INSERT INTO PRODUCT (PRODUCTID, NAME, COLOR) VALUES(2,'SHORTS','BLUE');
INSERT INTO PRODUCT (PRODUCTID, NAME, COLOR) VALUES(3,'BALL','YELLOW');

--** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **

WITH
     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0043 - WITH XMLNAMESPACES IS NOT SUPPORTED IN SNOWFLAKE ***/!!! XMLNAMESPACES ('uri' as ns1)
SELECT
       ProductID AS "ns1:ProductID",
       Name AS "ns1:Name",
       Color AS "ns1:Color"
FROM
       Product
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0044 - FOR XML RAW CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FOR XML RAW;
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWI

1. [SSC-PRF-TS0001](../performance-review/sqlServerPRF#ssc-prf-ts0001): Performance warning - recursion for CTE not checked. Might require a recursive keyword.
2. [SSC-EWI-TS0044](#ssc-ewi-ts0044): FOR XML clause is not supported in Snowflake.
3. [SSC-EWI-TS0015](#ssc-ewi-ts0015): Data type not supported in Snowflake

## SSC-EWI-TS0044

FOR XML clause is not supported in Snowflake.

### Severity

Critical

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added for the [FOR XML](https://docs.microsoft.com/en-us/sql/relational-databases/xml/for-xml-sql-server?view=sql-server-ver15) clause which is not supported in Snowflake SQL

#### Code Example

##### Input Code:

Copy code

```
 SELECT TOP 1 LastName
FROM AdventureWorks2019.Person.Person
FOR XML AUTO;
```

##### Generated Code:

Copy code

```
 SELECT TOP 1
LastName
FROM
AdventureWorks2019.Person.Person
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0044 - FOR XML AUTO CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FOR XML AUTO;
```

#### Best Practices

- Consider using UDFs to emulate the behavior of the source code. The following code provides suggestions of UDFs that can be used to achieve recreating the original behavior:

SQL Server

##### Query

Copy code

```
 CREATE TABLE TEMPTABLE (Ref INT, Des NVARCHAR(100), Qty INT)

INSERT INTO tempTable VALUES (100001, 'Normal', 1), (100002, 'Foobar', 1), (100003, 'Hello World', 2)

GO

-- FOR XML
SELECT *
FROM TempTable
FOR XML AUTO

GO
 
-- FOR XML RAW
SELECT *
FROM TempTable
FOR XML RAW
```

##### Result

Copy code

```
 -- FOR XML
<TempTable Ref="100001" Des="Normal" Qty="1"/><TempTable Ref="100002" Des="Foobar" Qty="1"/><TempTable Ref="100003" Des="Hello World" Qty="2"/>

-- FOR XML RAW
<row Ref="100001" Des="Normal" Qty="1"/><row Ref="100002" Des="Foobar" Qty="1"/><row Ref="100003" Des="Hello World" Qty="2"/>
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE TABLE TEMPTABLE (
Ref INT,
Des VARCHAR(100),
Qty INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO tempTable VALUES (100001, 'Normal', 1), (100002, 'Foobar', 1), (100003, 'Hello World', 2);

-- FOR XML
SELECT
*
FROM
TempTable
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0044 - FOR XML AUTO CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FOR XML AUTO;

-- FOR XML RAW
SELECT
*
FROM
TempTable
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0044 - FOR XML RAW CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FOR XML RAW;
```

##### Result

Copy code

```
 -- FOR XML
<TempTable DES="Normal" QTY="1" REF="100001"  /><TempTable DES="Foobar" QTY="1" REF="100002"  /><TempTable DES="Hello World" QTY="2" REF="100003"  />

-- FOR XML RAW
<row DES="Normal" QTY="1" REF="100001"  /><row DES="Foobar" QTY="1" REF="100002"  /><row DES="Hello World" QTY="2" REF="100003"  />
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0045

Labeled Statement is not supported in Snowflake Scripting.

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when a [labeled statement](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/goto-transact-sql?view=sql-server-ver15) in T-SQL is encountered that cannot be automatically transformed.

When GOTO/Label patterns appear inside a stored procedure with only forward jumps and top-level labels, they are automatically transformed into nested procedure definitions with `CALL`/`RETURN` semantics — no EWI is emitted in those cases. See the [LABEL and GOTO translation reference](../../translation-references/transact/transact-create-procedure-snow-script#label-and-goto) for details on the transformation.

This EWI is only emitted when the label **cannot** be transformed. This happens when the procedure contains a backward `GOTO` (one that targets a label appearing earlier in the source, which would require recursive calls), when labels appear inside anonymous blocks or UDFs (which do not support nested procedure definitions), or when labels are declared inside nested control flow blocks like `IF`, `WHILE`, or `TRY` (which cannot be extracted into nested procedures).

#### Code Example

The following example shows a backward GOTO pattern (retry logic) where the label `RetryConnection` appears before the `GOTO` that targets it, preventing automatic transformation:

##### Input Code:

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

##### Generated Code:

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

#### Best Practices

- For backward GOTO patterns like retry logic, refactor the control flow to use `WHILE` or `LOOP` constructs instead.
- For labels in anonymous blocks or UDFs, restructure the code into separate procedures or use `IF/ELSE` control flow.
- Forward GOTO/Label patterns inside stored procedures are automatically transformed — no manual action is required for those cases.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

1. [SSC-EWI-TS0087](sqlServerEWI#ssc-ewi-ts0087): GOTO is not supported in Snowflake.
2. [SSC-EWI-TS0103](sqlServerEWI#ssc-ewi-ts0103): GOTO targeting a label inside a nested block is not supported in Snowflake.

## SSC-EWI-TS0046

System table is not supported in Snowflake.

### Severity

Medium

#### Description

This EWI is added when referencing [SQL Server system tables](https://docs.microsoft.com/en-us/sql/relational-databases/system-catalog-views/object-catalog-views-transact-sql?view=sql-server-ver15) not supported or without equivalent in Snowflake SQL. See the [supported and unsupported system tables reference](../../translation-references/transact/transact-system-tables) for the complete list.

#### Code Example

##### Input Code:

Copy code

```
 SELECT *
FROM 
    sys.all_sql_modules
WHERE 
    [STATE] = 0; -- state must be ONLINE
```

##### Generated Code:

Copy code

```
 SELECT
    *
FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0046 - SYSTEM TABLE sys.all_sql_modules IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
    sys.all_sql_modules
WHERE
    STATE = 0; -- state must be ONLINE
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0047

RAISERROR Error Message may differ because of the SQL Server string format.

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0019](../functional-difference/sqlServerFDM#ssc-fdm-ts0019) documentation

### Severity

Low

#### Description

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
		!!!RESOLVE EWI!!! /*** SSC-EWI-TS0047 - RAISERROR ERROR MESSAGE MAY DIFFER BECAUSE OF THE SQL SERVER STRING FORMAT ***/!!!
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

## SSC-EWI-TS0049

Multiple Line If Body translation planned to be delivered in the future.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

Most of the cases in`IF` statements that contain a `Begin ... End` block inside their body are supported. This is a successful scenario (no SSC-EWI-TS0049 generated).

#### Code Example

##### Input Code:

Copy code

```
 CREATE OR ALTER FUNCTION [PURCHASING].[FOO](@status INT)
Returns INT
As
Begin
    declare @result as int = 10;
    SELECT @result = quantity FROM TABLE1 WHERE COL1 = @status;
    IF @result = 3
    BEGIN
        IF @result>0 SELECT @result=0  ELSE SELECT @result=1
        SELECT @result = 1 
    END
    return @result;
End
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE PROCEDURE PURCHASING.FOO (STATUS INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        RESULT INT := 10;
    BEGIN
         
        SELECT
            quantity
        INTO
            :RESULT
        FROM
            TABLE1
        WHERE
            COL1 = :STATUS;
        IF (:RESULT = 3) THEN
            BEGIN
                IF (:RESULT >0) THEN SELECT
                        0
                    INTO
                        :RESULT;
                ELSE
                    SELECT
                        1
                    INTO
                        :RESULT;
                END IF;
        SELECT
                    1
                INTO
                    :RESULT;
            END;
        END IF;
        RETURN :RESULT;
    END;
$$;
```

Note

In a general code example (Like the on top) the conversion is done successfully. But there are some edge cases where the “IF” statement is not converted and the EWI will be generated.

#### Manual Support

##### Case 1: Single Statement

For these cases, the transformation would be straightforward, since the transformed statement would appear in a select clause

Copy code

```
 IF @result = 0
BEGIN 
    SET @result =1
END
```

Copy code

```
 CASE WHEN (SELECT RESULT FROM CTE2)= 0 THEN
( SELECT 1 AS RESULT )
```

##### Case 2: Multiple Statements

For cases in which multiple statements are being transformed, we should transform the N Statement, and use it as the source table for the N+1 Statement.

Copy code

```
 IF @result = 0
BEGIN 
    Statement1
    Statement2
    Statement3
END
```

Copy code

```
 CASE WHEN (SELECT RESULT FROM CTE2)= 0 THEN
(
    SELECT TransformedStatement3
    FROM (
        SELECT TransformedStatement2
        FROM (
            SELECT TransformedStatement1
        ) T1
    ) T2
)
```

##### Case 3: Multiple set statements

For these cases, it will be necessary to replicate a transformation for each set statement.

Copy code

```
 IF @result = 0
BEGIN 
    SET @var1 = 1
    SET @var2 = 3
    SET @var3 = @var2
END
```

Copy code

```
 WITH CTE1 AS (
    SELECT 
        CASE WHEN (SELECT
                        RESULT
                    FROM
                        CTE0) = 0 THEN
        (SELECT 1) AS VAR1)
WITH CTE2 AS (
    SELECT
        CASE WHEN (SELECT
                        RESULT
                    FROM
                        CTE0)= 0 THEN
        (SELECT 3) AS VAR2)
WITH CTE3 AS (
    SELECT
        CASE WHEN (SELECT
                        RESULT
                    FROM
                        CTE0)= 0 THEN
        (SELECT T1.VAR2 
        FROM ((SELECT 3) AS VAR2) AS T1) AS VAR3) 
...
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0055

Default constraint was commented out and may have been added to a table definition.

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0020](../functional-difference/sqlServerFDM#ssc-fdm-ts0020) documentation.

### Severity

Medium

#### Description

This EWI is added when the default constraint is present in an Alter Table statement.

Currently, there is no support for that constraint. A workaround available to transform it, is when the table is previously defined to the Alter Table, in this way we identify the references, and the default constraint is unified on the table definition; otherwise, the constraint is only commented out.

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
  CONSTRAINT col1_constraint DEFAULT 30 FOR col1;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE table1 (
  col1 INTEGER DEFAULT 50,
  col2 VARCHAR COLLATE 'EN-CS',
  col3 DATE
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

ALTER TABLE table1
ADD col4 INTEGER,
  CONSTRAINT col1_constraint
                             !!!RESOLVE EWI!!! /*** SSC-EWI-TS0055 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION ***/!!!
                             DEFAULT 50 FOR col1,
  CONSTRAINT col1_constraint
                             !!!RESOLVE EWI!!! /*** SSC-EWI-TS0055 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION ***/!!!
                             DEFAULT 30 FOR col1;
```

Note

If all the content of the Alter Table is invalid, the Alter Table will be commented out.

#### Known Issues

When different default constraints are declared over the same column, only the first will be reflected on the Create Table Statement.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0056

A MASKING POLICY was created as a substitute for MASKED WITH.

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0021](../functional-difference/sqlServerFDM#ssc-fdm-ts0021) documentation

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

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
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0057 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER ***/!!!
CREATE OR REPLACE MASKING POLICY "default" AS
(val STRING)
RETURNS STRING ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE 'xxxxx'
END;

ALTER TABLE IF EXISTS table_name MODIFY COLUMN column_name!!!RESOLVE EWI!!! /*** SSC-EWI-TS0056 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/!!!  SET MASKING POLICY "default";
```

Note

The MASKING POLICY will be created previous to the ALTER TABLE statement. And it is expected to have and approximate behaviour. Some tweaks might be needed in regards to roles and user privileges.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0057

The user must previously define the masking role.

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0022](../functional-difference/sqlServerFDM#ssc-fdm-ts0022) documentation

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

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
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0057 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER ***/!!!
CREATE OR REPLACE MASKING POLICY "partial_1_xxxxx_1" AS
(val STRING)
RETURNS STRING ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE LEFT(val, 1) || 'xxxxx' || RIGHT(val, 1)
END;

ALTER TABLE IF EXISTS tableName MODIFY COLUMN columnName!!!RESOLVE EWI!!! /*** SSC-EWI-TS0056 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/!!!  SET MASKING POLICY "partial_1_xxxxx_1";
```

Note

As shown on line 6, there is a placeholder where the defined roles can be placed. There is room for one or several values separated by commas. Also, here, the use of single quotes is mandatory for each of the values.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0060

Datetime interval not supported by Snowflake.

### Severity

Medium

#### Description

This EWI is added when one of the following time parts is used as a parameter for a date-related function because they are not supported in Snowflake. For more information go to ‘supported date time parts ([Date & Time Functions | Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/functions-date-time#label-supported-date-time-parts)).

#### Code Example

##### Input code

Copy code

```
 SELECT
    -- Supported
    DATEPART(second, getdate()),
    -- Not supported
    DATEPART(millisecond, getdate()),
    DATEPART(microsecond, getdate());
```

##### Generated Code:

Copy code

```
 SELECT
    -- Supported
    DATE_PART(second, CURRENT_TIMESTAMP() :: TIMESTAMP),
    -- Not supported
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0060 - TIME PART 'millisecond' NOT SUPPORTED AS A FUNCTION PARAMETER ***/!!!
    DATEPART(millisecond, CURRENT_TIMESTAMP() :: TIMESTAMP),
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0060 - TIME PART 'microsecond' NOT SUPPORTED AS A FUNCTION PARAMETER ***/!!!
    DATEPART(microsecond, CURRENT_TIMESTAMP() :: TIMESTAMP);
```

#### Best Practices

- An UDF could be created to manually extract unsupported time parts in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0061

ALTER COLUMN not supported

### Severity

Medium

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added whenever there is an unsupported ALTER COLUMN statement

#### Code Example

##### Input Code:

Copy code

```
 ALTER TABLE SampleTable
ALTER COLUMN SampleColumn INT NULL SPARSE;
```

##### Generated Code:

Copy code

```
 ALTER TABLE IF EXISTS SampleTable
ALTER COLUMN SampleColumn
                          !!!RESOLVE EWI!!! /*** SSC-EWI-TS0061 - ALTER COLUMN COMMENTED OUT BECAUSE SPARSE COLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                          INT NULL SPARSE;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0063

Time zone not supported in Snowflake.

### Severity

Critical

#### Description

This EWI is added when there are Time zones that are not supported in Snowflake

#### Code Example

##### Input Code:

Copy code

```
 SELECT current_timestamp at time zone 'Turks And Caicos Standard Time';
```

##### Generated Code:

Copy code

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0063 - TIME ZONE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CURRENT_TIMESTAMP() at time zone 'Turks And Caicos Standard Time'
                                                                 ;
```

#### Best Practices

- A user defined function can be created to support multiple timezones.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0067

Invalid parameters in OPENXML table-valued function.

### Severity

Critical

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when there are invalid parameters in the OPENXML, specifically when the XML path cannot be accessed.

To avoid this EWI, please send the explicit node path through the parameters.

##### Input Code:

Copy code

```
 SELECT
    *
FROM
    OPENXML (@idoc, @path, 1) WITH (
        CustomerID VARCHAR(10),
        ContactName VARCHAR(20)
    );
```

##### Generated Code:

Copy code

```
 SELECT
    *
FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0067 - INVALID PARAMETERS IN OPENXML TABLE-VALUED FUNCTION ***/!!!
    OPENXML(@idoc, @path, 1);
```

##### Input code (Explicit parameter)

Copy code

```
 SELECT
    *
FROM
    OPENXML (@idoc, '/ROOT/Customer', 1) WITH(
        CustomerID VARCHAR(10),
        ContactName VARCHAR(20)
    );
```

##### Generated Code (Explicit parameter)

Copy code

```
 SELECT
    Left(value:Customer['@CustomerID'], '10') AS 'CustomerID',
    Left(value:Customer['@ContactName'], '20') AS 'ContactName'
FROM
    OPENXML_UDF($idoc, ':ROOT:Customer');
```

#### Best Practices

- Try to see if the path can be explicitly passed as a parameter.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0070

CURRENT\_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases.

Note

This `EWI` is deprecated, please refer to [SSC-FDM-TS0024](../functional-difference/sqlServerFDM#ssc-fdm-ts0024) documentation.

### Description

This EWI is added when the At Time Zone has the CURRENT\_TIMESTAMP. This is because the result may have different results in some instances.

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
CONVERT_TIMEZONE('Pacific/Honolulu', CURRENT_TIMESTAMP() !!!RESOLVE EWI!!! /*** SSC-EWI-TS0070 - CURRENT_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases ***/!!!);
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

## SSC-EWI-TS0072

RETURN statement will be ignored due to previous RETURN statement

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added when SELECT statements and OUPUT parameters should be returned. In this case, the resultsets from the SELECT statements are prioritized.

##### Input Code:

Copy code

```
 CREATE PROCEDURE SOMEPROC(@product_count INT OUTPUT,  @123 INT OUTPUT)
AS
BEGIN
		SELECT * from AdventureWorks.HumanResources.Department;
        SELECT * from AdventureWorks.HumanResources.Employee;
END
```

##### Generated Code:

Copy code

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "AdventureWorks.HumanResources.Department", "AdventureWorks.HumanResources.Employee" **
CREATE OR REPLACE PROCEDURE SOMEPROC (PRODUCT_COUNT OUT INT, _123 OUT INT)
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		ProcedureResultSet1 VARCHAR;
		ProcedureResultSet2 VARCHAR;
		return_arr ARRAY := array_construct();
	BEGIN
		ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
			SELECT
				*
			from
				AdventureWorks.HumanResources.Department;
		return_arr := array_append(return_arr, :ProcedureResultSet1);
		ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
			SELECT
				*
			from
				AdventureWorks.HumanResources.Employee;
		return_arr := array_append(return_arr, :ProcedureResultSet2);
		--** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
		RETURN return_arr;
	END;
$$;
```

#### Best Practices

- Remove the RETURN statement that should be ignored.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWI

1. [SSC-FDM-0020](../functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables;

## SSC-EWI-TS0073

Error message could be different in snowflake

Note

This EWI is deprecated, please refer to [SSC-FDM-TS0023](../functional-difference/sqlServerFDM#ssc-fdm-ts0023) documentation

### Severity

Low

#### Description

This EWI is added in the transformation of ERROR\_MESSAGE(). The exact message of the error could change in Snowflake.

##### Input Code:

Copy code

```
 SET @varErrorMessage = ERROR_MESSAGE()
```

##### Generated Code

Copy code

```
 BEGIN
VARERRORMESSAGE := SQLERRM !!!RESOLVE EWI!!! /*** SSC-EWI-TS0073 - ERROR MESSAGE COULD BE DIFFERENT IN SNOWFLAKE ***/!!!;
END;
```

#### Recommendation

If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-TS0074

Cast result may be different from TRY\_CAST/TRY\_CONVERT function due to missing dependencies

### Severity

Low

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI is added in the transformation of TRY\_CAST and TRY\_CONVERT functions. The exact result of these functions may change in Snowflake due to missing dependencies (some data types could not be resolved). This could be because the dependency was not in the source code.

##### Input Code:

Copy code

```
 SELECT TRY_CONVERT( INT, col1) FROM TABLE1;

SELECT TRY_CAST(COL1 AS FLOAT) FROM TABLE1
```

##### Generated Code

Copy code

```
 SELECT
CAST(col1 AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/!!!RESOLVE EWI!!! /*** SSC-EWI-TS0074 - CAST RESULT MAY BE DIFFERENT FROM TRY_CONVERT FUNCTION DUE TO MISSING DEPENDENCIES ***/!!!
FROM
TABLE1;

SELECT
CAST(COL1 AS FLOAT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/!!!RESOLVE EWI!!! /*** SSC-EWI-TS0074 - CAST RESULT MAY BE DIFFERENT FROM TRY_CAST FUNCTION DUE TO MISSING DEPENDENCIES ***/!!!
FROM
TABLE1;
```

#### Recommendation

If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-TS0075

Built In Procedure Not Supported

### Severity

Medium

#### Description

Translation for built-in procedures is not currently supported.

#### Example Code

##### Input Code:

Copy code

```
 EXEC sp_column_privileges_rowset_rmt 'Caption';
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0075 - TRANSLATION FOR BUILT-IN PROCEDURE 'sp_column_privileges_rowset_rmt' IS NOT CURRENTLY SUPPORTED. ***/!!!
EXEC sp_column_privileges_rowset_rmt 'Caption';
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0076

Default Parameters May Need To Be Reordered

Note

This EWI is deprecated. Please refer to [SSC-EWI-0002](generalEWI#ssc-ewi-0002) for the replacement issue identified by `IssueResources.json`.

### Severity

Medium

#### Description

Default parameters may need to be reordered. Snowflake only supports default parameters at the end of the parameters declarations.

#### Example Code

##### Input Code:

Copy code

```
 CREATE PROCEDURE MySampleProc
    @Param1 NVARCHAR(50) = NULL,
    @Param2 NVARCHAR(10),
    @Param3 NVARCHAR(10) = NULL,
    @Param4 NVARCHAR(10)
AS   
    SELECT 1;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0076 - DEFAULT PARAMETERS MAY NEED TO BE REORDERED. SNOWFLAKE ONLY SUPPORTS DEFAULT PARAMETERS AT THE END OF THE PARAMETERS DECLARATIONS. ***/!!!
CREATE OR REPLACE PROCEDURE MySampleProc (PARAM1 STRING DEFAULT NULL, PARAM2 STRING, PARAM3 STRING DEFAULT NULL, PARAM4 STRING)
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
        SELECT 1);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0077

Collation Not Supported

### Severity

Low

#### Description

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
--           !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATION Albanian_BIN NOT SUPPORTED ***/!!!
-- COLLATE Albanian_BIN
                     ;

SELECT 'a'
--           !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATION Albanian_CI_AI NOT SUPPORTED ***/!!!
-- COLLATE Albanian_CI_AI
                       ;

CREATE OR REPLACE TABLE ExampleTable (
    ID INT,
    Name VARCHAR(50)
--                     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATION collateName NOT SUPPORTED ***/!!!
-- COLLATE collateName
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0078

Default value not allowed in Snowflake.

### Severity

Medium

#### Description

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
                         !!!RESOLVE EWI!!! /*** SSC-EWI-TS0078 - DEFAULT OPTION NOT ALLOWED IN SNOWFLAKE ***/!!!
                         DEFAULT RANDOM(10);
```

##### 

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0079

Database console command is not supported

### Severity

Medium

#### Description

This EWI is added when a DBCC statement is found inside the input code.  
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
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0079 - DATABASE CONSOLE COMMAND 'CHECKIDENT' IS NOT SUPPORTED. ***/!!!
DBCC CHECKIDENT(@a, RESEED, @b) WITH NO_INFOMSGS;
```

#### Best Practices

- No additional user actions are required; it is just informative.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0080

Changing the execution context at runtime is not supported in Snowflake

### Severity

High

#### Description

Users in SQL Server can use the command `EXECUTE AS` to temporarily change the execution context, this modifies the execution privileges and affects the results of context-dependent functions like `USER_NAME()`. The `REVERT` command can be used to restore the context previous to the last `EXECUTE AS`.

Snowflake only supports the definition of an execution context in procedures, using either the `CREATE PROCEDURE` or `ALTER PROCEDURE` statements. Changing the context at runtime is not supported.

#### Code Example

Input Code:

Copy code

```
 CREATE PROCEDURE proc1()
WITH EXECUTE AS OWNER
AS
BEGIN
	SELECT USER_NAME();
	EXECUTE AS CALLER;
	SELECT USER_NAME();
	REVERT;
	SELECT USER_NAME();
END

GO
```

Output Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/05/2024" }}'
EXECUTE AS OWNER
AS
$$
	DECLARE
		ProcedureResultSet1 VARCHAR;
		ProcedureResultSet2 VARCHAR;
		ProcedureResultSet3 VARCHAR;
		return_arr ARRAY := array_construct();
	BEGIN
		ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
			SELECT
				CURRENT_USER();
		return_arr := array_append(return_arr, :ProcedureResultSet1);
		!!!RESOLVE EWI!!! /*** SSC-EWI-TS0080 - CHANGING THE EXECUTION CONTEXT AT RUNTIME IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
	EXECUTE AS CALLER;
		ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
			SELECT
				CURRENT_USER();
		return_arr := array_append(return_arr, :ProcedureResultSet2);
		!!!RESOLVE EWI!!! /*** SSC-EWI-TS0080 - CHANGING THE EXECUTION CONTEXT AT RUNTIME IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
	REVERT;
		ProcedureResultSet3 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet3) AS
			SELECT
				CURRENT_USER();
		return_arr := array_append(return_arr, :ProcedureResultSet3);
		--** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
		RETURN return_arr;
	END;
$$;
```

#### Best Practices

- Refactor the code so it works without having to switch the context.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0081

Using a full join in a delete statement is not supported

### Description

When transforming the DELETE statement, the table references found in the FROM clause of the statement are extracted and moved to the USING clause of the Snowflake delete statement.

The following EWI warns the user about the limitations of the outer join (+) syntax in Snowflake. To preserve the LEFT and RIGHT JOINs used in the original code, outer join syntax (+) is added to the conditions to indicate such behavior. However, in Snowflake, the (+) syntax can’t be used to indicate FULL JOINs. For more information, see [Joins in the WHERE clause](https://docs.snowflake.com/en/sql-reference/constructs/where#joins-in-the-where-clause).

#### Example code

##### Input Code :

Copy code

```
DELETE Employees
FROM Employees FULL OUTER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID
WHERE Departments.DepartmentID IS NULL;
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0081 - USING A FULL JOIN IN A DELETE STATEMENT IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
DELETE FROM
Employees
USING Departments
WHERE
Departments.DepartmentID IS NULL
AND Employees.DepartmentID = Departments.DepartmentID;
```

#### Best Practices

- Check the logic of your FULL JOIN, it might be possible to rewrite it as other type of JOIN. For example, the code included in the example code is essentially the same as a LEFT JOIN:

Input:

Copy code

```
DELETE Employees
FROM Employees LEFT OUTER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID
WHERE Departments.DepartmentID IS NULL;
```

Output:

Copy code

```
 DELETE FROM
    Employees
USING Departments
WHERE
    Departments.DepartmentID IS NULL
    AND Employees.DepartmentID = Departments.DepartmentID(+);
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0082

CROSS APPLY has been converted to LEFT OUTER JOIN and requires manual validation.

### Description

Manual validation is required because the conversion from CROSS APPLY to LEFT OUTER JOIN can lead to incorrect results or unexpected behavior in Snowflake. While the two functions might seem similar, they handle certain situations differently, especially when the subquery has no matches or the subquery is correlated with the outer table.

#### Example code

##### Setup Data

Copy code

```
-- Create a table to store monthly sales or metric data
CREATE TABLE sales_metrics (
    metric_id INT PRIMARY KEY,
    january_value VARCHAR(35),
    february_value VARCHAR(35),
    march_value VARCHAR(35)
);

-- Insert sample data
INSERT INTO sales_metrics (metric_id, january_value, february_value, march_value) VALUES
(1, 'sales-jan-1', 'sales-feb-1', 'sales-march-1'),
(2, 'sales-jan-2', 'sales-feb-2', 'sales-march-2');
```

##### Input Code :

Copy code

```
SELECT
    m.metric_id,
    monthly_data.metric_value,
    monthly_data.month_number
FROM
    sales_metrics m
CROSS APPLY (
    SELECT m.january_value AS metric_value, '01' AS month_number
    UNION ALL
    SELECT m.february_value AS metric_value, '02' AS month_number
    UNION ALL
    SELECT m.march_value AS metric_value, '03' AS month_number
) AS monthly_data;
```

##### Generated Code:

Copy code

```
SELECT
    m.metric_id,
    monthly_data.metric_value,
    monthly_data.month_number
FROM
    sales_metrics m
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0082 - CROSS APPLY HAS BEEN CONVERTED TO LEFT OUTER JOIN AND REQUIRES MANUAL VALIDATION. ***/!!!
    LEFT OUTER JOIN
        (
               SELECT
                m.january_value AS metric_value, '01' AS month_number
               UNION ALL
               SELECT
                m.february_value AS metric_value, '02' AS month_number
               UNION ALL
               SELECT
                m.march_value AS metric_value, '03' AS month_number
           ) AS monthly_data;
```

#### Best Practices

### Key Scenarios Where LEFT OUTER JOIN May Fail

- **Filtering Behavior:** If the original `CROSS APPLY` was intended to filter out rows from the main table that have no matches in the subquery, a `LEFT OUTER JOIN` will not replicate this behavior. Instead, it will include those rows with `NULL` values for the joined columns, which may not be the intended result.
- **Correlated Subqueries:** `CROSS APPLY` is specifically designed to support correlated subqueries, where the subquery references columns from the outer query. A standard `LEFT OUTER JOIN` does not support this pattern in the same way. Attempting to convert a correlated `CROSS APPLY` to a `LEFT OUTER JOIN` can lead to syntax errors, Cartesian products (duplicate rows), or logically incorrect results.
- **Result Set Differences:** The semantics of `CROSS APPLY` and `LEFT OUTER JOIN` differ, especially when the subquery returns no rows. `CROSS APPLY` will exclude such rows from the result, while `LEFT OUTER JOIN` will include them with `NULL` values.

**Recommendation:** Always review and test the output of queries where `CROSS APPLY` has been converted to `LEFT OUTER JOIN` to ensure correctness.

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0083

### Error Message

**ROLLBACK TRANSACTION requires the appropriate setup to work as intended.**

### Severity

**Low**

### Description

This EWI is generated when a `ROLLBACK TRANSACTION` statement is encountered, indicating that SnowConvert has successfully transformed the statement into a Snowflake-compatible format. However, the transformation requires manual verification because Snowflake’s transaction rollback behavior differs significantly from SQL Server’s `ROLLBACK TRANSACTION` functionality.

### Example Code

#### Input (SQL Server):

Copy code

```
BEGIN TRANSACTION MyTransaction;

    -- Some operations
    INSERT INTO Employees (Name, Department) VALUES ('Alice', 'Engineering');

    IF @@ERROR <> 0
    BEGIN
        ROLLBACK TRANSACTION MyTransaction;  -- Named transaction rollback
    END
    ELSE
    BEGIN
        COMMIT TRANSACTION MyTransaction;
    END
```

#### Output (Snowflake Scripting):

Copy code

```
BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BeginTransaction' NODE ***/!!!
    BEGIN TRANSACTION MyTransaction;

        -- Some operations
    --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "Employees" **
        INSERT INTO Employees (Name, Department) VALUES ('Alice', 'Engineering');
    IF (:ERROR <> 0) THEN
        BEGIN
            !!!RESOLVE EWI!!! /*** SSC-EWI-TS0083 - ROLLBACK TRANSACTION REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED. ***/!!!
            ROLLBACK TRANSACTION MyTransaction;  -- Named transaction rollback

        END;
    ELSE
        BEGIN
            COMMIT;
        END;
    END IF;
END;
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0085

INSERT WITH EXECUTE statement requires manual review.

### Severity

Medium

#### Description

This issue is generated when an `INSERT ... EXECUTE` statement is encountered that cannot be automatically transformed. In SQL Server, `INSERT ... EXEC` inserts the result set of a stored procedure or dynamic SQL into a table. Snowflake does not support this syntax directly. When the statement appears at the top level (outside a stored procedure), the standard transformation pattern cannot be applied and the statement is flagged for manual review.

#### Code Example

##### Input Code:

Copy code

```
INSERT INTO SalesReport
EXEC GenerateQuarterlySales @Quarter = 1;
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0085 - INSERT WITH EXECUTE NODE NEEDS TO BE CHECKED. ***/!!!
INSERT INTO SalesReport EXEC GenerateQuarterlySales @Quarter = 1;
```

#### Best Practices

- Rewrite the logic using Snowflake Scripting: call the procedure separately, capture its result with `RESULT_SCAN(LAST_QUERY_ID())`, and then `INSERT INTO ... SELECT` from the result set.
- If the procedure returns a fixed schema, consider using a temporary table or `TABLE()` function to capture the output.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0086

OPENQUERY is not supported in Snowflake.

### Severity

High

#### Description

This issue is generated when an `OPENQUERY` function is encountered. In SQL Server, `OPENQUERY` executes a pass-through query on a linked server and returns the result as a table. Snowflake does not have an equivalent linked server or `OPENQUERY` mechanism. The statement is preserved as-is with an EWI marker for manual migration.

#### Code Example

##### Input Code:

Copy code

```
SELECT *
FROM OPENQUERY(OracleFinance, 'SELECT account_id, balance FROM accounts WHERE status = ''ACTIVE''');
```

##### Generated Code:

Copy code

```
SELECT
    *
FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0086 - OPENQUERY NODE NEEDS TO BE CHECKED. ***/!!! OPENQUERY (OracleFinance, 'SELECT account_id, balance FROM accounts WHERE status = ''ACTIVE''');
```

#### Best Practices

- Replace `OPENQUERY` with Snowflake external tables, external stages, or data sharing to access data from external sources.
- If the linked server points to another database, consider migrating that data into Snowflake or using Snowflake’s connector ecosystem (e.g., Snowflake Connector for Oracle).
- For real-time access patterns, evaluate Snowflake External Network Access or External Functions.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0087

GOTO is not supported in Snowflake.

### Severity

High

#### Description

This issue is generated when a `GOTO` statement is encountered that cannot be automatically transformed.

When GOTO/Label patterns appear inside a stored procedure with only forward jumps to top-level labels, they are automatically transformed into nested procedure definitions with `CALL`/`RETURN` semantics — no EWI is emitted in those cases. See the [LABEL and GOTO translation reference](../../translation-references/transact/transact-create-procedure-snow-script#label-and-goto) for details on the transformation.

This EWI is only emitted when the `GOTO` **cannot** be transformed. This happens with backward GOTOs (where the target label appears before the `GOTO` in the source, which would require recursive calls), or when the `GOTO` appears inside anonymous blocks or UDFs (which do not support nested procedure definitions in Snowflake).

#### Code Example

The following example shows a backward GOTO used for retry logic. Because `RetryConnection` appears before the `GOTO` that jumps to it, the transformation cannot be applied and the EWI is emitted:

##### Input Code:

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

##### Generated Code:

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

#### Best Practices

- For backward GOTO patterns like retry logic, refactor the control flow to use `WHILE` or `LOOP` constructs instead.
- For GOTO in anonymous blocks or UDFs, restructure the code into separate procedures or use `IF/ELSE` control flow.
- Forward GOTO patterns inside stored procedures are automatically transformed — no manual action is required for those cases.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

- [SSC-EWI-TS0045](sqlServerEWI#ssc-ewi-ts0045): Labeled statement is not supported in Snowflake Scripting.
- [SSC-EWI-TS0103](sqlServerEWI#ssc-ewi-ts0103): GOTO targeting a label inside a nested block is not supported in Snowflake.

## SSC-EWI-TS0088

Note

This EWI is deprecated. Sequence option removal is now reported under the general [SSC-EWI-0120](generalEWI#ssc-ewi-0120).

Unsupported sequence options were removed during conversion.

### Severity

Low

#### Description

This issue is generated when a `CREATE SEQUENCE` statement with options that are not supported in Snowflake, such as `MINVALUE`, `MAXVALUE`, or `CYCLE`, is encountered. These options are removed during conversion because Snowflake sequences only support `START WITH` and `INCREMENT BY`. The EWI message lists the specific options that were removed.

#### Code Example

##### Input Code:

Copy code

```
CREATE SEQUENCE InvoiceNumberSeq
START WITH 1000
INCREMENT BY 5
MINVALUE 100
MAXVALUE 50000
CYCLE;
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0088 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE, CYCLE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE InvoiceNumberSeq
  START WITH 1000
  INCREMENT BY 5
;
```

#### Best Practices

- If your application relies on `CYCLE` behavior, implement a wrapper UDF that resets the sequence value when it exceeds a threshold.
- If `MINVALUE` or `MAXVALUE` bounds are critical, add application-level validation or a Snowflake task to monitor sequence values.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0089

SET statement is not supported in Snowflake.

### Severity

Low

#### Description

This issue is generated when a `SET` statement that changes a session option not supported in Snowflake and whose non-default value cannot be replicated is encountered. For example, `SET CONCAT_NULL_YIELDS_NULL OFF` changes SQL Server’s NULL concatenation behavior, but Snowflake always treats `NULL || value` as `NULL` (equivalent to `CONCAT_NULL_YIELDS_NULL ON`). Similarly, `SET NUMERIC_ROUNDABORT ON` raises errors on precision loss, which Snowflake does not support. The original statement is preserved with an EWI marker.

#### Code Example

##### Input Code:

Copy code

```
SET CONCAT_NULL_YIELDS_NULL OFF;
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0089 - SET CONCAT_NULL_YIELDS_NULL OFF IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
SET CONCAT_NULL_YIELDS_NULL OFF;
```

#### Best Practices

- Review the downstream code that depends on this `SET` option. For `CONCAT_NULL_YIELDS_NULL OFF`, replace `NULL` concatenation patterns with explicit `NVL()` or `COALESCE()` calls to handle NULL values.
- For `NUMERIC_ROUNDABORT ON`, add explicit rounding or precision checks in the application logic.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

- [SSC-FDM-TS0037](../functional-difference/sqlServerFDM#ssc-fdm-ts0037): SET statement with equivalent default behavior in Snowflake (e.g., `SET CONCAT_NULL_YIELDS_NULL ON`).

## SSC-EWI-TS0090

Agent Job step uses an unsupported subsystem and requires manual migration.

### Severity

Medium

#### Description

This issue is generated when a SQL Server Agent Job step that uses a subsystem other than `TSQL` or `SSIS` (e.g., `CmdExec`, `PowerShell`, `ANALYSISCOMMAND`) is encountered. These subsystems execute operating system commands or external tools that have no direct equivalent in Snowflake. The original `sp_add_jobstep` call is preserved with an EWI marker, and the step is not included in the generated Snowflake Task orchestration.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_add_jobstep
    @job_name = N'NightlyArchive',
    @step_name = N'ArchiveOldRecords',
    @step_id = 1,
    @subsystem = N'CmdExec',
    @command = N'powershell.exe -File "C:\Scripts\archive_records.ps1"';
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0090 - AGENT JOB STEP 'ArchiveOldRecords' USES UNSUPPORTED SUBSYSTEM 'CmdExec'. MANUAL MIGRATION REQUIRED. ***/!!!
EXEC msdb.dbo.sp_add_jobstep @job_name = N'NightlyArchive', @step_name = N'ArchiveOldRecords', @step_id = 1, @subsystem = N'CmdExec', @command = N'powershell.exe -File "C:\Scripts\archive_records.ps1"';
```

#### Best Practices

- For `CmdExec` or `PowerShell` steps, evaluate whether the logic can be rewritten as a Snowflake stored procedure, external function, or Snowflake task with a SQL body.
- For SSIS steps, use the built-in ETL-to-dbt migration, which automatically generates orchestrator stored procedures.
- Consider using Snowflake External Functions or Snowpark for operations that require external compute.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0091

Agent Job notification procedure requires manual setup of a Snowflake notification integration.

### Severity

Medium

#### Description

This issue is generated when a SQL Server Agent notification procedure such as `sp_send_dbmail`, `sp_notify_operator`, or similar email/alert procedures within an Agent Job context is encountered. These procedures rely on SQL Server’s Database Mail or Operator subsystem, which has no direct equivalent in Snowflake. A Snowflake notification integration must be manually configured to replicate this functionality.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_send_dbmail
    @profile_name = N'DBA_Alerts',
    @recipients = N'admin@example.com',
    @subject = N'ETL job completed';
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0091 - AGENT JOB NOTIFICATION PROCEDURE 'sp_send_dbmail' REQUIRES MANUAL SETUP OF A SNOWFLAKE NOTIFICATION INTEGRATION. ***/!!!
EXEC msdb.dbo.sp_send_dbmail @profile_name = N'DBA_Alerts', @recipients = N'admin@example.com', @subject = N'ETL job completed';
```

#### Best Practices

- Set up a [Snowflake Notification Integration](https://docs.snowflake.com/en/sql-reference/sql/create-notification-integration) with an email provider or cloud messaging service (AWS SNS, Azure Event Grid, GCP Pub/Sub).
- Use `SYSTEM$SEND_EMAIL()` in Snowflake to send email notifications from stored procedures and tasks.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0092

Agent Job procedure references a dynamic job name that cannot be resolved statically.

### Severity

Medium

#### Description

This issue is generated when an Agent Job management procedure (`sp_start_job`, `sp_stop_job`, `sp_delete_job`, `sp_update_job`) is encountered where the `@job_name` parameter is a variable rather than a string literal. Because the job name cannot be resolved at conversion time, the corresponding Snowflake Task cannot be determined. The original statement is preserved with an EWI marker for manual resolution.

#### Code Example

##### Input Code:

Copy code

```
DECLARE @jobName NVARCHAR(128);
SET @jobName = N'ETL_Daily_Load';
EXEC msdb.dbo.sp_start_job @job_name = @jobName;
```

##### Generated Code:

Copy code

```
DECLARE
  JOBNAME NVARCHAR(128);
BEGIN
  JOBNAME := 'ETL_Daily_Load';
  !!!RESOLVE EWI!!! /*** SSC-EWI-TS0092 - AGENT JOB PROCEDURE 'sp_start_job' REFERENCES A DYNAMIC JOB NAME THAT CANNOT BE RESOLVED STATICALLY. ***/!!!
  EXEC msdb.dbo.sp_start_job @job_name = @jobName;
END;
```

#### Best Practices

- If the job name is known at design time, replace the variable with a string literal so it can be resolved to the corresponding Snowflake Task (e.g., `EXECUTE TASK TASK_ETL_DAILY_LOAD`).
- If the job name is truly dynamic, use `EXECUTE IMMEDIATE` to build the `EXECUTE TASK` or `ALTER TASK` statement dynamically in Snowflake Scripting.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0093

Agent Job procedure is not supported.

### Severity

Low

#### Description

This issue is generated when a SQL Server Agent Job system procedure that does not have a supported translation to Snowflake is encountered. This includes procedures like `sp_update_jobstep`, `sp_add_jobserver`, and `sp_update_job` (when used without the `@enabled` parameter). These procedures manage Agent Job metadata that has no equivalent in Snowflake’s Task framework. The original statement is preserved with an EWI marker.

#### Code Example

##### Input Code:

Copy code

```
EXEC msdb.dbo.sp_update_jobstep
    @job_name = N'ETL_Nightly_Load',
    @step_id = 1,
    @step_name = N'UpdatedStepName';
```

##### Generated Code:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0093 - AGENT JOB PROCEDURE 'sp_update_jobstep' IS NOT SUPPORTED. ***/!!!
EXEC msdb.dbo.sp_update_jobstep @job_name = N'ETL_Nightly_Load', @step_id = 1, @step_name = N'UpdatedStepName';
```

#### Best Practices

- Review whether the procedure’s functionality is still needed in the Snowflake environment. Many Agent Job metadata operations (renaming steps, assigning servers) are not applicable in Snowflake’s Task model.
- If the procedure modifies job scheduling or enablement, use `ALTER TASK` in Snowflake instead.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0094

### Error Message

**WAITFOR DELAY variable may contain a time string incompatible with SYSTEM$WAIT.**

### Severity

**Medium**

### Description

This EWI is generated when a `WAITFOR DELAY` statement uses a variable or parameter expression instead of a literal time value. The statement is transformed to `CALL SYSTEM$WAIT()`, which expects a numeric value representing seconds (or milliseconds). However, the variable may hold a time string in `'HH:MM:SS'` format, which is incompatible with `SYSTEM$WAIT`.

For more information about `SYSTEM$WAIT`, see the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions/system_wait).

#### Code Example

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

#### Best Practices

- Ensure the variable passed to `SYSTEM$WAIT` contains a numeric value in seconds, not a time string in `'HH:MM:SS'` format.
- If the variable holds a time string, convert it to seconds before passing it to `SYSTEM$WAIT`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0095

SCOPE\_IDENTITY() called without a preceding INSERT to an identity table in the same scope.

### Severity

**High**

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

The target table for SCOPE\_IDENTITY() could not be determined. No preceding INSERT to an identity table found in the same scope.

This EWI is generated when `SCOPE_IDENTITY()` is called without a preceding `INSERT` statement to a table with an `IDENTITY` column in the same procedural scope. In SQL Server, `SCOPE_IDENTITY()` returns the last identity value inserted in the current scope, but without a detectable `INSERT`, the appropriate time-travel query cannot be generated.

The function call is kept as-is with this EWI, requiring manual review to determine the correct implementation.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
 CREATE PROCEDURE GetLastId
AS
BEGIN
    DECLARE @LastID INT = SCOPE_IDENTITY();
    SELECT @LastID;
END;
```

##### Generated Code (Snowflake):

Copy code

```
 CREATE OR REPLACE PROCEDURE GetLastId ()
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    LASTID INT := SCOPE_IDENTITY() !!!RESOLVE EWI!!! /*** SSC-EWI-TS0095 - SNOWCONVERT AI WAS UNABLE TO DETERMINE THE TARGET TABLE FOR SCOPE_IDENTITY(). NO PRECEDING INSERT TO AN IDENTITY TABLE FOUND IN THE SAME SCOPE. ***/!!!;
    ProcedureResultSet RESULTSET;
  BEGIN
    ProcedureResultSet := (SELECT
      :LASTID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

#### Best Practices

- Review the stored procedure logic to identify where the INSERT statement occurs
- If the INSERT is in a different scope (e.g., nested block), refactor the code to make the INSERT detectable
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0096

SCOPE\_IDENTITY() references a table that cannot be resolved in the symbol table.

### Severity

**High**

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

The target table for SCOPE\_IDENTITY() could not be resolved. Missing table definition.

This EWI is generated when `SCOPE_IDENTITY()` follows an INSERT statement, but the target table cannot be resolved in the symbol table. This may occur when:

- The table is defined in an external file not included in the conversion
- The table name uses dynamic SQL or is otherwise unresolvable
- The table definition is missing or incomplete

Without a resolvable table reference, it cannot be determined which identity column to query in the generated time-travel query.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
 CREATE PROCEDURE InsertOrder @CustomerID INT
AS
BEGIN
    DECLARE @OrderID INT;
    INSERT INTO UnknownTable (CustomerID) VALUES (@CustomerID);
    SET @OrderID = SCOPE_IDENTITY();
    SELECT @OrderID;
END;
```

##### Generated Code (Snowflake):

Copy code

```
 CREATE OR REPLACE PROCEDURE InsertOrder (CUSTOMERID INT)
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ORDERID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    INSERT INTO UnknownTable (CustomerID) VALUES (:CUSTOMERID);
    ORDERID := SCOPE_IDENTITY() !!!RESOLVE EWI!!! /*** SSC-EWI-TS0096 - SNOWCONVERT AI WAS UNABLE TO RESOLVE THE TARGET TABLE FOR SCOPE_IDENTITY(). MISSING TABLE DEFINITION. ***/!!!;
    ProcedureResultSet := (SELECT
      :ORDERID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

#### Best Practices

- Ensure all table definitions are included in the conversion input
- Verify that the table name in the INSERT statement matches the table definition
- If the table is external, provide the schema definition or manually implement the identity retrieval logic
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0097

SCOPE\_IDENTITY() references a table without an identifiable identity column.

### Severity

**High**

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

The identity column for SCOPE\_IDENTITY() could not be identified. Missing column definition.

This EWI is generated when `SCOPE_IDENTITY()` follows an INSERT statement to a table that exists in the symbol table but does not have an IDENTITY column defined. In SQL Server, `SCOPE_IDENTITY()` only returns values for tables with identity columns. Without an identifiable identity column, the appropriate `MAX(identity_column)` query for the time-travel transformation cannot be generated.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
 CREATE TABLE Orders (OrderID INT, CustomerID INT);
GO

CREATE PROCEDURE InsertOrder @CustomerID INT
AS
BEGIN
    DECLARE @OrderID INT;
    INSERT INTO Orders (CustomerID) VALUES (@CustomerID);
    SET @OrderID = SCOPE_IDENTITY();
    SELECT @OrderID;
END;
```

##### Generated Code (Snowflake):

Copy code

```
 CREATE OR REPLACE TABLE Orders (
  OrderID INT,
  CustomerID INT
)
;

CREATE OR REPLACE PROCEDURE InsertOrder (CUSTOMERID INT)
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ORDERID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    INSERT INTO Orders (CustomerID) VALUES (:CUSTOMERID);
    ORDERID := SCOPE_IDENTITY() !!!RESOLVE EWI!!! /*** SSC-EWI-TS0097 - SNOWCONVERT AI WAS UNABLE TO IDENTIFY THE IDENTITY COLUMN FOR SCOPE_IDENTITY(). MISSING COLUMN DEFINITION. ***/!!!;
    ProcedureResultSet := (SELECT
      :ORDERID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

#### Best Practices

- Verify that the table definition includes an IDENTITY column specification
- If the table should have an identity column, add the IDENTITY constraint to the CREATE TABLE statement before conversion
- If the table should not use SCOPE\_IDENTITY(), refactor the code to use a different method for retrieving the inserted ID
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0098

CONVERT with a non-literal style cannot be mapped to a Snowflake format string.

### Severity

**Medium**

### Description

This EWI is generated when the third argument of `CONVERT` is a variable or expression instead of a literal style code. Literal style values can be mapped to Snowflake format strings for `TO_VARCHAR`, `TO_DATE`, and `TO_TIMESTAMP`, but when the style is dynamic the correct format cannot be determined at conversion time. In those cases it falls back to `CAST`.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
SELECT CONVERT(DATE, @InputDate, @Style);
```

##### Generated Code (Snowflake SQL):

Copy code

```
SELECT
  !!!RESOLVE EWI!!! /*** SSC-EWI-TS0098 - CONVERT WITH A VARIABLE OR EXPRESSION AS THE STYLE ARGUMENT CANNOT BE AUTOMATICALLY MAPPED TO A SNOWFLAKE FORMAT STRING. REPLACE WITH THE APPROPRIATE TO_VARCHAR, TO_DATE, OR TO_TIMESTAMP CALL WITH THE KNOWN FORMAT STRING. ***/!!!
  CAST(@InputDate AS DATE);
```

#### Best Practices

- Replace the dynamic style argument with a known literal format whenever possible.
- If the style varies at runtime, rewrite the expression manually using the correct `TO_VARCHAR`, `TO_DATE`, `TO_TIMESTAMP`, or conditional logic in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0099

The OBJECT\_SCHEMA\_NAME function is not supported in Snowflake.

Note

This EWI is deprecated. `OBJECT_SCHEMA_NAME` is now converted to a helper UDF `OBJECT_SCHEMA_NAME_UDF`. When the two-argument form is used, refer to [SSC-FDM-TS0060](../functional-difference/sqlServerFDM#ssc-fdm-ts0060) for information about the removed `database_id` parameter.

### Severity

**Low**

Note

Some parts of the output code are omitted for clarity reasons.

#### Description

This EWI was generated when the SQL Server `OBJECT_SCHEMA_NAME(object_id [, database_id])` function was encountered, which returns the schema name for a schema-scoped object given its numeric object ID. Snowflake does not use numeric object IDs for metadata lookups.

This EWI has been replaced by an automatic conversion to a helper UDF (`OBJECT_SCHEMA_NAME_UDF`) that queries `INFORMATION_SCHEMA` to resolve schema names.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
SELECT OBJECT_SCHEMA_NAME(1);
```

##### Generated Code (Snowflake SQL) — Previous behavior:

Copy code

```
SELECT
OBJECT_SCHEMA_NAME(1) !!!RESOLVE EWI!!! /*** SSC-EWI-TS0099 - THE OBJECT_SCHEMA_NAME FUNCTION IS NOT SUPPORTED IN SNOWFLAKE ***/!!!;
```

##### Generated Code (Snowflake SQL) — Current behavior:

Copy code

```
SELECT
PUBLIC.OBJECT_SCHEMA_NAME_UDF(1);
```

#### Best Practices

- This EWI is no longer emitted. `OBJECT_SCHEMA_NAME` calls are now automatically converted to `OBJECT_SCHEMA_NAME_UDF`.
- Review the generated UDF to ensure it resolves the correct schema for your objects.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0100

Scope Resolution Method Pending Translation

### Severity

Medium

#### Description

This EWI is generated when SnowConvert AI cannot translate a SQL Server static method invoked with the scope-resolution operator (`::`). The original expression is preserved for manual conversion.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT geography::Point(47.653, -122.358, 4326);
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  geography :: Point(47.653, -122.358, 4326) !!!RESOLVE EWI!!! /*** SSC-EWI-TS0100 - PENDING SNOWCONVERT AI TRANSLATION FOR THE 'Point' METHOD OF THE 'geography' DATATYPE ***/!!!;
```

#### Best Practices

- Replace the static method with the Snowflake geospatial function that provides the required behavior.
- Validate coordinate order and spatial reference handling after rewriting the expression.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0101

OBJECTPROPERTY requires OBJECT\_ID as first argument for translation

### Severity

Medium

#### Description

This EWI is generated when SnowConvert AI encounters `OBJECTPROPERTY` without an `OBJECT_ID` call as its first argument. Only that supported shape can be translated to the Snowflake helper UDF.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT OBJECTPROPERTY(123, 'IsView');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
OBJECTPROPERTY(123, 'IsView') !!!RESOLVE EWI!!! /*** SSC-EWI-TS0101 - SNOWCONVERT AI WAS UNABLE TO TRANSLATE THE OBJECTPROPERTY FUNCTION, ONLY USAGES THAT SPECIFY THE OBJECT_ID FUNCTION AS FIRST PARAMETER ARE SUPPORTED ***/!!!;
```

#### Best Practices

- Rewrite the lookup against Snowflake `INFORMATION_SCHEMA` views using an object name instead of a SQL Server numeric object identifier.
- If possible before conversion, express the first argument as `OBJECT_ID(N'<object-name>')`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0102

Unsupported OBJECTPROPERTY property in Snowflake

### Severity

Low

#### Description

This EWI is generated when an `OBJECTPROPERTY` property has no equivalent in Snowflake. SnowConvert AI preserves the call so the metadata-dependent logic can be reviewed manually.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT OBJECTPROPERTY(OBJECT_ID(N'dbo.Orders'), 'IsIndexed');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
OBJECTPROPERTY(PUBLIC.OBJECT_ID_UDF('DBO.ORDERS'), 'IsIndexed') !!!RESOLVE EWI!!! /*** SSC-EWI-TS0102 - THE 'IsIndexed' OBJECT PROPERTY HAS NO EQUIVALENT IN SNOWFLAKE ***/!!!;
```

#### Best Practices

- Replace the property check with a query against the Snowflake metadata view appropriate to the migrated object type.
- Review any branching logic that depends on SQL Server-specific object properties.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0103

GOTO targeting a label inside a nested block is not supported in Snowflake.

### Severity

High

#### Description

This EWI is generated when a `GOTO` targets a label that is declared inside a nested control flow block (such as `IF`, `WHILE`, `BEGIN...END`, or `TRY...CATCH`). The GOTO/Label decomposition can only transform labels that are declared at the top level of a procedure body — labels buried inside nested blocks cannot be extracted into standalone nested procedures. When this happens, the `GOTO` is preserved with this EWI marker, while top-level labels in the same procedure are still transformed normally.

#### Code Example

In this example, `Done` is a top-level label and is transformed into a nested procedure. However, `HandlePartialFailure` is declared inside a `BEGIN...END` block, so the `GOTO` targeting it cannot be transformed:

##### Input Code:

##### SQL Server

Copy code

```
CREATE PROCEDURE dbo.ImportCustomerData
AS
BEGIN
    DECLARE @BatchId INT = 0, @IsValid INT = 0, @RowCount INT = 0
    IF @BatchId = 1 GOTO Done
    BEGIN
        IF @IsValid = 1 GOTO HandlePartialFailure
        SET @RowCount = 1
    HandlePartialFailure:
        SET @RowCount = 2
    END
Done:
    RETURN 0
END
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE dbo.ImportCustomerData ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SC_EXIT_CODE VARCHAR;
    BATCHID INT := 0;
    ISVALID INT := 0;
    ROWCOUNT INT := 0;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        IF (:BATCHID = 1) THEN
          BEGIN
            CALL Done();
            RETURN 'PROCESS FINISHED';
          END;
        END IF;
        BEGIN
          IF (:ISVALID = 1) THEN
            !!!RESOLVE EWI!!! /*** SSC-EWI-TS0103 - GOTO TARGETING A LABEL INSIDE A NESTED BLOCK IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
            GOTO HandlePartialFailure
          END IF;
          ROWCOUNT := 1;
          HandlePartialFailure:
          ROWCOUNT := 2;
        END;
        CALL Done();
      END;
    Done PROCEDURE ()
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

#### Best Practices

- Move the nested label to the top level of the procedure body so it can be transformed automatically.
- Alternatively, replace the GOTO with structured `IF/ELSE` or `LOOP` control flow to avoid the jump entirely.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Related EWIs

- [SSC-EWI-TS0045](sqlServerEWI#ssc-ewi-ts0045): Labeled statement is not supported in Snowflake Scripting.
- [SSC-EWI-TS0087](sqlServerEWI#ssc-ewi-ts0087): GOTO is not supported in Snowflake.

## SSC-EWI-TS0104

System table query pattern could not be automatically converted.

### Severity

**Medium**

### Description

This EWI is generated when a query pattern inside a system table query (such as `sysconstraints`) is encountered that cannot be translated automatically. Common triggers include:

- `OBJECT_NAME()` called with an argument that doesn’t map to a known column (for example, `OBJECT_NAME(status)` instead of `OBJECT_NAME(constid)` or `OBJECT_NAME(id)`)
- `OBJECT_NAME()` compared against a non-literal value (a column reference, variable, or expression instead of a string literal)

In these cases the original expression is preserved and the EWI is emitted so you can review and rewrite the query manually.

#### Code Example

##### Input Code (SQL Server):

Copy code

```
SELECT 1 FROM sysconstraints WHERE OBJECT_NAME(status) = 'X';
```

##### Generated Code (Snowflake SQL):

Copy code

```
SELECT
    1
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0104 - 'OBJECT_NAME(status) in sysconstraints query' COULD NOT BE AUTOMATICALLY CONVERTED IN SYSTEM TABLE QUERY. MANUAL REVIEW REQUIRED ***/!!!
    OBJECT_NAME(status) = 'X';
```

##### Input Code (SQL Server) - Non-literal comparison:

Copy code

```
SELECT 1 FROM sysconstraints WHERE OBJECT_NAME(constid) = col1;
```

##### Generated Code (Snowflake SQL):

Copy code

```
SELECT
    1
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0104 - 'Non-literal comparison with OBJECT_NAME in sysconstraints query' COULD NOT BE AUTOMATICALLY CONVERTED IN SYSTEM TABLE QUERY. MANUAL REVIEW REQUIRED ***/!!!
    OBJECT_NAME(constid) = col1;
```

#### Best Practices

- Replace `OBJECT_NAME(constid)` with `CONSTRAINT_NAME` and `OBJECT_NAME(id)` with `TABLE_NAME` when querying `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`.
- Ensure that the comparison value is a string literal. If you need to compare against a variable or column, rewrite the query to use the equivalent `INFORMATION_SCHEMA` column directly.
- Review the [sysconstraints translation reference](../../translation-references/transact/transact-system-tables#sysconstraints) for supported transformation patterns.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0105

sp\_add\_category for class ‘ALERT’ is not supported. Only JOB class categories are translated to Snowflake TAGs.

### Severity

Low

#### Description

This EWI is generated when `sp_add_category` uses a category class other than `JOB`. SnowConvert AI translates `JOB` categories to Snowflake tags, but preserves unsupported category classes.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
EXEC msdb.dbo.sp_add_category @class=N'ALERT', @type=N'NONE', @name=N'DemoAlert';
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0105 - SP_ADD_CATEGORY FOR CLASS 'ALERT' IS NOT SUPPORTED. ONLY JOB CLASS CATEGORIES ARE TRANSLATED TO SNOWFLAKE TAGS. ***/!!!
EXEC msdb.dbo.sp_add_category @class = N'ALERT', @type = N'NONE', @name = N'DemoAlert';
```

#### Best Practices

- Review whether the category is still needed after migration and model the requirement with Snowflake tags or monitoring integrations.
- Remove the preserved procedure call after implementing the Snowflake-native replacement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0106

CREATING TRANSACTION SAVEPOINTS IS NOT SUPPORTED IN SNOWFLAKE

### Severity

Low

#### Description

This EWI is generated for `SAVE TRANSACTION` and `SAVE TRAN` statements because Snowflake does not support SQL Server transaction savepoints. SnowConvert AI preserves the statement for manual redesign.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SAVE TRANSACTION ProcedureSave;
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0106 - CREATING TRANSACTION SAVEPOINTS IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
SAVE TRANSACTION ProcedureSave;
```

#### Best Practices

- Redesign the transaction so the entire unit of work can commit or roll back atomically.
- Split recoverable stages into idempotent procedures or persist intermediate state when partial recovery is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0107

CREATE TYPE AS TABLE cannot be converted to Snowflake

### Severity

Medium

#### Description

SQL Server **table types** created with `CREATE TYPE ... AS TABLE (...)` are not mapped to a single Snowflake `CREATE TYPE` equivalent. SnowConvert flags this pattern so you can redesign using tables, views, or other Snowflake constructs.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE TYPE dbo.OrderLines AS TABLE (
    order_id INT,
    line_no  INT,
    qty      DECIMAL(10, 2)
);
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0107 - CREATE TYPE AS TABLE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE TYPE dbo.OrderLines AS TABLE (
    order_id INT,
    line_no INT,
    qty DECIMAL(10, 2)
);
```

#### Best Practices

- Model reusable row shapes as permanent or transient tables, or use `OBJECT`/`VARIANT` patterns where appropriate.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0108

Delta-backed external tables may require Iceberg with Delta manifest for read correctness

### Severity

Medium

#### Description

This EWI is generated when SnowConvert AI converts an external table backed by a Delta file format. A regular Snowflake external table may not reproduce Delta transaction-log semantics, so an Iceberg table with a Delta manifest may be required.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE EXTERNAL TABLE silver.LineOfService (pk NVARCHAR(4000))
WITH (
  DATA_SOURCE = DataLakeSource,
  LOCATION = N'Silver/LineOfService',
  FILE_FORMAT = DeltaFileFormat
);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TS0066 - AUTO_REFRESH WAS SET TO FALSE. SNOWFLAKE DEFAULTS EXTERNAL TABLES TO AUTO_REFRESH = TRUE; ENABLE IT WITH A NOTIFICATION INTEGRATION IF AUTOMATIC METADATA REFRESH IS REQUIRED. **
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0108 - DELTA-BACKED EXTERNAL TABLES MAY REQUIRE ICEBERG WITH DELTA MANIFEST FOR READ CORRECTNESS. CONSIDER REGISTERING AS AN ICEBERG TABLE INSTEAD. ***/!!!
CREATE EXTERNAL TABLE silver.LineOfService (pk NVARCHAR(4000))
LOCATION = @DataLakeSource/Silver/LineOfService
FILE_FORMAT = DeltaFileFormat
AUTO_REFRESH = false;
```

#### Best Practices

- Confirm whether readers require Delta transaction-log correctness rather than file-level access only.
- Register the data as an Iceberg table using a Delta manifest when transactional consistency is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0109

SET ROWCOUNT is not supported in Snowflake. Use TOP or LIMIT on individual statements instead.

### Severity

Low

#### Description

The T-SQL `SET ROWCOUNT n` statement limits all subsequent DML and SELECT operations to return or modify at most `n` rows per statement, until it is reset with `SET ROWCOUNT 0`. Snowflake has no session-level row-count limiter; the `TOP` clause or `LIMIT` clause must be applied to each individual statement.

`SET ROWCOUNT` is flagged with this EWI and the original statement is preserved so you can locate each occurrence and apply the appropriate per-statement limit manually.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SET ROWCOUNT 100;
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0109 - SET ROWCOUNT IS NOT SUPPORTED IN SNOWFLAKE. USE TOP OR LIMIT ON INDIVIDUAL STATEMENTS INSTEAD. ***/!!!
SET ROWCOUNT 100;
```

#### Best Practices

- Replace `SET ROWCOUNT n` with `SELECT TOP n ...` or `SELECT ... LIMIT n` on each affected query.
- For `UPDATE` or `DELETE` statements that rely on `SET ROWCOUNT`, rewrite them as `UPDATE ... WHERE <pk> IN (SELECT TOP n <pk> FROM ...)` or use a CTE to scope the affected rows.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0110

External file format type is not supported as a file format in Snowflake.

### Severity

Medium

#### Description

This EWI is generated when a Synapse external file format type, such as `DELTA` or `RCFILE`, cannot be represented by a Snowflake file format. SnowConvert AI emits a Parquet placeholder that must be reviewed.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE EXTERNAL FILE FORMAT DeltaFileFormat WITH (FORMAT_TYPE = DELTA);
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0110 - 'DELTA' FORMAT NOT SUPPORTED AS A FILE FORMAT IN SNOWFLAKE. USE AN ICEBERG TABLE WITH DELTA MANIFEST OR REGISTER A DELTA EXTERNAL TABLE INSTEAD. ***/!!!
CREATE FILE FORMAT IF NOT EXISTS DeltaFileFormat
TYPE = PARQUET
COMPRESSION = AUTO;
```

#### Best Practices

- Do not treat the generated Parquet definition as behaviorally equivalent without validating the source files.
- Use an Iceberg table with a Delta manifest or another Snowflake-native ingestion design for Delta data.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0111

Table-valued parameters are not supported in Snowflake.

### Severity

High

#### Description

This EWI is generated for a SQL Server table-valued routine parameter and each table-position reference to it. Snowflake routines do not support table-valued parameters, so the routine interface must be redesigned.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
CREATE FUNCTION dbo.GetTasks (@RoleMap AS dbo.UserRoles READONLY)
RETURNS TABLE
AS RETURN (SELECT RoleID FROM @RoleMap);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION dbo.GetTasks (ROLEMAP dbo.UserRoles !!!RESOLVE EWI!!! /*** SSC-EWI-TS0111 - TABLE-VALUED PARAMETER '@RoleMap' IS NOT SUPPORTED IN SNOWFLAKE. THE PARAMETER DECLARATION AND EVERY REFERENCE TO IT HAVE TO BE REDESIGNED MANUALLY. ***/!!!)
RETURNS TABLE
AS
$$
  BEGIN
    RETURN (SELECT RoleID FROM
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0111 - TABLE-VALUED PARAMETER '@RoleMap' IS NOT SUPPORTED IN SNOWFLAKE. THE PARAMETER DECLARATION AND EVERY REFERENCE TO IT HAVE TO BE REDESIGNED MANUALLY. ***/!!!
      ROLEMAP);
  END;
$$;
```

#### Best Practices

- Replace the table-valued parameter with a temporary or transient table whose name or key is passed to the routine.
- Consider passing structured data in `VARIANT` only when the expected volume and schema make that design appropriate.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0112

MERGE target CTE could not be rewritten to a base table.

### Severity

High

#### Description

This EWI is generated when a SQL Server `MERGE` targets a CTE that SnowConvert AI cannot safely rewrite to one base table. Snowflake does not support `MERGE INTO` a CTE.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
WITH TGT AS (
  SELECT t1.Id, t1.Val
  FROM dbo.T1 t1
  JOIN dbo.T2 t2 ON t1.Id = t2.Id
)
MERGE INTO TGT
USING (SELECT 2 AS Id, 20 AS Val) AS SRC
ON TGT.Id = SRC.Id
WHEN NOT MATCHED THEN INSERT (Id, Val) VALUES (SRC.Id, SRC.Val);
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0112 - MERGE TARGET CTE COULD NOT BE REWRITTEN TO A BASE TABLE. SNOWFLAKE DOES NOT SUPPORT MERGE INTO A CTE. ***/!!!
WITH TGT AS (
  SELECT t1.Id, t1.Val FROM dbo.T1 t1
  JOIN dbo.T2 t2 ON t1.Id = t2.Id
)
MERGE INTO TGT
USING (SELECT 2 AS Id, 20 AS Val) AS SRC
ON TGT.Id = SRC.Id
WHEN NOT MATCHED THEN INSERT (Id, Val) VALUES (SRC.Id, SRC.Val);
```

#### Best Practices

- Identify the base table that should receive the changes and target it directly.
- Move eligible CTE filters into the `MERGE` join condition while preserving source semantics.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0113

The database principal existence test cannot be resolved because Snowflake has no numeric principal identifier.

### Severity

Medium

#### Description

This EWI is generated when SnowConvert AI cannot resolve a `DATABASE_PRINCIPAL_ID` existence test at conversion time. Snowflake has no equivalent numeric database-principal identifier.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT CASE WHEN DATABASE_PRINCIPAL_ID(@PrincipalName) IS NULL THEN -1 ELSE 1 END AS flag;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CASE WHEN DATABASE_PRINCIPAL_ID(@PrincipalName) !!!RESOLVE EWI!!! /*** SSC-EWI-TS0113 - DATABASE_PRINCIPAL_ID IS NOT SUPPORTED IN SNOWFLAKE: THERE IS NO NUMERIC PRINCIPAL IDENTIFIER TO RETURN. REWRITE THE TEST AGAINST A PRINCIPAL NAME. ***/!!! IS NULL THEN -1 ELSE 1 END AS flag;
```

#### Best Practices

- Rewrite the existence test against a principal name in Snowflake account metadata.
- Verify whether the source principal is a user or role and query the corresponding account-level view.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0114

Changing the collation of an existing column is not supported.

### Severity

Medium

#### Description

This EWI is generated when SnowConvert AI encounters a `COLLATE` clause while converting an existing SQL Server column. Snowflake does not support changing an existing column’s collation, so the clause is commented out for manual review.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
ALTER TABLE table1_alter ALTER COLUMN col1 VARCHAR(50) COLLATE Latin1_General_CI_AS NOT NULL;
```

##### Output Code:

##### Snowflake

Copy code

```
ALTER TABLE IF EXISTS table1_alter ALTER COLUMN col1 VARCHAR(50)
-- !!!RESOLVE EWI!!! /*** SSC-EWI-TS0114 - CHANGING THE COLLATION OF AN EXISTING COLUMN TO Latin1_General_CI_AS IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
-- COLLATE Latin1_General_CI_AS
NOT NULL;
```

#### Best Practices

- Define the required collation when creating the Snowflake column instead of altering it later.
- Review comparison and sorting behavior before removing the commented clause.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-TS0115

The T-SQL session global has no Snowflake equivalent.

### Severity

High

#### Description

This EWI is generated when SnowConvert AI encounters a T-SQL session global while targeting Snowflake Scripting. Snowflake has no direct equivalent for session globals such as `@@SPID`, so dependent logic must use explicit state or be redesigned.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
SELECT @@SPID AS s;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT @@SPID !!!RESOLVE EWI!!! /*** SSC-EWI-TS0115 - T-SQL SESSION GLOBAL '@@SPID' HAS NO SNOWFLAKE EQUIVALENT. REPLACE IT WITH EXPLICIT STATE OR REDESIGN THE DEPENDENT LOGIC. ***/!!! AS s;
```

#### Best Practices

- Identify the state represented by the session global and pass it explicitly where possible.
- Redesign logic that depends on SQL Server connection or cursor state.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
