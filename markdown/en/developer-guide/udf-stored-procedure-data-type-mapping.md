# Data Type Mappings Between SQL and Handler Languages

A stored procedure or user-defined function you write is called from SQL, and so receives and returns values in SQL data types. However,
its underlying handler will use data types from the handler’s language, such as Java, Python, or Scala. At runtime, Snowflake converts
between the SQL types and handler types for arguments and return values.

Note that Snowflake makes these conversions the following cases as well:

- When dynamically constructing a SQL statement that uses a value in a handler variable.
- When binding a handler variable’s value to a prepared statement.

This topic describes valid mappings between SQL data and types and those from the supported handler languages. Use this content to choose
data types when writing a handler.

For information about Snowflake SQL data types, see [Summary of data types](/sql-reference/intro-summary-data-types).

## SQL-Java Data Type Mappings

The table below shows the type mappings between SQL and Java. These mappings generally apply to both the arguments
passed to the procedure or function and the values returned from it. However, there are some exceptions, which are listed
in footnotes.

Note that some SQL data types (e.g. NUMBER) are compatible with multiple Java data types (e.g. `int`, `long`, etc.). In these cases,
you can use any Java data type that has enough capacity to hold the actual values that will be passed. If you
pass a SQL value to an incompatible Java data type (or vice versa), Snowflake throws an error.

