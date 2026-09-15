# SSIS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This section describes the **dbt output format** for SSIS: how Data Flow Tasks are converted into [dbt projects](/user-guide/data-engineering/dbt-projects-on-snowflake) and Control Flow tasks and containers into Snowflake orchestration. For a before/after example of each Data Flow component, see [Mappings and transformations](mappings-and-transformations).

The default conversion path is a dbt project. Eligible Data Flow graphs that connect a Flat File Source to an OLE DB Destination emit Direct COPY and do not create a dbt project. The `--SimplifySsisDataFlows` flag is not part of this dbt documentation series.

## How a Data Flow becomes a dbt project

Each Data Flow Task is converted into a standalone dbt project with a three-tier model architecture.

| Layer | Materialization | Purpose |
| --- | --- | --- |
| `models/staging/` | View | Clean, type-safe access to source data referenced in `sources.yml`. Generated from OLE DB Source, Flat File Source, ADO.NET Source, Excel Source, and Oracle Source. |
| `models/intermediate/` | Ephemeral by default | Transformation logic from the original Data Flow. Generated from Derived Column, Lookup, Aggregate, Conditional Split, and other transformations. Some components override that default: a Sort is materialized so its `ORDER BY` is preserved, and an OLE DB Command path can change the materialization of the models it feeds. |
| `models/marts/` | Table, incremental, or view | Business-ready data models that correspond to destinations. An OLE DB Destination, Excel Destination, Oracle Destination, or Flat File Destination becomes a mart named after the target. An OLE DB Command can produce an incremental model instead. |

Expand

Show lessSee more

Each Data Flow produces this project structure:

```
{DataFlowName}/
├── dbt_project.yml                   # Materialization config and hooks
├── profiles.yml                      # Snowflake connection profile
├── models/
│   ├── sources.yml                   # Source table definitions
│   ├── staging/
│   │   └── stg_raw__*.sql
│   ├── intermediate/
│   │   └── int_*.sql
│   └── marts/
│       └── {destination}.sql
└── macros/
    └── *.sql                         # Unload helpers such as copy_into_stage
```

Important

Before deploying, replace the `YOUR_SCHEMA` and `YOUR_DB` placeholders in `sources.yml` and `profiles.yml` with your actual Snowflake schema and database names.

Most Data Flows follow the default path: the Data Flow becomes a dbt project, and the Control Flow Task that runs it calls `EXECUTE DBT PROJECT`. One case skips the dbt project. When a Data Flow only moves a Flat File Source into an OLE DB Destination, the conversion emits a Direct COPY instead: the Task runs a `COPY INTO` statement against the staged file, and no dbt project is generated for that Data Flow. Eligibility depends on the shape of the Data Flow, so check the generated output to see which path each Data Flow took. For the generated statements, see [Mappings and transformations](mappings-and-transformations).

## Data flow components

These SSIS Data Flow sources, transformations, and destinations are supported. Unlisted Data Flow components generate EWI [SSC-EWI-SSIS0001](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001). Raw File Source, Raw File Destination, and XML Source are not yet available. For a before/after example of each, see [Mappings and transformations](mappings-and-transformations).

