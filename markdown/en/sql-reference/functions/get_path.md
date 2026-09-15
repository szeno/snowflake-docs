Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# GET\_PATH , `:`

Extracts a value from semi-structured data using a path name.

GET\_PATH is a variation of [GET](/sql-reference/functions/get); it takes a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant), [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object),
or [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) column name as the first argument, and extracts the value of the field or the
element according to the path name provided as the second argument.

## Syntax

Copy code

```
GET_PATH( <column_identifier> , '<path_name>' )

<column_identifier>:<path_name>

:( <column_identifier> , '<path_name>' )
```

## Arguments

`column_identifier`
:   An expression that evaluates to a VARIANT, OBJECT, or ARRAY column.

`path_name`
:   An expression that evaluates to a VARCHAR value. This value specifies the path to the field or element
    that you want to extract.

    For [structured types](/sql-reference/data-types-structured), you must specify a string constant.

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

- GET\_PATH is equivalent to a chain of [GET](/sql-reference/functions/get) functions. It returns NULL if the path name doesn’t correspond to any element.
- The path name syntax is standard JavaScript notation; it consists of a concatenation of field names (identifiers) preceded by
  periods (for example, `.`) and index operators (for example, `[<index>]`):

  - The first field name doesn’t require the leading period to be specified.
  - The index values in the index operators can be non-negative decimal numbers (for arrays) or single or double-quoted
    string literals (for object fields).

  For more details, see [Querying Semi-structured Data](/user-guide/querying-semistructured).
- GET\_PATH also supports a syntactic shortcut using the `:` character as the extraction operator that separates the column
  name (which can contain periods) from the path specifier.

  To maintain syntactic consistency, the path notation also supports SQL-style double-quoted identifiers, and use of `:` as path separators.

  When the `:` operator is used, any integer or string sub-expressions can be included within `[]`.

## Examples

Create a table with a VARIANT column and insert data. Use the [PARSE\_JSON](/sql-reference/functions/parse_json) function to insert the VARIANT data.
The VARIANT values contain nested ARRAY values and OBJECT values.

Copy code

```
CREATE OR REPLACE TABLE get_path_demo(
  id INTEGER,
  v  VARIANT);

INSERT INTO get_path_demo (id, v)
  SELECT 1,
         PARSE_JSON('{
           "array1" : [
             {"id1": "value_a1", "id2": "value_a2", "id3": "value_a3"}
           ],
           "array2" : [
             {"id1": "value_b1", "id2": "value_b2", "id3": "value_b3"}
           ],
           "object_outer_key1" : {
             "object_inner_key1a": "object_x1",
             "object_inner_key1b": "object_x2"
           }
         }');

INSERT INTO get_path_demo (id, v)
  SELECT 2,
         PARSE_JSON('{
           "array1" : [
             {"id1": "value_c1", "id2": "value_c2", "id3": "value_c3"}
           ],
           "array2" : [
             {"id1": "value_d1", "id2": "value_d2", "id3": "value_d3"}
           ],
           "object_outer_key1" : {
             "object_inner_key1a": "object_y1",
             "object_inner_key1b": "object_y2"
           }
         }');

SELECT * FROM get_path_demo;
```

```
+----+----------------------------------------+
| ID | V                                      |
|----+----------------------------------------|
|  1 | {                                      |
|    |   "array1": [                          |
|    |     {                                  |
|    |       "id1": "value_a1",               |
|    |       "id2": "value_a2",               |
|    |       "id3": "value_a3"                |
|    |     }                                  |
|    |   ],                                   |
|    |   "array2": [                          |
|    |     {                                  |
|    |       "id1": "value_b1",               |
|    |       "id2": "value_b2",               |
|    |       "id3": "value_b3"                |
|    |     }                                  |
|    |   ],                                   |
|    |   "object_outer_key1": {               |
|    |     "object_inner_key1a": "object_x1", |
|    |     "object_inner_key1b": "object_x2"  |
|    |   }                                    |
|    | }                                      |
|  2 | {                                      |
|    |   "array1": [                          |
|    |     {                                  |
|    |       "id1": "value_c1",               |
|    |       "id2": "value_c2",               |
|    |       "id3": "value_c3"                |
|    |     }                                  |
|    |   ],                                   |
|    |   "array2": [                          |
|    |     {                                  |
|    |       "id1": "value_d1",               |
|    |       "id2": "value_d2",               |
|    |       "id3": "value_d3"                |
|    |     }                                  |
|    |   ],                                   |
|    |   "object_outer_key1": {               |
|    |     "object_inner_key1a": "object_y1", |
|    |     "object_inner_key1b": "object_y2"  |
|    |   }                                    |
|    | }                                      |
+----+----------------------------------------+
```

Extract the `id3` value from `array2` in each row:

Copy code

```
SELECT id,
       GET_PATH(
         v,
         'array2[0].id3') AS id3_in_array2
  FROM get_path_demo;
```

```
+----+---------------+
| ID | ID3_IN_ARRAY2 |
|----+---------------|
|  1 | "value_b3"    |
|  2 | "value_d3"    |
+----+---------------+
```

Use the `:` operator to extract the same `id3` value from `array2` in each row:

Copy code

```
SELECT id,
       v:array2[0].id3 AS id3_in_array2
  FROM get_path_demo;
```

```
+----+---------------+
| ID | ID3_IN_ARRAY2 |
|----+---------------|
|  1 | "value_b3"    |
|  2 | "value_d3"    |
+----+---------------+
```

This example is the same as the previous example, but uses SQL-style double-quoted identifiers:

Copy code

```
SELECT id,
       v:"array2"[0]."id3" AS id3_in_array2
  FROM get_path_demo;
```

```
+----+---------------+
| ID | ID3_IN_ARRAY2 |
|----+---------------|
|  1 | "value_b3"    |
|  2 | "value_d3"    |
+----+---------------+
```

Extract the `object_inner_key1a` value from the nested OBJECT value in each row:

Copy code

```
SELECT id,
       GET_PATH(
         v,
         'object_outer_key1:object_inner_key1a') AS object_inner_key1A_values
  FROM get_path_demo;
```

```
+----+---------------------------+
| ID | OBJECT_INNER_KEY1A_VALUES |
|----+---------------------------|
|  1 | "object_x1"               |
|  2 | "object_y1"               |
+----+---------------------------+
```

Use the `:` operator to extract the same `object_inner_key1a` values:

Copy code

```
SELECT id,
       v:object_outer_key1.object_inner_key1a AS object_inner_key1a_values
  FROM get_path_demo;
```

```
+----+---------------------------+
| ID | OBJECT_INNER_KEY1A_VALUES |
|----+---------------------------|
|  1 | "object_x1"               |
|  2 | "object_y1"               |
+----+---------------------------+
```

This example is the same as the previous example, but uses SQL-style double-quoted identifiers:

Copy code

```
SELECT id,
       v:"object_outer_key1":"object_inner_key1a" AS object_inner_key1a_values
  FROM get_path_demo;
```

```
+----+---------------------------+
| ID | OBJECT_INNER_KEY1A_VALUES |
|----+---------------------------|
|  1 | "object_x1"               |
|  2 | "object_y1"               |
+----+---------------------------+
```
