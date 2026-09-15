Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# BIT\_LENGTH

Returns the length of a string or binary value in bits.

Snowflake doesn’t use fractional bytes so length is always calculated as 8 \* [OCTET\_LENGTH](/sql-reference/functions/octet_length).

## Syntax

Copy code

```
BIT_LENGTH(<string_or_binary>)
```

## Arguments

`string_or_binary`
:   The string or binary value for which the length is returned.

## Examples

This shows use of the `BIT_LENGTH` function on both string and BINARY values:

> > Copy code
> >
> > ```
> > CREATE TABLE bl (v VARCHAR, b BINARY);
> > INSERT INTO bl (v, b) VALUES 
> >    ('abc', NULL),
> >    ('\u0394', X'A1B2');
> > ```
>
> Query the data:
>
> > Copy code
> >
> > ```
> > SELECT v, b, BIT_LENGTH(v), BIT_LENGTH(b) FROM bl ORDER BY v;
> > +-----+------+---------------+---------------+
> > | V   | B    | BIT_LENGTH(V) | BIT_LENGTH(B) |
> > |-----+------+---------------+---------------|
> > | abc | NULL |            24 |          NULL |
> > | Δ   | A1B2 |            16 |            16 |
> > +-----+------+---------------+---------------+
> > ```
