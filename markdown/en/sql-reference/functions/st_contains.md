Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_CONTAINS

Returns TRUE if a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object is
completely inside another object of the same type.

More strictly, object g1 contains object g2 if and only if no points of g2 lie in the exterior of g1, and at least one
point of the interior of B lies in the interior of A. There are certain subtleties in this definition that are not
immediately obvious. For more details on what “contains” means, see the
[Dimensionally Extended 9-Intersection Model (DE-9IM)](https://en.wikipedia.org/wiki/DE-9IM).

Although ST\_COVERS and ST\_CONTAINS might seem similar, the two functions have subtle differences. For details on the differences
between “covers” and “contains”, see the
[Dimensionally Extended 9-Intersection Model (DE-9IM)](https://en.wikipedia.org/wiki/DE-9IM).

Note

This function does not support using a GeometryCollection or FeatureCollection as input values.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

See also:
:   [ST\_WITHIN](/sql-reference/functions/st_within) , [ST\_COVERS](/sql-reference/functions/st_covers) , [ST\_COVEREDBY](/sql-reference/functions/st_coveredby)

## Syntax

Copy code

```
ST_CONTAINS( <geography_expression_1> , <geography_expression_2> )

ST_CONTAINS( <geometry_expression_1> , <geometry_expression_2> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object that is not a GeometryCollection or FeatureCollection.

`geography_expression_2`
:   A GEOGRAPHY object that is not a GeometryCollection or FeatureCollection.

`geometry_expression_1`
:   A GEOMETRY object that is not a GeometryCollection or FeatureCollection.

`geometry_expression_2`
:   A GEOMETRY object that is not a GeometryCollection or FeatureCollection.

## Returns

BOOLEAN.

## Usage notes

- For GEOMETRY objects, the function reports an error if the two input GEOMETRY objects have different SRIDs.

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_CONTAINS function:

> Copy code
>
> ```
> create table geospatial_table_01 (g1 GEOGRAPHY, g2 GEOGRAPHY);
> insert into geospatial_table_01 (g1, g2) values 
>     ('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))', 'POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))');
> ```
>
> Copy code
>
> ```
> SELECT ST_CONTAINS(g1, g2) 
>     FROM geospatial_table_01;
> +---------------------+
> | ST_CONTAINS(G1, G2) |
> |---------------------|
> | True                |
> +---------------------+
> ```

### GEOMETRY examples

The query below shows several examples of using ST\_CONTAINS. Note how ST\_CONTAINS determines that:

- The Polygon contains itself.
- The Polygon does not contain the LineString that is on its border.

  Copy code

  ```
  SELECT ST_CONTAINS(poly, poly_inside),
     ST_CONTAINS(poly, poly),
     ST_CONTAINS(poly, line_on_boundary),
     ST_CONTAINS(poly, line_inside)
    FROM (SELECT
   TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))') AS poly,
   TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))') AS poly_inside,
   TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)') AS line_on_boundary,
   TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)') AS line_inside);
  ```

  Copy code

  ```
  +--------------------------------+------------------------+------------------------------------+-------------------------------+
  | ST_CONTAINS(POLY, POLY_INSIDE) | ST_CONTAINS(POLY,POLY) | ST_CONTAINS(POLY,LINE_ON_BOUNDARY) | ST_CONTAINS(POLY,LINE_INSIDE) |
  |--------------------------------+------------------------+------------------------------------+-------------------------------|
  | True                           | True                   | False                              | True                          |
  +--------------------------------+------------------------+------------------------------------+-------------------------------+
  ```
