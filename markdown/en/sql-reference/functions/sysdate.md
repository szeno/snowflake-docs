Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYSDATE

Returns the current timestamp for the system in the UTC time zone.

See also:
:   [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp)

## Syntax

Copy code

```
SYSDATE()
```

## Arguments

None.

## Returns

Returns the current timestamp in the UTC time zone.

The data type of the returned value is [TIMESTAMP\_NTZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations).

## Usage notes

- Despite the name, this returns a TIMESTAMP\_NTZ, not a DATE. To control the output format, use the session
  parameter TIMESTAMP\_NTZ\_OUTPUT\_FORMAT.
- This function is similar to CURRENT\_TIMESTAMP, except that:

  - It returns the current timestamp in the UTC time zone, whereas CURRENT\_TIMESTAMP returns the timestamp in the
    local time zone.
  - Its return value is TIMESTAMP\_NTZ, whereas CURRENT\_TIMESTAMP returns TIMESTAMP\_LTZ.
  - It requires parentheses (`SYSDATE()`), whereas CURRENT\_TIMESTAMP can be called without parentheses.
  - It does not support a parameter to specify the precision of fractional seconds.
- Do not use the returned value for precise time ordering between concurrent queries (processed by the same virtual
  warehouse) because the queries might be serviced by different compute resources (in the warehouse).

## Examples

Set the time output format to `YYYY-MM-DD HH24:MI:SS.FF4`, then return the SYSDATE and CURRENT\_TIMESTAMP.
Note the difference in the hour field due to the difference in time zone.

Copy code

```
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF4';
ALTER SESSION SET TIMESTAMP_LTZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF4';

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

SELECT SYSDATE(), CURRENT_TIMESTAMP();
```

```
+--------------------------+--------------------------+
| SYSDATE()                | CURRENT_TIMESTAMP()      |
|--------------------------+--------------------------|
| 2024-04-17 22:47:54.3520 | 2024-04-17 15:47:54.3520 |
+--------------------------+--------------------------+
```
