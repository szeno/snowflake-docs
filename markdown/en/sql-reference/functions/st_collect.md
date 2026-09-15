Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_COLLECT

There are two forms of ST\_COLLECT:

- Scalar: This function combines two [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) objects into one.
- Aggregate: This function combines all the GEOGRAPHY objects in a column into one GEOGRAPHY object.

## Syntax

Copy code

```
Scalar:

    ST_COLLECT( <geography_expression_1> , <geography_expression_2> )

Aggregate:

    ST_COLLECT( <geography_expression_1> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object.

`geography_expression_2`
:   A GEOGRAPHY object.

## Returns

The function returns a value of type GEOGRAPHY.

## Usage notes

- If g1 and g2 are both Point objects, the result is a MultiPoint object containing the two Points. Similarly,
  if g1 and g2 are both LineString objects, the result is a MultiLineString object. Etc.
- If g1 and g2 are different types of geospatial objects, or if at least one of the input GEOGRAPHY objects is a
  collection (e.g. MultiLineString, GeometryCollection, or FeatureCollection), then the result is a GeometryCollection
  containing both input objects.

## Examples

The queries below show both scalar and aggregate uses of the ST\_COLLECT function.

> Create and load the table:
>
> Copy code
>
> ```
> CREATE TABLE geo3 (g1 GEOGRAPHY, g2 GEOGRAPHY);
> INSERT INTO geo3 (g1, g2) VALUES
>     ( 'POINT(-180 -90)', 'POINT(-45 -45)' ),
>     ( 'POINT(   0   0)', 'POINT(-60 -60)' ),
>     ( 'POINT(+180 +90)', 'POINT(+45 +45)' );
> ```
>
> This calls ST\_COLLECT as a scalar function to create a MultiPoint value that contains both points in the same row:
>
> Copy code
>
> ```
> -- Scalar function:
> SELECT ST_COLLECT(g1, g2) FROM geo3;
> +------------------------+
> | ST_COLLECT(G1, G2)     |
> |------------------------|
> | {                      |
> |   "coordinates": [     |
> |     [                  |
> |       -180,            |
> |       -90              |
> |     ],                 |
> |     [                  |
> |       -45,             |
> |       -45              |
> |     ]                  |
> |   ],                   |
> |   "type": "MultiPoint" |
> | }                      |
> | {                      |
> |   "coordinates": [     |
> |     [                  |
> |       0,               |
> |       0                |
> |     ],                 |
> |     [                  |
> |       -60,             |
> |       -60              |
> |     ]                  |
> |   ],                   |
> |   "type": "MultiPoint" |
> | }                      |
> | {                      |
> |   "coordinates": [     |
> |     [                  |
> |       180,             |
> |       90               |
> |     ],                 |
> |     [                  |
> |       45,              |
> |       45               |
> |     ]                  |
> |   ],                   |
> |   "type": "MultiPoint" |
> | }                      |
> +------------------------+
> ```
>
> This calls ST\_COLLECT as an aggregate function to create a MultiPoint value that contains all the points in the
> same column:
>
> Copy code
>
> ```
> -- Aggregate function:
> SELECT ST_COLLECT(g1), ST_COLLECT(g2) FROM geo3;
> +------------------------+------------------------+
> | ST_COLLECT(G1)         | ST_COLLECT(G2)         |
> |------------------------+------------------------|
> | {                      | {                      |
> |   "coordinates": [     |   "coordinates": [     |
> |     [                  |     [                  |
> |       -180,            |       -45,             |
> |       -90              |       -45              |
> |     ],                 |     ],                 |
> |     [                  |     [                  |
> |       0,               |       -60,             |
> |       0                |       -60              |
> |     ],                 |     ],                 |
> |     [                  |     [                  |
> |       180,             |       45,              |
> |       90               |       45               |
> |     ]                  |     ]                  |
> |   ],                   |   ],                   |
> |   "type": "MultiPoint" |   "type": "MultiPoint" |
> | }                      | }                      |
> +------------------------+------------------------+
> ```
>
> This calls ST\_COLLECT first as an aggregate function on each column to create MultiPoint values that contains all
> the points in each column, and then calls ST\_COLLECT on those two MultiPoint values to create a GeometryCollection
> that contains all the points in both columns. The resulting GeometryCollection is hierarchical.
>
> Copy code
>
> ```
> -- Aggregate and then Collect:
> SELECT ST_COLLECT(ST_COLLECT(g1), ST_COLLECT(g2)) FROM geo3;
> +--------------------------------------------+
> | ST_COLLECT(ST_COLLECT(G1), ST_COLLECT(G2)) |
> |--------------------------------------------|
> | {                                          |
> |   "geometries": [                          |
> |     {                                      |
> |       "coordinates": [                     |
> |         [                                  |
> |           -180,                            |
> |           -90                              |
> |         ],                                 |
> |         [                                  |
> |           0,                               |
> |           0                                |
> |         ],                                 |
> |         [                                  |
> |           180,                             |
> |           90                               |
> |         ]                                  |
> |       ],                                   |
> |       "type": "MultiPoint"                 |
> |     },                                     |
> |     {                                      |
> |       "coordinates": [                     |
> |         [                                  |
> |           -45,                             |
> |           -45                              |
> |         ],                                 |
> |         [                                  |
> |           -60,                             |
> |           -60                              |
> |         ],                                 |
> |         [                                  |
> |           45,                              |
> |           45                               |
> |         ]                                  |
> |       ],                                   |
> |       "type": "MultiPoint"                 |
> |     }                                      |
> |   ],                                       |
> |   "type": "GeometryCollection"             |
> | }                                          |
> +--------------------------------------------+
> ```
