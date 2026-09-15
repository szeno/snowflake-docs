# Code Conversion - General Issues

## SSC-EWI-0001

Unrecognized token on the line of the source code.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Critical

#### Description

This issue occurs when there is an error while parsing the source code that is being converted. It means there is a source code syntax error or a specific statement of the code is not being recognized yet.

#### Example Code

The following example illustrates different parsing error scenarios where invalid syntax is placed in the input. Notice how the message varies between every scenario, these contents may be helpful on isolating and fixing the issue. For more information check “Message Contents” below.

##### Input Code:

Copy code

```
 CRATE;

CREATE TABLE someTable(col1 INTEGER, !);

CREATE TABRE badTable(col1 INTEGER);

CREATE PROCEDURE proc1()
BEGIN
    CREATE TABLE badEmbeddedTable(col1 INTEGER);
END;
```

##### Generated Code:

Copy code

```
 -- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '1' COLUMN '1'. **
--CRATE
     ;

CREATE OR REPLACE TABLE someTable (
    col1 INTEGER
--                ,
                 
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '3' COLUMN '37' OF THE SOURCE CODE STARTING AT '!'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS ',' ON LINE '3' COLUMN '35'. FAILED TOKEN WAS '!' ON LINE '3' COLUMN '37'. **
--                  !
                   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/04/2024" }}'
;

-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '5' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CREATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CREATE' ON LINE '5' COLUMN '1'. **
--CREATE TABRE badTable(col1 INTEGER)
                                   ;

CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/04/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CREATE OR REPLACE TABLE badEmbeddedTable (
            col1 INTEGER);
    END;
$$;
```

#### Message Contents

1. Starting clause: Specifies the starting location (line, column, and ‘text’) of the unrecognized code. The code will be commented from the ‘text’ element onward for every unrecognized element until the parser locates a possible recovery point.
2. Expected grammar clause: Specifies the type of grammar that the parser was expecting. Check if the commented code has a matching type of the expected grammar.
3. Last matching token clause (OPTIONAL): May appear if the unrecognized code was partially recognized. This signals the point up until the parser recognized valid elements, so check the following tokens in the commented code to make sure they are valid.
4. Failed Token clause (OPTIONAL): May only be present when a “Last matching Token clause” is also present. This represents at which point the parser ultimately determined the code is invalid or not recognized. Make sure this element can be placed in this syntactical location.

#### Deprecated Message Contents

Note

The items in this list are not actively in usage, and are left here for historical purposes.

1. Recovery Code (DEPRECATED): It is intended to be used as an error code, and may be supplied for better support during parser upgrade requests. It represents how the parser triggered its recovery mechanism.

#### Best Practices

- Check if the source code has the correct syntax.
- The message can be used to isolate and solve the issue.
- If the syntax is not supported, it may be manually changed to a supported syntax.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0002

Default Parameters May Need To Be Reordered

Note

This EWI is deprecated. Default parameters are now automatically reordered to the end of the parameter list instead of emitting this warning. Please refer to [SSC-FDM-0041](../functional-difference/generalFDM#ssc-fdm-0041) for the updated behavior.

### Severity

Medium

#### Description

Default parameters may need to be reordered. Snowflake only supports default parameters at the end of the parameter declarations.

#### Example Code

##### Input Code:

Copy code

```
 CREATE PROCEDURE MySampleProc
    @Param1 NVARCHAR(50) = NULL,
    @Param2 NVARCHAR(10),
    @Param3 NVARCHAR(10) = NULL,
    @Param4 NVARCHAR(10)
AS   
    SELECT 1;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE MySampleProc
!!!RESOLVE EWI!!! /*** SSC-EWI-0002 - DEFAULT PARAMETERS MAY NEED TO BE REORDERED. SNOWFLAKE ONLY SUPPORTS DEFAULT PARAMETERS AT THE END OF THE PARAMETERS DECLARATIONS ***/!!!
(PARAM1 STRING DEFAULT NULL, PARAM2 STRING, PARAM3 STRING DEFAULT NULL, PARAM4 STRING)
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ProcedureResultSet RESULTSET;
    BEGIN
        ProcedureResultSet := (
        SELECT 1);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0003

System column for built-in object has not been translated.

### Severity

Medium

#### Description

This EWI is generated when a built-in system object (table, view) is mapped to the Snowflake-equivalent object, but there is no map for one of its internal columns.

#### Code Example

**Input Code:**

Copy code

```
select name, 
       parent_object_id
    from sys.tables;
```

**Output Code:**

##### Snowflake

Copy code

```
select
    TABLE_NAME,
       parent_object_id !!!RESOLVE EWI!!! /*** SSC-EWI-0003 - SYSTEM COLUMN 'parent_object_id' FOR BUILT-IN OBJECT 'SYS.TABLES' HAS NOT BEEN TRANSLATED. ***/!!!
    from
    INFORMATION_SCHEMA.TABLES;
```

## SSC-EWI-0005

### Severity

Critical

#### Description

This issue appears when an unexpected transformation error occurs while trying to convert the source code and the output code file can not be generated.

#### Best Practices

- Check the error log file for more information about the issue.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0006

The current date/numeric format may have a different behavior in Snowflake.

### Severity

Medium

#### Description

This error is added because Snowflake does not support date/numeric formats in some functions as is supported in the source language.

The following format elements are the ones that may behave differently in [Snowflake](https://docs.snowflake.com/en/sql-reference/functions-conversion#label-date-time-format-conversion):

#### Redshift Date / Time

| Format Element | Description |
| --- | --- |
| HH | Hour of day (01–12). |
| MS | Millisecond (000–999). |
| US | Microsecond (000000–999999). |
| SSSS, SSSSS | Seconds past midnight (0–86399). |
| Y,YYY | Year (4 or more digits) with comma. |
| YYY | Last 3 digits of year. |
| Y | Last digit of year. |
| IYYY | ISO 8601 week-numbering year(4 or more digits). |
| IYY | Last 3 digits of ISO 8601 week-numbering year. |
| IY | Last 2 digits of ISO 8601 week-numbering year. |
| I | Last digit of ISO 8601 week-numbering year. |
| BC, bc, AD or ad | Era indicator (without periods). |
| B.C., b.c., A.D. or a.d. | Era indicator (with periods). |
| MONTH | Full upper case month name (blank-padded to 9 chars). |
| Month | Full capitalized month name (blank-padded to 9 chars). |
| month | Full lower case month name (blank-padded to 9 chars). |
| DAY | Full upper case day name (blank-padded to 9 chars). |
| Day | Full capitalized day name (blank-padded to 9 chars). |
| day | Full lower case day name (blank-padded to 9 chars). |
| DDD | Day of year (001–366). |
| IDDD | Day of ISO 8601 week-numbering year (001–371; day 1 of the year is Monday of the first ISO week). |
| D | Day of the week, Sunday (1) to Saturday (7). |
| ID | ISO 8601 day of the week, Monday (1) to Sunday (7). |
| W | Week of month (1–5) (the first week starts on the first day of the month). |
| WW | Week number of year (1–53) (the first week starts on the first day of the year). |
| IW | Week number of ISO 8601 week-numbering year (01–53; the first Thursday of the year is in week 1). |
| CC | Century (2 digits) (the twenty-first century starts on 2001-01-01). |
| J | Julian Date. |
| Q | Quarter. |
| RM | Month in upper case Roman numerals (I–XII; I=January). |
| rm | Month in lower case Roman numerals (i–xii; i=January). |
| TZ | Upper case time-zone abbreviation (only supported in `to_char`). |
| tz | Lower case time-zone abbreviation (only supported in `to_char`). |
| TZH | Time-zone hours. |
| TZM | Time-zone minutes. |
| OF | Time-zone offset from UTC (only supported in `to_char`). |
| FM prefix | Fill mode (suppress leading zeroes and padding blanks). |
| TH suffix | Upper case ordinal number suffix. |
| th suffix | Lower case ordinal number suffix. |
| FX prefix | Fixed format global option (see usage notes). |
| TM prefix | Translation mode (use localized day and month names based on [lc\_time](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-LC-TIME)). |
| SP suffix | Spell mode. |

Note

For more information please refer to [PostgreSQL Date/Time formats](https://www.postgresql.org/docs/current/functions-formatting.html#FUNCTIONS-FORMATTING-DATETIME-TABLE).

Note

The transformation of the TO\_CHAR function supports most of this format elements, for a full list of suppported format elements and their equivalent mappings please refer to the [Translation specification](../../translation-references/redshift/redshift-functions#for-datetime-values)

### BigQuery Format

Review the [BigQuery format elements reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements).

### Numeric

| Pattern | Description |
| --- | --- |
| PR | negative value in angle brackets |
| RN | Roman numeral (input between 1 and 3999) |
| TH or th | ordinal number suffix |
| V | shift specified number of digits (see notes) |
| EEEE | exponent for scientific notation |

Expand

Show lessSee more

Note

For more information please refer to [PostgreSQL Numeric formats](https://www.postgresql.org/docs/current/functions-formatting.html#FUNCTIONS-FORMATTING-NUMERIC-TABLE).

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 SELECT 
   DATE_TRUNC('decade', TIMESTAMP '2017-03-17 02:09:30'),
   DATE_TRUNC('century', TIMESTAMP '2017-03-17 02:09:30'),
   DATE_TRUNC('millennium', TIMESTAMP '2017-03-17 02:09:30');
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
      !!!RESOLVE EWI!!! /*** SSC-EWI-PG0005 - DECADE FORMAT IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
      DATE_TRUNC('decade', TIMESTAMP '2017-03-17 02:09:30'),
      !!!RESOLVE EWI!!! /*** SSC-EWI-PG0005 - CENTURY FORMAT IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
      DATE_TRUNC('century', TIMESTAMP '2017-03-17 02:09:30'),
      !!!RESOLVE EWI!!! /*** SSC-EWI-PG0005 - MILLENNIUM FORMAT IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
      DATE_TRUNC('millennium', TIMESTAMP '2017-03-17 02:09:30');
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0007

### Severity

Critical

#### Description

This error appears when an error occurs in writing the output file.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0008

COLLATE clause may have a different behavior in Snowflake

### Severity

Medium

#### Description

This warning is added when the collate clause is used as a column option because it is supported in Snowflake, but behaves differently in the collate specification. To verify which specifiers are supported in Snowflake, see [Collate specifications](https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification).

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE TABLE01 (
    col1 text COLLATE "C"
);
```

##### Generated Code:

Copy code

```
 CREATE TABLE TABLE01 (
    col1 text
              !!!RESOLVE EWI!!! /*** SSC-EWI-0008 - COLLATE CLAUSE MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!! COLLATE "C"
);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0009

Regexp\_Substr Function only supports POSIX regular expressions.

### Severity

Low

#### Description

Currently, there is no support in Snowflake for extended regular expression beyond the [POSIX Basic Regular Expression syntax](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).

This EWI is added every time a function call to *REGEX\_SUBSTR, REGEX\_REPLACE,* or *REGEX\_INSTR* is transformed to Snowflake to warn the user about possible unsupported regular expressions. Some of the features **not supported** are lookahead, lookbehind, and non-capturing groups.

#### Example Code

##### Input Code:

Copy code

```
 SELECT REGEXP_SUBSTR('qaqequ','q(?=u)', 1, 1);
```

##### Generated Code:

Copy code

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0009 - REGEXP_SUBSTR FUNCTION ONLY SUPPORTS POSIX REGULAR EXPRESSIONS ***/!!!
REGEXP_SUBSTR('qaqequ','q(?=u)', 1, 1);
```

#### Best Practices

- Check the regular expression used in each case to determine whether it needs manual intervention. More information about expanded regex support and alternatives in Snowflake can be found [**here**](https://community.snowflake.com/s/question/0D50Z00007ENLKsSAP/expanded-support-for-regular-expressions-regex)**.**
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0010

### Severity

Critical

#### Description

This error appears when there is not a transformation rule for a specific procedure statement.

#### Best Practices

- Check if the procedure statement is correct.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0011

### Severity

High

#### Description

This error appears when there is an unexpected end of the statement in the source code and the error cannot be handled correctly.

#### Best Practices

- Check if the source code is incomplete or if the statement that is being converted ends correctly.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0012

### Severity

High

#### Description

This error appears when there is an unexpected end of the statement in the source code

#### Example Code

##### Input Code:

Copy code

```
 CREATE VOLATILE SET TABLE VOLATILETABLE
(
    COL1                    INTEGER,
    COL2                    INTEGER,
    COL3                    INTEGER
)
ON COMMIT PRESERVE ROWS;
UPDATE TABLE2 as T2
SET T2.COL1 + VOLATILETABLE.COL1
WHERE T2.COL2 = VOLATILETABLE.COL2
    AND T2.COL3 = VOLATILETABLE.COL3
    AND     T2.COL4 = ( SELECT MAX(T3.COL1) 
                                   FROM
                                   TABLE3 T3
                                   WHERE T3.COL1 = T2.COL1);
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
CREATE OR REPLACE TEMPORARY TABLE VOLATILETABLE
(
    COL1 INTEGER,
    COL2 INTEGER,
    COL3 INTEGER
)
--    --** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--ON COMMIT PRESERVE ROWS
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "TABLE2", "TABLE3" **
UPDATE TABLE2 AS T2
    SET
        --** SSC-FDM-0025 - UNEXPECTED END OF STATEMENT. PLEASE CHECK THE LINE 9 OF ORIGINAL SOURCE CODE. **
        T2.COL1 + VOLATILETABLE.COL1
    FROM
        VOLATILETABLE
        WHERE T2.COL2 = _VOLATILETABLE.COL2
            AND T2.COL3 = _VOLATILETABLE.COL3
            AND     T2.COL4 = (
                SELECT
                    MAX(T3.COL1)
                                                  FROM
                    TABLE3 T3
                                                  WHERE T3.COL1 = T2.COL1);
```

#### Recommendation

- Check if the source code is incomplete or if the statement that is being converted ends correctly.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0013

### Severity

Critical

#### Description

This error appears when an exception is raised while converting an item from the source code.

#### Recommendation

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0014

### Severity

Critical

#### Description

This error appears when the body of a specific procedure statement is not generated.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0015

Pivot/Unpivot multiple function not supported.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

This section describes the different issues that could be triggered by PIVOT and UNPIVOT clauses. The not-supported scenarios are presented in the following table.

|  | PIVOT | UNPIVOT | ORACLE | TERADATA |
| --- | --- | --- | --- | --- |
| MULTIPLE COLUMN | X | X | X | X |
| RENAME COLUMN | X | X | X | X |
| MULTIPLE FUNCTION | X |  | X | X |
| WITH CLAUSE | X |  |  | X |
| XML OUTPUT FORMAT | X |  | X |  |
| IN CLAUSE SUBQUERY | X |  | X | X |
| IN CLAUSE ANY SEQUENCE | X |  | X |  |
| INCLUDE/EXCLUDE NULLS |  | X | X | X |

Expand

Show lessSee more

#### MULTIPLE COLUMN

Multiple columns are not supported by PIVOT and UNPIVOT clauses.

##### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM star1p UNPIVOT ((sales,cogs)  FOR  yr_qtr
    IN ((Q101Sales, Q101Cogs) AS 'Q101A',
        (Q201Sales, Q201Cogs) AS 'Q201A', 
        (Q301Sales, Q301Cogs) AS 'Q301A')) AS Tmp;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT * FROM
    star1p
           !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT MULTIPLE COLUMN NOT SUPPORTED ***/!!!
           UNPIVOT ((sales,cogs)  FOR  yr_qtr
    !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT MULTIPLE COLUMN NOT SUPPORTED ***/!!!
    IN ((Q101Sales, Q101Cogs) AS 'Q101A',
        (Q201Sales, Q201Cogs) AS 'Q201A',
        (Q301Sales, Q301Cogs) AS 'Q301A')) AS Tmp;
```

#### RENAME COLUMN

Renaming columns with aliases is not supported in Snowflake UNPIVOT clauses. SnowConvert will remove aliases for functions or columns to create a valid query and check that this change does not affect the original functionality.

For PIVOT, the use of column aliases is only supported for Teradata if the following two conditions are true: all expressions inside the IN clause have an alias associated and information is available about the columns that will be generated as a result, either by providing the table definition or using a subquery with an explicit column list as input to the clause.

##### Example Code

##### Input Code:

Copy code

```
CREATE TABLE star1(
	country VARCHAR(20),
	state VARCHAR(10), 
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
);

--SAMPLE 1
SELECT * FROM db1.star1p UNPIVOT (column1  FOR  for_column 
    IN (col1 AS 'as_col1', col2 AS 'as_col2')) Tmp;

--SAMPLE 2
SELECT *
FROM star1 PIVOT (
	SUM(sales) as ss1 FOR qtr                                                                                               
    IN ('Q1' AS Quarter1,                                                                                                     
    	'Q2' AS Quarter2, 
        'Q3' AS Quarter3)
)Tmp;

--SAMPLE 3
SELECT 
	* 
FROM (
	SELECT 
		country,
		state, 
		yr,
		qtr,
		sales,
		cogs
	FROM star1 ) A
PIVOT (
	SUM(sales) as ss1 FOR qtr                                                                                               
    IN ('Q1' AS Quarter1,                                                                                                     
    	'Q2' AS Quarter2, 
        'Q3' AS Quarter3)
)Tmp;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE star1 (
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "08/14/2024" }}'
;

