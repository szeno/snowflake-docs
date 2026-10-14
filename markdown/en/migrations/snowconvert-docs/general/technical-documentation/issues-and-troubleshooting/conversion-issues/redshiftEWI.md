# Code Conversion - Redshift Issues

## SSC-EWI-RS0002

Set “configuration parameter” is not supported in Snowflake.

### Severity

Medium

#### Description

The [`SET configuration parameter`](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html) clause in Redshift procedures is not supported in Snowflake. Snowflake uses [ALTER SESSION SET](/sql-reference/sql/alter-session) or session-level parameters instead. For more information, refer to [CREATE PROCEDURE documentation](/sql-reference/sql/create-procedure).

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure2(
    IN input_param INTEGER,
    OUT output_param NUMERIC
)
AS $$
BEGIN
    output_param := input_param * 1.7;
END;
$$
LANGUAGE plpgsql
SET enable_numeric_rounding to ON;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure2 (input_param INTEGER, output_param OUT NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0002 - SET CONFIGURATION PARAMETER 'enable_numeric_rounding' IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
SET enable_numeric_rounding to ON
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
    output_param := input_param * 1.7;
END;
$$;
```

#### Best Practices

- **Use ALTER SESSION SET:** Snowflake provides [ALTER SESSION SET](/sql-reference/sql/alter-session) to configure session-level parameters. Review whether the Redshift configuration parameter has an equivalent Snowflake session parameter.
- **Remove if unnecessary:** Some Redshift configuration parameters (e.g., `enable_numeric_rounding`) have no Snowflake equivalent and may be safely removed if Snowflake’s default behavior meets your requirements.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0003

View with no schema binding can not be removed due to missing references.

Note

This issue is deprecated and no longer generated

### Severity

Medium

#### Description

Redshift documentation for `CREATE VIEW` includes an optional clause that specifies that the particular view is not bound to the database objects such as tables or functions, nor to those objects that it is referencing. The documentation also clarifies that in such cases that this clause is used, the referenced objects must be qualified with a schema name. This clause allows to create a view and reference objects that might not exist yet. Their existence will be verified once the view is queried, but not at its definition.

However, there is no equivalent command nor obvious workaround to implement this functionality in Snowflake, furthermore, the Snowflake documentation suggests that the views are linked to a specific schema and so are the referenced objects in the view.

If the references linked to the View are present in the input code, the statement will be removed without issue. However, if the necessary references are missing, a warning message will be added to inform the user that the statement cannot be removed due to the missing references.

Analysis is performed solely on the input code and does not account for objects already deployed in Snowflake. Therefore the output may have some issues pointing to missing references, if the references are already present in the Snowflake database, the user can safely remove the statement without any issues.

#### Code Examples

##### Input Code:

##### Redshift

Copy code

```
 CREATE VIEW myView AS SELECT col1 FROM public.missingTable
WITH NO SCHEMA BINDING;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "public.missingTable" **
CREATE VIEW myView
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
AS SELECT col1 FROM
public.missingTable
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0003 - WITH NO SCHEMA BINDING STATEMENT CAN NOT BE REMOVED DUE TO MISSING REFERENCES. ***/!!!
WITH NO SCHEMA BINDING;
```

#### Best Practices

- To resolve this issue, it is suggested to add the missing references to the input code, if the object is already deployed in the Snowflake database, the statement can be remove without issue.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0004

HLLSKETCH data type not supported in Snowflake.

### Severity

High

#### Description

This conversion issue is added because the HLLSKETCH data type is not supported in Snowflake.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE table1
(
    col_hllsketch HLLSKETCH
);
```

##### Generated Code:

Copy code

```
 CREATE TABLE table1
(
    col_hllsketch HLLSKETCH !!!RESOLVE EWI!!! /*** SSC-EWI-RS0004 - HLLSKETCH DATA TYPE NOT SUPPORTED IN SNOWFLAKE. ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- Please verify all [aggregate functions](https://docs.snowflake.com/en/user-guide/querying-approximate-cardinality#sql-functions) provided by Snowflake to estimate cardinality using [HyperLogLog](https://docs.snowflake.com/en/user-guide/querying-approximate-cardinality#overview).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0005

Pending translation for column aliases in the PIVOT/UNPIVOT IN clause.

### Severity

High

#### Description

Pending translation for column aliases in the `PIVOT/UNPIVOT` `IN` clause. Snowflake now supports the `AS` clause for specifying column aliases in [`PIVOT`](/sql-reference/constructs/pivot) and [`UNPIVOT`](/sql-reference/constructs/unpivot) operations (added October 2025). This is not a Snowflake platform limitation.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 SELECT *
FROM count_by_color UNPIVOT (
    cnt FOR color IN (red AS r, green AS g, blue AS b)
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT *
FROM
    count_by_color UNPIVOT (
    cnt FOR color IN (red
                          !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - PENDING SNOWCONVERT AI TRANSLATION FOR COLUMN ALIASES IN THE PIVOT/UNPIVOT IN CLAUSE. ***/!!! AS r, green
                                                                                                                                                                              !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - PENDING SNOWCONVERT AI TRANSLATION FOR COLUMN ALIASES IN THE PIVOT/UNPIVOT IN CLAUSE. ***/!!! AS g, blue
                                                                                                                                                                                                                                                                                                                                 !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - PENDING SNOWCONVERT AI TRANSLATION FOR COLUMN ALIASES IN THE PIVOT/UNPIVOT IN CLAUSE. ***/!!! AS b)
);
```

#### Best Practices

- **Use native Snowflake support:** Snowflake now supports the `AS` clause for column aliases in `PIVOT/UNPIVOT IN` clauses. Remove the EWI marker and use the aliases directly:

Copy code

```
 SELECT *
FROM count_by_color UNPIVOT (
    cnt FOR color IN (red AS r, green AS g, blue AS b)
);
```

- **Further reading:** [Snowflake UNPIVOT](/sql-reference/constructs/unpivot), [Snowflake PIVOT](/sql-reference/constructs/pivot)
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0006

The behavior of the SUBSTRING function on binary data differs between Redshift and Snowflake.

### Severity

Medium

#### Description

The behavior of the `SUBSTRING` function on binary data differs between Redshift and Snowflake. In Redshift, `SUBSTRING` on `VARBYTE` operates on raw bytes. In Snowflake, `SUBSTRING` on `BINARY` operates on hex-encoded character pairs, so the same positional arguments may return different results.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 SELECT SUBSTRING('12345'::varbyte, 2, 4) AS substring_binary;
SELECT SUBSTRING('abc'::varbyte, 2, 4) AS substring_binary;
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT SUBSTRING('12345':: BINARY, 2, 4) !!!RESOLVE EWI!!! /*** SSC-EWI-RS0006 - THE BEHAVIOR OF THE SUBSTRING FUNCTION ON BINARY DATA DIFFERS BETWEEN REDSHIFT AND SNOWFLAKE. ***/!!! AS substring_binary;
SELECT SUBSTRING('abc':: BINARY, 2, 4) !!!RESOLVE EWI!!! /*** SSC-EWI-RS0006 - THE BEHAVIOR OF THE SUBSTRING FUNCTION ON BINARY DATA DIFFERS BETWEEN REDSHIFT AND SNOWFLAKE. ***/!!! AS substring_binary;
```

#### Best Practices

- **Verify binary output:** Compare `SUBSTRING` results on binary columns between Redshift and Snowflake to confirm correctness after migration.
- **Adjust offsets:** Because Snowflake’s `BINARY` type uses hex encoding, you may need to multiply position and length arguments by 2 to achieve equivalent byte-level extraction.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0007

Date literal is not supported in Snowflake.

### Severity

High

#### Description

Some DATE, TIME, or TIMESTAMP literal formats used in Redshift (e.g., `'2000-Jan-31'`, `'Jan-31-2000'`) are not recognized by Snowflake. These literals must be rewritten to a [supported Snowflake date format](/sql-reference/data-types-datetime) or converted using `TO_DATE` with an explicit format string.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 select datediff(century, '2000-Jan-31', 'Jan-31-2000');
```

##### Generated Code:

##### Snowflake

Copy code

```
  select
 DATEDIFF(YEAR,
                !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - '2000-Jan-31' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
                '2000-Jan-31',
                               !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - 'Jan-31-2000' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
                               'Jan-31-2000') / 100;
```

#### Best Practices

- **Use ISO 8601 format:** Rewrite date literals to `'YYYY-MM-DD'` format, which is universally supported in Snowflake.
- **Use TO\_DATE with format string:** If the original format must be preserved, use `TO_DATE('Jan-31-2000', 'MON-DD-YYYY')` to explicitly parse the date.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0008

Delete statement cannot be used on dynamic tables in Snowflake.

### Severity

High

#### Description

In Redshift, you can apply the DELETE statement to materialized views used for [streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html). In Snowflake, materialized views are transformed into [dynamic tables](/user-guide/dynamic-tables/overview), and the DELETE statement cannot be used on dynamic tables.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE MATERIALIZED VIEW mv AS
SELECT id, name, department_id FROM employees WHERE department_id = 101;

DELETE FROM mv
WHERE id = 2;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE DYNAMIC TABLE mv
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
SELECT id, name, department_id FROM
employees
WHERE department_id = 101;

!!!RESOLVE EWI!!! /*** SSC-EWI-RS0008 - MATERIALIZED VIEW IS TRANSFORMED INTO A DYNAMIC TABLE, AND THE DELETE STATEMENT CANNOT BE USED ON DYNAMIC TABLES IN SNOWFLAKE. ***/!!!
DELETE FROM
mv
WHERE id = 2;
```

#### Best Practices

- **Replace the dynamic table definition:** Because dynamic tables cannot be directly deleted from, you can achieve the same result by altering the dynamic table’s underlying query to exclude the rows you want to remove.
- **Use a regular table:** If row-level DML (INSERT, UPDATE, DELETE) is required, consider using a regular table with a scheduled task instead of a dynamic table.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0009

Source table semantic information not found in the provided code.

### Severity

Low

#### Description

Snowflake does not support the `MERGE ... REMOVE DUPLICATES` clause. A workaround is generated that includes an `INSERT WHEN NOT MATCHED` clause, which requires knowledge of the source table’s columns. If the source table definition was not included in the provided code, the column list cannot be generated and must be added manually.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 MERGE INTO target USING source ON target.id = source.id REMOVE DUPLICATES;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TEMPORARY TABLE source_duplicates AS
SELECT DISTINCT
source.*
FROM
source
INNER JOIN
target
ON target.id = source.id;
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0009 - SEMANTIC INFORMATION NOT FOUND FOR THE SOURCE TABLE IN THE CODE PROVIDED TO SNOWCONVERT AI. COLUMNS TO BE INSERTED MAY BE ADDED MANUALLY. ***/!!!
--** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT REJECTS DUPLICATE SOURCE ROWS. SNOWFLAKE ALLOWS DUPLICATES, WHICH MAY PRODUCE NON-DETERMINISTIC RESULTS. **
MERGE INTO target
USING source ON target.id = source.id
WHEN MATCHED THEN
DELETE
WHEN NOT MATCHED THEN
INSERT
VALUES ();
INSERT INTO target
SELECT
*
FROM
source_duplicates;
DROP TABLE IF EXISTS source_duplicates CASCADE;
```

#### Best Practices

- **Include all source DDL:** Provide the source table’s `CREATE TABLE` statement in the input code so columns can be resolved automatically.
- **Add columns manually:** If the source table definition is unavailable, fill in the `INSERT ... VALUES ()` clause with the correct column list from your Redshift catalog.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0010

Top-level procedure call with out parameters is not supported in Snowflake.

### Severity

Low

#### Description

Redshift allows top-level `CALL` statements to invoke procedures with `OUT` parameters without declaring a variable to receive the output. Snowflake requires that `OUT` parameters be assigned to a variable, which is only possible inside a stored procedure or anonymous block.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE get_total_sales_by_product(
    IN p_product_name VARCHAR(100),
    OUT p_total_sales DECIMAL(18, 2)
)
AS $$
BEGIN
    NULL;
END;
$$ LANGUAGE plpgsql;

CALL get_total_sales_by_product('Laptop');
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE get_total_sales_by_product (p_product_name VARCHAR(100), p_total_sales OUT DECIMAL(18, 2))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
NULL;
END;
$$;
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0010 - TOP-LEVEL PROCEDURE CALL WITH OUT PARAMETERS IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
CALL get_total_sales_by_product('Laptop');
```

#### Best Practices

- Move the call into an anonymous block and declare a variable to pass as an output parameter.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0011

Geospatial data types (GEOMETRY, GEOGRAPHY) are not supported in Iceberg V2 tables.

### Severity

High

#### Description

Redshift external tables can contain `GEOMETRY` or `GEOGRAPHY` columns, but those data types are not supported in Snowflake-managed Iceberg V2 tables. SnowConvert AI adds this EWI to geospatial columns so you can choose Iceberg V3 with `STORAGE_SERIALIZATION_POLICY=OPTIMIZED` or migrate the object as a regular Snowflake table.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE EXTERNAL TABLE spectrum_schema.stores (
  store_id INT,
  service_area GEOMETRY
)
STORED AS PARQUET
LOCATION 's3://my-data-lake/stores/';
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE ICEBERG TABLE spectrum_schema.stores (
  store_id INT,
  service_area GEOMETRY !!!RESOLVE EWI!!! /*** SSC-EWI-RS0011 - GEOMETRY DATA TYPE IS NOT SUPPORTED IN SNOWFLAKE-MANAGED ICEBERG V2 TABLES. CONSIDER USING ICEBERG V3 (REQUIRES STORAGE_SERIALIZATION_POLICY=OPTIMIZED) OR LEAVING THE TABLE AS A REGULAR SNOWFLAKE TABLE. ***/!!!
)
EXTERNAL_VOLUME = 'my_external_volume'
CATALOG = 'SNOWFLAKE'
BASE_LOCATION = 'stores/';
```

#### Best Practices

- Use Iceberg V3 with the required storage serialization policy when geospatial columns must remain in an Iceberg table.
- Otherwise, migrate the object as a regular Snowflake table.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-RS0012

The REGEXP\_INSTR PCRE parameter ‘p’ is not supported in Snowflake.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0012 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The REGEXP\_INSTR pcre parameter ‘p’ is not supported in Snowflake. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT REGEXP_INSTR(
  'passwd7 plain A1234 a1234',
  '(?=[^ ]*[a-z])(?=[^ ]*[0-9])[^ ]+',
  1, 2, 0, 'p'),
  REGEXP_INSTR('abc1', '(?=[a-z])', 1, 1, 0, 'ip'),
  REGEXP_INSTR('abc1', '(?=[a-z])', 1, 1, 0, 'P');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  REGEXP_INSTR('passwd7 plain A1234 a1234',
                                                '(?=[^ ]*[a-z])(?=[^ ]*[0-9])[^ ]+',
                                                1, 2, 0, 'p') !!!RESOLVE EWI!!! /*** SSC-EWI-RS0012 - THE REGEXP_INSTR PCRE PARAMETER 'p' IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!,
  REGEXP_INSTR('abc1', '(?=[a-z])', 1, 1, 0, 'ip') !!!RESOLVE EWI!!! /*** SSC-EWI-RS0012 - THE REGEXP_INSTR PCRE PARAMETER 'p' IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!,
  REGEXP_INSTR('abc1', '(?=[a-z])', 1, 1, 0, 'P') !!!RESOLVE EWI!!! /*** SSC-EWI-RS0012 - THE REGEXP_INSTR PCRE PARAMETER 'p' IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0012 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0013

The UNLOAD option has no Snowflake COPY INTO equivalent.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0013 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The unload option has no Snowflake copy into equivalent. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id FROM sales.orders')
TO 's3://company-exports/quoted/'
IAM_ROLE DEFAULT
ADDQUOTES;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/quoted/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0013 - THE UNLOAD OPTION 'ADDQUOTES' HAS NO SNOWFLAKE COPY INTO EQUIVALENT AND WAS REMOVED FROM THE GENERATED STATEMENT. ***/!!!
COPY INTO 's3://company-exports/quoted/'
FROM
(
SELECT
id
FROM
sales.orders
)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|');
```

#### Best Practices

Review the construct marked SSC-EWI-RS0013 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0015

The UNLOAD statement was not translated to COPY INTO.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0015 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The unload statement was not translated to copy into. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id, "Sale Year" FROM sales.orders')
TO 's3://company-exports/delimited/'
IAM_ROLE DEFAULT
CSV
PARTITION BY ("Sale Year");
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0015 - THE UNLOAD STATEMENT WAS NOT TRANSLATED TO COPY INTO: the partition folder name Redshift writes for the column "Sale Year" does not follow from its spelling ***/!!!
UNLOAD ('SELECT id, "Sale Year" FROM sales.orders')
TO 's3://company-exports/delimited/'
IAM_ROLE DEFAULT
CSV
PARTITION BY ("Sale Year");
```

#### Best Practices

Review the construct marked SSC-EWI-RS0015 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0016

The UNLOAD MAXFILESIZE value cannot be expressed as MAX\_FILE\_SIZE.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0016 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The unload maxfilesize value cannot be expressed as MAX\_FILE\_SIZE. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id FROM sales.orders')
TO 's3://company-exports/maxsize6/'
IAM_ROLE DEFAULT
CSV
MAXFILESIZE AS 6 GB;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/maxsize6/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0016 - THE UNLOAD OPTION 'MAXFILESIZE 6 GB' WAS REMOVED FROM THE GENERATED STATEMENT: ITS SIZE IS NOT A WHOLE NUMBER OF MEGABYTES OR GIGABYTES WITHIN THE 5 GB LIMIT SNOWFLAKE'S MAX_FILE_SIZE ACCEPTS. ***/!!!
COPY INTO 's3://company-exports/maxsize6/'
FROM
(
SELECT
id
FROM
sales.orders
)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Review the construct marked SSC-EWI-RS0016 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0017

The REFRESH MATERIALIZED VIEW option is not supported in Snowflake

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0017 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The refresh materialized view option is not supported in Snowflake. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
REFRESH MATERIALIZED VIEW CONCURRENTLY prod.vw_rpt_general_ledger;
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0017 - THE 'CONCURRENTLY' OPTION OF REFRESH MATERIALIZED VIEW IS NOT SUPPORTED IN SNOWFLAKE. THE STATEMENT WAS LEFT UNCONVERTED. ***/!!!
REFRESH MATERIALIZED VIEW CONCURRENTLY prod.vw_rpt_general_ledger;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0017 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0018

The procedure name cannot be rendered as an unquoted Snowflake identifier.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0018 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The procedure name cannot be rendered as an unquoted Snowflake identifier. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE PROCEDURE "crm.chery-prod"."p"() AS $$ BEGIN NULL; END; $$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE
--** SSC-FDM-RS0015 - PROCEDURE NAME '"crm.chery-prod"."p"' IS NOT A VALID SNOWFLAKE IDENTIFIER UNQUOTED, SO IT WAS RENAMED TO '"crm.chery-prod".p'. UPDATE REFERENCES FROM CODE OUTSIDE THIS CONVERSION. **
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0018 - THE PROCEDURE NAME SEGMENT '"crm.chery-prod"' HAS NO UNQUOTED SNOWFLAKE RENDERING THAT STILL NAMES THE SAME OBJECT, SO IT WAS LEFT DOUBLE-QUOTED. SNOWFLAKE DOCUMENTS DOUBLE-QUOTED NAMES AS UNSUPPORTED FOR SQL AND SNOWFLAKE SCRIPTING PROCEDURES, AND THEY ARE CASE-SENSITIVE, SO RENAME IT MANUALLY. ***/!!!
"crm.chery-prod".p ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$ BEGIN NULL; END; $$;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0018 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0019

The COPY statement was not translated to COPY INTO.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0019 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The copy statement was not translated to copy into. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
COPY t1 FROM 's3://bucket/key' FORMAT AS PARQUET;
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0019 - THE COPY STATEMENT WAS NOT TRANSLATED TO COPY INTO: a PARQUET load has no column-by-position COPY INTO equivalent ***/!!!
COPY t1 FROM 's3://bucket/key' FORMAT AS PARQUET;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0019 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0020

Redshift VARCHAR byte-width truncation is not supported for non-ASCII literals

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0020 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. Redshift varchar byte-width truncation is not supported for non-ascii literals. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT ('éé'::"VARCHAR")::VARCHAR(1) AS V;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ('éé' :: VARCHAR) :: VARCHAR(1) !!!RESOLVE EWI!!! /*** SSC-EWI-RS0020 - REDSHIFT VARCHAR SIZE LIMITS USE UTF-8 BYTES, AND THIS NON-ASCII LITERAL CANNOT BE TRUNCATED SAFELY FOR VARCHAR(1) IN SNOWFLAKE. REVIEW THE CAST ***/!!! AS V;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0020 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0021

COPY INTO was produced, but EXECUTE IMMEDIATE cannot bind the runtime FROM locations.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0021 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. Copy into was produced, but execute immediate cannot bind the runtime from locations from multiple branches with a single using list. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE PROCEDURE load_noelse()
AS $$
DECLARE
  sql_v varchar(1000);
  s3_path varchar(300);
  DeployEnvironment varchar(259) := 'prod';
BEGIN
  IF DeployEnvironment = 'prod' THEN
    s3_path := 's3://steam-user-data/email-appid/';
  END IF;
  sql_v := 'copy email_appid_temp from ''' || s3_path || ''' iam_role default format as csv';
  EXECUTE sql_v;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE load_noelse ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
  $$
    DECLARE
      sql_v varchar(1000);
      s3_path varchar(300);
      DeployEnvironment varchar(259) := 'prod';
    BEGIN
      IF (DeployEnvironment = 'prod') THEN
        s3_path := 's3://steam-user-data/email-appid/';
      END IF;
      sql_v := 'COPY INTO email_appid_temp
FROM ?
STORAGE_INTEGRATION = s3_path_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = ''"'')';
      !!!RESOLVE EWI!!! /*** SSC-EWI-RS0021 - COPY INTO WAS PRODUCED, BUT EXECUTE IMMEDIATE CANNOT BIND THE RUNTIME FROM LOCATIONS FROM MULTIPLE BRANCHES WITH A SINGLE USING LIST. ***/!!!
      --** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 's3_path_integration' WITH ACCESS TO 's3://steam-user-data/email-appid/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
      --** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 's3_path_integration' WITH ACCESS TO 's3_path' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
      EXECUTE IMMEDIATE :sql_v;
    END;
  $$;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0021 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0022

The Redshift outer-join marker could not be safely converted.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0022 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. The Redshift (+) outer-join predicate was not converted because it is not a provable one-sided equality conjunction. Review the emitted ansi predicate for equivalence. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT
   A.COL1,
   C.COL1
FROM
   table1 A,
   table2 B,
   table3 C
WHERE
   A.COL1 = B.COL1(+)
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   A.COL1,
   C.COL1
FROM
   table1 A,
   table2 B,
   table3 C
WHERE A.COL1 =
             !!!RESOLVE EWI!!! /*** SSC-EWI-RS0022 - THE REDSHIFT (+) OUTER-JOIN PREDICATE WAS NOT CONVERTED BECAUSE IT IS NOT A PROVABLE ONE-SIDED EQUALITY CONJUNCTION. REVIEW THE EMITTED ANSI PREDICATE FOR EQUIVALENCE. ***/!!! B.COL1;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0022 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.

## SSC-EWI-RS0023

Pending SnowConvert AI translation for an ambiguous quoted function overload.

### Severity

Medium

#### Description

SnowConvert AI reports SSC-EWI-RS0023 while converting Redshift code because it cannot reproduce the source behavior in Snowflake. Pending SnowConvert AI translation for an ambiguous quoted function overload. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE FUNCTION "ora$case" (x integer)
RETURNS character varying
IMMUTABLE
AS $$ SELECT 'int'; $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION "Ora$Case" (x character varying)
RETURNS character varying
IMMUTABLE
AS $$ SELECT 'varchar'; $$ LANGUAGE sql;

SELECT ora$case('text'::varchar), ora$case(1);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION "ora$case" (x integer)
RETURNS VARCHAR
LANGUAGE sql
IMMUTABLE
AS
  $$
    SELECT
      'int'
  $$
;
CREATE OR REPLACE FUNCTION "Ora$Case" (x VARCHAR)
RETURNS VARCHAR
LANGUAGE sql
IMMUTABLE
AS
  $$
    SELECT
      'varchar'
  $$
;
SELECT
  ora$case('text' :: varchar) !!!RESOLVE EWI!!! /*** SSC-EWI-RS0023 - PENDING SNOWCONVERT AI TRANSLATION FOR AN AMBIGUOUS QUOTED FUNCTION OVERLOAD 'ora$case'. ***/!!!,
  ora$case(1) !!!RESOLVE EWI!!! /*** SSC-EWI-RS0023 - PENDING SNOWCONVERT AI TRANSLATION FOR AN AMBIGUOUS QUOTED FUNCTION OVERLOAD 'ora$case'. ***/!!!;
```

#### Best Practices

Review the construct marked SSC-EWI-RS0023 and rewrite it with a Snowflake pattern that keeps the behavior you need. SnowConvert AI leaves the statement marked because the conversion could not be completed automatically.
