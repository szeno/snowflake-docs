# Informatica PowerCenter - Snowflake Scripting mappings and transformations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This page describes how an Informatica PowerCenter Mapping is converted to a Snowflake [stored procedure](/sql-reference/sql/create-procedure) in the Snowflake Scripting output format. For the dbt output format, see [dbt mappings and transformations](../dbt/mappings-and-transformations). For the concept map and the supported-component matrix, see the [Informatica PowerCenter overview](../README).

Warning

The Snowflake Scripting output format is in active development, so the generated code may change between releases. A transformation that isn’t converted produces a placeholder marked with an EWI code, as shown in [Unsupported transformations](#unsupported-transformations). For production migrations, use the generally available [dbt output format](../dbt/README). For the current status of each transformation, see [Supported transformations](README#supported-transformations).

## The mapping procedure

Each Mapping becomes one stored procedure named `public.m_<Mapping>`. The procedure takes a single `scope` parameter, returns `VARCHAR`, and runs as the caller. The data flow becomes the body, wrapped in a `BEGIN ... END` block:

Copy code

```
CREATE OR REPLACE PROCEDURE public.m_<Mapping> (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      -- Source Qualifier temporary tables, then the Target INSERT.
   END
$$;
```

The body is built in data-flow order:

1. If the Mapping references runtime variables, a `LET` declaration for each one reads its value with `GetControlVariableUDF` and the `scope` parameter. See [Variables and parameters](../variables-and-parameters).
2. If the Mapping uses a Sequence Generator, a `CREATE OR REPLACE SEQUENCE` statement is emitted first.
3. Each Source Qualifier becomes a `CREATE OR REPLACE TEMPORARY TABLE` statement. Pre-SQL and post-SQL on that Source Qualifier become `EXECUTE IMMEDIATE` statements around the table. See [Pre-SQL and post-SQL](#pre-sql-and-post-sql).
4. Each intermediate transformation becomes a common table expression (CTE), or a temporary table when its result feeds more than one downstream transformation.
5. A Mapplet instance first materializes its input as `tmp_mplt_in_cte_<instance>`, then either reads the Mapplet procedure inline with `TABLE(...)` or breaks the pipeline with `CALL` plus `RESULT_SCAN`. See [Mapplets](#mapplets).
6. The Target becomes the final write statement, which carries the upstream CTEs inside its source query. That statement is normally an `INSERT`, but an Update Strategy turns it into a `MERGE` or a `DELETE`. Pre-SQL and post-SQL on the Target run around that write statement.

The `scope` parameter is forwarded from the calling Task so the procedure resolves the same variable values the Workflow set at runtime. See [Workflows and orchestration](../workflows-and-orchestration).

## Source and Source Qualifier

A Source Definition emits no SQL of its own: it supplies the table metadata (database, schema, and table name) that the Source Qualifier reads. The Source Qualifier becomes a temporary table that selects the connected columns from the source table:

Informatica (`m_SimpleMapping`):

Copy code

```
<SOURCE NAME="SRC_TABLE" DATABASETYPE="Microsoft SQL Server" OWNERNAME="dbo">
   <!-- ID (primary key), NAME source fields omitted -->
</SOURCE>
<TRANSFORMATION NAME="SQ_SRC_TABLE" TYPE="Source Qualifier">
   <!-- ID, NAME ports omitted -->
   <TABLEATTRIBUTE NAME="Sql Query" VALUE=""/>
   <TABLEATTRIBUTE NAME="Source Filter" VALUE=""/>
</TRANSFORMATION>
```

Snowflake:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
   SELECT
      ID,
      NAME
   FROM
      YOUR_DB.dbo.SRC_TABLE;
```

The temporary table is named `tmp_sq_<name>` after the Source Qualifier. When the source connection cannot be resolved, the `YOUR_DB` and `YOUR_SCHEMA` placeholders are inserted into the qualified table name.

`Select Distinct=YES` projects `SELECT DISTINCT` on that temp table (`InfPcSourceQualifierBugFix_SelectDistinctYes_ProjectsLinkedPortsWithDistinct_Test`):

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_batch_params AS
   SELECT DISTINCT
      WORKFLOW_ID,
      WORKFLOW_NAME
   FROM
      YOUR_DB.dbo.BATCH_PARAMS
      ;
```

A Source Filter becomes a `WHERE` clause on the temp table (`InlineMode_SourceFilterOnly_AppendsWhereClauseWithFilter`):

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
   SELECT
      ID,
      NAME
   FROM
      YOUR_DB.dbo.SRC_TABLE
   WHERE
      ID > 10
      ;
```

A SQL Override that does not reference `$$VAR` replaces the generated `SELECT` with the override body (`InlineMode_MappingSqlOverrideNoVar_TempTableBodyIsOverrideVerbatim`):

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
   SELECT
      ID,
      NAME
   FROM
      YOUR_DB.dbo.SRC_TABLE
   WHERE
      ID > 0
      ;
```

When several sources are associated with one Source Qualifier, Snowflake Scripting `FROM` uses the first incoming source only. User Defined Join and filter text still land in `WHERE`. No EWI is emitted. The dbt format lists every incoming source. Review those procedures; do not assume a reconstructed `CROSS JOIN` or `LIMIT 1`. This User Defined Join example (`InlineMode_UserDefinedJoinOnly_AppendsWhereClauseWithJoinCondition`) still reads a single table:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
   SELECT
      ID,
      NAME
   FROM
      YOUR_DB.dbo.SRC_TABLE
   WHERE
      a.ID = b.ID
      ;
```

Important

Replace the `YOUR_DB` and `YOUR_SCHEMA` placeholders with your actual Snowflake database and schema before you run the procedure. Informatica does not export connection definitions, so they cannot be filled automatically.

### Flat File Source

A delimited flat-file source becomes a staged file read. SnowConvert generates a `FILE_FORMAT` from the Flat File Source attributes and casts each positional column to the corresponding source field type.

Informatica:

Copy code

```
<SOURCE DATABASETYPE="Flat File" DBDNAME="FlatFile" NAME="fl">
   <FLATFILE CODEPAGE="MS1252" DELIMITED="YES" DELIMITERS="," QUOTE_CHARACTER="DOUBLE" SKIPROWS="0"/>
   <SOURCEFIELD DATATYPE="string" FIELDNUMBER="1" NAME="FIELD1" PRECISION="2"/>
   <SOURCEFIELD DATATYPE="string" FIELDNUMBER="2" NAME="FIELD2" PRECISION="4"/>
</SOURCE>
```

Snowflake:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_fl AS
   SELECT
      FIELD1,
      FIELD2
   FROM
      (
         SELECT
            $1 :: VARCHAR(2) AS FIELD1,
            $2 :: VARCHAR(4) AS FIELD2
         FROM
            @public.landing_stage/infpc/sources/ScriptingCases/fl/fl.csv (FILE_FORMAT => 'ScriptingCases_m_FlatFileSource_fl')
      ) fl
```

The generated `file_formats.sql` file contains the corresponding file format:

Copy code

```
CREATE FILE FORMAT IF NOT EXISTS ScriptingCases_m_FlatFileSource_fl
TYPE = 'CSV'
FIELD_DELIMITER = ','
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ENCODING = 'WINDOWS1252'
EMPTY_FIELD_AS_NULL = TRUE;
```

Fixed-width flat-file sources don’t have an equivalent Snowflake file format. SnowConvert emits `SSC-EWI-INF0068`, doesn’t generate a `FILE_FORMAT`, and preserves a relational read as a placeholder for manual conversion.

## Expression

An Expression transformation becomes a CTE whose `SELECT` list carries each output port. A passthrough port appears as `col AS col`, and a computed port carries its translated formula. Informatica functions and operators convert to their Snowflake equivalents; for the full list, see [Expression functions](../expression-functions).

Informatica (`m_SimpleMapping`):

Copy code

```
<TRANSFORMATION NAME="EXP_Transform" TYPE="Expression">
   <TRANSFORMFIELD NAME="ID" PORTTYPE="INPUT/OUTPUT" EXPRESSION="ID"/>
   <TRANSFORMFIELD NAME="NAME" PORTTYPE="INPUT/OUTPUT" EXPRESSION="NAME"/>
</TRANSFORMATION>
```

Snowflake:

Copy code

```
WITH source_data AS
(
   SELECT
      ID,
      NAME
   FROM
      tmp_sq_src_table
)
SELECT
   ID AS ID,
   NAME AS NAME
FROM
   source_data
```

When an Expression feeds more than one downstream transformation, it is materialized as a `CREATE OR REPLACE TEMPORARY TABLE tmp_cte_<name>` instead of a CTE, so the result is computed once and reused.

A reserved-word port is quoted throughout the procedure (`InfPcExpressionBugFix_ReservedWordPortIsQuotedThroughoutProcedure`):

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_expr_lag_src AS
   SELECT
      OrderID,
      "ORDER"
   FROM
      YOUR_DB.YOUR_SCHEMA.EXPR_LAG_SRC
      ;
```

Chained LOCAL VARIABLE “lagger” ports become `LAG`. A depth-2 chain on `Amount` ordered by `RowSeq` emits `LAG(Amount, 2, 0)` (`InlineMode_LaggerChainDepth2_EmitsLagProcedure`):

Copy code

```
WITH cte_exp_lagger AS
(
   WITH source_data AS
   (
      SELECT
         RowSeq,
         Amount
      FROM
         tmp_sq_expr_lagchain_src
   )
   SELECT
      RowSeq AS RowSeq,
      Amount AS Amount,
      LAG(Amount, 2, 0) OVER (ORDER BY RowSeq) AS PrevPrevAmount
   FROM
      source_data
)
SELECT
   sd.RowSeq AS RowSeq,
   sd.Amount AS Amount,
   sd.PrevPrevAmount AS PrevPrevAmount
FROM
   cte_exp_lagger AS sd
   ;
```

## Target

The Target becomes the procedure’s final statement: an `INSERT` into the target table whose source query carries the upstream CTEs. The upstream data flow is aliased as `sd`:

Informatica (`m_SimpleMapping`):

Copy code

```
<TARGET NAME="TGT_TABLE" DATABASETYPE="Microsoft SQL Server">
   <TARGETFIELD NAME="ID" KEYTYPE="PRIMARY KEY" DATATYPE="nvarchar" PRECISION="50"/>
   <TARGETFIELD NAME="NAME" KEYTYPE="NOT A KEY" DATATYPE="nvarchar" PRECISION="100"/>
</TARGET>
```

Snowflake:

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.TGT_TGT_TABLE
WITH cte_exp_transform AS
(
   WITH source_data AS
   (
      SELECT
         ID,
         NAME
      FROM
         tmp_sq_src_table
   )
   SELECT
      ID AS ID,
      NAME AS NAME
   FROM
      source_data
)
SELECT
   *
FROM
   cte_exp_transform AS sd;
```

The CTEs are nested inside the `INSERT` rather than placed before it, because Snowflake Scripting does not accept a leading `WITH` clause as a statement inside a [`BEGIN ... END` block](/developer-guide/snowflake-scripting/blocks).

When the Session **Truncate target table** option is YES, a relational Target emits `TRUNCATE TABLE` immediately before the `INSERT` (`SnowflakeScriptingTargetTruncateBugFix_SessionTruncateTargetOptionYes_EmitsTruncateBeforeInsert_Test`). Flat-file stage unload does not honor truncate that way (see `SSC-EWI-INF0085`).

Copy code

```
TRUNCATE TABLE YOUR_DB.YOUR_SCHEMA.TGT_TGT_TABLE;
INSERT INTO YOUR_DB.YOUR_SCHEMA.TGT_TGT_TABLE
WITH cte_exp_transform AS
(
   SELECT
      ID,
      NAME
   FROM
      tmp_sq_src_table
)
SELECT
   *
FROM
   cte_exp_transform AS sd
   ;
```

### Flat File Target

A delimited flat-file target becomes a `COPY INTO <location>` statement that unloads rows to a stage. SnowConvert derives the file format from the Flat File Target attributes instead of treating the target as a relational table.

Informatica:

Copy code

```
<TARGET DATABASETYPE="Flat File" NAME="tgt">
   <FLATFILE CODEPAGE="UTF-8" DELIMITED="YES" DELIMITERS="|" QUOTE_CHARACTER="NONE" ROWDELIMITER="13,10"/>
   <TARGETFIELD DATATYPE="number" FIELDNUMBER="1" NAME="id" PRECISION="3" SCALE="0"/>
</TARGET>
```

Snowflake:

Copy code

```
EXECUTE IMMEDIATE 'COPY INTO @public.landing_stage/infpc/targets/tgt/ FROM (SELECT sd.FIELD1 AS id FROM tmp_sq_fl AS sd) FILE_FORMAT = (FORMAT_NAME = ''ScriptingCases_m_SqTarget_tgt'') HEADER = TRUE OVERWRITE = TRUE SINGLE = TRUE'
```

The canonical UTF-8 unload doesn’t produce `SSC-EWI-INF0074`. If the target specifies a non-UTF-8 code page, Snowflake still writes UTF-8 and SnowConvert emits this EWI:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0074 - FLAT FILE TARGET HAS CODEPAGE 'MS1252' (SNOWFLAKE ENCODING 'WINDOWS1252'). THE ENCODING OPTION IS ONLY VALID FOR COPY INTO <TABLE> (LOADING), NOT FOR COPY INTO <LOCATION> (UNLOADING). SNOWFLAKE ALWAYS WRITES UTF-8 WHEN UNLOADING TO STAGE. ***/!!!
```

If **Truncate target table option** is set to **YES**, SnowConvert doesn’t emit `TRUNCATE TABLE` because the target is a stage location. It emits a separate EWI:

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0085 - SESSION HAS 'TRUNCATE TARGET TABLE OPTION' (OR 'TRUNCATE TARGET OPTION') = YES, BUT FLAT FILE TARGET 'StudentsOut' UNLOADS TO A STAGE VIA COPY INTO <LOCATION>. THIS OPTION IS NOT HONOURED FOR STAGE-UNLOAD TARGETS — REVIEW WHETHER THE STAGE FILE NEEDS TO BE CLEARED BEFORE THIS LOAD. ***/!!!
```

## Naming conventions

Every generated object name is derived from the name of the transformation it came from, lowercased:

| Name | What it is |
| --- | --- |
| `tmp_sq_<name>` | The temporary table for a Source Qualifier. |
| `tmp_mplt_in_cte_<instance>` | The temporary table that holds a Mapplet instance’s input rows before the Mapplet procedure runs. |
| `<folder>_<mapplet>_<hash>` | The Mapplet’s own result-set procedure, for example `ScriptingCases_AnActiveMapplet_eeb91c86`. Mapping procedures stay `public.m_<Mapping>`. |
| `cte_<name>` | The CTE for an intermediate transformation. |
| `tmp_cte_<name>` | The same intermediate transformation, materialized as a temporary table instead because more than one downstream transformation reads it. |
| `source_data` | The inner CTE that carries a transformation’s input rows. |
| `sd` | The alias for the upstream data flow in the final write statement. |

Expand

Show lessSee more

## Filter

A Filter becomes a `WHERE` clause on its `source_data` input:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_cte_filtrans AS
   WITH source_data AS
   (
      SELECT
         ID,
         NAME,
         GRADE
      FROM
         tmp_sq_flt_fork2_src
   )
   SELECT
      ID,
      NAME,
      GRADE
   FROM
      source_data
   WHERE
      GRADE > 50;
```

This example is materialized as a temporary table because two downstream transformations read the filtered rows. A Filter with a single consumer becomes a `cte_<name>` CTE instead.

## Router

A Router materializes its input once, then emits one write statement per output group. Each group’s condition becomes that statement’s `WHERE` clause. The default group is written last, and its condition is the negation of every other group’s condition:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_cte_rtrtrans AS
   SELECT
      ID,
      GRADE
   FROM
      tmp_sq_rtr_c1_src;
INSERT INTO YOUR_DB.YOUR_SCHEMA.RTR_C1_MATCH (ID, GRADE)
SELECT
   ID AS ID,
   GRADE AS GRADE
FROM
   tmp_cte_rtrtrans
WHERE
   GRADE > 80;
INSERT INTO YOUR_DB.YOUR_SCHEMA.RTR_C1_DEF (ID, GRADE)
SELECT
   ID AS ID,
   GRADE AS GRADE
FROM
   tmp_cte_rtrtrans
WHERE
   NOT COALESCE(GRADE > 80, FALSE);
```

The default group wraps the negated condition in `COALESCE(..., FALSE)` so that rows where the condition evaluates to `NULL` still reach the default group, which is how PowerCenter routes them.

## Joiner

A Joiner becomes a CTE that joins its master and detail inputs on the join condition. The Informatica join type determines the SQL join: a normal join becomes an inner join, and master or detail outer joins become the corresponding outer join.

Snowflake (`InlineMode_Joiner_NormalInner_EmitsProcedureSql`):

Copy code

```
WITH cte_jnr_joiner_inner AS
(
   SELECT
      m.MKEY,
      m.MVAL,
      d.DKEY,
      d.DVAL
   FROM
      tmp_sq_jn14_mst AS m
      INNER JOIN
         tmp_sq_jn14_det AS d
         ON m.MKEY = d.DKEY
)
SELECT
   sd.MKEY AS MKEY,
   sd.MVAL AS MVAL,
   sd.DKEY AS DKEY,
   sd.DVAL AS DVAL
FROM
   cte_jnr_joiner_inner AS sd
   ;
```

## Union

A Union becomes a CTE whose `source_data` combines every input with `UNION ALL`, which preserves duplicate rows the way PowerCenter does:

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.U37_C1_TGT
WITH cte_uniont AS
(
   WITH source_data AS
   (
      SELECT
         TXT
      FROM
         tmp_sq_u37_c1_emp
      UNION ALL
      SELECT
         TXT
      FROM
         tmp_sq_u37_c1_stu
   )
   SELECT
      TXT AS TXT
   FROM
      source_data
)
SELECT
   *
FROM
   cte_uniont AS sd;
```

## Aggregator

An Aggregator becomes a CTE with a `GROUP BY` over its group-by ports. Each aggregate port carries its translated aggregate function, cast to the port’s declared type:

Copy code

```
SELECT
   DEPTCODE AS DEPTCODE,
   CAST(SUM(SALARY) AS NUMBER(18,2)) AS SUMSALARY,
```

An Aggregator with no group-by ports aggregates over the whole input, producing a single row.

## Sorter

A Sorter becomes an `ORDER BY` on its input. When the transformation has the distinct option enabled, duplicate rows are removed as well.

## Sequence Generator

A Sequence Generator becomes a native Snowflake [sequence](/sql-reference/sql/create-sequence), created at the top of the procedure body before any data flows. Downstream ports read it with `NEXTVAL`:

Copy code

```
CREATE OR REPLACE SEQUENCE YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq
   START WITH 1
   INCREMENT BY 1;
```

The sequence is named `<transformation>_seq` and persists after the procedure finishes, because a Snowflake sequence isn’t a temporary object. Reusable and non-reusable Sequence Generators are both converted.

When several consumers read the same Sequence Generator, one native sequence is created and each consumer `INSERT` reads `.NEXTVAL`. `SSC-EWI-INF0079` and `SSC-EWI-INF0083` disclose non-deterministic assignment and the shared counter versus PowerCenter session isolation (`Sequence_FanoutMultipleConsumers_EmitsExpectedProcedureSql`):

Copy code

```
CREATE OR REPLACE SEQUENCE YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq
   START WITH 1
   INCREMENT BY 1
   ;

!!!RESOLVE EWI!!! /*** SSC-EWI-INF0079 - THE SEQUENCE GENERATOR IS TRANSLATED TO A SNOWFLAKE NATIVE SEQUENCE (.NEXTVAL). ROW ORDERING IS NON-DETERMINISTIC (VALUES MAY BE ASSIGNED TO DIFFERENT ROWS BETWEEN RUNS). ADD A DETERMINISTIC ORDER BY IN THE SOURCE QUERY IF STABLE SEQUENCE ASSIGNMENT IS REQUIRED. ***/!!!
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0083 - THE SEQUENCE GENERATOR IS NON-REUSABLE WITH 'IS CURRENT VALUE SHARED' = NO, SO IN POWERCENTER EACH CONCURRENT SESSION GETS AN ISOLATED SEQUENCE COUNTER. THE TRANSLATION USES A SINGLE SNOWFLAKE NATIVE SEQUENCE OBJECT SHARED BY ALL SESSIONS, SO CONCURRENT RUNS DRAW FROM ONE COUNTER AND MAY PRODUCE INTERLEAVED OR NON-CONTIGUOUS VALUES PER SESSION. REVIEW WHETHER CONCURRENT EXECUTION REQUIRES PER-SESSION VALUE ISOLATION (E.G. USE A SEPARATE SEQUENCE OR A SESSION-SCOPED COUNTER). ***/!!!
INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_FANOUT_A (id, seq_val)
SELECT
   id AS id,
   YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq.NEXTVAL AS seq_val
FROM
   tmp_sq_seq_src_fanout
   ;

INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_FANOUT_B (id, seq_val)
SELECT
   id AS id,
   YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq.NEXTVAL AS seq_val
FROM
   tmp_sq_seq_src_fanout
   ;
```

## Normalizer

A Normalizer becomes a chain of CTEs that expand each repeating group into separate output rows, one CTE per generated occurrence.

## Rank

A Rank transformation assigns `ROW_NUMBER()` over the rank port and keeps the top or bottom N rows with `QUALIFY RANKINDEX <= N`. Top ranks sort the rank port in descending order; bottom ranks sort it in ascending order. SnowConvert uses `ROW_NUMBER()`, not `RANK()`, to match the number of rows that PowerCenter returns.

Informatica:

Copy code

```
<TRANSFORMATION NAME="RNK_TopN" TYPE="Rank">
   <TRANSFORMFIELD EXPRESSION="RANKINDEX" EXPRESSIONTYPE="RANKINDEX" NAME="RANKINDEX" PORTTYPE="OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="product_id" EXPRESSIONTYPE="GENERAL" NAME="product_id" PORTTYPE="INPUT/OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="product_name" EXPRESSIONTYPE="GENERAL" NAME="product_name" PORTTYPE="INPUT/OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="sales_amount" EXPRESSIONTYPE="RANKPORT" NAME="sales_amount" PORTTYPE="INPUT/OUTPUT"/>
   <TABLEATTRIBUTE NAME="Top/Bottom" VALUE="TOP"/>
   <TABLEATTRIBUTE NAME="Number of Ranks" VALUE="5"/>
</TRANSFORMATION>
```

Snowflake:

Copy code

```
WITH
--** SSC-FDM-INF0085 - RANK TRANSFORMATION: WHEN MULTIPLE INPUT ROWS HAVE THE SAME RANK-PORT VALUE AT THE QUALIFY BOUNDARY, POWERCENTER BREAKS TIES BY INPUT ROW ARRIVAL ORDER. SNOWFLAKE'S ROW_NUMBER() WINDOW DOES NOT GUARANTEE ARRIVAL-ORDER TIEBREAKING WITHOUT A STABLE ROW-IDENTITY KEY. IF INPUT DATA HAS TIED VALUES AT THE N-TH POSITION, THE SURVIVING ROW(S) MAY DIFFER FROM POWERCENTER. VERIFY THAT TIED INPUT DATA DOES NOT OCCUR OR THAT DOWNSTREAM LOGIC IS INSENSITIVE TO THE TIE SURVIVOR. **
cte_rnk_topn AS
(
   WITH source_data AS
   (
      SELECT
         product_id,
         product_name,
         sales_amount
      FROM
         tmp_sq_rank_topn_src
   )
   SELECT
      product_id AS product_id,
      product_name AS product_name,
      sales_amount AS sales_amount,
      ROW_NUMBER() OVER (ORDER BY sales_amount DESC) AS RANKINDEX
   FROM
      source_data
   QUALIFY
      RANKINDEX <= 5
)
SELECT
   sd.product_id AS product_id,
   sd.product_name AS product_name,
   sd.sales_amount AS sales_amount,
   sd.RANKINDEX AS rank_pos
FROM
   cte_rnk_topn AS sd
```

When a port has the `GROUPBY` expression type, SnowConvert partitions the row numbering by that port. The following example returns the top three salaries in each department.

Informatica:

Copy code

```
<TRANSFORMATION NAME="RNK_GroupedTopN" TYPE="Rank">
   <TRANSFORMFIELD EXPRESSION="RANKINDEX" EXPRESSIONTYPE="RANKINDEX" NAME="RANKINDEX" PORTTYPE="OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="emp_id" EXPRESSIONTYPE="GENERAL" NAME="emp_id" PORTTYPE="INPUT/OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="department" EXPRESSIONTYPE="GROUPBY" NAME="department" PORTTYPE="INPUT/OUTPUT"/>
   <TRANSFORMFIELD EXPRESSION="salary" EXPRESSIONTYPE="RANKPORT" NAME="salary" PORTTYPE="INPUT/OUTPUT"/>
   <TABLEATTRIBUTE NAME="Top/Bottom" VALUE="TOP"/>
   <TABLEATTRIBUTE NAME="Number of Ranks" VALUE="3"/>
</TRANSFORMATION>
```

Snowflake:

Copy code

```
WITH
--** SSC-FDM-INF0085 - RANK TRANSFORMATION: WHEN MULTIPLE INPUT ROWS HAVE THE SAME RANK-PORT VALUE AT THE QUALIFY BOUNDARY, POWERCENTER BREAKS TIES BY INPUT ROW ARRIVAL ORDER. SNOWFLAKE'S ROW_NUMBER() WINDOW DOES NOT GUARANTEE ARRIVAL-ORDER TIEBREAKING WITHOUT A STABLE ROW-IDENTITY KEY. IF INPUT DATA HAS TIED VALUES AT THE N-TH POSITION, THE SURVIVING ROW(S) MAY DIFFER FROM POWERCENTER. VERIFY THAT TIED INPUT DATA DOES NOT OCCUR OR THAT DOWNSTREAM LOGIC IS INSENSITIVE TO THE TIE SURVIVOR. **
cte_rnk_groupedtopn AS
(
   WITH source_data AS
   (
      SELECT
         emp_id,
         department,
         salary
      FROM
         tmp_sq_rank_grp_src
   )
   SELECT
      emp_id AS emp_id,
      department AS department,
      salary AS salary,
      ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS RANKINDEX
   FROM
      source_data
   QUALIFY
      RANKINDEX <= 3
)
SELECT
   sd.emp_id AS emp_id,
   sd.department AS department,
   sd.salary AS salary,
   sd.RANKINDEX AS rank_pos
FROM
   cte_rnk_groupedtopn AS sd
```

## Lookup

A connected Lookup becomes a CTE containing two inner CTEs: `lookup_reference` reads the lookup table, and `input_data` carries the incoming rows. They’re joined with a `LEFT JOIN` on the lookup condition, so rows with no match still pass through with `NULL` lookup values.

### Use Any Value

Because PowerCenter returns a single row per lookup, `lookup_reference` is deduplicated with `QUALIFY ROW_NUMBER()` partitioned by the lookup condition ports:

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.LKP_Tgt_Baseline (SC_ROW_ID, EmpId, DeptName)
WITH
--** SSC-FDM-INF0070 - Use Any Value RETURNS AN ARBITRARY ROW WHEN MULTIPLE ROWS MATCH; IN SNOWFLAKE THE SELECTED ROW MAY VARY PER RUN. ADD AN ORDER BY TO THE LOOKUP SQL OVERRIDE ONLY IF A SPECIFIC ROW IS REQUIRED. **
cte_lkptrans AS
(
   WITH lookup_reference AS
   (
      SELECT
         DeptCode ,
         DeptName
      FROM
         YOUR_DB.YOUR_SCHEMA.LKP_Dept_Baseline
      QUALIFY
         ROW_NUMBER() OVER (
         PARTITION BY
            DeptCode
         ORDER BY
            (
               SELECT
                  null
            )) = 1
   ),
   input_data AS
   (
      SELECT
         DeptCode DeptCode1,
         SC_ROW_ID SQ_LKP_Emp_Baseline__SC_ROW_ID,
         EmpId SQ_LKP_Emp_Baseline__EmpId
      FROM
         tmp_sq_lkp_emp_baseline
   )
   SELECT
      input_data.DeptCode1 ,
      input_data.SQ_LKP_Emp_Baseline__SC_ROW_ID ,
      input_data.SQ_LKP_Emp_Baseline__EmpId ,
      lookup_reference.DeptCode,
      lookup_reference.DeptName
   FROM
      input_data
      LEFT JOIN
         lookup_reference
         ON lookup_reference.DeptCode = input_data.DeptCode1
)
SELECT
   sd.SQ_LKP_Emp_Baseline__SC_ROW_ID AS SC_ROW_ID,
   sd.SQ_LKP_Emp_Baseline__EmpId AS EmpId,
   sd.DeptName AS DeptName
FROM
   cte_lkptrans AS sd;
```

Input ports are aliased `<source_qualifier>__<port>` inside `input_data` so they can’t collide with the lookup table’s own column names.

The `SSC-FDM-INF0070` note is emitted because the `ORDER BY` inside `ROW_NUMBER()` has no deterministic key. If a lookup can match several rows and you need a specific one, add an `ORDER BY` to the Lookup SQL override.

### Use All Values

When the multiple-match policy is **Use All Values**, the converter emits a plain `LEFT JOIN` with **no** `QUALIFY ROW_NUMBER()`. `SSC-FDM-INF0061` records that the join can increase the row count.

Snowflake (`Lookup_MultiMatchUseAllValues_EmitsExpectedProcedureSql`):

Copy code

```
WITH cte_lkptrans AS
(
   WITH lookup_reference AS
   (
      SELECT
         DeptCode ,
         DeptName
      FROM
         YOUR_DB.YOUR_SCHEMA.LKP_Dept_AllVal
   ),
   input_data AS
   (
      SELECT
         DeptCode DeptCode1,
         EmpId
      FROM
         tmp_sq_lkp_emp_allval
   )
   SELECT
      input_data.DeptCode1 ,
      input_data.EmpId ,
      lookup_reference.DeptCode,
      lookup_reference.DeptName
   FROM
      --** SSC-FDM-INF0061 - CONNECTED LOOKUP 'LKPTRANS' USES MULTI-MATCH POLICY 'USE ALL VALUES'. THE TRANSLATION EMITS A JOIN AGAINST 'LKP_Dept_AllVal'. ROW COUNT MAY INCREASE. **
      input_data
      LEFT JOIN
         lookup_reference
         ON lookup_reference.DeptCode = input_data.DeptCode1
)
SELECT
   NULL :: NUMERIC(10, 0) AS SC_ROW_ID,
   sd.EmpId AS EmpId,
   sd.DeptName AS DeptName
FROM
   cte_lkptrans AS sd
   ;
```

### Flat file Lookup

A connected flat-file Lookup follows the Use Any Value shape, but `lookup_reference` reads positional `$1` / `$2` columns from `@public.landing_stage/infpc/sources/<Folder>/<Def>/`. `SSC-EWI-INF0069` is emitted when the source file name cannot be resolved.

Snowflake (`Lookup_ConnectedFlatFileWithHeader_EmitsExpectedProcedureSql`):

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.FF_LKP_Tgt_Hdr (SC_ROW_ID, CustId, CustName)
WITH
--** SSC-FDM-INF0070 - Use Any Value RETURNS AN ARBITRARY ROW WHEN MULTIPLE ROWS MATCH; IN SNOWFLAKE THE SELECTED ROW MAY VARY PER RUN. ADD AN ORDER BY TO THE LOOKUP SQL OVERRIDE ONLY IF A SPECIFIC ROW IS REQUIRED. **
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0069 - FLAT FILE SOURCE FILE NAME COULD NOT BE RESOLVED. LANDING PATH '@public.landing_stage/infpc/sources/Lookup_SNOW_3719618/ff_lkp_hdr/UNKNOWN_FILE' REQUIRES A MANUAL FILE BINDING. ***/!!!
cte_lkptrans AS
(
   WITH lookup_reference AS
   (
      SELECT
         id ,
         name
      FROM
         (
            SELECT
               $1 :: NUMBER(10, 0) AS id,
               $2 :: VARCHAR(50) AS name
            FROM
               @public.landing_stage/infpc/sources/Lookup_SNOW_3719618/ff_lkp_hdr/UNKNOWN_FILE (FILE_FORMAT => 'Lookup_SNOW_3719618_m_Lookup_FlatFileHdr_ff_lkp_hdr')
         ) ff_lkp_hdr
      QUALIFY
         ROW_NUMBER() OVER (
         PARTITION BY
            id
         ORDER BY
            (
               SELECT
                  null
            )) = 1
   ),
   input_data AS
   (
      SELECT
         CustId in_CustId,
         SC_ROW_ID SQ_FF_LKP_Src_Hdr__SC_ROW_ID,
         CustId SQ_FF_LKP_Src_Hdr__CustId
      FROM
         tmp_sq_ff_lkp_src_hdr
   )
   SELECT
      input_data.SQ_FF_LKP_Src_Hdr__SC_ROW_ID ,
      input_data.SQ_FF_LKP_Src_Hdr__CustId ,
      lookup_reference.id,
      lookup_reference.name
   FROM
      input_data
      LEFT JOIN
         lookup_reference
         ON lookup_reference.id = input_data.in_CustId
)
SELECT
   sd.SQ_FF_LKP_Src_Hdr__SC_ROW_ID AS SC_ROW_ID,
   sd.SQ_FF_LKP_Src_Hdr__CustId AS CustId,
   sd.name AS CustName
FROM
   cte_lkptrans AS sd
   ;
```

### Unconnected Lookup

An unconnected Lookup becomes its own `CREATE FUNCTION` file. The function name is `<Folder>_<Def>_<8-hex SHA256 of identity>` (for example `Lookup_SNOW_3702098_m_Lookup_DisconnUnconn_LKPTRANS_222878c0`). The body uses `ANY_VALUE` and `EQUAL_NULL`. The calling Expression CTE invokes the function.

Snowflake (`Lookup_DisconnectedUnconnected_EmitsExpectedProcedureSql`):

Copy code

```
CREATE OR REPLACE FUNCTION public.Lookup_SNOW_3702098_m_Lookup_DisconnUnconn_LKPTRANS_222878c0 (in_code VARCHAR(10))
RETURNS VARCHAR(100)
LANGUAGE SQL
AS
$$
  SELECT
    ANY_VALUE(DeptName)
  FROM
    YOUR_DB.YOUR_SCHEMA.DL_Dept
  WHERE
    EQUAL_NULL(DeptCode, in_code)
$$
```

Call site from `m_Lookup_DisconnUnconn.sql`:

Copy code

```
WITH cte_exptrans AS
(
   SELECT
      SC_ROW_ID,
      EmpId,
      DeptCode,
      Lookup_SNOW_3702098_m_Lookup_DisconnUnconn_LKPTRANS_222878c0(DeptCode) AS o_dname
   FROM
      tmp_sq_dl_emp
)
SELECT
   sd.SC_ROW_ID AS SC_ROW_ID,
   sd.EmpId AS EmpId,
   sd.o_dname AS DeptName
FROM
   cte_exptrans AS sd
   ;
```

## Update Strategy

An Update Strategy changes the Target’s write statement instead of adding a CTE of its own. A `DD_UPDATE` strategy becomes a `MERGE` that matches on the target’s primary key:

Copy code

```
--** SSC-FDM-INF0019 - THE UPDATE STRATEGY LOGIC WAS MOVED TO THE TARGET MODEL. **
MERGE INTO YOUR_DB.YOUR_SCHEMA.us_upd_tgt AS tgt
USING tmp_sq_us_upd_src AS src ON tgt.order_id = src.order_id
WHEN MATCHED THEN
   UPDATE SET
      tgt.customer_name = src.customer_name,
      tgt.amount = src.amount;
```

A `DD_DELETE` strategy becomes a `DELETE` of the target rows whose key matches an incoming row. The `SSC-FDM-INF0019` note records that the strategy’s logic now lives in the target write statement rather than in a transformation of its own.

Important

Update Strategy is converted for the dispatch shapes shown earlier (`DD_UPDATE` → `MERGE`, `DD_DELETE` → `DELETE`). A Mapping whose strategy expression does not resolve to a recognized dispatch shape falls back to the dbt output. Review the generated procedure to confirm the write statement matches the strategy you expect.

## Mapplets

A Mapplet becomes its own result-set stored procedure, separate from the procedures of the Mappings that use it, so a Mapplet shared by several Mappings is converted once. Mapping procedures stay `public.m_<Mapping>`. Mapplet procedures use a hashed, folder-qualified name such as `ScriptingCases_AnActiveMapplet_eeb91c86`, because Informatica allows the same Mapplet name in different folders while Snowflake puts every procedure in one schema.

Input Transformation and Output Transformation objects inside a Mapplet are the Mapplet’s ports. They aren’t rows in the 34-name transformation catalog.

The Mapplet procedure takes an `in_table VARCHAR` parameter, reads the caller’s table through `IDENTIFIER(:in_table)`, and returns the Output Transformation’s exposed ports:

Copy code

```
CREATE OR REPLACE PROCEDURE public.ScriptingCases_AnActiveMapplet_eeb91c86 (in_table VARCHAR)
RETURNS TABLE (
   i11 VARCHAR(10),
   i21 NUMERIC(10, 0)
)
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      res RESULTSET;
   BEGIN
      res := (
      WITH cte_input AS
      (
         SELECT
            CAST(LEFT(i1, 10) AS VARCHAR(10)) AS i1,
            CAST(LEFT(i2, 10) AS VARCHAR(10)) AS i2
         FROM
            IDENTIFIER(:in_table)
      ),
      cte_internalfilter AS
      (
         WITH source_data AS
         (
            SELECT
               i1,
               i2
            FROM
               cte_input
         )
         SELECT
            i1,
            i2
         FROM
            source_data
         WHERE
            i2 > 10
      )
      SELECT
         CAST(LEFT(i1, 10) AS VARCHAR(10)) AS i11,
         CAST(i2 AS NUMERIC(10, 0)) AS i21
      FROM
         cte_internalfilter
         );
      RETURN TABLE(res);
   END;
$$;
```

`cte_input` is name-bound: it maps the Input Transformation’s port names onto columns of the caller’s table, and it casts each port to the declared type. The body is wrapped in the `DECLARE res RESULTSET; ... RETURN TABLE(res)` scaffold that Snowflake requires to return a result set.

The calling Mapping materializes those input rows as `tmp_mplt_in_cte_<instance>` and reads the procedure with `TABLE(...)`:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_mplt_in_cte_anactivemapplet AS
   SELECT
      i1 AS i1,
      i2 AS i2
   FROM
      tmp_sq_activemappletsource;
INSERT INTO YOUR_DB.YOUR_SCHEMA.ActiveMappletTarget (i11, i21)
WITH cte_anactivemapplet AS
(
   SELECT
      *
   FROM
      TABLE(public.ScriptingCases_AnActiveMapplet_eeb91c86('tmp_mplt_in_cte_anactivemapplet'))
)
SELECT
   sd.i11 AS i11,
   sd.i21 AS i21
FROM
   cte_anactivemapplet AS sd;
```

### Call sites that pass scope

The previous example is the inline form, where the Mapplet composes as a CTE. When the Mapplet procedure takes a `scope` parameter, Snowflake rejects `:scope` inside `FROM TABLE()`, so the converter emits a pipeline break instead: a `CALL` as a pre-hook, then `TABLE(RESULT_SCAN(LAST_QUERY_ID()))`:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_mplt_in_cte_mappletwithvariables AS
   SELECT
      ROW_NUMBER()
      OVER (
      ORDER BY
         null) AS __row_id,
      EmpName AS i_1,
      DeptCode AS i2
   FROM
      tmp_sq_tbg_employees;
CALL public.ScriptingCases_MappletWithVariables_853af6f1('tmp_mplt_in_cte_mappletwithvariables', :scope);
INSERT INTO YOUR_DB.YOUR_SCHEMA.D_TABLE_2 (TXT)
WITH cte_mappletwithvariables AS
(
   SELECT
      *
   FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()))
)
SELECT
   sd.o_out AS TXT
FROM
   cte_mappletwithvariables AS sd;
```

A `scope VARCHAR` parameter is added to the Mapplet procedure only when the Mapplet references a control variable. The pipeline-break form is also used when the Mapplet body runs DDL or DML before its final query, because Snowflake rejects those statements inside `FROM TABLE()`.

### No-input mapplets

A Mapplet that contains its own Source Qualifier has no input boundary, so its procedure takes no parameters and the call site passes no arguments, including no `:scope`:

Copy code

```
CREATE OR REPLACE PROCEDURE public.ScriptingCases_MappletNoInput_44cf2690 ()
RETURNS TABLE (
   EmpId NUMERIC(10, 0),
   EmpName VARCHAR(100),
   DeptCode VARCHAR(10),
   UpdatedSalary NUMERIC(10, 2)
)
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      res RESULTSET;
   BEGIN
      res := (
      WITH cte_sq_tbg_employees AS
      (
         SELECT
            EmpId,
            EmpName,
            DeptCode,
            Salary
         FROM
            YOUR_DB.dbo.Tbg_Employees
      ),
      cte_incrementsalaries AS
      (
         SELECT
            EmpId,
            EmpName,
            DeptCode,
            Salary + 2 AS UpdatedSalary
         FROM
            cte_sq_tbg_employees
      )
      SELECT
         CAST(EmpId AS NUMERIC(10, 0)) AS EmpId,
         CAST(LEFT(EmpName, 100) AS VARCHAR(100)) AS EmpName,
         CAST(LEFT(DeptCode, 10) AS VARCHAR(10)) AS DeptCode,
         CAST(UpdatedSalary AS NUMERIC(10, 2)) AS UpdatedSalary
      FROM
         cte_incrementsalaries
         );
      RETURN TABLE(res);
   END;
$$;
```

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.EmpTarget (EmpId, EmpName, DeptCode, UpdatedSalary)
WITH cte_mappletnoinput AS
(
   SELECT
      *
   FROM
      TABLE(public.ScriptingCases_MappletNoInput_44cf2690())
)
SELECT
   sd.EmpId AS EmpId,
   sd.EmpName AS EmpName,
   sd.DeptCode AS DeptCode,
   sd.UpdatedSalary AS UpdatedSalary
FROM
   cte_mappletnoinput AS sd;
```

### Passive mapplets

A passive Mapplet returns one row for each row you pass in, and the enclosing Mapping usually needs columns that bypass the Mapplet. Those carry columns are reunited with a converter-synthesized `__row_id`. Passive `cte_input` reads that surrogate as the first positional column (`$1 AS __row_id`) and reads the Input Transformation ports by name:

Copy code

```
WITH cte_input AS
(
   SELECT
      $1 AS __row_id,
      CAST(LEFT(i_1, 10) AS VARCHAR(10)) AS i_1,
      CAST(LEFT(i_21, 10) AS VARCHAR(10)) AS i_21
   FROM
      IDENTIFIER(:in_table)
)
```

The call site materializes `__row_id` on `tmp_mplt_in_cte_<instance>` and left-joins the Mapplet result back to the carry columns:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_mplt_in_cte_passivemapplet AS
   SELECT
      ROW_NUMBER()
      OVER (
      ORDER BY
         null) AS __row_id,
      Salary AS i_1,
      o_cal AS i_21,
      SQ_Tbg_Employees__Id,
      SQ_Tbg_Employees__Name,
      SQ_Tbg_Employees__DName
   FROM
      tmp_cte_exptrans;
INSERT INTO YOUR_DB.YOUR_SCHEMA.EmpTarget (Id, Name, DName, Salary)
WITH cte_passivemapplet AS
(
   SELECT
      m.o_calc AS o_calc,
      m.i_11 AS i_11,
      i.SQ_Tbg_Employees__Id AS SQ_Tbg_Employees__Id,
      i.SQ_Tbg_Employees__Name AS SQ_Tbg_Employees__Name,
      i.SQ_Tbg_Employees__DName AS SQ_Tbg_Employees__DName
   FROM
      tmp_mplt_in_cte_passivemapplet AS i
      LEFT JOIN
         TABLE(public.ScriptingCases_PassiveMapplet_4065eabc('tmp_mplt_in_cte_passivemapplet')) AS m
         ON m.__row_id = i.__row_id
)
SELECT
   sd.SQ_Tbg_Employees__Id AS Id,
   sd.SQ_Tbg_Employees__Name AS Name,
   sd.SQ_Tbg_Employees__DName AS DName,
   sd.o_calc AS Salary
FROM
   cte_passivemapplet AS sd;
```

The carry columns are aliased `<source_qualifier>__<port>` so they can’t collide with the Mapplet’s own output ports. `__row_id` doesn’t appear in your PowerCenter metadata.

### Multiple inputs or outputs

A Mapplet with more than one Input Transformation or Output Transformation isn’t converted to a procedure. The enclosing Mapping emits the same `SSC-EWI-INF0001` placeholder shown in [Unsupported transformations](#unsupported-transformations), including `Unsupported transformation 'mplt_multi_io'` and `null AS out_a` for the connected output port. No `FROM TABLE(public.ScriptingCases_mplt_multi_io(...))` call site is generated, and no Mapplet procedure file is emitted.

## Pre-SQL and post-SQL

Pre-SQL and post-SQL attached to a Source Qualifier or a Target become `EXECUTE IMMEDIATE` statements in the procedure body, positioned around the statement they belong to. Mapping-level hooks on a Source Qualifier run before and after the temporary table:

Copy code

```
EXECUTE IMMEDIATE 'TRUNCATE TABLE staging.pre';
CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
   SELECT
      ID,
      NAME
   FROM
      YOUR_DB.dbo.SRC_TABLE;
EXECUTE IMMEDIATE 'UPDATE audit.log SET n = n + 1';
```

`EXECUTE IMMEDIATE` is used rather than inlining the statement because the hook is arbitrary SQL that the converter doesn’t parse as part of the data flow.

When a Target has both mapping-level and session-level Pre-SQL or Post-SQL, the session value overrides the mapping value. Only the session hook is emitted around the `INSERT`:

Copy code

```
LET effective_tgt_tgt_table_pre_sql VARCHAR := COALESCE(public.GetControlVariableUDF('m_SimpleMapping_tgt_tgt_table_pre_sql', :scope) :: VARCHAR, 'TRUNCATE TABLE staging.tgt_mapping_pre');
IF (effective_tgt_tgt_table_pre_sql IS NOT NULL
AND effective_tgt_tgt_table_pre_sql <> '') THEN
   EXECUTE IMMEDIATE 'BEGIN
' || :effective_tgt_tgt_table_pre_sql || '
;
END;';
END IF;
INSERT INTO YOUR_DB.YOUR_SCHEMA.TGT_TGT_TABLE (ID, NAME)
WITH cte_exp_transform AS
(
   SELECT
      ID,
      NAME
   FROM
      tmp_sq_src_table
)
SELECT
   sd.ID AS ID,
   sd.NAME AS NAME
FROM
   cte_exp_transform AS sd;
LET effective_tgt_tgt_table_post_sql VARCHAR := COALESCE(public.GetControlVariableUDF('m_SimpleMapping_tgt_tgt_table_post_sql', :scope) :: VARCHAR, 'UPDATE audit.log SET tgt_mapping_post = CURRENT_TIMESTAMP()');
IF (effective_tgt_tgt_table_post_sql IS NOT NULL
AND effective_tgt_tgt_table_post_sql <> '') THEN
   EXECUTE IMMEDIATE 'BEGIN
' || :effective_tgt_tgt_table_post_sql || '
;
END;';
END IF
```

A hook that contains several statements is wrapped in its own `BEGIN ... END` block, and a hook that references Informatica variables is built by concatenating the variable values into the string before it runs. See [Workflows and orchestration](../workflows-and-orchestration).

## Reusable transformations

A reusable Filter, Expression, or Aggregator is emitted once under `shared_objects/` and reused from every Mapping that consumes it. Shared object names use the same `<Folder>_<Def>_<8-hex>` pattern as mapplets and unconnected Lookup UDFs. Mapping procedures stay `public.m_<Mapping>`. Two Mappings that consume the same reusable Expression publish one shared object (`folder/Informatica/shared_objects/Expression_SNOW_3702218_IncBy2_721a9976.sql`).

Reusable Lookup, Normalizer, and Sequence follow the same placement rule; their call-site SQL is the same shape as the non-reusable sections above.

### Reusable Filter

A reusable Filter becomes a BOOLEAN UDF. The Mapping CTE calls it in `WHERE`.

Snowflake (`FilterReusableSingle_EmitsSharedBooleanUdfAndCallsItFromCte`):

Copy code

```
CREATE OR REPLACE FUNCTION Filter_SNOW_3700504_FILTRANS_REUSE_53685749 (i_id NUMERIC(10, 0), i_txt VARCHAR(50), i_num NUMERIC(10, 0))
RETURNS BOOLEAN
AS
$$
  i_num > 58
$$
```

Copy code

```
WITH cte_reusefiltrans AS
(
   WITH source_data AS
   (
      SELECT
         ID AS i_id,
         NAME AS i_txt,
         GRADE AS i_num
      FROM
         tmp_sq_flt_reuse_src
   )
   SELECT
      i_id,
      i_txt,
      i_num
   FROM
      source_data
   WHERE
      Filter_SNOW_3700504_FILTRANS_REUSE_53685749(i_id, i_txt, i_num)
)
SELECT
   sd.i_id AS ID,
   sd.i_txt AS NAME,
   sd.i_num AS GRADE
FROM
   cte_reusefiltrans AS sd
   ;
```

### Reusable Expression

A reusable Expression becomes a UDTF. The Mapping reads it with `LATERAL`.

Snowflake (`EmitsUdtfDefinitionAndLateralCallSite`):

Copy code

```
CREATE OR REPLACE FUNCTION Expression_SNOW_3702218_IncBy2_721a9976 (i_value NUMERIC(38, 0))
RETURNS TABLE (
  i_value NUMERIC(38, 0),
  o_value NUMERIC(38, 0)
)
AS
$$
  SELECT
    i_value AS i_value,
    i_value * 2 AS o_value
$$
```

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_cte_incby2 AS
   SELECT
      input.SRC_ID AS SQ_EXPR_REUSE_SINGLE_SRC__SRC_ID,
      expr.i_value ,
      expr.o_value
   FROM
      tmp_sq_expr_reuse_single_src input,
      LATERAL Expression_SNOW_3702218_IncBy2_721a9976(CAST(input.NUM_IN AS NUMERIC(38, 0))) expr
      ;
INSERT INTO YOUR_DB.YOUR_SCHEMA.EXPR_REUSE_SINGLE_TGT (SRC_ID, NUM_OUT)
SELECT
   sd.SQ_EXPR_REUSE_SINGLE_SRC__SRC_ID AS SRC_ID,
   sd.o_value AS NUM_OUT
FROM
   tmp_cte_incby2 AS sd
   ;
```

### Reusable Aggregator

A reusable Aggregator becomes a result-set procedure. The Mapping loads an input temp table, `CALL`s the procedure, and reads `RESULT_SCAN(LAST_QUERY_ID())`.

Snowflake (`AggregatorReusableSameFolder_EmitsSharedProcedureAndCallsIt`):

Copy code

```
CREATE OR REPLACE PROCEDURE public.Aggregator_SNOW_3702589_MyReuseAggr_2a2afb38 (source_table VARCHAR)
RETURNS TABLE (
  departmentcode VARCHAR(10),
  AvgSalaryPerDept NUMBER(18,6),
  MinRowId NUMBER(10,0)
)
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    res RESULTSET;
  BEGIN
    res := (WITH source_data AS
    (
      SELECT
        *
      FROM
        IDENTIFIER(:source_table)
    )
    SELECT
      departmentcode AS departmentcode,
      CAST(AVG(Salary) AS NUMBER(18,6)) AS AvgSalaryPerDept,
      CAST(MIN(SC_ROW_ID) AS NUMBER(10,0)) AS MinRowId
    FROM
      source_data
    GROUP BY
      departmentcode);
    RETURN TABLE(res);
  END;
$$;
```

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_aggregator_snow_3702589_myreuseaggr_2a2afb38_input AS
   SELECT
      DeptCode AS departmentcode,
      Salary,
      SC_ROW_ID
   FROM
      tmp_sq_sc_agg_reuse_emp;
CALL public.Aggregator_SNOW_3702589_MyReuseAggr_2a2afb38('tmp_aggregator_snow_3702589_myreuseaggr_2a2afb38_input');
CREATE OR REPLACE TEMPORARY TABLE tmp_aggregator_snow_3702589_myreuseaggr_2a2afb38_out AS
   SELECT
      departmentcode AS departmentcode,
      AvgSalaryPerDept AS AvgSalaryPerDept,
      MinRowId AS MinRowId
   FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()))
      ;
