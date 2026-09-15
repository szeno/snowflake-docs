# Code Conversion - SSIS Conversion Issues

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This section provides detailed documentation for all Error, Warning, and Information (EWI) messages that SnowConvert may generate during SSIS to dbt conversion.

For assistance with any EWI, you can use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions, or contact [aim-support@snowflake.com](mailto:aim-support@snowflake.com) for additional support.

## SSC-EWI-SSIS0001

SSIS component requires manual implementation.

### Severity

Critical

### Description

This EWI is added when an SSIS component cannot be automatically converted to Snowflake SQL or dbt. The component is not supported by SnowConvert’s conversion engine and requires manual implementation. This typically occurs with custom components, third-party transformations, or components that have no direct equivalent in Snowflake’s architecture.

The conversion will place a placeholder comment in the generated code indicating where manual intervention is required.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
-- Component: ScriptComponent1 requires manual implementation
```

### Best Practices

- Review the original SSIS component’s logic and data transformation requirements
- If possible, implement equivalent functionality using Snowflake SQL, dbt models, or Snowflake stored procedures
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0002

SSIS expression requires manual translation to Snowflake SQL.

### Severity

High

### Description

This EWI is generated when an SSIS expression contains syntax that cannot be automatically translated to Snowflake SQL. This commonly occurs with:

- Complex nested expressions with unsupported functions
- SSIS-specific functions without direct Snowflake equivalents
- Malformed expressions (e.g., unbalanced parentheses)
- Expressions using unsupported operators or type conversions

The generated code will include a placeholder where the expression should be manually translated.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_simple_expression
WAREHOUSE=DUMMY_WAREHOUSE
AS
BEGIN
   LET User_message VARCHAR := public.GetControlVariableUDF('User_message', 'package_simple_expression') :: VARCHAR;
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: @[User::message] = UPPER( @[User::message] || ***/!!!
   ;
   CALL public.UpdateControlVariable('User_message', 'package_simple_expression', TO_VARIANT(:User_message));
END;
```

### Best Practices

- Carefully review the original SSIS expression logic
- If possible, manually translate the expression to valid Snowflake SQL syntax
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0003

Embedded SQL requires manual translation to Snowflake syntax.

### Severity

High

### Description

This EWI is added when SQL statements embedded in SSIS components (such as OLE DB Source, Lookup, or Execute SQL Task) cannot be automatically converted to Snowflake syntax. This typically occurs when:

- The source SQL dialect has syntax incompatible with Snowflake
- The SQL contains system-specific functions or objects
- The SQL uses features not supported in Snowflake

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL CANNOT BE CONVERTED FROM SQL SERVER TO SNOWFLAKE SQL ***/!!!
-- Original SQL: SELECT CustomerID, CustomerName FROM DimCustomer
--                WHERE CONVERT(VARCHAR, LastModified, 101) > '01/01/2020'
```

## SSC-EWI-SSIS0004

SSIS Control Flow Element requires manual implementation.

### Severity

High

### Description

This EWI is generated when an SSIS control flow element cannot be converted to Snowflake scripting. This can occur with various unsupported control flow tasks and containers, including but not limited to:

**Common Scenarios:**

- Control flow task types not yet supported by SnowConvert
- Container iteration logic that cannot be directly translated
- Complex control flow patterns without Snowflake equivalents
- Control flow elements with configurations that cannot be mapped to Snowflake

The specific control flow element that triggered this EWI will be identified in the error message, and manual implementation is required using Snowflake’s procedural SQL constructs.

### Common Cases

#### For Loop Container

For Loop containers emit `WHILE` when InitExpression, EvalExpression, and AssignExpression are present. This EWI is generated when those expressions are missing and the body runs once.

**Converted Code:**

Copy code

```
:force:

CREATE OR REPLACE TASK simpleforloop_package_for_loop_container
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.simpleforloop_package_execute_sql_task
AS
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT 'FORLOOP CONTAINER ITERATION LOGIC' CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
BEGIN
   -- Loop body tasks here
END;
```

**Best Practices for For Loop:**

- When the required expressions are missing, add explicit initialization, condition, and counter-update logic to the generated body

#### ForEach Loop Container (unsupported enumerators)

File, ADO, and From Variable enumerators are converted. Remaining ForEach enumerator types such as Item, NodeList, SMO, HDFS, and SchemaRowset emit this EWI. File enumerators that need stage mapping emit [SSC-EWI-SSIS0014](#ssc-ewi-ssis0014) instead.

**Converted Code:**

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT 'FOREACH CONTAINER ITERATION LOGIC' CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
FOR record IN cursor DO
   -- Loop body tasks here
END FOR;
```

**Best Practices for ForEach Loop:**

- For Item, NodeList, SMO, HDFS, and SchemaRowset enumerators, implement equivalent iteration with Snowflake Scripting

#### Other Unsupported Control Flow Elements

Other control flow tasks and elements that may generate this EWI include:

- Custom tasks without Snowflake equivalents
- Third-party control flow elements
- Certain configurations of standard tasks

## SSC-EWI-SSIS0005

Execute Package Task converted to asynchronous EXECUTE TASK.

### Severity

High

### Description

This EWI indicates that an SSIS Execute Package Task has been converted to a Snowflake TASK, which executes asynchronously by default. In SSIS, Execute Package Task runs synchronously within the parent package’s execution context. In Snowflake, EXECUTE TASK triggers the task to run asynchronously, which may affect orchestration logic, error handling, and variable passing between packages.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK parent_package_execute_package_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.parent_package_previous_task
AS
EXECUTE TASK public.childpackage_child_package;
-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0005 - THIS TASK RUNS ASYNCHRONOUSLY. Original SSIS Execute Package Task ran synchronously. ***/!!!
```

## SSC-EWI-SSIS0006

Execute Package Task variable bindings require manual implementation.

### Severity

High

### Description

This EWI is generated when an Execute Package Task contains variable bindings (parameter mappings between parent and child packages) that could not be automatically converted. SSIS allows parent packages to pass variable values to child packages through parameter bindings. This mechanism requires manual implementation in Snowflake.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0006 - SSIS EXECUTE PACKAGE TASK VARIABLE BINDINGS WERE NOT CONVERTED. ***/!!!
-- Original binding: ParentVariable -> ChildParam
-- Implement parameter passing mechanism manually
EXECUTE TASK public.childpackage;
```

## SSC-EWI-SSIS0007

Property expressions require manual implementation.

### Severity

High

### Description

This EWI is generated when an SSIS executable (task or container) uses property expressions to dynamically set properties at runtime, and these expressions could not be converted. Property expressions in SSIS allow dynamic configuration of task properties using expressions based on variables or parameters. In Snowflake, similar dynamic behavior must be implemented manually.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0007 - SSIS EXECUTABLE CONTAINS PROPERTY EXPRESSIONS that were not converted. ***/!!!
-- Original property expression: SqlStatementSource = @[User::SqlQuery]
-- Implement dynamic SQL logic manually
```

### Best Practices

- Use EXECUTE IMMEDIATE for dynamic SQL execution
- Validate dynamically constructed SQL to prevent injection risks
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0008

Execute Package Task references external package not in conversion scope.

### Severity

Medium

### Description

This EWI indicates that an Execute Package Task references a package that exists outside the current project or conversion scope. Ensure all dependent packages are available for the migration process.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0008 - EXECUTE PACKAGE TASK REFERENCES AN EXTERNAL PACKAGE ***/!!!
-- External package: C:\ExternalPackages\UtilityPackage.dtsx
-- Ensure this package is converted and accessible
EXECUTE TASK public.utilitypackage;
```

