# PostgreSQL - CREATE MATERIALIZED VIEW

Translation reference to convert PostgreSQL Materialized View to Snowflake Dynamic Table

## Applies to

- PostgreSQL
- Greenplum
- Netezza

## Description

Materialized Views are transformed into Snowflake Dynamic Tables. To properly configure Dynamic Tables, two essential parameters must be defined: TARGET\_LAG and WAREHOUSE. If these parameters are left unspecified in the configuration options, preassigned values will be used during the conversion, as demonstrated in the example below.

## Grammar Syntax

Copy code

```
CREATE MATERIALIZED VIEW [ IF  NOT EXISTS ] <table_name>
    [ (<column_name> [, ...] ) ]
    [ USING <method> ]
    [ WITH ( <storage_parameter> [= <value>] [, ... ] ) ]
    [ TABLESPACE <tablespace_name> ]
    AS <query>
    [ WITH [ NO ] DATA ]
```

## Code Examples

### Simple Case

Input Code:

#### PostgreSQL

Copy code

```
:force:
CREATE MATERIALIZED VIEW product_summary AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM products
GROUP BY category;
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE OR REPLACE DYNAMIC TABLE product_summary
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM
    products
GROUP BY category;
```

### IF NOT EXISTS

Note

:class: tip
This syntax is fully supported in Snowflake.

This clause has been removed during the migration from PostgreSQL to Snowflake.

### USING, TABLESPACE, and WITH

Note

This syntax is not needed in Snowflake.

These clauses are removed during the conversion process. In PostgreSQL, they are used to further customize data storage manually. This is something that Snowflake handles automatically (micro partitions), and it is typically not a concern.

## Related EWIs

1. [SSC-FDM-0031](../../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0031): Dynamic Table required parameters set by default