--SAMPLE 1
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "db1.star1p" **
SELECT
	* FROM db1.star1p UNPIVOT (column1  FOR  for_column
	    IN (col1 AS 'as_col1', col2 AS 'as_col2')) Tmp !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PivotUnpivotTableReference' NODE ***/!!!;

--SAMPLE 2
SELECT
	*
FROM
	star1 PIVOT (
	SUM(sales) FOR qtr IN ('Q1',
	   	'Q2',
	       'Q3')) Tmp (
		country,
		state,
		yr,
		cogs,
		Quarter1_ss1,
		Quarter2_ss1,
		Quarter3_ss1
	);

--SAMPLE 3
	SELECT
		*
	FROM (
		SELECT
				country,
				state,
				yr,
				qtr,
				sales,
				cogs
			FROM
				star1
	) A
	PIVOT (
		SUM(sales) FOR qtr IN ('Q1',
	    'Q2',
	        'Q3')) Tmp (
		country,
		state,
		yr,
		cogs,
		Quarter1_ss1,
		Quarter2_ss1,
		Quarter3_ss1
	);
```

#### MULTIPLE FUNCTION

Multiple function is not supported for PIVOT clauses, sometimes multiple function queries could be re-written using case statements, see the following Teradata sample for more information <https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/L0kKSOrOeu_68mcW3o8ilw>

##### Example Code

##### Input Code:

Copy code

```
 SELECT *
FROM STAR1 PIVOT(SUM(COL1), SUM(COL2) FOR YR IN ('Y1', 'Y2', 'Y3'))TMP;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT
*
FROM
STAR1
      !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT MULTIPLE FUNCTION NOT SUPPORTED ***/!!!
      PIVOT(SUM(COL1), SUM(COL2) FOR YR IN ('Y1', 'Y2', 'Y3'))TMP;
```

#### WITH CLAUSE

Teradata PIVOT has an optional WITH clause, this is not allowed in Snowflake’s PIVOT.

##### Example Code

##### Input Code:

Copy code

```
 SELECT *
FROM STAR1 PIVOT(SUM(COL1) FOR YR IN ('Y1', 'Y2', 'Y3') WITH SUM(*) AS withalias)TMP;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT
*
FROM
STAR1 PIVOT(SUM(COL1) FOR YR IN ('Y1', 'Y2', 'Y3')
                                                   !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT WITH CLAUSE NOT SUPPORTED ***/!!!
 WITH SUM(*) AS withalias)TMP;
```

#### XML OUTPUT FORMAT

XML output for the PIVOT clause is not supported by Snowflake.

##### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM   (SELECT product_code, quantity FROM pivot_test)
PIVOT XML (SUM(quantity) 
FOR (product_code) IN ('A','B','C'));
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT * FROM
(
SELECT product_code, quantity FROM
pivot_test)
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT XML OUTPUT FORMAT NOT SUPPORTED ***/!!!
PIVOT (SUM(quantity) FOR product_code IN ( 'A', 'B', 'C'));
```

#### IN CLAUSE SUBQUERY

Subqueries for the IN clause are not supported.

##### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM s1 PIVOT(SUM(COL1) FOR FORCOL IN (SELECT SELCOL FROM S2))DT;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT * FROM
s1 PIVOT (SUM(COL1) FOR FORCOL
                               !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT IN CLAUSE SUBQUERY NOT SUPPORTED ***/!!! IN (SELECT SELCOL FROM
                               S2));
```

#### IN CLAUSE ANY SEQUENCE

This error is triggered when ANY keyword is used in the IN clause. This is currently not supported.

##### **Example Code**

##### Input Code:

Copy code

```
 SELECT * FROM (SELECT product_code, quantity FROM pivot_test)
PIVOT (SUM(quantity)
FOR product_code IN (ANY, ANY, ANY));
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT * FROM (SELECT product_code, quantity FROM
pivot_test)
PIVOT (SUM(quantity)
FOR product_code
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT IN CLAUSE ANY SEQUENCE NOT SUPPORTED ***/!!!
 IN (ANY, ANY, ANY));
```

#### INCLUDE/EXCLUDE NULLS

INCLUDE NULLS or EXCLUDE NULLS are not valid options for UNPIVOT clauses in Snowflake.

##### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM db1.star1p UNPIVOT INCLUDE NULLS (column1  FOR  for_column IN (col1, col2)) Tmp;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT * FROM
db1.star1p
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT INCLUDE NULLS NOT SUPPORTED ***/!!!
UNPIVOT ( column1 FOR for_column IN (
col1,
col2)) Tmp;
```

#### Best Practices

- Re-write the query if possible, otherwise, no additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0016

Snowflake does not support the options clause.

### Severity

Medium

#### Description

This EWI is added to DDLs statements when the `OPTIONS` has unsupported options by Snowflake.

#### Code Example

**Input Code:**

##### BigQuery

Copy code

```
 CREATE VIEW my_view
OPTIONS (
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
) AS
SELECT column1, column2
FROM my_table;
```

**Output Code:**

##### Snowflake

Copy code

```
 CREATE VIEW my_view
!!!RESOLVE EWI!!! /*** SSC-EWI-0016 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: EXPIRATION_TIMESTAMP, PRIVACY_POLICY. ***/!!!
OPTIONS(
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
AS
SELECT column1, column2
FROM
  my_table;
```

## SSC-EWI-0020

CUSTOM UDF INSERTED.

### Severity

Low

### Summary

There are several User-Defined Functions (UDF) provided to reproduce source language behaviors that are not supported by Snowflake, functionality and descriptions are detailed below.

UDFs can be found in “UDF Helpers” folder created in the output path after the migration has occurred.

#### Best Practices

- Check if the UDF Helpers folder is being created with files inside it.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0021

Not supported.

### Severity

Medium

#### Description

This message appears when a specific node or statement from the source code is not supported in Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 WITH my_av ANALYTIC VIEW AS
(USING sales_av HIERARCHIES(time_hier) ADD MEASURES(lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1 )))) 
SELECT aValue from my_av;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - SubavFactoring NOT SUPPORTED IN SNOWFLAKE ***/!!!
WITH my_av ANALYTIC VIEW AS
(USING sales_av HIERARCHIES(time_hier) ADD MEASURES(lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1 ))))
SELECT aValue from my_av;
```

#### Best Practices

- If this error happens is because there is no Snowflake equivalent for the node that is being converted.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0022

One or more identifiers in a specific statement are considered parameters by default.

Warning

The EWI is only generated when Javascript is the target language for Stored Procedures. This is a deprecated translation feature, as Snowflake Scripting is the recommended target language for Stored Procedures.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

This error is used to report that one or more identifiers in a specific statement are considered parameters by default.

#### Example Code

##### Input Code:

Copy code

```
 -- Additional Params: -t javascript
CREATE MACRO SAME_MACRO_COLUMN_AND_PARAMATERS (
LOAD_USER_ID (VARCHAR (32), CHARACTER SET LATIN),
UPDATE_USER_ID (VARCHAR (32), CHARACTER SET LATIN)
) AS (
UPDATE TABLE1 SET LOAD_USER_ID = :LOAD_USER_ID, UPDATE_USER_ID = :UPDATE_USER_ID;
INSERT INTO TABLE1 (LOAD_USER_ID, UPDATE_USER_ID) VALUES (:LOAD_USER_ID, :UPDATE_USER_ID);
DELETE FROM TABLE1 WHERE :LOAD_USER_ID = LOAD_USER_ID;
);
```

##### Generated Code:

Copy code

```
-- Additional Params: -t javascript
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE PROCEDURE SAME_MACRO_COLUMN_AND_PARAMATERS (LOAD_USER_ID VARCHAR (32), UPDATE_USER_ID VARCHAR (32))
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
// REGION SnowConvert AI Helpers Code
var HANDLE_NOTFOUND;
var _RS, ROW_COUNT, _ROWS, MESSAGE_TEXT, SQLCODE = 0, SQLSTATE = '00000', ERROR_HANDLERS, ACTIVITY_COUNT = 0, INTO, _OUTQUERIES = [], DYNAMIC_RESULTS = -1;
var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
var fixBind = function (arg) {
arg = arg == undefined ? null : arg instanceof Date ? formatDate(arg) : arg;
return arg;
};
var EXEC = function (stmt,binds,noCatch,catchFunction,opts) {
try {
binds = binds ? binds.map(fixBind) : binds;
_RS = snowflake.createStatement({
sqlText : stmt,
binds : binds
});
_ROWS = _RS.execute();
ROW_COUNT = _RS.getRowCount();
ACTIVITY_COUNT = _RS.getNumRowsAffected();
HANDLE_NOTFOUND && HANDLE_NOTFOUND(_RS);
if (INTO) return {
INTO : function () {
return INTO();
}
};
if (_OUTQUERIES.length < DYNAMIC_RESULTS) _OUTQUERIES.push(_ROWS.getQueryId());
if (opts && opts.temp) return _ROWS.getQueryId();
} catch(error) {
MESSAGE_TEXT = error.message;
SQLCODE = error.code;
SQLSTATE = error.state;
var msg = `ERROR CODE: ${SQLCODE} SQLSTATE: ${SQLSTATE} MESSAGE: ${MESSAGE_TEXT}`;
if (catchFunction) catchFunction(error);
if (!noCatch && ERROR_HANDLERS) ERROR_HANDLERS(error); else throw new Error(msg);
}
};
// END REGION

EXEC(`UPDATE TABLE1
   SET
      LOAD_USER_ID = :1,
      UPDATE_USER_ID = :2`,[LOAD_USER_ID,UPDATE_USER_ID]);
// ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
EXEC(`INSERT INTO TABLE1 (LOAD_USER_ID, UPDATE_USER_ID)
VALUES (:1, :2)`,[LOAD_USER_ID,UPDATE_USER_ID]);
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Delete' NODE ***/!!!
//DELETE FROM
//   TABLE1
//WHERE
//   UPPER(RTRIM(:LOAD_USER_ID)) = UPPER(RTRIM(LOAD_USER_ID))
null
$$;
```

#### Best Practices

- Make sure all the dependencies(tables and views) related to the procedure statement are being migrated.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0023

Performance Review - A loop contains an insert, delete, or update statement.

Warning

The EWI is only generated when Javascript is the target language for Stored Procedures. This is a deprecated translation feature, as Snowflake Scripting is the recommended target language for Stored Procedures.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This warning indicates a possible consideration that the user should have in terms of performance.

#### Example Code

##### Input Code:

Copy code

```
 -- Additional Params: -t javascript
REPLACE PROCEDURE Database1.Proc1()
BEGIN
    DECLARE lNumber INTEGER DEFAULT 1;
    FOR class1 AS class2 CURSOR FOR 
      SELECT COL0,
      TRIM(COL1) AS COL1ALIAS,
      TRIM(COL2),
      COL3
      FROM someDb.prefixCol
    DO
      INSERT INTO TempDB.Table1 (:lgNumber, :lNumber, (',' || :class1.ClassCD || '_Ind CHAR(1) NOT NULL'));
      SET lNumber = lNumber + 1;
    END FOR;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE Database1.Proc1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var LNUMBER = 1;
    /*** SSC-EWI-0023 - PERFORMANCE REVIEW - THIS LOOP CONTAINS AN INSERT, DELETE OR UPDATE STATEMENT ***/
    for(var CLASS2 = new CURSOR(`SELECT
   COL0,
   TRIM(COL1) AS COL1ALIAS,
   TRIM(COL2),
   COL3
FROM
   someDb.prefixCol`,[],false).OPEN();CLASS2.NEXT();) {
        let CLASS1 = CLASS2.CURRENT;
        EXEC(`INSERT INTO TempDB.Table1
VALUES (:lgNumber, :1, (',' || :
!!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE class1.ClassCD MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
:2 || '_Ind CHAR(1) NOT NULL'))`,[LNUMBER,CLASS1.CLASSCD]);
        LNUMBER = LNUMBER + 1;
    }
    CLASS2.CLOSE();
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0025

Binding time variables might require a change in the query.

Warning

The EWI is only generated when Javascript is the target language for Stored Procedures. This is a deprecated translation feature, as Snowflake Scripting is the recommended target language for Stored Procedures.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

The action of binding time variables might require changes in the query that contains them.

#### Example Code

##### Input Code:

Copy code

```
 -- Additional Params: -t javascript
CREATE PROCEDURE P_1025()
BEGIN
  DECLARE LN_EMP_KEY_NO_PARAM NUMERIC DEFAULT -1;
  DECLARE FLOATVARNAME FLOAT DEFAULT 12.1;
  DECLARE hErrorMsg CHARACTER(30) DEFAULT 'NO ERROR';
  DECLARE CurrTs TIME DEFAULT CURRENT_TIME;
  DECLARE CurrTs2 TIME DEFAULT CURRENT_TIMESTAMP;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE P_1025 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  var LN_EMP_KEY_NO_PARAM = -1;
  var FLOATVARNAME = 12.1;
  var HERRORMSG = `NO ERROR`;
  var CURRTS = new Date() /*** SSC-EWI-0025 - BINDING TIME VARIABLE MIGHT REQUIRE CHANGE IN QUERY. ***/;
  var CURRTS2 = new Date();
$$;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0026

Qualified variables may require a cast.

Warning

The EWI is only generated when Javascript is the target language for Stored Procedures. This is a deprecated translation feature, as Snowflake Scripting is the recommended target language for Stored Procedures.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This warning is added when there is a query with a variable with a qualified member like an Oracle record or a Teradata for loop variable. Depending on where the variable is being used and the type of value, a cast may be necessary to work properly.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE TABLE1 (COL1 DATE);
CREATE TABLE TABLE2 (COL1 VARCHAR(25));

CREATE OR REPLACE PROCEDURE EXAMPLE
IS
    CURSOR C1 IS SELECT * FROM TABLE1;
BEGIN
    FOR REC1 IN C1 LOOP
		    insert into TABLE2 values (TO_CHAR(REC1.COL1, 'DD-MM-YYYY'));
    END LOOP;
END;
```

##### Generated Code:

Copy code

```
 -- Additional Params: -t javascript
CREATE OR REPLACE TABLE TABLE1 (COL1 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE TABLE2 (COL1 VARCHAR(25))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE EXAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	let C1 = new CURSOR(`SELECT * FROM
      TABLE1`,() => []);
	C1.OPEN();
	// ** SSC-EWI-0023 - PERFORMANCE REVIEW - THIS LOOP CONTAINS AN INSERT, DELETE OR UPDATE STATEMENT **
	while ( C1.NEXT() ) {
		let REC1 = C1.CURRENT;
		EXEC(`insert into TABLE2
		    values (TO_CHAR(
		    !!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE REC1.COL1 MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
		    ?, 'DD-MM-YYYY'))`,[REC1.COL1]);
	}
	C1.CLOSE();
$$;
```

##### Generated Code with adjustments:

Copy code

```
 CREATE OR REPLACE TABLE TABLE1 (COL1 TIMESTAMP
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE TABLE2 (COL1 VARCHAR(25))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE EXAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	let C1 = new CURSOR(`SELECT * FROM
      TABLE1`,() => []);
	C1.OPEN();
	// ** SSC-EWI-0023 - PERFORMANCE REVIEW - THIS LOOP CONTAINS AN INSERT, DELETE OR UPDATE STATEMENT **
	while ( C1.NEXT() ) {
		let REC1 = C1.CURRENT;
		EXEC(`insert into TABLE2
		    values (TO_CHAR(REC1.COL1::DATE, 'DD-MM-YYYY'))`,[REC1.COL1]);
	}
	C1.CLOSE();
$$;
```

#### Best Practices

- Check if a cast to a Date, Time, or Timestamp is necessary for the binding. Some cases are not necessary because an implicit conversion is done to the value.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0027

The following statement uses a variable/literal with an invalid query and it will not be executed.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

This warning is used to report that a specific statement uses a variable or literal with an invalid query and for that reason, it will not be executed.

#### Example Code

##### Input Code:

Copy code

```
 REPLACE PROCEDURE TEST.COLLECT_STATS () 
BEGIN
  COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME);

  SET STATS_STATEMENT = 'COLLECT STATS ON ' || OUT_DB || '.' || OUT_TBL || ' COLUMN(' || C4.ColumnName || ');';

  EXECUTE IMMEDIATE STATS_STATEMENT;

  EXECUTE IMMEDIATE 'COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME);';

  SET STATS_STATEMENT_NOT_DYNAMIC = 'COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME);';

  EXECUTE IMMEDIATE STATS_STATEMENT_NOT_DYNAMIC;

END;
;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE TEST.COLLECT_STATS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
--    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. COLLECT **
--    COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME);
    STATS_STATEMENT := 'COLLECT STATS ON ' || OUT_DB || '.' || OUT_TBL || ' COLUMN(' || C4.ColumnName || ')';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!

    EXECUTE IMMEDIATE STATS_STATEMENT;
    !!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!

    EXECUTE IMMEDIATE 'COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME)';
    STATS_STATEMENT_NOT_DYNAMIC := 'COLLECT STATS ON DBC.AccessRights COLUMN(COLNAME)';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!

    EXECUTE IMMEDIATE STATS_STATEMENT_NOT_DYNAMIC;
  END;
$$;
```

