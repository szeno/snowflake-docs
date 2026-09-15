Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# GET\_IGNORE\_CASE

Extracts a field value from an object; returns NULL if either of the arguments is NULL.

Note

This function is similar to [GET](/sql-reference/functions/get) but applies case-insensitive matching to field names.

See also:
:   [GET](/sql-reference/functions/get)

## Syntax

**OBJECT (or VARIANT containing an OBJECT)**

Copy code

```
GET_IGNORE_CASE( <object> , <field_name> )

GET_IGNORE_CASE( <variant> , <field_name> )
```

**MAP**

Copy code

```
GET_IGNORE_CASE( <map> , <key> )
```

## Arguments

`variant`
:   An expression that evaluates to a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) that contains either an ARRAY or an OBJECT.

`object`
:   An expression that evaluates to an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that contains key-value pairs.

`field_name`
:   An expression that evaluates to a VARCHAR. This specifies the key in a key-value pair for which you want to retrieve the value.

    `field_name` must not be an empty string.

    If `object` is a [structured OBJECT](/sql-reference/data-types-structured), you must specify a constant for
    `field_name`.

    If `object` does not contain the specified key:

    - If `object` is a semi-structured OBJECT, the function returns NULL.
    - If `object` is a structured OBJECT, an error occurs.

`map`
:   An expression that evaluates to a [MAP](/sql-reference/data-types-structured).

`key`
:   The key in a key-value pair for which you want to retrieve the value.

    If `map` does not contain the specified key, the function returns NULL.

## Returns

- The returned value is the specified element of the ARRAY, or the value that corresponds to the specified key of a key-value
  pair in the OBJECT.
- If the input object is a semi-structured OBJECT, ARRAY, or VARIANT value, the function returns a VARIANT value. The data type
  of the value is VARIANT because:

  - In an ARRAY value, each element is of type VARIANT.
  - In an OBJECT value, the value in each key-value pair is of type VARIANT.
- If the input object is a [structured OBJECT, structured ARRAY, or MAP](/sql-reference/data-types-structured),
  the function returns a value of the type specified for the object.

  For example, if the type of the input object is ARRAY(NUMBER), the function returns a NUMBER value.

## Usage notes

- This function returns the first exact match it finds. If the function only finds ambiguous (case-insensitive) matches, it returns the value for one of the matches; however, no guarantee can be made on which ambiguous field name is matched first.
- GET\_IGNORE\_CASE is a binary function that can be called in the following ways:
  - `object` is an OBJECT value and `field_name` is a string value, which can be a constant or an expression.

    This variation of GET\_IGNORE\_CASE extracts the value of the field with the provided name from the object value.
  - `v` is a VARIANT value and `field_name` is a string value, which can be a constant or an expression.

    Works similarly to GET\_IGNORE\_CASE with `object`, but additionally checks that `v` contains an object value (and returns NULL if `v` does not contain an object).

## Examples

Extract a field value from an object. The function returns the value for the exact match:

Copy code

```
SELECT GET_IGNORE_CASE(TO_OBJECT(PARSE_JSON('{"aa":1, "aA":2, "Aa":3, "AA":4}')),'aA') as output;

+--------+
| OUTPUT |
|--------|
| 2      |
+--------+
```

Extract a field value from an object. The function cannot find an exact match and so returns one of the ambiguous matches:

Copy code

```
SELECT GET_IGNORE_CASE(TO_OBJECT(PARSE_JSON('{"aa":1, "aA":2, "Aa":3}')),'AA') as output;

+--------+
| OUTPUT |
|--------|
| 3      |
+--------+
```

For more detailed examples, see [Querying Semi-structured Data](/user-guide/querying-semistructured).
