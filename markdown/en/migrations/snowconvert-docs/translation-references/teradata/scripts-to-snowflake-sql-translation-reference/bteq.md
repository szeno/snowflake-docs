# Teradata - BTEQ

Translation references to convert Teradata BTEQ files to Snowflake SQL

## Description

Note

Some parts in the output code are omitted for clarity reasons.

> Basic Teradata Query (BTEQ) is a general-purpose, command-based program that enables users on a workstation to communicate with one or more Teradata Database systems and to format reports for both print and screen output.

For more information, see the [Teradata BTEQ Reference](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018).

### Sample Source Patterns

#### 1. Basic BTEQ Example

The BTEQ content is relocated within an `EXECUTE IMMEDIATE` block to transfer the BTEQ script functionality to Snowflake SQL executable code.

All the DML and DDL statements inside BTEQ scripts are supported and successfully translated to Snowflake SQL. The commands that do not have support yet, or do not have support at all, are being marked with a warning message and commented out.

##### Teradata BTEQ

Copy code

```
 -- Additional Params: -q SnowScript
.LOGON 0/dbc,dbc;
   DATABASE tduser;

   CREATE TABLE employee_bkup (
      EmployeeNo INTEGER,
      FirstName CHAR(30),
      LastName CHAR(30),
      DepartmentNo SMALLINT,
      NetPay INTEGER
   )
   Unique Primary Index(EmployeeNo);

   DROP TABLE employee_bkup;

   .IF ERRORCODE <> 0 THEN .EXIT ERRORCODE;
.LOGOFF;
```

##### Snowflake SQL

Copy code

```
 EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    --.LOGON 0/dbc,dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE tduser;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      CREATE OR REPLACE TABLE employee_bkup (
        EmployeeNo INTEGER,
        FirstName CHAR(30),
        LastName CHAR(30),
        DepartmentNo SMALLINT,
        NetPay INTEGER,
        UNIQUE (EmployeeNo)
      );
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DROP TABLE employee_bkup;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
    END IF;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

#### 2. Bash Variable Placeholders Example

Migration of BTEQ code with Bash Variable Placeholders used for shell scripts is supported. These placeholders are migrated to Snowflake CLI template syntax (`<%VAR%>`) and [SSC-FDM-TD0003](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003) is added to the code. Please consider the following when migrating code with these placeholders:

- Migration of shell scripts is **not** supported. To migrate the BTEQ code, isolate it in a BTEQ file and supply it as input for the tool.
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) is required to execute the migrated code. Variables are passed via `-D` flags: `snow sql -f script.sql -D "VAR=value"`. For more information, see [SSC-FDM-TD0003](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003).

##### Teradata BTEQ

Copy code

```
 -- Additional Params: -q SnowScript
.LOGON dbc, dbc;

DATABASE testing;

SELECT $columnVar FROM $tableVar WHERE col2 = $nameExprVar;
INSERT INTO $tableName values ('$myString', $numValue);
UPDATE $dbName.$tableName SET col1 = $myValue;
DELETE FROM $tableName;

.LOGOFF;
```

##### Snowflake SQL

Copy code

```
 EXECUTE IMMEDIATE
$$
  --** SSC-FDM-TD0003 - BASH VARIABLES FOUND, SNOWFLAKE CLI IS REQUIRED TO RUN THIS SCRIPT. USE: snow sql -f <script> -D "VAR=value" FOR EACH VARIABLE. **
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    --.LOGON dbc, dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE testing;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      SELECT
        <%columnVar%>
      FROM
        <%tableVar%>
      WHERE
        col2 = <%nameExprVar%>;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      INSERT INTO <%tableName%>
      VALUES ('<%myString%>', <%numValue%>);
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      UPDATE <%dbName%>.<%tableName%>
        SET
          col1 = <%myValue%>
        ;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DELETE FROM
        <%tableName%>;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

#### 3. `.IF`, `.GOTO`, and `.LABEL` (Snowflake Scripting)

When the BTEQ script target is **Snowflake Scripting** (SnowScript), **`.IF`**, **`.GOTO`**, and **`.LABEL`** are translated by modeling jumps as **nested procedure calls** and **early returns** inside a single **`EXECUTE IMMEDIATE`  … ``** block. Snowflake does not provide BTEQ-style goto/label semantics.

