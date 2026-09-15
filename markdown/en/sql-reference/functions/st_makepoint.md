Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_MAKEPOINT , ST\_POINT

Constructs a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) object that represents a point with the specified longitude
and latitude.

See also:
:   [TO\_GEOGRAPHY](/sql-reference/functions/to_geography)

## Syntax

Copy code

```
ST_MAKEPOINT( <longitude> , <latitude> )
```

## Arguments

`longitude`
:   A REAL that represents the longitude.

`latitude`
:   A REAL that represents the latitude.

## Returns

The function returns a value of type GEOGRAPHY.

## Usage notes

- ST\_POINT is an alias for ST\_MAKEPOINT.

## Examples

This shows a simple use of the ST\_MAKEPOINT function:

> Copy code
>
> ```
> SELECT ST_MAKEPOINT(37.5, 45.5);
> +--------------------------+
> | ST_MAKEPOINT(37.5, 45.5) |
> |--------------------------|
> | POINT(37.5 45.5)         |
> +--------------------------+
> ```
