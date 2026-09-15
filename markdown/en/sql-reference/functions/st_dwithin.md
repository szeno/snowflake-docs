Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_DWITHIN

Returns TRUE if the minimum great circle distance between two points (two [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) objects) is
within the specified distance. Otherwise, returns FALSE.

If the parameters are GEOGRAPHY values that are not points (e.g. lines or polygons), this returns TRUE or FALSE based on the
minimum great circle distance between the two closest points of the two values.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Syntax

Copy code

```
ST_DWITHIN( <geography_expression_1> , <geography_expression_2> , <distance_in_meters> )
```

## Arguments

`geography_expression_1`
:   The argument must be an expression of type GEOGRAPHY.

`geography_expression_2`
:   The argument must be an expression of type GEOGRAPHY.

`distance_in_meters`
:   The argument must be an expression of type REAL. The distance is in meters.

## Returns

Returns a BOOLEAN.

## Usage notes

- Returns NULL if any input is NULL.

## Examples

This returns TRUE because the distance in meters between two points 1 degree apart along the equator is less than
150,000 meters:

> Copy code
>
> ```
> SELECT ST_DWITHIN (ST_MAKEPOINT(0, 0), ST_MAKEPOINT(1, 0), 150000);
> +-------------------------------------------------------------+
> | ST_DWITHIN (ST_MAKEPOINT(0, 0), ST_MAKEPOINT(1, 0), 150000) |
> |-------------------------------------------------------------|
> | True                                                        |
> +-------------------------------------------------------------+
> ```
