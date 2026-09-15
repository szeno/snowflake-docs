# SnowConvert AI - File and Object Level Breakdown - SQL Identified Objects

[![The SQL - Identified Objects section of the assessment report for Oracle.](/static/images/migrations/sc-assets/identifiedobjects.png "image")](/static/images/migrations/sc-assets/identifiedobjects.png)

## Conversion Rate - Object

Note

An object is considered successfully migrated if it does not have issues with medium, high or critical severity.

Represents the percentage of identified objects by SnowConvert AI that were successfully migrated. This will help to determine the number of objects that were successfully migrated and the objects that need manual work in order to complete the migration of the objects to Snowflake. If N/A is listed in the column, it means that the object type is not supported in Snowflake. A “-” could also be listed in this column, this means that the set of files migrated by SnowConvert AI did not contain objects of the specific type that could be identified.

### Formula

Copy code

```
:force:
(successfully_converted_objects / total_object_quantity) * 100
```

#### CSV Associated Field Names

- **All Languages**
  - **Tables:** SqlTableObjectConversionRate
  - **Views:** SqlViewObjectConversionRate
  - **Procedures:** SqlProcedureObjectConversionRate
  - **Functions:** SqlFunctionObjectConversionRate
  - **Triggers**: SqlTriggerObjectConversionRate
  - **Indexes:** N/A
- **Teradata**
  - **Macros:** SqlMacroObjectConversionRate
  - **Join Indexes:** SqlJoinIndexObjectConversionRate
- **Oracle**
  - **Packages:** SqlPackageObjectConversionRate
  - **Packages Bodies:** SqlPBodyObjectConversionRate
  - **Sequences:** SqlSequenceObjectConversionRate
  - **Synonyms:** SqlSynonymObjectConversionRate
  - **Types:** SqlTypeObjectConversionRate
  - **DB Link:** N/A
  - **Materialized Views:** SqlMaterializedObjectConversionRate
- **SQLServer**
  - **Materialized Views:** SqlMaterializedObjectConversionRate

#### Sample

Copy code

```
-- Table that is migrated successfully to Snowflake.
CREATE TABLE table1 (
  col1 INTEGER
);

-- Table that is not migrated successfully to Snowflake because of the data type of col1.
CREATE TABLE table2 (
  col1 ANYTYPE
);
```

**Expected Object Conversion Rate:** 50%

**Explanation:** With the previous sample code we will have a 50% Object Conversion Rate because only 1 of the 2 identified tables were successfully migrated to Snowflake.

## Conversion Rate - Code

