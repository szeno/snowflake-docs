Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_POLYGON\_TO\_CELLS\_STRINGS

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of VARCHAR values of the hexadecimal IDs of
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that have centroids contained by a Polygon
(specified by a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object).

See also:
:   [H3\_POLYGON\_TO\_CELLS\_STRINGS](/sql-reference/functions/h3_polygon_to_cells_strings) , [H3\_COVERAGE\_STRINGS](/sql-reference/functions/h3_coverage_strings)

## Syntax

Copy code

```
H3_POLYGON_TO_CELLS_STRINGS( <geography_polygon> , <target_resolution> )
```

## Arguments

`geography_polygon`
:   A GEOGRAPHY object that represents a Polygon.

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) that specifies the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cells.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an array of VARCHAR values for the hexadecimal IDs of the H3 cells that have centroids contained in the specified input
Polygon.

## Usage notes

- The function uses planar approximation, which treats points on the Earth’s surface as if they were connected by straight lines,
  rather than curved arcs. If you need a spherical approximation, use [H3\_COVERAGE\_STRINGS](/sql-reference/functions/h3_coverage_strings) instead.
- A cell is considered to be within the Polygon if its centroid is contained by the Polygon.

## Examples

The following example returns an ARRAY of VARCHAR values representing the hexadecimal IDs of H3 cells that have centroids
contained in the specified Polygon.

Copy code

```
SELECT H3_POLYGON_TO_CELLS_STRINGS(
  TO_GEOGRAPHY(
    'POLYGON((-122.481889 37.826683,-122.479487 37.808548,-122.474150 37.808904,-122.476510 37.826935,-122.481889 37.826683))'),
  9) AS h3_cells_in_polygon;
```

```
+----------------------+
| H3_CELLS_IN_POLYGON  |
|----------------------|
| [                    |
|   "8928308715bffff", |
|   "89283087397ffff", |
|   "89283087023ffff", |
|   "892830870abffff", |
|   "89283087027ffff", |
|   "89283087033ffff", |
|   "8928308702fffff", |
|   "892830870bbffff", |
|   "89283087037ffff"  |
| ]                    |
+----------------------+
```
