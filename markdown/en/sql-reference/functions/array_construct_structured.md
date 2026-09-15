Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_CONSTRUCT\_STRUCTURED

Returns a [structured ARRAY](/sql-reference/data-types-structured) constructed from one or more inputs, where
the element type is the common type of the inputs.

Unlike [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct), which returns a semi-structured ARRAY, this function returns
a structured `ARRAY(<type>)` value.

See also:
:   [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct)

## Syntax

Copy code

```
ARRAY_CONSTRUCT_STRUCTURED( <expr1> [ , <expr2> [ , ... ] ] )
```

## Arguments

`expr#`
:   The input expressions to evaluate; the resulting values become the elements of the array. All of the input
    expressions are cast to a single, common element type.

## Returns

Returns a [structured ARRAY](/sql-reference/data-types-structured), `ARRAY(<type>)`. The element type is the common
type that all of the input expressions are cast to. If any input can be NULL, the element type is nullable.

## Usage notes

- You must specify at least one argument. Unlike [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct), this function doesn’t
  support an empty argument list.
- At least one argument must have a non-NULL type. If every argument is an untyped NULL, the function returns an
  error because the element type can’t be determined.
- All of the arguments are cast to a single, common element type. For example, `ARRAY_CONSTRUCT_STRUCTURED(1, '1')`
  returns an array with a single element type, rather than an array with mixed types.
- NULL input values are retained as elements in the resulting array.
- The element type can itself be a structured type. For example, you can construct a structured ARRAY of structured
  ARRAY values or of [MAP](/sql-reference/data-types-structured) values.
- To construct a semi-structured ARRAY, use [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct).

## Examples

Construct a structured array of numbers:

Copy code

```
SELECT ARRAY_CONSTRUCT_STRUCTURED(1, 2, 3) AS structured_array;
```

```
+------------------+
| STRUCTURED_ARRAY |
|------------------|
| [                |
|   1,             |
|   2,             |
|   3              |
| ]                |
+------------------+
```

NULL input values are retained as elements in the resulting array:

Copy code

```
SELECT ARRAY_CONSTRUCT_STRUCTURED(NULL, 'a', 'b') AS structured_array;
```

```
+------------------+
| STRUCTURED_ARRAY |
|------------------|
| [                |
|   undefined,     |
|   "a",           |
|   "b"            |
| ]                |
+------------------+
```

Construct a structured array whose elements are themselves structured arrays:

Copy code

```
SELECT ARRAY_CONSTRUCT_STRUCTURED(
    [1, 2]::ARRAY(INT),
    [3, 4]::ARRAY(INT)) AS nested_array;
```

```
+--------------+
| NESTED_ARRAY |
|--------------|
| [            |
|   [          |
|     1,       |
|     2        |
|   ],         |
|   [          |
|     3,       |
|     4        |
|   ]          |
| ]            |
+--------------+
```
