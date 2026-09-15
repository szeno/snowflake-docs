# Geospatial functions

Geospatial functions operate on
[GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) and [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry) and convert GEOGRAPHY and GEOMETRY
values to and from other representations (such as VARCHAR).

| Sub-category | Function | Notes |
| --- | --- | --- |
| Conversion / Input / Parsing | [ST\_GEOGFROMGEOHASH](/sql-reference/functions/st_geogfromgeohash) | GEOGRAPHY only |
|  | [ST\_GEOGPOINTFROMGEOHASH](/sql-reference/functions/st_geogpointfromgeohash) | GEOGRAPHY only |
|  | [ST\_GEOGRAPHYFROMWKB](/sql-reference/functions/st_geographyfromwkb) | GEOGRAPHY only |
|  | [ST\_GEOGRAPHYFROMWKT](/sql-reference/functions/st_geographyfromwkt) | GEOGRAPHY only |
|  | [ST\_GEOMETRYFROMWKB](/sql-reference/functions/st_geometryfromwkb) | GEOMETRY only |
|  | [ST\_GEOMETRYFROMWKT](/sql-reference/functions/st_geometryfromwkt) | GEOMETRY only |
|  | [ST\_GEOMFROMGEOHASH](/sql-reference/functions/st_geomfromgeohash) | GEOMETRY only |
|  | [ST\_GEOMPOINTFROMGEOHASH](/sql-reference/functions/st_geompointfromgeohash) | GEOMETRY only |
|  | [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) | GEOGRAPHY only |
|  | [TO\_GEOMETRY](/sql-reference/functions/to_geometry) | GEOMETRY only |
|  | [TRY\_TO\_GEOGRAPHY](/sql-reference/functions/try_to_geography) | GEOGRAPHY only |
|  | [TRY\_TO\_GEOMETRY](/sql-reference/functions/try_to_geometry) | GEOMETRY only |
| Conversion / Output / Formatting | [ST\_ASGEOJSON](/sql-reference/functions/st_asgeojson) |  |
|  | [ST\_ASWKB](/sql-reference/functions/st_aswkb) |  |
|  | [ST\_ASBINARY](/sql-reference/functions/st_aswkb) | Alias for ST\_ASWKB |
|  | [ST\_ASEWKB](/sql-reference/functions/st_asewkb) |  |
|  | [ST\_ASWKT](/sql-reference/functions/st_aswkt) |  |
|  | [ST\_ASTEXT](/sql-reference/functions/st_aswkt) | Alias for ST\_ASWKT |
|  | [ST\_ASEWKT](/sql-reference/functions/st_asewkt) |  |
|  | [ST\_GEOHASH](/sql-reference/functions/st_geohash) |  |
| Constructor Functions | [ST\_MAKELINE](/sql-reference/functions/st_makeline) |  |
|  | [ST\_MAKEGEOMPOINT](/sql-reference/functions/st_makegeompoint) | GEOMETRY only |
|  | [ST\_GEOMPOINT](/sql-reference/functions/st_makegeompoint) | Alias for ST\_MAKEGEOMPOINT |
|  | [ST\_MAKEPOINT](/sql-reference/functions/st_makepoint) | GEOGRAPHY only |
|  | [ST\_POINT](/sql-reference/functions/st_makepoint) | Alias for ST\_MAKEPOINT |
|  | [ST\_MAKEPOLYGON](/sql-reference/functions/st_makepolygon) |  |
|  | [ST\_POLYGON](/sql-reference/functions/st_makepolygon) | Alias for ST\_MAKEPOLYGON |
|  | [ST\_MAKEPOLYGONORIENTED](/sql-reference/functions/st_makepolygonoriented) | GEOGRAPHY only |
| Accessor Functions | [ST\_DIMENSION](/sql-reference/functions/st_dimension) |  |
|  | [ST\_ENDPOINT](/sql-reference/functions/st_endpoint) |  |
|  | [ST\_POINTN](/sql-reference/functions/st_pointn) |  |
|  | [ST\_SRID](/sql-reference/functions/st_srid) |  |
|  | [ST\_STARTPOINT](/sql-reference/functions/st_startpoint) |  |
|  | [ST\_X](/sql-reference/functions/st_x) |  |
|  | [ST\_XMAX](/sql-reference/functions/st_xmax) |  |
|  | [ST\_XMIN](/sql-reference/functions/st_xmin) |  |
|  | [ST\_Y](/sql-reference/functions/st_y) |  |
|  | [ST\_YMAX](/sql-reference/functions/st_ymax) |  |
|  | [ST\_YMIN](/sql-reference/functions/st_ymin) |  |
| Relationship and Measurement Functions | [HAVERSINE](/sql-reference/functions/haversine) |  |
|  | [ST\_AREA](/sql-reference/functions/st_area) |  |
|  | [ST\_AZIMUTH](/sql-reference/functions/st_azimuth) |  |
|  | [ST\_CONTAINS](/sql-reference/functions/st_contains) |  |
|  | [ST\_COVEREDBY](/sql-reference/functions/st_coveredby) |  |
|  | [ST\_COVERS](/sql-reference/functions/st_covers) |  |
|  | [ST\_DISJOINT](/sql-reference/functions/st_disjoint) |  |
|  | [ST\_DISTANCE](/sql-reference/functions/st_distance) |  |
|  | [ST\_DWITHIN](/sql-reference/functions/st_dwithin) | GEOGRAPHY only |
|  | [ST\_HAUSDORFFDISTANCE](/sql-reference/functions/st_hausdorffdistance) | GEOGRAPHY only |
|  | [ST\_INTERSECTS](/sql-reference/functions/st_intersects) |  |
|  | [ST\_LENGTH](/sql-reference/functions/st_length) |  |
|  | [ST\_NPOINTS](/sql-reference/functions/st_npoints) |  |
|  | [ST\_NUMPOINTS](/sql-reference/functions/st_npoints) | Alias for ST\_NPOINTS |
|  | [ST\_PERIMETER](/sql-reference/functions/st_perimeter) |  |
|  | [ST\_WITHIN](/sql-reference/functions/st_within) |  |
| Transformation Functions | [ST\_BUFFER](/sql-reference/functions/st_buffer) | GEOMETRY only |
|  | [ST\_CENTROID](/sql-reference/functions/st_centroid) |  |
|  | [ST\_COLLECT](/sql-reference/functions/st_collect) (Scalar and Aggregate) | GEOGRAPHY only |
|  | [ST\_DIFFERENCE](/sql-reference/functions/st_difference) | GEOGRAPHY only |
|  | [ST\_ENVELOPE](/sql-reference/functions/st_envelope) | Deprecated for GEOGRAPHY |
|  | [ST\_INTERPOLATE](/sql-reference/functions/st_interpolate) | GEOGRAPHY only |
|  | [ST\_INTERSECTION](/sql-reference/functions/st_intersection) | GEOGRAPHY only |
|  | [ST\_INTERSECTION\_AGG](/sql-reference/functions/st_intersection_agg) (Scalar and Aggregate) | GEOGRAPHY only |
|  | [ST\_SETSRID](/sql-reference/functions/st_setsrid) | GEOMETRY only |
|  | [ST\_SIMPLIFY](/sql-reference/functions/st_simplify) |  |
|  | [ST\_SYMDIFFERENCE](/sql-reference/functions/st_symdifference) | GEOGRAPHY only |
|  | [ST\_TRANSFORM](/sql-reference/functions/st_transform) | GEOMETRY only |
|  | [ST\_UNION](/sql-reference/functions/st_union) | GEOGRAPHY only |
|  | [ST\_UNION\_AGG](/sql-reference/functions/st_union_agg) (Scalar and Aggregate) | GEOGRAPHY only |
| Utility Functions | [ST\_ISVALID](/sql-reference/functions/st_isvalid) |  |
| H3 Functions | [H3\_CELL\_TO\_BOUNDARY](/sql-reference/functions/h3_cell_to_boundary) | GEOGRAPHY only |
|  | [H3\_CELL\_TO\_CHILDREN](/sql-reference/functions/h3_cell_to_children) | GEOGRAPHY only |
|  | [H3\_CELL\_TO\_CHILDREN\_STRING](/sql-reference/functions/h3_cell_to_children_string) | GEOGRAPHY only |
|  | [H3\_CELL\_TO\_PARENT](/sql-reference/functions/h3_cell_to_parent) | GEOGRAPHY only |
|  | [H3\_CELL\_TO\_POINT](/sql-reference/functions/h3_cell_to_point) | GEOGRAPHY only |
|  | [H3\_COMPACT\_CELLS](/sql-reference/functions/h3_compact_cells) | GEOGRAPHY only |
|  | [H3\_COMPACT\_CELLS\_STRINGS](/sql-reference/functions/h3_compact_cells_strings) | GEOGRAPHY only |
|  | [H3\_COVERAGE](/sql-reference/functions/h3_coverage) | GEOGRAPHY only |
|  | [H3\_COVERAGE\_STRINGS](/sql-reference/functions/h3_coverage_strings) | GEOGRAPHY only |
|  | [H3\_GET\_RESOLUTION](/sql-reference/functions/h3_get_resolution) | GEOGRAPHY only |
|  | [H3\_GRID\_DISTANCE](/sql-reference/functions/h3_grid_distance) | GEOGRAPHY only |
|  | [H3\_GRID\_DISK](/sql-reference/functions/h3_grid_disk) | GEOGRAPHY only |
|  | [H3\_GRID\_PATH](/sql-reference/functions/h3_grid_path) | GEOGRAPHY only |
|  | [H3\_INT\_TO\_STRING](/sql-reference/functions/h3_int_to_string) | GEOGRAPHY only |
|  | [H3\_IS\_PENTAGON](/sql-reference/functions/h3_is_pentagon) | GEOGRAPHY only |
|  | [H3\_IS\_VALID\_CELL](/sql-reference/functions/h3_is_valid_cell) | GEOGRAPHY only |
|  | [H3\_LATLNG\_TO\_CELL](/sql-reference/functions/h3_latlng_to_cell) | GEOGRAPHY only |
|  | [H3\_LATLNG\_TO\_CELL\_STRING](/sql-reference/functions/h3_latlng_to_cell_string) | GEOGRAPHY only |
|  | [H3\_POINT\_TO\_CELL](/sql-reference/functions/h3_point_to_cell) | GEOGRAPHY only |
|  | [H3\_POINT\_TO\_CELL\_STRING](/sql-reference/functions/h3_point_to_cell_string) | GEOGRAPHY only |
|  | [H3\_POLYGON\_TO\_CELLS](/sql-reference/functions/h3_polygon_to_cells) | GEOGRAPHY only |
|  | [H3\_POLYGON\_TO\_CELLS\_STRINGS](/sql-reference/functions/h3_polygon_to_cells_strings) | GEOGRAPHY only |
|  | [H3\_STRING\_TO\_INT](/sql-reference/functions/h3_string_to_int) | GEOGRAPHY only |
|  | [H3\_TRY\_COVERAGE](/sql-reference/functions/h3_try_coverage) | GEOGRAPHY only |
|  | [H3\_TRY\_COVERAGE\_STRINGS](/sql-reference/functions/h3_try_coverage_strings) | GEOGRAPHY only |
|  | [H3\_TRY\_GRID\_DISTANCE](/sql-reference/functions/h3_try_grid_distance) | GEOGRAPHY only |
|  | [H3\_TRY\_GRID\_PATH](/sql-reference/functions/h3_try_grid_path) | GEOGRAPHY only |
|  | [H3\_TRY\_POLYGON\_TO\_CELLS](/sql-reference/functions/h3_try_polygon_to_cells) | GEOGRAPHY only |
|  | [H3\_TRY\_POLYGON\_TO\_CELLS\_STRINGS](/sql-reference/functions/h3_try_polygon_to_cells_strings) | GEOGRAPHY only |
|  | [H3\_UNCOMPACT\_CELLS](/sql-reference/functions/h3_uncompact_cells) | GEOGRAPHY only |
|  | [H3\_UNCOMPACT\_CELLS\_STRINGS](/sql-reference/functions/h3_uncompact_cells_strings) | GEOGRAPHY only |

Expand

Show lessSee more
