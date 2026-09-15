Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# TO\_GEOMETRY

Parses an input and returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

See also:
:   [TRY\_TO\_GEOMETRY](/sql-reference/functions/try_to_geometry) , [ST\_GEOMETRYFROMWKB](/sql-reference/functions/st_geometryfromwkb) , [ST\_GEOMETRYFROMWKT](/sql-reference/functions/st_geometryfromwkt)

## Syntax

Use one of the following:

Copy code

```
TO_GEOMETRY( <varchar_expression> [ , <srid> ] [ , <allow_invalid> ] )

TO_GEOMETRY( <binary_expression> [ , <srid> ] [ , <allow_invalid> ] )

TO_GEOMETRY( <variant_expression> [ , <srid> ] [ , <allow_invalid> ] )

TO_GEOMETRY( <geography_expression> [ , <srid> ] [ , <allow_invalid> ] )
```

## Arguments

**Required:**

`varchar_expression`
:   The argument must be a string expression that represents a valid geometric object in one of the following formats:

    - WKT (well-known text)
    - WKB (well-known binary) in hexadecimal format (without a leading `0x`)
    - EWKT (extended well-known text)
    - EWKB (extended well-known binary) in hexadecimal format (without a leading `0x`)
    - GeoJSON

`binary_expression`
:   The argument must be a binary expression in WKB or EWKB format.

`variant_expression`
:   The argument must be an OBJECT in GeoJSON format.

`geography_expression`
:   The argument must be an expression of type GEOGRAPHY.

**Optional:**

`srid`
:   The integer value of the SRID to use.

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

## Usage notes

- Issues an error if the input cannot be parsed as one of the supported formats (WKT, WKB, EWKT, EWKB, GeoJSON).
- For GeoJSON, WKT, and WKB input, if the `srid` argument is not specified, the resulting GEOMETRY object has the SRID
  set to 0.
- To construct a GEOMETRY object from WKT or EWKT input, you can also use [ST\_GEOMETRYFROMWKT](/sql-reference/functions/st_geometryfromwkt).
- To construct a GEOMETRY object from WKB or EWKB input, you can also use [ST\_GEOMETRYFROMWKB](/sql-reference/functions/st_geometryfromwkb).

## Examples

The following example shows how to use the TO\_GEOMETRY function to convert an object represented in WKT to a GEOMETRY object. The
example doesn’t specify the `srid` argument, and the SRID isn’t specified in the input representation of the object, so
the SRID is set to `0`.

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT TO_GEOMETRY('POINT(1820.12 890.56)');
```

```
+--------------------------------------+
| TO_GEOMETRY('POINT(1820.12 890.56)') |
|--------------------------------------|
| SRID=0;POINT(1820.12 890.56)         |
+--------------------------------------+
```

The following example converts an object represented in EWKT to a GEOMETRY object. The input EWKT specifies the SRID to use:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT TO_GEOMETRY('SRID=4326;POINT(1820.12 890.56)');
```

```
+------------------------------------------------+
| TO_GEOMETRY('SRID=4326;POINT(1820.12 890.56)') |
|------------------------------------------------|
| SRID=4326;POINT(1820.12 890.56)                |
+------------------------------------------------+
```

The following example demonstrates how to specify the SRID as the `srid` input argument:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT TO_GEOMETRY('POINT(1820.12 890.56)', 4326);
```

```
+--------------------------------------------+
| TO_GEOMETRY('POINT(1820.12 890.56)', 4326) |
|--------------------------------------------|
| SRID=4326;POINT(1820.12 890.56)            |
+--------------------------------------------+
```

The following example returns the GEOMETRY object for a geospatial object with a Z coordinate described in EWKT format:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT TO_GEOMETRY('SRID=32633;POINTZ(389866.35 5819003.03 30)');
```

```
+-----------------------------------------------------------+
| TO_GEOMETRY('SRID=32633;POINTZ(389866.35 5819003.03 30)') |
|-----------------------------------------------------------|
| SRID=32633;POINTZ(389866.35 5819003.03 30)                |
+-----------------------------------------------------------+
```

