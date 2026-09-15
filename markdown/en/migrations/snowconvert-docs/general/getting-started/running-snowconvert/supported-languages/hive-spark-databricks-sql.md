# SnowConvert AI - Hive-Spark-Databricks SQL

SnowConvert AI is a software tool that understands SQL scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI performs the following conversions:

### Hive-Spark- Databricks SQL to Snowflake SQL

SnowConvert AI understands the Hive- Spark - Databricks SQL source code and converts the Data Definition Language (DDL), Data Manipulation Language (DML), and functions in the source code to the corresponding SQL in the target: Snowflake.

#### Sample code

Hive - Spark - Databricks SQL basic input code:

Copy code

```
:force:
CREATE TABLE films (
  code        char(5) CONSTRAINT firstkey PRIMARY KEY,
  title       varchar(40) NOT NULL,
  did         integer NOT NULL,
  date_prod   date
);
```

Snowflake SQL output code:

Copy code

```
CREATE TABLE films (
  code        char(5) CONSTRAINT firstkey PRIMARY KEY,
  title       varchar(40) NOT NULL,
  did         integer NOT NULL,
  date_prod   date
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "databricks",  "convertedOn": "04/24/2025",  "domain": "test" }}';
```

As you can see, most of the structure remains the same. For example, some cases require the data types to be transformed.

# SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI: the software that converts your Hive-Spark-Databricks SQL files securely and automatically to the Snowflake cloud data platform.*
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* Parsing is an initial process by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

On the following few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Hive -Spark - Databricks SQL is capable of. If you’re ready, visit the [**Getting Started**](../../README) page in this documentation.
