# Code Conversion - BigQuery Functional Differences

Note

**Conversion Scope**

For Google BigQuery, assessment and translation for TABLES and VIEWS are currently supported. Although other types of statements are recognized, they are not fully supported.

## SSC-FDM-BQ0001

Accessing arrays produces NULL instead of an error for positive out of bounds indexes in Snowflake.

### Description

When accessing an ARRAY object by index in Snowflake, specifying an index greater than the size of the array will result in a NULL value, this differs with the behavior of BigQuery, where accessing an ARRAY with an index that is out of bounds will produce an error, unless the functions `SAFE_OFFSET` or `SAFE_ORDINAL` are used.

This FDM is added to any ARRAY access that is not safe.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 SELECT ([40, 12, 30])[8];

SELECT ([40, 12, 30])[SAFE_OFFSET(8)];
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
([40, 12, 30])[8];

SELECT
PUBLIC.SAFE_OFFSET_UDF( ([40, 12, 30]), 8);
```

#### Best Practices

- Analyze the uses of array access in the code. If there was never the risk of getting an out of bounds error in the original code, no difference will be observed and this FDM can be safely ignored.
- If the original code relies on out-of-bounds access raising an error (e.g., for flow control), add explicit bounds checking in Snowflake using `ARRAY_SIZE` before accessing the array.

## SSC-FDM-BQ0002

Exception system variables are not supported in Snowflake.

### Description

BigQuery’s [exception system variables](https://cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language#beginexceptionend) (`@@error.message`, `@@error.stack_trace`, `@@error.statement_text`, `@@error.formatted_stack_trace`) have no direct equivalent in Snowflake. Exception variable references are replaced with `OBJECT_CONSTRUCT('SQLERRM', SQLERRM, 'SQLCODE', SQLCODE, 'SQLSTATE', SQLSTATE)` as a workaround. This workaround provides basic error information but does not include stack trace or statement text details available in BigQuery. For more information, see [Handling Exceptions in Snowflake](/developer-guide/snowflake-scripting/exceptions).

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE PROCEDURE test.proc1()
BEGIN
  SELECT 1/0;
EXCEPTION WHEN ERROR THEN
  SELECT
    @@error.message as message,
    @@error.stack_trace as stack_trace,
    @@error.statement_text as statement_text,
    @@error.formatted_stack_trace as formatted_stack_trace;
END;
```

##### Result

Copy code

```
[
  {
    "message": "Query error: division by zero: 1 / 0 at [snowflake-snowconvert-team.test.proc1:2:3]",
    "stack_trace": [
      {
        "line": "2",
        "column": "3",
        "filename": null,
        "location": "snowflake-snowconvert-team.test.proc1"
      },
      {
        "line": "1",
        "column": "1",
        "filename": null,
        "location": null
      }
    ],
    "statement_text": "SELECT 1/0",
    "formatted_stack_trace": "At snowflake-snowconvert-team.test.proc1[2:3]\nAt [1:1]\n"
  }
]
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE test.proc1 ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}'
AS
$$
    BEGIN
    SELECT 1/0;
  EXCEPTION WHEN OTHER THEN
--      --** SSC-FDM-BQ0002 - EXCEPTION SYSTEM VARIABLES ARE NOT SUPPORTED IN SNOWFLAKE. **
--    SELECT
--      @@error.message as message,
--      @@error.stack_trace as stack_trace,
--      @@error.statement_text as statement_text,
--      @@error.formatted_stack_trace as formatted_stack_trace;
      RETURN OBJECT_CONSTRUCT('SQLERRM', SQLERRM, 'SQLCODE', SQLCODE, 'SQLSTATE', SQLSTATE);
    END;
$$;
```

##### Result

Copy code

```
{
  "SQLCODE": 100051,
  "SQLERRM": "Division by zero",
  "SQLSTATE": "22012"
}
```

#### Best Practices

- Snowflake provides three built-in exception variables as an alternative to BigQuery’s `@@error` system variables:

  | BigQuery Variable | Snowflake Equivalent | Notes |
  | --- | --- | --- |
  | `@@error.message` | `SQLERRM` | Error message text |
  | `@@error.statement_text` | N/A | No direct equivalent in Snowflake |
  | `@@error.stack_trace` | N/A | No direct equivalent in Snowflake |
  | `@@error.formatted_stack_trace` | N/A | No direct equivalent in Snowflake |
  | N/A | `SQLSTATE` | 5-character ANSI SQL state code |
  | N/A | `SQLCODE` | 5-digit signed integer error code |

  Expand

  Show lessSee more
- Review the generated `OBJECT_CONSTRUCT('SQLERRM', SQLERRM, 'SQLCODE', SQLCODE, 'SQLSTATE', SQLSTATE)` workaround and adjust it based on your specific error-handling requirements.
- For more information, see [Handling Exceptions in Snowflake](/developer-guide/snowflake-scripting/exceptions).

