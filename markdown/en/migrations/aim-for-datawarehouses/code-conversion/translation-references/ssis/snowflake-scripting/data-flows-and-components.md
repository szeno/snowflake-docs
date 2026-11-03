# SSIS - Snowflake Scripting data flows and components

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This page describes how an SSIS Data Flow Task is converted to a Snowflake [stored procedure](/sql-reference/sql/create-procedure) in the Snowflake Scripting output format. For the dbt output format, see [dbt data flows and components](../mappings-and-transformations). For the supported-component matrix, see the [Snowflake Scripting overview](README).

Warning

The Snowflake Scripting output format is in active development, so the generated code may change between releases. A component that isn’t converted produces a placeholder marked with an EWI code, as shown in [Unsupported components](#unsupported-components). For the current status of each component, see [Supported components](README#supported-components).

## The data flow procedure

Each Data Flow Task becomes one stored procedure named `public.<DataFlowName>`, where spaces in the Data Flow Task name are replaced by underscores. The procedure takes a single `scope` parameter, returns `VARCHAR`, and runs as the caller. The Data Flow becomes the body, wrapped in a `BEGIN ... END` block:

Copy code

```
CREATE OR REPLACE PROCEDURE public.Complete_Data_Flow (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      -- Source and transformation CTEs, then the destination INSERT.
   END
$$;
```

The conversion builds the body in data-flow order:

1. If the Data Flow reads package variables, a `LET` declaration for each one reads its value with `GetControlVariableUDF` and the `scope` parameter.
2. Each source becomes a CTE.
3. Each transformation becomes a CTE that reads the CTE before it, or a temporary table when more than one later statement reads its result.
4. Each destination becomes an `INSERT` statement that carries the upstream CTEs inside its source query.

The CTEs are nested inside the `INSERT` rather than placed before it, because Snowflake Scripting doesn’t accept a leading `WITH` clause as a statement inside a [`BEGIN ... END` block](/developer-guide/snowflake-scripting/blocks).

The `scope` parameter is forwarded from the calling Task so the procedure resolves the same package variables that the Task graph set at runtime. The Task sets the scope to the package name and calls the procedure:

Copy code

```
CREATE OR REPLACE TASK public.completedataflow_complete_data_flow
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.completedataflow
AS
BEGIN
   LET scope VARCHAR := 'CompleteDataFlow';
   CALL public.Complete_Data_Flow(:scope);
END;
```

When the Data Flow reads a package variable, for example through a parameter of an OLE DB Source SQL command, the procedure reads the variable at the top of the body and uses it as a bind variable (see [OLE DB Source](#ole-db-source)):

Copy code

```
LET User_MinValue FLOAT := public.GetControlVariableUDF('User_MinValue', :scope) :: FLOAT;
```

## Naming conventions

Every generated object name is derived from the name of the SSIS component it came from. The procedure keeps the original casing of the Data Flow Task name, and the CTE and temporary table names are lowercased. Spaces become underscores in all of them:

| Name | What it is |
| --- | --- |
| `public.<Data_Flow_Task_name>` | The stored procedure for a Data Flow Task. A numeric suffix such as `Data_Flow_Task_1` keeps names unique within a package. |
| `cte_<component>` | The CTE for a source or transformation, for example `cte_ole_db_source`. When two components have the same name, a numeric suffix keeps the CTE names unique, for example `cte_ole_db_source_1`. |
| `tmp_cte_<component>` | The same step, persisted as a temporary table because more than one later statement reads it. |

Expand

Show lessSee more

## Direct loads

Two Data Flow shapes skip the CTE chain. They are decided by the shape of the whole graph, not by an option, so check the generated output to see which path each Data Flow took.

### Direct INSERT

A Data Flow that only moves rows from one relational table into another relational table becomes a single `INSERT INTO ... SELECT` statement. The eligible shapes are a source that feeds a destination directly, or a source that feeds a destination through one Data Conversion or Row Count. The source must be an OLE DB, ADO.NET, or Oracle read of one named table or view, and the destination must be an OLE DB or Oracle destination that writes one named table. A source that runs a SQL command, takes its table name from a variable, or binds parameters isn’t eligible. A Data Conversion qualifies only when every conversion fails the component on error and truncation and the destination reads its normal output, and a Row Count qualifies only when it publishes exactly one output variable. A Data Flow inside a ForEach File container isn’t eligible either. The dbt output also uses this direct load.

Because the whole Data Flow is one statement, no procedure is created. The statement is written into the package Task:

Copy code

```
CREATE OR REPLACE TASK public.simpledataflow_simple_data_flow
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.simpledataflow
AS
BEGIN
   ---- Start block 'Package\Simple Data Flow'
   INSERT INTO dbo.TargetTable (Id, Name, Value)
   SELECT
      Id,
      Name,
      Value
   FROM
      SourceDB.dbo.SourceTable;
   ---- End block 'Package\Simple Data Flow'

END;
```

When the Data Flow includes a Row Count, the Row Count variable is updated after the `INSERT` from `SQLROWCOUNT`:

Copy code

```
INSERT INTO dbo.TBUG_DTBL1 (name)
SELECT
   name
FROM
   PBISMALL.dbo.TBUG_TBL1;
CALL public.UpdateControlVariable('User_rc1', 'RowCountConcurrency', TO_VARIANT(SQLROWCOUNT));
```

### Direct COPY

A Data Flow that only moves an eligible Flat File Source into an OLE DB Destination becomes a single `COPY INTO` statement. In the Snowflake Scripting format, the statement is created as a procedure, and the Task calls it with the package scope. The flat file connection manager becomes a named file format that carries the field delimiter, the number of header lines to skip, and null handling. The file itself is read from the shared `public.landing_stage`.

Snowflake (`Data_Flow_Task.sql`):

Copy code

```
CREATE OR REPLACE PROCEDURE public.Data_Flow_Task (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
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
            @public.landing_stage/ssis/DirectFlatFileLoad/OrdersFlatFile/input.csv (FILE_FORMAT => 'DirectFlatFileLoad_Data_Flow_Task_Orders_Source')
      )
      FORCE = TRUE;
   END
$$;
```

Snowflake (`etl_configuration/file_formats/file_formats.sql`):

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS DirectFlatFileLoad_Data_Flow_Task_Orders_Source
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
EMPTY_FIELD_AS_NULL = TRUE;
```

Every converted flat-file read binds to the generated `public.landing_stage`, so the file must be landed under the prefix the statement reads before the procedure runs. For the stage prefixes, the ingestion manifest, and the Openflow flows that land the files, see [Ingestion](../README#ingestion). For ForEach File containers, which keep their loop in the Task graph, see [ForEach File containers](../README#foreach-file-containers). A Flat File Source that isn’t an eligible Direct COPY becomes a placeholder. See [Unsupported components](#unsupported-components).

## Sources

### OLE DB Source

An OLE DB Source becomes a CTE named `cte_<component>` that selects the exposed columns from the source table. In SQL command access mode, the command is converted as embedded SQL from Transact-SQL to Snowflake SQL and becomes the body of the CTE.

#### Example

Table or view access mode (`cte_ole_db_source`):

Copy code

```
WITH cte_ole_db_source AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      dbo.SrcAggSum
)
```

SQL command access mode:

Copy code

```
WITH cte_ole_db_source AS
(
   --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "SsisPocTest.dbo.SrcHappy" **
   SELECT
      Id,
      Name,
      Value
   FROM
      SsisPocTest.dbo.SrcHappy
   WHERE
      Value > 10
)
```

When the migration input doesn’t include the definitions of the tables that the command reads, the CTE is flagged with [SSC-FDM-0007](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007).

A parameter marker (`?`) in the command is replaced by the package variable that the component binds it to. The procedure declares the variable at the top of its body and uses it as a bind variable:

Copy code

```
LET User_MinValue FLOAT := public.GetControlVariableUDF('User_MinValue', :scope) :: FLOAT;
INSERT INTO dbo.TgtParam (Id, Name, Value)
WITH cte_ole_db_source AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      SsisPocTest.dbo.SrcParam
   WHERE
      Value > :User_MinValue
)
SELECT
   Id,
   Name,
   Value
FROM
   cte_ole_db_source;
```

#### Limitations

A source whose table name or SQL command comes from a variable isn’t converted, because the rows only exist once the source runs. It becomes a placeholder marked with [SSC-EWI-SSIS0001](../../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001).

A SQL command that can’t be converted to Snowflake SQL, or whose parameter markers don’t match its bindings, becomes a placeholder marked with [SSC-EWI-SSIS0003](../../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0003). Declining a command with unmatched markers avoids emitting a query that silently filters on the wrong value. Convert the command by hand and replace the `NULL` columns:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL CANNOT BE CONVERTED FROM Transact TO SNOWFLAKE SQL ***/!!!
cte_ole_db_source AS
(
   SELECT
      null AS Id,
      null AS Name,
      null AS Value
)
```

### ADO.NET Source and Oracle Source

An ADO.NET Source becomes a `cte_ado_net_source` CTE, and an Oracle Source becomes a `cte_oracle_source` CTE. Both follow the same rules as the OLE DB Source: a table read selects the exposed columns, and a SQL command is converted and used as the body of the CTE.

Copy code

```
WITH cte_oracle_source AS
(
   --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "ORCL.hr.employees" **
   SELECT
      employee_id,
      full_name,
      department
   FROM
      ORCL.hr.employees
   WHERE
      active = 1
)
```

### Excel Source

An Excel Source becomes a CTE that reads the staged workbook through the generated `excel_source_udf` function. The function takes the stage path of the workbook, which the conversion stores in a package variable, the sheet name, and whether the first row is a header. Each column is read from the row object and cast to its SSIS type: text columns use `:: VARCHAR`, and numeric columns use `TRY_TO_DOUBLE`.

Copy code

```
WITH cte_excel_source AS
(
   SELECT
      data['ProductName'] :: VARCHAR AS ProductName,
      TRY_TO_DOUBLE(data['Quantity'] :: VARCHAR) AS Quantity,
      TRY_TO_DOUBLE(data['UnitPrice'] :: VARCHAR) AS UnitPrice,
      TRY_TO_DOUBLE(data['TotalAmount'] :: VARCHAR) AS TotalAmount
   FROM
      TABLE(excel_source_udf(GetControlVariableUDF('Package_Data_Flow_Task_Excel_Source_stage_file_path', :scope), 'Sales', 'YES')) AS excel_raw
)
```

The workbook must be landed on the stage before the procedure runs. See [Ingestion](../README#ingestion).

## Row-level transformations

### Derived Column

A Derived Column becomes a CTE whose `SELECT` list carries one translated expression per derived column, followed by the columns that pass through unchanged. SSIS expressions become their Snowflake equivalents: string concatenation with `+` becomes `||`, the SSIS equality operator `==` becomes `=`, and functions such as `LOWER` keep their names.

#### Example

SSIS expressions: `FirstName + " " + LastName` and `LOWER(Email)`.

Copy code

```
cte_derived_column AS
(
   SELECT
      FirstName || ' ' || LastName AS FullName,
      LOWER(Email) AS NormalizedEmail,
      CustomerId,
      FirstName,
      LastName,
      Email,
      IsActive
   FROM
      cte_conditional_split
)
```

#### Limitations

If one expression in a Derived Column can’t be converted, the whole component becomes a placeholder marked with SSC-EWI-SSIS0001, and its columns return `NULL`. Fix the expression by hand, or use the [dbt output format](../README).

### Data Convert

A Data Convert becomes a CTE that passes through the input columns and adds one cast for each conversion, aliased to the component’s output column name. Snowflake `::` casts are used. In the following example, the list of pass-through columns is shortened:

Copy code

```
cte_data_conversion AS
(
   SELECT
      Bike,
      CustomerName,
      Helmet,
      Gloves,
      Bike :: INTEGER AS BikeConverted
   FROM
      cte_pivot
)
```

### Row Count

A Row Count becomes a pass-through CTE that selects its output columns from the CTE before it. The rows flow downstream unchanged:

Copy code

```
cte_row_count AS
(
   SELECT
      FullName,
      NormalizedEmail,
      CustomerId,
      FirstName,
      LastName,
      Email,
      IsActive
   FROM
      cte_derived_column
)
```

#### Limitations

The procedure doesn’t write the row count into the SSIS package variable that the Row Count publishes, and the conversion doesn’t emit an EWI for it. If a later task reads that variable, set it yourself. The exception is the [Direct INSERT](#direct-insert) shape, which updates the variable from `SQLROWCOUNT`.

### Multicast

A Multicast becomes a pass-through CTE. When the Multicast feeds more than one destination, its result is read by more than one statement, so it’s persisted as a temporary table. See [Multiple destinations](#multiple-destinations).

### Cache Transform

A Cache Transform becomes a pass-through CTE that selects its columns from the CTE before it. The cache itself isn’t materialized.

Copy code

```
cte_cache_transform AS
(
   SELECT
      name,
      salary
   FROM
      cte_ole_db_source
)
```

### OLE DB Command

An OLE DB Command that runs a stored procedure becomes a call that runs once for each incoming row. The conversion persists the incoming rows as a temporary table, then runs an `EXECUTE IMMEDIATE` block that opens a cursor over them and calls the procedure for each row. Snowflake rejects `:rec.COLUMN` inside a `CALL`, so each field is first assigned to a declared variable and then passed as a bind variable.

For a command that runs `dbo.usp_WriteHistory` with the `ID` and `NAME` columns, the block that `EXECUTE IMMEDIATE` runs is:

Copy code

```
DECLARE arg_0 VARIANT; arg_1 VARIANT; c1 CURSOR FOR SELECT ID, NAME FROM cte_ole_db_command; BEGIN OPEN c1; FOR rec IN c1 DO arg_0 := rec.ID; arg_1 := rec.NAME; CALL dbo.usp_WriteHistory(:arg_0, :arg_1); END FOR; CLOSE c1; END
```

The block calls the procedure once for each row, so a command that handles many rows runs many calls. A command that has no input columns becomes a single `CALL <procedure>()`.

#### Limitations

An OLE DB Command that runs an `INSERT`, `UPDATE`, or `DELETE` statement isn’t converted in this format and becomes a placeholder marked with SSC-EWI-SSIS0001. The dbt output converts these commands into an incremental model.

## Routing and combining data

### Conditional Split

A Conditional Split is converted in one of two ways, depending on where its outputs go.

When one output continues the pipeline, the split becomes a CTE that filters the rows with that output’s condition. The SSIS condition `IsActive == TRUE` becomes `IsActive = TRUE`:

Copy code

```
cte_conditional_split AS
(
   SELECT
      CustomerId,
      FirstName,
      LastName,
      Email,
      IsActive
   FROM
      cte_ole_db_source
   WHERE
      IsActive = TRUE
)
```

When every output writes directly to a destination, the split owns the writes. It persists the input rows in a temporary table with a routing column, `ssis_output_name`, that holds the name of the output each row belongs to. The conversion then emits one `INSERT` for each destination, filtered by that name. The routing column is a `CASE` expression that lists the conditions in the order SSIS evaluates them, so each row goes to the first output whose condition is true, and rows that match no condition go to the default output.

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_cte_conditional_split AS
   WITH cte_employees AS
   (
      SELECT
         EmployeeKey,
         FirstName,
         LastName,
         BaseRate
      FROM
         dbo.DimEmployee
   )
   SELECT
      EmployeeKey,
      FirstName,
      LastName,
      BaseRate,
      CASE
         WHEN BaseRate < 10
            THEN 'Low'
         WHEN BaseRate < 20
            THEN 'Mid'
         WHEN BaseRate < 40
            THEN 'Large'
         ELSE 'Other rates'
      END AS ssis_output_name
   FROM
      cte_employees;
INSERT INTO "Low Rates" (EmployeeKey, FirstName, LastName, BaseRate)
SELECT
   EmployeeKey,
   FirstName,
   LastName,
   BaseRate
FROM
   tmp_cte_conditional_split
WHERE
   ssis_output_name = 'Low';
```

The `INSERT` statements for the `Mid`, `Large`, and `Other rates` outputs follow the same pattern.

#### Limitations

A Conditional Split that has an empty or duplicate output name, a condition that can’t be converted, or outputs that mix direct destinations with other components becomes a placeholder marked with SSC-EWI-SSIS0001.

The destinations in this example are Flat File Destinations. A Flat File Destination that receives rows from a Conditional Split is written with an `INSERT` into a table named after its connection manager. No file is written. Review these statements, and create the table or retarget the `INSERT` before you run the procedure. Flat File Destinations in any other position become placeholders. See [Unsupported components](#unsupported-components).

### Union All

A Union All becomes a CTE that combines every input with `UNION ALL`, which preserves duplicate rows the way SSIS does. Each input column is aliased to the Union All output column that it maps to:

Copy code

```
cte_union_all AS
(
   SELECT
      CustomerKey AS Key,
      FirstName AS Name
   FROM
      cte_ole_db_source
   UNION ALL
   SELECT
      EmployeeKey AS Key,
      FirstName AS Name
   FROM
      cte_ole_db_source_1
   UNION ALL
   SELECT
      ResellerKey AS Key,
      ResellerName AS Name
   FROM
      cte_ole_db_source_2
)
```

### Merge

A Merge becomes a CTE that combines its two inputs with `UNION ALL`. A column that exists in only one input is padded with `NULL` in the other branch.

SSIS requires sorted inputs for a Merge and produces a sorted output. `UNION ALL` doesn’t guarantee an order, so the CTE is flagged with [SSC-FDM-SSIS0002](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0002). Add an `ORDER BY` to the final query if row order matters downstream.

Copy code

```
--** SSC-FDM-SSIS0002 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. THE SSIS MERGE TRANSFORMATION ASSUMES SORTED INPUTS AND NATURALLY PRODUCES A SORTED, DETERMINISTIC OUTPUT. THE EQUIVALENT SQL UNION ALL DOES NOT GUARANTEE ORDER. **
cte_merge AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      cte_ole_db_source
   UNION ALL
   SELECT
      Id,
      Name,
      Value
   FROM
      cte_ole_db_source_1
)
```

### Merge Join

A Merge Join becomes a CTE that joins its left and right inputs on the join keys. The join type of the component decides the SQL join: inner, left outer, or full outer. Each output column is selected from the input that SSIS maps it to, through the `left_source` and `right_source` aliases.

Like the Merge, the Merge Join assumes sorted inputs and produces a sorted output, so the CTE is flagged with [SSC-FDM-SSIS0004](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0004).

Copy code

```
--** SSC-FDM-SSIS0004 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. THE SSIS MERGE JOIN TRANSFORMATION ASSUMES SORTED INPUTS AND NATURALLY PRODUCES A SORTED, DETERMINISTIC OUTPUT. THE EQUIVALENT SQL JOIN DOES NOT GUARANTEE ORDER. **
cte_merge_join AS
(
   SELECT
      left_source.Id,
      left_source.Name,
      right_source.Value
   FROM
      cte_left_source AS left_source
      INNER JOIN
         cte_right_source AS right_source
         ON left_source.Id = right_source.Id
)
```

### Lookup

A Lookup that matches the supported shape becomes a temporary table that left-joins the input rows to the reference query, plus one `INSERT` for each destination the Lookup feeds. The temporary table adds a match marker column, `ssis_lookup_matched_key`, taken from the reference key. A matched output writes the rows where the marker isn’t `NULL`, and a no-match output writes the rows where it is `NULL`.

The Lookup is converted only when it has all of these properties: an OLE DB connection, the **No cache** mode, a SQL query for the reference rows, a single equality condition, and exactly one column that it adds to the rows. Its no-match behavior must be **Fail component** or **Redirect rows to no match output**, and its outputs must connect directly to destinations.

#### Example

A Lookup that enriches each row with `RefName` and writes the matched rows. In this example, the reference query returns constant rows, so the converted query is a `VALUES` list. The reference query is converted as embedded SQL, the same way an OLE DB Source SQL command is, so a query that reads a table keeps its `FROM` clause:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_cte_lookup_reference AS
   WITH cte_ole_db_source AS
   (
      SELECT
         Id,
         Name,
         Value
      FROM
         dbo.LookupMatchSrc
   )
   SELECT
      lookup_input.Id,
      lookup_input.Name,
      lookup_input.Value,
      lookup_reference.RefName,
      lookup_reference.Id AS ssis_lookup_matched_key
   FROM
      cte_ole_db_source AS lookup_input
      LEFT JOIN
         (
            SELECT
               Id,
               RefName
            FROM
               (VALUES(1, 'North'), (2, 'South')) AS reference_data (
                  Id,
                  RefName
               )
         ) AS lookup_reference
         ON lookup_input.Id = lookup_reference.Id;
INSERT INTO dbo.LookupMatchTgt (Id, Name, Value, RefName)
SELECT
   Id,
   Name,
   Value,
   RefName
FROM
   tmp_cte_lookup_reference
WHERE
   ssis_lookup_matched_key IS NOT NULL;
```

When the Lookup redirects unmatched rows to a no-match output, the destination of that output reads the rows where the marker is `NULL`:

Copy code

```
INSERT INTO dbo.LookupRedirectTgt (Id, Name, Value)
SELECT
   Id,
   Name,
   Value
FROM
   tmp_cte_lookup_reference
WHERE
   ssis_lookup_matched_key IS NULL;
```

#### Limitations

A Lookup outside the supported shape, such as one that caches its reference rows or joins on several columns, becomes a placeholder marked with SSC-EWI-SSIS0001. Use the [dbt output format](../README) for those Lookups.

With **Fail component** as the no-match behavior, SSIS stops the Data Flow when a row has no match. The procedure doesn’t fail. It writes only the matched rows, so unmatched rows are dropped without an error. If a missing match must stop the load, add that check yourself.

## Aggregation and ordering

### Aggregate

An Aggregate becomes a CTE with a `GROUP BY` over the group-by columns. Each aggregation is renamed to the output column that SSIS exposes, so a group-by column can be renamed in the same step. An Aggregate with no group-by columns aggregates over the whole input and produces a single row.

#### Example

An Aggregate that groups by `Name`, exposes it as `Category`, and calculates a sum and a row count:

Copy code

```
cte_aggregate AS
(
   SELECT
      Name AS Category,
      SUM(Value) AS TotalValue,
      COUNT(*) AS RowCnt
   FROM
      cte_ole_db_source
   GROUP BY
      Name
)
```

The aggregation operations map as follows:

| SSIS operation | Snowflake |
| --- | --- |
| Count all | `COUNT(*)` |
| Count | `COUNT(col)`, which ignores `NULL` values |
| Count distinct | `COUNT(DISTINCT col)` |
| Sum, Minimum, Maximum | `SUM(col)`, `MIN(col)`, `MAX(col)` |
| Average, with a numeric or decimal output column | `TRUNC(AVG(col), scale)`, truncated to the scale of the output column as SSIS does |
| Average, with a float output column | `AVG(CAST(col AS FLOAT))`, a double average even over an integer input |

Expand

Show lessSee more

The following example has a decimal output column `AvgValue` with scale 2 and a float output column `AvgQty`:

Copy code

```
cte_aggregate AS
(
   SELECT
      Name,
      TRUNC(AVG(Value), 2) AS AvgValue,
      AVG(CAST(Qty AS FLOAT)) AS AvgQty,
      MIN(Value) AS MinValue,
      MAX(Qty) AS MaxQty
   FROM
      cte_ole_db_source
   GROUP BY
      Name
)
```

#### Limitations

An Aggregate with more than one output isn’t converted and becomes a placeholder marked with SSC-EWI-SSIS0001. An Average whose output column isn’t numeric, decimal, or float, such as a currency column, has no proven mapping, so the whole Aggregate becomes a placeholder too.

Snowflake groups text by exact value. When the Aggregate sets a comparison flag such as **Ignore case**, the grouping stays exact and the CTE is flagged with SSC-EWI-0073 so that you can review whether the difference matters for your data.

### Sort

A Sort becomes a CTE with an `ORDER BY` over the sort keys, in key-precedence order and with each key’s direction. The columns that the Sort doesn’t use as a key pass through unchanged.

Copy code

```
cte_sort AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      cte_ole_db_source
   ORDER BY
      Name ASC,
      Value DESC
)
```

When the Sort removes duplicate rows, the CTE keeps one row for each distinct combination of the sort keys with `QUALIFY ROW_NUMBER() = 1`:

Copy code

```
--** SSC-FDM-SSIS0030 - THE SSIS SORT WITH ELIMINATEDUPLICATES KEEPS THE LAST ROW OF EACH DUPLICATE GROUP IN INPUT ARRIVAL ORDER. THE CONVERTED SQL KEEPS EXACTLY ONE ROW PER GROUP, BUT ARRIVAL ORDER IS NOT RECORDED IN THE PACKAGE AND IS NOT REPRESENTED IN A SNOWFLAKE TABLE, SO A GROUP WHOSE NON-KEY COLUMNS DIFFER MAY KEEP A DIFFERENT ROW. ADD THE COLUMN THAT DECIDES THE SURVIVOR TO THE ROW_NUMBER ORDER BY IF ONE MUST BE CHOSEN. **
cte_sort AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      cte_ole_db_source
   QUALIFY
      ROW_NUMBER()
      OVER (
      PARTITION BY (
         Name, Value)
      ORDER BY
         Name ASC,
         Value ASC) = 1
   ORDER BY
      Name ASC,
      Value ASC
)
```

SSIS keeps the last row of each duplicate group in arrival order, which Snowflake doesn’t record. When two rows share the key but differ in other columns, the row that survives can differ from SSIS, and SSC-FDM-SSIS0030 reminds you to add the column that decides the survivor to the `ORDER BY` of the `ROW_NUMBER` window. A Sort that sets a comparison flag such as **Ignore case** keeps the exact-value comparison and also carries SSC-EWI-0073. A Sort that removes duplicates but has no sort keys produces a plain projection with no deduplication.

### Pivot

A Pivot becomes a static pivot. The CTE computes a set key for each row, groups the rows by it, and builds one output column for each declared pivot value with `MAX(CASE WHEN ... END)`.

#### Example

Copy code

```
cte_pivot AS
(
   WITH cte_pivot_pivot_input AS
   (
      SELECT
         Id,
         Name,
         Value,
         IFF(Name IN ('Bike', 'Helmet'), Id, TO_NUMBER(CONCAT('SSIS Pivot invalid key: ', COALESCE(Name, '<NULL>')))) AS ssis_pivot_set_key,
         COUNT(*)
         OVER (
         PARTITION BY
            Id, Name) AS ssis_pivot_pair_count
      FROM
         cte_ole_db_source
   )
   SELECT
      ssis_pivot_set_key AS Id,
      MAX(CASE
         WHEN Name = 'Bike'
            THEN IFF(ssis_pivot_pair_count = 1, Value, TO_NUMBER(CONCAT('SSIS Pivot duplicate key: ', COALESCE(Name, '<NULL>'))))
      END) AS Bike,
      MAX(CASE
         WHEN Name = 'Helmet'
            THEN IFF(ssis_pivot_pair_count = 1, Value, TO_NUMBER(CONCAT('SSIS Pivot duplicate key: ', COALESCE(Name, '<NULL>'))))
      END) AS Helmet
   FROM
      cte_pivot_pivot_input
   GROUP BY
      ssis_pivot_set_key
)
```

SSIS fails the Data Flow on a pivot key it doesn’t know and on a duplicate key for the same set. A `SELECT` has no direct way to fail on a row, so the CTE forces a runtime error: the `TO_NUMBER` calls try to convert the text `SSIS Pivot invalid key: ...` or `SSIS Pivot duplicate key: ...`, which fails the statement with an error that names the offending key. When the set keys arrive interleaved in the input, the CTE adds window functions that rebuild the contiguous segments SSIS reads, and a pass-through column takes its value from the first row of each set with `FIRST_VALUE`.

#### Limitations

A Pivot is converted only when the conversion can reproduce the order in which SSIS reads its input. The Pivot must have exactly one incoming path, and the output that feeds it must be marked as sorted, with sort key positions on its columns. The pivot values must be of a supported type, the declared pivot keys can’t repeat, and the Pivot can have only one set key. Otherwise, the Pivot becomes a placeholder marked with SSC-EWI-SSIS0001. In the following example, a Pivot without a declared input order is replaced by a placeholder while the rest of the Data Flow converts:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
cte_pivot AS
(
   SELECT
      null AS CustomerName,
      null AS Bike,
      null AS Helmet,
      null AS Gloves
)
```

When **Pass through unmatched pivot keys** is enabled, SSIS sends rows with unknown pivot keys to a separate output. The CTE doesn’t do that, so those rows produce `NULL` values instead, and the CTE is flagged with [SSC-FDM-SSIS0021](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0021).

### UnPivot

An UnPivot becomes a CTE that turns each configured source column into a row. With one destination column, the CTE uses a Snowflake `UNPIVOT`, aliasing each source column to the pivot key value that the component declares. With several destination columns, it emits one `SELECT` for each key group and combines them with `UNION ALL`, so the values in each group stay aligned.

A row whose pivoted columns are all `NULL` is emitted once, with `NULL` values for the pivot key and the value, by an extra `UNION ALL` branch.

#### Example

Single destination column:

Copy code

```
cte_unpivot AS
(
   SELECT
      Id,
      Metric,
      Amount :: NUMERIC(18, 2) AS Amount
   FROM
      cte_ole_db_source UNPIVOT (Amount FOR Metric IN (JanAmount AS "January total", FebAmount AS "February total"))
   UNION ALL
   SELECT
      Id,
      null AS Metric,
      null AS Amount
   FROM
      cte_ole_db_source
   WHERE
      JanAmount IS NULL
      AND FebAmount IS NULL
)
```

## Destinations

### OLE DB Destination and Oracle Destination

An OLE DB Destination or Oracle Destination in table or view access mode becomes an `INSERT INTO <table> (<columns>)` statement. The upstream CTEs are carried inside its source query, and the final `SELECT` reads the CTE of the component before the destination:

Copy code

```
INSERT INTO dbo.TgtAggSum (Category, TotalValue, RowCnt)
WITH cte_ole_db_source AS
(
   SELECT
      Id,
      Name,
      Value
   FROM
      dbo.SrcAggSum
),
cte_aggregate AS
(
   SELECT
      Name AS Category,
      SUM(Value) AS TotalValue,
      COUNT(*) AS RowCnt
   FROM
      cte_ole_db_source
   GROUP BY
      Name
)
SELECT
   Category,
   TotalValue,
   RowCnt
FROM
   cte_aggregate;
```

A destination that takes its table name from a variable or runs a SQL command becomes a placeholder.

### Excel Destination

An Excel Destination is written as an `INSERT` into a table named after the Excel sheet, with the same shape as the OLE DB Destination. No Excel file is created, so create a table with the sheet name, or change the target of the `INSERT`, before you run the procedure:

Copy code

```
INSERT INTO Sheet1 (ProductName, Quantity, UnitPrice)
WITH cte_ole_db_source AS
(
   SELECT
      ProductName,
      Quantity,
      UnitPrice
   FROM
      dbo.ProductData
)
SELECT
   ProductName,
   Quantity,
   UnitPrice
FROM
   cte_ole_db_source;
```

## Multiple destinations

When a Data Flow writes more than once, the shared step is read by more than one statement, and a CTE can’t be shared across statements. The conversion persists the step as a temporary table named `tmp_cte_<component>`, then emits one `INSERT` for each destination. A Multicast that feeds two OLE DB Destinations is the most common case:

Snowflake (`Two_Destinations_Data_Flow.sql`):

Copy code

```
CREATE OR REPLACE PROCEDURE public.Two_Destinations_Data_Flow (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      CREATE OR REPLACE TEMPORARY TABLE tmp_cte_multicast AS
         WITH cte_ole_db_source AS
         (
            SELECT
               Id,
               Name,
               Value
            FROM
               dbo.SourceTable
         )
         SELECT
            Id,
            Name,
            Value
         FROM
            cte_ole_db_source;
      INSERT INTO dbo.TargetTable (Id, Name, Value)
      SELECT
         Id,
         Name,
         Value
      FROM
         tmp_cte_multicast;
      INSERT INTO dbo.TargetTable2 (Id, Name, Value)
      SELECT
         Id,
         Name,
         Value
      FROM
         tmp_cte_multicast;
   END
$$;
```

A Multicast that fans out to a single destination doesn’t need a temporary table. The temporary table lives only for the session that runs the procedure.

## A complete example

The following Data Flow Task reads customers, keeps the active ones with a Conditional Split, derives a full name and a normalized email address, counts the rows, passes them through a Multicast, and loads them into a table. The Conditional Split condition is `IsActive == TRUE`, and the Derived Column expressions are `FirstName + " " + LastName` and `LOWER(Email)`.

Snowflake (`CompleteDataFlow.sql`):

Copy code

```
CREATE OR REPLACE TASK public.completedataflow
CONFIG = $${
  "package": {
    "User_RowCountVar": {"value": 0, "type": "NUMBER", "is_parameter": false}
  }
}$$
AS
BEGIN
   LET config VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('package');
   LET scope VARCHAR := 'CompleteDataFlow';
   CALL public.ClearVariables(:scope);
   CALL public.InitVariablesFromConfig(:scope, :config);
END;
CREATE OR REPLACE TASK public.completedataflow_complete_data_flow
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.completedataflow
AS
BEGIN
   LET scope VARCHAR := 'CompleteDataFlow';
   CALL public.Complete_Data_Flow(:scope);
END;
```

Snowflake (`Complete_Data_Flow.sql`):

Copy code

```
CREATE OR REPLACE PROCEDURE public.Complete_Data_Flow (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      INSERT INTO dbo.ProcessedCustomers (CustomerId, FullName, NormalizedEmail, IsActive)
      WITH cte_ole_db_source AS
      (
         SELECT
            CustomerId,
            FirstName,
            LastName,
            Email,
            IsActive
         FROM
            dbo.Customers
      ),
      cte_conditional_split AS
      (
         SELECT
            CustomerId,
            FirstName,
            LastName,
            Email,
            IsActive
         FROM
            cte_ole_db_source
         WHERE
            IsActive = TRUE
      ),
      cte_derived_column AS
      (
         SELECT
            FirstName || ' ' || LastName AS FullName,
            LOWER(Email) AS NormalizedEmail,
            CustomerId,
            FirstName,
            LastName,
            Email,
            IsActive
         FROM
            cte_conditional_split
      ),
      cte_row_count AS
      (
         SELECT
            FullName,
            NormalizedEmail,
            CustomerId,
            FirstName,
            LastName,
            Email,
            IsActive
         FROM
            cte_derived_column
      ),
      cte_multicast AS
      (
         SELECT
            FullName,
            NormalizedEmail,
            CustomerId,
            FirstName,
            LastName,
            Email,
            IsActive
         FROM
            cte_row_count
      )
      SELECT
         CustomerId,
         FullName,
         NormalizedEmail,
         IsActive
      FROM
         cte_multicast;
   END
$$;
```

The package declares the `User::RowCountVar` variable, which the root Task initializes. The Row Count in this procedure passes the rows through but doesn’t populate that variable. See [Row Count](#row-count).

## Unsupported components

When a Data Flow uses a component that the Snowflake Scripting format doesn’t convert, the conversion keeps the Data Flow connected by emitting a placeholder CTE. The placeholder selects `NULL` for each output column and is marked with [SSC-EWI-SSIS0001](../../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001). Fuzzy Lookup is one such component:

Copy code

```
WITH cte_ole_db_source AS
(
   SELECT
      InputID,
      CompanyName,
      City
   FROM
      dbo.InputData
),
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
cte_fuzzy_lookup AS
(
   SELECT
      null AS CompanyName,
      null AS RefCompanyName,
      null AS Industry,
      null AS _Similarity,
      null AS _Confidence,
      null AS _Similarity_CompanyName
)
SELECT
   1;
```

Downstream components still read the placeholder by name, so the rest of the procedure is generated normally. When a destination reads a placeholder, the destination loads `NULL` values. For some components, such as Copy Column, the placeholder also includes the original component definition as comments, which makes the component easier to convert by hand.

This example Data Flow has no destination, so the conversion closes the chain of CTEs with a trivial `SELECT 1` to keep the statement valid. A Data Flow with a destination ends in the destination’s `INSERT` instead. A destination that becomes a placeholder, such as a Flat File Destination, also ends the Data Flow in `SELECT 1`, so nothing is written.

The following components become a placeholder:

- Flat File Source, unless the Data Flow is an eligible [Direct COPY](#direct-copy).
- Flat File Destination, unless it receives rows directly from a Conditional Split, as described in [Conditional Split](#conditional-split).
- Character Map, Fuzzy Lookup, and Script Component.
- Any component that isn’t listed in [Supported components](README#supported-components), such as Copy Column.
- A supported component that is outside the shape the conversion handles, such as a Lookup that caches its reference rows, an Aggregate with more than one output, or an OLE DB Command that runs `INSERT`, `UPDATE`, or `DELETE`. The Limitations of each component describe its shape.

Convert the flagged component manually, or generate the package in the [dbt output format](../README), which supports more components today. Each placeholder is also listed in the conversion issues report, with the component that produced it.
