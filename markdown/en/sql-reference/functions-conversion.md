# Conversion functions

This family of functions can be used to convert an expression of any Snowflake data type to another data type.

## List of functions

| Sub-category | Function | Notes |
| --- | --- | --- |
| **Any data type** | [CAST , ::](/sql-reference/functions/cast) |  |
| [TRY\_CAST](/sql-reference/functions/try_cast) | Error-handling version of CAST. |
| **Text/character/binary data types** | [TO\_CHAR , TO\_VARCHAR](/sql-reference/functions/to_char) |  |
| [TO\_BINARY](/sql-reference/functions/to_binary) |  |
| [TRY\_TO\_BINARY](/sql-reference/functions/try_to_binary) | Error-handling version of TO\_BINARY. |
| **Numeric data types** | [TO\_DECFLOAT](/sql-reference/functions/to_decfloat) |  |
| [TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](/sql-reference/functions/to_decimal) |  |
| [TO\_DOUBLE](/sql-reference/functions/to_double) |  |
| [TRY\_TO\_DECFLOAT](/sql-reference/functions/try_to_decfloat) | Error-handling version of TO\_DECFLOAT. |
| [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](/sql-reference/functions/try_to_decimal) | Error-handling versions of TO\_DECIMAL, TO\_NUMBER, and so on. |
| [TRY\_TO\_DOUBLE](/sql-reference/functions/try_to_double) | Error-handling version of TO\_DOUBLE. |
| **Boolean data type** | [TO\_BOOLEAN](/sql-reference/functions/to_boolean) |  |
| [TRY\_TO\_BOOLEAN](/sql-reference/functions/try_to_boolean) | Error-handling version of TO\_BOOLEAN. |
| **Date and time data types** | [TO\_DATE , DATE](/sql-reference/functions/to_date) |  |
| [TO\_TIME , TIME](/sql-reference/functions/to_time) |  |
| [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp) |  |
| [TRY\_TO\_DATE](/sql-reference/functions/try_to_date) | Error-handling version of TO\_DATE. |
| [TRY\_TO\_TIME](/sql-reference/functions/try_to_time) | Error-handling version of TO\_TIME. |
| [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](/sql-reference/functions/try_to_timestamp) | Error-handling versions of TO\_TIMESTAMP, and so on. |
| **Semi-structured data types** | [TO\_ARRAY](/sql-reference/functions/to_array) |  |
| [TO\_OBJECT](/sql-reference/functions/to_object) |  |
| [TO\_VARIANT](/sql-reference/functions/to_variant) |  |
| **Geospatial data types** | [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) |  |
| [TRY\_TO\_GEOGRAPHY](/sql-reference/functions/try_to_geography) | Error-handling version of TO\_GEOGRAPHY. |
| [ST\_GEOGFROMGEOHASH](/sql-reference/functions/st_geogfromgeohash) |  |
| [ST\_GEOGPOINTFROMGEOHASH](/sql-reference/functions/st_geogpointfromgeohash) |  |
| [ST\_GEOGRAPHYFROMWKB](/sql-reference/functions/st_geographyfromwkb) |  |
| [ST\_GEOGRAPHYFROMWKT](/sql-reference/functions/st_geographyfromwkt) |  |
| [TO\_GEOMETRY](/sql-reference/functions/to_geometry) |  |
| [TRY\_TO\_GEOMETRY](/sql-reference/functions/try_to_geometry) | Error-handling version of TO\_GEOMETRY. |
| [ST\_GEOMETRYFROMWKB](/sql-reference/functions/st_geometryfromwkb) |  |
| [ST\_GEOMETRYFROMWKT](/sql-reference/functions/st_geometryfromwkt) |  |

Expand

Show lessSee more

## Error-handling conversion functions

Conversion functions with a TRY\_ prefix are special versions of their respective conversion functions. These functions return a NULL value instead of raising an error when the conversion cannot be performed:

