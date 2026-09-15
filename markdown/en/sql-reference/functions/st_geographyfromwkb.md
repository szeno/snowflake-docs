Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# ST\_GEOGRAPHYFROMWKB

Parses a
[WKB (well-known binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) or
[EWKB (extended well-known binary)](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling) input and returns a value of type
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography).

Aliases:
:   ST\_GEOGFROMWKB , ST\_GEOGRAPHYFROMEWKB , ST\_GEOGFROMEWKB

See also:
:   [TO\_GEOGRAPHY](/sql-reference/functions/to_geography)

## Syntax

Copy code

```
ST_GEOGRAPHYFROMWKB( <varchar_or_binary_expression> [ , <allow_invalid> ] )

ST_GEOGFROMWKB( <varchar_or_binary_expression> [ , <allow_invalid> ] )

ST_GEOGRAPHYFROMEWKB( <varchar_or_binary_expression> [ , <allow_invalid> ] )

ST_GEOGFROMEWKB( <varchar_or_binary_expression> [ , <allow_invalid> ] )
```

## Arguments

**Required:**

`varchar_or_binary_expression`
:   The argument must be a string or binary expression in WKB or EWKB that represents a valid geospatial object.

    A string expression must be in hexadecimal format (without a leading `0x`).

**Optional:**

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography).

## Usage notes

- Issues an error if the input cannot be parsed as WKB or EWKB.
- Issues an error if the input format is EWKB and the SRID is not 4326.
  See the [note on EWKT and EWKB handling](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling).

## Examples

The following example returns the GEOGRAPHY object for a geospatial object described in WKT format:

> Copy code
>
> ```
> -- Set the output format to WKT
> alter session set GEOGRAPHY_OUTPUT_FORMAT='WKT';
> ```
>
> Copy code
>
> ```
> select ST_GEOGRAPHYFROMWKB('01010000006666666666965EC06666666666C64240');
> +-------------------------------------------------------------------+
> | ST_GEOGRAPHYFROMWKB('01010000006666666666965EC06666666666C64240') |
> |-------------------------------------------------------------------|
> | POINT(-122.35 37.55)                                              |
> +-------------------------------------------------------------------+
> ```

The following example returns the GEOGRAPHY object for a geospatial object described in EWKT format:

> Copy code
>
> ```
> -- Set the output format to EWKT
> alter session set GEOGRAPHY_OUTPUT_FORMAT='EWKT';
> ```
>
> Copy code
>
> ```
> select ST_GEOGRAPHYFROMEWKB('0101000020E61000006666666666965EC06666666666C64240');
> +----------------------------------------------------------------------------+
> | ST_GEOGRAPHYFROMEWKB('0101000020E61000006666666666965EC06666666666C64240') |
> |----------------------------------------------------------------------------|
> | SRID=4326;POINT(-122.35 37.55)                                             |
> +----------------------------------------------------------------------------+
> ```