| BTEQ construct | Snowflake Scripting approach |
| --- | --- |
| Script body with labels | Wrapped in `EXECUTE IMMEDIATE`  … `` with `DECLARE`, nested procedures, and a top-level `BEGIN … END` |
| `.LABEL name` | Section `name` becomes a **nested procedure**; handoffs use `CALL name();` |
| `.GOTO name` | `CALL name();` followed by `RETURN 'PROCESS FINISHED';` |
| `.IF ERRORCODE …` | `IF (STATUS_OBJECT['SQLCODE'] …)` using a status object updated in `EXCEPTION` handlers |
| `.IF ACTIVITYCOUNT …` | `IF` on row count from `TABLE(RESULT_SCAN(LAST_QUERY_ID()))` |
| Error/status tracking | `STATUS_OBJECT` holds status fields; generated SQL may include **SSC-FDM-TD0013** (Snowflake `SQLCODE` is not the same as Teradata `ERRORCODE`) |

Expand

Show lessSee more

Note

To produce output in this form, set the Teradata/BTEQ **script output** to **Snowflake Scripting** (for example `-- Additional Params: -q SnowScript` in the samples below). Option names vary by interface; see the user guide for your product version.

The following example shows **`.IF ERRORCODE`** with **`.GOTO`** and **`.LABEL`**. Teradata BTEQ often branches on **`ERRORCODE`** after DDL and jumps to a labeled cleanup or next step.

##### Teradata BTEQ

Copy code

```
 -- Additional Params: -q SnowScript
DROP TABLE DP_DWEDW.TF035_PCOM_PROD_TRAT_SEL;
.IF ERRORCODE <> 0 THEN .GOTO CRIA_EXPRESS_1;
.LABEL CRIA_EXPRESS_1
DROP TABLE DP_DWEDW.TF035_DESCTO_EXPRESS;
.IF ERRORCODE <> 0 THEN .GOTO CRIA_EXPRESS_2;
.LABEL CRIA_EXPRESS_2
DROP TABLE DP_DWEDW.TF035_DEVOL_EXPRESS;
```

##### Snowflake SQL

Copy code

```
 EXECUTE IMMEDIATE
$$
  DECLARE
    SC_EXIT_CODE VARCHAR := 0;
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        DROP TABLE DP_DWEDW.TF035_PCOM_PROD_TRAT_SEL;
        IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
          CALL CRIA_EXPRESS_1();
          RETURN 'PROCESS FINISHED';
        END IF;
        CALL CRIA_EXPRESS_1();
      EXCEPTION
        WHEN OTHER CONTINUE THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
    CRIA_EXPRESS_1 PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        DROP TABLE DP_DWEDW.TF035_DESCTO_EXPRESS;
        IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
          CALL CRIA_EXPRESS_2();
          RETURN 'PROCESS FINISHED';
        END IF;
        CALL CRIA_EXPRESS_2();
      EXCEPTION
        WHEN OTHER CONTINUE THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
    CRIA_EXPRESS_2 PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        DROP TABLE DP_DWEDW.TF035_DEVOL_EXPRESS;
      EXCEPTION
        WHEN OTHER CONTINUE THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
  BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
  END
$$
;
```

After each statement that can set SQL state, the generated `IF` checks `STATUS_OBJECT['SQLCODE']`. On error, the script **calls** the target label procedure and **returns** from the current procedure so later statements in that section do not run. On success, it **calls** the next section’s procedure to continue the original linear flow.

The next example shows **`.IF ActivityCount = 0 THEN .GOTO …`**, expressed in Snowflake Scripting using the **last query id** and **`RESULT_SCAN`**.

##### Teradata BTEQ

Copy code

```
 -- Additional Params: -q SnowScript
.IF ActivityCount = 0 THEN .GOTO Continue_No_Rejects_00
DROP TABLE DROPTEDTABLE1;
.LABEL Continue_No_Rejects_00
SELECT A FROM AUDITORIA;
```

##### Snowflake SQL

Copy code

```
 EXECUTE IMMEDIATE
$$
  DECLARE
    SC_EXIT_CODE VARCHAR := 0;
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        IF ((SELECT
          COUNT(*)
        FROM
          TABLE(RESULT_SCAN(LAST_QUERY_ID()))) = 0) THEN
          CALL Continue_No_Rejects_00();
          RETURN 'PROCESS FINISHED';
        END IF;
        DROP TABLE DROPTEDTABLE1;
        CALL Continue_No_Rejects_00();
      EXCEPTION
        WHEN OTHER CONTINUE THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
    Continue_No_Rejects_00 PROCEDURE ()
    RETURNS VARCHAR
    AS
      BEGIN
        SELECT
          A
        FROM
          AUDITORIA;
      EXCEPTION
        WHEN OTHER CONTINUE THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
  BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
  END
$$
;
```

If **activity count is zero**, the generated script jumps to the label section with **`CALL Continue_No_Rejects_00()`** and **`RETURN 'PROCESS FINISHED'`**, skipping `DROP TABLE DROPTEDTABLE1`. Otherwise it runs `DROP TABLE`, then **calls** the label procedure to run `SELECT A FROM AUDITORIA`.

