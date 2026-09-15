Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ASGEOJSON

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
[GeoJSON](/sql-reference/data-types-geospatial#label-a-note-on-geojson-handling) representation of that value.

## Syntax

Copy code

```
ST_ASGEOJSON( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

An OBJECT in [GeoJSON](/sql-reference/data-types-geospatial#label-a-note-on-geojson-handling) format.

## Usage notes

For GEOMETRY objects:

- The returned GEOMETRY object uses the same coordinate system as the input GEOMETRY object.

  Note that the GeoJSON specification requires that geometry be in the WGS84 coordinate system (SRID = 4326). However, the
  ST\_ASGEOJSON function does not enforce this.
- The function does not add the SRID or any other CRS information to the output.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_ASGEOJSON function:

> Copy code
>
> ```
> create table geospatial_table (id INTEGER, g GEOGRAPHY);
> insert into geospatial_table values
>     (1, 'POINT(-122.35 37.55)'), (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');
> ```
>
> Copy code
>
> ```
> select st_asgeojson(g)
>     from geospatial_table
>     order by id;
> +------------------------+
> | ST_ASGEOJSON(G)        |
> |------------------------|
> | {                      |
> |   "coordinates": [     |
> |     -122.35,           |
> |     37.55              |
> |   ],                   |
> |   "type": "Point"      |
> | }                      |
> | {                      |
> |   "coordinates": [     |
> |     [                  |
> |       -124.2,          |
> |       42               |
> |     ],                 |
> |     [                  |
> |       -120.01,         |
> |       41.99            |
> |     ]                  |
> |   ],                   |
> |   "type": "LineString" |
> | }                      |
> +------------------------+
> ```
>
> Casting the VARIANT output to VARCHAR results in the following:
>
> Copy code
>
> ```
> select st_asgeojson(g)::varchar
>     from geospatial_table
>     order by id;
> +-------------------------------------------------------------------+
> | ST_ASGEOJSON(G)::VARCHAR                                          |
> |-------------------------------------------------------------------|
> | {"coordinates":[-122.35,37.55],"type":"Point"}                    |
> | {"coordinates":[[-124.2,42],[-120.01,41.99]],"type":"LineString"} |
> +-------------------------------------------------------------------+
> ```

### GEOMETRY examples

The following example demonstrates the ST\_ASGEOJSON function with a GEOMETRY object as input:

> Copy code
>
> ```
> SELECT ST_ASGEOJSON(TO_GEOMETRY('SRID=4326;LINESTRING(389866 5819003, 390000 5830000)')) AS geojson;
> ```
>
> Copy code
>
> ```
> +------------------------+
> | GEOJSON                |
> |------------------------|
> |{                       |
> |  "coordinates": [      |
> |    [                   |
> |      389866,           |
> |      5819003           |
> |    ],                  |
> |    [                   |
> |      390000,           |
> |      5830000           |
> |    ]                   |
> |  ],                    |
> |  "type": "LineString"  |
> |}                       |
> +------------------------+
> ```
