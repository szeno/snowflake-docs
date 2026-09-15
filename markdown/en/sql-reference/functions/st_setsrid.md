Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_SETSRID

Returns a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that has its SRID (spatial reference system identifier) set to the
specified value.

Use this function to change the SRID without affecting the coordinates of the object. If you also need to
[change the coordinates to match the new SRS (spatial reference system)](/sql-reference/data-types-geospatial#label-geometry-change-srs), use
[ST\_TRANSFORM](/sql-reference/functions/st_transform) instead.

## Syntax

Copy code

```
ST_SETSRID( <geometry_expression> , <srid> )
```

## Arguments

`geometry_expression`
:   The argument must be an expression of type GEOMETRY.

`srid`
:   The SRID to set in the returned GEOMETRY object.

## Returns

The function returns a value of type GEOMETRY.

## Usage notes

## Examples

The following example creates and returns a GEOMETRY object that uses the SRID 4326:

> Copy code
>
> ```
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';
>
> SELECT ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326);
>
> +-----------------------------------------------+
> | ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326) |
> |-----------------------------------------------|
> | SRID=4326;POINT(13 51)                        |
> +-----------------------------------------------+
> ```
