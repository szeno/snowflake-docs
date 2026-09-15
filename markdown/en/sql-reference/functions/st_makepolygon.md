Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_MAKEPOLYGON , ST\_POLYGON

Constructs a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that represents
a Polygon without holes. The function uses the specified LineString as the outer loop.

This function corrects the orientation of the loop to prevent the creation of Polygons that span more than half of the globe. In
contrast, [ST\_MAKEPOLYGONORIENTED](/sql-reference/functions/st_makepolygonoriented) doesn’t attempt to correct the orientation of the loop.

See also:
:   [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) , [TO\_GEOMETRY](/sql-reference/functions/to_geometry) , [ST\_MAKEPOLYGONORIENTED](/sql-reference/functions/st_makepolygonoriented)

## Syntax

Copy code

```
ST_MAKEPOLYGON( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   A GEOGRAPHY or GEOMETRY object that represents a LineString in which the last point is the same as the first (i.e. a
    loop).

## Returns

The function returns a value of type GEOGRAPHY or GEOMETRY.

## Usage notes

- The lines of the Polygon must form a loop. In other words, the last Point in the sequence of Points defining the LineString
  must be the same Point as the first Point in the sequence.
- ST\_POLYGON is an alias for ST\_MAKEPOLYGON.

- For GEOMETRY objects, the returned GEOMETRY object has the same SRID as the input.

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_MAKEPOLYGON function. The sequence of points below defines a great circle
rectangular area 1 degree wide and 2 degrees high, with the lower left corner of the polygon starting at the
equator (latitude) and Greenwich (longitude). The last point in the sequence is the same as the first point,
which completes the loop.

> Copy code
>
> ```
> SELECT ST_MAKEPOLYGON(
>    TO_GEOGRAPHY('LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)')
>    ) AS polygon1;
> +--------------------------------+
> | POLYGON1                       |
> |--------------------------------|
> | POLYGON((0 0,1 0,1 2,0 2,0 0)) |
> +--------------------------------+
> ```

### GEOMETRY examples

This shows a simple use of the ST\_MAKEPOLYGON function.

> Copy code
>
> ```
> SELECT ST_MAKEPOLYGON(
>   TO_GEOMETRY('LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)')
>   ) AS polygon;
> ```
>
> Copy code
>
> ```
> +--------------------------------+
> | POLYGON                        |
> |--------------------------------|
> | POLYGON((0 0,1 0,1 2,0 2,0 0)) |
> +--------------------------------+
> ```
