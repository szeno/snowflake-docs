# Informatica PowerCenter - dbt mappings and transformations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This page shows how each Informatica PowerCenter Mapping transformation is converted into a [dbt](/user-guide/data-engineering/dbt-projects-on-snowflake) model, with a before (Informatica) and after (Snowflake) example for each. For the dbt project layout and the three-tier model architecture, see the [dbt output overview](README). For the concept map and supported-component matrix, see the [Informatica PowerCenter overview](../README).

Each transformation becomes a SQL model: source reads become `stg_` staging models, intermediate transformations become `int_` models, and Targets become `marts` models. The examples below are taken from the test suite.

## Sources and staging

### Source Qualifier and Source Definition

A Source Qualifier (or Source Definition) becomes a **staging model** that reads from a table declared in `sources.yml`. One staging model per source is generated along with a `sources.yml` that lists the source tables.

Informatica (`m_different_source_qualifiers.XML`):

Copy code

```
<SOURCE NAME="DimCurrency" DATABASETYPE="Microsoft SQL Server" OWNERNAME="dbo">
   <!-- CurrencyKey (primary key), CurrencyAlternateKey, CurrencyName source fields omitted -->
</SOURCE>
<TRANSFORMATION NAME="SQ_DimCurrency" TYPE="Source Qualifier">
   <!-- CurrencyKey, CurrencyAlternateKey, CurrencyName ports omitted -->
   <TABLEATTRIBUTE NAME="Sql Query" VALUE=""/>
   <TABLEATTRIBUTE NAME="Source Filter" VALUE=""/>
   <TABLEATTRIBUTE NAME="Select Distinct" VALUE="NO"/>
</TRANSFORMATION>
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

Snowflake (`stg_raw__SQ_DimCurrency.sql`):

Copy code

```
SELECT
   DimCurrency.CurrencyKey AS CurrencyKey,
   DimCurrency.CurrencyAlternateKey AS CurrencyAlternateKey,
   DimCurrency.CurrencyName AS CurrencyName
FROM
   {{ source('raw', 'DimCurrency') }} AS DimCurrency
```

That empty **Sql Query**, **Source Filter**, and **Select Distinct = NO** shape is the default staging model. The conversion also covers these deltas:

- **Select Distinct = YES** becomes `SELECT DISTINCT` on the staging model. There’s no named dbt golden for that setting, so this page doesn’t show a Distinct fence.
- A **Source Filter** becomes a `WHERE` clause. Qualifiers in the filter are rewritten to match the `FROM` alias.
- A mapping or session **Sql Query** override replaces the generated `SELECT`. A session-only override is bound with a Jinja `var`.
- Source **Pre SQL** becomes a model `pre_hook`.

**Source Filter.** Snowflake (`stg_raw__sq_Dim_Corp_Hier.sql`):

Copy code

```
SELECT
   sc_Dim_Corp_Hier.Infopro_Div_Nbr AS Infopro_Div_Nbr,
   sc_Dim_Corp_Hier.is_Current AS is_Current
FROM
   {{ source('raw', 'sc_Dim_Corp_Hier') }} AS sc_Dim_Corp_Hier
WHERE
   sc_Dim_Corp_Hier.is_Current = 1
```

**Session SQL Override.** Snowflake (`stg_raw__SQ_DimCustomer.sql`):

Copy code

```
{{ config(materialized='table') }}
-- Self-referencing table(s): 'DimCustomer1' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
{% if var('NEWMAPPING11_sq_dimcustomer_sql_override', '') != '' %}
{{ var('NEWMAPPING11_sq_dimcustomer_sql_override') }}
{% else %}
-- Mapping-level SQL Query override (from Source Qualifier 'Sql Query' property)
SELECT
   4 AS CustomerKey
{% endif %}
```

**Source Pre SQL hook.** Snowflake (`stg_raw__SQ_DimEmployee.sql`):

Copy code

```
{{ config(
    materialized='view',
    pre_hook="TRUNCATE TABLE staging_load"
) }}
SELECT
   DimEmployee.EmployeeKey AS EmployeeKey,
   DimEmployee.FirstName AS FirstName
FROM
   {{ source('raw', 'DimEmployee') }} AS DimEmployee
```

Important

Replace the `YOUR_SCHEMA` and `YOUR_DB` placeholders in `sources.yml` with your actual Snowflake schema and database before you run the project.

### Flat File Source

A flat-file Source Definition becomes a `stg_flat_file__{source}` staging model that reads the file directly from a stage instead of from a table in `sources.yml`. Each source field is projected by position (`$1`, `$2`, and so on) and cast to the Snowflake type that matches the field, and the read binds to a `FILE_FORMAT` generated from the Flat File attributes. Reads land under `@public.landing_stage/infpc/sources/{folder}/{source}/`.

Informatica (`flat_file_source_basic.xml`):

Copy code

```
<SOURCE NAME="SRC_DAILY_RATES" DATABASETYPE="Flat File" DBDNAME="FlatFile">
   <FLATFILE CODEPAGE="MS1252" DELIMITED="YES" DELIMITERS="," QUOTE_CHARACTER="&quot;" SKIPROWS="1"/>
   <!-- REGION_CD, CURRENCY_CD, EXCHANGE_RATE, EFFECTIVE_DT source fields omitted -->
</SOURCE>
```

Snowflake (`stg_flat_file__SRC_DAILY_RATES.sql`):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0069 - FLAT FILE SOURCE FILE NAME COULD NOT BE RESOLVED. LANDING PATH '@public.landing_stage/infpc/sources/TestFolder/SRC_DAILY_RATES/UNKNOWN_FILE' REQUIRES A MANUAL FILE BINDING. ***/!!!
SELECT
   $1 :: VARCHAR(10) AS REGION_CD,
   $2 :: VARCHAR(3) AS CURRENCY_CD,
   $3 :: FLOAT AS EXCHANGE_RATE,
   $4 :: TIMESTAMP AS EFFECTIVE_DT
FROM
   @public.landing_stage/infpc/sources/TestFolder/SRC_DAILY_RATES/UNKNOWN_FILE (FILE_FORMAT => 'TestFolder_m_FLAT_FILE_DAILY_RATES_SRC_DAILY_RATES')
```

The matching `FILE_FORMAT` is written to `file_formats.sql`, where the delimiter, text qualifier, codepage, and skipped header rows come from the `FLATFILE` element:

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS TestFolder_m_FLAT_FILE_DAILY_RATES_SRC_DAILY_RATES
TYPE = 'CSV'
FIELD_DELIMITER = ','
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ENCODING = 'WINDOWS1252'
SKIP_HEADER = 1
EMPTY_FIELD_AS_NULL = TRUE;
```

Note

`SSC-EWI-INF0069` is emitted when the Mapping alone is converted, because the file name lives on the Session’s File Reader attributes rather than in the Mapping. Convert the Workflow along with the Mapping, or replace `UNKNOWN_FILE` with the file name you want to read.

A Workflow and Session can resolve the file basename. Snowflake (`stg_flat_file__SRC_DATA.sql` from `flat_file_source_duplicate_instances.xml`):

Copy code

```
SELECT
   $1 :: NUMERIC(5, 0) AS COL_ID,
   $2 :: VARCHAR(20) AS COL_VALUE
FROM
   @public.landing_stage/infpc/sources/TestFolder/SRC_DATA/src_data.csv (FILE_FORMAT => 'TestFolder_m_DUP_FLAT_FILE_SRC_DATA')
```

When the Session uses `$$` parameters for the source directory and filename, the staging model keeps them as dbt runtime variables:

Copy code

```
SELECT
   $1 :: VARCHAR(10) AS EMPLOYEE_ID,
   $2 :: VARCHAR(100) AS FULL_NAME,
   $3 :: FLOAT AS SALARY
FROM
   @public.landing_stage/infpc/sources/TestFolder/SRC_DIRECT_CSV/{{ var('SourceDirectory') }}/{{ var('SourceFileName') }} (FILE_FORMAT => 'TestFolder_m_DIRECT_LOAD_SRC_DIRECT_CSV')
```

The generated ingestion manifest records the source identity, original location, stage binding, and each consumer. Generated Openflow flows copy mapped files from customer object storage onto the generated internal landing stage. For the file-arrival workflow, see the [Informatica PowerCenter overview](../README).

A fixed-width flat file (`DELIMITED="NO"`) has no equivalent Snowflake file format, so no `FILE_FORMAT` is generated. The staging model projects `null` for each field and carries `SSC-EWI-INF0068` so you can map the field offsets by hand:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0068 - FLAT FILE SOURCE 'SRC_FIXED' USES FIXED-WIDTH FORMAT WHICH CANNOT BE MAPPED TO A SNOWFLAKE FILE_FORMAT. MANUAL CONVERSION IS REQUIRED. ***/!!!
SELECT
   null AS COL_A,
   null AS COL_B
```

## Row-level transformations

### Expression

An Expression transformation becomes an `int_` model whose `SELECT` list carries each output port’s formula. Informatica operators and functions convert to their Snowflake equivalents (for example, `||` stays string concatenation). For the full list, see the expression functions reference (coming soon).

Informatica (`MappingForTest.XML`):

Copy code

