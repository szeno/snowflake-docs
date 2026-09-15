# SQL Server-Azure Synapse - Built-in functions

Applies to

- SQL Server
- Azure Synapse Analytics

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../general/built-in-functions).

## Aggregate

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| TransactSQL | Snowflake | Notes |
| APPROX\_COUNT\_DISTINCT | APPROX\_COUNT\_DISTINCT |  |
| AVG​ | AVG |  |
| CHECKSUM\_AGG | *\*to be defined* |  |
| COUNT | COUNT |  |
| COUNT\_BIG | *\*to be defined* |  |
| GROUPING | GROUPING |  |
| GROUPING\_ID | GROUPING\_ID |  |
| MAX | MAX |  |
| MIN | MIN |  |
| STDEV | STDDEV, STDEV\_SAMP |  |
| STDEVP | STDDEV\_POP |  |
| SUM | SUM |  |
| VAR | VAR\_SAMP |  |
| VARP | VAR\_POP​ |  |

Expand

Show lessSee more

## Analytic

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| CUME\_DIST | CUME\_DIST |  |
| FIRST\_VALUE | FIRST\_VALUE |  |
| LAG | LAG |  |
| LAST\_VALUE | LAST\_VALUE |  |
| LEAD | LEAD |  |
| PERCENTILE\_CONT | PERCENTILE\_CONT |  |
| PERCENTILE\_DISC | PERCENTILE\_DISC |  |
| PERCENT\_RANK | PERCENT\_RANK |  |

Expand

Show lessSee more

## Collation

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| COLLATIONPROPERTY | *\*to be defined* |  |
| TERTIARY\_WEIGHTS | *\*to be defined* |  |

Expand

Show lessSee more

