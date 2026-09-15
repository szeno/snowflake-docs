Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# TO\_OBJECT

Converts the input value to an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object):

- For a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value containing an OBJECT, returns the OBJECT.
- For NULL input, or for a VARIANT value containing only [JSON null](/user-guide/semistructured-considerations#label-variant-null), returns NULL.
- For an OBJECT, returns the OBJECT itself.
- For all other input values, reports an error.

## Syntax

Copy code

```
TO_OBJECT( <expr> )
```

## Arguments

`expr`
:   An expression that evaluates to a VARIANT that contains an OBJECT.

## Returns

The data type of the returned value is OBJECT.

## Examples

This demonstrates simple usage of the TO\_OBJECT function:

> Create a table and insert a value of type VARIANT. (The function [PARSE\_JSON](/sql-reference/functions/parse_json) returns a VARIANT.)
>
> > Copy code
> >
> > ```
> > CREATE TABLE t1 (vo VARIANT);
> > INSERT INTO t1 (vo) 
> >     SELECT PARSE_JSON('{"a":1}');
> > ```
>
> Call the TO\_OBJECT function:
>
> > Copy code
> >
> > ```
> > SELECT TO_OBJECT(vo) from t1;
> > +---------------+
> > | TO_OBJECT(VO) |
> > |---------------|
> > | {             |
> > |   "a": 1      |
> > | }             |
> > +---------------+
> > ```
