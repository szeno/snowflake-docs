Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_YMIN

Returns the minimum latitude (Y coordinate) of all points contained in the specified
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_YMIN( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a REAL value.

## Usage notes

- The function takes into account the curvature of the edges toward the poles.

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_XMIN, ST\_XMAX, ST\_YMIN, and ST\_YMAX functions:

> Copy code
>
> ```
> CREATE or replace TABLE extreme_point_collection (id INTEGER, g GEOGRAPHY);
> INSERT INTO extreme_point_collection (id, g)
>     SELECT column1, TO_GEOGRAPHY(column2) FROM VALUES
>         (1, 'POINT(-180 0)'),
>         (2, 'POINT(180 0)'),
>         (3, 'LINESTRING(-179 0, 179 0)'),
>         (4, 'LINESTRING(-60 30, 60 30)'),
>         (5, 'LINESTRING(-60 -30, 60 -30)');
> ```
>
> Copy code
>
> ```
> SELECT
>     g,
>     ST_XMIN(g),
>     ST_XMAX(g),
>     ST_YMIN(g),
>     ST_YMAX(g)
>   FROM extreme_point_collection
>   ORDER BY id;
> +----------------------------+------------+------------+-------------------+-------------------+
> | G                          | ST_XMIN(G) | ST_XMAX(G) |        ST_YMIN(G) |        ST_YMAX(G) |
> |----------------------------+------------+------------+-------------------+-------------------|
> | POINT(-180 0)              |       -180 |        180 |   0               |   0               |
> | POINT(180 0)               |       -180 |        180 |   0               |   0               |
> | LINESTRING(-179 0,179 0)   |       -180 |        180 |  -6.883275617e-14 |   6.883275617e-14 |
> | LINESTRING(-60 30,60 30)   |        -60 |         60 |  30               |  49.106605351     |
> | LINESTRING(-60 -30,60 -30) |        -60 |         60 | -49.106605351     | -30               |
> +----------------------------+------------+------------+-------------------+-------------------+
> ```
