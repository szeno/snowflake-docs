Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_TRY\_COVERAGE

A special version of [H3\_COVERAGE](/sql-reference/functions/h3_coverage) that returns NULL if an error occurs when it
attempts to return an [array](/sql-reference/data-types-semistructured#label-data-type-array) of IDs (as INTEGER values) identifying the minimal
set of [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that completely cover a shape (specified by a
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object).

## Syntax

Copy code

```
H3_TRY_COVERAGE( <geography_expression> , <target_resolution> )
```

## Arguments

`geography_expression`
:   A GEOGRAPHY object.

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) specifying the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cells.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an array of INTEGER values or NULL.

- If the function can perform a successful calculation, returns an array of INTEGER values for the IDs of
  the minimal set of H3 cells that completely cover the specified input shape.
- If the function cannot perform a successful calculation, returns NULL without reporting an error.

## Usage notes

See [H3\_COVERAGE](/sql-reference/functions/h3_coverage) for the usage notes.

## Examples

The following example attempts to return an array of IDs that identify the minimal set of [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3)
cells that completely cover a shape (specified by a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object). Because the array with
the cells that cover the given hexagon at the given resolution exceeds the allowed size limit, the function returns NULL.

Copy code

```
SELECT H3_TRY_COVERAGE(
  TO_GEOGRAPHY('POLYGON((-108.959 40.948,
                         -109.015 37.077,
                         -102.117 36.956,
                         -102.134 40.953,
                         -108.959 40.948))'
              ), 15) AS set_of_h3_cells_covering_polygon;
```

```
+----------------------------------+
| SET_OF_H3_CELLS_COVERING_POLYGON |
|----------------------------------|
| NULL                             |
+----------------------------------+
```

For examples that successfully return an array of IDs, see [H3\_COVERAGE](/sql-reference/functions/h3_coverage).
