Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_TRY\_GRID\_PATH

A special version of [H3\_GRID\_PATH](/sql-reference/functions/h3_grid_path) that returns NULL if an error occurs when it
attempts to return an array of VARIANT values that contain the IDs of the
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that represent the line between two cells.

## Syntax

Copy code

```
H3_TRY_GRID_PATH( <cell_id_1> , <cell_id_2> )
```

## Arguments

`cell_id_1`
:   An INTEGER value that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR value that represents the cell ID
    in hexadecimal format.

`cell_id_2`
:   An INTEGER value that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR value that represents the cell ID
    in hexadecimal format.

## Returns

Returns a value of the ARRAY data type or NULL.

- If the function performs a successful calculation, returns an array of VARIANT values that contain the IDs of H3 cells
  that represent the line between the cells specified by `cell_id_1` and `cell_id_2`. For information about
  the format of the IDs, see [H3\_GRID\_PATH](/sql-reference/functions/h3_grid_path).
- If the line cannot be calculated (for example, when two cells belong to non-neighboring
  [base cells](https://h3geo.org/docs/library/index/cell/)), returns NULL without reporting an error.

## Usage notes

See [H3\_GRID\_PATH](/sql-reference/functions/h3_grid_path) for the usage notes.

## Examples

The following example attempts to return a line between two cells. Because the cells belong to non-neighboring
base cells, the function fails to return the line and returns NULL.

Copy code

```
SELECT H3_TRY_GRID_PATH('813d7ffffffffff', '81343ffffffffff');
```

```
+--------------------------------------------------------+
| H3_TRY_GRID_PATH('813D7FFFFFFFFFF', '81343FFFFFFFFFF') |
|--------------------------------------------------------|
| NULL                                                   |
+--------------------------------------------------------+
```

For examples that successfully calculate the path between two H3 cells, see [H3\_GRID\_PATH](/sql-reference/functions/h3_grid_path).
