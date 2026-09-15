Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_LENGTH

Returns the great circle length of the LineString(s) in a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object or the Euclidean
length of the LineString(s) in a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_LENGTH( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a REAL value, which represents the length:

- For GEOGRAPHY input values, the length is in meters.
- For GEOMETRY input values, the length is computed with the same units used to define the input coordinates.

## Usage notes

- If `geography_or_geometry_expression` is not a LineString, MultiLineString, or GeometryCollection containing linestrings, ST\_LENGTH returns 0.
- If `geography_or_geometry_expression` is a GeometryCollection, ST\_LENGTH returns the sum of the lengths of the linestrings in the collection.
- If you want the perimeter length of a polygon, use the [ST\_PERIMETER](/sql-reference/functions/st_perimeter) function instead.

## Examples

### GEOGRAPHY examples

This shows the length in meters of one degree of arc at the equator:

> Copy code
>
> ```
> SELECT ST_LENGTH(TO_GEOGRAPHY('LINESTRING(0.0 0.0, 1.0 0.0)'));
> +---------------------------------------------------------+
> | ST_LENGTH(TO_GEOGRAPHY('LINESTRING(0.0 0.0, 1.0 0.0)')) |
> |---------------------------------------------------------|
> |                                        111195.101177484 |
> +---------------------------------------------------------+
> ```

### GEOMETRY examples

The following example demonstrates how to use the ST\_LENGTH function.

> Copy code
>
> ```
> SELECT ST_LENGTH(g), ST_ASWKT(g)
> FROM (SELECT TO_GEOMETRY(column1) AS g
>   FROM VALUES ('POINT(1 1)'),
>               ('LINESTRING(0 0, 1 1)'),
>               ('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'));
> ```
>
> Copy code
>
> ```
> +--------------+--------------------------------+
> | ST_LENGTH(G) | ST_ASWKT(G)                    |
> |--------------+--------------------------------|
> |  0           | POINT(1 1)                     |
> |  1.414213562 | LINESTRING(0 0,1 1)            |
> |  0           | POLYGON((0 0,0 1,1 1,1 0,0 0)) |
> +--------------+--------------------------------+
> ```
