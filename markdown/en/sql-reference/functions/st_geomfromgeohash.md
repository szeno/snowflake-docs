Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_GEOMFROMGEOHASH

Returns a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object for the polygon that represents the boundaries of a
[geohash](https://en.wikipedia.org/wiki/Geohash).

The number of characters in a geohash determines precision. Removing characters
from the end of a geohash results in a geohash that is less precise and that identifies a
larger rectangular area.

The optional `precision` argument specifies the precision to use for the input geohash. For example, passing `5`
for `precision` specifies that the function uses the first 5 characters of the input geohash.

See also:
:   [ST\_GEOHASH](/sql-reference/functions/st_geohash), [ST\_GEOMPOINTFROMGEOHASH](/sql-reference/functions/st_geompointfromgeohash)

## Syntax

Copy code

```
ST_GEOMFROMGEOHASH( <geohash> [, <precision> ] )
```

## Arguments

**Required:**

`geohash`
:   The argument must be a geohash.

**Optional:**

`precision`
:   The number of characters to use in the geohash. You can specify a value from `1` to `20`.

    By default, `precision` is `20`, which produces a geohash that is 20 characters long.

## Returns

Returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

## Examples

The following example returns the GEOMETRY object for a geohash:

Copy code

```
SELECT ST_GEOMFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
  AS geometry_from_geohash,
  ST_AREA(ST_GEOMFROMGEOHASH('9q9j8ue2v71y5zzy0s4q'))
  AS area_of_geohash;
```

```
+---------------------------------+-----------------+
| GEOMETRY_FROM_GEOHASH           | AREA_OF_GEOHASH |
|---------------------------------+-----------------|
| {                               | 5.492996255e-26 |
|   "coordinates": [              |                 |
|     [                           |                 |
|       [                         |                 |
|         -1.223061000000001e+02, |                 |
|         3.755416199999996e+01   |                 |
|       ],                        |                 |
|       [                         |                 |
|         -1.223061000000001e+02, |                 |
|         3.755416200000012e+01   |                 |
|       ],                        |                 |
|       [                         |                 |
|         -1.223060999999998e+02, |                 |
|         3.755416200000012e+01   |                 |
|       ],                        |                 |
|       [                         |                 |
|         -1.223060999999998e+02, |                 |
|         3.755416199999996e+01   |                 |
|       ],                        |                 |
|       [                         |                 |
|         -1.223061000000001e+02, |                 |
|         3.755416199999996e+01   |                 |
|       ]                         |                 |
|     ]                           |                 |
|   ],                            |                 |
|   "type": "Polygon"             |                 |
| }                               |                 |
+---------------------------------+-----------------+
```

The following example returns the GEOMETRY object for a less precise geohash. The function uses the first 6 characters from the input geohash:

Copy code

```
SELECT ST_GEOMFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6)
  AS geometry_from_less_precise_geohash,
  ST_AREA(ST_GEOMFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6))
  AS area_of_geohash;
```

```
+------------------------------------+-----------------+
| GEOMETRY_FROM_LESS_PRECISE_GEOHASH | AREA_OF_GEOHASH |
|------------------------------------+-----------------|
| {                                  | 6.034970284e-05 |
|   "coordinates": [                 |                 |
|     [                              |                 |
|       [                            |                 |
|         -1.223107910156250e+02,    |                 |
|         3.755126953125000e+01      |                 |
|       ],                           |                 |
|       [                            |                 |
|         -1.223107910156250e+02,    |                 |
|         3.755676269531250e+01      |                 |
|       ],                           |                 |
|       [                            |                 |
|         -1.222998046875000e+02,    |                 |
|         3.755676269531250e+01      |                 |
|       ],                           |                 |
|       [                            |                 |
|         -1.222998046875000e+02,    |                 |
|         3.755126953125000e+01      |                 |
|       ],                           |                 |
|       [                            |                 |
|         -1.223107910156250e+02,    |                 |
|         3.755126953125000e+01      |                 |
|       ]                            |                 |
|     ]                              |                 |
|   ],                               |                 |
|   "type": "Polygon"                |                 |
| }                                  |                 |
+------------------------------------+-----------------+
```
