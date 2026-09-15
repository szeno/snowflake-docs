Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_COMPACT\_CELLS\_STRINGS

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) values that contain
the VARCHAR hexadecimal IDs of fewer, larger [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that cover the
same area as the H3 cells in the input. For information about compacted cells, see [Indexing](https://h3geo.org/docs/highlights/indexing/).

## Syntax

Copy code

```
H3_COMPACT_CELLS_STRINGS( <array_of_cell_ids> )
```

## Arguments

`array_of_cell_ids`
:   An array of VARIANT values that contain the VARCHAR hexadecimal values that represent H3 cell IDs ([indexes](https://h3geo.org/docs/core-library/h3Indexing)).

## Returns

Returns a value of the ARRAY data type or NULL.

- If the input is an array of VARCHAR hexadecimal values, returns an array that consists of VARIANT values that represent a
  compacted set of H3 cells. The VARIANT values contain the VARCHAR hexadecimal values that represent H3 cell IDs.
- If the input is NULL, returns NULL without reporting an error.

## Usage notes

- All of the VARCHAR hexadecimal values in the input must represent valid H3 cells.
- All of the H3 cells in the input must have the same resolution.
- The H3 cells in the input must cover unique areas without overlapping. Duplicate H3 cells are not allowed.

## Examples

The following example compacts a set of H3 cells, returning cells at a lower resolution that represent the same area.

Copy code

```
SELECT H3_COMPACT_CELLS_STRINGS(
  [
    '8a2a10705507fff',
    '8a2a1070550ffff',
    '8a2a10705517fff',
    '8a2a1070551ffff',
    '8a2a10705527fff',
    '8a2a1070552ffff',
    '8a2a10705537fff',
    '8a2a10705cdffff'
    ]
  ) AS compacted;
```

```
+----------------------+
| COMPACTED            |
|----------------------|
| [                    |
|   "8a2a10705cdffff", |
|   "892a1070553ffff"  |
| ]                    |
+----------------------+
```
