# Snowflake data types

Snowflake supports most basic SQL data types (with some restrictions) for use in columns, local variables, expressions, parameters,
and any other appropriate locations.

Note

You can also load unstructured data into Snowflake. For more information, see [Introduction to unstructured data](/user-guide/unstructured-intro).

In some cases, data of one type can be converted to another type. For example, INTEGER data can be converted to FLOAT data.

Some conversions are lossless, but others might lose information. The amount of loss depends upon the data types and the specific
values. For example, converting a FLOAT value to an INTEGER value removes the digits after the decimal place. (The value is
rounded to the nearest integer.)

In some cases, the user must specify the desired conversion, such as when passing a VARCHAR value to the
[TIME\_SLICE](/sql-reference/functions/time_slice) function, which expects a TIMESTAMP or DATE argument. We
call this explicit casting.

In other cases, data types are converted automatically, such as when adding a float and an integer. We call this

implicit casting (or
coercion). In Snowflake, data types are
automatically coerced whenever necessary and possible.

For more information about explicit and implicit casting, see [Data type conversion](/sql-reference/data-type-conversion).

For more information about Snowflake data types, see the following topics:

- [Summary of data types](/sql-reference/intro-summary-data-types)
- [Numeric data types](/sql-reference/data-types-numeric)
- [String & binary data types](/sql-reference/data-types-text)
- [Logical data types](/sql-reference/data-types-logical)
- [Date & time data types](/sql-reference/data-types-datetime)
- [Semi-structured data types](/sql-reference/data-types-semistructured)
- [Structured data types](/sql-reference/data-types-structured)
- [Unstructured data types](/sql-reference/data-types-unstructured)
- [Geospatial data types](/sql-reference/data-types-geospatial)
- [UUID data type](/sql-reference/data-types-uuid)
- [Vector data types](/sql-reference/data-types-vector)
- [User-defined types](/sql-reference/data-types-user-defined)
- [Unsupported data types](/sql-reference/data-types-unsupported)
- [Data type conversion](/sql-reference/data-type-conversion)
