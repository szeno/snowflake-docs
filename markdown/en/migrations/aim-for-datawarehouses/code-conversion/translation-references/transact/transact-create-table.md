# SQL Server-Azure Synapse - CREATE TABLE

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

## Basic CREATE TABLE

### Source

Copy code

```
:force:
CREATE TABLE [MYSCHEMA].[MYTABLE]
(
    [COL1] INT IDENTITY (1,1) NOT NULL,
    [COL2] INT,
    [COL2 COL3 COL4] VARCHAR,
    [COL VARCHAR_SPANISH] [VARCHAR](20) COLLATE Modern_Spanish_CI_AI DEFAULT 'HOLA',
    [COL VARCHAR_LATIN] [VARCHAR](20) COLLATE Latin1_General_CI_AI DEFAULT 'HELLO' 
);
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE MYSCHEMA.MYTABLE
(
    COL1 INT IDENTITY(1,1) ORDER NOT NULL,
    COL2 INT,
    "COL2 COL3 COL4" VARCHAR,
    "COL VARCHAR_SPANISH" VARCHAR(20) COLLATE 'ES-CI-AI' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ DEFAULT 'HOLA',
    "COL VARCHAR_LATIN" VARCHAR(20) COLLATE 'EN-CI-AI' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ DEFAULT 'HELLO'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;
```

## TEMPORARY TABLES

In the source code, there can be some table names that start with the character #.

Copy code

```
:force:
CREATE TABLE #MyLocalTempTable (
        COL1 INT,
        COL2 INT
);
```

If that is the case, they are transformed into temporary tables in the output code.

  

Let’s see how the code from above would be migrated.

Copy code

```
:force:
CREATE OR REPLACE TEMPORARY TABLE T_MyLocalTempTable (
        COL1 INT,
        COL2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

As you can see, **TEMPORARY** was added to the definition of the table, and the character **#** was replaced with **T\_**.

Also, all references of the table will be transformed too, to match the new name given to the temporary table.

## NULL and NOT NULL Column Option

`NULL` and `NOT NULL` column options are supported in Snowflake.

### Source

Copy code

```
:force:
CREATE TABLE [SCHEMA1].[TABLE1](
	[COL1] [varchar](20) NOT NULL
) ON [PRIMARY]
GO