```
<TRANSFORMATION NAME="EXPTRANS" TYPE="Expression">
   <TRANSFORMFIELD NAME="NAME" PORTTYPE="INPUT/OUTPUT" EXPRESSION="NAME"/>
   <TRANSFORMFIELD NAME="Description" PORTTYPE="INPUT/OUTPUT" EXPRESSION="Description" DEFAULTVALUE="&apos;&lt;No description&gt;&apos;"/>
   <TRANSFORMFIELD NAME="NEW_NAME" PORTTYPE="OUTPUT" EXPRESSION="NAME || &apos;!!!&apos;"/>
</TRANSFORMATION>
```

Snowflake (`int_EXPTRANS.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      NAME1 AS NAME
   FROM
      {{ ref('int_SALARY_RTRTRANS__HIGH_SALARY') }}
)
SELECT
   NAME AS NAME,
   '<No description>' AS Description,
   NAME || '!!!' AS NEW_NAME
FROM
   source_data
```

### Expression lagger

When an Expression uses the lagger pattern (a LOCAL VARIABLE port that forward-references another LOCAL VARIABLE to read the previous row), the conversion emits a `lag_values` CTE with Snowflake `LAG()`. Chained LOCAL VARIABLE ports become that CTE, not a self-join.

#### Example

Snowflake (`int_EXP_Lagger.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      OrderID,
      ShipCountry
   FROM
      {{ ref('stg_raw__SQ_Orders') }}
),
lag_values AS
(
   SELECT
      *,
      !!!RESOLVE EWI!!! /*** SSC-EWI-INF0065 - THIS EXPRESSION USES THE LAGGER TECHNIQUE (LOCAL VARIABLE FORWARD REFERENCE) TO ACCESS VALUES FROM PREVIOUS ROWS. TRANSLATED TO LAG() WINDOW FUNCTION WITH NON-DETERMINISTIC ORDER BY 1 BECAUSE NO PRECEDING SORTER TRANSFORMATION WAS FOUND. MANUAL INTERVENTION REQUIRED: REPLACE ORDER BY 1 WITH A DETERMINISTIC COLUMN TO ENSURE CORRECT ROW ORDERING. ***/!!!
      LAG(ShipCountry, 1)
      OVER (
      ORDER BY
         1) AS v_ShipCountry_Lagged
   FROM
      source_data
)
SELECT
   OrderID AS OrderID,
   v_ShipCountry_Lagged AS PrevShipCountry
FROM
   lag_values
```

#### Limitations

Without a Sorter ahead of the Expression, `LAG()` uses `ORDER BY 1`, which isn’t a deterministic key. Replace it with the columns you need. [SSC-EWI-INF0065](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0065).

### Filter

A Filter transformation becomes an `int_` model with a `WHERE` clause that carries the Filter condition.

Informatica (`m_dummy_filter_test.XML`):

Copy code

```
<TRANSFORMATION NAME="t_dummy_filter_1" TYPE="Filter">
   <!-- EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, SALARY input/output ports omitted -->
   <TABLEATTRIBUTE NAME="Filter Condition" VALUE="SALARY &gt; 10 AND SALARY &lt;= 100000"/>
</TRANSFORMATION>
```

Snowflake (`int_t_dummy_filter_1.sql`):

Copy code

```
SELECT
    SQ_employee_data.EMPLOYEE_ID AS EMPLOYEE_ID,
    null AS FIRST_NAME,
    SQ_employee_data.LAST_NAME AS LAST_NAME,
    SQ_employee_data.EMAIL AS EMAIL,
    SQ_employee_data.SALARY AS SALARY
FROM
    {{ ref('stg_raw__SQ_employee_data') }} AS SQ_employee_data
WHERE
    SALARY > 10
  AND SALARY <= 100000
```

## Combining data

### Joiner

A Joiner becomes an `int_` model with a SQL `JOIN`. The Informatica join type maps to the matching SQL join: Normal Join to `INNER JOIN`, Master Outer to `RIGHT JOIN`, Detail Outer to `LEFT JOIN`, and Full Outer to `FULL OUTER JOIN`. The Join condition becomes the `ON` clause.

Informatica (`m_dummy_joiner_test.XML`):

Copy code

```
<TRANSFORMATION NAME="t_join_DimProduct_FactInternetSales" TYPE="Joiner">
   <!-- master (DimProduct) and detail (FactInternetSales) ports omitted -->
   <TABLEATTRIBUTE NAME="Join Condition" VALUE="ProductKey1 = ProductKey"/>
   <TABLEATTRIBUTE NAME="Join Type" VALUE="Normal Join"/>
</TRANSFORMATION>
```

Snowflake (`int_t_join_DimProduct_FactInternetSales.sql`):

Copy code

```
SELECT
   SQ_FactInternetSales.UnitPrice AS UnitPrice,
   SQ_FactInternetSales.OrderQuantity AS OrderQuantity,
   SQ_FactInternetSales.CurrencyKey AS CurrencyKey,
   SQ_FactInternetSales.ProductKey AS ProductKey1,
   SQ_DimProduct.ProductKey AS ProductKey,
   SQ_DimProduct.EnglishProductName AS EnglishProductName,
   SQ_DimProduct.SpanishProductName AS SpanishProductName
FROM
   {{ ref('stg_raw__SQ_FactInternetSales') }} AS SQ_FactInternetSales
   INNER JOIN
      {{ ref('stg_raw__SQ_DimProduct') }} AS SQ_DimProduct
      ON SQ_FactInternetSales.ProductKey = SQ_DimProduct.ProductKey
```

### Union

A Union transformation becomes an `int_` model that combines its inputs with `UNION ALL`. Each input is a CTE that aligns its columns to the Union’s output ports.

Informatica (`union_simple_two_inputs.xml`):

Copy code

```
<TRANSFORMATION NAME="UNION" TYPE="Custom Transformation" TEMPLATENAME="Union Transformation">
   <GROUP NAME="OUTPUT" TYPE="OUTPUT"/>
   <GROUP NAME="A" TYPE="INPUT"/>
   <GROUP NAME="B" TYPE="INPUT"/>
   <!-- vala (output), vala1 (group A), vala2 (group B) ports omitted -->
   <FIELDDEPENDENCY INPUTFIELD="vala1" OUTPUTFIELD="vala"/>
   <FIELDDEPENDENCY INPUTFIELD="vala2" OUTPUTFIELD="vala"/>
</TRANSFORMATION>
```

Snowflake (`int_union.sql`):

Copy code

```
WITH a AS
(
   SELECT
      vala vala
   FROM
      {{ ref('stg_raw__SQ_tableA') }}
),
b AS
(
   SELECT
      valb vala
   FROM
      {{ ref('stg_raw__SQ_tableB') }}
)
SELECT
   a.vala vala
FROM
   a
UNION ALL
SELECT
   b.vala vala
FROM
   b
```

### Lookup

A connected Lookup becomes an `int_` model named `int_{lookup_name}` that joins each input row to the lookup source. The lookup source is a `lookup_reference` CTE; the Mapping input is an `input_data` CTE.

#### Conversion behavior

When **Lookup policy on multiple match** is **Use Any Value**, **Use First Value**, **Use Last Value**, or **Report Error**, `lookup_reference` keeps one row per lookup key with `QUALIFY ROW_NUMBER() = 1`. That matches Informatica’s single-row lookup behavior. When more than one lookup row can match, Snowflake’s row selection isn’t guaranteed to be stable between runs, so the conversion emits [SSC-FDM-INF0070](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0070).

When the policy is **Use All Values**, the same join is emitted **without** `QUALIFY`, so one input row can fan out to every matching lookup row. The conversion also emits [SSC-FDM-INF0061](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0061). When **Case Sensitive String Comparison** is `NO`, it emits `SSC-FDM-INF0088` because the generated join is still case-sensitive.

An unconnected Lookup isn’t this join. It becomes a dbt macro under `macros/` (for example `macros/ulkp_departments.sql`). The Expression, Filter, or Router that referenced `:LKP` calls that macro with Jinja, it doesn’t emit an `int_` `QUALIFY` join. Nested `:LKP` calls become nested macro invocations: the inner call has no extra Jinja braces, and the outer call wraps the whole expression.

A connected Lookup whose **Source Type** is **Flat File** still emits an `int_` join, but `lookup_reference` reads the lookup file’s staging model (`stg_flat_file__...`) instead of `{{ source() }}`. Its stage prefix uses the owning folder and Source Definition identity, just like a flat-file source. The ingestion manifest inventories the Lookup as a consumer of that source identity rather than creating a second landing source.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| Lookup table name | `{{ source() }}` or a staging `{{ ref() }}` | Becomes the `lookup_reference` CTE. |
| Lookup condition | `LEFT JOIN` `ON` clause | Each equality (and supported comparison) becomes a join predicate. |
| Lookup policy on multiple match: Use Any Value | `QUALIFY ROW_NUMBER() = 1` | Emits [SSC-FDM-INF0070](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0070) when the selected row can vary. The example below is this policy. |
| Lookup policy on multiple match: Use All Values | Join with no `QUALIFY` | Cardinality can grow. Emits [SSC-FDM-INF0061](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0061). See the Use All Values example below. |

Expand

Show lessSee more

#### Example

**Connected Use Any Value.** Informatica (`lookups_sample.XML`):

Copy code

```
<TRANSFORMATION NAME="t_lookup_currency" TYPE="Lookup Procedure">
   <!-- CurrencyKey, CurrencyAlternateKey, CurrencyName (lookup/output), CurrencyKey1 (input) ports omitted -->
   <TABLEATTRIBUTE NAME="Lookup table name" VALUE="DimCurrency"/>
   <TABLEATTRIBUTE NAME="Lookup condition" VALUE="CurrencyKey = CurrencyKey1"/>
   <TABLEATTRIBUTE NAME="Lookup policy on multiple match" VALUE="Use Any Value"/>
</TRANSFORMATION>
```

Snowflake (`int_t_lookup_currency.sql`):

Copy code

```
WITH lookup_reference AS
(
   SELECT
      CurrencyKey ,
      CurrencyAlternateKey ,
      CurrencyName
   FROM
      {{ source('raw', 'DimCurrency') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         CurrencyKey
      ORDER BY
         (
            SELECT
               --** SSC-FDM-INF0070 - Use Any Value RETURNS AN ARBITRARY ROW WHEN MULTIPLE ROWS MATCH; IN SNOWFLAKE THE SELECTED ROW MAY VARY PER RUN. ADD AN ORDER BY TO THE LOOKUP SQL OVERRIDE ONLY IF A SPECIFIC ROW IS REQUIRED. **
               null
         )) = 1
),
input_data AS
(
   SELECT
      CurrencyKey CurrencyKey1,
      TotalProductCost SQ_FactInternetSales__TotalProductCost,
      OrderDate SQ_FactInternetSales__OrderDate,
      ProductKey SQ_FactInternetSales__ProductKey1,
      CustomerKey SQ_FactInternetSales__CustomerKey1
   FROM
      {{ ref('stg_raw__SQ_FactInternetSales') }}
)
SELECT
   input_data.CurrencyKey1 ,
   input_data.SQ_FactInternetSales__TotalProductCost ,
   input_data.SQ_FactInternetSales__OrderDate ,
   input_data.SQ_FactInternetSales__ProductKey1 ,
   input_data.SQ_FactInternetSales__CustomerKey1 ,
   lookup_reference.CurrencyKey,
   lookup_reference.CurrencyAlternateKey,
   lookup_reference.CurrencyName
FROM
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.CurrencyKey = input_data.CurrencyKey1
```

**Connected Use All Values.** Informatica (`lookup_useallvalues_simple.xml`):

Copy code

```
<TRANSFORMATION NAME="LKPTRANS" TYPE="Lookup Procedure">
   <!-- DeptCode, DeptName (lookup/output), EmpName, DeptCode1 (input) ports omitted -->
   <TABLEATTRIBUTE NAME="Lookup table name" VALUE="Tbg_Departments"/>
   <TABLEATTRIBUTE NAME="Lookup policy on multiple match" VALUE="Use All Values"/>
   <TABLEATTRIBUTE NAME="Lookup condition" VALUE="DeptCode = DeptCode1"/>
   <TABLEATTRIBUTE NAME="Source Type" VALUE="Database"/>
</TRANSFORMATION>
```

Snowflake (`int_LKPTRANS.sql`):

Copy code

```
WITH lookup_reference AS
(
   SELECT
      DeptCode ,
      DeptName
   FROM
      {{ source('raw', 'Tbg_Departments') }}
),
input_data AS
(
   SELECT
      EmpName ,
      DeptCode DeptCode1
   FROM
      {{ ref('stg_raw__SQ_Tbg_Employees') }}
)
SELECT
   input_data.EmpName ,
   input_data.DeptCode1 ,
   lookup_reference.DeptCode,
   lookup_reference.DeptName
FROM
   --** SSC-FDM-INF0061 - CONNECTED LOOKUP 'LKPTRANS' USES MULTI-MATCH POLICY 'USE ALL VALUES'. THE TRANSLATION EMITS A JOIN AGAINST 'Tbg_Departments'. ROW COUNT MAY INCREASE. **
   --** SSC-FDM-INF0088 - CONNECTED LOOKUP 'LKPTRANS' USES CASE-INSENSITIVE STRING COMPARISON ('CASE SENSITIVE STRING COMPARISON' = NO), BUT THE EMITTED JOIN CONDITION IS CASE-SENSITIVE. LOOKUP MATCHES MAY DIFFER FROM POWERCENTER. **
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.DeptCode = input_data.DeptCode1
```

**Unconnected Lookup macro.** The Lookup isn’t an `int_` model. Snowflake (`macros/ulkp_departments.sql`):

Copy code

```
{% macro ulkp_departments(in_deptcode) %}
(
    SELECT MAX(DeptName)
    FROM {{ source('raw', 'Departments') }} AS lkp
    WHERE
   lkp.DeptCode = {{ in_deptcode }}
)
{% endmacro %}
```

**Nested unconnected Lookup.** Nested `:LKP` calls become nested macro invocations. Snowflake (`int_EXPTRANS.sql` excerpt from `expr_nested_lookup_with_literals_expected.sql`):

Copy code

```
      {{ lkptrans1('v_dcPre || \'\'') }} AS v_dc
   FROM
      locals_cte_2
),
results_with_locals AS
(
   SELECT
      *,
      {{ lkptrans1(lkptrans11('\'SOMETHING\'', '\'b\'')) }} AS NEWFIELD,
      '' || {{ lkptrans1('v_dc || \'\'') }} AS v_dc2,
      {{ lkptrans('locals_cte_3.v_dc') }} AS DeptName
   FROM
      locals_cte_3
)
```

**Connected flat-file Lookup.** Informatica (`flat_file_lookup_connected.xml`):

Copy code

```
<TRANSFORMATION NAME="Lkp_DivToCode" TYPE="Lookup Procedure">
   <!-- LKP_divID (lookup), divCode (lookup/output), divID, authNum (input) ports omitted -->
   <TABLEATTRIBUTE NAME="Lookup table name" VALUE=""/>
   <TABLEATTRIBUTE NAME="Lookup policy on multiple match" VALUE="Use Any Value"/>
   <TABLEATTRIBUTE NAME="Lookup condition" VALUE="LKP_divID = divID"/>
   <TABLEATTRIBUTE NAME="Source Type" VALUE="Flat File"/>
</TRANSFORMATION>
```

Snowflake (`int_Lkp_DivToCode.sql` from `flat_file_lookup_connected_expected.sql`):

Copy code

```
WITH lookup_reference AS
(
   SELECT
      LKP_divID ,
      divCode
   FROM
      {{ ref('stg_flat_file__Lkp_DivToCode') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         LKP_divID
      ORDER BY
         (
            SELECT
               --** SSC-FDM-INF0070 - Use Any Value RETURNS AN ARBITRARY ROW WHEN MULTIPLE ROWS MATCH; IN SNOWFLAKE THE SELECTED ROW MAY VARY PER RUN. ADD AN ORDER BY TO THE LOOKUP SQL OVERRIDE ONLY IF A SPECIFIC ROW IS REQUIRED. **
               null
         )) = 1
),
input_data AS
(
   SELECT
      divID ,
      authNum
   FROM
      {{ ref('stg_raw__SQ_SrcTable') }}
)
SELECT
   input_data.divID ,
   input_data.authNum ,
   lookup_reference.divCode
FROM
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.LKP_divID = input_data.divID
```

#### Limitations

When a lookup can match multiple rows under Use Any Value, Snowflake’s row selection isn’t guaranteed to be stable between runs, so [SSC-FDM-INF0070](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0070) is emitted. Add an `ORDER BY` to the lookup if you need a specific row.

Use All Values can increase the row count ([SSC-FDM-INF0061](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0061)). When **Case Sensitive String Comparison** is `NO`, the join is still case-sensitive (`SSC-FDM-INF0088`).

An unconnected Lookup with **Use All Values** still uses the unconnected macro path (`SELECT MAX(...)`), not the connected fan-out join.

## Aggregation and ranking

### Aggregator

An Aggregator becomes an `int_` model that computes each aggregate with a window function partitioned by the group-by ports, then keeps one row per group with `QUALIFY ROW_NUMBER() = 1`. This reproduces Informatica’s one-row-per-group output.

Informatica (`AggregatorMapping.XML`):

Copy code

```
<TRANSFORMATION NAME="AGGTRANS" TYPE="Aggregator">
   <TRANSFORMFIELD NAME="NAME" PORTTYPE="INPUT/OUTPUT" EXPRESSION="NAME"/>
   <TRANSFORMFIELD NAME="deptsalary" PORTTYPE="OUTPUT" EXPRESSION="SUM(SALARY)"/>
   <TRANSFORMFIELD NAME="SALARY" PORTTYPE="INPUT/OUTPUT" EXPRESSION="SALARY"/>
   <TRANSFORMFIELD NAME="DEPARTMENT" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="GROUPBY" EXPRESSION="DEPARTMENT"/>
</TRANSFORMATION>
```

Snowflake (`int_AGGTRANS.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      NAME,
      SALARY,
      DEPARTMENT
   FROM
      {{ ref('stg_raw__SQ_EMPLOYEE') }}
),
aggregation AS
(
   SELECT
      LAST_VALUE(NAME)
      OVER (
      PARTITION BY (
         DEPARTMENT)
      ORDER BY
         NAME,
         SALARY,
         DEPARTMENT) AS NAME,
      SUM(SALARY)
      OVER (
      PARTITION BY (
         DEPARTMENT)) AS deptsalary,
      LAST_VALUE(SALARY)
      OVER (
      PARTITION BY (
         DEPARTMENT)
      ORDER BY
         NAME,
         SALARY,
         DEPARTMENT) AS SALARY,
      LAST_VALUE(DEPARTMENT)
      OVER (
      PARTITION BY (
         DEPARTMENT)
      ORDER BY
         NAME,
         SALARY,
         DEPARTMENT) AS DEPARTMENT
   FROM
      source_data
   QUALIFY
      --** SSC-FDM-INF0002 - ALL INPUT COLUMNS WILL BE USED TO DETERMINE GROUP ORDER. **
      ROW_NUMBER()
      OVER (
      PARTITION BY (
         DEPARTMENT)
      ORDER BY
         NAME,
         SALARY,
         DEPARTMENT) = 1
)
SELECT
    NAME,
    deptsalary,
    SALARY,
    DEPARTMENT
FROM
    aggregation
```

#### Aggregator without group-by ports

When an Aggregator has no group-by ports, the whole input is one group. If the transformation also has no aggregate functions, so every port is a plain passthrough, the Aggregator is doing Informatica’s distinct emulation: it returns one row per distinct combination of its ports. That converts to a `SELECT DISTINCT` over the source CTE, with no window function and no `QUALIFY`.

Informatica (`aggregator_nogrp_distinct.xml`):

Copy code

```
<TRANSFORMATION NAME="AGG_Distinct" TYPE="Aggregator">
   <TRANSFORMFIELD NAME="code" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="GENERAL" EXPRESSION="code"/>
   <TRANSFORMFIELD NAME="label" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="GENERAL" EXPRESSION="label"/>
   <TABLEATTRIBUTE NAME="Sorted Input" VALUE="NO"/>
   <TABLEATTRIBUTE NAME="Transformation Scope" VALUE="All Input"/>
</TRANSFORMATION>
```

Snowflake (`int_AGG_Distinct.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      code,
      label
   FROM
      {{ ref('stg_raw__SQ_RefData') }}
)
SELECT DISTINCT
   code,
   label
FROM
   source_data
```

### Rank

A Rank transformation becomes an `int_` model that assigns `ROW_NUMBER()` over the rank port and keeps the top or bottom N rows with `QUALIFY`. The example below selects the bottom 10 rows by price.

Informatica (`rank_bottom_n.xml`):

Copy code

```
<TRANSFORMATION NAME="RNK_BottomProducts" TYPE="Rank">
   <!-- product_id (input/output), RANKINDEX (output) ports omitted -->
   <TRANSFORMFIELD NAME="price" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="RANKPORT"/>
   <TABLEATTRIBUTE NAME="Top/Bottom" VALUE="BOTTOM"/>
   <TABLEATTRIBUTE NAME="Number of Ranks" VALUE="10"/>
</TRANSFORMATION>
```

Snowflake (`int_rank.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      product_id,
      price
   FROM
      {{ ref('stg_raw__SQ_Products') }}
),
ranked_data AS
(
   SELECT
      product_id,
      price,
      ROW_NUMBER()
      OVER (
      ORDER BY
         price ASC) AS RANKINDEX
   FROM
      source_data
   QUALIFY
      RANKINDEX <= 10
)
SELECT
   RANKINDEX,
   product_id,
   price
FROM
   ranked_data
```

When the Rank has one or more group-by ports (`EXPRESSIONTYPE="GROUPBY"`), those ports become a `PARTITION BY` clause on the `ROW_NUMBER()` window, so the top or bottom N rows are picked within each group instead of across the whole input. The example below keeps the three highest-paid employees per department.

Informatica (`rank_grouped_top_n.xml`):

Copy code

```
<TRANSFORMATION NAME="RNK_TopPerDept" TYPE="Rank">
   <!-- RANKINDEX (output), employee_id and employee_name input/output ports omitted -->
   <TRANSFORMFIELD NAME="department" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="GROUPBY"/>
   <TRANSFORMFIELD NAME="salary" PORTTYPE="INPUT/OUTPUT" EXPRESSIONTYPE="RANKPORT"/>
   <TABLEATTRIBUTE NAME="Top/Bottom" VALUE="TOP"/>
   <TABLEATTRIBUTE NAME="Number of Ranks" VALUE="3"/>
</TRANSFORMATION>
```

Snowflake (`int_RNK_TopPerDept.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      employee_id,
      employee_name,
      department,
      salary
   FROM
      {{ ref('stg_raw__SQ_Employees') }}
),
ranked_data AS
(
   SELECT
      employee_id,
      employee_name,
      department,
      salary,
      ROW_NUMBER()
      OVER (
      PARTITION BY (
         department)
      ORDER BY
         salary DESC) AS RANKINDEX
   FROM
      source_data
   QUALIFY
      RANKINDEX <= 3
)
SELECT
   RANKINDEX,
   employee_id,
   employee_name,
   department,
   salary
FROM
   ranked_data
```

## Sorting

### Sorter

A Sorter becomes its own table-materialized intermediate model `int_{sorter_name}`, not an `ORDER BY` on the consumer. The model’s `config` sets `materialized='table'`, and the outer query carries the Sorter’s keys and direction.

#### Conversion behavior

The generated model wraps the upstream rows in a `source_data` CTE, copies them through a `sorted` CTE, and applies `ORDER BY` on the final `SELECT`. When **Distinct** is enabled, `sorted` uses `SELECT DISTINCT` (or a case-folded `QUALIFY` when **Case Sensitive** is `NO`). Nulls sort with `NULLS LAST`.

#### Example

Informatica (`sorter_simple_ascending.xml`):

Copy code

```
<TRANSFORMATION NAME="SRT_Simple_Asc" TYPE="Sorter">
   <TRANSFORMFIELD NAME="EMP_ID" ISSORTKEY="YES" PORTTYPE="INPUT/OUTPUT" SORTDIRECTION="ASCENDING"/>
   <!-- EMP_NAME, SALARY, DEPT ports omitted -->
   <TABLEATTRIBUTE NAME="Case Sensitive" VALUE="YES"/>
   <TABLEATTRIBUTE NAME="Distinct" VALUE="NO"/>
   <TABLEATTRIBUTE NAME="Transformation Scope" VALUE="All Input"/>
</TRANSFORMATION>
```

Snowflake (`int_SRT_Simple_Asc.sql`):

Copy code

```
{{ config(
    materialized='table'
) }}
WITH source_data AS
(
   SELECT
      EMP_ID,
      EMP_NAME,
      SALARY,
      DEPT
   FROM
      {{ ref('stg_raw__SQ_SRC_SORT_SIMPLE') }}
),
sorted AS
(
   SELECT
      *
   FROM
      source_data
)
SELECT
   *
FROM
   sorted
ORDER BY
   EMP_ID ASC NULLS LAST
```

When **Distinct** is `YES`, `sorted` uses `SELECT DISTINCT` and the outer `ORDER BY` lists every sort key:

Copy code

```
{{ config(
    materialized='table'
) }}
WITH source_data AS
(
   SELECT
      CITY_NAME,
      PROVINCE_CODE,
      CITY_TYPE
   FROM
      {{ ref('stg_raw__SQ_SRC_SORT_DISTINCT') }}
),
sorted AS
(
   SELECT DISTINCT
      CITY_NAME,
      PROVINCE_CODE,
      CITY_TYPE
   FROM
      source_data
)
SELECT
   *
FROM
   sorted
ORDER BY
   CITY_NAME ASC NULLS LAST,
   PROVINCE_CODE ASC NULLS LAST,
   CITY_TYPE ASC NULLS LAST
```

#### Limitations

When **Distinct** is `YES` and **Case Sensitive** is `NO`, the conversion deduplicates with a case-folded `QUALIFY` instead of `SELECT DISTINCT`, and emits `SSC-FDM-INF0082` because the surviving row’s casing can differ from PowerCenter’s arrival-order pick.

When **Transformation Scope** is **Transaction**, the sort is applied globally across all input rows and the model emits [SSC-FDM-INF0009](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0009). Transaction boundaries aren’t modeled in Snowflake SQL.

## Routing and normalizing

### Router

A Router produces **one `int_` model per output group**, each named `int_{router_name}__{group_name}` and filtered by that group’s condition. The default group keeps the rows that match no other group.

Informatica (`routerexample.XML`):

Copy code

```
<TRANSFORMATION NAME="RTRTRANS" TYPE="Router">
   <GROUP NAME="INPUT" TYPE="INPUT"/>
   <GROUP NAME="high_credits" TYPE="OUTPUT" EXPRESSION="Credits &gt; 70"/>
   <GROUP NAME="low_credits" TYPE="OUTPUT" EXPRESSION="Credits &gt; 5"/>
   <GROUP NAME="DEFAULT1" TYPE="OUTPUT/DEFAULT"/>
   <!-- FirstName, LastName, Department, Credits ports omitted -->
</TRANSFORMATION>
```

Snowflake (`int_RTRTRANS__high_credits.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      FirstName,
      LastName,
      Department,
      Credits
   FROM
      {{ ref('stg_raw__SQ_Students') }}
)
SELECT
   FirstName FirstName1,
   LastName LastName1,
   Department Department1,
   Credits Credits1
FROM
   source_data
WHERE
   Credits > 70
```

### Normalizer

A Normalizer becomes an `int_` model that pivots repeating groups from columns into rows. Each occurrence becomes a CTE, the occurrences are combined with `UNION ALL`, and a generated-column ID (`gcid_`) and generated key (`gk_`) reproduce Informatica’s occurrence numbering.

Informatica (`normalizer_simple_wide_to_tall.xml`):

Copy code

```
<TRANSFORMATION NAME="NRM_SimpleExpense" TYPE="Normalizer">
   <!-- EmpId, EmpName source fields omitted -->
   <SOURCEFIELD NAME="Expense" OCCURS="5"/>
   <!-- Expense_in1..in5 (inputs mapped from food/rent/transport/medical/misc_expense),
        Expense (output), GK_Expense, GCID_Expense ports omitted -->
</TRANSFORMATION>
```

Snowflake (`int_normalizer.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      empid,
      empname,
      food_expense,
      rent_expense,
      transport_expense,
      medical_expense,
      misc_expense
   FROM
      {{ ref('stg_raw__SQ_NRM_SIMPLE_SRC') }}
),
occurrence_1 AS
(
   SELECT
      empid,
      empname,
      food_expense AS expense,
      1 AS gcid_expense
   FROM
      source_data
),
occurrence_2 AS
(
   SELECT
      empid,
      empname,
      rent_expense AS expense,
      2 AS gcid_expense
   FROM
      source_data
),
normalized AS
(
   SELECT * FROM occurrence_1
   UNION ALL
   SELECT * FROM occurrence_2
),
with_gk AS
(
   SELECT
      empid,
      empname,
      expense,
      gcid_expense,
      ROW_NUMBER()
      OVER (
      ORDER BY
         empid,
         gcid_expense) AS gk_expense
   FROM
      normalized
)
SELECT
   *
FROM
   with_gk
```

Note

The example is trimmed to two occurrences for brevity. One `occurrence_n` CTE per repeating column is generated. VSAM Normalizers are not supported and generate an EWI.

#### Limitations

The generated key (`gk_`) port becomes a `ROW_NUMBER()`, which restarts at 1 on every run of the model. Two Normalizer settings change how PowerCenter keeps that counter, and each one adds a functional-difference marker to the generated model. `Restart=YES` is functionally equivalent in Snowflake, while `Reset=YES` can’t be reproduced.

`Restart=YES` restarts the counter for each session. Because `ROW_NUMBER()` already starts over on every run, the translation matches that behavior, and the model records it:

Copy code

```
--** SSC-FDM-INF0007 - NORMALIZER GK PORT IS TRANSLATED AS ROW_NUMBER() WHICH ALWAYS STARTS FROM 1 PER QUERY EXECUTION. THIS IS FUNCTIONALLY EQUIVALENT TO RESTART=YES IN INFORMATICA POWERCENTER. VERIFY GK VALUES IF USED AS A FOREIGN KEY IN DOWNSTREAM TARGETS. **
```

`Reset=YES` restores the counter to its pre-session value when the session ends, which the translation can’t reproduce:

Copy code

```
--** SSC-FDM-INF0008 - NORMALIZER RESET=YES IS NOT REPLICATED IN SNOWFLAKE. IN INFORMATICA, RESET=YES RESTORES THE GK COUNTER TO ITS PRE-SESSION VALUE AT SESSION END. IN THE SNOWFLAKE TRANSLATION, ROW_NUMBER() ALWAYS STARTS FROM 1. VERIFY GK VALUES IF USED AS A FOREIGN KEY IN DOWNSTREAM TARGETS. **
```

With either setting, check the `gk_` values before you use them as foreign keys in downstream targets.

## Keys and load strategy

### Sequence Generator

A Sequence Generator becomes a `ROW_NUMBER()` expression, offset by the Sequence’s start value. Because a dbt model is reprocessed on each run and rows are not inherently ordered, the generated numbers are not stable across runs, so `SSC-EWI-INF0043` is emitted.

Informatica (`seqgen_start_value_offset.xml`):

Copy code

```
<TRANSFORMATION NAME="SEQ_RowKey" TYPE="Sequence">
   <!-- NEXTVAL, CURRVAL output ports omitted -->
   <TABLEATTRIBUTE NAME="Start Value" VALUE="10"/>
   <TABLEATTRIBUTE NAME="Increment By" VALUE="1"/>
   <TABLEATTRIBUTE NAME="Cycle" VALUE="NO"/>
</TRANSFORMATION>
```

Snowflake (`int_seqgen.sql`):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0043 - THE SEQUENCE GENERATOR IS TRANSLATED TO ROW_NUMBER() OVER (ORDER BY 1). ROW ORDERING IS NON-DETERMINISTIC (VALUES MAY BE ASSIGNED TO DIFFERENT ROWS BETWEEN RUNS) AND SEQUENCE STATE IS NOT PERSISTED ACROSS DBT EXECUTIONS (ALWAYS RESTARTS FROM START VALUE). ADD A DETERMINISTIC ORDER BY IF STABLE SEQUENCE ASSIGNMENT IS REQUIRED. ***/!!!
WITH source_data AS
(
   SELECT
      *
   FROM
      {{ ref('stg_raw__SQ_Products') }}
),
sequence_data AS
(
   SELECT
      *,
      ROW_NUMBER()
      OVER (
      ORDER BY
         1) + 9 AS NEXTVAL
   FROM
      source_data
)
SELECT
   *
FROM
   sequence_data
```

Note

Add a deterministic `ORDER BY` to the `ROW_NUMBER()` window if you need stable surrogate keys, or generate keys with a Snowflake [sequence](/sql-reference/sql/create-sequence) for state that persists across runs.

#### Fan-out to multiple pipelines

When one Sequence Generator feeds more than one independent pipeline, a separate model is generated for each downstream pipeline, named `int_{sequence_name}__{pipeline_name}`. Each one reads from its own upstream model, so no shared model is left for several pipelines to reference.

The tradeoff is that each model runs its own `ROW_NUMBER()`. In PowerCenter all the pipelines draw from a single counter and receive non-overlapping values, while in dbt every pipeline starts over, so values overlap between pipelines. `SSC-EWI-INF0059` is emitted on each generated model to flag that difference.

Snowflake (`int_SEQTRANS__StudentResult.sql`):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0059 - A SEQUENCE GENERATOR IS CONNECTED TO MULTIPLE INDEPENDENT PIPELINES (FAN-OUT TOPOLOGY). IN INFORMATICA Power Center, THE SEQUENCE COUNTER IS SHARED ACROSS ALL PIPELINES, PRODUCING NON-OVERLAPPING IDS. IN DBT, EACH PIPELINE RECEIVES AN INDEPENDENT ROW_NUMBER() OVER (ORDER BY 1) STARTING FROM 1, SO COUNTER VALUES WILL OVERLAP BETWEEN PIPELINES. REVIEW THE GENERATED PER-PIPELINE INTERMEDIATE MODELS AND DETERMINE IF SEQUENTIAL NUMBERING ACROSS PIPELINES IS REQUIRED. ***/!!!
WITH source_data AS
(
   SELECT
      *
   FROM
      {{ ref('int_StudentPart2') }}
),
sequence_data AS
(
   SELECT
      *,
      ROW_NUMBER()
      OVER (
      ORDER BY
         1) * 10 AS NEXTVAL
   FROM
      source_data
)
SELECT
   *
FROM
   sequence_data
```

The second pipeline gets its own model, `int_SEQTRANS__DeptResult.sql`, with the same shape reading from `{{ ref('int_DeptPart1') }}`. If the pipelines need to keep the non-overlapping numbering they had in PowerCenter, give each model a distinct offset or replace `ROW_NUMBER()` with a shared Snowflake [sequence](/sql-reference/sql/create-sequence).

### Update Strategy

An Update Strategy directs how rows reach the Target. When a Mapping uses one and the Update Strategy expression is a static `DD_UPDATE`, the Target mart model is materialized as **incremental** with the **merge** strategy, so inserts and updates are applied with a Snowflake `MERGE`. Other expressions produce other load shapes, which the sections below describe.

When the Session Writer sets **Truncate target table option = YES** on a **relational** target with an insert-style Update Strategy, the mart uses `materialized='table'` instead of incremental append. That truncate shape doesn’t apply to flat-file unload.

Snowflake (`marts/d_table_4.sql`):

Copy code

```
{{ config(
    materialized='table'
) }}
SELECT
   DeptName AS TXT
FROM
   {{ ref('int_UPDTRANS') }}
```

Informatica (`update_strategy_multiple_targets_same_mapping.xml`):

Copy code

```
<TRANSFORMATION NAME="UPDTRANS" TYPE="Update Strategy">
   <!-- input/output ports omitted -->
   <TABLEATTRIBUTE NAME="Update Strategy Expression" VALUE="DD_UPDATE"/>
</TRANSFORMATION>
<TARGET NAME="After_Students_Clear" DATABASETYPE="Microsoft SQL Server">
   <TARGETFIELD NAME="Id" KEYTYPE="PRIMARY KEY" DATATYPE="int"/>
   <TARGETFIELD NAME="Name" KEYTYPE="NOT A KEY" DATATYPE="nvarchar"/>
   <!-- remaining target fields omitted -->
</TARGET>
```

Snowflake (mart model):

Copy code

```
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='Id',
    merge_update_columns=['Name'],
    alias='After_Students_Clear'
) }}
SELECT
   SALARY AS Id,
   NAME AS Name
FROM
   {{ ref('int_UPDTRANS') }}
```

In the insert, update, delete, and conditional cases that follow, the load logic lands on the mart model, so the Update Strategy becomes a passthrough `int_` model that carries `SSC-FDM-INF0019` to record where the logic went.

#### Static DD\_INSERT

A static `DD_INSERT` marks every row as an insert, so there’s no key to match and nothing to update. The mart is materialized as incremental with the **append** strategy, and neither `unique_key` nor `merge_update_columns` is generated.

Informatica:

Copy code

```
<TRANSFORMATION NAME="UPD_orders_insert" TYPE="Update Strategy">
   <!-- order_id, customer_name, amount, status input/output ports omitted -->
   <TABLEATTRIBUTE NAME="Update Strategy Expression" VALUE="DD_INSERT"/>
   <TABLEATTRIBUTE NAME="Forward Rejected Rows" VALUE="YES"/>
</TRANSFORMATION>
```

Snowflake (`int_UPD_orders_insert.sql`):

Copy code

```
--** SSC-FDM-INF0019 - THE UPDATE STRATEGY LOGIC WAS MOVED TO THE TARGET MODEL. **
SELECT
   order_id,
   customer_name,
   amount,
   status
FROM
   {{ ref('stg_raw__SQ_upd_src_orders') }}
```

Snowflake (mart model):

Copy code

```
{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}
SELECT
   order_id,
   customer_name,
   amount,
   status
FROM
   {{ ref('int_UPD_orders_insert') }}
```

#### Static DD\_DELETE

A static `DD_DELETE` marks every row for deletion, and a dbt materialization can’t express that on its own. The Update Strategy model is materialized as a **table** so the keys to remove are queryable, and the mart runs a `pre_hook` that deletes those keys from itself before the model body runs. The model body then selects `WHERE FALSE`, so the run removes rows without adding any.

Informatica:

Copy code

```
<TRANSFORMATION NAME="UPD_orders_delete" TYPE="Update Strategy">
   <!-- order_id, customer_name, amount, status input/output ports omitted -->
   <TABLEATTRIBUTE NAME="Update Strategy Expression" VALUE="DD_DELETE"/>
   <TABLEATTRIBUTE NAME="Forward Rejected Rows" VALUE="YES"/>
</TRANSFORMATION>
```

Snowflake (`int_UPD_orders_delete.sql`):

Copy code

```
{{ config(
    materialized='table'
) }}
--** SSC-FDM-INF0019 - THE UPDATE STRATEGY LOGIC WAS MOVED TO THE TARGET MODEL. **
SELECT
   order_id,
   customer_name,
   amount,
   status
FROM
   {{ ref('stg_raw__SQ_upd_src_orders') }}
```

Snowflake (mart model):

Copy code

```
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    pre_hook="
      DELETE FROM {{ this }}
      WHERE (order_id) IN (
        SELECT order_id
        FROM {{ ref('int_UPD_orders_delete') }}
      )
    "
) }}
SELECT
   order_id,
   customer_name,
   amount,
   status
FROM
   {{ ref('int_UPD_orders_delete') }}
WHERE
   FALSE
```

#### Conditional expressions

When the Update Strategy expression is conditional, the DD action is decided per row instead of once for the whole load, so the action becomes a `CASE` expression. Nested `IIF` calls become successive `WHEN` branches, and every DD action keeps its own branch: `DD_INSERT` is 0, `DD_UPDATE` is 1, `DD_DELETE` is 2, and `DD_REJECT` is 3. The mart merges the rows that resolve to insert or update, deletes the keys that resolve to delete in a `pre_hook`, and leaves out the rows that resolve to reject.

Informatica:

Copy code

```
<TRANSFORMATION NAME="UPD_products" TYPE="Update Strategy">
   <!-- product_id, product_name, price, quantity, action_flag input/output ports omitted -->
   <TABLEATTRIBUTE NAME="Update Strategy Expression" VALUE="IIF(ISNULL(product_name) OR price &lt; 0, DD_REJECT, IIF(action_flag = &apos;D&apos;, DD_DELETE, IIF(action_flag = &apos;U&apos;, DD_UPDATE, DD_INSERT)))"/>
   <TABLEATTRIBUTE NAME="Forward Rejected Rows" VALUE="YES"/>
</TRANSFORMATION>
```

Snowflake (mart model):

Copy code

```
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='product_id',
    merge_update_columns=['product_name', 'price', 'quantity', 'action_flag'],
    pre_hook="
      DELETE FROM {{ this }}
      WHERE (product_id) IN (
        SELECT product_id
        FROM {{ ref('int_UPD_products') }}
        WHERE CASE
   WHEN (product_name IS NULL)
   OR price < 0
      THEN 3 /*REJECT*/
   WHEN action_flag = 'D'
      THEN 2 /*DELETE*/
   WHEN action_flag = 'U'
      THEN 1 /*UPDATE*/
   ELSE 0 /*INSERT*/
END = 2 /*DELETE*/
      )
    "
) }}
SELECT
   product_id,
   product_name,
   price,
   quantity,
   action_flag
FROM
   {{ ref('int_UPD_products') }}
WHERE
   CASE
      WHEN (product_name IS NULL)
      OR price < 0
         THEN 3 /*REJECT*/
      WHEN action_flag = 'D'
         THEN 2 /*DELETE*/
      WHEN action_flag = 'U'
         THEN 1 /*UPDATE*/
      ELSE 0 /*INSERT*/
   END IN (0 /*INSERT*/, 1 /*UPDATE*/)
```

Because the mart now holds the routing logic, the Update Strategy model is materialized as a table and keeps only the passthrough columns:

Copy code

```
{{ config(
    materialized='table'
) }}

--** SSC-FDM-INF0019 - THE UPDATE STRATEGY LOGIC WAS MOVED TO THE TARGET MODEL. **
SELECT
   product_id,
   product_name,
   price,
   quantity,
   action_flag
FROM
   {{ ref('stg_raw__SQ_upd_src_products') }}
```

A `DECODE` expression selects the action the same way. When the actions it selects are only inserts and updates, as in `DECODE(current_flag, 'Y', DD_INSERT, DD_UPDATE)`, a merge already covers both, so the mart needs no control filter at all:

Copy code

```
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='emp_id',
    merge_update_columns=['emp_name', 'department']
) }}
SELECT
   emp_id,
   emp_name,
   department
FROM
   {{ ref('int_UPD_emp_current') }}
```

When the `DECODE` also selects `DD_DELETE`, for example `DECODE(TRUE, status = 'new', DD_INSERT, status = 'cancelled', DD_DELETE, DD_UPDATE)`, the action selection becomes a `CASE` chain and the mart takes the same `pre_hook` and filter shape as the `IIF` example:

Copy code

```
WHERE
   CASE
      WHEN status = 'new'
         THEN 0 /*INSERT*/
      WHEN status = 'cancelled'
         THEN 2 /*DELETE*/
      ELSE 1 /*UPDATE*/
   END IN (0 /*INSERT*/, 1 /*UPDATE*/)
```

## Reuse and external logic

### Mapplet

A Mapplet is a reusable group of transformations. A Mapplet is converted into a dbt **macro** under `macros/shared_models__{mapplet_name}.sql` and called from each Mapping that uses it, so the shared logic is defined once. A Mapplet that only reads its own sources is a macro with no arguments. A passive Mapplet that sits in the Mapping’s data flow takes an `inbound_sources` dictionary, including carry columns that pass through unchanged.

A Mapplet with more than one output group isn’t converted to a runnable macro. The conversion emits a commented-out placeholder instead, and you need to recover that logic by hand.

#### Conversion behavior

Each Mapplet instance becomes an `int_{instance}` model whose body is a single macro call. The macro file lands in the Mapping’s `macros/` directory (or in a shared package when the Mapplet comes from a shared folder).

#### Example

A Mapplet that owns its sources generates a macro with no arguments. Snowflake (`int_mplt_variables_mapplet.sql`):

Copy code

```
{{ AdventureWorksETLs.shared_models__mplt_variables_mapplet() }}
```

A passive Mapplet with carry columns generates a macro that loops over those columns. Snowflake (`macros/shared_models__mplt_passive_mapplet.sql`):

Copy code

```
{% macro shared_models__mplt_passive_mapplet(inbound_sources = {}) %}
WITH passive_mapplet_input AS
(
   SELECT
      {{ inbound_sources["passive_mapplet_input"]["columns"]["string_value"] | default('null', true) }} AS string_value,
      
{% for carry_col in inbound_sources.get('passive_mapplet_input', {}).get('carry_columns', []) %}
      {{ inbound_sources['passive_mapplet_input']['source_ref'] }}.{{ carry_col[0] }} AS {{ carry_col[1] }} ,
{% endfor %}
   FROM
      {{ inbound_sources["passive_mapplet_input"]["source_ref"] }}
),
EXPTRANS AS
(
   WITH source_data AS
   (
      SELECT
         string_value,
         
{% for carry_col in inbound_sources.get('passive_mapplet_input', {}).get('carry_columns', []) %}
      {{ carry_col[1] }} ,
{% endfor %}
      FROM
         passive_mapplet_input
   )
   SELECT
      string_value AS string_value,
      string_value || 'hello' AS processed_value,
      
{% for carry_col in inbound_sources.get('passive_mapplet_input', {}).get('carry_columns', []) %}
      {{ carry_col[1] }} ,
{% endfor %}
   FROM
      source_data
),
passive_mapplet_output AS
(
   SELECT
      processed_value,
      
{% for carry_col in inbound_sources.get('passive_mapplet_input', {}).get('carry_columns', []) %}
      {{ carry_col[1] }} ,
{% endfor %}
   FROM
      EXPTRANS
)
SELECT
   *
FROM
   passive_mapplet_output
{% endmacro %}
```

The Mapping that uses that Mapplet calls it with carry columns. Snowflake (`int_mplt_passive_mapplet.sql`):

Copy code

```
{{ AdventureWorksETLs.shared_models__mplt_passive_mapplet(inbound_sources = {
    "passive_mapplet_input": {
        "source_ref": ref('stg_raw__SQ_DimEmployee'),
        "columns": {
            "string_value": "LoginID"
        }
,
        "carry_columns": [
            ["FirstName", "SQ_DimEmployee__FirstName"],
            ["LastName", "SQ_DimEmployee__LastName"]
        ]
    }
}) }}
```

#### Limitations

Reusable transformations inside a Mapplet can still emit [SSC-FDM-INF0028](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0028). A Mapplet with multiple output groups isn’t generated as a working macro.

### Reusable Expression

A reusable Expression (REUSABLE=YES) becomes `macros/shared_models__{name}.sql`, not a copy of the Expression SQL in every Mapping. The Mapping’s `int_{name}.sql` calls that macro with `inbound_sources`. The named facts assert the macro wrapper `{% macro shared_models__EXP_Shared`, `{% endmacro %}`, `UPPER(NAME)`, and `inbound_sources["source_data"]`, and that the call site contains `shared_models__EXP_Shared(inbound_sources` without `SSC-FDM-INF0028`.

A reusable Lookup doesn’t follow that path. It stays on the connected or unconnected Lookup translation and does **not** create a `shared_models__*` file, so it can’t collide with the unconnected Lookup macro.

### Java Transformation

A Java Transformation (`TYPE="Custom Transformation"` and `TEMPLATENAME="Java Transformation"`) becomes an `int_` pass-through model. The Java source is copied into comments. It isn’t executed, and [SSC-FDM-INF0045](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0045) is always emitted.

#### Conversion behavior

Pass-through (`INPUT/OUTPUT`) columns are selected from the upstream model. Input-only ports that the Java code consumed aren’t projected. Output-only ports that Java would have set aren’t computed; they emit [SSC-EWI-INF0047](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0047). When **Is Active** is `YES`, the model still pass-throughs the input rows and also emits [SSC-EWI-INF0046](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0046), because an active Java transformation can change row cardinality.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| `TEMPLATENAME` = Java Transformation | Pass-through `int_` model | Distinguishes this Custom Transformation from Union and other templates. |
| Java snippets (`OnInputRow`, imports) | SQL comments | Not applied. [SSC-FDM-INF0045](../../../issues-and-troubleshooting/functional-difference/informaticaFDM#ssc-fdm-inf0045). |
| Is Active = NO | Pass-through `SELECT` of input/output ports | Output-only ports need a manual UDF. [SSC-EWI-INF0047](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0047). |
| Is Active = YES | Pass-through plus extra EWI | Cardinality may change in Informatica. [SSC-EWI-INF0046](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0046). |

Expand

Show lessSee more

#### Example

Informatica (`java_tx_passive.xml`):

Copy code

```
<TRANSFORMATION NAME="t_maskPII" TEMPLATENAME="Java Transformation" TYPE="Custom Transformation">
   <!-- CustomerId, CustomerName, Email (input/output); PhoneNumber (input); PhoneHash (output) omitted -->
   <TABLEATTRIBUTE NAME="Language" VALUE="Java"/>
   <TABLEATTRIBUTE NAME="Is Active" VALUE="NO"/>
   <TABLEATTRIBUTE NAME="Transformation Scope" VALUE="Row"/>
</TRANSFORMATION>
```

Snowflake (`int_t_maskPII.sql` from `java_tx_passive_expected.sql`):

Copy code

```
--** SSC-FDM-INF0045 - JAVA TRANSFORMATION 't_maskPII' CONTAINS CUSTOM JAVA CODE THAT CANNOT BE AUTOMATICALLY TRANSLATED. THE FOLLOWING JAVA CODE SNIPPETS MUST BE MANUALLY MIGRATED TO SNOWFLAKE (E.G., JAVA UDF, SNOWPARK PROCEDURE, OR INLINE SQL). PASS-THROUGH COLUMNS ARE FORWARDED BUT JAVA LOGIC IS NOT APPLIED. **
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0047 - OUTPUT-ONLY PORT 'PhoneHash' IS SET BY JAVA CODE AND CANNOT BE AUTOMATICALLY TRANSLATED. MANUAL MIGRATION REQUIRED. ***/!!!
--** 
--** TRANSFORMATION SCOPE: Row
--** 
--** --- IMPORT PACKAGES ---
--** import java.security.MessageDigest;
--** 
--** --- ON INPUT ROW ---
--** // Mask email
--** if (Email != null) {
--**     Email = Email.replaceAll("(.).*(@.*)", "$1***$2");
--** }
--** // Hash phone
--** if (PhoneNumber != null) {
--**     PhoneHash = PhoneNumber.hashCode() + "";
--** }
--** **
WITH source_data AS
(
   SELECT
      CustomerId,
      CustomerName,
      Email,
      PhoneNumber
   FROM
      {{ ref('stg_raw__SQ_Customer') }}
)
SELECT
   CustomerId,
   CustomerName,
   Email
FROM
   source_data
```

An active Java Transformation still doesn’t run the Java. Snowflake (`java_tx_active_expected.sql`):

Copy code

```
--** SSC-FDM-INF0045 - JAVA TRANSFORMATION 't_activeJava' CONTAINS CUSTOM JAVA CODE THAT CANNOT BE AUTOMATICALLY TRANSLATED. THE FOLLOWING JAVA CODE SNIPPETS MUST BE MANUALLY MIGRATED TO SNOWFLAKE (E.G., JAVA UDF, SNOWPARK PROCEDURE, OR INLINE SQL). PASS-THROUGH COLUMNS ARE FORWARDED BUT JAVA LOGIC IS NOT APPLIED. **
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0046 - ACTIVE JAVA TRANSFORMATION 't_activeJava' CANNOT BE AUTOMATICALLY TRANSLATED. THE TRANSFORMATION MAY CHANGE ROW CARDINALITY. MANUAL MIGRATION TO A SNOWFLAKE JAVA UDTF OR SNOWPARK PROCEDURE IS REQUIRED. ***/!!!
--** 
--** TRANSFORMATION SCOPE: All Input
--** 
--** --- ON INPUT ROW ---
--** generateRow();
--** Derived = CustomerName.toUpperCase();
--** generateRow();
--** **
WITH source_data AS
(
   SELECT
      CustomerId,
      CustomerName
   FROM
      {{ ref('stg_raw__SQ_Customer') }}
)
SELECT
   *
FROM
   source_data
```

#### Limitations

Migrate the Java to a Snowflake Java UDF, Java UDTF, or Snowpark procedure. The generated model never claims to execute the original Java.

### Stored Procedure

A connected Stored Procedure whose type is **Normal** becomes an `int_` model that calls the procedure as a per-row UDF and extracts output fields from the returned object. That isn’t a Snowflake `CALL`. The conversion emits [SSC-EWI-INF0040](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0040) so you can convert the procedure to a UDF that returns `OBJECT_CONSTRUCT` with names matching the output ports.

A disconnected Stored Procedure (source or target pre-load or post-load) doesn’t participate in the data flow. It becomes a folder-level `pre-hook` or `post-hook` in `dbt_project.yml`.

#### Conversion behavior

Connected Normal: wrap the upstream rows in `source_data`, call `schema.proc(...)` once per row, and project `:outputPort` fields. Disconnected: Source Pre Load and Source Post Load attach to the `staging` folder; Target Pre Load and Target Post Load attach to `marts`.

#### Property mapping

| Source property | Snowflake / dbt | Notes |
| --- | --- | --- |
| Stored Procedure Type = Normal (connected) | Per-row UDF expression in an `int_` model | [SSC-EWI-INF0040](../../../issues-and-troubleshooting/conversion-issues/informaticaEWI#ssc-ewi-inf0040). Not `CALL`. |
| Stored Procedure Name | UDF or `CALL` target | May be schema-qualified. |
| Stored Procedure Type = Source/Target Pre/Post Load | `pre-hook` / `post-hook` in `dbt_project.yml` | Disconnected only. |
| Call Text (disconnected) | `CALL` statement in the hook | Used for pre-load and post-load types, not for connected Normal. |

Expand

Show lessSee more

#### Example

**Connected Normal.** Informatica (`stored_procedure_happy_path.xml`):

Copy code

```
<TRANSFORMATION NAME="SP_CalcTax" TYPE="Stored Procedure">
   <!-- inSalary (input), outTaxAmount (output), RETURN_VALUE (return/output) omitted -->
   <TABLEATTRIBUTE NAME="Stored Procedure Name" VALUE="dbo.sp_calc_tax"/>
   <TABLEATTRIBUTE NAME="Connection Information" VALUE="$Target"/>
   <TABLEATTRIBUTE NAME="Stored Procedure Type" VALUE="Normal"/>
</TRANSFORMATION>
```

Snowflake (`int_SP_CalcTax.sql`):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0040 - THE STORED PROCEDURE TRANSFORMATION 'SP_CalcTax' IS TRANSLATED ASSUMING THE PROCEDURE HAS BEEN CONVERTED TO A UDF. THE ORIGINAL INFORMATICA TRANSFORMATION CALLED THE PROCEDURE ONCE PER ROW. THE TRANSLATION CALLS IT AS AN INLINE UDF. CONVERT THE STORED PROCEDURE TO A SNOWFLAKE UDF THAT RETURNS OBJECT_CONSTRUCT WITH NAMED FIELDS MATCHING THE OUTPUT PORT NAMES. ***/!!!
WITH source_data AS
(
   SELECT
      Salary AS inSalary,
      EmpID AS SQ_SRC_EMPLOYEES__EmpID,
      Salary AS SQ_SRC_EMPLOYEES__Salary
   FROM
      {{ ref('stg_raw__SQ_SRC_EMPLOYEES') }}
),
sp_result AS
(
   SELECT
      source_data.*,
      dbo.sp_calc_tax(source_data.inSalary, source_data.SQ_SRC_EMPLOYEES__EmpID, source_data.SQ_SRC_EMPLOYEES__Salary):outTaxAmount :: NUMBER AS outTaxAmount,
      dbo.sp_calc_tax(source_data.inSalary, source_data.SQ_SRC_EMPLOYEES__EmpID, source_data.SQ_SRC_EMPLOYEES__Salary):RETURN_VALUE :: NUMBER AS RETURN_VALUE
   FROM
      source_data
)
SELECT
   *
FROM
   sp_result
```

**Disconnected hooks.** Target Pre Load becomes a marts `pre-hook`. Snowflake (`dbt_project.yml`):

Copy code

```
name: YOUR_PROJECT_NAME
version: 1.0.0
config-version: 2
profile: YOUR_PROFILE_NAME
model-paths:
  - models
analysis-paths:
  - analyses
test-paths:
  - tests
seed-paths:
  - seeds
macro-paths:
  - macros
snapshot-paths:
  - snapshots
models:
  YOUR_PROJECT_NAME:
    staging:
      +materialized: view
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: incremental
      +pre-hook:
        - CALL dbo.TRUNCATE_TABLE('EMPLOYEES_STG')
vars:
  SESSSTARTTIME: 1753-01-01 00:00:00
  PMSESSIONNAME: null
  PMWORKFLOWNAME: null
```

All four Informatica hook slots map to dbt folders. Snowflake (`dbt_project.yml` excerpt):

Copy code

```
          staging:
            +materialized: view
            +pre-hook:
              - CALL dbo.INIT_LOAD_LOG('order_table', 'start_time')
            +post-hook:
              - CALL dbo.LOG_SOURCE_COMPLETE('ORDERS')
          intermediate:
            +materialized: ephemeral
          marts:
            +materialized: incremental
            +pre-hook:
              - CALL dbo.TRUNCATE_TABLE('ORDERS_FACT')
            +post-hook:
              - CALL dbo.REFRESH_AGGREGATES()
```

#### Limitations

Convert the connected procedure to a Snowflake UDF before you run the model. Named database connections can still raise an EWI so you can confirm the target.

## Targets

### Target Definition

A Target Definition becomes a **mart model** named after the target table. It reads from the last intermediate model in the Mapping and aliases the columns to the target’s column names.

Informatica (`m_dummy_source_target_test.XML`):

Copy code

```
<TARGET NAME="TargetTable" DATABASETYPE="Microsoft SQL Server">
   <TARGETFIELD NAME="TotalPrice" DATATYPE="decimal" PRECISION="19" SCALE="4"/>
   <TARGETFIELD NAME="gender" DATATYPE="char" PRECISION="1"/>
   <TARGETFIELD NAME="fullName" DATATYPE="varchar" PRECISION="101"/>
   <TARGETFIELD NAME="description" DATATYPE="varchar" PRECISION="500"/>
</TARGET>
```

Snowflake (`TargetTable.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
       t_dummy_filter_1__TotalPrice,
      GENDER,
       t_dummy_filter_1__description
   FROM
      {{ ref('int_t_dummy_gender') }}
)
SELECT
    sd.t_dummy_filter_1__TotalPrice AS TotalPrice,
    sd.GENDER AS gender,
    sd.t_dummy_filter_1__description AS description
FROM
    source_data AS sd
```

Mapping-level or session **Post SQL** on the Target becomes a mart `post_hook`. Snowflake (`TargetFlatPostSql.sql`):

Copy code

```
{{ config(
    post_hook="TRUNCATE TABLE mapping_staging"
) }}
WITH source_data AS
(
   SELECT
      EmployeeKey,
      FirstName
   FROM
      {{ ref('stg_raw__SQ_DimEmployee') }}
)
SELECT
   sd.EmployeeKey AS EmployeeKey,
   sd.FirstName AS FirstName
FROM
   source_data AS sd
```

When the Mapping includes an Update Strategy, the mart is materialized incrementally with a merge, as shown in [Update Strategy](#update-strategy).

### Flat File Target

A delimited flat-file Target Definition becomes a mart model materialized as a table, with a `post_hook` that calls a generated `copy_into_stage` macro to unload the model’s rows to a stage. The unload is bound to `public.landing_stage/infpc/targets/<Def>/` and carries the field delimiter, text qualifier, and record delimiter declared on the Flat File Target, so you don’t need to supply a stage path or a dbt variable of your own. This target prefix is an unload destination, not a landing source for the ingestion manifest or Openflow.

Two Informatica settings have no Snowflake equivalent when writing to a stage, and each raises an EWI on the mart model:

- A codepage on the target. Snowflake always writes UTF-8 when it unloads to a stage, so the encoding is dropped.
- An escape character. Snowflake’s CSV unload has no escape-character option, so fields that contain the delimiter have to be enclosed instead.

A fixed-width flat-file Target can’t be mapped to a Snowflake file format at all. Its mart model projects `null` for every column and carries an EWI so you can write the unload by hand.

## Direct copy loads

Some Sessions do nothing but move a static flat file into a relational table: a flat-file source, a Source Qualifier with no filter and no SQL override, and a target with no pre-SQL or post-SQL. SnowConvert folds that shape into a single `COPY INTO` statement inside the Workflow’s Task and doesn’t generate a dbt project for it. There are no models, no `sources.yml`, and no `EXECUTE DBT PROJECT` call, because there’s no transformation for dbt to run.

Informatica (`flat_file_direct_copy.xml`):

Copy code

```
<SESSION NAME="s_DIRECT_LOAD" MAPPINGNAME="m_DIRECT_LOAD">
   <SESSIONEXTENSION NAME="File Reader" SINSTANCENAME="SRC_DIRECT_CSV" SUBTYPE="File Reader" TYPE="READER">
      <ATTRIBUTE NAME="Source filename" VALUE="employees.csv"/>
   </SESSIONEXTENSION>
   <!-- Relational Writer extension and session attributes omitted -->
</SESSION>
```

Snowflake (`WF_DIRECT_LOAD.sql`):

Copy code

```
CREATE OR REPLACE TASK public.WF_DIRECT_LOAD
AS
SELECT
1;
CREATE OR REPLACE TASK public.TestFolder_WF_DIRECT_LOAD_s_DIRECT_LOAD
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.WF_DIRECT_LOAD
AS
BEGIN
   ---- Start block 'TestFolder.WF_DIRECT_LOAD.s_DIRECT_LOAD'
   COPY INTO YOUR_DB.YOUR_SCHEMA.TGT_EMPLOYEES (
      EMP_ID,
      EMP_NAME,
      COMPENSATION
   )
   FROM
   (
      SELECT
         $1 :: VARCHAR(10),
         $2 :: VARCHAR(100),
         $3 :: FLOAT
      FROM
         @public.landing_stage/infpc/sources/TestFolder/SRC_DIRECT_CSV/employees.csv (FILE_FORMAT => 'TestFolder_m_DIRECT_LOAD_SRC_DIRECT_CSV')
   );
   ---- End block 'TestFolder.WF_DIRECT_LOAD.s_DIRECT_LOAD'

END;
```

Alongside the Task, the conversion writes the two setup files the `COPY INTO` depends on. `file_formats.sql` holds the file format the read binds by name:

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS TestFolder_m_DIRECT_LOAD_SRC_DIRECT_CSV
TYPE = 'CSV'
FIELD_DELIMITER = ','
ENCODING = 'WINDOWS1252'
SKIP_HEADER = 1
EMPTY_FIELD_AS_NULL = TRUE;
```

Important

Replace the `YOUR_DB` and `YOUR_SCHEMA` placeholders in the `COPY INTO` target with your actual Snowflake database and schema. Generated Openflow flows copy the file from customer object storage onto the generated internal stage path that the `COPY INTO` statement reads. See the [Informatica PowerCenter overview](../README).

A Session qualifies for this shortcut only when it’s a pure load with a static source-to-table identity. When it isn’t, for example the Source Qualifier has a filter, the target has pre-SQL, or the Session doesn’t name a source file, the Session converts as a full dbt project instead. A parameterized source-to-table identity remains on the dbt or Snowflake Scripting path. SnowConvert doesn’t ship parameterized Direct COPY.
