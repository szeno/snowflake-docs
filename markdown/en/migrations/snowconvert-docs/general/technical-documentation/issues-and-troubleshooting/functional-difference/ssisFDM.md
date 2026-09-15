# Code Conversion - SSIS Functional Differences

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This section provides detailed documentation for all Functional Difference Messages (FDMs) that SnowConvert may generate during SSIS to dbt conversion. FDMs indicate where the converted code functions correctly but has behavioral differences from the original SSIS implementation.

For assistance with any FDM, you can use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions, or contact [aim-support@snowflake.com](mailto:aim-support@snowflake.com) for additional support.

## SSC-FDM-SSIS0001

Replace NULL with appropriate ORDER BY column(s) to ensure deterministic first match selection.

### Severity

None

### Description

This FDM is generated when a Lookup transformation is converted to SQL JOIN. In SSIS, the Lookup transformation returns the first matching row based on the order rows are read from the reference table. In standard SQL, when multiple rows match the join condition without an ORDER BY clause, any matching row may be returned, making the result non-deterministic.

To ensure consistent behavior matching SSIS, add an ORDER BY clause to the query that retrieves the first match.

### Converted Code

Copy code

```
:force:

WITH lookup_reference AS
(
   SELECT
      SalesTerritoryKey,
      SalesTerritoryAlternateKey,
      SalesTerritoryRegion,
      SalesTerritoryCountry,
      SalesTerritoryGroup,
      SalesTerritoryImage
   FROM
      {{ ref('stg_raw__lookup') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         SalesTerritoryKey
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
      EmployeeKey EmployeeKey,
      SalesTerritoryKey SalesTerritoryKey,
      BaseRate BaseRate,
      FirstName FirstName,
      LastName LastName
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   input_data.EmployeeKey,
   input_data.SalesTerritoryKey,
   input_data.BaseRate,
   input_data.FirstName,
   input_data.LastName,
   lookup_reference.SalesTerritoryRegion Region,
   lookup_reference.SalesTerritoryCountry Country
FROM
   input_data
   INNER JOIN
      lookup_reference
      ON lookup_reference.SalesTerritoryKey = input_data.SalesTerritoryKey
```

### Best Practices

- Replace `null` with appropriate ORDER BY columns (e.g., `ORDER BY modified_date DESC, customer_id`)
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0002

Add an ORDER BY clause to ensure sorted output.

### Severity

Low

### Description

This FDM is generated when a Merge transformation is converted to UNION ALL. In SSIS, the Merge transformation requires sorted inputs and naturally produces a sorted, deterministic output preserving the merge order. The equivalent SQL UNION ALL does not guarantee any particular order unless an explicit ORDER BY clause is added.

If the order of rows matters for downstream processing or matches SSIS behavior, add an ORDER BY clause to the final query.

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0002 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. **
WITH source1 AS (
   SELECT ProductID, ProductName, Price
   FROM {{ ref('stg_products') }}
),
source2 AS (
   SELECT ProductID, ProductName, Price
   FROM {{ ref('stg_new_products') }}
)
SELECT * FROM source1
UNION ALL
SELECT * FROM source2
-- Add ORDER BY ProductID if sorted output is required
```

### Best Practices

- Add `ORDER BY` clause matching the original SSIS sort keys if order matters
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0003

The SSIS container was converted inline.

### Severity

None

### Description

This FDM indicates that an SSIS container (Sequence Container, For Loop, or ForEach Loop) was converted inline rather than as a separate procedural block. In SSIS, containers create variable scopes and logical groupings. In the Snowflake conversion, container contents are expanded inline within the parent execution context.

This approach offers benefits:

- Improved debugging (direct visibility of all steps)
- Better performance (reduced nesting overhead)
- Simplified execution flow

However, variable scoping works differently—variables are in the parent scope rather than container scope.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK package_main
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0003 - THE SSIS 'SEQUENCE' CONTAINER WAS CONVERTED INLINE. Original container name: Package\Sequence Container **
   BEGIN
      -- Execute SQL Task 1
      INSERT INTO staging_table SELECT * FROM source_table1;

      -- Execute SQL Task 2
      INSERT INTO target_table SELECT * FROM staging_table;
   END;
END;
```

### Best Practices

- Review variable scope changes if the container had local variables
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0004

Add an ORDER BY clause to ensure sorted output.

### Severity

Low

### Description

This FDM is generated when a Merge Join transformation is converted to a standard SQL JOIN. In SSIS, the Merge Join transformation requires sorted inputs and naturally produces a sorted, deterministic output based on the join keys and the merge algorithm. The equivalent SQL JOIN does not guarantee any particular order unless an explicit ORDER BY clause is added.

