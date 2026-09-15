Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_GEOMPOINTFROMGEOHASH

Returns a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object for the point that represents center of a
[geohash](https://en.wikipedia.org/wiki/Geohash).

See also:
:   [ST\_GEOHASH](/sql-reference/functions/st_geohash), [ST\_GEOMFROMGEOHASH](/sql-reference/functions/st_geomfromgeohash)

## Syntax

Copy code

```
ST_GEOMPOINTFROMGEOHASH( <geohash> )
```

## Arguments

`geohash`
:   The argument must be a geohash.

## Returns

Returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) that represents the point that is the
center of the geohash.

## Examples

The following example returns the GEOMETRY object for the point at the center of a geohash:

Copy code

```
SELECT ST_GEOMPOINTFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
  AS geometry_center_point_of_geohash;
```

```
+----------------------------------+
| GEOMETRY_CENTER_POINT_OF_GEOHASH |
|----------------------------------|
| {                                |
|   "coordinates": [               |
|     -1.223061000000001e+02,      |
|     3.755416199999996e+01        |
|   ],                             |
|   "type": "Point"                |
| }                                |
+----------------------------------+
```
