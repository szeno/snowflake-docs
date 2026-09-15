Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_NULL\_VALUE

Returns TRUE if its [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument is a [JSON null](/user-guide/semistructured-considerations#label-variant-null) value.

Important

The JSON null value is distinct from the SQL NULL value.

This function returns TRUE only for JSON null values, not SQL NULL values.
The difference is shown in the first and third rows in
[the output for the example below](#label-parse-json-function-examples).

A missing JSON value is converted to a SQL NULL value, for which
IS\_NULL\_VALUE returns NULL. The 4th column in
[the output for the example below](#label-parse-json-function-examples)
shows this.

This function is different from the [IS [ NOT ] NULL](/sql-reference/functions/is-null) function.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is)

## Syntax

Copy code

```
IS_NULL_VALUE( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

This function returns a value of type BOOLEAN or NULL:

- Returns TRUE for a JSON null value.
- Returns FALSE for a non-null JSON value.
- Returns NULL for a SQL NULL value.

## Examples

This example uses the IS\_NULL\_VALUE function. First, create a table with a VARIANT column:

Copy code

```
CREATE OR REPLACE TABLE test_is_null_value_function (
  variant_value VARIANT);
```

Insert a string value into the column using the [PARSE\_JSON](/sql-reference/functions/parse_json) function:

Copy code

```
INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON('"string value"'));
```

Note

The PARSE\_JSON function returns a VARIANT value.

Insert a JSON null value into the column:

Copy code

```
INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON('null'));
```

Insert an empty object into the column:

Copy code

```
INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON('{}'));
```

Insert two rows with JSON name/value pairs into the VARIANT column :

Copy code

```
INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON('{"x": null}'));

INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON('{"x": "foo"}'));
```

Insert a NULL into the column:

Copy code

```
INSERT INTO test_is_null_value_function (variant_value)
  (SELECT PARSE_JSON(NULL));
```

Query the table:

Copy code

```
SELECT variant_value,
       variant_value:x value_of_x,
       IS_NULL_VALUE(variant_value) is_variant_value_a_json_null,
       IS_NULL_VALUE(variant_value:x) is_x_a_json_null,
       IS_NULL_VALUE(variant_value:y) is_y_a_json_null
  FROM test_is_null_value_function;
```

```
+----------------+------------+------------------------------+------------------+------------------+
| VARIANT_VALUE  | VALUE_OF_X | IS_VARIANT_VALUE_A_JSON_NULL | IS_X_A_JSON_NULL | IS_Y_A_JSON_NULL |
|----------------+------------+------------------------------+------------------+------------------|
| "string value" | NULL       | False                        | NULL             | NULL             |
| null           | NULL       | True                         | NULL             | NULL             |
| {}             | NULL       | False                        | NULL             | NULL             |
| {              | null       | False                        | True             | NULL             |
|   "x": null    |            |                              |                  |                  |
| }              |            |                              |                  |                  |
| {              | "foo"      | False                        | False            | NULL             |
|   "x": "foo"   |            |                              |                  |                  |
| }              |            |                              |                  |                  |
| NULL           | NULL       | NULL                         | NULL             | NULL             |
+----------------+------------+------------------------------+------------------+------------------+
```

In the query results:

- The `variant_value` column shows six rows of inserted VARIANT values.
- The `value_of_x` column shows the JSON value for the name `x` in each row.
- The `is_variant_value_a_json_null` column returns the results of the IS\_NULL\_VALUE function
  for the VARIANT value in each row.
- The `is_x_a_json_null` column returns the results of the IS\_NULL\_VALUE function
  for the name `x` in each row. Rows without an `x` name return NULL.
- The `is_y_a_json_null` column returns the results of the IS\_NULL\_VALUE function
  for the name `y` in each row. Because there is no matching `y` name in any
  row, all of the rows return NULL.