### Data Import (.IMPORT)

The BTEQ `.IMPORT` block (`.IMPORT VARTEXT|REPORT|FILE` paired with `.REPEAT` and a `USING` clause) is translated into a Snowflake `COPY INTO` statement or a staging-table + bulk DML pipeline, depending on the inner DML. A `CREATE TEMPORARY STAGE` and `PUT` are emitted at the top of the script so the file can be uploaded with the [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`).

| `.IMPORT` form | Inner DML | Snowflake output |
| --- | --- | --- |
| `VARTEXT` | `INSERT` | `COPY INTO target` |
| `VARTEXT` | `INSERT` + `.REPEAT n` | Staging table with `sc_seq` + sequenced `COPY INTO` + `INSERT … ORDER BY sc_seq LIMIT n` + `DROP TABLE` |
| `VARTEXT` | `UPDATE`, `DELETE`, `MERGE`, `SELECT` | Staging table built from the `USING` columns + bulk DML aliased `SRC` / `TGT` + `DROP TABLE` |
| `VARTEXT` | `EXEC` / `CALL` | Temporary `FILE FORMAT` + `LET … CURSOR FOR` + `FOR rec IN cursor DO … CALL proc(:col); END FOR` |
| `REPORT` / `FILE` (no format) | `INSERT` | `COPY INTO target` with `RTRIM(SUBSTRING($1, start, width))` per column |
| `REPORT` / `FILE` | `UPDATE`, `DELETE`, `MERGE`, `SELECT` | Same staging pattern as VARTEXT, with `RTRIM(SUBSTRING(...))` extraction in the load step |

Expand

Show lessSee more

#### 1. VARTEXT Format - `INSERT` (`COPY INTO`)

A single `INSERT … VALUES (:host, …)` over a delimited file is translated to a single `COPY INTO target` whose inner `SELECT` uses positional `$N` references to pick fields from the staged file. `:host` references that map to a `USING` column are rewritten to their corresponding position; literals and other expressions are kept as-is.

##### Teradata BTEQ

Copy code

```
.IMPORT VARTEXT ',' FILE = data.csv
.REPEAT *
USING (col1 VARCHAR(10), col2 VARCHAR(20))
INSERT INTO target_table VALUES (:col1, :col2);
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://data.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO target_table (
      col1,
      col2
    )
    FROM
    (
      SELECT
        $1,
        $2
      FROM
        @sc_import_stage/data.csv
    )
    FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
    ON_ERROR = 'CONTINUE';
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

If the `VALUES` list reorders the `USING` columns or interleaves literals (for example `VALUES (:col2, :col1, 'X')`), the `COPY INTO` source `SELECT` mirrors that order so each output position keeps its original semantics.

#### 2. VARTEXT Format - `INSERT` with `.REPEAT n` (Sequenced Staging)

When `.REPEAT` has a numeric limit (`.REPEAT 100`), BTEQ processes exactly that many rows. The translation uses a temporary staging table that captures the file row order through `METADATA$FILE_ROW_NUMBER` (column `sc_seq`), and then issues an `INSERT … SELECT … ORDER BY sc_seq LIMIT n` to reproduce the bounded behavior. The staging table is dropped after the insert.

##### Teradata BTEQ

Copy code

```
.IMPORT VARTEXT ',' FILE = data.csv
.REPEAT 100
USING (col1 VARCHAR(10), col2 VARCHAR(20))
INSERT INTO target (col1, col2) VALUES (:col1, :col2);
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://data.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    CREATE OR REPLACE TEMPORARY TABLE sc_import_staging (
      col1 VARCHAR(10),
      col2 VARCHAR(20),
      sc_seq INT
    );
    COPY INTO sc_import_staging (
      sc_seq,
      col1,
      col2
    )
    FROM
    (
      SELECT
        METADATA$FILE_ROW_NUMBER,
        $1,
        $2
      FROM
        @sc_import_stage/data.csv
    )
    FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
    ON_ERROR = 'CONTINUE';
    INSERT INTO target (col1, col2)
    SELECT
      col1,
      col2
    FROM
      sc_import_staging
    ORDER BY
      sc_seq
    LIMIT 100 ;
    DROP TABLE sc_import_staging;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 3. VARTEXT Format - `UPDATE` / `DELETE` / `MERGE` / `SELECT` (Staging + Bulk DML)

When the inner DML is `UPDATE`, `DELETE`, `MERGE`, or `SELECT`, the row-by-row Teradata pipeline is collapsed into a single bulk statement. The schema of the staging table is built from the `USING` clause (column names and CHAR / VARCHAR types are taken verbatim). The DML body is rewritten so that every `:host` becomes `SRC.<col>` and the target table is aliased `TGT`; the resulting statement runs once over the whole loaded file.

##### Teradata BTEQ

Copy code

```
.IMPORT VARTEXT ',' FILE = updates.csv
.REPEAT *
USING (key_col VARCHAR(20), new_value VARCHAR(50))
UPDATE target_table SET value_col = :new_value WHERE key_col = :key_col;
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://updates.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    CREATE OR REPLACE TEMPORARY TABLE sc_import_staging (
      key_col VARCHAR(20),
      new_value VARCHAR(50)
    );
    COPY INTO sc_import_staging (
      key_col,
      new_value
    )
    FROM
    (
      SELECT
        $1,
        $2
      FROM
        @sc_import_stage/updates.csv
    )
    FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
    ON_ERROR = 'CONTINUE';
    UPDATE target_table TGT
      SET
        value_col = SRC.new_value
      FROM
        sc_import_staging SRC
      WHERE
        TGT.key_col = SRC.key_col;
    DROP TABLE sc_import_staging;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

