Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_VARIANT

Converts any value to a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value or NULL (if input is NULL).

## Syntax

Copy code

```
TO_VARIANT( <expr> )
```

## Arguments

`expr`
:   An expression of any data type.

## Usage notes

- The `TO_VARIANT` function cannot be used directly in an INSERT statement.
  Instead, use `INSERT INTO ... SELECT...`. The Examples section
  shows how to do this.

## Examples

Use TO\_VARIANT and [PARSE\_JSON](/sql-reference/functions/parse_json) to insert VARIANT values into a table. The PARSE\_JSON function
returns a VARIANT value.

Copy code

```
CREATE OR REPLACE TABLE to_variant_example (
  v_varchar   VARIANT,
  v_number    VARIANT,
  v_timestamp VARIANT,
  v_array     VARIANT,
  v_object    VARIANT);

INSERT INTO to_variant_example (v_varchar, v_number, v_timestamp, v_array, v_object)
  SELECT
    TO_VARIANT('Skiing is fun!'),
    TO_VARIANT(3.14),
    TO_VARIANT('2024-01-25 01:02:03'),
    TO_VARIANT(ARRAY_CONSTRUCT('San Mateo', 'Seattle', 'Berlin')),
    PARSE_JSON(' { "key1": "value1", "key2": "value2" } ');

SELECT * FROM to_variant_example;
```

```
+------------------+----------+-----------------------+----------------+---------------------+
| V_VARCHAR        | V_NUMBER | V_TIMESTAMP           | V_ARRAY        | V_OBJECT            |
|------------------+----------+-----------------------+----------------+---------------------|
| "Skiing is fun!" | 3.14     | "2024-01-25 01:02:03" | [              | {                   |
|                  |          |                       |   "San Mateo", |   "key1": "value1", |
|                  |          |                       |   "Seattle",   |   "key2": "value2"  |
|                  |          |                       |   "Berlin"     | }                   |
|                  |          |                       | ]              |                     |
+------------------+----------+-----------------------+----------------+---------------------+
```
