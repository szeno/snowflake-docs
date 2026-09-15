# Code Conversion - BigQuery Issues

Note

**Conversion Scope**

For Google BigQuery, assessment and translation for TABLES and VIEWS are currently supported. Although other types of statements are recognized, they are not fully supported.

This page provides a comprehensive reference for how Google BigQuery grammar elements to Snowflake equivalents are translated. In this translation reference, you will find code examples, functional equivalence results, key differences, recommendations, known issues, and descriptions of each transformation.

## SSC-EWI-BQ0001

Snowflake does not support the options clause.

Warning

This EWI is deprecated; please refer to [SSC-EWI-0016](generalEWI#ssc-ewi-0016) for the latest version of this EWI.

### Severity

Medium

#### Description

This EWI is added to DDL statements when the `OPTIONS` has unsupported options by Snowflake.

#### Code Example

**Input Code:**

##### BigQuery

Copy code

```
 CREATE VIEW my_view
OPTIONS (
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
) AS
SELECT column1, column2
FROM my_table;
```

**Output Code:**

##### Snowflake

Copy code

```
 CREATE VIEW my_view
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: EXPIRATION_TIMESTAMP, PRIVACY_POLICY ***/!!!
OPTIONS(
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/26/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
  my_table;
```

##### Recommendations

- Add manual changes to the not-transformed expression.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0002

Micro-partitioning is automatically performed on all Snowflake tables.

Note

This issue is deprecated and no longer generated

### Severity

Medium

#### Description

This warning is added to the Create table when the partition by clause is present. `PARTITION BY` is an optional clause that controls [table partitioning](https://cloud.google.com/bigquery/docs/partitioned-tables) but is not supported in Snowflake.

All data in Snowflake tables is automatically divided into micro-partitions, which are contiguous units of storage. Each micro-partition contains between 50 MB and 500 MB of uncompressed data. This size and structure allows for extremely granular pruning of very large tables, which can be comprised of millions, or even hundreds of millions, of micro-partitions.

Snowflake stores metadata about all rows stored in a micro-partition, including:

- The range of values for each of the columns in the micro-partition.
- The number of distinct values.
- Additional properties used for both optimization and efficient query processing.

Also the tables are transparently partitioned using the ordering of the data as it is inserted/loaded. For more information please refer to [Benefits of Micro-partitioning](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions#benefits-of-micro-partitioninghttps://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions#benefits-of-micro-partitioning).

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE TABLE table1(
    transaction_id INT,
    transaction_date DATE
)
PARTITION BY transaction_date;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (
    transaction_id INT,
  transaction_date DATE
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0002 - MICRO-PARTITIONING IS AUTOMATICALLY PERFORMED ON ALL SNOWFLAKE TABLES. ***/!!!
PARTITION BY transaction_date
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}';
```

#### Recommendations

- No additional user actions are required, it is just informative.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0003

Pending translation for differential privacy.

### Severity

Medium

#### Description

BigQuery allows applying [differential privacy](https://cloud.google.com/bigquery/docs/differential-privacy#what_is_differential_privacy) over some statistical functions to introduce noise in the data, making it difficult to extract information about individuals when analyzing query results.

Snowflake now supports [differential privacy](/user-guide/diff-privacy/differential-privacy-overview) natively. However, the translation for this feature has not yet been implemented. Any use of differential privacy in BigQuery will be commented out and this issue will be generated to flag the need for manual conversion.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=2, privacy_unit_column=id)
    item,
    COUNT(quantity, contribution_bounds_per_group => (0,100)) total_quantity
FROM professors
GROUP BY item;
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0003 - PENDING SNOWCONVERT AI TRANSLATION FOR DIFFERENTIAL PRIVACY. ***/!!!
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=2, privacy_unit_column=id)
    item,
    COUNT(quantity,
                    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0003 - PENDING SNOWCONVERT AI TRANSLATION FOR DIFFERENTIAL PRIVACY. ***/!!! contribution_bounds_per_group => (0,100)) total_quantity
FROM
  professors
GROUP BY item;
```

#### Recommendations

1. **Use native Snowflake support:** Snowflake now supports [differential privacy](/user-guide/diff-privacy/differential-privacy-overview) natively. Rewrite the BigQuery differential privacy syntax using Snowflake’s privacy policies and privacy budgets.
2. **Key differences:** Snowflake’s differential privacy implementation uses privacy policies assigned to tables/views, privacy budgets to manage analyst queries, and privacy domains for fact and dimension columns. The syntax differs from BigQuery’s inline `WITH DIFFERENTIAL_PRIVACY` clause.
3. **Further reading:** [Snowflake Differential Privacy Overview](/user-guide/diff-privacy/differential-privacy-overview)

## SSC-EWI-BQ0004

Snowflake does not support named windows.

### Severity

Medium

#### Description

BigQuery allows the definition and usage of named windows in aggregate functions, they are defined in the `WINDOW` clause of the query they are used and can be used inside the `OVER` clause of these functions.

Snowflake does not support declaring named windows, please consider taking the window definition and apply it to all usages of that window directly in the `OVER` clause of the functions.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT
    COUNT(col1) OVER(myWindow)
FROM
    test.exampleTable
WINDOW
    myWindow AS (ORDER BY col2);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
    COUNT(col1)
    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0004 - SNOWFLAKE DOES NOT SUPPORT NAMED WINDOWS. ***/!!! OVER(myWindow)
FROM
    test.exampleTable
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0004 - SNOWFLAKE DOES NOT SUPPORT NAMED WINDOWS. ***/!!!
WINDOW
    myWindow AS (ORDER BY col2);
```

#### Recommendations

- Review your named window definitions, it might be possible to take the definition and apply it to the `OVER` clause of the functions it is used in. However, keep in mind the functional differences between BigQuery and Snowflake window frames still apply, take the following case as an example:

BigQuery:

Copy code

```
 SELECT
    COUNT(col1) OVER(myWindow)
FROM
    test.exampleTable
WINDOW
    myWindow AS (ORDER BY col2);
```

Snowflake:

Copy code

```
 SELECT
    COUNT(col1) OVER(ORDER BY col2)
FROM
    test.exampleTable;
```

These two queries will produce the same rows but the Snowflake results will not be ordered, this is because the `ORDER BY` clause for window frames does **not** impact the entire query ordering as it does in BigQuery.

## SSC-EWI-BQ0005

Javascript code has not been validated.

### Severity

High

### Description

Javascript code does not get transformed. Since the Javascript code extracted from BigQuery’s functions hasn’t been changed at all, this code might need some tweaks to work on Snowflake.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE FUNCTION test.languageJs (x integer, y integer)
RETURNS integer
LANGUAGE js
AS "return x * y;";
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE FUNCTION test.languageJs (x integer, y integer)
RETURNS DOUBLE
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0005 - JAVASCRIPT CODE HAS NOT BEEN VALIDATED BY SNOWCONVERT AI. ***/!!!
AS
$$
return x * y;
$$;
```

#### Recommendations

- Review all Javascript code before deployment.
- Javascript parameters in Snowflake must be uppercase.
- For more information, visit Snowflake’s [Introduction to Javascript UDFs](/developer-guide/udf/javascript/udf-javascript-introduction).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0006

Oriented parameter in the ST\_GEOGFROMTEXT function is not supported in Snowflake.

### Severity

Low

#### Description

This warning is added when the oriented parameter is specified in the [`ST_GEOGFROMTEXT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) function, because it is not supported in Snowflake. If this parameter is set to TRUE, any polygon in the input is assumed to be oriented as follows: if someone walks along the polygon boundary in the order of the input vertices, the interior of the polygon is to the left. This allows WKT to represent polygons larger than a hemisphere. If oriented is FALSE or omitted, this function returns the polygon with the smallest area.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', TRUE);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0006 - ORIENTED PARAMETER IN THE ST_GEOGFROMTEXT FUNCTION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
 ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
```

#### Recommendations

1. **Review polygon orientation:** If the `oriented` parameter was set to `TRUE`, verify that the polygon does not span more than a hemisphere. Snowflake’s `ST_GEOGFROMTEXT` always returns the polygon with the smallest area.
2. **Manual validation:** For polygons larger than a hemisphere, consider splitting them into smaller polygons or using alternative geospatial representations.
3. **Remove the parameter:** After manual review, remove the `oriented` parameter from the function call, as Snowflake’s `ST_GEOGFROMTEXT` accepts only the WKT string argument.

## SSC-EWI-BQ0007

Escape Sequence is not valid in Snowflake.

### Severity

Low

#### Description

Bell character (\a) and Vertical character (\v) are valid escape sequences in BigQuery, but not in Snowflake.

This warning is added when a bell character or vertical character escape sequence is found when translating BigQuery code. For more information, see [BigQuery Escape Sequences](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#escape_sequences).

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT "\a";
SELECT "\v";
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0007 - ESCAPE SEQUENCE \a IS NOT VALID IN SNOWFLAKE. ***/!!!
    '\a';
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0007 - ESCAPE SEQUENCE \v IS NOT VALID IN SNOWFLAKE. ***/!!!
    '\v';
```

#### Recommendations

1. **Replace with Unicode escapes:** Replace `\a` (bell character, U+0007) with `\x07` and `\v` (vertical tab, U+000B) with `\x0B`, which are supported by Snowflake.
2. **Review usage:** If the escape sequence was used for formatting purposes, consider whether it is still needed in the Snowflake context.

## SSC-EWI-BQ0008

Eight hex digit Unicode escape sequence is not supported in Snowflake.

### Severity

Low

#### Description

BigQuery supports Unicode sequences of 8 hex digits. Snowflake doesn’t support this kind of Unicode sequences.

This warning is added when an 8 hex digits Unicode sequence is found when translating BigQuery code. More about [BigQuery Escape Sequences](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#escape_sequences).

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT "\U00100000";
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0008 - EIGHT HEX DIGIT UNICODE ESCAPE SEQUENCE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
    '\U00100000';
```

#### Recommendations

1. **Use surrogate pairs:** Convert the 8-hex-digit Unicode sequence into two 4-hex-digit surrogate pair sequences. For example, `\U00100000` can be represented using surrogate pairs `\uDBC0\uDC00`.
2. **Use CHR function:** Alternatively, use Snowflake’s `CHR` function with the Unicode code point to generate the character at runtime.

## SSC-EWI-BQ0009

The correct return table clause was unabled to be generated. Missing symbol information.

### Severity

High

#### Description

Snowflake requires a valid RETURNS TABLE clause for CREATE TABLE FUNCTION statements. A new one has to be built from the ground up. To do this, an analysis is made on the CREATE TABLE FUNCTION query in order to properly infer the types of the columns of the resulting table. However there may be scenarios where there is currently a limitation to be able to build the return clause properly.

These scenarios will be considered in the future, but in the meantime this error will be added.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE TABLE FUNCTION tableValueFunction2()
AS
SELECT *
REPLACE("John" AS employee_name)
FROM employees;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE FUNCTION tableValueFunction2 ()
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0009 - SNOWCONVERT AI WAS UNABLE TO GENERATE THE CORRECT RETURN TABLE CLAUSE. MISSING SYMBOL INFORMATION. ***/!!!
RETURNS TABLE (
)
AS
  $$
      SELECT
        * REPLACE("John" AS employee_name) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ExceptReplaceOperator' NODE ***/!!!
      FROM
        employees
  $$;
```

#### Recommendations

1. **Manually define the RETURNS TABLE clause:** Inspect the original BigQuery TABLE FUNCTION body to determine the column names and types of the result set, then populate the empty `RETURNS TABLE()` clause with the correct column definitions.
2. **Provide source references:** If the issue is caused by missing references, ensure all referenced tables and views are included.

## SSC-EWI-BQ0010

The resulting table has no columns

### Severity

Medium

#### Description

This EWI is added when an external table whose definition has no columns is created. External tables in BigQuery can be defined using only OPTIONS (e.g., FORMAT and URIS) without explicit column definitions, relying on schema inference. When the resulting table structure has no columns after conversion, this EWI is emitted to flag that manual definition of the table schema may be required.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE EXTERNAL TABLE my_dataset.sensor_readings
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://my_bucket/sensors/*.parquet']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0010 - THE RESULTING TABLE HAS NO COLUMNS ***/!!!
CREATE EXTERNAL TABLE my_dataset.sensor_readings
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://my_bucket/sensors/*.parquet']
);
```

#### Recommendations

1. **Provide column definitions:** If the source BigQuery external table uses inferred schema, manually add the expected column definitions to the generated Snowflake external table based on the actual file structure.
2. **Use INFER\_SCHEMA:** Consider using Snowflake’s [INFER\_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) function with a sample file path (without wildcards) to generate the table template.
3. **Include table definitions:** Ensure all referenced table or view definitions are included so that symbol information can be collected.

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0011

Session variable assignment of complex datatype is not supported in Snowflake

### Severity

Medium

#### Description

In BigQuery, declaring a variable at script level allows it to be used in the entire script, to replicate this behavior in Snowflake [SQL variables](https://docs.snowflake.com/en/sql-reference/session-variables) are used.

However, declaring variables of datatypes that are complex like ARRAY, GEOGRAPHY, STRUCT or JSON will fail in Snowflake when trying to set the value to the SQL variable. When one of such cases is detected then this is EWI will be added to the SQL variable declaration.

Variables of these types can be declared without problems inside block statements and other procedural statements, this EWI applies only for variables declared at script level.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE TABLE test.JsonTable
(
    col1 JSON
);

DECLARE myVar1 JSON DEFAULT JSON'{"name": "John", "age": 30}';

INSERT INTO test.JsonTable VALUES (myVar1);

BEGIN
    DECLARE myVar2 JSON DEFAULT JSON'{"name": "Mike", "age": 27}';
    INSERT INTO test.JsonTable VALUES (myVar2);
END;

SELECT col1 FROM test.JsonTable;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE test.JsonTable
(
    col1 VARIANT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}';

!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0011 - SESSION VARIABLE ASSIGNMENT OF COMPLEX DATATYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
SET myVar1 = (
    SELECT
        PARSE_JSON('{"name": "John", "age": 30}')
);

INSERT INTO test.JsonTable
VALUES ($myVar1);

BEGIN
    LET myVar2 VARIANT DEFAULT PARSE_JSON('{"name": "Mike", "age": 27}');
    INSERT INTO test.JsonTable
    VALUES (:myVar2);
END;

SELECT col1 FROM
    test.JsonTable;
```

#### Recommendations

- If the uses of the variable are limited to a single scope or its value is never modified, consider declaring the variable locally in the scopes that use it, that will solve the issue.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0012

A correct OBJECT\_CONSTRUCT parameter was unable to be generated. Missing symbol information.

### Severity

High

#### Description

A correct `OBJECT_CONSTRUCT` parameter was unabled to be generated due to missing symbol information. This typically occurs when the table definition is not included, or when the table uses complex types (such as `STRUCT`) whose field names are needed to build the `OBJECT_CONSTRUCT` call.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 INSERT INTO test.tuple_sample
VALUES
  ((12, 34)),
  ((56, 78)),
  ((9, 99)),
  ((12, 35));
```

##### Generated Code:

##### Snowflake

Copy code

```
 INSERT INTO test.tuple_sample
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0012 - SNOWCONVERT AI WAS UNABLE TO GENERATE A CORRECT OBJECT_CONSTRUCT PARAMETER. MISSING SYMBOL INFORMATION. ***/!!!
VALUES
  ((12, 34)),
  ((56, 78)),
  ((9, 99)),
  ((12, 35));
```

#### Recommendations

1. **Provide table definitions:** Ensure all referenced table definitions (CREATE TABLE statements) are included so that symbol information can be collected.
2. **Manual replacement:** Inspect the original BigQuery INSERT statement and manually construct the `OBJECT_CONSTRUCT` call with the correct field names and values matching the target table’s schema.

## SSC-EWI-BQ0013

External table data format not supported in snowflake

Warning

This EWI is deprecated; please refer to [SSC-EWI-0029](generalEWI#ssc-ewi-0029) for the latest version of this EWI.

### Severity

Medium

#### Description

Snowflake supports the following BigQuery formats:

| BigQuery | Snowflake |
| --- | --- |
| AVRO | AVRO |
| CSV GOOGLE\_SHEETS | CSV |
| NEWLINE\_DELIMITED\_JSON JSON | JSON |
| ORC | ORC |
| PARQUET | PARQUET |

Expand

Show lessSee more

When an external table has other FORMAT not specified in the above table, this EWI will be generated to inform the user that the FORMAT is not supported.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table
OPTIONS (
  format = 'DATASTORE_BACKUP',
  uris = ['gs://backup_bucket/backup_folder/*']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0013 - EXTERNAL TABLE DATA FORMAT NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table
OPTIONS (
  format = 'DATASTORE_BACKUP',
  uris = ['gs://backup_bucket/backup_folder/*']
);
```

#### Recommendations

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0014

Hive partitioned external tables are not supported in Snowflake

### Severity

Medium

#### Description

Snowflake does not support hive partitioned external tables, when the WITH PARTITION COLUMNS clause is found in the external table, it will be marked as not supported using this EWI.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE EXTERNAL TABLE test.CustomHivePartitionedTable
WITH PARTITION COLUMNS (
  field_1 STRING,
  field_2 INT64)
OPTIONS (
  uris = ['gs://sc_external_table_bucket/folder_with_parquet/*'],
  format = 'PARQUET',
  hive_partition_uri_prefix = 'gs://sc_external_table_bucket/folder_with_parquet',
  require_hive_partition_filter = false);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_CUSTOMHIVEPARTITIONEDTABLE_FORMAT
TYPE = PARQUET;

CREATE EXTERNAL TABLE test.CustomHivePartitionedTable USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-0035 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_CUSTOMHIVEPARTITIONEDTABLE_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0014 - HIVE PARTITIONED EXTERNAL TABLES ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
WITH PARTITION COLUMNS (
  field_1 STRING,
  field_2 INT64)
PATTERN = 'folder_with_parquet/.*'
FILE_FORMAT = (TYPE = PARQUET)
!!!RESOLVE EWI!!! /*** SSC-EWI-0016 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: HIVE_PARTITION_URI_PREFIX, REQUIRE_HIVE_PARTITION_FILTER. ***/!!!
OPTIONS(
  hive_partition_uri_prefix = 'gs://sc_external_table_bucket/folder_with_parquet',
  require_hive_partition_filter = false
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}';
```

#### Recommendations

1. **Remove the WITH PARTITION COLUMNS clause:** Snowflake external tables use automatic partitioning based on the file path. Remove the `WITH PARTITION COLUMNS` clause from the generated code.
2. **Use Snowflake partitioning:** Define partition columns using expressions in the external table’s column definitions. Snowflake can automatically infer partition columns from the directory structure.
3. **Hive metastore integration:** If you use a Hive metastore, consider integrating it with Snowflake to synchronize external table metadata automatically.

## SSC-EWI-BQ0015

External table requires an external stage to access an external location, define and replace the EXTERNAL\_STAGE placeholder

Warning

This EWI is deprecated; please refer to [SSC-EWI-0032](generalEWI#ssc-ewi-0032) for the latest version of this EWI.

### Description

When transforming the CREATE EXTERNAL TABLE statement, an EXTERNAL\_STAGE placeholder will be generated that has to be replaced with the external stage created for connecting with the external location from Snowflake.

Please refer to the following guides to set up the necessary Storage Integration and External Stage in your Snowflake account:

- [For external tables referencing Amazon S3](https://docs.snowflake.com/en/user-guide/tables-external-s3)
- [For external tables referencing Google Cloud Storage](https://docs.snowflake.com/en/user-guide/tables-external-gcs)
- [For external tables referencing Azure Blob Storage](https://docs.snowflake.com/en/user-guide/tables-external-azure)

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER,
  Name STRING,
  Mail STRING,
  Position STRING,
  Salary INTEGER
)
OPTIONS(
  FORMAT='CSV',
  SKIP_LEADING_ROWS=1,
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Employees.csv']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER AS CAST(GET_IGNORE_CASE($1, 'c1') AS INTEGER),
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c2') AS STRING),
  Mail STRING AS CAST(GET_IGNORE_CASE($1, 'c3') AS STRING),
  Position STRING AS CAST(GET_IGNORE_CASE($1, 'c4') AS STRING),
  Salary INTEGER AS CAST(GET_IGNORE_CASE($1, 'c5') AS INTEGER)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Employees.csv'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER =1);
```

#### Recommendations

- Set up your external connection in the Snowflake account and replace the EXTERNAL\_STAGE placeholder to complete the transformation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-BQ0016

Select \* with multiple UNNEST operators will produce column ambiguity

Warning

This EWI is deprecated; please refer to [SSC-FDM-BQ0012](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0012) for the latest version of this issue. The description and examples below are kept for historical reference and may not match current SnowConvert AI output.

### Severity

Medium

#### Description

As part of the SnowConvert transformation for the UNNEST operator, the [FLATTEN](/sql-reference/functions/flatten) function is used, this function generates multiple columns not required to emulate the UNNEST operator functionality like the `THIS` or `PATH` columns.

When a SELECT \* with the UNNEST operator is found, SnowConvert will remove the unnecessary columns using the `EXCLUDE` keyword, however, when multiple UNNEST operators are used in the same statement, the columns can not be removed due to ambiguity problems, this EWI will be generated to mark these cases.

It is recommended to expand the SELECT expression list in order to specify only the expected columns and solve this issue.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT * FROM UNNEST ([10,20,30]);

SELECT * FROM UNNEST ([10,20,30]) AS numbers, UNNEST(['Hi', 'Hello', 'Bye']) AS words;
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
* EXCLUDE(SEQ, KEY, PATH, THIS, INDEX)
FROM
TABLE(FLATTEN(INPUT => [10,20,30])) AS F0_ (
SEQ,
KEY,
PATH,
INDEX,
F0_,
THIS
);

SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0016 - SELECT * WITH MULTIPLE UNNEST OPERATORS WILL RESULT IN COLUMN AMBIGUITY IN SNOWFLAKE ***/!!!
 * FROM
TABLE(FLATTEN(INPUT => [10,20,30])) AS numbers (
SEQ,
KEY,
PATH,
INDEX,
numbers,
THIS
),
TABLE(FLATTEN(INPUT => ['Hi', 'Hello', 'Bye'])) AS words (
SEQ,
KEY,
PATH,
INDEX,
words,
THIS
);
```

## SSC-EWI-BQ0017

Pending translation for UNNEST of an array of structs

### Severity

Medium

#### Description

When unnesting an array of structs, BigQuery generates a column for each struct field and splits the struct values into their corresponding columns. This transformation is not yet supported. Whenever it is detected that the UNNEST operator is applied over an array of structs, this EWI is generated to flag the need for manual conversion.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE TABLE test.myTestTable
(
  column1 ARRAY<STRUCT<x INT64, y STRING, z STRUCT<a INT64, b INT64>>>
);

SELECT structValues FROM test.myTestTable AS someTable, UNNEST(someTable.column1) AS structValues;
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE test.myTestTable
(
  column1 ARRAY DEFAULT []
);

SELECT structValues FROM
  test.myTestTable AS someTable,
  !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0017 - PENDING SNOWCONVERT AI TRANSLATION FOR UNNEST OF AN ARRAY OF STRUCTS ***/!!! UNNEST(someTable.column1) AS structValues;
```

#### Recommendations

1. **Use FLATTEN with LATERAL:** Manually flatten the array column using Snowflake’s [FLATTEN](/sql-reference/functions/flatten) function, then extract individual struct fields using dot notation or `GET` on the `VALUE` column.
2. **Example workaround:**

   Copy code

   ```
   SELECT f.VALUE:x::INT64 AS x, f.VALUE:y::STRING AS y
   FROM test.myTestTable AS t, LATERAL FLATTEN(INPUT => t.column1) AS f;
   ```

## SSC-EWI-BQ0018

BigQuery PARSE\_TIMESTAMP timezone argument is not natively supported in Snowflake; wrapped with CONVERT\_TIMEZONE.

### Severity

Medium

#### Description

BigQuery’s [PARSE\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp) accepts an optional third argument that specifies the time zone in which the input string should be interpreted. Snowflake’s [TO\_TIMESTAMP\_TZ](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp) does not have an equivalent argument.

To preserve the source semantics, the value is parsed as `TO_TIMESTAMP_NTZ`, then wraps the result with [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) to shift it from the supplied zone to UTC, and finally casts the value to `TIMESTAMP_TZ`. This EWI is added to flag the rewrite so the user can verify the time zone being passed in matches the originally intended semantics.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', '2024-12-25 14:30:00', 'America/New_York');
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
CONVERT_TIMEZONE('America/New_York', 'UTC', TO_TIMESTAMP_NTZ('2024-12-25 14:30:00', 'YYYY-MM-DD HH24:MI:SS')) :: TIMESTAMP_TZ !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0018 - BIGQUERY PARSE_TIMESTAMP TIMEZONE ARGUMENT IS NOT NATIVELY SUPPORTED IN SNOWFLAKE; WRAPPED WITH CONVERT_TIMEZONE. ***/!!!;
```

#### Recommendations

1. **Verify the timezone semantics match.** BigQuery interprets the input string as a wall-clock time in the supplied zone and stores the result as a UTC instant. The generated `CONVERT_TIMEZONE(<tz>, 'UTC', TO_TIMESTAMP_NTZ(...))` rewrite reproduces that semantic. Confirm the timezone identifier supplied is one Snowflake understands (see [Supported time zones](https://docs.snowflake.com/en/sql-reference/parameters#timezone)).
2. **Consider session timezone.** If the application logic depends on the session’s `TIMEZONE` parameter, set it explicitly with `ALTER SESSION SET TIMEZONE = 'UTC'` (or the appropriate value) before running the converted query.

## SSC-EWI-BQ0019

\_TABLE\_SUFFIX is a BigQuery wildcard-table pseudo-column with no Snowflake equivalent; rewrite the query against a single table with an explicit suffix/date column.

### Severity

High

#### Description

BigQuery exposes `_TABLE_SUFFIX` when querying wildcard tables so a query can filter the matched table names. Snowflake has no wildcard-table pseudo-column, so SnowConvert AI preserves the reference and adds this EWI for manual replacement with an explicit suffix or date column.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT *
FROM events
WHERE _TABLE_SUFFIX BETWEEN '20260101' AND '20260131';
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT * FROM events WHERE !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0019 - '_TABLE_SUFFIX' IS A BIGQUERY WILDCARD-TABLE PSEUDO-COLUMN WITH NO SNOWFLAKE EQUIVALENT. SNOWFLAKE HAS NO WILDCARD TABLES; REWRITE THE QUERY AGAINST A SINGLE TABLE USING AN EXPLICIT FILTER COLUMN. ***/!!! _TABLE_SUFFIX BETWEEN '20260101' AND '20260131';
```

#### Best Practices

1. Replace wildcard-table access with a single Snowflake table and filter on an explicit suffix or date column.

## SSC-EWI-BQ0020

\_PARTITIONDATE/\_PARTITIONTIME is a BigQuery ingestion-time partition pseudo-column with no Snowflake equivalent; reference an explicit partition column instead.

### Severity

Medium

#### Description

BigQuery exposes `_PARTITIONDATE` and `_PARTITIONTIME` for filtering ingestion-time partitioned tables. Snowflake manages micro-partitions automatically and does not expose either pseudo-column, so SnowConvert AI preserves the reference and adds this EWI for replacement with an explicit partition column.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT * FROM mydata WHERE _PARTITIONDATE = CURRENT_DATE();
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT * FROM mydata WHERE !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0020 - '_PARTITIONDATE' IS A BIGQUERY INGESTION-TIME PARTITION PSEUDO-COLUMN WITH NO SNOWFLAKE EQUIVALENT. SNOWFLAKE MANAGES MICRO-PARTITIONS AUTOMATICALLY; REWRITE THE QUERY TO REFERENCE AN EXPLICIT PARTITION COLUMN. ***/!!! _PARTITIONDATE = CURRENT_DATE();
```

#### Best Practices

1. Persist the required partition date or timestamp in an explicit column and rewrite predicates to reference it.

## SSC-EWI-BQ0021

ST\_MAKELINE with an array of geographies is not supported in Snowflake; rewrite using an aggregation such as ST\_COLLECT.

### Severity

Medium

#### Description

BigQuery accepts an array of geographies as a single `ST_MAKELINE` argument. Snowflake accepts only two geography arguments, so SnowConvert AI preserves the unsupported array form and adds this EWI for manual rewriting, such as with `ST_COLLECT`.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_MAKELINE([g1, g2, g3]) FROM segments;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  ST_MAKELINE([g1, g2, g3]) !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0021 - ST_MAKELINE WITH AN ARRAY ARGUMENT IS NOT SUPPORTED IN SNOWFLAKE. SNOWFLAKE'S ST_MAKELINE ACCEPTS ONLY TWO GEOGRAPHY ARGUMENTS; REWRITE USING AN AGGREGATION SUCH AS ST_COLLECT. ***/!!!
FROM
  segments;
```

#### Best Practices

1. Rewrite the array form with a supported aggregation such as `ST_COLLECT`, then validate the resulting geography.

## SSC-EWI-BQ0022

Multi-column (tuple) UNPIVOT is not supported in Snowflake.

### Severity

Medium

#### Description

BigQuery can unpivot tuples of multiple value columns in one `UNPIVOT` operation. Snowflake supports only a single value column per operation, so SnowConvert AI preserves the tuple form and adds this EWI for manual decomposition into single-column operations or `LATERAL FLATTEN`.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT * FROM produce
UNPIVOT((sales, quantity) FOR quarter IN ((q1_sales, q1_quantity) AS 'Q1'));
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  *
FROM
  produce !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0022 - MULTI-COLUMN (TUPLE) UNPIVOT IS NOT SUPPORTED IN SNOWFLAKE. REWRITE USING MULTIPLE SINGLE-COLUMN UNPIVOTS OR A LATERAL FLATTEN. ***/!!!
  UNPIVOT((sales, quantity) FOR quarter IN ((q1_sales, q1_quantity) AS 'Q1'));
```

#### Best Practices

1. Split the tuple into single-column `UNPIVOT` operations or use `LATERAL FLATTEN`.

## SSC-EWI-BQ0023

ST\_GEOGFROMGEOJSON ‘make\_valid’ parameter is not supported in Snowflake and was not translated.

### Severity

High

#### Description

BigQuery’s `ST_GEOGFROMGEOJSON` can use a second `make_valid` argument to repair invalid polygon data. Snowflake has no equivalent argument or geometry-repair function, so SnowConvert AI leaves the two-argument call unchanged and adds this EWI for manual review.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_GEOGFROMGEOJSON(json_str, TRUE) FROM tbl;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  ST_GEOGFROMGEOJSON(json_str, TRUE) !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0023 - THE 'MAKE_VALID' PARAMETER OF ST_GEOGFROMGEOJSON IS NOT SUPPORTED IN SNOWFLAKE. THERE IS NO EQUIVALENT GEOMETRY REPAIR FUNCTION. REVIEW THE CALL MANUALLY. ***/!!!
FROM
  tbl;
```

#### Best Practices

1. Validate or repair GeoJSON before calling the Snowflake function and review invalid-geometry handling.

## SSC-EWI-BQ0024

ST\_BUFFER converted using only its first two arguments; the dropped options and Snowflake’s planar GEOMETRY (vs BigQuery’s geodesic GEOGRAPHY) may change the result.

### Severity

Medium

#### Description

BigQuery’s `ST_BUFFER` accepts options beyond the geography and distance arguments, including segment count, spheroid use, endcap, and side. SnowConvert AI drops those extra arguments and emits Snowflake’s two-argument call, but the removed options and Snowflake’s planar `GEOMETRY` behavior can change the resulting shape.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_BUFFER(geog, 1000, 16) FROM tbl;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0024 - ST_BUFFER WAS CONVERTED USING ONLY ITS FIRST TWO ARGUMENTS; THE DROPPED OPTIONS (NUM_SEG_QUARTER_CIRCLE, USE_SPHEROID, ENDCAP, SIDE) AND SNOWFLAKE'S PLANAR GEOMETRY (VS BIGQUERY'S GEODESIC GEOGRAPHY) MAY CHANGE THE RESULT. ***/!!!
  ST_BUFFER(geog, 1000)
FROM
  tbl;
```

#### Best Practices

1. Compare representative buffer results and manually account for any dropped option that affects downstream geometry.

## SSC-EWI-BQ0025

Snowflake LIKE ANY/ALL requires a literal pattern list; the BigQuery UNNEST array is built at runtime.

### Severity

Medium

#### Description

BigQuery permits `LIKE ANY` and `LIKE ALL` to consume an array expanded by `UNNEST` at runtime. Snowflake requires a literal pattern list, so SnowConvert AI preserves the runtime-array form and adds this EWI because it cannot translate the expression directly.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT subscriber_id FROM customers
WHERE city LIKE ANY UNNEST(pattern_array);
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT subscriber_id FROM customers
WHERE !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0025 - SNOWFLAKE LIKE ANY/ALL REQUIRES A LITERAL PATTERN LIST; THE BIGQUERY UNNEST ARRAY IS BUILT AT RUNTIME AND CANNOT BE TRANSLATED DIRECTLY. ***/!!!
city LIKE ANY UNNEST(pattern_array) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'UNNEST' NODE ***/!!!;
```

#### Best Practices

1. Use a literal pattern list when possible, or rewrite runtime arrays with `FLATTEN` and an `EXISTS` predicate.

## SSC-EWI-BQ0026

MERGE WHEN NOT MATCHED BY SOURCE has no Snowflake equivalent; rewrite as a separate post-MERGE DELETE or UPDATE.

### Severity

Medium

#### Description

BigQuery `MERGE` supports `WHEN NOT MATCHED BY SOURCE` actions for target rows with no source match. Snowflake has no equivalent clause, so SnowConvert AI preserves it with this EWI and requires the `DELETE` or `UPDATE` to be implemented separately.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
MERGE target T USING source S ON T.id = S.id
WHEN MATCHED THEN UPDATE SET T.val = S.val
WHEN NOT MATCHED THEN INSERT (id, val) VALUES (S.id, S.val)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

##### Output Code:

##### Snowflake

Copy code

```
MERGE target T
USING source S ON T.id = S.id
WHEN MATCHED THEN
  UPDATE SET
    T.val = S.val
WHEN NOT MATCHED THEN
  INSERT (id, val)
  VALUES (S.id, S.val)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0026 - MERGE 'WHEN NOT MATCHED BY SOURCE' HAS NO SNOWFLAKE EQUIVALENT. REWRITE AS A SEPARATE POST-MERGE DELETE OR UPDATE STATEMENT. ***/!!!
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

#### Best Practices

1. Implement the source-only condition as a separate `DELETE` or `UPDATE` after the `MERGE` and test transaction semantics.

## SSC-EWI-BQ0027

A FOR loop record field referenced inside a SQL statement is not supported in Snowflake Scripting.

### Severity

Medium

#### Description

BigQuery permits a `FOR` loop record field to be referenced directly inside a SQL statement. Snowflake Scripting does not support that reference form, so SnowConvert AI adds this EWI where the field must first be assigned to a local variable and then bound with a colon.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
BEGIN
    FOR rec IN (SELECT id FROM users)
    DO
        INSERT INTO log VALUES(rec.id);
    END FOR;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
BEGIN
  LET rec_CURSOR_1 CURSOR
  FOR
    SELECT
      id
    FROM
      users;
  FOR rec IN rec_CURSOR_1 DO
    INSERT INTO log
    VALUES (
            !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0027 - A FOR LOOP RECORD FIELD REFERENCED INSIDE A SQL STATEMENT IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING. ASSIGN THE FIELD TO A LOCAL VARIABLE AND BIND THAT VARIABLE WITH A COLON INSIDE THE STATEMENT. ***/!!!
            rec.id);
  END FOR;
END;
```

#### Best Practices

1. Assign the record field to a local variable and use a colon-prefixed bind variable in the SQL statement.

## SSC-EWI-BQ0028

BigQuery’s DROP TABLE FUNCTION carries no signature, so the migrated DROP FUNCTION is emitted with empty parentheses; replace () with the parameter types if the source table-valued function declared parameters.

### Severity

Medium

#### Description

BigQuery’s `DROP TABLE FUNCTION` does not include a parameter signature. SnowConvert AI therefore emits empty parentheses, which Snowflake resolves only as a zero-argument overload; functions that declared parameters require their parameter types to be added manually.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
DROP TABLE FUNCTION mydataset.compute_sales;
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0028 - BIGQUERY'S DROP TABLE FUNCTION HAS NO SIGNATURE, SO THE MIGRATED DROP FUNCTION USES EMPTY PARENTHESES, WHICH SNOWFLAKE MATCHES ONLY TO THE ZERO-ARGUMENT OVERLOAD; IF THE SOURCE DECLARED PARAMETERS, REPLACE () WITH THEIR TYPES. ***/!!!
DROP FUNCTION mydataset.compute_sales ();
```

#### Best Practices

1. Replace the empty parentheses with the source function’s parameter types when dropping a non-zero-argument overload.

## SSC-EWI-BQ0029

BigQuery Python UDFs use a remote/containerized execution model with OPTIONS that are not supported in Snowflake.

### Severity

Medium

#### Description

BigQuery Python UDFs use a remote or containerized execution model configured through `OPTIONS`. Snowflake’s Python UDF model does not support those BigQuery execution options, so SnowConvert AI adds this EWI and requires the runtime configuration to be reviewed.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE FUNCTION test.pythonUdf (x INT64, y INT64)
RETURNS INT64
LANGUAGE python
AS """return x + 1;""";
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE FUNCTION test.pythonUdf (x INT, y INT)
RETURNS INT
LANGUAGE PYTHON
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0029 - BIGQUERY PYTHON UDFS USE A REMOTE/CONTAINERIZED EXECUTION MODEL WITH UNSUPPORTED OPTIONS IN SNOWFLAKE. ***/!!!
AS
$$
return x + 1;
$$;
```

#### Best Practices

1. Review the Python handler and replace unsupported BigQuery execution options with Snowflake-compatible configuration.

## SSC-EWI-BQ0030

Snowflake does not support a BigQuery CREATE AGGREGATE FUNCTION with a JavaScript or SQL body or the NOT AGGREGATE parameter modifier.

### Severity

High

#### Description

BigQuery aggregate functions can use JavaScript or SQL bodies and can mark parameters with `NOT AGGREGATE`. Snowflake aggregate functions require a Python handler and do not support that parameter modifier, so SnowConvert AI preserves the unsupported declaration with this EWI.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE AGGREGATE FUNCTION IF NOT EXISTS mydataset.jsScaledSum(x FLOAT64, factor FLOAT64 NOT AGGREGATE)
RETURNS INT64
LANGUAGE js
AS "return x;";
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0030 - SNOWFLAKE AGGREGATE FUNCTIONS SUPPORT ONLY A PYTHON HANDLER, NOT A JAVASCRIPT OR SQL BODY OR THE NOT AGGREGATE PARAMETER MODIFIER. ***/!!! AGGREGATE FUNCTION IF NOT EXISTS mydataset.jsScaledSum (x FLOAT, factor FLOAT)
RETURNS INT
LANGUAGE JAVASCRIPT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0005 - JAVASCRIPT CODE HAS NOT BEEN VALIDATED BY SNOWCONVERT AI. ***/!!!
AS
$$
return x;
$$;
```

#### Best Practices

1. Reimplement the aggregate function with a Snowflake Python handler and redesign any `NOT AGGREGATE` parameters.

## SSC-EWI-BQ0031

Snowflake CREATE FUNCTION does not support a TABLE type as an input parameter; TABLE(…) is allowed only in the RETURNS clause.

### Severity

High

#### Description

BigQuery table functions can declare a table type as an input parameter. Snowflake allows `TABLE(...)` only in a function’s `RETURNS` clause, so SnowConvert AI retains the rewritten table parameter and adds this EWI for redesigning the input.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE OR REPLACE TABLE FUNCTION inlineTableValuedFunction(
  orders TABLE<order_id INT64, item STRING>,
  item_name STRING)
RETURNS TABLE<year INT64, name STRING, total INT64>
AS (SELECT 2024 AS year, 'x' AS name, 1 AS total);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION inlineTableValuedFunction (
  orders !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0031 - SNOWFLAKE CREATE FUNCTION DOES NOT SUPPORT A TABLE TYPE AS AN INPUT PARAMETER; TABLE(...) IS ALLOWED ONLY IN THE RETURNS CLAUSE. THE PARAMETER WAS REWRITTEN TO TABLE(...). ***/!!! TABLE (
    order_id INT, item STRING
  ),
  item_name STRING)
RETURNS TABLE (year INT, name STRING, total INT)
AS
$$
  SELECT 2024 AS year, 'x' AS name, 1 AS total
$$;
```

#### Best Practices

1. Replace the table-valued input with scalar, array, or staged-table inputs supported by Snowflake functions.

## SSC-EWI-BQ0032

Remote functions are not supported in Snowflake. Use CREATE EXTERNAL FUNCTION with a pre-created API\_INTEGRATION as a workaround.

### Severity

Medium

#### Description

BigQuery remote functions use `REMOTE WITH CONNECTION` and an endpoint option. Snowflake does not support that syntax, so SnowConvert AI preserves it with this EWI; migrate the function to `CREATE EXTERNAL FUNCTION` with a pre-created API integration.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE FUNCTION mydataset.remote_udf(x INT64) RETURNS INT64
REMOTE WITH CONNECTION `myproject.us.my_connection`
OPTIONS (endpoint = 'https://example.com/api');
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE FUNCTION mydataset.remote_udf (x INT)
RETURNS INT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0032 - CREATE FUNCTION ... REMOTE WITH CONNECTION IS NOT SUPPORTED IN SNOWFLAKE. USE CREATE EXTERNAL FUNCTION WITH A PRE-CREATED API_INTEGRATION AS A WORKAROUND. ***/!!!
REMOTE WITH CONNECTION `myproject.us.my_connection`
OPTIONS(endpoint = 'https://example.com/api');
```

#### Best Practices

1. Create the required API integration and rewrite the function as a Snowflake external function.

## SSC-EWI-BQ0033

The ‘library’ OPTION for JavaScript UDFs has no Snowflake equivalent because Snowflake JavaScript UDFs cannot import external libraries.

### Severity

Medium

#### Description

BigQuery JavaScript UDFs can load external source files through the `library` option. Snowflake JavaScript UDFs cannot import external libraries, so SnowConvert AI comments out the option and adds this EWI while preserving the inline function body.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE FUNCTION mydataset.jsLibrary(x FLOAT64, y FLOAT64)
RETURNS FLOAT64
LANGUAGE js
OPTIONS(
    library=["gs://my-bucket/lib1.js"]
)
AS "return x * y;";
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE FUNCTION mydataset.jsLibrary (x FLOAT, y FLOAT)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
--!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0033 - THE 'LIBRARY' OPTION FOR JAVASCRIPT UDFS HAS NO SNOWFLAKE EQUIVALENT BECAUSE SNOWFLAKE JAVASCRIPT UDFS CANNOT IMPORT EXTERNAL LIBRARIES. ***/!!!
--library = ['gs://my-bucket/lib1.js']
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0005 - JAVASCRIPT CODE HAS NOT BEEN VALIDATED BY SNOWCONVERT AI. ***/!!!
AS
$$
return x * y;
$$;
```

#### Best Practices

1. Remove the external-library dependency or migrate the implementation to a supported Snowflake runtime and packaging model.
