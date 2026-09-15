Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# TO\_GEOGRAPHY

Parses an input and returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial).

See also:
:   [TRY\_TO\_GEOGRAPHY](/sql-reference/functions/try_to_geography) , [ST\_GEOGRAPHYFROMWKB](/sql-reference/functions/st_geographyfromwkb) , [ST\_GEOGRAPHYFROMWKT](/sql-reference/functions/st_geographyfromwkt)

## Syntax

Use one of the following:

Copy code

```
TO_GEOGRAPHY( <varchar_expression> [ , <allow_invalid> ] )

TO_GEOGRAPHY( <binary_expression> [ , <allow_invalid> ] )

TO_GEOGRAPHY( <variant_expression> [ , <allow_invalid> ] )

TO_GEOGRAPHY( <geometry_expression> [ , <allow_invalid> ] )
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

`geometry_expression`
:   The argument must be an expression of type GEOMETRY with the SRID 4326.

**Optional:**

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial).

## Usage notes

- Issues an error if the input cannot be parsed as one of the supported formats (WKT, WKB, EWKT, EWKB, GeoJSON).
- Issues an error if the input format is EWKT or EWKB and the SRID is not 4326.
  See the [note on EWKT and EWKB handling](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling).
- To construct a GEOGRAPHY object from WKT or EWKT input, you can also use [ST\_GEOGRAPHYFROMWKT](/sql-reference/functions/st_geographyfromwkt).
- To construct a GEOGRAPHY object from WKB or EWKB input, you can also use [ST\_GEOGRAPHYFROMWKB](/sql-reference/functions/st_geographyfromwkb).

- For the coordinates in WKT, EWKT, and GeoJSON, longitude appears before latitude (for example, `POINT(lon lat)`).

## Examples

This shows a simple use of the TO\_GEOGRAPHY function with VARCHAR data:

> Copy code
>
> ```
> select TO_GEOGRAPHY('POINT(-122.35 37.55)');
> ```
>
> ```
> +--------------------------------------+
> | TO_GEOGRAPHY('POINT(-122.35 37.55)') |
> |--------------------------------------|
> | POINT(-122.35 37.55)                 |
> +--------------------------------------+
> ```

The following example returns the GEOGRAPHY object for a geospatial object with a Z coordinate described in WKT format:

> Copy code
>
> ```
> select TO_GEOGRAPHY('POINTZ(-122.35 37.55 30)');
> ```
>
> ```
> +------------------------------------------+
> | TO_GEOGRAPHY('POINTZ(-122.35 37.55 30)') |
> |------------------------------------------|
> | POINTZ(-122.35 37.55 30)                 |
> +------------------------------------------+
> ```
