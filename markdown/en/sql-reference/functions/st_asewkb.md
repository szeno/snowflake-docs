Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# ST\_ASEWKB

Given a value of type [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) or [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry), return the
binary representation of that value in
[EWKB (extended well-known binary)](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling) format.

See also:
:   [ST\_ASWKB](/sql-reference/functions/st_aswkb)

## Syntax

Copy code

```
ST_ASEWKB( <geography_or_geometry_expression> )
```

## Arguments

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns

A value of type BINARY.

## Usage notes

- For GEOGRAPHY objects, the SRID in the return value is always 4326. See
  the [note on EWKT handling](/sql-reference/data-types-geospatial#label-a-note-on-ewkt-ewkb-handling).
- To return the output in WKB format, use [ST\_ASWKB](/sql-reference/functions/st_aswkb) instead.

## Examples

### GEOGRAPHY examples

The following example demonstrates the ST\_ASEWKB function. For the EWKB output, it is assumed that the [BINARY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-binary-output-format)
parameter is set to `HEX` (the default value for the parameter).

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
> select st_asewkb(g)
>     from geospatial_table
>     order by id;
> +--------------------------------------------------------------------------------------------+
> | ST_ASEWKB(G)                                                                               |
> |--------------------------------------------------------------------------------------------|
> | 0101000020E61000006666666666965EC06666666666C64240                                         |
> | 0102000020E610000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
> +--------------------------------------------------------------------------------------------+
> ```

### GEOMETRY examples

The example below demonstrates how to use the ST\_ASEWKB function. The example returns the EWKB representations of two geometries
that have different SRIDs.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
> INSERT INTO geometry_table VALUES
>   ('SRID=4326;POINT(-122.35 37.55)'),
>   ('SRID=0;LINESTRING(0.75 0.75, -10 20)');
>
> SELECT ST_ASEWKB(g) FROM geometry_table;
> ```
>
> Copy code
>
> ```
> +--------------------------------------------------------------------------------------------+
> | ST_ASEWKB(G)                                                                               |
> |--------------------------------------------------------------------------------------------|
> | 0101000020E61000006666666666965EC06666666666C64240                                         |
> | 01020000200000000002000000000000000000E83F000000000000E83F00000000000024C00000000000003440 |
> +--------------------------------------------------------------------------------------------+
> ```
