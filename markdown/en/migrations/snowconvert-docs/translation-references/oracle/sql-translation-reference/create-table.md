# Oracle - Create Table

In this section you could find information about TABLES, their syntax and current conversions.

## Description

In Oracle, the CREATE TABLE statement is used to create one of the following types of tables: a relational table which is the basic structure to hold user data, or an object table which is a table that uses an object type for a column definition. ([Oracle documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-TABLE.html#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6))

**Oracle syntax**

Copy code

```
CREATE [ { GLOBAL | PRIVATE } TEMPORARY | SHARDED | DUPLICATED | [ IMMUTABLE ] BLOCKCHAIN 
  | IMMUTABLE  ] 
   TABLE
  [ schema. ] table
  [ SHARING = { METADATA | DATA | EXTENDED DATA | NONE } ]
  { relational_table | object_table | XMLType_table }
  [ MEMOPTIMIZE FOR READ ]
  [ MEMOPTIMIZE FOR WRITE ]
  [ PARENT [ schema. ] table ] ;
```

**Snowflake Syntax**

Copy code

```
CREATE [ OR REPLACE ]
    [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE | TRANSIENT } ]
  TABLE [ IF NOT EXISTS ] <table_name> (
    -- Column definition
    <col_name> <col_type>
      [ inlineConstraint ]
      [ NOT NULL ]
      [ COLLATE '<collation_specification>' ]
      [
        {
          DEFAULT <expr>
          | { AUTOINCREMENT | IDENTITY }
            [
              {
                ( <start_num> , <step_num> )
                | START <num> INCREMENT <num>
              }
            ]
            [ { ORDER | NOORDER } ]
        }
      ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ COMMENT '<string_literal>' ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ ... ] ]

    -- Out-of-line constraints
    [ , outoflineConstraint [ ... ] ]
  )
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE } ]
  [ STAGE_FILE_FORMAT = (
     { FORMAT_NAME = '<file_format_name>'
       | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } [ formatTypeOptions ]
     } ) ]
  [ STAGE_COPY_OPTIONS = ( copyOptions ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

Note

For more Snowflake information review the following [documentation](https://docs.snowflake.com/en/sql-reference/sql/create-table).

## Sample Source Patterns

### 2.1. Physical and Table Properties

#### Oracle

Copy code

```
CREATE TABLE "MySchema"."BaseTable"
(
    BaseId NUMBER DEFAULT 10 NOT NULL ENABLE
) SEGMENT CREATION IMMEDIATE
  PCTFREE 0 PCTUSED 40 INITRANS 1 MAXTRANS 255
  COLUMN STORE COMPRESS FOR QUERY HIGH NO ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "MyTableSpace"
  PARTITION BY LIST ("BaseId")
 (
    PARTITION "P20211231"  VALUES (20211231) SEGMENT CREATION DEFERRED
    PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
    ROW STORE COMPRESS ADVANCED LOGGING
    STORAGE(
    BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
    TABLESPACE "MyTableSpace" 
  )
  PARALLEL;
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "MySchema"."BaseTable"
 (
     BaseId NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ DEFAULT 10 NOT NULL
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

Note

Table properties are removed because they are not required after the migration in Snowflake.

### 2.2. Constraints and Constraint States

#### CHECK Constraints

Snowflake supports CHECK constraints with deterministic, scalar expressions. Oracle-specific state clauses (`DEFERRABLE`, `RELY`, `INITIALLY`, `ENABLE`, `DISABLE`) are removed during conversion with **SSC-FDM-0046** annotations. CHECK constraints with unsupported expressions (UDFs, non-deterministic functions) are flagged with **SSC-EWI-0116**.

**Supported:**

- Basic CHECK constraints with scalar, deterministic expressions
- Column-level and table-level CHECK constraints
- Named and unnamed constraints

**Removed automatically (with SSC-FDM-0046):**

- `[NOT] DEFERRABLE` - Snowflake always validates immediately
- `[NOT] RELY` - Optimizer hint not supported
- `INITIALLY IMMEDIATE` / `INITIALLY DEFERRED`
- `ENABLE` / `DISABLE` - Snowflake constraints are always enforced

**Unsupported (flagged with SSC-EWI-0116):**

- User-defined functions (UDFs)
- Non-deterministic built-in functions
- Context-dependent functions
- Subqueries

##### Example 1: Basic CHECK Constraint

###### Oracle

Copy code

```
CREATE TABLE Products (
  ProductID NUMBER PRIMARY KEY,
  Price NUMBER(10,2) CHECK (Price > 0),
  Quantity NUMBER CHECK (Quantity >= 0 AND Quantity <= 1000)
);
```

###### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Products (
  ProductID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
  Price NUMBER(10, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ CHECK (Price > 0),
  Quantity NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ CHECK (Quantity >= 0
  AND Quantity <= 1000)
)
;
```

##### Example 2: CHECK Constraint with NOT DEFERRABLE (Removed)

The `NOT DEFERRABLE` clause is removed with **SSC-FDM-0046** because Snowflake always validates CHECK constraints immediately.

###### Oracle

Copy code

```
CREATE TABLE Accounts (
  AccountID NUMBER PRIMARY KEY,
  Balance NUMBER(15,2) CHECK (Balance >= -1000) NOT DEFERRABLE
);
```

###### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Accounts (
  AccountID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
  Balance NUMBER(15, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
                                                                                                          --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] DEFERRABLE **
                                                                                                          CHECK (Balance >= -1000)
)
;
```

##### Example 3: CHECK Constraint with RELY Clause (Removed)

###### Oracle

Copy code

```
CREATE TABLE Orders (
  OrderID NUMBER PRIMARY KEY,
  TotalAmount NUMBER(10,2) CONSTRAINT CHK_Amount CHECK (TotalAmount > 0) RELY
);
```

###### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Orders (
  OrderID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
  TotalAmount NUMBER(10, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
                                                                                                              --** SSC-FDM-0046 - UNSUPPORTED CHECK CONSTRAINT CLAUSE REMOVED: [NOT] RELY **
                                                                                                              CONSTRAINT CHK_Amount CHECK (TotalAmount > 0)
)
;
```

##### Example 4: CHECK Constraint with Unresolved Function (Unsupported)

When a CHECK constraint references a function that cannot be resolved, it is flagged with **SSC-EWI-0116** as a user-defined function.

###### Oracle

Copy code

```
CREATE TABLE Invoices (
  InvoiceID NUMBER NOT NULL,
  TaxCode VARCHAR2(10),
  CONSTRAINT chk_tax_code CHECK (validate_tax_code(TaxCode) = 1)
);
```

###### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Invoices (
  InvoiceID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ NOT NULL,
  TaxCode VARCHAR(10),
  CONSTRAINT chk_tax_code
                          !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH user-defined function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                          CHECK(validate_tax_code(TaxCode) = 1)
)
;
```

Note

The `USING INDEX` constraint clause is entirely removed from the output code during the conversion.

#### NOT NULL Constraint States

In case you have any constraint state after a NOT NULL constraint as follows:

- `RELY`
- `NO RELY`
- `RELY ENABLE`
- `RELY DISABLE`
- `VALIDATE`
- `NOVALIDATE`

These will also be commented out.

Note

The ENABLE constraint state will be completely removed from the output code during the conversion process. In the case of the DISABLE state, it will also be removed concurrently with the NOT NULL constraint.

#### Oracle

Copy code

```
CREATE TABLE Table1(
  col1 INT NOT NULL ENABLE,
  col2 INT NOT NULL DISABLE,
  col3 INT NOT NULL RELY
);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE Table1 (
    col1 INT NOT NULL,
    col2 INT ,
    col3 INT NOT NULL /*** SSC-FDM-OR0006 - CONSTRAINT STATE RELY REMOVED FROM NOT NULL INLINE CONSTRAINT ***/
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
  ;
```

### 2.3. Foreign Key

If there is a table with a NUMBER column with no precision nor scale, and another table with a NUMBER(\*,0) column that references to the previously mentioned NUMBER column, we will comment out this foreign key.

#### Oracle

Copy code

```
CREATE TABLE "MySchema"."MyTable"
(
    "COL1" NUMBER, 
    CONSTRAINT "PK" PRIMARY KEY ("COL1")
);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "MySchema"."MyTable"
    (
        "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
        CONSTRAINT "PK" PRIMARY KEY ("COL1")
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

### 2.4. Virtual Column

#### Oracle

Copy code

```
CREATE TABLE "MySchema"."MyTable"
(
    "COL1" NUMBER GENERATED ALWAYS AS (COL1 * COL2) VIRTUAL
);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "MySchema"."MyTable"
    (
        "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ AS (COL1 * COL2)
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

### 2.5. Identity Column

For identity columns, a sequence is created and assigned to the column.

#### Oracle

Copy code

```
CREATE TABLE "MySchema"."BaseTable"
(
	"COL0" NUMBER GENERATED BY DEFAULT ON NULL 
		AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 
		INCREMENT BY 1 
		START WITH 621 
		CACHE 20 
		NOORDER  NOCYCLE  NOT NULL ENABLE
);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "MySchema"."BaseTable"
	(
		"COL0" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ IDENTITY(621, 1) ORDER NOT NULL
	)
	COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
	;
```

### 2.6. CLOB and BLOB column declaration

Columns declared as CLOB or BLOB will be changed to VARCHAR.

#### Oracle

Copy code

```
CREATE TABLE T
(
 Col1 BLOB DEFAULT EMPTY_BLOB(),
Col5 CLOB DEFAULT EMPTY_CLOB()
);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE T
 (
  Col1 BINARY,
 Col5 VARCHAR
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

### 2.7. Constraint Name

Warning

The constraint name is removed from the code because it is not applicable in Snowflake.

#### Oracle

Copy code

```
CREATE TABLE "CustomSchema"."BaseTable"(
 "PROPERTY" VARCHAR2(64) CONSTRAINT "MICROSOFT_NN_PROPERTY" NOT NULL ENABLE
  );
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "CustomSchema"."BaseTable" (
  "PROPERTY" VARCHAR(64) NOT NULL /*** SSC-FDM-0012 - CONSTRAINT NAME '"MICROSOFT_NN_PROPERTY"' IN NULL OR NOT NULL CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE ***/
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;
```

### 2.8. Default columns with times

The columns declared as Date types will be cast to match with the specific date type.

#### Oracle

Copy code

```
CREATE TABLE TABLE1
(
"COL1" VARCHAR(50) DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TABLE1
(
 COL0 TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
 COL1 TIMESTAMP(6) DEFAULT CURRENT_TIME,
 COL2 TIMESTAMP(6) WITH LOCAL TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL3 TIMESTAMP(6) WITH TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL4 TIMESTAMP(6) WITHOUT TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL5 TIMESTAMP(6) DEFAULT TO_TIMESTAMP('01/01/1900 12:00:00.000000 AM', 'MM/DD/YYYY HH:MI:SS.FF6 AM')
 );
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE TABLE1
 (
 "COL1" VARCHAR(50) DEFAULT TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYY-MM-DD HH:MI:SS')
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;

 --** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR TABLE1. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
 CREATE OR REPLACE TABLE TABLE1
 (
  COL0 TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP(6),
  COL1 TIMESTAMP(6) DEFAULT CURRENT_TIME() :: TIMESTAMP(6),
  COL2 TIMESTAMP_LTZ(6) DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP_LTZ(6),
  COL3 TIMESTAMP_TZ(6) DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP_TZ(6),
  COL4 TIMESTAMP(6) WITHOUT TIME ZONE DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP(6) WITHOUT TIME ZONE,
  COL5 TIMESTAMP(6) DEFAULT TO_TIMESTAMP('01/01/1900 12:00:00.000000 AM', 'MM/DD/YYYY HH:MI:SS.FF6 AM') :: TIMESTAMP(6)
  )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

### 2.9 Sharing and Memoptimize options

Some options in Oracle are not required in Snowflake. That is the case for the `sharing` and `memoptimize` options, they will be removed in the output code.

#### Oracle

Copy code

```
CREATE TABLE table1 
    SHARING = METADATA (
     id NUMBER,
     name VARCHAR2(50),
     date DATE,
     CONSTRAINT pk_table PRIMARY KEY (id)
 ) MEMOPTIMIZE FOR READ;
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE table1 (
     id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
     name VARCHAR(50),
     date TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
     CONSTRAINT pk_table PRIMARY KEY (id)
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
 ;
```

### 2.10 AS SubQuery

The following properties and clauses are unsupported when creating a table through `AS SubQuery` in Snowflake.

Copy code

```
[ immutable_table_clauses ]
[ blockchain_table_clauses ]
[ DEFAULT COLLATION collation_name ]
[ ON COMMIT { DROP | PRESERVE } DEFINITION ]
[ ON COMMIT { DELETE | PRESERVE } ROWS ]
[ physical_properties ]
```

#### Oracle

Copy code

```
create table table1
-- NO DROP NO DELETE HASHING USING sha2_512 VERSION v1 -- blockchain_clause not yet supported
DEFAULT COLLATION somename
ON COMMIT DROP DEFINITION
ON COMMIT DELETE ROWS
COMPRESS
NOLOGGING
AS
   select
      *
   from
      table1;
```

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE table1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
-- NO DROP NO DELETE HASHING USING sha2_512 VERSION v1 -- blockchain_clause not yet supported
AS
   select
      *
   from
      table1;
```

## Known Issues

1. Some properties on the tables may be adapted to or commented on because the behavior in Snowflake is different.

## Related EWIs

1. [SSC-EWI-0116](../../../issues-and-troubleshooting/conversion-issues/generalEWI#scenario-1-check-constraints-with-unsupported-expressions): CHECK constraint with unsupported expression (UDF, non-deterministic).
2. [SSC-FDM-0006](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.
3. [SSC-FDM-0019](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0019): Semantic information could not be loaded.
4. [SSC-FDM-0046](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0046): Oracle state clause removed from CHECK constraint (DEFERRABLE, RELY, INITIALLY, ENABLE, DISABLE).
5. [SSC-FDM-OR0042](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.
6. [SSC-FDM-OR0006](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0006): Constraint state removed from not null inline constraint.
