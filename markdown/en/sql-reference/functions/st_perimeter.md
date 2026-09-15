Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_PERIMETER

Returns the length of the perimeter of the polygon(s) in a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_PERIMETER( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a REAL value, which represents the length:

- For GEOGRAPHY objects, the length is in meters.
- For GEOMETRY objects, the length is computed with the same unit used to define the coordinates.

## Usage notes

- If `geography_or_geometry_expression` is not a Polygon, MultiPolygon, or GeometryCollection containing Polygons, ST\_PERIMETER returns 0.
- If `geography_or_geometry_expression` is a GeometryCollection, ST\_PERIMETER returns the sum of the perimeters of the Polygons in the collection.
- Use this function (rather than ST\_LENGTH) to get the perimeter of a Polygon.

## Examples

### GEOGRAPHY examples

This calculates the length of the perimeter of a polygon that is one degree of arc on each edge and has one
edge on the equator:

> Copy code
>
> ```
> SELECT ST_PERIMETER(TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));
> +------------------------------------------------------------------+
> | ST_PERIMETER(TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')) |
> |------------------------------------------------------------------|
> |                                                 444763.468727621 |
> +------------------------------------------------------------------+
> ```

### GEOMETRY examples

The following example demonstrates how to use the ST\_PERIMETER function.

> Copy code
>
> ```
> SELECT ST_PERIMETER(g), ST_ASWKT(g)
> FROM (SELECT TO_GEOMETRY(column1) AS g
>   FROM VALUES ('POINT(1 1)'),
>               ('LINESTRING(0 0, 1 1)'),
>               ('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'));
> ```
>
> Copy code
>
> ```
> +-----------------+--------------------------------+
> | ST_PERIMETER(G) | ST_ASWKT(G)                    |
> |-----------------+--------------------------------|
> |               0 | POINT(1 1)                     |
> |               0 | LINESTRING(0 0,1 1)            |
> |               4 | POLYGON((0 0,0 1,1 1,1 0,0 0)) |
> +-----------------+--------------------------------+
> ```
