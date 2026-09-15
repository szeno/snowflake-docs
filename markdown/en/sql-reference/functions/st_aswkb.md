Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ASWKB , ST\_ASBINARY

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
binary representation of that value in
[WKB (well-known binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) format.

See also:
:   [ST\_ASEWKB](/sql-reference/functions/st_asewkb)

## Syntax

Use one of the following:

Copy code

```
ST_ASWKB( <geography_or_geometry_expression> )

ST_ASBINARY( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

A value of type BINARY.

## Usage notes

- ST\_ASBINARY is an alias for ST\_ASWKB.
- To return the output in EWKB format, use [ST\_ASEWKB](/sql-reference/functions/st_asewkb) instead.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_ASWKB function. For the WKB output, it is assumed that the [BINARY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-binary-output-format)
parameter is set to `HEX` (the default value for the parameter).

> Copy code
>
> ```
> create table geospatial_table (id INTEGER, g GEOGRAPHY);
> insert into geospatial_table values
>     (1, 'POINT(-122.35 37.55)'), (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');
> ```
>
> Copy code
>
> ```
> select st_aswkb(g)
>     from geospatial_table
>     order by id;
> +------------------------------------------------------------------------------------+
> | ST_ASWKB(G)                                                                        |
> |------------------------------------------------------------------------------------|
> | 01010000006666666666965EC06666666666C64240                                         |
> | 010200000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
> +------------------------------------------------------------------------------------+
> ```

### GEOMETRY examples

The example below demonstrates how to use the ST\_ASEWKB function. The example returns the EWKB representations of two geometries.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
> INSERT INTO geometry_table VALUES
>   ('POINT(-122.35 37.55)'), ('LINESTRING(0.75 0.75, -10 20)');
>
> SELECT ST_ASWKB(g) FROM geometry_table;
> ```
>
> Copy code
>
> ```
> +------------------------------------------------------------------------------------+
> | ST_ASWKB(G)                                                                        |
> |------------------------------------------------------------------------------------|
> | 01010000006666666666965EC06666666666C64240                                         |
> | 010200000002000000000000000000E83F000000000000E83F00000000000024C00000000000003440 |
> +------------------------------------------------------------------------------------+
> ```