If the order of rows matters for downstream processing or to match SSIS behavior exactly, add an ORDER BY clause.

### Converted Code

Copy code

```
:force:

SELECT
   --** SSC-FDM-SSIS0004 - ADD AN ORDER BY CLAUSE TO ENSURE SORTED OUTPUT. THE SSIS MERGE JOIN TRANSFORMATION ASSUMES SORTED INPUTS AND NATURALLY PRODUCES A SORTED, DETERMINISTIC OUTPUT. THE EQUIVALENT SQL JOIN DOES NOT GUARANTEE ORDER. **
   employeeassignments.employee_id,
   tasks.project_id AS "project identifier",
   employeeassignments.assignment_start_date,
   employeeassignments.assigned_hours,
   tasks.task_id
FROM
   {{ ref('stg_employee_assignments') }} AS employeeassignments
   INNER JOIN {{ ref('stg_tasks') }} AS tasks
      ON employeeassignments.task_id = tasks.task_id
-- Add ORDER BY employee_id, task_id if sorted output is required
```

### Best Practices

- Add `ORDER BY` clause on the join keys if order matters
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0005

Package was converted to stored procedure because it is being reused by other packages.

### Severity

None

### Description

This FDM indicates that an SSIS package was converted to a Snowflake stored PROCEDURE instead of a TASK because it is called by at least one ExecutePackage task from another control flow. This design choice provides several benefits:

**Benefits of PROCEDURE over TASK:**

- **Synchronous execution**: Calling packages wait for completion (matches SSIS behavior)
- **Reusability**: Can be called from multiple locations with different parameters
- **Return values**: Can return status codes or result sets to callers
- **Simpler orchestration**: Direct CALL statements instead of complex EXECUTE TASK chains

**Difference from SSIS:**