### Best Practices

- Create an inventory of all external package dependencies
- If possible, include external packages in the conversion scope
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0009

Unexpected error during component conversion.

### Severity

High

### Description

This EWI indicates that an unexpected error occurred during the conversion of a specific component. This is typically a rare occurrence and may be caused by:

- Corrupted package metadata
- Unusual component configuration
- Edge cases not covered by the converter

The component may have been partially converted. Review the generated code and contact support if the issue persists.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0009 - UNEXPECTED EXCEPTION CONVERTING COMPONENT. ***/!!!
-- Review component configuration and generated code
```

## SSC-EWI-SSIS0010

Multiple models write to the same destination table.

### Severity

High

### Description

This EWI is generated when multiple SSIS components write to the same destination table, resulting in multiple dbt models targeting the same table. This typically occurs when:

- Multiple Data Flow Tasks write to the same table
- Different packages in the same conversion write to the same table
- The same table is used as a destination in multiple transformations

### Converted Code

Copy code

```
:force:

-- Model 1: models/factsales.sql
-- Model 2: models/factsales_1.sql (automatically renamed)
-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0010 - A model associated with table 'FactSales' is already defined. ***/!!!
```

### Best Practices

- Review duplicate destination references in your packages
- If possible, consolidate multiple writes to the same table into a single model
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0011

Result binding configured for non-SELECT statement.

### Severity

High

### Description

This EWI is generated when an Execute SQL Task has a result binding configured (to capture query results into a variable), but the SQL statement is not a SELECT query. Result bindings only work with SELECT statements that return result sets. If the SQL statement is an INSERT, UPDATE, DELETE, or procedural statement, the result binding cannot be applied and must be manually addressed.

For non-query statements, consider using OUTPUT parameters or separate SELECT statements to retrieve values.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0011 - RESULT BINDING IS CONFIGURED FOR NON-QUERY STATEMENT. RESULT BINDING ONLY WORKS WITH SELECT QUERIES. ***/!!!
DELETE FROM Customers WHERE CustomerId = 1;
-- Original result binding: RowCount -> User::DeletedRows
```

### Best Practices

- Use separate SELECT statements to retrieve values after DML operations
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0012

XML result set requires manual implementation.

### Severity

High

### Description

This EWI is generated when an Execute SQL Task is configured to return results as XML, which is not directly supported in the conversion. SnowConvert supports SINGLEROW and FULLRESULTSET result types, but XML result sets require manual implementation.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0012 - XML RESULT SET TYPE IS NOT SUPPORTED. ONLY SINGLEROW AND FULLRESULTSET RESULT SET TYPES ARE SUPPORTED. ***/!!!
-- Original SQL: SELECT * FROM Customers FOR XML AUTO
-- Convert to supported result type or use JSON format
```

## SSC-EWI-SSIS0013

Complex property expression requires manual implementation.

### Severity

High

### Description

This EWI is generated when a property expression in an SSIS task contains patterns that cannot be automatically converted. SnowConvert supports simple property expressions such as:

- Single variable references: `@[User::VariableName]`
- Simple string concatenation: `"SELECT * FROM " + @[User::TableName]`

More complex patterns involving multiple operations, nested expressions, or complex string manipulation require manual conversion.

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0013 - PROPERTY EXPRESSION FOR SQLSTATEMENTSOURCE CONTAINS UNSUPPORTED PATTERNS. ONLY SINGLE VARIABLE REFERENCES OR SIMPLE STRING CONCATENATION WITH LITERALS AND VARIABLE REFERENCES IS SUPPORTED. ***/!!!
-- Implement complex expression logic manually
```

## SSC-EWI-SSIS0014

ForEach File Enumerator requires Snowflake stage mapping.

### Severity

High

### Description

This EWI is generated when a ForEach File Enumerator Container is used to iterate over files in a folder. In SSIS, this references local or network file system paths. In Snowflake, files must be staged in Snowflake internal or external stages. You must:

- Map the folder path to a Snowflake stage
- Replace the `<STAGE_PLACEHOLDER>` with your actual stage name
- Ensure files are uploaded to the stage before execution
- Implement the file enumeration logic using Snowflake’s LIST command

### Converted Code

Copy code

```
:force:

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - THE FOLDER PATH REQUIRES MANUAL MAPPING TO A SNOWFLAKE STAGE. ***/!!!
-- Original folder: C:\Data\InputFiles\
-- Replace <STAGE_PLACEHOLDER> with your stage name
-- Example: @my_stage/input_files/
DECLARE
   file_cursor CURSOR FOR
      SELECT relative_path
      FROM TABLE(RESULT_SCAN(
         SELECT system$list_files('<STAGE_PLACEHOLDER>')
      ))
      WHERE relative_path LIKE '%.csv';
```

### Best Practices

- Create a Snowflake stage for file storage
- Upload files to the stage using SnowSQL, Snowpipe, or cloud storage integration
- Update the stage reference in the generated code
- Test file enumeration with actual staged files
- Use Snowflake’s LIST command to verify files are accessible
- Document stage naming conventions for your project
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0015

Send Mail Task file attachments are not supported in Snowflake.

### Severity

High

### Description

This EWI is generated when an SSIS Send Mail Task is configured with file attachments. Snowflake’s `SYSTEM$SEND_EMAIL` procedure does not support sending file attachments directly. The email will be sent without the attachments.

To include file content in emails, you must upload files to a Snowflake stage and generate shareable links using `GET_PRESIGNED_URL()`.

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
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0015 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT FILE ATTACHMENTS. CONSIDER USING STAGED FILES WITH SHARED LINKS OR ALTERNATIVE DELIVERY METHODS. ***/!!!
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Report Attached', 'Please review the attached report.');
END;
```

### Best Practices

- Upload files to a Snowflake stage before sending the email
- Generate pre-signed URLs using `GET_PRESIGNED_URL(@stage_name, 'filename', expiration_seconds)`
- Include the shareable link in the email body instead of the attachment
- Consider using external file sharing services for large attachments
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0016

Send Mail Task email priority is not supported in Snowflake.

### Severity

Medium

### Description

This EWI is generated when an SSIS Send Mail Task is configured with a priority setting (High, Normal, or Low). Snowflake’s `SYSTEM$SEND_EMAIL` does not support email priority headers. The email will be sent without priority information.

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
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0016 - EMAIL PRIORITY SETTINGS (HIGH/NORMAL/LOW) ARE NOT SUPPORTED BY SYSTEM$SEND_EMAIL AND WILL BE IGNORED. ***/!!!
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Urgent Alert', 'Critical error detected.');
END;
```

### Best Practices

- Add priority indicators to the email subject line (e.g., `[URGENT]`, `[HIGH PRIORITY]`)
- No other manual action required for basic functionality
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0017

Send Mail Task file-based message source is not supported.

### Severity

High

### Description

