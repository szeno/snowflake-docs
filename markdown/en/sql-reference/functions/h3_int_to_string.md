Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_INT\_TO\_STRING

Converts the INTEGER value of an [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell ID to hexadecimal format.

See also:
:   [H3\_STRING\_TO\_INT](/sql-reference/functions/h3_string_to_int)

## Syntax

Copy code

```
H3_INT_TO_STRING( <cell_id> )
```

## Arguments

`cell_id`
:   An INTEGER value that represents the cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)).

## Returns

Returns the H3 cell ID in hexadecimal format.

## Examples

The following example converts the INTEGER value of an H3 cell ID to hexadecimal format.

Copy code

```
SELECT H3_INT_TO_STRING(617700171168612351);
```

```
+------------------------------------------------+
|          H3_INT_TO_STRING(617700171168612351)  |
|------------------------------------------------|
|                                89283087033FFFF |
+------------------------------------------------+
```
