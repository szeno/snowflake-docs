Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_TIMESTAMP

Returns the current timestamp for the system in the local time zone.

Aliases:
:   [LOCALTIMESTAMP](/sql-reference/functions/localtimestamp) , [GETDATE](/sql-reference/functions/getdate) , [SYSTIMESTAMP](/sql-reference/functions/systimestamp)

## Syntax

Copy code

```
CURRENT_TIMESTAMP( [ <fract_sec_precision> ] )

CURRENT_TIMESTAMP
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
  to an expression that calls the function (for example, `my_var := CURRENT_TIMESTAMP();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](/sql-reference/functions-context#label-context-function-usage-notes).
- The aliases SYSTIMESTAMP and GETDATE differ from CURRENT\_TIMESTAMP in the following ways:

  - They do not support the `fract_sec_precision` argument.
  - These functions must be called with parentheses.

## Examples

The examples in this section use the timestamp output format `YYYY-MM-DD HH24:MI:SS.FF`. To configure
your session to use the same output format, run the following statement:

Copy code

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
```

### Call the CURRENT\_TIMESTAMP function with different precision values

Return the current timestamp with fractional seconds precision set to `2`:

Copy code

```
SELECT CURRENT_TIMESTAMP(2);
```

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2024-04-17 15:41:38.29 |
+------------------------+
```

Return the current timestamp with fractional seconds precision set to `4`:

Copy code

```
SELECT CURRENT_TIMESTAMP(4);
```

```
+--------------------------+
| CURRENT_TIMESTAMP(4)     |
|--------------------------|
| 2024-04-17 15:42:14.2100 |
+--------------------------+
```

Return the current timestamp with fractional seconds precision set to the default (`9`):

Copy code

```
SELECT CURRENT_TIMESTAMP;
```

```
+-------------------------------+
| CURRENT_TIMESTAMP             |
|-------------------------------|
| 2024-04-17 15:42:55.130000000 |
+-------------------------------+
```

### Call the CURRENT\_TIMESTAMP function with different TIMEZONE settings

Set the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter to `America/New_York` and call the CURRENT\_TIMESTAMP function:

Copy code

```
ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT CURRENT_TIMESTAMP(2);
```

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2025-08-11 14:16:43.57 |
+------------------------+
```

Set the TIMEZONE parameter to `America/Los_Angeles` and call the CURRENT\_TIMESTAMP function:

Copy code

```
ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

SELECT CURRENT_TIMESTAMP(2);
```

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2025-08-11 11:17:18.19 |
+------------------------+
```
