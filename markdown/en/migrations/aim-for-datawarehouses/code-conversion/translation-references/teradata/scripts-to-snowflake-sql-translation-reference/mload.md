# Teradata - MLOAD

Translation references to convert Teradata MLOAD files to Snowflake Scripting.

## Description

The [Teradata MultiLoad (MLoad)](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Using-Teradata-MultiLoad) utility is designed for efficient batch maintenance of large databases, offering a command-driven approach for fast, high-volume data loading operations.

MLoad scripts are translated into Snowflake Scripting using the [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) command with staged files.

### Translation Structure

The generated output is organized into two distinct sections due to Snowflake’s execution model:

**1. Stage and file upload (outside EXECUTE IMMEDIATE)**

The [`CREATE TEMPORARY STAGE`](https://docs.snowflake.com/en/sql-reference/sql/create-stage) and [`PUT`](https://docs.snowflake.com/en/sql-reference/sql/put) commands are placed **before** the `EXECUTE IMMEDIATE` block.

**Why?** The `PUT` command is a **client-side** operation—it transfers files from your local machine to a Snowflake stage. This file transfer happens on your machine, not on the Snowflake server. As a result, `PUT` can only run through [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`) and cannot execute inside stored procedures, `EXECUTE IMMEDIATE` blocks, or the Snowflake web UI.

**2. Data loading (inside EXECUTE IMMEDIATE)**

The [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) statement and any additional logic are wrapped in an `EXECUTE IMMEDIATE` block with exception handling. This separation ensures the file upload completes first, and then the server-side data loading runs with proper error handling.

## Supported Commands

### .LOGTABLE

The [`.LOGTABLE`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/LOGTABLE) command stores checkpoint and restart information for MLoad sessions. Snowflake manages checkpointing internally, so this command is removed.

Since MLoad’s `IMPORT` command is translated to Snowflake’s `COPY INTO` statement, you can use the [`COPY_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/copy_history) table function to monitor and track your data loading operations. This function queries the loading history for a specified table within the last 14 days, returning details such as file names, load times, row counts, error messages, and statuses. For longer retention (up to 365 days), use the [`COPY_HISTORY` view](https://docs.snowflake.com/en/sql-reference/account-usage/copy_history) in the Account Usage schema.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LOGTABLE ${DATABASE}.LT_EMPLOYEES;
```

##### Snowflake Scripting

Copy code

```
--** SSC-FDM-TD0037 - REMOVED NEXT STATEMENT. USE COPY_HISTORY() FOR MONITORING **
-- .LOGTABLE ${DATABASE}.LT_EMPLOYEES;
```

### .SET Variables

The [`.SET`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/SET) command defines variables referenced with `&VARIABLE` throughout the script. These are translated to Snowflake Scripting variables using `DECLARE`.

#### Type Inference

Snowflake automatically infers the variable type from the assigned value, so explicit type declarations are **not required** in most cases. However, when the value involves **concatenation** (using the `||` operator), the `STRING` type must be explicitly declared.

| MLoad Source | Snowflake Translation |
| --- | --- |
| `.SET YEAR_VAL TO 2024;` | `YEAR_VAL := 2024;` |
| `.SET TBL TO 'MY_TABLE';` | `TBL STRING := 'MY_TABLE';` |
| `.SET DB_ALIAS TO &SRC_DB;` | `DB_ALIAS := :SRC_DB;` |
| `.SET KEY TO &A.&B;` | `KEY STRING := :A || :B;` |
| `.SET NAME TO 'ET_&TBL';` | `NAME STRING := 'ET_' || :TBL;` |

Expand

Show lessSee more

#### Bind Variables

Since the `.SET` command is translated to `DECLARE` variables in Snowflake Scripting, these variables must be referenced using [bind variable syntax](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#using-a-variable-in-a-sql-statement-binding) when used within SQL statements. This is done by prefixing the variable name with a colon (`:`), which allows for dynamic substitution of values at execution time.

##### Teradata MLoad

Copy code

```
INSERT INTO my_table VALUES (&my_variable, &another_var);
```

##### Snowflake Scripting

Copy code

```
INSERT INTO my_table (column1, column2) VALUES (:my_variable, :another_var);
```

#### Using Variables as Object Identifiers

When a variable represents the name of a database object (table, schema, etc.), the [`IDENTIFIER`](https://docs.snowflake.com/en/sql-reference/identifier-literal) function must be used. This function tells Snowflake to interpret the variable’s value as an object identifier rather than a string literal. The function ensures the variable is treated strictly as an identifier, reducing security risks.

**Important:** The `IDENTIFIER()` function does not support concatenation expressions directly. You cannot write `IDENTIFIER(:schema || '.' || :table)`. To handle concatenated object names, an intermediate variable with the `sc_` prefix (SnowConvert) is generated to hold the pre-computed concatenation result.

##### Teradata MLoad

Copy code

```
.SET table_name TO 'EMPLOYEES';
.SET schema_name TO 'HR';

SELECT * FROM &table_name;
DROP TABLE &schema_name..&table_name;
```

##### Snowflake Scripting

Copy code

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    table_name STRING := 'EMPLOYEES';
    schema_name STRING := 'HR';
    sc_schema_name_dot_table_name STRING := :schema_name || '.' || :table_name;
  BEGIN
    SELECT
      *
    FROM
      IDENTIFIER(:table_name);
    DROP TABLE IDENTIFIER(:sc_schema_name_dot_table_name);
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$;
```

#### Variable Concatenation

MLoad supports concatenating variables using the dot (`.`) operator. A single dot joins values directly, while a double dot inserts a literal dot separator:

| MLoad Pattern | Result | Snowflake Translation |
| --- | --- | --- |
| `&DB.&TBL` | `DBTBL` | `:DB || :TBL` |
| `&DB..&TBL` | `DB.TBL` | `:DB || '.' || :TBL` |
| `&A..&B.&C` | `A.BC` | `:A || '.' || :B || :C` |

Expand

Show lessSee more

When concatenation is used within a string literal, embedded variables are extracted and concatenated:

| MLoad Pattern | Snowflake Translation |
| --- | --- |
| `'ET_&TABLE_NAME'` | `'ET_' || :TABLE_NAME` |
| `'sales_&COUNTRY_CODE'` | `'sales_' || :COUNTRY_CODE` |
| `'&SRC_DB..&TARGET'` | `:SRC_DB || '.' || :TARGET` |

Expand

Show lessSee more

#### Variable Reassignment

When a variable is reassigned after its initial declaration, the reassignment is placed inside the `BEGIN` block.

##### Teradata MLoad

Copy code

```
.SET TBL TO 'TABLE1';
.SET TBL TO 'TABLE2';
```

##### Snowflake Scripting

Copy code

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    TBL STRING := 'TABLE1';
  BEGIN
    TBL := 'TABLE2';
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$;
```

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.SET DB_NAME TO '${DATABASE}';
.SET TABLE_NAME TO '${TABLE}';
.SET ERROR_TABLE TO 'ET_&TABLE_NAME';

DROP TABLE &DB_NAME..&ERROR_TABLE;
```

##### Snowflake Scripting

Copy code

```
EXECUTE IMMEDIATE
$$
  --** SSC-FDM-TD0003 - BASH VARIABLES FOUND, SNOWFLAKE CLI IS REQUIRED TO RUN THIS SCRIPT. USE: snow sql -f <script> -D "VAR=value" FOR EACH VARIABLE. **
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    DB_NAME STRING := '&{DATABASE}';
    TABLE_NAME STRING := '&{TABLE}';
    ERROR_TABLE STRING := 'ET_' || :TABLE_NAME;
    sc_DB_NAME_dot_ERROR_TABLE STRING := :DB_NAME || '.' || :ERROR_TABLE;
  BEGIN
    DROP TABLE IDENTIFIER(:sc_DB_NAME_dot_ERROR_TABLE);
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

### .BEGIN IMPORT MLOAD / .END MLOAD

These commands define the scope of an MLoad import operation. They are removed because Snowflake’s `COPY INTO` command is atomic and handles scope internally.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.BEGIN IMPORT MLOAD TABLES &DB_NAME..&TABLE_NAME
    WORKTABLES &DB_NAME..&WORK_TABLE
    ERRORTABLES &DB_NAME..&ERROR_TABLE
    CHECKPOINT 2000000;
...
.END MLOAD;
```

##### Snowflake Scripting

Copy code

```
--** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- .BEGIN IMPORT MLOAD TABLES &DB_NAME..&TABLE_NAME WORKTABLES ...
...
--** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- .END MLOAD;
```

### .LOGOFF

The `.LOGOFF` command terminates the MLoad session. This is not applicable in Snowflake and is removed from the output.

## Data Import Translation

### VARTEXT Format (Delimited Files)

The `VARTEXT` format loads delimited files. If no delimiter is specified, the default is pipe (`|`).

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LAYOUT employee_layout;
.FIELD employee_id * CHAR(10);
.FIELD first_name * CHAR(50);
.FIELD last_name * CHAR(50);
.FIELD department * CHAR(30);
.FIELD salary * CHAR(15);

.DML LABEL insert_employees;
INSERT INTO &DB_NAME..&TABLE_NAME (
    employee_id,
    first_name,
    last_name,
    department,
    salary
) VALUES (
    :employee_id,
    :first_name,
    :last_name,
    :department,
    :salary
);

.IMPORT INFILE ${DATA_DIR}/${FILE_NAME}
    FROM 1
    FORMAT VARTEXT '|'
    LAYOUT employee_layout
    APPLY insert_employees;
```

##### Snowflake Scripting

Copy code

```
--** SSC-FDM-TD0003 - BASH VARIABLES FOUND, SNOWFLAKE CLI IS REQUIRED TO RUN THIS SCRIPT. USE: snow sql -f <script> -D "VAR=value" FOR EACH VARIABLE. **
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://&{DATA_DIR}/&{FILE_NAME} @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    DB_NAME STRING := '&{DATABASE}';
    TABLE_NAME STRING := '&{TABLE}';
    sc_DB_NAME_dot_TABLE_NAME STRING := :DB_NAME || '.' || :TABLE_NAME;
  BEGIN
    BEGIN
      COPY INTO IDENTIFIER(:sc_DB_NAME_dot_TABLE_NAME) (
        employee_id,
        first_name,
        last_name,
        department,
        salary
      )
      FROM
      (
        SELECT
          $1,
          $2,
          $3,
          $4,
          $5
        FROM
          @sc_import_stage/&{FILE_NAME}
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|')
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

### TEXT/UNFORMAT Format (Fixed-Width Files)

The `TEXT` and `UNFORMAT` formats load fixed-width files. Field positions can use:

- **Asterisk (`*`)**: Automatic position calculation based on field length
- **Explicit number**: Specific byte position in the record

Fields are extracted using the `SUBSTRING` function.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LAYOUT employee_fixed_layout;
.FIELD employee_id 1 CHAR(10);
.FIELD first_name 11 CHAR(30);
.FILLER filler1 41 CHAR(20);
.FIELD last_name 61 CHAR(30);
.FILLER filler2 91 CHAR(20);
.FIELD department 111 CHAR(30);
.FIELD salary 141 CHAR(15);

.DML LABEL insert_employees;
INSERT INTO employees (employee_id, first_name, last_name, department, salary)
VALUES (:employee_id, :first_name, :last_name, :department, :salary);

.IMPORT INFILE employees.txt FORMAT TEXT LAYOUT employee_fixed_layout APPLY insert_employees;
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://employees.txt @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      COPY INTO employees (
        employee_id,
        first_name,
        last_name,
        department,
        salary
      )
      FROM
      (
        SELECT
          SUBSTRING($1, 1, 10),
          SUBSTRING($1, 11, 30),
          SUBSTRING($1, 61, 30),
          SUBSTRING($1, 111, 30),
          SUBSTRING($1, 141, 15)
        FROM
          @sc_import_stage/employees.txt
      )
      FILE_FORMAT = (TYPE = CSV)
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

Note

`.FILLER` fields are excluded from the `SELECT` statement.

## Field Options

### Trim Options

The `.FIELD` command supports options for trimming data:

| MLoad Option | Snowflake Function |
| --- | --- |
| `DROP LEADING BLANKS` | `LTRIM($n)` |
| `DROP TRAILING NULLS` | `RTRIM($n)` |
| `DROP LEADING BLANKS AND TRAILING NULLS` | `TRIM($n)` |

Expand

Show lessSee more

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LAYOUT employee_layout;
.FIELD first_name * VARCHAR(50) DROP LEADING BLANKS;
.FIELD last_name * VARCHAR(50) DROP TRAILING NULLS;
.FIELD department * VARCHAR(30) DROP LEADING BLANKS AND TRAILING NULLS;

.DML LABEL insert_employees;
INSERT INTO employees (first_name, last_name, department)
VALUES (:first_name, :last_name, :department);

.IMPORT INFILE employees.csv
    FORMAT VARTEXT ','
    LAYOUT employee_layout
    APPLY insert_employees;
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://employees.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      COPY INTO employees (
        first_name,
        last_name,
        department
      )
      FROM
      (
        SELECT
          LTRIM($1),
          RTRIM($2),
          TRIM($3)
        FROM
          @sc_import_stage/employees.csv
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

## Import Options

### FROM Clause (Skip Rows)

The `FROM n` clause specifies to start reading from row `n`. This translates to `SKIP_HEADER = n - 1`.

| MLoad | Snowflake |
| --- | --- |
| `FROM 1` | `SKIP_HEADER = 0` |
| `FROM 2` | `SKIP_HEADER = 1` |
| `FROM 5` | `SKIP_HEADER = 4` |

Expand

Show lessSee more

### WHERE Condition

The `WHERE` clause filters records during import. Since Snowflake’s [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) only supports `SELECT ... FROM ...` queries (without `WHERE`), the translation uses a **staging table pattern**:

1. Create a temporary staging table with the same structure as the target table
2. Load all data into the staging table using `COPY INTO`
3. Insert filtered records from the staging table into the target table using `INSERT INTO ... SELECT ... WHERE`
4. Drop the staging table

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LAYOUT employee_layout;
.FIELD employee_id * VARCHAR(10);
.FIELD first_name * VARCHAR(50);
.FIELD last_name * VARCHAR(50);
.FIELD department * VARCHAR(30);

.DML LABEL insert_employees;
INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (:employee_id, :first_name, :last_name, :department);

.IMPORT INFILE employees.csv
    FORMAT VARTEXT ','
    LAYOUT employee_layout
    APPLY insert_employees
    WHERE department = 'SALES';
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://employees.csv @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      CREATE OR REPLACE TEMPORARY TABLE sc_employees_staging LIKE employees;
      COPY INTO sc_employees_staging (
        employee_id,
        first_name,
        last_name,
        department
      )
      FROM
      (
        SELECT
          $1,
          $2,
          $3,
          $4
        FROM
          @sc_import_stage/employees.csv
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
      ON_ERROR = 'CONTINUE';
      INSERT INTO employees
      SELECT
        *
      FROM
        sc_employees_staging
      WHERE
        department = 'SALES';
      DROP TABLE sc_employees_staging;
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

## File Path Handling

MLoad’s `.IMPORT INFILE` path is translated to Snowflake’s [`PUT`](https://docs.snowflake.com/en/sql-reference/sql/put) command, which requires the `file://` protocol prefix. The file is uploaded to a stage (`@sc_import_stage`) and then referenced in the `COPY INTO` statement.

### Bash Variables in Paths

Bash variables (`${VAR}`) are converted to [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) template syntax (`<%VAR%>`). These require running the script through Snowflake CLI: `snow sql -f script.sql -D "VAR=value"`.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.IMPORT INFILE ${DATA_DIR}/${FILE_NAME}
  FORMAT VARTEXT '|'
  LAYOUT employee_layout
  APPLY employee_insert;
```

##### Snowflake Scripting

Copy code

```
--** SSC-FDM-TD0003 - BASH VARIABLES FOUND, SNOWFLAKE CLI IS REQUIRED TO RUN THIS SCRIPT. USE: snow sql -f <script> -D "VAR=value" FOR EACH VARIABLE. **
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://&{DATA_DIR}/&{FILE_NAME} @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      COPY INTO employees (
        employee_id,
        first_name,
        last_name
      )
      FROM
      (
        SELECT
          $1,
          $2,
          $3
        FROM
          @sc_import_stage/&{FILE_NAME}
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|')
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

### Local Variables in Paths (Not Supported)

Local MLoad variables (`&VAR`) are **not supported** in file paths for `PUT` and `COPY INTO` statements. An EWI marker is generated to indicate manual resolution is required.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.IMPORT INFILE &FILE_NAME
  FORMAT VARTEXT '|'
  LAYOUT local_input
  APPLY load_local;
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

!!!RESOLVE EWI!!! /*** SSC-EWI-TD0097 - LOCAL VARIABLES ARE CURRENTLY NOT SUPPORTED IN THE PUT STATEMENT. ***/!!!
--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://&FILE_NAME @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    FILE_NAME STRING := 'data.csv';
  BEGIN
    BEGIN
      COPY INTO employees (
        id,
        name
      )
      FROM
      (
        SELECT
          $1,
          $2
        FROM
          !!!RESOLVE EWI!!! /*** SSC-EWI-TD0097 - LOCAL VARIABLES ARE CURRENTLY NOT SUPPORTED IN THE COPY INTO STATEMENT. ***/!!!
          @sc_import_stage/&FILE_NAME
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|')
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

### Quoted Paths

Paths enclosed in single quotes (`'...'`) are handled differently. The `COPY INTO` statement uses the `FILES` clause to specify the file name instead of appending it to the stage path.

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.IMPORT INFILE '/data/employee records.csv'
  FORMAT VARTEXT '|'
  LAYOUT employee_layout
  APPLY employee_insert;
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT 'file:///data/employee records.csv' @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      COPY INTO employees (
        employee_id,
        first_name,
        last_name
      )
      FROM
      (
        SELECT
          $1,
          $2,
          $3
        FROM
          @sc_import_stage
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|')
      ON_ERROR = 'CONTINUE'
      FILES = ('employee records.csv');
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

### Windows Path Conversion

Quoted paths with Windows backslashes (`\`) are automatically converted to forward slashes (`/`) for compatibility with Snowflake’s `PUT` command.

| MLoad Path | Snowflake Output |
| --- | --- |
| `'C:\data\employees.csv'` | `'file://C:/data/employees.csv'` |

Expand

Show lessSee more

## Multiple Imports

When a script contains multiple `.IMPORT` commands:

- The `CREATE TEMPORARY STAGE` is executed once at the beginning
- All `PUT` commands for all imports are grouped together before the `EXECUTE IMMEDIATE` block
- Each import is translated to a separate `BEGIN...END` block inside the script

### Complete Example with Different Formats

The following example demonstrates two imports with different formats:

- First import: `VARTEXT` format (CSV with comma delimiter)
- Second import: `TEXT` format (fixed-width using `SUBSTRING`)

#### Sample Source Patterns

##### Teradata MLoad

Copy code

```
.LAYOUT employees_insert_layout;
    .FIELD id * VARCHAR(10);
    .FIELD first_name * VARCHAR(50);
    .FIELD last_name * VARCHAR(50);
    .FIELD department * VARCHAR(50);
    .FIELD salary * VARCHAR(10);

.DML LABEL employees_insert_dml;

INSERT INTO employees_target (
    id,
    first_name,
    last_name,
    department,
    salary
) VALUES (
    :id,
    :first_name,
    :last_name,
    :department,
    :salary
);

.IMPORT INFILE employees.csv
    FORMAT VARTEXT ','
    LAYOUT employees_insert_layout
    APPLY employees_insert_dml;

.LAYOUT employees_text_asterisk;
    .FIELD id * CHAR(10);
    .FIELD first_name * CHAR(50);
    .FIELD last_name * CHAR(50);
    .FIELD department * CHAR(50);
    .FIELD salary * CHAR(10);

.DML LABEL employees_dml;

INSERT INTO employees_target (
    id,
    first_name,
    last_name,
    department,
    salary
) VALUES (
    :id,
    :first_name,
    :last_name,
    :department,
    :salary
);

.IMPORT INFILE employees_fixed.txt
    FORMAT TEXT
    LAYOUT employees_text_asterisk
    APPLY employees_dml;
```

##### Snowflake Scripting

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://employees.csv @sc_import_stage;

--** SSC-FDM-TD0038 - PUT COMMAND REQUIRES EXECUTION THROUGH SNOWFLAKE CLI. **
PUT file://employees_fixed.txt @sc_import_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      COPY INTO employees_target (
        id,
        first_name,
        last_name,
        department,
        salary
      )
      FROM
      (
        SELECT
          $1,
          $2,
          $3,
          $4,
          $5
        FROM
          @sc_import_stage/employees.csv
      )
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',')
      ON_ERROR = 'CONTINUE';
    END;

    BEGIN
      COPY INTO employees_target (
        id,
        first_name,
        last_name,
        department,
        salary
      )
      FROM
      (
        SELECT
          SUBSTRING($1, 1, 10),
          SUBSTRING($1, 11, 50),
          SUBSTRING($1, 61, 50),
          SUBSTRING($1, 111, 50),
          SUBSTRING($1, 161, 10)
        FROM
          @sc_import_stage/employees_fixed.txt
      )
      FILE_FORMAT = (TYPE = CSV)
      ON_ERROR = 'CONTINUE';
    END;
  EXCEPTION
    WHEN OTHER CONTINUE THEN
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
  END
$$
```

## Translation Requirements

For the [`.IMPORT`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/IMPORT) command to be fully translated, all of the following conditions must be met. See [Known Limitations](#known-limitations) for unsupported features.

### Required Components

| Component | Requirement | Error if Missing |
| --- | --- | --- |
| [`.LAYOUT`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/LAYOUT) definition | Must be defined before the `.IMPORT` command | `SSC-EWI-TD0094` |
| [`.DML LABEL`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/DML-LABEL) definition | Must contain at least one `INSERT INTO...VALUES` statement | `SSC-EWI-TD0094` |

Expand

Show lessSee more

### Supported Formats

The following file formats are fully translated to Snowflake’s `COPY INTO` command:

| MLoad Format | Description | Snowflake FILE\_FORMAT |
| --- | --- | --- |
| `FORMAT VARTEXT ','` | Delimited file with separator | `TYPE = CSV FIELD_DELIMITER = ','` |
| `FORMAT VARTEXT` | Delimited file with default pipe separator | `TYPE = CSV FIELD_DELIMITER = '|'` |
| `FORMAT TEXT` | Fixed-width positional file | `TYPE = CSV` with `SUBSTRING` extraction |
| `FORMAT UNFORMAT` | Fixed-width positional file (binary-safe) | `TYPE = CSV` with `SUBSTRING` extraction |

Expand

Show lessSee more

### Supported Layout Definitions

Field definitions in `.LAYOUT` are translated based on the format type:

| MLoad Definition | Use Case | Snowflake Translation |
| --- | --- | --- |
| `.FIELD name * VARCHAR(n)` | Delimited files (VARTEXT) - auto position | `$1`, `$2`, `$3`… (positional columns) |
| `.FIELD name pos CHAR(n)` | Fixed-width files (TEXT/UNFORMAT) - explicit position | `SUBSTRING($1, pos, n)` |
| `.FILLER name pos CHAR(n)` | Skip unused bytes in fixed-width files | Excluded from SELECT |

Expand

Show lessSee more

### Supported DML Statements

The DML statement inside `.DML LABEL` determines how data is loaded:

| MLoad DML | Description | Snowflake Translation |
| --- | --- | --- |
| `INSERT INTO table (...) VALUES (...)` | Insert new records | `COPY INTO table (...) FROM (SELECT ...)` |

Expand

Show lessSee more

### Supported Field Modifiers

Field modifiers for trimming whitespace are translated to Snowflake string functions:

| MLoad Modifier | Description | Snowflake Function |
| --- | --- | --- |
| `DROP LEADING BLANKS` | Remove leading spaces | `LTRIM($n)` |
| `DROP TRAILING NULLS` | Remove trailing nulls/spaces | `RTRIM($n)` |
| `DROP LEADING BLANKS AND TRAILING NULLS` | Remove both leading and trailing | `TRIM($n)` |

Expand

Show lessSee more

### Supported IMPORT Clauses

The following `.IMPORT` options are translated to equivalent Snowflake functionality:

| MLoad Clause | Description | Snowflake Translation |
| --- | --- | --- |
| `FROM n` | Start reading from row n (skip header rows) | `SKIP_HEADER = n-1` in FILE\_FORMAT |
| `WHERE condition` | Filter records during import | Uses staging table pattern (see [WHERE Condition](#where-condition)) |
| `NOSTOP` | Continue on errors | `ON_ERROR = 'CONTINUE'` |

Expand

Show lessSee more

## Known Limitations

The following MLoad features are not currently supported and will generate an EWI marker (`SSC-EWI-TD0094`) indicating manual resolution is required:

### Unsupported Formats

| Format | EWI Message |
| --- | --- |
| `FORMAT BINARY` | `BINARY FORMAT IS PENDING TRANSLATION` |
| `FORMAT FASTLOAD` | `FASTLOAD FORMAT IS PENDING TRANSLATION` |

Expand

Show lessSee more

### Unsupported Layout Types

| Layout Type | EWI Message |
| --- | --- |
| `.TABLE tablename` | `TABLE TYPE LAYOUT IS PENDING TRANSLATION` |

Expand

Show lessSee more

### Unsupported DML Statements in IMPORT

The following DML statements are not supported **when used within a `.DML LABEL` applied by an `.IMPORT` command**. Standalone DML statements outside of the import context are translated correctly.

| DML Statement in `.DML LABEL` | EWI Message |
| --- | --- |
| `UPDATE` statement only | `NON INSERT-VALUES DML STATEMENTS ARE PENDING TRANSLATION` |
| `DELETE` statement only | `NON INSERT-VALUES DML STATEMENTS ARE PENDING TRANSLATION` |

Expand

Show lessSee more

### Missing Required Components

| Missing Component | EWI Message |
| --- | --- |
| `.LAYOUT` definition not found | `LAYOUT DEFINITION WAS NOT FOUND IN THE SCRIPT` |
| `.DML LABEL` definition not found | `DML LABEL WAS NOT FOUND IN THE SCRIPT` |

Expand

Show lessSee more

## Related EWIs and FDMs

### Functional Difference Messages

| Code | Description |
| --- | --- |
| [SSC-FDM-TD0003](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003) | Bash variables require Snowflake CLI for execution |
| [SSC-FDM-TD0037](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0037) | LOGTABLE removed; use `COPY_HISTORY()` for monitoring |
| [SSC-FDM-TD0038](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0038) | PUT command requires execution through Snowflake CLI |
| [SSC-FDM-0027](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027) | BEGIN/END MLOAD removed; not applicable in Snowflake |

Expand

Show lessSee more

### Issues

| Code | Description |
| --- | --- |
| [SSC-EWI-TD0094](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0094) | IMPORT command not converted due to unsupported features |
| [SSC-EWI-TD0095](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0095) | DML statement in IMPORT pending translation |
| [SSC-EWI-TD0096](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0096) | COPY INTO requires explicit file name |
| [SSC-EWI-TD0097](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0097) | Local variables not supported in PUT or COPY INTO |

Expand

Show lessSee more

## Related Topics

- [COPY INTO (Snowflake Documentation)](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [PUT (Snowflake Documentation)](https://docs.snowflake.com/en/sql-reference/sql/put)
- [COPY\_HISTORY Function](https://docs.snowflake.com/en/sql-reference/functions/copy_history)
- [Snowflake Scripting](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/index)
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
