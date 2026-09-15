Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_NPOINTS , ST\_NUMPOINTS

Returns the number of points in a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography)
object.

## Syntax

Copy code

```
ST_NPOINTS( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a value of type INTEGER.

## Usage notes

- Each Polygon loop lists the starting point twice (once as the start, once as the end). ST\_NPOINTS
  counts both occurrences. For example, given a triangular Polygon, ST\_NPOINTS returns 4, not 3.
- ST\_NUMPOINTS is an alias for ST\_NPOINTS.

  Note

  In some other systems, ST\_NUMPOINTS behaves differently from ST\_NPOINTS and returns the number of points for
  LineString / MultiLineString objects only.

## Examples

### GEOGRAPHY examples

This shows the number of points in a simple Polygon.

> Copy code
>
> ```
> create table geospatial_table_01 (g1 GEOGRAPHY, g2 GEOGRAPHY);
> insert into geospatial_table_01 (g1, g2) values 
>     ('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))', 'POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))');
> ```
>
> Copy code
>
> ```
> SELECT ST_NPOINTS(g1) 
>     FROM geospatial_table_01;
> +----------------+
> | ST_NPOINTS(G1) |
> |----------------|
> |              5 |
> +----------------+
> ```

### GEOMETRY examples

The following example demonstrates how to use the ST\_NPOINTS function.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_shapes (g GEOMETRY);
> INSERT INTO geometry_shapes VALUES
>     ('POINT(66 12)'),
>     ('MULTIPOINT((45 21), (12 54))'),
>     ('LINESTRING(40 60, 50 50, 60 40)'),
>     ('MULTILINESTRING((1 1, 32 17), (33 12, 73 49, 87.1 6.1))'),
>     ('POLYGON((17 17, 17 30, 30 30, 30 17, 17 17))'),
>     ('MULTIPOLYGON(((-10 0,0 10,10 0,-10 0)),((-10 40,10 40,0 20,-10 40)))'),
>     ('GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60, 50 50, 60 40), POINT(99 11))')
>     ;
>
> SELECT ST_NPOINTS(g), ST_ASWKT(g) FROM geometry_shapes;
> ```
>
> Copy code
>
> ```
> +---------------+-------------------------------------------------------------------------------------------------+
> | ST_NPOINTS(G) | ST_ASWKT(G)                                                                                     |
> |---------------+-------------------------------------------------------------------------------------------------|
> |             1 | POINT(66 12)                                                                                    |
> |             2 | MULTIPOINT((45 21),(12 54))                                                                     |
> |             3 | LINESTRING(40 60,50 50,60 40)                                                                   |
> |             5 | MULTILINESTRING((1 1,32 17),(33 12,73 49,87.1 6.1))                                             |
> |             5 | POLYGON((17 17,17 30,30 30,30 17,17 17))                                                        |
> |             8 | MULTIPOLYGON(((-10 0,0 10,10 0,-10 0)),((-10 40,10 40,0 20,-10 40)))                            |
> |             8 | GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60,50 50,60 40),POINT(99 11)) |
> +---------------+-------------------------------------------------------------------------------------------------+
> ```
