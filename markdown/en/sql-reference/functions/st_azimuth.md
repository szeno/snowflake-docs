Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_AZIMUTH

Given a Point that represents the origin (the location of the observer) and a specified Point, returns the azimuth in radians.
Both Points must be either [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry)
objects.

The [azimuth](https://en.wikipedia.org/wiki/Azimuth) is the angle between the two Points when the observer at the origin is facing the north (for GEOGRAPHY objects) or
the Y-axis (for GEOMETRY objects). The angle is positive in the clockwise direction and is:

- 0 for a line segment pointing north.
- π/2 for a line segment pointing east.
- π for a line segment pointing south.
- 3π/2 for a line segment pointing west.

If the two Points are the same location, the function returns NULL.

For GEOGRAPHY objects, on spherical Earth,
[the formula described here](https://en.wikipedia.org/wiki/Azimuth#In_geodesy) is used to determine the azimuth.

Caution

Systems using an elliptical Earth model use
[a more complex algorithm for Azimuth](https://en.wikipedia.org/wiki/Azimuth#In_geodesy), which occasionally yields
significantly different results.

## Syntax

Copy code

```
ST_AZIMUTH( <geography_expression_for_origin> , <geography_expression_for_target> )
ST_AZIMUTH( <geometry_expression_for_origin> , <geometry_expression_for_target> )
```

## Arguments

`geography_expression_for_origin`
:   A GEOGRAPHY object that is a Point representing the origin (where the observer is located).

`geography_expression_for_target`
:   A GEOGRAPHY object that is a Point for which you want to calculate the azimuth.

`geometry_expression_for_origin`
:   A GEOMETRY object that is a Point representing the origin (where the observer is located).

`geometry_expression_for_target`
:   A GEOMETRY object that is a Point for which you want to calculate the azimuth.

## Returns

Returns a value of type REAL that is the azimuth in radians.

## Usage notes

- If one of the input geospatial objects is not a Point, the function reports an error.
- Returns NULL if one or both input points are NULL.

## Examples

### GEOGRAPHY examples

The following example returns the azimuth in radians for an origin Point (0, 1) and a target Point (0, 0):

> Copy code
>
> ```
> SELECT ST_AZIMUTH(
>     TO_GEOGRAPHY('POINT(0 1)'),
>     TO_GEOGRAPHY('POINT(0 0)')
> );
> +---------------------------------+
> |                     ST_AZIMUTH( |
> |     TO_GEOGRAPHY('POINT(0 1)'), |
> |      TO_GEOGRAPHY('POINT(0 0)') |
> |                               ) |
> |---------------------------------|
> |                     3.141592654 |
> +---------------------------------+
> ```

The following example returns the azimuth in degrees for an origin Point (0, 1) and a target Point (1, 2):

> Copy code
>
> ```
> SELECT DEGREES(ST_AZIMUTH(
>     TO_GEOGRAPHY('POINT(0 1)'),
>     TO_GEOGRAPHY('POINT(1 2)')
> ));
> +---------------------------------+
> |             DEGREES(ST_AZIMUTH( |
> |     TO_GEOGRAPHY('POINT(0 1)'), |
> |      TO_GEOGRAPHY('POINT(1 2)') |
> |                              )) |
> |---------------------------------|
> |                    44.978182941 |
> +---------------------------------+
> ```

### GEOMETRY examples

The following example returns the azimuth in radians for an origin Point (0, 1) and a target Point (0, 0):

Copy code

```
SELECT ST_AZIMUTH(
    TO_GEOMETRY('POINT(0 1)', TO_GEOMETRY('POINT(0 0)')
);

+------------------------------------------------------------------+
| ST_AZIMUTH(TO_GEOMETRY('POINT(0 1)'), TO_GEOMETRY('POINT(0 0)')) |
|------------------------------------------------------------------|
| 3.141592654                                                      |
+------------------------------------------------------------------+
```

The following example returns the azimuth in degrees for an origin Point (0, 1) and a target Point (0.707, 0.707):

Copy code

```
SELECT ST_AZIMUTH(
    TO_GEOMETRY('POINT(0 0)', TO_GEOMETRY(0.707 0.707')
);

+-------------------------------------------------------------------------+
| ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(0.707 0.707')) |
|-------------------------------------------------------------------------|
| 0.7853981634                                                            |
+-------------------------------------------------------------------------+
```