| Component | Category | dbt mapping | Naming | Status |
| --- | --- | --- | --- | --- |
| [Microsoft.OLEDBSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/ole-db-source?view=sql-server-ver17) | Source | Staging model | stg\_raw\_\_{component\_name} | Available |
| [Microsoft.FlatFileSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/flat-file-source?view=sql-server-ver17) | Source | Staging model | stg\_raw\_\_{component\_name} | Available |
| [Microsoft.DataReaderSourceAdapter / Microsoft.ADONETSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/ado-net-source?view=sql-server-ver17) | Source | Staging (`source()` or embedded SQL) | stg\_raw\_\_{component\_name} | Available |
| [Microsoft.ExcelSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/excel-source?view=sql-server-ver17) | Source | Staging (READ\_EXCEL UDF) | stg\_raw\_\_{component\_name} | Available with limitations |
| [Microsoft.SSISOracleSrc](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/oracle-source?view=sql-server-ver17) | Source | Staging | stg\_raw\_\_{component\_name} | Available with limitations |
| [Microsoft.DerivedColumn](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/derived-column-transformation?view=sql-server-ver17) | Transformation | Intermediate (SELECT with expressions) | int\_{component\_name} | Available |
| [Microsoft.DataConvert](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/data-conversion-transformation?view=sql-server-ver17) | Transformation | Intermediate (CAST) | int\_{component\_name} | Available |
| [Microsoft.CharacterMap](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/character-map-transformation?view=sql-server-ver17) | Transformation | Intermediate (UPPER/LOWER) | int\_{component\_name} | Available |
| [Microsoft.Lookup](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/lookup-transformation?view=sql-server-ver17) | Transformation | Intermediate (LEFT JOIN) | int\_{component\_name} | Available. See [SSC-FDM-SSIS0001](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0001) |
| [Microsoft.UnionAll](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/union-all-transformation?view=sql-server-ver17) | Transformation | Intermediate (UNION ALL) | int\_{component\_name} | Available |
| [Microsoft.Merge](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/merge-transformation?view=sql-server-ver17) | Transformation | Intermediate (UNION ALL) | int\_{component\_name} | Available. See [SSC-FDM-SSIS0002](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0002) |
| [Microsoft.MergeJoin](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/merge-join-transformation?view=sql-server-ver17) | Transformation | Intermediate (JOIN) | int\_{component\_name} | Available. See [SSC-FDM-SSIS0004](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0004) |
| [Microsoft.ConditionalSplit](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/conditional-split-transformation?view=sql-server-ver17) | Transformation | Intermediate (router pattern with CTEs) | int\_{component\_name} | Available |
| [Microsoft.Multicast](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/multicast-transformation?view=sql-server-ver17) | Transformation | Intermediate (SELECT pass-through) | int\_{component\_name} | Available |
| [Microsoft.RowCount](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/row-count-transformation?view=sql-server-ver17) | Transformation | Intermediate with macro | int\_{component\_name} | Available |
| [Microsoft.Sort](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/sort-transformation?view=sql-server-ver17) | Transformation | Intermediate (QUALIFY / ORDER BY) | int\_{component\_name} | Available |
| [Microsoft.Aggregate](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/aggregate-transformation?view=sql-server-ver17) | Transformation | Intermediate (GROUP BY) | int\_{component\_name} | Available |
| [Microsoft.Pivot](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/pivot-transformation?view=sql-server-ver17) | Transformation | Intermediate (conditional aggregation) | int\_{component\_name} | Available |
| [Microsoft.UnPivot](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/unpivot-transformation?view=sql-server-ver17) | Transformation | Intermediate (UNPIVOT) | int\_{component\_name} | Available |
| [Microsoft.Cache](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/cache-transform?view=sql-server-ver17) | Transformation | Passthrough SELECT | int\_{component\_name} | Available with limitations |
| [Microsoft.FuzzyLookup](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/fuzzy-lookup-transformation?view=sql-server-ver17) | Transformation | Intermediate (CROSS JOIN + Jaro-Winkler) | int\_{component\_name} | Available |
| [Microsoft.OLEDBCommand](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/ole-db-command-transformation?view=sql-server-ver17) | Transformation | Incremental mart + delete/update macro | {target} | Available |
| Script Component | Transformation | EWI [SSC-EWI-SSIS0001](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001) | — | Not yet available |
| [Microsoft.OLEDBDestination](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/ole-db-destination?view=sql-server-ver17) | Destination | Mart | {target} | Available |
| [Microsoft.FlatFileDestination](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/flat-file-destination?view=sql-server-ver17) | Destination | Mart | {target} | Available |
| [Microsoft.ExcelDestination](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/excel-destination?view=sql-server-ver17) | Destination | Mart | {target} | Available |
| [Microsoft.SSISOracleDst](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/oracle-destination?view=sql-server-ver17) | Destination | Mart | {target} | Available |

Expand

Show lessSee more

## Control flow components

These SSIS Control Flow tasks and containers are supported:

