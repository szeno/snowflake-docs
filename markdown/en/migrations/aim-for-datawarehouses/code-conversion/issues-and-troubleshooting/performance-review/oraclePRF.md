# Code Conversion - Oracle Performance Review Messages

## SSC-PRF-OR0001

Package cursor FETCH uses PACKAGE\_CURSOR.FETCH\_CURSOR — stored procedure overhead per invocation.

#### Description

SnowConvert AI emits this review because each generated `PACKAGE_CURSOR.FETCH_CURSOR` call invokes an internal stored procedure and adds per-call overhead. Review fetches inside loops and increase `limit_per_fetch` when the consuming logic can process rows in batches.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE BODY schema_test.pkg_test AS
    CURSOR c_emp IS
        SELECT emp_id, emp_name
        FROM employees;
    PROCEDURE process_all IS
        v_id   NUMBER;
        v_name VARCHAR2(100);
    BEGIN
        OPEN c_emp;
        FETCH c_emp INTO v_id, v_name;
        CLOSE c_emp;
    END process_all;
END pkg_test;
```

##### Output Code:

##### Snowflake

Copy code

```
CALL PACKAGE_CURSOR.CREATE_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP"', 'SELECT emp_id, emp_name FROM schema_test.employees', 'SELECT emp_id, emp_name, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS _row_num FROM schema_test.employees');

CREATE OR REPLACE PROCEDURE SCHEMA_TEST_PKG_TEST.process_all ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    v_id NUMBER(38, 18);
    v_name VARCHAR(100);
  BEGIN
    --** SSC-FDM-OR0057 - CHECK UDF IMPLEMENTATION FOR PACKAGE_CURSOR.OPEN_CURSOR. **
    CALL PACKAGE_CURSOR.OPEN_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP"');
    --** SSC-PRF-OR0001 - PACKAGE_CURSOR.FETCH_CURSOR INCURS A TIME PENALTY ON EACH INVOCATION DUE TO INTERNAL STORED PROCEDURE EXECUTION OVERHEAD. TO REDUCE THE NUMBER OF CALLS AND IMPROVE PERFORMANCE, CONSIDER FETCHING ROWS IN BATCHES BY SETTING THE limit_per_fetch PARAMETER TO A VALUE GREATER THAN 1. **
    LET "SCHEMA_TEST_PKG_TEST.C_EMP.fetch_result_1" RESULTSET;
    "SCHEMA_TEST_PKG_TEST.C_EMP.fetch_result_1" := (
      CALL PACKAGE_CURSOR.FETCH_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP"')
    );
    LET "SCHEMA_TEST_PKG_TEST.C_EMP.batch_cursor_1" CURSOR
    FOR
      "SCHEMA_TEST_PKG_TEST.C_EMP.fetch_result_1";
    OPEN "SCHEMA_TEST_PKG_TEST.C_EMP.batch_cursor_1";
    FETCH
      "SCHEMA_TEST_PKG_TEST.C_EMP.batch_cursor_1"
    INTO
      v_id,
      v_name;
    CLOSE "SCHEMA_TEST_PKG_TEST.C_EMP.batch_cursor_1";
    CALL PACKAGE_CURSOR.CLOSE_CURSOR('"SCHEMA_TEST_PKG_TEST.C_EMP"');
  END;
$$;
```

#### Best Practices

- Set `limit_per_fetch` to a value greater than 1 when the consuming logic can process rows in batches.
- Review package cursor fetches inside loops because each generated helper invocation executes a stored procedure.
- For additional assistance, please email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-PRF-OR0002

The generated DBMS\_OUTPUT helper logs to a table on each call, which may impact performance.

### Description

Snowflake has no native equivalent of Oracle’s `DBMS_OUTPUT` server-side buffer. To preserve diagnostic output, SnowConvert AI translates `DBMS_OUTPUT` calls to generated helper procedures (`DBMS_OUTPUT.PUT_LINE_UDP`, `DBMS_OUTPUT.PUT_UDP`, and `DBMS_OUTPUT.NEW_LINE_UDP`) that write each message to a logging table.

Because every call performs a table write, using `DBMS_OUTPUT` inside loops or high-frequency code paths can noticeably impact performance. This message is emitted so that diagnostic output calls that are not required in Snowflake can be removed. It replaces the previous `SSC-FDM-OR0035` marker on these calls, and `PUT` / `NEW_LINE` no longer emit `SSC-EWI-OR0076`.

### Code Example

#### Input Code:

Copy code

```
CREATE OR REPLACE PROCEDURE dbms_output_put_proc
IS
BEGIN
    DBMS_OUTPUT.PUT('COLUMN: FRM_STATUS_G__C ');
END;
```

#### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE dbms_output_put_proc ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-PRF-OR0002 - THE GENERATED DBMS_OUTPUT HELPER LOGS TO A TABLE ON EACH CALL, WHICH MAY IMPACT PERFORMANCE. REMOVE DIAGNOSTIC OUTPUT CALLS THAT ARE NOT REQUIRED. **
    CALL DBMS_OUTPUT.PUT_UDP('COLUMN: FRM_STATUS_G__C ');
  END;
$$;
```

