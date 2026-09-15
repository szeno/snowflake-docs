Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_BUFFER

Returns a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that represents a MultiPolygon containing
the points within a specified distance of the input GEOMETRY object. The returned object effectively
represents a “buffer” around the input object.

You can also “shrink” the input object by specifying a negative value for the distance.

## Syntax

Copy code

```
ST_BUFFER( <geometry_expression> , <distance> )
```

## Arguments

`geometry_expression`
:   The argument must be an expression of type GEOMETRY.

`distance`
:   The distance from the GEOMETRY object. To “shrink” the object, you can specify a negative value for the distance.

    The units depend on the [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) of the GEOMETRY object. For example,
    [EPSG:4326](https://epsg.io/4326) units are degrees, while [EPSG:25833](https://epsg.io/25833)
    units are meters.

## Returns

Returns a GEOMETRY object.

## Usage notes

- SRIDs are based on the [EPSG standard](https://epsg.org/home.html) (v10.082). For example, the SRID 4326 corresponds to the authority EPSG with the code
  4326.
- ST\_BUFFER uses eight segments to approximate a quarter circle.
- If `distance` is a negative value, the returned object is smaller than the input object. You can use this to
  remove small irregularities from the shape.
- For LineStrings, the endcap and join styles are always round.
- LineStrings are always buffered on both sides.

## Examples

Before executing the examples, set the [GEOMETRY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-geometry-output-format) parameter to `WKT`:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
```

### Buffer a Point

Buffering a Point returns a MultiPolygon that approximates a circle around the Point. Because ST\_BUFFER uses eight
segments to approximate each quarter circle, the circle is drawn with 32 straight segments (33 points, because the ring
repeats its starting point). The area is therefore slightly smaller than the area of a true circle
(`PI() * 1 * 1`, or about `3.1416`).

The following example buffers a Point by a distance of `1` and reports the number of points and the area of the result:

Copy code

```
SELECT ST_NPOINTS(buffer) AS num_points,
       ST_AREA(buffer) AS area
  FROM (SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1) AS buffer);
```

```
+------------+-------------------+
| NUM_POINTS |              AREA |
|------------+-------------------|
|         33 | 3.121445152258052 |
+------------+-------------------+
```

To see the full shape, select the buffer directly (for example, `SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1)`).
The output is a MultiPolygon with a long list of coordinates for the 32 segments that approximate the circle.

### Buffer a LineString

ST\_BUFFER buffers a LineString on both sides and uses round endcaps, so the result is a capsule-shaped MultiPolygon.
The following example buffers a line that is 10 units long by a distance of `2`:

Copy code

```
SELECT ST_NPOINTS(buffer) AS num_points,
       ST_AREA(buffer) AS area
  FROM (SELECT ST_BUFFER(TO_GEOMETRY('LINESTRING(0 0, 10 0)'), 2) AS buffer);
```

```
+------------+--------------------+
| NUM_POINTS |               AREA |
|------------+--------------------|
|         36 | 52.485780609032204 |
+------------+--------------------+
```

The area is the rectangle along the line (10 units long and 4 units wide, for 40 square units) plus the two rounded ends,
which together approximate a circle with a radius of `2`.

### Specify the distance in meters

The units of `distance` depend on the SRID of the input object. The following example
buffers a Point in SRID 32633 (UTM zone 33N, which uses meters) by `100` meters. The resulting area is close to the area
of a circle with a 100-meter radius (`PI() * 100 * 100`, or about `31416` square meters):

Copy code

```
SELECT ST_AREA(buffer) AS area_sq_meters
  FROM (SELECT ST_BUFFER(TO_GEOMETRY('SRID=32633;POINT(0 0)'), 100) AS buffer);
```

```
+--------------------+
|     AREA_SQ_METERS |
|--------------------|
|  31214.45152258053 |
+--------------------+
```

### Shrink a shape with a negative distance

The following example uses a negative value for `distance` to remove small irregularities (such as spikes) from the shape.
The [TO\_GEOMETRY](/sql-reference/functions/to_geometry) call passes in TRUE as the second argument, which allows the function to create a GEOMETRY
object for [an invalid shape](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

Copy code

```
SELECT ST_BUFFER(TO_GEOMETRY('SRID=2261;POLYGON((
  1540792.21541900 290472.63529214, 1547018.61770388 302537.02285369,
  1546965.96550151 302752.51514772, 1547018.61770388 302537.02285369,
  1549532.42729914 301257.07398027, 1543327.42218339 289322.60923536,
  1540792.21541900 290472.63529214))', True), -1e-08) AS geom;
```

```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| GEOM                                                                                                                                                                                        |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MULTIPOLYGON(((1543327.42218339 289322.609235373,1540792.21541901 290472.635292145,1547018.61770388 302537.022853677,1549532.42729913 301257.073980266,1543327.42218339 289322.609235373))) |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
