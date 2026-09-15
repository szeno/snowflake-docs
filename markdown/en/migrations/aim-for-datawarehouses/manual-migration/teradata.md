# SnowConvert AI CLI - Teradata

## Specific CLI arguments

The following CLI arguments are specific for executing migrations with **SnowConvert AI CLI for Teradata**

### `--displaceDatabaseAsSchema`

This flag must be used with the `-s` parameter. When used it will maintain Teradata’s database name qualification as Snowflake’s data warehouse, contrary to its default behavior where it becomes a schema on Snowflake code. Let’s look at an example where `-s customSchema` is included:

Copy code

```
SELECT * FROM databaseName.tableName;
```

Copy code

```
-- Additional Params: -s customSchema
SELECT
* FROM
customSchema.tableName;
```

Copy code

```
-- Additional Params: -s customSchema --displaceDatabaseAsSchema
SELECT
* FROM
databaseName.customSchema.tableName;
```

#### `--CharacterToApproximateNumber <NUMBER>`

An integer value for the CHARACTER to Approximate Number transformation (Default: `10`).

#### `--DefaultDateFormat <STRING>`

String value for the Default DATE format (Default: `"YYYY/MM/DD"`).

#### `--DefaultTimeFormat <STRING>`

String value for the Default TIME format (Default: `"HH:MI:SS.FF6"`).

#### `--DefaultTimestampFormat <STRING>`

String value for the Default TIMESTAMP format (Default: `"YYYY/MM/DD HH:MI:SS.FF6"`).

#### `--DefaultTimezoneFormat <STRING>`

String value for the Default TIMEZONE format (Default: `"GMT-5"`).

#### `-p, --scriptTargetLanguage <TARGET_LANGUAGE>`

The string value specifies the target language to convert Bteq and Mload script files. Currently supported values are **SnowScript** and **Python**. The default value is set to **Python**.

#### `-n, --SessionMode <SESSION_MODE>`

SnowConvert AI CLI handles Teradata code in both TERA and ANSI modes. Currently, this is limited to the default case specification of character data and how it affects comparisons.

The string value specifies the Session Mode of the input code. Currently supported values are **TERA** and **ANSI**. The default value is set to **TERA**.

#### `--replaceDeleteAllToTruncate`

Flag to indicate whether Delete All statements must be replaced with Truncate or not. This will generate SSC-EWI-TD0037 when the replacement is done. Example:

Copy code

```
create table testTable(
    column1 varchar(30)
);

delete testTable all;

delete from testTable;
```

Copy code

```
CREATE OR REPLACE TABLE testTable (
    column1 varchar(30)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

DELETE FROM testTable;

DELETE FROM
    testTable;
```

Copy code

```
-- Additional Params: --replaceDeleteAllToTruncate
CREATE OR REPLACE TABLE testTable (
    column1 varchar(30)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

TRUNCATE TABLE testTable;

DELETE FROM
    testTable;
```

#### `--generateStoredProcedureTags`

Flag to indicate whether the SQL statements SELECT, INSERT, CREATE, DELETE, UPDATE, DROP, MERGE in Stored Procedures will be tagged on the converted code. This feature is used for easy statement identification on the migrated code. Wrapping these statements within these XML-like tags allows for other programs to quickly find and extract them. The decorated code looks like this:

Copy code

```
//<SQL_DELETE
EXEC(DELETE FROM SB_EDP_SANDBOX_LAB.PUBLIC.USER_LIST,[])
//SQL_DELETE!>
```

#### `--splitPeriodDatatype`

This flag is used to indicate that the tool should migrate any use of the `PERIOD` datatype as two separate `DATETIME` fields that will hold the original period begin and end values, anytime a period field or function is migrated using this flag SSC-FDM-TD0004 will be added to warn about this change.

Copy code

```
CREATE TABLE myTable(
   col1 PERIOD(DATE),
   col2 VARCHAR(50),
   col3 PERIOD(TIMESTAMP)
);
```

Copy code

```
CREATE OR REPLACE TABLE myTable (
   col1 VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!,
   col2 VARCHAR(50),
   col3 VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy code

```
-- Additional Params: --splitPeriodDatatype
CREATE OR REPLACE TABLE myTable (
   col1_begin DATE,
   col1_end DATE /*** SSC-FDM-TD0004 - PERIOD DATA TYPES ARE HANDLED AS TWO DATA FIELDS ***/,
   col2 VARCHAR(50),
   col3_begin TIMESTAMP,
   col3_end TIMESTAMP /*** SSC-FDM-TD0004 - PERIOD DATA TYPES ARE HANDLED AS TWO DATA FIELDS ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### `--arrange`

Flag to indicate whether the input code should be processed before parsing and transformation.

#### `--RenamingFile`

The path to a .json file that specifies new names for certain objects such as Tables, Views, Procedures, Functions, and Macros. This parameter can’t be used with the `customSchema` argument. Navigate to the [Renaming Feature](renaming-feature) to learn more about this argument.

#### `--UseCollateForCaseSpecification`

This flag indicates whether to use COLLATE or UPPER to preserve Case Specification functionality, for example, CASESPECIFIC or NOT CASESPECIFIC. By default, it is turned off, meaning that the UPPER function will be used to emulate case insensitivity (NOT CASESPECIFIC).
