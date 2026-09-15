Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_DATE , IS\_DATE\_VALUE

Returns TRUE if its [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument contains a [DATE](/sql-reference/data-types-datetime#label-datatypes-date) value.

IS\_DATE and IS\_DATE\_VALUE are synonymous.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is) , [IS\_TIME](/sql-reference/functions/is_time) , [IS\_TIMESTAMP\_\*](/sql-reference/functions/is_timestamp)

## Syntax

Copy code

```
IS_DATE( <variant_expr> )

IS_DATE_VALUE( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if the VARIANT value contains a DATE value. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

Return all of the DATE values in a VARIANT column.

Note

The output format for date values is set using the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) parameter.
The default setting is `YYYY-MM-DD`.

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

Show the DATE values in the data by using the IS\_DATE function in a WHERE clause. Only the DATE value
is returned in the output. The TIME and TIMESTAMP values aren’t returned.

Copy code

```
SELECT v FROM vardttm WHERE IS_DATE(v);
```

```
+--------------+
| V            |
|--------------|
| "2024-02-24" |
+--------------+
```
