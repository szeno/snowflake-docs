Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_GEOGRAPHY

Parses an input and returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial).

This function is identical to [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) except that it returns
NULL when TO\_GEOGRAPHY would return an error.

See also:
:   [TO\_GEOGRAPHY](/sql-reference/functions/to_geography)

## Syntax

Use one of the following:

Copy code

```
TRY_TO_GEOGRAPHY( <varchar_expression> [ , <allow_invalid> ] )

TRY_TO_GEOGRAPHY( <binary_expression> [ , <allow_invalid> ] )

TRY_TO_GEOGRAPHY( <variant_expression> [ , <allow_invalid> ] )
```

## Arguments

**Required:**

`varchar_expression`
:   The argument must be a string expression that represents a valid geometric object in one of the following formats:

    - WKT (well-known text).
    - WKB (well-known binary) in hexadecimal format (without a leading `0x`).
    - EWKT (extended well-known text).
    - EWKB (extended well-known binary) in hexadecimal format (without a leading `0x`).
    - GeoJSON.

`binary_expression`
:   The argument must be a binary expression in WKB or EWKB format.

`variant_expression`
:   The argument must be an OBJECT in GeoJSON format.

**Optional:**

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type GEOGRAPHY.

## Usage notes

- Returns NULL if the input cannot be parsed as the appropriate supported format (WKT, WKB, EWKT, EWKB, GeoJSON).
- Returns NULL if the input format is EWKT or EWKB and the SRID is not 4326.
  See the [note on EWKT and EWKB handling](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling).

- For the coordinates in WKT, EWKT, and GeoJSON, longitude appears before latitude (for example, `POINT(lon lat)`).

## Examples

This shows a simple use of the TRY\_TO\_GEOGRAPHY function with VARCHAR data:

> Copy code
>
> ```
> select TRY_TO_GEOGRAPHY('Not a valid input for this data type.');
> +-----------------------------------------------------------+
> | TRY_TO_GEOGRAPHY('NOT A VALID INPUT FOR THIS DATA TYPE.') |
> |-----------------------------------------------------------|
> | NULL                                                      |
> +-----------------------------------------------------------+
> ```
