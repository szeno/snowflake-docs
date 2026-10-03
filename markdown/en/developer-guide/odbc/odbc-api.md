# ODBC Driver API support

This topic lists the ODBC routines relevant to Snowflake and indicates whether they are supported. The routines are organized into
categories based on the function they perform.

ODBC 3.x advertises conformance with version 3.52 of the ODBC API, and ODBC 4.x advertises version 3.80. Where the two versions behave differently, the Notes column says so. For the full list of changes, see [Migrating from ODBC Driver 3.x to 4.x](/developer-guide/odbc/odbc-migration).

For the complete API reference, see the [Microsoft ODBC Programmer’s Reference](https://msdn.microsoft.com/en-us/library/ms714177.aspx).

## Connecting to a data source

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLAllocHandle` | ✔ |  |
| `SQLConnect` | ✔ |  |
| `SQLDriverConnect` | ✔ |  |
| `SQLAllocEnv` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLAllocConnect` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLBrowseConnect` | ✔ |  |

Expand

Show lessSee more

## Obtaining information about a driver and data source

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLDataSources` | ✔ |  |
| `SQLDrivers` | ✔ |  |
| `SQLGetInfo` | ✔ |  |
| `SQLGetFunctions` | ✔ |  |
| `SQLGetTypeInfo` | ✔ | ODBC 4.x always reports `COLUMN_SIZE` 29 for `SQL_TYPE_TIMESTAMP`, and doesn’t accept the `ODBC_USE_STANDARD_TIMESTAMP_COLUMNSIZE` parameter. |

Expand

Show lessSee more

## Setting and retrieving driver attributes

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLSetConnectAttr` | ✔ | Setting SQL\_ATTR\_METADATA\_ID puts catalog function arguments into identifier mode, and the two versions fold unquoted identifiers differently. See [catalog functions](#label-odbc-api-catalog-functions). |
| `SQLGetConnectAttr` | ✔ | Read-only mode is not supported. SQL\_MODE\_READ\_ONLY is passed to the driver, but Snowflake still writes to the database.     Also, some attributes were introduced post API version 3.52: SQL\_ATTR\_ASYNC\_DBC\_EVENT, SQL\_ATTR\_ASYNC\_DBC\_FUNCTIONS\_ENABLE, SQL\_ATTR\_ASYNC\_DBC\_PCALLBACK, SQL\_ATTR\_ASYNC\_DBC\_PCONTEXT, SQL\_ATTR\_DBC\_INFO\_TOKEN. |
| `SQLSetConnectOption` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLGetConnectOption` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLSetEnvAttr` | ✔ |  |
| `SQLGetEnvAttr` | ✔ | The SQL\_ATTR\_CONNECTION\_POOLING attribute was introduced after ODBC API version 3.52 and is not supported. |
| `SQLSetStmtAttr` | ✔ | SQL\_ATTR\_CURSOR\_SCROLLABLE only supports a SQL\_NONSCROLLABLE value.   SQL\_ATTR\_USE\_BOOKMARKS only supports a SQL\_UB\_OFF value.   SQL\_ATTR\_CURSOR\_TYPE only supports a SQL\_CURSOR\_FORWARD\_ONLY value. In ODBC 4.x, any other value is replaced with SQL\_CURSOR\_FORWARD\_ONLY and the function returns SQL\_SUCCESS\_WITH\_INFO with SQLSTATE 01S02. ODBC 3.x returns SQL\_SUCCESS.     In ODBC 3.x, SQL\_ATTR\_ENABLE\_AUTO\_IPD defaults to true for compatibility with third-party tools, even though the ODBC standard says it should default to false. To change the default to false, set the [EnableAutoIpdByDefault](/developer-guide/odbc/odbc-parameters#label-odbc-configuration-parameters-enableautoipdbydefault) parameter to `false`.     ODBC 4.x doesn’t populate the implementation parameter descriptor automatically. SQL\_ATTR\_ENABLE\_AUTO\_IPD always reads SQL\_FALSE, setting it to SQL\_FALSE is accepted as a no-op, and setting it to SQL\_TRUE returns SQL\_ERROR with SQLSTATE HYC00. The EnableAutoIpdByDefault parameter doesn’t apply.     Setting SQL\_ATTR\_METADATA\_ID puts catalog function arguments into identifier mode, and the two versions fold unquoted identifiers differently. See [catalog functions](#label-odbc-api-catalog-functions).     Unsupported attributes: SQL\_ATTR\_SIMULATE\_CURSOR, SQL\_ATTR\_FETCH\_BOOKMARK\_PTR, SQL\_ATTR\_KEYSET\_SIZE. |
| `SQLGetStmtAttr` | ✔ | In addition to the standard attributes, the Snowflake implementation supports SQL\_SF\_STMT\_ATTR\_LAST\_QUERY\_ID and SQL\_SF\_STMT\_ATTR\_MULTI\_STATEMENT\_COUNT. See [Snowflake-specific behavior](#label-odbc-api-sqlsetconnectattr-specific-behavior). |
| `SQLSetStmtOption` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. Replaced by `SQLSetStmtAttr`. |
| `SQLGetStmtOption` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. Replaced by `SQLGetStmtAttr`. |
| `SQLParamOptions` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. Replaced by `SQLSetStmtAttr`. |

Expand

Show lessSee more

Each of the preceding functions has a corresponding function that accepts wide characters (unicode). Each such
unicode function has the name shown above, followed by “W”. For example, the function `SQLGetStmtAttr`, which
accepts a char array as the third parameter, has a corresponding function named `SQLGetStmtAttrW`, which accepts a
wchar array as the third parameter.

### Snowflake-specific behavior

- `SQLSetConnectAttr`

  > This method supports two Snowflake-specific attributes:
  >
  > | Attribute Name | Description |
  > | --- | --- |
  > | SQL\_SF\_CONN\_ATTR\_APPLICATION | This overrides the value specified by the APPLICATION setting in the registry or .ini file. |
  > | SQL\_SF\_CONN\_ATTR\_PRIV\_KEY | ODBC 3.x only. An `EVP_PKEY*` pointer to an in-memory copy of the private key. This overrides the `PRIV_KEY_FILE` and `PRIV_KEY_PWD` settings in the registry or .ini file. ODBC 4.x does not support this attribute. Set `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` or `SQL_SF_CONN_ATTR_PRIV_KEY_BASE64` with `SQLSetConnectAttr`, or use the `PRIV_KEY_FILE` DSN/connection-string keyword. See [Configuration differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-config). |
  >
  > Expand
  >
  > Show lessSee more
  >
  > In Snowflake ODBC driver version 3.4.0 and up, you can use the following additional attributes in `SQLSetConnectAttr`:
  >
  > | Attribute name | Description |
  > | --- | --- |
  > | `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` | Lets you pass the contents of a private key directly into the connection. Make sure to pass the full key contents, including the header and footer. |
  > | `SQL_SF_CONN_ATTR_PRIV_KEY_BASE64` | Lets you pass a base64-encoded private key directly into the connection. This attribute was introduced in version 3.11.0 of the ODBC driver. |
  > | `SQL_SF_CONN_ATTR_PRIV_KEY_PASSWORD` | If you’re passing an encrypted private key in the `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT`, this attribute lets you specify the password.  Using `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` might be necessary, if your application and the ODBC driver are linked to incompatible versions of OpenSSL, and you’re seeing crashes coming from the ODBC driver when key-pair authentication is used.  The following C++ code illustrates the implementation:  Copy code  ``` std::string fileContent = loadKeyFileContent(keyFilePath); SQLSetConnectAttr(dbc, SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT, (SQLPOINTER)fileContent.c_str(), SQL_NTS); ``` |
  >
  > Expand
  >
  > Show lessSee more
- `SQLSetStmtAttr` and `SQLGetStmtAttr`

  > These methods support two Snowflake-specific attributes:
  >
  > | Attribute name | Description |
  > | --- | --- |
  > | `SQL_SF_STMT_ATTR_LAST_QUERY_ID` | Read-only. Returns the query ID of the most recent statement run on the statement handle, or an empty string before the first execution. Both versions reject attempts to set it: ODBC 4.x returns SQL\_ERROR with SQLSTATE HY092, and ODBC 3.x returns an error saying the attribute isn’t settable. In ODBC 4.x, the query ID is populated after `SQLExecDirect` and after `SQLPrepare` followed by `SQLExecute`. A partial example is in the [Examples](#examples) section below. |
  > | `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` | Sets the number of statements in a multi-statement request, which enables multi-statement result sets through `SQLMoreResults`. Both driver versions support setting it. The default is `-1`, which leaves the count to the server. A value of 0 or greater is sent to the server as the `MULTI_STATEMENT_COUNT` parameter.     ODBC 4.x accepts `-1` through `32767` and returns SQL\_ERROR with SQLSTATE HY024 for a value outside that range, and `SQLGetStmtAttr` returns the value you set. ODBC 3.x accepts any value without validating the range, and reading the attribute back doesn’t reflect a value you set. |
  >
  > Expand
  >
  > Show lessSee more

## Setting and retrieving descriptor fields

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLGetDescField` | ✔ |  |
| `SQLGetDescRec` | ✔ |  |
| `SQLSetDescField` | ✔ |  |
| `SQLSetDescRec` | ✔ |  |

Expand

Show lessSee more

## Preparing SQL requests

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLAllocStmt` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLBindParameter` | ✔ |  |
| `SQLPrepare` | ✔ |  |
| `SQLGetCursorName` | ✔ |  |
| `SQLSetCursorName` | ✔ |  |
| `SQLSetScrollOptions` | ✔ | Supported by the Snowflake driver, but deprecated ODBC API. |
| `SQLSetParam` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 2.x. Replaced by `SQLBindParameter`. |

Expand

Show lessSee more

Note

- There is an upper limit to the size of data that you can bind. For details, see [Limits on Query Text Size](/user-guide/query-size-limits).
- [SQL Statements Supported for Preparation](/user-guide/sql-prepare) lists the types of SQL statements that are supported for preparation.

## Submitting requests

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLExecute` | ✔ |  |
| `SQLExecDirect` | ✔ |  |
| `SQLNativeSql` | ✔ |  |
| `SQLDescribeParam` | ✔ | Regardless of the data type bound to the parameter, Snowflake performs a server-side conversion and returns a VARCHAR with a maximum length of 134217728. |
| `SQLNumParams` | ✔ |  |
| `SQLParamData` | ✔ | Support for this function was added in version 2.23.3 of the ODBC Driver. |
| `SQLPutData` | ✔ | Support for this function was added in version 2.23.3 of the ODBC Driver. |

Expand

Show lessSee more

## Retrieving results and information about results

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLBindCol` | ✔ | The ODBC driver does not currently support semi-structured data, including `VARIANT`, `OBJECT` and `ARRAY` data types. |
| `SQLError` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. Replaced by `SQLGetDiagRec`. |
| `SQLGetData` | ✔ |  |
| `SQLGetDiagField` | ✔ |  |
| `SQLGetDiagRec` | ✔ |  |
| `SQLRowCount` | ✔ |  |
| `SQLNumResultCols` | ✔ |  |
| `SQLDescribeCol` | ✔ |  |
| `SQLColAttribute` | ✔ | For [GEOGRAPHY](/sql-reference/data-types-geospatial) columns, `SQL_DESC_TYPE_NAME` returns `GEOGRAPHY`. Note that other descriptors (e.g. `SQL_DESC_CONCISE_TYPE`) do not indicate that the column type is `GEOGRAPHY`. |
| `SQLColAttributes` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 2.x. Replaced by `SQLColAttribute`. |
| `SQLFetch` | ✔ |  |
| `SQLFetchScroll` | ✔ | The `FetchOrientation` argument supports the SQL\_FETCH\_NEXT value only. All other types of fetch fail. |
| `SQLExtendedFetch` |  | Replaced by `SQLFetchScroll` in API version 3.x driver. |
| `SQLSetPos` |  | Snowflake does not support the functionality. |
| `SQLBulkOperations` |  | Snowflake does not support the functionality. |

Expand

Show lessSee more

## Obtaining information about the data source’s system tables (catalog functions)

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLColumnPrivileges` |  | Returns an empty results set. |
| `SQLColumns` | ✔ | In ODBC 4.x, several catalog metadata columns follow the ODBC definitions of `COLUMN_SIZE` and `BUFFER_LENGTH` instead of the Snowflake storage widths that ODBC 3.x reported:     `REMARKS` and `COLUMN_DEF` return `SQL_NULL_DATA` when the value is absent, instead of an empty string.   `BUFFER_LENGTH` for `NUMBER` and `DECIMAL` is precision + 2. For example, `NUMBER(38,0)` reports 40.   `COLUMN_SIZE` for `FLOAT`, `DOUBLE`, and `REAL` is 15, the number of significant decimal digits.   `COLUMN_SIZE` for `TIMESTAMP` types is 20 + scale (19 when the scale is 0), and `BUFFER_LENGTH` is 16.   `BUFFER_LENGTH` for `DATE` and `TIME` is 6.   For `DATE`, `TIME`, and `TIMESTAMP` columns, `SQL_DATA_TYPE` returns the verbose type `SQL_DATETIME` and `SQL_DATETIME_SUB` returns the subtype. `DATA_TYPE` still returns the concise type.   `COLUMN_SIZE`, `BUFFER_LENGTH`, and `CHAR_OCTET_LENGTH` for `VARIANT`, `OBJECT`, `ARRAY`, `GEOGRAPHY`, and `GEOMETRY` follow the session `VARCHAR_AND_BINARY_MAX_SIZE_IN_RESULT` value.     For the full list, see [Behavior differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-behavior-differences). |
| `SQLForeignKeys` | ✔ | In ODBC 4.x, when `SQL_ATTR_METADATA_ID` is `SQL_TRUE`, an unquoted catalog, schema, or table name is folded to uppercase before the lookup, so a lowercase name matches the stored name. ODBC 3.x compared the name case-sensitively and returned an empty result set.     ODBC 4.x also treats an empty string table name the same as an omitted one when it chooses between `SHOW EXPORTED KEYS` and `SHOW IMPORTED KEYS`. If you pass an empty `PKTableName` with a populated `FKTableName`, ODBC 4.x scopes the query to the foreign key side and returns the relationship. ODBC 3.x returned an empty result set. |
| `SQLPrimaryKeys` | ✔ | In ODBC 4.x, when `SQL_ATTR_METADATA_ID` is `SQL_TRUE`, an unquoted catalog, schema, or table name is folded to uppercase before the lookup, so a lowercase name matches the stored name. ODBC 3.x compared the name case-sensitively and returned an empty result set. |
| `SQLProcedureColumns` | ✔ | In ODBC 4.x, `BUFFER_LENGTH` for `NUMBER` and `DECIMAL` columns is the ODBC transfer octet length, precision + 2, instead of the Snowflake storage width that ODBC 3.x returned. |
| `SQLProcedures` | ✔ | In the result set, the `NUM_INPUT_PARAMS` column contains the number of arguments for the procedure (the value of the max\_num\_arguments column in the output of the `SHOW PROCEDURES` command).     The `NUM_OUTPUT_PARAMS` column contains NULL values because stored procedures in Snowflake don’t support output parameters.     The `NUM_RESULT_SETS` column also contains NULL values because stored procedures in Snowflake don’t return result sets.     The `PROCEDURE_TYPE` column always contains `SQL_PT_FUNCTION` because stored procedures in Snowflake always return a value.     In ODBC 4.x, the `REMARKS` column returns `SQL_NULL_DATA` when a description is absent, instead of an empty string. |
| `SQLSpecialColumns` |  | Returns an empty results set. |
| `SQLStatistics` |  | Returns an empty results set. |
| `SQLTablePrivileges` |  | Returns an empty results set. |
| `SQLTables` | ✔ | If the parameter passed to the function is “TABLE”, the function returns all types of tables, including transient tables and temporary tables.     If the parameter passed to the function is “VIEW”, the function returns all types of views, including materialized views.     If the parameter passed to the function is “TABLE, VIEW” or “%”, the function returns information about all types of tables and all types of views.     In ODBC 4.x, the `REMARKS` column returns `SQL_NULL_DATA` when a comment is absent, instead of an empty string. |

Expand

Show lessSee more

If the name passed to the catalog function has an invalid character, or if the name does not match any database object, the function returns an empty result set.

Setting `SQL_ATTR_METADATA_ID` to `SQL_TRUE` puts the catalog function arguments into identifier mode. In ODBC 4.x, `SQLTables`, `SQLColumns`, `SQLPrimaryKeys`, `SQLForeignKeys`, `SQLProcedures`, and `SQLProcedureColumns` all honor the attribute.

In ODBC 4.x identifier mode, an unquoted name is folded to uppercase before the lookup, which matches how Snowflake stores unquoted identifiers, and a double-quoted name stays case-sensitive. ODBC 3.x compares an unquoted name case-sensitively against the stored uppercase name, so a lowercase name returns an empty result set. The default pattern mode (`SQL_FALSE`) is case-sensitive in both versions.

## Terminating a statement

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLFreeStmt` | ✔ |  |
| `SQLCloseCursor` | ✔ |  |
| `SQLCancel` | ✔ | When cancelling during a data-at-execution sequence, ODBC 4.x discards all of the data accumulated by `SQLPutData`, so a retry starts from a clean parameter. ODBC 3.x retained the accumulated data, and a retry concatenated the old and new chunks. |
| `SQLEndTran` | ✔ |  |
| `SQLTransact` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. Replaced by `SQLEndTran`. |

Expand

Show lessSee more

## Terminating a connection

| Function Name | Supported | Notes |
| --- | --- | --- |
| `SQLCancelHandle` | ✔ | With `SQL_HANDLE_STMT`, this function behaves the same as `SQLCancel`.     With `SQL_HANDLE_DBC`, driver doesn’t cancel anything, because asynchronous connection-level operations are not supported. ODBC 4.x returns SQL\_ERROR with SQLSTATE HY010 if a statement on the connection is executing asynchronously or is waiting for data-at-execution, and otherwise returns SQL\_SUCCESS without doing anything. ODBC 3.x always returns SQL\_SUCCESS without doing anything.     In ODBC 4.x, `SQL_HANDLE_ENV` and `SQL_HANDLE_DESC` return SQL\_ERROR with SQLSTATE HY092. |
| `SQLDisconnect` | ✔ |  |
| `SQLFreeHandle` | ✔ |  |
| `SQLFreeConnect` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |
| `SQLFreeEnv` | ✔ | Supported by the Snowflake driver, but deprecated in ODBC API version 3.x. |

Expand

Show lessSee more

## Custom SQL data types

Some SQL data types supported by Snowflake have no direct mapping in ODBC (e.g. TIMESTAMP\_\*tz, VARIANT). To enable the ODBC driver to work with
the unsupported data types, the header file shipped with the driver includes definitions for the following custom data types:

Copy code

```
////////////////////////////////////////////////////////////////////////////////////////////////////
/// Custom SQL Data Type Definition
///
///
////////////////////////////////////////////////////////////////////////////////////////////////////

#define SQL_SF_TIMESTAMP_LTZ 2000
#define SQL_SF_TIMESTAMP_TZ  2001
#define SQL_SF_TIMESTAMP_NTZ 2002
#define SQL_SF_ARRAY         2003
#define SQL_SF_OBJECT        2004
#define SQL_SF_VARIANT       2005
```

In ODBC 3.x, result set metadata reports these codes only when the `ODBC_USE_CUSTOM_SQL_DATA_TYPES` session parameter is `TRUE`, and the parameter defaults to `FALSE`. With the default, `SQLDescribeCol` and the `SQL_DESC_CONCISE_TYPE` descriptor field report `SQL_TYPE_TIMESTAMP` for all three TIMESTAMP variants (`SQL_TIMESTAMP` for an ODBC 2.x application) and `SQL_VARCHAR` for ARRAY, OBJECT, VARIANT, GEOGRAPHY, and GEOMETRY. Setting the parameter to `TRUE` reports the custom codes instead, with GEOGRAPHY and GEOMETRY both reporting `SQL_SF_OBJECT`, and changes the `SQL_DESC_TYPE_NAME` of the TIMESTAMP variants from `TIMESTAMP` to `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ`, or `TIMESTAMP_TZ`. The parameter doesn’t affect parameter binding, so you can pass these codes to `SQLBindParameter` whatever its value.

ODBC 4.x never reports these codes in result set metadata. There’s no equivalent of the `ODBC_USE_CUSTOM_SQL_DATA_TYPES` parameter, so the types always report the way ODBC 3.x reports them by default. `SQLGetTypeInfo` does publish all of them, along with VECTOR as code 2006.

ODBC 4.x accepts `SQL_SF_TIMESTAMP_LTZ`, `SQL_SF_TIMESTAMP_TZ`, and `SQL_SF_TIMESTAMP_NTZ` as the *ParameterType* argument of `SQLBindParameter`. It can’t bind semi-structured or vector values, so `SQL_SF_ARRAY`, `SQL_SF_OBJECT`, `SQL_SF_VARIANT`, and VECTOR return SQL\_ERROR with SQLSTATE HYC00 at bind time. A vendor code that `SQLGetTypeInfo` doesn’t publish at all, such as 2007, returns SQLSTATE HY004 instead, which distinguishes a type the driver knows but can’t bind from one it doesn’t recognize. ODBC 3.x accepts the semi-structured codes at bind time and fails later during execution with SQLSTATE HY000. To insert a semi-structured value in either version, bind it as `SQL_VARCHAR` and convert it in the statement with `PARSE_JSON(?)`, `TO_ARRAY(?)`, or `TO_OBJECT(?)`.

The following code demonstrates sample usage of the custom data types:

Copy code

```
// bind insert as timestamp_ntz
SQLRETURN rc;
rc = SQLPrepare(odbc.StmtHandle,
               (SQLCHAR *) "insert into testtimestampntz values (?)",
               SQL_NTS);

 SQL_TIMESTAMP_STRUCT bindData;
 SQLLEN datalen = sizeof(SQL_TIMESTAMP_STRUCT);
 bindData.year = 2017;
 bindData.month = 11;
 bindData.day = 30;
 bindData.hour = 18;
 bindData.minute = 17;
 bindData.second = 5;
 bindData.fraction = 123456789;

 rc = SQLBindParameter(
   odbc.StmtHandle, 1, SQL_PARAM_INPUT,
   SQL_C_TIMESTAMP, SQL_SF_TIMESTAMP_NTZ,
   100, 0, &bindData, sizeof(bindData), &datalen);

 rc = SQLExecute(odbc.StmtHandle);

 // query table
 rc = SQLExecDirect(odbc.StmtHandle, (SQLCHAR *)"select * from testtimestampntz", SQL_NTS);

 rc = SQLFetch(odbc.StmtHandle);

 // fetch data as timestamp
 SQL_TIMESTAMP_STRUCT ret;
 SQLLEN retLen = (SQLLEN) 0;
 rc = SQLGetData(odbc.StmtHandle, 1, SQL_C_TIMESTAMP, &ret, (SQLLEN)sizeof(ret), &retLen);
```

## Examples

This section provides examples of using the API.

### Retrieving the last query ID

Retrieving the last query ID is a Snowflake extension to the ODBC standard.

To retrieve the last query ID, call the function `SQLGetStmtAttr` (or `SQLGetStmtAttrW`), passing the attribute
SQL\_SF\_STMT\_ATTR\_LAST\_QUERY\_ID and a character array large enough to hold the query ID.

The example below shows how to retrieve the query ID for a query:

Copy code

```
// Space to store the query ID.
// The SQLGetStmtAttr() function fills this in with the actual ID.
char queryId[37];   // Maximum 36 chars plus string terminator.

// The length (in characters) of the query ID. The SQLGetStmtAttr() function fills this in
// with the actual length of the query ID (usually 36).
SQLINTEGER idLen;

// Execute a query.
rc = SQLExecDirect(odbc.StmtHandle, (SQLCHAR *) "select 1", SQL_NTS);

// Retrieve the query ID (queryId) and the length of that query ID (idLen).
SQLGetStmtAttr(odbc.StmtHandle, SQL_SF_STMT_ATTR_LAST_QUERY_ID, queryId, sizeof(queryId), &idLen);
```

If you are executing on Linux or macOS, call `SQLGetStmtAttrW` and pass parameters
of the appropriate data type (for example, “wchar” rather than “char”).

### Best practices to improve performance when retrieving data

When retrieving data with `SQLFetch`, you can use the `SQLGetData` or `SQLBindCol` functions to access
the contents of the cells. In most cases, using `SQLBindCol` provides better performance because it reduces the number
of ODBC calls you need to make to retrieve data and because it lets you take advantage of copying data in-memory.

#### Using `SQLGetData` to retrieve cell data

The following example uses the `SQLGetData` function to retrieve cell values from the data buffer returned
by `SQLFetch`. Notice that you need to call `SQLGetData` once for each cell in the row.

Copy code

```
SQLRETURN rc;
SQLSMALLINT numCols;
const size_t s_MaxDataLen = 300;

// fetch with SQLGetData()
// query table
rc = SQLExecDirect(stmt, (SQLCHAR *)"select * from table", SQL_NTS);

// Find out the number of result set columns.
rc = SQLNumResultCols(stmt, &numCols);

// buffer for one cell
vector<char> dataBuffer(s_MaxDataLen);
SQLLEN dataLen = (SQLLEN)0;

// call SQLFetch() per row and SQLGetData() per column per row
while (true)
{
    rc = SQLFetch(stmt);
    if ((rc != SQL_SUCCESS) && (rc != SQL_SUCCESS_WITH_INFO))
    {
        break;
    }
    for (SQLUSMALLINT i = 0; i < numCols; i++)
    {
        rc = SQLGetData(stmt, i + 1, SQL_C_CHAR, dataBuffer.data(), (SQLLEN)s_MaxDataLen, &dataLen);
        std::string data;
        if (SQL_NULL_DATA == dataLen)
            continue;
        if (SQL_NO_TOTAL == dataLen)
            dataLen = s_MaxDataLen;
        data = std::string(dataBuffer.data(), dataLen);
    }
}
rc = SQLCloseCursor(stmt);
```

#### Using `SQLBindCol` to bind the columns for one row of data

The following example uses the `SQLBindCol` function to retrieve cell values from the data buffer returned by
`SQLFetch`. It creates an in-memory buffer for the number of columns in a row and then makes a single
`SQLBindCol` call to bind the application buffers to the result set. Finally, it calls `SQLFetch` once per row and
loads the cell values into the buffer. This approach can significantly increase the speed and efficiency of retrieving data.

Copy code

```
SQLRETURN rc;
SQLSMALLINT numCols;
const size_t s_MaxDataLen = 300;

// fetch with SQLBindCol()
// query table
rc = SQLExecDirect(stmt, (SQLCHAR *)"select * from table", SQL_NTS);

// Find out the number of result set columns.
rc = SQLNumResultCols(stmt, &numCols);

// buffer for one row
vector<char> rowBuffer(s_MaxDataLen * numCols);
vector<SQLLEN> columnLenBuffer(numCols);

// call SQLBindCol() per column
for (SQLSMALLINT i = 0; i < numCols; ++i)
{
    SQLBindCol(stmt, i + 1, SQL_C_CHAR, &rowBuffer[s_MaxDataLen * i],
               s_MaxDataLen, &columnLenBuffer[i]);
}

// call SQLFetch() per row
while (true)
{
    rc = SQLFetch(stmt);
    if ((rc != SQL_SUCCESS) && (rc != SQL_SUCCESS_WITH_INFO))
    {
         break;
    }
    // go through data for each cell in buffer without ODBC calls
    for (SQLUSMALLINT i = 0; i < numCols; i++)
    {
        std::string data;
        SQLLEN len = columnLenBuffer[i];
        if (SQL_NULL_DATA == len)
            continue;
        if (SQL_NO_TOTAL == len)
            len = s_MaxDataLen;
        data = std::string(&rowBuffer[s_MaxDataLen * i], len);
    }
}
rc = SQLCloseCursor(stmt);
```

#### Using `SQLBindCol` to bind the columns for multiple rows of data

You can improve performance even more by fetching multiple rows in a single `SQLFetch` call, which reduces
the number of ODBC `SQLFetch` calls needed to process all the rows of a query table.

The following example:

- Determines the number of columns in the result set.
- Creates an in-memory array to store the data from multiple columns.
- Calls `SQLBindCol` for each column to bind the application buffers to the result set.
- Calls `SQLFetch` to get the specified number of rows (100) and processes the data in the in-memory buffer without making ODBC calls, until the end of the query table is reached.

This approach can significantly increase the speed and efficiency of retrieving data. For a query table with 20 columns and 1000 rows, this example would make only 20 `SQLBindCol` and 10 `SQLFetch` calls instead of 20000 `SQLGetData` calls to load all of the table data.

Copy code

```
SQLRETURN rc;
SQLSMALLINT numCols;
const size_t s_MaxDataLen = 300;

// fetch with SQLBindCol() and SQL_ATTR_ROW_ARRAY_SIZE > 1
const size_t s_numRowsPerSQLFetch = 100;
SQLULEN numRowsFetched = 0;
rc = SQLSetStmtAttr(stmt, SQL_ATTR_ROW_ARRAY_SIZE, (SQLPOINTER)s_numRowsPerSQLFetch, 0);
rc = SQLSetStmtAttr(stmt, SQL_ATTR_ROWS_FETCHED_PTR, (SQLPOINTER)&numRowsFetched, sizeof(SQLULEN));

// query table
rc = SQLExecDirect(stmt, (SQLCHAR *)"select * from table", SQL_NTS);

// Find out the number of result set columns.
rc = SQLNumResultCols(stmt, &numCols);

// buffer for all columns; each column has buffer size of s_numRowsPerSQLFetch
// To retrieve multiple rows per SQLFetch() call, use the default behavior of SQL_BIND_BY_COLUMN
vector<vector<char> > colArray(numCols);
vector<vector<SQLLEN> > colLenArray(numCols);

// call SQLBindCol() per column
for (SQLSMALLINT i = 0; i < numCols; ++i)
{
    // initialize buffer for each column
    colArray[i].resize(s_MaxDataLen * s_numRowsPerSQLFetch);
    colLenArray[i].resize(s_numRowsPerSQLFetch);

    SQLBindCol(stmt, i + 1, SQL_C_CHAR, colArray[i].data(),
                s_MaxDataLen, colLenArray[i].data());
}

// call SQLFetch() per s_numRowsPerSQLFetch rows
while (true)
{
    rc = SQLFetch(stmt);
    if ((rc != SQL_SUCCESS) && (rc != SQL_SUCCESS_WITH_INFO))
    {
        break;
    }
    // go through data for each cell in buffer without ODBC calls
    for (SQLULEN rowIndex = 0; rowIndex < numRowsFetched; rowIndex++)
    {
        for (SQLUSMALLINT colIndex = 0; colIndex < numCols; colIndex++)
        {
            std::string data;
            SQLLEN len = colLenArray[colIndex][rowIndex];
            if (SQL_NULL_DATA == len)
                continue;
            if (SQL_NO_TOTAL == len)
                len = s_MaxDataLen;
            data = std::string(&(colArray[colIndex][s_MaxDataLen * rowIndex]), len);
        }
    }
}
rc = SQLCloseCursor(stmt);
```
