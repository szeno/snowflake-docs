# SnowConvert AI - Object Conversion Summary

[![The Object Conversion Summary section of the assessment report for Sql](/static/images/migrations/sc-assets/Screenshot2023-08-24at3.54.38PM.png "image")](/static/images/migrations/sc-assets/Screenshot2023-08-24at3.54.38PM.png)

## Identified Objects

The count of all the top-level DDL objects (such as Table, View, and Procedure) that the SnowConvert AI identified. If an object has a parsing error that makes it unreconcilable, it would not be identified.

### CSV Associated field name

- TotalIdentifiedObjects

#### Sample

Copy code

```
:force:
-- Statement without parsing error
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

-- Statements with parsing error
CREATE TABLE table2(
     column1 INT,
     column2 INT INT
);

CRATE TABLE table3(
     column1 INT
);
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

-- Statements with parsing error
CREATE OR REPLACE TABLE table2 (
     column1 INT
--                ,
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '10' COLUMN '6' OF THE SOURCE CODE STARTING AT 'column2'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS 'INT' ON LINE '10' COLUMN '14'. CODE '15'. **
--     column2 INT INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '13' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '13' COLUMN '1'. CODE '81'. **
--CRATE TABLE table3(
--     column1 INT
--)
 ;
```

**Expected Identified Objects: 2**

**Explanation:** The `table1` presented doesn’t have a parsing error; the `table2` even though it has a parsing error, the parser is still capable of recognizing the object as a table, so both are counted as an identified object; the `table3` has a parsing error that makes it unreconcilable for the parser and, as a consequence, is not counted as an identified object.

## Object Conversion Rate

The percentage of fully converted objects among the objects identified

### Formula

Copy code

```
(identify_objects_converted_successfully / total_identify_objects) * 100
```

#### CSV Associated field name

- ObjectConversionRate

#### Sample

Copy code

```
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

CREATE VIEW view1 AS
SELECT orderkey
FROM orders;

CREATE TABLE table2(
     COLNAME VARCHAR(20)
)
ON COMMIT PRESERVE ROWS;
```

Copy code

```
:force:
CREATE OR REPLACE TABLE table1 (
     column1 INT,
     column2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "orders" **
CREATE OR REPLACE VIEW view1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
     orderkey
FROM
     orders;

CREATE TABLE OR REPLACE table2 (
COLNAME VARCHAR(20)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

**Expected Object Conversion Rate: 66.66%**

**Explanation:** In this example we have 3 statements, all of them have been identified as an object, but just the `table1`, and the `view1` have a 100% conversion rate. The `table3` has an error warning meaning that the conversion of this table is not 100%, that’s why just 2 of the 3 statements are counted as fully converted objects.

## Fully Converted Objects

The number of identify objects that were converted successfully, meaning this objects have a 100% conversion rate.

### CSV Associated field name

- ObjectsSuccessfullyConverted

#### Sample

Copy code

```
:force:
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

CREATE VIEW view1 AS
SELECT orderkey
FROM orders;

CREATE TABLE table2(
     COLNAME VARCHAR(20)
)
ON COMMIT PRESERVE ROWS;
```

Copy code

```
:force:
CREATE OR REPLACE TABLE table1 (
     column1 INT,
     column2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE VIEW view1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
     orderkey
FROM
     orders;

CREATE OR REPLACE TABLE table2 (
COLNAME VARCHAR(20)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

**Expected Fully Converted Objects: 2**

**Explanation:** In this example we have 3 statements, all of them have been identified as an object, but just the `table1`, and the `view1` have a 100% conversion rate. The `table3` has an error warning meaning that the conversion of this table is not 100%, that’s why just 2 of the 3 statements are counted as fully converted objects.

## Unrecognized Elements

Represents any code element (or parts of them) such as DML, DDL, control statements, with parsing errors that SnowConvert AI was unable to process.

### CSV Associated field name

- UnrecognizedElements

#### Sample

Copy code

```
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

CREATE VIEWW view1 AS
SELECT orderkey
FROM orders;
```

Copy code

```
CREATE OR REPLACE TABLE table1 (
     column1 INT,
     column2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '6' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CREATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CREATE' ON LINE '6' COLUMN '1'. CODE '81'. **
--CREATE VIEWW view1 AS
--SELECT orderkey
--FROM orders;
```

**Expected Unrecognized Elements: 1**

**Explanation:** In this example we have 2 statements, the table1 is successfully identified as an object, in the other hand the view1, has a parsing error that means it’s impossible to identify the view as an object, because of this SnowConvert AI reports 1 Unrecognized object.

## Lines of Code in Unrecognized Elements

Represents the number of lines in unrecognized elements.

### CSV Associated field name

- UnrecognizedElementsLOC

#### Sample

Copy code

```
CREATE TABLE table1(
     column1 INT,
     column2 INT
);

CREATE VIEWW view1 AS
SELECT orderkey
FROM orders;
```

Copy code

```
CREATE OR REPLACE TABLE table1 (
     column1 INT,
     column2 INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '6' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CREATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CREATE' ON LINE '6' COLUMN '1'. CODE '81'. **
--CREATE VIEWW view1 AS
--SELECT orderkey
--FROM orders;
```

**Expected Lines of Code in Unrecognized Elements: 3**

**Explanation:** The element `view1` is an unrecognized element, this means that the lines related to this elements are counted as Lines of Code in Unrecognized Elements.

## Wrapped Objects

Represent the number of wrapped objects present in source input code

Note

This field applies only to Oracle reports.

### CSV Associated field name

- WrappedObjects

#### Sample

Copy code

```
CREATE OR REPLACE PROCEDURE PROC123 wrapped
a000000
b2
abcd
abcd
abcd
abcd
abcd
abcd
7
5f 9a
s25TmlGXjM9M+sFyW30UiYolBNowg6Rff8upynSmTEOUpAF/NYAbDvDIFsjmTDq1lhTLv74p
xZxnFllpF1iGaIfGOejm9divodC9qOeCQyIa89b2l+uNwqOzJHmOKVySIoi/l9IooFyJs9Es
FQyI4Q==

/
```

Copy code

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. Wrapped PROCEDURE IS OUT OF TRANSLATION SCOPE. **
--CREATE OR REPLACE PROCEDURE PROC123 wrapped
--a000000
--b2
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--7
--5f 9a
--s25TmlGXjM9M+sFyW30UiYolBNowg6Rff8upynSmTEOUpAF/NYAbDvDIFsjmTDq1lhTLv74p
--xZxnFllpF1iGaIfGOejm9divodC9qOeCQyIa89b2l+uNwqOzJHmOKVySIoi/l9IooFyJs9Es
--FQyI4Q==
```

**Expected Lines of Code in Unrecognized Elements: 1**

**Explanation:** The procedure is declared as a wrapped object, that’s why is counted as a wrapped object.
