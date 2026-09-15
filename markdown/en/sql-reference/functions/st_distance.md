Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_DISTANCE

Returns the minimum great circle distance between two [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or the minimum Euclidean distance
between two [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) objects.

## Syntax

Copy code

```
ST_DISTANCE( <geography_or_geometry_expression_1> , <geography_or_geometry_expression_2> )
```

## Arguments

`geography_or_geometry_expression_1`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

`geography_or_geometry_expression_2`
:   The argument must be of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a FLOAT value, which represents the distance, or NULL:

- For GEOGRAPHY input values, the distance is in meters.
- For GEOMETRY input values, the distance is computed with the same units used to define the input coordinates.
- Returns NULL if one or more input points are NULL.

## Usage notes

- For GEOMETRY objects, the function reports an error if the two input GEOMETRY objects have different SRIDs.

## Examples

The following examples use the ST\_DISTANCE function.

### GEOGRAPHY examples

Show the distance in meters between two points 1 degree apart along the equator (approximately 111 kilometers or
69 miles).

Copy code

```
WITH d AS
  ( ST_DISTANCE(ST_MAKEPOINT(0, 0), ST_MAKEPOINT(1, 0)) )
SELECT d / 1000 AS kilometers, d / 1609 AS miles;
```

```
+---------------+--------------+
|    KILOMETERS |        MILES |
|---------------+--------------|
| 111.195101177 | 69.108204585 |
+---------------+--------------+
```

Show the output of the ST\_DISTANCE function when one or more input values are NULL:

Copy code

```
SELECT ST_DISTANCE(ST_MAKEPOINT(0, 0), ST_MAKEPOINT(NULL, NULL)) AS null_input;
```

```
+------------+
| NULL_INPUT |
|------------|
|       NULL |
+------------+
```

### GEOMETRY examples

The following example compares the distance calculated for GEOGRAPHY and GEOMETRY input objects.

Copy code

```
SELECT ST_DISTANCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')) AS geometry_distance,
  ST_DISTANCE(TO_GEOGRAPHY('POINT(0 0)'), TO_GEOGRAPHY('POINT(1 1)')) AS geography_distance;
```

```
+-------------------+--------------------+
| GEOMETRY_DISTANCE | GEOGRAPHY_DISTANCE |
|-------------------+--------------------|
|       1.414213562 |   157249.628092508 |
+-------------------+--------------------+
```

For additional examples, see [Examples comparing the GEOGRAPHY and GEOMETRY data types](/sql-reference/data-types-geospatial#label-geometry-geography-diffs-examples).