| SQL Type | Java Type | Notes |
| --- | --- | --- |
| ARRAY | `String[]` | Formats the elements of the array as strings. |
| ARRAY | `String` | Formats the array as a JSON string (e.g. `[1, "foo", null]`). |
| BINARY | `byte[]` |  |
| BINARY | `String` | Encodes the binary string in hexadecimal. [[4]](#footnote-4) |
| BINARY | `InputStream` | Exposes the BINARY value as a sequence of bytes. |
| BOOLEAN | `boolean` | Cannot be null. |
| BOOLEAN | `Boolean` |  |
| BOOLEAN | `String` | [[4]](#footnote-4) |
| DATE | `java.sql.Date` |  |
| DATE | `String` | Formats the date as `YYYY-MM-DD`. [[4]](#footnote-4) |
| FLOAT | `double` | Cannot be null. |
| FLOAT | `Double` |  |
| FLOAT | `float` | Cannot be null. Might result in precision loss. |
| FLOAT | `Float` | Might result in precision loss. |
| FLOAT | `String` | Might result in precision loss (float -> string conversion is lossy). |
| GEOGRAPHY | `String` | Formats the geography as [GeoJSON](https://tools.ietf.org/html/rfc7946). |
| GEOGRAPHY | [Geography](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Geography.html) | [[5]](#footnote-5) |
| MAP | `Map<String, String>` | The output format is MAP(VARCHAR, VARCHAR). |
| NUMBER | `short` | Cannot be null. Must fit in the range of short (no fractional part, and integer part cannot exceed the max/min short values). |
| NUMBER | `Short` | Must fit in the range of short (no fractional part, and integer part cannot exceed the max/min short values). |
| NUMBER | `int` | Cannot be null. Must fit in the range of int (no fractional part, and integer part cannot exceed the max/min int values). |
| NUMBER | `Integer` | Must fit in the range of int (no fractional part, and integer part cannot exceed the max/min int values). |
| NUMBER | `long` | Cannot be null. Must fit in the range of long (no fractional part, and integer part cannot exceed the max/min long values). |
| NUMBER | `Long` | Must fit in the range of long (no fractional part, and integer part cannot exceed the max/min long values). |
| NUMBER | `java.math.BigDecimal` |  |
| NUMBER | `java.math.BigInteger` | Must fit into the range of BigInteger (no fractional part). |
| NUMBER | `String` |  |
| OBJECT | `Map<String, String>` | The map’s keys are the object’s keys, and the values are formatted as strings. |
| OBJECT | `String` | Formats the object as a JSON string (e.g. `{"x": 3, "y": true}`). |
| TIME | `java.sql.Time` | [[3]](#footnote-3) |
| TIME | `String` | Formats the time as `HH:MI:SS.SSSSSSSSS` where the fractional seconds part depends on the precision of the time. [[3]](#footnote-3) |
| TIMESTAMP\_LTZ | `java.sql.Timestamp` | Must fit in the range of java.sql.Timestamp. [[3]](#footnote-3) |
| TIMESTAMP\_LTZ | `String` | The output format is `DY, DD MON YYYY HH24:MI:SS TZHTZM`. [[1]](#footnote-1) , [[3]](#footnote-3) , [[4]](#footnote-4) |
| TIMESTAMP\_NTZ | `java.sql.Timestamp` | Must fit in the range of java.sql.Timestamp. Treats the wallclock time as an offset from the Unix epoch (imposing a UTC time zone, effectively). [[3]](#footnote-3) |
| TIMESTAMP\_NTZ | `String` | Treats the wallclock time as an offset from the Unix epoch (imposing a UTC time zone, effectively). The output format is `DY, DD MON YYYY HH:MI:SS`. [[2]](#footnote-2) , [[3]](#footnote-3) , [[4]](#footnote-4) |
| TIMESTAMP\_TZ | `java.sql.Timestamp` | Must fit in the range of java.sql.Timestamp. [[3]](#footnote-3) |
| TIMESTAMP\_TZ | `String` | The output format is `DY, DD MON YYYY HH24:MI:SS TZHTZM`. [[1]](#footnote-1) , [[3]](#footnote-3) , [[4]](#footnote-4) |
| VARCHAR | `String` |  |
| VARIANT | [Variant](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Variant.html) | The [Variant](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Variant.html) data type is a class in the Snowpark package. For more information, see [Snowpark Package Types Supported for User-Defined Functions](#label-java-udf-supported-snowpark-types). For an example, see [Passing a VARIANT value to an in-line Java UDF](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-passing-variant). |

Expand

Show lessSee more

[1]
The format matches the Internet (RFC) Timestamp Format `DY, DD MON YYYY HH24:MI:SS TZHTZM` as described in [Timestamp formats](/sql-reference/date-time-input-output#label-date-time-input-output-timestamp-formats). If a timezone offset (the `TZHTZM` component) is present, it is typically digits (e.g. `-0700` indicates 7 hours behind UTC). If the timezone offset is `Z` (for “Zulu”) rather than digits, that is synonymous with “+0000” (UTC).

[2]
The format matches the Internet (RFC) Timestamp Format `DY, DD MON YYYY HH24:MI:SS` as described in [Timestamp formats](/sql-reference/date-time-input-output#label-date-time-input-output-timestamp-formats). If the string is followed by a space and `Z` (for “Zulu”), that explicitly indicates that the offset is “+0000” (UTC).

[3]
Although Snowflake can store time values with nanosecond precision, the java.sql.time library maintains only millisecond precision. Conversion between Snowflake and Java data types can reduce effective precision to milliseconds.

[4]
This type mapping is supported when converting SQL arguments to Java, but not when converting Java return types to SQL types.

[5]
Java does not have a native Geography data type. The [Geography](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Geography.html) data type referred to here is a class in the Snowpark package. For more information, see [Snowpark Package Types Supported for User-Defined Functions](#label-java-udf-supported-snowpark-types).

### Arrays

Java UDFs can receive arrays of any of the following Java data types:

| Data Type | Notes |
| --- | --- |
| `String` |  |
| `boolean` | The Snowflake ARRAY must contain only BOOLEAN elements and must not contain any NULL values. |
| `double`  `float` | The Snowflake ARRAY must contain either of the following, and must not contain any NULL values.   - [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) elements. - [Fixed-point](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) elements (with any scale). |
| `int`  `long`  `short` | The Snowflake ARRAY must contain only [fixed-point](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) elements with a scale of 0, and must not contain any NULL values. |

Expand

Show lessSee more

### NULL Values

Snowflake supports two distinct NULL values: SQL `NULL` and VARIANT’s JSON `null`. (For information about Snowflake
VARIANT NULL, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).)

Java supports one `null` value, which is only for non-primitive data types.

A SQL `NULL` argument to a Java handler translates to the Java `null` value, but only for Java data types that
support `null`.

A returned Java `null` value translates back to SQL `NULL`.

### TIMESTAMP\_LTZ Values and Time Zones

A Java UDF is largely isolated from the environment in which it is called. However, the timezone is inherited from
the calling environment. If the caller’s session set a default time zone before calling the Java UDF, then the Java
UDF has the same default time zone. Java UDF uses the same [IANA Time Zone Database](https://www.iana.org/time-zones) data as the native [TIMEZONE](/sql-reference/parameters#label-timezone)
Snowflake SQL uses (i.e. data from release 2025b of the Time Zone Database).

### Snowpark Package Types Supported for User-Defined Functions

In a user-defined function, you can use a specific subset of types that are included in the Snowflake
[Snowpark Java package](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html). Although these types are
designed for use in Snowpark code, a few are also supported for use in UDFs for the convenience they can provide. (For more about
Snowpark, see the [Snowpark documentation](/developer-guide/snowpark/index).)

Note

The Snowpark library is a requirement for stored procedures written in Java, Python, and Scala. As a result, you can use Snowpark types
there without restriction.

Snowpark types in the following table are supported in UDF code. You should not use other Snowpark types in UDF code; they are not
supported there.

| Snowpark Type | Snowpark Version Required | Description |
| --- | --- | --- |
| [Geography](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Geography.html) | 1.2.0 and later | Represents the Snowflake [GEOGRAPHY](/sql-reference/data-types-geospatial) type. For an example that uses the `Geography` data type, see [Passing a GEOGRAPHY value to an in-line Java UDF](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-passing-geo). |
| [Variant](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Variant.html) | 1.4.0 and later | Represents Snowflake [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) data. For an example that uses the `Variant` data type, see [Passing a VARIANT value to an in-line Java UDF](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-passing-variant). |

Expand

Show lessSee more

#### Specifying the Snowpark Package as a Dependency

When developing UDF code that uses the Snowpark package, you’ll need to set up your development environment so that you can compile and
run code with Snowpark dependencies. For more, see [Setting Up Other Development Environments for Snowpark Java](/developer-guide/snowpark/java/setup-other-environments).

When deploying a UDF by executing the [CREATE FUNCTION](/sql-reference/sql/create-function) statement, you can specify the Snowpark
package as a dependency without uploading the JAR file to a stage (the library is already in Snowflake). To do this, specify the package
name and version in the `PACKAGES` clause. For a syntax example, see [Passing a GEOGRAPHY value to an in-line Java UDF](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-passing-geo).

## SQL-JavaScript Data Type Mappings

The following table shows the Snowflake SQL data types and the corresponding JavaScript data types:

| SQL Data Type | JavaScript Data Type | Notes |
| --- | --- | --- |
| ARRAY | `JSON` |  |
| BOOLEAN | `number` | The values `true` and `false` are represented by `1` and `0` respectively. Note that this behavior may change in future releases, so you should rely on JavaScript truthiness rather than direct value comparisons. |
| DATE | `date` |  |
| GEOGRAPHY, GEOMETRY | `JSON` |  |
| REAL, FLOAT, FLOAT8, FLOAT4, DOUBLE, DOUBLE PRECISION | `number` |  |
| TIME | `string` |  |
| TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ | `date` or `SfDate` | When a timestamp is passed as an argument to a stored procedure, the timestamp is converted to a JavaScript `date` object. In other situations (e.g. when retrieving from `ResultSet`), a timestamp is converted to an `SfDate` object. For more details about the `SfDate` data type, which is not a standard JavaScript data type, see the [JavaScript stored procedures API](/developer-guide/stored-procedure/stored-procedures-api). |
| VARCHAR, CHAR, CHARACTER, STRING, TEXT | `string` |  |
| VARIANT | `JSON` |  |

Expand

Show lessSee more

### Notes

Not all Snowflake SQL data types have a corresponding JavaScript data type. For example, JavaScript does not
directly support the INTEGER or NUMBER data types. In these cases, you should convert the SQL data type to an
appropriate alternative data type. For example, you can convert a SQL INTEGER into a SQL FLOAT, which can then be
converted to a JavaScript value of data type `number`.

The table below shows appropriate conversions for the incompatible SQL data types:

| Incompatible SQL Data Type | Compatible SQL Data Type |
| --- | --- |
| BINARY | Uint8Array |
| INTEGER | FLOAT |
| NUMBER, NUMERIC, DECIMAL | FLOAT |
| OBJECT | Uint8Array |

Expand

Show lessSee more

#### When Returning Values

If the `return`
statement in the JavaScript returns a data type different from the stored procedure’s declared return type,
the JavaScript value is cast to the SQL data type if possible. For example, if a number is returned, but the
stored procedure is declared as returning a string, the number is converted to a string within JavaScript, and
then copied to the string returned in the SQL statement. (Keep in mind that some JavaScript programming errors, such as
returning the wrong data type, can be hidden by this behavior.)

If no valid cast for the conversion exists, then an error occurs.

#### When Binding Values

When you bind JavaScript variables to SQL statements, Snowflake converts from the JavaScript data types to
the SQL data types. You can bind variables of the following JavaScript data types:

- number
- string
- SfDate

  For more details about the `SfDate` data type, which is not a standard JavaScript data type, see
  the [JavaScript stored procedures API](/developer-guide/stored-procedure/stored-procedures-api).

For more information about binding, including some examples, see [Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

You might also find the following topics helpful:

- [JavaScript data types](/developer-guide/udf/javascript/udf-javascript-introduction#label-javascript-data-types)
- [JavaScript arguments and returned values](/developer-guide/udf/javascript/udf-javascript-introduction#label-js-udf-arguments)

## SQL-Python Data Type Mappings

The table below shows the type mappings between SQL and Python. These mappings generally apply to both the arguments
passed to the Python handler and the values returned from it.

| SQL Type | Python Type | Notes |
| --- | --- | --- |
| ARRAY | `list` | When a Python data type is converted to ARRAY, if there is any embedded Python decimal data, the embedded Python decimal will be converted to a String in the ARRAY. |
| BINARY | `bytes` |  |
| BOOLEAN | `bool` |  |
| DATE | `datetime.date` |  |
| FLOAT | `float` | Floating point operations can have small rounding errors, which can accumulate, especially when aggregate functions process large numbers of rows. Rounding errors can vary each time a query is executed if the rows are processed in a different order. For more information, see [Numeric Data Types: Float](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers). |
| GEOGRAPHY, GEOMETRY | `dict` | Formats the geography as [GeoJSON](https://tools.ietf.org/html/rfc7946) and then converts it to a Python dict. |
| MAP | `dict` | MAP is not supported as a return type. |
| NUMBER | `int` or `decimal.Decimal` | If the scale of the NUMBER type is 0 then the int Python type is used. Otherwise decimal.Decimal type is used. |
| OBJECT | `dict` | When a Python data type is converted to OBJECT, if there is any embedded Python decimal data, the embedded Python decimal will be converted to a String in the OBJECT. |
| TIME | `datetime.time` | Although Snowflake can store time values with nanosecond precision, the Python datetime.time type maintains only millisecond precision. Conversion between Snowflake and Python data types can reduce effective precision to milliseconds. |
| TIMESTAMP\_LTZ | `datetime.datetime` | Use local timezone to convert internal UTC time to local “naive” datetime. Requires “naive” datetime as return type. |
| TIMESTAMP\_NTZ | `datetime.datetime` | Directly convert to “naive” datetime. Requires “naive” datetime as return type. |
| TIMESTAMP\_TZ | `datetime.datetime` | Convert to “aware” datetime with timezone information. Requires “aware” datetime as return type. |
| VARCHAR | `str` |  |
| VARIANT | `dict`, `list`, `int`, `float`, `str`, or `bool` | Each variant row is converted to a Python type dynamically for arguments and vice versa for return values. The following types are converted to strings instead of native Python types: decimal, binary, date, time, timestamp\_ltz, timestamp\_ntz, timestamp\_tz. When a Python data type is converted to VARIANT and Python decimal data is embedded, the embedded Python decimal is converted to a string in the VARIANT. |
| VECTOR | `memoryview` |  |

Expand

Show lessSee more

## SQL-Scala Data Type Mappings

Snowflake supports the following Scala data types in addition to the Java types listed in [SQL-Java Data Type Mappings](#label-sql-java-data-type-mappings):

| SQL Data Type | Scala Type | Notes |
| --- | --- | --- |
| ARRAY | `Array[String]` |  |
| BINARY | `Array[Byte]` |  |
| BOOLEAN | `Boolean` or `Option[Boolean]` |  |
| DOUBLE | `Double` or `Option[Double]` |  |
| FLOAT | `Float` or `Option[Float]` |  |
| MAP | `Map[String, String]` | The output format is MAP(VARCHAR, VARCHAR). |
| NUMBER | The following types are supported:   - `Int` or `Option[Int]` - `Long` or `Option[Long]` |  |
| OBJECT | `Map[String, String]` |  |
| VARCHAR | `String` |  |
| VARIANT | `String` | Formats the value depending on the type that is represented. [Variant null](/user-guide/semistructured-considerations#label-variant-null) is formatted as the string “null”. |

Expand

Show lessSee more

For [DATE](/sql-reference/data-types-datetime#label-datatypes-date) and [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp), use the Java types listed in
[SQL-Java Data Type Mappings](#label-sql-java-data-type-mappings).