INSERT INTO YOUR_DB.YOUR_SCHEMA.SC_AGG_REUSE_TGT (DeptCode, AvgSalary, SC_ROW_ID)
SELECT
   sd.departmentcode AS DeptCode,
   sd.AvgSalaryPerDept AS AvgSalary,
   sd.MinRowId AS SC_ROW_ID
FROM
   tmp_aggregator_snow_3702589_myreuseaggr_2a2afb38_out AS sd
   ;
```

## Java Transformation

A Java Transformation (`TYPE="Custom Transformation"` with `TEMPLATENAME="Java Transformation"`) is converted as a pass-through CTE. Incoming columns are forwarded; the Java source is not applied. `SSC-FDM-INF0045` records that the Java logic must be migrated by hand (for example to a Java UDF or Snowpark procedure).

Informatica (`m_JavaTx_PurePass`):

Copy code

```
<TRANSFORMATION NAME="t_JavaPass" TYPE="Custom Transformation" TEMPLATENAME="Java Transformation">
   <!-- RecId, Label, Amount ports omitted -->
</TRANSFORMATION>
```

Snowflake (`InlineMode_JavaPurePassthrough_ForwardsValuesUnchangedDespiteJavaMutation`):

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.JTX_PASS_TGT (RecId, Label, Amount)
WITH
-- SSC-FDM-INF0045: Java transformation 't_JavaPass' contains custom Java
-- code that cannot be automatically translated. The following Java code
-- snippets must be manually migrated to Snowflake (e.g., Java UDF, Snowpark
-- procedure, or inline SQL). Pass-through columns are forwarded but the Java
-- logic is not applied.
--
-- TRANSFORMATION SCOPE: Row
--
-- --- IMPORT PACKAGES ---
-- import java.util.Locale;
--
-- --- ON INPUT ROW ---
-- // Modify values in place then forward the row.
-- if (Label != null) { Label = Label.toUpperCase(Locale.ROOT); }
-- Amount = Amount + 1;
-- generateRow();
cte_t_javapass AS
(
   SELECT
      RecId,
      Label,
      Amount
   FROM
      tmp_sq_jtx_pass_src
)
SELECT
   sd.RecId AS RecId,
   sd.Label AS Label,
   sd.Amount AS Amount
FROM
   cte_t_javapass AS sd
   ;
```

