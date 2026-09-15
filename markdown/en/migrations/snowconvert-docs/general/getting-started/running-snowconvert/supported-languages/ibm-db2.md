# SnowConvert AI - IBM DB2

## What is SnowConvert AI for IBM DB2?

SnowConvert AI is a software tool that understands SQL IBM DB2 scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI for IBM DB2 performs the following conversions:

### IBM DB2 to Snowflake SQL

SnowConvert AI recognizes the IBM DB2 source code and converts the different statements into the appropriate SQL for the Snowflake target.

### Sample code

#### Input Code:

Copy code

```
CREATE TABLE IF NOT EXISTS your_project_id.my_dataset.product_catalog (
  product_ID INT,
  stock_level BLOB
)
;
```

#### Output Code:

Copy code

```
CREATE TABLE IF NOT EXISTS your_project_id.my_dataset.product_catalog (
  product_ID INT,
  stock_level BINARY
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/02/2025",  "domain": "no-domain-provided" }}'
;
```

As you can see, most of the structure remains the same, but some column properties have to be transformed into Snowflake equivalents. For more information please refer to [IBM DB2 Translation References documentation](../../../../translation-references/db2/README).

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI*: the software that converts securely and automatically your IBM DB2 files to the Snowflake cloud data platform.
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

In the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for IBM DB2 is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation.