For examples that convert a GEOGRAPHY object to a GEOMETRY object, see [Converting between GEOGRAPHY and GEOMETRY](/sql-reference/data-types-geospatial#label-geometry-geography-converting).

The next examples use the TO\_GEOMETRY function in queries on data in a table.

Create a temporary table and insert rows with GEOMETRY values:

Copy code

```
CREATE OR REPLACE TEMP TABLE demo_to_geometry AS
SELECT
  1                                                     AS id,
  'POINT(10 20)'                                        AS wkt_col,         -- VARCHAR (WKT)
  'SRID=32633;POINT(500000.0 4649776.22)'               AS ewkt_col,        -- VARCHAR (EWKT)
  ST_ASWKB(TO_GEOMETRY('LINESTRING(0 0, 1 1)'))         AS wkb_bin_col,     -- BINARY (WKB)
  PARSE_JSON('{"type":"Point","coordinates":[10,20]}')  AS geojson_col,     -- VARIANT (GeoJSON)
  TO_GEOGRAPHY('POINT(-122.35 37.55)')                  AS geog_col,        -- GEOGRAPHY
  'POLYGON((0 0,2 2,2 0,0 2,0 0))'                      AS invalid_wkt_col, -- invalid shape
  0                                                     AS srid0,           -- SRID columns to show positional args
  3857                                                  AS srid_col,
  TRUE                                                  AS allow_true,      -- allow_invalid flags from columns
  FALSE                                                 AS allow_false
UNION ALL
SELECT
  2,
  'LINESTRING(0 0, 10 10)',
  'SRID=32633;POINT(389866.35 5819003.03)',
  ST_ASWKB(TO_GEOMETRY('POINT(2 3)')),
  PARSE_JSON('{"type":"LineString","coordinates":[[0,0],[1,1]]}'),
  TO_GEOGRAPHY('LINESTRING(-124.2 42,-120.01 41.99)'),
  'POLYGON((0 0,1 1,1 0,0 1,0 0))',
  0,
  3857,
  TRUE,
  FALSE;
```

This table has columns with data types that the TO\_GEOMETRY function accepts as inputs in the following formats:

- VARCHAR (WKT/WKB and hex/EWKT/EWKB/GeoJSON)
- BINARY (WKB/EWKB)
- VARIANT (GeoJSON object)
- GEOGRAPHY

Optional `srid` and `allow_invalid` values can follow any of these formats. The [St\_Aswkb](st_aswkb) function
generates valid WKB BINARY values.

The following example converts VARCHAR values in the `wkt_col` column to GEOMETRY values by using the default
SRID of `0`:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(wkt_col) AS g
  FROM demo_to_geometry;
```

```
+----+------------------------------+
| ID | G                            |
|----+------------------------------|
|  1 | SRID=0;POINT(10 20)          |
|  2 | SRID=0;LINESTRING(0 0,10 10) |
+----+------------------------------+
```

The following example converts VARCHAR values in the `wkt_col` column to GEOMETRY values by using the
SRID value in the `srid_col` column:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(wkt_col, srid_col) AS g
  FROM demo_to_geometry;
```

```
+----+----------------------------------+
| ID | G                                |
|----+----------------------------------|
|  1 | SRID=3857;POINT(10 20)           |
|  2 | SRID=3857;LINESTRING(0 0,10 10)  |
+----+----------------------------------+
```

The following example converts VARCHAR values in the `ewkt_col` column to GEOMETRY values, with the SRID value
embedded in the `ewkt_col` column value:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(ewkt_col) AS g
  FROM demo_to_geometry;
```

```
+----+--------------------------------------------+
| ID | G                                          |
|----+--------------------------------------------|
|  1 | SRID=32633;POINT(500000 4649776.22)        |
|  2 | SRID=32633;POINT(389866.35 5819003.03)     |
+----+--------------------------------------------+
```

The following example converts BINARY values in the `wkb_bin_col` column to GEOMETRY values:

Copy code

```
ALTER SESSION SET BINARY_OUTPUT_FORMAT='HEX';

SELECT id, TO_GEOMETRY(wkb_bin_col) AS g
  FROM demo_to_geometry;
```

```
+----+----------------------------+
| ID | G                          |
|----+----------------------------|
|  1 | SRID=0;LINESTRING(0 0,1 1) |
|  2 | SRID=0;POINT(2 3)          |
+----+----------------------------+
```

The following example converts VARIANT values in the `geojson_col` column to GEOMETRY values
by using the SRID value in the `srid_col` column:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(geojson_col, srid_col) AS g
  FROM demo_to_geometry;
```

```
+----+--------------------------------+
| ID | G                              |
|----+--------------------------------|
|  1 | SRID=3857;POINT(10 20)         |
|  2 | SRID=3857;LINESTRING(0 0,1 1)  |
+----+--------------------------------+
```

The following example converts GEOGRAPHY values in the `geog_col` column to GEOMETRY values
by using the SRID value in the `srid_col` column:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(geog_col, srid_col) AS g
  FROM demo_to_geometry;
```

```
+----+-----------------------------------------------+
| ID | G                                             |
|----+-----------------------------------------------|
|  1 | SRID=4326;POINT(-122.35 37.55)                |
|  2 | SRID=4326;LINESTRING(-124.2 42,-120.01 41.99) |
+----+-----------------------------------------------+
```

The following example converts VARCHAR values in the `invalid_wkt_col` column to GEOMETRY values by using
the SRID value in the `srid0` column (`0`) and the `allow_invalid` value in the `allow_true`
column:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TO_GEOMETRY(invalid_wkt_col, srid0, allow_true) AS g
  FROM demo_to_geometry;
```

The output includes shapes that aren’t valid:

```
+----+---------------------------------------+
| ID | G                                     |
|----+---------------------------------------|
|  1 | SRID=0;POLYGON((0 0,2 2,2 0,0 2,0 0)) |
|  2 | SRID=0;POLYGON((0 0,1 1,1 0,0 1,0 0)) |
+----+---------------------------------------+
```
