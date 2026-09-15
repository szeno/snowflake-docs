Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_BINARY

Returns TRUE if its [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument contains a [binary string](/sql-reference/data-types-text#label-binary-datatypes) value.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is)

## Syntax

Copy code

```
IS_BINARY( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if the VARIANT value contains a BINARY value. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

Return all of the BINARY values in a VARIANT column.

Note

The output format for BINARY values is set using the [BINARY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-binary-output-format) parameter.
The default setting is `HEX`.

Create and load a table with a BINARY value in a VARIANT column:

Copy code

```
CREATE OR REPLACE TABLE varbin (v VARIANT);

INSERT INTO varbin SELECT TO_VARIANT(TO_BINARY('snow', 'utf-8'));
```

Show the BINARY values in the data by using the IS\_BINARY function in a WHERE clause:

Copy code

```
SELECT v AS hex_encoded_binary_value
  FROM varbin
  WHERE IS_BINARY(v);
```

```
+--------------------------+
| HEX_ENCODED_BINARY_VALUE |
|--------------------------|
| "736E6F77"               |
+--------------------------+
```
