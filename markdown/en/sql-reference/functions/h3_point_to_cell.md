Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_POINT\_TO\_CELL

Returns the INTEGER value of an [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell ID for a Point (specified by a
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object) at a given resolution.

See also:
:   [H3\_POINT\_TO\_CELL\_STRING](/sql-reference/functions/h3_point_to_cell_string) , [H3\_CELL\_TO\_POINT](/sql-reference/functions/h3_cell_to_point)

## Syntax

Copy code

```
H3_POINT_TO_CELL( <geography_point> , <target_resolution> )
```

## Arguments

`geography_point`
:   A GEOGRAPHY object that represents a Point.

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) that specifies the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cell.

    Specifying any other INTEGER value results in an error.

## Returns

Returns an INTEGER value that corresponds to the H3 cell ID for the given location and resolution.

## Examples

The following example returns the H3 cell ID for the Brandenburg Gate at resolution 8.

Copy code

```
SELECT H3_POINT_TO_CELL(ST_POINT(13.377704, 52.516262), 8);
```

```
+-----------------------------------------------------+
| H3_POINT_TO_CELL(ST_POINT(13.377704, 52.516262), 8) |
|-----------------------------------------------------|
|                                  613036919424548863 |
+-----------------------------------------------------+
```

The following example demonstrates that you cannot specify a resolution outside of 0 through 15.

Copy code

```
SELECT H3_POINT_TO_CELL(ST_POINT(13.377704, 52.516262), 18);
```

```
100410 (P0000): Invalid H3 resolution value: 18. Resolution must be between 0 (coarsest) and 15 (finest).
```
