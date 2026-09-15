Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_MAKEGEOMPOINT , ST\_GEOMPOINT

Constructs a [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) object that represents a Point with the specified longitude and latitude.

See also:
:   [TO\_GEOMETRY](/sql-reference/functions/to_geometry)

## Syntax

Copy code

```
ST_MAKEGEOMPOINT( <longitude> , <latitude> )
```

## Arguments

`longitude`
:   A REAL that represents the longitude.

`latitude`
:   A REAL that represents the latitude.

## Returns

The function returns a value of type GEOMETRY.

## Usage notes

- ST\_GEOMPOINT is an alias for ST\_MAKEGEOMPOINT.

## Examples

For examples, see [Examples comparing the GEOGRAPHY and GEOMETRY data types](/sql-reference/data-types-geospatial#label-geometry-geography-diffs-examples). The examples use the
ST\_GEOMPOINT alias.
