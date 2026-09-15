Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_TIME

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [TIME](/sql-reference/data-types-datetime#label-datatypes-time) value. This function does not convert values of
other data types, including timestamps, to TIME values.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

    [AS\_DATE](/sql-reference/functions/as_date) , [AS\_TIMESTAMP\_\*](/sql-reference/functions/as_timestamp)

## Syntax

Copy code

```
AS_TIME( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type TIME or NULL:

- If the type of the value in the `variant_expr` argument is TIME, the function returns a value of type TIME.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_time_example (time1 VARIANT);

INSERT INTO as_time_example (time1)
  SELECT TO_VARIANT(TO_TIME('12:34:56'));
```

Use the AS\_TIME function in a query to cast a VARIANT value to a TIME value:

Copy code

```
SELECT AS_TIME(time1) AS time_value
  FROM as_time_example;
```

```
+------------+
| TIME_VALUE |
|------------|
| 12:34:56   |
+------------+
```