The same staging pattern is used for `DELETE` (emits `USING sc_import_staging SRC`), `MERGE` (replaces the source `(SELECT :host AS col …) s` derived table with `sc_import_staging SRC`, keeping the original source alias when present), and `SELECT` (appends `, sc_import_staging SRC` to the `FROM` clause).

#### 4. VARTEXT Format - `EXEC` / `CALL` (Cursor Loop)

When the inner statement is `EXEC` or `CALL`, the load is row-driven by design — each call invokes a procedure with one row’s values. A temporary `FILE FORMAT` is emitted, a Snowflake Scripting `CURSOR` is declared whose `SELECT` aliases each `$N` to the corresponding `USING` column name, and iteration occurs with `FOR rec IN sc_cursor DO … END FOR`. Because Snowflake’s `CALL` cannot accept `rec.colN` directly as an argument, each host-parameter argument is captured into a `LET` local and passed through `:bind` syntax. Literal arguments pass through unchanged.

##### Teradata BTEQ

Copy code

```
.IMPORT VARTEXT ',' FILE = inputs.csv
.REPEAT *
USING (CAMPAIGN_ID CHAR(9), EVENT_CD CHAR(9))
EXEC PROC_NAME (:CAMPAIGN_ID, :EVENT_CD);
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://inputs.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    CREATE OR REPLACE TEMPORARY FILE FORMAT sc_vartext_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 0;
    LET sc_cursor CURSOR
    FOR
      SELECT
        $1 AS CAMPAIGN_ID,
        $2 AS EVENT_CD
      FROM
        @sc_import_stage/inputs.csv (FILE_FORMAT => 'sc_vartext_format');
    FOR rec IN sc_cursor DO
      LET CAMPAIGN_ID VARCHAR := rec.CAMPAIGN_ID;
      LET EVENT_CD VARCHAR := rec.EVENT_CD;
      CALL PROC_NAME(:CAMPAIGN_ID, :EVENT_CD);
    END FOR;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 5. REPORT / FILE Format (Fixed-Width)

`.IMPORT REPORT` (and `.IMPORT FILE` with no format keyword) reads files as fixed-width records — each column occupies a fixed number of bytes given by the CHAR/VARCHAR width in the `USING` clause. The translation forces the entire input line into `$1` by setting `FIELD_DELIMITER = '\x7f'` (a delimiter that does not appear in normal text) and extracts each field with `RTRIM(SUBSTRING($1, start, width))`. The `RTRIM` matches BTEQ CHAR-equality semantics (trailing-space-insensitive) so that downstream `WHERE`, `JOIN`, and `MERGE`-`ON` predicates keep working against trimmed Snowflake `VARCHAR` values.

##### Teradata BTEQ

Copy code

```
.IMPORT REPORT FILE = report.txt
.REPEAT *
USING (name CHAR(20), amount CHAR(10))
INSERT INTO target_table VALUES (:name, :amount);
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://report.txt @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO target_table (
      name,
      amount
    )
    FROM
    (
      SELECT
        RTRIM(SUBSTRING($1, 1, 20)),
        RTRIM(SUBSTRING($1, 21, 10))
      FROM
        @sc_import_stage/report.txt
    )
    FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '\x7f')
    ON_ERROR = 'CONTINUE';
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

`UPDATE` / `DELETE` / `MERGE` / `SELECT` and `EXEC` / `CALL` paired with `.IMPORT REPORT` follow the same pipelines documented above for VARTEXT, with the load step replaced by the `RTRIM(SUBSTRING(...))` extraction shown here.

#### Unsupported `.IMPORT` Cases