### Best Practices

- Remove `DBMS_OUTPUT` calls that were used only for debugging or tracing and are not required in the migrated code.
- Where diagnostic output must be kept, avoid placing `DBMS_OUTPUT` calls inside loops or frequently executed branches to minimize the per-call table writes.
- For additional assistance, please email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support@snowflake.com).

## SSC-PRF-OR0003

BULK COLLECT translated to ARRAY\_AGG materializes the entire result set into a single ARRAY.

#### Description

SnowConvert AI translates `BULK COLLECT` to `ARRAY_AGG`, which materializes the full result set in one array. Review the expected row volume and bound or batch the query when the array could approach Snowflake variable limits.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE "PORTFOLIO_ANALYTICS" ("PORTFOLIO_ID" NUMBER(20,0), "CASH_PCT" NUMBER, "BETA" NUMBER);

CREATE OR REPLACE PROCEDURE MD_PORT_ANALYTIC_POP_Q AS
  TYPE ANAL_UPLOAD_FIELDS_TAB IS TABLE OF "PORTFOLIO_ANALYTICS"%ROWTYPE;
  LV_ANAL_UPLOAD_FIELDS_TAB ANAL_UPLOAD_FIELDS_TAB;
BEGIN
  SELECT PORTFOLIO_ID, CASH_PCT, NULL AS BETA
    BULK COLLECT INTO LV_ANAL_UPLOAD_FIELDS_TAB
    FROM (
      WITH SRC AS (SELECT 10 PORTFOLIO_ID, 1.5 CASH_PCT FROM DUAL)
      SELECT PORTFOLIO_ID, CASH_PCT, NULL AS BETA FROM SRC
    );
  INSERT INTO "PORTFOLIO_ANALYTICS" ("PORTFOLIO_ID", "CASH_PCT", "BETA")
  VALUES (
    LV_ANAL_UPLOAD_FIELDS_TAB(1).PORTFOLIO_ID,
    LV_ANAL_UPLOAD_FIELDS_TAB(1).CASH_PCT,
    LV_ANAL_UPLOAD_FIELDS_TAB(1).BETA
  );
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE "PORTFOLIO_ANALYTICS" (
  "PORTFOLIO_ID" NUMBER(20) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  "CASH_PCT" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  "BETA" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
;

CREATE OR REPLACE PROCEDURE MD_PORT_ANALYTIC_POP_Q ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
--    --** SSC-FDM-OR0053 - EMBEDDED COLLECTION TYPE DEFINITION 'PL COLLECTION TYPE DEFINITION' WAS REMOVED. COLLECTION VARIABLES ARE TRANSFORMED TO ARRAY BY OTHER RULES. **
--    TYPE ANAL_UPLOAD_FIELDS_TAB IS TABLE OF "PORTFOLIO_ANALYTICS"%ROWTYPE;
    LV_ANAL_UPLOAD_FIELDS_TAB ARRAY /*** SSC-FDM-OR0084 - COLLECTION TYPE 'ANAL_UPLOAD_FIELDS_TAB' WAS MAPPED TO A SNOWFLAKE ARRAY; ELEMENT INDEXING WAS ADJUSTED FROM 1-BASED TO 0-BASED. ***/;
  BEGIN
    SELECT
      ARRAY_AGG(OBJECT_CONSTRUCT('PORTFOLIO_ID', PORTFOLIO_ID, 'CASH_PCT', CASH_PCT, 'BETA', NULL)) /*** SSC-PRF-OR0003 - BULK COLLECT WAS TRANSLATED TO ARRAY_AGG, WHICH MATERIALIZES THE ENTIRE RESULT SET INTO A SINGLE ARRAY. FOR LARGE RESULT SETS THIS MAY EXCEED SNOWFLAKE'S PER-VARIABLE MEMORY LIMIT; REVIEW THE EXPECTED VOLUME AND CONSIDER BOUNDING THE QUERY. ***/
    INTO
      :LV_ANAL_UPLOAD_FIELDS_TAB
    FROM
      (
        WITH SRC AS
        (
          SELECT
            10 PORTFOLIO_ID,
            1.5 CASH_PCT
          FROM
            DUAL
        )
        SELECT
          PORTFOLIO_ID,
          CASH_PCT,
          NULL AS BETA
        FROM
          SRC);
    INSERT INTO "PORTFOLIO_ANALYTICS"("PORTFOLIO_ID", "CASH_PCT", "BETA")
    SELECT
      :LV_ANAL_UPLOAD_FIELDS_TAB[0]:PORTFOLIO_ID,
      :LV_ANAL_UPLOAD_FIELDS_TAB[0]:CASH_PCT,
      :LV_ANAL_UPLOAD_FIELDS_TAB[0]:BETA;
  END;
$$;
```

#### Best Practices

- Bound the source query when the result set can be large, or process rows in smaller batches.
- Test representative volumes and monitor the generated array’s memory requirements.
- For additional assistance, please email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).
