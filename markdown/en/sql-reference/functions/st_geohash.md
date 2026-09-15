Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_GEOHASH

Returns the [geohash](https://en.wikipedia.org/wiki/Geohash) for a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography)
or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object. A geohash is a short base32 string that identifies a great circle
rectangle containing a location in the world.

The number of characters in a geohash determines precision. Removing characters
from the end of a geohash results in a geohash that is less precise and that identifies a
larger rectangular area.

ST\_GEOHASH returns a geohash that is 20 characters long.
The optional `precision` argument specifies the precision of the returned geohash.
For example, passing `5` for `precision` returns a shorter geohash (5 characters long) that is less precise.

Note

For a geospatial object that is not a point, the function might return a geohash of less precision, regardless of the default or
specified value for `precision`.

In these cases, precision is determined by the bounding box of the geospatial object. ST\_GEOHASH first determines the geohashes
of the lower left and upper right corners of the bounding box and then returns the prefix that is common to these two geohashes.

See also:
:   [ST\_GEOGFROMGEOHASH](/sql-reference/functions/st_geogfromgeohash), [ST\_GEOGPOINTFROMGEOHASH](/sql-reference/functions/st_geogpointfromgeohash)

## Syntax

Copy code

```
ST_GEOHASH( <geography_expression> [, <precision> ] )

ST_GEOHASH( <geometry_expression> [, <precision> ] )
```

## Arguments

**Required:**

`geography_expression`
:   The argument must be an expression of type GEOGRAPHY.

`geometry_expression`
:   The argument must be an expression of type GEOMETRY with the SRID 4326.

**Optional:**

`precision`
:   The number of characters to use in the geohash. You can specify a value from `1` to `20`.

    By default, `precision` is `20`, which produces a geohash that is 20 characters long.

## Returns

Returns the geohash (a value of type STRING) for the specified object.

If the object is a Polygon and the two points of the bounding box do not share the same geohash prefix, the function might return
an empty string.

## Examples

The following example returns the geohash for a GEOGRAPHY point:

Copy code

```
SELECT ST_GEOHASH(
  TO_GEOGRAPHY('POINT(-122.306100 37.554162)'))
  AS geohash_of_point_a;
```

```
+----------------------+
| GEOHASH_OF_POINT_A   |
|----------------------|
| 9q9j8ue2v71y5zzy0s4q |
+----------------------+
```

The following example returns a geohash for the same GEOGRAPHY point with less precision:

Copy code

```
SELECT ST_GEOHASH(
  TO_GEOGRAPHY('POINT(-122.306100 37.554162)'),
  5) AS less_precise_geohash_a;
```

```
+------------------------+
| LESS_PRECISE_GEOHASH_A |
|------------------------|
| 9q9j8                  |
+------------------------+
```

The following example returns the geohash for a GEOMETRY point:

Copy code

```
SELECT ST_GEOHASH(
  TO_GEOMETRY('POINT(-122.306100 37.554162)', 4326))
  AS geohash_of_point_a;
```

```
+----------------------+
| GEOHASH_OF_POINT_A   |
|----------------------|
| 9q9j8ue2v71y5zzy0s4q |
+----------------------+
```

The following example shows two geohashes that share the same prefix, which indicates that the two GEOGRAPHY points are near to each other.

Copy code

```
SELECT
  ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.306100 37.554162)'))
    AS geohash_of_point_a,
  ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.323111 37.562333)'))
    AS geohash_of_point_b;
```

```
+----------------------+----------------------+
| GEOHASH_OF_POINT_A   | GEOHASH_OF_POINT_B   |
|----------------------+----------------------|
| 9q9j8ue2v71y5zzy0s4q | 9q9j8qp02yms1tpjesmc |
+----------------------+----------------------+
```

Copy code

```
SELECT
  ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.306100 37.554162)'),
    5) AS less_precise_geohash_a,
  ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.323111 37.562333)'),
    5) AS less_precise_geohash_b;
```

```
+------------------------+------------------------+
| LESS_PRECISE_GEOHASH_A | LESS_PRECISE_GEOHASH_B |
|------------------------+------------------------|
| 9q9j8                  | 9q9j8                  |
+------------------------+------------------------+
```

The following example returns the geohash for a polygon. The lower left and upper right corners of the bounding box of this polygon
are the same two GEOGRAPHY points used in the previous examples. As shown in this example, ST\_GEOHASH returns the prefix common to the
geohashes of the lower left and upper right corners of the bounding box.

Copy code

```
SELECT
  ST_GEOHASH(
    TO_GEOGRAPHY(
      'POLYGON((-122.306100 37.554162, -122.306100 37.562333, -122.323111 37.562333, -122.323111 37.554162, -122.306100 37.554162))'
    )
  ) AS geohash_of_polygon;
```

```
+--------------------+
| GEOHASH_OF_POLYGON |
|--------------------|
| 9q9j8              |
+--------------------+
```