- [TRY\_CAST](/sql-reference/functions/try_cast)
- [TRY\_TO\_BINARY](/sql-reference/functions/try_to_binary)
- [TRY\_TO\_BOOLEAN](/sql-reference/functions/try_to_boolean)
- [TRY\_TO\_DATE](/sql-reference/functions/try_to_date)
- [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](/sql-reference/functions/try_to_decimal)
- [TRY\_TO\_DOUBLE](/sql-reference/functions/try_to_double)
- [TRY\_TO\_GEOGRAPHY](/sql-reference/functions/try_to_geography)
- [TRY\_TO\_GEOMETRY](/sql-reference/functions/try_to_geometry)
- [TRY\_TO\_TIME](/sql-reference/functions/try_to_time)
- [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](/sql-reference/functions/try_to_timestamp)

These functions only support string expressions (that is, VARCHAR or CHAR data type) as input.

Important

These error-handling conversion functions are optimized for situations where conversion errors are relatively infrequent:

- If there are no (or very few) errors, they should result in no visible performance impact.
- If there are a large number of conversion failures, using these functions can result in significantly slower performance. Also, when using them with the VARIANT type, some operations might result in reduced performance.

## Numeric formats in conversion functions

The functions
[TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](/sql-reference/functions/to_decimal), and
[TO\_DOUBLE](/sql-reference/functions/to_double)
accept an optional parameter that specifies the format of the input string,
if the input expression evaluates to a string. For more information
about the values this parameter can have, see
[SQL format models](/sql-reference/sql-format-models).

## Date and time formats in conversion functions

The following functions allow you to specify the expected date, time, or timestamp format to parse or produce a string:

- [TO\_CHAR , TO\_VARCHAR](/sql-reference/functions/to_char)
- [TO\_DATE , DATE](/sql-reference/functions/to_date)
- [TRY\_TO\_DATE](/sql-reference/functions/try_to_date)
- [TO\_TIME , TIME](/sql-reference/functions/to_time)
- [TRY\_TO\_TIME](/sql-reference/functions/try_to_time)
- [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp)
- [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](/sql-reference/functions/try_to_timestamp)

You specify the format in an optional argument, using the following case-insensitive elements to describe the format:

| Format element | Description |
| --- | --- |
| `YYYY` | Four-digit [1] year. |
| `YY` | Two-digit [1] year, controlled by the [TWO\_DIGIT\_CENTURY\_START](/sql-reference/parameters#label-two-digit-century-start) session parameter. For example, when set to `1980`, values of `79` and `80` are parsed as `2079` and `1980`, respectively. |
| `Y` | One-digit or two-digit [2] year without leading zeros, controlled by the [TWO\_DIGIT\_CENTURY\_START](/sql-reference/parameters#label-two-digit-century-start) session parameter. For example, when the parameter is set to `1990`, values of `2005` and `1991` are serialized as `5` and `91`, respectively. |
| `MM` | Two-digit [1] month (`01` = January, and so on). |
| `MO` | One-digit or two-digit [2] month without leading zeros (`1` = January, and so on). |
| `MON` | Abbreviated month name [3]. |
| `MMMM` | Full month name [3]. |
| `DD` | Two-digit [1] day of month (`01` through `31`). |
| `D` | One-digit or two-digit [2] day of month without leading zeros (`1` through `31`). |
| `DY` | Abbreviated day of week. |
| `HH24` | Two digits [1] for hour (`00` through `23`). You *must not* specify `AM` / `PM` or `A` / `P`. |
| `HH12` | Two digits [1] for hour (`01` through `12`). You can specify `AM` / `PM` or `A` / `P`. |
| `H24` | One or two digits [2] for hour without leading zeros (`0` through `23`). You *must not* specify `AM` / `PM` or `A` / `P`. |
| `H12` | One or two digits [2] for hour without leading zeros (`1` through `12`). You can specify `AM` / `PM` or `A` / `P`. |
| `AM` , `PM` | Ante meridiem (`AM`) / post meridiem (`PM`). Use this only with `HH12` and `H12` (*not* with `HH24` or `H24`). |
| `P` | Ante meridiem (`A`) / post meridiem (`P`). Use this only with `HH12` and `H12` (*not* with `HH24` or `H24`). |
| `HH` | Synonym for `HH24`. |
| `H` | Synonym for `H24`. |
| `MI` | Two digits [1] for minute (`00` through `59`). |
| `ME` | One or two digits [2] for minute without leading zeros (`0` through `59`). |
| `SS` | Two digits [1] for second (`00` through `59`). |
| `S` | One or two digits [2] for second without leading zeros (`0` through `59`). |
| `FF[0-9]` | Fractional seconds with precision `0` (seconds) to `9` (nanoseconds), for example, `FF`, `FF0`, `FF3`, `FF9`. Specifying `FF` is equivalent to `FF9` (nanoseconds). |
| `TZH:TZM` , `TZHTZM` , `TZH` | Two-digit [1] time zone hour and minute, offset from UTC. Can be prefixed by `+`/`-` for sign. |
| `UUUU` | Four-digit year in [ISO format](https://en.wikipedia.org/wiki/ISO_8601), which is negative for BCE years. |

Expand

Show lessSee more

[1] The number of digits describes the output produced when serializing values to text. When parsing text, Snowflake accepts up to the specified number of digits. For example, a day number can be one or two digits.

[2] The number of digits describes the output produced when serializing values to text: values are serialized without leading zeros. When parsing text, Snowflake accepts one or two digits.

[3] For the MON format element, the output produced when serializing values to text is the abbreviated month name. For the MMMM format element, the output produced when serializing values to text is the full month name. When parsing text, Snowflake accepts the three-letter abbreviation or the full month name for both MON and MMMM. For example, “January” or “Jan”, “February” or “Feb”, and so on are accepted when parsing text.

Note

- When a date-only format is used, the associated time is assumed to be midnight on that day.
- Anything in the format between double quotes or other than the above elements is parsed/formatted without being interpreted.
  Snowflake recommends always enclosing literal characters in double quotes
  (for example, `"T"`, `"EST"`, `"Z"`) to ensure they are treated as literals.
- For more details about valid ranges, number of digits, and best practices, see
  [Additional information about using date, time, and timestamp formats](/sql-reference/date-time-input-output#label-date-time-input-output-additional-information).

### Usage notes

Anything in the format between double quotes or other than the above elements is parsed/formatted without being interpreted.

### Examples

Convert a string to a date using a specified input format of `dd/mm/yyyy`. The display format for dates in the output
is determined by the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) session parameter (default `YYYY-MM-DD`).

Copy code

```
SELECT TO_DATE('3/4/2024', 'dd/mm/yyyy');
```

```
+-----------------------------------+
| TO_DATE('3/4/2024', 'DD/MM/YYYY') |
|-----------------------------------|
| 2024-04-03                        |
+-----------------------------------+
```

Convert a date to a string, and specify a [date output format](/sql-reference/parameters#label-date-output-format)
of `mon dd, yyyy`.

Copy code

```
SELECT TO_VARCHAR('2024-04-05'::DATE, 'mon dd, yyyy');
```

```
+------------------------------------------------+
| TO_VARCHAR('2024-04-05'::DATE, 'MON DD, YYYY') |
|------------------------------------------------|
| Apr 05, 2024                                   |
+------------------------------------------------+
```

## Binary formats in conversion functions

[TO\_CHAR , TO\_VARCHAR](/sql-reference/functions/to_char), and [TO\_BINARY](/sql-reference/functions/to_binary) accept an optional
argument specifying the expected format to parse or produce a string.

The format can be one of the following strings (case-insensitive):

> - HEX
> - BASE64
> - UTF-8

For more information about these formats, see [Overview of supported binary formats](/sql-reference/binary-input-output#label-overview-of-supported-binary-formats).

For examples of using these formats, see the Examples section of
[Binary input and output](/sql-reference/binary-input-output).