- Must be explicitly called with `CALL procedure_name()` instead of automatic execution
- Parameters must be passed explicitly in the CALL statement
- No automatic task scheduling (must be invoked programmatically)

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0005 - PACKAGE WAS CONVERTED TO STORED PROCEDURE BECAUSE IT IS BEING REUSED BY OTHER PACKAGES. **
CREATE OR REPLACE PROCEDURE public.utilitypackage(input_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
   -- Package logic here
   INSERT INTO log_table VALUES (CURRENT_TIMESTAMP(), :input_param);
   RETURN 'SUCCESS';
END;
$$;

-- Parent Package 1 calls the procedure
CREATE OR REPLACE TASK public.parent_package_1_execute_utility
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   CALL public.utilitypackage('param_value_1');
END;

-- Parent Package 2 calls the procedure
CREATE OR REPLACE TASK public.parent_package_2_execute_utility
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   CALL public.utilitypackage('param_value_2');
END;
```

### Best Practices

- Use CALL statements to invoke the procedure from parent packages
- Pass parameters explicitly in the CALL statement
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0006

Event handler stored procedure created but not automatically triggered.

### Severity

None

### Description

This FDM indicates that an SSIS event handler has been converted to a Snowflake stored procedure, but unlike SSIS where event handlers are automatically triggered by runtime events (OnError, OnPreExecute, OnPostExecute, etc.), the generated stored procedure must be invoked manually or through a custom triggering mechanism.

In SSIS, event handlers automatically fire when their associated event occurs during package execution. In Snowflake, there is no built-in event handler mechanism. The converted stored procedure contains the event handler logic but requires explicit invocation using a `CALL` statement.

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0006 - EVENT HANDLER STORED PROCEDURE CREATED BUT NOT AUTOMATICALLY TRIGGERED. MANUAL INVOCATION OR TRIGGERING MECHANISM IMPLEMENTATION REQUIRED. **
CREATE OR REPLACE PROCEDURE public.package_execute_sql_task_onerror_handler ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      LET User_ErrorCount NUMERIC := public.GetControlVariableUDF('User_ErrorCount', 'MyPackage') :: NUMERIC;
      INSERT INTO TaskErrorLog (TaskName, ErrorTime) VALUES ('Execute SQL Task', CURRENT_TIMESTAMP());
      RETURN 'SUCCESS';
   END;
$$;
```

### Best Practices

- Add explicit `CALL` statements to invoke the event handler procedure at appropriate points in your orchestration
- For OnError handlers, wrap task execution in BEGIN…EXCEPTION blocks and call the handler in the exception handler
- For OnPreExecute/OnPostExecute handlers, add CALL statements before/after the relevant task execution
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0007

Send Mail Task SMTP connection settings are managed by Snowflake.

### Severity

None

### Description

This FDM indicates that SSIS Send Mail Task SMTP connection settings were not converted. In SSIS, you configure custom SMTP server settings through an SMTP Connection Manager. In Snowflake, email delivery is managed entirely through the built-in Notification Integration service, and custom SMTP servers cannot be specified.

This is informational only and does not require action. Snowflake’s email service is reliable and properly configured.

### Converted Code

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
   --** SSC-FDM-SSIS0007 - CUSTOM SMTP SERVER SETTINGS ARE NOT APPLICABLE. SNOWFLAKE MANAGES EMAIL DELIVERY THROUGH THE NOTIFICATION INTEGRATION. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Test', 'Test message');
END;
```

### Best Practices

- No manual action required
- Snowflake handles email delivery through its managed infrastructure
- Ensure recipients are verified in your Snowflake account
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0008

Send Mail Task FROM address added to email body.

### Severity

None

### Description

This FDM indicates that the SSIS Send Mail Task FROM address has been preserved by prepending it to the email body. Snowflake’s email service uses a fixed sender address managed by your Snowflake account and does not allow custom FROM addresses.

The original FROM address is included in the message body so recipients can see who intended to send the email.

### Converted Code

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

### Best Practices

- No manual action required for basic functionality
- The FROM address is preserved in the message body for reference
- Consider updating email templates if the sender information format needs adjustment
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0009

Send Mail Task CC addresses added to recipients list.

### Severity

None

### Description

This FDM indicates that CC (carbon copy) recipients from the SSIS Send Mail Task have been merged into the main recipients list. Snowflake’s `SYSTEM$SEND_EMAIL` does not distinguish between TO and CC recipients. All recipients receive the email, but they will not see the CC distinction in their email client.

### Converted Code

Copy code

```
:force:

BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com", "team@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   --** SSC-FDM-SSIS0009 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT CC ADDRESSING. ALL CC RECIPIENTS HAVE BEEN ADDED TO THE MAIN RECIPIENTS LIST. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com,team@example.com', 'Status Update', 'All systems operational.');
END;
```

### Best Practices

- No manual action required for basic functionality
- All recipients will receive the email successfully
- If TO/CC distinction is important, consider adding recipient information in the email body
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0010

Send Mail Task BCC addresses added to recipients list.

### Severity

None

### Description

This FDM indicates that BCC (blind carbon copy) recipients from the SSIS Send Mail Task have been merged into the main recipients list. This is an important behavioral change: in SSIS, BCC recipients are hidden from other recipients. In Snowflake, all recipients are visible to each other because `SYSTEM$SEND_EMAIL` does not support BCC addressing.

**Privacy concern:** Recipients who were originally BCC’d will now be visible to all other recipients.

### Converted Code

Copy code

```
:force:

BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com", "audit@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   --** SSC-FDM-SSIS0010 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT BCC ADDRESSING. ALL BCC RECIPIENTS HAVE BEEN ADDED TO THE MAIN RECIPIENTS LIST, MAKING THEM VISIBLE TO ALL RECIPIENTS. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com,audit@example.com', 'Audit Trail', 'Process completed.');
END;
```

### Best Practices

- Review if BCC privacy is required for your use case
- If recipients must remain hidden, send separate emails to each BCC recipient
- Consider implementing a wrapper procedure that sends individual emails for BCC scenarios
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0011

Bulk Insert Task MaximumErrors has semantic differences in Snowflake.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `MaximumErrors` setting has been converted to Snowflake’s `ON_ERROR` option, but the behavior differs. In SSIS, `MaximumErrors` specifies the maximum number of errors allowed before the bulk insert fails. In Snowflake, `ON_ERROR` controls the behavior when errors occur but works differently:

| SSIS MaximumErrors | Snowflake ON\_ERROR |
| --- | --- |
| 0 (fail on first error) | `ABORT_STATEMENT` |
| N (fail after N errors) | `SKIP_FILE_N` (skips file after N errors) |
| Large value (continue) | `CONTINUE` |

Expand

Show lessSee more

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0011 - SSIS BULKINSERTTASK MAXIMUMERRORS SPECIFIES ERROR COUNT THRESHOLD. SNOWFLAKE ON_ERROR CONTROLS BEHAVIOR WHEN ERRORS OCCUR. REVIEW ERROR HANDLING STRATEGY. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV')
   ON_ERROR = SKIP_FILE_5;
END;
```

### Best Practices

- Review your error tolerance requirements
- `ON_ERROR = CONTINUE` is most permissive (skips bad records)
- `ON_ERROR = ABORT_STATEMENT` stops on first error
- `ON_ERROR = SKIP_FILE_N` skips the file after N errors per file
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0012

Bulk Insert Task BatchSize is managed automatically by Snowflake.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `BatchSize` setting is not applicable in Snowflake. In SSIS, `BatchSize` controls how many rows are committed in each batch transaction. Snowflake’s COPY INTO command manages batching automatically for optimal performance and does not expose batch size configuration.

Snowflake uses micro-partitions and automatic parallelization to achieve high-performance data loading without manual batch tuning.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0012 - SSIS BULKINSERTTASK BATCHSIZE IS NOT AVAILABLE IN SNOWFLAKE. SNOWFLAKE MANAGES BATCHING AUTOMATICALLY FOR OPTIMAL PERFORMANCE. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- No manual action required
- Snowflake automatically optimizes batch processing
- For very large loads, consider splitting into multiple files for parallel processing
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0013

Bulk Insert Task KeepIdentity cannot override Snowflake autoincrement behavior.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `KeepIdentity` option behavior differs in Snowflake. In SQL Server, `KeepIdentity=True` preserves identity values from the source file, while `KeepIdentity=False` allows SQL Server to generate new identity values.

In Snowflake, COPY INTO always loads values from the file as-is. If you need Snowflake to generate identity values, you must either:

- Remove the identity column from the source file
- Load into a staging table and use INSERT with column mapping

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0013 - SSIS BULKINSERTTASK KEEPIDENTITY CANNOT OVERRIDE SNOWFLAKE AUTOINCREMENT. USE EXPLICIT COLUMN MAPPING TO LOAD IDENTITY VALUES INTO NON-AUTOINCREMENT COLUMNS. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- If preserving identity values: load directly (Snowflake default behavior)
- If generating new identity values: remove the identity column from the source file, or use a staging table approach
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

To have Snowflake auto-generate identity values, load to a staging table and insert with an explicit column list:

Copy code

```
:force:

-- Step 1: Load all columns to staging
COPY INTO staging_table FROM '@my_stage' FILE_FORMAT = (TYPE = 'CSV');

-- Step 2: Insert with column list (exclude identity column)
INSERT INTO target_table (col1, col2, col3)
SELECT col1, col2, col3 FROM staging_table;
```

## SSC-FDM-SSIS0014

Bulk Insert Task TableLock is not needed in Snowflake.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `TableLock` option is not applicable in Snowflake. In SQL Server, `TableLock=True` acquires a table-level lock during bulk insert for better performance by reducing lock overhead.

Snowflake uses Multi-Version Concurrency Control (MVCC), which allows concurrent reads during writes without explicit locking. Table locks are not needed or supported because Snowflake handles concurrency automatically.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0014 - SSIS BULKINSERTTASK TABLELOCK IS NOT NEEDED IN SNOWFLAKE. MVCC ARCHITECTURE ALLOWS CONCURRENT READS DURING WRITES WITHOUT EXPLICIT LOCKING. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- No manual action required
- Snowflake’s MVCC architecture handles concurrency automatically
- Readers see consistent data without being blocked by writers
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0015

Bulk Insert Task SortedData hint is not available in Snowflake.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `SortedData` option is not applicable in Snowflake. In SQL Server, specifying `SortedData` with a column name hints that the data is pre-sorted, allowing SQL Server to optimize the bulk insert by avoiding re-sorting for clustered index maintenance.

Snowflake does not use traditional indexes. For query optimization on sorted data access patterns, use the `CLUSTER BY` clause on table definitions instead.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0015 - SSIS BULKINSERTTASK SORTEDDATA HINT IS NOT AVAILABLE IN SNOWFLAKE. USE CLUSTER BY ON TABLE DEFINITION FOR SIMILAR OPTIMIZATION. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- If sort optimization is important, define clustering on the target table
- Snowflake automatically manages micro-partition pruning
- Clustering is most beneficial for very large tables with common filter patterns
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Define clustering on the target table for similar optimization to SortedData:

Copy code

```
:force:

ALTER TABLE target_table CLUSTER BY (sort_column);
```

## SSC-FDM-SSIS0016

Bulk Insert Task CheckConstraints is always enforced in Snowflake.

### Severity

None

### Description

This FDM indicates that the SSIS Bulk Insert Task `CheckConstraints` option behavior differs in Snowflake. In SQL Server, `CheckConstraints=False` (the default for bulk insert) disables CHECK constraint validation during the load for better performance.

In Snowflake, constraints are always validated during data loading. However, Snowflake’s constraint enforcement is different from SQL Server—NOT NULL constraints are enforced, but CHECK, UNIQUE, and FOREIGN KEY constraints are not enforced (they are informational only).

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0016 - SSIS BULKINSERTTASK CHECKCONSTRAINTS OPTION IS IMPLICIT IN SNOWFLAKE. CONSTRAINTS ARE ALWAYS VALIDATED DURING DATA LOADING. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- Review constraint requirements for data integrity
- NOT NULL constraints are enforced by Snowflake
- CHECK, UNIQUE, and FOREIGN KEY constraints are informational only
- Implement data validation logic in your ETL process if strict constraint checking is required
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0017

Bulk Insert Task field terminator not specified, using SSIS default value.

### Severity

None

### Description

This FDM is generated when an SSIS Bulk Insert Task does not explicitly specify a field terminator (`FieldTerminator`) in the `.dtsx` package configuration. When no field terminator is specified, SnowConvert uses the SSIS default value (typically a tab character `\t` or comma `,`). The default value is applied to the `FIELD_DELIMITER` option in the generated Snowflake `COPY INTO` statement.

Verify that the default field terminator matches the actual format of your data file to ensure correct column parsing.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0017 - FIELD TERMINATOR NOT SPECIFIED IN DTSX. USING SSIS DEFAULT VALUE ','. VERIFY THIS MATCHES YOUR DATA FILE FORMAT. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\r\n')
   ON_ERROR = CONTINUE;
END;
```

### Best Practices

- Verify the default field terminator matches your actual data file format
- Open the source data file and confirm the column separator character
- Update the `FIELD_DELIMITER` value in the FILE\_FORMAT if it does not match
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0018

Bulk Insert Task row terminator not specified, using SSIS default value.

### Severity

None

### Description

This FDM is generated when an SSIS Bulk Insert Task does not explicitly specify a row terminator (`RowTerminator`) in the `.dtsx` package configuration. When no row terminator is specified, SnowConvert uses the SSIS default value (typically `\r\n` on Windows). The default value is applied to the `RECORD_DELIMITER` option in the generated Snowflake `COPY INTO` statement.

Verify that the default row terminator matches the actual format of your data file to ensure correct row parsing.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   --** SSC-FDM-SSIS0018 - ROW TERMINATOR NOT SPECIFIED IN DTSX. USING SSIS DEFAULT VALUE '\r\n'. VERIFY THIS MATCHES YOUR DATA FILE FORMAT. **
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\r\n')
   ON_ERROR = CONTINUE;
END;
```

### Best Practices

- Verify the default row terminator matches your actual data file format
- Files created on Windows typically use `\r\n`, while Unix/Linux files use `\n`
- Update the `RECORD_DELIMITER` value in the FILE\_FORMAT if it does not match
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0019

Excel Source file staging required.

### Severity

None

### Description

This FDM appears in the migration assessment report for every Excel Source component conversion. It is a reminder that Snowflake requires Excel files to be staged before they can be processed.

In SSIS, Excel Source components read directly from file system paths (e.g., `C:\Data\sales.xlsx`). In Snowflake, files must be uploaded to a stage (internal or external) before they can be queried by the generated `excel_source_udf` UDF.

The assessment report message includes the stage file path variable name used in the generated code, which you must configure with the actual location of your staged Excel file.

### Converted Code

The generated dbt model references the stage path via a dbt variable:

Copy code

```
:force:

WITH excel_raw_data AS
(
   SELECT
      data
   FROM
      TABLE(excel_source_udf('{{ var('Package_Data_Flow_Task_Excel_Source_stage_file_path') }}', 'Sales', 'YES'))
),
parsed_data AS
(
   SELECT
      data['ProductName'] :: VARCHAR AS ProductName,
      TRY_TO_DOUBLE(data['Quantity'] :: VARCHAR) AS Quantity
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
```

Update the variable in `dbt_project.yml`:

Copy code

```
:force:

vars:
  Package_Data_Flow_Task_Excel_Source_stage_file_path: "@my_stage/sales.xlsx"
```

### Best Practices

- Create a Snowflake stage: `CREATE OR REPLACE STAGE my_stage;`
- Upload your Excel file: `PUT file:///path/to/sales.xlsx @my_stage AUTO_COMPRESS = FALSE;`
- Update the stage file path variable in `dbt_project.yml` to point to the staged file
- Verify the file is staged correctly using `LIST @my_stage;`
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0020

Excel Source legacy format may have behavioral differences.

### Severity

None

### Description

This FDM appears in the migration assessment report when an SSIS Excel Source component references a legacy `.xls` (Excel 97-2003) or binary `.xlsb` file format. These legacy formats may have minor differences in date and number handling compared to the modern `.xlsx` format.

The generated `excel_source_udf` UDF auto-detects the format from the filename extension, so the generated code works with all Excel formats. However, certain data type conversions — particularly dates stored as serial numbers — may behave differently between formats.

In legacy Excel formats, dates are stored as serial numbers (days since 1899-12-30). If date columns appear as numbers in the output, use the `DATEADD` serial conversion pattern.

### Converted Code

The generated dbt model is the same for all Excel formats:

Copy code

```
:force:

WITH excel_raw_data AS
(
   SELECT
      data
   FROM
      TABLE(excel_source_udf('{{ var('Package_Data_Flow_Task_Excel_Source_stage_file_path') }}', 'Sheet1', 'YES'))
),
parsed_data AS
(
   SELECT
      data['OrderId'] :: VARCHAR AS OrderId,
      TRY_TO_DATE(data['OrderDate'] :: VARCHAR) AS OrderDate,
      TRY_TO_DOUBLE(data['Amount'] :: VARCHAR) AS Amount
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
```

If date columns come through as serial numbers, convert them manually:

Copy code

```
:force:

-- Convert Excel date serial number to Snowflake DATE
DATEADD('day', TRY_TO_DOUBLE(data['OrderDate'] :: VARCHAR), '1899-12-30' :: DATE) AS OrderDate
```

### Best Practices

- Convert legacy `.xls` or `.xlsb` files to `.xlsx` format before migration if possible
- For date columns that appear as numbers, use `DATEADD('day', serial_number, '1899-12-30')` to convert
- Test the output data types and values against the original SSIS component’s results
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0021

SSIS Pivot PassThroughUnmatchedPivotKeys behavioral difference.

### Severity

Low

### Description

This FDM is generated when an SSIS Pivot transformation has the `PassThroughUnmatchedPivotKeys` property enabled. In SSIS, this setting causes rows with unmatched pivot key values to be passed through to a separate output for further processing. The converted SQL uses `CASE WHEN ... THEN` with `GROUP BY`, which produces `NULL` values for unmatched pivot keys instead of routing them to a separate output.

If your downstream logic depends on capturing unmatched pivot key rows, you must implement additional filtering to separate matched and unmatched rows.

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0021 - SSIS PIVOT WITH PASSTHROUGHUNMATCHEDPIVOTKEYS ENABLED PASSES UNMATCHED PIVOT KEY ROWS TO A SEPARATE OUTPUT. THE CONVERTED SQL PRODUCES NULL VALUES FOR UNMATCHED PIVOT KEYS INSTEAD. **
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
   END) AS Bike
