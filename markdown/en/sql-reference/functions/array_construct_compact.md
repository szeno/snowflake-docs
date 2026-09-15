Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_CONSTRUCT\_COMPACT

Returns an array constructed from zero, one, or more inputs; the constructed
array omits any NULL input values.

See also:
:   [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct)

## Syntax

Copy code

```
ARRAY_CONSTRUCT_COMPACT( [ <expr1> ] [ , <expr2> [ , ... ] ] )
```

## Arguments

`expr#`
:   These are the input expressions to evaluate; the resulting values are put into the array.
    The expressions do not all need to evaluate to the same data type.

## Returns

The data type of the returned value is `ARRAY`.

## Usage notes

- SQL NULL values are skipped when building the result array, resulting in a compacted (i.e. dense) array.

## Examples

Construct a basic dense array consisting of different data types:

Copy code

```
SELECT ARRAY_CONSTRUCT_COMPACT(null,'hello',3::double,4,5);
+-----------------------------------------------------+
| ARRAY_CONSTRUCT_COMPACT(NULL,'HELLO',3::DOUBLE,4,5) |
|-----------------------------------------------------|
| [                                                   |
|   "hello",                                          |
|   3.000000000000000e+00,                            |
|   4,                                                |
|   5                                                 |
| ]                                                   |
+-----------------------------------------------------+
```
