# Semi-structured and structured data functions

These functions are used with:

- [Semi-structured data formats](/user-guide/semistructured-data-formats) (including JSON, Avro, and XML)
- [Semi-structured data types](/sql-reference/data-types-semistructured) (including VARIANT, OBJECT, and ARRAY)
- [Structured data types](/sql-reference/data-types-structured) (including structured OBJECT, structured ARRAY, and MAP)

## List of semi-structured and structured data functions

The functions are grouped by type of operation performed:

- Parsing JSON and XML data.
- Creating and manipulating [ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array) and [OBJECTs](/sql-reference/data-types-semistructured#label-data-type-object).
- Extracting values from semi-structured and structured data (for example, from an ARRAY, OBJECT, or MAP).
- Converting/casting semi-structured data types and structured data types to/from other data types.
- Determining the data type for values in semi-structured data (that is, type predicates).

| Sub-category | Function | Notes |
| --- | --- | --- |
| **JSON and XML Parsing** | [CHECK\_JSON](/sql-reference/functions/check_json) |  |
|  | [CHECK\_XML](/sql-reference/functions/check_xml) |  |
|  | [JSON\_EXTRACT\_PATH\_TEXT](/sql-reference/functions/json_extract_path_text) |  |
|  | [PARSE\_JSON](/sql-reference/functions/parse_json) |  |
|  | [PARSE\_XML](/sql-reference/functions/parse_xml) |  |
|  | [STRIP\_NULL\_VALUE](/sql-reference/functions/strip_null_value) |  |
| **Array/Object Creation and Manipulation** | [ARRAY\_AGG](/sql-reference/functions/array_agg) | See also [Aggregate functions](/sql-reference/functions-aggregation). |
|  | [ARRAY\_APPEND](/sql-reference/functions/array_append) |  |
|  | [ARRAY\_CAT](/sql-reference/functions/array_cat) |  |
|  | [ARRAY\_COMPACT](/sql-reference/functions/array_compact) |  |
|  | [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) |  |
|  | [ARRAY\_CONSTRUCT\_COMPACT](/sql-reference/functions/array_construct_compact) |  |
|  | [ARRAY\_CONSTRUCT\_STRUCTURED](/sql-reference/functions/array_construct_structured) |  |
|  | [ARRAY\_CONTAINS](/sql-reference/functions/array_contains) |  |
|  | [ARRAY\_DISTINCT](/sql-reference/functions/array_distinct) |  |
|  | [ARRAY\_EXCEPT](/sql-reference/functions/array_except) |  |
|  | [ARRAY\_FLATTEN](/sql-reference/functions/array_flatten) |  |
|  | [ARRAY\_GENERATE\_RANGE](/sql-reference/functions/array_generate_range) |  |
|  | [ARRAY\_INSERT](/sql-reference/functions/array_insert) |  |
|  | [ARRAY\_INTERSECTION](/sql-reference/functions/array_intersection) |  |
|  | [ARRAY\_MAX](/sql-reference/functions/array_max) |  |
|  | [ARRAY\_MIN](/sql-reference/functions/array_min) |  |
|  | [ARRAY\_POSITION](/sql-reference/functions/array_position) |  |
|  | [ARRAY\_PREPEND](/sql-reference/functions/array_prepend) |  |
|  | [ARRAY\_REMOVE](/sql-reference/functions/array_remove) |  |
|  | [ARRAY\_REMOVE\_AT](/sql-reference/functions/array_remove_at) |  |
|  | [ARRAY\_REPEAT](/sql-reference/functions/array_repeat) |  |
|  | [ARRAY\_REVERSE](/sql-reference/functions/array_reverse) |  |
|  | [ARRAY\_SIZE](/sql-reference/functions/array_size) |  |
|  | [ARRAY\_SLICE](/sql-reference/functions/array_slice) |  |
|  | [ARRAY\_SORT](/sql-reference/functions/array_sort) |  |
|  | [ARRAY\_TO\_STRING](/sql-reference/functions/array_to_string) |  |
|  | [ARRAY\_UNION\_AGG](/sql-reference/functions/array_union_agg) | See also [Aggregate functions](/sql-reference/functions-aggregation). |
|  | [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg) | See also [Aggregate functions](/sql-reference/functions-aggregation). |
|  | [ARRAYS\_OVERLAP](/sql-reference/functions/arrays_overlap) |  |
|  | [ARRAYS\_TO\_OBJECT](/sql-reference/functions/arrays_to_object) |  |
|  | [ARRAYS\_ZIP](/sql-reference/functions/arrays_zip) |  |
|  | [OBJECT\_AGG](/sql-reference/functions/object_agg) | See also [Aggregate functions](/sql-reference/functions-aggregation). |
|  | [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) |  |
|  | [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null) |  |
|  | [OBJECT\_CONSTRUCT\_KEEP\_NULL\_STRUCTURED](/sql-reference/functions/object_construct_keep_null_structured) |  |
|  | [OBJECT\_DELETE](/sql-reference/functions/object_delete) |  |
|  | [OBJECT\_INSERT](/sql-reference/functions/object_insert) |  |
|  | [OBJECT\_PICK](/sql-reference/functions/object_pick) |  |
|  | [PROMPT](/sql-reference/functions/prompt) |  |
| **Higher-order** | [FILTER](/sql-reference/functions/filter) | See also [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions). |
|  | [REDUCE](/sql-reference/functions/reduce) | See also [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions). |
|  | [TRANSFORM](/sql-reference/functions/transform) | See also [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions). |
| **Map Creation and Manipulation** | [MAP\_CAT](/sql-reference/functions/map_cat) |  |
|  | [MAP\_CONSTRUCT](/sql-reference/functions/map_construct) |  |
|  | [MAP\_CONTAINS\_KEY](/sql-reference/functions/map_contains_key) |  |
|  | [MAP\_DELETE](/sql-reference/functions/map_delete) |  |
|  | [MAP\_ENTRIES](/sql-reference/functions/map_entries) |  |
|  | [MAP\_INSERT](/sql-reference/functions/map_insert) |  |
|  | [MAP\_KEYS](/sql-reference/functions/map_keys) |  |
|  | [MAP\_PICK](/sql-reference/functions/map_pick) |  |
|  | [MAP\_SIZE](/sql-reference/functions/map_size) |  |
| **Extraction** | [FLATTEN](/sql-reference/functions/flatten) | [Table function](/sql-reference/functions-table). |
|  | [GET](/sql-reference/functions/get) |  |
|  | [GET\_IGNORE\_CASE](/sql-reference/functions/get_ignore_case) |  |
|  | [GET\_PATH , :](/sql-reference/functions/get_path) | Variation of GET. |
|  | [OBJECT\_KEYS](/sql-reference/functions/object_keys) | Extracts keys from key/value pairs in [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object). |
|  | [XMLGET](/sql-reference/functions/xmlget) |  |
| **Conversion/Casting** | [AS\_\*<object\_type>\*](/sql-reference/functions/as) |  |
|  | [AS\_ARRAY](/sql-reference/functions/as_array) |  |
|  | [AS\_BINARY](/sql-reference/functions/as_binary) |  |
|  | [AS\_CHAR , AS\_VARCHAR](/sql-reference/functions/as_char-varchar) |  |
|  | [AS\_DATE](/sql-reference/functions/as_date) |  |
|  | [AS\_DECIMAL , AS\_NUMBER](/sql-reference/functions/as_decimal-number) |  |
|  | [AS\_DOUBLE , AS\_REAL](/sql-reference/functions/as_double-real) |  |
|  | [AS\_INTEGER](/sql-reference/functions/as_integer) |  |
|  | [AS\_OBJECT](/sql-reference/functions/as_object) |  |
|  | [AS\_TIME](/sql-reference/functions/as_time) |  |
|  | [AS\_TIMESTAMP\_\*](/sql-reference/functions/as_timestamp) |  |
|  | [STRTOK\_TO\_ARRAY](/sql-reference/functions/strtok_to_array) |  |
|  | [TO\_ARRAY](/sql-reference/functions/to_array) |  |
|  | [TO\_JSON](/sql-reference/functions/to_json) |  |
|  | [TO\_OBJECT](/sql-reference/functions/to_object) |  |
|  | [TO\_VARIANT](/sql-reference/functions/to_variant) |  |
|  | [TO\_XML](/sql-reference/functions/to_xml) |  |
| **Type Predicates** | [IS\_\*<object\_type>\*](/sql-reference/functions/is) |  |
|  | [IS\_ARRAY](/sql-reference/functions/is_array) |  |
|  | [IS\_BOOLEAN](/sql-reference/functions/is_boolean) |  |
|  | [IS\_BINARY](/sql-reference/functions/is_binary) |  |
|  | [IS\_CHAR , IS\_VARCHAR](/sql-reference/functions/is_char-varchar) |  |
|  | [IS\_DATE , IS\_DATE\_VALUE](/sql-reference/functions/is_date-value) |  |
|  | [IS\_DECIMAL](/sql-reference/functions/is_decimal) |  |
|  | [IS\_DOUBLE , IS\_REAL](/sql-reference/functions/is_double-real) |  |
|  | [IS\_INTEGER](/sql-reference/functions/is_integer) |  |
|  | [IS\_NULL\_VALUE](/sql-reference/functions/is_null_value) |  |
|  | [IS\_OBJECT](/sql-reference/functions/is_object) |  |
|  | [IS\_TIME](/sql-reference/functions/is_time) |  |
|  | [IS\_TIMESTAMP\_\*](/sql-reference/functions/is_timestamp) |  |
|  | [TYPEOF](/sql-reference/functions/typeof) |  |

Expand

Show lessSee more
