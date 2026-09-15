Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ENVELOPE

Deprecated Feature

This function has been deprecated for GEOGRAPHY objects. The use of this function with GEOGRAPHY objects will be obsoleted in
a future release (TBD).

As an alternative, for GEOGRAPHY objects, use [ST\_XMIN](/sql-reference/functions/st_xmin), [ST\_XMAX](/sql-reference/functions/st_xmax), [ST\_YMIN](/sql-reference/functions/st_ymin), and [ST\_YMAX](/sql-reference/functions/st_ymax) to determine
the vertices of the bounding box around an input GEOGRAPHY object.

Returns the minimum bounding box (a rectangular “envelope”) that encloses a specified
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_ENVELOPE( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

## Returns

The function returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry)
that represents the minimum bounding box around the input object.

## Usage notes

- For GEOGRAPHY objects:

  - If `geography_expression` is a LineString that represents a meridian arc (an arc along a line of longitude),
    ST\_ENVELOPE returns that LineString.
  - If `geography_expression` is a LineString that represents an arc on a parallel (an arc along a line of latitude)
    other than the equator, ST\_ENVELOPE returns a Polygon that represents the bounding box for the arc.
  - If `geography_expression` is a single Point, ST\_ENVELOPE returns that Point.
- For GEOMETRY objects:

  - In degenerate cases (e.g. where the input is a point or a vertical or horizontal line), the function may return a geometry of
    lower dimension (i.e. a Point or LineString).

  - For GEOMETRY objects, the returned GEOMETRY object has the same SRID as the input.

## Examples

### GEOGRAPHY examples

The following example returns the minimum bounding box for a polygon:

> Copy code
>
> ```
> SELECT ST_ENVELOPE(
>     TO_GEOGRAPHY(
>         'POLYGON((-122.306067 37.55412, -122.32328 37.561801, -122.325879 37.586852, -122.306067 37.55412))'
>     )
> ) as minimum_bounding_box_around_polygon;
> +-----------------------------------------------------------------------------------------------------------------------+
> | MINIMUM_BOUNDING_BOX_AROUND_POLYGON                                                                                   |
> |-----------------------------------------------------------------------------------------------------------------------|
> | POLYGON((-122.325879 37.55412,-122.306067 37.55412,-122.306067 37.586852,-122.325879 37.586852,-122.325879 37.55412)) |
> +-----------------------------------------------------------------------------------------------------------------------+
> ```

The following example passes in a LineString that represents a meridian arc. The function returns the same LineString, rather
than a Polygon.

> Copy code
>
> ```
> SELECT ST_ENVELOPE(
>     TO_GEOGRAPHY(
>         'LINESTRING(-122.32328 37.561801, -122.32328 37.562001)'
>     )
> ) as minimum_bounding_box_around_meridian_arc;
> +-------------------------------------------------------+
> | MINIMUM_BOUNDING_BOX_AROUND_MERIDIAN_ARC              |
> |-------------------------------------------------------|
> | LINESTRING(-122.32328 37.561801,-122.32328 37.562001) |
> +-------------------------------------------------------+
> ```

The following example passes in a LineString that represents an arc on a parallel that is not the equator. The function
returns a Polygon that represents the bounding box:

> Copy code
>
> ```
> SELECT ST_ENVELOPE(
>     TO_GEOGRAPHY(
>         'LINESTRING(-122.32328 37.561801,-122.32351 37.561801)'
>     )
> ) as minimum_bounding_box_around_arc_along_parallel;
> +---------------------------------------------------------------------------------------------------------------------+
> | MINIMUM_BOUNDING_BOX_AROUND_ARC_ALONG_PARALLEL                                                                      |
> |---------------------------------------------------------------------------------------------------------------------|
> | POLYGON((-122.32351 37.561801,-122.32328 37.561801,-122.32328 37.561801,-122.32351 37.561801,-122.32351 37.561801)) |
> +---------------------------------------------------------------------------------------------------------------------+
> ```

The following example passes in a single Point. The function returns the same Point:

> Copy code
>
> ```
> SELECT ST_ENVELOPE(
>     TO_GEOGRAPHY(
>         'POINT(-122.32328 37.561801)'
>     )
> ) as minimum_bounding_box_around_point;
> +-----------------------------------+
> | MINIMUM_BOUNDING_BOX_AROUND_POINT |
> |-----------------------------------|
> | POINT(-122.32328 37.561801)       |
> +-----------------------------------+
> ```

### GEOMETRY examples
