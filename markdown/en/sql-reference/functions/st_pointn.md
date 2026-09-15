Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_POINTN

Returns a Point at a specified index in a LineString.

See also:
:   [ST\_ENDPOINT](/sql-reference/functions/st_endpoint) , [ST\_STARTPOINT](/sql-reference/functions/st_startpoint)

## Syntax

Copy code

```
ST_POINTN( <geography_or_geometry_expression> , <index> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY that represents a LineString.

`index`
:   The index of the Point to return. The index must be an integer.

    A negative index is interpreted as the offset from the end of the LineString. For example, `-1` is interpreted as the last
    Point in the LineString, `-2` is interpreted as the second to the last Point, etc.

## Returns

The function returns a value of type GEOGRAPHY or GEOMETRY that contains the Point at the specified index of the LineString.

## Usage notes

- If `geography_or_geometry_expression` is not a LineString, the function reports an error.
- If `index` is out of bounds (e.g. exceeds the number of Points in the LineString), the function reports an error.

## Examples

### GEOGRAPHY examples

The following query returns the second Point in a LineString:

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
SELECT ST_POINTN(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), 2);

+--------------------------------------------------------------+
| ST_POINTN(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), 2) |
|--------------------------------------------------------------|
| POINT(2 2)                                                   |
+--------------------------------------------------------------+
```

The following query uses a negative index to return the second Point from the end of a LineString:

Copy code

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
SELECT ST_POINTN(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), -2);

+---------------------------------------------------------------+
| ST_POINTN(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), -2) |
|---------------------------------------------------------------|
| POINT(3 3)                                                    |
+---------------------------------------------------------------+
```

### GEOMETRY examples

The following query returns the second Point in a LineString:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
SELECT ST_POINTN(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), 2);

+-------------------------------------------------------------+
| ST_POINTN(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), 2) |
|-------------------------------------------------------------|
| POINT(2 2)                                                  |
+-------------------------------------------------------------+
```

The following query uses a negative index to return the second Point from the end of a LineString:

Copy code

```
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
SELECT ST_POINTN(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), -2);

+--------------------------------------------------------------+
| ST_POINTN(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), -2) |
|--------------------------------------------------------------|
| POINT(3 3)                                                   |
+--------------------------------------------------------------+
```
