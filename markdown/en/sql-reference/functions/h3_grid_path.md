Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_GRID\_PATH

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of the IDs of the [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cells that represent
the line between two cells. The IDs in the returned ARRAY are INTEGER values (if INTEGER values were provided as the input IDs)
or VARCHAR values containing the hexadecimal IDs (if hexadecimal IDs were provided as the input IDs).

## Syntax

Copy code

```
H3_GRID_PATH( <cell_id_1> , <cell_id_2> )
```

## Arguments

`cell_id_1`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR that represents the cell ID in hexadecimal format.

`cell_id_2`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR that represents the cell ID in hexadecimal format.

## Returns

Returns an ARRAY of the IDs of H3 cells that represent the line between the cells specified by `cell_id_1` and
`cell_id_2`. The IDs are in one of the following formats:

- If `cell_id_1` and `cell_id_2` are INTEGER values, the function returns the IDs as INTEGER values.
- If `cell_id_1` and `cell_id_2` are VARCHAR values containing the hexadecimal IDs, the function returns the
  hexadecimal IDs as VARCHAR values.

## Usage notes

The two input cell IDs must use the same resolution.

## Examples

The following example returns an ARRAY of the IDs of H3 cells that represent the line between the cells with the IDs
`617540519103561727` and `617540519052967935` (both specified as INTEGER values).

Copy code

```
SELECT H3_GRID_PATH(617540519103561727, 617540519052967935);
```

```
+------------------------------------------------------+
| H3_GRID_PATH(617540519103561727, 617540519052967935) |
|------------------------------------------------------|
| [                                                    |
|   617540519103561727,                                |
|   617540519046414335,                                |
|   617540519047462911,                                |
|   617540519044055039,                                |
|   617540519045103615,                                |
|   617540519052967935                                 |
| ]                                                    |
+------------------------------------------------------+
```

The following example returns an ARRAY of the IDs of H3 cells that represent the line between the cells with the IDs
`891f1d48b93ffff` and `891f1d4888fffff` (both specified as VARCHAR values).

Copy code

```
SELECT H3_GRID_PATH('891f1d48b93ffff', '891f1d4888fffff');
```

```
+----------------------------------------------------+
| H3_GRID_PATH('891F1D48B93FFFF', '891F1D4888FFFFF') |
|----------------------------------------------------|
| [                                                  |
|   "891f1d48b93ffff",                               |
|   "891f1d4882bffff",                               |
|   "891f1d4883bffff",                               |
|   "891f1d48807ffff",                               |
|   "891f1d48817ffff",                               |
|   "891f1d4888fffff"                                |
| ]                                                  |
+----------------------------------------------------+
```
