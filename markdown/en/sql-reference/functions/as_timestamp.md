Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_TIMESTAMP\_\*

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to the respective
[timestamp](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) value:

- AS\_TIMESTAMP\_LTZ (value with local time zone)
- AS\_TIMESTAMP\_NTZ (value with no time zone)
- AS\_TIMESTAMP\_TZ (value with time zone)

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [AS\_DATE](/sql-reference/functions/as_date) , [AS\_TIME](/sql-reference/functions/as_time)

## Syntax

Copy code

```
AS_TIMESTAMP_LTZ( <variant_expr> )

AS_TIMESTAMP_NTZ( <variant_expr> )

AS_TIMESTAMP_TZ( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of a timestamp type or NULL:

- If the type of the value in the `variant_expr` argument is a timestamp type, the function returns a value of same timestamp type.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_timestamp_example (timestamp1 VARIANT);

INSERT INTO as_timestamp_example (timestamp1)
  SELECT TO_VARIANT(TO_TIMESTAMP_NTZ('2024-10-10 12:34:56'));
```

Use the AS\_TIMESTAMP\_NTZ function in a query to cast a VARIANT value to a TIMESTAMP\_NTZ value:

Copy code

```
SELECT AS_TIMESTAMP_NTZ(timestamp1) AS timestamp_value
  FROM as_timestamp_example;
```

```
+-------------------------+
| TIMESTAMP_VALUE         |
|-------------------------|
| 2024-10-10 12:34:56.000 |
+-------------------------+
```
