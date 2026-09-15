Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# LOCALTIME

Returns the current time for the system.

ANSI-compliant alias for [CURRENT\_TIME](/sql-reference/functions/current_time).

## Syntax

Copy code

```
LOCALTIME()

LOCALTIME
```

## Arguments

None.

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

Show the current local time and local timestamp:

Copy code

```
SELECT LOCALTIME(), LOCALTIMESTAMP();
```

```
+-------------+-------------------------------+
| LOCALTIME() | LOCALTIMESTAMP()              |
|-------------+-------------------------------|
| 15:32:45    | 2024-04-17 15:32:45.775 -0700 |
+-------------+-------------------------------+
```
