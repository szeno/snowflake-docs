Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_DIMENSION

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
“dimension” of the value. The dimension of a GEOGRAPHY or GEOMETRY value is:

| Geospatial Object Type | Dimension |
| --- | --- |
| Point / MultiPoint | 0 |
| LineString / MultiLineString | 1 |
| Polygon / MultiPolygon | 2 |
| GeometryCollection | The dimension of the collection is equal to the maximum dimension of all the values inside the collection.  For example, if a GeometryCollection contains a Point (dimension 0) and a LineString (dimension 1), the dimension of the GeometryCollection is 1. |
| Feature | The dimension of the Feature is the same as the dimension of the geospatial object in the Feature. |
| FeatureCollection | The rule is the same as for GeometryCollection. |

Expand

Show lessSee more

The returned values (0, 1, 2) correspond to the common meaning of the word “dimension”: a polygon is a two-dimensional
object, a line is a one-dimensional object, and a point is a zero-dimensional object.

## Syntax

Copy code

```
ST_DIMENSION( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

A value of type INTEGER.

## Usage notes

- If the function is passed NULL, the function returns NULL.
- For GEOGRAPHY objects:

  - If the function is passed a GeometryCollection containing at least one NULL element and no non-NULL elements, the function
    returns 0.
  - If the function is passed a GeometryCollection containing at least one NULL element and at least one non-NULL element, the
    function returns the maximum dimension of the non-NULL elements.

  Note that some other systems return different values for NULL inputs.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_DIMENSION function:

> Copy code
>
> ```
> create table geospatial_table_02 (id INTEGER, g GEOGRAPHY);
> insert into geospatial_table_02 values
>     (1, 'POINT(-122.35 37.55)'),
>     (2, 'MULTIPOINT((-122.35 37.55), (0.00 -90.0))'),
>     (3, 'LINESTRING(-124.20 42.00, -120.01 41.99)'),
>     (4, 'LINESTRING(-124.20 42.00, -120.01 41.99, -122.5 42.01)'),
>     (5, 'MULTILINESTRING((-124.20 42.00, -120.01 41.99, -122.5 42.01), (10.0 0.0, 20.0 10.0, 30.0 0.0))'),
>     (6, 'POLYGON((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.00))'),
>     (7, 'MULTIPOLYGON(((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.0)), ((20.0 20.0, 40.0 20.0, 40.0 40.0, 20.0 40.0, 20.0 20.0)))')
>     ;
> ```
>
> Copy code
>
> ```
> select st_dimension(g) as dimension, st_aswkt(g)
>     from geospatial_table_02
>     order by dimension, id;
> +-----------+----------------------------------------------------------------------------------------------------+
> | DIMENSION | ST_ASWKT(G)                                                                                        |
> |-----------+----------------------------------------------------------------------------------------------------|
> |         0 | POINT(-122.35 37.55)                                                                               |
> |         0 | MULTIPOINT((-122.35 37.55),(0 -90))                                                                |
> |         1 | LINESTRING(-124.2 42,-120.01 41.99)                                                                |
> |         1 | LINESTRING(-124.2 42,-120.01 41.99,-122.5 42.01)                                                   |
> |         1 | MULTILINESTRING((-124.2 42,-120.01 41.99,-122.5 42.01),(10 0,20 10,30 0))                          |
> |         2 | POLYGON((-124.2 42,-120.01 41.99,-121.1 42.01,-124.2 42))                                          |
> |         2 | MULTIPOLYGON(((-124.2 42,-120.01 41.99,-121.1 42.01,-124.2 42)),((20 20,40 20,40 40,20 40,20 20))) |
> +-----------+----------------------------------------------------------------------------------------------------+
> ```

### GEOMETRY examples

The following example demonstrates the ST\_DIMENSION function:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_shapes (g GEOMETRY);
> INSERT INTO geometry_shapes VALUES
>     ('POINT(66 12)'),
>     ('MULTIPOINT((45 21), (12 54))'),
>     ('LINESTRING(40 60, 50 50, 60 40)'),
>     ('MULTILINESTRING((1 1, 32 17), (33 12, 73 49, 87.1 6.1))'),
>     ('POLYGON((17 17, 17 30, 30 30, 30 17, 17 17))'),
>     ('MULTIPOLYGON(((-10 0,0 10,10 0,-10 0)),((-10 40,10 40,0 20,-10 40)))'),
>     ('GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60, 50 50, 60 40), POINT(99 11))')
>     ;
>
> SELECT ST_DIMENSION(g), ST_ASWKT(g) FROM geometry_shapes;
> ```
>
> Copy code
>
> ```
> +-----------------+-------------------------------------------------------------------------------------------------+
> | ST_DIMENSION(G) | ST_ASWKT(G)                                                                                     |
> |-----------------+-------------------------------------------------------------------------------------------------|
> |               0 | POINT(66 12)                                                                                    |
> |               0 | MULTIPOINT((45 21),(12 54))                                                                     |
> |               1 | LINESTRING(40 60,50 50,60 40)                                                                   |
> |               1 | MULTILINESTRING((1 1,32 17),(33 12,73 49,87.1 6.1))                                             |
> |               2 | POLYGON((17 17,17 30,30 30,30 17,17 17))                                                        |
> |               2 | MULTIPOLYGON(((-10 0,0 10,10 0,-10 0)),((-10 40,10 40,0 20,-10 40)))                            |
> |               2 | GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60,50 50,60 40),POINT(99 11)) |
> +-----------------+-------------------------------------------------------------------------------------------------+
> ```
