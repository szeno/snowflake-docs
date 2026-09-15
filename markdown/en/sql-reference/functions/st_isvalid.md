Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ISVALID

Returns TRUE if the specified [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object represents a
[valid shape](/sql-reference/data-types-geospatial#label-geospatial-invalid-shape-handling-intro). Examples of
invalid shapes include shapes with self-intersections and spikes.

## Syntax

Copy code

```
ST_ISVALID( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a BOOLEAN value.

## Usage notes

- ST\_ISVALID only checks for the validity of a shape. It doesn’t modify data. When constructing objects from
  spatial formats (such as WKT, WKB, EWKT, EWKB, or GeoJSON), conversion functions (for example, [TO\_GEOGRAPHY](/sql-reference/functions/to_geography),
  [TO\_GEOMETRY](/sql-reference/functions/to_geometry), [ST\_GEOGRAPHYFROMWKT](/sql-reference/functions/st_geographyfromwkt), or [ST\_GEOMETRYFROMWKT](/sql-reference/functions/st_geometryfromwkt)) parse input and by default
  attempt to validate or repair shapes. If a conversion function can’t repair a shape, it returns
  an error unless you accept invalid shapes.
- To ingest data that might be invalid (for example, data that you plan to correct later), specify TRUE for the
  additional `allow_invalid` argument when you call the conversion function to allow an invalid shape.
  You can then use the ST\_ISVALID function to flag invalid rows in a table.
- Some geospatial functions might return an error or unusable results when given invalid shapes. Use the
  ST\_ISVALID function to check validity. You can correct invalid shapes before performing spatial analytics.
- When shapes are invalid, simple corrections include buffering with a small positive or negative distance
  (for example, to remove tiny spikes or resolve self-intersections) and then rechecking validity using the
  ST\_ISVALID function.

## Examples

The following examples use the ST\_ISVALID function.

Determine whether a polygon is a valid shape:

Copy code

```
SELECT ST_ISVALID(
    TO_GEOGRAPHY('POLYGON((-93.086 37.557,-86.699 37.497,-93.198 35.123,-93.086 37.557))')
  ) AS is_valid;
```

```
+----------+
| IS_VALID |
|----------|
| True     |
+----------+
```

Copy code

```
SELECT ST_ISVALID(
    TO_GEOGRAPHY( 'POLYGON((-92.799 37.601,-88.240 37.617,-92.733 36.198,-88.305 36.171,-92.799 37.601))', TRUE)
  ) AS is_valid;
```

```
+----------+
| IS_VALID |
|----------|
| False    |
+----------+
```

Correct an invalid shape by using the [ST\_BUFFER](/sql-reference/functions/st_buffer) function to add small buffer:

Copy code

```
WITH g AS (
  SELECT TO_GEOMETRY('POLYGON((0 0, 2 2, 2 0, 0 2, 0 0))', TRUE) AS geom
)
SELECT ST_ISVALID(geom) AS is_valid_before_buffer,
  ST_ISVALID(ST_BUFFER(geom, -0.001)) AS is_valid_after_buffer
  FROM g;
```

```
+------------------------+-----------------------+
| IS_VALID_BEFORE_BUFFER | IS_VALID_AFTER_BUFFER |
|------------------------+-----------------------|
| False                  | True                  |
+------------------------+-----------------------+
```