Cases that cannot be reliably translated emit [SSC-EWI-TD0094](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0094) on the `.IMPORT` line with a case-specific reason. The trailing `.REPEAT` / `USING` / DML body is preserved in the output, commented out under [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073), so the user can still see the original code and rewrite it manually. No `CREATE TEMPORARY STAGE`, `PUT`, or `COPY INTO` is emitted for the unsupported file. The cases are:

- `.IMPORT DATA` — Teradata’s binary client format has no Snowflake equivalent.
- `.IMPORT INDICDATA` — Teradata’s binary indicator-bytes format.
- `.IMPORT DDNAME = …` — z/OS JCL DD card reference.
- Dynamic `USING` clause (column name templated with a bash variable, e.g. `USING (${COL_NAME} VARCHAR(10))`) — the layout is not known at conversion time.

When `.IMPORT … FILE = ${VAR}` references a file path that is a single bash variable, [SSC-EWI-TD0096](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0096) is added to the `COPY INTO` stage reference because the basename cannot be inferred. When the directory portion is variable but the filename is a literal (`FILE = ${DIR}/data.csv`), the basename is known and no EWI is emitted.

### Data Export (.EXPORT)

The BTEQ `.EXPORT` block (`.EXPORT REPORT|DATA|FILE=` paired with a `SELECT` and terminated by `.EXPORT RESET`) is translated into Snowflake’s unload-form `COPY INTO @stage` followed by a `GET` that downloads the file with the [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`). A `CREATE TEMPORARY STAGE` is emitted once at the top of the script and shared across every `.EXPORT` block.

| `.EXPORT` form | `FIELD_DELIMITER` | `HEADER` | Notes |
| --- | --- | --- | --- |
| `REPORT FILE=` | `'|'` | `TRUE` | Default for an explicit `REPORT` keyword. |
| `FILE=` (no format) | `'|'` | `TRUE` | `.EXPORT FILE=` without a format keyword defaults to `REPORT`. |
| `DATA FILE=` | `'|'` | `FALSE` | Teradata binary format is rendered as Snowflake CSV without headers. |
| `… , LIMIT = n` | (as above) | (as above) | The bound `SELECT` is wrapped with `LIMIT n`. |
| `.SET SEPARATOR 'x'` + `REPORT` | `'x'` | `TRUE` | The active `.SET SEPARATOR` value overrides the default delimiter. |
| Single computed column (concatenation, function call, etc.) | `NONE` | `FALSE` | The expression already produces the entire output line, so no extra delimiter or header is inserted. |
| `.EXPORT RESET` | — | — | Dropped from the output (no Snowflake equivalent). |

Expand

Show lessSee more

`PUT` and `GET` cannot run inside Snowflake Scripting blocks, so the `GET` is emitted at the top level after the `EXECUTE IMMEDIATE` block and is annotated with [SSC-FDM-TD0038](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0038).

#### 1. `.EXPORT REPORT FILE=` (explicit REPORT)

A multi-column `SELECT` becomes a `COPY INTO @sc_export_stage/<file>` with the default pipe delimiter and a header row.

##### Teradata BTEQ

Copy code

```
.EXPORT REPORT FILE=report.txt
SELECT col1, col2, col3 FROM source_table;
.EXPORT RESET
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO @sc_export_stage/report.txt
    FROM
    (
      SELECT
        col1,
        col2,
        col3
      FROM
        source_table
    )
    FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = '|' FIELD_OPTIONALLY_ENCLOSED_BY = NONE RECORD_DELIMITER = '\n')
    HEADER = TRUE
    SINGLE = TRUE
    OVERWRITE = TRUE;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$

--** SSC-FDM-TD0038 - GET COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
GET @sc_export_stage/report.txt file://./;
```

#### 2. `.EXPORT FILE=` (no format keyword)

When no format keyword is present, BTEQ defaults to `REPORT`. The conversion is identical to the explicit `REPORT` case.

##### Teradata BTEQ

Copy code

```
.EXPORT FILE=extract.txt
SELECT emp_id, emp_name FROM employees;
.EXPORT RESET
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO @sc_export_stage/extract.txt
    FROM
    (
      SELECT
        emp_id,
        emp_name
      FROM
        employees
    )
    FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = '|' FIELD_OPTIONALLY_ENCLOSED_BY = NONE RECORD_DELIMITER = '\n')
    HEADER = TRUE
    SINGLE = TRUE
    OVERWRITE = TRUE;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$

