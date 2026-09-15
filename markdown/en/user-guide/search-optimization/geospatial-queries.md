# Speeding up geospatial queries with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The search optimization service can improve the performance of queries with predicates that use geospatial functions with
GEOGRAPHY objects.

The following sections provide more information about search optimization support for geospatial queries:

- [Enabling search optimization for geospatial queries](#label-search-optimization-service-geospatial-support-setup)
- [Supported predicates with geospatial functions](#label-search-optimization-service-geo-predicates)
- [Other performance considerations](#label-search-optimization-service-geo-performance)
- [Examples that use geospatial functions](#label-search-optimization-service-geo-examples)

Note

GEOMETRY objects aren’t yet supported.

## Enabling search optimization for geospatial queries

To improve the performance of geospatial queries on a table, use the
[ON GEO clause in the ALTER TABLE … ADD SEARCH OPTIMIZATION command](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
for specific columns. Enabling search optimization at the table level doesn’t enable it for columns with geospatial data types.

For example:

Copy code

```
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON GEO(mygeocol);
```

For more information, see [Enabling and disabling search optimization](/user-guide/search-optimization/enabling).

## Supported predicates with geospatial functions

For queries with predicates that use the following functions:

- [ST\_INTERSECTS](/sql-reference/functions/st_intersects)
- [ST\_CONTAINS](/sql-reference/functions/st_contains)
- [ST\_WITHIN](/sql-reference/functions/st_within)
- [ST\_DWITHIN](/sql-reference/functions/st_dwithin)
- [ST\_COVERS](/sql-reference/functions/st_covers)
- [ST\_COVEREDBY](/sql-reference/functions/st_coveredby)

The search optimization service can improve performance if:

- One input expression is a GEOGRAPHY column in a table, and
- The other input expression is a GEOGRAPHY constant (created through a
  [conversion or constructor function](/sql-reference/functions-geospatial)).
- For ST\_DWITHIN, the distance argument is a non-negative REAL constant.

Note that this feature has the same
[limitations that apply to the search optimization service](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-limitations).

## Other performance considerations

Because the search optimization service is designed for predicates that are highly selective and because predicates filter by proximity
between geospatial objects, clustering geospatial objects by proximity in the table can result in better performance. You can cluster
your data either by specifying the sort order when loading the data or by using Automatic Clustering, depending on whether the base
table changes frequently:

Loading Pre-Sorted Data
:   If the data in your base table does not change often, you can specify the sort order when loading the data. You can then enable search
    optimization on the GEOGRAPHY column. For example:

    Copy code

    ```
    CREATE TABLE new_table AS SELECT * FROM source_table ORDER BY st_geohash(geom);
    ALTER TABLE new_table ADD SEARCH OPTIMIZATION ON GEO(geom);
    ```

    After every large change made to your base data, you can manually re-sort the data.

### Automatic clustering

If there are frequent updates to your base table, you can use the [ALTER TABLE … CLUSTER BY …](/sql-reference/sql/alter-table#label-alter-table-clusteringaction)
command to enable [Automatic Clustering](/user-guide/tables-auto-reclustering) so the table is automatically reclustered as it
changes.

The following example adds a new column `geom_geohash` of the type VARCHAR and stores the geohash or H3 index of the GEOGRAPHY column
`geom` in that new column. It then enables Automatic Clustering with the new column as the cluster key. This approach will
automatically recluster the parts of the table that change.

Copy code

```
CREATE TABLE new_table AS SELECT *, ST_GEOHASH(geom) AS geom_geohash FROM source_table;
ALTER TABLE new_table CLUSTER BY (geom_geohash);
ALTER TABLE new_table ADD SEARCH OPTIMIZATION ON GEO(geom);
```

## Examples that use geospatial functions

The following statements create and configure the table used in the examples in this section. The last statement uses the
[ON clause in ALTER TABLE … ADD SEARCH OPTIMIZATION](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding) command
to add search optimization for the `g1` GEOGRAPHY column.

Copy code

```
CREATE OR REPLACE TABLE geospatial_table (id NUMBER, g1 GEOGRAPHY);
INSERT INTO geospatial_table VALUES
  (1, 'POINT(-122.35 37.55)'),
  (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)'),
  (3, 'POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))');
ALTER TABLE geospatial_table ADD SEARCH OPTIMIZATION ON GEO(g1);
```

## Examples of supported predicates

The following query is an example of a query supported by the search optimization service. The search optimization service can
use search access paths to improve the performance of this query:

Copy code

```
SELECT id FROM geospatial_table WHERE
  ST_INTERSECTS(
    g1,
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));
```

The following are examples of additional predicates that are supported by the search optimization service:

Copy code

```
...
  ST_INTERSECTS(
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
    g1)
```

Copy code

```
...
  ST_CONTAINS(
    TO_GEOGRAPHY('POLYGON((-74.17 40.64, -74.1796875 40.58, -74.09 40.58, -74.09 40.64, -74.17 40.64))'),
    g1)
```

Copy code

```
...
  ST_CONTAINS(
    g1,
    TO_GEOGRAPHY('MULTIPOINT((0 0), (1 1))'))
```

Copy code

```
...
  ST_WITHIN(
   TO_GEOGRAPHY('{"type" : "MultiPoint","coordinates" : [[-122.30, 37.55], [-122.20, 47.61]]}'),
   g1)
```

Copy code

```
...
  ST_WITHIN(
    g1,
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'))
```

Copy code

```
...
  ST_COVERS(
    TO_GEOGRAPHY('POLYGON((-1 -1, -1 4, 4 4, 4 -1, -1 -1))'),
    g1)
```

Copy code

```
...
  ST_COVERS(
    g1,
    TO_GEOGRAPHY('POINT(0 0)'))
```

Copy code

```
...
  ST_COVEREDBY(
    TO_GEOGRAPHY('POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))'),
    g1)
```

Copy code

```
...
  ST_COVEREDBY(
    g1,
    TO_GEOGRAPHY('POINT(-122.35 37.55)'))
```

Copy code

```
...
  ST_DWITHIN(
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
    g1,
    100000)
```

Copy code

```
...
  ST_DWITHIN(
    g1,
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
    100000)
```

## Examples of constructing GEOGRAPHY constants

The following are examples of predicates that use different
[conversion and constructor functions](/sql-reference/functions-geospatial) for the GEOGRAPHY constant.

Copy code

```
...
  ST_INTERSECTS(
    g1,
    ST_GEOGRAPHYFROMWKT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'))
```

Copy code

```
...
  ST_INTERSECTS(
    ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
    g1)
```

Copy code

```
...
  ST_CONTAINS(
    ST_GEOGRAPHYFROMEWKT('POLYGON((-74.17 40.64, -74.1796875 40.58, -74.09 40.58, -74.09 40.64, -74.17 40.64))'),
    g1)
```

Copy code

```
...
  ST_WITHIN(
    ST_GEOGRAPHYFROMWKB('01010000006666666666965EC06666666666C64240'),
    g1)
```

Copy code

```
...
  ST_COVERS(
    g1,
    ST_MAKEPOINT(0.2, 0.8))
```

Copy code

```
...
  ST_INTERSECTS(
    g1,
    ST_MAKELINE(
      TO_GEOGRAPHY('MULTIPOINT((0 0), (1 1))'),
      TO_GEOGRAPHY('POINT(0.8 0.2)')))
```

Copy code

```
...
  ST_INTERSECTS(
    ST_POLYGON(
      TO_GEOGRAPHY('SRID=4326;LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)')),
    g1)
```

Copy code

```
...
  ST_WITHIN(
    g1,
    TRY_TO_GEOGRAPHY('POLYGON((-1 -1, -1 4, 4 4, 4 -1, -1 -1))'))
```

Copy code

```
...
  ST_COVERS(
    g1,
    ST_GEOGPOINTFROMGEOHASH('s00'))
```
