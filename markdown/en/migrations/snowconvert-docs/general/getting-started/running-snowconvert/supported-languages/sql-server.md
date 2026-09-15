# SnowConvert AI - SQL Server

## What is SnowConvert AI for SQL Server?

SnowConvert AI is a software tool that understands SQL Server scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI for SQL Server performs the following conversions:

### SQL Server to Snowflake SQL

SnowConvert AI understands the SQL Server source code and converts the Data Definition Language (DDL), Data Manipulation Language (DML), and functions in the source code to the corresponding SQL in the target: Snowflake.

#### Sample code

SQL Server basic input code:

Copy code

```
CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);
```

Snowflake SQL output code:

Copy code

```
CREATE OR REPLACE TABLE Persons (
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;
```

As you can see, most of the structure remains the same. There are some cases where the datatypes have to be transformed, for example.

### SQL Server Stored Procedures to JavaScript Embedded in Snowflake SQL

SnowConvert AI takes SQL Server stored procedures and converts them to JavaScript embedded into Snowflake SQL. SQL Server’s CREATE PROCEDURE is replaced by Snowflake’s CREATE OR REPLACE PROCEDURE. JavaScript is called as a scripting language, and all of the inner statements are converted to JavaScript.

#### Sample code

SQL Server basic stored procedure:

Copy code

```
CREATE PROCEDURE SelectAllCustomers
AS
SELECT * FROM Customers
GO;
```

Snowflake SQL output code, with embedded JavaScript:

Copy code

```
:force:
-- Additional Params: -t JavaScript
CREATE OR REPLACE PROCEDURE SelectAllCustomers ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   // REGION SnowConvert AI Helpers Code
   // END REGION

 EXEC(`SELECT
   *
FROM
   Customers`);
$$;
```

- When creating the JavaScript code, there is a portion of code added as a *helper*, required for an easier transformation of the contents of the procedure.
- You can expect to see warnings with an associated code to help you find out what is happening in the converted code. (See [issues and troubleshooting](../../../technical-documentation/issues-and-troubleshooting/README))

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI*: the software that converts securely and automatically your SQL Server files to the Snowflake cloud data platform.
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

On the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for SQL Server is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation.
