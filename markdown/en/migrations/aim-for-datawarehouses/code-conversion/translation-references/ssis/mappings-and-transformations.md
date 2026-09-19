# SSIS - Mappings and transformations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This page shows how each SSIS Data Flow component is converted into a [dbt](/user-guide/data-engineering/dbt-projects-on-snowflake) model, with a before and after example for each. For the supported-component matrix and the Control Flow deep-dives, see the [SSIS overview](README).

A Data Flow Task becomes a dbt project. Within that project, each component becomes a SQL model: source reads become `stg_` staging models, transformations become `int_` models, and destinations become models named after the target table. The examples below are taken from the test suite.

## Sources and staging

### OLE DB Source

An OLE DB Source becomes a **staging model** that reads from a table declared in `sources.yml`.

#### Conversion behavior

In table or view access mode, the staging model is named `stg_raw__<component>_<table>` and selects every column that the component exposes, aliasing each one to its output name. The table itself isn’t hardcoded: the model reads through `{{ source('raw', '<table>') }}`, and a generated `sources.yml` lists the tables that the package reads.

In SQL command access mode, the component runs a query instead of naming a table. The query becomes the body of the staging model and is converted as embedded SQL. Every table that the query reads is replaced with a `{{ source('raw', '<table>') }}` reference and gets its own entry in `sources.yml`, so a two-table join produces two entries. When the migration input doesn’t include the definitions of those tables, the model is flagged with [SSC-FDM-0007](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007).

#### Example

The first example uses table or view access mode.

`sources.yml`:

Copy code

```
version: 2
sources:
  - name: raw
    schema: YOUR_SCHEMA
    database: YOUR_DB
    tables:
      - name: DimCustomer
```

Snowflake (`stg_raw__ole_db_source_dimcustomer.sql`):

Copy code

```
SELECT
    CustomerKey AS CustomerKey,
    GeographyKey AS GeographyKey,
    CustomerAlternateKey AS CustomerAlternateKey,
    Title AS Title,
    FirstName AS FirstName,
    MiddleName AS MiddleName,
    LastName AS LastName,
    NameStyle AS NameStyle,
    BirthDate AS BirthDate,
    MaritalStatus AS MaritalStatus,
    Suffix AS Suffix,
    Gender AS Gender,
    EmailAddress AS EmailAddress,
    YearlyIncome AS YearlyIncome,
    TotalChildren AS TotalChildren,
    NumberChildrenAtHome AS NumberChildrenAtHome,
    EnglishEducation AS EnglishEducation,
    SpanishEducation AS SpanishEducation,
    FrenchEducation AS FrenchEducation,
    EnglishOccupation AS EnglishOccupation,
    SpanishOccupation AS SpanishOccupation,
    FrenchOccupation AS FrenchOccupation,
    HouseOwnerFlag AS HouseOwnerFlag,
    NumberCarsOwned AS NumberCarsOwned,
    AddressLine1 AS AddressLine1,
    AddressLine2 AS AddressLine2,
    Phone AS Phone,
    DateFirstPurchase AS DateFirstPurchase,
    CommuteDistance AS CommuteDistance
FROM
    {{ source('raw', 'DimCustomer') }}
```

The second example uses SQL command access mode, where the component runs a join across two tables.

SSIS (the component’s SQL command):

Copy code

```
SELECT d.CustomerKey as CustomerKey, f.UnitPrice From DimCustomer d inner join FactInternetSales f on  d.CustomerKey = f.CustomerKey
```

Snowflake (`stg_raw__ole_db_source.sql`):

Copy code

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "DimCustomer", "FactInternetSales" **
SELECT
d.CustomerKey as CustomerKey,
f.UnitPrice
From
{{ source('raw', 'DimCustomer') }} d
inner join
{{ source('raw', 'FactInternetSales') }} f
on d.CustomerKey = f.CustomerKey
```

`sources.yml`:

Copy code

```
version: 2
sources:
  - name: raw
    schema: YOUR_SCHEMA
    database: YOUR_DB
    tables:
      - name: DimCustomer
      - name: FactInternetSales
