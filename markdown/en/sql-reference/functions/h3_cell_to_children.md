Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_CELL\_TO\_CHILDREN

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of the INTEGER IDs of the children of an
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell for a given resolution.

See also:
:   [H3\_CELL\_TO\_CHILDREN\_STRING](/sql-reference/functions/h3_cell_to_children_string) , [H3\_CELL\_TO\_PARENT](/sql-reference/functions/h3_cell_to_parent)

## Syntax

Copy code

```
H3_CELL_TO_CHILDREN( <cell_id> , <target_resolution> )
```

## Arguments

`cell_id`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)).

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) specifying the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cells.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an array of the INTEGER values of the IDs of the children of an H3 cell at the specified target resolution.

## Examples

The following example returns an array of the IDs of the children of the H3 cell with the ID `613036919424548863`:

Copy code

```
SELECT H3_CELL_TO_CHILDREN(613036919424548863, 9);
```

```
+--------------------------------------------+
| H3_CELL_TO_CHILDREN(613036919424548863, 9) |
|--------------------------------------------|
| [                                          |
|   617540519050084351,                      |
|   617540519050346495,                      |
|   617540519050608639,                      |
|   617540519050870783,                      |
|   617540519051132927,                      |
|   617540519051395071,                      |
|   617540519051657215                       |
| ]                                          |
+--------------------------------------------+
```