--** SSC-FDM-TD0038 - GET COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
GET @sc_export_stage/extract.txt file://./;
```

#### 3. `.EXPORT DATA FILE=` (binary → CSV)

Teradata’s binary `DATA` format has no Snowflake equivalent. The conversion writes the staged file as CSV without a header row.

##### Teradata BTEQ

Copy code

```
.EXPORT DATA FILE=output.dat
SELECT col1, col2 FROM source_table;
.EXPORT RESET
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO @sc_export_stage/output.dat
    FROM
    (
      SELECT
        col1,
        col2
      FROM
        source_table
    )
    FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = '|' FIELD_OPTIONALLY_ENCLOSED_BY = NONE RECORD_DELIMITER = '\n')
    HEADER = FALSE
    SINGLE = TRUE
    OVERWRITE = TRUE;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$

--** SSC-FDM-TD0038 - GET COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
GET @sc_export_stage/output.dat file://./;
```

#### 4. `.SET SEPARATOR` overrides `FIELD_DELIMITER`

A `.SET SEPARATOR 'x'` statement before an `.EXPORT REPORT` block sets the active separator for every subsequent `.EXPORT` until another `.SET SEPARATOR` (session-sticky behavior). The conversion uses the captured separator as the `FIELD_DELIMITER` and drops the `.SET SEPARATOR` statement from the output.

##### Teradata BTEQ

Copy code

```
.SET SEPARATOR ';'
.EXPORT REPORT FILE=output.csv
SELECT col1, col2 FROM source_table;
.EXPORT RESET
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO @sc_export_stage/output.csv
    FROM
    (
      SELECT
        col1,
        col2
      FROM
        source_table
    )
    FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = ';' FIELD_OPTIONALLY_ENCLOSED_BY = NONE RECORD_DELIMITER = '\n')
    HEADER = TRUE
    SINGLE = TRUE
    OVERWRITE = TRUE;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$

--** SSC-FDM-TD0038 - GET COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
GET @sc_export_stage/output.csv file://./;
```

#### 5. Single computed column (`FIELD_DELIMITER = NONE`)

When the bound `SELECT` projects exactly one computed expression — typically a string concatenation or function call — the expression already produces the entire output line. The conversion emits `FIELD_DELIMITER = NONE` and `HEADER = FALSE` so Snowflake does not insert an extra delimiter or column-name header. The output is byte-identical to BTEQ’s `REPORT` for this shape.

##### Teradata BTEQ

Copy code

```
.EXPORT REPORT FILE=privileged_status.txt
SELECT TRIM(USERNAME) || '|' || TRIM(DATABASENAME) AS PRIVILEGED_STATUS FROM ACCESS_TYPES;
.EXPORT RESET
```

##### Snowflake SQL

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0) /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  BEGIN
    COPY INTO @sc_export_stage/privileged_status.txt
    FROM
    (
      SELECT
        TRIM(USERNAME) || '|' || TRIM(DATABASENAME) AS PRIVILEGED_STATUS
      FROM
        ACCESS_TYPES
    )
    FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = NONE FIELD_OPTIONALLY_ENCLOSED_BY = NONE RECORD_DELIMITER = '\n')
    HEADER = FALSE
    SINGLE = TRUE
    OVERWRITE = TRUE;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$

--** SSC-FDM-TD0038 - GET COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
GET @sc_export_stage/privileged_status.txt file://./;
```

#### 6. BTEQ output-formatting commands (`.SET WIDTH`, `.SET TITLEDASHES`, …)

BTEQ output-formatting commands (`.SET WIDTH`, `.SET TITLEDASHES`, `.SET TITLES`, `.SET SIDETITLES`, `.SET RTITLE`) commonly surround real `.EXPORT` blocks in customer scripts. They have no Snowflake equivalent and are commented out in the output under [SSC-FDM-TD0100](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0100) so the user can audit what was removed.

#### Unsupported `.EXPORT` Cases

Cases that cannot be reliably translated emit [SSC-EWI-TD0099](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0099) on the `.EXPORT` line with the variant token (`INDICDATA`, `DIF`, or `DDNAME`). The bound `SELECT` is preserved and no `CREATE TEMPORARY STAGE`, `COPY INTO`, or `GET` is emitted for the unsupported export. The cases are:

- `.EXPORT INDICDATA` — Teradata’s binary indicator-bytes format.
- `.EXPORT DIF` — Legacy Data Interchange Format (spreadsheet-oriented).
- `.EXPORT … DDNAME = …` — z/OS JCL DD card reference (mainframe-only).

### File Inclusion (.RUN FILE)