FROM
   source_data
GROUP BY
   CustomerName
```

### Best Practices

- If unmatched rows need separate handling, add a WHERE clause to filter rows where all pivot columns are NULL
- Consider creating a separate model for unmatched rows using `NOT IN` or `NOT EXISTS` against the expected pivot key values
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0022

SSIS Pivot assumes input data is sorted by Set Key.

### Severity

Low

### Description

This FDM is generated when an SSIS Pivot transformation is converted to SQL. The SSIS Pivot transformation assumes that the input data is sorted by the Set Key column, and the transformation’s output preserves this sort order. The converted SQL uses `GROUP BY`, which does not require or preserve sort order. If downstream consumers depend on sorted output, an explicit `ORDER BY` clause must be added.

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0022 - THE SSIS PIVOT TRANSFORMATION ASSUMES INPUT DATA IS SORTED BY THE SET KEY COLUMN. THE CONVERTED SQL USES GROUP BY WHICH DOES NOT REQUIRE OR PRESERVE SORT ORDER. VERIFY THAT DOWNSTREAM CONSUMERS DO NOT DEPEND ON SORTED OUTPUT. **
WITH source_data AS
(
   SELECT
      Region,
      CustomerName,
      Product,
      Quantity
   FROM
      {{ ref('stg_raw__source') }}
)
SELECT
   Region,
   CustomerName,
   MAX(CASE
      WHEN Product = 'Bike'
         THEN Quantity
   END) AS Bike,
   MAX(CASE
      WHEN Product = 'Helmet'
         THEN Quantity
   END) AS Helmet
FROM
   source_data
GROUP BY
   Region,
   CustomerName
```

