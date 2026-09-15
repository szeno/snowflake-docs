Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_HAUSDORFFDISTANCE

Returns the discrete [Hausdorff distance](https://en.wikipedia.org/wiki/Hausdorff_distance) between two
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) objects.

The Hausdorff distance indicates how similar the two objects are. Two objects are considered to be similar if each point in
one object is close to a point in the other object. The Hausdorff distance is the greatest distance between a point in one
object and a point in the other object.

ST\_HAUSDORFFDISTANCE returns the discrete Hausdorff distance, which is calculated by comparing only the vertices (discrete
points) and not arbitrary points along the edge.

## Syntax

Copy code

```
ST_HAUSDORFFDISTANCE( <geography_expression_1> , <geography_expression_2> )
```

## Arguments

`geography_expression_1`
:   The argument must be an expression of type GEOGRAPHY.

`geography_expression_2`
:   The argument must be an expression of type GEOGRAPHY.

## Returns

Returns a value of type REAL that represents the discrete Hausdorff distance in degrees.

## Usage notes

- Returns NULL if one or more input points are NULL.

## Examples

This example returns the Hausdorff distance between two points (point `0 0` and point `0 1`):

> Copy code
>
> ```
> SELECT ST_HAUSDORFFDISTANCE(ST_POINT(0, 0), ST_POINT(0, 1));
> +------------------------------------------------------+
> | ST_HAUSDORFFDISTANCE(ST_POINT(0, 0), ST_POINT(0, 1)) |
> |------------------------------------------------------|
> |                                                    1 |
> +------------------------------------------------------+
> ```

The next example compares three Polygons (`a`, `b`, and `c`).

The distance between the farthest points in `a` and `c` (point `0 1` and point `0 3`) is greater than the distance
between the farthest points in `a` and `b` (point `1 0` and point `2 0`).

As a result, the value returned by ST\_HAUSDORFFDISTANCE is smaller for `a` and `c`. This indicates that `a` and `c`
are more similar than `a` and `b`.

> Copy code
>
> ```
> WITH
>     a AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 1, 1 0, 0 -1, -1 0))')),
>     b AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 1, 2 0, 0 -1, -1 0))')),
>     c AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 3, 1 0, 0 -1, -1 0))'))
> SELECT
>     ST_HAUSDORFFDISTANCE(a, b) as distance_between_a_and_b,
>     ST_HAUSDORFFDISTANCE(a, c) as distance_between_a_and_c;
> +--------------------------+--------------------------+
> | DISTANCE_BETWEEN_A_AND_B | DISTANCE_BETWEEN_A_AND_C |
> |--------------------------+--------------------------|
> |                        1 |                        2 |
> +--------------------------+--------------------------+
> ```