This EWI is generated when an SSIS Send Mail Task uses a File Connection as the message source type. Snowflake’s `SYSTEM$SEND_EMAIL` requires the message body to be provided as a string value directly. Loading email content from external files is not supported during conversion.

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
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0017 - LOADING EMAIL BODY FROM A FILE CONNECTION IS NOT SUPPORTED. THE MESSAGE SOURCE MUST BE DIRECT INPUT OR FROM A VARIABLE. ***/!!!
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Newsletter', '');
END;
```

### Best Practices

- Load the file content into a Snowflake stage
- Read the file content using Snowflake functions and store it in a variable
- Pass the variable content to `SYSTEM$SEND_EMAIL`
- Consider migrating email templates to Snowflake tables or variables
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0018

Send Mail Task HTML body format is not supported in Snowflake.

### Severity

Medium

### Description

This EWI is generated when an SSIS Send Mail Task is configured with HTML body format. Snowflake’s `SYSTEM$SEND_EMAIL` only supports plain text email bodies. HTML tags will appear as literal text in the email and will not be rendered.

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
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0018 - SYSTEM$SEND_EMAIL ONLY SUPPORTS PLAIN TEXT EMAIL BODIES. HTML FORMATTING WILL NOT BE PRESERVED. ***/!!!
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Formatted Report', '<html><body><h1>Report</h1><p>Status: <b>Success</b></p></body></html>');
END;
```

### Best Practices

- Convert HTML content to plain text before sending
- Use text formatting conventions like asterisks for emphasis (`*bold*`)
- Use ASCII art or spacing for tabular data
- Consider using external email services if HTML formatting is required
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0019

SSIS Character Map operation `'ByteReversal'` (`MapFlags=2048`) is not supported in Snowflake.

### Severity

Medium

#### Description

This EWI is generated when a Character Map transformation uses an operation that has no Snowflake equivalent. Only the Uppercase (`512`) and Lowercase (`256`) operations are translated to `UPPER()` and `LOWER()`; every other `MapFlags` value — byte reversal, Hiragana, Katakana, half width, full width, linguistic casing, Simplified or Traditional Chinese — is reported and the column passes through unchanged.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<component
  refId="Package\Data Flow Task\Character Map"
  componentClassID="Microsoft.CharacterMap"
  usesDispositions="true"
  name="Character Map"
  version="2">
  <inputs>
    <input
      refId="Package\Data Flow Task\Character Map.Inputs[Character Map Input]"
      name="Character Map Input">
      <inputColumns>
        <inputColumn
          refId="Package\Data Flow Task\Character Map.Inputs[Character Map Input].Columns[FullName]"
          cachedDataType="wstr"
          cachedLength="100"
          cachedName="FullName"
          errorOrTruncationOperation="Map Column"
          lineageId="Package\Data Flow Task\OLE DB Source.Outputs[OLE DB Source Output].Columns[FullName]"
          truncationRowDisposition="FailComponent"
          usageType="readWrite">
          <properties>
            <property dataType="System.UInt32" name="MapFlags">2048</property>
          </properties>
        </inputColumn>
      </inputColumns>
    </input>
  </inputs>