## Configuration

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| ​@@DBTS | *\*to be defined* |  |
| @@LANGID | *\*to be defined* |  |
| @@LANGUAGE | *\*to be defined* |  |
| @@LOCK\_TIMEOUT | *\*to be defined* |  |
| @@MAX\_CONNECTIONS | *\*to be defined* |  |
| @@MAX\_PRECISION | *\*to be defined* |  |
| @@NESTLEVEL | *\*to be defined* |  |
| @@OPTIONS | *\*to be defined* |  |
| @@REMSERVER | *\*to be defined* |  |
| @@SERVERNAME | CONCAT(‘[app.snowflake.com](http://app.snowflake.com/)’, CURRENT\_ACCOUNT( )) |  |
| @@SERVICENAME | *\*to be defined* |  |
| @@SPID | *\*to be defined* |  |
| @@TEXTSIZE | *\*to be defined* |  |
| @@VERSION | *\*to be defined* | Can be mimicked by using CURRENT\_VERSION |

Expand

Show lessSee more

## Conversion

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| CAST | CAST | Returns NULL if the value isn’t a number, otherwise returns the numeric value as its. When using operators such as <, >, =, <> then must be followed by a NULL |
| CONVERT | Check [CONVERT](#convert) | Same behavior as CAST |
| PARSE | *\*to be defined* |  |
| TRY\_CAST | TRY\_CAST | Returns NULL if the value isn’t a number, otherwise returns the numeric value as its. When using operators such as <, >, =, <> then must be followed by a NULL |
| [TRY\_CONVERT](#try_convert) | *\*to be defined* | Same behavior as TRY\_CAST |
| TRY\_PARSE | TRY\_CAST | Behavior may be different when parsing an integer as date or timestamp. |

Expand

Show lessSee more

## Cryptographic

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| ASYMKEY\_ID | *\*to be defined* |  |
| ASYMKEYPROPERTY | *\*to be defined* |  |
| CERTENCODED | *\*to be defined* |  |
| CERTPRIVATEKEY | *\*to be defined* |  |
| DECRYPTBYASYMKEY | *\*to be defined* |  |
| DECRYPTBYCERT | *\*to be defined* |  |
| DECRYPTBYKEY | *\*to be defined* |  |
| DECRYPTBYKEYAUTOASYMKEY | *\*to be defined* |  |
| DECRYPTBYKEYAUTOCERT | *\*to be defined* |  |
| DECRYPTBYPASSPHRASE | \_\*to be defined\_​ | Can be mimicked by using DENCRYPT\_RAW |
| ENCRYPTBYASYMKEY | *\*to be defined* |  |
| ENCRYPTBYCERT | *\*to be defined* |  |
| ENCRYPTBYKEY | *\*to be defined* |  |
| ENCRYPTBYPASSPHRASE | *\*to be defined* | Can be mimicked by using ENCRYPT\_RAW |
| HASHBYTES | **MD5, SHA1, SHA2** | Currently only supported separated hash. Use proper one according to the required algorithm  **MD5**, is a 32-character hex-encoded  **SHA1**, has a 40-character hex-encoded string containing the 160-bit  **SHA2**, a hex-encoded string containing the N-bit SHA-2 message digest. Sizes are:  224 = SHA-224  256 = SHA-256 (Default)  384 = SHA-384  512 = SHA-512 |
| IS\_OBJECTSIGNED | *\*to be defined* |  |
| KEY\_GUID | *\*to be defined* |  |
| KEY\_ID | *\*to be defined* |  |
| KEY\_NAME | *\*to be defined* |  |
| SIGNBYASYMKEY | *\*to be defined* |  |
| SIGNBYCERT | *\*to be defined* |  |
| SYMKEYPROPERTY | *\*to be defined* |  |
| VERIFYSIGNEDBYCERT | *\*to be defined* |  |

Expand

Show lessSee more

## Cursor

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| @@CURSOR\_ROWS | *\*to be defined* | ​ |
| @@FETCH\_STATUS | *\*to be defined* |  |
| CURSOR\_STATUS | *\*to be defined* |  |

Expand

Show lessSee more

## Data type

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| DATALENGTH | OCTET\_LENGTH | ​Snowflake doesn’t use fractional bytes so length is always calculated as 8 \* OCTET\_LENGTH |
| IDENT\_SEED | *\*to be defined* |  |
| IDENT\_CURRENT | *\*to be defined* |  |
| IDENTITY | *\*to be defined* |  |
| IDENT\_INCR | *\*to be defined* |  |
| SQL\_VARIANT\_PROPERTY | *\*to be defined* |  |

Expand

Show lessSee more

## Date & Time

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| @@DATEFIRST | *\*to be defined* |  |
| @@LANGUAGE | *\*to be defined* |  |
| CURRENT\_TIMESTAMP | CURRENT\_TIMESTAMP |  |
| CURRENT\_TIMEZONE | *\*to be defined* |  |
| DATEADD | DATEADD |  |
| DATEDIFF | DATEDIFF |  |
| DATEDIFF\_BIG | *\*to be defined* |  |
| DATEFROMPARTS | DATE\_FROM\_PARTS |  |
| DATENAME | *\*to be defined* | This function receives two arguments: a datepart and date. It returns a string. Here are the supported dateparts from TSQL to Snowflake  **year, yyyy, yy** -> DATE\_PART(YEAR, “$date”) **quarter, qq, q** -> DATE\_PART(QUARTER, “$date”) **month, mm, m** -> **MONTHNAME**( “$date”), though only providing a three-letter english month name **dayofyear, dy, y** -> DATE\_PART(DAYOFYEAR, “$date”) **day, dd, d** -> DATE\_PART(DAY, “$date”) **week, wk, ww** -> DATE\_PART(WEEK, “$date”)  **weekday, dw** -> **DAYNAME**(“$date”), though only providing an three-letter english day name **hour, hh** -> DATE\_PART(HOUR, “$date”) **minute, n** -> DATE\_PART(MINUTE, “$date”) **second, ss, s** -> DATE\_PART(SECOND, “$date”) **millisecond, ms** -> DATE\_PART(MS, “$date”) **microsecond, mcs** -> DATE\_PART(US, “$date”) **nanosecond, ns** -> DATE\_PART(NS, “$date”) **TZoffset, tz** -> needs a special implementation to get the time offset |
| DATEPART | DATE\_PART |  |
| DATETIME2FROMPARTS | *\*to be defined* |  |
| DATETIMEFROMPARTS | *\*to be defined* | ​Can be mimicked by using a combination of **DATE\_FROM\_PARTS and TIME\_FROM\_PARTS** |
| DATETIMEOFFSETFROMPARTS | *\*to be defined* |  |
| DAY | DAY |  |
| EOMONTH | *\*to be defined* | Can be mimicked by using **LAST\_DAY** |
| GETDATE | GETDATE |  |
| GETUTCDATE | *\*to be defined* | Can be mimicked by using **CONVERT\_TIMEZONE** |
| ISDATE | *\*to be defined* | Can be mimicked by using **TRY\_TO\_DATE**  Returns NULL if the value isn’t a **date**, otherwise returns the date value as its. When using operators such as <, >, =, <> then must be followed by a NULL |
| MONTH | MONTH |  |
| SMALLDATETIMEFROMPARTS | *\*to be defined* | ​​Can be mimicked by using a combination of **DATE\_FROM\_PARTS and TIME\_FROM\_PARTS** |
| SWITCHOFFSET | *\*to be defined* | ​Can be mimicked by using **CONVERT\_TIMEZONE** |
| SYSDATETIME | LOCALTIME |  |
| SYSDATETIMEOFFSET | *\*to be defined* | ​Can be mimicked by using **CONVERT\_TIMEZONE and LOCALTIME** |
| SYSUTCDATETIME | *\*to be defined* | ​​Can be mimicked by using **CONVERT\_TIMEZONE and LOCALTIME** |
| TIMEFROMPARTS | TIME\_FROM\_PARTS | ​ |
| TODATETIMEOFFSET | *\*to be defined* | ​Can be mimicked by using **CONVERT\_TIMEZONE** |
| YEAR | YEAR |  |

Expand

Show lessSee more

## JSON

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| ISJSON | CHECK\_JSON | ​This is a ‘preview feature’ in Snowflake |
| JSON\_VALUE | *\*to be defined* | Can be mimic by using  TO\_VARCHAR(GET\_PATH(PARSE\_JSON(JSON), PATH)) |
| JSON\_QUERY | *\*to be defined* |  |
| JSON\_MODIFY | *\*to be defined* |  |

Expand

Show lessSee more

## Mathematical

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| ABS | ABS |  |
| ACOS | ACOS |  |
| ASIN | ASIN |  |
| ATAN | ATAN |  |
| ATN2 | ATAN2 |  |
| CEILING | CEIL |  |
| COS | COS |  |
| COT | COT |  |
| DEGREES | DEGREES |  |
| EXP | EXP |  |
| FLOOR | FLOOR |  |
| LOG | LN |  |
| LOG10 | LOG |  |
| PI | PI |  |
| POWER | POWER |  |
| RADIANS | RADIANS |  |
| RAND | RANDOM |  |
| ROUND | ROUND |  |
| SIGN | SIGN |  |
| SIN | SIN |  |
| SQRT | SQRT |  |
| SQUARE | SQUARE |  |

Expand

Show lessSee more

## Logical

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| CHOOSE | *\*to be defined* | Can be mimic by using DECODE |
| GREATEST | GREATEST |  |
| IIF | IIF |  |
| LEAST | LEAST |  |
| NULLIF | NULLIF |  |

Expand

Show lessSee more

## Metadata

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| TransactSQL | Snowflake | Notes |
| @@PROCID | *\*to be defined* |  |
| APP\_NAME | *\*to be defined* |  |
| APPLOCK\_MODE | *\*to be defined* |  |
| APPLOCK\_TEST | *\*to be defined* |  |
| ASSEMBLYPROPERTY | *\*to be defined* |  |
| COL\_LENGTH | A UDF named COL\_LENGTH\_UDF is provided to retrieve this information. This UDF works only with VARCHAR types, as specified in the Transact-SQL documentation. For other data types, it returns NULL. |  |
| COL\_NAME | *\*to be defined* |  |
| COLUMNPROPERTY | *\*to be defined* |  |
| DATABASE\_PRINCIPAL\_ID | *\*to be defined* | Maps to CURRENT\_USER when no args |
| DATABASEPROPERTYEX | *\*to be defined* |  |
| DB\_ID | *\*to be defined* | We recommend changing to CURRENT\_DATABASE(). If there is a need to emulate this functionality.  SELECT DATE\_PART(EPOCH,CREATED) FROM INFORMATION\_SCHEMA.DATABASES WHERE DATABASE\_NAME = ‘DB’ ;  Can achieve something similar |
| DB\_NAME | *\*to be defined* | Mostly used in the procedurename mentioned above |
| FILE\_ID | *\*to be defined* |  |
| FILE\_IDEX | *\*to be defined* |  |
| FILE\_NAME | *\*to be defined* |  |
| FILEGROUP\_ID | *\*to be defined* |  |
| FILEGROUP\_NAME | *\*to be defined* |  |
| FILEGROUPPROPERTY | *\*to be defined* |  |
| FILEPROPERTY | *\*to be defined* |  |
| FULLTEXTCATALOGPROPERTY | *\*to be defined* |  |
| FULLTEXTSERVICEPROPERTY | *\*to be defined* |  |
| INDEX\_COL | *\*to be defined* |  |
| INDEXKEY\_PROPERTY | *\*to be defined* |  |
| INDEXPROPERTY | *\*to be defined* |  |
| NEXT VALUE FOR | *\*to be defined* |  |
| OBJECT\_DEFINITION | *\*to be defined* |  |
| OBJECT\_ID | *\*to be defined* | In most cases can be replaced. Most cases are like: IF OBJECT\_ID(‘dbo.TABLE’) IS NOT NULL DROP TABLE dbo.Table which can be replaced by a DROP TABLE IF EXISTS (this syntax is also supported in SQL SERVER). If the object\_id needs to be replicated, a UDF is added depending on the second parameter of the function call. |
| OBJECT\_NAME | *\*to be defined* | Can be replaced by: CREATE OR REPLACE PROCEDURE FOO() RETURNS STRING LANGUAGE JAVASCRIPT AS ‘ var rs = snowflake.execute({sqlText:`SELECT CURRENT_DATABASE() | '.' | ?`, binds:[arguments.callee.name]}); rs.next(); var procname = rs.getColumnValue(1); return procname; ‘; |
| OBJECT\_NAME(@@PROCID) | ‘ObjectName’ | This transformation only occurs when it is inside a DeclareStatement.  ObjectName is the name of the TopLevelObject that contains the Function. |
| OBJECT\_SCHEMA\_NAME | *\*to be defined* |  |
| OBJECT\_SCHEMA\_NAME(@@PROCID) | :OBJECT\_SCHEMA\_NAME | This transformation only occurs when it is inside a DeclareStatement. |
| OBJECTPROPERTY | *\*to be defined* |  |
| OBJECTPROPERTYEX | *\*to be defined* |  |
| ORIGINAL\_DB\_NAME | *\*to be defined* |  |
| PARSENAME | PARSENAME\_UDF | It creates a UDF to emulate the same behavior of Parsename function. |
| *\*to be defined* |  |  |
| SCHEMA\_NAME | *\*to be defined* |  |
| SCOPE\_IDENTITY | *\*to be defined* | It this is needed I would recommend to use sequences, and capture the value before insert |
| SERVERPROPERTY | *\*to be defined* |  |
| STATS\_DATE | *\*to be defined* |  |
| TYPE\_ID | *\*to be defined* |  |
| TYPE\_NAME | *\*to be defined* |  |
| TYPEPROPERTY | *\*to be defined* |  |
| VERSION | *\*to be defined* |  |

Expand

Show lessSee more

## Ranking

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| DENSE\_RANK | DENSE\_RANK |  |
| NTILE | NTILE |  |
| RANK | RANK |  |
| ROW\_NUMBER | ROW\_NUMBER |  |

Expand

Show lessSee more

## Replication

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| PUBLISHINGSERVERNAME | *\*to be defined* |  |

Expand

Show lessSee more

## Rowset

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| OPENDATASOURCE | *\*to be defined* |  |
| OPENJSON | *\*to be defined* |  |
| QPENQUERY | *\*to be defined* |  |
| OPENROWSET | *\*to be defined* |  |
| OPENXML | OPENXML\_UDF | User-defined function used as a equivalent behavior in Snowflake. |
| STRING\_SPLIT | SPLIT\_TO\_TABLE | The enable\_ordinal flag in Transact-SQL’s STRING\_SPLIT is not directly supported by Snowflake’s SPLIT\_TO\_TABLE function. If the ordinal column is required, a user-defined function (UDF) named STRING\_SPLIT\_UDF will be generated to replicate this behavior. Without the ordinal column, note that STRING\_SPLIT returns a single column named value, while SPLIT\_TO\_TABLE returns three columns: value, index (equivalent to ordinal), and seq. For additional details, see the [SPLIT\_TO\_TABLE documentation](https://docs.snowflake.com/en/sql-reference/functions/split_to_table). |

Expand

Show lessSee more

## Security

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| CERTENCODED | *\*to be defined* |  |
| CERTPRIVATEKEY | *\*to be defined* |  |
| CURRENT\_USER | CURRENT\_USER |  |
| DATABASE\_PRINCIPAL\_ID | *\*to be defined* |  |
| HAS\_PERMS\_BY\_NAME | *\*to be defined* |  |
| IS\_MEMBER | *\*to be defined* | Change to query INFORMATION\_SCHEMA although the client might require defining new roles |
| IS\_ROLEMEMBER | *\*to be defined* | Snowflake’s a similar function  **IS\_ROLE\_IN\_SESSION** |
| IS\_SRVROLEMEMBER | *\*to be defined* |  |
| LOGINPROPERTY | *\*to be defined* |  |
| ORIGINAL\_LOGIN | *\*to be defined* |  |
| PERMISSIONS | *\*to be defined* |  |
| PWDCOMPARE | *\*to be defined* |  |
| PWDENCRYPT | *\*to be defined* |  |
| SCHEMA\_ID | *\*to be defined* |  |
| SCHEMA\_NAME | *\*to be defined* |  |
| SESSION\_USER | *\*to be defined* |  |
| SUSER\_ID | *\*to be defined* |  |
| SUSER\_NAME | *\*to be defined* |  |
| SUSER\_SID | *\*to be defined* |  |
| SUSER\_SNAME | *\*to be defined* |  |
| sys.fn\_builtin\_permissions | *\*to be defined* |  |
| sys.fn\_get\_audit\_file | *\*to be defined* |  |
| sys.fn\_my\_permissions | *\*to be defined* |  |
| SYSTEM\_USER | *\*to be defined* |  |
| USER\_ID | *\*to be defined* |  |
| USER\_NAME | *\*to be defined* | Maps to CURRENT\_USER |

Expand

Show lessSee more

## String

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| ASCII | ASCII |  |
| CHAR | CHR, CHAR |  |
| CHARINDEX | CHARINDEX |  |
| CONCAT | CONCAT |  |
| CONCAT\_WS | CONCAT\_WS |  |
| COALESCE | COALESCE |  |
| DIFFERENCE | *\*to be defined* |  |
| FORMAT | TO\_CHAR | Supports numeric format specifiers (P, N, %) and date/time custom specifiers (dd, MM, yyyy, HH, mm, ss, fff, dddd, F–FFFFFFF, z, and more), including single-character specifiers (`%y`, `%M`, `%d`, `%H`, `%h`, `%m`, `%s`). Some date/time specifiers (`dddd`, `F`–`FFFFFFF`, `z`) are translated with SSC-FDM-0036 due to behavioral differences. SSC-EWI-0006 may be generated for remaining unsupported formats. |
| LEFT | LEFT |  |
| LEN | LEN |  |
| LOWER | LOWER |  |
| LTRIM | LTRIM |  |
| NCHAR | *\*to be defined* |  |
| PATINDEX | *\*to be defined* | Map to REGEXP\_INSTR |
| QUOTENAME | QUOTENAME\_UDF | It creates a UDF to emulate the same behavior of Quotename function |
| REPLACE | REPLACE |  |
| REPLICATE | REPEAT |  |
| REVERSE | REVERSE |  |
| RIGHT | RIGHT |  |
| RTRIM | RTRIM |  |
| SOUNDEX | SOUNDEX |  |
| SPACE | *\*to be defined* |  |
| STR | *\*to be defined* |  |
| STRING\_AGG | *\*to be defined* |  |
| STRING\_ESCAPE | *\*to be defined* |  |
| STRING\_SPLIT | SPLIT\_TO\_TABLE |  |
| STUFF | *\*to be defined* | CREATE OR REPLACE FUNCTION STUFF(S string, STARTPOS int, LENGTH int, NEWSTRING string) RETURNS string LANGUAGE SQL AS ‘ left(S, STARTPOS) |
| SUBSTRING | SUBSTRING |  |
| TRANSLATE | TRANSLATE |  |
| TRIM | TRIM |  |
| UNICODE | UNICODE |  |
| UPPER | UPPER |  |

Expand

Show lessSee more

## System

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| $PARTITION | *\*to be defined* |  |
| @@ERROR | *\*to be defined* |  |
| @@IDENTITY | *\*to be defined* | It this is needed I would recommend to use sequences, and capture the value before insert |
| @@PACK\_RECEIVED | *\*to be defined* |  |
| @@ROWCOUNT | *\*to be defined* |  |
| @@TRANCOUNT | *\*to be defined* |  |
| BINARY\_CHECKSUM | *\*to be defined* |  |
| CHECKSUM | *\*to be defined* |  |
| COMPRESS | COMPRESS | ​Snowflake’s version has a method argument to indicate the compression method. These are the valid values: **SNAPPY, ZLIB, ZSTD, BZ2**  The compression level is specified in parentheses and must be a non-negative integer |
| CONNECTIONPROPERTY | *\*to be defined* |  |
| CONTEXT\_INFO | *\*to be defined* |  |
| CURRENT\_REQUEST\_ID | *\*to be defined* |  |
| CURRENT\_TRANSACTION\_ID | *\*to be defined* |  |
| DECOMPRESS | *\*to be defined* | Snowflake has two functions for these: **DECOMPRESS\_BINARY** and **DECOMPRESS\_STRING**​ |
| ERROR\_LINE | *\*to be defined* | SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/conversion-issues/generalEWI)**.  JavaScript: Will map to **ERROR\_LINE** helper. EXEC helper will capture the Exception line property from the stack trace. |
| ERROR\_MESSAGE | SQLERRM | Added **SSC-FDM-TS0023** returned error message could be different in Snowflake. |
| ERROR\_NUMBER | *\*to be defined* | SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/conversion-issues/generalEWI)**.  JavaScript: Will map to **ERROR\_NUMBER** helper. EXEC helper will capture the Exception code property. |
| ERROR\_PROCEDURE | *Mapped* | SnowScript: Use current procedure name, added **SSC-FDM-TS0023** result value is based on the stored procedure where the function is called instead of where the exception occurs.  JavaScript: Will map to **ERROR\_PROCEDURE** helper, taken from the `arguments.callee.name` procedure property |
| ERROR\_SEVERITY | *\*to be defined* | SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/conversion-issues/generalEWI)**. |
| ERROR\_STATE | SQLSTATE | SnowScript: Converted to **SQLSTATE** snowflake property, added **SSC-FDM-TS0023** returned value could be different in Snowflake.  JavaScript: Helper will capture Exception state property |
| FORMATMESSAGE | FORMATEMESSAGE\_UDF | It creates a UDF to emulate the same behavior of FORMATMESSAGE function but with some limitations. |
| GET\_FILESTREAM\_TRANSACTION\_CONTEXT | *\*to be defined* |  |
| GETANSINULL | *\*to be defined* |  |
| HOST\_ID | *\*to be defined* |  |
| HOST\_NAME | *\*to be defined* |  |
| ISNULL | NVL |  |
| ISNUMERIC | *\*to be defined* | No direct equivalent but can be mapped to a custom UDF, returning the same values as in TSQL. |
| MIN\_ACTIVE\_ROWVERSION | *\*to be defined* | ​ |
| NEWID | *\*to be defined* | ​Maps to UUID\_STRING |
| NEWSEQUENTIALID | *\*to be defined* | ​ |
| ROWCOUNT\_BIG | *\*to be defined* | ​ |
| SESSION\_CONTEXT | *\*to be defined* | ​ |
| SESSION\_ID | *\*to be defined* | ​ |
| XACT\_STATE | *\*to be defined* | ​ |

Expand

Show lessSee more

## System Statistical

| TransactSql | Snowflake | Notes |
| --- | --- | --- |
| @@CONNECTIONS | *\*to be defined* | ​Snowflake’s a similar function: **LOGIN\_HISTORY.**  Returns login events within a specified time range |
| @@PACK\_RECEIVED | *\*to be defined* |  |
| @@CPU\_BUSY | *\*to be defined* |  |
| @@PACK\_SENT | *\*to be defined* |  |
| @@TIMETICKS | *\*to be defined* |  |
| @@IDLE | *\*to be defined* |  |
| @@TOTAL\_ERRORS | *\*to be defined* |  |
| @@IO\_BUSY | *\*to be defined* |  |
| @@TOTAL\_READ | *\*to be defined* |  |
| @@PACKET\_ERRORS | *\*to be defined* |  |
| @@TOTAL\_WRITE | *\*to be defined* |  |

Expand

Show lessSee more

## Text & Image

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| TEXTPTR | *\*to be defined* |  |
| TEXTVALID | *\*to be defined* |  |

Expand

Show lessSee more

## Trigger

| TransactSQL | Snowflake | Notes |
| --- | --- | --- |
| COLUMNS\_UPDATED | *\*to be defined* |  |
| EVENTDATA | *\*to be defined* |  |
| TRIGGER\_NESTLEVEL | *\*to be defined* |  |
| UPDATE | *\*to be defined* |  |

Expand

Show lessSee more

# System functions

This section describes the functional equivalents of system functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## ISNULL

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Replaces NULL with the specified replacement value. ([ISNULL in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/isnull-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
ISNULL ( check_expression , replacement_value )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nvl.html)

Copy code

```
NVL( <expr1> , <expr2> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT ISNULL(NULL, 'SNOWFLAKE') AS COMPANYNAME;
```

**Result:**

| COMPANYNAME |
| --- |
| SNOWFLAKE |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
NVL(NULL, 'SNOWFLAKE') AS COMPANYNAME;
```

**Result:**

| COMPANYNAME |
| --- |
| SNOWFLAKE |

Expand

Show lessSee more

## NEWID

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Creates a unique value of type uniqueidentifier. ([NEWID in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
NEWID ( )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nvl.html)

Copy code

```
UUID_STRING()
```

### Examples

Warning

Outputs may differ because it generates a unique ID in runtime

#### SQL Server

Copy code

```
:force: 

SELECT NEWID ( ) AS ID;
```

**Result:**

| ID |
| --- |
| 47549DDF-837D-41D2-A59C-A6BC63DF7910 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
UUID_STRING( ) AS ID;
```

**Result:**

| ID |
| --- |
| 6fd4312a-7925-4ad9-85d8-e039efd82089 |

Expand

Show lessSee more

## NULLIF

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a null value if the two specified expressions are equal.

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
NULLIF ( check_expression , replacement_value )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nullif.html)

Copy code

```
:force:
NULLIF( <expr1> , <expr2> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT NULLIF(6,9) AS RESULT1, NULLIF(5,5) AS RESULT2;
```

**Result:**

| RESULT1 | RESULT2 |
| --- | --- |
| 6 | null |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
NULLIF(6,9) AS RESULT1,
NULLIF(5,5) AS RESULT2;
```

**Result:**

| RESULT1 | RESULT2 |
| --- | --- |
| 6 | null |

Expand

Show lessSee more

## @@ROWCOUNT

Applies to

- SQL Server

### Description

Returns the number of rows affected by the last statement. ([@@ROWCOUNT in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/rowcount-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
@@ROWCOUNT
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/dml-status)

Copy code

```
SQLROWCOUNT
```

### Examples

#### SQL Server

Copy code

```
:force: 

CREATE TABLE table1
(
    column1 INT
);

CREATE PROCEDURE procedure1
AS
BEGIN
    declare @addCount int = 0;

    INSERT INTO table1 (column1) VALUES (1),(2),(3);
    set @addCount = @addCount + @@ROWCOUNT

   select @addCount
END
;
GO

EXEC procedure1;
```

**Result:**

|  |
| --- |
| 3 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

CREATE OR REPLACE TABLE table1
(
    column1 INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/13/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ADDCOUNT INT := 0;
        ProcedureResultSet RESULTSET;
    BEGIN
         

        INSERT INTO table1 (column1) VALUES (1),(2),(3);
        ADDCOUNT := :ADDCOUNT + SQLROWCOUNT;
        ProcedureResultSet := (

       select
            :ADDCOUNT);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;

CALL procedure1();
```

**Result:**

| :ADDCOUNT |
| --- |
| 3 |

Expand

Show lessSee more

## FORMATMESSAGE

Applies to

- SQL Server

### Description

Constructs a message from an existing message in sys.messages or from a provided string. ([FORMATMESSAGE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/formatmessage-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

Since Snowflake does not support `FORMATMESSAGE` function, the [FORMATMESSAGE\_UDF](#formatmessage_udf) is added to simulate its behavior.

### Syntax

#### SQL Server

Copy code

```
:force:
FORMATMESSAGE ( { msg_number  | ' msg_string ' | @msg_variable} , [ param_value [ ,...n ] ] )
```

### Examples

#### SQL Server

Copy code

```
:force:
SELECT FORMATMESSAGE('This is the %s and this is the %s.', 'first variable', 'second variable') AS RESULT;
```

**Result:**

| RESULT |
| --- |
| This is the first variable and this is the second variable. |

Expand

Show lessSee more

#### Snowflake

Copy code

```
:force:
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('This is the %s and this is the %s.', ARRAY_CONSTRUCT('first variable', 'second variable')) AS RESULT;
```

**Result:**

| RESULT |
| --- |
| This is the first variable and this is the second variable. |

Expand

Show lessSee more

### Related EWIs

1. [SSC-FDM-TS0008](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0008): FORMATMESSAGE function was converted to UDF.

## FORMATMESSAGE\_UDF

Snowflake does not have a function with the functionality of `FORMATMESSAGE`. The following Python UDF is generated to emulate the behavior of `FORMATMESSAGE`.

Copy code

```
:force:
CREATE OR REPLACE FUNCTION FORMATMESSAGE_UDF(MESSAGE STRING, ARGS ARRAY)
RETURNS STRING
LANGUAGE python
IMMUTABLE
RUNTIME_VERSION = '3.8'
HANDLER = 'format_py'
as
$$
def format_py(message,args):
  return message % (*args,)
$$;
```

This UDF may not work correctly on some cases:

- Using the `%I64d` placeholder will throw an error.
- If the number of substitution arguments is different than the number of place holders, it will throw an error.
- Some unsigned placeholders like `%u` or `%X` will not behave properly when formatting the value.
- It cannot handle message\_ids.

## String functions

This section describes the functional equivalents of string functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## CHAR

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a single-byte character with the integer sent as a parameter on the ASCII table ([CHAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
CHAR( expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/chr.html)

Copy code

```
:force:
{CHR | CHAR} ( <input> )
```

##### JavaScript

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode)

Copy code

```
:force:
String.fromCharCode( expression1, ... , expressionN )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CHAR(170) AS SMALLEST_A
```

**Output:**

| SMALLEST\_A |
| --- |
| ª |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CHAR(170) AS SMALLEST_A;
```

**Result:**

| SMALLEST\_A |
| --- |
| ª |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION get_char(expression float)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  return String.fromCharCode( EXPRESSION );
$$;

SELECT GET_CHAR(170) SMALLEST_A;
```

**Result:**

| SMALLEST\_A |
| --- |
| ª |

Expand

Show lessSee more

## CHARINDEX

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the index of the first occurrence of the specified value sent as a parameter when it matches ([CHARINDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
CHARINDEX( expression_to_find, expression_to_search [, start] )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/charindex.html)

Copy code

```
CHARINDEX( <expr1>, <expr2> [ , <start_pos> ] )
```

##### JavaScript

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/indexOf)

Copy code

```
String.indexOf( search_value [, index] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CHARINDEX('t', 'Customer') AS MatchPosition;
```

**Result:**

| INDEX |
| --- |
| 33 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CHARINDEX('t', 'Customer') AS MatchPosition;
```

**Result:**

| INDEX |
| --- |
| 33 |

Expand

Show lessSee more

##### JavaScript

Note

Indexes in Transact start at 1, instead of JavaScript which start at 0.

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION get_index
(
  expression_to_find varchar, 
  expression_to_search varchar, 
  start_index  float
)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return EXPRESSION_TO_SEARCH.indexOf(EXPRESSION_TO_FIND, START_INDEX)+1;
$$;

SELECT GET_INDEX('and', 'Give your heart and soul to me, and life will always be la vie en rose', 20) AS INDEX;
```

**Result:**

| INDEX |
| --- |
| 33 |

Expand

Show lessSee more

## COALESCE

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Evaluates the arguments in order and returns the current value of the first expression that initially doesn’t evaluate to NULL. For example,SELECT COALESCE(NULL, NULL, ‘third\_value’, ‘fourth\_value’); returns the third value because the third value is the first value that isn’t null. ([COALESCE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/coalesce-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
COALESCE ( expression [ ,...n ] )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/coalesce.html)

Copy code

```
:force:
COALESCE( <expr1> , <expr2> [ , ... , <exprN> ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT TOP 10 StartDate, 
COALESCE(EndDate,'2000-01-01') AS FIRST_NOT_NULL 
FROM HumanResources.EmployeeDepartmentHistory
```

**Result:**

| StartDate | FIRST\_NOT\_NULL |
| --- | --- |
| 2009-01-14 | 2000-01-01 |
| 2008-01-31 | 2000-01-01 |
| 2007-11-11 | 2000-01-01 |
| 2007-12-05 | 2010-05-30 |
| 2010-05-31 | 2000-01-01 |
| 2008-01-06 | 2000-01-01 |
| 2008-01-24 | 2000-01-01 |
| 2009-02-08 | 2000-01-01 |
| 2008-12-29 | 2000-01-01 |
| 2009-01-16 | 2000-01-01 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT TOP 10
StartDate,
COALESCE(EndDate,'2000-01-01') AS FIRST_NOT_NULL
FROM
HumanResources.EmployeeDepartmentHistory;
```

**Result:**

| StartDate | FIRST\_NOT\_NULL |
| --- | --- |
| 2009-01-14 | 2000-01-01 |
| 2008-01-31 | 2000-01-01 |
| 2007-11-11 | 2000-01-01 |
| 2007-12-05 | 2010-05-30 |
| 2010-05-31 | 2000-01-01 |
| 2008-01-06 | 2000-01-01 |
| 2008-01-24 | 2000-01-01 |
| 2009-02-08 | 2000-01-01 |
| 2008-12-29 | 2000-01-01 |
| 2009-01-16 | 2000-01-01 |

Expand

Show lessSee more

## CONCAT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Makes a concatenation of string values with others. ([CONCAT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
CONCAT ( string_value1, string_value2 [, string_valueN ] )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/concat.html)

Copy code

```
CONCAT( <expr1> [ , <exprN> ... ] )

<expr1> || <expr2> [ || <exprN> ... ]
```

##### JavaScript

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/concat)

Copy code

```
:force: 

 String.concat( expression1, ..., expressionN )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CONCAT('Ray',' ','of',' ','Light') AS TITLE;
```

**Output:**

| TITLE |
| --- |
| Ray of Light |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CONCAT('Ray',' ','of',' ','Light') AS TITLE;
```

**Output:**

| TITLE |
| --- |
| Ray of Light |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION concatenate_strs(strings array)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  var result = ""
  STRINGS.forEach(element => result = result.concat(element));
  return result;
$$;
SELECT concatenate_strs(array_construct('Ray',' ','of',' ','Light')) TITLE;
```

**Output:**

| TITLE |
| --- |
| Ray of Light |

Expand

Show lessSee more

## LEFT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the right part of a character string with the specified number of characters. ([RIGHT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
LEFT ( character_expression , integer_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/left.html)

Copy code

```
LEFT ( <expr> , <length_expr> )
```

##### JavaScript

Function used to emulate the behavior

Copy code

```
:force: 

function LEFT(string, index){
    if(index < 0){
        throw new RangeError('Invalid INDEX on LEFT function');
    }
    return string.slice( 0, index);
  }
return LEFT(STR, INDEX);
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT LEFT('John Smith', 5) AS FIRST_NAME;
```

**Output:**

| FIRST\_NAME |
| --- |
| John |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT LEFT('John Smith', 5) AS FIRST_NAME;
```

**Output:**

| FIRST\_NAME |
| --- |
| John |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION left_str(str varchar, index float)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
    function LEFT(string, index){
      if(index < 0){
          throw new RangeError('Invalid INDEX on LEFT function');
      }
      return string.slice( 0, index);
    }
  return LEFT(STR, INDEX);
$$;
SELECT LEFT_STR('John Smith', 5) AS FIRST_NAME;
```

**Output:**

| FIRST\_NAME |
| --- |
| John |

Expand

Show lessSee more

## LEN

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the length of a string ([LEN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/len-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
LEN( string_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/length.html)

Copy code

```
LENGTH( <expression> )
LEN( <expression> )
```

##### JavaScript

[JavaScript SQL complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/length)

Copy code

```
:force: 

 string.length
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT LEN('Sample text') AS [LEN];
```

**Output:**

| LEN |
| --- |
| 11 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT LEN('Sample text') AS LEN;
```

**Output:**

| LEN |
| --- |
| 11 |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION get_len(str varchar)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return STR.length;
$$;
SELECT GET_LEN('Sample text') LEN;
```

**Output:**

| LEN |
| --- |
| 11 |

Expand

Show lessSee more

## LOWER

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts a string to lowercase ([LOWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/lower-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

LOWER ( character_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/lower.html)

Copy code

```
:force: 

LOWER( <expr> )
```

##### JavaScript

[JavaScript SQL complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase)

Copy code

```
:force: 

 String.toLowerCase( )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') AS LOWERCASE;
```

**Output:**

| LOWERCASE |
| --- |
| you are a prediction of the good ones |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 
SELECT LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') AS LOWERCASE;
```

**Output:**

| LOWERCASE |
| --- |
| you are a prediction of the good ones |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION to_lower(str varchar)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  return STR.toLowerCase();
$$;

SELECT TO_LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') LOWERCASE;
```

**Output:**

| LOWERCASE |
| --- |
| you are a prediction of the good ones |

Expand

Show lessSee more

## NCHAR

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the UNICODE character of an integer sent as a parameter ([NCHAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/nchar-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

Copy code

```
NCHAR( expression )
```

##### Arguments

`expression`: Integer expression.

##### Return Type

String value, it depends on the input received.

### Examples

#### Query

Copy code

```
:force: 

SELECT NCHAR(170);
```

##### Result

|  |
| --- |
| ª |

Expand

Show lessSee more

Note

The equivalence for this function in JavaScript is documented in [CHAR](#char).

## REPLACE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Replaces all occurrences of a specified string value with another string value. ([REPLACE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/replace-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
REPLACE ( string_expression , string_pattern , string_replacement )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/replace.html)

Copy code

```
REPLACE( <subject> , <pattern> [ , <replacement> ] )
```

##### JavaScript

Copy code

```
:force: 

 String.replace( pattern, new_expression)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT REPLACE('Real computer software', 'software','science') AS COLUMNNAME;
```

**Output:**

Copy code

```
COLUMNNAME           |
---------------------|
Real computer science|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT REPLACE('Real computer software', 'software','science') AS COLUMNNAME;
```

**Output:**

Copy code

```
COLUMNNAME           |
---------------------|
Real computer science|
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION REPLACER (str varchar, pattern varchar, new_expression varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.replace( PATTERN, NEW_EXPRESSION );
$$;

SELECT REPLACER('Real computer software', 'software', 'science') AS COLUMNNAME;
```

**Output:**

Copy code

```
COLUMNNAME             |
---------------------|
Real computer science|
```

## REPLICATE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Replicates a string value a specified number of times ([REPLICATE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/replicate-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
REPLICATE( string_expression, number_expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/repeat.html)

Copy code

```
REPEAT(<input>, <n>)
```

##### JavaScript

[JavaScript Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/repeat)

Copy code

```
String.repeat( number_expression )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT REPLICATE('Staying alive',5) AS RESULT
```

**Result:**

Copy code

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT REPEAT('Staying alive',5) AS RESULT;
```

**Result:**

Copy code

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION REPEAT_STR (str varchar, occurrences float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
 
   return STR.repeat( OCCURRENCES );
$$;

SELECT REPEAT_STR('Staying alive ', 5) AS RESULT;
```

**Result:**

Copy code

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

## RIGHT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the right part of a character string with the specified number of characters. ([RIGHT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
RIGHT ( character_expression , integer_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/right.html)

Copy code

```
RIGHT( <expr> , <length_expr> )
```

##### JavaScript

UDF used to emulate the behavior

Copy code

```
:force: 

 function RIGHT(string, index){
      if(index< 0){
          throw new RangeError('Invalid INDEX on RIGHT function');
      }
      return string.slice( string.length - index, string.length );
    }
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT RIGHT('John Smith', 5) AS LAST_NAME;
```

**Output:**

Copy code

```
   LAST_NAME|      
------------|
       Smith|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT RIGHT('John Smith', 5) AS LAST_NAME;
```

**Output:**

Copy code

```
   LAST_NAME|      
------------|
       Smith|
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION right_str(str varchar, index float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function RIGHT(string, index){
      if(index< 0){
          throw new RangeError('Invalid INDEX on RIGHT function');
      }
      return string.slice( string.length - index, string.length );
    }
  return RIGHT(STR, INDEX);
$$;

SELECT RIGHT_STR('John Smith', 5) AS LAST_NAME;
```

**Output:**

Copy code

```
   LAST_NAME|      
------------|
       Smith|
```

## RTRIM

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a character expression after it removes leading blanks ([RTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
RTRIM( string_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/rtrim.html)

Copy code

```
RTRIM(<expr> [, <characters> ])
```

##### JavaScript

Custom function used to emulate the behavior

Copy code

```
:force: 

 function RTRIM(string){
    return string.replace(/s+$/,"");
}
```

### Examples

#### SQL Server

**Input:**

Copy code

```
:force: 

SELECT RTRIM('LAST TWO BLANK SPACES  ') AS [RTRIM]
```

**Output:**

Copy code

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT RTRIM('LAST TWO BLANK SPACES  ') AS RTRIM;
```

**Result:**

Copy code

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION rtrim(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  function RTRIM(string){
    return string.replace(/s+$/,"");
    }
   return RTRIM( STR );
$$;

SELECT RTRIM('LAST TWO BLANK SPACES  ') AS RTRIM;
```

**Result:**

Copy code

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

## SPACE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a number of occurrences of blank spaces ([SPACE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
SPACE ( integer_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/space.html)

Copy code

```
SPACE(<n>)
```

##### JavaScript

Custom function used to emulate the behavior

Copy code

```
:force: 

 function SPACE( occurrences ){
    return ' '.repeat( occurrences );
}
```

### Examples

#### SQL Server

**Input:**

Copy code

```
:force: 

SELECT CONCAT('SOME', SPACE(5), 'TEXT') AS RESULT;
```

**Output:**

Copy code

```
RESULT       |
-------------|
SOME     TEXT|
```

##### Snowflake SQL

**Input:**

Copy code

```
:force: 

SELECT CONCAT('SOME', SPACE(5), 'TEXT') AS RESULT;
```

**Output:**

Copy code

```
RESULT       |
-------------|
SOME     TEXT|
```

##### JavaScript

**Input:**

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION SPACE(occurrences float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function SPACE( occurrences ){
    return ' '.repeat( occurrences );
    }
    return SPACE( OCCURRENCES );
$$;

SELECT CONCAT('SOME', SPACE(5), 'TEXT') RESULT;
```

**Output:**

Copy code

```
RESULT       |
-------------|
SOME     TEXT|
```

## SUBSTRING

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a character expression after it removes leading blanks ([RTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
SUBSTRING( string_expression, start, length )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/substr.html)

Copy code

```
SUBSTR( <base_expr>, <start_expr> [ , <length_expr> ] )

SUBSTRING( <base_expr>, <start_expr> [ , <length_expr> ] )
```

##### JavaScript

Custom function used to emulate the behavior

Copy code

```
:force: 

 string.substring( indexA [, indexB])
```

### Examples

#### SQL Server

**Input:**

Copy code

```
:force: 

SELECT SUBSTRING('abcdef', 2, 3) AS SOMETEXT;
```

**Output:**

Copy code

```
SOMETEXT|
--------|
bcd     |
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT SUBSTRING('abcdef', 2, 3) AS SOMETEXT;
```

**Result:**

Copy code

```
SOMETEXT|
--------|
bcd     |
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION REPLACER_LENGTH(str varchar, index float, length float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    var start = INDEX - 1;
    var end = STR.length - (LENGTH - 1);
    return STR.substring(start, end);
$$;

SELECT REPLACER_LENGTH('abcdef', 2, 3) AS SOMETEXT;
```

**Result:**

Copy code

```
SOMETEXT|
--------|
bcd     |
```

## UPPER

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts a string to uppercase ([UPPER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/upper-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
UPPER( string_expression )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/upper.html)

Copy code

```
UPPER( <expr> )
```

##### JavaScript

[JavaScript SQL complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/toUpperCase)

Copy code

```
:force: 

 String.toUpperCase( )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT UPPER('you are a prediction of the good ones') AS [UPPER]
```

**Output:**

Copy code

```
+-------------------------------------|
|UPPER                                |
+-------------------------------------|
|YOU ARE A PREDICTION OF THE GOOD ONES|
+-------------------------------------|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
UPPER('you are a prediction of the good ones') AS UPPER;
```

**Output:**

Copy code

```
+-------------------------------------|
|UPPER                                |
+-------------------------------------|
|YOU ARE A PREDICTION OF THE GOOD ONES|
+-------------------------------------|
```

##### JavaScript

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION to_upper(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return STR.toUpperCase();
$$;

SELECT TO_UPPER('you are a prediction of the good ones') UPPER;
```

**Output:**

Copy code

```
UPPER                                |
-------------------------------------|
YOU ARE A PREDICTION OF THE GOOD ONES|
```

## ASCII

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the number code of a character on the ASCII table ([ASCII in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ascii-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
ASCII( expression )
```

#### Arguments

`expression`: `VARCVHAR` or `CHAR` expression.

#### Return Type

`INT`.

### Examples

### Query

Copy code

```
:force:
SELECT ASCII('A') AS A , ASCII('a') AS a;
```

#### Result

Copy code

```
          A|          a|
-----------| ----------|
         65|         97|
```

## ASCII in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the number code of a character on the ASCII table ([JavaScript charCodeAt function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/charCodeAt)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 string.charCodeAt( [index] )
```

##### Arguments

`index`(Optional): Index of string to get character and return its code number on the ASCII table. If this parameter is not specified, it takes 0 as default. \

##### Return Type

`Int`.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION get_ascii(c char)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return C.charCodeAt();
$$;

SELECT GET_ASCII('A') A, GET_ASCII('a') a;
```

##### Result

Copy code

```
          A|          a|
-----------| ----------|
         65|         97|
```

## QUOTENAME

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a string delimited using quotes ([QUOTENAME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/quotename-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
QUOTENAME( string_expression [, quote_character])
```

#### Arguments

`string_expression`: String to delimit.

`quote_character`: one-character to delimit the string.

#### Return Type

`NVARCHAR(258)`. Null if the quote is different of (‘), ([]), (“), ( () ), ( >< ), ({}) or (`).

### Examples

### Query

Copy code

```
:force:
SELECT QUOTENAME('Hello', '`') AS HELLO;
```

#### Result

Copy code

```
    HELLO|      
---------|
  `Hello`|
```

## QUOTENAME in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, this function is not available in JavaScript, but it can be implemented using predefined functions.

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 function QUOTENAME(string, quote){
    return quote.concat(string, quote);
}
```

##### Arguments

`string`: String expression to delimit.

`quote`: Quote to be used as a delimiter.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION QUOTENAME(str varchar, quote char)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  function QUOTENAME(string, quote){
    const allowed_quotes = /[\']|[\"]|[(]|[)]|[\[]|[\]]|[\{]|[\}]|[\`]/;
    
    if(!allowed_quotes.test(quote)) throw new TypeError('Invalid Quote');
    
    return quote.concat(string, quote);
  }
   return QUOTENAME(STR, QUOTE);
$$;

SELECT QUOTENAME('Hola', '`') HELLO;
```

##### Result

Copy code

```
    HELLO|      
---------|
  `Hello`|
```

## CONCAT\_WS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Makes a concatenation of string values with others using a separator between them ([CONCAT\_WS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
CONCAT_WS( separator, expression1, ... ,expressionN )
```

#### Arguments

`separator`: Separator to join.

`expression1, ... ,expressionN:` Expression to be found into a string.

#### Return Type

String value, depends on the input received.

### Examples

### Query

Copy code

```
:force:
SELECT CONCAT_WS(' ', 'Mariah','Carey') AS NAME;
```

#### Result

Copy code

```
        NAME|      
------------|
Mariah Carey|
```

## Join in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Concatenates the string arguments to the calling string using a separator ([JavaScript Join function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array/join)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Array.join( separator )
```

##### Arguments

`separator`: Character to join.

##### Return Type

`String`.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION join_strs(separator varchar, strings array)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return STRINGS.join(SEPARATOR);
$$;
SELECT join_strs(' ',array_construct('Mariah','Carey')) NAME;
```

##### Result

Copy code

```
        NAME|      
------------|
Mariah Carey|
```

## SOUNDEX

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a four-character code to evaluate the similarity of two strings ([SOUNDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/soundex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
SOUNDEX( string_expression )
```

#### Arguments

`string_expression`: String expression to reverse.

#### Return Type

The same data type of the string expression sent as a parameter.

### Examples

### Query

Copy code

```
:force:
SELECT SOUNDEX('two') AS TWO , SOUNDEX('too') AS TOO;
```

#### Result

Copy code

```
      TWO|      TOO|
---------|---------|
     T000|     T000|
```

## SOUNDEX in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, JavaScript does not provide a method that executes the SOUNDEX algorithm, but it can be implemented manually.

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 const dic = {A:0, B:1, C:2, D:3, E:0, F:1, G:2, H:0, I:0, J:2, K:2, L:4, M:5, N:5, O:0, P:1, Q:2, R:6, S:2, T:3, U:0, V:1, W:0, X:2, Y:0, Z:2};

  function getCode(letter){
      return dic[letter.toUpperCase()];
  }

  function SOUNDEX(word){
    var initialCharacter = word[0].toUpperCase();
    var initialCode = getCode(initialCharacter);
    for(let i = 1; i < word.length; ++i) {
        const letterCode = getCode(word[i]);
        if (letterCode && letterCode != initialCode) {
             initialCharacter += letterCode;
             if(initialCharacter.length == 4) break;
        }
        initialCode = letterCode;
    }
      
      return initialCharacter.concat( '0'.repeat( 4 - initialCharacter.length));
      
  }
```

##### Arguments

`word`: String expression to get its SOUNDEX equivalence.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION get_soundex(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  const dic = {A:0, B:1, C:2, D:3, E:0, F:1, G:2, H:0, I:0, J:2, K:2, L:4, M:5, N:5, O:0, P:1, Q:2, R:6, S:2, T:3, U:0, V:1, W:0, X:2, Y:0, Z:2};

  function getCode(letter){
      return dic[letter.toUpperCase()];
  }

  function SOUNDEX(word){
    var initialCharacter = word[0].toUpperCase();
    var initialCode = getCode(initialCharacter);
    for(let i = 1; i < word.length; ++i) {
        const letterCode = getCode(word[i]);
        if (letterCode && letterCode != initialCode) {
             initialCharacter += letterCode;
             if(initialCharacter.length == 4) break;
        }
        initialCode = letterCode;
    }
    
    return initialCharacter.concat( '0'.repeat( 4 - initialCharacter.length));    
  }
  
  return SOUNDEX( STR );
$$;

SELECT GET_SOUNDEX('two') AS TWO , GET_SOUNDEX('too') AS TOO;
```

##### Result

Copy code

```
      TWO|      TOO|
---------|---------|
     T000|     T000|
```

## REVERSE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Reverses a string ([REVERSE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/reverse-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
REVERSE( string_expression )
```

#### Arguments

`string_expression`: String expression to reverse.

#### Return Type

The same data type of the string expression sent as a parameter.

### Examples

### Query

Copy code

```
:force:
SELECT REVERSE('rotator') AS PALINDROME;
```

#### Result

Copy code

```
      PALINDROME|      
----------------|
         rotator|
```

## reverse in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, this function is not available in JavaScript, but it can be implemented using predefined functions.

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 function REVERSE(string){
    return string.split("").reverse().join("");
}
```

##### Arguments

`string`: String expression to reverse.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION REVERSE(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.split("").reverse().join("");
$$;

SELECT REVERSE('rotator') PALINDROME;
```

##### Result

Copy code

```
      PALINDROME|      
----------------|
         rotator|
```

## STRING\_ESCAPE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Escapes special characters in texts and returns text with escaped characters. ([STRING\_ESCAPE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/string-escape-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
STRING_ESCAPE( text, type )
```

#### Arguments

`text`: Text to escape characters.

`type`: Format type to escape characters. Currently, JSON is the only format supported.

#### Return Type

`VARCHAR`.

### Examples

### Query

Copy code

```
:force:
SELECT STRING_ESCAPE('\   /  \\    "     ', 'json') AS [ESCAPE];
```

#### Result

Copy code

```
:force:
ESCAPE|
--------------------------|
  \\   \/  \\\\    \"     |
```

## stringify in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts an object to a JSON string format ([JavaScript stringify function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 JSON.stringify( value )
```

##### Arguments

`value`: Object expression to convert.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION string_escape (str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return JSON.stringify( STR );
$$;

SELECT STRING_ESCAPE('\   /  \\    "     ') ESCAPE;
```

##### Result

Copy code

```
:force:
                    ESCAPE|
--------------------------|
  \\   \/  \\\\    \"     |
```

## TRIM

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a character expression without blank spaces ([TRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
TRIM( string_expression )
```

#### Arguments

`string_expression:` String expressions to convert.

#### Return Type

`VARCHAR` or `NVARCHAR`

### Examples

### SQL Server

Copy code

```
:force:
SELECT TRIM('  FIRST AND LAST TWO BLANK SPACES  ') AS [TRIM];
```

**Output:**

Copy code

```
+-------------------------------|
|TRIM                           |
+-------------------------------|
|FIRST AND LAST TWO BLANK SPACES|
+-------------------------------|
```

#### Snowflake SQL

Copy code

```
:force:
SELECT TRIM('  FIRST AND LAST TWO BLANK SPACES  ') AS TRIM;
```

**Output:**

Copy code

```
+-------------------------------|
|TRIM                           |
+-------------------------------|
|FIRST AND LAST TWO BLANK SPACES|
+-------------------------------|
```

## trim in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Replaces the occurrences of a pattern using a new one sent as a parameter ([JavaScript Replace function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 String.trim( )
```

##### Arguments

This function does not receive any parameters.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION TRIM_STR(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.trim( );
$$;

SELECT TRIM_STR('  FIRST AND LAST TWO BLANK SPACES  ')TRIM
```

##### Result

Copy code

```
                           TRIM|      
-------------------------------|
FIRST AND LAST TWO BLANK SPACES|
```

## DIFFERENCE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns an integer measuring the difference between two strings using the SOUNDEX algorithm ([DIFFERENCE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/difference-transact-sql?view=sql-server-ver15)).  
It counts the common characters of the strings resulting by executing the SOUNDEX algorithm.

### Sample Source Pattern

### Syntax

Copy code

```
DIFFERENCE( expression1, expression1 )
```

#### Arguments

`expression1, expression2:` String expressions to be compared.

#### Return Type

`Int`.

### Examples

### Query

Copy code

```
:force:
SELECT DIFFERENCE('Like', 'Mike');
```

#### Result

Copy code

```
    Output |
-----------|
         3 |
```

## DIFFERENCE in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, this functionality is not available in JS, but this can be implemented easily.

Note

This functions requires the [SOUNDEX algorithm implementation](#soundex-in-js).

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 function DIFFERENCE(strA, strB) {
    var count = 0;
    for (var i = 0; i < strA.length; i++){
       if ( strA[i] == strB[i] ) count++; 
    }
    
    return count;
}
```

##### Arguments

`strA, strB`: String expressions resulting by executing the SOUNDEX algorithm.

##### Return Type

`String`.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION SOUNDEX_DIFFERENCE(str_1 varchar, str_2 varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function DIFFERENCE(strA, strB) {
      var count = 0;
      for (var i = 0; i < strA.length; i++){
         if ( strA[i] == strB[i] ) count++; 
      }
    
    return count;
    }
    
    return DIFFERENCE(STR_1, STR_2);
$$;

SELECT SOUNDEX_DIFFERENCE(GET_SOUNDEX('two'), GET_SOUNDEX('too')) DIFFERENCE;
```

##### Result

Copy code

```
   DIFFERENCE|
-------------|
            4|
```

## FORMAT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a value formatted with the specified format and optional culture ([FORMAT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/format-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
FORMAT( value, format [, culture])
```

#### Arguments

`value:` String expressions to give format.

format: Desired format.

culture (Optional): NVarchar argument specifying culture. If it is not specified, takes the languages of the current session.

#### Return Type

NULL if the culture parameter is invalid, otherwise, it follows the next data types:

| Category |  | .NET type |
| --- | --- | --- |
| Numeric | bigint | Int64 |
| Numeric | int | Int32 |
| Numeric | smallint | Int16 |
| Numeric | tinyint | Byte |
| Numeric | decimal | SqlDecimal |
| Numeric | numeric | SqlDecimal |
| Numeric | float | Double |
| Numeric | real | Single |
| Numeric | smallmoney | Decimal |
| Numeric | money | Decimal |
| Date and Time | date | DateTime |
| Date and Time | time | TimeSpan |
| Date and Time | datetime | DateTime |
| Date and Time | smalldatetime | DateTime |
| Date and Time | datetime2 | DateTime |
| Date and Time | datetimeoffset | DateTimeOffset |

Expand

Show lessSee more

### Examples

### Query

Copy code

```
:force:
SELECT FORMAT(CAST('2022-01-24' AS DATE), 'd', 'en-gb')  AS 'Great Britain';
```

#### Result

Copy code

```
  GREAT BRITAIN|
---------------|
     24/01/2022|
```

##### Query

Copy code

```
:force:
SELECT FORMAT(244900.25, 'C', 'cr-CR')  AS 'CURRENCY';
```

##### Result

| CURRENCY |
| --- |
| ₡244,900.25 |

Expand

Show lessSee more

### Date/Time Custom Format Specifiers

Many SQL Server custom date/time format specifiers are translated to their Snowflake `TO_CHAR` equivalents. Some specifiers have behavioral differences and are flagged with [SSC-FDM-0036](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0036).

#### Standard Single-Character Formats

These single-character formats expand to a full date/time pattern:

| SQL Server | Snowflake `TO_CHAR` Format | Example Output |
| --- | --- | --- |
| `d` | `MM/DD/YYYY` | `03/05/2025` |
| `D` | `DY, MMMM D, YYYY` | `Wed, March 5, 2025` |
| `t` | `HH12:MI PM` | `02:07 PM` |
| `T` | `HH12:MI:SS PM` | `02:07:03 PM` |
| `s` | `YYYY-MM-DD"T"HH24:MI:SS` | `2025-03-05T14:07:03` |
| `g` | `MM/DD/YYYY HH12:MI PM` | `03/05/2025 2:07 PM` |
| `G` | `MM/DD/YYYY HH12:MI:SS PM` | `03/05/2025 2:07:03 PM` |
| `y` / `Y` | `MMMM YYYY` | `March 2025` |
| `M` / `m` | `MMMM D` | `March 5` |

Expand

Show lessSee more

#### Custom Format Specifiers

These are building blocks for composite format strings (e.g., `MM/dd/yyyy HH:mm:ss`):

| SQL Server | Snowflake | Description |
| --- | --- | --- |
| `yyyy` | `YYYY` | 4-digit year |
| `yy` | `YY` | 2-digit year |
| `%y` / `y` | `Y` | Year without padding |
| `MMMM` | `MMMM` | Full month name |
| `MMM` | `MON` | Abbreviated month name |
| `MM` | `MM` | 2-digit month |
| `%M` / `M` | `MO` | Month without padding |
| `dd` | `DD` | 2-digit day |
| `ddd` | `DY` | Abbreviated day name |
| `%d` / `d` | `D` | Day without padding |
| `HH` | `HH24` | 24-hour padded |
| `%H` / `H` | `H24` | 24-hour without padding |
| `hh` | `HH12` | 12-hour padded |
| `%h` / `h` | `H12` | 12-hour without padding |
| `mm` | `MI` | Minutes padded |
| `%m` / `m` | `ME` | Minutes without padding |
| `ss` | `SS` | Seconds padded |
| `%s` / `s` | `S` | Seconds without padding |
| `tt` | `PM` | AM/PM designator |
| `t` | `P` | Single-char AM/PM (A or P) |
| `f`–`ffffff` | `F1`–`F6` | Fractional seconds (with trailing zeros) |

Expand

Show lessSee more

The following date/time specifiers are translated with an FDM marker:

| SQL Server Specifier | Description | Snowflake Equivalent | Behavioral Difference |
| --- | --- | --- | --- |
| `dddd` | Full day name | `DY` | Snowflake returns abbreviated day names (e.g., “Mon” vs “Monday”) |
| `F`–`FFFFFFF` | Fractional seconds (1–7 digits, no trailing zeros) | `F1`–`F7` | Snowflake always includes trailing zeros |
| `z` | UTC offset (hours only) | `TZH` | Formatting differences in offset representation |

Expand

Show lessSee more

#### Date/Time Conversion Example

##### Query

Copy code

```
:force:

SELECT FORMAT(CAST('12/12/2024' as datetime), 'dddd, MMMM dd yyyy HH:mm:ss.FFF');
```

##### Snowflake Equivalent

Copy code

```
:force:

SELECT
 TO_CHAR(TO_TIMESTAMP_NTZ('12/12/2024'), 'DY, MMMM DD YYYY HH24:MI:SS.F3') /*** SSC-FDM-0036 - TRANSFORMATION OF dddd, MMMM dd yyyy HH:mm:ss.FFF FORMAT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/;
```

#### Related Issues

1. [SSC-FDM-0036](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0036): The transformed date format may have a different behavior in Snowflake.
2. [SSC-EWI-0006](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0006): Generated for format specifiers that remain unsupported.

### Numeric Format Specifiers

SQL Server numeric format specifiers are translated to Snowflake `TO_CHAR` patterns:

| SQL Server Format | Snowflake `TO_CHAR` Format | Description |
| --- | --- | --- |
| `P` / `Pn` | `FM9,999,999,999,999.00%` | Percentage, multiplies by 100 (default 2 decimals) |
| `N` / `Nn` | `TM9(n,3)` | Number with thousand separators (default 2 decimals) |
| `#,#` | `TM9(0,3)` | Grouping, no zeros |
| `#,#.##` | `TM9(2,3)` | Grouping with optional decimals |
| `#,##0` | `FM99,990` | Grouping with minimum integer digit |
| `0.00` | `FM9999999999990.00` | Fixed decimal places |
| `0.00%` | `FM9999999999999.00%` | Percent suffix with fixed decimals |
| `#,#%` | `TM9(0,3)%` | Percent with grouping, no zeros |
| `#,#.##%` | `TM9(2,3)%` | Percent with grouping and decimals |

Expand

Show lessSee more

## FORMAT in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

There are different functions to format date and integer values in JavaScript. Unfortunately, these functionalities are not integrated into one method.

### DateTime values

#### Syntax

Copy code

```
:force: 

 Intl.DateTimeFormat( format ).format( value )
```

##### Arguments

`locales` (Optional): String expression of the format to apply.

`options` (Optional): Object with different supported properties for formats of numeric expressions ([JavaScript NumberFormat function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)).

`value`: Numeric expression to format.

##### Return Type

`String`.

### Numeric values

#### Syntax

Copy code

```
:force: 

 Intl.NumberFormat( [locales [, options]] ).format( value )
```

##### Arguments

`locales` (Optional): String expression of the format to apply.

`options` (Optional): Object with different supported properties for formats of numeric expressions ([JavaScript NumberFormat function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)).

`value`: Numeric expression to format.

##### Return Type

`String`.

### Examples

#### DateTime

##### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION format_date(date timestamp, format varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return new Intl.DateTimeFormat( FORMAT ).format( DATE );
$$;
SELECT FORMAT_DATE(TO_DATE('2022-01-24'), 'en-gb') GREAT_BRITAIN;
```

##### Result

Copy code

```
  GREAT_BRITAIN|      
---------------|
     24/01/2022|
```

#### Numeric

##### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION format_numeric(number float, locales varchar, options variant)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return new Intl.NumberFormat( LOCALES , OPTIONS ).format( NUMBER );
$$;
SELECT FORMAT_NUMERIC(244900.25, 'de-DE', PARSE_JSON('{ style: "currency", currency: "CRC" }')) CURRENCY;
```

##### Result

Copy code

```
       CURRENCY|      
---------------|
 244.900,25 CRC|
```

## PATINDEX

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the starting position of the first occurrence of a pattern in a specified expression ([PATINDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/patindex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
PATINDEX( pattern, expression )
```

#### Arguments

`pattern`: Pattern to find.

`expression`: Expression to search.

#### Return Type

Integer. Returns 0 if the pattern is not found.

### Examples

### Query

Copy code

```
:force:
SELECT PATINDEX( '%on%', 'No, no, non esistono più') AS [PATINDEX]
```

#### Result

Copy code

```
    PATINDEX|      
------------|
          10|
```

## search in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Finds the index of a pattern using REGEX ([JavaScript search function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/search)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 String.search( regex )
```

##### Arguments

`regex`: Regular expression which matches with the desired pattern.

##### Return Type

Integer. If the pattern does not match with any part of the string, returns -1.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION get_index_pattern(pattern varchar, str varchar)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  function GET_PATTERN(pattern, string){
    return string.search(new RegExp( pattern ));
    }
   return GET_PATTERN(PATTERN, STR) + 1;
$$;

SELECT GET_INDEX_PATTERN('on+', 'No, no, non esistono più') PATINDEX;
```

##### Result

Copy code

```
    PATINDEX|      
------------|
          10|
```

## STR

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns character data converted from numeric data. The character data is right-justified, with a specified length and decimal precision. ([STR in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/str-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

### Syntax

#### SQL Server

Copy code

```
STR ( float_expression [ , length [ , decimal ] ] )
```

##### Snowflake SQL

Copy code

```
:force:
STR_UDF( numeric_expression, number_format )
```

#### Arguments

`numeric_expression`: Float expression with a decimal point.

`length` (Optional): Length that the returning expression will have, including point notation, decimal, and float parts.

`decimal`(Optional): Is the number of places to the right of the decimal point.

#### Return Type

`VARCHAR`.

### Examples

### SQL Server

**Input:**

Copy code

```
:force:
/* 1 */
SELECT STR(123.5);

/* 2 */
SELECT STR(123.5, 2);

/* 3 */
SELECT STR(123.45, 6);

/* 4 */
SELECT STR(123.45, 6, 1);
```

**Output:**

Copy code

```
1) 124
2) **
3) 123
4) 123.5
```

#### Snowflake SQL

**Input:**

Copy code

```
:force:
/* 1 */
SELECT
PUBLIC.STR_UDF(123.5, '99999');

/* 2 */
SELECT
PUBLIC.STR_UDF(123.5, '99');

/* 3 */
SELECT
PUBLIC.STR_UDF(123.45, '999999');

/* 4 */
SELECT
PUBLIC.STR_UDF(123.45, '9999.9');
```

**Output:**

Copy code

```
1) 124

2) ##

3) 123
4) 123.5
```

## STR in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, this functionality is not available in JS, but it can be implemented easily using the predefined functions for strings.

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 function validLength(number, max_length, float_precision) {
  var float_point = number.match(/[\.][0-9]+/);
  /*if the number does not have point float, checks if the float precision 
   * and current number are greater than max_length
   */
   if(!float_point) return number.length + float_precision + 1 < max_length; 
    //removes the '.' and checks if there is overflow with the float_precision
    return number.length - float_point[0].trim('.').length + float_precision  < max_length;
} 
 function STR(number, max_length, float_precision) {
  var number_str = number.toString();
   //if the expression exceeds the max_length, returns '**'
   if(number_str.length > max_length || float_precision > max_length) return '**';
   if(validLength(number_str, max_length, float_precision)) {
      return number.toFixed(float_precision);
    }
    return number.toFixed(max_length - float_precision);
}
```

##### Arguments

`number`: Float expression with a decimal point.

`max_length`: Length that the returning expression will have, including point notation, decimal, and float parts.

`float_precision`: Is the number of places to the right of the decimal point.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION STR(number float, max_length float, float_precision float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function validLength(number, max_length, float_precision) {
        var float_point = number.match(/[\.][0-9]+/);
        if(!float_point) return number.length + float_precision + 1 < max_length; 
        return number.length - float_point[0].trim('.').length + float_precision  < max_length;
    } 
    function STR(number, max_length, float_precision) {
      var number_str = number.toString();
      if(number_str.length > max_length || float_precision > max_length) return '**';
      if(validLength(number_str, max_length, float_precision)) {
        return number.toFixed(float_precision);
      }
      return number.toFixed(max_length - float_precision);
    }
    return STR( NUMBER, MAX_LENGTH, FLOAT_PRECISION );
$$;

SELECT STR(12345.674, 12, 6);
```

##### Result

Copy code

```
           STR|
--------------|
  12345.674000|
```

## LTRIM

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a character expression after it removes leading blanks ([LTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ltrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
LTRIM( string_expression )
```

#### Arguments

`string_expression:` String expressions to convert.

#### Return Type

`VARCHAR` or `NVARCHAR`

### Examples

### Query

Copy code

```
:force:
SELECT LTRIM('  FIRST TWO BLANK SPACES') AS [LTRIM]
```

#### Result

Copy code

```
                 LTRIM|      
----------------------|
FIRST TWO BLANK SPACES|
```

## LTRIM in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, this function is not available in JavaScript, but it can be implemented using regular expressions.

### Sample Source Pattern

#### Implementation Example

Copy code

```
:force: 

 function LTRIM(string){
    return string.replace(/^s+/,"");
}
```

##### Arguments

`string`: String expression to remove blank spaces.

##### Return Type

String.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION ltrim(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  function LTRIM(string){
    return string.replace(/^s+/,"");
    }
   return LTRIM(S TR );
$$;

SELECT LTRIM('  FIRST TWO BLANK SPACES') AS LTRIM;
```

##### Result

Copy code

```
                 LTRIM|      
----------------------|
FIRST TWO BLANK SPACES|
```

## Ranking functions

This section describes the functional equivalents of ranking functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to their usage in stored procedures in Snowflake.

## DENSE\_RANK

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This function returns the rank of each row within a result set partition, with no gaps in the ranking values. The rank of a specific row is one plus the number of distinct rank values that come before that specific row. ([DENSE\_RANK in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/dense-rank-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

 DENSE_RANK ( ) OVER ( [ <partition_by_clause> ] < order_by_clause > )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/dense_rank.html)

Copy code

```
:force: 

 DENSE_RANK( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '15' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--              OVER ( [ <partition_by_clause> ] < order_by_clause > )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT TOP 10 BUSINESSENTITYID, NATIONALIDNUMBER, RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK FROM HUMANRESOURCES.EMPLOYEE AS TOTAL
```

**Result:**

Copy code

```
BUSINESSENTITYID|NATIONALIDNUMBER|DENSE_RANK|
----------------|----------------|----------|
              57|10708100        |         1|
              54|109272464       |         2|
             273|112432117       |         3|
               4|112457891       |         4|
             139|113393530       |         5|
             109|113695504       |         6|
             249|121491555       |         7|
             132|1300049         |         8|
             214|131471224       |         9|
              51|132674823       |        10|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT TOP 10
BUSINESSENTITYID,
NATIONALIDNUMBER,
RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK
FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

Copy code

```
BUSINESSENTITYID|NATIONALIDNUMBER|DENSE_RANK|
----------------|----------------|----------|
              57|10708100        |         1|
              54|109272464       |         2|
             273|112432117       |         3|
               4|112457891       |         4|
             139|113393530       |         5|
             109|113695504       |         6|
             249|121491555       |         7|
             132|1300049         |         8|
             214|131471224       |         9|
              51|132674823       |        10|
```

#### Related EWIs

- [SSC-EWI-0001](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001): Unrecognized token on the line of the source code.

## RANK

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the rank of each row within the partition of a result set. The rank of a row is one plus the number of ranks that come before the row in question. ([RANK in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rank-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

 RANK ( ) OVER ( [ partition_by_clause ] order_by_clause )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/rank.html)

Copy code

```
:force: 

 RANK( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '9' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--        OVER ( [ partition_by_clause ] order_by_clause )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT TOP 10 BUSINESSENTITYID, NATIONALIDNUMBER, RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK FROM HUMANRESOURCES.EMPLOYEE AS TOTAL
```

**Result:**

Copy code

```
BUSINESSENTITYID|NATIONALIDNUMBER|RANK|
----------------|----------------|----|
              57|10708100        |   1|
              54|109272464       |   2|
             273|112432117       |   3|
               4|112457891       |   4|
             139|113393530       |   5|
             109|113695504       |   6|
             249|121491555       |   7|
             132|1300049         |   8|
             214|131471224       |   9|
              51|132674823       |  10|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT TOP 10
BUSINESSENTITYID,
NATIONALIDNUMBER,
RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK
FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

Copy code

```
BUSINESSENTITYID|NATIONALIDNUMBER|RANK|
----------------|----------------|----|
              57|10708100        |   1|
              54|109272464       |   2|
             273|112432117       |   3|
               4|112457891       |   4|
             139|113393530       |   5|
             109|113695504       |   6|
             249|121491555       |   7|
             132|1300049         |   8|
             214|131471224       |   9|
              51|132674823       |  10|
```

#### Related EWIs

- [SSC-EWI-0001](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001): Unrecognized token on the line of the source code.

## ROW\_NUMBER

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Numbers the output of a result set. More specifically, returns the sequential number of a row within a partition of a result set, starting at 1 for the first row in each partition. ([ROW\_NUMBER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/row-number-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

 ROW_NUMBER ( )   
    OVER ( [ PARTITION BY value_expression , ... [ n ] ] order_by_clause )
```

##### Snowflake SQL

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/row_number.html)

Copy code

```
:force: 

 ROW_NUMBER( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '2' COLUMN '5' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--    OVER ( [ PARTITION BY value_expression , ... [ n ] ] order_by_clause )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT 
ROW_NUMBER() OVER(ORDER BY NAME  ASC) AS RowNumber, 
NAME
FROM HUMANRESOURCES.DEPARTMENT
```

**Output:**

Copy code

```
RowNumber|NAME                      |
---------|--------------------------|
        1|Document Control          |
        2|Engineering               |
        3|Executive                 |
        4|Facilities and Maintenance|
        5|Finance                   |
        6|Human Resources           |
        7|Information Services      |
        8|Marketing                 |
        9|Production                |
       10|Production Control        |
       11|Purchasing                |
       12|Quality Assurance         |
       13|Research and Development  |
       14|Sales                     |
       15|Shipping and Receiving    |
       16|Tool Design               |
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
ROW_NUMBER() OVER(ORDER BY NAME ASC) AS RowNumber,
NAME
FROM
HUMANRESOURCES.DEPARTMENT;
```

**Output:**

Copy code

```
RowNumber|NAME                      |
---------|--------------------------|
        1|Document Control          |
        2|Engineering               |
        3|Executive                 |
        4|Facilities and Maintenance|
        5|Finance                   |
        6|Human Resources           |
        7|Information Services      |
        8|Marketing                 |
        9|Production                |
       10|Production Control        |
       11|Purchasing                |
       12|Quality Assurance         |
       13|Research and Development  |
       14|Sales                     |
       15|Shipping and Receiving    |
       16|Tool Design               |
```

#### Related EWIs

- [SSC-EWI-0001](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001): Unrecognized token on the line of the source code.

## Logical functions

This section describes the functional equivalents of logical functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to their usage in stored procedures in Snowflake.

## IIF

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns one of two values, depending on whether the Boolean expression evaluates to true or false. ([IIF in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/logical-functions-iif-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
IIF( boolean_expression, true_value, false_value )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/iff.html)

Copy code

```
IFF( <condition> , <expr1> , <expr2> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT IIF( 2 > 3, 'TRUE', 'FALSE' ) AS RESULT
```

**Result:**

Copy code

```
RESULT|
------|
 FALSE|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
IFF( 2 > 3, 'TRUE', 'FALSE' ) AS RESULT;
```

**Result:**

Copy code

```
RESULT|
------|
 FALSE|
```

## XML Functions

This section describes the translation of XML functions in Transact-SQL to Snowflake SQL.

## Query

Applies to

- SQL Server

Warning

This transformation will be delivered in the future

### Description

Specifies an XQuery against an instance of the **xml** data type. The result is of **xml** type. The method returns an instance of untyped XML. ([`Query() in Transact-SQL`](https://learn.microsoft.com/en-us/sql/t-sql/xml/query-method-xml-data-type?view=sql-server-ver16))

### Sample Source Patterns

The following example details the transformation for .query( )

#### SQL Server

##### Input

Copy code

```
:force: 

 CREATE TABLE xml_demo(object_col XML);

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    xml_demo.object_col.query('/Root/ProductDescription/Features/Warranty') as Warranty,
    xml_demo.object_col.query('/Root/ProductDescription/Features/Maintenance') as Maintenance
from xml_demo;
```

##### Output

Copy code

```
 Warranty                                     | Maintenance                                                                          |
----------------------------------------------|--------------------------------------------------------------------------------------|
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
```

##### Snowflake SQL

##### Input

Copy code

```
:force: 

 CREATE OR REPLACE TABLE xml_demo (
    object_col VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Warranty') as Warranty,
    XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Maintenance') as Maintenance
from
    xml_demo;
```

##### Output

Copy code

```
 Warranty                                     | Maintenance                                                                          |
----------------------------------------------|--------------------------------------------------------------------------------------|
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0036](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.

## Value

Applies to

- SQL Server

Warning

This transformation will be delivered in the future

### Description

Performs an XQuery against the XML and returns a value of SQL type. This method returns a scalar value. ([`value() in Transact-SQL`](https://learn.microsoft.com/en-us/sql/t-sql/xml/value-method-xml-data-type?view=sql-server-ver16)).

### Sample Source Patterns

The following example details the transformation for .value( )

#### SQL Server

##### Input

Copy code

```
:force: 

 CREATE TABLE xml_demo(object_col XML);

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    xml_demo.object_col.value('(/Root/ProductDescription/@ProductID)[1]', 'int' ) as ID,
    xml_demo.object_col.value('(/Root/ProductDescription/@ProductName)[1]', 'varchar(max)' ) as ProductName,
    xml_demo.object_col.value('(/Root/ProductDescription/Features/Warranty)[1]', 'varchar(max)' ) as Warranty
from xml_demo;
```

##### Output

Copy code

```
 ID | ProductName | Warranty               |
----|-------------|------------------------|
1   | Road Bike   | 1 year parts and labor |
2   | Skate       | 1 year parts and labor |
```

##### Snowflake SQL

##### Input

Copy code

```
:force: 

 CREATE OR REPLACE TABLE xml_demo (
    object_col VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    GET(XMLGET(object_col, 'ProductDescription'), '@ProductID') :: INT as ID,
    GET(XMLGET(object_col, 'ProductDescription'), '@ProductName') :: VARCHAR as ProductName,
    GET(XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Warranty', 0), '$') :: VARCHAR as Warranty
from
    xml_demo;
```

##### Output

Copy code

```
 ID | PRODUCTNAME | WARRANRTY              |
----|-------------|------------------------|
1   | Road Bike   | 1 year parts and labor |
2   | Skate       | 1 year parts and labor |
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0036](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.

## Aggregate functions

This section describes the functional equivalents of aggregate functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## COUNT

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This function returns the number of items found in a group. COUNT operates like the COUNT\_BIG function. These functions differ only in the data types of their return values. COUNT always returns an int data type value. COUNT\_BIG always returns a bigint data type value. ([COUNT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
COUNT ( { [ [ ALL | DISTINCT ] expression ] | * } )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

Copy code

```
:force:
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT COUNT(NATIONALIDNUMBER) FROM HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

| TOTAL |
| --- |
| 290 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
COUNT(NATIONALIDNUMBER) FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

| TOTAL |
| --- |
| 290 |

Expand

Show lessSee more

## COUNT\_BIG

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This function returns the number of items found in a group. COUNT\_BIG operates like the COUNT function. These functions differ only in the data types of their return values. COUNT\_BIG always returns a bigint data type value. COUNT always returns an int data type value. ([COUNT\_BIG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/count-big-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
COUNT_BIG ( { [ [ ALL | DISTINCT ] expression ] | * } )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

Copy code

```
:force:
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT COUNT_BIG(NATIONALIDNUMBER) FROM HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

| TOTAL |
| --- |
| 290 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
COUNT(NATIONALIDNUMBER) FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

| TOTAL |
| --- |
| 290 |

Expand

Show lessSee more

## SUM

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Returns the sum of all the values, or only the DISTINCT values, in the expression. SUM can be used with numeric columns only. Null values are ignored. ([SUM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sum-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
SUM ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/sum.html)

Copy code

```
:force:
SUM( [ DISTINCT ] <expr1> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT SUM(VACATIONHOURS) FROM HUMANRESOURCES.EMPLOYEE AS TOTALVACATIONHOURS;
```

**Result:**

| TOTALVACATIONHOURS |
| --- |
| 14678 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
SUM(VACATIONHOURS) FROM
HUMANRESOURCES.EMPLOYEE AS TOTALVACATIONHOURS;
```

**Result:**

| TOTALVACATIONHOURS |
| --- |
| 14678 |

Expand

Show lessSee more

## Custom UDFs

### Description

Some Transact-SQL functions or behaviors may not be available or may behave differently in Snowflake. To minimize these differences, some functions are replaced with Custom UDFs.

These UDFs are automatically created during migration, in the `UDF Helper` folder, inside the `Output` folder. There is one file per custom UDF.

## OPENXML UDF

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

This custom UDF is added to process a rowset view over an XML document. This would be used for declarations in because it works as a rowset provider.

[Optional parameters](https://learn.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql?view=sql-server-ver16#remarks) and different node types are not supported in this version of the UDF. The element node is processed by default.

### Custom UDF overloads

**Parameters**

1. **XML**: A `VARCHAR` that represents the readable content of the XML.
2. **PATH**: A varchar that contains the pattern of the nodes to be processed as rows.

#### UDF

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION OPENXML_UDF(XML VARCHAR, PATH VARCHAR)
RETURNS TABLE(VALUE VARIANT)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT VALUE from TABLE(FLATTEN(input=>XML_JSON_SIMPLE(PARSE_XML(XML)), path=>PATH))
$$;

CREATE OR REPLACE FUNCTION XML_JSON_SIMPLE(XML VARIANT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
function toNormalJSON(xmlJSON) {
    var finalres = {};
    var name=xmlJSON['@'];
    var res = {};
    finalres[name] = res;
    for(var key in xmlJSON)
    {
        if (key == "@")
        {
            res["$name"] = xmlJSON["@"];
        }
        else if (key == "$") {
            continue;
        }
        else if (key.startsWith("@"))
        {
            // This is an attribute
            res[key]=xmlJSON[key];
        }
        else
        {
            var elements = xmlJSON['$']
            var value = xmlJSON[key];
            res[key] = [];
            if (Array.isArray(value))
            {
                for(var elementKey in value)
                {
                    var currentElement = elements[elementKey];
                    var fixedElement = toNormalJSON(currentElement);
                    res[key].push(fixedElement);
                }
            }
            else if (value === 0)
            {
                var fixedElement = toNormalJSON(elements);
                res[key].push(fixedElement);
            }
        }
    }
    return finalres;
}
return toNormalJSON(XML);
$$;
```

##### Transact-SQL

##### Query

Copy code

```
:force: 

DECLARE @idoc INT, @doc VARCHAR(1000);  
SET @doc ='  
<ROOT>  
<Customer CustomerID="VINET" ContactName="Paul Henriot">  
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">  
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>  
      <OrderDetail OrderID="10248" ProductID="42" Quantity="10"/>  
   </Order>  
</Customer>  
<Customer CustomerID="LILAS" ContactName="Carlos Gonzlez">  
   <Order CustomerID="LILAS" EmployeeID="3" OrderDate="1996-08-16T00:00:00">  
      <OrderDetail OrderID="10283" ProductID="72" Quantity="3"/>  
   </Order>  
</Customer>  
</ROOT>';  

EXEC sp_xml_preparedocument @idoc OUTPUT, @doc;  
 
SELECT *  FROM OPENXML (@idoc, '/ROOT/Customer',1)  
WITH (CustomerID  VARCHAR(10), ContactName VARCHAR(20));
```

##### Result

Copy code

```
CustomerID  | ContactName
----------------------------|
VINET     | Paul Henriot
LILAS     | Carlos Gonzlez
```

##### Snowflake

Note

The following example is isolated into a stored procedure because environment variables only support 256 bytes of storage, and the XML demo code uses more than that limit.

##### Query

Copy code

```
:force: 

DECLARE
IDOC INT;
DOC VARCHAR(1000);
BlockResultSet RESULTSET;
BEGIN
DOC := '  
<ROOT>  
<Customer CustomerID="VINET" ContactName="Paul Henriot">  
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">  
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>  
      <OrderDetail OrderID="10248" ProductID="42" Quantity="10"/>  
   </Order>  
</Customer>  
<Customer CustomerID="LILAS" ContactName="Carlos Gonzlez">  
   <Order CustomerID="LILAS" EmployeeID="3" OrderDate="1996-08-16T00:00:00">  
      <OrderDetail OrderID="10283" ProductID="72" Quantity="3"/>  
   </Order>  
</Customer>  
</ROOT>';
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0075 - TRANSLATION FOR BUILT-IN PROCEDURE 'sp_xml_preparedocument' IS NOT CURRENTLY SUPPORTED. ***/!!!

EXEC sp_xml_preparedocument :IDOC OUTPUT, :DOC;
BlockResultSet := (

SELECT
Left(value:Customer['@CustomerID'], '10') AS 'CustomerID',
Left(value:Customer['@ContactName'], '20') AS 'ContactName'
FROM
OPENXML_UDF(:IDOC, ':ROOT:Customer'));
RETURN TABLE(BlockResultSet);
END;
```

##### Result

| CustomerID | ContactName |
| --- | --- |
| VINET | Paul Henriot |
| LILAS | Carlos Gonzlez |

Expand

Show lessSee more

##### Query

Copy code

```
:force: 

SET code = '<ROOT>  
<Customer CustomerID="VINET" ContactName="Paul Henriot">  
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">  
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>  
   </Order>  
</Customer>  
</ROOT>';
SELECT
Left(value:Customer['@CustomerID'],10) as "CustomerID",  
Left(value:Customer['@ContactName'],20) as "ContactName"
FROM TABLE(OPENXML_UDF($code,'ROOT:Customer'));
```

##### Result

| CustomerID | ContactName |
| --- | --- |
| VINET | Paul Henriot |

Expand

Show lessSee more

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-TS0075](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0075): Built In Procedure Not Supported.

## STR UDF

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This custom UDF converts numeric data to character data.

### Custom UDF overloads

#### Parameters

1. **FLOAT\_EXPR**: A numeric expression to be converted to varchar.
2. **FORMAT**: A varchar expression with the length and number of decimals of the resulting varchar. This format is automatically generated.

##### UDF

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION PUBLIC.STR_UDF(FLOAT_EXPR FLOAT, FORMAT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    TRIM(TRIM(SELECT TO_CHAR(FLOAT_EXPR, FORMAT)), '.')
$$;

CREATE OR REPLACE FUNCTION PUBLIC.STR_UDF(FLOAT_EXPR FLOAT)
RETURNS VARCHAR
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    STR_UDF(FLOAT_EXPR, '999999999999999999')
$$;
```

##### Transact-SQL

##### Query

Copy code

```
:force: 

SELECT
    STR(123.5) as A,
    STR(123.5, 2) as B,
    STR(123.45, 6) as C,
    STR(123.45, 6, 1) as D;
```

##### Result

| A | B | C | D |
| --- | --- | --- | --- |
| 124 | \*\* | 123 | 123.5 |

Expand

Show lessSee more

##### Snowflake

##### Query

Copy code

```
:force: 

SELECT
    PUBLIC.STR_UDF(123.5, '99999') as A,
    PUBLIC.STR_UDF(123.5, '99') as B,
    PUBLIC.STR_UDF(123.45, '999999') as C,
    PUBLIC.STR_UDF(123.45, '9999.9') as D;
```

## SWITCHOFFSET\_UDF

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This custom UDF is added to return a datetimeoffset value that is changed from the stored time zone offset to a specified new time zone offset.

### Custom UDF overloads

**Parameters**

1. **source\_timestamp**: A TIMESTAMP\_TZ that can be resolved to a datetimeoffset(n) value.
2. **target\_tz**: A varchar that represents the time zone offset

#### UDF

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION PUBLIC.SWITCHOFFSET_UDF(source_timestamp TIMESTAMP_TZ, target_tz varchar)
RETURNS TIMESTAMP_TZ
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS 
$$
WITH tz_values AS (
SELECT 
    RIGHT(source_timestamp::varchar, 5) as source_tz,
    
    REPLACE(source_tz::varchar, ':', '') as source_tz_clean,
    REPLACE(target_tz::varchar, ':', '') as target_tz_clean,
    
    target_tz_clean::integer - source_tz_clean::integer as offset,
    
    RIGHT(offset::varchar, 2) as tz_min,
    PUBLIC.OFFSET_FORMATTER(RTRIM(offset::varchar, tz_min)) as tz_hrs,
    
    
    TIMEADD( hours, tz_hrs::integer, source_timestamp ) as adj_hours,
    TIMEADD( minutes, (LEFT(tz_hrs, 1) || tz_min)::integer, adj_hours::timestamp_tz ) as new_timestamp
    
FROM DUAL)
SELECT 
    (LEFT(new_timestamp, 24) || ' ' || target_tz)::timestamp_tz
FROM tz_values
$$;

-- ==========================================================================
-- Description: The function OFFSET_FORMATTER(offset_hrs varchar) serves as
-- an auxiliary function to format the offset hours and its prefix operator.
-- ==========================================================================  
CREATE OR REPLACE FUNCTION PUBLIC.OFFSET_FORMATTER(offset_hrs varchar)
RETURNS varchar
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
CASE
   WHEN LEN(offset_hrs) = 0 THEN '+' || '0' || '0'
   WHEN LEN(offset_hrs) = 1 THEN '+' || '0' || offset_hrs
   WHEN LEN(offset_hrs) = 2 THEN
        CASE 
            WHEN LEFT(offset_hrs, 1) = '-' THEN '-' || '0' || RIGHT(offset_hrs, 1)
            ELSE '+' || offset_hrs
        END
    ELSE offset_hrs
END
$$;
```

##### Transact-SQL

##### Query

Copy code

```
:force: 

SELECT 
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Result

Copy code

```
SELECT 
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Snowflake

##### Query

Copy code

```
:force: 

SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  PUBLIC.SWITCHOFFSET_UDF('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Result

| fr\_time | cr\_time |
| --- | --- |
| 1998-09-20 7:45:50.71345 +02:00 | 1998-09-19 23:45:50.7134500 -06:00 |

Expand

Show lessSee more

## Metadata functions

This section describes the functional equivalents of metadata functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to their usage in stored procedures in Snowflake.

## DB\_NAME

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the name of a specified database.([DB\_NAME in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

 DB_NAME ( [ database_id ] )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/current_database.html)

Copy code

```
:force: 

 CURRENT_DATABASE() /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DB_NAME();
```

**Result:**

| RESULT |
| --- |
| ADVENTUREWORKS2019 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CURRENT_DATABASE() /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/;
```

**Result:**

| RESULT |
| --- |
| ADVENTUREWORKS2019 |

Expand

Show lessSee more

### Known issues

**1. CURRENT\_DATABASE function has different behavior in certain cases**

DB\_NAME function can be invoked with the **database\_id** parameter, which returns the name of the specified database. Without parameters, the function returns the current database name. However, Snowflake does not support this parameter and the CURRENT\_DATABASE function will always return the current database name.

### Related EWIs

1. [SSC-FDM-TS0010](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0010): CURRENT\_DATABASE function has different behavior in certain cases.

## OBJECT\_ID

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the database object identification number of a schema-scoped object.[(OBJECT\_ID in Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/object-id-transact-sql?view=sql-server-ver16).

#### SQL Server syntax

Copy code

```
:force: 

 OBJECT_ID ( '[ database_name . [ schema_name ] . | schema_name . ]   
  object_name' [ ,'object_type' ] )
```

### Sample Source Patterns

#### 1. Default transformation

##### SQL Server

Copy code

```
:force: 

 IF OBJECT_ID_UDF('DATABASE2.DBO.TABLE1') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL

Copy code

```
:force: 

 BEGIN
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '0' OF THE SOURCE CODE STARTING AT 'IF'. EXPECTED 'If Statement' GRAMMAR. LAST MATCHING TOKEN WAS 'null' ON LINE '1' COLUMN '48'. FAILED TOKEN WAS ')' ON LINE '1' COLUMN '52'. CODE '70'. **
--IF OBJECT_ID_UDF('DATABASE2.DBO.TABLE1') is not null) THEN
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
DROP TABLE IF EXISTS TABLE1;
END;
```

#### 2. Unknown database

##### SQL Server

Copy code

```
:force: 

 IF OBJECT_ID_UDF('DATABASE1.DBO.TABLE1') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL

Copy code

```
:force: 

  IF (
 OBJECT_ID_UDF('DATABASE1.DBO.TABLE1') is not null) THEN
     DROP TABLE IF EXISTS TABLE1;
 END IF;
```

#### 3. Different object names

##### SQL Server

Copy code

```
:force: 

 IF OBJECT_ID_UDF('DATABASE1.DBO.TABLE2') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL

Copy code

```
:force: 

  IF (
 OBJECT_ID_UDF('DATABASE1.DBO.TABLE2') is not null) THEN
     DROP TABLE IF EXISTS TABLE1;
 END IF;
```

### Known issues

**1. OBJECT\_ID\_UDF function has different behavior in certain cases**

OBJECT\_ID returns the object identification number but the OBJECT\_ID\_UDF returns a boolean value, so that they are equivalent only when OBJECT\_ID is used with not null condition.

### Related EWIs

- [SSC-EWI-0001](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001): Unrecognized token on the line of the source code.
- [SSC-FDM-0007](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007): Element with missing dependencies

## Analytic Functions

This section describes the functional equivalents of analytic functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## LAG

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Accesses data from a previous row in the same result set without the use of a self-join starting with SQL Server 2012 (11.x).
LAG provides access to a row at a given physical offset that comes before the current row.
Use this analytic function in a SELECT statement to compare values in the current row with values in a previous row. ([COUNT in Transact-SQL](#lag)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
LAG (scalar_expression [,offset] [,default])  
    OVER ( [ partition_by_clause ] order_by_clause )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

Copy code

```
:force:
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT TOP 10 
LAG(E.VacationHours,1) OVER(ORDER BY E.NationalIdNumber) as PREVIOUS,
E.VacationHours AS ACTUAL 
FROM HumanResources.Employee E
```

**Result:**

| PREVIOUS | ACTUAL |
| --- | --- |
| NULL | 10 |
| 10 | 89 |
| 89 | 10 |
| 10 | 48 |
| 48 | 0 |
| 0 | 95 |
| 95 | 55 |
| 55 | 67 |
| 67 | 84 |
| 84 | 85 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT TOP 10
LAG(E.VacationHours,1) OVER(ORDER BY E.NationalIdNumber) as PREVIOUS,
E.VacationHours AS ACTUAL
FROM
HumanResources.Employee E;
```

**Result:**

| PREVIOUS | ACTUAL |
| --- | --- |
| NULL | 10 |
| 10 | 89 |
| 89 | 10 |
| 10 | 48 |
| 48 | 0 |
| 0 | 95 |
| 95 | 55 |
| 55 | 67 |
| 67 | 84 |
| 84 | 85 |

Expand

Show lessSee more

## Data Type functions

This section describes the functional equivalents of data type functions in Transact-SQL to Snowflake SQL and JavaScript code.

## DATALENGTH

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the number of bytes used to represent any expression. ([DATALENGTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datalength-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
DATALENGTH ( expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/cast.html)

Copy code

```
:force: 
OCTET_LENGTH(<string_or_binary>)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATALENGTH('SomeString') AS SIZE;
```

**Result:**

| SIZE |
| --- |
| 10 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT OCTET_LENGTH('SomeString') AS SIZE;
```

**Result:**

| SIZE |
| --- |
| 10 |

Expand

Show lessSee more

## Mathematical functions

This section describes the functional equivalents of mathematical functions in Transact-SQL to Snowflake SQL and JavaScript code, oriented to their usage in stored procedures in Snowflake.

## ABS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

A mathematical function that returns the absolute (positive) value of the specified numeric expression. (`ABS` changes negative values to positive values. `ABS` has no effect on zero or positive values.) ([ABS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
ABS( expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/abs.html)

Copy code

```
:force: 
ABS( <num_expr> )
```

##### JavaScript

[JavaScript complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/abs)

Copy code

```
:force: 
Math.abs( expression )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT ABS(-5);
```

**Result:**

| ABS(-5) |
| --- |
| 5 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT ABS(-5);
```

**Result:**

| ABS(-5) |
| --- |
| 5 |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_abs(a float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.abs(A);
$$
;
SELECT COMPUTE_ABS(-5);
```

**Result:**

| COMPUTE\_ABS(-5) |
| --- |
| 5 |

Expand

Show lessSee more

### Related Documentation

- [Transact-SQL supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## AVG

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Note

SnowConvert AI Helpers Code section is omitted.

This function returns the average of the values in a group. It ignores null values. ([AVG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/avg-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
AVG ( [ ALL | DISTINCT ] expression )  
   [ OVER ( [ partition_by_clause ] order_by_clause ) ]
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/avg.html)

Copy code

```
:force: 
AVG( [ DISTINCT ] <expr1> )

AVG( [ DISTINCT ] <expr1> ) OVER (
                                 [ PARTITION BY <expr2> ]
                                 [ ORDER BY <expr3> [ ASC | DESC ] [ <window_frame> ] ]
                                 )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT AVG(VACATIONHOURS) AS AVG_VACATIONS FROM HUMANRESOURCES.EMPLOYEE;
```

**Result:**

| AVG\_VACATIONS |
| --- |
| 50 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT AVG(VACATIONHOURS) AS AVG_VACATIONS FROM HUMANRESOURCES.EMPLOYEE;
```

**Result:**

| AVG\_VACATIONS |
| --- |
| 50 |

Expand

Show lessSee more

## CEILING

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

A mathematical function that returns the smallest greater integer greater/equal to the number sent as a parameter ([CEILING in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ceiling-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

CEILING( expression )
```

##### Snowflake SQL

Copy code

```
:force: 

CEIL( <input_expr> [, <scale_expr> ] )
```

##### JavaScript

Copy code

```
:force: 

 Math.ceil( expression )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CEILING(642.20);
```

**Result:**

| CEILING(642.20) |
| --- |
| 643 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT CEIL(642.20);
```

**Result:**

| CEIL(642.20) |
| --- |
| 643 |

Expand

Show lessSee more

##### JavaScript

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_ceil(a double)
RETURNS double
LANGUAGE JAVASCRIPT
AS
$$
  return Math.ceil(A);
$$
;
SELECT COMPUTE_CEIL(642.20);
```

**Result:**

Copy code

```
COMPUTE_CEIL(642.20)|
--------------------|
                 643|
```

## FLOOR

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the largest integer less than or equal to the specified numeric expression. ([FLOOR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/floor-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
FLOOR ( numeric_expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/floor.html)

Copy code

```
FLOOR( <input_expr> [, <scale_expr> ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT FLOOR (124.87) AS FLOOR;
```

**Result:**

Copy code

```
FLOOR|
-----|
  124|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT FLOOR (124.87) AS FLOOR;
```

**Result:**

Copy code

```
FLOOR|
-----|
  124|
```

## POWER

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the value of the specified expression to the specified power. ([POWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
POWER ( float_expression , y )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/pow.html)

Copy code

```
POW(x, y)

POWER (x, y)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT POWER(2, 10.0) AS IntegerResult
```

**Result:**

Copy code

```
IntegerResult |
--------------|
          1024|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT POWER(2, 10.0) AS IntegerResult;
```

**Result:**

Copy code

```
IntegerResult |
--------------|
          1024|
```

### Related Documentation

- [SQL Server supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## ROUND

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a numeric value, rounded to the specified length or precision. ([ROUND in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/round-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
ROUND ( numeric_expression , length [ ,function ] )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/round.html)

Copy code

```
ROUND( <input_expr> [, <scale_expr> ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT ROUND(123.9994, 3) AS COL1, ROUND(123.9995, 3) AS COL2;
```

**Result:**

Copy code

```
COL1    |COL2    |
--------|--------|
123.9990|124.0000|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT ROUND(123.9994, 3) AS COL1,
ROUND(123.9995, 3) AS COL2;
```

**Result:**

Copy code

```
COL1   | COL2  |
--------|------|
123.999|124.000|
```

### Related Documentation

- [SQL Server supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## SQRT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the square root of the specified float value. ([SQRT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sqrt-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
SQRT ( float_expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/sqrt.html)

Copy code

```
SQRT(expr)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT SQRT(25) AS RESULT;
```

**Result:**

Copy code

```
RESULT|
------|
   5.0|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT SQRT(25) AS RESULT;
```

**Result:**

Copy code

```
RESULT|
------|
   5.0|
```

## SQUARE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the square of the specified float value. ([SQUARE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/square-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
SQUARE ( float_expression )  ****
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/square.html)

Copy code

```
SQUARE(expr)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT SQUARE (5) AS SQUARE;
```

**Result:**

Copy code

```
SQUARE|
------|
  25.0|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT SQUARE (5) AS SQUARE;
```

**Result:**

Copy code

```
SQUARE|
------|
    25|
```

## STDEV

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Returns the statistical standard deviation of all values in the specified expression. ([STDEV in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 

 STDEV ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/stddev.html)

Copy code

```
:force: 

 STDDEV( [ DISTINCT ] <expression_1> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT
    STDEV(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS STDEV;
```

**Result:**

Copy code

```
           STDEV|
----------------|
28.7862150320948|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
    STDDEV(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS STDEV;
```

**Result:**

Copy code

```
       STDEV|
------------|
28.786215034|
```

## STDEVP

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Returns the statistical standard deviation for the population for all values in the specified expression. ([STDVEP in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
STDEVP ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop.html)

Copy code

```
STDDEV_POP( [ DISTINCT ] expression_1)
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT
    STDEVP(VACATIONHOURS) AS STDEVP_VACATIONHOURS
FROM
    HumanResources.Employee;
```

**Result:**

Copy code

```
STDEVP_VACATIONHOURS|
--------------------|
  28.736540767245085|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
    STDDEV_POP(VACATIONHOURS) AS STDEVP_VACATIONHOURS
FROM
    HumanResources.Employee;
```

**Result:**

Copy code

```
STDEVP_VACATIONHOURS|
--------------------|
        28.736540763|
```

## VAR

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Returns the statistical variance of all values in the specified expression. ([VAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/var-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
VAR ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL

Copy code

```
VAR_SAMP( [DISTINCT] <expr1> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT
    VAR(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS VAR;
```

**Result:**

Copy code

```
             VAR|
----------------|
28.7862150320948|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
    VAR_SAMP(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS VAR;
```

**Result:**

Copy code

```
       VAR|
----------|
828.646176|
```

## POWER

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the value of the specified expression for a specific power.  
([POWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
POWER( base, exp )
```

#### Arguments

`base`: Base of number, it must be a float expression.  
`exp`: Power to which raise the base.

#### Return Type

The return type depends on the input expression:

| Input Type | Return Type |
| --- | --- |
| float, real | float |
| decimal(p, s) | decimal(38, s) |
| int, smallint, tinyint | int |
| bigint | bigint |
| money, smallmoney | money |
| bit, char, nchar, varchar, nvarchar | float |

### Examples

### Query

Copy code

```
:force:
SELECT POWER(2, 3)
```

#### Result

Copy code

```
POWER(2, 3)|
-----------|
        8.0|
```

## POW in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the base of the exponent power.  
([JavaScript POW function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.pow( base, exp )
```

##### Arguments

`base`: Base of number, it must be a float expression.  
`exp`: Power to which raise the base.

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION compute_pow(base float, exp float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
    return Math.pow(BASE, EXP);
$$
;
SELECT COMPUTE_POW(2, 3);
```

##### Result

Copy code

```
COMPUTE_POW(2, 3)|
-----------------|
                8|
```

## ACOS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arccosine in radians of the number sent as a parameter ([ACOS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/acos-transact-sql?view=sql-server-ver15)).

Mathematically, the arccosine is the inverse function of the cosine, resulting in the following definition:  
`y = cos^{-1} \Leftrightarrow x = cos(y)`

For `y = cos^{-1}(x)`:  
- Range: `0\leqslant y \leqslant \pi` or `0^{\circ}\leqslant y \leqslant 180^{\circ}`  
- Domain: `-1\leqslant x \leqslant 1`

### Sample Source Pattern

### Syntax

Copy code

```
:force:
ACOS ( expression )
```

#### Arguments

`expression`: Numeric **float** expression, where expression is in`[-1,1]`.

#### Return Type

Numeric float expression between 0 and π. If the numeric expression sent by parameter is out of the domain `[-1, 1]`, the database engine throws an error.

### Examples

### Query

Copy code

```
:force:
SELECT ACOS(-1.0);
```

#### Result

Copy code

```
ACOS(-1.0)       |
-----------------|
3.141592653589793|
```

## ACOS in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arccosine of a specified number  
([JavaScript ACOS function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/acos)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.acos( expression )
```

##### Arguments

`expression`: Numeric expression, where expression is in`[-1,1]`.

##### Return Type

Numeric expression between 0 and π. If the numeric expression sent by parameter is out of the range of the arccosine in radians `[-1, 1]`, the function returns NaN.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION compute_acos(a double)
  RETURNS double
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.acos(A);
$$
;
SELECT COMPUTE_ACOS(-1);
```

##### Result

Copy code

```
COMPUTE_ACOS(-1)|
---------------|
    3.141592654|
```

## ASIN

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arcsine in radians of the number sent as parameter ([ASIN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/asin-transact-sql?view=sql-server-ver15)).

The arcsine is the inverse function of the sine , summarized in the next definition:  
`y = sin^{-1} \Leftrightarrow x = sin(x)`

For `y = sin^{-1}(x)`:  
- Range: `-\frac{\pi}{2}\leqslant y \leqslant \frac{\pi}{2}` or `-90^{\circ}\leqslant y \leqslant 90^{\circ}`  
- Domain: `-1\leqslant x \leqslant 1`

### Sample Source Pattern

### Syntax

Copy code

```
:force:
ASIN( expression )
```

#### Arguments

`expression`: Numeric **float** expression, where expression is in`[-1,1]`.

#### Return Type

Numeric float expression between `-\frac{\pi}{2}` and `\frac{\pi}{2}`. If the numeric expression sent by parameter is not in `[-1, 1]`, the database engine throws an error.

### Examples

### Query

Copy code

```
:force:
SELECT ASIN(0.5);
```

#### Result

Copy code

```
ASIN(0.5)         |
------------------|
0.5235987755982989|
```

## ASIN in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arcsine of a specified number  
([JavaScript ASIN function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/asin)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.asin( expression )
```

##### Arguments

`expression`: Numeric expression, where expression is in`[-1,1]`.

##### Return Type

Numeric expression between `-\frac{\pi}{2}` and `\frac{\pi}{2}`. If the numeric expression sent by parameter is out of the domain of the arccosine `[-1, 1]`, the function returns NaN.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION compute_asin(a float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.asin(A);
$$
;
SELECT COMPUTE_ASIN(0.5);
```

##### Result

Copy code

```
COMPUTE_ASIN(1)   |
------------------|
      0.5235987756|
```

## COS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the cosine of the angle sent through parameters (must be measured in radians) ([COS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cos-transact-sql?view=sql-server-ver15)).

The cosine is defined as:  
`y = cos(x)`  
Where:  
- Range: `-1\leqslant y \leqslant 1`  
- Domain: `\mathbb{R}`

### Sample Source Pattern

### Syntax

Copy code

```
:force:
COS( expression )
```

#### Arguments

`expression`: Numeric **float** expression, where expression is in `\mathbb{R}`.

#### Return Type

Numeric float expression in `[-1, 1]`.

### Examples

### Query

Copy code

```
:force:
SELECT COS(PI())
```

#### Result

Copy code

```
COS(PI())|
---------|
     -1.0|
```

## COS in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Static function that returns the cosine of an angle in radians  
([JavaScript COS function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/cos)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.cos( expression )
```

##### Arguments

`expression:` Numeric expressions.

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_cos(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.cos(ANGLE); 
$$
;
SELECT COMPUTE_COS(PI());
```

##### Result

Copy code

```
COMPUTE_COS(PI())|
-----------------|
               -1|
```

## COT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the cotangent of the angle in radians sent through parameters ([COT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cot-transact-sql?view=sql-server-ver15)).

The cosine is defined as:  
`cot(x) = \frac{cos(x)}{sin(x)}` or `cot(x) = \frac{1}{tan(x)}`  
To calculate the cosine, the parameter must comply with the constraints of sine and [cosine](#cos) functions.

### Sample Source Pattern

### Syntax

Copy code

```
:force:
COT( expression )
```

#### Arguments

`expression`: Numeric **float** expression, where expression is in `\mathbb{R}-\{sin(expression)=0 \wedge tan(expression) =0\}`.

#### Return Type

Numeric float expression in `\mathbb{R}`.

### Examples

### Query

Copy code

```
:force:
SELECT COT(1)
```

#### Result

Copy code

```
COT(1)            |
------------------|
0.6420926159343306|
```

## COT in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Unfortunately, the object `Math`in JavaScript does not provide a method to calculate the cotangent of a given angle.  
This could be calculated using the equation: `cot(x) = \frac{cos(x)}{sin(x)}`

### Sample Source Pattern

#### Implementation example

Copy code

```
:force: 

 function cot(angle){
    return Math.cos(angle)/Math.sin(angle);
}
```

##### Arguments

`angle:` Numeric expression in radians.

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_cot(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function cot(angle){
    return Math.cos(angle)/Math.sin(angle);
  }
  return cot(ANGLE);
    
$$
;
SELECT COMPUTE_COT(1);
```

##### Result

Copy code

```
COMPUTE_COT(1);   |
------------------|
0.6420926159343308|
```

## RADIANS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts degrees to radians.  
([RADIANS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/radians-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
RADIANS( expression )
```

#### Arguments

`expression`: Numeric expression in degrees.

#### Return Type

Same data type sent through parameter as a numeric expression in radians.

### Examples

### Query

Copy code

```
:force:
SELECT RADIANS(180.0)
```

#### Result

| RADIANS(180) |
| --- |
| 3.141592653589793116 |

Expand

Show lessSee more

Note

Cast the parameter of this function to float, otherwise, the above statement will return 3 instead of PI value.

## RADIANS in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

JavaScript does not provide a method to convert degrees to radians of a given angle.  
This could be calculated using the equation: `Radians = \frac{\pi}{180^{\circ}} \cdot angle`

### Sample Source Pattern

#### Implementation example

Copy code

```
:force: 

 function radians(angle){
    return (Math.PI/180) * angle;
}
```

##### Arguments

`angle`: Float expression in degrees.

##### Return Type

Same data type sent through parameter as a numeric expression in radians.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION RADIANS(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
    function radians(angle){
      return (Math.PI/180) * angle;
    }
    return radians(ANGLE);
$$
;
SELECT RADIANS(180);
```

##### Result

| RADIANS(180) |
| --- |
| 3.141592654 |

Expand

Show lessSee more

## PI

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the constant value of PI  
([PI in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/pi-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
PI( )
```

#### Arguments

This method does not receive any parameters.

#### Return Type

Float.

### Examples

### Query

Copy code

```
:force:
CREATE PROCEDURE CIRCUMFERENCE @radius float
AS 
    SELECT 2 * PI() * @radius;
GO:

EXEC CIRCUMFERENCE @radius = 2;
```

#### Result

Copy code

```
CIRCUMFERENCE @radius = 2 |
--------------------------|
          12.5663706143592|
```

## PI in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Constant which represents the PI number (approximately 3.141592…)  
([JavaScript PI Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/PI)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.PI
```

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION circumference(radius float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function circumference(r){
    return 2 * Math.PI * r;
  }
  return circumference(RADIUS); 
$$
;
SELECT CIRCUMFERENCE(2);
```

##### Result

Copy code

```
  CIRCUMFERENCE(2)|
------------------|
12.566370614359172|
```

## DEGREES

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts the angle in radians sent through parameters to degrees ([DEGREES in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
DEGREES( expression )
```

#### Arguments

`expression`: Numeric **float** expression in radians.

#### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

### Query

Copy code

```
:force:
SELECT DEGREES(PI())
```

#### Result

Copy code

```
DEGREES(PI())|
-------------|
        180.0|
```

## DEGREES in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

JavaScript does not provide a method to convert radians to degrees of a given angle.  
This could be calculated using the equation: `Degrees = \frac{180^{\circ}}{\pi} \cdot angle`

### Sample Source Pattern

#### Implementation example

Copy code

```
:force: 

 function degress(angle){
    return (180/Math.PI) * angle;
}
```

##### Arguments

`angle`: Numeric expression in radians.

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_degrees(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function degrees(angle){
    return (180/Math.PI) * angle;
  }
  return degrees(ANGLE);
    
$$
;
SELECT COMPUTE_DEGREES(PI());
```

##### Result

Copy code

```
COMPUTE_DEGREES(PI())|
---------------------|
                180.0|
```

## LOG

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the natural logarithm of a number  
([LOG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/log-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
LOG( expression [, base ] )
```

#### Arguments

`expression`: Numeric expression.

`base` (optional): Base to calculate the logarithm of a number, it is Euler by default.

#### Return Type

Float.

### Examples

### Query

Copy code

```
:force:
SELECT LOG(8, 2)
```

#### Result

Copy code

```
LOG(8, 2)  |
-----------|
          3|
```

## LOG in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the logarithm using the Euler’s number as a base. ([JavaScript LOG function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log)).

Warning

Unfortunately, JavaScript does not provide a method that receives a logarithm base through its parameters, but this can be solved by dividing the base by the argument.

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.log( expression )
```

##### Arguments

`expression`: Numeric expression. It must be positive, otherwise returns NaN.\

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION base_log(base float, exp float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  function getBaseLog(x, y){
    return Math.log(y)/Math.log(x);
  }
  return getBaseLog(EXP, BASE)
$$
;
SELECT BASE_LOG(2, 8);
```

##### Result

Copy code

```
BASE_LOG(2, 8)|
--------------|
             3|
```

## ATAN

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arctangent in radians of the number sent as a parameter ([ATAN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/atan-transact-sql?view=sql-server-ver15)).

The arctangent is the inverse function of the tangent, summarized in the next definition:  
`y = arctan^{-1} \Leftrightarrow x = tan(x)`

For `y = tan^{-1}(x)`:  
- Range: `-\frac{\pi}{2}\leqslant y \leqslant \frac{\pi}{2}` or `-90^{\circ}\leqslant y \leqslant 90^{\circ}`  
- Domain: `\mathbb{R}`

### Sample Source Pattern

### Syntax

Copy code

```
:force:
ATAN( expression )
```

#### Arguments

`expression`: Numeric **float** expression, or a numeric type which could be converted to float.

#### Return Type

Numeric float expression between `-\frac{\pi}{2}` and `\frac{\pi}{2}`.

### Examples

### Query

Copy code

```
:force:
SELECT ATAN(-30);
```

#### Result

Copy code

```
ATAN(-30)          |
-------------------|
-1.5374753309166493|
```

## ATAN in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arctangent of a specified number  
([JavaScript ATAN function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/atan)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.atan( expression )
```

##### Arguments

`expression`: Numeric expression.

##### Return Type

Numeric expression between `-\frac{\pi}{2}` and `\frac{\pi}{2}`.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION compute_atan(a float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.atan(A);
$$
;
SELECT COMPUTE_ATAN(-30);
```

##### Result

Copy code

```
COMPUTE_ATAN(-30)|
-----------------|
     -1.537475331|
```

## ATN2

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arctangent in radians of two coordinates sent as a parameter ([ATN2 in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/atn2-transact-sql?view=sql-server-ver15)).

For `z = tan^{-1}(x, y)`:  
- Range: `-\pi\leqslant z \leqslant \pi` or `-180^{\circ}\leqslant z \leqslant 180^{\circ}`  
- Domain: `\mathbb{R}`

### Sample Source Pattern

### Syntax

Copy code

```
:force:
ATN2( expression_1, expression_2 )
```

#### Arguments

`expression1`and `expression2`: Numeric expressions.

#### Return Type

Numeric expression between `-\pi` and `\pi`.

### Examples

### Query

Copy code

```
:force:
SELECT ATN2(7.5, 2);
```

#### Result

Copy code

```
ATN2(7.5, 2)      |
------------------|
1.3101939350475555|
```

## ATAN2 in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Function that returns the arctangent of two parameters  
([JavaScript ATAN2 function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.atan2( expression_1, expression_2 )
```

##### Arguments

`expression_1`and `expression_2`: Numeric expressions.

##### Return Type

Numeric expression between `-\pi` and `\pi`.

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_atan2(x float, y float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.atan2(X, Y);
$$
;
SELECT COMPUTE_ATAN2(7.5, 2);
```

##### Result

Copy code

```
ATAN2(7.5, 3)     |
------------------|
       1.310193935|
```

## LOG10

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the base 10 logarithm of a number  
([LOG10 in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/log10-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
LOG10( expression )
```

#### Arguments

`expression`: Numeric expression, must be positive.

#### Return Type

Float.

### Examples

### Query

Copy code

```
:force:
SELECT LOG10(5)
```

#### Result

Copy code

```
LOG10(5)         |
-----------------|
0.698970004336019|
```

## LOG10 in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the base 10 logarithm of a number  
([JavaScript LOG10 function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log10)).

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.log10( expression )
```

##### Arguments

`expression`: Numeric expression. It must be positive, otherwise returns NaN.\

##### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

#### Query

Copy code

```
:force: 

 CREATE OR REPLACE FUNCTION compute_log10(argument float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
    return Math.log10(ARGUMENT);
$$
;
SELECT COMPUTE_LOG10(7.5);
```

##### Result

Copy code

```
COMPUTE_LOG10(5)|
----------------|
    0.6989700043|
```

## EXP

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the exponential value of Euler ([EXP in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/exp-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

### Syntax

Copy code

```
:force:
EXP( expression )
```

#### Arguments

`expression`: Numeric expression.

#### Return Type

Same data type sent through parameter as a numeric expression.

### Examples

### Query

Copy code

```
:force:
SELECT EXP(LOG(20)), LOG(EXP(20))  
GO
```

#### Result

Copy code

```
EXP(LOG(20))   |LOG(EXP(20))    |
---------------|----------------|
           20.0|            20.0|
```

## EXP in JS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Constant which represents Euler’s number (approximately 2.718…)  
([JavaScript Euler’s Number Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/E)).  
JavaScript allows make different operations using this constant, instead of Transact-SQL which only supports the exponential of Euler.

### Sample Source Pattern

#### Syntax

Copy code

```
:force: 

 Math.E
```

### Examples

#### Query

Copy code

```
:force: 

CREATE OR REPLACE FUNCTION compute_exp(x float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.E**X;
$$
;
SELECT COMPUTE_EXP(LN(20)), LN(COMPUTE_EXP(20));
```

##### Result

Copy code

```
COMPUTE_EXP(LOG(20))|LOG(COMPUTE_EXP(20))|
--------------------|--------------------|
                20.0|                20.0|
```

## Conversion functions

This section describes the functional equivalents of date & time functions in Transact-SQL to Snowflake SQL code.

## CONVERT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Convert an expression of one data type to another. ([CONVERT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
CONVERT ( data_type [ ( length ) ] , expression [ , style ] )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/cast.html)

Copy code

```
:force: 
CAST( <source_expr> AS <target_data_type> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CONVERT(INT, '1998') as MyDate
```

##### Result

| MyDate |
| --- |
| 1998 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CAST('1998' AS INT) as MyDate;
```

##### Result

| MYDATE |
| --- |
| 1998 |

Expand

Show lessSee more

##### Casting date type to varchar

##### SQL Server

Copy code

```
:force: 

SELECT CONVERT(varchar, getdate(), 1) AS RESULT;
```

##### Result

| RESULT |
| --- |
| 12/08/22 |

Expand

Show lessSee more

##### Swowflake SQL

Copy code

```
:force: 

SELECT
TO_VARCHAR(CURRENT_TIMESTAMP() :: TIMESTAMP, 'mm/dd/yy') AS RESULT;
```

##### Result

| RESULT |
| --- |
| 12/08/22 |

Expand

Show lessSee more

##### Casting date type to varchar with size

##### SQL Server

Copy code

```
:force: 

SELECT CONVERT(varchar(2), getdate(), 1) AS RESULT;
```

##### Result

| RESULT |
| --- |
| 07 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
LEFT(TO_VARCHAR(CURRENT_TIMESTAMP() :: TIMESTAMP, 'mm/dd/yy'), 2) AS RESULT;
```

##### Result

| RESULT |
| --- |
| 07 |

Expand

Show lessSee more

The supported formats for dates casts are:

**Date formats**

| Code | Format |
| --- | --- |
| 1 | mm/dd/yy |
| 2 | yy.mm.dd |
| 3 | dd/mm/yy |
| 4 | dd.mm.yy |
| 5 | dd-mm-yy |
| 6 | dd-Mon-yy |
| 7 | Mon dd, yy |
| 10 | mm-dd-yy |
| 11 | yy/mm/dd |
| 12 | yymmdd |
| 23 | yyyy-mm-dd |
| 101 | mm/dd/yyyy |
| 102 | yyyy.mm.dd |
| 103 | dd/mm/yyyy |
| 104 | dd.mm.yyyy |
| 105 | dd-mm-yyyy |
| 106 | dd Mon yyyy |
| 107 | Mon dd, yyyy |
| 110 | mm-dd-yyyy |
| 111 | yyyy/mm/dd |
| 112 | yyyymmdd |

Expand

Show lessSee more

**Time formats**

| Code | Format |
| --- | --- |
| 8 | hh:mm:ss |
| 14 | hh:mm:ss:ff3 |
| 24 | hh:mm:ss |
| 108 | hh:mm:ss |
| 114 | hh:mm:ss:ff3 |

Expand

Show lessSee more

**Date and time formats**

|  |  |
| --- | --- |
| 0 | Mon dd yyyy hh:mm AM/PM |
| 9 | Mon dd yyyy hh:mm:ss:ff3 AM/PM |
| 13 | dd Mon yyyy hh:mm:ss:ff3 AM/PM |
| 20 | yyyy-mm-dd hh:mm:ss |
| 21 | yyyy-mm-dd hh:mm:ss:ff3 |
| 22 | mm/dd/yy hh:mm:ss AM/PM |
| 25 | yyyy-mm-dd hh:mm:ss:ff3 |
| 100 | Mon dd yyyy hh:mm AM/PM |
| 109 | Mon dd yyyy hh:mm:ss:ff3 AM/PM |
| 113 | dd Mon yyyy hh:mm:ss:ff3 |
| 120 | yyyy-mm-dd hh:mm:ss |
| 121 | yyyy-mm-dd hh:mm:ss:ff3 |
| 126 | yyyy-mm-dd T hh:mm:ss:ff3 |
| 127 | yyyy-mm-dd T hh:mm:ss:ff3 |

Expand

Show lessSee more

**Islamic calendar dates**

| Code | Format |
| --- | --- |
| 130 | dd mmm yyyy hh:mi:ss:ff3 AM/PM |
| 131 | dd mmm yyyy hh:mi:ss:ff3 AM/PM |

Expand

Show lessSee more

If there is no pattern matching with the current code, it will be formatted to `yyyy-mm-dd hh:mm:ss`

##### Converting string to DATE or DATETIME with style

When `CONVERT` targets a `DATE`, `DATETIME`, or `DATETIME2` type and includes a **literal** style code, it is mapped to `TO_DATE` or `TO_TIMESTAMP` with the corresponding Snowflake format string.

##### SQL Server

Copy code

```
SELECT
    CONVERT(DATE, StartDate, 101) AS StartDt,
    CONVERT(DATE, EndDate, 103) AS EndDt,
    CONVERT(DATETIME, EventTime, 120) AS EventTs
FROM Events
```

##### Snowflake SQL

Copy code

```
SELECT
  TO_DATE(StartDate, 'mm/dd/yyyy') AS StartDt,
  TO_DATE(EndDate, 'dd/mm/yyyy') AS EndDt,
  TO_TIMESTAMP(EventTime, 'yyyy-mm-dd hh:mm:ss') AS EventTs
FROM
  Events;
```

The following table shows which target types produce `TO_DATE` versus `TO_TIMESTAMP`:

| Target Type | Snowflake Function |
| --- | --- |
| DATE | TO\_DATE |
| DATETIME | TO\_TIMESTAMP |
| DATETIME2 | TO\_TIMESTAMP |

Expand

Show lessSee more

##### Converting VARBINARY / BINARY with style

When converting to `VARBINARY` or `BINARY` with a hex style (1 or 2), it is mapped to `TO_BINARY(expr, 'HEX')`. Style 0 (default/ASCII) maps to a plain `CAST`. For `VARBINARY(MAX)`, the outer `CAST` is omitted.

##### SQL Server

Copy code

```
SELECT CONVERT(VARBINARY(16), @UGIDString, 0);
SELECT CONVERT(VARBINARY(16), @UGIDString, 1);
SELECT CONVERT(VARBINARY(MAX), @HexData, 2);
SELECT CONVERT(BINARY(16), @HexData, 1);
```

##### Snowflake SQL

Copy code

```
SELECT CAST(@UGIDString AS VARBINARY(16));
SELECT CAST(TO_BINARY(@UGIDString, 'HEX') AS VARBINARY(16));
SELECT TO_BINARY(@HexData, 'HEX');
SELECT CAST(TO_BINARY(@HexData, 'HEX') AS BINARY(16));
```

##### Converting with a dynamic style variable

When the style argument is a variable or expression instead of a literal, the format string cannot be determined at conversion time. The function falls back to `CAST` and emits [SSC-EWI-TS0098](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0098).

##### SQL Server

Copy code

```
SELECT CONVERT(DATE, @InputDate, @Style)
```

##### Snowflake SQL

Copy code

```
SELECT
  !!!RESOLVE EWI!!! /*** SSC-EWI-TS0098 - CONVERT WITH A VARIABLE OR EXPRESSION AS THE STYLE ARGUMENT CANNOT BE AUTOMATICALLY MAPPED TO A SNOWFLAKE FORMAT STRING. REPLACE WITH THE APPROPRIATE TO_VARCHAR, TO_DATE, OR TO_TIMESTAMP CALL WITH THE KNOWN FORMAT STRING. ***/!!!
  CAST(@InputDate AS DATE);
```

##### Converting unresolved expression to varchar with a literal style

When the target type is a character type (such as `varchar`) and the style is a literal, the conversion is mapped to `TO_VARCHAR` with the corresponding Snowflake format string, even when the source expression’s type cannot be fully resolved. The result is wrapped in `LEFT` if the target type specifies a length.

##### SQL Server

Copy code

```
SELECT CONVERT(varchar(8), @param, 112)
```

##### Snowflake SQL

Copy code

```
SELECT LEFT(TO_VARCHAR(@param, 'yyyymmdd'), 8)
```

### Related EWIs

1. [SSC-EWI-TS0098](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0098): CONVERT with a non-literal style cannot be mapped to a Snowflake format string.

## TRY\_CONVERT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a value cast to the specified data type if the cast succeeds; otherwise, returns null.

([SQL Server Language Reference TRY\_CONVERT](https://docs.microsoft.com/en-us/sql/t-sql/functions/try-convert-transact-sql?view=sql-server-ver15))

#### Syntax

Copy code

```
:force:
TRY_CONVERT ( data_type [ ( length ) ], expression [, style ] )
```

### Source Patterns

#### Basic Transformation

To transform this function, we have to check the parameters of the TRY\_CONVERT first.

Copy code

```
:force:
TRY_CONVERT( INT, 'test')
```

If the expression that needs to be casted is a string, it will be transfomed to TRY\_CAST, which is a function of Snowflake.

Copy code

```
:force:
TRY_CAST( 'test' AS INT)
```

#### TRY\_CAST

The TRY\_CAST shares the same transformation with TRY\_CONVERT.

##### Example

##### Sql Server

Copy code

```
:force:
SELECT TRY_CAST('12345' AS NUMERIC) NUMERIC_RESULT,
 TRY_CAST('123.45' AS DECIMAL(20,2)) DECIMAL_RESULT,
 TRY_CAST('123' AS INT) INT_RESULT,
 TRY_CAST('123.02' AS FLOAT) FLOAT_RESULT,
 TRY_CAST('123.02' AS DOUBLE PRECISION) DOUBLE_PRECISION_RESULT,

 TRY_CAST('2017-01-01 12:00:00' AS DATE) DATE_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATETIME) DATETIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS SMALLDATETIME) SMALLDATETIME_RESULT,
 TRY_CAST('12:00:00' AS TIME) TIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP) TIMESTAMP_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATETIMEOFFSET) DATETIMEOFFSET_RESULT,

 TRY_CAST(1234 AS VARCHAR) VARCHAR_RESULT,
 TRY_CAST(1 AS CHAR) CHAR_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS SQL_VARIANT) SQL_VARIANT_RESULT,
 TRY_CAST('LINESTRING(-122.360 47.656, -122.343 47.656 )' AS GEOGRAPHY) GEOGRAPHY_RESULT;
```

The result will be the same with the example of TRY\_CONVERT.

##### Snowflake

Copy code

```
:force:
SELECT
 TRY_CAST('12345' AS NUMERIC(38, 18)) NUMERIC_RESULT,
 TRY_CAST('123.45' AS DECIMAL(20,2)) DECIMAL_RESULT,
 TRY_CAST('123' AS INT) INT_RESULT,
 TRY_CAST('123.02' AS FLOAT) FLOAT_RESULT,
 TRY_CAST('123.02' AS DOUBLE PRECISION) DOUBLE_PRECISION_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATE) DATE_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(3)) DATETIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(0)) SMALLDATETIME_RESULT,
 TRY_CAST('12:00:00' AS TIME(7)) TIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS BINARY(8)) TIMESTAMP_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_TZ(7)) DATETIMEOFFSET_RESULT,
 TO_VARCHAR(1234) VARCHAR_RESULT,
 TO_CHAR(1) CHAR_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS VARIANT) SQL_VARIANT_RESULT,
 TRY_CAST('LINESTRING(-122.360 47.656, -122.343 47.656 )' AS GEOGRAPHY) GEOGRAPHY_RESULT;
```

### Known Issues

If the data type is Varchar or Char, then it will be transformed differently.

Copy code

```
:force:
TRY_CONVERT(VARCHAR, 1234);
TRY_CONVERT(CHAR, 1);
```

If TRY\_CAST is used with VARCHAR or CHAR in Snowflake, it will cause an error, so it will be transformed to

Copy code

```
:force:
TO_VARCHAR(1234);
TO_CHAR(1);
```

The same happens with the data types of SQL\_VARIANT and GEOGRAPHY.

Copy code

```
:force:
TRY_CONVERT(SQL_VARIANT, '2017-01-01 12:00:00');
TRY_CONVERT(GEOGRAPHY, 'LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

Are transformed to

Copy code

```
:force:
TO_VARIANT('2017-01-01 12:00:00');
TO_GEOGRAPHY('LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

If the expression is not a string, there is a very high chance that it will fail, since the TRY\_CAST of snowflake works only with string expressions.

In this case, another transformation will be done

Copy code

```
:force:
TRY_CAST(14.85 AS INT)
```

Will be transformed to

Copy code

```
:force:
CAST(14.85 AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/
```

Now, with these transformation, there could be problems depending on what is being done with the functions. The TRY\_CONVERT of SqlServer returns nulls if the convertion was not possible.

This can be used to do logic like this

Copy code

```
:force:
SELECT 
    CASE
        WHEN TRY_CONVERT( INT, 'Expression') IS NULL
        THEN 'FAILED'
        ELSE 'SUCCEDDED'
    END;
```

That type of conditions with the TRY\_CONVERT can be used with the TRY\_CAST, but what happens if it is transformed to TO\_VARCHAR, TOCHAR or to the CAST? If the convertion in those functions fails, it will cause an error instead of just returning null.

#### Examples

In this sample we have several TRY\_CONVERT with different data types

##### SQL Server

Copy code

```
:force:
SELECT TRY_CONVERT(NUMERIC, '12345') NUMERIC_RESULT,
 TRY_CONVERT(DECIMAL(20,2), '123.45') DECIMAL_RESULT,
 TRY_CONVERT(INT, '123') INT_RESULT,
 TRY_CONVERT(FLOAT, '123.02') FLOAT_RESULT,
 TRY_CONVERT(DOUBLE PRECISION, '123.02') DOUBLE_PRECISION_RESULT,

 TRY_CONVERT(DATE, '2017-01-01 12:00:00') DATE_RESULT,
 TRY_CONVERT(DATETIME, '2017-01-01 12:00:00') DATETIME_RESULT,
 TRY_CONVERT(SMALLDATETIME, '2017-01-01 12:00:00') SMALLDATETIME_RESULT,
 TRY_CONVERT(TIME, '12:00:00') TIME_RESULT,
 TRY_CONVERT(TIMESTAMP, '2017-01-01 12:00:00') TIMESTAMP_RESULT,
 TRY_CONVERT(DATETIMEOFFSET, '2017-01-01 12:00:00') DATETIMEOFFSET_RESULT,

 TRY_CONVERT(VARCHAR, 1234) VARCHAR_RESULT,
 TRY_CONVERT(CHAR, 1) CHAR_RESULT,
 TRY_CONVERT(SQL_VARIANT, '2017-01-01 12:00:00') SQL_VARIANT_RESULT,
 TRY_CONVERT(GEOGRAPHY, 'LINESTRING(-122.360 47.656, -122.343 47.656 )') GEOGRAPHY_RESULT;
```

If we migrate that select, we will get the following result

##### Snowflake

Copy code

```
:force:
SELECT
 CAST('12345' AS NUMERIC(38, 18)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ NUMERIC_RESULT,
 CAST('123.45' AS DECIMAL(20,2)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DECIMAL_RESULT,
 CAST('123' AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ INT_RESULT,
 CAST('123.02' AS FLOAT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ FLOAT_RESULT,
 CAST('123.02' AS DOUBLE PRECISION) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DOUBLE_PRECISION_RESULT,
 CAST('2017-01-01 12:00:00' AS DATE) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATE_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(3)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATETIME_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(0)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ SMALLDATETIME_RESULT,
 CAST('12:00:00' AS TIME(7)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ TIME_RESULT,
 CAST('2017-01-01 12:00:00' AS BINARY(8)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ TIMESTAMP_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_TZ(7)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATETIMEOFFSET_RESULT,
 TO_VARCHAR(1234) VARCHAR_RESULT,
 TO_CHAR(1) CHAR_RESULT,
 TO_VARIANT('2017-01-01 12:00:00') SQL_VARIANT_RESULT,
 TO_GEOGRAPHY('LINESTRING(-122.360 47.656, -122.343 47.656 )') GEOGRAPHY_RESULT;
```

Let’s execute each one and compare the result.

| Alias | SqlServer Result | Snowflake Result |
| --- | --- | --- |
| NUMERIC\_RESULT | 12345 | 12345 |
| DECIMAL\_RESULT | 123.45 | 123.45 |
| INT\_RESULT | 123 | 123 |
| FLOAT\_RESULT | 123.02 | 123.02 |
| DOUBLE\_PRECISION\_RESULT | 123.02 | 123.02 |
| DATE\_RESULT | 2017-01-01 | 2017-01-01 |
| DATETIME\_RESULT | 2017-01-01 12:00:00.000 | 2017-01-01 12:00:00.000 |
| SMALLDATETIME\_RESULT | 2017-01-01 12:00:00 | 2017-01-01 12:00:00.000 |
| TIME\_RESULT | 12:00:00.0000000 | 12:00:00 |
| TIMESTAMP\_RESULT | 0x323031372D30312D | 2017-01-01 12:00:00.000 |
| DATETIMEOFFSET\_RESULT | 2017-01-01 12:00:00.0000000 +00:00 | 2017-01-01 12:00:00.000 -0800 |
| VARCHAR\_RESULT | 1234 | 1234 |
| CHAR\_RESULT | 1 | 1 |
| SQL\_VARIANT\_RESULT | 2017-01-01 12:00:00 | “2017-01-01 12:00:00” |
| GEOGRAPHY\_RESULT | 0xE610000001148716D9CEF7D34740D7A3703D0A975EC08716D9CEF7D34740CBA145B6F3955EC0 | { “coordinates”: [ [ -122.36, 47.656 ], [ -122.343, 47.656 ] ], “type”: “LineString” } |

Expand

Show lessSee more

### Related EWIs

1. [SSC-FDM-TS0005](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0005): TRY\_CONVERT/TRY\_CAST could not be converted to TRY\_CAST.

## Date & Time functions

This section describes the functional equivalents of date & time functions in Transact-SQL to Snowflake SQL and JavaScript code.

## AT TIME ZONE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Converts an *inputdate* to the corresponding *datetimeoffset* value in the target time zone. ([AT TIME ZONE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
inputdate AT TIME ZONE timezone
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone.html)

Copy code

```
CONVERT_TIMEZONE( <source_tz> , <target_tz> , <source_timestamp_ntz> )

CONVERT_TIMEZONE( <target_tz> , <source_timestamp> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT CAST('2022-11-24 11:00:45.2000000 +00:00' as datetimeoffset) at time zone 'Alaskan Standard Time';
```

**Result:**

Copy code

```
                          DATE|
------------------------------|
2022-11-24 02:00:45.200 -09:00|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CONVERT_TIMEZONE('America/Anchorage', CAST('2022-11-24 11:00:45.2000000 +00:00' as TIMESTAMP_TZ(7)));
```

**Result:**

Copy code

```
                          DATE|
------------------------------|
2022-11-24 02:00:45.200 -09:00|
```

##### SQL Server

Copy code

```
:force: 

SELECT current_timestamp at time zone 'Central America Standard Time';
```

**Result:**

Copy code

```
                          DATE|
------------------------------|
2022-10-10 10:55:50.090 -06:00|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
CONVERT_TIMEZONE('America/Costa_Rica', CURRENT_TIMESTAMP() /*** SSC-FDM-TS0024 - CURRENT_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases ***/);
```

**Result:**

Copy code

```
                          DATE|
------------------------------|
2022-10-10 10:55:50.090 -06:00|
```

### Known Issues

1. Snowflake does not support all the time zones that SQL Server does. You can check the supported time zones at this [link](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone.html).

#### SQL Server

Copy code

```
:force: 

SELECT current_timestamp at time zone 'Turks And Caicos Standard Time';
```

**Result:**

Copy code

```
                          DATE|
------------------------------|
2022-12-14 20:04:18.317 -05:00|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0063 - TIME ZONE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CURRENT_TIMESTAMP() at time zone 'Turks And Caicos Standard Time';
```

### Related EWIs

1. [SSC-FDM-TS0024](../../issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0024): CURRENT\_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases.
2. [SSC-EWI-TS0063](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0063): Time zone not supported in Snowflake.

## DATEADD

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns an integer representing the specified datepart of the specified date. ([DATEPART in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
DATEADD (datepart , number , date )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/dateadd.html)

Copy code

```
DATEADD( <date_or_time_part>, <value>, <date_or_time_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATEADD(year,123, '20060731') as ADDDATE;
```

**Result:**

Copy code

```
                 ADDDATE|
------------------------|
 2129-07-31 00:00:00.000|
```

##### Snowflake SQL

Copy code

```
:force: 

SELECT
DATEADD(year, 123, '20060731') as ADDDATE;
```

**Result:**

Copy code

```
                 ADDDATE|
------------------------|
 2129-07-31 00:00:00.000|
```

## DATEDIFF

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the count (as a signed integer value) of the specified datepart boundaries crossed between the specified startdate and enddate. ([DATEDIFF in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
DATEDIFF ( datepart , startdate , enddate )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/datediff.html)

Copy code

```
DATEDIFF( <date_or_time_part>, <date_or_time_expr1>, <date_or_time_expr2> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATEDIFF(year,'2005-12-31 23:59:59.9999999', '2006-01-01 00:00:00.0000000');
```

**Result:**

| DIFF |
| --- |
| 1 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT DATEDIFF(year,'2005-12-31 23:59:59.9999999', '2006-01-01 00:00:00.0000000');
```

**Result:**

| DIFF |
| --- |
| 1 |

Expand

Show lessSee more

## DATEFROMPARTS

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns a **date** value that maps to the specified year, month, and day values.([DATEFROMPARTS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datefromparts-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
DATEFROMPARTS ( year, month, day )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/date_from_parts.html)

Copy code

```
:force:
DATE_FROM_PARTS( <year>, <month>, <day> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATEFROMPARTS ( 2010, 12, 31 ) AS RESULT;
```

**Result:**

| RESULT |
| --- |
| 2022-12-12 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT DATE_FROM_PARTS ( 2010, 12, 31 ) AS RESULT;
```

**Result:**

| RESULT |
| --- |
| 2022-12-12 |

Expand

Show lessSee more

## DATENAME

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns a character string representing the specified datepart of the specified date. ([DATENAME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datename-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
DATENAME ( datepart , date )
```

##### Snowflake SQL

Note

This transformation uses several functions depending on the inputs

Copy code

```
:force: 
DATE_PART( <date_or_time_part> , <date_or_time_expr> )
MONTHNAME( <date_or_timestamp_expr> )
DAYNAME( <date_or_timestamp_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATENAME(month, getdate()) AS DATE1,
DATENAME(day, getdate()) AS DATE2,
DATENAME(dw, GETDATE()) AS DATE3;
```

**Result:**

| DATE1 | DATE2 | DATE3 |
| --- | --- | --- |
| May | 3 | Tuesday |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
MONTHNAME_UDF(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE1,
DAYNAME_UDF(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE2,
DAYNAME(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE3;
```

**Result:**

| DATE1 | DATE2 | DATE3 |
| --- | --- | --- |
| May | Tue | Tue |

Expand

Show lessSee more

## DATEPART

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns an integer representing the specified datepart of the specified date. ([DATEPART in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force: 
DATEPART ( datepart , date )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/date_part.html)

Copy code

```
:force: 
DATE_PART( <date_or_time_part> , <date_or_time_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DATEPART(YEAR, '10-10-2022') as YEAR
```

**Result:**

| YEAR |
| --- |
| 2022 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
DATE_PART(YEAR, '10-10-2022' :: TIMESTAMP) as YEAR;
```

**Result:**

| YEAR |
| --- |
| 2022 |

Expand

Show lessSee more

## DAY

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns an integer that represents the day (day of the month) of the specified date. ([DAY in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/day-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
DAY ( date )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

Copy code

```
:force:
DAY( <date_or_timestamp_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT DAY('10-10-2022') AS DAY
```

**Result:**

| DAY |
| --- |
| 10 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT DAY('10-10-2022' :: TIMESTAMP) AS DAY;
```

**Result:**

| DAY |
| --- |
| 10 |

Expand

Show lessSee more

## EOMONTH

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

This function returns the last day of the month containing a specified date, with an optional offset. ([EOMONTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/eomonth-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
EOMONTH ( start_date [, month_to_add ] )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/last_day.html)

Copy code

```
:force:
LAST_DAY( <date_or_time_expr> [ , <date_part> ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT EOMONTH (GETDATE()) AS Result;
```

**Result:**

| RESULT |
| --- |
| 2022-05-31 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
LAST_DAY(DATEADD('month', 0, CURRENT_TIMESTAMP() :: TIMESTAMP)) AS Result;
```

**Result:**

| RESULT |
| --- |
| 2022-05-31 |

Expand

Show lessSee more

## GETDATE

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns the current database system timestamp as a **datetime** value without the database time zone offset. ([GETDATE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/getdate-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
GETDATE()
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp.html)

Copy code

```
:force:
CURRENT_TIMESTAMP( [ <fract_sec_precision> ] )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT GETDATE() AS DATE;
```

**Result:**

| DATE |
| --- |
| 2022-05-06 09:54:42.757 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT CURRENT_TIMESTAMP() :: TIMESTAMP AS DATE;
```

**Result:**

| DATE |
| --- |
| 2022-05-06 08:55:05.422 |

Expand

Show lessSee more

## MONTH

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns an integer that represents the month of the specified *date*. ([MONTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/month-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
MONTH( date )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

Copy code

```
:force:
MONTH ( <date_or_timestamp_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT MONTH('10-10-2022') AS MONTH
```

**Result:**

| MONTH |
| --- |
| 10 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT MONTH('10-10-2022' :: TIMESTAMP) AS MONTH;
```

**Result:**

| MONTH |
| --- |
| 10 |

Expand

Show lessSee more

## SWITCHOFFSET

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

The SWITCHOFFSET adjusts a given timestamp value to a specific timezone offset. This is done through numerical values. More information can be found at [SWITCHOFFSET (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/switchoffset-transact-sql?view=sql-server-ver16).

### Sample Source Pattern

#### Syntax

[A UDF Helper](#switchoffset_udf) accomplish functional equivalence, also it shares the same syntax as the SQLServer’s SWITCHOFFSET function.

##### SQLServer

Copy code

```
:force: 

 SWITCHOFFSET ( datetimeoffset_expression, timezoneoffset_expression )
```

##### Snowflake SQL

Copy code

```
:force: 

 SWITCHOFFSET_UDF ( timestamp_tz_expression, timezoneoffset_expression )
```

#### Example

##### SQLServer

Copy code

```
:force: 

SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

**Result:**

| fr\_time | cr\_time |
| --- | --- |
| 1998-09-20 7:45:50.71345 +02:00 | 1998-09-19 23:45:50.7134500 -06:00 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  PUBLIC.SWITCHOFFSET_UDF('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

**Result:**

| fr\_time | cr\_time |
| --- | --- |
| 1998-09-20 7:45:50.71345 +02:00 | 1998-09-19 23:45:50.7134500 -06:00 |

Expand

Show lessSee more

## SYSDATETIME

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a datetime2(7) value that contains the date and time of the computer on which the instance of SQL Server is running. ([SYSDATETIME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sysdatetime-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
SYSDATETIME ( )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/localtime.html)

Copy code

```
:force:
LOCALTIME()
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT SYSDATETIME ( ) AS SYSTEM_DATETIME;
```

**Result:**

| SYSTEM\_DATETIME |
| --- |
| 2022-05-06 12:08:05.501 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT LOCALTIME ( ) AS SYSTEM_DATETIME;
```

**Result:**

| SYSTEM\_DATETIME |
| --- |
| 211:09:14 |

Expand

Show lessSee more

## SYSUTCDATETIME

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns a datetime2(7) value that contains the date and time of the computer on which the instance of SQL Server is running. ([SYSUTCDATETIME in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/sysutcdatetime-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
SYSUTCDATETIME ( )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/localtime.html)

Copy code

```
:force:
SYSDATE()
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT SYSUTCDATETIME() as SYS_UTC_DATETIME;
```

**Result:**

| SYSTEM\_UTC\_DATETIME |
| --- |
| 2023-02-02 20:59:28.0926502 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT
SYSDATE() as SYS_UTC_DATETIME;
```

**Result:**

| SYSTEM\_UTC\_DATETIME |
| --- |
| 2023-02-02 21:02:05.557 |

Expand

Show lessSee more

## YEAR

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Returns an integer that represents the year of the specified *date*. ([YEAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/year-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern

#### Syntax

##### SQL Server

Copy code

```
:force:
YEAR( date )
```

##### Snowflake SQL

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

Copy code

```
:force:
YEAR ( <date_or_timestamp_expr> )
```

### Examples

#### SQL Server

Copy code

```
:force: 

SELECT YEAR('10-10-2022') AS YEAR
```

**Result:**

| YEAR |
| --- |
| 2022 |

Expand

Show lessSee more

##### Snowflake SQL

Copy code

```
:force: 

SELECT YEAR('10-10-2022' :: TIMESTAMP) AS YEAR;
```

**Result:**

| YEAR |
| --- |
| 2022 |

Expand

Show lessSee more
