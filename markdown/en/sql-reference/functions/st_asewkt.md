Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ASEWKT

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
text (VARCHAR) representation of that value in [EWKT (extended well-known text)](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling)
format.

See also:
:   [ST\_ASWKT](/sql-reference/functions/st_aswkt)

## Syntax

Copy code

```
ST_ASEWKT( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

A VARCHAR.

## Usage notes

- For GEOGRAPHY objects, the SRID in the return value is always 4326. See the
  [note on EWKT handling](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling).
- To return the output in WKT format, use [ST\_ASWKT](/sql-reference/functions/st_aswkt) instead.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_ASEWKT function:

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
> select st_asewkt(g)
>     from geospatial_table
>     order by id;
> +-----------------------------------------------+
> | ST_ASEWKT(G)                                  |
> |-----------------------------------------------|
> | SRID=4326;POINT(-122.35 37.55)                |
> | SRID=4326;LINESTRING(-124.2 42,-120.01 41.99) |
> +-----------------------------------------------+
> ```

### GEOMETRY examples

The example below demonstrates how to use the ST\_ASEWKT function. The example returns the EWKT representations of two geometries
that have different SRIDs.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
> INSERT INTO geometry_table VALUES
>   ('SRID=4326;POINT(-122.35 37.55)'),
>   ('SRID=0;LINESTRING(0.75 0.75, -10 20)');
>
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';
> SELECT ST_ASEWKT(g) FROM geometry_table;
> ```
>
> Copy code
>
> ```
> +-------------------------------------+
> | ST_ASEWKT(G)                        |
> |-------------------------------------|
> | SRID=4326;POINT(-122.35 37.55)      |
> | SRID=0;LINESTRING(0.75 0.75,-10 20) |
> +-------------------------------------+
> ```
