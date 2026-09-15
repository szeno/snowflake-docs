Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_GRID\_DISK

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of the IDs of the [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that
are within the specified grid distance (`k_value`) of the given cell. The grid distance, often written as `k` in the H3
model, is the number of steps between cells in the H3 grid. The IDs in the returned ARRAY are INTEGER values (if an INTEGER
value was provided as the input ID) or VARCHAR values containing the hexadecimal IDs (if a hexadecimal ID was provided
as the input ID).

## Syntax

Copy code

```
H3_GRID_DISK( <cell_id> , <k_value> )
```

## Arguments

`cell_id`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR that represents the cell ID in hexadecimal format.

`k_value`
:   An INTEGER that represents the grid distance `k`: the number of steps between cells in the H3 grid. You must specify a
    non-negative value. For example, `0` returns only the specified cell, and `1` returns that cell plus its immediate
    neighbors.

## Returns

Returns an ARRAY of the IDs of H3 cells that are within the distance `k_value` from the cell specified by
`cell_id`. The IDs are in one of the following formats:

- If `cell_id` is an INTEGER value, the function returns the IDs as INTEGER values.
- If `cell_id` is a VARCHAR value containing the hexadecimal ID, the function returns the hexadecimal IDs as VARCHAR
  values.

## Examples

The following example returns an ARRAY of the IDs of H3 cells within the grid distance of 1 from the cell with the ID
`617540519050084351` (specified as an INTEGER value).

Copy code

```
SELECT H3_GRID_DISK(617540519050084351, 1);
```

```
+-------------------------------------+
| H3_GRID_DISK(617540519050084351, 1) |
|-------------------------------------|
| [                                   |
|   617540519050084351,               |
|   617540519051657215,               |
|   617540519050608639,               |
|   617540519050870783,               |
|   617540519050346495,               |
|   617540519051395071,               |
|   617540519051132927                |
| ]                                   |
+-------------------------------------+
```

The following example returns an ARRAY of the IDs of H3 cells within the grid distance of 1 from the cell with the ID
`891f1d48863ffff` (specified as a VARCHAR value).

Copy code

```
SELECT H3_GRID_DISK('891f1d48863ffff', 1);
```

```
+------------------------------------+
| H3_GRID_DISK('891F1D48863FFFF', 1) |
|------------------------------------|
| [                                  |
|   "891f1d48863ffff",               |
|   "891f1d4887bffff",               |
|   "891f1d4886bffff",               |
|   "891f1d4886fffff",               |
|   "891f1d48867ffff",               |
|   "891f1d48877ffff",               |
|   "891f1d48873ffff"                |
| ]                                  |
+------------------------------------+
```
