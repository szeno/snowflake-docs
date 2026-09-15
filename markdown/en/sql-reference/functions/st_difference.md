Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_DIFFERENCE

Given two input GEOGRAPHY objects, returns a GEOGRAPHY object that represents the points in the first object that are not in the
second object (i.e. the difference between the two objects).

See also:
:   [ST\_INTERSECTION](/sql-reference/functions/st_intersection) , [ST\_UNION](/sql-reference/functions/st_union) , [ST\_SYMDIFFERENCE](/sql-reference/functions/st_symdifference)

## Syntax

Copy code

```
ST_DIFFERENCE( <geography_expression_1> , <geography_expression_2> )
```

## Arguments

`geography_expression_1`
:   A GEOGRAPHY object.

`geography_expression_2`
:   A GEOGRAPHY object.

## Returns

The function returns a value of type GEOGRAPHY.

If all points of `geography_expression_1` are in `geography_expression_2` (i.e. the difference is an empty set of
points), the function returns NULL.

## Usage notes

- If any vertex of one input object is on the boundary of the other input object (excluding the vertices), the output might not be
  accurate.
- The function is not guaranteed to produce normalized and/or minimal results. For example, an output could consist of a
  LineString containing several Points that actually forms just one straight segment.

## Examples

The following example returns a GEOGRAPHY object that represents the difference between two input GEOGRAPHY objects:

> Copy code
>
> ```
> ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';
>
> SELECT ST_DIFFERENCE(
>   TO_GEOGRAPHY('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))'),
>   TO_GEOGRAPHY('POLYGON((3 0, 3 4, 2 4, 1 3, 2 2, 1 1, 2 0, 3 0))'))
> AS difference_between_objects;
> ```

This example produces the following output:

> Copy code
>
> ```
> +-------------------------------------------------------------------------------------------------------------+
> | DIFFERENCE_BETWEEN_OBJECTS                                                                                  |
> |-------------------------------------------------------------------------------------------------------------|
> | POLYGON((1 1,1.5 1.500171359,1 2,1.5 2.500285599,1 3,1.5 3.500399839,1 4,0 4,0 0,1 0,1.5 0.5000571198,1 1)) |
> +-------------------------------------------------------------------------------------------------------------+
> ```

The following images illustrate the differences in the areas that represent the input and output objects:

| Input | Output |
| --- | --- |
| Areas of input objects passed to ST_DIFFERENCE | Areas of output objects returned by ST_DIFFERENCE |

Expand

Show lessSee more
