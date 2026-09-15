Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial), [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_GEOMETRY

Parses an input and returns a value of type [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

This function is identical to [TO\_GEOMETRY](/sql-reference/functions/to_geometry) except that it returns NULL
when TO\_GEOMETRY would return an error.

See also:
:   [TO\_GEOMETRY](/sql-reference/functions/to_geometry)

## Syntax

Use one of the following:

Copy code

```
TRY_TO_GEOMETRY( <varchar_expression> [ , <srid> ] [ , <allow_invalid> ] )

TRY_TO_GEOMETRY( <binary_expression> [ , <srid> ] [ , <allow_invalid> ] )

TRY_TO_GEOMETRY( <variant_expression> [ , <srid> ] [ , <allow_invalid> ] )
```

## Arguments

**Required:**

`varchar_expression`
:   The argument must be a string expression that represents a valid geometric object in one of the following formats:

    - WKT (well-known text).
    - WKB (well-known binary) in hexadecimal format (without a leading `0x`).
    - EWKT (extended well-known text).
    - EWKB (extended well-known binary) in hexadecimal format (without a leading `0x`).
    - GeoJSON.

`binary_expression`
:   The argument must be a binary expression in WKB or EWKB format.

`variant_expression`
:   The argument must be an OBJECT in GeoJSON format.

**Optional:**

`srid`
:   The integer value of the SRID to use.

`allow_invalid`
:   If TRUE, specifies that the function returns a GEOGRAPHY or GEOMETRY object, even when the input shape isn’t valid and
    can’t be repaired. For more information, see [Specifying how invalid geospatial shapes are handled](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro).

## Returns

The function returns a value of type GEOMETRY or NULL when TO\_GEOMETRY would return an error.

## Usage notes

- Returns NULL if the input can’t be parsed as the appropriate supported format (WKT, WKB, EWKT, EWKB, GeoJSON).
- For GeoJSON, WKT, and WKB input, if the `srid` argument is not specified, the resulting GEOMETRY object has the SRID
  set to 0.

## Examples

This shows a simple use of the TRY\_TO\_GEOMETRY function with VARCHAR data:

Copy code

```
SELECT TRY_TO_GEOMETRY('INVALID INPUT');
```

Copy code

```
+----------------------------------+
| TRY_TO_GEOMETRY('INVALID INPUT') |
|----------------------------------|
| NULL                             |
+----------------------------------+
```

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

The following example tries to convert VARCHAR values in the `invalid_wkt_col` column to GEOMETRY values,
but the shapes aren’t valid:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT id, TRY_TO_GEOMETRY(invalid_wkt_col) AS g_or_null
  FROM demo_to_geometry;
```

```
+----+-----------+
| ID | G_OR_NULL |
|----+-----------|
|  1 | NULL      |
|  2 | NULL      |
+----+-----------+
```
