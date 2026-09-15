Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_TIME

Returns the current time for the system.

Aliases:
:   [LOCALTIME](/sql-reference/functions/localtime)

## Syntax

Copy code

```
CURRENT_TIME( [ <fract_sec_precision> ] )

CURRENT_TIME
```

## Arguments

`fract_sec_precision`
:   This optional argument indicates the precision with which to report the
    time. For example, a value of 3 says to use 3 digits after the decimal
    point (i.e. to specify the time with a precision of milliseconds).

    The default precision is 9 (nanoseconds).

    Valid values range from 0 - 9. However, most platforms do not support true
    nanosecond precision; the precision that you get might be less than the
    precision you specify. In practice, precision is usually approximately
    milliseconds (3 digits) at most.

    Note

    - Fractional seconds are only displayed if they have been explicitly set in the [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format) parameter for the session (e.g. `'HH24:MI:SS.FF'`).

## Returns

Returns a value of type [TIME](/sql-reference/data-types-datetime#label-datatypes-time).

## Usage notes

- The setting of the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter affects the return value. The returned time is
  in the time zone for the session.
- The display format for times in the output is determined by the [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format)
  session parameter (default `HH24:MI:SS`).
- To comply with the ANSI standard, this function can be called without parentheses in SQL statements.

  However, if you are setting a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
  to an expression that calls the function (for example, `my_var := function_name();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](/sql-reference/functions-context#label-context-function-usage-notes).
- Do not use the returned value for precise time ordering between concurrent queries (processed by the same virtual
  warehouse) because the queries might be serviced by different compute resources (in the warehouse).

## Examples

Set the time output format to `HH24:MI:SS.FF`, then return the current time with fractional seconds precision first set to 2, then 4, and then the default (9):

Copy code

```
ALTER SESSION SET TIME_OUTPUT_FORMAT = 'HH24:MI:SS.FF';

SELECT CURRENT_TIME(2);
```

```
+-----------------+
| CURRENT_TIME(2) |
|-----------------|
| 15:35:51.24     |
+-----------------+
```

Copy code

```
SELECT CURRENT_TIME(4);
```

```
+-----------------+
| CURRENT_TIME(4) |
|-----------------|
| 15:36:53.5570   |
+-----------------+
```

Copy code

```
SELECT CURRENT_TIME;
```

```
+--------------------+
| CURRENT_TIME       |
|--------------------|
| 15:37:29.644000000 |
+--------------------+
```
