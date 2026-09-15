Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# LOCALTIMESTAMP

Returns the current timestamp for the system in the local time zone.

ANSI-compliant alias for [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp).

## Syntax

Copy code

```
LOCALTIMESTAMP( [ <fract_sec_precision> ] )

LOCALTIMESTAMP
```

## Arguments

`fract_sec_precision`
:   This optional argument indicates the precision with which to report the
    time. For example, a value of 3 says to use 3 digits after the decimal
    point (that is, to specify the time with a precision of milliseconds).

    The default precision is 9 (nanoseconds).

    Valid values range from 0 - 9. However, most platforms do not support true
    nanosecond precision; the precision that you get might be less than the
    precision you specify. In practice, precision is usually approximately
    milliseconds (3 digits) at most.

    Note

    Fractional seconds are only displayed if they have been explicitly set in the [TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format) parameter for the session (e.g. `'YYYY-MM-DD HH24:MI:SS.FF'`).

## Returns

Returns the current system time. The data type of the returned value is
[TIMESTAMP\_LTZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations).

## Usage notes

- The setting of the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter affects the return value. The returned timestamp is in the time zone for the session.
- The setting of the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) parameter does not affect the return value.
- Do not use the returned value for precise time ordering between concurrent queries (processed by the same virtual warehouse) because the queries might be serviced by different compute resources (in the warehouse).

- To comply with the ANSI standard, this function can be called without parentheses in SQL statements.

  However, if you are setting a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
  to an expression that calls the function (for example, `my_var := LOCALTIMESTAMP();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](/sql-reference/functions-context#label-context-function-usage-notes).

## Examples

Show the current local time and local timestamp:

Copy code

```
SELECT LOCALTIME(), LOCALTIMESTAMP();
```

```
+-------------+-------------------------------+
| LOCALTIME() | LOCALTIMESTAMP()              |
|-------------+-------------------------------|
| 07:58:09    | 2024-04-18 07:58:09.848 -0700 |
+-------------+-------------------------------+
```