### Best Practices

- Add an `ORDER BY` clause if downstream consumers depend on sorted output
- Use the same sort key as the original SSIS Pivot Set Key column
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0023

SSIS expression circular variable reference detected.

### Severity

Medium

### Description

This FDM is generated when SnowConvert detects a circular reference while expanding an SSIS variable expression. A circular reference occurs when a variable’s expression references itself (directly or indirectly through other variables). When this happens, SnowConvert uses the default value for the variable’s data type instead of attempting to resolve the infinite loop.

Review the original SSIS variable definitions to determine the intended value and update the generated code accordingly.

### Converted Code

Copy code

```
:force:

--** SSC-FDM-SSIS0023 - CIRCULAR REFERENCE DETECTED WHEN EXPANDING VARIABLE 'User::Counter'. THE DEFAULT VALUE FOR TYPE 'Int32' HAS BEEN USED INSTEAD. **
CREATE OR REPLACE TASK public.my_package
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   LET User_Counter NUMERIC := 0;
   -- Original variable expression referenced itself: @[User::Counter] + 1
   -- Default value for Int32 (0) was used instead
END;
```

### Best Practices

- Review the original SSIS variable definitions to identify the circular dependency chain
- Determine the intended initial value and update the generated code manually
- Break the circular dependency by reorganizing variable assignments
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0024