#### Best Practices

- Check if a cast to a Date, Time, or Timestamp is necessary for the binding. Some cases are not necessary because an implicit conversion is done to the value.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0028

Type not supported by Snowflake

### Severity

Medium

#### Description

This message appears when a type is not supported in Snowflake.

#### Example

##### Input Code (Oracle):

Copy code

```
 CREATE TABLE MYTABLE
(
    COL1 SYS.ANYDATASET
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE MYTABLE
    (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
        COL1 SYS.ANYDATASET
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0029

External table data format not supported in snowflake

### Severity

Medium

#### Description

Snowflake supports the following External Table formats:

| BigQuery | Snowflake |
| --- | --- |
| AVRO | AVRO |
| CSV GOOGLE\_SHEETS | CSV |
| NEWLINE\_DELIMITED\_JSON JSON | JSON |
| ORC | ORC |
| PARQUET | PARQUET |

Expand

Show lessSee more

When an external table has other FORMAT not specified in the above table, this EWI will be generated to inform the user that the FORMAT is not supported.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table
OPTIONS (
  format = 'DATASTORE_BACKUP',
  uris = ['gs://backup_bucket/backup_folder/*']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0029 - EXTERNAL TABLE DATA FORMAT NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-0035 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_BACKUP_RESTORE_TABLE_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://backup_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'backup_folder/.*'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0030

The statement below has usages of dynamic SQL

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

This error is used to indicate that the statement has usages of dynamic SQL. Each specific source language has its own set of statements that can execute dynamic SQL. Dynamic SQL refers to code that is built as text using the string manipulation tools the database engine language provides.

This scenario is considered a complex pattern because dynamic SQL is built and executed in runtime making it more difficult to track and debug errors. This error is meant to be a helper to spot some problems that a static-code analyzer such as Snow Convert cannot.

#### Code Example

#### Teradata

##### Input

Copy code

```
 REPLACE PROCEDURE teradata_dynamic_sql()
BEGIN
  DECLARE str_sql VARCHAR(20);
  SET str_sql = 'UPDATE TABLE
                    SET COLA = 0,
                        COLB = ''test''';

  EXECUTE IMMEDIATE str_sql;
  EXECUTE IMMEDIATE 'INSERT INTO TABLE1(COL1) VALUES(1)';
  EXECUTE str_sql;
  CALL DBC.SysExecSQL('INSERT INTO TABLE1(COL1) VALUES(1)');
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE teradata_dynamic_sql ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/04/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    str_sql VARCHAR(20);
  BEGIN
     
    str_sql := 'UPDATE "TABLE"
   SET COLA = 0,
       COLB = ''test''';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE str_sql;
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE 'INSERT INTO TABLE1 (COL1)
VALUES (1);';
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE str_sql;
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE 'INSERT INTO TABLE1 (COL1)
VALUES (1);';
  END;
$$;
```

#### Oracle

##### Input

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_dynamic_sql
AS
    dynamic_statement VARCHAR(100);
    numeric_variable INTEGER;
    dynamic_statement VARCHAR(100);
    column_variable VARCHAR(100);
    cursor_variable SYS_REFCURSOR;
    c INTEGER;
    dynamic_statement VARCHAR(100);
BEGIN
    dynamic_statement := 'INSERT INTO sample_table(col1) VALUES(1)';
    numeric_variable := 3;
    column_variable := 'col1';

    EXECUTE IMMEDIATE dynamic_statement;
    EXECUTE IMMEDIATE 'INSERT INTO sample_table(col1) VALUES(' || numeric_variable || ')';

    OPEN cursor_variable FOR dynamic_statement;
    OPEN cursor_variable FOR 'SELECT ' || column_variable || ' FROM sample_table';
    OPEN cursor_variable FOR 'SELECT col1 FROM sample_table';

    
    c := DBMS_SQL.OPEN_CURSOR;
    dynamic_statement := 'SELECT * FROM sample_table';
    DBMS_SQL.PARSE(c, dynamic_statement);
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_dynamic_sql ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        dynamic_statement VARCHAR(100);
        numeric_variable INTEGER;
        dynamic_statement VARCHAR(100);
        column_variable VARCHAR(100);
        cursor_variable_res RESULTSET;
        c INTEGER;
        dynamic_statement VARCHAR(100);
    BEGIN
        dynamic_statement := 'INSERT INTO sample_table(col1) VALUES(1)';
        numeric_variable := 3;
        column_variable := 'col1';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE :dynamic_statement;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE 'INSERT INTO sample_table(col1) VALUES(' || NVL(:numeric_variable :: STRING, '') || ')';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_variable_res := (
            EXECUTE IMMEDIATE :dynamic_statement
        );
        LET cursor_variable CURSOR
        FOR
            cursor_variable_res;
        OPEN cursor_variable;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_variable_res := (
            EXECUTE IMMEDIATE 'SELECT ' || NVL(:column_variable :: STRING, '') || ' FROM
   sample_table'
        );
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0133 - THE CURSOR VARIABLE NAMED 'cursor_variable' HAS ALREADY BEEN ASSIGNED IN ANOTHER CURSOR ***/!!!
        LET cursor_variable CURSOR
        FOR
            cursor_variable_res;
        OPEN cursor_variable;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_variable_res := (
            EXECUTE IMMEDIATE 'SELECT col1 FROM
   sample_table'
        );
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0133 - THE CURSOR VARIABLE NAMED 'cursor_variable' HAS ALREADY BEEN ASSIGNED IN ANOTHER CURSOR ***/!!!
        LET cursor_variable CURSOR
        FOR
            cursor_variable_res;
        OPEN cursor_variable;
        c :=
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_SQL.OPEN_CURSOR' IS NOT CURRENTLY SUPPORTED. ***/!!!
        '' AS OPEN_CURSOR;
        dynamic_statement := 'SELECT * FROM
   sample_table';
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_SQL.PARSE' IS NOT CURRENTLY SUPPORTED. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    DBMS_SQL.PARSE(:c, :dynamic_statement);
    END;
$$;
```

#### SQL Server

##### Input

Copy code

```
 CREATE OR ALTER PROCEDURE transact_dynamic_sql
AS
BEGIN
    DECLARE @dynamicStatement AS VARCHAR(200);
    DECLARE @numericVariable AS VARCHAR(200);

    SET @dynamicStatement = 'INSERT INTO sample_table(col1) VALUES(1);';
    SET @numericVariable = '3';

    EXECUTE (@dynamicStatement);
    EXEC ('INSERT INTO sampleTable(col1) VALUES (' + @numericVariable + ');');
    EXECUTE ('INSERT INTO sampleTable(col1) VALUES(10);') AS USER = 'DbAdmin';
    
    INSERT INTO sampleTable EXECUTE sp_executesql @statement = 'SELECT * FROM sampleTable;';
    INSERT INTO sampleTable EXECUTE ('SELECT * FROM sampleTable;');
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE transact_dynamic_sql ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/13/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        DYNAMICSTATEMENT VARCHAR(200);
        NUMERICVARIABLE VARCHAR(200);
    BEGIN
         
         
        DYNAMICSTATEMENT := 'INSERT INTO sample_table (col1) VALUES(1);';
        NUMERICVARIABLE := '3';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE :DYNAMICSTATEMENT;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE 'INSERT INTO sampleTable (col1) VALUES (' || :NUMERICVARIABLE || ');';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - EXECUTE AS USER/LOGIN NOT SUPPORTED IN SNOWFLAKE ***/!!!
        EXECUTE IMMEDIATE 'INSERT INTO sampleTable (col1) VALUES(10);';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INSERT WITH EXECUTE' NODE ***/!!!
        INSERT INTO sampleTable EXECUTE IMMEDIATE 'SELECT
   *
FROM
   sampleTable;';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INSERT WITH EXECUTE' NODE ***/!!!
    INSERT INTO sampleTable EXECUTE IMMEDIATE 'SELECT
   *
FROM
   sampleTable;';
    END;
$$;
```

#### Issues Inside of Dynamic SQL

Something important to take into account is that when migrating dynamic SQL code, no type of issue inside of dynamic SQL will be reported in the output code or in the assessment reports. This will happen even when the documentation of an issue or the translation specification describes that an issue will always be added to the output code. Here is an example of a migration in Oracle where this situation might be encountered:

##### Oracle

Copy code

```
 SELECT dbms_random.value() FROM dual;

CREATE OR REPLACE PROCEDURE dynamic_sql_procedure
AS
  result VARCHAR(100) := 'SELECT dbms_random.value() from dual';
BEGIN
  NULL;  
END;
```

##### Snowflake

Copy code

```
 SELECT
  --** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
  DBMS_RANDOM.VALUE_UDF() FROM dual;

CREATE OR REPLACE PROCEDURE dynamic_sql_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    result VARCHAR(100) := 'SELECT
   DBMS_RANDOM.VALUE_UDF() from dual';
  BEGIN
    NULL;
  END;
$$;
```

In the previous example, the query and the variable assignment inside the procedure will be converted exactly the same, the difference is that in the dynamic SQL code the conversion issues will not be shown in the output code and in the assessment reports.

#### Best Practices

- Use this tag to track every dynamically built statement and review its correctness when troubleshooting.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0031

Function not supported.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Medium

#### Description

This warning is used to report that a specific ***built-in function*** of Teradata, Oracle, or SQL Server is not supported.

#### Example Code

##### **Input Code (Oracle):**

Copy code

```
 SELECT VALUE(ST) FROM SampleTable ST;
```

##### **Output Code:**

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - VALUE FUNCTION NOT SUPPORTED ***/!!!
 VALUE(ST) FROM
 SampleTable ST;
```

##### **Input Code (Teradata):**

Copy code

```
 SELECT HASHBUCKET(HASHROW(col1)) FROM my_table;
```

##### **Output Code:**

Copy code

```
 SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHBUCKET FUNCTION NOT SUPPORTED ***/!!!
   HASHBUCKET(
              !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHROW FUNCTION NOT SUPPORTED ***/!!!
              HASHROW(col1))
 FROM
   my_table;
```

Note

Teradata hash functions (HASHBUCKET, HASHROW, HASHAMP, HASHBAKAMP) are tied to Teradata’s shared-nothing AMP architecture for data distribution. Snowflake manages data distribution internally and has no equivalent mechanism. While Snowflake provides a [HASH](https://docs.snowflake.com/en/sql-reference/functions/hash) function, the HASH function uses a different algorithm, produces values in a different range (Snowflake HASH: signed 64-bit integers; HASHBUCKET: 0–1,048,575), and handles NULLs differently. For this reason, SnowConvert marks these functions with EWI markers rather than attempting an automatic translation.

#### Best Practices

- Please refer to the following links to check the current transformation of the specific function you are trying to convert:
  - [Oracle built-in functions](../../translation-references/oracle/functions/README)
  - [Teradata built-in functions](../../translation-references/teradata/sql-translation-reference/teradata-built-in-functions)
  - [SQL Server built-in functions](../../translation-references/transact/transact-built-in-functions)
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0032

External table requires an external stage to access an external location, define and replace the EXTERNAL\_STAGE placeholder

### Description

When transforming the CREATE EXTERNAL TABLE statement, an EXTERNAL\_STAGE placeholder will be generated that has to be replaced with the external stage created for connecting with the external location from Snowflake.

Please refer to the following guides to set up the necessary Storage Integration and External Stage in your Snowflake account:

- [For external tables referencing Amazon S3](https://docs.snowflake.com/en/user-guide/tables-external-s3)
- [For external tables referencing Google Cloud Storage](https://docs.snowflake.com/en/user-guide/tables-external-gcs)
- [For external tables referencing Azure Blob Storage](https://docs.snowflake.com/en/user-guide/tables-external-azure)

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
 CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER,
  Name STRING,
  Mail STRING,
  Position STRING,
  Salary INTEGER
)
OPTIONS(
  FORMAT='CSV',
  SKIP_LEADING_ROWS=1,
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Employees.csv']
);
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER AS CAST(GET_IGNORE_CASE($1, 'c1') AS INTEGER),
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c2') AS STRING),
  Mail STRING AS CAST(GET_IGNORE_CASE($1, 'c3') AS STRING),
  Position STRING AS CAST(GET_IGNORE_CASE($1, 'c4') AS STRING),
  Salary INTEGER AS CAST(GET_IGNORE_CASE($1, 'c5') AS INTEGER)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Employees.csv'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER =1);
```

#### Best Practices

- Set up your external connection in the Snowflake account and replace the EXTERNAL\_STAGE placeholder to complete the transformation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0033

Format removed, semantic information not found.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This warning appears when a column used in a ***CAST*** function with a specific output format was not found in the source code.

#### Example Code

##### Input Code (Teradata):

Copy code

```
 CREATE VIEW SampleView AS
SELECT
    DAY_DATE(FORMAT 'MMM-YYYY')(CHAR(8))
FROM
    SampleTable;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
CREATE OR REPLACE VIEW SampleView
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
    CAST(RPAD(TO_VARCHAR(
    DAY_DATE !!!RESOLVE EWI!!! /*** SSC-EWI-0033 - FORMAT 'MMM-YYYY' REMOVED, SEMANTIC INFORMATION NOT FOUND. ***/!!!), 8) AS CHAR(8))
    FROM
    SampleTable;
```

#### Best Practices

- Make sure all the dependencies(tables and views) related to the procedure statement are being migrated.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0034

Format removed.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This warning appears when the format of the column used in a CAST function is removed.

#### Example Code

##### Input Code (Teradata):

Copy code

