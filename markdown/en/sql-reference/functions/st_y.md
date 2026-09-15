Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_Y

Returns the latitude (Y coordinate) of a Point represented by a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

## Syntax

Copy code

```
ST_Y( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of the type GEOGRAPHY or GEOMETRY and must contain a Point.

## Returns

Returns a REAL value.

## Usage notes

- Issues an error if the argument is not a Point.

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_X and ST\_Y functions with VARCHAR data:

> Copy code
>
> ```
> SELECT ST_X(ST_MAKEPOINT(37.5, 45.5)), ST_Y(ST_MAKEPOINT(37.5, 45.5));
> +--------------------------------+--------------------------------+
> | ST_X(ST_MAKEPOINT(37.5, 45.5)) | ST_Y(ST_MAKEPOINT(37.5, 45.5)) |
> |--------------------------------+--------------------------------|
> |                           37.5 |                           45.5 |
> +--------------------------------+--------------------------------+
> ```

This shows use of the ST\_X and ST\_Y functions with NULL values:

> Copy code
>
> ```
> SELECT
>     ST_X(ST_MAKEPOINT(NULL, NULL)), ST_X(NULL),
>     ST_Y(ST_MAKEPOINT(NULL, NULL)), ST_Y(NULL)
>     ;
> +--------------------------------+------------+--------------------------------+------------+
> | ST_X(ST_MAKEPOINT(NULL, NULL)) | ST_X(NULL) | ST_Y(ST_MAKEPOINT(NULL, NULL)) | ST_Y(NULL) |
> |--------------------------------+------------+--------------------------------+------------|
> |                           NULL |       NULL |                           NULL |       NULL |
> +--------------------------------+------------+--------------------------------+------------+
> ```
