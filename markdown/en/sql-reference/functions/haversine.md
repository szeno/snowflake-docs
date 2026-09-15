Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# HAVERSINE

Calculates the great-circle distance in kilometers between two points on the
Earth’s surface, using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).
The two points are specified by their latitude and longitude in decimal degrees.

Note

Snowflake recommends using the [ST\_DISTANCE](/sql-reference/functions/st_distance) function instead of the HAVERSINE function.
The ST\_DISTANCE function performs the calculation using values of geospatial types, which
enables you to store geospatial data and use the [geospatial functions](/sql-reference/functions-geospatial)
on the data. In addition, join predicates that use the ST\_DISTANCE function perform better than join predicates
that use the HAVERSINE function.

## Syntax

Copy code

```
HAVERSINE( <lat1>, <lon1>, <lat2>, <lon2> )
```

## Arguments

`lat1`
:   The latitude of the first point in decimal degrees.

`lon1`
:   The longitude of the first point in decimal degrees.

`lat2`
:   The latitude of the second point in decimal degrees.

`lon2`
:   The longitude of the second point in decimal degrees.

## Returns

This function returns a value of type FLOAT.

## Examples

The following example returns the geospatial distance in kilometers between New York and Los Angeles:

Copy code

```
SELECT HAVERSINE(
    40.7127,
    -74.0059,
    34.0500,
    -118.2500
  ) AS distance_in_kilometers;
```

```
+------------------------+
| DISTANCE_IN_KILOMETERS |
|------------------------|
|         3936.385096389 |
+------------------------+
```

The following example is the same as the previous example, but it returns the geospatial distance
in meters instead of kilometers by multiplying the result by 1000:

Copy code

```
SELECT HAVERSINE(
    40.7127,
    -74.0059,
    34.0500,
    -118.2500
  ) * 1000 AS distance_in_meters;
```

```
+--------------------+
| DISTANCE_IN_METERS |
|--------------------|
|   3936385.09638929 |
+--------------------+
```
