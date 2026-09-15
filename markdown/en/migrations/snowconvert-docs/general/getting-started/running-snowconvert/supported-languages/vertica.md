# SnowConvert AI - Vertica

## What is SnowConvert AI for Vertica?

SnowConvert AI is a software tool that understands SQL Vertica scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI for Vertica performs the following conversions:

### Vertica to Snowflake SQL

SnowConvert AI recognizes the Vertica source code and converts the different statements into the appropriate SQL for the Snowflake target.

### Sample code

#### Input Code:

Copy code

```
CREATE TABLE data_types_conversion (
    int8_col INT8,
    long_varbinary_col LONG VARBINARY(65000),
    uuid_col UUID
);
```

#### Output Code:

Copy code

```
CREATE TABLE data_types_conversion (
    int8_col INTEGER,
    long_varbinary_col VARBINARY(65000),
    uuid_col VARCHAR(36)
);
```

As you can see, most of the structure remains the same, but some column properties have to be transformed into Snowflake equivalents. For more information please refer to [Vertica Translation References documentation.](../../../../translation-references/vertica/README)

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI*: the software that converts securely and automatically your Vertica files to the Snowflake cloud data platform.
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

In the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Vertica is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation.