SSIS FileSystemTask directory path translated to Snowflake stage prefix.

### Severity

None

### Description

This FDM indicates that an SSIS File System Task directory operation has been translated to use Snowflake stage prefix-based paths. Unlike traditional file systems where directories are distinct entities, Snowflake stages use prefix-based paths — a “directory” is simply a common prefix shared by multiple file paths.

When the generated code uses `REMOVE @stage/path/` with a trailing slash, it deletes **all files** that match the prefix pattern `path/`, not a single directory entry. This is functionally equivalent to recursively deleting a directory in a traditional file system, but the semantics are different.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_delete_temp_directory
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_TempFolder VARCHAR := public.GetControlVariableUDF('User_TempFolder', 'package') :: VARCHAR;
   ---- Start block 'Package\Delete Temp Directory'
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   --** SSC-FDM-SSIS0024 - SNOWFLAKE STAGES USE PREFIX-BASED PATHS, NOT REAL DIRECTORIES. THE REMOVE COMMAND WITH A TRAILING SLASH DELETES ALL FILES MATCHING THE PREFIX PATTERN. **
   EXECUTE IMMEDIATE CONCAT('REMOVE ', :User_TempFolder, '/');
   ---- End block 'Package\Delete Temp Directory'

END;
```

### Best Practices

- Ensure the trailing slash is present in directory operations to match all files under the prefix
- Be cautious: `REMOVE @stage/data/` will delete all files starting with `data/`, including nested paths like `data/subdir/file.txt`
- For delete-directory-content operations (keep the directory but remove its contents), the generated code re-creates a `.keep` placeholder file after the REMOVE to preserve the prefix
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0025

SSIS FileSystemTask variable must contain a valid Snowflake stage path.

### Severity

None

### Description

This FDM indicates that the generated File System Task operation uses an SSIS variable to build the stage path dynamically at runtime. The variable value must contain a valid Snowflake stage path (e.g., `@my_stage/path/to/file.txt`) when the task executes.

In SSIS, File System Task variables typically contain local file system paths (e.g., `C:\Data\input.csv`). After migration, these variables must be updated to hold Snowflake stage paths instead. The variable value is set through the task CONFIG section or the `UpdateControlVariable` procedure.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_delete_source_file
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_SourceFilePath VARCHAR := public.GetControlVariableUDF('User_SourceFilePath', 'package') :: VARCHAR;
   ---- Start block 'Package\Delete Source File'
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   EXECUTE IMMEDIATE CONCAT('REMOVE ', :User_SourceFilePath);
   ---- End block 'Package\Delete Source File'

END;
```

