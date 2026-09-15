# Geospatial data types

Snowflake offers native support for geospatial features such as points, lines, and polygons on the Earth’s surface.

Tip

You can use the search optimization service to improve query performance.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Data types

Snowflake provides the following data types for geospatial data:

- The [GEOGRAPHY](#label-data-types-geography) data type, which models Earth as though it were a perfect sphere.
- The [GEOMETRY](#label-data-types-geometry) data type, which represents features in a planar (Euclidean, Cartesian)
  coordinate system.

### GEOGRAPHY data type

The GEOGRAPHY data type follows the WGS 84 standard (spatial reference ID 4326; for details, see
<https://epsg.io/4326>).

Points on the earth are represented as degrees of longitude (from -180 degrees to +180 degrees) and latitude
(-90 to +90). Snowflake uses 14 decimal places to store GEOGRAPHY coordinates. When the data includes decimal
places exceeding this limit, the coordinates are rounded to ensure compliance with the specified length constraint.

Altitude currently isn’t supported.

Line segments are interpreted as great circle arcs on the Earth’s surface.

Snowflake also provides
[geospatial functions](/sql-reference/functions-geospatial) that
operate on the GEOGRAPHY data type.

If you have geospatial data — such as longitude and latitude data, WKT, WKB, GeoJSON, and so on — we suggest converting and
storing the data in GEOGRAPHY columns, rather than keeping the data in their original formats in VARCHAR, VARIANT, or NUMBER columns.
Storing your data in GEOGRAPHY columns can significantly improve the performance of queries that use geospatial functionality.

When the input to a geospatial function for the GEOGRAPHY data type represents a polygon, the starting point and ending point in
the polygon must be the same. Otherwise, the function might return errors.

### GEOMETRY data type

The GEOMETRY data type represents features in a planar (Euclidean, Cartesian) coordinate system.

The coordinates are represented as pairs of real numbers (x, y). Currently, only 2D coordinates are supported.

The units of the X and Y are determined by the [spatial reference system (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system) associated with the GEOMETRY object.
The spatial reference system is identified by the [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) number. Unless
the SRID is provided when creating the GEOMETRY object or by calling [ST\_SETSRID](/sql-reference/functions/st_setsrid), the SRID is 0.

Snowflake uses 14 decimal places to store GEOMETRY coordinates. When the data includes decimal
places exceeding this limit, the coordinates are rounded to ensure compliance with the specified length constraint.

Snowflake provides a set of
[geospatial functions that operate on the GEOMETRY data type](/sql-reference/functions-geospatial). For these functions:

- All functions assume planar coordinates, even if the geometry uses a non-planar SRS.
- The measurement functions (for example, [ST\_LENGTH](/sql-reference/functions/st_length)) use the same units as the coordinate system.
- For functions that accept multiple GEOMETRY expressions as arguments (for example, [ST\_DISTANCE](/sql-reference/functions/st_distance)),
  the input expressions must be defined in the same SRS.

## Geospatial input and output

The following sections cover the supported standard formats and object types when reading and writing geospatial data.

- [Supported standard input and output formats](#label-data-types-geospatial-io-formats)
- [Supported geospatial object types](#label-data-types-geospatial-object-types)
- [Specifying the output format for result sets](#label-data-types-geospatial-output-format)
- [Examples of inserting and querying GEOGRAPHY data](#label-data-types-geospatial-io-examples)

### Supported standard input and output formats

The GEOGRAPHY and GEOMETRY data types support the following standard industry formats for input and output:

- [Well-Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
  (WKT)
- [Well-Known Binary](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary)
  (WKB)
- [Extended WKT and WKB (EWKT and EWKB)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Format_variations)
  (see the [note on EWKT and EWKB handling](#label-a-note-on-ewkt-ewkb-handling))
- [IETF GeoJSON](https://tools.ietf.org/html/rfc7946)
  (see the [note on GeoJSON handling](#label-a-note-on-geojson-handling))

You might also find the following Open Geospatial Consortium’s Simple Feature Access references helpful:

- [Common Architecture](https://www.opengeospatial.org/standards/sfa)
- [SQL Option](https://www.opengeospatial.org/standards/sfs)

Any departure from these standards is noted explicitly in the Snowflake documentation.

#### GeoJSON handling for GEOGRAPHY values

The WKT and WKB standards specify a format only. The semantics of WKT/WKB objects depend on the reference system (for
example, a plane or a sphere).

The GeoJSON standard, on the other hand, specifies both a format and its semantics: GeoJSON points are explicitly
WGS 84 coordinates, and GeoJSON line segments are planar edges (straight lines).

Contrary to that, the Snowflake GEOGRAPHY data type interprets all line segments, including those input from or
output to GeoJSON format, as great circle arcs. In essence, Snowflake treats GeoJSON as JSON-formatted WKT with spherical
semantics.

#### EWKT and EWKB handling for GEOGRAPHY values

EWKT and EWKB are non-standard formats [introduced by PostGIS](https://postgis.net/docs/ST_GeomFromEWKT.html).
They enhance the WKT and WKB formats by including a [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier), which specifies the
coordinate reference system to use with the data. Snowflake currently supports only WGS84, which maps to SRID=4326.

By default, Snowflake issues an error if an EWKB or EWKT input value contains an SRID other than 4326. Conversely, all EWKB and EWKT output values have SRID=4326.

### Supported geospatial object types

The GEOGRAPHY and GEOMETRY data types can store the following types of geospatial objects:

- WKT / WKB / EWKT / EWKB / GeoJSON geospatial objects:

  - Point
  - MultiPoint
  - LineString
  - MultiLineString
  - Polygon
  - MultiPolygon
  - GeometryCollection
- These GeoJSON-specific geospatial objects:

  - Feature
  - FeatureCollection

### Specifying the output format for result sets

The session parameters [GEOGRAPHY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-geography-output-format) and
[GEOMETRY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-geometry-output-format) control the rendering of GEOGRAPHY and GEOMETRY columns in
result sets (respectively).

These parameters can have one of the following values:

| Parameter value | Description |
| --- | --- |
| `GeoJSON` (default) | The GEOGRAPHY / GEOMETRY result is rendered as an OBJECT in GeoJSON format. |
| `WKT` | The GEOGRAPHY / GEOMETRY result is rendered as a VARCHAR in WKT format. |
| `WKB` | The GEOGRAPHY / GEOMETRY result is rendered as a BINARY in WKB format. |
| `EWKT` | The GEOGRAPHY / GEOMETRY result is rendered as a VARCHAR in EWKT format. |
| `EWKB` | The GEOGRAPHY / GEOMETRY result is rendered as a BINARY in EWKB format. |

Expand

Show lessSee more

For `EWKT` and `EWKB`, the SRID is always 4326 in the output. See [EWKT and EWKB handling for GEOGRAPHY values](#label-a-note-on-ewkt-ewkb-handling).

This parameter affects all clients, including the Snowflake UI and the SnowSQL command-line client, as well as the
JDBC, ODBC, Node.js, Python, and so on drivers and connectors.

For example, the JDBC Driver returns the following metadata for a GEOGRAPHY-typed result column (column `i` in this
example):

- If `GEOGRAPHY_OUTPUT_FORMAT='GeoJSON'` or `GEOMETRY_OUTPUT_FORMAT='GeoJSON'`:

  - `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.VARCHAR`.
  - `ResultSetMetaData.getColumnClassName(i)` returns `"java.lang.String"`.
- If `GEOGRAPHY_OUTPUT_FORMAT='WKT'` or `'EWKT'`, or if `GEOMETRY_OUTPUT_FORMAT='WKT'` or `'EWKT'`:

  - `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.VARCHAR`.
  - `ResultSetMetaData.getColumnClassName(i)` returns `"java.lang.String"`.
- If `GEOGRAPHY_OUTPUT_FORMAT='WKB'` or `'EWKB'`, or if `GEOMETRY_OUTPUT_FORMAT='WKB'` or `'EWKB'`:

  - `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.BINARY`.
  - `ResultSetMetaData.getColumnClassName(i)` returns `"[B"` (array of byte).

Note

APIs for retrieving database-specific type names (`getColumnTypeName` in JDBC and the
`SQL_DESC_TYPE_NAME` descriptor in ODBC) always return `GEOGRAPHY` and `GEOMETRY` for the type name,
regardless of the values of the `GEOGRAPHY_OUTPUT_FORMAT` and `GEOMETRY_OUTPUT_FORMAT` parameters. For details, see:

- [Snowflake-specific behavior](/developer-guide/jdbc/jdbc-api#label-jdbc-resultset-meta-data-snowflake-specific-behavior) in the JDBC Driver documentation.
- [Retrieving results and information about results](/developer-guide/odbc/odbc-api#label-odbc-api-result-functions) in the ODBC Driver documentation.

### Examples of inserting and querying GEOGRAPHY data

The code below shows sample input and output for the GEOGRAPHY data type. Note the following:

- For the coordinates in WKT, EWKT, and GeoJSON, longitude appears before latitude (for example, `POINT(lon lat)`).

- For the WKB and EWKB output, it is assumed that the [BINARY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-binary-output-format) parameter
  is set to `HEX` (the default value for the parameter).

The following example creates a table with a GEOGRAPHY column, inserts data in WKT format, and returns
the data in different output formats.

Copy code

```
CREATE OR REPLACE TABLE geospatial_table (id INTEGER, g GEOGRAPHY);
INSERT INTO geospatial_table VALUES
  (1, 'POINT(-122.35 37.55)'),
  (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');
```

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='GeoJSON';
```

Copy code

```
SELECT g
  FROM geospatial_table
  ORDER BY id;
```

```
+------------------------+
| G                      |
|------------------------|
| {                      |
|   "coordinates": [     |
|     -122.35,           |
|     37.55              |
|   ],                   |
|   "type": "Point"      |
| }                      |
| {                      |
|   "coordinates": [     |
|     [                  |
|       -124.2,          |
|       42               |
|     ],                 |
|     [                  |
|       -120.01,         |
|       41.99            |
|     ]                  |
|   ],                   |
|   "type": "LineString" |
| }                      |
+------------------------+
```

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
```

Copy code

```
SELECT g
  FROM geospatial_table
  ORDER BY id;
```

```
+-------------------------------------+
| G                                   |
|-------------------------------------|
| POINT(-122.35 37.55)                |
| LINESTRING(-124.2 42,-120.01 41.99) |
+-------------------------------------+
```

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKB';
```

Copy code

```
SELECT g
  FROM geospatial_table
  ORDER BY id;
```

```
+------------------------------------------------------------------------------------+
| G                                                                                  |
|------------------------------------------------------------------------------------|
| 01010000006666666666965EC06666666666C64240                                         |
| 010200000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
+------------------------------------------------------------------------------------+
```

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='EWKT';
```

Copy code

```
SELECT g
  FROM geospatial_table
  ORDER BY id;
```

```
+-----------------------------------------------+
| G                                             |
|-----------------------------------------------|
| SRID=4326;POINT(-122.35 37.55)                |
| SRID=4326;LINESTRING(-124.2 42,-120.01 41.99) |
+-----------------------------------------------+
```

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='EWKB';
```

Copy code

```
SELECT g
  FROM geospatial_table
  ORDER BY id;
```

```
+--------------------------------------------------------------------------------------------+
| G                                                                                          |
|--------------------------------------------------------------------------------------------|
| 0101000020E61000006666666666965EC06666666666C64240                                         |
| 0102000020E610000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
+--------------------------------------------------------------------------------------------+
```

## Using geospatial data in Snowflake

The following sections cover how to work with geospatial data in Snowflake.

- [Understanding the effects of using different SRIDs with GEOMETRY](#label-geometry-store-srid)
- [Changing the spatial reference system (SRS) and SRID of a GEOMETRY object](#label-geometry-change-srs)
- [Performing DML operations on GEOGRAPHY and GEOMETRY columns](#label-data-types-geospatial-dml-operations)
- [Loading geospatial data from stages](#label-data-types-geospatial-stages)
- [Using geospatial data with Java UDFs](#label-data-types-geospatial-udf-java)
- [Using geospatial data with JavaScript UDFs](#label-data-types-geospatial-udf-javascript)
- [Using geospatial data with Python UDFs](#label-data-types-geospatial-udf-python)
- [Using GEOGRAPHY objects with H3](#label-data-types-geospatial-h3)

### Understanding the effects of using different SRIDs with GEOMETRY

In a GEOMETRY column, you can insert objects that have different [SRIDs](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier). If the column contains more than one SRID, some of the
important performance optimizations aren’t applied. This can result in slower queries, in particular when joining on a geospatial
predicate.

### Changing the spatial reference system (SRS) and SRID of a GEOMETRY object

To change the [SRS](https://en.wikipedia.org/wiki/Spatial_reference_system) and [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) of an existing GEOMETRY object, call the [ST\_TRANSFORM](/sql-reference/functions/st_transform) function,
passing in the new SRID. The function returns a new GEOMETRY object with the new SRID and the coordinates converted to use the
SRS. For example, to return a GEOMETRY object for `geometry_expression` that uses the SRS for SRID 32633, execute the following
statement:

Copy code

```
SELECT ST_TRANSFORM(geometry_expression, 32633);
```

If the original SRID isn’t set correctly in the existing GEOMETRY object, specify the original SRID as an additional argument.
For example, if `geometry_expression` is a GEOMETRY object that uses the SRID 4326, and you want to transform this to use the
SRID 28992, execute the following statement:

Copy code

```
SELECT ST_TRANSFORM(geometry_expression, 4326, 28992);
```

If a GEOMETRY object uses the correct coordinates for a SRS but has the wrong SRID, you can fix the SRID by calling the
[ST\_SETSRID](/sql-reference/functions/st_setsrid) function. For example, the following statement sets the SRID for
`geometry_expression` to 4326, while leaving the coordinates unchanged:

Copy code

```
SELECT ST_SETSRID(geometry_expression, 4326);
```

### Performing DML operations on GEOGRAPHY and GEOMETRY columns

When a GEOGRAPHY or GEOMETRY column is the target of a DML operation (INSERT, COPY, UPDATE, MERGE, or CREATE TABLE AS…), the
column’s source expression can be any of the following types:

- GEOGRAPHY or GEOMETRY : An expression of type GEOGRAPHY or GEOMETRY is usually the result of a parsing function, a constructor
  function, or an existing GEOGRAPHY or GEOMETRY column. For a complete list of supported functions and categories of functions,
  see [Geospatial functions](/sql-reference/functions-geospatial).
- VARCHAR: Interpreted as a WKT, WKB (in hex format), EWKT, EWKB (in hex format), or GeoJSON formatted string (see
  [TO\_GEOGRAPHY(VARCHAR)](/sql-reference/functions/to_geography)).
- BINARY: Interpreted as a WKB binary (see [TO\_GEOGRAPHY(BINARY)](/sql-reference/functions/to_geography) and
  [TO\_GEOMETRY(BINARY)](/sql-reference/functions/to_geometry)).
- VARIANT: Interpreted as a GeoJSON object (see [TO\_GEOGRAPHY(VARIANT)](/sql-reference/functions/to_geography) and
  [TO\_GEOMETRY(VARIANT)](/sql-reference/functions/to_geometry)).

### Loading geospatial data from stages

You can load data from CSV or JSON/AVRO files in a stage directly (that is, without copy transforms) into a
GEOGRAPHY column.

- CSV: String values from the corresponding CSV column are parsed as GeoJSON, WKT, EWKT, WKB, or EWKB (see
  [TO\_GEOGRAPHY(VARCHAR)](/sql-reference/functions/to_geography)).
- JSON/AVRO: The JSON values in the file are interpreted as GeoJSON (see
  [TO\_GEOGRAPHY(VARIANT)](/sql-reference/functions/to_geography)).

  See also [GeoJSON handling for GEOGRAPHY values](#label-a-note-on-geojson-handling).

Loading data from other file formats (Parquet, ORC, and so on) is
possible through a [COPY](/sql-reference/sql/copy-into-table) transform.

### Using geospatial data with Java UDFs

Java UDFs allow the GEOGRAPHY type as an argument and as a return value. See [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings) and
[Passing a GEOGRAPHY value to an in-line Java UDF](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-passing-geo) for details.

### Using geospatial data with JavaScript UDFs

JavaScript UDFs allow the GEOGRAPHY or GEOMETRY type as an argument and as a return value.

If a JavaScript UDF has an argument of type GEOGRAPHY or GEOMETRY, that argument is visible as a JSON object in GeoJSON
format inside the UDF body.

If a JavaScript UDF returns GEOGRAPHY or GEOMETRY, the UDF body is expected to return a JSON object in GeoJSON format.

For example, these two JavaScript UDFs are roughly equivalent to the built-in functions ST\_X and ST\_MAKEPOINT:

Copy code

```
CREATE OR REPLACE FUNCTION my_st_x(g GEOGRAPHY) RETURNS REAL
LANGUAGE JAVASCRIPT
AS
$$
  if (G["type"] != "Point")
  {
     throw "Not a point"
  }
  return G["coordinates"][0]
$$;

CREATE OR REPLACE FUNCTION my_st_makepoint(lng REAL, lat REAL) RETURNS GEOGRAPHY
LANGUAGE JAVASCRIPT
AS
$$
  g = {}
  g["type"] = "Point"
  g["coordinates"] = [ LNG, LAT ]
  return g
$$;
```

### Using geospatial data with Python UDFs

Python UDFs allow the GEOGRAPHY and GEOMETRY types as arguments and as return values.

If a Python UDF has an argument of type GEOGRAPHY or GEOMETRY, that argument is represented as a
GeoJSON object, which is converted to a Python `dict` object inside the UDF body.

If a Python UDF returns GEOGRAPHY or GEOMETRY, the UDF body is expected to return a Python `dict` object
that complies with the structure of GeoJSON.

For example, this Python UDF returns the number of distinct geometries that constitute a composite GEOGRAPHY type:

Copy code

```
CREATE OR REPLACE FUNCTION py_numgeographys(geo GEOGRAPHY)
RETURNS INTEGER
LANGUAGE PYTHON
RUNTIME_VERSION = 3.10
PACKAGES = ('shapely')
HANDLER = 'udf'
AS $$
from shapely.geometry import shape, mapping
def udf(geo):
    if geo['type'] not in ('MultiPoint', 'MultiLineString', 'MultiPolygon', 'GeometryCollection'):
        raise ValueError('Must be a composite geometry type')
    else:
        g1 = shape(geo)
        return len(g1.geoms)
$$;
```

Check [Snowflake Labs](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/geospatial/Python%20UDFs) for more samples
of Python UDFs. Some of them enable complex spatial manipulations or simplify data ingestion. For example,
[this UDF](https://github.com/Snowflake-Labs/sf-samples/blob/main/samples/geospatial/Python%20UDFs/PY_LOAD_GEOFILES.sql) allows
reading formats that aren’t supported natively, such as Shapefiles (.SHP), TAB, KML, GPKG, and others.

Note

The code samples in Snowflake Labs are intended solely for reference and educational purposes. These code samples aren’t covered
by any Service Level Agreement.

### Using GEOGRAPHY objects with H3

`H3`\_ is a [hierarchical geospatial index](https://h3geo.org/docs/highlights/indexing) that partitions
the world into hexagonal cells in a [discrete global grid system](https://en.wikipedia.org/wiki/Discrete_global_grid).

Snowflake provides SQL functions that enable you to use H3 with [GEOGRAPHY](#label-data-types-geography) objects. You can
use these functions to:

- Get the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)) for a GEOGRAPHY object that represents a Point (and vice versa).
- Get the IDs of the minimal set of H3 cells that cover a GEOGRAPHY object.
- Get the IDs of the H3 cells that have centroids within a GEOGRAPHY object that represents a Polygon.
- Get the GEOGRAPHY object that represents the boundary of an H3 cell.
- Get the parents and children of a given H3 cell.
- Get the longitude and latitude of the centroid of an H3 cell (and vice versa).
- Get the [resolution](https://h3geo.org/docs/core-library/restable) of an H3 cell.
- Get the hexadecimal representation of an H3 cell ID (and vice versa).

For more information about these functions, see [Geospatial functions](/sql-reference/functions-geospatial).

## Choosing the geospatial data type to use (GEOGRAPHY or GEOMETRY)

The next sections explain the differences between the GEOGRAPHY and GEOMETRY data types:

- [Understanding the differences between GEOGRAPHY and GEOMETRY](#label-geometry-geography-diffs)
- [Examples comparing the GEOGRAPHY and GEOMETRY data types](#label-geometry-geography-diffs-examples)
- [Understanding the differences in input data validation](#label-geometry-geography-validate)

### Understanding the differences between GEOGRAPHY and GEOMETRY

Although both the GEOGRAPHY and GEOMETRY data types define geospatial features, the types use different models. The following
table summarizes the differences.

| GEOGRAPHY data type | GEOMETRY data type |
| --- | --- |
| - Defines features on a sphere. - Only the WGS84 coordinate system. [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) is always 4326. - Coordinates are latitude (-90 to 90) and longitude (-180 to 180) in degrees. - Results of measurement operations (ST\_LENGTH, ST\_AREA, and so on) are in meters. - Segments are interpreted as great circle arcs on the Earth’s surface. | - Defines features on a plane. - Any coordinate system is supported. - Units of coordinate values are defined by the spatial reference system. - Results of measurement operations (ST\_LENGTH, ST\_AREA, and so on) are in the same unit as coordinates. For example, if the   input coordinates are in degrees, the results are in degrees. - Segments are interpreted as straight lines on the plane. |

Expand

Show lessSee more

### Examples comparing the GEOGRAPHY and GEOMETRY data types

The following examples compare the output of the geospatial functions when using the GEOGRAPHY and GEOMETRY data types as input.

#### Example 1: Querying the distance between Berlin and San Francisco

The following table compares the output of [ST\_DISTANCE](/sql-reference/functions/st_distance) for GEOGRAPHY types and GEOMETRY types:

| ST\_DISTANCE using   GEOGRAPHY input | ST\_DISTANCE using   GEOMETRY input |
| --- | --- |
| Copy code  ``` SELECT ST_DISTANCE(     ST_POINT(13.4814, 52.5015),     ST_POINT(-121.8212, 36.8252))   AS distance_in_meters; ```  ``` +--------------------+ | DISTANCE_IN_METERS | |--------------------| |   9182410.99227821 | +--------------------+ ``` | Copy code  ``` SELECT ST_DISTANCE(     ST_GEOMPOINT(13.4814, 52.5015),     ST_GEOMPOINT(-121.8212, 36.8252))   AS distance_in_degrees; ```  ``` +---------------------+ | DISTANCE_IN_DEGREES | |---------------------| |       136.207708844 | +---------------------+ ``` |

Expand

Show lessSee more

As shown in the example above:

- With GEOGRAPHY input values, the input coordinates are in degrees, and the output value is in meters. (The result is 9,182 km.)
- With GEOMETRY input values, the input coordinates and output value are degrees. (The result is 136.208 degrees.)

#### Example 2: Querying the area of Germany

The following table compares the output of [ST\_AREA](/sql-reference/functions/st_area) for GEOGRAPHY types and GEOMETRY types:

| ST\_AREA using   GEOGRAPHY input | ST\_AREA using   GEOMETRY input |
| --- | --- |
| Copy code  ``` SELECT ST_AREA(border) AS area_in_sq_meters   FROM world_countries   WHERE name = 'Germany'; ```  ``` +-------------------+ | AREA_IN_SQ_METERS | |-------------------| |  356379183635.591 | +-------------------+ ``` | Copy code  ``` SELECT ST_AREA(border) as area_in_sq_degrees   FROM world_countries_geom   WHERE name = 'Germany'; ```  ``` +--------------------+ | AREA_IN_SQ_DEGREES | |--------------------| |       45.930026848 | +--------------------+ ``` |

Expand

Show lessSee more

As shown in the example above:

- With GEOGRAPHY input values, the input coordinates are in degrees, the output value is in square meters. The result is
  356,379 km^2.
- With GEOMETRY input values, the input coordinates are in degrees, and the output value is in square degrees. The result is
  45.930 square degrees.

#### Example 3: Querying the names of countries overlapping the line from Berlin to San Francisco

The following table compares the output of [ST\_INTERSECTS](/sql-reference/functions/st_intersects) for GEOGRAPHY types and GEOMETRY types:

| ST\_INTERSECTS using   GEOGRAPHY input | ST\_INTERSECTS using   GEOMETRY input |
| --- | --- |
| Copy code  ``` SELECT name FROM world_countries WHERE   ST_INTERSECTS(border,     TO_GEOGRAPHY(       'LINESTRING(13.4814 52.5015, -121.8212 36.8252)'     )); ```  ``` +--------------------------+ | NAME                     | |--------------------------| |                  Germany | |                  Denmark | |                  Iceland | |                Greenland | |                   Canada | | United States of America | +--------------------------+ ``` | Copy code  ``` SELECT name FROM world_countries_geom WHERE   ST_INTERSECTS(border,     TO_GEOMETRY(       'LINESTRING(13.4814 52.5015, -121.8212 36.8252)'     )); ```  ``` +--------------------------+ | NAME                     | |--------------------------| |                  Germany | |                  Belgium | |              Netherlands | |           United Kingdom | | United States of America | +--------------------------+ ``` |
| Countries intersecting when using GEOGRAPHY | Countries intersecting when using GEOMETRY |

Expand

Show lessSee more

### Understanding the differences in input data validation

To create a GEOMETRY or GEOGRAPHY object for an input shape, you must use a shape that is well-formed and valid, according to the
[OGC rules for Simple Features](https://www.ogc.org/standards/sfa). The next sections explain how the validity of input data differs between GEOMETRY and GEOGRAPHY.

#### A shape can be valid GEOGRAPHY but invalid GEOMETRY

A given shape can be a valid GEOGRAPHY object but an invalid GEOMETRY object, and vice versa.

For example, self-intersecting polygons are disallowed by the OGC rules. A given set of points might define edges that intersect in
the Cartesian domain but not on a sphere. Consider the following polygon:

Copy code

```
POLYGON((0 50, 25 50, 50 50, 0 50))
```

In the Cartesian domain, this polygon degrades to a line and, as a result, is invalid.

However, on a sphere, this same polygon doesn’t intersect itself and is valid:

![POLYGON((0 50, 25 50, 50 50, 0 50)) invalid geometry, but valid geography](/static/images/geography-valid-geometry-invalid-example.png)

#### Conversion and constructor functions handle validation differently

When the input data is invalid, the GEOMETRY and GEOGRAPHY functions handle validation in different ways:

- Some of the functions for constructing and converting to GEOGRAPHY objects might attempt to repair the shape to handle problems
  such as unclosed loops, spikes, cuts, and self-intersecting loops in polygons. For example, when either the
  [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) function or the
  [ST\_MAKEPOLYGON](/sql-reference/functions/st_makepolygon) function is used to
  construct a polygon, the function corrects the orientation of the loop to prevent the creation of polygons that span more than half of the
  globe. However, the [ST\_MAKEPOLYGONORIENTED](/sql-reference/functions/st_makepolygonoriented) function doesn’t attempt to correct the orientation of
  the loop.

  If the function is successful in repairing the shape, the function returns a GEOGRAPHY object.
- The functions for constructing and converting to GEOMETRY objects (for example, [TO\_GEOMETRY](/sql-reference/functions/to_geometry)) don’t
  support the ability to repair the shape.

## Converting between GEOGRAPHY and GEOMETRY

Snowflake supports converting from a GEOGRAPHY object to a GEOMETRY object (and vice versa). Snowflake also supports
transformations of objects that use different spatial reference systems (SRS).

The following example converts a GEOGRAPHY object that represents a point to a GEOMETRY object with the [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) 0:

Copy code

```
SELECT TO_GEOMETRY(TO_GEOGRAPHY('POINT(-122.306100 37.554162)'));
```

To set the SRID of the new GEOMETRY object, pass the SRID as an argument to the constructor function. For example:

Copy code

```
SELECT TO_GEOMETRY(TO_GEOGRAPHY('POINT(-122.306100 37.554162)', 4326));
```

If you need to set the SRID of an existing GEOMETRY object, see [Changing the spatial reference system (SRS) and SRID of a GEOMETRY object](#label-geometry-change-srs).

## Automatic performance optimizations for queries with geospatial predicates

Snowflake automatically implements the following performance optimizations for queries
with geospatial predicates:

- [GeoJoin](#label-geojoin)
- [Geospatial pruning for GEOMETRY predicates](#label-geometry-pruning)

### GeoJoin

*GeoJoin* is a Snowflake query optimization feature for geospatial joins. It’s a specialized join rewrite optimization
that improves performance when joining tables based on predicates that call geospatial functions, such as ST\_INTERSECTS,
ST\_CONTAINS, ST\_DWITHIN, and so on. For example, a GeoJoin might be used to find all stores within specific geographic
regions.

GeoJoin has the following characteristics:

- Automatically optimizes queries that join tables that use geospatial functions.
- Performs spatial overlap analysis between geographic datasets.

The GeoJoin optimization is triggered automatically by Snowflake’s query optimizer when it detects appropriate geospatial
join patterns in your SQL queries. No additional configuration is required to benefit from improved performance.

### Geospatial pruning for GEOMETRY predicates

Snowflake can improve the performance of some queries that filter on a GEOMETRY column by
[pruning micro-partitions](/user-guide/tables-clustering-micropartitions#label-micropartitions-query-pruning) that can’t contain matching
rows. This optimization uses bounding-box metadata stored with GEOMETRY values to avoid scanning data that is guaranteed
not to satisfy the predicate. That is, Snowflake skips micro-partitions whose stored bounding-box metadata don’t
intersect the bounding box of a constant geometry in your filter.

Snowflake performs this optimization automatically, and no additional configuration is required to benefit
from improved performance.

#### Predicates that can benefit from geospatial pruning

Pruning is designed for filter predicates on a GEOMETRY column where one side is a constant geometry, such as a
literal or constant-foldable expression. For example:

- `ST_INTERSECTS(geom_col, <constant_geometry>)`
- `ST_CONTAINS(geom_col, <constant_geometry>)`
- `ST_COVERS(geom_col, <constant_geometry>)`
- `ST_COVEREDBY(geom_col, <constant_geometry>)`
- `ST_WITHIN(geom_col, <constant_geometry>)`

These are the specific types of predicates that benefit from file-level pruning that uses bounding boxes.

#### How geospatial pruning works

A GEOMETRY value is stored with metadata that includes the following items:

- A bounding box (xmin, ymin, xmax, ymax)
- An SRID value

Snowflake uses file-level bounding-box metadata as the primary signal for pruning.

Snowflake pre-checks micro-partitions for bounding-box intersections before evaluating the exact geometry predicate.
If the metadata indicates that no bounding-box overlap is possible, the micro-partitions can be skipped.

The following illustration shows a bounding-box line with two intersecting shapes and two non-intersecting shapes:

![Bounding-box line with two intersecting shapes and two non-intersecting shapes](/static/images/geospatial-pruning.png)

The illustration shows a geospatial query that is similar to the following example:

Copy code

```
SELECT *
  FROM <table>
  WHERE ST_CONTAINS(<geo_column>, <constant_geometry>);
```

For a bounding box that is specified from the geospatial constant (shown in blue), only the micro-partitions that
correspond with bounding boxes that overlap the bounding-box line (shown in green) are scanned. Micro-partitions
that correspond with bounding boxes that don’t overlap (shown in red) are pruned.

#### SRID behavior

Spatial predicates in Snowflake are SRID-sensitive. Therefore, mixing incompatible SRIDs in the same column might
return incorrect results. For the best results and deterministic behavior, keep SRIDs consistent within a GEOMETRY
column, which is also the common real-world pattern.

#### Geospatial pruning for Iceberg tables

For Iceberg GEOMETRY columns, Snowflake tries to use the bounding-box metadata for geospatial pruning, the same way it
does for GEOMETRY columns in standard Snowflake tables. If the necessary statistics are present in the underlying Iceberg
metadata, the same pruning logic applies without modification.

#### Other performance considerations for geospatial pruning

Geospatial pruning works best when the data layout allows Snowflake to skip large ranges of micro-partitions. If rows
with similar locations are spread across many micro-partitions, Snowflake might need to scan a large portion of the
table, even when pruning is used.

Clustering by location can improve pruning efficiency. When you cluster rows by a spatial key derived from your GEOMETRY column,
objects that are near each other are more likely to be stored in the same micro-partitions. As a result, spatial filters,
such as ST\_INTERSECTS or ST\_CONTAINS with a constant geometry, can prune more micro-partitions and read less data.

Follow these best practices to optimize geospatial pruning:

- Cluster by a discretized spatial index, such as H3 or geohash, computed from a representative point of the
  geometry, such as the centroid. Use a resolution appropriate for your query window sizes.
- If your geometries are large, such as polygons that cover wide areas, consider clustering by multiple keys
  to reduce over-clustering and improve selectivity. For example, cluster by H3 at two resolutions or a coarse
  grid key plus a finer grid key. For datasets with a dominant query pattern — for example, “within a city” or
  “within a tile” — choose a clustering key that aligns with that pattern.

The following example clusters a table by a GEOMETRY column that contains points:

Copy code

```
ALTER TABLE <table_name>
  CLUSTER BY (H3_POINT_TO_CELL(<geo_column>, <h3_resolution>));
```

The following example clusters a table by a GEOMETRY column that contains LineStrings and Polygons:

Copy code

```
ALTER TABLE <table_name>
  CLUSTER BY (H3_POINT_TO_CELL(ST_CENTROID(<geo_column>), <h3_resolution>));
```

Note

- Clustering doesn’t change query results. It changes how data is organized on storage. The benefits of clustering
  depend on data distribution, table size, and query patterns.
- You can monitor pruning effectiveness by comparing bytes scanned and micro-partitions scanned before and after
  clustering.

#### Limitations for geospatial pruning

The following limitations apply to geospatial pruning:

- It applies only to GEOMETRY (planar) predicates.

  To prune GEOGRAPHY predicates, use [search optimization](/user-guide/search-optimization-service).
- It applies only when one predicate argument is a constant.

  If both predicate arguments are columns (for example, `ST_INTERSECTS(a.geom, b.geom)`), this optimization
  doesn’t apply. For such cases, [GeoJoin](#label-geojoin) might be used.

## Specifying how invalid geospatial shapes are handled

By default, when you use a [geospatial conversion function](/sql-reference/functions-geospatial) to convert
[data in a supported input format](#label-data-types-geospatial-io-formats) to a GEOGRAPHY or GEOMETRY object, the function
does the following:

1. The function attempts to validate the shape in the input data.
2. The function determines if the shape is valid according to the
   [Open Geospatial Consortium’s Simple Feature Access / Common Architecture](https://www.ogc.org/standards/sfa) standard.
3. If the shape is invalid, the function attempts to repair the data (for example, fixing polygons by closing the rings).
4. If the shape is still invalid after the repairs, the function reports an error and doesn’t create the GEOGRAPHY or GEOMETRY
   object. (For the TRY\_\* functions, the functions return NULL, rather than reporting an error.)

With this feature, you have more control over the validation and repair process. You can:

- Allow these conversion functions to create GEOGRAPHY and GEOMETRY objects for invalid shapes.
- Determine if the shape for a GEOGRAPHY or GEOMETRY object is invalid.

### Understanding the effects of invalid shapes on geospatial functions

Different [geospatial functions](/sql-reference/functions-geospatial) have different effects when you pass in a GEOGRAPHY
or GEOMETRY object for an invalid shape.

#### Effects on GEOMETRY objects

For GEOMETRY objects:

- The following functions return results based on the original invalid shape:

  - [ST\_AREA](/sql-reference/functions/st_area)
  - [ST\_ASGEOJSON](/sql-reference/functions/st_asgeojson)
  - [ST\_ASWKB](/sql-reference/functions/st_aswkb)
  - [ST\_ASWKT](/sql-reference/functions/st_aswkt)
  - [ST\_CENTROID](/sql-reference/functions/st_centroid)
  - [ST\_CONTAINS](/sql-reference/functions/st_contains)
  - [ST\_DIMENSION](/sql-reference/functions/st_dimension)
  - [ST\_DISTANCE](/sql-reference/functions/st_distance)
  - [ST\_ENVELOPE](/sql-reference/functions/st_envelope)
  - [ST\_INTERSECTS](/sql-reference/functions/st_intersects)
  - [ST\_LENGTH](/sql-reference/functions/st_length)
  - [ST\_NPOINTS , ST\_NUMPOINTS](/sql-reference/functions/st_npoints)
  - [ST\_PERIMETER](/sql-reference/functions/st_perimeter)
  - [ST\_SETSRID](/sql-reference/functions/st_setsrid)
  - [ST\_SRID](/sql-reference/functions/st_srid)
  - [ST\_X](/sql-reference/functions/st_x)
  - [ST\_XMAX](/sql-reference/functions/st_xmax)
  - [ST\_XMIN](/sql-reference/functions/st_xmin)
  - [ST\_Y](/sql-reference/functions/st_y)
  - [ST\_YMAX](/sql-reference/functions/st_ymax)
  - [ST\_YMIN](/sql-reference/functions/st_ymin)
- The following functions validate the shape and fail with an error if the shape is invalid:

  - [ST\_MAKELINE](/sql-reference/functions/st_makeline)
  - [ST\_MAKEPOLYGON](/sql-reference/functions/st_makepolygon)

#### Effects on GEOGRAPHY objects

For GEOGRAPHY objects:

- The following functions return results based on the original invalid shape:

  - [ST\_ASWKB](/sql-reference/functions/st_aswkb)
  - [ST\_ASWKT](/sql-reference/functions/st_aswkt)
  - [ST\_ASGEOJSON](/sql-reference/functions/st_asgeojson)
  - [ST\_AZIMUTH](/sql-reference/functions/st_azimuth)
  - [ST\_COLLECT](/sql-reference/functions/st_collect)
  - [ST\_DIMENSION](/sql-reference/functions/st_dimension)
  - [ST\_GEOHASH](/sql-reference/functions/st_geohash)
  - [ST\_HAUSDORFFDISTANCE](/sql-reference/functions/st_hausdorffdistance)
  - [ST\_MAKELINE](/sql-reference/functions/st_makeline)
  - [ST\_NPOINTS , ST\_NUMPOINTS](/sql-reference/functions/st_npoints)
  - [ST\_POINTN](/sql-reference/functions/st_pointn)
  - [ST\_SRID](/sql-reference/functions/st_srid)
  - [ST\_ENDPOINT](/sql-reference/functions/st_endpoint)
  - [ST\_STARTPOINT](/sql-reference/functions/st_startpoint)
  - [ST\_X](/sql-reference/functions/st_x)
  - [ST\_Y](/sql-reference/functions/st_y)
- The following functions validate the shape and fail with an error if the shape is invalid:

  - [ST\_COLLECT](/sql-reference/functions/st_collect)
  - [ST\_MAKEPOLYGON](/sql-reference/functions/st_makepolygon)
  - [ST\_MAKEPOLYGONORIENTED](/sql-reference/functions/st_makepolygonoriented)
- The following functions return NULL if it isn’t possible to compute the value:

  - [ST\_AREA](/sql-reference/functions/st_area)
  - [ST\_CENTROID](/sql-reference/functions/st_centroid)
  - [ST\_CONTAINS](/sql-reference/functions/st_contains)
  - [ST\_COVERS](/sql-reference/functions/st_covers)
  - [ST\_DIFFERENCE](/sql-reference/functions/st_difference)
  - [ST\_DISTANCE](/sql-reference/functions/st_distance)
  - [ST\_DWITHIN](/sql-reference/functions/st_dwithin)
  - [ST\_ENVELOPE](/sql-reference/functions/st_envelope)
  - [ST\_INTERSECTION](/sql-reference/functions/st_intersection)
  - [ST\_INTERSECTION\_AGG](/sql-reference/functions/st_intersection_agg)
  - [ST\_INTERSECTS](/sql-reference/functions/st_intersects)
  - [ST\_LENGTH](/sql-reference/functions/st_length)
  - [ST\_PERIMETER](/sql-reference/functions/st_perimeter)
  - [ST\_SIMPLIFY](/sql-reference/functions/st_simplify)
  - [ST\_SYMDIFFERENCE](/sql-reference/functions/st_symdifference)
  - [ST\_UNION](/sql-reference/functions/st_union)
  - [ST\_UNION\_AGG](/sql-reference/functions/st_union_agg)
  - [ST\_XMAX](/sql-reference/functions/st_xmax)
  - [ST\_XMIN](/sql-reference/functions/st_xmin)
  - [ST\_YMAX](/sql-reference/functions/st_ymax)
  - [ST\_YMIN](/sql-reference/functions/st_ymin)

### Working with invalid shapes

The next sections explain how to allow functions to create invalid shapes and how to determine if a GEOGRAPHY or GEOMETRY object
represents an invalid or repaired shape.

#### Allowing conversion functions to create invalid shapes

To allow the following conversion functions to create invalid geospatial objects, pass `TRUE` for the second argument
(`allowInvalid`):

Copy code

```
TO_GEOGRAPHY( <input> [, <allowInvalid> ] )
```

Copy code

```
ST_GEOGFROMWKB( <input> [, <allowInvalid> ] )
```

Copy code

```
ST_GEOGFROMWKT( <input> [, <allowInvalid> ] )
```

Copy code

```
TO_GEOMETRY( <input> [, <allowInvalid> ] )
```

Copy code

```
ST_GEOMFROMWKB( <input> [, <allowInvalid> ] )
```

Copy code

```
ST_GEOMFROMWKT( <input> [, <allowInvalid> ] )
```

By default, the `allowInvalid` argument is `FALSE`.

When you pass `TRUE` for the `allowInvalid` argument, the conversion function returns a GEOGRAPHY or GEOMETRY
object, even when the input shape is invalid and can’t be repaired successfully.

For example, the following input shape is a LineString that consists of the same two Points. Passing `TRUE` for the
`allowInvalid` argument returns a GEOMETRY object that represents an invalid shape:

Copy code

```
SELECT TO_GEOMETRY('LINESTRING(100 102,100 102)', TRUE);
```

#### Determining if a shape is invalid

To determine if a GEOGRAPHY or GEOMETRY object is invalid, call the [ST\_ISVALID](/sql-reference/functions/st_isvalid) function.

The following example checks if an object is valid:

Copy code

```
SELECT TO_GEOMETRY('LINESTRING(100 102,100 102)', TRUE) AS g, ST_ISVALID(g);
```
