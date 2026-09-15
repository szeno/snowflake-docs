Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_COMPACT

Returns a compacted array with missing and null values removed, effectively converting sparse arrays into dense arrays.

## Syntax

Copy code

```
ARRAY_COMPACT( <array1> )
```

## Arguments

`array1`
:   The source array.

## Usage notes

- Semi-structured data (e.g. JSON data) can contain explicit null values, which are distinct from SQL NULLs. A null value in semi-structured data indicates a missing value.
- `array1` should be either an ARRAY data type or a VARIANT data type containing an array value.
- If the argument is NULL, the result will be NULL.
- When you pass a [structured array](/sql-reference/data-types-structured) to the function, the function returns a structured
  array of the same type.

## Examples

This example shows how to use `ARRAY_COMPACT()`:

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
> >     SELECT 2, ARRAY_CONSTRUCT(10, NULL, 30), ARRAY_CONSTRUCT(40);
> > ```
>
> Execute the query:
>
> > Copy code
> >
> > ```
> > SELECT array1, ARRAY_COMPACT(array1) FROM array_demo WHERE ID = 2;
> > +--------------+-----------------------+
> > | ARRAY1       | ARRAY_COMPACT(ARRAY1) |
> > |--------------+-----------------------|
> > | [            | [                     |
> > |   10,        |   10,                 |
> > |   undefined, |   30                  |
> > |   30         | ]                     |
> > | ]            |                       |
> > +--------------+-----------------------+
> > ```