When the Java transformation is active, has output-only ports, uses Update Strategy (`setOutRowType`), or generates transactions, the converter stacks `SSC-EWI-INF0046` through `SSC-EWI-INF0049` on the same FDM. Output-only ports are projected as `NULL` until the Java logic is migrated:

Copy code

```
-- SSC-FDM-INF0045: Java transformation 't_JavaCombo' contains custom Java
-- code that cannot be automatically translated. The following Java code
-- snippets must be manually migrated to Snowflake (e.g., Java UDF, Snowpark
-- procedure, or inline SQL). Pass-through columns are forwarded but the Java
-- logic is not applied.
--
-- SSC-EWI-INF0046: Active Java transformation 't_JavaCombo' cannot be
-- automatically translated. The transformation may change row cardinality.
-- Manual migration to a Snowflake Java UDTF or Snowpark procedure is required.
--
-- SSC-EWI-INF0047: Output-only port 'FLAG_OUT' is set by Java code and cannot
-- be automatically translated. The port is projected as NULL until the Java
-- logic is manually migrated.
--
-- SSC-EWI-INF0048: Java transformation uses Update Strategy (setOutRowType).
-- Manual migration of the row-type logic is required.
--
-- SSC-EWI-INF0049: Java transformation generates transactions (commit/rollback).
-- Snowflake transaction semantics differ. Manual review is required.
--
-- TRANSFORMATION SCOPE: Transaction
--
-- --- ON INPUT ROW ---
-- generateRow();
-- setOutRowType(UPDATE);
-- commitTransaction();
-- FLAG_OUT = ITEM_ID;
cte_t_javacombo AS
(
   SELECT
      ITEM_ID,
      DESCR,
      null AS FLAG_OUT
   FROM
      tmp_sq_java_combo_src
)
```

