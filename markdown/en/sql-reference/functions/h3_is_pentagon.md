Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_IS\_PENTAGON

Returns TRUE if the boundary of an [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell represents a pentagon.

## Syntax

Copy code

```
H3_IS_PENTAGON( <cell_id> )
```

## Arguments

`cell_id`
:   An INTEGER value that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR value that represents the cell ID
    in hexadecimal format.

## Returns

Returns a BOOLEAN or NULL.

- The value is TRUE if the input represents a pentagon. Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

The following example specifies an integer that does not represent a pentagon.

Copy code

```
SELECT H3_IS_PENTAGON(613036919424548863);
```

```
+------------------------------------+
| H3_IS_PENTAGON(613036919424548863) |
|------------------------------------|
| False                              |
+------------------------------------+
```

The following example specifies a hexadecimal string that represents a pentagon.

Copy code

```
SELECT H3_IS_PENTAGON('804dfffffffffff');
```

```
+-----------------------------------+
| H3_IS_PENTAGON('804DFFFFFFFFFFF') |
|-----------------------------------|
| True                              |
+-----------------------------------+
```
