Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_DATE

Returns the current date of the system.

## Syntax

Copy code

```
CURRENT_DATE()

CURRENT_DATE
```

## Arguments

None.

## Returns

The function returns a value of type [DATE](/sql-reference/data-types-datetime#label-datatypes-date).

## Usage notes

- The setting of the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter affects the return value. The returned date is
  in the time zone for the session.
- The display format for dates in the output is determined by the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format)
  session parameter (default `YYYY-MM-DD`).
- To comply with the ANSI standard, this function can be called without parentheses in SQL statements.

  However, if you are setting a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
  to an expression that calls the function (for example, `my_var := CURRENT_DATE();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](/sql-reference/functions-context#label-context-function-usage-notes).

## Examples

Show the current date, time, and timestamp:

Copy code

```
SELECT CURRENT_DATE(), CURRENT_TIME(), CURRENT_TIMESTAMP();
```

```
+----------------+----------------+-------------------------------+
| CURRENT_DATE() | CURRENT_TIME() | CURRENT_TIMESTAMP()           |
|----------------+----------------+-------------------------------|
| 2024-04-18     | 07:47:37       | 2024-04-18 07:47:37.084 -0700 |
+----------------+----------------+-------------------------------+
```
