Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_AREA

Returns the area of the Polygon(s) in a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_AREA( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a REAL value, which represents the area:

- For GEOGRAPHY input values, the area is in square meters.
- For GEOMETRY input values, the area is computed with the same units used to define the input coordinates.

## Usage notes

- If `geography_expression` is not a Polygon, MultiPolygon, or GeometryCollection containing polygons, ST\_AREA returns 0.
- If `geography_expression` is a GeometryCollection, ST\_AREA returns the sum of the areas of the polygons in the collection.

## Examples

### GEOGRAPHY examples

This uses the ST\_AREA function with GEOGRAPHY objects to calculate the area of Earth’s surface 1 degree on each side with the
bottom of the area on the equator:

> Copy code
>
> ```
> SELECT ST_AREA(TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')) AS area;
> +------------------+
> |             AREA |
> |------------------|
> | 12364036567.0764 |
> +------------------+
> ```

### GEOMETRY examples

The following example calls the ST\_AREA function with GEOMETRY objects that represent a Point, LineString, and Polygon.

> Copy code
>
> ```
> SELECT ST_AREA(g), ST_ASWKT(g)
> FROM (SELECT TO_GEOMETRY(column1) as g
>   from values ('POINT(1 1)'),
>               ('LINESTRING(0 0, 1 1)'),
>               ('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'));
> ```
>
> Copy code
>
> ```
> +------------+--------------------------------+
> | ST_AREA(G) | ST_ASWKT(G)                    |
> |------------+--------------------------------|
> |          0 | POINT(1 1)                     |
> |          0 | LINESTRING(0 0,1 1)            |
> |          1 | POLYGON((0 0,0 1,1 1,1 0,0 0)) |
> +------------+--------------------------------+
> ```
