Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_COVERAGE

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of IDs (as INTEGER values) identifying the minimal set of
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that completely cover a shape (specified by a
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object).

See also:
:   [H3\_COVERAGE\_STRINGS](/sql-reference/functions/h3_coverage_strings) , [H3\_POLYGON\_TO\_CELLS](/sql-reference/functions/h3_polygon_to_cells)

## Syntax

Copy code

```
H3_COVERAGE( <geography_expression> , <target_resolution> )
```

## Arguments

`geography_expression`
:   A GEOGRAPHY object.

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) specifying the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cells.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an ARRAY of INTEGER values for the IDs of the minimal set of H3 cells that have completely cover the specified input
shape.

## Usage notes

- The function uses spherical approximation, which treats points on the Earth’s surface as if they were connected by arcs, rather
  than straight lines. If you need a planar approximation, use [H3\_POLYGON\_TO\_CELLS](/sql-reference/functions/h3_polygon_to_cells) instead.
- A cell is included in the result set if its boundary intersects the input shape.
- When you apply [FLATTEN](/sql-reference/functions/flatten) to the ARRAY returned by the function,
  [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) each value explicitly to an integer.

## Examples

The following example returns an ARRAY of the IDs that identify the minimal set of H3 cells that completely cover the specified
Polygon.

Copy code

```
SELECT H3_COVERAGE(
  TO_GEOGRAPHY(
    'POLYGON((-122.481889 37.826683,-122.479487 37.808548,-122.474150 37.808904,-122.476510 37.826935,-122.481889 37.826683))'),
  8) AS set_of_h3_cells_covering_polygon;
```

```
+----------------------------------+
| SET_OF_H3_CELLS_COVERING_POLYGON |
|----------------------------------|
| [                                |
|   613196571542028287,            |
|   613196571548319743,            |
|   613196571598651391,            |
|   613196571539931135,            |
|   613196571560902655,            |
|   613196571550416895             |
| ]                                |
+----------------------------------+
```
