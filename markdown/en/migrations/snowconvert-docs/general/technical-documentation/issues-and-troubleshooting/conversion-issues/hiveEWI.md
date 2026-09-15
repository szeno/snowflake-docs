# Code Conversion - Hive Issues

Note

**Conversion Scope**

For Hive, the assessment and translation capabilities primarily focus on TABLES and VIEWS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

This page provides a comprehensive reference for how Hive grammar elements are translated to Snowflake equivalents. In this translation reference, you will find code examples, functional equivalence results, key differences, recommendations, known issues, and descriptions of each transformation.

## SSC-EWI-HV0001

The ROW FORMAT clause is not supported in Snowflake

### Severity

Medium

#### Description

This EWI is added when a ROW FORMAT statement is encountered.

#### Code Example

**Input Code:**

##### Hive

Copy code

```
 CREATE TABLE parquet_table (
id INT, data STRING
)
 ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' COLLECTION ITEMS TERMINATED BY ';' MAP KEYS TERMINATED BY ':' LINES TERMINATED BY '\n' NULL DEFINED AS 'NULL_VALUE';
```

**Generated Code:**

##### Snowflake

Copy code

```
 CREATE TABLE parquet_table (
 id INT,
 data STRING
)
!!!RESOLVE EWI!!! /*** SSC-EWI-HV0001 - THE ROW FORMAT CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' ESCAPED BY '\\'
COLLECTION ITEMS TERMINATED BY ';'
MAP KEYS TERMINATED BY ':'
LINES TERMINATED BY '\n'
NULL DEFINED AS 'NULL_VALUE'
;
```