</component>
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0019 - SSIS CHARACTER MAP OPERATION 'ByteReversal' (MAPFLAGS=2048) IS NOT SUPPORTED IN SNOWFLAKE. ONLY UPPERCASE (512) AND LOWERCASE (256) OPERATIONS ARE TRANSLATED. THIS COLUMN PASSES THROUGH UNCHANGED. ***/!!!
WITH source_data AS
(
   SELECT
      FullName,
      Score
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   FullName,
   Score
FROM
   source_data
```

#### Best Practices

- Review whether the mapped operation is required downstream; the column keeps its original value, so any consumer that expected the transformed text needs to be adjusted
- Implement the operation with Snowflake string functions where an equivalent exists, or with a UDF for the locale-specific conversions
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0020

Bulk Insert Task native data file type is not supported in Snowflake.

### Severity

Critical

### Description

This EWI is generated when an SSIS Bulk Insert Task is configured with `DataFileType` set to `DTSBulkInsert_DataFileType_Native` or `DTSBulkInsert_DataFileType_WideNative`. These binary formats are SQL Server proprietary and cannot be read by Snowflake’s COPY INTO command.

Native data files store data in SQL Server’s internal binary format for faster bulk operations. Since Snowflake cannot interpret these formats, the source data must be exported to a supported format (CSV, JSON, Parquet, etc.) before migration.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0020 - SSIS BULKINSERTTASK NATIVE OR WIDENATIVE DATA FILE TYPE IS NOT SUPPORTED IN SNOWFLAKE. EXPORT SOURCE DATA TO CSV FORMAT BEFORE MIGRATION. ***/!!!
   COPY INTO target_table
   FROM '@{STAGE_PLACEHOLDER}'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- Export data from SQL Server to CSV or another supported format before migration
- Consider Parquet format for better performance with large datasets
- Update the FILE\_FORMAT in the generated code to match your exported format
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0021

Bulk Insert Task LastRow option is not supported in Snowflake.

### Severity

High

### Description

This EWI is generated when an SSIS Bulk Insert Task specifies a `LastRow` value to limit the number of rows loaded. Snowflake’s COPY INTO command does not support stopping at a specific row number.

To achieve similar functionality, you must load the data into a staging table and then use SQL with ROW\_NUMBER() and LIMIT to select the desired row range.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0021 - SSIS BULKINSERTTASK LASTROW OPTION IS NOT SUPPORTED IN SNOWFLAKE. USE TEMPORARY TABLE WITH ROW_NUMBER AND LIMIT/OFFSET TO SELECT SPECIFIC ROW RANGE. ***/!!!
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV', SKIP_HEADER = 1);
END;
```

### Best Practices

- Load data into a staging table first, then use SQL to filter rows
- Consider pre-processing the source file to contain only the needed rows
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Load all data to a staging table, then insert only the rows up to the desired LastRow value:

Copy code

```
:force:

-- Step 1: Load all data to staging
COPY INTO staging_table FROM '@my_stage' FILE_FORMAT = (TYPE = 'CSV');

-- Step 2: Insert only rows up to LastRow value (e.g., 1000)
INSERT INTO target_table
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS rn
  FROM staging_table
) WHERE rn <= 1000;
```

## SSC-EWI-SSIS0022

Bulk Insert Task FireTriggers option is not supported in Snowflake.

### Severity

Medium

### Description

This EWI is generated when an SSIS Bulk Insert Task has the `FireTriggers` option enabled. In SQL Server, this option causes INSERT triggers to fire during the bulk load operation. Snowflake does not have traditional database triggers.

To implement trigger-like behavior in Snowflake, use Streams and Tasks to detect and process data changes after the load completes.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0022 - SSIS BULKINSERTTASK FIRETRIGGERS OPTION IS NOT SUPPORTED IN SNOWFLAKE. CONSIDER USING SNOWFLAKE STREAMS AND TASKS TO IMPLEMENT TRIGGER-LIKE BEHAVIOR. ***/!!!
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- Review the original SQL Server trigger logic
- Create a Snowflake Stream on the target table to capture data changes
- Create a scheduled Task to process the stream data (equivalent to trigger logic)
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Implement trigger-like behavior using Snowflake Streams and Tasks:

Copy code

```
:force:

-- Step 1: Create a stream to capture inserts
CREATE OR REPLACE STREAM target_table_stream ON TABLE target_table;

-- Step 2: Create a task to process the stream (trigger logic)
CREATE OR REPLACE TASK process_inserts
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 minute'
  WHEN SYSTEM$STREAM_HAS_DATA('target_table_stream')
AS
  INSERT INTO audit_table
  SELECT *, CURRENT_TIMESTAMP()
  FROM target_table_stream
  WHERE METADATA$ACTION = 'INSERT';
```

## SSC-EWI-SSIS0023

Bulk Insert Task FormatFile is not supported in Snowflake.

### Severity

Medium

### Description

This EWI is generated when an SSIS Bulk Insert Task uses a format file (`.fmt` or `.xml`) to define the data layout. Snowflake does not support SQL Server format files. Instead, you must create an equivalent Snowflake FILE FORMAT object that defines the same parsing rules.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0023 - SSIS BULKINSERTTASK FORMAT FILE IS NOT SUPPORTED IN SNOWFLAKE. CREATE EQUIVALENT FILE FORMAT OBJECT MANUALLY BASED ON FORMAT FILE CONTENTS. ***/!!!
   COPY INTO target_table
   FROM '@my_stage'
   FILE_FORMAT = (TYPE = 'CSV');
END;
```

### Best Practices

- Review the original format file to understand field definitions, terminators, and data types
- Create an equivalent Snowflake FILE FORMAT object
- For complex format files with column mappings, consider using a staging table with explicit column selection
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Create an equivalent Snowflake FILE FORMAT based on the format file contents:

Copy code

```
:force:

CREATE OR REPLACE FILE FORMAT my_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('', 'NULL');
```

## SSC-EWI-SSIS0024

Bulk Insert Task stage and file upload not included in translation.

### Severity

Medium

### Description

This EWI is always generated for Bulk Insert Task conversions to remind you that Snowflake requires files to be staged before they can be loaded. Unlike SSIS which can read directly from file system paths, Snowflake’s COPY INTO command requires files to be in a Snowflake stage (internal or external).

You must create a stage, upload your source files, and replace the `{STAGE_PLACEHOLDER}` in the generated code with your actual stage name.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_bulk_insert_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0024 - THE STAGE AND FILE UPLOAD ARE NOT INCLUDED IN THE TRANSLATION. CREATE A SNOWFLAKE STAGE AND UPLOAD THE SOURCE FILE BEFORE EXECUTING THE COPY INTO STATEMENT. REPLACE {STAGE_PLACEHOLDER} WITH YOUR STAGE NAME. ***/!!!
   COPY INTO target_table
   FROM '@{STAGE_PLACEHOLDER}'
   PATTERN = '.*data_file.*'
   FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER = ',', RECORD_DELIMITER = '\n')
   ON_ERROR = CONTINUE;
END;
```

### Best Practices

- Create a Snowflake stage for your source files
- Upload files using SnowSQL CLI with the PUT command
- Replace `{STAGE_PLACEHOLDER}` with your stage name in the generated code
- Verify files are staged correctly using `LIST @my_stage;`
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Create a stage and upload your source files before executing the COPY INTO:

Copy code

```
:force:

-- 1. Create a stage
CREATE OR REPLACE STAGE my_bulk_stage;

-- 2. Upload file using SnowSQL CLI
-- PUT file:///path/to/data.csv @my_bulk_stage AUTO_COMPRESS = FALSE;

-- 3. Replace @{STAGE_PLACEHOLDER} in generated code
```

## SSC-EWI-SSIS0025

Flat File Source stage path variable requires manual mapping to a Snowflake stage.

### Severity

High

### Description

This EWI is generated when a Flat File Source component references a stage path variable that must be manually mapped to a Snowflake stage. In SSIS, Flat File Source components read directly from file system paths. In Snowflake, files must be staged before they can be queried. The generated code uses a dbt variable for the stage path, which must be updated to point to the actual Snowflake stage containing the source file.

### Converted Code

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0025 - FLAT FILE SOURCE STAGE PATH VARIABLE 'Data_Flow_Task_Flat_File_Source_stage_path' REQUIRES MANUAL MAPPING TO A SNOWFLAKE STAGE. ***/!!!
SELECT
   $1 :: NUMERIC AS id,
   $2 :: VARCHAR(100) AS name,
   $3 :: NUMERIC(10, 2) AS amount,
   $4 :: DATE AS order_date
FROM
   @{{ var('Data_Flow_Task_Flat_File_Source_stage_path') }} (FILE_FORMAT => 'TestPackage_Data_Flow_Task_Flat_File_Source')
WHERE
   METADATA$FILE_ROW_NUMBER > 1
```

### Best Practices

- Create a Snowflake stage and upload your flat files before execution
- Update the stage path variable in the task CONFIG section to point to your Snowflake stage (e.g., `@my_stage/input_files/`)
- Verify the FILE\_FORMAT object matches your source file’s delimiters and encoding
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0026

SSIS property expression is not supported.

### Severity

High

### Description

This EWI is generated when an SSIS component uses a property expression that cannot be converted to Snowflake. Property expressions in SSIS dynamically set component properties at runtime using SSIS expression syntax. Certain property expressions — particularly those referencing project parameters, complex concatenations, or unsupported expression functions — cannot be automatically translated. The original expression is preserved in the generated code as a comment for manual resolution.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.TestPackage
CONFIG = $${
  "package": {
    "Data_Flow_Task_Flat_File_Source_stage_path": {"value": "!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0026 - PROPERTY EXPRESSION 'ConnectionString' IS NOT SUPPORTED. **/ @[$Project::FlatFileDir] + \"\\\\input.csv\"", "type": "VARCHAR", "is_parameter": false}
  }
}$$
AS
BEGIN
   LET config VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('package');
   LET scope VARCHAR := 'TestPackage';
   CALL public.ClearVariables(:scope);
   CALL public.InitVariablesFromConfig(:scope, :config);
END;
```

### Best Practices

- Review the original SSIS property expression and manually implement the equivalent logic
- For connection string expressions, replace with the actual Snowflake stage path or connection reference
- Use dbt variables (`{{ var('...') }}`) or Snowflake task CONFIG parameters for runtime configuration
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0027

Flat File Source connection manager not found.

### Severity

High

### Description

This EWI is generated when a Flat File Source component references a connection manager that cannot be found in the SSIS package. This typically occurs when:

- The connection manager is defined at the project level and not embedded in the `.dtsx` package
- The connection manager reference is broken or misconfigured
- The `.conmgr` file is missing from the project

Without the connection manager, SnowConvert cannot determine the file path, format, or column definitions, so the generated code contains null placeholder columns.

### Converted Code

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0027 - FLAT FILE SOURCE CONNECTION MANAGER NOT FOUND. ***/!!!
SELECT
   null AS col_a,
   null AS col_b
```

### Best Practices

- Locate the missing connection manager (`.conmgr` file) and include it in the conversion scope
- Verify the connection manager reference ID matches between the Data Flow component and the package
- Manually define the source query with the correct columns and stage path
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0028

Excel Source error row redirection requires alternative implementation.

### Severity

High

### Description

This EWI appears in the migration assessment report when an SSIS Excel Source component has an error output configured with `RedirectRow` disposition. In SSIS, error rows can be redirected to a separate output for logging or reprocessing. This pattern cannot be directly translated to Snowflake SQL.

The generated dbt model processes all rows without error redirection. To achieve similar error handling behavior in Snowflake, use `TRY_TO_*` casting functions with error flag columns for defensive error handling, and create separate error capture models if needed.

### Converted Code

The generated dbt model reads data normally without error handling:

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
      TRY_TO_DOUBLE(data['id'] :: VARCHAR) AS id,
      data['name'] :: VARCHAR AS name
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
```

To add error row redirection, modify the model like this:

Copy code

```
:force:

-- Add an error flag column to identify rows with conversion issues
SELECT
   TRY_TO_DOUBLE(data['id'] :: VARCHAR) AS id,
   data['name'] :: VARCHAR AS name,
   CASE WHEN TRY_TO_DOUBLE(data['id'] :: VARCHAR) IS NULL AND data['id'] :: VARCHAR IS NOT NULL THEN TRUE ELSE FALSE END AS _has_error
FROM
   excel_raw_data
```

### Best Practices

- Use `TRY_TO_NUMBER`, `TRY_TO_DATE`, and other `TRY_TO_*` functions for defensive casting
- Add error flag columns to identify rows with conversion issues
- Create a separate dbt model to capture and log error rows: `SELECT * FROM {{ ref('my_model') }} WHERE _has_error = TRUE`
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0029

Excel Source parameterized queries require dbt vars or macros.

### Severity

High

### Description

This EWI appears in the migration assessment report when an SSIS Excel Source component uses parameter mappings to pass runtime values into the query. SSIS allows parameterized queries in Excel Source using `?` placeholders bound to SSIS variables. This pattern cannot be directly translated.

The generated dbt model reads the full Excel sheet without applying parameter filtering. You must manually add the equivalent filtering using dbt `var()` functions or Jinja templating.

### Converted Code

The generated dbt model reads all data from the sheet:

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
      data['ProductName'] :: VARCHAR AS ProductName,
      TRY_TO_DOUBLE(data['Quantity'] :: VARCHAR) AS Quantity
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
-- Add equivalent parameter filtering here:
-- WHERE ProductName = '{{ var("filter_product") }}'
```

### Best Practices

- Replace SSIS parameter placeholders with dbt `{{ var('param_name') }}` references
- Pass values at runtime using `dbt run --vars '{"param_name": "value"}'`
- Add WHERE clauses or CTE filters to replicate the original parameterized query logic
- Consider using dbt macros for complex parameterized logic
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0030

Excel Source project-level connection manager requires external resolution.

### Severity

Medium

### Description

This EWI appears in the migration assessment report when an SSIS Excel Source component references a connection manager defined at the project level (in a `.conmgr` file) rather than embedded in the `.dtsx` package. SnowConvert cannot automatically resolve project-level connection managers because the `.conmgr` file may not be included in the conversion scope.

The generated dbt model may use a placeholder or default stage path. You must locate the corresponding `.conmgr` file and extract the `ConnectionString` property to determine the Excel file path and HDR (header row) setting, then update the stage file path variable in `dbt_project.yml`.

### Converted Code

The generated dbt model uses a stage file path variable that needs to be updated:

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
      data['Column1'] :: VARCHAR AS Column1
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
```

### Best Practices

- Locate the `.conmgr` file in your SSIS project directory — it will be named after the connection manager
- Open the `.conmgr` file and find the `ConnectionString` property to get the Excel file path and `HDR=YES/NO` setting
- Include `.conmgr` files in the conversion input folder and re-run the conversion for better results
- Update the `stage_file_path` variable in `dbt_project.yml` to point to your Snowflake stage
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0031

Excel Source CONFIG variable requires manual mapping.

### Severity

Medium

### Description

This EWI appears in the migration assessment report when the conversion creates a CONFIG variable for an Excel Source stage file path. The generated orchestration task includes a CONFIG section with a default value derived from the original SSIS package’s connection string. You must update this variable to reference the correct Snowflake stage and Excel file path before execution.

The default value follows the pattern `@excel_source_stage/<filename>.xlsx` and is also registered in `dbt_project.yml` under the `vars:` section.

### Converted Code

The orchestration task includes the stage file path as a CONFIG variable:

Copy code

```
:force:

CREATE OR REPLACE TASK public.my_package
WAREHOUSE=DUMMY_WAREHOUSE
CONFIG = $${
  "package": {
    "Data_Flow_Task_Excel_Source_stage_file_path": {"value": "@excel_source_stage/sales_data.xlsx", "type": "VARCHAR", "is_parameter": false}
  }
}$$
AS
BEGIN
   LET config VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('package');
   LET scope VARCHAR := 'my_package';
   CALL public.ClearVariables(:scope);
   CALL public.InitVariablesFromConfig(:scope, :config);
END;
```

### Best Practices

- Upload your Excel file to a Snowflake stage: `PUT file:///path/to/sales_data.xlsx @my_stage AUTO_COMPRESS = FALSE;`
- Update the CONFIG variable value to point to the staged file (e.g., `@my_stage/sales_data.xlsx`)
- Also update the corresponding variable in `dbt_project.yml` under `vars:`
- Verify the file is accessible from the stage using `LIST @my_stage;`
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0032

Excel Source variable-based access mode not supported.

### Severity

High

### Description

This EWI appears in the migration assessment report when an SSIS Excel Source component uses a variable-based access mode to dynamically resolve the sheet name or SQL query at runtime. SSIS supports four access modes:

- **0**: Table or view (static sheet name) — supported
- **1**: Table name or view name from variable — **not supported**
- **2**: SQL command (static query) — supported
- **3**: SQL command from variable — **not supported**

For modes 1 and 3, the sheet name or query is stored in an SSIS variable and resolved at runtime. This dynamic resolution cannot be automatically translated. The generated model reads the full sheet using the static `OpenRowset` value from the component configuration. You must manually add the dynamic sheet or query logic using dbt vars.

### Converted Code

The generated dbt model uses the static sheet name from the component definition:

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

### Best Practices

- Replace the static sheet name with a dbt `{{ var('sheet_name') }}` reference if it needs to be dynamic
- Pass the sheet name at runtime using `dbt run --vars '{"sheet_name": "Sheet1"}'`
- If the variable resolved to a SQL command (access mode 3), convert the query logic to WHERE clauses or CTEs in the dbt model
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0033

Excel Source SQL command filtering logic not preserved.

### Severity

Medium

### Description

This EWI appears in the migration assessment report when an SSIS Excel Source component uses the SQL Command access mode (mode 2) with a query that includes filtering, joins, or aggregation logic. For example, the original SSIS component might use `SELECT * FROM [Sheet1$] WHERE Status = 'Active'`.

The generated dbt model reads the full Excel sheet via the `excel_source_udf` UDF and does not apply the original SQL filtering. You must add the equivalent filtering as downstream CTEs or WHERE clauses in the dbt model.

### Converted Code

The generated dbt model reads all data from the sheet without the original SQL filtering:

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
      data['ProductName'] :: VARCHAR AS ProductName,
      data['Status'] :: VARCHAR AS Status,
      TRY_TO_DOUBLE(data['Quantity'] :: VARCHAR) AS Quantity
   FROM
      excel_raw_data
)
SELECT
   *
