Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# ST\_GEOMETRYFROMWKB

Parses a
[WKB (well-known binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) or EWKB
(extended well-known binary) input and returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

Aliases:
:   ST\_GEOMFROMWKB , ST\_GEOMETRYFROMEWKB , ST\_GEOMFROMEWKB

See also:
:   [TO\_GEOMETRY](/sql-reference/functions/to_geometry)

## Syntax

Copy code

```
ST_GEOMETRYFROMWKB( <varchar_or_binary_expression> [ , <srid> ]  [ , <allow_invalid> ] )

ST_GEOMFROMWKB( <varchar_or_binary_expression> [ , <srid> ]  [ , <allow_invalid> ] )

ST_GEOMETRYFROMEWKB( <varchar_or_binary_expression> [ , <srid> ] [ , <allow_invalid> ] )

ST_GEOMFROMEWKB( <varchar_or_binary_expression> [ , <srid> ] [ , <allow_invalid> ] )
```

## Arguments

**Required:**

`varchar_or_binary_expression`
:   The argument must be a string or binary expression in WKB or EWKB that represents a valid geospatial object.

    A string expression must be in hexadecimal format (without a leading `0x`).

**Optional:**

`srid`
:   The integer value of the SRID to use.

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

## Usage notes

- Issues an error if the input cannot be parsed as WKB or EWKB.
- For WKB input, if the `srid` argument is not specified, the resulting GEOMETRY object has the SRID set to 0.

## Examples

The following example returns the GEOMETRY object for a geospatial object described in EWKB format:

> Copy code
>
> ```
> -- Set the geometry output format to EWKT
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';
>
> SELECT ST_GEOMETRYFROMEWKB('0101000020797F000066666666A9CB17411F85EBC19E325641');
> ```
>
> Copy code
>
> ```
> +---------------------------------------------------------------------------+
> | ST_GEOMETRYFROMEWKB('0101000020797F000066666666A9CB17411F85EBC19E325641') |
> |---------------------------------------------------------------------------|
> | SRID=32633;POINT(389866.35 5819003.03)                                    |
> +---------------------------------------------------------------------------+
> ```

In the next example, the input is in WKB format, which does not specify the SRID:

> Copy code
>
> ```
> -- Set the geometry output format to EWKT
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';
>
> SELECT ST_GEOMETRYFROMEWKB('010100000066666666A9CB17411F85EBC19E325641');
> ```
>
> Copy code
>
> ```
> +-------------------------------------------------------------------+
> | ST_GEOMETRYFROMEWKB('010100000066666666A9CB17411F85EBC19E325641') |
> |-------------------------------------------------------------------|
> | SRID=0;POINT(389866.35 5819003.03)                                |
> +-------------------------------------------------------------------+
> ```
