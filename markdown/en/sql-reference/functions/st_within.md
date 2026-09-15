Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_WITHIN

Returns true if the first geospatial object is fully contained by the second geospatial object. In other words:

- The first [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object `g1` is fully contained by the second GEOGRAPHY object
  `g2`.
- The first [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object `g1` is fully contained by the second GEOMETRY object
  `g2`.

Calling `ST_WITHIN(g1, g2)` is equivalent to calling `ST_CONTAINS(g2, g1)`.

Although ST\_COVEREDBY and ST\_WITHIN might seem similar, the two functions have subtle differences. For details on the differences
between “covered by” and “within”, see the
[Dimensionally Extended 9-Intersection Model (DE-9IM)](https://en.wikipedia.org/wiki/DE-9IM).

Note

This function does not support using a GeometryCollection or FeatureCollection as input values.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

See also:
:   [ST\_CONTAINS](/sql-reference/functions/st_contains) , [ST\_COVEREDBY](/sql-reference/functions/st_coveredby)

## Syntax

Copy code

```
ST_WITHIN( <geography_expression_1> , <geography_expression_2> )

ST_WITHIN( <geometry_expression_1> , <geometry_expression_2> )
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

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_WITHIN function:

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
> SELECT ST_WITHIN(g1, g2) 
>     FROM geospatial_table_01;
> +-------------------+
> | ST_WITHIN(G1, G2) |
> |-------------------|
> | False             |
> +-------------------+
> ```
