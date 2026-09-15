Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_TIMESTAMP\_\*

Verifies whether a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument contains the respective
[timestamp](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) value:

- IS\_TIMESTAMP\_LTZ (value with local time zone).
- IS\_TIMESTAMP\_NTZ (value with no time zone).
- IS\_TIMESTAMP\_TZ (value with time zone).

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is) , [IS\_DATE , IS\_DATE\_VALUE](/sql-reference/functions/is_date-value) , [IS\_TIME](/sql-reference/functions/is_time)

## Syntax

Copy code

```
IS_TIMESTAMP_LTZ( <variant_expr> )

IS_TIMESTAMP_NTZ( <variant_expr> )

IS_TIMESTAMP_TZ( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if the VARIANT value contains a timestamp. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

Show all timestamps in a VARIANT column, with the output using the time zone specified for the session.

Note

The output format for the time zone is set using a parameter:

- The [TIMESTAMP\_LTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ltz-output-format) parameter sets the format for TIMESTAMP\_LTZ values.
- The [TIMESTAMP\_NTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ntz-output-format) parameter sets the format for TIMESTAMP\_NTZ values.
- The [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-tz-output-format) parameter sets the format for TIMESTAMP\_TZ values.

In these examples, the local time zone is US Pacific Standard Time (-08:00 relative to GMT/UCT).

Create and load a table with various date and time values in a VARIANT column:

Copy code

```
CREATE OR REPLACE TABLE vardttm (v VARIANT);
```

Copy code

```
INSERT INTO vardttm SELECT TO_VARIANT(TO_DATE('2024-02-24'));
INSERT INTO vardttm SELECT TO_VARIANT(TO_TIME('20:57:01.123456789+07:00'));
INSERT INTO vardttm SELECT TO_VARIANT(TO_TIMESTAMP('2023-02-24 12:00:00.456'));
INSERT INTO vardttm SELECT TO_VARIANT(TO_TIMESTAMP_LTZ('2022-02-24 13:00:00.123 +01:00'));
INSERT INTO vardttm SELECT TO_VARIANT(TO_TIMESTAMP_NTZ('2021-02-24 14:00:00.123 +01:00'));
INSERT INTO vardttm SELECT TO_VARIANT(TO_TIMESTAMP_TZ('2020-02-24 15:00:00.123 +01:00'));
```

Use the [TYPEOF](/sql-reference/functions/typeof) function in a query to show the data types of the values stored in the VARIANT column `v`:

Copy code

```
SELECT v, TYPEOF(v) AS type FROM vardttm;
```

```
+---------------------------------+---------------+
| V                               | TYPE          |
|---------------------------------+---------------|
| "2024-02-24"                    | DATE          |
| "20:57:01"                      | TIME          |
| "2023-02-24 12:00:00.456"       | TIMESTAMP_NTZ |
| "2022-02-24 04:00:00.123 -0800" | TIMESTAMP_LTZ |
| "2021-02-24 14:00:00.123"       | TIMESTAMP_NTZ |
| "2020-02-24 15:00:00.123 +0100" | TIMESTAMP_TZ  |
+---------------------------------+---------------+
```

Show the TIMESTAMP\_NTZ values in the data by using the IS\_TIMESTAMP\_NTZ function in a WHERE clause:

Copy code

```
SELECT * FROM vardttm WHERE IS_TIMESTAMP_NTZ(v);
```

```
+---------------------------+
| V                         |
|---------------------------|
| "2023-02-24 12:00:00.456" |
| "2021-02-24 14:00:00.123" |
+---------------------------+
```

Show the TIMESTAMP\_LTZ values in the data by using the IS\_TIMESTAMP\_LTZ function in a WHERE clause:

Copy code

```
SELECT * FROM vardttm WHERE IS_TIMESTAMP_LTZ(v);
```

```
+---------------------------------+
| V                               |
|---------------------------------|
| "2022-02-24 04:00:00.123 -0800" |
+---------------------------------+
```

Show the TIMESTAMP\_TZ values in the data by using the IS\_TIMESTAMP\_TZ function in a WHERE clause:

Copy code

```
SELECT * FROM vardttm WHERE IS_TIMESTAMP_TZ(v);
```

```
+---------------------------------+
| V                               |
|---------------------------------|
| "2020-02-24 15:00:00.123 +0100" |
+---------------------------------+
```
