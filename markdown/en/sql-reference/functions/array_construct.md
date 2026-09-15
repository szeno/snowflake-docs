Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_CONSTRUCT

Returns an array constructed from zero, one, or more inputs.

For more information about constructing and using arrays, see [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array).

See also:
:   [ARRAY\_CONSTRUCT\_COMPACT](/sql-reference/functions/array_construct_compact) , [ARRAY\_CONSTRUCT\_STRUCTURED](/sql-reference/functions/array_construct_structured)

## Syntax

Copy code

```
ARRAY_CONSTRUCT( [ <expr1> ] [ , <expr2> [ , ... ] ] )
```

## Arguments

The arguments are values (or expressions that evaluate to values). The argument values can be
different data types.

## Returns

The data type of the returned value is ARRAY.

## Usage notes

- If the function is called with `N` arguments, the size of the resulting array is `N`.
- In many contexts, you can use an [ARRAY constant](/sql-reference/data-types-semistructured#label-array-constant) (also called an *ARRAY literal*) instead of
  the ARRAY\_CONSTRUCT function.
- An array can contain both SQL NULL values and JSON null values. For more information, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).

## Examples

Construct a basic array consisting of numeric data types:

Copy code

```
SELECT ARRAY_CONSTRUCT(10, 20, 30);
```

```
+-----------------------------+
| ARRAY_CONSTRUCT(10, 20, 30) |
|-----------------------------|
| [                           |
|   10,                       |
|   20,                       |
|   30                        |
| ]                           |
+-----------------------------+
```

Construct a basic array consisting of different data types, including a SQL NULL value (`undefined`) and
a JSON null value (`null`):

Copy code

```
SELECT ARRAY_CONSTRUCT(NULL, PARSE_JSON('null'), 'hello', 3::DOUBLE, 4, 5);
```

```
+---------------------------------------------------------------------+
| ARRAY_CONSTRUCT(NULL, PARSE_JSON('NULL'), 'HELLO', 3::DOUBLE, 4, 5) |
|---------------------------------------------------------------------|
| [                                                                   |
|   undefined,                                                        |
|   null,                                                             |
|   "hello",                                                          |
|   3.000000000000000e+00,                                            |
|   4,                                                                |
|   5                                                                 |
| ]                                                                   |
+---------------------------------------------------------------------+
```

Construct an empty array:

Copy code

```
SELECT ARRAY_CONSTRUCT();
```

```
+-------------------+
| ARRAY_CONSTRUCT() |
|-------------------|
| []                |
+-------------------+
```

Create a table and insert arrays into an ARRAY column:

Copy code

```
CREATE OR REPLACE TABLE construct_array_example (id INT, array_column ARRAY);

INSERT INTO construct_array_example (id, array_column)
  SELECT 1,
         ARRAY_CONSTRUCT(1, 2, 3);

INSERT INTO construct_array_example (id, array_column)
  SELECT 2,
         ARRAY_CONSTRUCT(4, 5, 6);

INSERT INTO construct_array_example (id, array_column)
  SELECT 3,
         ARRAY_CONSTRUCT(7, 8, 9);

SELECT * FROM construct_array_example;
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
|  3 | [            |
|    |   7,         |
|    |   8,         |
|    |   9          |
|    | ]            |
+----+--------------+
```
