Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_CELL\_TO\_CHILDREN\_STRING

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of the VARCHAR values containing the hexadecimal IDs of the children of an
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell for a given resolution.

See also:
:   [H3\_CELL\_TO\_CHILDREN](/sql-reference/functions/h3_cell_to_children) , [H3\_CELL\_TO\_PARENT](/sql-reference/functions/h3_cell_to_parent)

## Syntax

Copy code

```
H3_CELL_TO_CHILDREN_STRING( <cell_id> , <target_resolution> )
```

## Arguments

`cell_id`
:   A VARCHAR that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)) in hexadecimal format.

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) specifying the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cells.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an array of the VARCHAR values of the hexadecimal IDs of the children of an H3 cell at the specified target resolution.

## Examples

The following example returns an array of the IDs (in hexadecimal format) of the children of the H3 cell with the ID
`881F1D4887FFFFF` (in hexadecimal format):

Copy code

```
SELECT H3_CELL_TO_CHILDREN_STRING('881F1D4887FFFFF', 9);
```

```
+--------------------------------------------------+
| H3_CELL_TO_CHILDREN_STRING('881F1D4887FFFFF', 9) |
|--------------------------------------------------|
| [                                                |
|   "891f1d48863ffff",                             |
|   "891f1d48867ffff",                             |
|   "891f1d4886bffff",                             |
|   "891f1d4886fffff",                             |
|   "891f1d48873ffff",                             |
|   "891f1d48877ffff",                             |
|   "891f1d4887bffff"                              |
| ]                                                |
+--------------------------------------------------+
```
