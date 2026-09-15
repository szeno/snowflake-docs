# SnowConvert AI - Oracle

## What is SnowConvert AI for Oracle?

SnowConvert AI is a software tool that understands [Oracle SQL and PL/SQL](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/index.html), and performs the following conversions:

- Oracle SQL to [Snowflake SQL](https://www.snowflake.com/)
- Oracle PL/SQL to:
  - [Snowflake Scripting](/developer-guide/snowflake-scripting/index)
  - [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript) embedded in Snowflake SQL

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- ***SQL (Structured Query Language):*** The standard language for storing, manipulating, and retrieving data in most modern database architectures.
- ***PL/SQL:*** Procedural Language for SQL. This was created by Oracle, and is still used by Oracle as the scripting language for stored procedures and functions in Oracle.
- ***SnowConvert AI*****:** The software that converts securely and automatically your Oracle files to the Snowflake cloud data platform.
- ***Conversion rule or transformation rule:*** Rules that allow SnowConvert AI to convert from a portion of source code and determine the expected target code.
- ***Parse:*** Parse or parsing is an initial process done by SnowConvert AI to understand the source code, and build up an internal data structure to process the conversion rules.

Let’s dive into some of the code conversions that **Snowflake SnowConvert AI** can perform.

## Code Conversions

### Oracle SQL to Snowflake SQL

SnowConvert AI for Oracle takes in Oracle source code in SQL and converts the Data Definition Language (DDL), Data Manipulation Language (DML), and functions in the source code to the corresponding SQL in Snowflake SQL.

#### Example

Here is an example of the conversion of a simple `CREATE TABLE` statement.

The source code:

Copy code

```
CREATE TABLE "MyTable"
(
  "COL1" NUMBER,
  "COL2" NUMBER,
  "COL3" NUMBER GENERATED ALWAYS AS (COL1 * COL2) VIRTUAL,
  "COL4" LONG,
  "COL5" CLOB,
  "COL6" ROWID,
  "COL7" NVARCHAR2(10),
  "COL8" RAW(255),
  CONSTRAINT "PK" PRIMARY KEY ("COL1")
);
```

The migrated Snowflake SQL code:

Copy code

```
CREATE OR REPLACE TABLE "MyTable"
  (
    "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    "COL2" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    "COL3" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ AS (COL1 * COL2),
    "COL4" VARCHAR,
    "COL5" VARCHAR,
    "COL6" VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!,
    "COL7" VARCHAR(10),
    "COL8" BINARY,
    CONSTRAINT "PK" PRIMARY KEY ("COL1")
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
  ;
```

In this converted SQL you will notice that we are converting many things. A few highlights:

- Adding `PUBLIC` Schema by default for all the Table and view names if the user doesn’t specify one
- `CREATE TABLE` to `CREATE OR REPLACE TABLE`
- Data Type Conversions:
  - `LONG` to `VARCHAR`
  - `CLOB` to `VARCHAR`
  - `ROWID` to `VARCHAR`
  - `NVARCHAR2` to `VARCHAR`
  - `RAW` to `BINARY`
- Data Type Attributes: `GENERATED ALWAYS AS (COL1 * COL2) VIRTUAL` to `AS (COL1 * COL2)`

For more information about data types and their equivalent: [Data Types](../../../../translation-references/oracle/README). More examples can be found in the rest of the documentation.

### Oracle PL/SQL

SnowConvert AI takes Oracle stored procedures and functions (**PL/SQL**) and converts them to either **Snowflake Scripting** or **JavaScript** embedded into Snowflake SQL. Oracle `CREATE PROCEDURE` and `REPLACE PROCEDURE` syntax is replaced by Snowflake `CREATE OR REPLACE PROCEDURE` syntax.

#### Example

Here is an example of the conversion of a simple `CREATE PROCEDURE` in Oracle that does an insert into a table used for logging.

Note

This example will be used for both Snowflake Scripting and JavaScript.

Copy code

```
CREATE OR REPLACE PROCEDURE SC_DEMO.PROC_LOG
      (final_proc  VARCHAR2,
       final_message   VARCHAR2,
       logger_type VARCHAR2 DEFAULT 'I')
AS
BEGIN
  INSERT INTO SC_DEMO.PROC_LOG_TABLE
    VALUES (SC_DEMO.final_logging_seq.NEXTVAL,
            sysdate,
            SUBSTR(logger_type, 1, 1),
            SUBSTR(final_proc, 1, 30),
            SUBSTR(final_message, 1, 1024));
  COMMIT;

END;
```

### To Snowflake Scripting

Snowflake Scripting works as an extension to Snowflake SQL, it adds support for procedural logic and this allows us to create Stored Procedures and replicate similar behaviours and statements of Oracle PL/SQL.

#### Migrated Example

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE SC_DEMO.PROC_LOG
(final_proc VARCHAR, final_message VARCHAR,
 logger_type VARCHAR DEFAULT 'I')
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    INSERT INTO SC_DEMO.PROC_LOG_TABLE
      VALUES (SC_DEMO.final_logging_seq.NEXTVAL, CURRENT_TIMESTAMP(),
              SUBSTR(:logger_type, 1, 1),
              SUBSTR(:final_proc, 1, 30),
              SUBSTR(:final_message, 1, 1024));
    --** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
    COMMIT;
  END;
$$;
```

### To JavaScript

JavaScript is called as a scripting language, all inner statements are converted to JavaScript. If you want to understand better the JavaScript API check [this documentation](https://docs.snowflake.com/en/sql-reference/stored-procedures-javascript.html).

#### Migrated Example

Copy code

```
:force:
-- Additional Params: -t JavaScript
CREATE OR REPLACE PROCEDURE SC_DEMO.PROC_LOG
(final_proc STRING, final_message STRING,
 logger_type STRING DEFAULT 'I')
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  EXEC(`INSERT INTO SC_DEMO.PROC_LOG_TABLE
  VALUES (SC_DEMO.final_logging_seq.NEXTVAL, CURRENT_TIMESTAMP(),
            SUBSTR(?, 1, 1),
            SUBSTR(?, 1, 30),
            SUBSTR(?, 1, 1024))`,[LOGGER_TYPE,FINAL_PROC,FINAL_MESSAGE]);
  EXEC(`--** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
COMMIT;`);
$$;
```

In this converted SQL you will notice that we have converted to a new language (JavaScript) embedded into Snowflake SQL. There are more than a few highlights, but suffice it to say that this documentation has all the essentials to understand this kind of conversion.

The line that states `// ... Necessary SnowConvert AI Helpers are inserted here ...` will actually have the **SnowConvert AI JavaScript Helpers**. They can be lengthy, so they are removed from this first example.

#### 

And that’s it! Snowflake SnowConvert AI takes the pain and frustration out of changing data platforms. Learn more about getting started with SnowConvert AI for Oracle on the next page.