### Best Practices

- Update the variable’s default value in the task CONFIG section to use a Snowflake stage path (e.g., `@my_stage/data/input.csv`)
- Ensure the stage path includes the `@` prefix followed by the stage name
- For directory paths, include a trailing slash (e.g., `@my_stage/data/output/`)
- Test with `LIST @my_stage` to verify the file exists at the expected path before running the task
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0026

SSIS FileSystemTask CreateDirectory translated using COPY INTO placeholder file.

### Severity

None

### Description

This FDM indicates that an SSIS File System Task `CreateDirectory` operation has been translated using a workaround because Snowflake stages do not support empty directories. In a traditional file system, you can create an empty directory. In Snowflake, a “directory” only exists as long as there are files with that prefix.

To simulate directory creation, the generated code writes a `.dummy` placeholder file to the target path using `COPY INTO`. This ensures the prefix exists and can be referenced by subsequent operations.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_create_output_directory
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_NewDirectory VARCHAR := public.GetControlVariableUDF('User_NewDirectory', 'package') :: VARCHAR;
   ---- Start block 'Package\Create Output Directory'
   --** SSC-FDM-SSIS0026 - SINCE SNOWFLAKE STAGES USE PREFIX-BASED PATHS, THE DIRECTORY IS CREATED BY WRITING A .DUMMY PLACEHOLDER FILE TO THE TARGET PATH VIA COPY INTO. **
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   EXECUTE IMMEDIATE CONCAT('COPY INTO ', :User_NewDirectory, '/.dummy FROM (SELECT ''empty'') FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE) OVERWRITE = TRUE SINGLE = TRUE');
   ---- End block 'Package\Create Output Directory'