## SSC-FDM-BQ0003

Unable to generate correct return table clause due to missing dependent object information.

Note

This issue is deprecated and no longer generated. Check [SSC-EWI-BQ0009](../conversion-issues/bigqueryEWI#ssc-ewi-bq0009) for the issue now generated for this scenario

### Description

Snowflake requires a valid RETURNS TABLE clause for CREATE TABLE FUNCTION statements.

If the original BigQuery source code does not have a RETURNS TABLE clause, one must be built. To do this, an analysis is made to the CREATE TABLE FUNCTION query to properly infer the types of the columns of the resulting table. When the required information cannot be gathered, this EWI is added.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE FUNCTION function_name_noreturns_asterisk_join (parameter_name INTEGER)
AS
  SELECT *
  FROM unknownTable1 t1
  JOIN unknownTable2 t2 ON t1.col1 = t2.fk_col1;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "unknownTable1", "unknownTable2" **

CREATE OR REPLACE FUNCTION function_name_noreturns_asterisk_join (parameter_name INTEGER)
----** SSC-FDM-BQ0003 - UNABLE TO GENERATE CORRECT RETURNS TABLE CLAUSE DUE TO MISSING DEPENDENT OBJECT INFORMATION. **
--RETURNS TABLE (
--)
AS
    $$
      SELECT *
      FROM
      unknownTable1 t1
      JOIN
          unknownTable2 t2 ON t1.col1 = t2.fk_col1
    $$;
```

#### Best Practices

- Always try to include any dependent object definitions in the input code, so that important information is available for analysis.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-BQ0004

The INFER\_SCHEMA function requires a file path without wildcards to generate the table template, replace the FILE\_PATH placeholder with it

Warning

This FDM is deprecated; please refer to [SSC-FDM-0034](generalFDM#ssc-fdm-0034) for the latest version of this FDM.

### Description

The [INFER\_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) function is used in Snowflake to generate the columns definition of a table based on the structure of a file, it requires a LOCATION parameter that specifies the path to a file or folder that will be used to construct the table columns, however, this path does not support regex, meaning that the wildcard `*` character is not supported.

When the table has no columns, all URIs are checked to find one that does not use wildcards and use it in the INFER\_SCHEMA function. When no URI meets such criteria, this FDM and a FILE\_PATH placeholder is generated, and the placeholder has to be replaced with the path of one of the files referenced by the external table to generate the table columns.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2
OPTIONS(
  FORMAT='JSON',
  URIS=['gs://sc_external_table_bucket/folder_with_json/*']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2 USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-BQ0004 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_json/.*'
FILE_FORMAT = (TYPE = JSON);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-BQ0005

Parsing the CSV header is not supported in external tables, columns must be renamed to match the original names

### Description

Snowflake external tables do not support parsing the header of CSV files. SKIP\_HEADER is used as a workaround to avoid runtime errors, but the resulting table column names will have auto-generated names (`c1`, `c2`, …, `cN`) instead of the original header names.

When an external table with CSV file format and no explicit column list is detected, the `SKIP_HEADER = 1` file format option is added. The columns must be manually renamed to match the original names from the CSV header.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_csv
OPTIONS(
  FORMAT='CSV',
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Employees.csv']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_CSV_FORMAT
TYPE = CSV
SKIP_HEADER = 1;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_csv
--** SSC-FDM-BQ0005 - PARSING THE CSV HEADER IS NOT SUPPORTED IN EXTERNAL TABLES, COLUMNS MUST BE RENAMED TO MATCH THE ORIGINAL NAMES **
USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/folder_with_csv/Employees.csv', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_CSV_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Employees.csv'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

#### Best Practices

- Rename the auto-generated column names (`c1`, `c2`, …, `cN`) back to the original column names from the CSV file header.
- If the original column names are known, use `ALTER TABLE ... RENAME COLUMN` or recreate the external table with explicit column definitions.
- For non-external-table loading scenarios, consider using `MATCH_BY_COLUMN_NAME` with `PARSE_HEADER = TRUE` in the file format to automatically match columns by header names.

## SSC-FDM-BQ0006

Reading from Google Drive is not supported in Snowflake, upload the files to the external location and replace the FILE\_PATH placeholders

### Description

Snowflake does not support reading data from files hosted in Google Drive, this FDM is generated to notify it, please upload the Google Drive files to the external location so they can be accessed through the external stage.

The PATTERN clause will hold autogenerated placeholders FILE\_PATH0, FILE\_PATH1, …, FILE\_PATHN that should be replaced with the file/folder path after the files were moved to the external location.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_drive_test
OPTIONS(
  FORMAT='JSON',
  URIS=['https://drive.google.com/open?id=someFileId']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_DRIVE_TEST_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_drive_test USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-0035 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_DRIVE_TEST_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS AN EXTERNAL LOCATION, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
--** SSC-FDM-BQ0006 - READING FROM GOOGLE DRIVE IS NOT SUPPORTED IN SNOWFLAKE, UPLOAD THE FILES TO THE EXTERNAL LOCATION AND REPLACE THE FILE_PATH PLACEHOLDERS **
PATTERN = 'FILE_PATH0'
FILE_FORMAT = (TYPE = JSON);
```

#### Best Practices

- Download the files from Google Drive and upload them to a cloud storage location accessible by Snowflake (e.g., Amazon S3, Azure Blob Storage, or Google Cloud Storage).
- Create or configure an external stage in Snowflake pointing to the cloud storage location.
- Replace the `FILE_PATH` placeholders in the `PATTERN` clause with the actual file or folder paths relative to the external stage.

## SSC-FDM-BQ0007

The GOOGLE\_SHEETS format is not supported in Snowflake. CSV file type is used as a workaround.

### Description

The GOOGLE\_SHEETS format is not supported in Snowflake. CSV file type is used as a workaround because the structure of Google Sheets data is similar to CSV.

When an external table using the GOOGLE\_SHEETS format is detected, an external table with the CSV file format is produced instead. The resulting table expects a CSV file rather than a Google Sheets source.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.spreadsheetTable
(
  Name STRING,
  Code INTEGER,
  Price INTEGER,
  Expiration_date DATE
)
OPTIONS(
  format="GOOGLE_SHEETS",
  skip_leading_rows = 1,
  uris=['https://docs.google.com/spreadsheets/d/someFileId/edit?usp=sharing']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
--** SSC-FDM-BQ0007 - THE GOOGLE_SHEETS FORMAT IS NOT SUPPORTED IN SNOWFLAKE. CSV FILE TYPE IS USED AS A WORKAROUND. **
CREATE OR REPLACE EXTERNAL TABLE test.spreadsheetTable
(
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c1') AS STRING),
  Code INTEGER AS CAST(GET_IGNORE_CASE($1, 'c2') AS INTEGER),
  Price INTEGER AS CAST(GET_IGNORE_CASE($1, 'c3') AS INTEGER),
  Expiration_date DATE AS CAST(GET_IGNORE_CASE($1, 'c4') AS DATE)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS AN EXTERNAL LOCATION, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
--** SSC-FDM-BQ0006 - READING FROM GOOGLE DRIVE IS NOT SUPPORTED IN SNOWFLAKE, UPLOAD THE FILES TO THE EXTERNAL LOCATION AND REPLACE THE FILE_PATH PLACEHOLDERS **
PATTERN = 'FILE_PATH0'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- Export the Google Sheets data as CSV files and upload them to a cloud storage location accessible by Snowflake.
- Verify that the CSV export preserves the expected data types and formatting, especially for dates, numbers, and text fields with commas.
- If the external table also references Google Drive URIs, see [SSC-FDM-BQ0006](#ssc-fdm-bq0006) for instructions on migrating the files to an external stage.

## SSC-FDM-BQ0008

Where clause references a column of STRUCT type. Comparison operations may produce different results in Snowflake.

### Description

BigQuery STRUCT types have no direct equivalent in Snowflake. VARIANT is used as a workaround (see [SSC-FDM-0034](generalFDM#ssc-fdm-0034)). When a comparison involves a Snowflake VARIANT created from a BigQuery STRUCT, the results may differ because Snowflake compares both keys and values, whereas BigQuery compares only values regardless of field names.

This FDM is added when a WHERE clause comparison involves a column of STRUCT type that was converted to VARIANT.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE test.compExprTable
(
  COL1 STRUCT<sc1 INT64>,
  COL2 STRUCT<sc2 INT64>
);

SELECT * FROM test.compExprTable WHERE COL1 <> (COL2);
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE test.compExprTable
(
  COL1 VARIANT /*** SSC-FDM-0034 - STRUCT<INT64> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
  COL2 VARIANT /*** SSC-FDM-0034 - STRUCT<INT64> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}';

SELECT * FROM
  test.compExprTable
--** SSC-FDM-BQ0008 - WHERE CLAUSE REFERENCES A COLUMN OF STRUCT TYPE. COMPARISON OPERATIONS MAY PRODUCE DIFFERENT RESULTS IN SNOWFLAKE. **
WHERE COL1 <> (COL2);
```

#### Best Practices

- Review WHERE clause comparisons involving STRUCT-derived VARIANT columns. If the original BigQuery query compared STRUCTs by value only, extract and compare individual fields explicitly in Snowflake.
- For example, replace `WHERE col1 <> col2` with `WHERE col1:sc1 <> col2:sc2` to compare specific field values instead of the entire VARIANT object.
- For more information on VARIANT comparison behavior, see the [Snowflake VARIANT documentation](https://docs.snowflake.com/en/sql-reference/data-types-semistructured).

## SSC-FDM-BQ0010

Geography function is not required in Snowflake.

### Description

Snowflake automatically detects GEOGRAPHY data from [WGS 84](https://spatialreference.org/ref/epsg/wgs-84/) formatted strings (WKT, WKB, GeoJSON), so explicit geography conversion functions like `ST_GEOGFROMTEXT` are not required in VALUES clause inserts. The function call is removed and the string literal is passed directly. This FDM is added to notify that the geography function was removed.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType VALUES
(ST_GEOGFROMTEXT('POINT(-122.35 37.55)')),
(ST_GEOGFROMTEXT('LINESTRING(-124.20 42.00, -120.01 41.99)'));

SELECT * FROM test.geographyType;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'POINT(-122.35 37.55)'), (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'LINESTRING(-124.20 42.00, -120.01 41.99)');

ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';
SELECT * FROM
test.geographyType;
```

#### Best Practices

- This FDM can be safely ignored in most cases. Snowflake natively supports GEOGRAPHY data from WKT, WKB, and GeoJSON string formats without requiring explicit conversion functions.
- If the removed function performed validation or transformation beyond simple type casting, verify that the inserted data is valid GEOGRAPHY data in Snowflake.
- For more information, see the [Snowflake GEOGRAPHY data type documentation](https://docs.snowflake.com/en/sql-reference/data-types-geospatial).

## SSC-FDM-BQ0011

Named parameters in this script were transformed to Snowflake CLI variables.

### Description

BigQuery supports named parameters using the `@parameter_name` syntax in queries. These named parameters are transformed to Snowflake CLI variables using the `<% parameter_name %>` syntax.

To execute the transformed `.sql` scripts containing named parameters, use Snowflake CLI with variable substitution.

For more information on how to set up and use Snowflake CLI, see [What is Snowflake CLI?](/developer-guide/snowflake-cli/index)

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT column1 FROM test.parametersExample WHERE column2 = @searchValue;
```

##### Example execution (using the bq query command)

Copy code

```
bq query \
  --use_legacy_sql=false \
  --parameter=searchValue:Int64:80 \
  'SELECT column1 FROM test.parametersExample WHERE column2 = @searchValue'
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-BQ0011 - NAMED PARAMETERS IN THIS SCRIPT WERE TRANSFORMED TO SNOWFLAKE CLI VARIABLES. **
SELECT column1 FROM
test.parametersExample
WHERE column2 = <% searchValue %>;
```

##### Example execution (Snowflake CLI)

Copy code

```
snow sql -f output_file_path -D "searchValue=80"
```

### Best Practices

- Install and configure [Snowflake CLI](/developer-guide/snowflake-cli/index) to execute the transformed scripts with variable substitution using the `-D` flag (e.g., `snow sql -f script.sql -D "param=value"`).
- Review each transformed `<% parameter_name %>` variable to ensure the parameter name and intended value match the original BigQuery `@parameter_name` usage.
- If the transformed script will be executed outside of Snowflake CLI (e.g., in a Snowflake worksheet), replace `<% parameter_name %>` variables with literal values or session variables as appropriate.

## SSC-FDM-BQ0012

Select \* with multiple UNNEST operators will produce column ambiguity in Snowflake

### Description

As part of the SnowConvert transformation for the UNNEST operator, the [FLATTEN](/sql-reference/functions/flatten) function is used, this function generates multiple columns not required to emulate the UNNEST operator functionality like the `THIS` or `PATH` columns.

When a SELECT \* with the UNNEST operator is found, SnowConvert will remove the unnecessary columns using the `EXCLUDE` keyword, however, when multiple UNNEST operators are used in the same statement, the columns can not be removed due to ambiguity problems, this FDM will be generated to mark these cases.

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
--** SSC-FDM-BQ0012 - SELECT * WITH MULTIPLE UNNEST OPERATORS WILL RESULT IN COLUMN AMBIGUITY IN SNOWFLAKE **
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

#### Recommendations

1. **Expand the SELECT list:** Replace `SELECT *` with an explicit column list specifying only the columns you need from each UNNEST/FLATTEN result. This eliminates the ambiguity caused by duplicate metadata columns.
2. **Use table aliases:** Qualify each column reference with the corresponding table alias to avoid ambiguity between the FLATTEN results.

## SSC-FDM-BQ0013

BigQuery PIVOT output column names may differ from Snowflake; downstream queries that reference pivot output columns may need updates.

### Description

BigQuery and Snowflake both support a [PIVOT](https://docs.snowflake.com/en/sql-reference/constructs/pivot) operator with the same syntax, including the optional `IN`-list aliasing form (`'Q1' AS first`). Single-aggregate PIVOT operators are passed through unchanged. The operator produces the same rows on both engines, but they can name the resulting columns differently:

- In Snowflake, an unaliased string value such as `'Q1'` becomes a column named `'Q1'` (the literal keeps its quotes and must be referenced as `"'Q1'"`); an `IN`-list alias replaces the value (`'Q1' AS first` becomes `FIRST`); and an aggregate alias is appended as a suffix (`SUM(amount) AS total` appends `_TOTAL`). See the [Snowflake PIVOT documentation](https://docs.snowflake.com/en/sql-reference/constructs/pivot) for the exact rules.
- BigQuery applies its own naming for the same constructs (see the [BigQuery PIVOT operator](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#pivot_operator)), which can differ from Snowflake’s for unaliased values and for aliased aggregates.

This FDM is emitted only when the output column names can actually diverge — that is, when **at least one `IN`-list value is unaliased, or the aggregate function is aliased**. When every `IN`-list value is aliased **and** the aggregate has no alias, both engines produce identical column names, so the marker is suppressed and no downstream changes are required.

The pivot itself executes correctly in both engines; the FDM only flags that downstream queries (`SELECT pivoted_col FROM ...`, `ORDER BY`, joins, view definitions) that reference the output columns by name may need to be updated to match the Snowflake naming rule.

Multi-aggregate PIVOT (`PIVOT(agg1, agg2 FOR ...)`) is not supported in Snowflake. It is currently passed through unchanged without emitting this FDM; a dedicated EWI is planned as follow-up work.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT * FROM sales PIVOT(SUM(amount) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
  *
FROM
  sales
  --** SSC-FDM-BQ0013 - BIGQUERY PIVOT OUTPUT COLUMN NAMES MAY DIFFER FROM SNOWFLAKE; DOWNSTREAM QUERIES THAT REFERENCE PIVOT OUTPUT COLUMNS MAY NEED UPDATES **
  PIVOT(
    SUM(amount)
    FOR quarter
    IN ('Q1', 'Q2', 'Q3', 'Q4')
  );
```

When every `IN`-list value is aliased and the aggregate has no alias, the column names match on both engines, so no marker is added:

Copy code

```
SELECT
  *
FROM
  sales PIVOT(
    SUM(amount)
    FOR quarter
    IN ('Q1' AS first, 'Q2' AS second)
  );
```

#### Recommendations

1. **Inspect downstream column references.** Review every `SELECT`, `WHERE`, `ORDER BY`, `JOIN`, or view definition that references the PIVOT result columns by name and update it to the Snowflake naming rule. For example, where BigQuery exposed an unaliased value `'Q1'`, Snowflake produces the column `'Q1'`, referenced as `"'Q1'"`.
2. **Avoid the difference at the source.** To get identical column names on both engines, alias every `IN`-list value and leave the aggregate unaliased (for example `IN ('Q1' AS first, 'Q2' AS second)`). With both conditions met, this FDM is not emitted.
3. **Or rename explicitly downstream.** Wrap the PIVOT in a subquery and alias the output columns so downstream queries are insulated from the engine difference.

## SSC-FDM-BQ0014

ST\_DISTANCE third argument (use\_spheroid) was removed; Snowflake always uses sphere-based geography distance.

### Description

BigQuery’s [ST\_DISTANCE](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_distance) function accepts an optional third boolean argument `use_spheroid` that controls whether the distance computation uses the WGS84 ellipsoid (`TRUE`) or a perfect sphere (`FALSE`, the default). Snowflake’s [ST\_DISTANCE](https://docs.snowflake.com/en/sql-reference/functions/st_distance) accepts only two arguments and always uses sphere-based math for `GEOGRAPHY` inputs.

When the BigQuery argument is statically the literal `FALSE` the third argument is silently dropped because the calls are semantically identical. When the argument is the literal `TRUE`, a column reference, or any other expression whose value cannot be proven equal to `FALSE` at compile time, the third argument is removed and this FDM is added to flag the spheroid-vs-sphere divergence — the result will differ from BigQuery’s by up to ~0.5% on long distances.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_DISTANCE(g1, g2) FROM cities;
SELECT ST_DISTANCE(g1, g2, FALSE) FROM cities;
SELECT ST_DISTANCE(g1, g2, TRUE) FROM cities;
SELECT ST_DISTANCE(g1, g2, use_spheroid_col) FROM cities;
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT ST_DISTANCE(g1, g2) FROM cities;
SELECT ST_DISTANCE(g1, g2) FROM cities;
SELECT ST_DISTANCE(g1, g2) /*** SSC-FDM-BQ0014 - THE THIRD ARGUMENT 'USE_SPHEROID' OF ST_DISTANCE WAS REMOVED. SNOWFLAKE ALWAYS USES SPHERE-BASED GEOGRAPHY DISTANCE. ***/ FROM cities;
SELECT ST_DISTANCE(g1, g2) /*** SSC-FDM-BQ0014 - THE THIRD ARGUMENT 'USE_SPHEROID' OF ST_DISTANCE WAS REMOVED. SNOWFLAKE ALWAYS USES SPHERE-BASED GEOGRAPHY DISTANCE. ***/ FROM cities;
```

#### Recommendations

1. **Accept sphere-based math when precision tolerance permits.** For most application use cases the difference between sphere and ellipsoid distance is below 0.5%; if downstream code is not sensitive to that, the FDM can be safely waived.
2. **Verify whether the dropped argument was column-driven.** If the third argument was a column reference, evaluate whether the query was actually exercising spheroid math at runtime. A column always-FALSE makes the difference moot; a column always-TRUE means every row needs the precision difference reviewed.

## SSC-FDM-BQ0015

PARSE\_JSON ‘wide\_number\_mode’ argument is not supported in Snowflake and was removed.

### Description

BigQuery’s [PARSE\_JSON](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#parse_json) accepts an optional named argument `wide_number_mode => 'exact' | 'round'` that controls how numbers exceeding `INT64`/`FLOAT64` precision are handled at parse time. Snowflake’s [PARSE\_JSON](https://docs.snowflake.com/en/sql-reference/functions/parse_json) does not expose an equivalent option; it preserves number precision up to 38 digits natively.

When the BigQuery `PARSE_JSON` call includes the `wide_number_mode` named argument, the argument is stripped and this FDM is emitted to flag the silent removal so the user can verify Snowflake’s 38-digit precision is sufficient for their data.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT PARSE_JSON('{"big": 9007199254740993}', wide_number_mode => 'exact') AS j;
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-BQ0015 - PARSE_JSON 'WIDE_NUMBER_MODE' ARGUMENT IS NOT SUPPORTED IN SNOWFLAKE AND WAS REMOVED. SNOWFLAKE PRESERVES NUMBER PRECISION UP TO 38 DIGITS. **
PARSE_JSON('{"big": 9007199254740993}') AS j;
```

#### Recommendations

1. **Verify number magnitudes against Snowflake’s 38-digit limit.** If the JSON payloads in your data set never exceed 38 significant digits, the removed argument has no functional effect and the FDM can be waived.
2. **For overflowing values, project to text or split.** If the data legitimately contains numbers wider than 38 digits, store and read those fields as strings (`x::STRING`) and only cast to NUMBER for the subset of values known to fit.

## SSC-FDM-BQ0016

SESSION\_USER returns an email address in BigQuery. Snowflake CURRENT\_USER returns a username.

### Description

BigQuery’s [SESSION\_USER](https://cloud.google.com/bigquery/docs/reference/standard-sql/security_functions#session_user) returns the email address of the authenticated IAM principal that submitted the query (for example, `alice@example.com` for a user, or a service-account email for a service account). Snowflake’s closest equivalent is [CURRENT\_USER](https://docs.snowflake.com/en/sql-reference/functions/current_user), which returns the **Snowflake username** of the active session, not an email address.

Every `SESSION_USER()` call is rewritten to `CURRENT_USER()` and this FDM is emitted to flag the format change. The rewrite preserves the *intent* of identifying the active principal, but downstream code that relies on the value being an email — string parsing for the `@domain` portion, joins against an `email`-keyed identity table, audit-log records that compare against IAM identities — will need to be reviewed.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT SESSION_USER() AS u;

INSERT INTO audit_log (action, who) VALUES ('LOGIN', SESSION_USER());
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
  --** SSC-FDM-BQ0016 - SESSION_USER RETURNS AN EMAIL ADDRESS IN BIGQUERY. SNOWFLAKE CURRENT_USER RETURNS A USERNAME. **
  CURRENT_USER() AS u;

INSERT INTO audit_log (action, who)
VALUES ('LOGIN',
--** SSC-FDM-BQ0016 - SESSION_USER RETURNS AN EMAIL ADDRESS IN BIGQUERY. SNOWFLAKE CURRENT_USER RETURNS A USERNAME. **
CURRENT_USER());
```

#### Recommendations

1. **Audit identity comparisons and joins.** Any predicate that compares the result of `SESSION_USER()` against a stored email column (for example, `WHERE email = SESSION_USER()`) will not match in Snowflake — the right side is now a username. Either rewrite the predicate to compare against the Snowflake username column, or maintain a username-to-email mapping table.
2. **Review string parsing on the result.** Code that extracts the domain portion (e.g., `SUBSTR(SESSION_USER(), STRPOS(SESSION_USER(), '@') + 1)`) becomes incorrect — Snowflake usernames do not contain `@`. Rework the logic against a column that holds the email, or remove the parsing if the username alone is sufficient.
3. **Update audit and provenance records.** If audit tables capture `SESSION_USER()` for compliance or traceability, document the format change in the table’s data dictionary and confirm with stakeholders that a Snowflake username satisfies the record-keeping requirement.

## SSC-FDM-BQ0017

CURRENT\_DATETIME timezone argument was wrapped with CONVERT\_TIMEZONE

#### Description

BigQuery accepts a timezone argument in `CURRENT_DATETIME`, while Snowflake requires an explicit conversion of `CURRENT_TIMESTAMP`. SnowConvert AI wraps the call with `CONVERT_TIMEZONE`, but timezone database rules, daylight-saving behavior, and sub-second precision can differ between platforms.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT CURRENT_DATETIME('Asia/Tokyo');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) :: TIMESTAMP_NTZ /*** SSC-FDM-BQ0017 - BIGQUERY CURRENT_DATETIME TIMEZONE ARGUMENT WAS WRAPPED WITH CONVERT_TIMEZONE. SNOWFLAKE TIMEZONE DATABASE/DST RULES AND SUB-SECOND PRECISION (NANOSECONDS VS MICROSECONDS) MAY DIFFER FROM BIGQUERY. ***/;
```

#### Best Practices

1. Confirm the timezone identifier and daylight-saving rules, and account for Snowflake’s microsecond precision.

## SSC-FDM-BQ0018

BigQuery BIGNUMERIC/BIGDECIMAL precision may exceed Snowflake DECFLOAT

#### Description

BigQuery `BIGNUMERIC` and `BIGDECIMAL` values can contain up to 76 digits of precision. SnowConvert AI maps them to Snowflake `DECFLOAT`, which preserves 38 significant digits over a wide exponent range, so wider source values can be rounded.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE TABLE financial_values (amount BIGNUMERIC);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE TABLE financial_values (
  amount DECFLOAT /*** SSC-FDM-BQ0018 - BIGQUERY BIGNUMERIC/BIGDECIMAL SUPPORTS UP TO 76 DIGITS OF PRECISION; SNOWFLAKE DECFLOAT PRESERVES 38 SIGNIFICANT DIGITS WITH A WIDE EXPONENT RANGE. VALUES WITH MORE THAN 38 SIGNIFICANT DIGITS MAY BE ROUNDED. ***/
);
```

#### Best Practices

1. Test values wider than 38 significant digits and store them as strings if exact preservation is required.

## SSC-FDM-BQ0019

ST\_AREA/ST\_LENGTH use\_spheroid argument was removed; Snowflake always uses sphere-based geography computation.

#### Description

BigQuery `ST_AREA` and `ST_LENGTH` accept a `use_spheroid` argument that selects spheroid-based computation. Snowflake always uses sphere-based geography computation, so SnowConvert AI removes the argument and adds this FDM because results can differ.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_AREA(geog, TRUE) FROM polygons;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ST_AREA(geog) /*** SSC-FDM-BQ0019 - THE 'USE_SPHEROID' ARGUMENT WAS REMOVED FROM ST_AREA/ST_LENGTH. SNOWFLAKE ALWAYS USES SPHERE-BASED GEOGRAPHY COMPUTATION. ***/ FROM polygons;
```

#### Best Practices

1. Compare representative results when the source requested spheroid computation.

## SSC-FDM-BQ0020

ST\_CENTROID centroid math differs between BigQuery (geodesic) and Snowflake (spherical); results may drift for large polygons.

#### Description

BigQuery computes geography centroids using geodesic math, while Snowflake uses spherical math. SnowConvert AI preserves the `ST_CENTROID` call and adds this FDM because the resulting point can drift for large polygons.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_CENTROID(ST_GEOGFROMTEXT('LINESTRING(0 0, 2 2)'));
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  ST_CENTROID(ST_GEOGFROMTEXT('LINESTRING(0 0, 2 2)')) /*** SSC-FDM-BQ0020 - ST_CENTROID USES GEODESIC CENTROID MATH IN BIGQUERY AND SPHERICAL MATH IN SNOWFLAKE; RESULTS MAY DRIFT FOR LARGE POLYGONS. ***/;
```

#### Best Practices

1. Compare centroid results for representative large polygons and define an acceptable spatial tolerance.

## SSC-FDM-BQ0021

Snowflake’s ST\_BUFFER operates on planar GEOMETRY and does not accept GEOGRAPHY arguments, while BigQuery’s ST\_BUFFER uses geodesic GEOGRAPHY; review the input type and results.

#### Description

BigQuery’s two-argument `ST_BUFFER` operates on geodesic `GEOGRAPHY` values. Snowflake’s function operates on planar `GEOMETRY` and does not accept `GEOGRAPHY`, so the input type and resulting shape may differ even though SnowConvert AI preserves the call.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_BUFFER(geog, 1000) FROM tbl;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  ST_BUFFER(geog, 1000) /*** SSC-FDM-BQ0021 - SNOWFLAKE'S ST_BUFFER OPERATES ON PLANAR GEOMETRY AND DOES NOT ACCEPT GEOGRAPHY ARGUMENTS, WHILE BIGQUERY'S ST_BUFFER USES GEODESIC GEOGRAPHY. THE INPUT MAY NEED TO BE A GEOMETRY AND THE RESULTING SHAPE CAN DIFFER. ***/
FROM
  tbl;
```

#### Best Practices

1. Convert or project the input to a suitable `GEOMETRY` and compare representative buffer shapes before deployment.

## SSC-FDM-BQ0022

CURRENT\_TIME timezone argument was wrapped with CONVERT\_TIMEZONE

#### Description

BigQuery accepts a timezone argument in `CURRENT_TIME`, while Snowflake requires converting `CURRENT_TIMESTAMP` before casting to `TIME`. SnowConvert AI emits that rewrite, but timezone database rules, daylight-saving behavior, and sub-second precision can differ.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT CURRENT_TIME('America/Los_Angeles');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
CONVERT_TIMEZONE('America/Los_Angeles', CURRENT_TIMESTAMP()) :: TIME /*** SSC-FDM-BQ0022 - BIGQUERY CURRENT_TIME TIMEZONE ARGUMENT WAS WRAPPED WITH CONVERT_TIMEZONE. SNOWFLAKE TIMEZONE DATABASE/DST RULES AND SUB-SECOND PRECISION (NANOSECONDS VS MICROSECONDS) MAY DIFFER FROM BIGQUERY. ***/;
```

#### Best Practices

1. Confirm the timezone identifier and daylight-saving rules, and account for Snowflake’s microsecond precision.

## SSC-FDM-BQ0023

CURRENT\_DATE timezone argument was wrapped with CONVERT\_TIMEZONE

#### Description

BigQuery accepts a timezone argument in `CURRENT_DATE`, while Snowflake requires converting `CURRENT_TIMESTAMP` before extracting the date. SnowConvert AI wraps the expression with `TO_DATE(CONVERT_TIMEZONE(...))`, but timezone database and daylight-saving rules can differ.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT CURRENT_DATE('America/Los_Angeles') AS d;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
TO_DATE(CONVERT_TIMEZONE('America/Los_Angeles', CURRENT_TIMESTAMP())) /*** SSC-FDM-BQ0023 - BIGQUERY CURRENT_DATE TIMEZONE ARGUMENT WAS WRAPPED WITH TO_DATE(CONVERT_TIMEZONE(...)). SNOWFLAKE TIMEZONE DATABASE/DST RULES MAY DIFFER FROM BIGQUERY. ***/ AS d;
```

#### Best Practices

1. Confirm that the timezone identifier and daylight-saving behavior match the source application’s expectations.

## SSC-FDM-BQ0024

ST\_ASGEOJSON returns a STRING in BigQuery and an OBJECT in Snowflake

#### Description

BigQuery `ST_ASGEOJSON` returns serialized GeoJSON as a string, while Snowflake returns an `OBJECT`. SnowConvert AI preserves the function call and adds this FDM because downstream string operations may require an explicit `TO_VARCHAR`.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT ST_ASGEOJSON(geog_col) FROM locations;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  ST_ASGEOJSON(geog_col) /*** SSC-FDM-BQ0024 - ST_ASGEOJSON RETURNS A STRING IN BIGQUERY AND AN OBJECT IN SNOWFLAKE. WRAP IN TO_VARCHAR IF A STRING TYPE IS REQUIRED DOWNSTREAM. ***/
FROM
  locations;
```

#### Best Practices

1. Wrap the call in `TO_VARCHAR` when downstream logic requires a string.

## SSC-FDM-BQ0025

BigQuery INSTR counts overlapping matches for the occurrence argument while Snowflake REGEXP\_INSTR counts non-overlapping ones, so results may differ.

#### Description

BigQuery `INSTR` counts overlapping matches when an occurrence argument is supplied. Snowflake `REGEXP_INSTR` counts non-overlapping matches, so SnowConvert AI adds this FDM when a multi-character search and later occurrence can return a different position.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
SELECT INSTR('aaaa', 'aa', 1, 2) AS p;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-BQ0025 - BIGQUERY INSTR COUNTS OVERLAPPING MATCHES FOR THE OCCURRENCE ARGUMENT WHILE SNOWFLAKE REGEXP_INSTR COUNTS NON-OVERLAPPING MATCHES; RESULTS MAY DIFFER FOR SEARCH STRINGS THAT CAN OVERLAP. **
REGEXP_INSTR('aaaa', 'aa', 1, 2) AS p;
```

#### Best Practices

1. Test occurrence values with overlapping search strings and implement custom matching logic if source-compatible positions are required.