```
 CREATE VIEW SampleView AS
SELECT
    DAY_DATE(FORMAT 'MMM-YYYY') + 1
FROM
    SampleTable;
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
CREATE OR REPLACE VIEW SampleView
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
    DAY_DATE !!!RESOLVE EWI!!! /*** SSC-EWI-0034 - FORMAT 'MMM-YYYY' REMOVED. ***/!!! + 1
FROM
    SampleTable;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0035

Check statement not supported.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

***CHECK*** constraint is not supported by Snowflake but it does not affect functionally.

#### Example Code

##### Input Code Oracle :

Copy code

```
 CREATE TABLE "Schema"."BaseTable"(
  "COLUMN1" VARCHAR2(255),
  CHECK ( COLUMN1 IS NOT NULL )
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE "Schema"."BaseTable" (
    "COLUMN1" VARCHAR(255),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
    CHECK ( COLUMN1 IS NOT NULL )
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
  ;
```

##### Input Code Teradata:

Copy code

```
 CREATE TABLE TABLE1,
    NO FALLBACK,
    NO BEFORE JOURNAL,
    NO AFTER JOURNAL
(
    COL0 BYTEINT,
    CONSTRAINT constraint_name CHECK (COL1 < COL2)
)
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TABLE1
(
    COL0 BYTEINT,
    !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
    CONSTRAINT constraint_name CHECK (COL1 < COL2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;
```

##### Input Code SqlServer

Copy code

```
 ALTER TABLE table_name2
ADD column_name VARCHAR(255)
CONSTRAINT constraint_name 
CHECK NOT FOR REPLICATION (column_name > 1);
```

##### Generated Code:

Copy code

```
 ALTER TABLE IF EXISTS table_name2
ADD column_name VARCHAR(255)
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
CONSTRAINT constraint_name
CHECK NOT FOR REPLICATION (column_name > 1);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0036

Data type converted to another data type.

### Severity

Low

#### Description

This warning appears when a data type is changed into another one.

#### Example Code

##### Source Code:

Copy code

```
 CREATE TABLE SampleTable (
    SampleYear INTERVAL YEAR(2),
    SampleMonth INTERVAL MONTH(2)
);
```

##### Converted Code:

Copy code

```
 CREATE OR REPLACE TABLE SampleTable (
    SampleYear VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR(2) DATA TYPE CONVERTED TO VARCHAR ***/!!!,
    SampleMonth VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL MONTH(2) DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0040

Clause Not Supported.

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This warning is added when there is a statement that is not supported in Snowflake.

#### Example Code

In the following example, the `PERCENT` clause from SQL Server is used on the SELECT query, this is not supported by Snowflake.

##### Input Code (SQL Server):

Copy code

```
 SELECT TOP 1 PERCENT * FROM SampleTable;
```

##### Source Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT
TOP 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
	*
FROM
	SampleTable;
```

#### Best Practices

- Review the original functionality of the statement and check if it is actually needed for your specific needs in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0041

The file has an unexpected encoding and was not translated

Note

This `EWI` is deprecated, please refer to [SSC-OOS-0001](../out-of-scope/generalOOS#ssc-oos-0001) documentation.

### Description

This issue happens when a source code file has an encoding format not recognized by the tool. Character encoding is the process of assigning numbers to graphical characters, in this context written characters of human language, thus the error indicates the conversion tool could not recognize certain characters.

#### Best Practices

- All files in the input folder should have the same encoding to avoid this error.
- The appropriate encoding should be selected through the conversion settings or by utilizing the –encoding conversion parameter with the [SnowConvert AI CLI](/migrations/aim-for-datawarehouses/manual-migration/README). To determine which encoding to select online tools such as [Free Online Formater](https://freeonlineformatter.com/encoding-string) can be used or run the command `file -i *` in the case of Linux or OS.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0045

Column Name is Snowflake Reserved Keyword.

### Severity

Medium

#### Description

In some cases, column names that are valid in the source language may conflict with Snowflake’s reserved keywords. These conflicts arise because Snowflake reserves a set of keywords that cannot be used directly as column names without special handling. For details, refer to Snowflake’s official documentation on [reserved and limited keywords](https://docs.snowflake.com/en/sql-reference/reserved-keywords).

#### Code example

##### Input

Copy code

```
 CREATE TABLE T1
(
    LOCALTIME VARCHAR,
    CURRENT_USER VARCHAR
);
```

##### Output

Copy code

```
 CREATE OR REPLACE TABLE T1
    (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0045 - COLUMN NAME 'LOCALTIME' IS A SNOWFLAKE RESERVED KEYWORD ***/!!!
    "LOCALTIME" VARCHAR,
    !!!RESOLVE EWI!!! /*** SSC-EWI-0045 - COLUMN NAME 'CURRENT_USER' IS A SNOWFLAKE RESERVED KEYWORD ***/!!!
    "CURRENT_USER" VARCHAR
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

#### Best Practices

- Consider renaming the columns that use names that are not supported in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0046

Nested function/procedure declarations are considered a complex pattern and not supported in Snowflake.

### Severity

Critical

#### Description

Snowflake does not support the declaration of nested functions/procedures, this warning is added to any create function or create procedure statement in which nested declarations were found.

#### Code example

##### Input

Copy code

```
 CREATE OR REPLACE FUNCTION myFunction
RETURN INTEGER
IS
   total_count INTEGER;
   -- Function Declaration
   FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER;
   FUNCTION function_definition
   RETURN INTEGER
   IS
   count INTEGER;
   PROCEDURE procedure_declaration(param1 INTEGER)
   IS
       BEGIN
            NULL;
       END;
  BEGIN
    RETURN count;
  end;
BEGIN
    -- Your logic to calculate the total employee count goes here
    RETURN total_count;
END;
```

##### Output

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0046 - NESTED FUNCTION/PROCEDURE DECLARATIONS ARE NOT SUPPORTED IN SNOWFLAKE. ***/!!!
CREATE OR REPLACE FUNCTION myFunction ()
RETURNS FLOAT
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
AS
$$
  let TOTAL_COUNT;
  !!!RESOLVE EWI!!! /*** SSC-EWI-OR0057 - TRANSFORMATION FOR NESTED FUNCTION IS NOT SUPPORTED IN THIS SCENARIO ***/!!!
  /*    -- Function Declaration
     FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER; */
  // Function Declaration
  ;
  !!!RESOLVE EWI!!! /*** SSC-EWI-OR0057 - TRANSFORMATION FOR NESTED FUNCTION IS NOT SUPPORTED IN THIS SCENARIO ***/!!!
  /*    FUNCTION function_definition
     RETURN INTEGER
     IS
     count INTEGER;
     PROCEDURE procedure_declaration(param1 INTEGER)
     IS
         BEGIN
              NULL;
         END;
    BEGIN
      RETURN count;
    end; */
  ;
  // Your logic to calculate the total employee count goes here
  return TOTAL_COUNT;
$$;
```

#### Best Practices

- Remove the nested declarations from the function/procedure.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0049

A Global Temporary Table is being referenced.

Note

This `EWI` is deprecated, please refer to [SSC-FDM-0023](../functional-difference/generalFDM#ssc-fdm-0023) documentation.

### Severity

Medium

#### Description

Global Temporary tables are transformed into regular Create Table. References to these tables may behave different than expected.

#### Code example

##### Input

Copy code

```
 create global temporary table t1 
    (col1 varchar); 
create view view1 as 
    select col1 from t1;
```

##### Output

Copy code

```
 --** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE t1
    (col1 varchar)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW view1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
select col1 from
    !!!RESOLVE EWI!!! /*** SSC-EWI-0049 - A Global Temporary Table is being referenced ***/!!!
    t1;
```

#### Related Issues

- [SSC-FDM-0009](../functional-difference/generalFDM#ssc-fdm-0009): GLOBAL TEMPORARY TABLE functionality not supported.

### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0052

Unusable object

### Severity

Medium

#### Description

This error happens when the source code uses a parameter or variable that is not supported or was not recognized by the conversion tool.

#### Example code

##### Input Code (Oracle):

Copy code

```
 -- Additional Params: -t JavaScript
CREATE OR REPLACE PROCEDURE PROCEDURE_PARAMETERS(PARAM SDO_GEOMETRY)
AS
    VARIABLE SDO_GEOMETRY;
BEGIN
    VARIABLE := PARAM;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROCEDURE_PARAMETERS (PARAM GEOMETRY)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // REGION SnowConvert AI Helpers Code
    var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
    var fixBind = function (arg) {
        arg = arg instanceof Date ? formatDate(arg) : IS_NULL(arg) ? null : arg;
        return arg;
    };
    var SQL = {
        FOUND : false,
        NOTFOUND : false,
        ROWCOUNT : 0,
        ISOPEN : false
    };
    var _RS, _ROWS, SQLERRM = "normal, successful completion", SQLCODE = 0;
    var getObj = (_rs) => Object.assign(new Object(),_rs);
    var getRow = (_rs) => (values = Object.values(_rs)) && (values = values.splice(-1 * _rs.getColumnCount())) && values;
    var fetch = (_RS,_ROWS,fmode) => _RS.getRowCount() && _ROWS.next() && (fmode ? getObj : getRow)(_ROWS) || (fmode ? new Object() : []);
    var EXEC = function (stmt,binds,opts) {
        try {
            binds = !(arguments[1] instanceof Array) && ((opts = arguments[1]) && []) || (binds || []);
            opts = opts || new Object();
            binds = binds ? binds.map(fixBind) : binds;
            _RS = snowflake.createStatement({
                    sqlText : stmt,
                    binds : binds
                });
            _ROWS = _RS.execute();
            if (opts.sql !== 0) {
                var isSelect = stmt.toUpperCase().trimStart().startsWith("SELECT");
                var affectedRows = isSelect ? _RS.getRowCount() : _RS.getNumRowsAffected();
                SQL.FOUND = affectedRows != 0;
                SQL.NOTFOUND = affectedRows == 0;
                SQL.ROWCOUNT = affectedRows;
            }
            if (opts.row === 2) {
                return _ROWS;
            }
            var INTO = function (opts) {
                if (opts.vars == 1 && _RS.getColumnCount() == 1 && _ROWS.next()) {
                    return _ROWS.getColumnValue(1);
                }
                if (opts.rec instanceof Object && _ROWS.next()) {
                    var recordKeys = Object.keys(opts.rec);
                    Object.assign(opts.rec,Object.fromEntries(new Map(getRow(_ROWS).map((element,Index) => [recordKeys[Index],element]))))
                    return opts.rec;
                }
                return fetch(_RS,_ROWS,opts.row);
            };
            var BULK_INTO_COLLECTION = function (into) {
                for(let i = 0;i < _RS.getRowCount();i++) {
                    FETCH_INTO_COLLECTIONS(into,fetch(_RS,_ROWS,opts.row));
                }
                return into;
            };
            if (_ROWS.getRowCount() > 0) {
                return _ROWS.getRowCount() == 1 ? INTO(opts) : BULK_INTO_COLLECTION(opts);
            }
        } catch(error) {
            RAISE(error.code,error.name,error.message)
        }
    };
    var RAISE = function (code,name,message) {
        message === undefined && ([name,message] = [message,name])
        var error = new Error(message);
        error.name = name
        SQLERRM = `${(SQLCODE = (error.code = code))}: ${message}`
        throw error;
    };
    var FETCH_INTO_COLLECTIONS = function (collections,fetchValues) {
        for(let i = 0;i < collections.length;i++) {
            collections[i].push(fetchValues[i]);
        }
    };
    var IS_NULL = (arg) => !(arg || arg === 0);
    // END REGION

    let VARIABLE = new SDO_GEOMETRY();
    VARIABLE =
        !!!RESOLVE EWI!!! /*** SSC-EWI-0052 - UNUSABLE OBJECT PARAM, ITS DATATYPE WAS NOT TRANSFORMED ***/!!!
        PARAM;
$$;
```

#### Best Practices

- Look for an alternative for the used data type.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0053

Object may not work.

### Severity

Low

#### Description

This error happens when the conversion tool could not determine the data type of a variable. This may happen because the declaration of a variable could be missing.

#### Example code

##### Input Code (Oracle):

Copy code

```
 -- Additional Params: -t javascript
CREATE OR REPLACE PROCEDURE PROCEDURE_VARIABLES
AS
    VARIABLE INTEGER;
BEGIN
    VARIABLE := ANOTHER_VARIABLE;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROCEDURE_VARIABLES ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // REGION SnowConvert AI Helpers Code
    var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
    var fixBind = function (arg) {
        arg = arg instanceof Date ? formatDate(arg) : IS_NULL(arg) ? null : arg;
        return arg;
    };
    var SQL = {
        FOUND : false,
        NOTFOUND : false,
        ROWCOUNT : 0,
        ISOPEN : false
    };
    var _RS, _ROWS, SQLERRM = "normal, successful completion", SQLCODE = 0;
    var getObj = (_rs) => Object.assign(new Object(),_rs);
    var getRow = (_rs) => (values = Object.values(_rs)) && (values = values.splice(-1 * _rs.getColumnCount())) && values;
    var fetch = (_RS,_ROWS,fmode) => _RS.getRowCount() && _ROWS.next() && (fmode ? getObj : getRow)(_ROWS) || (fmode ? new Object() : []);
    var EXEC = function (stmt,binds,opts) {
        try {
            binds = !(arguments[1] instanceof Array) && ((opts = arguments[1]) && []) || (binds || []);
            opts = opts || new Object();
            binds = binds ? binds.map(fixBind) : binds;
            _RS = snowflake.createStatement({
                    sqlText : stmt,
                    binds : binds
                });
            _ROWS = _RS.execute();
            if (opts.sql !== 0) {
                var isSelect = stmt.toUpperCase().trimStart().startsWith("SELECT");
                var affectedRows = isSelect ? _RS.getRowCount() : _RS.getNumRowsAffected();
                SQL.FOUND = affectedRows != 0;
                SQL.NOTFOUND = affectedRows == 0;
                SQL.ROWCOUNT = affectedRows;
            }
            if (opts.row === 2) {
                return _ROWS;
            }
            var INTO = function (opts) {
                if (opts.vars == 1 && _RS.getColumnCount() == 1 && _ROWS.next()) {
                    return _ROWS.getColumnValue(1);
                }
                if (opts.rec instanceof Object && _ROWS.next()) {
                    var recordKeys = Object.keys(opts.rec);
                    Object.assign(opts.rec,Object.fromEntries(new Map(getRow(_ROWS).map((element,Index) => [recordKeys[Index],element]))))
                    return opts.rec;
                }
                return fetch(_RS,_ROWS,opts.row);
            };
            var BULK_INTO_COLLECTION = function (into) {
                for(let i = 0;i < _RS.getRowCount();i++) {
                    FETCH_INTO_COLLECTIONS(into,fetch(_RS,_ROWS,opts.row));
                }
                return into;
            };
            if (_ROWS.getRowCount() > 0) {
                return _ROWS.getRowCount() == 1 ? INTO(opts) : BULK_INTO_COLLECTION(opts);
            }
        } catch(error) {
            RAISE(error.code,error.name,error.message)
        }
    };
    var RAISE = function (code,name,message) {
        message === undefined && ([name,message] = [message,name])
        var error = new Error(message);
        error.name = name
        SQLERRM = `${(SQLCODE = (error.code = code))}: ${message}`
        throw error;
    };
    var FETCH_INTO_COLLECTIONS = function (collections,fetchValues) {
        for(let i = 0;i < collections.length;i++) {
            collections[i].push(fetchValues[i]);
        }
    };
    var IS_NULL = (arg) => !(arg || arg === 0);
    // END REGION

    let VARIABLE;
    VARIABLE =
        !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT ANOTHER_VARIABLE MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
        ANOTHER_VARIABLE;
$$;
```

#### Best Practices

- Make sure the input code has the variable declared.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0054

Unsupported outer join subquery

Note

Some parts in the output code are omitted for clarity reasons.

### Severity

Low

#### Description

This error happens when a correlated subquery is found within an OR logical expression of an OUTER JOIN (Left, Right or Full). In those cases they could produce inconsistent results or cause the following error:

**`SQL compilation error: Unsupported subquery type cannot be evaluated.`**

These limitations with subqueries are briefly mentioned in [Snowflake documentation](https://docs.snowflake.com/en/user-guide/querying-subqueries.html#limitations) and some information about them can also be found in [Snowflake forums.](https://community.snowflake.com/s/question/0D53r00009mIxwYCAS/sql-compilation-error-unsupported-subquery-type-cannot-be-evaluated)

#### Example code

##### Input Code (Teradata):

Copy code

```
 SELECT a.Column1, b.Column2
FROM
    TableA a
    LEFT JOIN TableB b ON (a.Column1 = b.Column1)
    AND (
        a.Column2 = b.Column2
        OR EXISTS(
            SELECT * FROM Table3 c
            WHERE c.Column1 = a.Column1
        )
    );
```

##### Generated Code:

Copy code

```
 // SnowConvert AI Helpers Code section is omitted.
SELECT
    a.Column1,
    b.Column2
FROM
    TableA a
   LEFT JOIN
        TableB b ON (a.Column1 = b.Column1)
   AND (
       a.Column2 = b.Column2
       OR EXISTS
                !!!RESOLVE EWI!!! /*** SSC-EWI-0054 - CORRELATED SUBQUERIES WITHIN AN OR EXPRESSION OF AN OUTER JOIN COULD CAUSE COMPILATION ERRORS ***/!!!(
                    SELECT
                        * FROM
                        Table3 c
                               WHERE c.Column1 = a.Column1
       )
   );
```

#### Best Practices

- Verify the output code does not produce a compilation error.
- Verify the output code’s functional equivalence.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0056

Custom Types Not Supported

Note

**Deprecation:** This issue code is deprecated. SnowConvert now translates many Oracle and cross-dialect `CREATE TYPE` definitions to [Snowflake native user-defined types](https://docs.snowflake.com/en/sql-reference/sql/create-type) where supported. This entry’s **Input Code** and **Generated Code** examples are kept for historical reference and may not match current tool output. For current behavior, see the translation reference for your source: [Oracle](../../translation-references/oracle/sql-translation-reference/create_type), [IBM DB2](../../translation-references/db2/db2-create-type), [Teradata](../../translation-references/teradata/sql-translation-reference/teradata-create-type), [SQL Server / Azure Synapse](../../translation-references/transact/transact-create-type), [PostgreSQL / Greenplum / Netezza](../../translation-references/postgres/ddls/postgresql-create-type), [Sybase IQ](../../translation-references/sybase/sybase-create-type).

### Severity

Low

#### Description

This message appears when a user-defined type (UDT) is defined. User-defined types are not supported in Snowflake, so references to the custom type are changed to an appropriate Snowflake type (such as VARIANT or OBJECT).

Snowflake has a UDT Private Preview feature available. For more information about accessing this feature, please contact [udt-prpr@snowflake.com](mailto:udt-prpr@snowflake.com).

Note

The type definition is commented on but is still being taken into account for resolving usages, see SSC-EWI-0062 for more information.

#### Example code

##### Input Code (Oracle):

Copy code

```
 CREATE TYPE type1 AS OBJECT (column1 INT);

CREATE OR REPLACE PROCEDURE record_procedure
IS
    TYPE record_typ IS RECORD(col1 INTEGER, col2 FLOAT);
BEGIN
    NULL;
END;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - USER-DEFINED TYPES ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES WERE CHANGED TO VARIANT. A UDT PRIVATE PREVIEW FEATURE IS AVAILABLE, FOR MORE INFORMATION, PLEASE CONTACT udt-prpr@snowflake.com ***/!!!
CREATE TYPE type1 AS OBJECT (column1 INT)
;

CREATE OR REPLACE PROCEDURE record_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - USER-DEFINED TYPES ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES WERE CHANGED TO OBJECT. A UDT PRIVATE PREVIEW FEATURE IS AVAILABLE, FOR MORE INFORMATION, PLEASE CONTACT udt-prpr@snowflake.com ***/!!!
        TYPE record_typ IS RECORD(col1 INTEGER, col2 FLOAT);
    BEGIN
        NULL;
    END;
$$;
```

#### Best Practices

- Consider using Snowflake’s OBJECT or VARIANT data types as alternatives to user-defined types for storing complex structured data.
- For more information about the UDT Private Preview feature, contact [udt-prpr@snowflake.com](mailto:udt-prpr@snowflake.com).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0058

Functionality is not currently supported by Snowflake Scripting

### Severity

Medium

#### Description

This error happens when a statement used in a create procedure is not currently supported by Snowflake Scripting.

#### Example code

##### Input Code (Oracle):

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC01
IS
  number_variable INTEGER;
BEGIN
  EXECUTE IMMEDIATE 'SELECT 1 FROM DUAL' INTO number_variable;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC01 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    number_variable INTEGER;
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
    EXECUTE IMMEDIATE 'SELECT 1 FROM DUAL'
                                           !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                                           INTO number_variable;
  END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0062

Custom type usage changed to variant

### Severity

Low

#### Description

This message appears when a Custom Type is referenced, and then its usage is changed to a variant.

Note

This message is heavily related to SSC-EWI-0056.

#### Example code

##### Input Code (Oracle):

Copy code

```
 CREATE TYPE type1 AS OBJECT(type1_column1 INT);

CREATE TABLE table1
(
column1 type1
);
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE type1 AS OBJECT(type1_column1 INT)
;

CREATE OR REPLACE TABLE table1
(
column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'type1' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE VIEW table1_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
column1:type1_column1 :: VARCHAR AS type1_column1
FROM
table1;
```

#### Best Practices

- Remember to transform all of its input data into a Variant-compliant data type as well.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-0064

Referenced custom type in query not found

### Severity

High

#### Description

This error happens when a Custom Type is referenced in a source for a DML statement, but the Custom Type was never defined.  
For example in a Table Column whose type might be a UDT but it was never defined.

Warning

Not to be confused with SSC-FDM-0015, which is when it was referenced in a DDL query.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 --Type was never defined
--CREATE TYPE type1;

CREATE TABLE table1
(
--the type will be unresolved
column1 type1
);

SELECT
column1
FROM table1;
```

##### Generated Code:

Copy code

```
 --Type was never defined
--CREATE TYPE type1;
!!!RESOLVE EWI!!! /*** SSC-EWI-0050 - MISSING DEPENDENT OBJECT "type1" ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0063 - 'PUBLIC.table1_view' ADDED BECAUSE 'table1' USED A CUSTOM TYPE ***/!!!
CREATE OR REPLACE TABLE table1
(
--the type will be unresolved
column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0064 - REFERENCED CUSTOM TYPE 'type1' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/!!! /*** SSC-FDM-0015 - DATA TYPE 'type1' NOT RECOGNIZED ***/
);

CREATE OR REPLACE VIEW PUBLIC.table1_view
AS
SELECT
column1
FROM
table1;

SELECT
column1 !!!RESOLVE EWI!!! /*** SSC-EWI-0064 - REFERENCED CUSTOM TYPE 'type1' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/!!!
FROM
table1;
```

#### Best Practices

- Verify that the type that was referenced was defined in the input code.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0066

Expression not supported in Snowflake.

### Severity

High

#### Description

This error is used to inform that a *specific* **expression** is not supported in Snowflake.

#### Example Code

##### **Input Code:**

Copy code

```
 SELECT * from T1 where (cast('2016-03-17' as DATE), 
       cast('2016-03-21' as DATE)) OVERLAPS
       (cast('2016-03-20' as DATE), cast('2016-03-22' as DATE));
```

##### **Output Code:**

Copy code

```
 SELECT * from
       T1
where
       !!!RESOLVE EWI!!! /*** SSC-EWI-0066 - EXPRESSION 'OVERLAPS' IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! (cast('2016-03-17' as DATE),
       cast('2016-03-21' as DATE)) OVERLAPS
       (cast('2016-03-20' as DATE), cast('2016-03-22' as DATE));
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0067

UDF was transformed to Snowflake procedure, calling procedures inside a query is not supported.

### Severity

High

#### Description

This error is added when a call to a UDF (user defined function) is found inside a query. Oracle UDFs and UDFs inside packages and some SQL Server UDFs, are being transformed to Snowflake Stored Procedures, which can not be called from a query.

The function is transformed to a Stored procedure to maintain functional equivalence and the function call is transformed to an empty Snowflake UDF function.

Note

This EWI is strongly related to [SSC-EWI-0068](../functional-difference/generalFDM#ssc-fdm-0029)

#### Example Code

##### SQL Server:

##### Input Code

Copy code

```
 CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS INT
AS
BEGIN
    DECLARE @i int = 0, @p int;
    Select @p = COUNT(*) FROM PURCHASING.VENDOR
    
    WHILE (@p < 1000)
    BEGIN
        SET @i = @i + 1
        SET @p = @p + @i
    END
        
    IF (@i = 6)
        RETURN 1
    
    RETURN @p
END;
GO

SELECT PURCHASING.FOO() AS RESULT;
```

##### Generated Code

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "PURCHASING.VENDOR" **
CREATE OR REPLACE PROCEDURE PURCHASING.FOO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I INT := 0;
        P INT;
    BEGIN
         
        Select
            COUNT(*)
        INTO
            :P
 FROM
            PURCHASING.VENDOR;
        WHILE (:P < 1000) LOOP
            I := :I + 1;
            P := :P + :I;
        END LOOP;
        IF ((:I = 6)) THEN
            RETURN 1;
        END IF;
        RETURN :P;
    END;
$$;

SELECT
    PURCHASING.FOO() !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! AS RESULT;
```

##### Oracle:

##### Input Code

Copy code

```
 CREATE FUNCTION employee_function (param1 in NUMBER) RETURN NUMBER is
  var1    employees.employee_ID%TYPE;
  var2    employees.manager_ID%TYPE;
  var3    employees.title%TYPE;
BEGIN
  SELECT employee_ID, manager_ID, title
  INTO var1, var2, var3
  FROM employees
    START WITH manager_ID = param1
    CONNECT BY manager_ID = PRIOR employee_id;
  RETURN var1;
EXCEPTION
   WHEN no_data_found THEN RETURN param1;
END employee_function;

SELECT employee_function(2) FROM employees;
```

##### Generated Code

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employees" **
CREATE OR REPLACE PROCEDURE employee_function (param1 NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1    employees.employee_ID%TYPE;
    var2    employees.manager_ID%TYPE;
    var3    employees.title%TYPE;
  BEGIN
    SELECT employee_ID, manager_ID, title
    INTO
      :var1,
      :var2,
      :var3
    FROM
      employees
      START WITH manager_ID = :param1
    CONNECT BY
      manager_ID = PRIOR employee_id;
    RETURN :var1;
  EXCEPTION
     WHEN no_data_found THEN
      RETURN :param1;
  END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employees" **

SELECT
  !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! employee_function(2) FROM
  employees;
```

#### Best Practices

- The source code may need to be restructured to fit with the Snowflake user-defined functions [approach](https://docs.snowflake.com/en/sql-reference/user-defined-functions.html#udfs-user-defined-functions).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0068

User defined function was transformed to a Snowflake procedure.

Snowflake user defined functions do not support the same features as Oracle or SQL Server. To maintain the functional equivalence the function is transformed to a Snowflake stored procedure. This will affect their usage in queries.

### Example Code

#### SQL Server:

##### Input Code

Copy code

```
 CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS INT
AS
BEGIN
    DECLARE @i int = 0, @p int;
    Select @p = COUNT(*) FROM PURCHASING.VENDOR
    
    WHILE (@p < 1000)
    BEGIN
        SET @i = @i + 1
        SET @p = @p + @i
    END
        
    IF (@i = 6)
        RETURN 1
    
    RETURN @p
END;
```

##### Generated Code

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE PURCHASING.FOO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "06/25/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I INT := 0;
        P INT;
    BEGIN
         
        Select
            COUNT(*)
        INTO
            :P
 FROM
            PURCHASING.VENDOR;
        WHILE (:P < 1000) LOOP
            I := :I + 1;
            P := :P + :I;
        END LOOP;
        IF ((:I = 6)) THEN
            RETURN 1;
        END IF;
        RETURN :P;
    END;
$$;
```

##### Oracle:

##### Input Code

Copy code

```
CREATE OR REPLACE FUNCTION FUN1(PAR1 VARCHAR)
RETURN VARCHAR
IS
    VAR1 VARCHAR(20);
    VAR2 VARCHAR(20);
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 where col1 = 1;
    VAR2 := PAR1 || VAR1;
    RETURN VAR2;
END;
/
```

##### Generated Code

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE FUN1(PAR1 VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    VAR1 VARCHAR(20);
    VAR2 VARCHAR(20);
  BEGIN
    SELECT COL1 INTO
      :VAR1
    FROM
      TABLE1
    where col1 = 1;
    VAR2 := NVL(:PAR1 :: STRING, '') || NVL(:VAR1 :: STRING, '');
    RETURN :VAR2;
  END;
$$;
```

### Best Practices

- Separate the inside queries to maintain the same logic.
- The source code may need to be restructured to fit with the Snowflake user-defined functions [approach](https://docs.snowflake.com/en/sql-reference/user-defined-functions.html#udfs-user-defined-functions).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0073

Pending Functional Equivalence Review

### Severity

Medium

#### Description

This EWI is added when there is a grammar clause in the input platform that has not been reviewed by the development team. The code may require manual revision for it to work in Snowflake.

#### Example Code

##### SQLServer:

##### Input Code

Copy code

```
 CREATE OR ALTER PROC SampleProcedure
AS
BEGIN
   INSERT INTO aTable (columnA = 'varcharValue', columnB = 1);
   INSERT exampleTable VALUES ('Hello', 23);
   INSERT INTO exampleTable DEFAULT VALUES;
END
```

##### Generated Code

Copy code

```
 CREATE OR REPLACE PROCEDURE SampleProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      INSERT INTO aTable (columnA = 'varcharValue', columnB = 1);
      INSERT INTO exampleTable VALUES ('Hello', 23);
      !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INSERT WITH DEFAULT VALUES' NODE ***/!!!
      INSERT INTO exampleTable DEFAULT VALUES;
   END;
$$;
```

Notice in line 6 of the input code, that there is a reference to a `INSERT` statement with `DEFAULT VALUES`, this statement is currently not supported and that is why in lines 11 and 12 the EWI is generated.

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0077

Cycle found between CTE calls. CTEs cannot be ordered.

### Severity

Low

#### Description

This warning is added when a query that has several CTE (Common Table Expression) reference calls creates a cycle that cannot determine the calling order of the CTEs, and then the CTEs cannot be ordered and the query will remain as the source.

#### Example Code

##### Input Code (Teradata):

Copy code

```
 WITH t1(c1) as (SELECT c1 FROM t2),
     t2(c2) as (SELECT c2 FROM t3),
     RECURSIVE t3(c3) as (SELECT c3, someOtherColumn FROM t1, t3)
     SELECT * FROM t1;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0077 - CYCLE FOUND BETWEEN CTE REFERENCE CALLS, CTES CANNOT BE ORDERED AND THE QUERY WILL REMAIN AS ORIGINAL ***/!!!
WITH RECURSIVE t1(c1) AS
(
     SELECT
          c1 FROM t2
),
t2(c2) AS
(
     SELECT
          c2 FROM t3
),
t3(c3) AS
(
     SELECT
          c3,
          someOtherColumn FROM t1, t3
)
SELECT
     * FROM t1;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0080

Default value is not allowed on binary columns

### Severity

Low

#### Description

This EWI is added when the source code has a default value for BINARY data type, which is not supported in Snowflake SQL

##### Example Code

**Input Code (SqlServer):**

Copy code

```
 create table test1345
(
  key1 binary default 0
);
```

**Output Code:**

Copy code

```
 CREATE OR REPLACE TABLE test1345
(
  key1 BINARY
              !!!RESOLVE EWI!!! /*** SSC-EWI-0080 - DEFAULT VALUE IS NOT ALLOWED ON BINARY COLUMNS ***/!!!
              default 0
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

##### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0084

XMLTABLE is not supported.

### Severity

High

#### Description

XMLTABLE function is not currently supported.

#### Example Code

##### Input Code (DB2):

Copy code

```
 SELECT
    *
FROM
    XMLTABLE(
        'stringValue' PASSING BY REF passingExpr AS AliasName
    ) AS XMLTABLENAME
```

##### Generated Code:

Copy code

```
 SELECT
    *
FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-0084 - XMLTABLE IS NOT SUPPORTED BY SNOWFLAKE ***/!!!
    XMLTABLE(
        'stringValue' PASSING BY REF passingExpr AS AliasName
    ) AS XMLTABLENAME
```

#### Best Practices

- Check this [blog](https://www.snowflake.com/blog/easily-load-xml-sql/) for XML transformations in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0086

Replaced invalid characters for new identifier

Note

This `EWI` is deprecated, please refer to [SSC-FDM-0030](../functional-difference/generalFDM#ssc-fdm-0030) documentation.

### Severity

Low

#### Description

The given identifier has invalid characters for the output language. Those characters were replaced with their UTF-8 codes.

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE PROCEDURE PROC1
AS
    "VAR0" INT;
    "VAR`/1ͷ" VARCHAR(20);
    "o*/o" FLOAT;
    " . " INT;
    ". ." INT;
    "123Name" INT;
    "return" INT;
    yield INT;
    ident#10 INT;
BEGIN
    NULL;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        "VAR0" INT;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0086 - IDENTIFIER '"VAR`/1ͷ"' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES ***/!!!
        VAR_u60_u2F1ͷ VARCHAR(20);
        !!!RESOLVE EWI!!! /*** SSC-EWI-0086 - IDENTIFIER '"o*/o"' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES ***/!!!
        o_u2A_u2Fo FLOAT;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0086 - IDENTIFIER '" . "' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES ***/!!!
        _u20_u2E_u20 INT;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0086 - IDENTIFIER '". ."' HAS INVALID CHARACTERS. CHARACTERS WERE REPLACED WITH THEIR UTF-8 CODES ***/!!!
        _u2E_u20_u2E INT;
        "123Name" INT;
        "return" INT;
        yield INT;
        IDENT_HASHTAG_10 INT;
    BEGIN
        NULL;
    END;
$$;
```

#### Best Practices

- No end-user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0092

Materialized View was converted to regular View.

Danger

Deprecated

### Severity

Low

#### Description

Currently, all Materialized Views are being converted to regular Views. This process eliminates additional clauses that the Materialized Views may have had. For more information, see [Limitations on creating materialized views](https://docs.snowflake.com/en/user-guide/views-materialized.html#label-limitations-on-creating-materialized-views).

#### Example Code

##### Input Code:

Copy code

```
 CREATE MATERIALIZED VIEW MATERIALIZED_VIEW1
SEGMENT CREATION IMMEDIATE
ORGANIZATION HEAP PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
INMEMORY PRIORITY NONE MEMCOMPRESS FOR QUERY LOW DISTRIBUTE AUTO NO DUPLICATE
AS
select
   *
from
   aTable;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0092 - MATERIALIZED VIEW WAS CONVERTED TO REGULAR VIEW. ***/!!!
CREATE OR REPLACE VIEW MATERIALIZED_VIEW1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
select
   *
from
   aTable;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0094

Label declaration not supported

### Severity

Low

#### Description

Currently there is no equivalent for labels declaration in Snow Scripting, so an EWI is added, and the label is commented out

#### Example Code

##### Input Code (Oracle):

Copy code

```
 CREATE OR REPLACE PROCEDURE Example ( grade NUMBER )
IS
BEGIN
	<<CASE1>><<CASE2>>
	CASE grade
		WHEN 10 THEN NULL;
		ELSE NULL;
	END CASE CASE1;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE Example (grade NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		!!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <<CASE1>><<CASE2>> ***/!!!
		CASE :grade
			WHEN 10 THEN
				NULL;
			ELSE NULL;
		END CASE;
	END;
$$;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0095

Create Type not supported in Snowflake

Note

**Deprecation:** This issue code is deprecated. Snowflake supports native user-defined types, and SnowConvert emits `CREATE TYPE` for many supported patterns. This entry’s **Input Code** and **Generated Code** examples are preserved as historical reference. For current conversion behavior, see the translation reference for your source: [Oracle](../../translation-references/oracle/sql-translation-reference/create_type), [IBM DB2](../../translation-references/db2/db2-create-type), [Teradata](../../translation-references/teradata/sql-translation-reference/teradata-create-type), [SQL Server / Azure Synapse](../../translation-references/transact/transact-create-type), [PostgreSQL / Greenplum / Netezza](../../translation-references/postgres/ddls/postgresql-create-type), [Sybase IQ](../../translation-references/sybase/sybase-create-type).

### Severity

High

#### Description

User-defined types (UDTs) created with the `CREATE TYPE` statement are not currently supported in Snowflake. When a `CREATE TYPE` statement is encountered, this warning is added to indicate that manual intervention is required.

Snowflake has a UDT Private Preview feature available. For more information about accessing this feature, please contact [udt-prpr@snowflake.com](mailto:udt-prpr@snowflake.com).

#### Example Code

##### Input Code (Oracle):

Copy code

```
CREATE OR REPLACE TYPE address_type AS OBJECT (
    street VARCHAR2(100),
    city VARCHAR2(50),
    state VARCHAR2(2),
    zip_code VARCHAR2(10)
);
```

##### Generated Code:

Copy code

```
--** SSC-EWI-0095 - USER-DEFINED TYPE: 'address_type' IS CURRENTLY NOT SUPPORTED IN SNOWFLAKE. A UDT PRIVATE PREVIEW FEATURE IS AVAILABLE, FOR MORE INFORMATION, PLEASE CONTACT udt-prpr@snowflake.com **
CREATE OR REPLACE TYPE address_type AS OBJECT (
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip_code VARCHAR(10)
);
```

#### Best Practices

- Consider using Snowflake’s OBJECT or VARIANT data types as alternatives to user-defined types for storing complex structured data.
- For more information about the UDT Private Preview feature, contact [udt-prpr@snowflake.com](mailto:udt-prpr@snowflake.com).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0101

Commented out transaction label name because is not applicable in Snowflake

### Severity

Low

#### Description

Snowflake does not operate transaction label names because there should not be nested transactions to identify in different COMMIT or ROLLBACK statements.

#### Example code

##### Input Code (SQL Server):

Copy code

```
 CREATE PROCEDURE TestTransaction
AS
BEGIN
    DROP TABLE IF EXISTS NEWTABLE;
    CREATE TABLE NEWTABLE(COL1 INT, COL2 VARCHAR);
      BEGIN TRANSACTION LabelA;
        INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
        INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
      COMMIT TRANSACTION LabelA;
END
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE TestTransaction ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DROP TABLE IF EXISTS NEWTABLE;
        CREATE OR REPLACE TABLE NEWTABLE (
            COL1 INT,
            COL2 VARCHAR
        );
            BEGIN TRANSACTION
            !!!RESOLVE EWI!!! /*** SSC-EWI-0101 - COMMENTED OUT TRANSACTION LABEL NAME BECAUSE IS NOT APPLICABLE IN SNOWFLAKE ***/!!!
            LabelA;
            INSERT INTO NEWTABLE VALUES (1, 'MICHAEL');
        INSERT INTO NEWTABLE VALUES(2, 'JACKSON');
            COMMIT;
    END;
$$;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0102

Removed statement option from code, already handled in conversion to Snowflake

Note

This `EWI` is deprecated.

### Severity

Low

#### Description

Snowflake statements could remove some options when they are handled by the conversion rule. So it will be removed from the output code but the functionality is equivalent.

#### Example code

##### Input Code (PostgreSQL):

Copy code

```
 -- Case 1:
TRUNCATE ONLY table_base2 RESTART IDENTITY CASCADE;

-- Case 2:
TRUNCATE TABLE table_inherit_and_generated RESTART IDENTITY CASCADE;
```

##### Generated Code:

Copy code

```
 -- Case 1:
!!!RESOLVE EWI!!! /*** SSC-EWI-0102 - REMOVED ONLY OPTION FROM CODE, ALREADY HANDLED IN CONVERSION TO SNOWFLAKE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0102 - REMOVED CASCADE OPTION FROM CODE, ALREADY HANDLED IN CONVERSION TO SNOWFLAKE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0102 - REMOVED RESTART IDENTITY OPTION FROM CODE, ALREADY HANDLED IN CONVERSION TO SNOWFLAKE ***/!!!
TRUNCATE table_base2;

-- Case 2:
!!!RESOLVE EWI!!! /*** SSC-EWI-0102 - REMOVED CASCADE OPTION FROM CODE, ALREADY HANDLED IN CONVERSION TO SNOWFLAKE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0102 - REMOVED RESTART IDENTITY OPTION FROM CODE, ALREADY HANDLED IN CONVERSION TO SNOWFLAKE ***/!!!
TRUNCATE TABLE table_inherit_and_generated;
```

#### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0107

Interval Literal Not Supported In Current Scenario

### Severity

High

#### Description

Snowflake Intervals can only be used in arithmetic operations. Intervals used in any other scenario are not supported.

#### Example Code

**Input Code:**

Copy code

```
 SELECT INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

**Output Code:**

Copy code

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!!
 INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

##### Best Practices

- No end-user action is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0108

The following subquery matches at least one of the patterns considered invalid and may produce compilation errors

### Severity

High

#### Description

In Snowflake, there are multiple patterns and elements in a subquery that are not supported and make it not executable. According to the [Snowflake documentation on subqueries](https://docs.snowflake.com/en/user-guide/querying-subqueries#types-supported-by-snowflake) the following subquery types are **supported**:

- Uncorrelated scalar subqueries in any place that a value expression can be used.
- Correlated scalar subqueries in WHERE clauses.
- EXISTS, ANY / ALL, and IN subqueries in WHERE clauses. These subqueries can be correlated or uncorrelated.

Please note that the list above is not exhaustive, meaning that subqueries that match none of the specified types may still be considered valid.

To help avoid errors, a set of subquery patterns that normally invalidate subqueries is known, this EWI is added to warn the user that the subquery matches at least one of these patterns and therefore may produce errors when compiled in Snowflake.

#### Example Code

##### Input Code:

Copy code

```
 CREATE TABLE tableA
(
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE TABLE tableB
(
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey');

INSERT INTO tableB VALUES (50, 'Hey');
INSERT INTO tableB VALUES (50, 'Example');
INSERT INTO tableB VALUES (10, 'Bye');

-- Snowflake only allows the usage of FETCH in subqueries that are uncorrelated scalar, this subquery execution will fail
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB WHERE col3 = col1 FETCH FIRST ROW ONLY);

-- This subquery is uncorrelated scalar so FETCH is valid to use
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB FETCH FIRST ROW ONLY);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE tableA
    (
        col1 INTEGER,
        col2 VARCHAR(20)
    )
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/05/2024",  "domain": "test" }}'
    ;

    CREATE OR REPLACE TABLE tableB
    (
        col3 INTEGER,
        col4 VARCHAR(20)
    )
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/05/2024",  "domain": "test" }}'
    ;

    INSERT INTO tableA
    VALUES (50, 'Hey');

    INSERT INTO tableB
    VALUES (50, 'Hey');

    INSERT INTO tableB
    VALUES (50, 'Example');

    INSERT INTO tableB
    VALUES (10, 'Bye');

    -- Snowflake only allows the usage of FETCH in subqueries that are uncorrelated scalar, this subquery execution will fail
SELECT col2
FROM
    tableA
    WHERE col2 =
                 --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (SELECT
                         ANY_VALUE( col4) FROM
                         tableB
                     WHERE col3 = col1
                     FETCH FIRST 1 ROW ONLY);

    -- This subquery is uncorrelated scalar so FETCH is valid to use
SELECT col2
FROM
    tableA
    WHERE col2 = (SELECT col4 FROM
                         tableB
                     FETCH FIRST 1 ROW ONLY);
```

#### Best Practices

- Check the subquery in Snowflake, if it compiles without problems then this EWI can be safely ignored.
- Please check the complex patterns section for subqueries inside the assessment report, it contains a list of the patterns that normally invalidate subqueries and their occurrences, it can be used to review the migrated subqueries and why are they considered invalid.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0109

Alter Table syntax is not applicable in Snowflake.

### Severity

Medium

#### Description

The Alter Table syntax used is not applicable in Snowflake, then this message is being added.

#### Example Code:

##### Input Code:

Copy code

```
 ALTER TABLE SOMENAME DEFAULT COLLATION SOMENAME;

ALTER TABLE SOMENAME ROW ARCHIVAL;

ALTER TABLE SOMENAME MODIFY CLUSTERING;

ALTER TABLE SOMENAME DROP CLUSTERING;

ALTER TABLE SOMENAME SHRINK SPACE COMPACT CASCADE;
```

##### Generated Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
DEFAULT COLLATION SOMENAME;

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
ROW ARCHIVAL;

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
MODIFY CLUSTERING;

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
DROP CLUSTERING;

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
SHRINK SPACE COMPACT CASCADE;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0110

Transformation Not Performed Due To Missing Dependencies

### Severity

Low

#### Description

When there are missing dependencies, the EWI is added to indicate that a transformation cannot be executed. Abstract syntax trees are utilized to create a semantic model of the input code, which is then used to generate new code that replicates the functionality of the original source. However, in this particular scenario, the transformation could not be completed because the semantic model lacks certain dependencies.

#### Example code

##### Input Code :

Copy code

```
 ALTER TABLE MissingTable ADD
CONSTRAINT constraint1  DEFAULT (suser_name()) FOR col1;
```

##### Generated Code:

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "MissingTable" **
!!!RESOLVE EWI!!! /*** SSC-EWI-0110 - TRANSFORMATION NOT PERFORMED DUE TO MISSING DEPENDENCIES ***/!!!

ALTER TABLE MissingTable
ADD
CONSTRAINT constraint1 DEFAULT (CURRENT_USER()) FOR col1;
```

#### Best Practices

- Add the missing dependencies to the input code.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0111

Only one level of nesting is allowed for nested procedures in Snowflake.

### Severity

Critical

#### Description

Snowflake supports only a single level of nesting for procedures. Defining a nested procedure inside another nested procedure is not allowed. If this pattern is detected, this error will be generated.

#### Example code

##### Input Code :

Copy code

```
CREATE OR REPLACE PROCEDURE calculate_executive_salary (
    p_result OUT NUMBER
)
AS
    PROCEDURE calculate_senior_level (
        senior_result OUT NUMBER
    )
    AS
        PROCEDURE calculate_base_level (
            base_result OUT NUMBER
        )
        AS
        BEGIN
            base_result := 75000;
        END calculate_base_level;
    BEGIN
        calculate_base_level(senior_result);
        senior_result := senior_result * 1.5;
    END calculate_senior_level;
BEGIN
    calculate_senior_level(p_result);
END calculate_executive_salary;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE calculate_executive_salary (p_result OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        calculate_senior_level PROCEDURE (senior_result NUMBER(38, 18)
           )
        RETURNS NUMBER
        AS
            DECLARE
                !!!RESOLVE EWI!!! /*** SSC-EWI-0111 - ONLY ONE LEVEL OF NESTING IS ALLOWED FOR NESTED PROCEDURES IN SNOWFLAKE. ***/!!!
                PROCEDURE calculate_base_level (
                    base_result OUT NUMBER
                )
                AS
                BEGIN
                    base_result := 75000;
                END calculate_base_level;
                call_results NUMBER;
            BEGIN
                call_results := (
                CALL
                calculate_base_level(:senior_result)
                );
                senior_result := :call_results;
                senior_result := :senior_result * 1.5;
                RETURN senior_result;
            END;
        call_results NUMBER;
        BEGIN
        call_results := (
            CALL
            calculate_senior_level(:p_result)
        );
        p_result := :call_results;
        END;
$$;
```

#### Best Practices

- Refactor your code to avoid more than one level of nested procedures. Move deeply nested procedures to the top level or restructure your logic to comply with Snowflake’s single-level nesting limitation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0112

Nested procedure overloading is not supported.

### Severity

Critical

#### Description

Snowflake does not support overloading of nested procedures. In other words, you cannot define multiple nested procedures with the same name but different parameter lists within the same parent procedure. If the source code contains overloaded nested procedures, this error will be generated to indicate that such patterns are not supported in Snowflake.

#### Example code

##### Input Code :

Copy code

```
CREATE OR REPLACE PROCEDURE demonstrate_salary_calculations(
    final_summary OUT VARCHAR2
)
AS
    result1 VARCHAR2(100);
    result2 VARCHAR2(100);
    result3 VARCHAR2(100);

    PROCEDURE calculate_salary(
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Standard: 55000';
    END;

    PROCEDURE calculate_salary(
        base_amount IN NUMBER,
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Calculated: ' || (base_amount * 1.15);
    END;

    PROCEDURE calculate_salary(
        employee_level IN VARCHAR2,
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Level ' || UPPER(employee_level) || ': 60000';
    END;

BEGIN
    calculate_salary(result1);
    calculate_salary(50000, result2);
    calculate_salary('senior', result3);
    final_summary := result1 || ' | ' || result2 || ' | ' || result3;
END demonstrate_salary_calculations;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE demonstrate_salary_calculations (final_summary OUT VARCHAR
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        result1 VARCHAR(100);
        result2 VARCHAR(100);
        result3 VARCHAR(100);
        calculate_salary PROCEDURE(output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Standard: 55000';
                RETURN output;
            END;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED. ***/!!!
        calculate_salary PROCEDURE(base_amount NUMBER(38, 18), output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Calculated: ' || NVL((:base_amount * 1.15) :: STRING, '');
                RETURN output;
            END;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED. ***/!!!
        calculate_salary PROCEDURE(employee_level VARCHAR, output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Level ' || NVL(UPPER(:employee_level) :: STRING, '') || ': 60000';
                RETURN output;
            END;
        call_results VARCHAR;
        BEGIN
        call_results := (
            CALL
            calculate_salary(:result1)
        );
        result1 := :call_results;
        call_results := (
            CALL
            calculate_salary(50000, :result2)
        );
        result2 := :call_results;
        call_results := (
            CALL
            calculate_salary('senior', :result3)
        );
        result3 := :call_results;
        final_summary := NVL(:result1 :: STRING, '') || ' | ' || NVL(:result2 :: STRING, '') || ' | ' || NVL(:result3 :: STRING, '');
        END;
$$;
```

#### Best Practices

- Attempting to overload nested procedures in Snowflake will result in compilation errors or unexpected behavior. To ensure compatibility, you should refactor your code to avoid overloading nested procedures. Consider renaming procedures so that each nested procedure has a unique name within its scope, or restructure your logic to eliminate the need for overloading. Additionally, review and update all procedure calls to use the new unique names.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0113

The usage of Snowflake scripting UDF is not supported in this scenario.

### Severity

Medium

#### Description

The usage of Snowflake Scripting UDFs in specific scenarios is not supported. The following cases are not supported:

- Snowflake Scripting UDFs can’t be used when creating a materialized view.
- Snowflake Scripting UDFs can’t be used to specify a default column value.

#### Example code

##### Input Code :

Copy code

```
CREATE TABLE Table1 (
  col1 INT DEFAULT SnowScriptUdf()
);

CREATE MATERIALIZED VIEW CreateView1
AS
SELECT 
  col1,
  SnowScriptUdf() AS col2
FROM Table1;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE Table1 (
col1 INT DEFAULT SnowScriptUdf() !!!RESOLVE EWI!!! /*** SSC-EWI-0113 - THE USAGE OF SNOWFLAKE SCRIPTING UDF IS NOT SUPPORTED IN THIS SCENARIO. ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/17/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE DYNAMIC TABLE CreateView1
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/17/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
      col1,
      SnowScriptUdf() !!!RESOLVE EWI!!! /*** SSC-EWI-0113 - THE USAGE OF SNOWFLAKE SCRIPTING UDF IS NOT SUPPORTED IN THIS SCENARIO. ***/!!! AS col2
FROM
      Table1;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0114

MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING.

### Severity

Medium

Note

Some parts in the output code are omitted for clarity reasons.

#### Description

In database systems like DB2, Teradata, and others, it is possible to declare both CONTINUE and EXIT exception handlers in the same procedural block. However, Snowflake Scripting does not support mixing CONTINUE and EXIT handlers within the same EXCEPTION block.

When a procedure with both types of handlers declared in the same block is encountered, separate EXCEPTION blocks are generated for each handler type and this EWI is added to indicate that manual review and testing are required to ensure the converted code maintains the intended behavior.

**Key Behavioral Differences:**

- **CONTINUE HANDLER**: Allows execution to continue after handling the exception
- **EXIT HANDLER**: Terminates the current block after handling the exception

Since Snowflake cannot mix these behaviors in a single EXCEPTION block, the conversion may result in different execution flow compared to the source system.

#### Example Code

##### Input Code:

**DB2**

Copy code

```
CREATE OR REPLACE PROCEDURE with_continueAndExit()
BEGIN
    DECLARE test_1 INTEGER DEFAULT 10;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
        INSERT INTO error_test VALUES ('EXCEPTION');
    
    DECLARE EXIT HANDLER FOR SQLSTATE '20000' 
        INSERT INTO error_test VALUES ('ERROR 2000');
    
    SET test_1 = 1 / 0;
    INSERT INTO error_test VALUES ('EXIT');
END;
```

##### Generated Code:

**Snowflake**

Copy code

```
CREATE OR REPLACE PROCEDURE with_continueAndExit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        test_1 INTEGER DEFAULT 10;
    BEGIN
        test_1 := 1 / 0;
        INSERT INTO error_test VALUES ('EXIT');
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                INSERT INTO error_test VALUES ('EXCEPTION')
        !!!RESOLVE EWI!!! /*** SSC-EWI-0114 - MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '20000') THEN
                        INSERT INTO error_test VALUES ('ERROR 2000')
                END
    END;
$$;
```

#### Best Practices

When dealing with mixed CONTINUE and EXIT handlers:

1. **Review Exception Handling Logic**: Carefully review the converted code to understand how exceptions are handled in each block.
2. **Test Thoroughly**: Test all error scenarios to ensure the behavior matches the source system’s expectations.
3. **Consider Refactoring**: If possible, refactor the code to use only one type of handler (either all CONTINUE or all EXIT) within a block.
4. **Use Nested Blocks**: Consider restructuring the logic using nested BEGIN…END blocks, where each block has its own exception handling strategy.
5. **Document Behavior Changes**: Document any differences in exception handling behavior for future maintenance.

##### Recommended Pattern

Instead of mixing handlers, consider this approach:

Copy code

```
BEGIN
    -- Handle operations that should continue on error
    BEGIN
        operation1();
        operation2();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            log_error('Continue handler');
    END;
    
    -- Handle operations that should exit on error
    BEGIN
        critical_operation();
    EXCEPTION
        WHEN OTHER EXIT THEN
            log_error('Exit handler');
    END;
END;
```

#### Related Documentation

- [DB2 CONTINUE HANDLER](../../translation-references/db2/db2-continue-handler#mixed-continue-and-exit-handlers)
- [DB2 EXIT HANDLER](../../translation-references/db2/db2-exit-handler#mixed-continue-and-exit-handlers)
- [Teradata Exception Handlers](../../translation-references/teradata/teradata-to-snowflake-scripting-translation-reference#exception-handlers)
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0115

Iceberg table contains unsupported datatypes.

### Severity

Medium

#### Description

This EWI is emitted for tables that contain datatypes currently not supported by Snowflake on Iceberg tables.
Currently, Snowflake offers support for Iceberg tables in V2 format.

#### Example code

##### Input Code :

Copy code

```
-- Additional Params: --TablesTransformationTarget SnowflakeIceberg
CREATE TABLE unsupported_types_table
(
  column1 TIMESTAMP(8) WITH TIME ZONE,
  column2 JSON(1000),
  column3 XML(1000)
);
```

##### Generated Code:

Copy code

```
 -- Additional Params: --TablesTransformationTarget SnowflakeIceberg
!!!RESOLVE EWI!!! /*** SSC-EWI-0115 - ICEBERG TABLE CONTAINS THE FOLLOWING UNSUPPORTED DATATYPES: TIMESTAMP(8) WITH TIME ZONE, JSON(1000), XML(1000) ***/!!!
CREATE OR REPLACE ICEBERG TABLE unsupported_types_table
(
 column1 TIMESTAMP_TZ(8),
 column2 VARIANT,
 column3 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!
)
CATALOG = 'SNOWFLAKE'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 1,  "minor": 0,  "patch": "0.0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/16/2025",  "domain": "no-domain-provided",  "migrationid": "9CebAVkM33qsfTnTrMh3Dw==" }}'
;
```

#### Best Practices

- Consider modifying the columns and logic to make use of datatypes supported in Iceberg tables
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0116

Unsupported construct in Snowflake

Note

This issue code is used for multiple scenarios. See the applicable scenario below.

### Scenario 1: CHECK Constraints with Unsupported Expressions

Note

Some parts in the output code are omitted for clarity reasons.

#### Severity

Low

#### Description

This EWI is emitted when a CHECK constraint expression contains functions or constructs that Snowflake does not support in CHECK constraints. Snowflake CHECK constraints only support deterministic, scalar expressions without user-defined functions or non-deterministic built-in functions.

The unsupported expression types include:

- **User-defined functions (UDFs)**: Any function that is not a Snowflake built-in function, including schema-qualified function calls or unresolved function references
- **Non-deterministic functions**: Built-in functions that return different values on each call or depend on session/system context, such as `NEWID()`, `RAND()`, `UUID_STRING()`, `GETDATE()`, `CURRENT_TIMESTAMP()`, `CURRENT_USER()`, `CURRENT_ROLE()`

When this EWI is emitted, the CHECK constraint is flagged with the `!!!RESOLVE EWI!!!` marker and the specific reason (e.g., “user-defined function”, “non-deterministic function”) is included in the annotation.

#### Example Code

##### Example 1: CHECK Constraint with User-Defined Function

###### Input Code (SQL Server):

Copy code

```
CREATE TABLE Orders (
  Price DECIMAL(10,2) CHECK (dbo.IsValidPrice(Price) = 1)
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE Orders (
  Price DECIMAL(10, 2)
                       !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH user-defined function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                       CHECK (dbo.IsValidPrice(Price) = 1)
)
;
```

##### Example 2: CHECK Constraint with Non-Deterministic Function

###### Input Code (SQL Server):

Copy code

```
CREATE TABLE Sessions (
  Token NVARCHAR(100) CHECK (Token <> CAST(NEWID() AS NVARCHAR(100)))
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE Sessions (
  Token NVARCHAR(100)
                      !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH non-deterministic function: 'NEWID' IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                      CHECK (Token <> CAST(NEWID() AS NVARCHAR(100)))
)
;
```

##### Example 3: CHECK Constraint with Unresolved Function (Oracle)

###### Input Code (Oracle):

Copy code

```
CREATE TABLE invoices (
  invoice_id NUMBER NOT NULL,
  tax_code VARCHAR2(10),
  CONSTRAINT chk_tax_code CHECK (validate_tax_code(tax_code) = 1)
);
```

###### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE invoices (
  invoice_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ NOT NULL,
  tax_code VARCHAR(10),
  CONSTRAINT chk_tax_code
                          !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH user-defined function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                          CHECK(validate_tax_code(tax_code) = 1)
)
;
```

#### Best Practices

- **Replace UDFs with inline expressions**: If the user-defined function performs validation logic, consider rewriting it as an inline SQL expression using Snowflake built-in functions
- **Remove dynamic constraints**: CHECK constraints with non-deterministic functions typically try to enforce rules that change over time. Consider alternative approaches such as:
  - Application-level validation
  - Triggers or streams to validate data changes
  - Regular scheduled tasks to audit and flag violations
- **Simplify validation logic**: Ensure CHECK constraints only use deterministic, scalar expressions that can be evaluated at insert/update time
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Scenario 2: Interval Values Inside Semi-Structured Type Columns

#### Severity

Medium

#### Description

This EWI is emitted when the `--UseIntervalDatatype` preview flag is enabled in the SnowConvert AI Desktop application and an INTERVAL data type appears inside a semi-structured type column such as ARRAY, MAP, or STRUCT. Snowflake does not support storing INTERVAL values inside VARIANT-based columns. The outer type is still converted (for example, STRUCT becomes VARIANT), but the EWI warns that the INTERVAL values within cannot be preserved.

For more details on how interval types are handled across languages, see the [Interval Data Types](../../translation-references/general/interval-data-types) translation reference.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
CREATE TABLE test.table1
(
  col1 ARRAY<INTERVAL>
);
```

##### Generated Code (BigQuery):

Copy code

```
CREATE TABLE test.table1 (
  col1 ARRAY !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - SNOWFLAKE DOES NOT SUPPORT INTERVAL VALUES INSIDE SEMI-STRUCTURED TYPE COLUMNS ***/!!! DEFAULT []
)
;
```

##### Input Code (Hive):

Copy code

```
CREATE TABLE tb1
(col1 STRUCT<a:INTERVAL, b:INT>);
```

##### Generated Code (Hive):

Copy code

```
CREATE TABLE tb1 (
  col1 VARIANT /*** SSC-FDM-0034 - STRUCT<INTERVAL, INT> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/!!!RESOLVE EWI!!! /*** SSC-EWI-0116 - SNOWFLAKE DOES NOT SUPPORT INTERVAL VALUES INSIDE SEMI-STRUCTURED TYPE COLUMNS ***/!!!
)
;
```

#### Best Practices

- Consider extracting interval values from semi-structured columns into dedicated INTERVAL-typed columns
- If interval values must be stored in VARIANT columns, store them as strings and convert back to intervals when needed using CAST expressions
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0117

Snowflake does not support interval data type in UDFs or Snowflake Scripting.

### Severity

Medium

#### Description

This EWI is emitted when the `--UseIntervalDatatype` preview flag is enabled in the SnowConvert AI Desktop application and an INTERVAL data type is used in a context not yet supported by Snowflake Scripting: UDF or procedure parameters, return types, or variable declarations. The INTERVAL type is preserved in the output for reference, but the EWI warns that it will not work at runtime in these contexts.

For more details on how interval types are handled across languages, see the [Interval Data Types](../../translation-references/general/interval-data-types) translation reference.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
CREATE FUNCTION test.fn1(p1 INTERVAL)
RETURNS INT64
AS (1);
```

##### Generated Code (BigQuery):

Copy code

```
CREATE FUNCTION test.fn1 (p1 INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/!!!RESOLVE EWI!!! /*** SSC-EWI-0117 - SNOWFLAKE DOES NOT SUPPORT THE INTERVAL DATA TYPE IN UDF/PROCEDURE PARAMETERS, RETURN TYPES, OR VARIABLE DECLARATIONS ***/!!!)
RETURNS INT
AS
$$
  1
$$;
```

##### Input Code (Teradata):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE PROCEDURE test_proc(IN p1 INTERVAL DAY TO SECOND)
BEGIN
  SELECT 1;
END;
```

##### Generated Code (Teradata):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE OR REPLACE PROCEDURE test_proc (P1 INTERVAL DAY TO SECOND !!!RESOLVE EWI!!! /*** SSC-EWI-0117 - SNOWFLAKE DOES NOT SUPPORT THE INTERVAL DATA TYPE IN UDF/PROCEDURE PARAMETERS, RETURN TYPES, OR VARIABLE DECLARATIONS ***/!!!)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    SELECT 1;
  END;
$$;
```

#### Best Practices

- Consider using VARCHAR parameters for interval values and converting them inside the procedure body using CAST expressions
- If the interval parameter is used only for datetime arithmetic within the procedure, consider passing the numeric components separately
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0118

Snowflake does not support interval columns in Dynamic Tables.

### Severity

Medium

#### Description

This EWI is emitted when the `--UseIntervalDatatype` preview flag is enabled in the SnowConvert AI Desktop application and a materialized view (converted to a Snowflake Dynamic Table) references columns with INTERVAL data types. Snowflake Dynamic Tables do not support INTERVAL-typed columns. The Dynamic Table is still generated, but the EWI warns that it may fail at runtime.

For more details on how interval types are handled across languages, see the [Interval Data Types](../../translation-references/general/interval-data-types) translation reference.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE src_table
(
  col1 INT64,
  col2 INTERVAL
);

CREATE MATERIALIZED VIEW mv1
AS
SELECT col1, col2 FROM src_table;
```

##### Generated Code (BigQuery):

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE src_table (
  col1 INT,
  col2 INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/
)
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0118 - SNOWFLAKE DOES NOT SUPPORT INTERVAL COLUMNS IN DYNAMIC TABLES ***/!!!
CREATE OR REPLACE DYNAMIC TABLE mv1
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
AS
  SELECT
    col1,
    col2
  FROM
    src_table;
```

#### Best Practices

- Consider excluding INTERVAL columns from the Dynamic Table query, or casting them to VARCHAR before selecting
- If the interval values are needed in downstream queries, consider creating a regular view instead of a Dynamic Table for the INTERVAL columns
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0119

Interval type column was converted to VARCHAR.

### Severity

Low

#### Description

This EWI is emitted in Dynamic Table contexts when the `--UseIntervalDatatype` preview flag in the SnowConvert AI Desktop application is **not** enabled and a source column had an INTERVAL data type that was converted to VARCHAR. This alerts users that the column in the Dynamic Table query originally referenced an interval-typed column that lost its type during conversion.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
CREATE TABLE src_table
(
  col1 INT64,
  col2 INTERVAL
);

CREATE MATERIALIZED VIEW mv1
AS
SELECT col1, col2 FROM src_table;
```

##### Generated Code (BigQuery):

Copy code

```
CREATE TABLE src_table (
  col1 INT,
  col2 VARCHAR(30) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
;

CREATE OR REPLACE DYNAMIC TABLE mv1
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
AS
  SELECT
    col1,
    col2 !!!RESOLVE EWI!!! /*** SSC-EWI-0119 - INTERVAL TYPE COLUMN WAS CONVERTED TO VARCHAR ***/!!!
  FROM
    src_table;
```

#### Best Practices

- If using the SnowConvert AI Desktop application, consider enabling the `--UseIntervalDatatype` preview flag to preserve native INTERVAL types where possible
- Review the VARCHAR columns in the output to ensure the string representation of interval values is compatible with your application logic
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0120

Unsupported sequence options were removed during conversion.

### Severity

Low

#### Description

This EWI is generated when a `CREATE SEQUENCE` statement with options that are not supported in Snowflake is encountered. The unsupported options (such as `MINVALUE`, `MAXVALUE`, or `CYCLE`) are removed during conversion because Snowflake sequences do not support them. The EWI message lists the specific options that were removed.

When a `START WITH` clause is not explicitly present, the start value is inferred from `MINVALUE` (for positive increments) or `MAXVALUE` (for negative increments) before removing those options.

#### Example Code

##### Input Code (DB2):

Copy code

```
CREATE SEQUENCE dwh.seq_tcor_party AS INTEGER
MINVALUE 23177568 MAXVALUE 2147483647
START WITH 23177568 INCREMENT BY 1
CACHE 500 NO CYCLE NO ORDER;
```

##### Generated Code (DB2):

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0120 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE dwh.seq_tcor_party
  START WITH 23177568
  INCREMENT BY 1
  NOORDER
;
```

#### Best Practices

- If your application relies on `CYCLE` behavior, implement a wrapper UDF that resets the sequence value when it exceeds a threshold.
- If `MINVALUE` or `MAXVALUE` bounds are critical, add application-level validation or a Snowflake task to monitor sequence values.
- Review the inferred `START WITH` value to ensure it matches your expected sequence starting point.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0121

DELETE from error table with WHERE clause has no direct Snowflake equivalent.

### Severity

Low

#### Description

This EWI is emitted when a `DELETE` statement targets an error-logging table and includes a `WHERE` clause. Snowflake error tables are read-only virtual views accessible via `ERROR_TABLE(<base_table>)` — they cannot be deleted from selectively. The only supported operation is a full truncation via `TRUNCATE ERROR_TABLE(<base_table>)`.

When the `DELETE` has no `WHERE` clause, SnowConvert converts it to `TRUNCATE ERROR_TABLE(<base_table>)` automatically. When a `WHERE` clause is present, that automatic conversion is not possible, so the statement is kept as-is and annotated with this EWI.

#### Example Code

##### Input Code (Oracle):

Copy code

```
CREATE TABLE ERR$_ORDERS (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$   VARCHAR2(2000),
    ORA_ERR_ROWID$  ROWID,
    ORA_ERR_OPTYP$  VARCHAR2(2),
    ORA_ERR_TAG$    VARCHAR2(2000),
    ORDER_ID        NUMBER
);

DELETE FROM "ERR$_ORDERS" WHERE ORA_ERR_TAG$ = 'BATCH_1';
```

##### Generated Code:

Copy code

```
----** SSC-FDM-0050 - EXPLICIT ERROR LOGGING TABLE REMOVED; NOT REQUIRED IN SNOWFLAKE. READ ERRORS WITH 'SELECT * FROM ERROR_TABLE(ORDERS)'. **
--CREATE TABLE ERR$_ORDERS (
--  ORA_ERR_NUMBER$ NUMBER,
--  ORA_ERR_MESG$ VARCHAR2(2000),
--  ORA_ERR_ROWID$ ROWID,
--  ORA_ERR_OPTYP$ VARCHAR2(2),
--  ORA_ERR_TAG$ VARCHAR2(2000),
--  ORDER_ID NUMBER
--);

!!!RESOLVE EWI!!! /*** SSC-EWI-0121 - DELETE FROM ERROR TABLE WITH WHERE CLAUSE HAS NO DIRECT SNOWFLAKE EQUIVALENT. SNOWFLAKE ERROR TABLES ONLY SUPPORT TRUNCATE VIA 'TRUNCATE ERROR_TABLE(ORDERS)'. ***/!!!
DELETE FROM
  "ERR$_ORDERS"
WHERE
  "ORA_ERR_TAG$" = 'BATCH_1';
```

#### Best Practices

- If the goal is to clear all captured errors, replace the `DELETE` with `TRUNCATE ERROR_TABLE(<base_table>)`.
- If the goal is to retain only a subset of error rows, consider reading errors with `SELECT * FROM ERROR_TABLE(<base_table>)`, filtering in application logic, and storing the relevant rows in a custom audit table.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0122

Error logging column has no equivalent in Snowflake

### Severity

Low

#### Description

This EWI is emitted when a `SELECT` from an error-logging table references a system column that has no direct equivalent in Snowflake’s `ERROR_TABLE()` output. SnowConvert maps well-known error system columns to their Snowflake counterparts where possible:

| Oracle column | Snowflake equivalent |
| --- | --- |
| `ORA_ERR_NUMBER$` | `error_code` |
| `ORA_ERR_MESG$` | `ERROR_METADATA:error_message` |

Expand

Show lessSee more

Columns that cannot be mapped — notably `ORA_ERR_ROWID$`, `ORA_ERR_OPTYP$`, and `ORA_ERR_TAG$` — are preserved as quoted identifiers and annotated with this EWI. Payload columns (copied from the base table) are rewritten using `IFF(IS_ARRAY(ERROR_DATA:<COL>), GET(ERROR_DATA:<COL>, 0), ERROR_DATA:<COL>)`.

#### Example Code

##### Input Code (Oracle):

Copy code

```
CREATE TABLE ERR$_employees (
    ORA_ERR_OPTYP$  VARCHAR2(2),
    ORA_ERR_TAG$    VARCHAR2(2000),
    emp_id          NUMBER
);

SELECT ORA_ERR_OPTYP$, ORA_ERR_TAG$, emp_id FROM ERR$_employees;
```

##### Generated Code:

Copy code

```
----** SSC-FDM-0050 - ERROR LOGGING TABLE REMOVED; THIS TABLE IS NOT REQUIRED IN SNOWFLAKE. READ ERRORS WITH 'SELECT * FROM ERROR_TABLE(employees)'. **
--CREATE TABLE ERR$_employees (
--  ORA_ERR_OPTYP$ VARCHAR2(2),
--  ORA_ERR_TAG$ VARCHAR2(2000),
--  emp_id NUMBER
--);

SELECT
  "ORA_ERR_OPTYP$" !!!RESOLVE EWI!!! /*** SSC-EWI-0122 - THE ERROR LOGGING COLUMN 'ORA_ERR_OPTYP$' HAS NO DIRECT EQUIVALENT IN SNOWFLAKE'S ERROR TABLE OUTPUT. REVIEW MANUALLY. ***/!!!,
  "ORA_ERR_TAG$" !!!RESOLVE EWI!!! /*** SSC-EWI-0122 - THE ERROR LOGGING COLUMN 'ORA_ERR_TAG$' HAS NO DIRECT EQUIVALENT IN SNOWFLAKE'S ERROR TABLE OUTPUT. REVIEW MANUALLY. ***/!!!,
  IFF(IS_ARRAY(ERROR_DATA:EMP_ID), GET(ERROR_DATA:EMP_ID, 0), ERROR_DATA:EMP_ID) "emp_id"
FROM
  ERROR_TABLE(employees);
```

#### Best Practices

- Review each flagged column and determine whether the data it contained in Oracle is relevant in the migrated environment.
- For `ORA_ERR_OPTYP$` (operation type: I/U/D), consider querying `ERROR_METADATA` for contextual information, or track the operation type in application logic before the DML call.
- For `ORA_ERR_TAG$` (user-defined tag), the value was set in the `LOG ERRORS INTO ... (<tag>)` clause at DML time; there is no direct equivalent in Snowflake’s error table — store the tag value in a separate audit table if needed.
- For `ORA_ERR_ROWID$` (original row ROWID), Snowflake does not expose physical row addresses; remove this column reference or replace it with a logical key.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0123

Snowflake does not support interval values inside semi-structured type columns

### Severity

Medium

#### Description

Snowflake does not support `INTERVAL` values stored inside semi-structured types (`ARRAY`, `OBJECT`, `VARIANT`). This EWI is emitted when the `--UseIntervalDatatype` preview flag is enabled in the SnowConvert AI Desktop application and an `INTERVAL` appears nested inside an `ARRAY` or a `STRUCT` column. The container is still converted (`ARRAY<INTERVAL>` to `ARRAY`, and `STRUCT` to `VARIANT`), but the nested `INTERVAL` element cannot be preserved as a native interval value, so the flagged usage requires manual review.

Without the `--UseIntervalDatatype` preview flag this EWI is not emitted, because `INTERVAL` is converted to `VARCHAR` and is no longer a nested interval value.

#### Example Code

##### Input Code (BigQuery):

Copy code

```
CREATE TABLE test.table1
(
  col1 ARRAY<INTERVAL>
);
```

##### Generated Code:

Copy code

```
CREATE TABLE test.table1 (
  col1 ARRAY !!!RESOLVE EWI!!! /*** SSC-EWI-0123 - SNOWFLAKE DOES NOT SUPPORT INTERVAL VALUES INSIDE SEMI-STRUCTURED TYPE COLUMNS ***/!!! DEFAULT []
)
;
```

#### Best Practices

- Avoid storing `INTERVAL` values inside `ARRAY` or `STRUCT` columns; store the interval as a separate scalar column, or persist it as a normalized string and reconstruct the interval in arithmetic expressions.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0124

Snowflake does not support interval data type in UDFs or Snowflake Scripting

### Severity

Medium

#### Description

SnowConvert AI emits this issue when an interval data type is used in a UDF or procedure parameter, return type, or variable declaration because Snowflake does not support intervals in those contexts. Replace the interval with a supported representation and verify every use of the converted value.

#### Code Example

##### Input Code:

##### BigQuery

Copy code

```
CREATE FUNCTION test.fn1(p1 INTERVAL)
RETURNS INT64
AS (1);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE FUNCTION test.fn1 (p1 INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/!!!RESOLVE EWI!!! /*** SSC-EWI-0124 - SNOWFLAKE DOES NOT SUPPORT THE INTERVAL DATA TYPE IN UDF/PROCEDURE PARAMETERS, RETURN TYPES, OR VARIABLE DECLARATIONS ***/!!!)
RETURNS INT
AS
$$
  1
$$;
```

#### Best Practices

- Replace interval parameters, return types, and local variables with a supported representation such as a numeric quantity and unit or a normalized string.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0125

Dynamic SQL variable back-propagation failed

### Severity

Low

#### Description

SnowConvert AI emits this issue when it cannot determine the value a variable holds when dynamic SQL executes. The assignment is converted independently, so review whether the resulting value forms valid Snowflake SQL for the associated `EXECUTE IMMEDIATE` statement.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE PROCEDURE p AS
BEGIN
  DECLARE @x NVARCHAR(50);
  SET @x = NEWID();
  EXEC('SELECT * FROM ' + @x);
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    X NVARCHAR(50);
  BEGIN
    X :=
    !!!RESOLVE EWI!!! /*** SSC-EWI-0125 - SNOWCONVERT COULD NOT DETERMINE WHAT VALUE THIS VARIABLE HOLDS WHEN THE DYNAMIC SQL EXECUTES. THE ASSIGNMENT EXPRESSION WAS CONVERTED ON ITS OWN; PLEASE REVIEW THAT ITS VALUE IS COMPATIBLE WITH THE EXECUTE IMMEDIATE THAT USES IT. ***/!!!
    UUID_STRING();
    EXECUTE IMMEDIATE 'SELECT
   *
FROM
   ' || :X;
  END;
$$;
```

#### Best Practices

- Review every assignment that can reach the flagged `EXECUTE IMMEDIATE` and verify that the converted expression produces valid Snowflake SQL.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0126

Dynamic SQL block could not be fully reconstructed

### Severity

Medium

#### Description

SnowConvert AI emits this issue when it cannot fully reconstruct a dynamic SQL block. Review the generated variable substitutions and `EXECUTE IMMEDIATE` body because they may not preserve every source branch.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE PROCEDURE p AS
BEGIN
  DECLARE @x NVARCHAR(200);
  DECLARE @y NVARCHAR(200);
  SET @x = 'tbl /*>>orphan*/ x';
  SET @y = 'SELECT * FROM ' + @x;
  EXECUTE sp_executesql @y;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p ()
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    X NVARCHAR(200);
    Y NVARCHAR(200);
    ProcedureResultSet RESULTSET;
  BEGIN
    X := 'tbl ' || ' x';
    Y := 'SELECT * FROM ' || :X || ';';
    ProcedureResultSet := (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0126 - SNOWCONVERT COULD NOT FULLY RECONSTRUCT THIS DYNAMIC SQL BLOCK; VARIABLE SUBSTITUTIONS AND/OR THE EXECUTE IMMEDIATE BODY MAY BE INCORRECT. PLEASE REVIEW THE GENERATED CODE. ***/!!!
    EXECUTE IMMEDIATE :y );
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

#### Best Practices

- Compare the generated dynamic SQL block with every source branch and correct variable substitutions before deployment.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0127

dbt-output-bindings.json was rejected by strict validation

### Severity

Low

#### Description

SnowConvert AI reads `dbt-output-bindings.json` from the input folder and validates it strictly: unknown keys, wrong-typed values, and secret-shaped fields are all rejected. When the file is rejected it is not applied — the generated `profiles.yml` and `sources.yml` keep their placeholder values and carry a warning header naming the offending file and the validation message. For the bindings file below, validation fails with `Unknown key 'bogus' at bogus. Allowed keys at this level: defaultTarget, mappings.` and the issue is recorded against `/in/dbt-output-bindings.json`.

#### Code Example

##### Input Code:

##### dbt

Copy code

```
{ "defaultTarget": {}, "bogus": 1 }
```

##### Output Code:

##### Snowflake

Copy code

```
# ==============================================================================
# WARNING: dbt-output-bindings.json was found at /in/dbt-output-bindings.json
#          but failed strict validation:
#
#   Unknown key 'bogus' at bogus. Allowed keys at this level: defaultTarget, mappings.
#
# The placeholders below were NOT replaced. Fix the bindings file and re-run the conversion.
# See SSC-EWI-0127 in the ETL Issues report for the structured record.
# ==============================================================================
```

#### Best Practices

- Correct the reported validation error in `dbt-output-bindings.json`, rerun the conversion, and verify that no placeholder values remain.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0128

Computed column data type couldn’t be inferred.

### Severity

Low

#### Description

When a source table defines a computed / virtual / generated column, the resulting Snowflake data type is inferred from the column expression so it can be emitted as a typed Snowflake virtual column. When the data type cannot be determined — for example, an arithmetic expression over columns whose types are not resolvable in the current scope, or an expression wrapping a function whose return type is unknown — it falls back to `VARIANT` for the column type and this EWI is emitted so the inferred type can be reviewed.

The column is still translated and remains usable; only its declared data type defaults to `VARIANT`. Where the expression is otherwise supported by Snowflake virtual columns, the `AS (<expression>)` definition is preserved inline.

#### Example Code

##### Input Code (SQL Server):

Copy code

```
CREATE TABLE COMPUTED_COLUMNS(
    my_column AS (Col13 * Col13 - Col4)
)
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE COMPUTED_COLUMNS (
  my_column VARIANT AS (Col13 * Col13 - Col4) !!!RESOLVE EWI!!! /*** SSC-EWI-0128 - COMPUTED COLUMN DATA TYPE COULDN'T BE INFERRED, VARIANT USED INSTEAD. ***/!!!
)
;
```

##### Input Code (SQL Server) — expression derived from a `SQL_VARIANT` column:

Copy code

```
CREATE TABLE settings (
    setting_id INT PRIMARY KEY,
    raw_value SQL_VARIANT,
    derived AS (raw_value + 1)
);
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE settings (
    setting_id INT PRIMARY KEY,
    raw_value VARIANT,
    derived VARIANT AS (raw_value + 1) !!!RESOLVE EWI!!! /*** SSC-EWI-0128 - COMPUTED COLUMN DATA TYPE COULDN'T BE INFERRED, VARIANT USED INSTEAD. ***/!!!
)
;
```

**About this example.** The `derived` column is computed from `raw_value`, a `SQL_VARIANT` column (translated to Snowflake `VARIANT`). Because the value a `VARIANT` holds is only known at runtime, a concrete result type for `raw_value + 1` cannot be inferred, so the computed column’s data type falls back to `VARIANT` and SSC-EWI-0128 is emitted. If you know the intended result type, replace `VARIANT` with the explicit Snowflake data type.

#### Best Practices

- Review the computed column and, if you know the intended result type, replace `VARIANT` with the explicit Snowflake data type that matches the expression.
- When the expression references columns whose types could not be resolved, ensure those base columns are declared in the same migration scope so the type can be inferred automatically.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0129

Dynamic SQL variable has too many possible values to resolve

### Severity

Low

#### Description

SnowConvert AI emits this issue when conditional assignments produce more possible dynamic SQL values than it can resolve safely. Review every branch that contributes to the generated statement and verify the runtime SQL in Snowflake.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE PROCEDURE p AS
BEGIN
  DECLARE @s NVARCHAR(200);
  SET @s = '';
  IF 1 = 1 SET @s = @s + 'a1'; ELSE SET @s = @s + 'b1';
  IF 1 = 1 SET @s = @s + 'a2'; ELSE SET @s = @s + 'b2';
  IF 1 = 1 SET @s = @s + 'a3'; ELSE SET @s = @s + 'b3';
  IF 1 = 1 SET @s = @s + 'a4'; ELSE SET @s = @s + 'b4';
  IF 1 = 1 SET @s = @s + 'a5'; ELSE SET @s = @s + 'b5';
  IF 1 = 1 SET @s = @s + 'a6'; ELSE SET @s = @s + 'b6';
  IF 1 = 1 SET @s = @s + 'a7'; ELSE SET @s = @s + 'b7';
  IF 1 = 1 SET @s = @s + 'a8'; ELSE SET @s = @s + 'b8';
  IF 1 = 1 SET @s = @s + 'a9'; ELSE SET @s = @s + 'b9';
  IF 1 = 1 SET @s = @s + 'aA'; ELSE SET @s = @s + 'bA';
  EXEC('SELECT * FROM t WHERE k = ''' + @s + '''');
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE p ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    S NVARCHAR(200);
  BEGIN
    S := '';
    IF (1 = 1) THEN S := :S || 'a1'; ELSE S := :S || 'b1'; END IF;
    IF (1 = 1) THEN S := :S || 'a2'; ELSE S := :S || 'b2'; END IF;
    IF (1 = 1) THEN S := :S || 'a3'; ELSE S := :S || 'b3'; END IF;
    IF (1 = 1) THEN S := :S || 'a4'; ELSE S := :S || 'b4'; END IF;
    IF (1 = 1) THEN S := :S || 'a5'; ELSE S := :S || 'b5'; END IF;
    IF (1 = 1) THEN S := :S || 'a6'; ELSE S := :S || 'b6'; END IF;
    IF (1 = 1) THEN
      S := !!!RESOLVE EWI!!! /*** SSC-EWI-0129 - SNOWCONVERT COULD NOT RESOLVE THIS VARIABLE FOR THE DYNAMIC SQL BECAUSE ITS CONDITIONAL ASSIGNMENTS PRODUCE TOO MANY POSSIBLE VALUES. PLEASE REVIEW THE GENERATED CODE. ***/!!! :S || 'a7';
    ELSE
      S := :S || 'b7';
    END IF;
    IF (1 = 1) THEN S := :S || 'a8'; ELSE S := :S || 'b8'; END IF;
    IF (1 = 1) THEN S := :S || 'a9'; ELSE S := :S || 'b9'; END IF;
    IF (1 = 1) THEN S := :S || 'aA'; ELSE S := :S || 'bA'; END IF;
    EXECUTE IMMEDIATE 'SELECT * FROM t WHERE k = ''' || :S || '''';
  END;
$$;
```

#### Best Practices

- Reduce the number of conditional assignments reaching the dynamic SQL statement or rewrite the branches as explicit `EXECUTE IMMEDIATE` statements.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0130

Reference to object missing from source

### Severity

Medium

#### Description

The converted code references an object whose definition was not part of the conversion scope, so SnowConvert AI could not resolve it and left the reference as-is. In the example below the collection type `WBC_MISSING_TABLE_TYPE` is never declared, and the emitted message is `'WBC_MISSING_TABLE_TYPE' IS NOT DEFINED IN THE PROVIDED SOURCE. INCLUDE ITS DEFINITION IN THE CONVERSION SCOPE OR REVIEW THE GENERATED CODE.`

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE WBC_TM (K VARCHAR2(10), N NUMBER);

CREATE OR REPLACE PROCEDURE WBC_PM AS
  D WBC_MISSING_TABLE_TYPE;
BEGIN
  SELECT DISTINCT N BULK COLLECT INTO D FROM WBC_TM;
END;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE WBC_TM (
  K VARCHAR(10),
  N NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
;

CREATE OR REPLACE PROCEDURE WBC_PM ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    D WBC_MISSING_TABLE_TYPE !!!RESOLVE EWI!!! /*** SSC-EWI-0130 - 'WBC_MISSING_TABLE_TYPE' IS NOT DEFINED IN THE PROVIDED SOURCE. INCLUDE ITS DEFINITION IN THE CONVERSION SCOPE OR REVIEW THE GENERATED CODE. ***/!!!;
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0130 - 'WBC_MISSING_TABLE_TYPE' IS NOT DEFINED IN THE PROVIDED SOURCE. INCLUDE ITS DEFINITION IN THE CONVERSION SCOPE OR REVIEW THE GENERATED CODE. ***/!!!
    SELECT DISTINCT
      N
    BULK COLLECT INTO D
    FROM
      WBC_TM;
  END;
$$;
```

#### Best Practices

- Include the missing object’s definition in the conversion scope and rerun the conversion.
- If the object is intentionally external, verify that the preserved call is valid in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0131

Hybrid Table without a primary key is not supported in Snowflake

### Severity

Medium

#### Description

SnowConvert AI emits this issue when a hybrid table has no primary key, which Snowflake requires. A standard table is generated as a workaround, so review whether to add a primary key and restore hybrid-table behavior.

#### Code Example

##### Input Code:

##### Oracle

Copy code

```
CREATE TABLE orders (
  order_id NUMBER,
  customer_id NUMBER
);
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0131 - HYBRID TABLES WITHOUT A PRIMARY KEY CONSTRAINT ARE NOT SUPPORTED IN SNOWFLAKE. A STANDARD TABLE IS USED AS A WORKAROUND. ***/!!!
CREATE OR REPLACE TABLE orders (
  order_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  customer_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
);
```

#### Best Practices

- Add a primary key when hybrid-table behavior is required; otherwise review whether the generated standard table is acceptable.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-0132

Indexed column data type not supported for Hybrid Tables

### Severity

Medium

#### Description

SnowConvert AI emits this issue when an indexed column uses a data type that Snowflake hybrid tables do not support. Review the column type and index requirements, or use a standard table if the indexed hybrid-table design cannot be preserved.

#### Code Example

##### Input Code:

##### Transact

Copy code

```
CREATE TABLE dbo.stores (
  store_id GEOGRAPHY NOT NULL,
  CONSTRAINT pk_stores PRIMARY KEY (store_id)
);
```

##### Output Code:

##### Snowflake

```
HybridTablesEvaluated: 1
HybridTablesSelected: 0
HybridTablesSkipped: 1
HybridTablesSkippedUnsupportedIndexedDataType: 1
Issue code: SSC-EWI-0132
```

#### Best Practices

- Change the indexed column to a data type supported by Snowflake hybrid tables or remove the index before deployment.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
