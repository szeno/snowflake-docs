Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_STRING\_TO\_INT

Converts an [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell ID in hexadecimal format to an INTEGER value.

See also:
:   [H3\_INT\_TO\_STRING](/sql-reference/functions/h3_int_to_string)

## Syntax

Copy code

```
H3_STRING_TO_INT( <cell_id> )
```

## Arguments

`cell_id`
:   A VARCHAR that represents the cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)) in hexadecimal format.

## Returns

Returns an INTEGER value that represents the H3 cell ID.

## Examples

The following example converts an H3 cell ID from hexadecimal format to an INTEGER value.

Copy code

```
SELECT H3_STRING_TO_INT('89283087033FFFF');
```

```
+------------------------------------------------+
|            H3_STRING_TO_INT('89283087033FFFF') |
|------------------------------------------------|
|                             617700171168612351 |
+------------------------------------------------+
```
