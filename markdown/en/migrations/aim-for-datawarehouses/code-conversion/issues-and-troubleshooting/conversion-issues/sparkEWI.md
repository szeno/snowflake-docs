# Code Conversion - Spark Issues

Note

Conversion Scope

For Spark SQL, the assessment and translation capabilities primarily focus on TABLES and VIEWS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

This page provides a comprehensive reference for how Spark grammar elements are translated to Snowflake equivalents. In this translation reference, you will find code examples, functional equivalence results, key differences, recommendations, known issues, and descriptions of each transformation.

## SSC-EWI-SPK0001

CREATE TABLE without columns is not supported in Snowflake

### Severity

Medium

#### Description

This EWI is added when a `CREATE TABLE` statement is encountered without column definitions.

#### Code Example

**Input Code:**

##### Spark

Copy code

```
 CREATE TABLE table_name1;
```

**Output Code:**

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-SPK0001 - CREATE TABLE WITHOUT COLUMNS IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE TABLE table_name1;
```
