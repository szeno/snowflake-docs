Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# GETDATE

Returns the current timestamp for the system in the local time zone.

Alias for [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp).

## Syntax

Copy code

```
GETDATE()
```

## Arguments

None. This function must be called with parentheses.

## Returns

Returns the current system time. The data type of the returned value is
[TIMESTAMP\_LTZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations).

## Usage notes

- The setting of the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter affects the return value. The returned timestamp is in the time zone for the session.
- The setting of the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) parameter does not affect the return value.
- Do not use the returned value for precise time ordering between concurrent queries (processed by the same virtual warehouse) because the queries might be serviced by different compute resources (in the warehouse).

- This function does not support the `fract_sec_precision` argument that is supported by
  the [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) function.

## Examples

Show the current system timestamp:

Copy code

```
SELECT GETDATE();
```

```
+-------------------------------+
| GETDATE()                     |
|-------------------------------|
| 2024-04-17 15:44:20.960000000 |
+-------------------------------+
```
