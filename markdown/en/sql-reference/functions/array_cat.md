Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_CAT

Returns a concatenation of two arrays.

## Syntax

Copy code

```
ARRAY_CAT( <array1> , <array2> )
```

## Arguments

`array1`
:   The source array.

`array2`
:   The array to be appended to `array1`.

## Returns

An ARRAY containing the elements from `array2` appended after the elements of `array1`.

## Usage notes

- Both arguments must either be [structured ARRAYs](/sql-reference/data-types-structured) or
  [semi-structured ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array).

- If you are passing in semi-structured ARRAYs, both arguments must be of ARRAY type or VARIANT containing an array.
- If you are passing in structured ARRAYs, the function returns an ARRAY of a type that can accommodate both input types.
- If either argument is NULL, the function returns NULL without reporting any error.

## Examples

This example shows how to use `ARRAY_CAT()`:

> Create a simple table and data:
>
> > Copy code
> >
> > ```
> > CREATE TABLE array_demo (ID INTEGER, array1 ARRAY, array2 ARRAY);
> > ```
> >
> > Copy code
> >
> > ```
> > INSERT INTO array_demo (ID, array1, array2) 
> >     SELECT 1, ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(3, 4);
> > ```
>
> Execute the query:
>
> > Copy code
> >
> > ```
> > SELECT ARRAY_CAT(array1, array2) FROM array_demo;
> > +---------------------------+
> > | ARRAY_CAT(ARRAY1, ARRAY2) |
> > |---------------------------|
> > | [                         |
> > |   1,                      |
> > |   2,                      |
> > |   3,                      |
> > |   4                       |
> > | ]                         |
> > +---------------------------+
> > ```