FROM
   parsed_data
-- Original SSIS SQL: SELECT * FROM [Sheet1$] WHERE Status = 'Active'
-- Add the equivalent filtering:
WHERE
   Status = 'Active'
```

### Best Practices

- Check the assessment report for the original SQL command text
- Add the equivalent WHERE clause, JOINs, or aggregation as CTEs in the dbt model
- Test the output row count to ensure it matches the original SSIS component’s results
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0034

Flat file format is not supported.

### Severity

High

### Description

This EWI is generated when an SSIS Flat File Source component uses a file format that cannot be automatically converted to Snowflake. Snowflake’s COPY INTO command and FILE\_FORMAT objects support delimited (CSV) files but do not directly support certain SSIS flat file formats such as:

- **FixedWidth**: Files where columns are defined by character position and width
- **RaggedRight**: Files where the last column has a variable length delimiter

For these formats, the source file must be pre-processed or transformed into a delimited format before loading into Snowflake.

### Converted Code

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0034 - FLAT FILE FORMAT 'FixedWidth' IS NOT SUPPORTED. ***/!!!
SELECT
   null AS col_a,
   null AS col_b
```

### Best Practices

- Convert FixedWidth files to CSV or another delimited format before staging in Snowflake
- For RaggedRight files, add a consistent delimiter to the last column
- Use Python UDFs or external functions for complex format transformations
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0035

