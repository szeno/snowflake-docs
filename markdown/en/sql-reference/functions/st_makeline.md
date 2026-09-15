Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_MAKELINE

Constructs a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that represents
a line connecting the points in the input objects.

See also:
:   [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) , [TO\_GEOMETRY](/sql-reference/functions/to_geometry)

## Syntax

Copy code

```
ST_MAKELINE( <geography_expression_1> , <geography_expression_2> )

ST_MAKELINE( <geometry_expression_1> , <geometry_expression_2> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object containing the points to connect. This object must be a Point, MultiPoint, or LineString.

`geography_expression_2`
:   A GEOGRAPHY object containing the points to connect. This object must be a Point, MultiPoint, or LineString.

`geometry_expression_1`
:   A GEOMETRY object containing the points to connect. This object must be a Point, MultiPoint, or LineString.

`geometry_expression_2`
:   A GEOMETRY object containing the points to connect. This object must be a Point, MultiPoint, or LineString.

## Returns

The function returns a value of type GEOGRAPHY or GEOMETRY. The value is a LineString that connects all of the points specified by
the input GEOGRAPHY or GEOMETRY objects.

## Usage notes

- If an input GEOGRAPHY object contains multiple points, ST\_MAKELINE connects all of the points specified in the object.
- ST\_MAKELINE connects the points in the order in which they are specified in the input.

- For GEOMETRY objects, the function reports an error if the two input GEOMETRY objects have different SRIDs.

- For GEOMETRY objects, the returned GEOMETRY object has the same SRID as the input.

## Examples

### GEOGRAPHY examples

The examples in this section display output in WKT format:

> Copy code
>
> ```
> alter session set GEOGRAPHY_OUTPUT_FORMAT='WKT';
> ```

The following example uses ST\_MAKELINE to construct a LineString that connects two Points:

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>                    TO_GEOGRAPHY('POINT(37.0 45.0)'),
>                    TO_GEOGRAPHY('POINT(38.5 46.5)')
>                   ) AS line_between_two_points;
> +-----------------------------+
> | LINE_BETWEEN_TWO_POINTS     |
> |-----------------------------|
> | LINESTRING(37 45,38.5 46.5) |
> +-----------------------------+
> ```

The following example constructs a LineString that connects a Point with the points in a MultiPoint:

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>                    TO_GEOGRAPHY('POINT(-122.306067 37.55412)'),
>                    TO_GEOGRAPHY('MULTIPOINT((-122.32328 37.561801), (-122.325879 37.586852))')
>                   ) AS line_between_point_and_multipoint;
> +-----------------------------------------------------------------------------+
> | LINE_BETWEEN_POINT_AND_MULTIPOINT                                           |
> |-----------------------------------------------------------------------------|
> | LINESTRING(-122.306067 37.55412,-122.32328 37.561801,-122.325879 37.586852) |
> +-----------------------------------------------------------------------------+
> ```

As demonstrated by the output of the example, ST\_MAKELINE connects the points in the order in which they are specified in the input.

The following example constructs a LineString that connects the points in a MultiPoint with another LineString:

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>                    TO_GEOGRAPHY('MULTIPOINT((-122.32328 37.561801), (-122.325879 37.586852))'),
>                    TO_GEOGRAPHY('LINESTRING(-122.306067 37.55412, -122.496691 37.495627)')
>                   ) AS line_between_multipoint_and_linestring;
> +---------------------------------------------------------------------------------------------------+
> | LINE_BETWEEN_MULTIPOINT_AND_LINESTRING                                                            |
> |---------------------------------------------------------------------------------------------------|
> | LINESTRING(-122.32328 37.561801,-122.325879 37.586852,-122.306067 37.55412,-122.496691 37.495627) |
> +---------------------------------------------------------------------------------------------------+
> ```

### GEOMETRY examples

The examples in this section display output in WKT format:

> Copy code
>
> ```
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
> ```

The first example constructs a line between two Points:

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>   TO_GEOMETRY('POINT(1.0 2.0)'),
>   TO_GEOMETRY('POINT(3.5 4.5)')) AS line_between_two_points;
> ```
>
> Copy code
>
> ```
> +-------------------------+
> | LINE_BETWEEN_TWO_POINTS |
> |-------------------------|
> | LINESTRING(1 2,3.5 4.5) |
> +-------------------------+
> ```

The next example demonstrates creating a LineString that connects points in a MultiPoint with a Point

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>   TO_GEOMETRY('POINT(1.0 2.0)'),
>   TO_GEOMETRY('MULTIPOINT(3.5 4.5, 6.1 7.9)')) AS line_from_point_and_multipoint;
> ```
>
> Copy code
>
> ```
> +---------------------------------+
> | LINE_FROM_POINT_AND_MULTIPOINT  |
> |---------------------------------|
> | LINESTRING(1 2,3.5 4.5,6.1 7.9) |
> +---------------------------------+
> ```

The following example constructs a LineString that connects the points in a MultiPoint with another LineString:

> Copy code
>
> ```
> SELECT ST_MAKELINE(
>   TO_GEOMETRY('LINESTRING(1.0 2.0, 10.1 5.5)'),
>   TO_GEOMETRY('MULTIPOINT(3.5 4.5, 6.1 7.9)')) AS line_from_linestring_and_multipoint;
> ```
>
> Copy code
>
> ```
> +------------------------------------------+
> | LINE_FROM_LINESTRING_AND_MULTIPOINT      |
> |------------------------------------------|
> | LINESTRING(1 2,10.1 5.5,3.5 4.5,6.1 7.9) |
> +------------------------------------------+
> ```
