Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_TIME

Verifies whether a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument contains a [TIME](/sql-reference/data-types-datetime#label-datatypes-time) value.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is) , [IS\_DATE , IS\_DATE\_VALUE](/sql-reference/functions/is_date-value) , [IS\_TIMESTAMP\_\*](/sql-reference/functions/is_timestamp)

## Syntax

Copy code

```
IS_TIME( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if the VARIANT value contains a TIME value. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

Return all of the TIME values in a VARIANT column.

Note

The output format for TIME values is set using the [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format) parameter. The default setting is `HH24:MI:SS`.

Create and load a table with various date and TIME values in a VARIANT column:

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

Show the TIME values in the data by using the IS\_TIME function in a WHERE clause. Only the TIME value
is returned in the output. The DATE and TIMESTAMP values aren’t returned.

Copy code

```
SELECT v FROM vardttm WHERE IS_TIME(v);
```

```
+------------+
| V          |
|------------|
| "20:57:01" |
+------------+
```
