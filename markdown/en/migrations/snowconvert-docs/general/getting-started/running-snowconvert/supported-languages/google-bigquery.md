# SnowConvert AI - Google BigQuery

## What is SnowConvert AI for Google BigQuery?

SnowConvert AI is a software tool that understands SQL Google BigQuery scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types

Specifically, SnowConvert AI for Google BigQuery performs the following conversions:

### Google BigQuery to Snowflake SQL

SnowConvert AI recognizes the Google BigQuery source code and converts the different statements into the appropriate SQL for the Snowflake target.

### Sample code

#### Input Code:

Copy code

```
CREATE TABLE IF NOT EXISTS your_project_id.my_dataset.product_catalog (
  product_sku STRING,
  stock_level INT64,
  unit_price FLOAT64
);
```

#### Output Code:

Copy code

```
CREATE TABLE IF NOT EXISTS your_project_id.my_dataset.product_catalog (
  product_sku STRING,
  stock_level INT,
  unit_price FLOAT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/08/2025",  "domain": "test" }}';
```

As you can see, most of the structure remains the same, but some column properties have to be transformed into Snowflake equivalents. For more information please refer to Google [BigQuery Translation References documentation](../../../../translation-references/bigquery/README).

### SnowConvert AI Terminology

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

- *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
- *SnowConvert AI*: the software that converts securely and automatically your Google BigQuery files to the Snowflake cloud data platform.
- *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
- *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

In the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Google BigQuery is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation.
