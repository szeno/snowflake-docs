Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# ST\_GEOGFROMGEOHASH

Returns a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object for the polygon that represents the boundaries of a
[geohash](/sql-reference/functions/st_geohash).

The optional `precision` argument specifies the precision to use for the input geohash.
For example, passing `5` for `precision` specifies that the function should use the first 5 characters of the input geohash.

See also:
:   [ST\_GEOHASH](/sql-reference/functions/st_geohash), [ST\_GEOGPOINTFROMGEOHASH](/sql-reference/functions/st_geogpointfromgeohash)

## Syntax

Copy code

```
ST_GEOGFROMGEOHASH( <geohash> [, <precision> ] )
```

## Arguments

**Required:**

`geohash`
:   The argument must be a geohash.

**Optional:**

`precision`
:   The number of characters to use from the input geohash. For example, passing `5` for `precision` causes
    the function to use the first 5 characters in the geohash.

    You can specify a value from `1` to `20`.

    By default, `precision` is `20`, which causes the function to use up to the first 20 characters of the geohash.

## Returns

The function returns a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography).

## Examples

The following example returns the GEOGRAPHY object for a geohash:

> Copy code
>
> ```
> SELECT ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
>     AS geography_from_geohash,
>     ST_AREA(ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q'))
>     AS area_of_geohash;
> +---------------------------------+-----------------+
> | GEOGRAPHY_FROM_GEOHASH          | AREA_OF_GEOHASH |
> |---------------------------------+-----------------|
> | {                               |  5.48668572e-16 |
> |   "coordinates": [              |                 |
> |     [                           |                 |
> |       [                         |                 |
> |         -1.223061000000001e+02, |                 |
> |         3.755416199999996e+01   |                 |
> |       ],                        |                 |
> |       [                         |                 |
> |         -1.223061000000001e+02, |                 |
> |         3.755416200000012e+01   |                 |
> |       ],                        |                 |
> |       [                         |                 |
> |         -1.223060999999998e+02, |                 |
> |         3.755416200000012e+01   |                 |
> |       ],                        |                 |
> |       [                         |                 |
> |         -1.223060999999998e+02, |                 |
> |         3.755416199999996e+01   |                 |
> |       ],                        |                 |
> |       [                         |                 |
> |         -1.223061000000001e+02, |                 |
> |         3.755416199999996e+01   |                 |
> |       ]                         |                 |
> |     ]                           |                 |
> |   ],                            |                 |
> |   "type": "Polygon"             |                 |
> | }                               |                 |
> +---------------------------------+-----------------+
> ```

The following example returns the GEOGRAPHY object for a less precise geohash. The function uses the first 6 characters from the input geohash:

> Copy code
>
> ```
> SELECT ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6)
>     AS geography_from_less_precise_geohash,
>     ST_AREA(ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6))
>     AS area_of_geohash;
> +-------------------------------------+-----------------+
> | GEOGRAPHY_FROM_LESS_PRECISE_GEOHASH | AREA_OF_GEOHASH |
> |-------------------------------------+-----------------|
> | {                                   | 591559.75661851 |
> |   "coordinates": [                  |                 |
> |     [                               |                 |
> |       [                             |                 |
> |         -1.223107910156250e+02,     |                 |
> |         3.755126953125000e+01       |                 |
> |       ],                            |                 |
> |       [                             |                 |
> |         -1.223107910156250e+02,     |                 |
> |         3.755676269531250e+01       |                 |
> |       ],                            |                 |
> |       [                             |                 |
> |         -1.222998046875000e+02,     |                 |
> |         3.755676269531250e+01       |                 |
> |       ],                            |                 |
> |       [                             |                 |
> |         -1.222998046875000e+02,     |                 |
> |         3.755126953125000e+01       |                 |
> |       ],                            |                 |
> |       [                             |                 |
> |         -1.223107910156250e+02,     |                 |
> |         3.755126953125000e+01       |                 |
> |       ]                             |                 |
> |     ]                               |                 |
> |   ],                                |                 |
> |   "type": "Polygon"                 |                 |
> | }                                   |                 |
> +-------------------------------------+-----------------+
> ```
