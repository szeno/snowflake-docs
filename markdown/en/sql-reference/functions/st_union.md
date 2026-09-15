Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_UNION

Given two input GEOGRAPHY objects, returns a GEOGRAPHY object that represents the combined set of shapes for both objects (i.e.
the union of the two shapes).

See also:
:   [ST\_UNION\_AGG](/sql-reference/functions/st_union_agg) , [ST\_INTERSECTION](/sql-reference/functions/st_intersection) , [ST\_DIFFERENCE](/sql-reference/functions/st_difference) , [ST\_SYMDIFFERENCE](/sql-reference/functions/st_symdifference)

## Syntax

Copy code

```
ST_UNION( <geography_expression_1> , <geography_expression_2> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object.

`geography_expression_2`
:   A GEOGRAPHY object.

## Returns

The function returns a value of type GEOGRAPHY.

## Usage notes

- If any vertex of one input object is on the boundary of the other input object (excluding the vertices), some points in the
  union might be represented more than once in the output,

  For example, in the following statement:

  Copy code

  ```
  SELECT ST_UNION(
    TO_GEOGRAPHY('POINT(1 1)'),
    TO_GEOGRAPHY('LINESTRING(1 0, 1 2)')
  );
  ```

  `POINT(1 1)` is on the boundary of `LINESTRING(1 0, 1 2)` but is not a vertex of it.

  In this example, ST\_UNION is not guaranteed to produce minimal output. The expected output should be the input linestring:

  Copy code

  ```
  LINESTRING(1 0, 1 2)
  ```

  But the actual output might be:

  Copy code

  ```
  GEOMETRYCOLLECTION(POINT(1 1),LINESTRING(1 0,1 1,1 2))
  ```

  where `POINT (1,1)` is represented twice in the output: once as the point itself and once as a point within the LineString.

## Examples

The following example returns a GEOGRAPHY object that represents the union of two input GEOGRAPHY objects:

> Copy code
>
> ```
> ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';
>
> SELECT ST_UNION(
>   TO_GEOGRAPHY('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))'),
>   TO_GEOGRAPHY('POLYGON((3 0, 3 4, 2 4, 1 3, 2 2, 1 1, 2 0, 3 0))')
> ) AS union_of_objects;
> ```

This example produces the following output:

> Copy code
>
> ```
> +-------------------------------------------------------------------------------------------------------------------------------------------+
> | UNION_OF_OBJECTS                                                                                                                          |
> |-------------------------------------------------------------------------------------------------------------------------------------------|
> | POLYGON((3 0,3 4,2 4,1.5 3.500399839,1 4,0 4,0 0,1 0,1.5 0.5000571198,2 0,3 0),(1.5 1.500171359,1 2,1.5 2.500285599,2 2,1.5 1.500171359)) |
> +-------------------------------------------------------------------------------------------------------------------------------------------+
> ```

The following images illustrate the differences in the areas that represent the input and output objects:

| Input | Output |
| --- | --- |
| Areas of input objects passed to ST_UNION | Areas of output objects returned by ST_UNION |

Expand

Show lessSee more
