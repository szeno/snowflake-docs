# SnowConvert AI - File and Object Level Breakdown - SQL Files

[![The SQL - Files section of the assessment report for Oracle.](/static/images/migrations/sc-assets/image(390).png "image")](/static/images/migrations/sc-assets/image(390).png)

Note

In Teradata, this table applies to all the files with the following extensions:

- .sql
- .dml
- .ddl

## Code Conversion Rate

This section shows the code conversion rate of the SQL files.

### Formula

Copy code

```
(converted_lines / total_lines) * 100
```

#### CSV Associated Field Names

- SqlLoCConversionRate

#### Sample

Consider the following example, even though the second table is not recognized due to a parsing error, the comments inside are considered supported lines of code.

Copy code

```
:force:
CREATE TABLE sample_table1  -- converted
(    -- line with error
 -- Comment 1  -- converted
 col1 INTEGER,  -- converted
 -- Comment 2  -- converted
 col2 INTEGER,  -- converted
 -- Comment 3  -- converted
 col3 INTEGER,  -- converted
 -- Comment 4  -- converted
 col4 !INTEGER,  -- line with error
 -- Comment 5  -- converted
 col5 INTEGER!  -- line with error
);

CREATE !TABLE sample_table2 -- line with error
(    -- line with error
 -- Comment 1  -- converted
     col1 INTEGER,  -- line with error
 -- Comment 2  -- converted
 col2 INTEGER  -- line with error
)    -- line with error
```

**Expected Conversion Rate**: 65%

**Explanation:** There is a total of 20 lines of code, and 13 of them were successfully converted by the tool. Using the formula, the conversion rate is (13/20)\*100.

A line with an error is defined as every line of code that contains at least one error message. For more information check the Issues and Troubleshooting section of each language documentation.

## Conversion Rate - Files Generated

Note

This field applies only to Teradata reports.

It describes the percentage of SQL files that were successfully generated. The files that were not generated in the output are due to unexpected issues during the process of transformation.

### Formulae

Copy code

```
(files_generated / total_files) * 100
```

#### CSV Associated Field Names

- SqlFilesConversionRate

#### Sample

Copy code

```
input_folder
    input1.sql
    input2.sql
    input3.sql
```

Copy code

```
:force:
input_folder
    input1.sql
    input2.sql
```

**Expected Files Generated Conversion Rate**: 66.67%

**Explanation:** Only 2 of the 3 input files of the conversion were successfully generated in the output.

## Conversion Rate - LOC

Note

This field applies only to Teradata reports.

It describes the same as the [Code Conversion Rate](file-and-object-level-breakdown-sql-files#code-conversion-rate) common section but applies to all the supported SQL file extensions in Teradata.

## Total File Quantity

Note

This field applies only to Teradata reports.

It describes the total number of identified SQL files.

### CSV Associated Field Names

- SqlFileCount

#### Sample

Copy code

```
input_folder
    input1.sql
    input2.dml
    input3.ddl
    input4.bteq
    input5.fl
```

**Expected Total File Quantity**: 3

**Explanation:** In this sample, 3 of the files have a supported SQL extension.

## Total LOC

Note

This field applies only to Teradata reports.

It describes the same as the [Lines of Code](file-and-object-level-breakdown-sql-files#lines-of-code) common section but applies to all the supported SQL file extensions in Teradata.

## Lines of Code

It represents the number of lines of code in the SQL extension files. This counting does not consider blank lines, only the ones that contain code, comments, or both.

### CSV Associated Field Names

- SqlLinesCount

#### Sample

Copy code

```
:force:
Folder1
    input1.sql            -- 20 lines
    input2.sql            -- 20 lines
Folder2
    input3.sql            -- 10 lines
    input4.sql            -- 5 lines
    input5.txt            -- 15 lines
```

Copy code

```
CREATE TABLE sample_table1
(
 -- Comment 1
 col1 INTEGER,
 -- Comment 2
 col2 INTEGER,
 -- Comment 3
 col3 INTEGER,
 -- Comment 4
 col4 !INTEGER,
 -- Comment 5
 col5 INTEGER!
);

CREATE !TABLE sample_table2
(
 -- Comment 1
     col1 INTEGER,
 -- Comment 2
 col2 INTEGER
)
```

**Expected Lines of code**: 55

**Explanation:** Only the lines in the SQL extension files are considered in this section.

## Total Object Quantity

It describes the number of objects successfully identified in the SQL extension files.

### CSV Associated Field Names

- SqlIdentifiedObjects

#### Sample

Copy code

```
CREATE TABLE sample_table1
(
 -- Comment 1
 col1 INTEGER,
 -- Comment 2
 col2 INTEGER,
 -- Comment 3
 col3 INTEGER,
 -- Comment 4
 col4 !INTEGER,
 -- Comment 5
 col5 INTEGER!
);

CREATE !TABLE sample_table2
(
 -- Comment 1
     col1 INTEGER,
 -- Comment 2
 col2 INTEGER
)
```

**Expected Identified Objects**: 1

**Explanation:** There are two `CREATE TABLE` statements in this example. The first one is fully recognized since it is parsed correctly, but the second one has two misspelled words in the definition so it is not recognized by Snow Convert.

## Parsing Errors

This section shows the total number of unrecognized fragments of code in the SQL files.

### CSV Associated Field Names

- SqlTotalParsingErrors

#### Sample

Copy code

```
CREATE TABLE sample_table1
(
 -- Comment 1
 col1 INTEGER,
 -- Comment 2
 col2 INTEGER,
 col3 INTEGER,
 col4 !INTEGER,

 col5 INTEGER!

);

CREATE !TABLE sample_table2
(
 -- Comment 1
     col1 INTEGER,
 -- Comment 2
 col2 INTEGER
)
```

**Expected Parsing Errors**: 3

**Explanation:** There are two parsing errors inside the first table and the second table is considered a whole parsing error due to the misspelled keyword.
