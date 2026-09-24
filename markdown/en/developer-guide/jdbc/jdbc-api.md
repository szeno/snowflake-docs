# JDBC Driver API support

The Snowflake JDBC driver is a JDBC type 4 driver that supports the core JDBC functionality in version 1.0 of the JDBC API. You are welcome to try methods from later
versions of the API, but Snowflake does not guarantee that these methods are supported.

For the complete API reference, see the [Java SE Technologies documentation](http://www.oracle.com/technetwork/java/javase/jdbc/index.html).

The Snowflake JDBC driver requires Java LTS (Long-Term Support) versions 1.8 or higher. The driver requires the `java.sql` package, which is included in the Standard Edition (SE) and the Enterprise Edition (EE)
of Java.

As of August, 2019, the `java.sql` package documentation is available at <https://docs.oracle.com/javase/8/docs/api/java/sql/package-summary.html>

The driver can be used with most client tools and applications that support JDBC for connecting to a database server.

This topic does not document the entire JDBC API. Instead, the topic:

- Lists the supported interfaces from the JDBC API and the supported methods within each interface.
- Documents areas where Snowflake extends the JDBC API standard.
- Documents areas where the JDBC API standard is ambiguous and the Snowflake implementation might behave differently
  from other systems.

In general, if a method is called and fails, the method will raise an exception (e.g. `SQLException`).

The supported JDBC interfaces are listed alphabetically and paired with their corresponding Snowflake extension classes (where applicable).

## Object: `CallableStatement`

A CallableStatement is used to execute a stored procedure.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| None | `CallableStatement` extends `PreparedStatement`, so inherited methods such as `execute()`, `executeQuery()`, and the indexed `setXxx(int, ...)` setters still work. The `CallableStatement`-specific methods listed under **Unsupported Methods** throw `SQLFeatureNotSupportedException` because Snowflake stored procedures don’t accept OUT or INOUT parameters. |
| **Unsupported Methods** |  |
| `getBigDecimal(int, int)` |  |
| `getBoolean(int)` |  |
| `getByte(int)` |  |
| `getBytes(int)` |  |
| `getDate(int)` |  |
| `getDouble(int)` |  |
| `getFloat(int)` |  |
| `getInt(int)` |  |
| `getLong(int)` |  |
| `getObject(int)` |  |
| `getShort(int)` |  |
| `getString(int)` |  |
| `getTime(int)` |  |
| `getTimestamp(int)` |  |
| `registerOutParameter(int, int, int)` |  |
| `registerOutParameter(int, int)` |  |
| `wasNull()` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

None.

## Interface: `SnowflakeCallableStatement`

The SnowflakeCallableStatement interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type CallableStatement, for example by calling the
Connection.prepareCall() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC CallableStatement interface and the
SnowflakeCallableStatement interface. To access the SnowflakeCallableStatement methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

| Method Name | Description |
| --- | --- |
| `getQueryID()` | Returns the Snowflake query ID of the most recently executed query of this `CallableStatement` |

Expand

Show lessSee more

getQueryID()
:   Purpose:
    :   This method returns the Snowflake query ID of the most recently executed query of this `CallableStatement`. If no
        query has been executed yet with the callable statement, the method returns null.

    Arguments:
    :   None.

    Returns:
    :   This method returns the ID as a String that contains a UUID.
        Information about UUIDs is included in the description of the SQL function
        [UUID\_STRING](/sql-reference/functions/uuid_string).

    Throws:
    :   The method can throw `SQLException`.

## Object: `Connection`

A `Connection` object represents a connection to a database server. The connection object allows users not only
to connect to a particular database server, but also create `Statement` objects, which can be used to
execute SQL statements.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `abort()` |  |
| `clearWarnings()` |  |
| `close()` | Snowflake-specific behavior (see below). |
| `commit()` |  |
| `createStatement()` |  |
| `createStatement(int, int)` |  |
| `createStatement(int, int, int)` |  |
| `getAutoCommit()` |  |
| `getCatalog()` |  |
| `getClientInfo()` |  |
| `getHoldability()` |  |
| `getMetaData()` | Snowflake-specific behavior (see below). |
| `getSchema()` |  |
| `getTransactionIsolation()` |  |
| `getTypeMap()` |  |
| `getWarnings()` |  |
| `isClosed()` |  |
| `isReadOnly()` |  |
| `isValid()` |  |
| `nativeSQL(String)` |  |
| `prepareCall(String)` |  |
| `prepareCall(String, boolean)` |  |
| `prepareCall(String, int, int)` |  |
| `prepareCall(String, int, int, int)` |  |
| `prepareStatement(String)` |  |
| `prepareStatement(String, int)` |  |
| `prepareStatement(String, int[])` |  |
| `prepareStatement(String, String[])` |  |
| `prepareStatement(String, int, int)` |  |
| `prepareStatement(String, int, int, int)` | Snowflake-specific behavior (see below) |
| `prepareStatement(String, boolean)` |  |
| `setAutoCommit(boolean)` |  |
| `setCatalog(String)` |  |
| `setClientInfo(String, String)` | Calling this method causes a `SQLClientInfoException`. |
| `setClientInfo(Properties)` | Calling this method causes a `SQLClientInfoException`. |
| `setReadOnly(boolean)` |  |
| `setSchema(String)` |  |
| **Unsupported Methods** |  |
| `rollback()` |  |
| `setTransactionIsolation(int)` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

- `close()`
  Closes the object. After an object has been closed, calling almost any method of the closed object will raise a `SQLException`. Calling
  `close` on an already closed object is harmless and will not raise an exception.

- `getMetaData()`
  Lets you get metadata about the JDBC driver and Snowflake. For example, you can find out whether transactions are supported.

  For more information about the methods that you can call on the returned value,
  see [Object:](#label-jdbc-database-meta-data).
- `prepareStatement(String sql)`

  > This method returns a `preparedStatement` object that can be used to execute the SQL statement.
  > The `preparedStatement` object’s `execute()` method can be called to
  > execute the statement. The statement can be executed as-is, or after binding values to the statement.
  >
  > Note
  >
  > In some systems, after a statement has been prepared, that statement can be executed repeatedly without re-compiling the statement.
  > Preparing once and executing repeatedly can save a small amount of time and resources.
  >
  > In Snowflake, prepareStatement() does not actually compile the code. Instead,
  > `PreparedStatement.execute()`, `PreparedStatement.executeQuery()`,
  > and `PreparedStatement.executeUpdate()` compile and execute the statement.
  > Therefore preparing the statement before execution does not save resources
  > compared to simply using `Statement.execute()`.
- `prepareCall(String sql)`
- `prepareCall(String sql, boolean)`
- `prepareCall(String sql, int, int)`
- `prepareCall(String sql, int, int, int)`
  As in most JDBC implementations, the `prepareCall` methods can be used to bind parameters to a stored procedure. For example, the
  following is supported:

  Copy code

  ```
  CallableStatement stmt = testConnection.prepareCall("call read_result_set(?,?) ");
  ```

  However, in the Snowflake JDBC Driver, the `prepareCall` methods do not support the `? =` syntax to support binding the return value of a stored procedure.
  For example, the following is not supported:

  Copy code

  ```
  CallableStatement stmt = testConnection.prepareCall("? = call read_result_set() ");  -- INVALID
  ```

## Interface: `SnowflakeConnection`

The SnowflakeConnection interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type Connection, for example by calling the
DriverManager.getConnection() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC Connection interface and the
SnowflakeConnection interface. To access the SnowflakeConnection methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

These methods are in addition to the methods supported by the JDBC `Connection` interface.

| Method Name | Description |
| --- | --- |
| `createResultSet(String)` | Given the query ID of an asynchronously-launched SQL statement, retrieves the query results and returns them in a ResultSet object. |
| `downloadStream(String, String, boolean)` | Downloads a file from the given internal stage and returns an InputStream. |
| `getSessionID()` | Gets the session ID of the current session. |
| `prepareStatement(String, Boolean)` | Overloaded `prepareStatement()` method (see below for details). |
| `uploadStream(String, String, InputStream, String, boolean)` | Compresses data from a stream and uploads it to the specified path and file name in an internal stage. |

Expand

Show lessSee more

public ResultSet createResultSet(String queryID)
:   Purpose:
    :   Given the queryID of an [asynchronously-launched SQL statement](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), retrieve the
        query results and return them in a ResultSet object.

        This method can typically be called up to 24 hours after the SQL statement finished.

    Arguments:
    :   queryID: The query ID of the query for which you want the results.

    Returns:
    :   The ResultSet. If the query has not yet finished running, the server returns an “empty” ResultSet. The user
        can call `resultSet.unwrap(SnowflakeResultSet.class).getStatus()` to find out when the data is available.

    Throws:
    :   This method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the Connection object.

    Examples:
    :   Copy code

        ```
        ResultSet resultSet;
        resultSet = connection.unwrap(SnowflakeConnection.class).createResultSet(queryID);
        ```

        See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for a more extensive example that includes a call to this
        method.

public InputStream downloadStream(String stageName, String sourceFileName, boolean decompress)
:   Purpose:
    :   This method downloads a file from the given internal stage and returns an input stream.

    Arguments:
    :   stageName: Stage name.

        sourceFileName: File path in stage.

        decompress: True if file compressed.

    Returns:
    :   This method returns an InputStream.

    Throws:
    :   This method throws SQLException if a SQL error occurs.

    Examples:
    :   For a partial example, see [Download data files directly from an internal stage to a stream](/developer-guide/jdbc/jdbc-using#label-jdbc-download-from-stage-to-stream).

public String getSessionID()
:   Purpose:
    :   This method returns the session ID of the current session.

    Arguments:
    :   None

    Returns:
    :   Returns the session ID as a String.

    Throws:
    :   This method throws SQLException if any SQL error occurs, for example if the connection is closed.

    Usage Notes:
    :   Since the session ID does not change while the connection is open, the session ID is cached locally (rather
        than retrieved from the server each time) to improve performance.

public prepareStatement(String sql, Boolean skipParsing)
:   This method is deprecated. The skipParsing parameter no longer affects the behavior of the method; this
    method behaves the same as the `prepareStatement(String sql)` method, regardless of the setting of the
    skipParsing parameter.

    New code should use the method `prepareStatement(String sql)`.

    When convenient, existing code that uses the two-argument version of this method should be updated to use
    the one-argument method `prepareStatement(String sql)`.

public void uploadStream(String stageName, String destPrefix, InputStream inputStream, String destFileName, boolean compressData)
:   Purpose:
    :   This method compresses data from a stream and uploads it at an internal stage location.
        The data will be uploaded as one file. No splitting is done in this method.

    Arguments:
    :   stageName: Stage name (e.g. `~` or table name or stage name).

        destPrefix: Path / prefix under which the data should be uploaded on the stage.

        inputStream: Input stream from which the data will be uploaded.

        destFileName: Destination file name to use.

        compressData: Compress data or not before uploading stream.

    Returns:
    :   Nothing.

    Throws:
    :   This method throws a `java.sql.SQLException` if it failed to compress and put data from a stream at the stage.

    Notes:
    :   The caller is responsible for releasing the `inputStream` after the method is called.

    Examples:
    :   For a partial example, see [Upload data files directly from a stream to an internal stage](/developer-guide/jdbc/jdbc-using#label-jdbc-upload-from-stream-to-stage).

## Object: `DatabaseMetaData`

The DatabaseMetaData class provides information about the features that the database server (in this case,
Snowflake) supports.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `allProceduresAreCallable()` |  |
| `allTablesAreSelectable()` |  |
| `dataDefinitionCausesTransactionCommit()` |  |
| `dataDefinitionIgnoredInTransactions()` |  |
| `doesMaxRowSizeIncludeBlobs()` |  |
| `getCatalogs()` |  |
| `getCatalogSeparator()` |  |
| `getCatalogTerm()` |  |
| `getColumnPrivileges(String, String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `columnNamePattern` argument. Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schemaPattern`, `tableNamePattern`, and `columnNamePattern` arguments. See [Snowflake-specific behavior](#label-jdbc-database-meta-data-snowflake-specific-behavior) for additional information about this method. |
| `getColumns(String, String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern`, `tableNamePattern`, and `columnNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schemaPattern`, `tableNamePattern`, and `columnNamePattern` arguments. |
| `getCrossReference(String, String, String, String, String, String)` | Supports [null](#label-database-meta-data-null-support) for the `parentCatalog`, `parentSchema`, `parentTable`, `foreignCatalog`, `foreignSchema`, and `foreignTable` arguments. |
| `getDatabaseProductName()` |  |
| `getDatabaseProductVersion()` |  |
| `getDefaultTransactionIsolation()` |  |
| `getDriverMajorVersion()` |  |
| `getDriverMinorVersion()` |  |
| `getDriverName()` |  |
| `getDriverVersion()` |  |
| `getExportedKeys(String, String, String)` | Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schema`, and `table` arguments. |
| `getExtraNameCharacters()` |  |
| `getFunctionColumns()` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern`, `functionNamePattern`, and `columnNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `columnNamePattern` argument. |
| `getFunctions(String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern` and `functionNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `schemaPattern` and `functionNamePattern` arguments. |
| `getIdentifierQuoteString()` |  |
| `getImportedKeys(String, String, String)` | Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schema`, and `table` arguments. |
| `getIndexInfo(String, String, String, boolean, boolean)` |  |
| `getMaxBinaryLiteralLength()` |  |
| `getMaxCatalogNameLength()` |  |
| `getMaxCharLiteralLength()` |  |
| `getMaxColumnNameLength()` |  |
| `getMaxColumnsInGroupBy()` |  |
| `getMaxColumnsInIndex()` |  |
| `getMaxColumnsInOrderBy()` |  |
| `getMaxColumnsInSelect()` |  |
| `getMaxColumnsInTable()` |  |
| `getMaxConnections()` |  |
| `getMaxCursorNameLength()` |  |
| `getMaxIndexLength()` |  |
| `getMaxProcedureNameLength()` |  |
| `getMaxRowSize()` |  |
| `getMaxSchemaNameLength()` |  |
| `getMaxStatementLength()` |  |
| `getMaxStatements()` |  |
| `getMaxTableNameLength()` |  |
| `getMaxTablesInSelect()` |  |
| `getMaxUserNameLength()` |  |
| `getNumericFunctions()` |  |
| `getPrimaryKeys(String, String, String)` | Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schema`, and `table` arguments. |
| `getProcedureColumns(String, String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern`, `procedureNamePattern`, and `columnNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `columnNamePattern` argument. |
| `getProcedures(String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern` and `procedureNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `columnNamePattern` argument. |
| `getProcedureTerm()` |  |
| `getSchemas()` |  |
| `getSchemas(String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern` argument. Supports [null](#label-database-meta-data-null-support) for the `catalogName` and `schemaPattern` arguments. |
| `getSchemaTerm()` |  |
| `getSearchStringEscape()` |  |
| `getSQLKeywords()` |  |
| `getSQLStateType()` |  |
| `getStreams(String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `originalSchemaPattern` and `streamName` arguments. Supports [null](#label-database-meta-data-null-support) for the `originalCatalog`, `originalSchemaPattern`, and `streamName` arguments. See [Snowflake-specific behavior](#label-jdbc-database-meta-data-snowflake-specific-behavior) for additional information about this method. |
| `getStringFunctions()` |  |
| `getSystemFunctions()` |  |
| `getTablePrivileges(String, String, String)` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern` and `tableNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `catalog` and `schemaPattern` arguments. |
| `getTables(String, String, String, String[])` | Supports [wildcards](#label-database-meta-data-wildcard-support) for the `schemaPattern` and `tableNamePattern` arguments. Supports [null](#label-database-meta-data-null-support) for the `catalog`, `schemaPattern`, `tableNamePattern`, and `types` arguments. |
| `getTableTypes()` |  |
| `getTimeDateFunctions()` |  |
| `getTypeInfo()` |  |
| `getURL()` |  |
| `getUserName()` |  |
| `isCatalogAtStart()` |  |
| `isReadOnly()` |  |
| `nullPlusNonNullIsNull()` |  |
| `nullsAreSortedAtEnd()` |  |
| `nullsAreSortedAtStart()` |  |
| `nullsAreSortedHigh()` |  |
| `nullsAreSortedLow()` |  |
| `storesLowerCaseIdentifiers()` |  |
| `storesLowerCaseQuotedIdentifiers()` |  |
| `storesMixedCaseIdentifiers()` |  |
| `storesMixedCaseQuotedIdentifiers()` |  |
| `storesUpperCaseIdentifiers()` |  |
| `storesUpperCaseQuotedIdentifiers()` |  |
| `supportsAlterTableWithAddColumn()` |  |
| `supportsAlterTableWithDropColumn()` |  |
| `supportsANSI92EntryLevelSQL()` |  |
| `supportsANSI92FullSQL()` |  |
| `supportsANSI92IntermediateSQL()` |  |
| `supportsCatalogsInDataManipulation()` |  |
| `supportsCatalogsInIndexDefinitions()` |  |
| `supportsCatalogsInPrivilegeDefinitions()` |  |
| `supportsCatalogsInProcedureCalls()` |  |
| `supportsCatalogsInTableDefinitions()` |  |
| `supportsColumnAliasing()` |  |
| `supportsConvert()` |  |
| `supportsConvert(int, int)` |  |
| `supportsCoreSQLGrammar()` |  |
| `supportsCorrelatedSubqueries()` |  |
| `supportsDataDefinitionAndDataManipulationTransactions()` |  |
| `supportsDataManipulationTransactionsOnly()` |  |
| `supportsDifferentTableCorrelationNames()` |  |
| `supportsExpressionsInOrderBy()` |  |
| `supportsExtendedSQLGrammar()` |  |
| `supportsFullOuterJoins()` |  |
| `supportsGroupBy()` |  |
| `supportsGroupByBeyondSelect()` |  |
| `supportsGroupByUnrelated()` |  |
| `supportsIntegrityEnhancementFacility()` |  |
| `supportsLikeEscapeClause()` |  |
| `supportsLimitedOuterJoins()` |  |
| `supportsMinimumSQLGrammar()` |  |
| `supportsMixedCaseIdentifiers()` |  |
| `supportsMixedCaseQuotedIdentifiers()` |  |
| `supportsMultipleResultSets()` |  |
| `supportsMultipleTransactions()` |  |
| `supportsNonNullableColumns()` |  |
| `supportsOpenCursorsAcrossCommit()` |  |
| `supportsOpenCursorsAcrossRollback()` |  |
| `supportsOpenStatementsAcrossCommit()` |  |
| `supportsOpenStatementsAcrossRollback()` |  |
| `supportsOrderByUnrelated()` |  |
| `supportsOuterJoins()` |  |
| `supportsPositionedDelete()` |  |
| `supportsPositionedUpdate()` |  |
| `supportsSchemasInDataManipulation()` |  |
| `supportsSchemasInIndexDefinitions()` |  |
| `supportsSchemasInPrivilegeDefinitions()` |  |
| `supportsSchemasInProcedureCalls()` |  |
| `supportsSchemasInTableDefinitions()` |  |
| `supportsSelectForUpdate()` |  |
| `supportsStoredProcedures()` |  |
| `supportsSubqueriesInComparisons()` |  |
| `supportsSubqueriesInExists()` |  |
| `supportsSubqueriesInIns()` |  |
| `supportsSubqueriesInQuantifieds()` |  |
| `supportsTableCorrelationNames()` |  |
| `supportsTransactionIsolationLevel(int)` |  |
| `supportsTransactions()` |  |
| `supportsUnion()` |  |
| `supportsUnionAll()` |  |
| `usesLocalFilePerTable()` |  |
| `usesLocalFiles()` |  |
| **Unsupported Methods** |  |
| `getBestRowIdentifier(String, String, String, int, boolean)` |  |
| `getVersionColumns(String, String, String)` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

public ResultSet getColumnPrivileges(String, String, String, String)
:   This method always returns an empty set because Snowflake does not support column-level privileges.

public ResultSet getStreams(String, String, String)
:   Purpose:
    :   This method returns information about [streams](/user-guide/streams-intro) contained within specified databases and schemas.

    Arguments:
    :   - `originalCatalog`: Name of the database.
        - `originalSchemaPattern`: Pattern to identify the schema (supports [wildcards](#label-database-meta-data-wildcard-support)).
        - `streamName`: Name of the stream (supports [wildcards](#label-database-meta-data-wildcard-support)).

    Returns:
    :   This method returns a `ResultSet` containing rows for each stream, with each row including the following columns:

        - `name`: Name of the stream.
        - `database_name`: Name of the database for the schema containing the stream.

          A database object (e.g. a stream) is contained in a schema, which in turn is contained in a database.
        - `schema_name`: Name of the schema containing the stream.
        - `owner`: Role that owns the stream.
        - `comment`: Comments associated with the stream.
        - `table_name`: Name of the table whose DML updates are tracked by the stream.
        - `source_type`: Source object for the stream. Possible values include:

          - `table`
          - `view`
          - `directory table`
          - `external table`
        - `base_tables`: Underlying tables for the view. This column applies only to streams on views.
        - `type`: Type of the stream. Currently, the function always returns `DELTA`.
        - `stale`: Whether the stream was last read before the `stale_after` time passed. If `TRUE`, the stream might be stale.

          When a stream is stale, it cannot be read. You can recreate the stream to resume reading from it. To prevent
          a stream from become stale, you should consume the stream before the `stale_after` time has passed.
        - `mode`: Type of stream. Possible values include:

          - `APPEND_ONLY`: Indicates the stream is an append-only stream.
          - `INSERT_ONLY`: Indicates the stream only returns information for inserted rows. This value applies only to streams on external tables.
          - `DEFAULT`: Indicates the stream is on tables.

    Throws:
    :   This method throws an `SQLException` if a SQL error occurs.

### Support for null parameters

Some DatabaseMetaData methods accept `null` values for database object names (e.g. table/catalog names).
By default, a `null` value means that the method does not filter on that argument. For example, if you pass
`getColumns()` a `null` value for the `schemaPattern` argument, then `getColumns()` returns values
for all schemas.

For some of those methods, the default behavior for `null` arguments can be overridden with the following
[parameters](/sql-reference/parameters):

- [CLIENT\_METADATA\_REQUEST\_USE\_CONNECTION\_CTX](/sql-reference/parameters#label-client-metadata-request-use-connection-ctx).
- [CLIENT\_METADATA\_USE\_SESSION\_DATABASE](/sql-reference/parameters#label-client-metadata-use-session-database).

### Support for wildcards in database object names

Some DatabaseMetaData methods support pattern-matching wildcards in database object names, such as table/catalog
names. The supported wildcard characters are:

- `%`: Matches any string of zero or more characters.
- `_`: Matches any one character.

The following example shows what to pass to the `getColumns()` method to get the names of all tables and all
columns in the specified database (`TEMPORARYDB1`) and schema (`TEMPORARYSCHEMA1`):

Copy code

```
getColumns( connection,
    "TEMPORARYDB1",      // Database name.
    "TEMPORARYSCHEMA1",  // Schema name.
    "%",                 // All table names.
    "%"                  // All column names.
    );
```

It is common for database object names, such as table names, to contain underscores, for example
`SHIPPING_ADDRESSES`. Searching for `SHIPPING_ADDRESSES` without escaping the underscore will of course
find not only the table named `SHIPPING_ADDRESSES`, but also tables such as `SHIPPING2ADDRESSES`. If
you want to search for `SHIPPING_ADDRESSES`, but not `SHIPPING2ADDRESSES`, then you need to escape the
wildcard character to indicate that you want it treated as a literal. To escape the character, precede it with a
backslash.

The backslash character itself must also be escaped if you want to use it as a literal character. For example, to
search for a table named `T_&`, in which the underscore, the ampersand, and the backslash are literal parts
of the name, not wildcard characters or escape characters, the method call should look similar to the following:

Copy code

```
");
getColumns(
    connection, "TEMPORARYDB1", "TEMPORARYSCHEMA1", "T\\_\\\\", "%" // All column names.
    );
System.out.println("//
```

Each backslash above must be escaped an extra time because the Java compiler expects backslashes to be escaped:

Copy code

```
Java sees...............: T\\_\\%\\\\
SQL sees................: T\_\%\\
The actual table name is: T_%\
```

## Object: `Driver`

The Driver provides methods that allow you to get a connection to the database, as well as get information
about the driver itself.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `acceptsURL(String)` |  |
| `connect(String, Properties)` |  |
| `getMajorVersion()` |  |
| `getMinorVersion()` |  |
| `getPropertyInfo(String, Properties)` |  |
| `isDisableIncidents()` |  |
| `jdbcCompliant()` |  |
| `setDisableIncidents()` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

None.

### Examples

The following code snippet shows part of a program to get property information:

Copy code

```
-
  // Demonstrate the Driver.getPropertyInfo() method.
  public static void do_the_real_work(String connectionString) throws Exception {
    Properties properties = new Properties();
    Driver driver = DriverManager.getDriver(connectionString);
    DriverPropertyInfo[] dpinfo = driver.getPropertyInfo("", properties);
    System.out.println(dpinfo[0].description);
  }
```

Note that in the general case, the call to this method should be inside a loop. If you retrieve information about
a property and then set that property, the new setting might make additional properties relevant, so you might
need to retrieve those and set them.

## Object: `ParameterMetaData`

This provides information about parameters in a PreparedStatement.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `getParameterCount()` |  |
| `getParameterType(int)` |  |
| `getParameterTypeName(int)` |  |
| `getPrecision(int)` |  |
| `getScale(int)` |  |
| `isNullable` |  |
| **Unsupported Methods** |  |
| `getParameterClassName(int)` |  |
| `getParameterMode()` |  |
| `isSigned` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

None.

## Object: `PreparedStatement`

The PreparedStatement interface describes methods that, for example, allow you to execute queries.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `addBatch()` | Snowflake-specific behavior (see below for details). |
| `clearParameters()` |  |
| `getParameterMetaData()` |  |
| `execute()` | Snowflake-specific behavior (see below for details). |
| `executeBatch(String)` |  |
| `executeLargeBatch(String)` |  |
| `executeLargeUpdate(String)` |  |
| `executeQuery()` | Snowflake-specific behavior (see below for details). |
| `executeUpdate()` | Snowflake-specific behavior (see below for details). |
| `setBigDecimal(int, BigDecimal)` |  |
| `setBoolean(int, boolean)` |  |
| `setByte(int, byte)` |  |
| `setBytes(int, byte[])` |  |
| `setDate(int, Date)` |  |
| `setDouble(int, double)` |  |
| `setFloat(int, float)` |  |
| `setInt(int, int)` |  |
| `setLong(int, long)` |  |
| `setNull(int, int)` |  |
| `setObject(int, Object, int, int)` | Snowflake-specific behavior (see below for details). |
| `setObject(int, Object, int)` | Snowflake-specific behavior (see below for details). |
| `setObject(int, Object)` |  |
| `setShort(int, short)` |  |
| `setString(int, String)` |  |
| `setTime(int, Time)` |  |
| `setTimestamp(int, Timestamp)` |  |
| **Unsupported Methods** |  |
| `setAsciiStream(int, InputStream, int)` |  |
| `setBinaryStream(int, InputStream, int)` |  |
| `setUnicodeStream(int, InputStream, int)` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

- `addBatch()`

  > Supported for INSERT statements only.
  >
  > The `addBatch` method (combined with `executeBatch`) allows multiple rows of data to be inserted as part of a single INSERT
  > statement.
  >
  > The difference between using a batch and not using a batch is similar to the difference between using a multi-row insert and a single-row
  > insert:
  >
  > Copy code
  >
  > ```
  > INSERT INTO t1 (c1, c2) VALUES (1, 'One');   -- single row inserted.
  >
  > INSERT INTO t1 (c1, c2) VALUES (1, 'One'),   -- multiple rows inserted.
  >                             (2, 'Two'),
  >                             (3, 'Three');
  > ```
  >
  > Inserting batches of rows is usually more efficient than inserting the same number of rows in individual `INSERT` statements. The
  > advantage is even greater when using AUTOCOMMIT (i.e. when each INSERT is an individual transaction).
  >
  > For an example of using `addBatch`, see [Batch inserts](/developer-guide/jdbc/jdbc-using#label-jdbc-batch-updates).
  >
  > Note
  >
  > There is an upper limit to the size of data that you can bind, or that you can combine in a batch. For details, see [Limits on Query Text Size](/user-guide/query-size-limits).
- `execute()`
  This method compiles and executes the SQL statement that was provided when the `PreparedStatement` object was created. The statement can be any
  type of SQL statement. The `execute()` method does not return a `ResultSet`.

  This method does not return anything. If you are executing a query and need to get a `ResultSet` back when the statement executes,
  then use the `executeQuery()` method.
- `executeQuery()`
  This method compiles and executes the SQL statement that was provided when the `PreparedStatement` object was created, and returns a `ResultSet`.
- `executeUpdate()`
  This method compiles and executes the SQL statement that was provided when the `PreparedStatement` object was created. The statement must be a DML
  statement (INSERT, UPDATE, DELETE, etc.) or a SQL statement that does not return anything (e.g. a DDL statement).

  The `executeUpdate()` method returns an integer, which is the number of rows updated if the statement was a DML statement. If the
  statement did not update any rows, the function returns `0`.

  If you need to execute a SQL statement that returns a ResultSet, then use a different method, such as executeQuery().
- `setObject()`

  When you bind a timestamp variable to a timestamp column, you can use this method to specify the timestamp variation
  ([TIMESTAMP\_LTZ , TIMESTAMP\_NTZ , TIMESTAMP\_TZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations)) that should be used to interpret the timestamp value. For details, see
  [Binding variables to timestamp columns](/developer-guide/jdbc/jdbc-using#label-jdbc-bind-timestamp-values).

## Interface: `SnowflakePreparedStatement`

The SnowflakePreparedStatement interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type PreparedStatement, for example by calling the
Connection.prepareStatement() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC PreparedStatement interface and the
SnowflakePreparedStatement interface. To access the SnowflakePreparedStatement methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

The methods below are in addition to the methods supported by the `PreparedStatement` interface.

| Method Name | Description |
| --- | --- |
| `executeAsyncQuery()` | Performs an asynchronous query. |
| `getQueryID()` | Returns the Snowflake query ID of the most recently executed query of this `SnowflakePreparedStatement`. |

Expand

Show lessSee more

executeAsyncQuery()
:   Purpose:
    :   This method performs an [asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), which involves submitting an SQL
        statement for execution, then returning control to the caller without waiting for the query to finish.

        Any SQL statement that is valid for `executeQuery()` is also valid for `executeAsyncQuery()`.

        Note

        File transfer statements, such as PUT and GET, are valid for `executeAsyncQuery()`, but behave synchronously.

    Arguments:
    :   None.

    Returns:
    :   An “empty” ResultSet. The user should poll the result set by calling
        `resultSet.unwrap(SnowflakeResultSet.class).getStatus()` until the query results become available.

    Throws:
    :   This method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the PreparedStatement object.

    Examples:
    :   Copy code

        ```
        ...
        PreparedStatement prepStatement = connection.prepareStatement("insert into testTable values (?)");
        prepStatement.setInt(1, 33);
        ResultSet rs = prepStatement.executeAsyncQuery();
        ...
        ```

        See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for a more extensive example using the very similar
        `SnowflakeStatement.executeAsyncQuery()` method.

getQueryID()
:   Purpose:
    :   This method returns the Snowflake query ID of the most recently executed query of this `SnowflakePreparedStatement`. If no query has been
        executed yet with this prepared statement, the method returns null.

    Arguments:
    :   None.

    Returns:
    :   The method returns the ID as a String that contains a UUID.

    Throws:
    :   The method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the
        `SnowflakePreparedStatement`.

        For [asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), the query ID does not become available until the
        execution of the statement completes. If you call `SnowflakePreparedStatement.getQueryID()` after calling
        `executeAsyncQuery()` but before the statement finishes executing, the return value could be NULL.
        Instead, call `resultSet.unwrap(SnowflakeResultSet.class).getQueryID()` on the `ResultSet` object
        returned by `executeAsyncQuery()`.

    Examples:
    :   This partial example shows how to call the method:

        Copy code

        ```
        ---------
            // Retrieve the query ID from the PreparedStatement.
            String queryID;
            queryID = preparedStatement.unwrap(SnowflakePreparedStatement.class).getQueryID();
            // -- <) -----------------------
        ```

## Enum: `QueryStatus`

The enum type is a Snowflake-specific type that:

- Defines the constants that represent the status of [an asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query).
- Defines methods that return details about any errors that occurred when executing SQL statements.

This enum type is in the `net.snowflake.client.core` package.

### Enum constants

Each enum constant represents a different possible status for the asynchronous query.

| Enum Constant | Description |
| --- | --- |
| RUNNING | The query is still running. |
| ABORTING | The query is in the process of being aborted on the server side. |
| SUCCESS | The query finished successfully. |
| FAILED\_WITH\_ERROR | The query finished unsuccessfully. |
| QUEUED | The query is queued for execution (i.e. has not yet started running), typically because it is waiting for resources. |
| DISCONNECTED | The session’s connection is broken. The query’s state will change to “FAILED\_WITH\_ERROR” soon. |
| RESUMING\_WAREHOUSE | The warehouse is starting up and the query is not yet running. |
| BLOCKED | The statement is waiting on a lock held by another statement. |
| NO\_DATA | Data about the statement is not yet available, typically because the statement has not yet started executing. |

Expand

Show lessSee more

### Methods

The enum type defines the following methods, which you can use to get details about an error when the query status is
`FAILED_WITH_ERROR`.

| Method Name | Description |
| --- | --- |
| `getErrorCode()` | Returns the error code from the server if an error occurred during query execution. |
| `getErrorMessage()` | Returns the error message from the server if an error occurred during query execution. |

Expand

Show lessSee more

getErrorCode()
:   Purpose:
    :   If an error occurred during the execution of the query, this method returns the error code from the server.

    Arguments:
    :   None.

    Returns:
    :   The method returns the error code as an `int`. If no error occurred, the method returns the value `0`.

    Examples:
    :   Copy code

        ```
        QueryStatus queryStatus = resultSet.unwrap(SnowflakeResultSet.class).getStatus();
        if (queryStatus == queryStatus.FAILED_WITH_ERROR) {
          // Print the error code to stdout
          System.out.format("Error code: %d%n", queryStatus.getErrorCode());
        }
        ```

        See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for a more extensive example that includes a call to this
        method.

getErrorMessage()
:   Purpose:
    :   If an error occurred during the execution of the query, this method returns the error message from the server.

    Arguments:
    :   None.

    Returns:
    :   The method returns the error message as a `String`. If no error occurred, the method returns the value
        `No error reported`.

    Examples:
    :   Copy code

        ```
        QueryStatus queryStatus = resultSet.unwrap(SnowflakeResultSet.class).getStatus();
        if (queryStatus == queryStatus.FAILED_WITH_ERROR) {
          // Print the error message to stdout
          System.out.format("Error message: %s%n", queryStatus.getErrorMessage());
        }
        ```

        See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for a more extensive example that includes a call to this
        method.

## Object: `ResultSet`

The ResultSet interface documents methods that retrieve the results of queries, for example to read the rows and
columns returned by a SELECT statement.

A Snowflake ResultSet is a read-only object; it is not updatable.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `close()` | Snowflake-specific behavior (see below for details). |
| `findColumn(String)` |  |
| `getBigDecimal(int, int)` |  |
| `getBigDecimal(String, int)` |  |
| `getBoolean(int)` |  |
| `getBoolean(String)` |  |
| `getByte(int)` |  |
| `getByte(String)` |  |
| `getBytes(int)` |  |
| `getBytes(String)` |  |
| `getDate(int)` | Snowflake-specific behavior (see below for details). |
| `getDate(int, Calendar)` | Snowflake-specific behavior (see below for details). |
| `getDate(String)` | Snowflake-specific behavior (see below for details). |
| `getDate(String, Calendar)` | Snowflake-specific behavior (see below for details). |
| `getDouble(int)` |  |
| `getDouble(String)` |  |
| `getFloat(int)` |  |
| `getFloat(String)` |  |
| `getInt(int)` |  |
| `getInt(String)` |  |
| `getLong(int)` |  |
| `getLong(String)` |  |
| `getMetaData()` | Snowflake-specific behavior (see below for details). |
| `getObject(int)` |  |
| `getObject(String)` |  |
| `getShort(int)` |  |
| `getShort(String)` |  |
| `getString(int)` |  |
| `getString(String)` |  |
| `getTime(int)` | Snowflake-specific behavior (see below for details). |
| `getTime(String)` | Snowflake-specific behavior (see below for details). |
| `getTimestamp(int)` | Snowflake-specific behavior (see below for details). |
| `getTimestamp(String)` | Snowflake-specific behavior (see below for details). |
| `next()` | Snowflake-specific behavior (see below for details). |
| `wasNull()` |  |
| **Unsupported Methods** |  |
| `clearWarnings()` |  |
| `getArray(int)` |  |
| `getArray(String)` |  |
| `getAsciiStream(int)` |  |
| `getAsciiStream(String)` |  |
| `getBinaryStream(int)` |  |
| `getBinaryStream(String)` |  |
| `getCursorName()` |  |
| `getUnicodeStream(int)` |  |
| `getUnicodeStream(String)` |  |
| `getWarnings()` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

- `close()`
  Closes the object. After an object has been closed, calling almost any method of the closed object will raise a `SQLException`. Calling
  `close` on an already closed object is harmless and will not raise an exception.
- `getDate()`, `getTime()`, `getTimestamp()`
  In version 3.12.17 and later versions of the JDBC Driver, these methods use the session time zone (specified by the
  [TIMEZONE](/sql-reference/parameters#label-timezone) parameter). Older versions use the time zone of the JVM.

  To change these methods to use the time zone of the JVM, set the [JDBC\_USE\_SESSION\_TIMEZONE](/sql-reference/parameters#label-jdbc-use-session-timezone) parameter to
  `FALSE`.
- `getMetaData()`
  If the ResultSet object is for [an asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), then this method will block
  until the query has finished executing. You can use `resultSet.unwrap(SnowflakeResultSet.class).getStatus()` to get
  the query status before calling this method.
- `next()`
  This makes the next row in the result set the “current” row. Calls to the `get*()` methods, such as `getInt()`,
  get values from the current row.

  If the `ResultSet` has been closed by a call to the `close` method, then subsequent calls to `next` return false, rather than raise an exception.

  If the ResultSet object is for [an asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), then this method will block
  until the results are available. You can use `resultSet.unwrap(SnowflakeResultSet.class).getStatus()` to get the
  query status before calling this
  method.

## Interface: `SnowflakeResultSet`

The SnowflakeResultSet interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type ResultSet, for example by calling the
Statement.getResultSet() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC ResultSet interface and the
SnowflakeResultSet interface. To access the SnowflakeResultSet methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

| Method Name | Description |
| --- | --- |
| `getQueryID()` | Returns the Snowflake query ID of the statement that generated this result set. |
| `getStatus()` | For a ResultSet returned by an asynchronous query, returns the status of the query. |

Expand

Show lessSee more

getQueryID()
:   Purpose:
    :   This method returns the Snowflake query ID of the statement that generated this result set.

    Arguments:
    :   None.

    Returns:
    :   The method returns the ID as a String that contains a UUID.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the
        `ResultSet`.

    Examples:
    :   Copy code

        ```
        -------------------
            String queryID2;
            queryID2 = resultSet.unwrap(SnowflakeResultSet.class).getQueryID();
            // -- <) -----------------------
        ```

getStatus()
:   Purpose:
    :   For a ResultSet returned by an asynchronous query, such as `SnowflakeStatement.executeAsyncQuery()`,
        this method returns the status of the query. The status indicates whether the query finished successfully,
        finished unsuccessfully, or has not yet finished.

    Arguments:
    :   None.

    Returns:
    :   A [QueryStatus enum constant](#label-jdbc-querystatus).

    Throws:
    :   This method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the ResultSet object.

    Examples:
    :   Copy code

        ```
        QueryStatus queryStatus = resultSet.unwrap(SnowflakeResultSet.class).getStatus();
        ```

        See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for a more extensive example that includes a call to this
        method.

## Object: `ResultSetMetaData`

This provides information about a ResultSet, for example, the number of columns in the ResultSet.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `getCatalogName(int)` | Snowflake-specific behavior (see below for details). |
| `getColumnCount()` |  |
| `getColumnDisplaySize(int)` |  |
| `getColumnLabel(int)` |  |
| `getColumnName(int)` |  |
| `getColumnType(int)` |  |
| `getColumnTypeName(int)` | Snowflake-specific behavior (see below for details). |
| `getPrecision(int)` |  |
| `getScale(int)` |  |
| `getSchemaName(int)` | Snowflake-specific behavior (see below for details). |
| `getTableName(int)` | Snowflake-specific behavior (see below for details). |
| `isAutoIncrement(int)` |  |
| `isCaseSensitive(int)` |  |
| `isCurrency(int)` |  |
| `isDefinitelyWritable(int)` |  |
| `isNullable(int)` |  |
| `isReadOnly(int)` |  |
| `isSearchable(int)` |  |
| `isSigned(int)` |  |
| `isWritable(int)` |  |
| **Unsupported Methods** |  |
| None. |  |

Expand

Show lessSee more

### Snowflake-specific behavior

- The `ResultSetMetaData` class does not have a `close()` method. An open `ResultSetMetaData` object is implicitly closed when the user closes
  the `ResultSet` from which the `ResultSetMetaData` object was created.
- `getCatalogName()`, `getSchemaName()`, `getTableName()`

  If the ResultSet object is for [an asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), these methods return empty
  strings.
- For [GEOGRAPHY](/sql-reference/data-types-geospatial) columns, `getColumnTypeName` returns `GEOGRAPHY`.

  Note that the `getColumnType` and `getColumnClassName` methods do not indicate that the column type is
  `GEOGRAPHY`.

## Interface: `SnowflakeResultSetMetaData`

The SnowflakeResultSetMetaData interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type ResultSetMetaData, for example by calling the
ResultSet.getMetaData() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC ResultSetMetaData interface and the
SnowflakeResultSetMetaData interface. To access the SnowflakeResultSetMetaData methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `getColumnIndex(String columnName)` |  |
| `getColumnNames()` |  |
| `getInternalColumnType(int column)` |  |
| `getQueryID()` |  |

Expand

Show lessSee more

getColumnIndex(String columnName):
:   Purpose:
    :   Returns the index of the column that corresponds to the columnName. For example, if a column named “BirthDate”
        is the third column in the table, then getColumnIndex(“BirthDate”) returns 2. (Indexes are 0-based, not 1-based.)

    Arguments:
    :   The name of the column for which you want to find the index.

    Returns:
    :   Returns an integer that contains the index of the column that corresponds to the columnName.
        If the columnName does not match any column in the result set, this returns -1.

    Throws:
    :   The method can throw `SQLException`.

getColumnNames():
:   Purpose:
    :   This function returns the list of all column names in the resultset.

        This is different from the function getColumnName(int column) in ResultSetMetaData, which returns a single
        column name based on an index.

    Arguments:
    :   None.

    Returns:
    :   The data type of the returned value is “List<String>”. The list contains the names of the columns. The names
        are in the same order as the column indexes.

    Throws:
    :   The method can throw `SQLException`.

getInternalColumnType(int column):
:   Purpose:
    :   Returns the data type of the specified column.

    Arguments:
    :   column: This indicates the index (1-based) of the column for which you want the data type.

    Returns:
    :   Returns the data type of the specified column. The data type is an integer.

getQueryID()
:   Purpose:
    :   Returns the Snowflake query ID of the query to which this metadata applies.

    Arguments:
    :   None.

    Returns:
    :   This method returns the query ID of the query for which this metadata was generated.
        The query ID is a String that contains a UUID. Information about UUIDs is included in the description of the
        SQL function [UUID\_STRING](/sql-reference/functions/uuid_string).

    Throws:
    :   The method can throw `SQLException`.

## Object: `SnowflakeTimestampWithTimezone`

A `SnowflakeTimestampWithTimezone` object provides information
about the time zone associated with the Java `Timestamp` object’s time stamp.
You can use this object to extract the time zone directly instead of parsing
the information from the Java `Timestamp` string. To access this functionality, you must import the
following Java libraries:

- `java.sql.Timestamp;`
- `java.time.ZonedDateTime;`
- `java.util.TimeZone;`

### Methods

| Method Name | Notes |
| --- | --- |
| **Constructors** |  |
| Copy code  ``` SnowflakeTimestampWithTimezone(     long seconds,     int nanoseconds,     TimeZone tz) ``` | - Number of seconds since January 1, 1970 (Internet time). - Number of fractional nanoseconds. - ID of the time zone. |
| Copy code  ``` SnowflakeTimestampWithTimezone(     Timestamp ts,     TimeZone tz) ``` | - `Timestamp` object representing the desired time. - ID of the time zone. |
| Copy code  ``` SnowflakeTimestampWithTimezone(     Timestamp ts) ``` | - `Timestamp` object representing the desired time. |
| **Supported Methods** |  |
| `getTimezone()` | Snowflake-specific behavior (see below for details). |
| `toZonedDateTime()` | Snowflake-specific behavior (see below for details). |

Expand

Show lessSee more

### Snowflake-specific behavior

- `getTimezone()`

  Returns the time zone from the time stamp.

  Copy code

  ```
  import java.sql.Timestamp;
  import java.time.ZonedDateTime;
  import java.util.TimeZone;

  public void testGetTimezone() {
   String timezone = "Australia/Sydney";

   // Create a timestamp from a point in time
   Long datetime = System.currentTimeMillis();
   Timestamp currentTimestamp = new Timestamp(datetime);
   SnowflakeTimestampWithTimezone ts =
       new SnowflakeTimestampWithTimezone(currentTimestamp, TimeZone.getTimeZone(timezone));

   // Verify timezone was set
   assertEquals(ts.getTimezone().getID(), timezone);
  }
  ```
- `toZonedDateTime()`

  Converts a `SnowflakeTimestampWithTimezone` time stamp to a zoned date time (Java `ZonedDateTime` object).

  Copy code

  ```
  import java.sql.Timestamp;
  import java.time.ZonedDateTime;
  import java.util.TimeZone;

  public void testToZonedDateTime() {
   String timezone = "Australia/Sydney";
   String zonedDateTime = "2022-03-17T10:10:08+11:00[Australia/Sydney]";

   // Create a timestamp from a point in time
   Long datetime = 1647472208000L;
   Timestamp timestamp = new Timestamp(datetime);
   SnowflakeTimestampWithTimezone ts =
       new SnowflakeTimestampWithTimezone(timestamp, TimeZone.getTimeZone(timezone));
   ZonedDateTime zd = ts.toZonedDateTime();

   // Verify timestamp was converted to zoned datetime
   assertEquals(zd.toString(), zonedDateTime);
  }
  ```

## Object: `Statement`

A `Statement` object represents a SQL statement. The statement object allows users to perform tasks such as:

- Execute a SQL statement.
- Set a timeout for the execution of the statement.
- Retrieve a result set for a query.

### Methods

| Method Name | Notes |
| --- | --- |
| **Supported Methods** |  |
| `cancel()` |  |
| `close()` | Snowflake-specific behavior (see below for details). |
| `execute(String)` |  |
| `executeBatch(String)` |  |
| `executeLargeBatch(String)` |  |
| `executeLargeUpdate(String)` |  |
| `executeQuery(String)` |  |
| `executeUpdate(String)` |  |
| `getBatchQueryID()` | Snowflake-specific behavior (see below for details). |
| `getMaxFieldSize()` |  |
| `getMaxRows()` |  |
| `getMoreResults()` |  |
| `getQueryTimeout()` |  |
| `getResultSet()` |  |
| `getUpdateCount()` | Snowflake-specific behavior (see below for details). |
| `setCursorName(String)` |  |
| `setMaxRows(int)` |  |
| `setQueryTimeout(int)` |  |
| **Unsupported Methods** |  |
| `clearWarnings()` |  |
| `getWarnings()` |  |
| `setEscapeProcessing(boolean)` |  |
| `setMaxFieldSize(int)` |  |

Expand

Show lessSee more

### Snowflake-specific behavior

- `close()`
  This method closes the object. After an object has been closed, calling almost any method of the closed object will raise a
  `SQLException`. Calling `close` on an already closed object is harmless and will not raise an exception.
- `getBatchQueryID()`

  > This method returns a list of the Snowflake query IDs of the most recently executed query batch of this `Statement`. If no
  > query has been executed yet with the statement, the method returns null.
  >
  > This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the
  > statement. For example:
  >
  > > Copy code
  > >
  > > ```
  > > ---------------
  > >  connection.setAutoCommit(false);
  > >  statement.addBatch("SELECT 1;");
  > >  statement.addBatch("SELECT 2;");
  > >  statement.executeBatch();
  > >  connection.commit();
  > >  connection.setAutoCommit(true);
  > >  List<String> batchQueryIDs1;
  > >  // Since getQueryID is not standard JDBC API, we must call unwrap() to
  > >  // use these Snowflake methods.
  > >  batchQueryIDs1 = statement.unwrap(SnowflakeStatement.class).getBatchQueryIDs();
  > >  int num_query_ids = batchQueryIDs1.size();
  > >  if (num_query_ids != 2) {
  > >    System.out.println("ERROR: wrong number of query IDs in batch 1.");
  > >  }
  > >  // Check that each query ID is plausible.
  > >  for (int i = 0; i < num_query_ids; i++) {
  > >    String qid = batchQueryIDs1.get(i);
  > >    if (!is_plausible_query_id(qid)) {
  > >      msg = "SEVERE WARNING: suspicious query ID in batch";
  > >      System.out.println("msg");
  > >      System.out.println(qid);
  > >    }
  > >  }
  > >  // -- <) -----------------------
  > > ```
- `getUpdateCount()`
  This method returns the number of rows updated by the most recently executed SQL statement.

  - If the statement was a DML statement (INSERT, UPDATE, DELETE, etc.), then `getUpdateCount()` returns the number of rows that
    were added, deleted, or changed. Note that this value can be `0` if no rows were changed.
  - If the statement was a SELECT statement, then `getUpdateCount()` returns `-1`.
  - If the statement was a DDL statement, then `getUpdateCount()` returns `-1`.

## Interface: `SnowflakeStatement`

The SnowflakeStatement interface contains Snowflake-specific methods. When you use the
Snowflake JDBC driver to create an object of type Statement, for example by calling the
Connection.createStatement() method, you actually get an object of a different (hidden)
Snowflake-specific type, which implements both the JDBC Statement interface and the
SnowflakeStatement interface. To access the SnowflakeStatement methods in that object,
you [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the object.

### Additional methods

| Method Name | Description |
| --- | --- |
| `executeAsyncQuery()` | Performs an asynchronous query. |
| `getQueryID()` | Returns the Snowflake query ID of the most recently executed query of this `Statement`. |
| `setParameter(String, Value)` | Sets Snowflake-specific parameters. |

Expand

Show lessSee more

executeAsyncQuery(String)
:   Purpose:
    :   This method performs an [asynchronous query](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), which involves submitting an SQL
        statement for execution, then returning control to the caller without waiting for the query to finish.

    Arguments:
    :   A string containing the SQL command to execute. Any SQL statement that is valid for `executeQuery()` is
        also valid for `executeAsyncQuery()`.

        Note

        File transfer statements, such as PUT and GET, are valid for `executeAsyncQuery()`, but behave synchronously.

    Returns:
    :   An “empty” ResultSet. The user should poll the result set by calling
        `resultSet.unwrap(SnowflakeResultSet.class).getStatus()` until the query results become available.

    Throws:
    :   The method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the Statement object.

    Examples:
    :   See [Examples of asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query-examples) for an example that includes a call to this method.

getQueryID()
:   Purpose:
    :   This method returns the Snowflake query ID of the most recently executed query of this `Statement`.

    Arguments:
    :   None.

    Returns:
    :   The query ID of the most recently executed query of this statement.
        The query ID is a String that contains a UUID.
        If no query has been executed yet with the statement, the method returns null.

    Throws:
    :   The method can throw `SQLException`.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the Statement.

        For [asynchronous queries](/developer-guide/jdbc/jdbc-using#label-jdbc-asynchronous-query), the query ID does not become available until the
        execution of the statement completes. If you call `SnowflakeStatement.getQueryID()` after calling
        `executeAsyncQuery()` but before the statement finishes executing, the return value could be NULL.
        Instead, call `resultSet.unwrap(SnowflakeResultSet.class).getQueryID()` on the `ResultSet` object
        returned by `executeAsyncQuery()`.

    Examples:
    :   Copy code

        ```
        -------------------
            String queryID1;
            queryID1 = statement.unwrap(SnowflakeStatement.class).getQueryID();
            // -- <) -----------------------
        ```

setParameter(String parameter\_name, <type> <value>)
:   Purpose:
    :   The `SnowflakeStatement` class provides the `setParameter` method as a Snowflake extension. This allows
        the caller to set Snowflake-specific JDBC parameters.

        The method is overloaded. Different JDBC parameters require different data types. A method exists for each
        valid data type that can be passed as the second argument to the function.

    Arguments:
    :   parameter\_name:
        :   This string must contain the name of a pre-defined Snowflake JDBC parameter. The pre-defined
            JDBC parameters (and their valid values or ranges) are listed below:

            | JDBC Parameter | Notes |
            | --- | --- |
            | MULTI\_STATEMENT\_COUNT | Integer specifying the number of statements (`0` = unlimited number of statements; `1` or higher indicates the exact number of statements that should be executed). |

            Expand

            Show lessSee more

        value:
        :   This is the value to assign to the specified JDBC parameter. Make sure that the data type is compatible
            with the JDBC parameter you specified.

    Returns:
    :   Nothing.

    Throws:
    :   This function can throw SQLException.

    Notes:
    :   This method is a Snowflake extension to the JDBC standard. To use this method, you must [unwrap](/developer-guide/jdbc/jdbc-using#label-jdbc-unwrapping) the Statement.

    Examples:
    :   Copy code

        ```
        Statement statement1;
        ...
        // Tell Statement to expect to execute 2 statements:
        statement1.unwrap(SnowflakeStatement.class).setParameter(
                "MULTI_STATEMENT_COUNT", 2);
        ```

## Interface: `SQLException`

SQLException objects are thrown by JDBC driver methods when an error occurs, and contain information about that error.

| Method Name | Description |
| --- | --- |
| `getErrorCode()` | Returns a Snowflake-specific error code. |
| `getMessage()` | This returns a string that describes the error. |
| `getSQLState()` | Returns the SQLState. |

Expand

Show lessSee more

getErrorCode()
:   Purpose:
    :   This method returns a custom Snowflake error code.

    Arguments:
    :   None.

    Returns:
    :   A Snowflake-specific error code.

    Notes:
    :   See also the `getSQLState()` method.

getMessage()
:   Purpose:
    :   This method returns a string that describes the error.

    Arguments:
    :   None.

    Returns:
    :   A Snowflake-specific error message.

getSQLState()
:   Purpose:
    :   This method returns a string that contains a 5-character alphanumeric value based on the error.

    Arguments:
    :   None.

    Returns:
    :   A Snowflake-specific SQLState. An SQLState is a 5-character alphanumeric string that indicates the
        specific error that occurred.