Java **source** is not converted. Generate the Mapping in the [dbt output format](../dbt/mappings-and-transformations) if you need a different fallback shape, or migrate the Java by hand.

## Stored Procedure

A **connected Normal** Stored Procedure is not a Snowflake `CALL`. It becomes a per-row UDF CTE chain: `source_data` aliases the incoming ports, and `sp_result` invokes the procedure as a UDF and extracts named fields from the returned object. `SSC-EWI-INF0040` records that you must convert the Informatica procedure to a Snowflake UDF that returns `OBJECT_CONSTRUCT` with those field names.

Informatica (`m_sp_happy_path`):

Copy code

```
<TRANSFORMATION NAME="SP_CalcTax" TYPE="Stored Procedure">
   <TRANSFORMFIELD NAME="inSalary" PORTTYPE="INPUT"/>
   <TRANSFORMFIELD NAME="outTaxAmount" PORTTYPE="OUTPUT"/>
   <TRANSFORMFIELD NAME="RETURN_VALUE" PORTTYPE="RETURN/OUTPUT"/>
   <TABLEATTRIBUTE NAME="Stored Procedure Name" VALUE="dbo.sp_calc_tax"/>
   <TABLEATTRIBUTE NAME="Stored Procedure Type" VALUE="Normal"/>
</TRANSFORMATION>
```

