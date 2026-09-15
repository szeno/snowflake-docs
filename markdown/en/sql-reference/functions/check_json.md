Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Parsing)

# CHECK\_JSON

Checks the validity of a JSON document. If the input string is a valid JSON
document or a NULL, the output is NULL (i.e. no error). If the input cannot be
translated to a valid JSON value, the output string contains the error message.

## Syntax

Copy code

```
CHECK_JSON( <string_or_variant_expr> )
```

## Arguments

`string_or_variant_expr`
:   A `VARIANT` or string value (or expression) to check.

    If the expression is of type `VARIANT`, it should contain a
    string.

## Examples

Create a table and insert some `VARCHAR` and `VARIANT` values:

> Copy code
>
> ```
> CREATE TABLE sample_json_table (ID INTEGER, varchar1 VARCHAR, variant1 VARIANT);
> INSERT INTO sample_json_table (ID, varchar1) VALUES 
>     (1, '{"ValidKey1": "ValidValue1"}'),
>     (2, '{"Malformed -- Missing value": }'),
>     (3, NULL)
>     ;
> UPDATE sample_json_table SET variant1 = varchar1::VARIANT;
> ```

Use the `CHECK_JSON` function to check the validity of potential
JSON-compatible strings in a `VARCHAR` column:

> Copy code
>
> ```
> SELECT ID, CHECK_JSON(varchar1), varchar1 FROM sample_json_table ORDER BY ID;
> +----+----------------------+----------------------------------+
> | ID | CHECK_JSON(VARCHAR1) | VARCHAR1                         |
> |----+----------------------+----------------------------------|
> |  1 | NULL                 | {"ValidKey1": "ValidValue1"}     |
> |  2 | misplaced }, pos 32  | {"Malformed -- Missing value": } |
> |  3 | NULL                 | NULL                             |
> +----+----------------------+----------------------------------+
> ```

Use the `CHECK_JSON` function to check the validity of potential
JSON-compatible strings in a `VARIANT` column:

> Copy code
>
> ```
> SELECT ID, CHECK_JSON(variant1), variant1 FROM sample_json_table ORDER BY ID;
> +----+----------------------+--------------------------------------+
> | ID | CHECK_JSON(VARIANT1) | VARIANT1                             |
> |----+----------------------+--------------------------------------|
> |  1 | NULL                 | "{\"ValidKey1\": \"ValidValue1\"}"   |
> |  2 | misplaced }, pos 32  | "{\"Malformed -- Missing value\": }" |
> |  3 | NULL                 | NULL                                 |
> +----+----------------------+--------------------------------------+
> ```
