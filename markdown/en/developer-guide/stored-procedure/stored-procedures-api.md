# JavaScript stored procedures API

This topic covers the JavaScript API for Snowflake stored procedures.
The API consists of JavaScript objects and the methods in those objects.

## Object: `snowflake`

The `snowflake` object is accessible by default to the JavaScript code in a stored procedure; you do not need to create the object.
This object contains the methods in the stored procedure API. For example:

> Copy code
>
> ```
> CREATE PROCEDURE stproc1()
>   RETURNS STRING NOT NULL
>   LANGUAGE JAVASCRIPT
>   AS
>   -- "$$" is the delimiter for the beginning and end of the stored procedure.
>   $$
>   // The "snowflake" object is provided automatically in each stored procedure.
>   var statement = snowflake.createStatement(...);
>   ...
>   $$
>   ;
> ```

More extensive code examples are provided in [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

### Constants

None.

### Methods

addEvent(name [, attributes ] )
:   Adds an event for tracing.

    For more information about trace events with JavaScript, refer to [Emitting trace events in JavaScript](/developer-guide/logging-tracing/tracing-javascript)

    Parameters:
    :   `name`

        > The name of the event to add.

        `attributes`

        > An object specifying attributes to associate with the event.

    Errors:
    :   Throws a JavaScript Error if:

        - `name` is not a string.
        - There are zero or more than two arguments.

    Examples:
    :   Add a `my_event` event with `score` and `pass` attributes.

        Copy code

        ```
        snowflake.addEvent('my_event', {'score': 89, 'pass': true});
        ```

createStatement(sql\_command\_object)
:   Creates a `Statement` object representing the statement specified by `sql_command_object`. You can use the
    `Statement.execute()` method to execute the statement.

    Parameter(s):
    :   `sql_command_object`

        > A JSON object (dictionary) that contains the text of the SQL statement to execute and values to bind to that statement.
        > Properties of the *sql\_command\_object* JSON object include:
        >
        > - `sqlText`: A string containing the SQL statement to execute.
        > - `binds`: An array of values to bind to placeholders in the SQL statement specified by `sqlText`.

    Returns:
    :   A `Statement` object.

    Errors:
    :   Throws a JavaScript Error if:

        - `sqlText` is missing or contains an empty query text.
        - The statement tries to bind an argument whose data type is not supported. For information about data type
          mapping, see [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
          For more information about binding, see [Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

    Examples:
    :   The following example does not bind any values:

        Copy code

        ```
        var stmt = snowflake.createStatement(
          {sqlText: "INSERT INTO table1 (col1) VALUES (1);"}
        );
        ```

        The following example binds values. Values in the `binds` property array are bound to `?` placeholders in the SQL text
        in the order they appear in the array.

        Copy code

        ```
        var stmt = snowflake.createStatement(
          {
          sqlText: "INSERT INTO table2 (col1, col2) VALUES (?, ?);",
          binds:["LiteralValue1", variable2]
          }
        );
        ```

        For more information about binding, including additional examples,
        see [Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

execute(sql\_command\_object)
:   Executes the SQL statement specified as the argument.

    `snowflake.execute` differs from `Statement.execute`, which you use to execute the statement represented by the
    `Statement` object, rather than executing the method’s argument.

    Parameters:
    :   `sql_command_object`

        > A JSON object (dictionary) that contains the text of the SQL statement to execute and values to bind to that statement.
        > Properties of the *sql\_command\_object* JSON object include:
        >
        > - `sqlText`: A string containing the SQL statement to execute.
        > - `binds`: An array of values to bind to placeholders in the SQL statement specified by `sqlText`.

    Returns:
    :   A result set in the form of a `ResultSet` object.

    Errors:
    :   Throws a JavaScript Error if:

        - An error, such as a compile error, occurred while executing the query.
        - `sqlText` is missing or contains an empty query text.
        - The statement tries to bind an argument whose data type is not supported. For information about data type
          mapping, see [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
          For more information about binding, including additional examples,
          see [Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

log(level, message[, attributes])
:   Logs a message at the specified severity level, optionally with attributes.

    For more information, see [Logging messages in JavaScript](/developer-guide/logging-tracing/logging-javascript).

    Parameters:
    :   `level`

        > The severity level at which to log the message. You can specify one of the following strings:
        >
        > - `'off'`
        > - `'trace'`
        > - `'debug'`
        > - `'info'`
        > - `'warn'`
        > - `'error'`
        > - `'fatal'`

        `message`

        > The message to log.

        `attributes`

        > Optional. A JSON object with key-value pairs.

    Errors:
    :   Throws a JavaScript error if:

        - `level` is not a string.
        - `level` is not one of the supported `level` values listed above.

    Examples:
    :   Copy code

        ```
        snowflake.log("error", "Error message", {"custom1": "value1", "custom2": "value2"});
        ```

setSpanAttribute(key, value)
:   Sets an attribute for the current span when tracing events.

    For more information about trace events with JavaScript, refer to [Emitting trace events in JavaScript](/developer-guide/logging-tracing/tracing-javascript)

    Parameters:
    :   `key`

        > The attribute’s key.

        `value`

        > The attribute’s value.

    Errors:
    :   Throws a JavaScript error if:

        - Two arguments aren’t specified.
        - `key` is not a string.

    Examples:
    :   Set an attribute whose key is `example.boolean` and whose value is `true`.

        Copy code

        ```
        snowflake.setSpanAttribute("example.boolean", true);
        ```

## Object: `Statement`

A stored procedure `Statement` object provides the methods for executing a query statement and accessing
metadata (such as column data types) about the statement.

At the time the Statement object is created, the SQL is parsed, and a prepared statement is created.

### Constants

None.

### Methods

execute()
:   This method executes the prepared statement stored in this `Statement` object.

    `Statement.execute` differs from `snowflake.execute`, which you use to execute the method’s argument, rather than
    a statement represented by the `Statement` object.

    Parameters:
    :   None because the method uses information that is already stored in the `Statement` object.

    Returns:
    :   A result set in the form of a `ResultSet` object.

    Errors:
    :   Throws a JavaScript Error if the query fails.

    Examples:
    :   See [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

getColumnCount()
:   This method returns the number of columns in the result set for an executed query. If the query has not yet been executed, this method throws an Error.

    Parameters:
    :   None.

    Returns:
    :   The number of columns.

    Errors:
    :   Throw a JavaScript Error if the statement has not yet been executed (and thus the number of returned columns cannot necessarily
        be determined).

    Examples:
    :   Copy code

        ```
        var column_count = statement.getColumnCount();
        ```

getColumnName(colIdx)
:   This method returns the name of the specified column.

    Parameters:
    :   The index number of the column (starting from `1`, not `0`).

    Returns:
    :   The name of the column.

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified index exists.

getColumnScale(colIdx)
:   This method returns the scale of the specified column. The scale is the number of digits after the decimal point. The scale of the column was specified
    in the CREATE TABLE or ALTER TABLE statement. For example:

    > Copy code
    >
    > ```
    > CREATE TABLE scale_example  (
    >     n10_4 NUMERIC(10, 4)    // Precision is 10, Scale is 4.
    >     );
    > ```

    Although this method can be called for any data type, it is intended for use with numeric data types.

    Parameters:
    :   The index of the column for which you want the scale (starting from `1`, not `0`).

    Returns:
    :   The scale of the column (for numeric columns); `0` for non-numeric (columns).

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified index exists.

    Examples:
    :   See [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage) (search for `getColumnScale()`).

getColumnSqlType(colIdx|colName)
:   This method returns the SQL data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The SQL data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified name or index exists.

getColumnType(colIdx|colName)
:   This method returns the JavaScript data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The JavaScript data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified index or name exists.

getNumDuplicateRowsUpdated()
:   This method returns the number of “duplicate” rows (often called *multi-joined rows*) updated by this Statement.
    (For information about how multi-joined rows are formed, see the
    [Usage Notes and Examples for the UPDATE statement](/sql-reference/sql/update#label-update-statement-usage-notes).)

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of multi-joined rows updated.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsAffected()
:   This method returns the number of rows affected (e.g. inserted/updated/deleted) by this Statement.

    If more than one type of change applies (e.g. a [MERGE](/sql-reference/sql/merge) operation inserted some rows and
    updated others), then the number is the total number of rows affected by all of the changes.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows affected.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsDeleted()
:   This method returns the number of rows deleted by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows deleted.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsInserted()
:   This method returns the number of rows inserted by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows inserted.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsUpdated()
:   This method returns the number of rows updated by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows updated.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getRowCount()
:   This method returns the number of rows in the result set for an executed query. If the query has not yet been executed, this method throws an Error.

    Parameters:
    :   None.

    Returns:
    :   The number of rows.

    Errors:
    :   Throw a JavaScript Error if the statement has not yet been executed (and thus the number of returned rows cannot be determined).

    Examples:
    :   Copy code

        ```
        var row_count = statement.getRowCount();
        ```

getQueryId()
:   This method returns the UUID of the most recent query executed.

    Parameters:
    :   None.

    Returns:
    :   A string containing a UUID, which is the query ID.

    Errors:
    :   If no query has been executed yet by this statement, the method throws the error
        “Statement is not executed yet.”

    Examples:
    :   Copy code

        ```
        var queryId = statement.getQueryId();
        ```

getSqlText()
:   This method returns the text of the prepared query in the `Statement` object.

    Parameters:
    :   None.

    Returns:
    :   A string of the prepared query text.

    Errors:
    :   None.

    Examples:
    :   Copy code

        ```
        var queryText = statement.getSqlText();
        ```

isColumnNullable(colIdx)
:   This method returns whether the specified column allows SQL NULL values.

    Parameters:
    :   The index of the column (starting from `1`, not `0`).

    Returns:
    :   `true` if the column allows SQL NULL values; otherwise, `false`.

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified index exists.

isColumnText(colIdx)
:   This method returns true if the column data type is one of the following SQL text data types:

    - CHAR or CHAR(N), as well as their synonyms CHARACTER and CHARACTER(N)
    - VARCHAR or VARCHAR(N)
    - STRING
    - TEXT

    Otherwise, it returns false.

    Parameters:
    :   The index of the column (starting from `1`, not `0`).

    Returns:
    :   `true` if the column data type is one of the SQL text data types; `false` for all other data types.

    Errors:
    :   Throws a JavaScript Error if:

        - The `Statement` has not yet been executed.
        - No column with the specified index exists.

    Note

    The API provides several methods for determining the data type of a column. The first method is described in detail above. The remaining methods have
    the same parameters and errors; the only difference is the return value.

isColumnArray(colIdx)
:   Returns:
    :   `true` if the column data type is ARRAY (for semi-structured data); `false` for all other data types.

isColumnBinary(colIdx)
:   Returns:
    :   `true` if the column data type is BINARY or VARBINARY; `false` for all other data types.

isColumnBoolean(colIdx)
:   Returns:
    :   `true` if the column data type is BOOLEAN; `false` for all other data types.

isColumnDate(colIdx)
:   Returns:
    :   `true` if the column data type is DATE; `false` for all other data types.

isColumnNumber(colIdx)
:   Returns:
    :   `true` if the column data type is one of the SQL numeric types (NUMBER, NUMERIC, DECIMAL, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT,
        FLOAT, FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, or REAL); `false` for all other data types.

isColumnObject(colIdx)
:   Returns:
    :   `true` if the column data type is OBJECT (for semi-structured data); `false` for all other data types.

isColumnTime(colIdx)
:   Returns:
    :   `true` if the column data type is TIME or DATETIME; `false` for all other data types.

isColumnTimestamp(colIdx)
:   Returns:
    :   `true` if the column data type is one of the SQL timestamp types (TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ); `false`
        for all other data types, including other date and time data types (DATE, TIME, or DATETIME).

isColumnVariant(colIdx)
:   Returns:
    :   `true` if the column data type is VARIANT (for semi-structured data); `false` for all other data types.

## Object: `ResultSet`

This object contains the results returned by a query. The results are treated as a set of zero or more rows, each of which contains one or more columns. The term
“set” is not used here in the mathematical sense. In mathematics, a set is unordered, whereas a `ResultSet` has an order.

A `ResultSet` is similar in some ways to the concept of a SQL cursor. For example, you can see one row at a time in a `ResultSet`, just as you can see
one row at a time in a cursor.

Typically, after you retrieve a `ResultSet`, you iterate through it by repeating the following operations:

- Call `next()` to get the next row.
- Retrieve data from the current row by calling methods such as `getColumnValue()`.

If you do not know enough about the data in the `ResultSet` (e.g. you do not know the data type of each column), then you can call other methods that provide information about
the data.

Some of the methods of the `ResultSet` object are similar to the methods of the `Statement` object. For example, both objects have a
`getColumnSqlType(colIdx)` method.

### Constants

None.

### Methods

getColumnCount()
:   This method returns the number of columns in this ResultSet.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of columns.

    Errors:
    :   None.

getColumnSqlType(colIdx|colName)
:   This method returns the SQL data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The SQL data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        - `ResultSet` is empty or `next()` has not yet been called.
        - No column with the specified index or name exists.

getColumnValue(colIdx|colName)
:   This method returns the value of a column in the current row (i.e. the row most recently retrieved by `next()`).

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The value of the specified column.

    Errors:
    :   Throws a JavaScript Error if:

        - `ResultSet` is empty or `next()` has not yet been called.
        - No column with the specified index or name exists.

    Examples:
    :   Convert a row in the database into a JavaScript array:

        > Copy code
        >
        > ```
        > var valueArray = [];
        > // For each row...
        > while (myResultSet.next())  {
        >     // Append each column of the current row...
        >     valueArray.push(myResultSet.getColumnValue('MY_COLUMN_NAME1'));
        >     valueArray.push(myResultSet.getColumnValue('MY_COLUMN_NAME2'));
        >     ...
        >     // Do something with the row of data that we retrieved.
        >     f(valueArray);
        >     // Reset the array before getting the next row.
        >     valueArray = [];
        >     }
        > ```

        Also, a column’s value can be accessed as a property of the `ResultSet` object (e.g. `myResultSet.MY_COLUMN_NAME`).

        > Copy code
        >
        > ```
        > var valueArray = [];
        > // For each row...
        > while (myResultSet.next())  {
        >     // Append each column of the current row...
        >     valueArray.push(myResultSet.MY_COLUMN_NAME1);
        >     valueArray.push(myResultSet.MY_COLUMN_NAME2);
        >     ...
        >     // Do something with the row of data that we retrieved.
        >     f(valueArray);
        >     // Reset the array before getting the next row.
        >     valueArray = [];
        >     }
        > ```

    Note

    Remember that unless the column name was delimited with double quotes in the CREATE TABLE statement, the column name should be all uppercase in the
    JavaScript code.

getColumnValueAsString(colIdx|colName)
:   This method returns the value of a column as a string, which is useful when you need a column value regardless of the original data type in the table.

    The method is identical to the method `getColumnValue()` except that it returns a string value.

    For more details, see `getColumnValue()`.

getNumRowsAffected()
:   This method returns the number of rows affected (e.g. inserted/updated/deleted) by the Statement that generated this ResultSet.

    If more than one type of change applies (e.g. a [MERGE](/sql-reference/sql/merge) operation inserted some rows and
    updated others), then the number is the total number of rows affected by all of the changes.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows affected.

    Errors:
    :   None.

getQueryId()
:   This method returns the UUID of the most recent query executed.

    Parameters:
    :   None.

    Returns:
    :   A string containing a UUID, which is the query ID.

    Examples:
    :   Copy code

        ```
        var queryId = resultSet.getQueryId();
        ```

getRowCount()
:   This method returns the number of rows in this ResultSet. (This is the total number of rows, not the number of rows that
    haven’t been consumed yet.)

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows.

    Errors:
    :   None.

next()
:   This method gets the next row in the `ResultSet` and makes it available for access.

    This method does not return the new data row. Instead, it makes the row available so that you can call methods such as `ResultSet.getColumnValue()` to
    retrieve the data.

    Note that you must call `next()` for each row in the result set, including the first row.

    Parameters:
    :   None.

    Returns:
    :   `true` if it retrieved a row and `false` if there are no more rows to retrieve.

        Thus, you can iterate through `ResultSet` until `next()` returns false.

    Errors:
    :   None.

## Object: `SfDate`

JavaScript does not have a native data type that corresponds to the Snowflake SQL data types
TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, and TIMESTAMP\_TZ. When you retrieve a value of type TIMESTAMP from the database
and want to store it as a JavaScript variable (for example, copy the value from a ResultSet to a JavaScript variable),
use the Snowflake-defined JavaScript data type `SfDate`.
The `SfDate` (“SnowFlake Date”) data type is an extension of the JavaScript date data type.
`SfDate` has extra methods, which are documented below.

### Constants

None.

### Methods

Unless otherwise specified, the examples below assume UTC time zone.

getEpochSeconds()
:   This method returns the number of seconds since the beginning of “the epoch” (midnight January 1, 1970).

    Parameters:
    :   None.

    Returns:
    :   The number of seconds between midnight January 1, 1970 and the timestamp stored in the variable.

    Examples:
    :   Create the stored procedure:

        > Copy code
        >
        > ```
        > CREATE OR REPLACE PROCEDURE test_get_epoch_seconds(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getEpochSeconds();
        >     $$
        >     ;
        > ```

        Pass the procedure different timestamps and retrieve the number of seconds since the epoch for each timestamp.

        > Copy code
        >
        > ```
        > CALL test_get_epoch_seconds('1970-01-01 00:00:00.000000000');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |                      0 |
        > +------------------------+
        > ```
        >
        > Copy code
        >
        > ```
        > CALL test_get_epoch_seconds('1970-01-01 00:00:01.987654321');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |                      1 |
        > +------------------------+
        > ```
        >
        > Copy code
        >
        > ```
        > CALL test_get_epoch_seconds('1971-01-01 00:00:00');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |               31536000 |
        > +------------------------+
        > ```

getNanoSeconds()
:   This method returns the value of the nanoseconds field of the object. Note that this is just the fractional
    seconds, not the nanoseconds since the beginning of the epoch. Thus the value is always between 0 and 999999999.

    Parameters:
    :   None.

    Returns:
    :   The number of nanoseconds.

    Examples:
    :   Create the stored procedure:

        > Copy code
        >
        > ```
        > CREATE OR REPLACE PROCEDURE test_get_nano_seconds2(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getNanoSeconds();
        >     $$
        >     ;
        > -- Should be 0 nanoseconds.
        > -- (> SNIPPET_TAG=query_03_01
        > CALL test_get_nano_seconds2('1970-01-01 00:00:00.000000000');
        > ```

        Pass the procedure different timestamps and retrieve the number of nanoseconds from each.

        > Copy code
        >
        > ```
        > CALL test_get_nano_seconds2('1970-01-01 00:00:00.000000000');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |                      0 |
        > +------------------------+
        > ```
        >
        > Copy code
        >
        > ```
        > CALL test_get_nano_seconds2('1970-01-01 00:00:01.987654321');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |              987654321 |
        > +------------------------+
        > ```
        >
        > Copy code
        >
        > ```
        > CALL test_get_nano_seconds2('1971-01-01 00:00:00.000123456');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |                 123456 |
        > +------------------------+
        > ```

getScale()
:   This method returns the precision of the data type, i.e. the number of digits after the decimal point.
    For example, the precision of TIMESTAMP\_NTZ(3) is 3 (milliseconds). The precision of TIMESTAMP\_NTZ(0) is 0 (no
    fractional seconds). The precision of TIMESTAMP\_NTZ is 9 (nanoseconds).

    The minimum is 0. The maximum is 9 (precision is to 1 nanosecond). The default precision is 9.

    Parameters:
    :   None.

    Returns:
    :   The number of digits after the decimal place (number of digits in the fractional seconds field).

    Examples:
    :   Create the stored procedure:

        > Copy code
        >
        > ```
        > CREATE OR REPLACE PROCEDURE test_get_scale(TSV VARCHAR, SCALE VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ(" + SCALE + ");";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getScale();
        >     $$
        >     ;
        >
        > -- Should be 0.
        > -- (> SNIPPET_TAG=query_04_01
        > CALL test_get_scale('1970-01-01 00:00:00', '0');
        > ```

        In this example, the timestamp is defined as TIMESTAMP\_NTZ(0), so the precision is 0.

        > Copy code
        >
        > ```
        > CALL test_get_scale('1970-01-01 00:00:00', '0');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              0 |
        > +----------------+
        > ```

        In this example, the timestamp is defined as TIMESTAMP\_NTZ(2), so the precision is 2.

        > Copy code
        >
        > ```
        > CALL test_get_scale('1970-01-01 00:00:01.123', '2');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              2 |
        > +----------------+
        > ```

        In this example, the timestamp is defined as TIMESTAMP\_NTZ, so the precision is 9, which is the default.

        > Copy code
        >
        > ```
        > CALL test_get_scale('1971-01-01 00:00:00.000123456', '9');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              9 |
        > +----------------+
        > ```

getTimezone()
:   This method returns the timezone as the number of minutes before or after UTC.

    Parameters:
    :   None.

    Returns:
    :   The timezone as a number of minutes before or after UTC.

    Examples:
    :   Create the stored procedure:

        > Copy code
        >
        > ```
        > CREATE OR REPLACE PROCEDURE test_get_Timezone(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_TZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getTimezone();
        >     $$
        >     ;
        > ```

        In this example, the time zone is 8 hours (480 minutes) behind UTC.

        > Copy code
        >
        > ```
        > CALL test_get_timezone('1970-01-01 00:00:01-08:00');
        > +-------------------+
        > | TEST_GET_TIMEZONE |
        > |-------------------|
        > |              -480 |
        > +-------------------+
        > ```

        In this example, the time zone is 11 hours (660 minutes) ahead of UTC.

        > Copy code
        >
        > ```
        > CALL test_get_timezone('1971-01-01 00:00:00.000123456+11:00');
        > +-------------------+
        > | TEST_GET_TIMEZONE |
        > |-------------------|
        > |               660 |
        > +-------------------+
        > ```

toString()
:   Parameters:
    :   None.

    Returns:
    :   This method returns a string representation of the timestamp.

    Examples:
    :   This shows a simple example of creating an `SfDate` and calling its `toString` method:

        > Copy code
        >
        > ```
        > CREATE OR REPLACE PROCEDURE test_toString(TSV VARCHAR)
        >     RETURNS VARIANT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_TZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.toString();
        >     $$
        >     ;
        > ```
        >
        > Copy code
        >
        > ```
        > CALL test_toString('1970-01-02 03:04:05');
        > +------------------------------------------------------------------+
        > | TEST_TOSTRING                                                    |
        > |------------------------------------------------------------------|
        > | "Fri Jan 02 1970 03:04:05 GMT+0000 (Coordinated Universal Time)" |
        > +------------------------------------------------------------------+
        > ```
