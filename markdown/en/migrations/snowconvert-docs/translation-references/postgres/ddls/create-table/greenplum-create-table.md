# Greenplum - CREATE TABLE

Translation from Greenplum to Snowflake

## Description

This section explains features exclusive to Greenplum.

For more information, please refer to [`CREATE TABLE`](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-sql_commands-CREATE_TABLE.html) the documentation.

## Grammar Syntax

Copy code

```
CREATE TABLE <table_name> (
  [ <column_name> <data_type> [ ENCODING ( <storage_directive> [, ...] ) ]
] )
[ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
    | DISTRIBUTED RANDOMLY
    | DISTRIBUTED REPLICATED ]
```

## ENCODING

Note

This syntax is not needed in Snowflake.

The compression encoding for a column. In Snowflake, defining ENCODING is unnecessary because it automatically handles data compression, unlike Greenplum, which could set up the encoding manually. For this reason, the ENCODING statement is removed during migration.

### Grammar Syntax

Copy code

```
:force:
ENCODING ( <storage_directive> [, ...] )
```

### Sample Source

#### Input Code:

##### Greenplum

Copy code

```
:force:
CREATE TABLE TABLE1 (
   COL1 integer ENCODING (compresstype = quicklz, blocksize = 65536)
);
```

#### Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

## DISTRIBUTED BY

Note

:class: tip
This syntax is fully supported in Snowflake.

The DISTRIBUTED BY clause in Greenplum controls how table data is physically distributed across the system’s segments. Meanwhile, CLUSTER BY is a subset of columns in a table (or expressions on a table) that are explicitly designated to co-locate the data in the table in the same micro-partitions.

### Grammar Syntax

Copy code

```
:force:
DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
```

### Sample Source Patterns

#### Input Code:

##### Greenplum

Copy code

```
:force:
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
DISTRIBUTED BY (colum1, colum2);
```

#### Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
--** SSC-FDM-GP0001 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF DISTRIBUTED BY **
CLUSTER BY (colum1, colum2)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

## DISTRIBUTED RANDOMLY - REPLICATED

Note

This syntax is not needed in Snowflake.

The DISTRIBUTED REPLICATED or DISTRIBUTED RANDOMLY clause in Greenplum controls how table data is physically distributed across the system’s segments. As Snowflake automatically handles data storage, these options will be removed in the migration.

### Grammar Syntax

Copy code

```
:force:
DISTRIBUTED RANDOMLY | DISTRIBUTED REPLICATED
```

### Sample Source Patterns

#### Input Code:

##### Greenplum

Copy code

```
:force:
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
DISTRIBUTED RANDOMLY;
```

#### Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

## Related EWIs

1. [SSC-FDM-GP0001](../../../../issues-and-troubleshooting/functional-difference/greenplumFDM#ssc-fdm-gp0001): The performance of the CLUSTER BY may vary compared to the performance of Distributed By.