Snowflake (`ConnectedNormalSp_HappyPath_EmitsUdfCallWithInf0040InSql`):

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
      tmp_sq_src_employees
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

A disconnected or midstream Stored Procedure still has no Scripting translator and emits the `SSC-EWI-INF0001` placeholder described in [Unsupported transformations](#unsupported-transformations). Convert those shapes in the [dbt output format](../dbt/mappings-and-transformations), or migrate the call by hand.

## A complete example

The following Mapping reads a source table, passes the columns through an Expression, and writes them to a target.

Informatica (`m_SimpleMapping`):

Copy code

```
<SOURCE NAME="SRC_TABLE" DATABASETYPE="Microsoft SQL Server" OWNERNAME="dbo">
   <!-- ID (primary key), NAME source fields omitted -->
</SOURCE>
<TARGET NAME="TGT_TABLE" DATABASETYPE="Microsoft SQL Server">
   <!-- ID (primary key), NAME target fields omitted -->
</TARGET>
<MAPPING NAME="m_SimpleMapping">
   <TRANSFORMATION NAME="SQ_SRC_TABLE" TYPE="Source Qualifier">
      <!-- ID, NAME ports omitted -->
   </TRANSFORMATION>
   <TRANSFORMATION NAME="EXP_Transform" TYPE="Expression">
      <TRANSFORMFIELD NAME="ID" PORTTYPE="INPUT/OUTPUT" EXPRESSION="ID"/>
      <TRANSFORMFIELD NAME="NAME" PORTTYPE="INPUT/OUTPUT" EXPRESSION="NAME"/>
   </TRANSFORMATION>
   <TRANSFORMATION NAME="TGT_TGT_TABLE" TYPE="Target Definition">
      <!-- ID, NAME input ports omitted -->
   </TRANSFORMATION>
   <!-- INSTANCE + CONNECTOR chain SRC_TABLE -> SQ_SRC_TABLE -> EXP_Transform -> TGT_TGT_TABLE omitted -->
</MAPPING>
<WORKFLOW NAME="WF_SimpleMapping">
   <SESSION NAME="s_m_SimpleMapping" MAPPINGNAME="m_SimpleMapping"/>
</WORKFLOW>
```

Snowflake:

Copy code

```
CREATE OR REPLACE PROCEDURE public.m_SimpleMapping (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      CREATE OR REPLACE TEMPORARY TABLE tmp_sq_src_table AS
         SELECT
            ID,
            NAME
         FROM
            YOUR_DB.dbo.SRC_TABLE;
      INSERT INTO YOUR_DB.YOUR_SCHEMA.TGT_TGT_TABLE
      WITH cte_exp_transform AS
      (
         WITH source_data AS
         (
            SELECT
               ID,
               NAME
            FROM
               tmp_sq_src_table
         )
         SELECT
            ID AS ID,
            NAME AS NAME
         FROM
            source_data
      )
      SELECT
         *
      FROM
         cte_exp_transform AS sd;
   END
$$;
```

The Workflow’s Task calls this procedure and forwards the scope:

Copy code

```
CALL public.m_SimpleMapping(:scope);
```

## Unsupported transformations

When a Mapping uses a transformation that the Snowflake Scripting format doesn’t convert, the data flow is kept connected by emitting a placeholder CTE. The placeholder selects `NULL` for each output port, includes the original transformation definition as comments, and is marked with `SSC-EWI-INF0001`. Transaction Control is one such transformation:

Informatica (`m_UnsupportedNode`):

Copy code

```
<TRANSFORMATION NAME="TC_Transform" TYPE="Transaction Control">
   <TRANSFORMFIELD NAME="ID" PORTTYPE="INPUT/OUTPUT"/>
   <TRANSFORMFIELD NAME="NAME" PORTTYPE="INPUT/OUTPUT"/>
   <TABLEATTRIBUTE NAME="Transaction Control Condition" VALUE="TC_CONTINUE_TRANSACTION"/>
</TRANSFORMATION>
```

Snowflake (`UnsupportedTransformation_MarkersRemainBalanced_AroundResolveEwiBlock`):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - INFORMATICA POWERCENTER TRANSFORMATION IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
cte_tc_transform AS
(
   -- Unsupported transformation 'TC_Transform' (UnsupportedTransformation) — no inline scripting translator registered for this type
   --
   --<TRANSFORMATION NAME="TC_Transform" TYPE="Transaction Control" ... >
   --  ...
   --</TRANSFORMATION>
   --
   SELECT
      null AS ID,
      null AS NAME
)
```

Downstream transformations still reference this CTE by name, so the rest of the procedure is generated normally. Convert the flagged transformation manually, or generate the Mapping in the [dbt output format](../dbt/mappings-and-transformations). Disconnected Stored Procedure, Java **source**, and multi-IO Mapplets also land here or in the [Mapplets](#mapplets) INF0001 note; connected Normal Stored Procedure and Java pass-through are documented above.
