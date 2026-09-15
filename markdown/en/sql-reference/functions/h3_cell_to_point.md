Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_CELL\_TO\_POINT

Returns the [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object representing the Point that is the centroid of an
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell.

See also:
:   [H3\_POINT\_TO\_CELL](/sql-reference/functions/h3_point_to_cell) , [H3\_POINT\_TO\_CELL\_STRING](/sql-reference/functions/h3_point_to_cell_string)

## Syntax

Copy code

```
H3_CELL_TO_POINT( <cell_id> )
```

## Arguments

`cell_id`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR that represents the cell ID in hexadecimal format.

## Returns

Returns a GEOGRAPHY object for the Point that represents the centroid of the H3 cell with the specified ID.

## Examples

The following example returns the GEOGRAPHY object for the Point that represents the centroid of the H3 cell containing the
Brandenburg Gate. The example specifies the H3 cell ID as an INTEGER value.

Copy code

```
SELECT H3_CELL_TO_POINT(613036919424548863);
```

```
+--------------------------------------+
| H3_CELL_TO_POINT(613036919424548863) |
|--------------------------------------|
| {                                    |
|   "coordinates": [                   |
|     1.337676791184706e+01,           |
|     5.251638386722465e+01            |
|   ],                                 |
|   "type": "Point"                    |
| }                                    |
+--------------------------------------+
```

The following example specifies the hexadecimal value of the H3 cell ID as a VARCHAR to return the same coordinates as the previous
example.

Copy code

```
SELECT H3_CELL_TO_POINT('881F1D4887FFFFF');
```

```
+-------------------------------------+
| H3_CELL_TO_POINT('881F1D4887FFFFF') |
|-------------------------------------|
| {                                   |
|   "coordinates": [                  |
|     1.337676791184706e+01,          |
|     5.251638386722465e+01           |
|   ],                                |
|   "type": "Point"                   |
| }                                   |
+-------------------------------------+
```