Non-standard header row delimiter is not supported.

### Severity

High

### Description

This EWI is generated when an SSIS Flat File connection manager specifies a header row delimiter that is not a newline character. Snowflake’s FILE\_FORMAT expects header rows to be terminated by the standard record delimiter (typically `\n` or `\r\n`). Non-standard header row delimiters cannot be configured in Snowflake.

### Converted Code

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0035 - FLAT FILE HEADER ROW DELIMITER IS NOT A NEWLINE CHARACTER. THIS IS NOT SUPPORTED. ***/!!!
SELECT
   $1 :: VARCHAR(50) AS col_a,
   $2 :: VARCHAR(50) AS col_b
FROM
   @{{ var('Data_Flow_Task_Flat_File_Source_stage_path') }} (FILE_FORMAT => 'TestPackage_Data_Flow_Task_Flat_File_Source')
WHERE
   METADATA$FILE_ROW_NUMBER > 1
```

### Best Practices

- Pre-process the source file to replace the non-standard header delimiter with a newline character
- Alternatively, remove the header row and use `SKIP_HEADER = 0` in the FILE\_FORMAT
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0036

Flat File Source feature is not supported.

### Severity

High

### Description

This EWI is generated when a Flat File Source component uses a feature that is not supported by SnowConvert’s conversion engine. The specific unsupported feature is identified in the EWI message. Common unsupported features include:

- **Multiple Flat Files connection manager**: Connection managers configured to read from multiple files simultaneously
- **Per-column delimiters**: Different delimiters for individual columns
- **Per-column text qualified settings**: Individual text qualifier settings per column
- **Unsupported CodePage**: Character encoding not supported by Snowflake
- **Unsupported LocaleID**: Locale-specific formatting not supported by Snowflake
- **Multi-character text qualifier**: Text qualifiers longer than a single character

### Converted Code

Copy code

```
:force:

!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0036 - MULTIPLE FLAT FILES CONNECTION MANAGER IS NOT SUPPORTED. ***/!!!
SELECT
   null AS col_a,
   null AS col_b
```

### Best Practices

- Review the specific unsupported feature identified in the EWI message
- For multiple flat files, use Snowflake’s PATTERN option in COPY INTO to load multiple files from a stage
- For per-column delimiters, pre-process the file to use a uniform delimiter
- For unsupported code pages, convert the file encoding to UTF-8 before staging
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0037

SSIS expression function not reviewed for Snowflake equivalence.

### Severity

Medium

### Description

This EWI is generated when an SSIS expression uses a function that has not been reviewed for Snowflake equivalence. The function has been passed through to the generated code as-is, but it may not exist or behave differently in Snowflake. Manual review is required to verify or replace the function with the appropriate Snowflake equivalent.

### Converted Code

Copy code

```
:force:

WITH source_data AS
(
   SELECT
      Name
   FROM
      {{ ref('stg_raw__ole_db_source') }}
)
SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0037 - SSIS EXPRESSION FUNCTION 'TOKEN' HAS NOT BEEN REVIEWED FOR SNOWFLAKE EQUIVALENCE ***/!!!
   TOKEN(Name, ',', 1) AS TokenResult,
   Name AS Name
FROM
   source_data
```

### Best Practices

- Look up the SSIS expression function in the [SSIS Expression Reference](https://learn.microsoft.com/en-us/sql/integration-services/expressions/functions-ssis-expression) to understand its behavior
- Find the equivalent Snowflake function (e.g., SSIS `TOKEN` → Snowflake `SPLIT_PART`)
- Replace the function call with the Snowflake equivalent and test the output
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0038

SSIS FileSystemTask path requires manual mapping to a Snowflake stage.

### Severity

High

### Description

This EWI is generated when an SSIS File System Task uses a File Connection Manager to reference a file or directory path. In SSIS, File System Tasks operate directly on local or network file system paths. In Snowflake, file operations use stages instead of file system paths.

The generated code uses `@<STAGE_PLACEHOLDER>` where the original path was. You must replace this placeholder with the actual Snowflake stage and path that corresponds to the original file location.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_delete_report_file
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   ---- Start block 'Package\Delete Report File'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0038 - THE PATH(S) REQUIRES MANUAL MAPPING TO A SNOWFLAKE STAGE(S). ***/!!!
   EXECUTE IMMEDIATE 'REMOVE @<STAGE_PLACEHOLDER>/Data/Input/report.txt';
   ---- End block 'Package\Delete Report File'

END;
```

### Best Practices

- Replace `@<STAGE_PLACEHOLDER>` with your actual Snowflake stage name (e.g., `@my_stage`)
- Create the stage if it does not exist: `CREATE OR REPLACE STAGE my_stage;`
- Ensure files are uploaded to the stage before executing file operations
- For operations referencing multiple paths, each `@<STAGE_PLACEHOLDER>` may map to a different stage
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0039

SSIS FileSystemTask overwrite=false not supported in Snowflake.

### Severity

High

### Description

This EWI is generated when an SSIS File System Task is configured with `OverwriteDestinationFile = False`. In SSIS, this setting causes the task to fail if the destination file or directory already exists, providing a safety guard against accidental overwrites.

Snowflake’s `COPY FILES INTO` command always silently overwrites existing files at the destination. There is no built-in mechanism to check for file existence before copying. If your workflow depends on the fail-if-exists behavior, you must implement a manual check.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_copy_file_no_overwrite
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_SourceFilePath VARCHAR := public.GetControlVariableUDF('User_SourceFilePath', 'package') :: VARCHAR;
   LET User_DestFilePath VARCHAR := public.GetControlVariableUDF('User_DestFilePath', 'package') :: VARCHAR;
   ---- Start block 'Package\Copy File No Overwrite'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0039 - THE ORIGINAL SSIS TASK WAS CONFIGURED TO FAIL IF THE DESTINATION EXISTS. SNOWFLAKE DOES NOT SUPPORT THIS BEHAVIOR AND WILL SILENTLY OVERWRITE. ***/!!!
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   EXECUTE IMMEDIATE CONCAT('COPY FILES INTO ', :User_DestFilePath, ' FROM ', :User_SourceFilePath);
   ---- End block 'Package\Copy File No Overwrite'

END;
```

### Best Practices

- If fail-if-exists behavior is required, add a pre-check using `LIST @stage/path` and raise an error if the file exists
- Consider using `SYSTEM$STREAM_HAS_DATA` or a control table to track file processing state
- Review whether the overwrite guard is critical to your workflow or simply a safety measure
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

#### Manual Support

Implement a file existence check before copying:

Copy code

```
:force:

-- Check if destination file exists before copying
LET file_count INTEGER := (SELECT COUNT(*) FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   WHERE "name" LIKE '%dest_file.csv%');
IF (:file_count > 0) THEN
   RAISE 'Destination file already exists. Aborting copy to prevent overwrite.';