END;
```

### Best Practices

- The `.dummy` file is a zero-overhead placeholder and can be left in place
- If the original SSIS task was configured with `OverwriteDestinationFile = False`, the `OVERWRITE = TRUE` clause is omitted, meaning the COPY INTO will fail if the `.dummy` file already exists (simulating “fail if directory exists”)
- Subsequent file operations to the same directory path will work correctly regardless of the `.dummy` file
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0027

SSIS Cache Transform duplicate key validation behavior difference

#### Description

This FDM is generated when a Cache Transform is configured with `TreatDuplicateKeysAsError = true`. SSIS enforces that validation at run time and fails the package on a duplicate key, while the dbt translation is a passthrough `SELECT` that does not enforce it, so duplicate rows flow through unchanged.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<property dataType="System.Boolean" name="TreatDuplicateKeysAsError">true</property>
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-SSIS0027 - SSIS CACHE TRANSFORM WITH TREATDUPLICATEKEYSASERROR=TRUE ENFORCES DUPLICATE KEY VALIDATION AT RUNTIME. IN THE DBT TRANSLATION, THIS VALIDATION IS NOT ENFORCED AND DUPLICATE ROWS WILL PASS THROUGH UNCHANGED. THE TRANSLATED SQL WORKS CORRECTLY AS A PASSTHROUGH. IF DUPLICATE KEY VALIDATION IS REQUIRED FOR DATA QUALITY, CONSIDER ADDING A DBT TEST OR UNIQUE CONSTRAINT. **
SELECT
   name,
   salary
FROM
   {{ ref('stg_raw__ole_db_source') }}
```

#### Best Practices

- Add a `unique` dbt test on the cache key when the duplicate-key validation was a data-quality guard
- Alternatively deduplicate explicitly with `QUALIFY ROW_NUMBER() OVER (PARTITION BY <key> ORDER BY ...) = 1` if the downstream lookup expects one row per key
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0028

SSIS FileSystemTask directory path translated to Snowflake stage prefix

#### Description

This FDM is generated when a File System Task operates on a directory. Snowflake stages use prefix-based paths rather than real directories, so the generated `REMOVE` with a trailing slash deletes every file that matches the prefix pattern instead of removing a directory entry.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<FileSystemData
  TaskOperationType="DeleteDirectory"
  TaskSourcePath="User::TempFolder"
  TaskIsSourceVariable="True" />
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.filesystemtask_delete_directory_variable_delete_temp_directory
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.filesystemtask_delete_directory_variable
AS
BEGIN
   CALL public.SetRunContext();
   LET User_TempFolder VARCHAR := public.GetControlVariableUDF('User_TempFolder', 'filesystemtask_delete_directory_variable') :: VARCHAR;
   ---- Start block 'Package\Delete Temp Directory'
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   --** SSC-FDM-SSIS0028 - SNOWFLAKE STAGES USE PREFIX-BASED PATHS, NOT REAL DIRECTORIES. THE REMOVE COMMAND WITH A TRAILING SLASH DELETES ALL FILES MATCHING THE PREFIX PATTERN. **
   REMOVE :User_TempFolder;
   ---- End block 'Package\Delete Temp Directory'

   CALL public.UpdateControlVariable('User_TempFolder', 'filesystemtask_delete_directory_variable', TO_VARIANT(:User_TempFolder));
END;
```

#### Best Practices

- Review the prefix value, because a broader prefix than intended removes every file underneath it — including files that were not in the original directory
- Remember that no directory entry survives the operation, so a later step that expected an empty directory to exist must recreate the placeholder
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SSIS0029

The SSIS task was disabled in the source package and has been commented out.

#### Description

This FDM is generated when a task or container was disabled in the source package. The task is still created in the Snowflake task graph so the dependency chain is preserved, but its body is commented out, so it performs no work when the graph runs.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<DTS:Executable
  DTS:refId="Package\disabled_expression"
  DTS:CreationName="Microsoft.ExpressionTask"
  DTS:Description="Expression Task"
  DTS:Disabled="True"
  DTS:DTSID="{709B3D47-E0CD-458F-BC45-BB3097F44DF0}"
  DTS:ExecutableType="Microsoft.ExpressionTask"
  DTS:LocaleID="-1"
  DTS:ObjectName="disabled_expression"
  DTS:ThreadHint="0">
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.disabled_expression_task_disabled_expression
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.disabled_expression_task
AS
--** SSC-FDM-SSIS0029 - THE SSIS TASK 'Package\disabled_expression' WAS DISABLED IN THE SOURCE PACKAGE AND HAS BEEN COMMENTED OUT. **
--User_message := UPPER(:User_message || 'message');
```

#### Best Practices

- Uncomment and review the generated body if the task was disabled only temporarily in the source package
- Remove the task from the graph entirely when the logic is obsolete, so the converted orchestration does not carry an empty step
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this FDM
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
