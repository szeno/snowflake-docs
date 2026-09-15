Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_DATE

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [DATE](/sql-reference/data-types-datetime#label-datatypes-date) value. This function does not convert values of
other data types, including timestamps, to DATE values.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

## Syntax

Copy code

```
AS_DATE( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type DATE or NULL:

- If the type of the value in the `variant_expr` argument is DATE, the function returns a value of type DATE.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_date_example (date1 VARIANT);

INSERT INTO as_date_example (date1)
 SELECT TO_VARIANT(TO_DATE('2024-10-10'));
```

Use the AS\_DATE function in a query to cast a VARIANT value to a DATE value:

Copy code

```
SELECT AS_DATE(date1) date_value
  FROM as_date_example;
```

```
+------------+
| DATE_VALUE |
|------------|
| 2024-10-10 |
+------------+
```
