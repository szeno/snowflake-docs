Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_UNION\_AGG

Given a GEOGRAPHY column, returns a GEOGRAPHY object that represents the combined set of points that are in
at least one of the shapes represented by the objects in the column (that is, the union of the shapes).

See also:
:   [ST\_UNION](/sql-reference/functions/st_union) , [ST\_INTERSECTION\_AGG](/sql-reference/functions/st_intersection_agg)

## Syntax

Copy code

```
ST_UNION_AGG( <geography_column> )
```

## Arguments

`geography_column`
:   A GEOGRAPHY column.

## Returns

The function returns a value of type GEOGRAPHY.

## Examples

Create a table with a GEOMETRY column and insert data:

Copy code

```
CREATE OR REPLACE TABLE st_union_agg_demo_table (g GEOGRAPHY);

INSERT INTO st_union_agg_demo_table VALUES
  ('POINT(1 1)'),
  ('POINT(0 1)'),
  ('LINESTRING(0 0, 0 1)'),
  ('LINESTRING(0 0, 0 2)'),
  ('POLYGON((10 10, 11 11, 11 10, 10 10))'),
  ('POLYGON((10 10, 11 11, 11 10, 10 10))');
```

Use the ST\_UNION\_AGG function to return a GEOGRAPHY object that represents the combined set of points that are in
at least one of the shapes represented by the objects in the GEOGRAPHY column:

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';

SELECT ST_UNION_AGG(g) AS union_of_shapes
  FROM st_union_agg_demo_table;
```

```
+-------------------------------------------------------------------------------------------+
| UNION_OF_SHAPES                                                                           |
|-------------------------------------------------------------------------------------------|
| GEOMETRYCOLLECTION(POINT(1 1),LINESTRING(0 0,0 1,0 2),POLYGON((11 10,11 11,10 10,11 10))) |
+-------------------------------------------------------------------------------------------+
```
