Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ENDPOINT

Returns the last Point in a LineString.

See also:
:   [ST\_POINTN](/sql-reference/functions/st_pointn) , [ST\_STARTPOINT](/sql-reference/functions/st_startpoint)

## Syntax

Copy code

```
ST_ENDPOINT( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY that represents a LineString.

## Returns

The function returns a value of type GEOGRAPHY or GEOMETRY that contains the last Point of the specified LineString.

## Usage notes

- If `geography_or_geometry_expression` is not a LineString, the function reports an error.

## Examples

### GEOGRAPHY examples

The following query returns the last Point in a LineString:

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
SELECT ST_ENDPOINT(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'));

+-------------------------------------------------------------+
| ST_ENDPOINT(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)')) |
|-------------------------------------------------------------|
| POINT(4 4)                                                  |
+-------------------------------------------------------------+
```

### GEOMETRY examples

The following query returns the last Point in a LineString:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
SELECT ST_ENDPOINT(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'));

+------------------------------------------------------------+
| ST_ENDPOINT(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)')) |
|------------------------------------------------------------|
| POINT(4 4)                                                 |
+------------------------------------------------------------+
```
