Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ASWKT , ST\_ASTEXT

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
text (VARCHAR) representation of that value in
[WKT (well-known text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format.

See also:
:   [ST\_ASEWKT](/sql-reference/functions/st_asewkt)

## Syntax

Use one of the following:

Copy code

```
ST_ASWKT( <geography_or_geometry_expression> )

ST_ASTEXT( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

A VARCHAR.

## Usage notes

- ST\_ASTEXT is an alias for ST\_ASWKT.
- To return the output in EWKT format, use [ST\_ASEWKT](/sql-reference/functions/st_asewkt) instead.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_ASWKT function:

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
> select st_astext(g)
>     from geospatial_table
>     order by id;
> +-------------------------------------+
> | ST_ASTEXT(G)                        |
> |-------------------------------------|
> | POINT(-122.35 37.55)                |
> | LINESTRING(-124.2 42,-120.01 41.99) |
> +-------------------------------------+
> ```
>
> Copy code
>
> ```
> select st_aswkt(g)
>     from geospatial_table
>     order by id;
> +-------------------------------------+
> | ST_ASWKT(G)                         |
> |-------------------------------------|
> | POINT(-122.35 37.55)                |
> | LINESTRING(-124.2 42,-120.01 41.99) |
> +-------------------------------------+
> ```

### GEOMETRY examples

The example below demonstrates how to use the ST\_ASEWKT function. The example returns the EWKT representations of two geometries.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
> INSERT INTO geometry_table VALUES
>   ('POINT(-122.35 37.55)'), ('LINESTRING(0.75 0.75, -10 20)');
>
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
> SELECT ST_ASWKT(g) FROM geometry_table;
> ```
>
> Copy code
>
> ```
> +------------------------------+
> | ST_ASWKT(G)                  |
> |------------------------------|
> | POINT(-122.35 37.55)         |
> | LINESTRING(0.75 0.75,-10 20) |
> +------------------------------+
> ```
