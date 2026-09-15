Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_CONTAINS

Returns TRUE if the specified value is found in the specified array.

## Syntax

Copy code

```
ARRAY_CONTAINS( <value_expr> , <array> )
```

## Arguments

`value_expr`
:   Value to find in `array`.

    - If `array` is a [semi-structured array](/sql-reference/data-types-semistructured#label-data-type-array), `value_expr` must evaluate to a
      [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
    - If `array` is a [structured array](/sql-reference/data-types-structured), `value_expr` must evaluate
      to a type that is [comparable](/sql-reference/data-types-structured#label-structured-types-compare-struct-struct) to the type of the array.

`array`
:   The array to search.

## Returns

This function returns a value of BOOLEAN type or NULL:

- The function returns TRUE if `value_expr` is present in `array`, including the following cases:

  - When the `value_expr` argument is NULL and there is a SQL NULL value in the array (`undefined`).
  - When the `value_expr` argument is JSON null and there is a JSON null value in the array (`null`).
- The function returns FALSE if `value_expr` isn’t present in `array`, including when the
  `value_expr` argument is JSON null and there are no JSON null values in the array.
- The function returns NULL if the `value_expr` argument is NULL and there are no SQL NULL values in the array.

For more information about NULL values in arrays, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).

## Usage notes

- The function does not support wildcards in `value_expr`. However, you can
  use the [ARRAY\_TO\_STRING](/sql-reference/functions/array_to_string) function to convert an array to a string, then search the
  string with wildcard characters. For example, you can specify wildcards to search the
  returned string using the [[ NOT ] LIKE](/sql-reference/functions/like) and [REGEXP\_LIKE](/sql-reference/functions/regexp_like) functions.
- If `array` is a semi-structured array, [explicit casting](/sql-reference/data-type-conversion#label-data-type-explicit-casting)
  of the `value_expr` value to a VARIANT value is required for values of the following data types:

  - [String & binary](/sql-reference/data-types-text)
  - [Date & time](/sql-reference/data-types-datetime)

  The following example explicitly casts a string value to a VARIANT value:

  Copy code

  ```
  SELECT ARRAY_CONTAINS('mystring2'::VARIANT, ARRAY_CONSTRUCT('mystring1', 'mystring2'));
  ```

  Explicit casting isn’t required for values of other data types.

## Examples

The following queries use the ARRAY\_CONTAINS function in a SELECT list.

In this example, the function returns TRUE because the `value_expr` argument is `'hello'`
and the array contains a VARIANT value that stores the string `'hello'`:

Copy code

```
SELECT ARRAY_CONTAINS('hello'::VARIANT, ARRAY_CONSTRUCT('hello', 'hi'));
```

```
+------------------------------------------------------------------+
| ARRAY_CONTAINS('HELLO'::VARIANT, ARRAY_CONSTRUCT('HELLO', 'HI')) |
|------------------------------------------------------------------|
| True                                                             |
+------------------------------------------------------------------+
```

In this example, the function returns FALSE because the `value_expr` argument is `'hello'`
but the array doesn’t contain a VARIANT value that stores the string `'hello'`:

Copy code

```
SELECT ARRAY_CONTAINS('hello'::VARIANT, ARRAY_CONSTRUCT('hola', 'bonjour'));
```

```
+----------------------------------------------------------------------+
| ARRAY_CONTAINS('HELLO'::VARIANT, ARRAY_CONSTRUCT('HOLA', 'BONJOUR')) |
|----------------------------------------------------------------------|
| False                                                                |
+----------------------------------------------------------------------+
```

In this example, the function returns NULL because the `value_expr` argument is NULL but
the array doesn’t contain a SQL NULL value:

Copy code

```
SELECT ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('hola', 'bonjour'));
```

```
+----------------------------------------------------------+
| ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('HOLA', 'BONJOUR')) |
|----------------------------------------------------------|
| NULL                                                     |
+----------------------------------------------------------+
```

In this example, the function returns TRUE because the `value_expr` argument is NULL and
the array contains a SQL NULL value:

Copy code

```
SELECT ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('hola', NULL));
```

```
+-----------------------------------------------------+
| ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('HOLA', NULL)) |
|-----------------------------------------------------|
| True                                                |
+-----------------------------------------------------+
```

In this example, the function returns TRUE because the `value_expr` argument is a
JSON null value and the array contains a JSON null value:

Copy code

```
SELECT ARRAY_CONTAINS(PARSE_JSON('null'), ARRAY_CONSTRUCT('hola', PARSE_JSON('null')));
```

```
+---------------------------------------------------------------------------------+
| ARRAY_CONTAINS(PARSE_JSON('NULL'), ARRAY_CONSTRUCT('HOLA', PARSE_JSON('NULL'))) |
|---------------------------------------------------------------------------------|
| True                                                                            |
+---------------------------------------------------------------------------------+
```

In this example, the function returns NULL because the `value_expr` argument is
NULL but the array doesn’t contain a SQL NULL value (although it does contain a JSON null value):

Copy code

```
SELECT ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('hola', PARSE_JSON('null')));
```

```
+-------------------------------------------------------------------+
| ARRAY_CONTAINS(NULL, ARRAY_CONSTRUCT('HOLA', PARSE_JSON('NULL'))) |
|-------------------------------------------------------------------|
| NULL                                                              |
+-------------------------------------------------------------------+
```

The following query uses the ARRAY\_CONTAINS function in a WHERE clause. First, create a
table with an ARRAY column and insert data:

Copy code

```
CREATE OR REPLACE TABLE array_example (id INT, array_column ARRAY);

INSERT INTO array_example (id, array_column)
  SELECT 1, ARRAY_CONSTRUCT(1, 2, 3);

INSERT INTO array_example (id, array_column)
  SELECT 2, ARRAY_CONSTRUCT(4, 5, 6);

SELECT * FROM array_example;
```

```
+----+--------------+
| ID | ARRAY_COLUMN |
|----+--------------|
|  1 | [            |
|    |   1,         |
|    |   2,         |
|    |   3          |
|    | ]            |
|  2 | [            |
|    |   4,         |
|    |   5,         |
|    |   6          |
|    | ]            |
+----+--------------+
```

Run a query that specifies the value to find for `value_expr` and the
ARRAY column for `array`:

Copy code

```
SELECT * FROM array_example WHERE ARRAY_CONTAINS(5, array_column);
```

```
+----+--------------+
| ID | ARRAY_COLUMN |
|----+--------------|
|  2 | [            |
|    |   4,         |
|    |   5,         |
|    |   6          |
|    | ]            |
+----+--------------+
```
