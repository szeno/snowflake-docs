Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_COMPACT\_CELLS

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) values that
contain the INTEGER IDs of fewer, larger [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that cover
the same area as the H3 cells in the input. For information about compacted cells, see [Indexing](https://h3geo.org/docs/highlights/indexing/).

## Syntax

Copy code

```
H3_COMPACT_CELLS( <array_of_cell_ids> )
```

## Arguments

`array_of_cell_ids`
:   An array of VARIANT values that contain the INTEGER values that represent H3 cell IDs ([indexes](https://h3geo.org/docs/core-library/h3Indexing)).

## Returns

Returns a value of the ARRAY data type or NULL.

- If the input is an array of INTEGER values, returns an array that consists of VARIANT values that represent a
  compacted set of H3 cells. The VARIANT values contain the INTEGER values that represent H3 cell IDs.
- If the input is NULL, returns NULL without reporting an error.

## Usage notes

- All of the INTEGER values in the input must represent valid H3 cells.
- All of the H3 cells in the input must have the same resolution.
- The H3 cells in the input must cover unique areas without overlapping. Duplicate H3 cells are not allowed.

## Examples

The following example compacts a set of H3 cells, returning cells at a lower resolution that represent the same area.

Copy code

```
SELECT H3_COMPACT_CELLS(
  [
    622236750562230271,
    622236750562263039,
    622236750562295807,
    622236750562328575,
    622236750562361343,
    622236750562394111,
    622236750562426879,
    622236750558396415
  ]
) AS compacted;
```

```
+-----------------------+
| COMPACTED             |
|-----------------------|
| [                     |
|   622236750558396415, |
|   617733150935089151  |
| ]                     |
+-----------------------+
```
