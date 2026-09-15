# SnowConvert AI - Teradata

## What is SnowConvert AI for Teradata?

SnowConvert AI is a software tool that understands [**Teradata SQL**](https://www.teradata.com/), BTEQ, and other Teradata-specific scripts (such as Fastload, Multiload, TPump, and TPT files) and converts this source code into functionally equivalent [**Snowflake**](https://www.snowflake.com/) code.

### Conversion Types

Specifically, SnowConvert AI for Teradata performs the following conversions:

### Teradata SQL to Snowflake SQL

SnowConvert AI understands the Teradata source code and converts the Data Definition Language (DDL), Data Manipulation Language (DML), and functions in the source code to the corresponding SQL in the target: Snowflake. SnowConvert AI can migrate the source code in any of these three extensions **.sql, .dml, ddl**

### Teradata Stored Procedures to JavaScript Embedded in Snowflake SQL

SnowConvert AI takes Teradata stored procedures (usually written in SQL) and converts them to JavaScript embedded into Snowflake SQL. Teradata’s CREATE PROCEDURE and REPLACE PROCEDURE language is replaced by Snowflake’s CREATE OR REPLACE PROCEDURE language. JavaScript is called as a scripting language, and all of the inner statements are converted to JavaScript.

### Teradata BTEQ, Fastload, Multiload, and TPT to Python

Basic Teradata Query (BTEQ) is Teradata’s proprietary scripting language. All BTEQ script files will be converted to Python scripts. A helper class will be called from the converted scripts to create the functional equivalence between the source and the target. More information about the Python Helpers can be found on our [Translation Reference page](../../../../translation-references/teradata/README). BTEQ can be batch run from outside the Snowflake environment. Learn more about how [**you can connect Python scripts directly to Snowflake**](https://docs.snowflake.com/en/user-guide/python-connector.html).

BTEQ files are also the foundation for multiple other proprietary data types that Teradata has created:

- Fastload
- Multiload
- TPUMP

Each one of these file types are extensions of BTEQ. SnowConvert AI translates each one of these file types to Python.

Each of these conversions are optimized to give you the most functionally equivalent output ready for use in Snowflake. For more information on the power of the kind of conversion SnowConvert AI can provide, you can learn more about our tool by visiting our complete [**SQL reference guide**](../../../../translation-references/teradata/README).

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *BTEQ (Basic Teradata Query):* BTEQ was the first utility and query tool for Teradata.
- TPT (Teradata Parallel Transporter): TPT is a new generation utility tool that aims to create a one-stop tool for all the activities related to loading and exporting data from/to Teradata databases.
- *SnowConvert AI*: the software that converts securely and automatically your Teradata files to the Snowflake cloud data platform.
- *Conversion rule or transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure to process the conversion rules.

On the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Teradata is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation. If you’re interested in getting more information about SnowConvert AI in general, visit our [**SnowConvert AI for Teradata**](../../../../translation-references/teradata/README) information page.

## Translation Sample

*Teradata SQL Statement*

Copy code

```
-- CREATE TABLE DDL
CREATE SET TABLE TABLE1,
    NO BEFORE JOURNAL,
    NO AFTER JOURNAL,
    CHECKSUM = DEFAULT,
    DEFAULT MERGEBLOCKRATIO
(
    COL1 VARCHAR(15) CHARACTER SET LATIN NOT CASESPECIFIC,
    Col2 BYTEINT CHECK ( CurrentFlag  IN (0 ,1 ) ) NOT NULL,
    COL3 DATE FORMAT 'yyyy-mm-dd',
    COL4 BLOB(2097088000),
    COL5 BYTEINT,
    COL7 INTEGER NOT NULL COMPRESS (1 ,2 ,3 ,4),
    COL8 INTERVAL HOUR(2) TO MINUTE
);

-- REPLACE VIEW DDL
REPLACE VIEW VIEW1 AS
SELECT * FROM TABLE1
UNION ALL
SELECT MAX(COL1) FROM TABLE1;
```

*The Converted Snowflake SQL Code*:

Copy code

```
-- CREATE TABLE DDL
--** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
CREATE OR REPLACE TABLE TABLE1
(
    COL1 VARCHAR(15) COLLATE 'en-cs',
    Col2 BYTEINT
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
 CHECK ( CurrentFlag  IN (0 ,1 ) ) NOT NULL,
    COL3 DATE,
    COL4 BINARY /*** SSC-FDM-TD0001 - COLUMN CONVERTED FROM BLOB DATA TYPE ***/,
    COL5 BYTEINT,
    COL7 INTEGER NOT NULL,
    COL8 VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL HOUR(2) TO MINUTE DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

-- REPLACE VIEW DDL
CREATE OR REPLACE VIEW VIEW1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
AS
SELECT
    * FROM
    TABLE1
    UNION ALL
    SELECT
    MAX(COL1) FROM
    TABLE1;
```

In this converted SQL you will notice that we are converting many things such as:

- Adding `PUBLIC` Schema by default for all the Table and view names if the user doesn’t specify one (see how to specify a Schema).
- `CREATE SET TABLE` to `CREATE TABLE`
- `REPLACE VIEW` to `CREATE OR REPLACE VIEW`
- Data Types: `BLOB` to `BINARY` and `INTERVAL` to `VARCHAR`
- Data Type Attributes: `NOT CASESPECIFIC` to `COLLATE`
- Removing pieces of the Teradata SQL that are not necessary in Snowflake due to Snowflake’s architecture such as `NO BEFORE JOURNAL`, `NO AFTER JOURNAL`, `CHECKSUM`, `COMPRESS`, and `DEFAULT MERGEBLOCKRATIO`.
