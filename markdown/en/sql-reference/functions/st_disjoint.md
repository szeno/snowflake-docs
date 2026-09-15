Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_DISJOINT

Returns TRUE if the two [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) objects or the two
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) objects are disjoint (i.e. do not share any portion of space). ST\_DISJOINT is
equivalent to NOT [ST\_INTERSECTS(expr1, expr2)](/sql-reference/functions/st_intersects).

Note

This function does not support using a GeometryCollection or FeatureCollection as input values.

See also:
:   [ST\_INTERSECTS](/sql-reference/functions/st_intersects)

## Syntax

Copy code

```
ST_DISJOINT( <geography_expression_1> , <geography_expression_2> )

ST_DISJOINT( <geometry_expression_1> , <geometry_expression_2> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object.

`geography_expression_2`
:   A GEOGRAPHY object.

`geometry_expression_1`
:   A GEOMETRY object.

`geometry_expression_2`
:   A GEOMETRY object.

## Returns

BOOLEAN.

## Usage notes

- For GEOMETRY objects, the function reports an error if the two input GEOMETRY objects have different SRIDs.

## Examples

### GEOGRAPHY examples

The following examples use the ST\_DISJOINT function to determine if two geospatial objects are disjoint:

> Copy code
>
> ```
> -- These two polygons are disjoint and do not intersect.
> SELECT ST_DISJOINT(
>     TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
>     TO_GEOGRAPHY('POLYGON((3 3, 5 3, 5 5, 3 5, 3 3))')
>     );
> +---------------------------------------------------------+
> | ST_DISJOINT(                                            |
> |     TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'), |
> |     TO_GEOGRAPHY('POLYGON((3 3, 5 3, 5 5, 3 5, 3 3))')  |
> |     )                                                   |
> |---------------------------------------------------------|
> | True                                                    |
> +---------------------------------------------------------+
> ```
>
> Copy code
>
> ```
> -- These two polygons intersect and are not disjoint.
> SELECT ST_DISJOINT(
>     TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
>     TO_GEOGRAPHY('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))')
>     );
> +---------------------------------------------------------+
> | ST_DISJOINT(                                            |
> |     TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'), |
> |     TO_GEOGRAPHY('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))')  |
> |     )                                                   |
> |---------------------------------------------------------|
> | False                                                   |
> +---------------------------------------------------------+
> ```