END IF;
```

## SSC-EWI-SSIS0041

SSIS FileSystemTask references an external or unresolvable connection manager.

### Severity

High

### Description

This EWI is generated when an SSIS File System Task references a connection manager for its source or destination path that is not defined within the `.dtsx` package file. This typically occurs when the connection manager is defined at the project level (in a `.conmgr` file) or when the reference is broken.

Without the connection manager definition, SnowConvert cannot resolve the file path. The unresolvable path is replaced with `@<STAGE_PLACEHOLDER>` in the generated code.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_copy_from_external_source
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_DestFilePath VARCHAR := public.GetControlVariableUDF('User_DestFilePath', 'package') :: VARCHAR;
   ---- Start block 'Package\Copy From External Source'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0041 - THE CONNECTION MANAGER REFERENCED BY TASKSOURCEPATH OR TASKDESTINATIONPATH IS NOT DEFINED IN THE DTSX FILE. IT MAY BE A PROJECT-LEVEL CONNECTION MANAGER. THE PATH CANNOT BE RESOLVED. ***/!!!
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   EXECUTE IMMEDIATE CONCAT('COPY FILES INTO ', :User_DestFilePath, ' FROM @<STAGE_PLACEHOLDER>');
   ---- End block 'Package\Copy From External Source'

END;
```

### Best Practices

- Locate the missing connection manager in your SSIS project (check for `.conmgr` files)
- Include `.conmgr` files in the conversion input folder and re-run the conversion
- Replace `@<STAGE_PLACEHOLDER>` with the correct Snowflake stage path derived from the connection manager’s file path
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0043

SSIS FileSystemTask SetAttributes operation not supported in Snowflake.

### Severity

High

### Description

This EWI is generated when an SSIS File System Task is configured with the `SetAttributes` operation. In SSIS, this operation sets file system attributes such as Read-Only, Hidden, Archive, or System on a file or directory. Snowflake stages do not support file attributes — all staged files are accessible without attribute-based access control.

The generated code contains an empty statement (`;`) with diagnostic comments preserving the original task configuration for reference.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_set_file_attributes
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   ---- Start block 'Package\Set File Attributes'
   ---- TaskOperationType="SetAttributes"
   ---- TaskSourcePath="Data/report.txt"
   ---- TaskIsSourceVariable="False"
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0043 - SNOWFLAKE STAGES DO NOT SUPPORT FILE ATTRIBUTES (READ-ONLY, HIDDEN, ETC.). THIS OPERATION CANNOT BE TRANSLATED. ***/!!!
    ;
   ---- End block 'Package\Set File Attributes'

END;
```

### Best Practices

- Review whether the file attribute setting is critical to your workflow
- If access control is needed, use Snowflake role-based access control (RBAC) on the stage instead
- The empty statement can be safely removed if no alternative is needed
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0044

SSIS FileSystemTask COPY FILES destination appends source filename.

### Severity

High

### Description

This EWI is generated for every file-level copy, move, or rename operation in an SSIS File System Task. Snowflake’s `COPY FILES INTO` command treats the destination as a directory prefix and appends the source filename automatically. This means:

- If your SSIS task copies `source.csv` to a destination path `@stage/output/renamed.csv`, the actual result will be `@stage/output/renamed.csv/source.csv` — which is likely not the intended behavior
- If the destination is a directory path (e.g., `@stage/output/`), the behavior is correct

Review the destination path in the generated code and adjust manually if the destination refers to a specific file rather than a directory.

### Converted Code

Copy code

```
:force:

CREATE OR REPLACE TASK public.package_copy_data_file
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   LET User_SourceFilePath VARCHAR := public.GetControlVariableUDF('User_SourceFilePath', 'package') :: VARCHAR;
   LET User_DestFilePath VARCHAR := public.GetControlVariableUDF('User_DestFilePath', 'package') :: VARCHAR;
   ---- Start block 'Package\Copy Data File'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0044 - THE COPY FILES COMMAND TREATS THE DESTINATION AS A DIRECTORY PREFIX AND APPENDS THE SOURCE FILENAME. IF THE DESTINATION PATH REFERS TO A SPECIFIC FILE RATHER THAN A DIRECTORY, THE RESULTING PATH MAY BE INCORRECT. REVIEW AND ADJUST MANUALLY IF NEEDED. ***/!!!
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   EXECUTE IMMEDIATE CONCAT('COPY FILES INTO ', :User_DestFilePath, ' FROM ', :User_SourceFilePath);
   ---- End block 'Package\Copy Data File'

END;
```

### Best Practices

- If the destination is a directory, the generated code works correctly as-is
- If the destination is meant to be a specific filename (rename scenario), use a two-step approach: copy to a directory, then rename using `COPY FILES INTO` + `REMOVE`
- For move operations, verify that the source file is correctly removed after the copy
- Use the Snowflake AIM Agent for Data Warehouses to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0046

SSIS system variable `'StartTime'` is not supported.

### Severity

Medium

#### Description

This EWI is generated when an SSIS expression or Execute SQL Task references a system variable that has no equivalent in Snowflake task graphs. System variables that do map — such as `UserName`, `PackageName`, `PackageID`, and `ExecutionInstanceGUID` — are replaced with `CURRENT_USER()` and `SYSTEM$TASK_RUNTIME_INFO(...)` calls, while the remaining ones are reported and left unresolved.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<SQLTask:ParameterBinding
  SQLTask:ParameterName="3"
  SQLTask:DtsVariableName="System::StartTime"
  SQLTask:ParameterDirection="Input"
  SQLTask:DataType="129"
  SQLTask:ParameterSize="255" />
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.package2_execute_sql_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package2
AS
BEGIN
   ---- Start block 'Package\Execute SQL Task'
   INSERT INTO etl_results.package_system_variables (username, packagename, packageid, starttime, executioninstanceguid) VALUES (CURRENT_USER(), SYSTEM$TASK_RUNTIME_INFO('CURRENT_ROOT_TASK_NAME'), SYSTEM$TASK_RUNTIME_INFO('CURRENT_ROOT_TASK_UUID'),
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0046 - THE SSIS SYSTEM VARIABLE 'StartTime' DOES NOT HAVE A DIRECT EQUIVALENT IN SNOWFLAKE TASK GRAPHS AND CANNOT BE AUTOMATICALLY CONVERTED. ***/!!!
   :System_StartTime, SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_RUN_GROUP_ID'));
   ---- End block 'Package\Execute SQL Task'

END;
```

#### Best Practices

- Replace the unresolved reference with the closest Snowflake equivalent — for example `CURRENT_TIMESTAMP()` for a start time, or another `SYSTEM$TASK_RUNTIME_INFO` key
- Remove the reference when the value was only used for logging that Snowflake already records
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0047

SSIS FileSystemTask path requires manual mapping to a Snowflake stage

### Severity

High

#### Description

This EWI is generated for every File System Task path that must be mapped to a Snowflake stage. Snowflake has no access to the operating system file paths used by SSIS, so the converted statement carries a `@<STAGE_PLACEHOLDER>` prefix that must be replaced with a real stage before the task can run.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<FileSystemData
  TaskOperationType="DeleteFile"
  TaskSourcePath="{FILE-CONN-FS01-0000-000000000001}"
  TaskIsSourceVariable="False"
  TaskOverwriteDestFile="True" />
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.filesystemtask_delete_file_connmgr_delete_report_file
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.filesystemtask_delete_file_connmgr
AS
BEGIN
   ---- Start block 'Package\Delete Report File'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0047 - THE PATH(S) REQUIRES MANUAL MAPPING TO A SNOWFLAKE STAGE(S). ***/!!!
   REMOVE '@<STAGE_PLACEHOLDER>/Data/Input/report.txt';
   ---- End block 'Package\Delete Report File'

