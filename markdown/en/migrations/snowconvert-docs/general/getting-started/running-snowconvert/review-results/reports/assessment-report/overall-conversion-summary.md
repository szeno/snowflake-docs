# SnowConvert AI - Overall Conversion Summary

[![The Overall Conversion Summary section of the assessment report for Oracle](/static/images/migrations/sc-assets/Screenshot2023-08-23at12.09.16PM.png "image")](/static/images/migrations/sc-assets/Screenshot2023-08-23at12.09.16PM.png)

## Total Files

Represents the number of files discovered in the input address and that were successfully migrated by SnowConvert.

### CSV Associated field name

- TotalFiles

#### Sample

Copy code

```
input_folder
   ├> sql_file.sql
   ├> notes.txt
   └> views.csv
```

Copy code

```
output_folder
   └> sql_file.sql
```

**Expected Total Files:** 1

**Explanation:** With the previous sample, we will only have the SQL file as valid for migration, as the other two files have an extension that SnowConvert AI cannot recognize.

## SQL Files

Note

This field applies only to Teradata reports.

This is the number of files detected in the input folder that have an extension of .sql, .ddl, or .dml.

### CSV Associated field name

- SqlFileCount

#### Sample

Copy code

```
input_folder
    ├> ddl_file.ddl
    ├> dml_file.dml
    ├> sql_file.sql
    ├> other_file.ignore
    └> bteq_file.bteq
```

Copy code

```
output_folder
    ├> ddl_file.ddl
    ├> dml_file.dml
    ├> sql_file.sql
    └> bteq_file_BTEQ.py
```

**Expected SQL Files:** 3