```

#### Limitations

`sources.yml` is generated with `YOUR_DB` and `YOUR_SCHEMA` placeholders. Replace them with your Snowflake database and schema before you run the project.

### Excel Source

An Excel Source becomes a **staging model** that reads the worksheet through the `excel_source_udf` Python UDF.

#### Conversion behavior

The workbook is bound to the landing stage, and an `excel_raw_data` CTE reads it with `TABLE(excel_source_udf('<stage path>', '<worksheet>', '<HDR flag>'))`. A `parsed_data` CTE then types each column: text columns are cast with `:: VARCHAR`, and numeric, date, timestamp, time, and Boolean columns use the matching `TRY_TO_` function, so a value that can’t be parsed becomes null instead of failing the load. The original Excel connection string is kept as a comment at the top of the model. When the connection sets `HDR=NO`, the worksheet has no header row and the columns are named `F1`, `F2`, and so on.

The workbook is also inventoried for ingestion, under the package folder alone: an Excel connection manager adds no segment of its own, so the manifest entry and the UDF read the same `ssis/<package>/` prefix.

#### Example

Snowflake (`stg_raw__excel_source.sql`):

Copy code

```
--Original Excel path: Provider=Microsoft.ACE.OLEDB.16.0;Data Source=C:\data\sales_data.xlsx;Extended Properties="Excel 12.0 XML;HDR=YES";
WITH excel_raw_data AS
(
   SELECT
      data
   FROM
      TABLE(excel_source_udf('@public.landing_stage/ssis/Package/sales_data.xlsx', 'Sales', 'YES'))
),
parsed_data AS
(
   SELECT
      data['ProductName'] :: VARCHAR AS ProductName,
      TRY_TO_DOUBLE(data['Quantity'] :: VARCHAR) AS Quantity,
      TRY_TO_DOUBLE(data['UnitPrice'] :: VARCHAR) AS UnitPrice,
      TRY_TO_DOUBLE(data['TotalAmount'] :: VARCHAR) AS TotalAmount
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
```

#### Limitations

An error output that uses the `RedirectRow` disposition can’t be translated directly. The model still reads the worksheet the same way, but it’s flagged with [SSC-EWI-SSIS0028](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0028) and the component is reported as `Partial` in the assessment report. Use `TRY_TO_*` functions with error flag columns for defensive error handling, and create separate error-capture models if needed.

### ADO.NET Source

An ADO.NET Source becomes a **staging model** in the same way an OLE DB Source does.

#### Conversion behavior

In table or view access mode, the model selects every column that the component exposes, aliases each one to its output name, and reads the table through `{{ source('raw', '<table>') }}`. The schema qualifier in the component’s table or view name is dropped from the source reference, because the schema comes from `sources.yml`.

#### Example

Snowflake (`stg_raw__ado_net_source.sql`), for a component that reads `"dbo"."Departments"`:

Copy code

```
SELECT
   dept_name AS dept_name,
   id AS id
FROM
   {{ source('raw', 'Departments') }}
```

### Oracle Source

An Oracle Source becomes a **staging model** that reads the Oracle table through a dbt source.

#### Conversion behavior

In table access mode, the component’s table name resolves the source table, the schema qualifier is dropped from the source reference, and each column is aliased to its output name. The Oracle SQL command access mode is normalized to the OLE DB SQL command mode, so the query itself is converted as embedded SQL rather than as part of the component.

#### Example

Snowflake (`stg_raw__oracle_source.sql`), for a component that reads `"HR"."DEPARTMENTS"`:

Copy code

```
SELECT
   dept_id AS dept_id,
   dept_name AS dept_name
FROM
   {{ source('raw', 'DEPARTMENTS') }}
```

#### Limitations

When an Oracle Source uses a SQL command and that query can’t be converted to Snowflake SQL, the staging model keeps the original statement as a comment and is flagged with [SSC-EWI-SSIS0003](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0003):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL CANNOT BE CONVERTED FROM ETL TO SNOWFLAKE SQL ***/!!!
--SELECT employee_id, full_name, department FROM hr.employees WHERE active = 1
SELECT
   *
FROM
   DUAL
```

### Flat File Source

A Flat File Source becomes a **staging model** that reads the file from the landing stage through a generated file format.

#### Conversion behavior

The staging model is named `stg_flat_file__<component>` and reads the file positionally: the first column becomes `$1`, the second `$2`, and so on, each cast to the type that the connection manager declares and aliased to the column name. The file itself is read from `@public.landing_stage/ssis/<package>/<connection manager>/<file>`, and the flat file connection manager becomes a named file format called `<package>_<data flow>_<component>` that carries the field delimiter, the encoding that matches the code page, and `NULL` handling.

That prefix follows the connection manager’s identity. A package-local connection manager binds `ssis/<package>/<connection manager>/`, while a project-level one binds `ssis/projects/<connection manager>_<identity>/`, so every package that resolves the same project connection manager reads one prefix. A connection manager driven by a [ForEach File Enumerator](README#foreach-loop-containers) also carries the enumerated folder, and the read becomes a pattern over that prefix rather than a single file, with the nested path segments included when the enumerator is recursive.

When the connection manager puts column names in the first data row, the model filters that row out with `WHERE METADATA$FILE_ROW_NUMBER > 1`. When the component doesn’t retain `NULL` values, each column is wrapped in `COALESCE` with a default for its type, so an empty field becomes that default instead of `NULL`. When the component retains `NULL` values, the same model is generated without the `COALESCE` calls. A fixed-width connection manager is read with `SUBSTR` over `$1` instead of positional columns.

The read is also inventoried for ingestion. A delimited connection manager becomes a source in the generated ingestion manifest, which is what lands the file under the prefix the model reads. A Multiple Flat Files connection manager isn’t inventoried, and a fixed-width one is inventoried only when every column declares a width. For how a file reaches that prefix, see the [SSIS overview](README).

#### Example

Snowflake (`stg_flat_file__flat_file_source.sql`), for a comma-delimited file with a header row and retain `NULL`s turned off:

Copy code

```
SELECT
   COALESCE($1, '') :: VARCHAR(50) AS col_a,
   COALESCE($2, '') :: VARCHAR(50) AS col_b,
   COALESCE($3, '') :: VARCHAR(50) AS col_c
FROM
   @public.landing_stage/ssis/TestPackage/MyFlatFile/input.csv (FILE_FORMAT => 'TestPackage_Data_Flow_Task_Flat_File_Source')
WHERE
   METADATA$FILE_ROW_NUMBER > 1
```

Snowflake (`file_formats.sql`):

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS TestPackage_Data_Flow_Task_Flat_File_Source
TYPE = 'CSV'
FIELD_DELIMITER = ','
ENCODING = 'WINDOWS1252'
EMPTY_FIELD_AS_NULL = TRUE;
```

#### Limitations

A fixed-width connection manager can only be read when every column declares a width. When one or more columns have no width, the layout can’t be resolved: the staging model falls back to selecting `NULL` for each column, is flagged with `SSC-EWI-SSIS0051`, and no file format is generated for it.

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0051 - SNOWCONVERT AI WAS UNABLE TO RESOLVE THE FIXED-WIDTH COLUMN LAYOUT. ONE OR MORE COLUMNS HAVE NO COLUMN WIDTH. ***/!!!
SELECT
   null AS col_a,
   null AS col_b
```

## Row-level transformations

### Derived Column

A Derived Column becomes an `int_` model whose `SELECT` list carries one expression per derived column.

#### Conversion behavior

The input rows are wrapped in a `source_data` CTE that reads from the upstream model with `{{ ref() }}`. Each SSIS expression becomes its Snowflake equivalent in the `SELECT` list: string concatenation stays `||`, and date parts become the matching Snowflake function. Columns that pass through unchanged are selected alongside the derived ones, so downstream components still see the full row.

#### Example

Snowflake (`int_derived_column.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      FirstName,
      MiddleName,
      LastName,
      BirthDate
   FROM
      {{ ref('stg_raw__ole_db_source_dimcustomer') }}
)
SELECT
   FirstName || ' ' || MiddleName || ' ' || LastName AS FullName,
   YEAR(BirthDate) AS BirthDateYear,
   FirstName AS FirstName,
   MiddleName AS MiddleName,
   LastName AS LastName,
   BirthDate AS BirthDate
FROM
   source_data
```

### Data Convert

A Data Convert becomes an `int_` model that casts each converted column to the target type.

#### Conversion behavior

Each conversion becomes a `::` cast aliased to the component’s output column name. When the component adds a converted copy instead of replacing the column, the original column is kept and the cast column is emitted next to it under its SSIS output name, such as `"Copy of BirthDate"`.

#### Example

Snowflake (`int_data_conversion.sql`, column list shortened):

Copy code

```
WITH source_data AS
(
   SELECT
      GeographyKey,
      BirthDate,
      TotalChildren,
      CustomerKey
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   GeographyKey,
   BirthDate,
   TotalChildren,
   CustomerKey,
   GeographyKey :: BINARY(50) AS "Copy of GeographyKey",
   BirthDate :: DATE AS "Copy of BirthDate",
   TotalChildren :: NUMERIC(18, 2) AS "Copy of TotalChildren"
FROM
   source_data AS sd
```

### Character Map

A Character Map becomes an `int_` model that applies supported character operations to string columns and passes other columns through unchanged.

#### Conversion behavior

Uppercase and lowercase operations become the Snowflake `UPPER` and `LOWER` functions. The generated model reads the upstream model through a `source_data` CTE and applies each operation in the `SELECT` list. Operations can replace a column in place or create a new output column.

#### Example

Snowflake (`int_character_map.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      FullName,
      Score
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   UPPER(FullName) AS FullName,
   Score
FROM
   source_data
```

#### Limitations

Only uppercase and lowercase operations are translated. For unsupported map flags, such as byte reversal, the column passes through unchanged and the generated model includes `SSC-EWI-SSIS0019`.

### OLE DB Command

An OLE DB Command becomes an **incremental model** that applies the component’s parameterized `DELETE` or `UPDATE` to the table that the command names.

#### Conversion behavior

The model is named after the target table and is generated under `models/marts/`. Its `config` block sets `materialized='incremental'` and an incremental strategy that matches the command: `delete_only` for a `DELETE` and `update_only` for an `UPDATE`. The `WHERE` clause parameters become the `unique_key`, as a single value for one key column and as an array for a composite key, and a schema-qualified command also sets `schema`. Each model is tagged `oledb_command` plus `delete_operation` or `update_operation`.

A `DELETE` model selects only the key columns. An `UPDATE` model also selects the `SET` columns and lists them in `merge_update_columns`. The conversion adds the matching strategy macro to the project, `get_incremental_delete_only_sql` or `get_incremental_update_only_sql`, which runs a `MERGE INTO` that ends in `WHEN MATCHED THEN DELETE` or `WHEN MATCHED THEN UPDATE SET`.

#### Example

SSIS (the component’s SQL command):

Copy code

```
DELETE FROM dbo.Contacts WHERE ContactID = ?
```

With `ContactID` mapped to that parameter, the conversion generates `models/marts/Contacts.sql`. The model’s `config` block sets `materialized='incremental'`, `incremental_strategy='delete_only'`, `unique_key='ContactID'`, and `schema='dbo'`, the model carries the `oledb_command` and `delete_operation` tags, and its `SELECT` returns only `ContactID`.

## Combining data

### Lookup

A Lookup becomes an `int_` model that joins the input rows to a deduplicated lookup source.

#### Conversion behavior

The generated model has two CTEs: `lookup_reference` reads the reference model and keeps one row per lookup key with `QUALIFY ROW_NUMBER() = 1`, and `input_data` reads the upstream model. The two are combined with an `INNER JOIN` on the lookup condition, and the returned lookup columns are appended to the input columns.

When the lookup key can contain nulls, the join uses `EQUAL_NULL` so that null keys match the way they do in SSIS.

Chained lookups become one model each. The second Lookup reads the first one’s model with `{{ ref('int_lookup') }}` rather than re-reading the source.

#### Example

Snowflake (`int_lookup.sql`), a lookup with no deterministic ordering:

Copy code

```
WITH lookup_reference AS
    (
        SELECT
            CustomerKey ,
            FirstName
        FROM
            {{ ref('stg_raw__lookup') }}
    QUALIFY
    ROW_NUMBER() OVER (
    PARTITION BY
    CustomerKey
    ORDER BY
   (
    SELECT
--** SSC-FDM-SSIS0001 - REPLACE NULL WITH APPROPRIATE ORDER BY COLUMN(S) TO ENSURE DETERMINISTIC FIRST MATCH SELECTION. SSIS LOOKUP RETURNS THE FIRST MATCHING ROW, SO PROPER ORDERING IS REQUIRED WHEN MULTIPLE ROWS MATCH THE JOIN CONDITION. **
    null
    )) = 1
    ),
    input_data AS
   (
SELECT
    ProductKey ,
    OrderDateKey ,
    CustomerKey ,
    OrderQuantity ,
    TotalPrice ,
    OrderDate
FROM
    {{ ref('stg_raw__ole_db_source') }}
    )
SELECT
    input_data.ProductKey,
    input_data.OrderDateKey,
    input_data.CustomerKey,
    input_data.OrderQuantity,
    input_data.TotalPrice,
    input_data.OrderDate,
    lookup_reference.FirstName CustomerName
FROM
    input_data
        INNER JOIN
    lookup_reference
    ON lookup_reference.CustomerKey = input_data.CustomerKey
```

Snowflake (`int_lookup_1.sql`), the second Lookup in the same Data Flow, with sort columns available and a null-safe join:

Copy code

```
WITH lookup_reference AS
    (
        SELECT
            DateKey ,
            CalendarYear
        FROM
            {{ ref('stg_raw__lookup_1') }}
    QUALIFY
    ROW_NUMBER() OVER (
    PARTITION BY
    DateKey
    ORDER BY DateKey, FullDateAlternateKey) = 1
    ),
    input_data AS
   (
SELECT
    CustomerName ,
    ProductKey ,
    OrderDateKey ,
    CustomerKey ,
    OrderQuantity ,
    TotalPrice ,
    OrderDate
FROM
    {{ ref('int_lookup') }}
    )
SELECT
    input_data.CustomerName,
    input_data.ProductKey,
    input_data.OrderDateKey,
    input_data.CustomerKey,
    input_data.OrderQuantity,
    input_data.TotalPrice,
    input_data.OrderDate,
    lookup_reference.CalendarYear
FROM
    input_data
        INNER JOIN
    lookup_reference
    ON EQUAL_NULL(lookup_reference.DateKey, input_data.OrderDateKey)
```

#### Limitations

An SSIS Lookup returns the first matching row. When the conversion can’t determine a deterministic order for the lookup source, it emits [SSC-FDM-SSIS0001](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0001) and leaves `null` in the `ORDER BY`. Replace that `null` with the columns that make the match deterministic, otherwise the row that Snowflake keeps can vary between runs.

### Fuzzy Lookup

A Fuzzy Lookup becomes an `int_` model that matches rows by string similarity instead of by equality.

#### Conversion behavior

The generated model has two CTEs: `lookup_reference` reads the reference model, and `input_data` reads the upstream model. The two are combined with a `CROSS JOIN`, and each fuzzy-matched column pair is scored with `JAROWINKLER_SIMILARITY` divided by `100.0`. A `WHERE` clause keeps only the pairs that meet the component’s minimum similarity, and `QUALIFY ROW_NUMBER() <= 1`, partitioned by the input columns and ordered by the similarity score, keeps the best match for each input row.

The model returns the passthrough input columns, the reference columns that the component copies, a `_Similarity` and a `_Confidence` column, and one `_Similarity_<column>` column per fuzzy-matched column. Copied reference columns keep the output names from the SSIS component. In the example below, the copied `CompanyName` column is named `RefCompanyName` because that is the name in the package, not because the conversion adds a prefix.

#### Example

Snowflake (`int_fuzzy_lookup.sql`):

Copy code

```
--** SSC-FDM-SSIS0024 - THE SSIS FUZZYLOOKUP TRANSFORMATION USES A TOKEN-BASED SIMILARITY ALGORITHM. THE CONVERTED SQL USES JAROWINKLER_SIMILARITY WHICH IS A CHARACTER-LEVEL ALGORITHM. SIMILARITY SCORES MAY DIFFER BETWEEN SOURCE AND TARGET. _CONFIDENCE IS APPROXIMATED AS _SIMILARITY (NO EQUIVALENT RELATIVE CONFIDENCE METRIC IN SNOWFLAKE). UNMATCHED INPUT ROWS ARE EXCLUDED — SSIS PRESERVES ALL INPUT ROWS WITH SIMILARITY=0 AND NULL REFERENCE COLUMNS. **
WITH lookup_reference AS
(
   SELECT
      RefID ,
      CompanyName ,
      Industry
   FROM
      {{ ref('stg_raw__fuzzy_lookup') }}
),
input_data AS
(
   SELECT
      InputID InputID,
      CompanyName CompanyName,
      City City
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   input_data.CompanyName,
   lookup_reference.CompanyName RefCompanyName,
   lookup_reference.Industry,
   JAROWINKLER_SIMILARITY(input_data.CompanyName, lookup_reference.CompanyName) / 100.0 AS _Similarity,
   JAROWINKLER_SIMILARITY(input_data.CompanyName, lookup_reference.CompanyName) / 100.0 AS _Confidence,
   JAROWINKLER_SIMILARITY(input_data.CompanyName, lookup_reference.CompanyName) / 100.0 AS _Similarity_CompanyName
FROM
   input_data
   CROSS JOIN lookup_reference
WHERE
   JAROWINKLER_SIMILARITY(input_data.CompanyName, lookup_reference.CompanyName) / 100.0 >= 0.3
QUALIFY
   ROW_NUMBER() OVER (
   PARTITION BY
      input_data.InputID, input_data.CompanyName, input_data.City
   ORDER BY
      JAROWINKLER_SIMILARITY(input_data.CompanyName, lookup_reference.CompanyName) DESC) <= 1
```

The reference table is read through its own staging model (`stg_raw__fuzzy_lookup.sql`) and is listed in the generated `sources.yml`.

#### Limitations

Every converted Fuzzy Lookup emits `SSC-FDM-SSIS0024`, because the two matching algorithms don’t behave identically. SSIS uses token-based similarity, while `JAROWINKLER_SIMILARITY` is character-level, so scores can differ between source and target. `_Confidence` is approximated as `_Similarity`, since Snowflake has no equivalent relative confidence metric. Unmatched input rows are excluded from the output, while SSIS keeps them with a similarity of 0 and null reference columns.

### Union All

A Union All becomes an `int_` model that combines its inputs with `UNION ALL`.

#### Conversion behavior

Each input becomes its own CTE (`input_1`, `input_2`, and so on) that reads one upstream model and renames its columns to the Union All output names. The CTEs are then combined with `UNION ALL` in input order, so columns line up even when the sources name them differently.

#### Example

Snowflake (`int_union_all.sql`):

Copy code

```
WITH input_1 AS
(
   SELECT
      CustomerKey Key,
      FirstName Name
   FROM
      {{ ref('stg_raw__ole_db_source') }}
),
input_2 AS
(
   SELECT
      FirstName Name,
      EmployeeKey Key
   FROM
      {{ ref('stg_raw__ole_db_source_1') }}
),
input_3 AS
(
   SELECT
      ResellerKey Key,
      ResellerName Name
   FROM
      {{ ref('stg_raw__ole_db_source_2') }}
)
SELECT
   input_1.Key Key,
   input_1.Name Name
FROM
   input_1
UNION ALL
SELECT
   input_2.Key Key,
   input_2.Name Name
FROM
   input_2
UNION ALL
SELECT
   input_3.Key Key,
   input_3.Name Name
FROM
   input_3
```

### Merge

A Merge becomes an `int_` model that stacks its two inputs with `UNION ALL`.

#### Conversion behavior

Each input becomes its own CTE, `merge_input_1` and `merge_input_2`, that reads one upstream model and renames its columns to the Merge output names. The two CTEs are then combined with `UNION ALL`. When one input doesn’t supply a column that the other one does, that branch selects `NULL` under the output column name, so both branches produce the same shape.

#### Example

Snowflake (`int_merge.sql`), where only the second input supplies `Cost`:

Copy code

```
--** SSC-FDM-SSIS0002 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. THE SSIS MERGE TRANSFORMATION ASSUMES SORTED INPUTS AND NATURALLY PRODUCES A SORTED, DETERMINISTIC OUTPUT. THE EQUIVALENT SQL UNION ALL DOES NOT GUARANTEE ORDER. **
WITH merge_input_1 AS
(
   SELECT
      ProductID ProductID,
      ProductName ProductName,
      Price Price,
      CategoryID CategoryID
   FROM
      {{ ref('stg_raw__ole_db_source') }}
),
merge_input_2 AS
(
   SELECT
      ProductID ProductID,
      ProductName ProductName,
      Price Price,
      CategoryID CategoryID,
      Cost Cost
   FROM
      {{ ref('stg_raw__ole_db_source_1') }}
)
SELECT
   merge_input_1.ProductID ProductID,
   merge_input_1.ProductName ProductName,
   merge_input_1.Price Price,
   merge_input_1.CategoryID CategoryID,
   null Cost
FROM
   merge_input_1
UNION ALL
SELECT
   merge_input_2.ProductID ProductID,
   merge_input_2.ProductName ProductName,
   merge_input_2.Price Price,
   merge_input_2.CategoryID CategoryID,
   merge_input_2.Cost Cost
FROM
   merge_input_2
```

#### Limitations

An SSIS Merge assumes sorted inputs and produces a sorted, deterministic output. `UNION ALL` doesn’t guarantee order, so every converted Merge emits [SSC-FDM-SSIS0002](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0002). Add an `ORDER BY` clause if anything downstream depends on the order.

### Merge Join

A Merge Join becomes an `int_` model that joins its two inputs with a SQL join.

#### Conversion behavior

The model reads both upstream models with `{{ ref() }}` and aliases each one to its model name, so the join predicates and the output columns are qualified. The component’s join type determines the SQL join: a left outer join becomes `LEFT JOIN`. Each pair of join columns becomes an equality predicate, and multiple pairs are combined with `AND`. Output columns keep the names the component gives them, quoted when the name contains a space. When the component is set to treat `NULL`s as equal, each predicate uses `EQUAL_NULL(...)` instead of `=`.

#### Example

Snowflake (`int_merge_join.sql`), for a left outer join on two columns:

Copy code

```
SELECT
   --** SSC-FDM-SSIS0004 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. THE SSIS MERGE JOIN TRANSFORMATION ASSUMES SORTED INPUTS AND NATURALLY PRODUCES A SORTED, DETERMINISTIC OUTPUT. THE EQUIVALENT SQL JOIN DOES NOT GUARANTEE ORDER. **
   employeeassignments.employee_id,
   tasks.project_id AS "project identifier",
   employeeassignments.assignment_start_date,
   employeeassignments.assigned_hours,
   tasks.task_id,
   tasks.task_name,
   tasks.task_status
FROM
   {{ ref('stg_raw__employeeassignments') }} AS employeeassignments
   LEFT JOIN
      {{ ref('stg_raw__tasks') }} AS tasks
      ON employeeassignments.employee_id = tasks.employee_id
      AND employeeassignments.project_id = tasks.project_id
```

#### Limitations

An SSIS Merge Join assumes sorted inputs and produces a sorted, deterministic output. A SQL join doesn’t guarantee order, so every converted Merge Join emits [SSC-FDM-SSIS0004](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0004). Add an `ORDER BY` clause if anything downstream depends on the order.

## Aggregation and ranking

### Aggregate

An Aggregate becomes an `int_` model that groups rows and applies aggregate functions.

#### Conversion behavior

Group-by columns appear in both the `SELECT` and `GROUP BY` clauses. Aggregate output columns become the corresponding Snowflake functions: `COUNT`, `COUNT(DISTINCT ...)`, `SUM`, `AVG`, `MIN`, or `MAX`. When no group-by columns are configured, the functions aggregate the entire input. When the component contains only group-by columns, the generated query groups by those columns without applying aggregate functions.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| `AggregationType` | `GROUP BY` or an aggregate function | Values map to Group By, Count, Count All, Count Distinct, Sum, Average, Minimum, and Maximum. |
| `AggregationColumnId` | Source column reference | Identifies the input column used by the group or aggregate expression. |
| `AggregationComparisonFlags` | Manual review | A nonzero value emits [`SSC-EWI-0073`](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073) because SSIS string-comparison options don’t have direct Snowflake equivalents. |
| `IsBig` | Manual review | A true value emits [`SSC-EWI-0073`](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073). Snowflake handles large numeric values natively. |

Expand

Show lessSee more

#### Example

Snowflake (`int_aggregate.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      department,
      salary
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   department,
   SUM(salary) AS total_salary
FROM
   source_data
GROUP BY
   department
```

### Pivot

A Pivot becomes an `int_` model that converts row values into columns by using conditional aggregation.

#### Conversion behavior

Set-key and passthrough columns appear in the `SELECT` and `GROUP BY` clauses. Each declared pivot-key value becomes an output column that uses `MAX(CASE WHEN ... THEN ... END)`. The Pivot always generates an intermediate model.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| `PassThroughUnmatchedPivotKeys` | Conditional aggregation | When enabled, unmatched keys produce null values instead of a separate output and the model emits [`SSC-FDM-SSIS0021`](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0021). |
| `PivotUsage` | Column role | Maps a column to passthrough, set key, pivot key, or pivot value behavior. |
| `SourceColumn` | Source column reference | Identifies the input column from which an output column is derived. |
| `PivotKeyValue` | `CASE` comparison value | Maps a specific pivot-key value to its output column. |

Expand

Show lessSee more

#### Example

Snowflake (`int_pivot.sql`):

Copy code

```
--** SSC-FDM-SSIS0022 - THE SSIS PIVOT TRANSFORMATION ASSUMES INPUT DATA IS SORTED BY THE SET KEY COLUMN. THE CONVERTED SQL USES GROUP BY WHICH DOES NOT REQUIRE OR PRESERVE SORT ORDER. VERIFY THAT DOWNSTREAM CONSUMERS DO NOT DEPEND ON SORTED OUTPUT. **
WITH source_data AS
(
   SELECT
      CustomerName,
      Product,
      Quantity
   FROM
      {{ ref('stg_raw__source') }}
)
SELECT
   CustomerName,
   MAX(CASE
      WHEN Product = 'Bike'
         THEN Quantity
   END) AS Bike,
   MAX(CASE
      WHEN Product = 'Helmet'
         THEN Quantity
   END) AS Helmet,
   MAX(CASE
      WHEN Product = 'Gloves'
         THEN Quantity
   END) AS Gloves
FROM
   source_data
GROUP BY
   CustomerName
```

#### Limitations

SSIS expects Pivot input to be sorted by the set key. The generated Snowflake query uses `GROUP BY`, which doesn’t require or preserve that order, so it emits [SSC-FDM-SSIS0022](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0022). Verify that downstream consumers don’t depend on sorted output.

### UnPivot

An UnPivot becomes an `int_` model that converts input columns into rows.

#### Conversion behavior

When all unpivoted columns map to one destination value column, the model uses Snowflake `UNPIVOT`. When they map to multiple destination columns, the model generates one filtered `SELECT` per pivot-key value and combines them with `UNION ALL`. Passthrough columns remain unchanged. An additional `UNION` preserves the SSIS behavior for input rows in which all unpivoted values are null.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| `PivotKeyValue` | Pivot-key literal or passthrough marker | A nonempty value identifies the source column in the unpivoted output. An empty value identifies a passthrough column. |
| `DestinationColumn` | Destination value column | Determines whether the model uses native `UNPIVOT` or the multiple-destination `UNION ALL` pattern. |
| `PivotKey` | Pivot-key output column | Identifies the output column that receives each `PivotKeyValue`. |

Expand

Show lessSee more

#### Example

Snowflake (`int_unpivot.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      Ham,
      Milk,
      Soda,
      Chips,
      customer,
      description
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   Sales,
   customer,
   description,
   q1 :: NUMERIC AS q1
FROM
   source_data UNPIVOT (q1 FOR Sales IN (Ham, Milk, Soda, Chips))
UNION
SELECT
   null AS Sales,
   customer,
   description,
   null AS q1
FROM
   source_data
WHERE
   Ham IS NULL
   AND Milk IS NULL
   AND Soda IS NULL
   AND Chips IS NULL
```

## Sorting

### Sort

A Sort becomes an `int_` model that orders the rows and keeps one row per sort key.

#### Conversion behavior

The input rows are wrapped in a `source_data` CTE. The model then applies `QUALIFY ROW_NUMBER() = 1` partitioned by the sort columns, which reproduces the Sort component’s removal of rows with duplicate sort values, and an `ORDER BY` that carries each sort column and its direction.

#### Example

Snowflake (`int_sort.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      name,
      salary
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   name,
   salary
FROM
   source_data
QUALIFY
   ROW_NUMBER()
   OVER (
   PARTITION BY (
      name)
   ORDER BY
      name ASC) = 1
ORDER BY
   name ASC
```

## Routing and normalizing

### Conditional Split

A Conditional Split becomes one `int_` model per output, including the default output.

#### Conversion behavior

Each output gets a model named `int_conditional_split_<output>` that wraps the upstream model in a `source_data` CTE, selects every input column, and filters with a `WHERE` clause. To reproduce SSIS first-match behavior, a group’s `WHERE` clause carries its own condition and then negates every condition declared above it. The default output’s model negates all of the conditions with `NOT COALESCE(<condition>, FALSE)`, which keeps rows whose conditions evaluate to `NULL` in the default output. Each downstream component reads the model for the output it’s connected to.

#### Example

The models below come from a Conditional Split that declares the conditions `BaseRate < 10`, `BaseRate < 20`, and `BaseRate < 40` in that order, plus a default output.

Snowflake (`int_conditional_split_low.sql`), the first group, which has no earlier condition to negate:

Copy code

```
WITH source_data AS
(
   SELECT
      EmployeeKey,
      FirstName,
      LastName,
      BaseRate
   FROM
      {{ ref('stg_raw__employees') }}
)
SELECT
   EmployeeKey,
   FirstName,
   LastName,
   BaseRate
FROM
   source_data
WHERE
   BaseRate < 10
```

Snowflake (`int_conditional_split_mid.sql`), the second group, which negates the first condition:

Copy code

```
WITH source_data AS
(
   SELECT
      EmployeeKey,
      FirstName,
      LastName,
      BaseRate
   FROM
      {{ ref('stg_raw__employees') }}
)
SELECT
   EmployeeKey,
   FirstName,
   LastName,
   BaseRate
FROM
   source_data
WHERE
   BaseRate < 20
   AND NOT (BaseRate < 10)
```

The third group follows the same pattern with every earlier condition inside one negation, so its filter is `BaseRate < 40 AND NOT (BaseRate < 10 OR BaseRate < 20)`.

Snowflake (`int_conditional_split_other_rates.sql`), the default output:

Copy code

```
WITH source_data AS
(
   SELECT
      EmployeeKey,
      FirstName,
      LastName,
      BaseRate
   FROM
      {{ ref('stg_raw__employees') }}
)
SELECT
   EmployeeKey,
   FirstName,
   LastName,
   BaseRate
FROM
   source_data
WHERE
   NOT COALESCE(BaseRate < 10, FALSE)
   AND NOT COALESCE(BaseRate < 20, FALSE)
   AND NOT COALESCE(BaseRate < 40, FALSE)
```

#### Limitations

A condition that can’t be converted to Snowflake SQL, such as one that references a package variable, is replaced with a `_` placeholder and flagged with [SSC-EWI-SSIS0002](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0002). The flag appears both in the group that owns the condition and in the default output’s negation of it, so fix the expression in every model that carries it.

For non-default outputs, earlier conditions are negated without `COALESCE`. If an earlier condition evaluates to `NULL`, SQL’s three-valued logic can exclude the row from a later output even when that later condition is true. Review nullable expressions and wrap them with `COALESCE(<condition>, FALSE)` where needed to preserve SSIS first-match behavior.

### Multicast

A Multicast becomes a single passthrough `int_` model.

#### Conversion behavior

In SSIS, a Multicast copies its input to two or more identical outputs. The generated `int_multicast` model reproduces the input: it selects every input column from the upstream model, without renaming or reordering. Each downstream branch reads this one model, so the fan-out comes from the model references rather than from the component itself. The conversion reports the component as successful and emits no issues.

#### Example

Snowflake (`int_multicast.sql`):

Copy code

```
SELECT
   CurrencyKey,
   CurrencyAlternateKey,
   CurrencyName
FROM
   {{ ref('stg_raw__ole_db_source') }}
```

### Cache

A Cache Transform becomes a passthrough `int_` model.

#### Conversion behavior

In SSIS, the Cache Transform writes its input to a Cache connection manager so that downstream Lookups can read it, and passes the same rows through unchanged. The generated model reproduces the passthrough part: it selects every input column from the upstream model, without renaming or reordering. Cache file persistence and cache index columns don’t appear in the generated SQL, because dbt materializations handle persistence and a downstream Lookup reads the model with its own query.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| `ConnectionName` | Not translated | References the Cache connection manager, which has no runtime equivalent in dbt. |
| `TreatDuplicateKeysAsError` | Informational notice | A true value emits `SSC-FDM-SSIS0027`. The passthrough SQL is generated either way. |
| `CacheColumnName` | Not translated | Column names are preserved from the upstream model in passthrough mode. |
| `usageType` | Source column reference | Always read-only for a Cache Transform, so every input column is passed through. |

Expand

Show lessSee more

#### Example

Snowflake (`int_cache_transform.sql`):

Copy code

```
SELECT
   name,
   salary
FROM
   {{ ref('stg_raw__ole_db_source') }}
```

#### Limitations

When the component sets `TreatDuplicateKeysAsError` to true, SSIS fails the package on a duplicate cache key. The generated model doesn’t enforce that check, so duplicate rows pass through unchanged and the model emits `SSC-FDM-SSIS0027`. The SQL runs correctly as a passthrough. If you need the validation, add a dbt uniqueness test or a Snowflake unique constraint.

## Keys and load strategy

### Row Count

A Row Count becomes a pass-through `int_` model that records the row count in the package variable.

#### Conversion behavior

The model is materialized as a view and selects every input column unchanged, so the component doesn’t alter the data flow. The count itself is captured by a `pre_hook` that calls the `m_update_row_count_variable` macro with the SSIS variable name, the relation to count, and the variable scope.

#### Example

Snowflake (`int_data_flow_task_row_count.sql`, column list shortened):

Copy code

```
{{ config(
    materialized='view',
    pre_hook="""{{ m_update_row_count_variable(
        variable_name='User_Variable',
        target_relation=ref('stg_raw__ole_db_source'),
        variable_scope='Package'
    ) }}"""
) }}
WITH source_data AS
(
   SELECT
      CustomerKey,
      GeographyKey,
      CustomerAlternateKey,
      Title
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
    sd.CustomerKey,
    sd.GeographyKey,
    sd.CustomerAlternateKey,
    sd.Title
FROM
    source_data AS sd
```

## Reuse and external logic

This series doesn’t convert an SSIS Mapplet equivalent. Shared logic stays inline in each Data Flow’s models.

## Targets

### OLE DB Destination

An OLE DB Destination becomes the model that writes the Data Flow’s output to the destination table.

#### Conversion behavior

The model is named after the destination component and carries a `config(alias=...)` that points at the destination table, so the table keeps its original name even when the component doesn’t. The model reads the last upstream model, aliases each column to the destination column name, and applies any cast that the column mapping requires.

#### Example

Snowflake (`ole_db_destination.sql`):

Copy code

```
{{ config(
    alias='newDimCustomer'
) }}
WITH source_data AS
(
   SELECT
      CustomerKey,
      AddressLine1,
      AddressLine2,
      FullName,
      BirthDateYear
   FROM
      {{ ref('stg_raw__ole_db_source_dimcustomer') }}
)
SELECT
    sd.CustomerKey AS CustomerKey,
    sd.AddressLine1 AS AddressLine1,
    sd.AddressLine2 AS AddressLine2,
    sd.FullName AS FullName,
    sd.BirthDateYear :: VARCHAR(50) AS BirthDateString
FROM
    source_data AS sd
```

### Excel Destination

An Excel Destination becomes the model that writes the Data Flow’s output, using the worksheet name as the model alias.

#### Conversion behavior

The model follows the same pattern as an OLE DB Destination: it reads the last upstream model in a `source_data` CTE and aliases each column to the destination column name. The `config(alias=...)` value is the worksheet name with its trailing `$`, surrounding quotes, and brackets removed, so `Sheet1$` becomes `Sheet1` and `'Sales Data$'` becomes `Sales Data`. When the component doesn’t name a worksheet, the model is generated without an alias.

#### Example

Snowflake (`excel_destination.sql`):

Copy code

```
{{ config(
    alias='Sheet1'
) }}
WITH source_data AS
(
   SELECT
      ProductName,
      Quantity,
      UnitPrice
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   sd.ProductName AS ProductName,
   sd.Quantity AS Quantity,
   sd.UnitPrice AS UnitPrice
FROM
   source_data AS sd
```

### Oracle Destination

An Oracle Destination becomes the model that writes the Data Flow’s output to the Oracle target table.

#### Conversion behavior

An Oracle Destination has no access mode property, so the conversion resolves the schema and table from the component’s table name. The table name becomes the model’s `config(alias=...)`, and the model reads the last upstream model in a `source_data` CTE and aliases each column to the destination column name.

#### Example

Snowflake (`oracle_destination.sql`), for a component that writes to `"HR"."EMPLOYEES"`:

Copy code

```
{{ config(
    alias='EMPLOYEES'
) }}
WITH source_data AS
(
   SELECT
      emp_id,
      emp_name
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   sd.emp_id AS emp_id,
   sd.emp_name AS emp_name
FROM
   source_data AS sd
```

### Flat File Destination

A Flat File Destination becomes a model under `models/marts/`, and, when the destination can be bound to the landing stage, an unload from that model back out to the stage.

#### Conversion behavior

The model is named after the component and carries a `config(alias=...)` that holds the flat file connection manager name. It reads the last upstream model in a `source_data` CTE and aliases each column to the destination column name, the same way an OLE DB Destination does. What the `config` block adds on top of that depends on the destination’s overwrite setting and on whether the connection manager can be bound to the stage:

- A **bound destination that overwrites** is materialized as a table and gets a `post_hook` that calls the generated `copy_into_stage` macro with the package’s landing prefix. The macro runs a `COPY INTO` from the model out to that stage path using a CSV file format built from the connection manager’s options. The conversion also adds `macros/copy_into_stage.sql` and the same shared `public.landing_stage` that direct COPY loads use.
- A **bound destination that appends** drops the `materialized='table'` setting and passes the connection manager’s field delimiter, text qualifier, and header setting to the macro along with `overwrite=false`.
- A **destination that can’t be bound** keeps the plain mart with no unload at all. This covers a fixed-width or ragged-right connection manager, a multi-file or plain file connection manager, and a connection manager that the package never declares.
- An eligible **Flat File Source that feeds a Flat File Destination set to overwrite** skips dbt entirely. The Data Flow must be a two-component passthrough flow with a supported source, a destination bound to the landing stage, and mapped columns. No mart and no macro are generated, and the Data Flow becomes a single stage-to-stage `COPY INTO` inside the package task. Other flows use the dbt model path. This is a different case from the direct COPY loads described later on this page, which move a Flat File Source into an OLE DB Destination.

#### Example

Snowflake (`models/marts/flat_file_destination.sql`), a bound destination that overwrites:

Copy code

```
{{ config(
    materialized='table',
    post_hook="{{ copy_into_stage('public.landing_stage/ssis/TestPackage/', record_delimiter='\\r\\n', header=true) }}",
    alias='MyFlatFile'
) }}
WITH source_data AS
(
   SELECT
      col_a,
      col_b
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   sd.col_a AS col_a,
   sd.col_b AS col_b
FROM
   source_data AS sd
```

Snowflake (`models/marts/flat_file_destination.sql`), the same destination set to append, with a pipe delimiter, a double-quote text qualifier, and no header row:

Copy code

```
{{ config(
    post_hook="{{ copy_into_stage('public.landing_stage/ssis/AppendPackage/', field_delimiter='|', field_optionally_enclosed_by='\"', record_delimiter='\\r\\n', header=false, overwrite=false) }}",
    alias='PipeFile'
) }}
WITH source_data AS
(
   SELECT
      col_a,
      col_b
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   sd.col_a AS col_a,
   sd.col_b AS col_b
FROM
   source_data AS sd
```

Snowflake (`models/marts/flat_file_currency_info.sql`), a destination that isn’t bound to the stage, so the model is generated without a `post_hook`:

Copy code

```
{{ config(
    materialized='table',
    alias='Currency Info'
) }}
WITH source_data AS
(
   SELECT
      CurrencyKey,
      CurrencyAlternateKey,
      CurrencyName
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   sd.CurrencyKey AS CurrencyKey,
   sd.CurrencyAlternateKey AS CurrencyAlternateKey,
   sd.CurrencyName AS CurrencyName
FROM
   source_data AS sd
```

Snowflake (`StageCopyPackage.sql`), a Flat File Source feeding a Flat File Destination set to overwrite, which becomes a stage-to-stage copy instead of a dbt model:

Copy code

```
CREATE OR REPLACE TASK public.stagecopypackage
AS
SELECT
   1;
CREATE OR REPLACE TASK public.stagecopypackage_data_flow_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.stagecopypackage
AS
BEGIN
   ---- Start block 'Package\Data Flow Task'
   COPY INTO @public.landing_stage/ssis/StageCopyPackage/
   FROM
   (
      SELECT
         $1 :: VARCHAR(50) col_a,
         $2 :: VARCHAR(50) col_b
      FROM
         @public.landing_stage/ssis/StageCopyPackage/SourceFile/source.csv (FILE_FORMAT => 'StageCopyPackage_Data_Flow_Task_Flat_File_Source')
   )
   FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' FIELD_OPTIONALLY_ENCLOSED_BY = '"' RECORD_DELIMITER = '\r\n')
   HEADER = TRUE
   OVERWRITE = TRUE
   SINGLE = TRUE;
   ---- End block 'Package\Data Flow Task'

END;
```

#### Limitations

A destination whose flat file connection manager can’t be bound to the landing stage still produces a model, but nothing writes the rows back out to a file. Add the unload yourself if the package depends on the output file. When the package doesn’t declare the connection manager at all, the conversion can’t resolve a name for it and the model’s alias becomes `CONNECTION_MANAGER_NAME_WAS_NOT_FOUND`. Replace that alias before you run the project.

## Direct copy loads

### Direct COPY

A Data Flow that only moves a Flat File Source into an OLE DB Destination becomes a direct `COPY INTO` load instead of a dbt project.

#### Conversion behavior

This is the default for eligible Flat File Source to OLE DB Destination graphs. The Data Flow becomes a Snowflake task that runs one `COPY INTO` statement, and no dbt project is generated for that Data Flow. The statement lists the destination columns, reads the staged file positionally as `$1`, `$2`, and so on, and applies the casts that the column mapping requires. The flat file connection manager becomes a named file format that carries the field delimiter, the number of header lines to skip, and null handling, and the file itself is read from the shared landing stage. The `--SimplifySsisDataFlows` conversion option is outside the scope of this page, and a Data Flow that isn’t eligible for a direct load falls back to the dbt project conversion described earlier on this page.

#### Example

Snowflake (`DirectFlatFileLoad.sql`):

Copy code

```
CREATE OR REPLACE TASK public.directflatfileload
AS
SELECT
   1;
CREATE OR REPLACE TASK public.directflatfileload_data_flow_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.directflatfileload
AS
BEGIN
   ---- Start block 'Package\Data Flow Task'
   COPY INTO sales.customer_orders (
customer_id,
customer_name
)
   FROM
   (
      SELECT
         $1 :: NUMERIC,
         $2 :: VARCHAR(50) :: VARCHAR(20)
      FROM
         @public.landing_stage/ssis/DirectFlatFileLoad/OrdersFlatFile/input.csv (FILE_FORMAT => 'DirectFlatFileLoad_Data_Flow_Task_Orders_Source')
   );
   ---- End block 'Package\Data Flow Task'

END;
```

Snowflake (`DirectFlatFileLoad/file_formats.sql`):

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS DirectFlatFileLoad_Data_Flow_Task_Orders_Source
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
EMPTY_FIELD_AS_NULL = TRUE;
```

#### Limitations

Every converted flat-file read binds to the generated `public.landing_stage`. That stage is internal, so a `COPY INTO` statement finds a file only once the file has been landed under the prefix it reads. The conversion also writes an ingestion manifest and an Openflow flow definition that carry those same prefixes. Import the flow into Openflow, fill in the bucket, region, endpoint, and credential parameters for the object storage that holds your source files, and enable it. Each object then lands where its `COPY INTO` expects it, so keep the stage name and the subfolder layout that those statements read.

#### ForEach File loads

Not every ForEach File body collapses. SnowConvert AI chooses among patterned COPY, a retained loop that still emits Direct COPY, or a complete fallback to a dbt project.

The bound prefix is `ssis/<package>/<connection manager>/<enumerated folder>/`. The examples below use package `ForEachFlatFileLoad`, connection manager `OrdersFlatFile`, and enumerated folder `c/landing/sales` (from `C:\landing\sales`).

**Collapsed patterned COPY (non-recursive)**

When the ForEach File enumerator can be replaced by a single stage pattern, orchestration emits one `COPY INTO` with a non-recursive `PATTERN`. There is no dbt project.

Copy code

```
:force:

CREATE OR REPLACE TASK public.foreachflatfileload_process_files
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.foreachflatfileload
AS
BEGIN
   COPY INTO sales.customer_orders (
      customer_id,
      customer_name
   )
   FROM
   (
      SELECT
         $1 :: NUMERIC,
         $2 :: VARCHAR(50) :: VARCHAR(20)
      FROM
         @public.landing_stage/ssis/ForEachFlatFileLoad/OrdersFlatFile/c/landing/sales/ (FILE_FORMAT => 'ForEachFlatFileLoad_Process_Files_Data_Flow_Task_Orders_Source')
   )
   PATTERN = 'sales_[^/]{2}_[^/]*\.csv';
END;
```

A folder-only Flat File connection string uses the same collapsed patterned COPY.

**Collapsed patterned COPY (recursive)**

When the enumerator is recursive, the `COPY INTO` statement uses `PATTERN = '(?:[^/]+/)*sales_[^/]{2}_[^/]*\.csv'` to include nested path segments.

**Retained loop with Direct COPY**

Nested Sequence containers, rich bodies (for example row-count variables), and observable downstream variable use keep the ForEach loop. Orchestration still emits Direct COPY inside the loop body. These shapes are not collapsed to a single patterned `COPY INTO`.

Copy code

```
:force:

LIST @public.landing_stage/ssis/ForEachFallbackLoad/OrdersFlatFile/c/landing/sales PATTERN = '.*/.*\.csv';
LET file_cursor CURSOR
FOR
   SELECT
      REGEXP_SUBSTR($1, '[^/]+$') AS FILE_VALUE,
      '@' || $1 AS STAGE_FILE_PATH
   FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   WHERE
      $1 NOT LIKE '%ssis/ForEachFallbackLoad/OrdersFlatFile/c/landing/sales/%/%';
FOR file_row IN file_cursor DO
   User_CurrentFileName := :file_row.FILE_VALUE;
   CALL public.UpdateControlVariable('User_CurrentFileName', 'ForEachFallbackLoad', TO_VARIANT(:User_CurrentFileName));
   COPY INTO sales.customer_orders (
      customer_id,
      customer_name
   )
   FROM
   (
      SELECT
         $1 :: NUMERIC,
         $2 :: VARCHAR(50) :: VARCHAR(20)
      FROM
         :file_row.STAGE_FILE_PATH (FILE_FORMAT => 'ForEachFallbackLoad_Process_Files_Nested_Sequence_Data_Flow_Task_Orders_Source')
   );
END FOR;
```

**Complete fallback to dbt**

Ineligible shapes (dynamic file specs, non-trivial derived columns, and similar) retain complete fallback artifacts: LIST/CURSOR orchestration plus `EXECUTE DBT PROJECT`. They are not Direct COPY collapses.

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - THE FOLDER PATH REQUIRES MANUAL MAPPING TO A SNOWFLAKE STAGE. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0007 - SSIS EXECUTABLE CONTAINS PROPERTY EXPRESSIONS that were not converted. ***/!!!
LIST @<STAGE_PLACEHOLDER>/landing/sales PATTERN = '.*/.*\.csv';
LET file_cursor CURSOR
FOR
   SELECT
      REGEXP_SUBSTR($1, '[^/]+$') AS FILE_VALUE
   FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   WHERE
      $1 NOT LIKE '%landing/sales/%/%';
FOR file_row IN file_cursor DO
   User_CurrentFileName := :file_row.FILE_VALUE;
   CALL public.UpdateControlVariable('User_CurrentFileName', 'ForEachFallbackLoad', TO_VARIANT(:User_CurrentFileName));
   LET dbt_vars_json VARCHAR := public.BuildDbtVarsJsonUDF('ForEachFallbackLoad');
   LET full_args VARCHAR := 'build --target dev --vars ''' || dbt_vars_json || '''';
   EXECUTE DBT PROJECT public.Process_Files_Data_Flow_Task ARGS=:full_args;
END FOR;
```
