Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# ST\_GEOGPOINTFROMGEOHASH

Returns a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object for the Point that represents the center of a
[geohash](/sql-reference/functions/st_geohash).

See also:
:   [ST\_GEOHASH](/sql-reference/functions/st_geohash), [ST\_GEOGFROMGEOHASH](/sql-reference/functions/st_geogfromgeohash)

## Syntax

Copy code

```
ST_GEOGPOINTFROMGEOHASH( <geohash> )
```

## Arguments

`geohash`
:   The argument must be a geohash.

## Returns

The function returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) that represents the Point that is
the center of the geohash.

## Examples

The following example returns the GEOGRAPHY object for the Point at the center of a geohash:

> Copy code
>
> ```
> SELECT ST_GEOGPOINTFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
>     AS geography_center_point_of_geohash;
> +-----------------------------------+
> | GEOGRAPHY_CENTER_POINT_OF_GEOHASH |
> |-----------------------------------|
> | {                                 |
> |   "coordinates": [                |
> |     -1.223060999999999e+02,       |
> |     3.755416200000003e+01         |
> |   ],                              |
> |   "type": "Point"                 |
> | }                                 |
> +-----------------------------------+
> ```
