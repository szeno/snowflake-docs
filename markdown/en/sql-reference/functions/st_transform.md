Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_TRANSFORM

Converts a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object from one
[spatial reference system (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system) to another.

Use this function to
[change the SRID and the coordinates of the object to match the new SRS (spatial reference system)](/sql-reference/data-types-geospatial#label-geometry-change-srs).
If you just need to change the SRID without changing the coordinates (e.g. if the SRID was incorrect), use [ST\_SETSRID](/sql-reference/functions/st_setsrid)
instead.

## Syntax

Copy code

```
ST_TRANSFORM( <geometry_expression> [ , <from_srid> ] , <to_srid> );
```

## Arguments

**Required:**

`geometry_expression`
:   The argument must be of type GEOMETRY.

`to_srid`
:   The [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) that identifies the SRS to use. The function transforms the input GEOMETRY
    object to a new object that uses this SRS.

**Optional:**

`from_srid`
:   The SRID identifying the current SRS of the input GEOMETRY object.

    If this argument is omitted, the function uses the SRID specified in the input GEOMETRY object.

## Returns

The function returns a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that uses the SRS identified by `to_srid`.

## Usage notes

- SRIDs are based on the [EPSG standard](https://epsg.org/home.html) (v10.082). For example, the SRID 4326 corresponds to the authority EPSG with the code
  4326.
- Make sure that either the input GEOMETRY has the correct SRID set or that you specify the `from_srid` argument.
- Currently, the function does not support datum grid files. All transformations are performed using the static parameters of the
  datum without any grid file correction.
- If `geometry_expression`, `from_srid`, or `to_srid` are NULL, this function returns NULL.
- If `from_srid` or `to_srid` cannot be resolved to a valid SRID, an error occurs.

## Examples

The following example transforms a POINT GEOMETRY object from EPSG:32633 (WGS 84 / UTM zone 33N) to EPSG:3857 (Web Mercator).

Copy code

```
-- Set the output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT
  ST_TRANSFORM(
    ST_GEOMFROMWKT('POINT(389866.35 5819003.03)', 32633),
    3857
  ) AS transformed_geom;
```

```
+---------------------------------------------------------------+
| transformed_geom                                              |
|---------------------------------------------------------------|
| SRID=3857;POINT(1489140.093765644 6892872.198680112)          |
+---------------------------------------------------------------+
```

If the source SRID is not set correctly in the GEOMETRY object, you can specify the SRID in the `to_srid` argument of the
function. For example, to transform a POINT GEOMETRY object from EPSG:4326 (WGS84) to EPSG:28992 (Amersfoort / RD New):

Copy code

```
-- Set the output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT
  ST_TRANSFORM(
    ST_GEOMFROMWKT('POINT(4.500212 52.161170)'),
    4326,
    28992
  ) AS transformed_geom;
```

```
+---------------------------------------------------------------+
| transformed_geom                                              |
|---------------------------------------------------------------|
| SRID=28992;POINT (94308.66600006013 464038.16881095537)       |
+---------------------------------------------------------------+
```