CREATE TABLE [SCHEMA1].[TABLE2](
	[COL1] [varchar](20) NULL
) ON [PRIMARY]
GO
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE SCHEMA1.TABLE1 (
	COL1 VARCHAR(20) NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

CREATE OR REPLACE TABLE SCHEMA1.TABLE2 (
	COL1 VARCHAR(20) NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## IDENTITY Column Option

For identity columns, a sequence is created and assigned to the column.

### Source

Copy code

```
:force:
CREATE TABLE acct3.UnidentifiedCash3 (
UnidentifiedCash_ID3 INT IDENTITY (666, 313) NOT NULL
);
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE acct3.UnidentifiedCash3 (
UnidentifiedCash_ID3 INT IDENTITY(666, 313) ORDER NOT NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;
```

## DEFAULT Column Option

The default Expr is supported in Snowflake, however, in Sql Server it can come together with a constraint Name. Since that part is not supported in Snowflake, it has been removed, and a warning has been added.

### Source

Copy code

```
:force:
CREATE TABLE [SCHEMA1].[TABLE1] (
    [COL1] VARCHAR (10) CONSTRAINT [constraintName] DEFAULT ('0') NOT NULL
);
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE SCHEMA1.TABLE1 (
COL1 VARCHAR(10) DEFAULT ('0') /*** SSC-FDM-0012 - CONSTRAINT NAME 'constraintName' IN DEFAULT EXPRESSION CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE ***/ NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## COLUMN Constraint

### Source

Copy code

```
:force:
CREATE TABLE [SalesLT].[Address](
	[AddressID] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[AddressLine1] [nvarchar](60) NOT NULL,
	[AddressLine2] [nvarchar](60) NULL,
	[City] [nvarchar](30) NOT NULL,
	[StateProvince] [dbo].[Name] NOT NULL,
	[CountryRegion] [dbo].[Name] NOT NULL,
	[PostalCode] [nvarchar](15) NOT NULL,
	[rowguid] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[ModifiedDate] [datetime] NOT NULL,
	CONSTRAINT [PK_Address_AddressID] PRIMARY KEY CLUSTERED 
	(
		[AddressID] ASC
	)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
	CONSTRAINT [AK_Address_rowguid] UNIQUE NONCLUSTERED 
	(
		[rowguid] ASC
	)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
```

### Expected

Copy code

```
:force:
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "[dbo].[Name]" **
CREATE OR REPLACE TABLE SalesLT.Address (
	AddressID INT IDENTITY(1,1) ORDER NOT NULL,
	AddressLine1 VARCHAR(60) NOT NULL,
	AddressLine2 VARCHAR(60) NULL,
	City VARCHAR(30) NOT NULL,
	StateProvince VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE DBO.NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!! NOT NULL,
	CountryRegion VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-TS0015 - DATA TYPE DBO.NAME IS NOT SUPPORTED IN SNOWFLAKE ***/!!! NOT NULL,
	PostalCode VARCHAR(15) NOT NULL,
	rowguid VARCHAR
 	               !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'ROWGUIDCOL COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
 	               ROWGUIDCOL  NOT NULL,
	ModifiedDate TIMESTAMP_NTZ(3) NOT NULL,
		CONSTRAINT PK_Address_AddressID PRIMARY KEY (AddressID),
		CONSTRAINT AK_Address_rowguid UNIQUE (rowguid)
	)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;
```

## CHECK Constraints

Snowflake supports CHECK constraints with deterministic, scalar expressions. SQL Server CHECK constraints are migrated to Snowflake, handling dialect-specific clauses and detecting unsupported expressions.

**Supported:**

- Basic CHECK constraints with scalar, deterministic expressions
- Column-level and table-level CHECK constraints
- Named and unnamed constraints

**Unsupported (flagged with SSC-EWI-0116):**

- User-defined functions (UDFs)
- Non-deterministic built-in functions (e.g., `NEWID()`, `RAND()`)
- Context-dependent functions (e.g., `GETDATE()`, `CURRENT_USER()`)
- Subqueries

**Removed automatically:**

- `NOT FOR REPLICATION` clause (SQL Server-specific)

### Basic CHECK Constraint

#### SQL Server

Copy code

```
:force:
CREATE TABLE Products (
  ProductID INT PRIMARY KEY,
  Price DECIMAL(10,2) CHECK (Price > 0),
  Quantity INT CHECK (Quantity >= 0 AND Quantity <= 1000)
);
```

#### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE Products (
  ProductID INT PRIMARY KEY,
  Price DECIMAL(10, 2) CHECK (Price > 0),
  Quantity INT CHECK (Quantity >= 0
  AND Quantity <= 1000)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### CHECK Constraint with NOT FOR REPLICATION (Removed)

The `NOT FOR REPLICATION` clause is specific to SQL Server replication and is automatically removed during conversion.

#### SQL Server

Copy code

```
:force:
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  Price DECIMAL(10,2) CHECK NOT FOR REPLICATION (Price > 0)
);
```

#### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE Orders (
  OrderID INT PRIMARY KEY,
  Price DECIMAL(10, 2) CHECK (Price > 0)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### CHECK Constraint with User-Defined Function (Unsupported)

When a CHECK constraint references a user-defined function, it is flagged with **SSC-EWI-0116** because Snowflake does not support UDFs in CHECK constraints.

#### SQL Server

Copy code

```
:force:
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  Price DECIMAL(10,2) CHECK (dbo.IsValidPrice(Price) = 1)
);
```

#### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE Orders (
  OrderID INT PRIMARY KEY,
  Price DECIMAL(10, 2)
                       !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH user-defined function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                       CHECK (dbo.IsValidPrice(Price) = 1)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### CHECK Constraint with Non-Deterministic Function (Unsupported)

Non-deterministic functions like `NEWID()` are flagged with **SSC-EWI-0116**.

#### SQL Server

Copy code

```
:force:
CREATE TABLE Sessions (
  SessionID INT PRIMARY KEY,
  Token NVARCHAR(100) CHECK (Token <> CAST(NEWID() AS NVARCHAR(100)))
);
```

#### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE Sessions (
  SessionID INT PRIMARY KEY,
  Token NVARCHAR(100)
                      !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH non-deterministic function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                      CHECK (Token <> CAST(NEWID() AS NVARCHAR(100)))
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### Related Issues

- [SSC-EWI-0116](../../issues-and-troubleshooting/conversion-issues/generalEWI#scenario-1-check-constraints-with-unsupported-expressions): CHECK constraint with unsupported expression
- [SSC-FDM-0044](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0044): CHECK constraint added inside stored procedure/UDF will not validate existing data

## COLLATE Column Option

For the Collate transformation, please check the following [link](./transact-general-statements#collate)

## ENCRYPTED WITH Column Option

The Encrypted With is not supported in Snowflake, so it is being removed, and a warning is added.

### Source

Copy code

```
:force:
CREATE TABLE [SCHEMA1].[TABLE1] (
    [COL1] NVARCHAR(60) ENCRYPTED WITH (COLUMN_ENCRYPTION_KEY = MyCEK, ENCRYPTION_TYPE = RANDOMIZED, ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256')
);
```

### Expected

Copy code

```
:force:
CREATE OR REPLACE TABLE SCHEMA1.TABLE1 (
    COL1 VARCHAR(60)
--                     --** SSC-FDM-TS0009 - ENCRYPTED WITH NOT SUPPORTED IN SNOWFLAKE **
--                     ENCRYPTED WITH (COLUMN_ENCRYPTION_KEY = MyCEK, ENCRYPTION_TYPE = RANDOMIZED, ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256')
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## NOT FOR REPLICATION

The NOT FOR REPLICATION option is not supported in Snowflake. It is used for the identity that is being migrated to a `SEQUENCE`.

Warning

Notice that `NOT FOR REPLICATION` is a statement that is not required in Snowflake because it is translated to an equivalent, so it is removed.

### Source

Copy code

```
:force:
CREATE TABLE [TABLE1] (
    [COL1] INT IDENTITY (1, 1) NOT FOR REPLICATION NOT NULL
) ON [PRIMARY];
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1 (
    COL1 INT IDENTITY(1, 1) ORDER NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## ON PRIMARY

The `ON PRIMARY` option is a statement that is used in SQL Server to define on which file an object, e.g. a table, is going to be created. Such as on a primary or secondary file group inside the database. Snowflake provides a different logic and indicates distinct constraints. Please review the following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/constraints) for more information.

### Source

Copy code

```
:force:
CREATE TABLE [TABLE1](
[COL1] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
 CONSTRAINT [pk_dimAddress_AddressId] PRIMARY KEY CLUSTERED ([COL1]) 
 WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1 (
 COL1 VARCHAR(255) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL
  CONSTRAINT pk_dimAddress_AddressId PRIMARY KEY (COL1)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/23/2024" }}'
 ;
```

## ASC/DESC Column Sorting

Column sorting is not supported in Snowflake, the `ASC` or `DESC` keywords are being removed.

### Source

Copy code

```
:force:
CREATE TABLE [TABLE1](
	[COL1] [int] NOT NULL,
 CONSTRAINT [constraint1] PRIMARY KEY CLUSTERED ([COL1] ASC)
) ON [PRIMARY]
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1 (
	COL1 INT NOT NULL,
	 CONSTRAINT constraint1 PRIMARY KEY (COL1)
	)
	COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/23/2024" }}'
	;
```

## COMPUTED Columns

Computed columns are supported in Snowflake, we just need to add the explicit data type in order to be able to deploy the table, for example.

### Source

Copy code

```
:force:
CREATE TABLE [TABLE1](
	[COL2] [int] NOT NULL,
	[COL2] [int] NOT NULL,
	[COL1] AS (COL3 * COL2),
)
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1 (
	COL2 INT NOT NULL,
	COL2 INT NOT NULL,
	COL1 VARIANT AS (COL3 * COL2) /*** SSC-FDM-TS0014 - COMPUTED COLUMN WAS TRANSFORMED TO ITS SNOWFLAKE EQUIVALENT, FUNCTIONAL EQUIVALENCE VERIFICATION PENDING. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

If the computed expression cannot transform, a warning is added, and a simple column definition with the expression return type will be used instead, like in the following example:

### Source

Copy code

```
:force:
CREATE TABLE [TABLE1](
	[Col1] AS (CONVERT ([XML], ExpressionValue))
)
```

The expression `CONVERT ([NUMERIC], ExpressionValue)` is not yet supported, so after inspection, its type will be determined to be XML, so the transformation will be

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1 (
	Col1 TEXT AS (CAST(ExpressionValue AS VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!)) /*** SSC-FDM-TS0014 - COMPUTED COLUMN WAS TRANSFORMED TO ITS SNOWFLAKE EQUIVALENT, FUNCTIONAL EQUIVALENCE VERIFICATION PENDING. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

A process will run to determine the original expression type in SQL Server. However, the column will have the equivalent target type. In the previous example, the column type in SQLServer was XML, but the target type in Snowflake for storing an XML is TEXT. For more information about data type mapping, check the [data types sections](./transact-data-types).

## MASKED WITH Column Option

In SQL Server the data masking is used to keep sensitive information from nonprivileged users. Review the [SQL SERVER documentation](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking?view=sql-server-ver16) for more information. In Snowflake, there is a dynamic data masking functionality but it is available to Enterprise Edition only. Please review the following [Snowflake documentation](https://docs.snowflake.com/en/user-guide/security-column-ddm-use).

### Input

Copy code

```
:force:
CREATE TABLE TABLE1
(
	[COL1] [nvarchar](50) MASKED WITH (FUNCTION = 'default()') NULL
);
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLE1
(
	COL1 VARCHAR(50)
 	                !!!RESOLVE EWI!!! /*** SSC-EWI-TS0017 - COLUMN MASKING NOT SUPPORTED IN CREATE TABLE ***/!!!
 MASKED WITH (FUNCTION = 'default()') NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## ROWGUIDCOL Column Option

`ROWGUIDCOL` is no applicable in Snowflake. It is used in SQL Server for [UNIQUEIDENTIFIER](https://docs.microsoft.com/en-us/sql/t-sql/data-types/uniqueidentifier-transact-sql?view=sql-server-ver15) types that are currently translated to `VARCHAR`. For example:

### Input

Copy code

```
:force:
CREATE TABLE TABLEROWID (
    [ROWGUID] UNIQUEIDENTIFIER ROWGUIDCOL NOT NULL
) ON [PRIMARY];
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLEROWID (
    ROWGUID VARCHAR
                    !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'ROWGUIDCOL COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                    ROWGUIDCOL NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

## GENERATED ALWAYS AS ROW START/END Column Option

`ROW START/END` is not supported in Snowflake. An error is added when this kind of column option is transformed.

### Input

Copy code

```
:force:
CREATE TABLE TABLEROWID (
    [COL1] DATETIME GENERATED ALWAYS AS ROW START NOT NULL
) ON [PRIMARY];
```

### Output

Copy code

```
:force:
CREATE OR REPLACE TABLE TABLEROWID (
    COL1 TIMESTAMP_NTZ(3) GENERATED ALWAYS AS ROW START !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'GeneratedClause' NODE ***/!!! NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0036](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-EWI-0040](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040): Statement Not Supported.
3. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
4. [SSC-EWI-TS0017](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0017): Masking not supported.
5. [SSC-FDM-0012](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0012): Constraint in default expression is not supported.
6. [SSC-FDM-TS0002](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0002): This message is shown when there is a collate clause that is not supported in Snowflake.
7. [SSC-FDM-TS0009](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0009): Encrypted with not supported in Snowflake.
8. [SSC-FDM-TS0014](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0014): Computed column transformed.
9. [SSC-EWI-TS0015](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0015): Data type is not supported in Snowflake.
10. [SSC-PRF-0002](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0002): Case-insensitive columns can decrease the performance of queries.

## Azure Synapse Analytics

Translation specification for Azure Synapse Analytics Tables

Applies to

- Azure Synapse Analytics

### Description

This section presents the translation for syntax specific to [Azure Synapse Analytics Tables](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-azure-sql-data-warehouse?view=aps-pdw-2016-au7).

#### CREATE TABLE

Copy code

```
:force:
CREATE TABLE { database_name.schema_name.table_name | schema_name.table_name | table_name }
( 
    { column_name <data_type>  [ <column_options> ] } [ ,...n ]
)  
[ WITH ( <table_option> [ ,...n ] ) ]  
[;]
```

#### CREATE TABLE AS

Copy code

```
:force:
CREATE TABLE { database_name.schema_name.table_name | schema_name.table_name | table_name }
    [ ( column_name [ ,...n ] ) ]  
    WITH ( 
      <distribution_option> -- required
      [ , <table_option> [ ,...n ] ]    
    )  
    AS <select_statement>  
    OPTION <query_hint> 
[;]
```

### Source Patterns

#### WITH table options

Azure Synapse Analytics presents an additional syntax for defining table options.

Copy code

```
:force:
<table_option> ::=
    {
       CLUSTERED COLUMNSTORE INDEX -- default for Azure Synapse Analytics 
      | CLUSTERED COLUMNSTORE INDEX ORDER (column [,...n])  
      | HEAP --default for Parallel Data Warehouse
      | CLUSTERED INDEX ( { index_column_name [ ASC | DESC ] } [ ,...n ] ) -- default is ASC
    }  
    {
        DISTRIBUTION = HASH ( distribution_column_name )
      | DISTRIBUTION = HASH ( [distribution_column_name [, ...n]] ) 
      | DISTRIBUTION = ROUND_ROBIN -- default for Azure Synapse Analytics
      | DISTRIBUTION = REPLICATE -- default for Parallel Data Warehouse
    }
    | PARTITION ( partition_column_name RANGE [ LEFT | RIGHT ] -- default is LEFT  
        FOR VALUES ( [ boundary_value [,...n] ] ) )
```

Snowflake automatically handles table optimization through mechanisms like micro-partitioning. For this reason, an equivalent syntax for some of these table options does not exist in Snowflake. Therefore, it is not necessary to define some of Transact’s table options.

Table options that will be omitted:

- CLUSTERED COLUMNSTORE INDEX (without column)
- HEAP
- DISTRIBUTION
- PARTITION

`CLUSTERED [ COLUMNSTORE ] INDEX` with columns, will be transformed to Snowflake’s `CLUSTER BY`. A performance review PRF will be added as it is advised to check if defining a CLUSTER KEY is necessary.

##### Transact

Copy code

```
:force:
CREATE TABLE my_table (
    enterprise_cif INT,
    name NVARCHAR(100),
    address NVARCHAR(255),
    created_at DATETIME
) 
WITH (
    DISTRIBUTION = HASH(enterprise_cif),
    CLUSTERED INDEX (enterprise_cif)
);
```

##### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE my_table (
  enterprise_cif INT,
  name VARCHAR(100),
  address VARCHAR(255),
  created_at TIMESTAMP_NTZ(3)
)
--** SSC-PRF-0007 - PERFORMANCE REVIEW - CLUSTER BY **
CLUSTER BY (enterprise_cif)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2024" }}'
;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-PRF-0007](../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0007): PERFORMANCE REVIEW - CLUSTER BY.

## TEXTIMAGE\_ON

Applies to

- SQL Server

Note

Non-relevant statement.

Warning

Notice that this statement removed from the migration because it is a non-relevant syntax. It means that it is not required in Snowflake.\*\*

### Description

`TEXTIMAGE_ON [PRIMARY]` is a way in Transact to handle the large information groups inside a table. In Snowflake it is not required to define these kinds of characteristics because Snowflake handles large data files or information in a different arrangement.

### Sample

### Source Patterns

Notice that in this example the `TEXTIMAGE_ON [PRIMARY]` has been removed due to the unnecessary syntax.

#### SQL Server

Copy code

```
 CREATE TABLE [dbo].[TEST_Person](
	[date_updated] [datetime] NULL
 ) TEXTIMAGE_ON [PRIMARY]
```

#### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE dbo.TEST_Person (
	date_updated TIMESTAMP_NTZ(3) NULL
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
 ;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.
