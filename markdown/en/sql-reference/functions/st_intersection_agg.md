Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_INTERSECTION\_AGG

Given a GEOGRAPHY column, returns a GEOGRAPHY object that represents the shape containing the combined set of points that are
common to the shapes represented by the objects in the column (that is, the intersection of the shapes).

See also:
:   [ST\_INTERSECTION](/sql-reference/functions/st_intersection) , [ST\_UNION\_AGG](/sql-reference/functions/st_union_agg)

## Syntax

Copy code

```
ST_INTERSECTION_AGG( <geography_column> )
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
CREATE OR REPLACE TABLE st_intersection_agg_demo_table (g GEOGRAPHY);

INSERT INTO st_intersection_agg_demo_table VALUES
  ('POLYGON((10 10, 11 11, 11 10, 10 10))'),
  ('POLYGON((10 10, 11 10, 10 11, 10 10))'),
  ('POLYGON((10.5 10.5, 10 10, 11 10, 10.5 10.5))');
```

Use the ST\_INTERSECTION\_AGG function to return a GEOGRAPHY object that represents the intersection of
the shapes represented by the objects in the GEOGRAPHY column:

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';

SELECT ST_INTERSECTION_AGG(g) AS intersection_of_shapes
  FROM st_intersection_agg_demo_table;
```

```
+--------------------------------------------+
| INTERSECTION_OF_SHAPES                     |
|--------------------------------------------|
| POLYGON((10.5 10.5,10 10,11 10,10.5 10.5)) |
+--------------------------------------------+
```