END;
```

#### Best Practices

- Replace `@<STAGE_PLACEHOLDER>` with the stage that holds the migrated files, keeping the relative path that follows it
- When the path came from a variable, set the variable value to a full stage path so no placeholder remains in the generated task
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0048

SSIS FileSystemTask overwrite=false not supported in Snowflake

### Severity

High

#### Description

This EWI is generated when a File System Task copy, move, or rename operation is configured with `OverwriteDestination = false`. The original task was meant to fail when the destination already existed; Snowflake’s `COPY FILES INTO` has no such option and silently overwrites the destination instead.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<FileSystemData
  TaskOperationType="CopyFile"
  TaskSourcePath="User::SourceFilePath"
  TaskIsSourceVariable="True"
  TaskDestinationPath="User::DestFilePath"
  TaskIsDestinationVariable="True"
  TaskOverwriteDestFile="False" />
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.filesystemtask_copy_file_no_overwrite_copy_file_no_overwrite
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.filesystemtask_copy_file_no_overwrite
AS
BEGIN
   CALL public.SetRunContext();
   LET User_SourceFilePath VARCHAR := public.GetControlVariableUDF('User_SourceFilePath', 'filesystemtask_copy_file_no_overwrite') :: VARCHAR;
   LET User_DestFilePath VARCHAR := public.GetControlVariableUDF('User_DestFilePath', 'filesystemtask_copy_file_no_overwrite') :: VARCHAR;
   ---- Start block 'Package\Copy File No Overwrite'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0048 - THE ORIGINAL SSIS TASK WAS CONFIGURED TO FAIL IF THE DESTINATION EXISTS. SNOWFLAKE DOES NOT SUPPORT THIS BEHAVIOR AND WILL SILENTLY OVERWRITE. ***/!!!
   --** SSC-FDM-SSIS0025 - THE VARIABLE(S) VALUE(S) MUST CONTAIN A VALID SNOWFLAKE STAGE PATH. **
   COPY FILES INTO :User_DestFilePath
   FROM :User_SourceFilePath;
   ---- End block 'Package\Copy File No Overwrite'

   CALL public.UpdateControlVariable('User_SourceFilePath', 'filesystemtask_copy_file_no_overwrite', TO_VARIANT(:User_SourceFilePath));
   CALL public.UpdateControlVariable('User_DestFilePath', 'filesystemtask_copy_file_no_overwrite', TO_VARIANT(:User_DestFilePath));
END;
```

#### Best Practices

- Add an explicit existence check before the copy — for example a `LIST` on the destination prefix — and raise an error when a file is already present, if the fail-fast behavior mattered
- Confirm that overwriting is acceptable for this destination, since the generated task will not stop when the file exists
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0049

SSIS Data Flow error-output path is not supported

### Severity

Medium

#### Description

This EWI is generated when a Data Flow component is reached through an error-output path — the red line in SSIS. Error outputs are not currently supported by the converter, so the generated dbt model carries the regular-flow columns and does not reproduce the SSIS error-redirection behavior.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<path
  refId="Package\Data Flow Task.Paths[ADO NET Source Error Output]"
  endId="Package\Data Flow Task\Flat File Destination.Inputs[Flat File Destination Input]"
  name="ADO NET Source Error Output"
  startId="Package\Data Flow Task\ADO NET Source.Outputs[ADO NET Source Error Output]" />
```

##### Output Code:

##### Snowflake

Copy code

```
{{ config(
    materialized='table',
    alias='TABLE'
) }}
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0049 - THIS COMPONENT IS REACHED THROUGH AN SSIS DATA FLOW ERROR-OUTPUT PATH (RED LINE). ERROR OUTPUTS ARE NOT CURRENTLY SUPPORTED BY THE CONVERTER; THE GENERATED DBT MODEL CARRIES THE REGULAR-FLOW COLUMNS AND WILL NOT REFLECT THE SSIS ERROR-REDIRECTION BEHAVIOR. REVIEW THE GENERATED MODEL AND IMPLEMENT THE ERROR-HANDLING BRANCH MANUALLY. ***/!!!
WITH source_data AS
(
   SELECT
      dept_name,
      id,
      ErrorCode,
      ErrorColumn
   FROM
      {{ ref('stg_raw__ado_net_source') }}
)
SELECT
   sd.dept_name AS dept_name,
   sd.id AS id,
   sd.ErrorCode AS ErrorCode,
   sd.ErrorColumn AS ErrorColumn
FROM
   source_data AS sd
```

#### Best Practices

- Implement the error branch explicitly, for example by filtering the rows that fail the validation into a separate model or by adding dbt tests that quarantine them
- Note that the `ErrorCode` and `ErrorColumn` columns are projected but never populated by the converted model
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0050

Execute SQL Task parameter marker has no parameter binding.

### Severity

High

#### Description

This EWI is generated when an Execute SQL Task statement contains a `?` parameter marker that has no matching parameter binding in the package. The marker is left unresolved in the generated task, so the statement does not compile until the parameter is mapped or replaced.

#### Code Example

##### Input Code:

##### SSIS

Copy code

```
<SQLTask:SqlTaskData
  SQLTask:Connection="{C1234567-89AB-CDEF-0123-456789ABCDEF}"
  SQLTask:SqlStatementSource="DELETE FROM dbo.StaleRows WHERE Id = ?"
  xmlns:SQLTask="www.microsoft.com/sqlserver/dts/tasks/sqltask">
</SQLTask:SqlTaskData>
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TASK public.package_executesqltaskparametermarkers_unbound_positional_marker
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package_executesqltaskparametermarkers
AS
BEGIN
   ---- Start block 'Package\Unbound Positional Marker'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0050 - THE PARAMETER MARKER '?' HAS NO MATCHING PARAMETER BINDING AND WAS LEFT UNRESOLVED. MAP THE PARAMETER IN THE EXECUTE SQL TASK OR REPLACE THE MARKER MANUALLY. ***/!!!
   DELETE FROM dbo.StaleRows
   WHERE
      Id = ?;
   ---- End block 'Package\Unbound Positional Marker'

END;
```

#### Best Practices

- Add the missing parameter mapping in the Execute SQL Task and convert again, so the marker is replaced with the bound variable reference
- Replace the marker with a literal or a task variable when the value is fixed
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SSIS0051

Fixed-width column layout could not be resolved.

### Severity

High

#### Description

This EWI is generated when a fixed-width Flat File connection manager does not provide a column width for one or more columns. The converter cannot compute the substring boundaries without those widths, so a fallback model that projects `null` for every column is generated instead of the parsing logic.

#### Code Example

##### Input Code:

##### SSIS

```
var connectionManager = new SsisFlatFileConnectionManager
{
  Name = ConnectionManagerName,
  Format = "FixedWidth",
  CodePage = 1252,
  ColumnNamesInFirstDataRow = true,
  TextQualifier = "_x003C_none_x003E_",
  Columns = new()
  {
    FlatFileFixedWidthStringColumn("col_a", 5),
    FlatFileFixedWidthStringColumn("col_b", 8),
  },
};
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0051 - SNOWCONVERT AI WAS UNABLE TO RESOLVE THE FIXED-WIDTH COLUMN LAYOUT. ONE OR MORE COLUMNS HAVE NO COLUMN WIDTH. ***/!!!
SELECT
   null AS col_a,
   null AS col_b
```

#### Best Practices

- Set the column width of every column in the Flat File connection manager and convert again, so the fixed-width layout can be resolved
- Replace the fallback projection with explicit `SUBSTR()` expressions over the raw line when the source file layout is known
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this EWI
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
