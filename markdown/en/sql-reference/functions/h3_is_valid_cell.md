Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_IS\_VALID\_CELL

Returns TRUE if the input represents a valid [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell.

## Syntax

Copy code

```
H3_IS_VALID_CELL( <cell_id> )
```

## Arguments

`cell_id`
:   An INTEGER value that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR value that represents the cell ID
    in hexadecimal format.

## Returns

Returns a BOOLEAN or NULL.

- The value is TRUE if the input represents a valid H3 cell. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

The following example specifies an integer that represents a valid H3 cell.

Copy code

```
SELECT H3_IS_VALID_CELL(613036919424548863);
```

```
+--------------------------------------+
| H3_IS_VALID_CELL(613036919424548863) |
|--------------------------------------|
| True                                 |
+--------------------------------------+
```

The following example specifies a string that does not represent a valid H3 cell.

Copy code

```
SELECT H3_IS_VALID_CELL('Invalid Cell');
```

```
+----------------------------------+
| H3_IS_VALID_CELL('INVALID CELL') |
|----------------------------------|
| False                            |
+----------------------------------+
```