**Explanation:** In this case, the 3 files with extensions DDL, DML, and SQL are recognized as SQL Files. Other extensions are not counted for SQL Files. Teradata script files are not counted for SQL files, those are counted for [Script files](#script-files).

## Script Files

Note

This field applies only to Teradata reports.

This is the number of files in the input folder that are of the following type:

- **BTEQ**: .bteq, .btq
- **FastLoad:** .fload, .fl
- **MultiLoad:** .mload, .mld, ml
- **TPump:** .tpump, .tp
- **TPT:** .tpt

### CSV Associated field name

- ScriptFileCount

#### Sample

Copy code

```
input_folder
    ├> bteq_file.bteq
    ├> btq_file.btq
    ├> fload_file.fload
    ├> mload_file.mload
    ├> sql_file.sql
    ├> tpt_file.tpt
    └> tpump_file.tpump
```

Copy code

```
output_folder
    ├> bteq_file_BTEQ.py
    ├> btq_file_BTEQ.py
    ├> fload_file_FastLoad.py
    ├> mload_file_MultiLoad.py
    ├> sql_file.sql
    ├> tpt_file_TPT.py
    └> tpump_file_TPump.py
```

**Expected Script Files:** 6

**Explanation:** In this case, the 6 files with extensions with Script file extensions are recognized as Script Files. The 2 extensions for BTEQ files previously mentioned are counted but the SQL file is not counted because it is a [SQL File](#sql-files).

## Total Files Not Generated

Represents the number of files found in the input address that, because of a failure in SnowConvert AI, failed to generate the migrated output file.

### CSV Associated field name

- TotalFilesNotGenerated

#### Sample

Copy code

```
input_folder
   ├> input1.sql
   ├> input2.sql
   └> input3.sql
```

Copy code

```
output_folder
   ├> input1.sql
   └> input2.sql
```

**Expected Total File Not Generated:** 1

**Explanation:**

## Conversion Speed

Represents the number of lines processed per second during the migration.

### Formula

Copy code

```
total_lines_of_code / conversion_time
```

#### CSV Associated field name

- ConversionSpeed

#### Sample

Copy code

```
CREATE TABLE table1(
     column1 INT,
     column2 INT
     column3 INT
);

CREATE VIEW view1 AS
SELECT orderkey
FROM orders;
```

**Expected Conversion Speed: 4 lines/sec**

**Explanation:** Let’s say that the example execution time was 2 seconds, taking into account that the number of lines is 8. Applying the formula 8/2 = 4, so the Converting Speed is 4 lines per sec.

## Conversion Time

Represents the duration of SnowConvert AI’s migration.

### CSV Associated field name

- ElapsedTime

## Total Conversion Errors

The total count of conversion errors that occurred during the conversion process. This type of error could be related to file I/O, memory management, or any abnormal situation that cannot be handled by SnowConvert AI. These are unhandled code exceptions and are considered critical issues.

### CSV Associated field name

- TotalConversionErrors

## Total Parsing Errors

The total count of parsing errors that occurred during the code analysis process. A parsing error occurs when the parser (the component that reads the source code files) encounters something unexpected. This usually means a syntax error, which refers to a code element in the file that did not match the SQL grammar specification that the parser was expecting. In other cases, these errors can also occur because the parser is not yet ready to support a specific grammar. Parsing errors are also considered critical issues. If this number is high in relation to the migration workload size, input code revision is advised.

### CSV Associated field name

- TotalParsingErrors

#### Sample

Copy code

```
-- Statement without parsing error
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

-- Statements with parsing error
CRATE TABLE table2(
     column1 INT
);

CREATE VIEW view1 AS
SELECT orderkey
FROM FROM orders;
```

Copy code

```
-- Statement without parsing error
CREATE OR REPLACE TABLE table1 (
     column1 INT,
     column2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '8' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '8' COLUMN '1'. CODE '81'. **
---- Statements with parsing error
--CRATE TABLE table2(
--     column1 INT
--)
 ;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "orders" **
CREATE OR REPLACE VIEW view1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
AS
SELECT
     orderkey
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '14' COLUMN '1' OF THE SOURCE CODE STARTING AT 'FROM'. EXPECTED 'FROM' GRAMMAR. LAST MATCHING TOKEN WAS 'FROM' ON LINE '14' COLUMN '1'. FAILED TOKEN WAS 'FROM' ON LINE '14' COLUMN '6'. CODE '44'. **
--FROM
    ;
```

**Expected Total Parsing Errors: 2**

**Explanation:** The first table presented doesn’t have a parsing error, all of it grammar is correct, but the two following statements present parsing errors because they have a grammar problem, like the second table that the `CREATE` has a spelling mistake, or the double `FROM` on the `SELECT` of the view.

## Total Warnings

The total count of warnings that SnowConvert AI generated for the given input. A warning is inserted when the translation of a specific element is mostly functionally equivalent but there are some corner cases in which some user intervention might be required. They have low severity because their intention is to provide information that can be reviewed if the code shows any kind of functional difference when executed on the target platform.

### CSV Associated field name

- TotalWarnings

#### Sample

Copy code

```
CREATE TABLE table1(
     COL1 SYS.XMLTYPE
);

SELECT TIMESTAMP '1998-12-25 09:26:50.12' AT LOCAL
FROM DUAL;

CREATE TABLE table2(
INTERVAL_YEAR_TYPE INTERVAL YEAR(2)
);
```

Copy code

```
CREATE OR REPLACE TABLE table1 (
     COL1 SYS.XMLTYPE
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

SELECT
     TIMESTAMP '1998-12-25 09:26:50.12'
FROM
     DUAL;

CREATE OR REPLACE TABLE table2 (
INTERVAL_YEAR_TYPE VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR(2) DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

**Expected Total Warnings: 3**

**Explanation:** In the last example, there is a type of warning in all three statements.

## Total Lines of Code (LOC)

The total number of lines of code in the input files, that were processed by the conversion tool.

Note

Blank lines are not counted.

### CSV Associated field name

- TotalLinesOfCode

#### Sample

Copy code

```
:force:
CREATE TABLE table1(
 column1 INT
);

-- Create View
CREATE VIEW view1 AS
SELECT orderkey
FROM orders;
```

**Expected Total Lines of Code(LOC): 8**

**Explanation:** Although the file shows 10 lines, the valid code lines are 8, because blank lines are not counted.
