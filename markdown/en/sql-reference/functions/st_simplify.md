Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_SIMPLIFY

Given an input [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that represents
a Line or Polygon, returns a simpler approximation of the object. The function identifies and removes selected vertices, resulting
in a similar object that has fewer vertices.

For example, if the input object is a Polygon with 50 vertices, ST\_SIMPLIFY can return a simpler Polygon with only 20 of those
vertices.

When simplifying an object, the function removes a vertex only if the distance between that vertex and the edge resulting from
the removal of that vertex is within the specified tolerance.

## Syntax

Copy code

```
ST_SIMPLIFY( <geography_expression>, <tolerance> [ , <preserve_collapsed> ] )
ST_SIMPLIFY( <geometry_expression>, <tolerance> )
```

## Arguments

**Required:**

`geography_expression` OR `geometry_expression`
:   The GEOGRAPHY or GEOMETRY object to simplify.

    Depending on the type of the GEOGRAPHY or GEOMETRY object, ST\_SIMPLIFY has the following effect:

    | Type of Object | Effect of ST\_SIMPLIFY |
    | --- | --- |
    | LineString, MultiLineString, Polygon, or MultiPolygon | ST\_SIMPLIFY applies the simplification algorithm |
    | Point or MultiPoint | ST\_SIMPLIFY has no effect. |
    | GeometryCollection or FeatureCollection | For GEOGRAPHY objects, ST\_SIMPLIFY applies the simplification algorithm to each object in the collection.     For GEOMETRY objects, ST\_SIMPLIFY does not support these types. |

    Expand

    Show lessSee more

`tolerance`
:   The maximum distance used by the simplification algorithm. Depending on the data type of the object, the following units are used for
    the operation:

    - GEOGRAPHY - Distance is interpreted in meters.
    - GEOMETRY - Distance is interpreted in the units of the object’s SRID (spatial reference system identifier). For example, the
      distance is interpreted in degrees for EPSG:4326, in meters for many projected SRIDs, or in feet for some local SRIDs.

      If the distance exceeds this tolerance for a candidate vertex, ST\_SIMPLIFY keeps that vertex in the simplified object.

**Optional:**

`preserve_collapsed`
:   (For GEOGRAPHY objects only) If `TRUE`, retains objects that would otherwise be too small given the tolerance.

    For example, when `preserve_collapsed` is `FALSE` and `tolerance` is `10` (meters), a 1m long line
    is reduced to a point in the simplified object. When `preserve_collapsed` is `TRUE`, the line is preserved in
    the simplified object.

    Default: `FALSE`.

## Returns

The function returns a value of type GEOGRAPHY or GEOMETRY.

## Examples

### GEOGRAPHY examples

The examples in this section display output in WKT format:

> Copy code
>
> ```
> alter session set GEOGRAPHY_OUTPUT_FORMAT='WKT';
> ```

The following example returns a simplified LineString that has fewer vertices than the original LineString.
In the simplified object, a vertex is omitted if the distance between the vertex and the edge that replaces the vertex
is less than 1000 meters.

> Copy code
>
> ```
> SELECT ST_SIMPLIFY(
>     TO_GEOGRAPHY('LINESTRING(-122.306067 37.55412, -122.32328 37.561801, -122.325879 37.586852)'),
>     1000);
> +----------------------------------------------------------------------------------------------------+
> | ST_SIMPLIFY(                                                                                       |
> |     TO_GEOGRAPHY('LINESTRING(-122.306067 37.55412, -122.32328 37.561801, -122.325879 37.586852)'), |
> |     1000)                                                                                          |
> |----------------------------------------------------------------------------------------------------|
> | LINESTRING(-122.306067 37.55412,-122.325879 37.586852)                                             |
> +----------------------------------------------------------------------------------------------------+
> ```

### GEOMETRY examples

The examples in this section display output in WKT format:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
```

The following example returns a simplified LineString that has fewer vertices than the original LineString. In the simplified
object, a vertex is omitted if the distance between the vertex and the edge that replaces the vertex is less than 500 meters.

Copy code

```
SELECT ST_SIMPIFY(
  TO_GEOMETRY('LINESTRING(1100 1100, 2500 2100, 3100 3100, 4900 1100, 3100 1900)'),
  500);

+----------------------------------------------------------------------------------------------------+
| ST_SIMPLIFY(TO_GEOMETRY('LINESTRING(1100 1100, 2500 2100, 3100 3100, 4900 1100, 3100 1900)'), 500) |
|----------------------------------------------------------------------------------------------------|
| LINESTRING(1100 1100,3100 3100,4900 1100,3100 1900)                                                |
+----------------------------------------------------------------------------------------------------+
```

The following example simplifies an ellipse that has 36 initial vertices to a shape with 16 or 10 vertices, depending on the
`tolerance` argument:

Copy code

```
SELECT ST_NUMPOINTS(geom) AS numpoints_before,
  ST_NUMPOINTS(ST_Simplify(geom, 0.5)) AS numpoints_simplified_05,
  ST_NUMPOINTS(ST_Simplify(geom, 1)) AS numpoints_simplified_1
  FROM
  (SELECT ST_BUFFER(to_geometry('LINESTRING(0 0, 1 1)'), 10) As geom);

+------------------+-------------------------+------------------------+
| NUMPOINTS_BEFORE | NUMPOINTS_SIMPLIFIED_05 | NUMPOINTS_SIMPLIFIED_1 |
|------------------+-------------------------+------------------------|
|               36 |                      16 |                     10 |
+------------------+-------------------------+------------------------+
```
