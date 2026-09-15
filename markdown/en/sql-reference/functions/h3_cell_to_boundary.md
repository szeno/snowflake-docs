Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_CELL\_TO\_BOUNDARY

Returns the [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object representing the boundary of an
[H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell.

## Syntax

Copy code

```
H3_CELL_TO_BOUNDARY( <cell_id> )
```

## Arguments

`cell_id`
:   An INTEGER that represents the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)), or a VARCHAR that represents the cell ID in hexadecimal format.

## Returns

Returns a GEOGRAPHY object that represents the boundary of the H3 cell with the specified ID.

## Examples

The following example returns the GEOGRAPHY object that represents the boundary of the H3 cell containing the Brandenburg Gate.
The example specifies the H3 cell ID as an INTEGER value.

Copy code

```
SELECT H3_CELL_TO_BOUNDARY(613036919424548863);
```

```
+-----------------------------------------+
| H3_CELL_TO_BOUNDARY(613036919424548863) |
|-----------------------------------------|
| {                                       |
|   "coordinates": [                      |
|     [                                   |
|       [                                 |
|         1.337146281884266e+01,          |
|         5.251934565725256e+01           |
|       ],                                |
|       [                                 |
|         1.336924966147084e+01,          |
|         5.251510220405509e+01           |
|       ],                                |
|       [                                 |
|         1.337455447449988e+01,          |
|         5.251214028989955e+01           |
|       ],                                |
|       [                                 |
|         1.338207263166664e+01,          |
|         5.251342164903257e+01           |
|       ],                                |
|       [                                 |
|         1.338428664751681e+01,          |
|         5.251766506194694e+01           |
|       ],                                |
|       [                                 |
|         1.337898164779325e+01,          |
|         5.252062715603375e+01           |
|       ],                                |
|       [                                 |
|         1.337146281884266e+01,          |
|         5.251934565725256e+01           |
|       ]                                 |
|     ]                                   |
|   ],                                    |
|   "type": "Polygon"                     |
| }                                       |
+-----------------------------------------+
```

The following example specifies the hexadecimal value of H3 cell ID as a VARCHAR to return the same coordinates as the previous
example.

Copy code

```
SELECT H3_CELL_TO_BOUNDARY('881F1D4887FFFFF');
```

```
+----------------------------------------+
| H3_CELL_TO_BOUNDARY('881F1D4887FFFFF') |
|----------------------------------------|
| {                                      |
|   "coordinates": [                     |
|     [                                  |
|       [                                |
|         1.337146281884266e+01,         |
|         5.251934565725256e+01          |
|       ],                               |
|       [                                |
|         1.336924966147084e+01,         |
|         5.251510220405509e+01          |
|       ],                               |
|       [                                |
|         1.337455447449988e+01,         |
|         5.251214028989955e+01          |
|       ],                               |
|       [                                |
|         1.338207263166664e+01,         |
|         5.251342164903257e+01          |
|       ],                               |
|       [                                |
|         1.338428664751681e+01,         |
|         5.251766506194694e+01          |
|       ],                               |
|       [                                |
|         1.337898164779325e+01,         |
|         5.252062715603375e+01          |
|       ],                               |
|       [                                |
|         1.337146281884266e+01,         |
|         5.251934565725256e+01          |
|       ]                                |
|     ]                                  |
|   ],                                   |
|   "type": "Polygon"                    |
| }                                      |
+----------------------------------------+
```