| Element | Category | Conversion target | Status | Notes |
| --- | --- | --- | --- | --- |
| [Microsoft.Pipeline (Data Flow Task)](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/data-flow?view=sql-server-ver17) | Task | dbt project or Direct COPY | Available | Eligible Flat File Source to OLE DB Destination graphs emit COPY and no dbt project |
| [Microsoft.ExecuteSQLTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-sql-task?view=sql-server-ver17) | Task | Inline SQL or stored procedure | Available | See [Execute SQL Task](#execute-sql-task) |
| [Microsoft.ExecutePackageTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-package-task?view=sql-server-ver17) | Task | Inline EXECUTE TASK or CALL | Available | See [Execute Package Task](#execute-package-task) |
| [Microsoft.SendMailTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/send-mail-task?view=sql-server-ver17) | Task | SYSTEM$SEND\_EMAIL | Available with limitations | See [Send Mail Task](#send-mail-task) |
| [Microsoft.BulkInsertTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/bulk-insert-task?view=sql-server-ver17) | Task | COPY INTO + FILE\_FORMAT | Available with limitations | See [Bulk Insert Task](#bulk-insert-task); native format stays EWI |
| [Microsoft.FileSystemTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/file-system-task?view=sql-server-ver17) | Task | Stage COPY FILES / REMOVE | Available with limitations | Stage operations, not dbt models |
| [Microsoft.ExpressionTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/expression-task?view=sql-server-ver17) | Task | Assignment (:=) or SELECT | Available | Converts SSIS expressions to Snowflake Scripting assignments |
| [STOCK:SEQUENCE (Sequence Container)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/sequence-container?view=sql-server-ver17) | Container | Inline sequential | Available | See [Sequence Containers](#sequence-containers) |
| [STOCK:FORLOOP (For Loop Container)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/for-loop-container?view=sql-server-ver17) | Container | WHILE when Init/Eval/Assign present; else once + EWI | Available with limitations | See [For Loop Containers](#for-loop-containers) |
| [STOCK:FOREACHLOOP (File)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) | Container | LIST / CURSOR | Available with limitations | Stage mapping [SSC-EWI-SSIS0014](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0014) |
| [STOCK:FOREACHLOOP (ADO)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) | Container | Cursor + variable assignments | Available with limitations | Source query placeholder emits [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004) |
| [STOCK:FOREACHLOOP (From Variable)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) | Container | FLATTEN + RESULT\_SCAN | Available | Iterates values from a variable collection |
| [STOCK:FOREACHLOOP (other)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) | Container | EWI stub | Not yet available | Item, NodeList, SMO, HDFS, SchemaRowset |
| [Event Handlers](https://learn.microsoft.com/en-us/sql/integration-services/integration-services-ssis-event-handlers?view=sql-server-ver17) | Container | Stored procedures; supported scoped OnPre/Post handlers are CALL-wired | Available with limitations | Package-level and OnError/Warning handlers can remain untriggered; Partial + [SSC-FDM-SSIS0006](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0006) |
| [Microsoft.ScriptTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/script-task?view=sql-server-ver17) | Task | EWI [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004) | Not yet available | Script logic requires manual migration |

Expand

Show lessSee more

**Note**: Unlisted Control Flow elements generate EWI [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004).

### Container Conversion Details

Sequence, For Loop, and ForEach containers are converted inline within the parent task or procedure. Event Handlers are converted to stored procedures; supported scoped handlers can be wired into the parent orchestration with `CALL`.

#### Sequence Containers

[Sequence containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/sequence-container?view=sql-server-ver17) are converted inline within the parent TASK. The container’s boundaries are marked with comments in the generated code, and all tasks within the container execute sequentially in the same TASK scope.

**Conversion characteristics:**

- No separate procedure or TASK is created for the container
- Container boundaries are clearly marked BEGIN … END blocks
- All tasks execute sequentially within the parent TASK
- Task execution order based on precedence constraints is maintained
- **Limitation**: Only “Success” precedence constraints are fully supported. Conditional execution based on task outcomes (Failure or Completion constraints) is not currently implemented and will require manual post-migration adjustments

**Behavioral differences:**

- FDM generated: [SSC-FDM-SSIS0003](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0003)
- Variable scoping differs from SSIS: Container variables are accessible throughout the entire parent TASK, not just within the container scope

**Example:**

Copy code

```
:force:

-- BEGIN Sequence Container: MySequence
-- Task 1 within sequence
EXECUTE DBT PROJECT public.DataFlow1 ARGS='build --target dev';
-- Task 2 within sequence
EXECUTE DBT PROJECT public.DataFlow2 ARGS='build --target dev';
-- END Sequence Container: MySequence
```

#### For Loop Containers

[For Loop containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/for-loop-container?view=sql-server-ver17) convert to Snowflake Scripting `WHILE` loops when InitExpression, EvalExpression, and AssignExpression are present.

##### Conversion behavior

| Source | Snowflake | Notes |
| --- | --- | --- |
| InitExpression | Assignment before the loop | Sets the loop counter |
| EvalExpression | `WHILE` condition | Loop continues while the condition is true |
| AssignExpression | Assignment at the end of the loop body | Increments or updates the counter |
| Missing Init/Eval/Assign | Body once + EWI | [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004) |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

User_Counter := :User_MinValue;
WHILE (:User_Counter <= :User_MaxValue) LOOP
   -- Loop body tasks
   User_Counter := :User_Counter + 1;
END LOOP;
```

##### Limitations

- When Init, Eval, or Assign expressions are not present, the converted body runs once and [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004) is generated.

#### ForEach Loop Containers

**File Enumerator (Supported)**

[ForEach File Enumerator containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) are converted to Snowflake stage operations using the LIST command and cursor pattern:

Copy code

```
:force:

-- List files from Snowflake stage
LIST @<STAGE_PLACEHOLDER>/FolderPath PATTERN = '.*/file_pattern\.csv';

-- Create cursor for iteration
LET file_cursor CURSOR FOR
   SELECT REGEXP_SUBSTR($1, '[^/]+$') AS FILE_VALUE
   FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   WHERE $1 NOT LIKE '%FolderPath/%/%';

-- Iterate through files
FOR file_row IN file_cursor DO
   User_CurrentFileName := :file_row.FILE_VALUE;
   EXECUTE DBT PROJECT public.My_DataFlow_Project ARGS='build --target dev';
END FOR;
```

**Configuration requirements:**

After migration, you’ll need to:

- Replace `<STAGE_PLACEHOLDER>` with your actual Snowflake stage name
- Ensure the folder path is correctly mapped to a Snowflake stage
- Verify that files are properly staged in Snowflake

An [EWI (SSC-EWI-SSIS0014)](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0014) is generated to remind you of this manual configuration step.

**ADO enumerator**

ForEach ADO enumerators emit a cursor plus per-row variable assignments. The cursor source is a placeholder `SELECT null` until you replace it with the upstream result-set query. That placeholder emits [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004). This is not a LIST pattern.

##### Conversion behavior

| Source | Snowflake | Notes |
| --- | --- | --- |
| ADO enumerator | Cursor over a query | Replace `SELECT null` with the query that populated the recordset |
| Column mappings | Variable assignments inside `FOR` | Each mapped column is assigned and persisted with `UpdateControlVariable` |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

LET ado_cursor CURSOR
FOR
   SELECT
      null;
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT 'FOREACH ADO ENUMERATOR - cursor source variable: User_ResultSetObject. Replace SELECT null with the query from the upstream Execute SQL Task that populates this variable.' CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
FOR ado_row IN ado_cursor DO
   User_ColumnA := :ado_row.User_ColumnA;
   CALL public.UpdateControlVariable('User_ColumnA', 'orders_package', TO_VARIANT(:User_ColumnA));
   User_ColumnB := :ado_row.User_ColumnB;
   CALL public.UpdateControlVariable('User_ColumnB', 'orders_package', TO_VARIANT(:User_ColumnB));
   -- Loop body tasks
END FOR;
```

##### Limitations

- [SSC-EWI-SSIS0004](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004). Replace `SELECT null` with the upstream result-set query before running the task.

**From Variable enumerator**

ForEach From Variable enumerators flatten a collection variable and iterate with `RESULT_SCAN`, not LIST.

##### Conversion behavior

| Source | Snowflake | Notes |
| --- | --- | --- |
| Collection variable | `TABLE(FLATTEN(...))` | One row per collection element |
| Cursor | `RESULT_SCAN(LAST_QUERY_ID())` | Feeds the `FOR` loop |
| Mapped variable | Assignment from `VALUE` | Updated with `UpdateControlVariable` |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

SELECT
   VALUE
FROM
   TABLE(FLATTEN(:User_MonthCollection));
LET from_var_cursor CURSOR
FOR
   SELECT
      VALUE
   FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));
FOR from_var_row IN from_var_cursor DO
   User_MonthValue := :from_var_row.VALUE;
   CALL public.UpdateControlVariable('User_MonthValue', 'orders_package', TO_VARIANT(:User_MonthValue));
   -- Loop body tasks
END FOR;
```

**Other enumerator types**

ForEach Item, NodeList, SMO, HDFS, and SchemaRowset enumerators are not yet available. An [EWI (SSC-EWI-SSIS0004)](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0004) is generated for these cases.

#### Event Handlers

[Event handlers](https://learn.microsoft.com/en-us/sql/integration-services/integration-services-ssis-event-handlers?view=sql-server-ver17) are converted to stored procedures. Supported scoped OnPreExecute and OnPostExecute handlers can be CALL-wired from the converted orchestration. Package-level handlers and OnError or OnWarning procedures can remain untriggered.

##### Conversion behavior

| Source | Snowflake | Notes |
| --- | --- | --- |
| Scoped OnPreExecute / OnPostExecute | Stored procedure + `CALL` | Wired around the converted task or container |
| OnError / OnWarning | Stored procedure | Can remain untriggered |
| Package-level handlers | Stored procedure | Can remain untriggered |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

--** SSC-FDM-SSIS0006 - EVENT HANDLER STORED PROCEDURE CREATED BUT NOT AUTOMATICALLY TRIGGERED. MANUAL INVOCATION OR TRIGGERING MECHANISM IMPLEMENTATION REQUIRED. **
CREATE OR REPLACE PROCEDURE public.orders_package_execute_sql_task_onerror_handler ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      INSERT INTO TaskErrorLog (TaskName, ErrorTime) VALUES ('Execute SQL Task', CURRENT_TIMESTAMP());
      RETURN 'SUCCESS';
   END;
$$;

CREATE OR REPLACE PROCEDURE public.orders_package_execute_sql_task_onpreexecute_handler ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      INSERT INTO TaskLog (TaskName, StartTime) VALUES ('Execute SQL Task', CURRENT_TIMESTAMP());
      RETURN 'SUCCESS';
   END;
$$;

CREATE OR REPLACE PROCEDURE public.orders_package_execute_sql_task_onpostexecute_handler ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      INSERT INTO TaskLog (TaskName, EndTime) VALUES ('Execute SQL Task', CURRENT_TIMESTAMP());
      RETURN 'SUCCESS';
   END;
$$;

CREATE OR REPLACE TASK public.orders_package_sequence_container
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.orders_package
AS
BEGIN
   CALL public.orders_package_execute_sql_task_onpreexecute_handler();
   UPDATE Employees
      SET Status = 'Active'
      WHERE Department = 'Sales';
   CALL public.orders_package_execute_sql_task_onpostexecute_handler();
END;
```

##### Limitations

- OnError, OnWarning, and package-level handler procedures can remain untriggered and require manual invocation or a triggering mechanism. See [SSC-FDM-SSIS0006](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0006).

### Execute SQL Task

[Execute SQL Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-sql-task?view=sql-server-ver17) are converted as inline SQL statements or separate stored procedures, depending on complexity and result set bindings.

**Conversion approach:**

- **Simple SQL statements**: Converted inline within the parent TASK
- **Complex statements with result sets**: May be converted to separate stored procedures
- **Result bindings**: Handled where possible; unsupported patterns generate [EWI SSC-EWI-SSIS0011](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0011)

### Execute Package Task

[Execute Package Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-package-task?view=sql-server-ver17) are handled differently based on package type:

| Package Type | Conversion | Notes |
| --- | --- | --- |
| **Local** (single reference) | Inline execution within parent TASK | Package logic expanded inline |
| **Reusable** (2+ references or parameters) | CALL to stored procedure | Enables synchronous execution with parameters; generates [FDM SSC-FDM-SSIS0005](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0005) |
| **External** | CALL with path resolution | Generates [EWI SSC-EWI-SSIS0008](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0008) for manual verification |

Expand

Show lessSee more

**Asynchronous execution note:**

TASK-based Execute Package conversions run asynchronously. For synchronous behavior, packages are converted to stored procedures. See [EWI SSC-EWI-SSIS0005](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0005).

### File System Task

[File System Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/file-system-task?view=sql-server-ver17) convert to Snowflake stage operations (`COPY FILES` and `REMOVE`). They do not become dbt models.

##### Conversion behavior

| Source operation | Snowflake | Notes |
| --- | --- | --- |
| Copy | `COPY FILES INTO ... FROM ...` | Destination is treated as a directory prefix |
| Move | `COPY FILES` then `REMOVE` | Removes the source after copy |
| Delete directory content | `REMOVE` then a `.keep` `COPY INTO` | Prefix-based stage paths |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

-- Copy
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0044 - THE COPY FILES COMMAND TREATS THE DESTINATION AS A DIRECTORY PREFIX AND APPENDS THE SOURCE FILENAME. IF THE DESTINATION PATH REFERS TO A SPECIFIC FILE RATHER THAN A DIRECTORY, THE RESULTING PATH MAY BE INCORRECT. REVIEW AND ADJUST MANUALLY IF NEEDED. ***/!!!
--** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
COPY FILES INTO :User_DestFilePath
FROM :User_SourceFilePath;

-- Move
COPY FILES INTO :User_DestFilePath
FROM :User_SourceFilePath;
REMOVE :User_SourceFilePath;

-- Delete directory content
--** SSC-FDM-SSIS0028 - SNOWFLAKE STAGES USE PREFIX-BASED PATHS, NOT REAL DIRECTORIES. THE REMOVE COMMAND WITH A TRAILING SLASH DELETES ALL FILES MATCHING THE PREFIX PATTERN. **
REMOVE :User_TempFolder;
EXECUTE IMMEDIATE 'COPY INTO ' || :User_TempFolder || '/.keep FROM (SELECT ''empty'') FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE) OVERWRITE = TRUE SINGLE = TRUE';
```

##### Limitations

- Destination paths are directory prefixes ([SSC-EWI-SSIS0044](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0044)).
- Snowflake stages use prefix-based paths rather than real directories, so `REMOVE` with a trailing slash deletes every file matching the prefix (`SSC-FDM-SSIS0028`).
- Variable values must contain a valid Snowflake stage path ([SSC-FDM-SSIS0025](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0025)).

### Expression Task

[Expression Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/expression-task?view=sql-server-ver17) convert SSIS expressions to Snowflake Scripting assignments (`:=`). They do not become dbt models.

##### Conversion behavior

| Source | Snowflake | Notes |
| --- | --- | --- |
| Expression Task | `variable := <converted expression>` | Functions such as `UPPER` are rewritten to Snowflake |

Expand

Show lessSee more

##### Example

Copy code

```
:force:

User_message := UPPER(:User_message || 'message');
```

### Send Mail Task

[Send Mail Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/send-mail-task?view=sql-server-ver17) are converted to Snowflake Tasks that use `SYSTEM$SEND_EMAIL` with a dynamically created Notification Integration.

#### Conversion behavior

| Aspect | SSIS | Snowflake |
| --- | --- | --- |
| Email Service | Custom SMTP server | Snowflake’s built-in email service |
| Configuration | SMTP Connection Manager | Notification Integration |
| Sender Address | Custom FROM address | Fixed by Snowflake account |
| CC/BCC Support | Full support | Not supported (merged into recipients) |
| Attachments | File attachments supported | Not supported |
| HTML Body | Supported | Plain text only |
| Priority | High/Normal/Low | Not supported |

Expand

Show lessSee more

#### Property mapping

| SSIS Property | Snowflake Equivalent | Notes |
| --- | --- | --- |
| ToLine | `ALLOWED_RECIPIENTS` + recipients parameter | Direct mapping |
| FromLine | Prepended to message body | [FDM SSC-FDM-SSIS0008](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0008) |
| CCLine | Added to recipients list | [FDM SSC-FDM-SSIS0009](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0009) |
| BCCLine | Added to recipients list | [FDM SSC-FDM-SSIS0010](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0010) (privacy concern) |
| Subject | `subject` parameter | Direct mapping |
| MessageSource | `message` parameter | Direct mapping |
| MessageSourceType (DirectInput) | Supported | - |
| MessageSourceType (Variable) | Supported | Variable reference converted |
| MessageSourceType (FileConnection) | Not supported | [EWI SSC-EWI-SSIS0017](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0017) |
| Priority | Not supported | [EWI SSC-EWI-SSIS0016](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0016) |
| FileAttachments | Not supported | [EWI SSC-EWI-SSIS0015](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0015) |
| SMTPConnection | Managed by Snowflake | [FDM SSC-FDM-SSIS0007](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0007) |
| BodyFormat (HTML) | Not supported | [EWI SSC-EWI-SSIS0018](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0018) |

Expand

Show lessSee more

#### Example

Each Send Mail Task is converted to a Snowflake Task containing:

1. **Notification Integration Creation**: Created dynamically via `EXECUTE IMMEDIATE`
2. **SYSTEM$SEND\_EMAIL Call**: Sends the email through the integration

Copy code

```
:force:

CREATE OR REPLACE TASK public.my_package_send_mail_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.my_package
AS
BEGIN
   -- Step 1: Create Notification Integration dynamically
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com", "team@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;

   -- Step 2: Send the email
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com,team@example.com', 'Subject', 'Message body');
END;
```

**Basic Email (To, Subject, Body):**

Copy code

```
:force:

BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Daily Report', 'The daily report is ready.');
END;
```

**Email with FROM Address:**

Copy code

```
:force:

BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("noreply@company.com", "admin@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   --** SSC-FDM-SSIS0008 - SNOWFLAKE'S EMAIL INTEGRATION USES A FIXED SENDER ADDRESS. THE ORIGINAL FROM ADDRESS HAS BEEN PREPENDED TO THE MESSAGE BODY FOR REFERENCE. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'noreply@company.com,admin@example.com', 'Notification', 'Email sent by: noreply@company.com

Package completed successfully.');
END;
```

**Email with Multiple Features (attachments, priority, CC):**

Copy code

```
:force:

BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("noreply@company.com", "admin@example.com", "team@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0015 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT FILE ATTACHMENTS. CONSIDER USING STAGED FILES WITH SHARED LINKS OR ALTERNATIVE DELIVERY METHODS. ***/!!!
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0016 - EMAIL PRIORITY SETTINGS (HIGH/NORMAL/LOW) ARE NOT SUPPORTED BY SYSTEM$SEND_EMAIL AND WILL BE IGNORED. ***/!!!
   --** SSC-FDM-SSIS0008 - SNOWFLAKE'S EMAIL INTEGRATION USES A FIXED SENDER ADDRESS. THE ORIGINAL FROM ADDRESS HAS BEEN PREPENDED TO THE MESSAGE BODY FOR REFERENCE. **
   --** SSC-FDM-SSIS0009 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT CC ADDRESSING. ALL CC RECIPIENTS HAVE BEEN ADDED TO THE MAIN RECIPIENTS LIST. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'noreply@company.com,admin@example.com,team@example.com', 'Monthly Report', 'Email sent by: noreply@company.com

Please review the attached monthly report.');
END;
```

#### Prerequisites for Snowflake Email

Before using converted Send Mail Tasks:

1. **Email Notification Integration permissions**: Account admin must grant `CREATE INTEGRATION ON ACCOUNT` to the executing role
2. **Recipient verification**: All email addresses in `ALLOWED_RECIPIENTS` must be verified in Snowflake
3. **Update warehouse name**: Replace `DUMMY_WAREHOUSE` with your actual warehouse name

#### Limitations

**File Attachments:**

Upload files to a Snowflake stage and share links instead:

Copy code

```
:force:

-- Upload file to stage
PUT file://report.pdf @my_stage;

-- Get shareable link (valid for 1 hour)
LET file_url STRING := GET_PRESIGNED_URL(@my_stage, 'report.pdf', 3600);

-- Include link in email body
CALL SYSTEM$SEND_EMAIL('my_integration', 'admin@example.com', 'Report Available',
  'Download the report from: ' || :file_url);
```

**BCC Privacy:**

Send separate emails to maintain recipient privacy:

Copy code

```
:force:

-- Send to main recipients
CALL SYSTEM$SEND_EMAIL('my_integration', 'admin@example.com', 'Subject', 'Message');

-- Send separately to BCC recipients
CALL SYSTEM$SEND_EMAIL('my_integration', 'audit@example.com', 'Subject', 'Message');
```

### Bulk Insert Task

[Bulk Insert Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/bulk-insert-task?view=sql-server-ver17) are converted to Snowflake Tasks that use `COPY INTO` with an inline FILE\_FORMAT. The conversion generates a stage placeholder that you must configure before execution.

#### Conversion behavior

| Aspect | SSIS | Snowflake |
| --- | --- | --- |
| Data Source | File system path or UNC path | Snowflake Stage (internal or external) |
| File Format | Format file (.fmt/.xml) or inline options | FILE\_FORMAT object or inline options |
| Native Format | Native/WideNative supported | Not supported (CSV, JSON, Parquet, etc.) |
| Row Filtering | FirstRow/LastRow options | Not directly supported |
| Batch Control | BatchSize configurable | Automatic management |
| Error Handling | MaximumErrors count | ON\_ERROR behavior |
| Triggers | FireTriggers option | Not supported (use Streams/Tasks) |
| Table Locking | TableLock option | Not needed (MVCC) |

Expand

Show lessSee more

#### Property mapping

| SSIS Property | Snowflake Equivalent | Notes |
| --- | --- | --- |
| DestinationTableName | `COPY INTO table` | Square brackets `[]` removed |
| DataFileType (Char) | `TYPE = 'CSV'` | Direct mapping |
| DataFileType (Native) | Not supported | [EWI SSC-EWI-SSIS0020](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0020) |
| FieldTerminator | `FIELD_DELIMITER` | Parsed from SSIS format |
| RowTerminator | `RECORD_DELIMITER` | Parsed from SSIS format |
| FirstRow | `SKIP_HEADER` | Value - 1 |
| LastRow | Not supported | [EWI SSC-EWI-SSIS0021](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0021) |
| MaximumErrors | `ON_ERROR` | [FDM SSC-FDM-SSIS0011](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0011) |
| KeepNulls=True | `NULL_IF = ()` | Empty tuple |
| KeepNulls=False | `NULL_IF = ('', 'NULL', 'null')` | Default behavior |
| KeepIdentity=False | FDM generated | [FDM SSC-FDM-SSIS0017](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0017) |
| TableLock=True | Not needed | [FDM SSC-FDM-SSIS0014](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0014) |
| FireTriggers=True | Not supported | [EWI SSC-EWI-SSIS0022](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0022) |
| FormatFile | Not supported | [EWI SSC-EWI-SSIS0023](../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0023) |
| CheckConstraints=True | Always enforced | [FDM SSC-FDM-SSIS0016](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0016) |
| BatchSize | Automatic | [FDM SSC-FDM-SSIS0012](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0012) |
| SortedData | Not available | [FDM SSC-FDM-SSIS0015](../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0015) |

Expand

Show lessSee more

#### Terminator Parsing

SSIS uses specific tokens for field and row terminators. These are converted to Snowflake escape sequences:

| SSIS Format | Snowflake Output |
| --- | --- |
| `{CR}{LF}` | `\r\n` |
| `{CR}` | `\r` |
| `{LF}` | `\n` |
| `{TAB}` | `\t` |
| `Tab` | `\t` |
| `Comma {,}` | `,` |
| `Semicolon {;}` | `;` |
| `Vertical Bar {|}` | `|` |

Expand

Show lessSee more

#### Example

Each Bulk Insert Task is converted to a Snowflake Task containing a COPY INTO statement with an inline FILE\_FORMAT:

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   ---- Start block 'Package\BulkInsertTask'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0024 - THE STAGE AND FILE UPLOAD ARE NOT INCLUDED IN THE TRANSLATION. CREATE A SNOWFLAKE STAGE AND UPLOAD THE SOURCE FILE BEFORE EXECUTING THE COPY INTO STATEMENT. REPLACE {STAGE_PLACEHOLDER} WITH YOUR STAGE NAME. ***/!!!
   COPY INTO target_table
   FROM '@{STAGE_PLACEHOLDER}'
   PATTERN = '.*data_file.*'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\r\n', SKIP_HEADER = 1, NULL_IF = ('', 'NULL', 'null'), ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
   ON_ERROR = CONTINUE;
   ---- End block 'Package\BulkInsertTask'
END;
```

**Basic Bulk Insert (CSV with default options):**

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_load_customers
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0024 - THE STAGE AND FILE UPLOAD ARE NOT INCLUDED IN THE TRANSLATION. CREATE A SNOWFLAKE STAGE AND UPLOAD THE SOURCE FILE BEFORE EXECUTING THE COPY INTO STATEMENT. REPLACE {STAGE_PLACEHOLDER} WITH YOUR STAGE NAME. ***/!!!
   COPY INTO Customers
   FROM '@{STAGE_PLACEHOLDER}'
   PATTERN = '.*customers\.csv.*'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\r\n', SKIP_HEADER = 0, NULL_IF = ('', 'NULL', 'null'), ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
   ON_ERROR = CONTINUE;
END;
```

**Bulk Insert with Tab Delimiter and Header Skip:**

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_load_products
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0024 - THE STAGE AND FILE UPLOAD ARE NOT INCLUDED IN THE TRANSLATION. CREATE A SNOWFLAKE STAGE AND UPLOAD THE SOURCE FILE BEFORE EXECUTING THE COPY INTO STATEMENT. REPLACE {STAGE_PLACEHOLDER} WITH YOUR STAGE NAME. ***/!!!
   COPY INTO Products
   FROM '@{STAGE_PLACEHOLDER}'
   PATTERN = '.*products\.txt.*'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = '\t', RECORD_DELIMITER = '\n', SKIP_HEADER = 1, NULL_IF = ('', 'NULL', 'null'), ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
   ON_ERROR = SKIP_FILE_10;
END;
```

**Bulk Insert with Multiple EWIs (Native format, LastRow, FireTriggers):**

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_load_orders
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0020 - SSIS BULKINSERTTASK NATIVE OR WIDENATIVE DATA FILE TYPE IS NOT SUPPORTED IN SNOWFLAKE. EXPORT SOURCE DATA TO CSV FORMAT BEFORE MIGRATION. ***/!!!
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0021 - SSIS BULKINSERTTASK LASTROW OPTION IS NOT SUPPORTED IN SNOWFLAKE. USE TEMPORARY TABLE WITH ROW_NUMBER AND LIMIT/OFFSET TO SELECT SPECIFIC ROW RANGE. ***/!!!
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0022 - SSIS BULKINSERTTASK FIRETRIGGERS OPTION IS NOT SUPPORTED IN SNOWFLAKE. CONSIDER USING SNOWFLAKE STREAMS AND TASKS TO IMPLEMENT TRIGGER-LIKE BEHAVIOR. ***/!!!
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0024 - THE STAGE AND FILE UPLOAD ARE NOT INCLUDED IN THE TRANSLATION. CREATE A SNOWFLAKE STAGE AND UPLOAD THE SOURCE FILE BEFORE EXECUTING THE COPY INTO STATEMENT. REPLACE {STAGE_PLACEHOLDER} WITH YOUR STAGE NAME. ***/!!!
   COPY INTO Orders
   FROM '@{STAGE_PLACEHOLDER}'
   PATTERN = '.*orders\.dat.*'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\r\n', SKIP_HEADER = 0, NULL_IF = ('', 'NULL', 'null'), ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
   ON_ERROR = CONTINUE;
END;
```

#### Stage Setup (Required)

Before executing converted Bulk Insert Tasks, you must:

1. **Create a Snowflake stage:**

Copy code

```
:force:

CREATE OR REPLACE STAGE my_bulk_stage;
```

2. **Upload files using SnowSQL CLI:**

Copy code

```
:force:

PUT file:///path/to/data.csv @my_bulk_stage AUTO_COMPRESS = FALSE;
```

3. **Replace the stage placeholder in generated code:**

Copy code

```
:force:

-- Change this:
FROM '@{STAGE_PLACEHOLDER}'

-- To this:
FROM '@my_bulk_stage'
```

4. **Verify files are staged:**

Copy code

```
:force:

LIST @my_bulk_stage;
```

#### Limitations

**Native Data Format:**

Export SQL Server data to CSV format before migration. The native binary format is not supported by Snowflake.

**LastRow Filtering:**

Load to staging table and filter:

Copy code

```
:force:

-- Load all data
COPY INTO staging_table FROM '@my_stage' ...;

-- Insert only rows up to LastRow value
INSERT INTO target_table
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS rn
  FROM staging_table
) WHERE rn <= 1000;  -- Original LastRow value
```

**FireTriggers (Trigger-like Behavior):**

Use Snowflake Streams and Tasks:

Copy code

```
:force:

-- Create stream to capture inserts
CREATE OR REPLACE STREAM target_stream ON TABLE target_table;

-- Create task to process inserts (trigger logic)
CREATE OR REPLACE TASK process_inserts
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 minute'
  WHEN SYSTEM$STREAM_HAS_DATA('target_stream')
AS
  INSERT INTO audit_table
  SELECT *, CURRENT_TIMESTAMP()
  FROM target_stream
  WHERE METADATA$ACTION = 'INSERT';
```

### dbt Project Execution

Within the orchestration code, Data Flow Tasks are executed using Snowflake’s [`EXECUTE DBT PROJECT`](/sql-reference/sql/execute-dbt-project) command:

Copy code

```
:force:

EXECUTE DBT PROJECT schema.project_name ARGS='build --target dev'
```

**Important requirements:**

- The `project_name` must match the name you used when deploying the dbt project (via `CREATE DBT PROJECT` or Snowflake Workspace deployment)
- Arguments passed are standard dbt CLI arguments (like `build`, `run`, `test`)
- Each execution runs the entire dbt project with all models in dependency order

**Deployment:**

Before executing dbt projects in orchestration, deploy them using:

- Snowflake CLI: `snow dbt deploy --schema schema_name --database database_name package_name`
- Snowflake Workspace: Upload and deploy via UI
