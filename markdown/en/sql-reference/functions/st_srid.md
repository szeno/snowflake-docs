Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_SRID

Returns the SRID (spatial reference system identifier) of a [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or
[GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object.

Currently, for any value of the GEOGRAPHY type, only SRID 4326 is supported and is returned.

## Syntax

Copy code

```
ST_SRID( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

Returns a value of type NUMBER(4,0).

## Usage notes

- Returns NULL if the input is NULL.

## Examples

### GEOGRAPHY examples

This shows a simple use of the ST\_SRID function:

> Copy code
>
> ```
> SELECT ST_SRID(ST_MAKEPOINT(37.5, 45.5));
> +-----------------------------------+
> | ST_SRID(ST_MAKEPOINT(37.5, 45.5)) |
> |-----------------------------------|
> |                              4326 |
> +-----------------------------------+
> ```

This shows use of the ST\_SRID function with NULL values:

> Copy code
>
> ```
> SELECT ST_SRID(ST_MAKEPOINT(NULL, NULL)), ST_SRID(NULL);
> +-----------------------------------+---------------+
> | ST_SRID(ST_MAKEPOINT(NULL, NULL)) | ST_SRID(NULL) |
> |-----------------------------------+---------------|
> |                              NULL |          NULL |
> +-----------------------------------+---------------+
> ```