The BTEQ [`.RUN FILE = <path>`](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018) command is translated into Snowflake’s [`EXECUTE IMMEDIATE FROM @<stage>/<file>`](https://docs.snowflake.com/en/sql-reference/sql/execute-immediate-from), which loads and runs a SQL file from a Snowflake stage in the same session. A `CREATE STAGE IF NOT EXISTS sc_run_stage` and a `PUT` are emitted at the top of the converted parent script so that the referenced file is uploaded to the stage with the [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`) before the parent’s `EXECUTE IMMEDIATE FROM` runs. The referenced child script is also converted in the same migration run; the `EXECUTE IMMEDIATE FROM` invocation points at the converted output (e.g. `child.bteq` → `child_BTEQ.sql`).

| `.RUN` form | Snowflake output | Marker |
| --- | --- | --- |
| `.RUN FILE = child.bteq` (target present in input) | `CREATE STAGE` + `PUT` + `EXECUTE IMMEDIATE FROM @sc_run_stage/child_BTEQ.sql` | [SSC-FDM-TD0048](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0048) |
| `.RUN FILE = $LOGON_ID` (logon credentials) | `.RUN` line dropped from execution | [SSC-FDM-TD0049](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0049) |
| `.RUN FILE = child.bteq` (child also issues `.RUN`) | Same as resolved, plus chain warning | [SSC-FDM-TD0050](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0050) |
| `.RUN FILE = script.sql, SKIP = n` | Commented out, no stage/PUT | [SSC-EWI-TD0100](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0100) |
| `.RUN FILE = X` paired with `.EXPORT FILE = X` (checkpoint) | Commented out, no stage/PUT | [SSC-EWI-TD0101](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0101) |
| `.RUN FILE = missing.sql` (file absent from input or unresolvable variable) | Commented out, no stage/PUT | [SSC-EWI-TD0103](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0103) |

Expand

Show lessSee more

`PUT` cannot run inside Snowflake Scripting blocks, so the `PUT` is emitted at the top level before the parent’s `EXECUTE IMMEDIATE` block and is annotated with [SSC-FDM-TD0038](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0038).

#### 1. Resolved `.RUN FILE = <child>` (target present in input)

The happy path: the referenced file is found in the migration input tree (matched by basename). The stage + PUT prelude is emitted and the `.RUN` line is rewritten to `EXECUTE IMMEDIATE FROM @sc_run_stage/<basename>_BTEQ.sql`. The conversion supports `.bteq`, `.btq`, and `.sql` source extensions; the converted output uses the `_BTEQ.sql` suffix (consistent with the BTEQ-target naming convention).

##### Teradata BTEQ

Copy code

```
DATABASE mydb;
.RUN FILE = child.bteq
SELECT * FROM mytable;
```

##### Snowflake SQL

Copy code

```
CREATE STAGE IF NOT EXISTS sc_run_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://child_BTEQ.sql @sc_run_stage AUTO_COMPRESS = FALSE OVERWRITE = TRUE;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    USE DATABASE mydb;
    --** SSC-FDM-TD0048 - .RUN FILE CONVERTED TO EXECUTE IMMEDIATE FROM. **
    EXECUTE IMMEDIATE FROM @sc_run_stage/child_BTEQ.sql;
    SELECT
      *
    FROM
      mytable;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 2. Logon-credentials `.RUN FILE` (Snowflake CLI handles auth)

Some BTEQ scripts source a credential file before connecting (`.RUN FILE = $LOGON_ID`, `.RUN FILE = ${LOGIN_SCRIPT}`, etc.). Snowflake configures authentication outside SQL via `snow connection`, so the `.RUN` line has no Snowflake equivalent and is dropped from the executable output under [SSC-FDM-TD0049](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0049).

##### Teradata BTEQ

Copy code

```
.RUN FILE = $LOGON_ID
```

##### Snowflake SQL

Copy code

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    --** SSC-FDM-TD0049 - LOGON IS NOT REQUIRED WHEN RUNNING THROUGH SNOWFLAKE CLI. THE CONNECTION IS CONFIGURED VIA snow connection. **

--    .RUN FILE = $LOGON_ID
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 3. Chained `.RUN` (child also issues `.RUN`)

When a `.RUN` target itself contains `.RUN FILE` commands, BTEQ produces a flat chain; Snowflake’s `EXECUTE IMMEDIATE FROM` produces nested execution instead. The data end state matches, but transaction scope and error propagation differ. The parent is flagged with [SSC-FDM-TD0050](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0050) so the reviewer can confirm the nested behaviour is acceptable. The conversion still produces the resolved-shape output (stage + PUT + `EXECUTE IMMEDIATE FROM`).

##### Teradata BTEQ

Copy code

```
.RUN FILE = middle_chain.bteq
```

`middle_chain.bteq` itself contains `.RUN FILE = leaf_chain.bteq`.

##### Snowflake SQL

Copy code

```
CREATE STAGE IF NOT EXISTS sc_run_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://middle_chain_BTEQ.sql @sc_run_stage AUTO_COMPRESS = FALSE OVERWRITE = TRUE;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    --** SSC-FDM-TD0048 - .RUN FILE CONVERTED TO EXECUTE IMMEDIATE FROM. **
    !!!RESOLVE EWI!!! /*** SSC-FDM-TD0050 - .RUN CHAINING DETECTED. THE CHILD SCRIPT ITSELF ISSUES .RUN; EXECUTE IMMEDIATE FROM NESTS INSTEAD OF CHAINING. REVIEW EXECUTION ORDER. ***/!!!
    EXECUTE IMMEDIATE FROM @sc_run_stage/middle_chain_BTEQ.sql;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 4. `.RUN … SKIP = n` (no Snowflake equivalent)

`EXECUTE IMMEDIATE FROM` loads the entire stage file as a single SQL unit and offers no way to skip leading records. The `.RUN` line is commented out under [SSC-EWI-TD0100](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0100); no stage or PUT is emitted.

##### Teradata BTEQ

Copy code

```
.RUN FILE = script.sql, SKIP = 4
```

##### Snowflake SQL

Copy code

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-TD0100 - .RUN SKIP= NOT SUPPORTED. EXECUTE IMMEDIATE FROM HAS NO SKIP EQUIVALENT. ***/!!!

--    .RUN FILE = script.sql, SKIP = 4
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### 5. `.RUN` reading a sibling `.EXPORT` (checkpoint round-trip)

`EXECUTE IMMEDIATE FROM` reads from the stage copy of the file uploaded with `PUT` *before* the script started. A write performed by `.EXPORT` earlier in the same session is invisible to a subsequent `.RUN` of the same path. The path collision is detected and [SSC-EWI-TD0101](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0101) is emitted on the `.RUN`; the unrelated `.EXPORT` converts on its own.

##### Teradata BTEQ

Copy code

```
.EXPORT INDICDATA FILE = checkpoint.dat
SELECT col1 FROM source_table;
.RUN FILE = checkpoint.dat
```

##### Snowflake SQL

Copy code

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-TD0099 - PENDING SNOWCONVERT AI TRANSLATION FOR THE .EXPORT INDICDATA VARIANT. ***/!!!

--    .EXPORT INDICDATA FILE = checkpoint.dat
    SELECT
      col1
    FROM
      source_table;
    !!!RESOLVE EWI!!! /*** SSC-EWI-TD0101 - .RUN AND .EXPORT REFERENCE THE SAME FILE. EXECUTE IMMEDIATE FROM CANNOT READ A FILE WRITTEN EARLIER IN THE SAME SESSION. ***/!!!

--    .RUN FILE = checkpoint.dat
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

#### Unsupported `.RUN` Cases

Cases that cannot be reliably translated emit [SSC-EWI-TD0103](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0103) on the `.RUN` line. The line is commented out and no `CREATE STAGE` or `PUT` is emitted. The cases are:

- `.RUN FILE = <name>` where the target file is **not present in the migration input tree**.
- `.RUN FILE = $VAR` / `${VAR}` / `<% VAR %>` where the path contains a substitution variable that cannot be resolved (logon-shaped variables are intercepted by [SSC-FDM-TD0049](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0049) instead).
- `.RUN FILE = ''` — empty filename.

### Known Issues

1. **There may be BTEQ commands that do not have an equivalent in Snowflake SQL**

Since BTEQ is a command-based program, there may be some commands in your input code that do not have a hundred percent functional equivalence in Snowflake SQL. Those particular cases are identified, marked with warnings in the output code, and documented in the further pages.

### Related EWIs

1. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-FDM-TD0003](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003): Bash variable found, Snowflake CLI is required to run this script.
3. [SSC-FDM-TD0013](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0013): The Snowflake error code mismatches the original Teradata error code.
4. [SSC-EWI-TD0094](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0094): The IMPORT command was not converted.
5. [SSC-EWI-TD0096](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0096): COPY INTO requires an explicit target file name.
6. [SSC-EWI-TD0099](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0099): Pending translation for the .EXPORT command variant.
7. [SSC-EWI-TD0100](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0100): .RUN SKIP= not supported.
8. [SSC-EWI-TD0101](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0101): .RUN checkpoint file not supported.
9. [SSC-EWI-TD0103](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0103): .RUN file not found in source.
10. [SSC-FDM-TD0038](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0038): PUT/GET command requires execution through Snowflake CLI.
11. [SSC-FDM-TD0048](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0048): .RUN FILE converted to EXECUTE IMMEDIATE FROM.
12. [SSC-FDM-TD0049](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0049): Logon credentials not required when running through Snowflake CLI.
13. [SSC-FDM-TD0050](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0050): .RUN chaining detected.
14. [SSC-FDM-TD0100](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0100): BTEQ output-formatting setting has no Snowflake equivalent.
