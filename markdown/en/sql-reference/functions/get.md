Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# GET

Extracts a value from an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) or an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) (or a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) that
contains an ARRAY or OBJECT).

The function returns NULL if either of the arguments is NULL.

Note that this function should not be confused with the [GET](/sql-reference/sql/get) DML command.

See also:
:   [GET\_IGNORE\_CASE](/sql-reference/functions/get_ignore_case) , [GET\_PATH , :](/sql-reference/functions/get_path)

## Syntax

**ARRAY (or VARIANT containing an ARRAY)**

Copy code

```
GET( <array> , <index> )

GET( <variant> , <index> )
```

**OBJECT (or VARIANT containing an OBJECT)**

Copy code

```
GET( <object> , <field_name> )

GET( <variant> , <field_name> )
```

**MAP**

Copy code

```
GET( <map> , <key> )
```

## Arguments

`array`
:   An expression that evaluates to an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array).

`index`
:   An expression that evaluates to an INTEGER. This specifies the position of the element to retrieve from the ARRAY. The
    position is 0-based, not 1-based.

    If the index points outside of the array boundaries, or if the indexed element does not exist (in a sparse array):

    - If `array` is a semi-structured ARRAY, this function returns NULL.
    - If `array` is a structured ARRAY, an error occurs.

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

- GET applies case-sensitive matching to `field_name`. For case-insensitive matching, use [GET\_IGNORE\_CASE](/sql-reference/functions/get_ignore_case).
- If the first parameter is of type VARIANT:
  - If the second parameter is of type VARCHAR (e.g. a `field_name`), the function returns NULL if `variant`
    does not contain an OBJECT.
  - If the second parameter is of type INTEGER (e.g. an `index`), the function returns NULL if `variant`
    does not contain an ARRAY.

## Examples

Create a table with sample data:

> Copy code
>
> ```
> CREATE TABLE vartab (a ARRAY, o OBJECT, v VARIANT);
> INSERT INTO vartab (a, o, v) 
>   SELECT
>     ARRAY_CONSTRUCT(2.71, 3.14),
>     OBJECT_CONSTRUCT('Ukraine', 'Kyiv'::VARIANT, 
>                      'France',  'Paris'::VARIANT),
>     TO_VARIANT(OBJECT_CONSTRUCT('weatherStationID', 42::VARIANT,
>                      'timestamp', '2022-03-07 14:00'::TIMESTAMP_LTZ::VARIANT,
>                      'temperature', 31.5::VARIANT,
>                      'sensorType', 'indoor'::VARIANT))
>     ;
> ```
>
> Copy code
>
> ```
> SELECT a, o, v FROM vartab;
> +---------+----------------------+-------------------------------------------------+
> | A       | O                    | V                                               |
> |---------+----------------------+-------------------------------------------------|
> | [       | {                    | {                                               |
> |   2.71, |   "France": "Paris", |   "sensorType": "indoor",                       |
> |   3.14  |   "Ukraine": "Kyiv"  |   "temperature": 31.5,                          |
> | ]       | }                    |   "timestamp": "2022-03-07 14:00:00.000 -0800", |
> |         |                      |   "weatherStationID": 42                        |
> |         |                      | }                                               |
> +---------+----------------------+-------------------------------------------------+
> ```

Extract the first element of an ARRAY:

> Copy code
>
> ```
> SELECT GET(a, 0) FROM vartab;
> +-----------+
> | GET(A, 0) |
> |-----------|
> | 2.71      |
> +-----------+
> ```

Given the name of a country, extract the name of the capital city of that country from an OBJECT containing country names and
capital cities:

> Copy code
>
> ```
> SELECT GET(o, 'Ukraine') FROM vartab;
> +-------------------+
> | GET(O, 'UKRAINE') |
> |-------------------|
> | "Kyiv"            |
> +-------------------+
> ```

Extract the temperature from a VARIANT that contains an OBJECT:

> Copy code
>
> ```
> SELECT GET(v, 'temperature') FROM vartab;
> +-----------------------+
> | GET(V, 'TEMPERATURE') |
> |-----------------------|
> | 31.5                  |
> +-----------------------+
> ```

For more detailed examples, see [Querying Semi-structured Data](/user-guide/querying-semistructured).

For examples of using GET with XMLGET, see the Examples and Usage Notes sections in [XMLGET](/sql-reference/functions/xmlget).
