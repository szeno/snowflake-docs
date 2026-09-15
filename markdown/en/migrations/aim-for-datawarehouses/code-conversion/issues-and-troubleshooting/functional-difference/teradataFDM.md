# Code Conversion - Teradata Functional Differences

## SSC-FDM-TD0001

Column converted from Blob data type.

### Description

This message is shown when a data type BLOB is found. Since BLOB is not supported in Snowflake, the type is changed to Binary.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE TableExample
(
ColumnExample BLOB
);
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TableExample
(
ColumnExample BINARY /*** SSC-FDM-TD0001 - COLUMN CONVERTED FROM BLOB DATA TYPE ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0002

Column converted from Clob data type.

### Description

This message is shown when a data type CLOB is found. Since CLOB is not supported in Snowflake, the type is changed to VARCHAR.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE TableExample
(
ColumnExample CLOB
)
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TableExample
(
ColumnExample VARCHAR /*** SSC-FDM-TD0002 - COLUMN CONVERTED FROM CLOB DATA TYPE ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0003

Bash variable found, Snowflake CLI is required to run this script

### Description

When the source code of a BTEQ script file migrated to Snowflake Scripting contains Bash variable placeholders (`$variable` or `${variable}`), they are transformed into Snowflake CLI template variables (`<%variable%>`).

This warning is generated to point out that the execution of the migrated script depends on [Snowflake CLI](/developer-guide/snowflake-cli/index) to work. Snowflake CLI performs client-side substitution of all `<% %>` tokens before sending the SQL to Snowflake, regardless of position (including inside `EXECUTE IMMEDIATE $$` blocks). Please consider the following when running the script:

- All variables must be supplied via the `-D` flag: `snow sql -f script.sql -D "VAR=value"`.
- Multiple variables require separate `-D` flags: `snow sql -f script.sql -D "VAR1=value1" -D "VAR2=value2"`.

#### Example Code

##### Input Code:

Copy code

```
 .LOGON dbc, dbc;

select '$variable', '${variable}', '${variable}_concatenated';

select $colname from $tablename where info = $id;

select ${colname} from ${tablename} where info = ${id};

.LOGOFF;
```

##### Generated Code:

Copy code

```
:force:
EXECUTE IMMEDIATE
$$
  --** SSC-FDM-TD0003 - BASH VARIABLES FOUND, SNOWFLAKE CLI IS REQUIRED TO RUN THIS SCRIPT. USE: snow sql -f <script> -D "VAR=value" FOR EACH VARIABLE. **
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    --.LOGON dbc, dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      SELECT
        '<%variable%>',
        '<%variable%>',
        '<%variable%>_concatenated';
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      SELECT
        <%colname%>
      FROM
        <%tablename%>
      WHERE
        info = <%id%>;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      SELECT
        <%colname%>
      FROM
        <%tablename%>
      WHERE
        info = <%id%>;
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

#### Best Practices

- Run the migrated script with Snowflake CLI: `snow sql -f script.sql -D "variable=value" -D "colname=col1" -D "tablename=my_table" -D "id=123"`
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0004

Period types are handled as two data fields

### Description

Teradata has a period data type used to represent a time interval, with instances of this type having a beginning and ending bound of the same type (time, date or timestamp) along with a set of functions that allow initializing and manipulating period data such as PERIOD, BEGIN, END, and OVERLAPS.

Since the period type is not supported by Snowflake, this type and its related functions are transformed using the following rules:

- Any period type declaration in column tables is migrated as a two-column of the same type.
- The [period value constructor function](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Date-and-Time-Functions-and-Expressions/Period-Functions-and-Operators) is migrated into two different constructors of the period subtype one with the begin value and the other with the end value.
- Supported functions that expect period type parameters are migrated to UDFs as well, these UDFs expect at most two parameters for the begin value and the end value.

#### Example code

##### Input code:

Copy code

```
 -- Additional Params: --SplitPeriodDatatype
CREATE TABLE DateTable
(
	COL1 PERIOD(DATE) DEFAULT PERIOD (DATE '2005-02-03', UNTIL_CHANGED)
);
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE DateTable
(
	COL1_begin DATE DEFAULT DATE '2005-02-03',
	COL1_end DATE DEFAULT DATE '9999-12-31' /*** SSC-FDM-TD0004 - PERIOD DATA TYPES ARE HANDLED AS TWO DATA FIELDS ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0005

Non-standard time zone offsets are not supported in Snowflake, rounded to nearest valid time zone

### Description

While Teradata provides the flexibility to define any time zone offset between `-12:59` and `+14:00` using the `SET TIME ZONE` query, Snowflake exclusively supports time zones listed in the [IANA Time Zone Database](https://www.iana.org/time-zones).

If the specified offset in the SET TIME ZONE query does not align with an IANA standard time zone, Snowflake will automatically round it to the nearest standard time zone with the closest offset. In such a case, a warning message will be generated.

#### Example Code

##### Input Code:

Copy code

```
-- Will be rounded to Asia/Colombo (+05:30)
SET TIME ZONE '05:26';
```

##### Generated Code:

Copy code

```
 -- Will be rounded to Asia/Colombo (+05:30)
--** SSC-FDM-TD0005 - NON-STANDARD TIME ZONE OFFSETS NOT SUPPORTED IN SNOWFLAKE, ROUNDED TO NEAREST VALID TIME ZONE **
ALTER SESSION SET TIMEZONE = 'Asia/Colombo';
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0006

View With Check Option Not Supported.

### Description

This message is shown when a view with the WITH CHECK OPTION clause is found, which is not supported in Snowflake, so it is commented out from the code.

This clause works with updatable views that can be used to execute INSERT and UPDATE commands over the view and internally update the table associated with the view.

The clause is used to restrict the rows that will be affected by the command using the WHERE clause in the view.

For more details see the [documentation](https://docs.teradata.com/r/SQL-Data-Definition-Language-Syntax-and-Examples/July-2021/View-Statements/CREATE-VIEW-and-REPLACE-VIEW/CREATE-VIEW-and-REPLACE-VIEW-Syntax-Elements/WITH-CHECK-OPTION) about the clause functionality.

#### Example code

##### Input code:

Copy code

```
REPLACE VIEW VIEWWITHOPTIONTEST AS
LOCKING ROW FOR ACCESS
SELECT
    *
FROM SOMETABLE
WHERE app_id = 'SUPPLIER'
WITH CHECK OPTION;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE VIEW VIEWWITHOPTIONTEST
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
    *
FROM
    SOMETABLE
WHERE
    UPPER(RTRIM( app_id)) = UPPER(RTRIM('SUPPLIER'))
--    --** SSC-FDM-TD0006 - VIEW WITH OPTION NOT SUPPORTED IN SNOWFLAKE **
--    WITH CHECK OPTION
                     ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0007

Variant column does not support collation.

### Description

This message is shown when a Variant data type in the transformation of a code has a COLLATE clause. Since COLLATE is not supported with the data type VARIANT, it will be removed and a message will be added.

#### Example code

##### Input code:

Copy code

```
-- Additional Params: --useCollateForCaseSpecification
CREATE TABLE TableExample
(
ColumnExample JSON(2500) NOT CASESPECIFIC
)
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TableExample
(
ColumnExample VARIANT
--                      NOT CASESPECIFIC /*** SSC-FDM-TD0007 - VARIANT COLUMN DOES NOT SUPPORT COLLATION ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

The data type JSON is converted to VARIANT, while NOT CASESPECIFIC is converted to a COLLATE clause.

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0008

When NVP\_UDF fourth parameter is non-literal and it contains a backslash, that backslash needs to be escaped.

### Description

Non-literal delimiters with spaces need their backslash escaped in Snowflake.

#### Example code

##### Input code

Copy code

```
SELECT NVP('store = whole foods&#x26;&#x26;store: ?Bristol farms','store', '&#x26;&#x26;', valueDelimiter, 2);
```

##### Generated Code

Copy code

```
 SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', valueDelimiter, 2) /*** SSC-FDM-TD0008 - WHEN NVP_UDF FOURTH PARAMETER IS NON-LITERAL AND IT CONTAINS A BACKSLASH, THAT BACKSLASH NEEDS TO BE ESCAPED ***/;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0009

Converted from integer to varchar for current session default.

### Description

This message is shown when a DEFAULT SESSION is found and the data type is NOT a VARCHAR. If that is the case, the data type is changed to VARCHAR and a message is added.

#### Code Example

##### Input Code:

Copy code

```
 CREATE TABLE TableExample
(
ColumnExample INTEGER DEFAULT SESSION,
ColumnExample2 VARCHAR DEFAULT SESSION
)
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE TableExample
(
ColumnExample VARCHAR DEFAULT CURRENT_SESSION() /*** SSC-FDM-TD0009 - CONVERTED FROM INTEGER TO VARCHAR FOR CURRENT_SESSION DEFAULT ***/,
ColumnExample2 VARCHAR DEFAULT CURRENT_SESSION()
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Let’s look at the example. Note that ColumnExample has a data type INTEGER with DEFAULT SESSION. Since the data type is not VARCHAR, in the output it is transformed to VARCHAR.

The data type of ColumnExample2 hasn’t changed since it is already VARCHAR.

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0010

Table columns between tables (Teradata) DBC.COLUMNSV and INFORMATION\_SCHEMA.COLUMNS (Snowflake). But some columns might not have an exact match in Snowflake.

### Description

Uses of the table `DBC.COLUMNSV` in Teradata are converted to `INFORMATION_SCHEMA.COLUMNS`, but some columns might not have an exact match in Snowflake. That means there are some columns in Teradata for which there is **no** equivalent in Snowflake, and there are others that do have a matching column but the content is not exactly the same.

[![image](/static/images/migrations/sc-assets/TeradataTable(3).png)](/static/images/migrations/sc-assets/TeradataTable(3).png)

[![image](/static/images/migrations/sc-assets/SnowConvertTable(5).png)](/static/images/migrations/sc-assets/SnowConvertTable(5).png)

Notice, for example, that there is no equivalent column for *“ColumnFormat*” in Snowflake and notice also that *“DATA\_TYPE”* seems to be the match for the column *“ColumnType”* in Teradata, but their content greatly differ.

#### Code Example

##### Input Code:

Copy code

```
 SELECT columnname FROM dbc.columnsV WHERE tablename = 'TableN';
```

##### Generated Code:

Copy code

```
 SELECT
COLUMN_NAME AS COLUMNNAME
FROM
--** SSC-FDM-TD0010 - USES OF TABLE DBC.COLUMNSV ARE CONVERTED TO INFORMATION_SCHEMA.COLUMNS, BUT SOME COLUMNS MIGHT NOT HAVE AND EXACT MATCH IN SNOWFLAKE **
INFORMATION_SCHEMA.COLUMNS
WHERE
UPPER(RTRIM(TABLE_NAME)) = UPPER(RTRIM('TableN'));
```

#### Best Practices

- Review what columns were used in Teradata and check if the available content in Snowflake matches your needs.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0011

Unicode BMP escape is not supported.

### Description

Snowflake doesn’t support Unicode BMP, so this message is shown when Teradata [Unicode Delimited Character Literal](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Types-and-Literals/Data-Literals/Unicode-Delimited-Character-Literals) with Unicode BMP escape is transformed to Snowflake.

#### Example code

##### Input Code:

Copy code

```
 SELECT U&'hola #+005132 mundo' UESCAPE '#';
```

##### Generated Code:

Copy code

```
 SELECT
--** SSC-FDM-TD0011 - UNICODE BMP IS NOT SUPPORTED IN SNOWFLAKE **
'hola \u+005132 mundo';
```

#### Best Practices

- Check if a Unicode equivalent exists.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0012

Invalid default value.

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0006](../conversion-issues/teradataEWI#ssc-ewi-td0006) documentation

### Description

The **DEFAULT TIME** / **DEFAULT DATE** / **DEFAULT CURREN\_DATE** */* **DEFAULT DEFAULT CURRENT\_TIME** */* **DEFAULT CURRENT\_TIMESTAMP** column specifications are not supported for the **FLOAT** data type.

#### Example Code

##### Teradata:

Copy code

```
CREATE TABLE T_2004
(
    -- In the output code all of these columns will be FLOAT type
    -- and will include the SSC-FDM-TD0012 message.
    COL1 FLOAT DEFAULT TIME,
    COL2 FLOAT DEFAULT DATE,
    COL3 FLOAT DEFAULT CURRENT_DATE,
    COL4 FLOAT DEFAULT CURRENT_TIME,
    COL5 FLOAT DEFAULT CURRENT_TIMESTAMP
);
```

##### Snowflake Scripting:

Copy code

```
 CREATE TABLE T_2004
(
    -- In the output code all of these columns will be FLOAT type
    -- and will include the SSC-FDM-TD0012 message.
    COL1 FLOAT DEFAULT TIME /*** SSC-FDM-TD0012 - DEFAULT CURRENT_TIME NOT VALID FOR DATA TYPE ***/,
    COL2 FLOAT DEFAULT DATE /*** SSC-FDM-TD0012 - DEFAULT CURRENT_DATE NOT VALID FOR DATA TYPE ***/,
    COL3 FLOAT DEFAULT CURRENT_DATE /*** SSC-FDM-TD0012 - DEFAULT CURRENT_DATE NOT VALID FOR DATA TYPE ***/,
    COL4 FLOAT DEFAULT CURRENT_TIME /*** SSC-FDM-TD0012 - DEFAULT CURRENT_TIME NOT VALID FOR DATA TYPE ***/,
    COL5 FLOAT DEFAULT CURRENT_TIMESTAMP /*** SSC-FDM-TD0012 - DEFAULT CURRENT_TIMESTAMP NOT VALID FOR DATA TYPE ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0013

The Snowflake error code doesn’t match the original Teradata error code.

### Description

This message is shown because the error code saved in the BTEQ ERRORCODE built-in variable could not be the same in Snowflake Scripting.

#### Example code

##### Input code:

Copy code

```
SELECT * FROM table1;

.IF ERRORCODE<>0 THEN .EXIT 1

.QUIT 0
```

##### Generated Code:

Copy code

```
 -- Additional Params: -q snowscript

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      SELECT
        *
      FROM
        table1;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN 1;
    END IF;
    RETURN 0;
  END
$$
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0014

File execution inconsistency

### Description

This EWI appears when the migrated code is a BTEQ sentence executing an environment file with SQL statements E.g. $(<$INPUT\_SQL\_FILE). The difference between the BTEQ execution and the python generated code is that BTEQ continues with the other statements in the file when one of them fails but the python execution stops whenever an error occurs.

#### Example Code

##### Teradata BTEQ:

Copy code

```
 .logmech LDAP;
.logon $LOGON_STR;
.SET DEFAULTS;

$(<$INPUT_SQL_FILE)

.export reset
.logoff
.quit
```

##### Python:

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

from snowconvert.helpers import exec_file
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
#** SSC-FDM-TD0022 - SHELL VARIABLES FOUND, RUNNING THIS CODE IN A SHELL SCRIPT IS REQUIRED **
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. LOGMECH **
  #.logmech LDAP;

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. LOGON **
  #.logon $LOGON_STR

  #** SSC-EWI-TD0005 - THE STATEMENT WAS CONVERTED BUT ITS FUNCTIONALITY IS NOT IMPLEMENTED YET **
  Export.defaults()
  #** SSC-FDM-TD0014 - EXECUTION OF FILE WITH SQL STATEMENTS STOPS WHEN AN ERROR OCCURS **
  exec_file("$INPUT_SQL_FILE")
  #** SSC-EWI-TD0005 - THE STATEMENT WAS CONVERTED BUT ITS FUNCTIONALITY IS NOT IMPLEMENTED YET **
  Export.reset()
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. LOGOFF **
  #.logoff

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0015

Regexp\_Substr Function only supports POSIX regular expressions.

Note

This FDM is deprecated, please refer to [SSC-EWI-0009](../conversion-issues/generalEWI#ssc-ewi-0009) documentation

### Description

Currently, there is no support in Snowflake for extended regular expression beyond the POSIX Basic Regular Expression syntax.

This EWI is added every time a function call to *REGEX\_SUBSTR, REGEX\_REPLACE,* or *REGEX\_INSTR* is transformed to Snowflake to warn the user about possible unsupported regular expressions. Some of the features **not supported** are lookahead, lookbehind, and non-capturing groups.

#### Example Code

##### Teradata:

Copy code

```
 SELECT REGEXP_SUBSTR('qaqequ','q(?=u)', 1, 1);
```

##### Snowflake Scripting:

Copy code

```
 SELECT
--** SSC-FDM-TD0015 - REGEXP_SUBSTR FUNCTION ONLY SUPPORTS POSIX REGULAR EXPRESSIONS **
REGEXP_SUBSTR('qaqequ','q(?=u)', 1, 1);
```

#### Best Practices

- Check the regular expression used in each case to determine whether it needs manual intervention. More information about expanded regex support and alternatives in Snowflake can be found [**here**](https://community.snowflake.com/s/question/0D50Z00007ENLKsSAP/expanded-support-for-regular-expressions-regex)**.**
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0016

Value ‘l’ for parameter ‘match\_arg’ is not supported in Snowflake

### Description

In Teradata functions like *REGEX\_SUBSTR, REGEX\_REPLACE,* or *REGEX\_INSTR* have a parameter called *“match\_arg*”, a character argument with the following valid values:

- `'i'`: case-insensitive matching.
- `'c'`: case sensitive matching.
- `'n'`: the period character (match any character) can match the newline character.
- `'m'`: source string is treated as multiple lines instead of as a single line.
- **`'l'`**: if source\_string exceeds the current maximum allowed source\_string size (currently 16 MB), a NULL is returned instead of an error.
- `'x'`: ignore whitespace (only affects the pattern string).

The argument can contain more than one character.

In Snowflake, the equivalent argument for these functions is *`regexp_parameters.`*A *s*tring of one or more characters that specifies the regular expression parameters used for searching for matches. The supported values are:

- `c`: case-sensitive.
- `i`: case-insensitive.
- `m`: multi-line mode.
- `e`: extract sub-matches.
- `s`: the ‘.’ the wildcard also matches the newline character as well.

As it can be seen, values `'i', 'c', 'm'` are the same in both languages, and the `'n'` value in Teradata is mapped to `'s'`. However, values `'l', 'x'` don’t have an equivalent counterpart.

For the `'x'` value, the functionality is replicated by generating a call to the `REGEXP_REPLACE` function. However, the `'l'` parameter can not be replicated so this warning is generated for these cases.

#### Input Code:

Copy code

```
 SELECT REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'i'),
       REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'c'),
       REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'm'),
       REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'n'),
       REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'l'),
       REGEXP_SUBSTR('Chip Chop','ch(i|o)p', 1, 1, 'x');
```

##### Generated Code:

Copy code

```
 SELECT
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1, 'i'),
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1, 'c'),
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1, 'm'),
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1, 's'),
       --** SSC-FDM-TD0016 - VALUE 'l' FOR PARAMETER 'match_arg' IS NOT SUPPORTED IN SNOWFLAKE **
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1),
       REGEXP_SUBSTR('Chip Chop', 'ch(i|o)p', 1, 1);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0017

The use of foreign tables is not supported in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0076](../conversion-issues/teradataEWI#ssc-ewi-td0076) documentation

### Description

[Foreign tables](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Definition-Language-Syntax-and-Examples/September-2020/Table-Statements/CREATE-FOREIGN-TABLE) enable access to data in external object storage, such as semi-structured and unstructured data in Amazon S3, Azure Blob storage, and Google Cloud Storage. This syntax is not supported in Snowflake. However, there are other alternatives in Snowflake that can be used instead, such as external tables, iceberg tables, and standard tables.

#### Example code

##### Input code:

Copy code

```
 SELECT cust_id, income, age FROM
FOREIGN TABLE (SELECT cust_id, income, age FROM twm_customer)@hadoop1 T1;
```

##### Generated Code:

Copy code

```
 SELECT
cust_id,
income,
age FROM
--** SSC-FDM-TD0017 - THE USE OF FOREIGN TABLES IS NOT SUPPORTED IN SNOWFLAKE. **
 FOREIGN TABLE (SELECT cust_id, income, age FROM twm_customer)@hadoop1 T1;
```

#### Best Practices

- Instead of foreign tables in Teradata, you can use [Snowflake external tables](/user-guide/tables-external). External tables reference data files located in a cloud storage (Amazon S3, Google Cloud Storage, or Microsoft Azure) data lake. This enables querying data stored in files in a data lake as if it were inside a database. External tables can access data stored in any format supported by [COPY INTO <table>](/sql-reference/sql/copy-into-table) statements. \* Another alternative is [Snowflake’s Iceberg tables](https://www.snowflake.com/blog/iceberg-tables-powering-open-standards-with-snowflake-innovations/?lang=es). So, you can think of Iceberg tables as tables that use open formats and customer-supplied cloud storage. This data is stored in Parquet files. \* Finally, there are the [standard Snowflake tables](/sql-reference/sql/create-table) which can be an option to cover the functionality of foreign tables in Teradata \* If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0018

JSON path was not recognized.

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0063](../conversion-issues/teradataEWI#ssc-ewi-td0063) documentation

## SSC-FDM-TD0019

Transaction and profile query tags not supported, using session query tag instead.

#### Description

Teradata can read query-band values from the transaction, session, and profile scopes. The Snowflake equivalent is the `QUERY_TAG` parameter, which exists only at session, user, and account level — there is no transaction or profile scope. When a non-session scope is requested, the session query tag is referenced instead and this marker is emitted, because the value read at run time may differ from the Teradata one.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT GETQUERYBANDVALUE(3, 'department');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-TD0019 - TRANSACTION AND PROFILE LEVEL QUERY TAGS NOT SUPPORTED IN SNOWFLAKE, REFERENCING SESSION QUERY TAG INSTEAD **
GETQUERYBANDVALUE_UDF('department');
```

#### Best Practices

- **Move the query band to session scope**: redesign logic that depends on transaction- or profile-specific values around Snowflake session, user, or account parameters.
- **Check concurrency assumptions**: session-level tagging does not provide the isolation a transaction-scoped query band gave in Teradata.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0020

JSON value was not recognized due to invalid format.

#### Description

A `JSON_TABLE` column expression (`colexpr`) must be deserialized to build the generated projection. When one of its items is not valid JSON, or does not use the property names Teradata expects, the item cannot be interpreted: it is omitted from the generated projection and this marker is emitted, so the converted query can return fewer columns than the source.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT *
FROM JSON_TABLE (
  ON (
    SELECT state_name, json_payload
    FROM regional_schools
  )
  USING
    rowexpr('$.schools[*]')
    colexpr('[{"Ordinal": true}, {"jsonpath": "$.name", "type": "CHAR(12)"}]')
) AS school_rows;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  *
FROM
  (
    SELECT
      state_name,
      --** SSC-FDM-TD0020 - UNRECOGNIZED JSON LITERAL {"Ordinal":"true"} **
      rowexpr.value:name :: CHAR(12) AS Column_1
    FROM
      regional_schools,
      TABLE(FLATTEN(INPUT => json_payload:schools)) rowexpr
  ) school_rows;
```

#### Best Practices

- **Validate the literal**: make sure `colexpr` is well-formed JSON and uses the exact, case-sensitive property names Teradata expects (for example `"ordinal"`, not `"Ordinal"`).
- **Diff the projection**: compare the generated column list against the source alias list to spot items that were dropped.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0021

Built-in reference to PROTECTIONTYPE is not supported in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0046](../conversion-issues/teradataEWI#ssc-ewi-td0046) documentation

#### Description

This error appears when a query referencing the [DBC.DATABASES](https://www.docs.teradata.com/r/hNI_rA5LqqKLxP~Y8vJPQg/GqTx8VuBIkfaC4fso9f5cw) table is executed, and the selected column has no equivalence in Snowflake.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
CREATE VIEW SAMPLE_VIEW
AS
SELECT PROTECTIONTYPE FROM DBC.DATABASES;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE VIEW SAMPLE_VIEW
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":0,"minor":0,"patch":"0"},"attributes":{"component":"teradata","convertedOn":"08/14/2024"}}'
AS
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0046 - BUILT-IN REFERENCE TO PROTECTIONTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
PROTECTIONTYPE
FROM INFORMATION_SCHEMA.DATABASES;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0022

Shell variables found, running this code in a shell script is required.

#### Description

In Teradata scripts, shell variables store temporary values that can be accessed throughout the script. They are written as `$name` or `$\{name\}`, and their values are set with the assignment operator (`=`).

Copy code

```
#!/bin/bash
# define a shell variable
tablename="mytable"
# use the variable in a Teradata SQL query
bteq <<EOF
.LOGON myhost/myuser,mypassword
SELECT * FROM ${tablename};
.LOGOFF
EOF
```

Shell variables behave like string interpolation, so that functionality is kept after conversion. When converting scripts to Python, the variables keep the same source format and the converted code must be run from a shell script (`.sh` file).

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT $column FROM ${tablename}
```

##### Output Code:

##### Snowflake

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
#** SSC-FDM-TD0022 - SHELL VARIABLES FOUND, RUNNING THIS CODE IN A SHELL SCRIPT IS REQUIRED **
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    SELECT $column FROM ${tablename}
    """)
  snowconvert.helpers.quit_application()
if __name__ == "__main__":
  main()
```

#### Best Practices

- Running the converted code in a shell script is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0023

String Similarity might have a different behavior.

#### Description

Teradata `StringSimilarity` with the `jaro_winkler` comparison is translated to the generated `PUBLIC.JAROWINKLER_UDF`. The UDF can return values that differ from the Teradata implementation for some character sets and edge cases, so the conversion is marked for result validation.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT *
FROM StringSimilarity (
  ON (
    SELECT customer_name, comparison_name
    FROM customer_matches
  ) PARTITION BY ANY
  USING ComparisonColumnPairs ('jaro_winkler(customer_name,comparison_name) AS similarity')
) AS matches;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  *
FROM
  --** SSC-FDM-TD0023 - STRING SIMILARITY MIGHT HAVE A DIFFERENT BEHAVIOR. **
  (
    SELECT
      PUBLIC.JAROWINKLER_UDF(customer_name, comparison_name) AS similarity
    FROM
      customer_matches
  ) matches;
```

#### Best Practices

- **Re-baseline your thresholds**: compare representative Teradata and Snowflake similarity scores before keeping existing match cut-offs.
- **Cover the edge cases**: include empty strings, NULLs, accented characters, and near-threshold values in the validation data set.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0024

Set table functionality not supported.

### Description

This EWI is shown when a Create Table with the SET option is found. Since the SET TABLE is not supported in Snowflake, it is removed.

#### Example Code

##### Teradata:

Copy code

```
 CREATE SET TABLE TableExample
(
ColumnExample Number
)
```

Copy code

```
 CREATE SET VOLATILE TABLE SOMETABLE, LOG AS
(SELECT ColumnExample FROM TableExample);
```

##### Snowflake Scripting:

Copy code

```
 --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
CREATE OR REPLACE TABLE TableExample
(
ColumnExample NUMBER(38, 18)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy code

```
 --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
CREATE OR REPLACE TEMPORARY TABLE SOMETABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
(
SELECT
ColumnExample FROM
TableExample
);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0025

Teradata Database Temporal Table is not supported in Snowflake

### Description

The [Teradata Database Temporal Support](https://docs.teradata.com/r/0TSAVrLIwk23SLHbA4nUvQ/root) involves the creation of temporal tables and temporal DDL and DML objects. The support for temporal (time-aware) tables and data are not supported in Snowflake since there is not an absolute equivalent.

All these statements are recognized (parsed), but to execute the queries in Snowflake, these elements are removed in the translation process.

It is worth noting that in cases where an `abort` statement is encountered, it will be transformed into a `Delete` command to keep the equivalence functionality allows you to undo operations performed during a transaction and restore the database to the state it had at the beginning.

#### Example code

The following example shows a Temporal-form Select being translated to a usual Select.

##### Input code:

Copy code

```
 SEQUENCED VALIDTIME
   SELECT
   Policy_ID,
   Customer_ID
   FROM Policy
      WHERE Policy_Type = 'AU';
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-TD0025 - TEMPORAL FORMS ARE NOT SUPPORTED IN SNOWFLAKE **
--SEQUENCED VALIDTIME
SELECT
   Policy_ID,
   Customer_ID
   FROM
   Policy
      WHERE
   UPPER(RTRIM( Policy_Type)) = UPPER(RTRIM('AU'));
```

Case where the `Abort` command is used in the context of a transaction.

##### Input code:

Copy code

```
 CREATE OR REPLACE PROCEDURE TEST.ABORT_STATS()
BEGIN
    CURRENT VALIDTIME AND NONSEQUENCED TRANSACTIONTIME ABORT
     FROM table_1
     WHERE table_1.x1 = 1;
END;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE PROCEDURE TEST.ABORT_STATS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --    CURRENT VALIDTIME AND NONSEQUENCED TRANSACTIONTIME
        --** SSC-FDM-TD0025 - TEMPORAL FORMS ARE NOT SUPPORTED IN SNOWFLAKE **
        LET _ROW_COUNT FLOAT;
        SELECT
            COUNT(*)
        INTO
            _ROW_COUNT
            FROM
            table_1
                 WHERE table_1.x1 = 1;
            IF (_ROW_COUNT > 0) THEN
            ROLLBACK;
            END IF;
    END;
$$;
```

#### 

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0026

GOTO statement was removed due to if statement inversion.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

It is common to use GOTO command with IF and LABEL commands to replicate the functionality of an SQL if statement. When used in this way, it is possible to transform them directly into an if, if-else, or even an if-elseif-else statement. However, in these cases, the GOTO commands become unnecessary and should be removed to prevent them from being replaced by a LABEL section.

#### Example Code

**Input Code:**

Copy code

```
 -- Additional Params: --scriptsTargetLanguage SnowScript
.If ActivityCount = 0 THEN .GOTO endIf
DROP TABLE TABLE1;
.Label endIf
SELECT A FROM TABLE1;
```

**Output Code**

Copy code

```
 EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    IF (NOT (STATUS_OBJECT['SQLROWCOUNT'] = 0)) THEN
      --** SSC-FDM-TD0026 - GOTO endIf WAS REMOVED DUE TO IF STATEMENT INVERSION **

      BEGIN
        DROP TABLE TABLE1;
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
      EXCEPTION
        WHEN OTHER THEN
          STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
      END;
    END IF;
    /*.Label endIf*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    BEGIN
      SELECT
        A
      FROM
        TABLE1;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
  END
$$
```

##### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0027

TD\_UNPIVOT transformation requires column information that could not be found, columns missing in result

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0061](../conversion-issues/teradataEWI#ssc-ewi-td0061) documentation.

### Description

The [TD\_UNPIVOT](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Operators-and-User-Defined-Functions/Table-Operators/TD_UNPIVOT) function is supported and transformed, and can be used to represent columns from a table as rows.

However, this transformation requires information about the table/tables columns to work, more specifically the names of the columns. When this information is not present the transformation may be left in an incomplete state where columns are missing from the result, this EWI is generated in these cases.

#### Example code

##### Input Code:

Copy code

```
 CREATE TABLE unpivotTable  (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
);

SELECT * FROM
 TD_UNPIVOT(
 	ON unpivotTable
 	USING
 	VALUE_COLUMNS('Income', 'Expenses')
 	UNPIVOT_COLUMN('Semester')
 	COLUMN_LIST('firstSemesterIncome, firstSemesterExpenses', 'secondSemesterIncome, secondSemesterExpenses')
 	COLUMN_ALIAS_LIST('First', 'Second')
 )X ORDER BY mykey;

SELECT * FROM
 TD_UNPIVOT(
 	ON unknownTable
 	USING
 	VALUE_COLUMNS('MonthIncome')
 	UNPIVOT_COLUMN('Months')
 	COLUMN_LIST('januaryIncome', 'februaryIncome', 'marchIncome', 'aprilIncome')
 	COLUMN_ALIAS_LIST('January', 'February', 'March', 'April')
 )X ORDER BY yearKey;
```

##### Generated Code:

Copy code

```
 CREATE TABLE unpivotTable (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

SELECT
	* FROM
	(
		SELECT
			myKey,
			TRIM(GET_IGNORE_CASE(OBJECT_CONSTRUCT('FIRSTSEMESTERINCOME', 'First', 'FIRSTSEMESTEREXPENSES', 'First', 'SECONDSEMESTERINCOME', 'Second', 'SECONDSEMESTEREXPENSES', 'Second'), Semester), '"') AS Semester,
			Income,
			Expenses
		FROM
			unpivotTable UNPIVOT(Income FOR Semester IN (
				firstSemesterIncome,
				secondSemesterIncome
			)) UNPIVOT(Expenses FOR Semester1 IN (
				firstSemesterExpenses,
				secondSemesterExpenses
			))
		WHERE
			Semester = 'FIRSTSEMESTERINCOME'
			AND Semester1 = 'FIRSTSEMESTEREXPENSES'
			OR Semester = 'SECONDSEMESTERINCOME'
			AND Semester1 = 'SECONDSEMESTEREXPENSES'
	) X ORDER BY mykey;

	SELECT
	* FROM
	--** SSC-FDM-TD0027 - TD_UNPIVOT TRANSFORMATION REQUIRES COLUMN INFORMATION THAT COULD NOT BE FOUND, COLUMNS MISSING IN RESULT **
	(
		SELECT
			TRIM(GET_IGNORE_CASE(OBJECT_CONSTRUCT('JANUARYINCOME', 'January', 'FEBRUARYINCOME', 'February', 'MARCHINCOME', 'March', 'APRILINCOME', 'April'), Months), '"') AS Months,
			MonthIncome
		FROM
			unknownTable UNPIVOT(MonthIncome FOR Months IN (
				januaryIncome,
				februaryIncome,
				marchIncome,
				aprilIncome
			))
	) X ORDER BY yearKey;
```

#### Best Practices

- There are two ways of supplying the information about columns to the conversion tool: put the table specification in the same file as the TD\_UNPIVOT call or specify a column list in the SELECT query of the ON expression instead of SELECT \* or the table name.
- This issue can be safely ignored if ALL the columns from the input table/tables are unpivoted, otherwise, the result will have missing columns.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0028

JSON\_TABLE not transformed, column names could not be retrieved from semantic information

Note

This FDM is deprecated, please refer to [SSC-EWI-TD0060](../conversion-issues/teradataEWI#ssc-ewi-td0060) documentation.

### Description

The JSON\_TABLE function can be transformed, however, this transformation requires knowing the name of the columns that are being selected in the JSON\_TABLE ON subquery.

This message is generated to warn the user that the column names were not explicitly put in the subquery (for example, a SELECT \* was used) and the semantic information of the tables being referenced was not found, meaning the column names could not be extracted.

#### Example code

##### Input Code:

Copy code

```
 CREATE TABLE demo.Train (
    firstCol INT,
    jsonCol JSON(400),
    thirdCol VARCHAR(30)
);

SELECT * FROM JSON_TABLE
(ON (SELECT T.*
           FROM demo.Train T)
USING rowexpr('$.schools[*]')
               colexpr('[ {"jsonpath" : "$.name",
                           "type" : "CHAR(20)"},
                          {"jsonpath" : "$.type",
                           "type" : "VARCHAR(20)"}]')
)
AS JT;

SELECT * FROM JSON_TABLE
(ON (SELECT T.*
           FROM demo.missingTable T)
USING rowexpr('$.schools[*]')
               colexpr('[ {"jsonpath" : "$.name",
                           "type" : "CHAR(20)"},
                          {"jsonpath" : "$.type",
                           "type" : "VARCHAR(20)"}]')
)
AS JT;
```

##### Generated Code:

Copy code

```
 CREATE TABLE demo.Train (
    firstCol INT,
    jsonCol VARIANT,
    thirdCol VARCHAR(30)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT
    * FROM
    (
        SELECT
            firstCol,
            rowexpr.value:name :: CHAR(20) AS Column_0,
            rowexpr.value:type :: VARCHAR(20) AS Column_1,
            thirdCol
        FROM
            demo.Train T,
            TABLE(FLATTEN(INPUT => jsonCol:schools)) rowexpr
    ) JT;

    SELECT
    * FROM
    --** SSC-FDM-TD0028 - JSON_TABLE NOT TRANSFORMED, COLUMN NAMES COULD NOT BE RETRIEVED FROM SEMANTIC INFORMATION **
    JSON_TABLE
   (ON
       !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (
        SELECT
            T.*
                  FROM
            demo.missingTable T)
   USING rowexpr('$.schools[*]')
                  colexpr('[ {"jsonpath" : "$.name",
                           "type" : "CHAR(20)"},
                          {"jsonpath" : "$.type",
                           "type" : "VARCHAR(20)"}]')
   )
   AS JT;
```

#### Best Practices

- Please check the code provided is complete, if you did not provide the table definition please re-execute the code with the table definition present.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0029

Snowflake supported formats for TO\_CHAR differ from Teradata and may fail or have different behavior

### Format elements that depend on session parameters

Some Teradata format elements are mapped to Snowflake functions that depend on the value of session parameters. To avoid functional differences in the results you should set these session parameters to the same values they have in Teradata. Identified format elements that are mapped to this kind of functions are:

- **D**: Mapped to `DAYOFWEEK` function, the results of this function depend on the `WEEK_START` session parameter, by default Teradata considers Sunday as the first day of the week, while in Snowflake it is Monday.
- **WW**: Mapped to `WEEK` function, this function depends on the session parameter `WEEK_OF_YEAR_POLICY` which by default is set to use the ISO standard (the first week of year is the first to contain at least four days of January) but in Teradata is set to consider January first as the start of the first week.

To modify session parameters, use `ALTER SESSION SET parameter_name = value`. For more information, see the [Snowflake session parameters reference](/sql-reference/parameters).

#### Single parameter version of TO\_CHAR

The single parameter version of `TO_CHAR(Datetime)` makes use of the default formats specified in the session parameters `TIMESTAMP_LTZ_OUTPUT_FORMAT`, `TIMESTAMP_NTZ_OUTPUT_FORMAT`, `TIMESTAMP_TZ_OUTPUT_FORMAT` and `TIME_OUTPUT_FORMAT`. To avoid differences in behavior please set them to the same values used in Teradata.

For `TO_CHAR(Numeric)` Snowflake generates the varchar representation using either the `TM9` or `TME` formats to get a compact representation of the number, Teradata also generates compact representations of the numbers so no action is required.

#### Example Code

##### Input Code:

Copy code

```
 select to_char(date '2008-09-13', 'DD/RM/YYYY');

select to_char(date '2010-10-20', 'DS');

select to_char(1255.495, 'SC9999.9999', 'nls_iso_currency = ''EUR''');

select to_char(45620);
```

##### Generated Code:

Copy code

```
 SELECT
TO_CHAR(date '2008-09-13', 'DD/') || PUBLIC.ROMAN_NUMERALS_MONTH_UDF(date '2008-09-13') || TO_CHAR(date '2008-09-13', '/YYYY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;

SELECT
TO_CHAR(date '2010-10-20', 'MM/DD/YYYY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;

SELECT
PUBLIC.INSERT_CURRENCY_UDF(TO_CHAR(1255.495, 'S9999.0000'), 2, 'EUR') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;

SELECT
TO_CHAR(45620) /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

### Best Practices

- When using FF either try to use DateTime types with the same precision that you use in Teradata or add a precision to the format element to avoid the different behavior.
- When using timezone-related format elements, use the first parameter of type `TIMESTAMP_TZ` to avoid different behavior. Also remember that the `TIME` type cannot have time zone information in Snowflake.
- Set the necessary session parameters with the default values from Teradata to avoid different behavior.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0030

A return statement was added at the end of the label section to ensure the same execution flow

### Description

When a Goto statement is replaced with a Label section and does not contain a return statement, one is added at the end of the section to ensure the same execution flow.

BTEQ after a Goto command is executed, the statements between the goto command and the label command with the same name are ignored. So, to avoid those statements being executed the label section should contain a return statement.

In addition, it is worth mentioning the Goto command skips all the other statements except for the Label with the same name, which is when the execution resumes. Therefore, the execution will never resume in a label section defined before the Goto command.

#### Example Code

##### Input Code:

Copy code

```
 -- Additional Params: --scriptsTargetLanguage SnowScript
.LOGON dbc,dbc;
select 'STATEMENTS';
.GOTO LABEL_B
select 'IGNORED STATEMENTS';
.label LABEL_B
select 'LABEL_B STATEMENTS';
```

##### Generated Code

Copy code

```
 EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: --scriptsTargetLanguage SnowScript
    --.LOGON dbc,dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      SELECT
        'STATEMENTS';
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

    /*.label LABEL_B*/

    BEGIN
      SELECT
        'LABEL_B STATEMENTS';
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    --** SSC-FDM-TD0030 - A RETURN STATEMENT WAS ADDED AT THE END OF THE LABEL SECTION LABEL_B TO ENSURE THE SAME EXECUTION FLOW **
    RETURN 0;
    BEGIN
      SELECT
        'IGNORED STATEMENTS';
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    /*.label LABEL_B*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    BEGIN
      SELECT
        'LABEL_B STATEMENTS';
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
  END
$$
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0031

ST\_DISTANCE results are slightly different from ST\_SPHERICALDISTANCE

### Description

The Teradata function ST\_SPHERICALDISTANCE calculates the distance between two spherical coordinates on the planet using the Haversine formula, on the other side, the Snowflake ST\_DISTANCE function does not utilize the haversine formula to calculate the minimum distance between two geographical points.

#### Example Code

##### Input Code:

Copy code

```
 --The distance between New York and Los Angeles
Select Cast('POINT(-73.989308 40.741895)' As ST_GEOMETRY) As location1,
	Cast('POINT(40.741895 34.053691)' As ST_GEOMETRY) As location2,
	location1.ST_SPHERICALDISTANCE(location2) As Distance_In_km;
```

##### Teradata Output

| location1 | location2 | Distance\_In\_Km |
| --- | --- | --- |
| POINT (-73.989308 40.741895) | POINT (40.741895 34.053691) | 9351139.978062356 |

Expand

Show lessSee more

##### Generated Code

Copy code

```
 --The distance between New York and Los Angeles
SELECT
	TO_GEOGRAPHY('POINT(-73.989308 40.741895)') As location1,
	TO_GEOGRAPHY('POINT(40.741895 34.053691)') As location2,
	--** SSC-FDM-TD0031 - ST_DISTANCE RESULTS ARE SLIGHTLY DIFFERENT FROM ST_SPHERICALDISTANCE **
	ST_DISTANCE(
	location1, location2) As Distance_In_km;
```

##### Snowflake Output

| LOCATION1 | LOCATION2 | DISTANCE\_IN\_KM |
| --- | --- | --- |
| { “coordinates”: [ -73.989308, 40.741895 ], “type”: “Point” } | { “coordinates”: [ 40.741895, 34.053691 ], “type”: “Point” } | 9351154.65572674 |

Expand

Show lessSee more

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0032

CASESPECIFIC clause was removed from LIKE expression

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This error appears when the `LIKE` expression is accompanied by the `[NOT] CASESPECIFIC` clause.

#### Example Code

##### Input Code:

Copy code

```
 SELECT * FROM MY_TABLE
WHERE Name Like 'Marco%' (NOT CASESPECIFIC);
```

##### Generated Code

Copy code

```
 SELECT
    * FROM
    MY_TABLE
WHERE Name ILIKE 'Marco%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

#### Best Practices

- Case-Specific Behavior in TERADATA depends on TMODE system configuration.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0033

ACTIVITY\_COUNT transformation might require manual adjustments

Note

This FDM is deprecated.

### Description

The `ACTIVITY_COUNT` status variable returns the number of rows affected by an SQL DML statement in an embedded SQL or stored procedure application. For more information, see the [Teradata ACTIVITY\_COUNT documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/Result-Code-Variables/ACTIVITY_COUNT).

As explained in its translation specification, there is a workaround to emulate `ACTIVITY_COUNT`’s behavior through:

Copy code

```
 SELECT $1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

However, this presents some limitations listed below.

### Limitations

#### First case

If `ACTIVITY_COUNT` is called twice or more times before executing another DML statement, the transformation might not return the expected values.

##### Teradata

Copy code

```
 REPLACE PROCEDURE InsertEmployeeSalaryAndLog_1 ()
BEGIN
    DECLARE row_count1 INT;

    INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
    VALUES (101, 'Alice', 'Smith', 10, 70000.00);

    -- Get the ACTIVITY_COUNT
    SET row_count1 = ACTIVITY_COUNT;
    SET row_count1 = ACTIVITY_COUNT;

    -- Insert the ACTIVITY_COUNT into the activity_log table
    INSERT INTO activity_log (operation, row_count)
    VALUES ('INSERT PROCEDURE', row_count1);
END;

REPLACE PROCEDURE InsertEmployeeSalaryAndLog_2 ()
BEGIN
    DECLARE row_count1 INT;
    DECLARE message VARCHAR(100);

    INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
    VALUES (101, 'Alice', 'Smith', 10, 70000.00);

    -- Get the ACTIVITY_COUNT
    SET row_count1 = ACTIVITY_COUNT + 1;
    SET row_count1 = ACTIVITY_COUNT;

    -- Insert the ACTIVITY_COUNT into the activity_log table
    INSERT INTO activity_log (operation, row_count)
    VALUES ('INSERT PROCEDURE', row_count1);
END;
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE InsertEmployeeSalaryAndLog_1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/15/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        row_count1 INT;
    BEGIN

        INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
        VALUES (101, 'Alice', 'Smith', 10, 70000.00);

           -- Get the ACTIVITY_COUNT
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;

        -- Insert the ACTIVITY_COUNT into the activity_log table
        INSERT INTO activity_log (operation, row_count)
        VALUES ('INSERT PROCEDURE', :row_count1);
    END;
$$;

CREATE OR REPLACE PROCEDURE InsertEmployeeSalaryAndLog_2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/15/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        row_count1 INT;
        message VARCHAR(100);
    BEGIN

        INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
        VALUES (101, 'Alice', 'Smith', 10, 70000.00);

           -- Get the ACTIVITY_COUNT
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/ + 1;
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;

        -- Insert the ACTIVITY_COUNT into the activity_log table
        INSERT INTO activity_log (operation, row_count)
        VALUES ('INSERT PROCEDURE', :row_count1);
    END;
$$;
```

In both procedures, `ACTIVITY_COUNT` is called twice before another DML statement is called. In Teradata, `ACTIVITY_COUNT` will return the number of rows in the `INSERT` statement above them, even when called twice. However, since the Snowflake transformation uses `LAST_QUERY_ID()`, the result depends on the result set held by `LAST_QUERY_ID()`.

`InsertEmployeeSalaryAndLog_1()` requires no manual adjustments. Check the Query History (bottom-up):

[![image](/static/images/migrations/sc-assets/image(461).png)](/static/images/migrations/sc-assets/image(461).png)

1. `INSERT` statement is executed. `LAST_QUERY_ID()` will point to this statement.
2. `SELECT` (first `ACTIVITY_COUNT`) is executed, and `$1` will be `1`. `LAST_QUERY_ID()` will point to this statement.
3. `SELECT` (second `ACTIVITY_COUNT`) is executed; since the last statement result was `1`, `$1` will be `1` for this `SELECT` as well.
4. Finally, `row_count1` holds the value `1`, which is inserted in `activity_log`.

On the other side, `InsertEmployeeSalaryAndLog_2()` does require manual adjustments. Check the Query History (bottom-up):

[![image](/static/images/migrations/sc-assets/image(460).png)](/static/images/migrations/sc-assets/image(460).png)

1. `INSERT` statement is executed. `LAST_QUERY_ID()` will point to this statement.
2. SELECT (first `ACTIVITY_COUNT`) is executed, and `$1` will be `1`. However, notice how `QUERY_TEXT` has the `+ 10`; this will affect the result that will be scanned. `LAST_QUERY_ID()` will point to this statement.
3. `SELECT` (second `ACTIVITY_COUNT`) is executed. The result for the last query is `11`; thus `$1` will hold `11` instead of the expected `1`.
4. Finally, `row_count1` holds the value `11`, which is inserted in `activity_log`.

These are the values inserted in `activity_log`:

| LOG\_ID | OPERATION | ROW\_COUNT | LOG\_TIMESTAMP |
| --- | --- | --- | --- |
| 1 | INSERT PROCEDURE | 1 | 2024-07-15 09:22:21.725 |
| 101 | INSERT PROCEDURE | 11 | 2024-07-15 09:22:26.248 |

Expand

Show lessSee more

#### Adjustments for the first case

As per Snowflake’s documentation for [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id), you can specify the query to return, based on the position of the query. `LAST_QUERY_ID(-1)` returns the latest query, `(-2)` the second last query, and so on.

The fix for the problem in `InsertEmployeeSalaryAndLog_2()` will be to simply specify `LAST_QUERY_ID(-2)` in the second use of `ACTIVITY_COUNT` (second `SELECT`) so that it gets the results from the `INSERT` statement instead:

Copy code

```
 ...
INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
        VALUES (101, 'Alice', 'Smith', 10, 70000.00);

           -- Get the ACTIVITY_COUNT
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/ + 1;
        row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID(-2)))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;
...
```

#### Second case

If `ACTIVITY_COUNT` is called after a non DML statement was executed, the transformation will not return the expected values.

##### Teradata

Copy code

```
REPLACE PROCEDURE InsertEmployeeSalaryAndLog_3 ()
BEGIN
    DECLARE row_count1 INT;
    DECLARE emp_id INT;
    DECLARE message VARCHAR(100);

    INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
    VALUES (101, 'Alice', 'Smith', 10, 70000.00);

    SELECT employee_id INTO emp_id FROM employees;
    -- Get the ACTIVITY_COUNT
    SET row_count1 = ACTIVITY_COUNT;
    SET message = 'EMPLOYEE INSERTED - ID: ' || emp_id;

    -- Insert the ACTIVITY_COUNT into the activity_log table
    INSERT INTO activity_log (operation, row_count)
    VALUES (message, row_count1);
END;
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE InsertEmployeeSalaryAndLog_3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/15/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        row_count1 INT;
        emp_id INT;
        message VARCHAR(100);
    BEGIN

        INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
        VALUES (101, 'Alice', 'Smith', 10, 70000.00);
        SELECT
            employee_id INTO
            :emp_id
        FROM
            employees;
               -- Get the ACTIVITY_COUNT
               row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
               ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;
               message := 'EMPLOYEE INSERTED - ID: ' || emp_id;

               -- Insert the ACTIVITY_COUNT into the activity_log table
               INSERT INTO activity_log (operation, row_count)
               VALUES (:message, :row_count1);
    END;
$$;
```

Similar to the previous, `LAST_QUERY_ID` does not point to the correct query and thus returns an incorrect value, which is assigned to row\_count1. Check the Query History (bottom-up):

[![image](/static/images/migrations/sc-assets/image(462).png)](/static/images/migrations/sc-assets/image(462).png)

1. `INSERT` statement is executed. `LAST_QUERY_ID()` will point to this statement.
2. `SELECT INTO` is executed, and $1 will be 101. `LAST_QUERY_ID()` will point to this statement.
3. `SELECT` (`ACTIVITY_COUNT`) is executed. The result for the last query is `101`; thus `$1` will hold `101` instead of the expected 1.
4. Finally, `row_count1` holds the value `101`, which is inserted in `activity_log`.

These are the values inserted in activity\_log:

| LOG\_ID | OPERATION | ROW\_COUNT | LOG\_TIMESTAMP |
| --- | --- | --- | --- |
| 1 | EMPLOYEE INSERTED - ID: 101 | 101 | 2024-07-15 11:00:38.000 |

Expand

Show lessSee more

#### Adjustments for the second case

1. One possible fix is to specify the correct query to return by `LAST_QUERY_ID`. For example, here `LAST_QUERY_ID(-2)` will be the correct query to point to.

Copy code

```
 ...
row_count1 := (
            SELECT
                $1
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID(-2)))
               ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;
               ...
```

2. Another possible fix is to use `ACTIVITY_COUNT` (`SELECT`) immediately after executing the `INSERT` statement.

Copy code

```
...
INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (101, 'Alice', 'Smith', 10, 70000.00);
-- Get the ACTIVITY_COUNT
       row_count1 := (
    SELECT
        $1
    FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()))
       ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;
SELECT
    employee_id INTO
    :emp_id
FROM
    employees;
       message := 'EMPLOYEE INSERTED - ID: ' || emp_id;
...
```

#### Best Practices

- Make sure to point to the correct query when using `LAST_QUERY_ID`.
- Make sure `ACTIVITY_COUNT` is used immediately after the DML statement to evaluate.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0034

Period contains transformed to user defined function.

### Description

The Teradata `CONTAINS` expression performs a validation indicating whether the element at the right is contained in the element at the left which is supposed to be of `PERIOD` type. The CONTAINS only applies for `DATE`, `TIME`, `TIMESTAMP` or `PERIOD`. Since `PERIOD` is not supported in Snowflake, a user-defined function will emulate the logic of the native `CONTAINS` behavior.

#### Example Code

##### Input Code:

Copy code

```
  UPDATE TABLE1
  SET COL1 = CURRENT_TIMESTAMP
  WHERE COL3 CONTAINS CURRENT_TIMESTAMP;
```

##### Generated Code

Copy code

```
  UPDATE TABLE1
  SET
    COL1 = CURRENT_TIMESTAMP()
  WHERE
    PUBLIC.PERIOD_CONTAINS_UDF(COL3, CURRENT_TIMESTAMP()) /*** SSC-FDM-TD0034 - PERIOD CONTAINS EXPRESSION TRANSFORMED TO USER DEFINED FUNCTION. ***/
```

#### Best Practices

- The `VARCHAR` used instead of `PERIOD` assumes `<PERIOD_BEGIN>*<PERIOD_END>` format in all the values. If the values are split by a token different than `*`, you can change the value returned from the `PUBLIC.GET_PERIOD_SEPARATOR` UDF. Notice that the structure should have a token that marks the begin and end of a PERIOD, so the two dates, times or timestamps should be always separated with the same token.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0035

Statistics function not needed in Snowflake.

Note

This FDM is deprecated, please refer to [SSC-FDM-0037](../functional-difference/generalFDM#ssc-fdm-0037) documentation

### Description

DROP, COLLECT, or HELP statistics are not needed in Snowflake. Snowflake already collects statistics used for automatic query optimization, which is why these statistics statements are used in Teradata.

#### Example Code

##### Input Code:

Copy code

```
  HELP STATISTICS TestName;
```

##### Generated Code

Copy code

```
  ----** SSC-FDM-TD0035 - HELP STATISTICS NOT NEEDED. SNOWFLAKE AUTOMATICALLY COLLECTS STATISTICS. **
  --HELP STATISTICS TestName
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0036

Snowflake does not support the period datatype, all periods are handled as varchar instead

Note

Some parts in the output code are omitted for clarity reasons.

### Precision of generated varchar representations

PERIOD\_UDF generates the varchar representation of a period using the default formats for timestamps and time specified in Snowflake, this means timestamps will have three precision digits and time variables will have zero, because of this you may find that the results have a higher/lower precision from the expected, there are two options to modify how many precision digits are included in the resulting string:

- Use the three parameters version of PERIOD\_UDF: This overload of the function takes the`PRECISIONDIGITS`parameter, an integer between 0 and 9 to control how many digits of the fractional time part will be included in the result. Note that even if Snowflake supports up to nine digits of precision the maximum in Teradata is six. Example:

| Call | Result |
| --- | --- |
| `PUBLIC.PERIOD_UDF(time '13:30:45.870556', time '15:35:20.344891', 0)` | `'13:30:45*15:35:20'` |
| `PUBLIC.PERIOD_UDF(time '13:30:45.870556', time '15:35:20.344891', 2)` | `'13:30:45.87*15:35:20.34'` |
| `PUBLIC.PERIOD_UDF(time '13:30:45.870556', time '15:35:20.344891', 5)` | `'13:30:45.87055*15:35:20.34489'` |

Expand

Show lessSee more

- Alter the session parameters `TIMESTAMP_NTZ_OUTPUT_FORMAT` and `TIME_OUTPUT_FORMAT`: The commands `ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT = <format>` and`ALTER SESSION SET TIME_OUTPUT_FORMAT = <format>`

  can be used to modify the formats Snowflake uses by default for the current session, modifying them to include the desired number of precision digits changes the result of future executions of PERIOD\_UDF for the current session.

#### Example code

##### Input code:

Copy code

```
 create table vacations (
    employeeName varchar(50),
    duration period(date)
);

insert into vacations values ('Richard', period(date '2021-05-15', date '2021-06-15'));

select end(duration) from vacations;
```

##### Generated Code:

Copy code

```
 CREATE OR REPLACE TABLE vacations (
    employeeName varchar(50),
    duration VARCHAR(24) /*** SSC-FDM-TD0036 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

INSERT INTO vacations
VALUES ('Richard', PUBLIC.PERIOD_UDF(date '2021-05-15', date '2021-06-15') /*** SSC-FDM-TD0036 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/);

SELECT
    PUBLIC.PERIOD_END_UDF(duration) /*** SSC-FDM-TD0036 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/ from
    vacations;
```

#### Best Practices

- Since the behavior of`PERIOD`and its related functions is emulated using varchar, we recommend reviewing the results obtained to ensure its correctness.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0037

LOGTABLE removed.

### Description

The [`.LOGTABLE`](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Teradata-MultiLoad-Commands/LOGTABLE) command in [MLoad](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-MultiLoad-Reference-20.00/Using-Teradata-MultiLoad) is used for checkpoint and restart metadata, but Snowflake handles these features automatically. Instead of `.LOGTABLE`, you can monitor and audit your data loads in Snowflake using the [`COPY_HISTORY`](/sql-reference/functions/copy_history) function and related [account usage views](/sql-reference/account-usage).

#### Code Example

##### Input Code:

Copy code

```
.LOGTABLE ${DATABASE}.LT_EMPLOYEES;
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0037 - REMOVED NEXT STATEMENT. USE COPY_HISTORY() FOR MONITORING **
-- .LOGTABLE ${DATABASE}.LT_EMPLOYEES;
```

#### Best Practices

- Use [`COPY_HISTORY`](/sql-reference/functions/copy_history) and related Snowflake account usage views to monitor load history.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0038

PUT command requires execution through Snowflake CLI.

### Description

The [`PUT`](/sql-reference/sql/put) command lets you upload files to a Snowflake [stage](/sql-reference/sql/create-stage), but it only works when you run your script with [Snowflake CLI](/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`). It won’t work inside scripts, procedures, or the web UI. If your script includes a `PUT` command, make sure to run it using Snowflake CLI.

#### Code Example

##### Generated Code:

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

#### Best Practices

- Run scripts containing [`PUT`](/sql-reference/sql/put) commands using [Snowflake CLI](/developer-guide/snowflake-cli/index): `snow sql -f script.sql`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0039

Collation handled at query level for this table, any new query over this table should apply collation appropriately.

### Description

If using the SnowConvert AI Desktop application and the “Use COLLATE for Case Specification” is enabled, the case insensitive behavior of the NOT CASESPECIFIC clause will be emulated by modifying comparisons in queries with the UPPER function. This is performed at query level instead of using collation at the column level. This warning will be generated on any table whose case sensitivity is being emulated at the query level to remind the user that any new query over these tables will require to properly handle the case sensitivity behavior on comparisons.

#### Example code

##### Input code:

Copy code

```
CREATE TABLE my_table
(
    col1 VARCHAR(50) NOT CASESPECIFIC
);

SELECT * FROM my_table WHERE col1 = 'test';
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0039 - COLLATION HANDLED AT QUERY LEVEL FOR THIS TABLE, ANY NEW QUERY OVER THIS TABLE SHOULD APPLY COLLATION APPROPRIATELY **
CREATE OR REPLACE TABLE my_table
(
    col1 VARCHAR(50)
);

SELECT
    * FROM
    my_table
WHERE
    UPPER(RTRIM( col1)) = UPPER(RTRIM('test'));
```

#### Best Practices

- If you provided all your queries over the table to SnowConvert as part of your transformation then no additional actions are required, this FDM is informational only.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0040

Column-level FORMAT clause is not supported in Snowflake. Conversion functions are used in DML statements as a workaround.

### Description

In Teradata, the `FORMAT` clause on a column definition tells the system how to display and parse datetime values. For example, a column defined as `DATE FORMAT 'MM-DD-YYYY'` expects date strings like `'03-30-2026'`.

Snowflake does not have an equivalent `FORMAT` clause on column definitions. To preserve the original behavior:

1. The `FORMAT` clause is **commented out** in the `CREATE TABLE` output.
2. **Explicit conversion functions** (`TO_DATE`, `TO_TIMESTAMP`, or `TO_TIME`) are **added** around string literals in DML statements that reference the formatted column, using the Snowflake-equivalent format string.

This ensures that DML statements continue to parse string literals the same way Teradata did.

Note

When the FORMAT matches Snowflake’s default output format for the column type (`'YYYY-MM-DD'` for `DATE`, `'HH:MI:SS'` for `TIME`, `'YYYY-MM-DDBHH:MI:SS'` for `TIMESTAMP`), the FORMAT clause is **silently removed** from the DDL without this FDM, and no conversion functions are added to DML statements. These formats are natively handled by Snowflake. This FDM only appears for non-standard formats that require explicit conversion.

Important

For this transformation to work, the `CREATE TABLE` statement that defines the `FORMAT` clause **must be included** in the conversion input. The FORMAT value and column type are read from the DDL and used when converting DML statements. If the DDL is not included, the tool has no way to know which format applies and the conversion functions will not be added.

#### Conversion function mapping

| Column Type | Conversion Function |
| --- | --- |
| `DATE` | `TO_DATE` |
| `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE` | `TO_TIMESTAMP` |
| `TIME`, `TIME WITH TIME ZONE` | `TO_TIME` |

Expand

Show lessSee more

#### Example Code

##### Input code:

Copy code

```
CREATE TABLE employee (
  id INTEGER,
  hire_date DATE FORMAT 'MM-DD-YYYY'
);

SELECT * FROM employee WHERE hire_date = '03-30-2026';
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE employee (
  id INTEGER,
  hire_date DATE
--                 --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'MM-DD-YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                 FORMAT 'MM-DD-YYYY'
)
;

SELECT
  *
FROM
  employee
WHERE
  hire_date = TO_DATE('03-30-2026', 'MM-DD-YYYY');
```

##### Example with BETWEEN:

Copy code

```
CREATE TABLE event_range (
  id INTEGER,
  event_date DATE FORMAT 'MM-DD-YYYY'
);

SELECT * FROM event_range WHERE event_date BETWEEN '01-01-2026' AND '12-31-2026';
```

Copy code

```
CREATE OR REPLACE TABLE event_range (
  id INTEGER,
  event_date DATE
--                  --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'MM-DD-YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                  FORMAT 'MM-DD-YYYY'
)
;

SELECT
  *
FROM
  event_range
WHERE
  event_date BETWEEN TO_DATE('01-01-2026', 'MM-DD-YYYY') AND TO_DATE('12-31-2026', 'MM-DD-YYYY');
```

##### Example with INSERT VALUES:

Copy code

```
CREATE TABLE target_events (
  event_date DATE FORMAT 'DD/MM/YYYY'
);

INSERT INTO target_events (event_date) VALUES ('30/03/2026');
```

Copy code

```
CREATE OR REPLACE TABLE target_events (
  event_date DATE
--                  --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'DD/MM/YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                  FORMAT 'DD/MM/YYYY'
)
;

INSERT INTO target_events (event_date)
VALUES (TO_DATE('30/03/2026', 'DD/MM/YYYY'));
```

##### Example with MERGE:

Copy code

```
CREATE TABLE hr_target (
  id INTEGER,
  hire_date DATE FORMAT 'MM/DD/YYYY'
);

CREATE TABLE hr_source (
  id INTEGER
);

MERGE INTO hr_target AS t
USING hr_source AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET hire_date = '03/30/2026'
WHEN NOT MATCHED THEN INSERT (id, hire_date) VALUES (s.id, '03/30/2026');
```

Copy code

```
CREATE OR REPLACE TABLE hr_target (
  id INTEGER,
  hire_date DATE
--                 --** SSC-FDM-TD0040 - COLUMN-LEVEL FORMAT CLAUSE 'MM/DD/YYYY' IS NOT SUPPORTED IN SNOWFLAKE. CONVERSION FUNCTIONS ARE USED IN DML STATEMENTS AS A WORKAROUND. **
--                 FORMAT 'MM/DD/YYYY'
)
;

CREATE OR REPLACE TABLE hr_source (
  id INTEGER
)
;

MERGE INTO hr_target AS t USING hr_source AS s ON t.id = s.id
WHEN MATCHED THEN
  UPDATE SET
    hire_date = TO_DATE('03/30/2026', 'MM/DD/YYYY')
WHEN NOT MATCHED THEN
  INSERT(id, hire_date)
  VALUES (s.id, TO_DATE('03/30/2026', 'MM/DD/YYYY'));
```

#### Best Practices

- Always include the `CREATE TABLE` statements that define `FORMAT` clauses in the conversion input. Without them, the correct format for DML conversion cannot be determined.
- After conversion, verify that the converted code behaves correctly when these formats are present. In particular, check that the format string in the generated `TO_DATE` / `TO_TIMESTAMP` / `TO_TIME` calls matches the original Teradata FORMAT.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0041

Column-level display-only FORMAT clause is not supported in Snowflake. No action needed.

### Description

Teradata supports a display-only `FORMAT 'X(n)'` clause on character-type columns (`VARCHAR`, `CHAR`, `CLOB`, `STRING`). This format controls only the display width of the column and has no effect on data storage or query behavior. Snowflake does not support this clause, so it is commented out.

Because the `X(n)` format is purely cosmetic, **no conversion functions are added to DML statements** and no manual intervention is required. This FDM is informational only.

#### Example Code

##### Input code:

Copy code

```
CREATE TABLE customer (
  name VARCHAR(100) FORMAT 'X(50)',
  id INTEGER
);

SELECT * FROM customer WHERE name = 'John';
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0039 - COLLATION HANDLED AT QUERY LEVEL FOR THIS TABLE, ANY NEW QUERY OVER THIS TABLE SHOULD APPLY COLLATION APPROPRIATELY **
CREATE OR REPLACE TABLE customer (
  name VARCHAR(100)
--                    --** SSC-FDM-TD0041 - COLUMN-LEVEL DISPLAY-ONLY FORMAT CLAUSE 'X(50)' IS NOT SUPPORTED IN SNOWFLAKE. NO ACTION NEEDED. **
--                    FORMAT 'X(50)'
                                   ,
  id INTEGER
)
;

SELECT
  *
FROM
  customer
WHERE
  UPPER(RTRIM(name)) = UPPER(RTRIM('John'));
```

Note

The `UPPER(RTRIM(...))` wrapping on the WHERE clause is due to the collation handling for `NOT CASESPECIFIC` columns ([SSC-FDM-TD0039](#ssc-fdm-td0039)), not the FORMAT clause.

#### Best Practices

- No action is required for this FDM. The `X(n)` display format has no functional impact in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0042

SIGNAL condition information items other than MESSAGE\_TEXT are not supported in Snowflake. RAISE is used as a workaround.

### Description

In Teradata, the `SIGNAL` statement can include a `SET` clause with multiple condition information items such as `MESSAGE_TEXT`, `CLASS_ORIGIN`, `SUBCLASS_ORIGIN`, `RETURNED_SQLSTATE`, and others. These items provide additional context when raising an error condition.

Snowflake’s `RAISE` statement only supports a single message through the `EXCEPTION` declaration. The `MESSAGE_TEXT` value is preserved and used to declare a Snowflake exception, but any other condition information items (e.g., `CLASS_ORIGIN`, `SUBCLASS_ORIGIN`) are dropped because Snowflake has no equivalent mechanism.

This FDM is attached to the generated `RAISE` statement whenever unsupported condition information items are present in the original `SIGNAL` statement.

#### Example Code

##### Input code:

Copy code

```
REPLACE PROCEDURE SignalSqlstateExtra(testValue INTEGER)
BEGIN
  IF (testValue > 5) THEN
    SIGNAL SQLSTATE VALUE '75001' SET MESSAGE_TEXT = 'Balance is too low', CLASS_ORIGIN = 'SP';
  ELSE
    INSERT INTO exampleTable VALUES ('testValue', testValue);
  END IF;
END;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE SignalSqlstateExtra (TESTVALUE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SIGNAL_EXCEPTION_75001 EXCEPTION (-20001, 'Balance is too low');
  BEGIN
    IF (:testValue > 5) THEN
      --** SSC-FDM-TD0042 - SIGNAL CONDITION INFORMATION ITEMS OTHER THAN MESSAGE_TEXT ARE NOT SUPPORTED IN SNOWFLAKE. RAISE IS USED AS A WORKAROUND. **
      RAISE SIGNAL_EXCEPTION_75001;
    ELSE
      INSERT INTO exampleTable
      VALUES ('testValue', :testValue);
    END IF;
  END;
$$;
```

Note

When all condition information items in the `SET` clause are supported (i.e., only `MESSAGE_TEXT` is present), the `SIGNAL` is converted to `RAISE` without this FDM.

#### Best Practices

- Review each occurrence of this FDM to determine if the dropped condition information items (`CLASS_ORIGIN`, `SUBCLASS_ORIGIN`, etc.) are critical for your error-handling logic. If so, consider adding custom logging to capture that information.
- The `MESSAGE_TEXT` value is always preserved in the Snowflake `EXCEPTION` declaration, so the primary error message remains intact.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0043

Dynamic MESSAGE\_TEXT in SIGNAL is not supported by Snowflake exceptions. CUSTOM\_SQLERRM is used as a workaround.

### Description

In Teradata, `SIGNAL ... SET MESSAGE_TEXT` can accept a variable or expression as the error message, allowing the message to be built dynamically at runtime. For example:

Copy code

```
SET errorText = 'The given value ' || testValue || ' is greater than 5';
SIGNAL SQLSTATE VALUE '75001' SET MESSAGE_TEXT = errorText;
```

In Snowflake Scripting, the `EXCEPTION` declaration requires a compile-time literal for the message. There is no way to dynamically set the exception message at raise time using the `RAISE` statement.

As a workaround:

1. The exception is declared with a static fallback message (e.g., `'Condition 75001 signaled'`).
2. The dynamic value is assigned to a `CUSTOM_SQLERRM` variable before the `RAISE`.

The `CUSTOM_SQLERRM` variable holds the intended dynamic message, but when the exception propagates, Snowflake reports the static message from the `EXCEPTION` declaration — not the dynamic one. Exception handlers that need the dynamic message must read `CUSTOM_SQLERRM` explicitly.

#### Example Code

##### Input code:

Copy code

```
REPLACE PROCEDURE SignalSqlstateDynamic(testValue INTEGER)
BEGIN
  IF (testValue > 5) THEN
    SET errorText = 'The given value ' || testValue || ' is greater than 5';
    SIGNAL SQLSTATE VALUE '75001' SET MESSAGE_TEXT = errorText;
  ELSE
    INSERT INTO exampleTable VALUES ('testValue', testValue);
  END IF;
END;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE SignalSqlstateDynamic (TESTVALUE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    CUSTOM_SQLERRM VARCHAR;
    SIGNAL_EXCEPTION_75001 EXCEPTION (-20001, 'Condition 75001 signaled');
  BEGIN
    IF (:testValue > 5) THEN
      errorText := 'The given value ' || testValue || ' is greater than 5';
      CUSTOM_SQLERRM := errorText;
      --** SSC-FDM-TD0043 - DYNAMIC MESSAGE_TEXT IN SIGNAL IS NOT SUPPORTED BY SNOWFLAKE EXCEPTIONS. CUSTOM_SQLERRM IS USED AS A WORKAROUND. **
      RAISE SIGNAL_EXCEPTION_75001;
    ELSE
      INSERT INTO exampleTable
      VALUES ('testValue', :testValue);
    END IF;
  END;
$$;
```

#### Best Practices

- In exception handlers, read `CUSTOM_SQLERRM` to retrieve the dynamic error message instead of relying on the exception’s static message.
- If the dynamic message is only used for logging purposes, consider moving the logging statement before the `RAISE` so it captures the dynamic value directly.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0044

PREPARE with USING variables bound at EXECUTE IMMEDIATE time instead of OPEN CURSOR time.

### Description

In Teradata, the `PREPARE ... FROM query` statement stages a SQL query for execution, and the `OPEN cursor USING var1, var2` statement binds variable values **at OPEN time**, allowing the cursor to use the current values of those variables when the cursor is opened.

In Snowflake, `PREPARE S1 FROM query` is transformed into `EXECUTE IMMEDIATE query USING (var1, var2)`, which binds the variable values **at EXECUTE IMMEDIATE time** (when the PREPARE is converted). The cursor is then fixed at the `LET CURSOR FOR RESULTSET` declaration. This means that:

- Variable values are captured earlier in the execution flow (at PREPARE/EXECUTE IMMEDIATE time, not OPEN time)
- Reassigning the resultset variable or re-executing PREPARE in a loop will **not** update the cursor

This functional difference marker indicates that the binding timing has changed. Review your code to ensure that variables contain the correct values at PREPARE time (EXECUTE IMMEDIATE time in Snowflake).

#### Example Code

##### Input Code:

Copy code

```
REPLACE PROCEDURE fetch_simple_cursor_placeholder(OUT procedure_result INTEGER)
BEGIN
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = ?';
    DECLARE column_value INTEGER DEFAULT 0;
    DECLARE intermediate_result INTEGER DEFAULT 0;

    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    SET column_value = 1;
    OPEN C1 USING column_value;
    FETCH C1 INTO intermediate_result;
    CLOSE C1;
END;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE fetch_simple_cursor_placeholder (PROCEDURE_RESULT OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = ?';
    column_value INTEGER DEFAULT 0;
    intermediate_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
    prepareQuery_aux_sql := SQL_string_sel;
    --** SSC-FDM-TD0044 - USING VARIABLES BOUND AT EXECUTE IMMEDIATE TIME INSTEAD OF OPEN CURSOR TIME. CURSOR IS FIXED AT LET CURSOR FOR RESULTSET DECLARATION; REASSIGNING THE RESULTSET VARIABLE OR RE-EXECUTING PREPARE IN A LOOP WILL NOT UPDATE THE CURSOR. **
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql USING (column_value)
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    column_value := 1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      intermediate_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;
```

**Note:** In the generated code, `column_value` is bound when `EXECUTE IMMEDIATE` runs (where it still equals 0), not when `OPEN CURSOR_S1_INSTANCE_V0` executes (after it’s set to 1). In Teradata, the binding happens at OPEN time, so the cursor would use the value 1.

#### Best Practices

- **Review variable assignment order**: Ensure variables used in USING clauses have the correct values **before** the PREPARE statement is executed (which becomes EXECUTE IMMEDIATE in Snowflake).
- **Move assignments earlier**: If variables are assigned after PREPARE but before OPEN in Teradata, move those assignments to **before** the PREPARE statement.
- **Test cursor behavior**: Verify that cursors return the expected result sets, especially in loops or when variable values change between PREPARE and OPEN.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0045

ECHO was transformed to SYSTEM$LOG\_INFO.

#### Description

Teradata `ECHO` statements inside procedure or macro bodies are translated to Snowflake `SYSTEM$LOG_INFO` calls. There are two functional differences: the message is written to an event table instead of the BTEQ console, so an event table must be configured for the account; and any BTEQ command carried in the `ECHO` text is recorded as a plain message rather than executed.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
REPLACE MACRO LogLoadStatus ()
AS (
  ECHO 'Load started';
  INSERT INTO load_audit VALUES (CURRENT_TIMESTAMP);
);
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE LogLoadStatus ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-TD0045 - SYSTEM$LOG_INFO REQUIRES AN EVENT TABLE TO BE CONFIGURED IN THE SNOWFLAKE ACCOUNT, BTEQ COMMANDS EXECUTED THROUGH ECHO WILL BE LOGGED AS MESSAGES INSTEAD. **
    SYSTEM$LOG_INFO('Load started');
    INSERT INTO load_audit
    VALUES (CURRENT_TIMESTAMP);
  END;
$$;
```

#### Best Practices

- **Configure an event table** for the account and monitor it, otherwise the converted messages are not persisted anywhere.
- **Re-implement executed commands**: if the original `ECHO` emitted a BTEQ command for execution, replace it with an explicit orchestration step — `SYSTEM$LOG_INFO` only records the text.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0046

CAST-level date FORMAT clause is not supported in Snowflake. If the column is used as a string, an explicit TO\_VARCHAR with the format may be needed.

### Description

In Teradata, the `FORMAT` clause on a `CAST` expression controls how a date or timestamp value is displayed when implicitly converted to a string. For example:

Copy code

```
CAST(capture_date AS DATE FORMAT 'YYYY/MM/DD')
```

Snowflake does not support inline `FORMAT` clauses on `CAST`. When the format is verified to contain only recognized datetime elements (e.g., `YYYY`, `MM`, `DD`), the `FORMAT` clause is removed and this FDM is emitted instead of an EWI, because the date conversion itself is functionally correct — the only difference is the display format.

If the result is later used in a string context (concatenation, assignment to `VARCHAR`, etc.), you may need to wrap the expression with `TO_VARCHAR` and the corresponding Snowflake format string.

Note

When the format contains unsupported or unrecognized elements, or when the operand type cannot be resolved as a datetime type, [SSC-EWI-TD0025](../conversion-issues/teradataEWI#ssc-ewi-td0025) is emitted instead.

#### Example Code

##### Input Code:

Copy code

```
CREATE TABLE event_log (
  capture_date TIMESTAMP(0)
);

SELECT
  CAST(capture_date AS DATE FORMAT 'YYYY/MM/DD') AS rpt_date
FROM event_log;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE event_log (
  capture_date TIMESTAMP(0)
)
;

SELECT
  TO_DATE(capture_date) /*** SSC-FDM-TD0046 - CAST-LEVEL DATE FORMAT CLAUSE YYYY/MM/DD IS NOT SUPPORTED IN SNOWFLAKE. IF THE COLUMN IS USED AS A STRING, AN EXPLICIT TO_VARCHAR WITH THE FORMAT MAY BE NEEDED. ***/ AS rpt_date
FROM
  event_log;
```

When the result is wrapped in a `CAST ... AS VARCHAR`, the format is applied inside a `TO_VARCHAR` call:

##### Input Code:

Copy code

```
CREATE TABLE event_log (
  capture_date TIMESTAMP(0)
);

SELECT
  CAST(CAST(capture_date AS DATE FORMAT 'YYYY/MM/DD') AS VARCHAR(20)) AS rpt_str
FROM event_log;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE TABLE event_log (
  capture_date TIMESTAMP(0)
)
;

SELECT
  LEFT(TO_VARCHAR(TO_DATE(capture_date), 'YYYY/MM/DD'), 20) AS rpt_str
FROM
  event_log;
```

#### Best Practices

- If the converted column is only used as a date (comparisons, filters, date arithmetic), the conversion is functionally equivalent and no action is needed.
- If the column is used in a string context (e.g., concatenation, display, assignment to `VARCHAR`), wrap the expression with `TO_VARCHAR` and the appropriate Snowflake format string. For example: `TO_VARCHAR(TO_DATE(capture_date), 'YYYY/MM/DD')`.
- Review the Snowflake [TO\_VARCHAR](/sql-reference/functions/to_varchar) documentation for supported format models.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0047

This macro references a Teradata built-in view that has no Snowflake equivalent.

### Description

Teradata provides a set of system views under the `DBC` database (e.g., `DBC.Software_Event_LogV`, `DBC.EventLog`) that expose infrastructure-level metrics such as disk usage, software events, and resource monitoring. These views are specific to the Teradata platform and have no functional equivalent in Snowflake.

When a `CREATE MACRO` (or `REPLACE MACRO`) whose body references one of these unsupported DBC views is encountered, the entire macro is commented out and this FDM marker is emitted. The marker identifies the specific unsupported view that triggered the action.

Note that macros referencing *supported* DBC views (such as `DBC.Columns` or `DBC.Tables`, which map to `INFORMATION_SCHEMA` equivalents) are converted normally and do not trigger this marker.

#### Example Code

##### Input Code:

Copy code

```
CREATE MACRO PackDiskSummary AS
(
  SELECT TheDate, TheTime, VProc, Event_Tag
  FROM DBC.Software_Event_LogV;
);
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TD0047 - THIS MACRO REFERENCES TERADATA BUILT-IN VIEW DBC.Software_Event_LogV WHICH MONITORS TERADATA-SPECIFIC INFRASTRUCTURE. DUE TO PLATFORM DIFFERENCES, THIS FUNCTIONALITY CANNOT BE EMULATED IN SNOWFLAKE. **
--CREATE MACRO PackDiskSummary
--AS
--(
--  SELECT
--    TheDate,
--    TheTime,
--    VProc,
--    Event_Tag
--  FROM
--    DBC.Software_Event_LogV;
--)
```

When a macro contains a mix of supported and unsupported DBC references, the entire macro is still commented out because partial conversion would produce a broken procedure.

##### Input Code (mixed references):

Copy code

```
CREATE MACRO MixedMacro AS
(
  SELECT tablename FROM dbc.tables;
  SELECT theDate FROM DBC.EventLog;
);
```

##### Generated Code:

Copy code

```
----** SSC-FDM-TD0047 - THIS MACRO REFERENCES TERADATA BUILT-IN VIEW DBC.EventLog WHICH MONITORS TERADATA-SPECIFIC INFRASTRUCTURE. DUE TO PLATFORM DIFFERENCES, THIS FUNCTIONALITY CANNOT BE EMULATED IN SNOWFLAKE. **
--CREATE MACRO MixedMacro
--AS
--(
--  SELECT
--    tablename
--  FROM
--    dbc.tables;
--  SELECT
--    theDate
--  FROM
--    DBC.EventLog;
--)
```

#### Best Practices

- Review the commented-out macro to determine whether the underlying monitoring or diagnostic need can be addressed through Snowflake-native features such as `INFORMATION_SCHEMA`, `ACCOUNT_USAGE`, or `QUERY_HISTORY()`.
- If only part of the macro logic depends on the unsupported view, consider splitting it into separate procedures — one for the convertible queries and one for the Teradata-specific monitoring logic.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0048

`.RUN FILE` converted to `EXECUTE IMMEDIATE FROM`.

### Description

The BTEQ [`.RUN FILE = <path>`](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018) command sources another BTEQ script inline. It is converted to Snowflake’s [`EXECUTE IMMEDIATE FROM @<stage>/<file>`](/sql-reference/sql/execute-immediate-from), which loads and runs a SQL file from a Snowflake stage in the same session. The conversion also emits a `CREATE STAGE IF NOT EXISTS sc_run_stage` and a `PUT` for the referenced file at the top of the converted script, so that the file is uploaded to the stage before the parent script tries to execute it.

The marker is informational — it tells the reader that the original `.RUN FILE` line was rewritten, not commented out. The referenced child script is also converted in the same migration run; the `EXECUTE IMMEDIATE FROM` invocation points at the converted output (e.g. `child.bteq` → `child_BTEQ.sql`).

#### Code Example

##### Input Code:

Copy code

```
DATABASE mydb;
.RUN FILE = child.bteq
SELECT * FROM mytable;
```

##### Generated Code:

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

#### Best Practices

- **Run the converted scripts through the Snowflake CLI**: the prelude `PUT file://… @sc_run_stage` is a client-side directive that only the [Snowflake CLI](/developer-guide/snowflake-cli/index) (`snow sql -f script.sql`) or SnowSQL can execute. The Snowflake web UI cannot execute `PUT`.
- **Keep referenced files in the input tree**: The `.RUN FILE` target is resolved by basename against the migration input tree. If the file is not present at conversion time, the conversion falls back to [SSC-EWI-TD0103](../conversion-issues/teradataEWI#ssc-ewi-td0103).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0049

Logon credentials not required when running through Snowflake CLI.

### Description

Some BTEQ scripts use `.RUN FILE = $LOGON_ID` (or a similar `$LOGON…` / `${…LOGIN…}` variable) to source a credential file before connecting to the Teradata server. Snowflake handles authentication outside of SQL: the [Snowflake CLI](/developer-guide/snowflake-cli/index) reads the connection profile from `snow connection` (typically `~/.snowflake/connections.toml`) before any script runs, so logging in inside the script is unnecessary. This pattern is detected, the `.RUN` line is dropped from the executable output, and this marker is attached so the user can confirm the credentials are configured at the CLI level.

The marker recognises both the `&NAME` Teradata-style and `${NAME}` / `$NAME` bash-style placeholders when the variable name contains `LOGON` or `LOGIN`.

#### Code Example

##### Input Code:

Copy code

```
.RUN FILE = $LOGON_ID
```

##### Generated Code:

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

#### Best Practices

- **Configure the Snowflake connection once at the CLI level**: define the target connection with `snow connection add` (or edit `~/.snowflake/connections.toml`) and reference it via `snow sql --connection <name> -f script.sql`. Detailed instructions are in the [Snowflake CLI configuration](/developer-guide/snowflake-cli/connecting/configure-connections) docs.
- **Remove the original logon-credentials file from migration**: the file referenced by `.RUN FILE = $LOGON_ID` typically contains `.LOGON host/user,password` and has no Snowflake equivalent. It does not need to be migrated.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0050

`.RUN` chaining detected.

### Description

A `.RUN FILE` target is itself a script that issues one or more `.RUN FILE` commands of its own. In BTEQ this produces a flat **chain** of execution: the parent runs the child to completion, then continues. Snowflake’s [`EXECUTE IMMEDIATE FROM`](/sql-reference/sql/execute-immediate-from) instead **nests** the child’s execution inside the parent’s session and inherits the parent’s transaction context. The end state of the data is the same in both models, but error propagation, transaction scope, and side effects can differ when nesting replaces chaining. This marker is emitted on the parent so the reviewer audits the chain and confirms the nested behaviour is acceptable.

The detection is performed at the lineage phase: any script in the migration input that contains `.RUN FILE` is recorded; when another script’s `.RUN FILE` resolves to one of those, the parent’s `.RUN` is flagged.

#### Code Example

##### Input Code:

Copy code

```
.RUN FILE = middle_chain.bteq
```

`middle_chain.bteq` itself contains:

Copy code

```
.RUN FILE = leaf_chain.bteq
```

##### Generated Code:

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

#### Best Practices

- **Audit transaction and error semantics**: in BTEQ the child’s `.LOGOFF` / non-zero error code propagates to the parent linearly; under nested `EXECUTE IMMEDIATE FROM`, the child runs inside the parent’s anonymous block and any uncaught exception bubbles up through the parent’s exception handler instead. Adjust error handling at the parent level if your workflow depends on per-child exit codes.
- **Flatten the chain when possible**: if the chain exists only to share boilerplate (e.g. `.LOGON` followed by `DATABASE …`), inline the shared statements at the top of the leaf script and skip the intermediate `.RUN`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0051

The cedilla pair `çç` was interpreted as the SQL concatenation operator `||`. If `çç` was intended as part of an identifier name, double-quote the identifier in the source.

### Description

In Teradata, the cedilla pair `çç` is an alternative spelling of the string concatenation operator (synonym for `||` and `!!`). It typically appears in scripts that originated from EBCDIC-encoded sources, where the `!!` symbol was transcoded as `çç` during character-set conversion.

When `çç` is surrounded by whitespace (for example, `C1 çç C2`), the operator is unambiguous and it is converted to `||` silently with no marker. However, the lowercase `ç` is also a valid identifier character in Teradata. When `çç` appears flush against identifier characters with no surrounding whitespace (for example, `C1ççC2`), the lexer must decide whether the cedilla pair is part of an identifier name or the concatenation operator. The `çç` is split out and treated as the concatenation operator, then this FDM is emitted at the split site so the user can review the interpretation.

The marker is informational only. The generated SQL is functionally equivalent to the original Teradata semantics in the typical case where `çç` was indeed an EBCDIC-transcoded concatenation operator. The marker serves as an audit trail in the rare case where the original author actually intended the cedilla pair to be part of an identifier name.

#### Example Code

##### Input Code:

Copy code

```
SELECT C1ççC2 FROM TABLE1;
```

##### Generated Code:

Copy code

```
SELECT
  C1 || C2 /*** SSC-FDM-TD0051 - THE CEDILLA PAIR 'çç' WAS INTERPRETED AS THE SQL CONCATENATION OPERATOR '||'. IF 'çç' WAS INTENDED AS PART OF AN IDENTIFIER NAME, DOUBLE-QUOTE THE IDENTIFIER IN THE SOURCE. ***/
FROM
  TABLE1;
```

#### Best Practices

- The marker is informational. In the overwhelming majority of cases the `çç` pair is an EBCDIC-transcoded concatenation operator and the converted code is correct as generated; the marker can be removed after a quick review.
- If you find a case where `çç` was actually intended as part of an identifier name, fix it in the **source** by double-quoting the identifier (for example, change `C1ççC2` to `"C1ççC2"`) and re-run the conversion. With the identifier explicitly quoted, the lexer will not split it and no FDM will be emitted.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0052

`DELETE` without `WHERE` clause replaced with `TRUNCATE TABLE` for performance.

### Description

Inside a Teradata macro, `DELETE FROM <table>;` without a `WHERE` clause removes every row of the target table but is still a fully-logged DML operation. Snowflake offers a much faster equivalent for the same intent: [`TRUNCATE TABLE`](/sql-reference/sql/truncate-table), which deletes all rows in a single metadata operation. When a Teradata macro is translated into a Snowflake stored procedure, unconditional `DELETE` statements are rewritten as `TRUNCATE TABLE` and this marker is attached so the user can audit the change.

The optimization is **only applied when the macro contains fewer than three DML statements**. Macros with three or more DML statements are wrapped in an explicit `BEGIN TRANSACTION … COMMIT` block so the whole body can be rolled back on failure; `TRUNCATE TABLE` cannot be rolled back the same way as `DELETE`, so the original `DELETE` is preserved in those multi-DML scenarios to keep transactional semantics intact.

#### Example Code

##### Input Code:

Copy code

```
REPLACE MACRO BRG_SERVICE_DIAG_BUILD
AS
(
DELETE FROM BRG_SERVICE_DIAG;

INSERT INTO BRG_SERVICE_DIAG
SELECT PRIMARY_DIAG_CODE_DIM_CK, 1 SEQ, CLAIM_NBR, CLAIM_TRANS_CK,
       MEMBER_ELIGIBILITY_CK, PRIMARY_DIAG_CODE, 0 DIAG_COUNT, PLAN_DIM_CK
FROM FT_CLAIM_TRANSACTION A
WHERE PRIMARY_DIAG_CODE_DIM_CK > 0;
);
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE BRG_SERVICE_DIAG_BUILD ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-TD0052 - DELETE WITHOUT WHERE CLAUSE REPLACED WITH TRUNCATE TABLE FOR PERFORMANCE. ORIGINAL: DELETE FROM BRG_SERVICE_DIAG **
    TRUNCATE TABLE BRG_SERVICE_DIAG;
    INSERT INTO BRG_SERVICE_DIAG SELECT
      PRIMARY_DIAG_CODE_DIM_CK,
      1 SEQ,
      CLAIM_NBR,
      CLAIM_TRANS_CK,
      MEMBER_ELIGIBILITY_CK,
      PRIMARY_DIAG_CODE,
      0 DIAG_COUNT,
      PLAN_DIM_CK
    FROM
      FT_CLAIM_TRANSACTION A
    WHERE
      PRIMARY_DIAG_CODE_DIM_CK > 0;
  END;
$$;
```

When the macro contains three or more DML statements the optimization is **not** applied. The original `DELETE` is preserved so the macro body can be wrapped in `BEGIN TRANSACTION … COMMIT` and rolled back on failure:

Copy code

```
REPLACE MACRO MULTI_DML_MACRO
AS
(
DELETE FROM STAGING_TABLE;

INSERT INTO STAGING_TABLE
SELECT * FROM SOURCE_TABLE WHERE STATUS = 'ACTIVE';

UPDATE TARGET_TABLE
SET LAST_UPDATE = CURRENT_TIMESTAMP
WHERE ID IN (SELECT ID FROM STAGING_TABLE);
);
```

Copy code

```
CREATE OR REPLACE PROCEDURE MULTI_DML_MACRO ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    BEGIN TRANSACTION;
    DELETE FROM
      STAGING_TABLE;
    INSERT INTO STAGING_TABLE SELECT
      *
    FROM
      SOURCE_TABLE
    WHERE
      UPPER(RTRIM(STATUS)) = UPPER(RTRIM('ACTIVE'));
    UPDATE TARGET_TABLE
      SET
        LAST_UPDATE = CURRENT_TIMESTAMP()
      WHERE
        ID IN (
          SELECT
            ID
          FROM
            STAGING_TABLE
        );
    COMMIT;
  EXCEPTION
    WHEN OTHER THEN
      ROLLBACK;
      RAISE;
  END;
$$;
```

#### Best Practices

- **Confirm the change is acceptable for your workflow**: `TRUNCATE TABLE` is a metadata-only operation that bypasses `DELETE` triggers, does not honour row-level access policies in the same way, and cannot be rolled back as part of a transaction. If any of those properties matter for the original macro, replace the `TRUNCATE TABLE` with `DELETE FROM <table>;` and remove this marker.
- **Verify the resolved table name**: The optimization is applied only when the table reference resolves to a simple table name. If your macro deletes from a table expression that does not match this pattern, the original `DELETE` is preserved unchanged.
- **Multi-DML macros are unchanged on purpose**: when the macro has three or more DML statements, the procedure body is wrapped in `BEGIN TRANSACTION … COMMIT` and the original `DELETE` is kept so a failure later in the body can roll back every change atomically. If you want the `TRUNCATE` optimization in those cases, split the macro so the unconditional `DELETE` lives in its own (smaller) macro.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0053

UPPERCASE column attribute is not supported in Snowflake.

### Description

The Teradata `UPPERCASE` column attribute indicates that character values are automatically folded to uppercase when stored. Snowflake has no equivalent column-level attribute.

When SnowConvert encounters a column defined with `UPPERCASE`, it comments out the attribute in the DDL and emits this FDM marker. For DML statements (`INSERT`, `UPDATE`, `MERGE`) that write to such a column, SnowConvert wraps the corresponding values in `UPPER()` to preserve the case-folding semantics at write time.

#### Example Code

##### Input Code:

Copy code

```
CREATE TABLE employees (
    name VARCHAR(100) UPPERCASE
);
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0039 - COLLATION HANDLED AT QUERY LEVEL FOR THIS TABLE, ANY NEW QUERY OVER THIS TABLE SHOULD APPLY COLLATION APPROPRIATELY **
CREATE OR REPLACE TABLE employees (
  name VARCHAR(100)
--                    --** SSC-FDM-TD0053 - UPPERCASE COLUMN ATTRIBUTE IS NOT SUPPORTED IN SNOWFLAKE. UPPER() IN DML STATEMENTS IS USED AS A WORKAROUND. **
--                    UPPERCASE
)
;
```

The following example shows that values inserted into an `UPPERCASE` column are automatically wrapped in `UPPER()`:

##### Input Code (DML):

Copy code

```
CREATE TABLE employees (
    name VARCHAR(100) UPPERCASE,
    department VARCHAR(50)
);

INSERT INTO employees (name, department) VALUES ('John', 'Sales');
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0039 - COLLATION HANDLED AT QUERY LEVEL FOR THIS TABLE, ANY NEW QUERY OVER THIS TABLE SHOULD APPLY COLLATION APPROPRIATELY **
CREATE OR REPLACE TABLE employees (
  name VARCHAR(100)
--                    --** SSC-FDM-TD0053 - UPPERCASE COLUMN ATTRIBUTE IS NOT SUPPORTED IN SNOWFLAKE. UPPER() IN DML STATEMENTS IS USED AS A WORKAROUND. **
--                    UPPERCASE
                                ,
  department VARCHAR(50)
)
;

INSERT INTO employees (name, department)
VALUES (UPPER('John'), 'Sales');
```

#### Best Practices

- Review each `UPPERCASE` column and confirm that `UPPER()` wrapping in `INSERT`, `UPDATE`, and `MERGE` statements is sufficient — external data-loading processes (ETL, COPY INTO) must also apply `UPPER()` independently.
- For query-time enforcement, consider adding a Snowflake collation (`COLLATE 'upper'`) to the column definition, which handles case folding transparently for comparisons.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0054

HELP TABLE is not supported in Snowflake.

### Description

The Teradata `HELP TABLE` statement returns column-level metadata (data type, nullability, default values) for a specified table. Snowflake does not support this statement.

SnowConvert replaces `HELP TABLE` with Snowflake’s `DESCRIBE TABLE`, which provides equivalent schema information, and emits this FDM marker to indicate the substitution.

#### Example Code

##### Input Code:

Copy code

```
HELP TABLE db1.t1;
```

##### Generated Code:

Copy code

```
--** SSC-FDM-TD0054 - HELP TABLE IS NOT SUPPORTED IN SNOWFLAKE. DESCRIBE TABLE IS USED AS A WORKAROUND. **
DESCRIBE TABLE db1.t1;
```

#### Best Practices

- Review any application or script logic that parses `HELP TABLE` output — the column ordering and naming in `DESCRIBE TABLE` results may differ from Teradata’s `HELP TABLE` output.
- If programmatic schema inspection is needed, consider querying `INFORMATION_SCHEMA.COLUMNS` instead, which provides richer metadata and is more portable.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0055

Transaction-scoped QUERY\_BAND converted as session-scoped QUERY\_TAG.

### Description

The Teradata `SET QUERY_BAND ... FOR TRANSACTION` statement tags the current transaction with metadata, with the tag automatically cleared when the transaction ends. Snowflake has no transaction-scoped query tag; the nearest equivalent is `ALTER SESSION SET QUERY_TAG`, which applies for the duration of the session.

When SnowConvert encounters `SET QUERY_BAND ... FOR TRANSACTION` inside a stored procedure, it converts it to `ALTER SESSION SET QUERY_TAG` and emits this FDM marker to highlight the scope difference. The `FOR SESSION` variant is converted silently without a marker, since the session-level scope matches Snowflake’s behavior.

#### Example Code

##### Input Code:

Copy code

```
REPLACE PROCEDURE procedure1 ()
BEGIN
  SET QUERY_BAND = 'BLOCKCOMPRESSION=YES;' FOR TRANSACTION;
END;
```

##### Generated Code:

Copy code

```
CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-TD0055 - TRANSACTION-SCOPED QUERY BAND CONVERTED AS SESSION-SCOPED QUERY_TAG. SNOWFLAKE HAS NO TRANSACTION-SCOPED QUERY TAG. **
    ALTER SESSION SET QUERY_TAG = 'BLOCKCOMPRESSION=YES;';
  END;
$$;
```

#### Best Practices

- Because `ALTER SESSION SET QUERY_TAG` persists for the entire session, consider resetting it (e.g., `ALTER SESSION SET QUERY_TAG = ''`) at the end of the procedure body if isolation between procedure calls is important.
- If multiple concurrent sessions run the same procedure, session-level tagging will not distinguish individual transactions the way `FOR TRANSACTION` did in Teradata.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0056

Redundant pre-export cleanup command commented out.

### Description

A common BTEQ pattern before an `.EXPORT FILE` is to run `.OS rm /path/to/file` (or `.OS rm -f /path/to/file`) to delete any existing output file so the export starts fresh. In Snowflake this is unnecessary: `COPY INTO @stage/file ... OVERWRITE = TRUE` already overwrites the destination unconditionally.

When a `.OS rm` command that is immediately adjacent to an `.EXPORT FILE` pointing at the same path is detected, the `.OS rm` line is commented out and this FDM marker is emitted. If the paths differ, or if a statement intervenes between the `.OS rm` and the `.EXPORT`, the original EWI is preserved and no FDM is applied.

#### Example Code

##### Input Code:

Copy code

```
.OS rm /tmp/output.txt
.EXPORT FILE = /tmp/output.txt
SELECT * FROM t1;
.EXPORT RESET
```

##### Generated Code:

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    --** SSC-FDM-TD0056 - REDUNDANT PRE-EXPORT CLEANUP COMMAND COMMENTED OUT. SNOWFLAKE COPY INTO WITH OVERWRITE = TRUE ALREADY OVERWRITES THE DESTINATION FILE. **
--    .OS rm /tmp/output.txt
    COPY INTO @sc_export_stage/output.txt
    FROM
    (
      SELECT * FROM t1
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
GET @sc_export_stage/output.txt file://./;
```

#### Best Practices

- The marker is informational — the generated `COPY INTO ... OVERWRITE = TRUE` is functionally equivalent to the delete-then-export pattern and no manual action is required.
- If the `.OS rm` targeted a different path than the export (e.g., cleaning up an older file), it will be preserved with an EWI and must be handled manually, typically by replacing it with a Snowflake stage file removal operation.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0057

Semantic information for the period value could not be found.

#### Description

Translating a period predicate requires the period element type, which determines both the end-value sentinel and the granularity used in the generated expression. When the declaration of the period value cannot be resolved, a `PERIOD(DAY)` value is assumed and this marker is emitted, because a `TIME` or `TIMESTAMP` based period would need a different sentinel.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT employee_id
FROM employment_history
WHERE END(active_period) IS UNTIL_CHANGED;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
employee_id FROM
employment_history
WHERE
PERIOD_END(active_period) = DATE '9999-12-31' /*** SSC-FDM-TD0057 - SEMANTIC INFORMATION FOR THE PERIOD VALUE COULD NOT BE FOUND, PERIOD(DAY) ASSUMED ***/;
```

#### Best Practices

- **Add the declaration to the input**: include the table or parameter definition that declares the period value so its element type can be resolved.
- **Check the sentinel**: when the source period is based on `TIME` or `TIMESTAMP`, verify the generated end value and granularity manually.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0058

Derived period column removed, references rewritten to PERIOD\_CONSTRUCT.

#### Description

Snowflake has no equivalent for a plain Teradata derived period declaration, `PERIOD FOR name(begin_column, end_column)`. The derived column is removed from the table definition and every reference to it is rewritten to `PERIOD_CONSTRUCT(begin_column, end_column)`, so the value is still available in queries but is no longer a column of the table.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
CREATE TABLE employment (
  employee_id INTEGER,
  job_start DATE NOT NULL,
  job_end DATE NOT NULL,
  PERIOD FOR job_duration(job_start, job_end)
);

SELECT job_duration
FROM employment;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-TD0058 - DERIVED PERIOD COLUMN 'job_duration' REMOVED, REFERENCES REWRITTEN TO PERIOD_CONSTRUCT(job_start, job_end) **
CREATE OR REPLACE TABLE employment (
  employee_id INTEGER,
  job_start DATE NOT NULL,
  job_end DATE NOT NULL
)
;

SELECT
PERIOD_CONSTRUCT(job_start, job_end) AS job_duration FROM
employment;
```

#### Best Practices

- **Keep both boundary columns**: the rewrite depends on `begin_column` and `end_column` being present wherever the derived period was referenced.
- **Review metadata consumers**: queries, views, or tools that expected the derived period to be a physical column will no longer find it in the table definition.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0059

Teradata SQL Assistant named parameter found.

#### Description

Teradata SQL Assistant accepts client-side named parameters written as `?name`, whose value is prompted for at execution time. They are converted to Snowflake CLI template variables, `<%name%>`, which means the value must be supplied through the Snowflake CLI when the script runs instead of being requested interactively.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT order_id
FROM monthly_orders
WHERE order_month BETWEEN 202201 AND ?END_DATE_YYYYMM;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  order_id
FROM
  monthly_orders
WHERE
  order_month BETWEEN 202201 AND <%END_DATE_YYYYMM%> /*** SSC-FDM-TD0059 - TERADATA SQL ASSISTANT NAMED PARAMETER. THE VALUE MUST BE SUPPLIED THROUGH THE SNOWFLAKE CLI AT RUN TIME. ***/;
```

#### Best Practices

- **Define every template variable** when executing the script through the Snowflake CLI; an undefined variable is not substituted.
- **Check quoting**: values that are not numeric literals may need quotes around the template variable in the converted statement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0060

Null call clause not applicable to Snowflake SQL UDF.

#### Description

A Teradata SQL UDF can declare `RETURNS NULL ON NULL INPUT` so the body is skipped and NULL returned whenever an argument is NULL. Snowflake SQL UDFs always evaluate the body, so the clause is removed and this marker is attached to the return definition.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
REPLACE FUNCTION calculate_score ()
RETURNS INTEGER VARYING USING FUNCTION calculate_score_impl
SPECIFIC calculate_score
NO SQL
NO EXTERNAL DATA
PARAMETER STYLE SQLTable
RETURNS NULL ON NULL INPUT
DETERMINISTIC
EXTERNAL NAME 'calculate_score.cpp';
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION calculate_score ()
RETURNS INTEGER /*** SSC-FDM-TD0060 - 'RETURNS NULL ON NULL INPUT' IS NOT PRESERVED; SNOWFLAKE SQL UDFS ALWAYS EVALUATE THE BODY EVEN WHEN AN ARGUMENT IS NULL. ***/
VARYING USING FUNCTION calculate_score_impl !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'VaryingClause' NODE ***/!!!
NO EXTERNAL DATA !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ExternalDataAccess' NODE ***/!!!
PARAMETER STYLE SQLTable !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ParameterStyleKeywords' NODE ***/!!!
IMMUTABLE
AS
$$
EXTERNAL NAME 'calculate_score.cpp'
$$;
```

#### Best Practices

- **Guard against NULL in the body**: add explicit NULL checks where evaluating the body with a NULL argument could raise an error or return a different value.
- **Test each nullable argument** individually and in combination after migration.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0061

Snowflake UNPIVOT value-column types could not be verified.

#### Description

Snowflake requires the value columns of an `UNPIVOT` to share a data type. When the datatypes of the participating columns cannot be resolved, that requirement cannot be checked at conversion time, so the clause is preserved with this informational marker: the statement may compile if the source columns turn out to be compatible.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT employee_id, measure_name, measure_value
FROM missing_measure_source
UNPIVOT (measure_value FOR measure_name IN (measure_a, measure_b)) AS u;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  employee_id,
  measure_name,
  measure_value
FROM
  missing_measure_source UNPIVOT (measure_value FOR measure_name IN (measure_a, measure_b) /*** SSC-FDM-TD0061 - THE UNPIVOT VALUE COLUMN TYPES COULD NOT BE RESOLVED, SO THEIR COMPATIBILITY WAS NOT VERIFIED. SNOWFLAKE UNPIVOT REQUIRES VALUE COLUMNS OF THE SAME DATA TYPE. ***/) AS u;
```

#### Best Practices

- **Add the source definition to the migration input** so the value-column datatypes can be resolved and the compatibility check performed.
- **Unify incompatible columns**: if the types differ, cast them to one common type in a derived table before applying `UNPIVOT`. See [SSC-EWI-TD0105](../conversion-issues/teradataEWI#ssc-ewi-td0105) for the case where incompatibility is confirmed.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0100

BTEQ output-formatting setting has no Snowflake equivalent.

### Description

BTEQ has several `.SET` commands that control how query results are rendered for the BTEQ console (page width, header dashes, side titles, etc.). These commands shape the visual layout of REPORT output and have no equivalent in Snowflake — Snowflake’s `COPY INTO @stage` writes a CSV file and lets the consumer format it. The conversion comments out the source line and attaches this marker so you can audit what was removed without losing visibility into the original script.

The runtime variant token is the original `.SET` command name (`(.SET WIDTH)`, `(.SET TITLEDASHES)`, `(.SET TITLES)`, `(.SET SIDETITLES)`, `(.SET RTITLE)`).

#### Code Example

##### Input Code:

Copy code

```
.SET WIDTH 4000
.SET TITLEDASHES OFF
.EXPORT FILE=privileged_status.txt
SELECT TRIM(USERNAME) || '|' || TRIM(DATABASENAME) AS PRIVILEGED_STATUS FROM ACCESS_TYPES;
```

##### Generated Code:

Copy code

```
CREATE TEMPORARY STAGE IF NOT EXISTS sc_export_stage;

EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    --** SSC-FDM-TD0100 - BTEQ OUTPUT-FORMATTING SETTING (.SET WIDTH) HAS NO SNOWFLAKE EQUIVALENT AND IS SAFE TO IGNORE. **
--    .SET WIDTH 4000
    --** SSC-FDM-TD0100 - BTEQ OUTPUT-FORMATTING SETTING (.SET TITLEDASHES) HAS NO SNOWFLAKE EQUIVALENT AND IS SAFE TO IGNORE. **
--    .SET TITLEDASHES OFF
    COPY INTO @sc_export_stage/privileged_status.txt
    FROM
    (
      SELECT TRIM(USERNAME) || '|' || TRIM(DATABASENAME) AS PRIVILEGED_STATUS FROM ACCESS_TYPES
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

#### Best Practices

- The marker is informational — the underlying conversion is unaffected and the BTEQ output-formatting commands can safely be ignored on Snowflake.
- If you need to reproduce the exact BTEQ visual layout (column widths, header dashes), apply post-processing to the downloaded CSV using your preferred tool (`awk`, Python, `csvlook`, etc.).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-TD0101

The Antiselect row-distribution clause was removed.

#### Description

Teradata `Antiselect` accepts row-distribution clauses such as `PARTITION BY`, `HASH BY`, `LOCAL ORDER BY`, and `DIMENSION`. They control how rows are distributed and ordered across AMPs but do not change which columns are projected, so they are removed when the operator is translated to Snowflake `SELECT * EXCLUDE`, and this marker records the removal.

#### Code Example

##### Input Code:

##### Teradata

Copy code

```
SELECT *
FROM Antiselect (
  ON employee_source PARTITION BY department_id
  USING Exclude ('salary')
) AS public_employee_data;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  --** SSC-FDM-TD0101 - ROW-DISTRIBUTION CLAUSE WAS REMOVED BECAUSE IT DOES NOT AFFECT THE PROJECTED COLUMNS. **
  * EXCLUDE(salary)
FROM
  employee_source public_employee_data;
```

#### Best Practices

- **Check ordering assumptions**: confirm that downstream processing does not depend on the physical row distribution or local ordering the removed clause produced.
- **Order explicitly when needed**: add a Snowflake `ORDER BY` only where deterministic result ordering is actually required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
