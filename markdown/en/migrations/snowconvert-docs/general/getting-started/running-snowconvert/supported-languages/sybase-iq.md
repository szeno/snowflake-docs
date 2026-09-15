# SnowConvert AI - Sybase IQ

## What is SnowConvert AI for Sybase IQ?

SnowConvert AI is a software tool that understands Sybase IQ scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI for Sybase IQ performs the following conversions:

### Sybase IQ to Snowflake SQL

SnowConvert AI understands the Sybase IQ source code and converts the Data Definition Language (DDL), Data Manipulation Language (DML), and functions in the source code to the corresponding SQL in the target: Snowflake.

#### Sample code

Sybase IQ basic input code:

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
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"sybase"}}'
;
```

As you can see, most of the structure remains the same. For example, some cases require the data types to be transformed.

#### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI: the software that converts your Sybase IQ files securely and automatically to the Snowflake cloud data platform.*
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* Parsing is an initial process by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

On the following few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Sybase IQ is capable of. If you’re ready, visit the [**Getting Started**](../../README) page in this documentation.