Represents the percentage of lines or characters of code of the top-level object that were successfully migrated. You can read more about the different conversion rate modes and how they are calculated by SnowConvert AI [here](../../../review-results/reports/assessment-report/README#conversion-rate-modes).

### CSV Associated Field Names

Note

Each top-level object will have two fields for the code conversion rate in the `Assessment.csv` report. One will be for the conversion rate using lines of code and the other using the characters.

- **All Languages:**
  - **Tables**
    - **Lines of Code:** SqlTableLoCConversionRate
    - **Characters:** SqlTableCharacterConversionRate
  - **Views**
    - **Lines of Code:** SqlViewLoCConversionRate
    - **Characters:** SqlViewCharacterConversionRate
  - **Procedures**
    - **Lines of Code:** SqlProcedureLoCConversionRate
    - **Characters:** SqlProcedureCharacterConversionRate
  - **Functions**
    - **Lines of Code:** SqlFunctionLoCConversionRate
    - **Characters:** SqlFunctionCharacterConversionRate
  - **Indexes**
    - **Lines of Code:** N/A
    - **Characters:** N/A
  - **Triggers**
    - **Lines of Code:** SqlTriggerLoCConversionRate
- **Teradata**
  - **Macros**
    - **Lines of Code:** SqlMacroLoCConversionRate
    - **Characters:** SqlMacroCharacterConversionRate
  - **Join Indexes**
    - **Lines of Code:** SqlJoinIndexLoCConversionRate
    - **Characters:** SqlJoinIndexCharacterConversionRate
- **Oracle**
  - **Materialized Views**
    - **Lines of Code:** SqlMaterializedViewLoCConversionRate
    - **Characters:** SqlMaterializedViewCharacterConversionRate
  - **Packages**
    - **Lines of Code:** SqlPackageLoCConversionRate
    - **Characters:** SqlPackageCharacterConversionRate
  - **Package Bodies**
    - **Lines of Code:** SqlPBodyLoCConversionRate
    - **Characters:** SqlPBodyCharacterConversionRate
  - **Sequences**
    - **Lines of Code:** SqlSequenceLoCConversionRate
    - **Characters:** SqlSequenceCharacterConversionRate
  - **Synonyms**
    - **Lines of Code:** SqlSynonymLoCConversionRate
    - **Characters:** SqlSynonymCharacterConversionRate
  - **Types**
    - **Lines of Code:** SqlTypeLoCConversionRate
    - **Characters:** SqlTypeCharacterConversionRate
- **SQLServer**
  - **Materialized Views**
    - **Lines of Code:** SqlMaterializedViewLoCConversionRate
    - **Characters:** SqlMaterializedViewCharacterConversionRate

#### Sample

Copy code

```
:force:
CREATE TABLE table1 (
  col1 INTEGER
);
CREATE TABLE table2 (
  col1 ANYTYPE
);
```

**Expected Code Conversion Rate:** 83.33%

**Explanation:** In the previous sample code, there are two `CREATE TABLE` statements and SnowConvert AI is executed using lines of code to calculate the code conversion rate. `table1` was successfully migrated but `table2` was not migrated completely, in this case, line 5 of the input code could not be migrated and only 5 of the 6 total lines of code were migrated successfully. This calculation will generate a conversion rate for tables of 83.33%.

## Lines of Code

Represents the total amount of lines code used for the identified top-level objects. It is important to take into account that the lines of code of the top-level object as well as the comments are used for this column. On the other hand, empty lines will not be counted in this column.

### CSV Associated Field Names

- **All Languages**
  - **Tables:** SqlTableTotalLinesOfCode
  - **Views:** SqlViewTotalLinesOfCode
  - **Procedures:** SqlProcedureTotalLinesOfCode
  - **Functions:** SqlFunctionTotalLinesOfCode
  - **Indexes:** SqlIndexTotalLinesOfCode
  - **Triggers:** SqlTriggerTotalLinesOfCode
- **Teradata**
  - **Macros:** SqlMacroTotalLinesOfCode
  - **Join Indexes:** SqlJoinIndexTotalLinesOfCode
- **Oracle**
  - **Packages:** SqlPackageTotalLinesOfCode
  - **Packages Bodies:** SqlPBodyTotalLinesOfCode
  - **Sequences:** SqlSequenceTotalLinesOfCode
  - **Synonyms:** SqlSynonymTotalLinesOfCode
  - **Types:** SqlTypeTotalLinesOfCode
  - **DB Link:** SqlDbLinkTotalLinesOfCode
  - **Materialized Views:** SqlMaterializedViewTotalLinesOfCode
- **SQLServer**
  - **Materialized Views:** SqlMaterializedViewTotalLinesOfCode

#### Sample

Copy code

```
-- Hello World
CREATE TABLE table1 (
  col1 INTEGER
);

CREATE TABLE table2 (
-- Hello world 2
  col1 ANYTYPE
);
```

**Expected Lines of Code:** 8

**Explanation:** In this case, we have 6 lines that come from the code used for the `CREATE TABLE` statements and 2 for comments that are inside of the top-level objects.

## Total Object Quantity

Represents the total amount of objects identified by SnowConvert AI during the parsing phase.

### CSV Associated Field Names

- **All Languages**
  - **Tables:** SqlTableTotalOccurrences
  - **Views:** SqlViewTotalOccurrences
  - **Procedures:** SqlProcedureTotalOccurrences
  - **Functions:** SqlFunctionTotalOccurrences
  - **Indexes:** SqlIndexTotalOccurrences
  - **Triggers:** SqlTriggerTotalOccurrences
- **Teradata**
  - **Macros:** SqlMacroTotalOccurrences
  - **Join Indexes:** SqlJoinIndexTotalOccurrences
- **Oracle**
  - **Packages:** SqlPackageTotalOccurrences
  - **Packages Bodies:** SqlPBodyTotalOccurrences
  - **Sequences:** SqlSequenceTotalOccurrences
  - **Synonyms:** SqlSynonymTotalOccurrences
  - **Types:** SqlTypeTotalOccurrences
  - **DB Link:** SqlDbLinkTotalOccurrences
  - **Materialized Views:** SqlMaterializedViewTotalOccurrences
- **SQLServer**
  - **Materialized Views:** SqlMaterializedViewTotalOccurrences

#### Sample

Copy code

```
:force:
-- Successfully parsed table.
CREATE TABLE table1 (
  col1 INTEGER
);

-- Table with a parsing error that could not be identified.
CRATE TABLE table2 (
  col1 INTEGER
);
```

**Expected Total Object Quantity:** 1.

**Explanation:** One table was completely parsed by SnowConvert AI during the parsing phase but the other table has a parsing error that causes SnowConvert AI to not identify it as a table object.

## Parsing Errors

Represents the number of parsing errors that are inside of the identified objects of each top-level object type.

### CSV Associated Field Names

- **All Languages**
  - **Tables:** SqlTableTotalParsingErrors
  - **Views:** SqlViewTotalParsingErrors
  - **Materialized Views:** SqlMaterializedViewTotalParsingErrors
  - **Procedures:** SqlProcedureTotalParsingErrors
  - **Functions:** SqlFunctionParsingErrors
  - **Triggers**: SqlTriggerTotalParsingErrors
  - **Indexes**: SqlIndexTotalParsingErrors
- **Teradata**
  - **Macros:** SqlMacroTotalParsingErrors
  - **Join Indexes:** SqlJoinIndexTotalParsingErrors
- **Oracle**
  - **Packages:** SqlPackageTotalParsingErrors
  - **Packages Bodies:** SqlPBodyTotalParsingErrors
  - **Sequences:** SqlSequenceTotalParsingErrors
  - **Synonyms:** SqlSynonymTotalParsingErrors
  - **Types:** SqlTypeTotalParsingErrors
  - **DB Link:** SqlDbLinkTotalParsingErrors
  - **Materialized Views:** SqlMaterializedViewTotalParsingErrors
- **SQLServer**
  - **Materialized Views:** SqlMaterializedViewTotalParsingErrors

#### Sample

Copy code

```
-- Table with parsing error but still was identified by SnowConvert.
CREATE TABLE table1 (
  col3 NUMBER,
);

-- Table with parsing error but was not identified by SnowConvert.
CRATE TABLE table2 (
  col1 INTEGER
);
```

**Expected Parsing Errors:** 1

**Explanation:** Only one parsing error will be reported in the **Parsing Errors** column because SnowConvert AI was able to only identify the first table. Since the second table was not identified, those parsing errors will not be counted in the **Parsing Errors** column.
