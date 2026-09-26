# Data types for Apache Iceberg™ tables

Snowflake supports most of the data types defined by the [Apache Iceberg™ specification](https://iceberg.apache.org/spec/),
and writes Iceberg data types to table files so that your Iceberg tables remain interoperable across different compute engines
when you use Snowflake as the catalog.

For an overview of the Iceberg data types that Snowflake supports,
see [Supported data types](#label-tables-iceberg-data-type-mapping-table).

## Approximate types

If your table uses an Iceberg data type that Snowflake doesn’t support an *exact match* for,
Snowflake uses an *approximate* Snowflake type. This type mapping affects column values for converted tables and Iceberg tables
that use Snowflake as the catalog.

For example, consider a table with a column of Iceberg type `int`. Snowflake processes the column values using the
Snowflake data type NUMBER(10,0).

NUMBER(10,0) has a range of (-9,999,999,999, +9,999,999,999),
but `int` has a more limited range of (-2,147,483,648, +2,147,483,647). If you try to insert a value of 3,000,000,000 into that column,
Snowflake returns an out-of-range error message.

For details about approximate types, see the notes in the [Supported data types](#label-tables-iceberg-data-type-mapping-table) table.

## Supported data types

The tables in this section show the relationship between Iceberg data types and Snowflake data types. They use the following columns:

Iceberg type:
:   The data type defined in the Apache Iceberg specification.
    When you use Snowflake as the catalog, Snowflake writes the Iceberg type to your table data files so that your tables remain
    interoperable across different compute engines.

Snowflake type:
:   The Snowflake data type that is used to process and return table data. For example,
    if your schema specifies the Iceberg type `timestamp`, Snowflake processes and returns values using the Snowflake data type
    TIMESTAMP\_NTZ(6) with microsecond precision.

Notes:
:   Additional usage notes, including notes for working with [approximate types](#label-tables-iceberg-approximate-types).

### Numeric types

#### Snowflake as the catalog

The following table shows how Iceberg numeric data types map to Snowflake numeric data types for tables that use Snowflake as the
Iceberg catalog (Snowflake-managed tables). When you create a Snowflake-managed Iceberg table, you can use
[Iceberg data types](https://iceberg.apache.org/spec/#schemas-and-data-types) to define numeric columns.

| Iceberg data type | Snowflake data type | Notes |
| --- | --- | --- |
| `int` (32-bit signed integer) | [NUMBER(10,0)](/sql-reference/data-types-numeric#label-data-type-number) | Inserting a 10-digit number smaller than the minimum or larger than the maximum 32-bit signed integer value results in an out-of-range error. |
| `long` (64-bit signed integer) | [NUMBER(19,0)](/sql-reference/data-types-numeric#label-data-type-number) | Inserting a 19-digit number smaller than the minimum or larger than the maximum 64-bit signed integer value results in an out-of-range error. |
| `float` (single-precision 32-bit IEEE 754 floating point) | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | Synonymous with the Snowflake DOUBLE data type. Snowflake treats all floating-point numbers as double-precision 64-bit floating-point numbers, but writes Iceberg floats as 32-bit floating-point numbers in table data files.  Narrowing conversions from 64 bits to 32 bits result in precision loss.  You can’t use `float` or `double` as primary keys (in accordance with the [Apache Iceberg spec](https://iceberg.apache.org/spec/#identifier-field-ids)). |
| `double` (double-precision 64-bit IEEE 754 floating point) | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | Synonymous with the Snowflake DOUBLE data type. Snowflake treats all floating-point numbers as double-precision 64-bit floating-point numbers.  Narrowing conversions from 64 bits to 32 bits result in precision loss.  You can’t use `float` or `double` as primary keys (in accordance with the [Apache Iceberg spec](https://iceberg.apache.org/spec/#identifier-field-ids)). |
| `decimal(P,S)` | [NUMBER(P,S)](/sql-reference/data-types-numeric#label-data-type-number) | Specifying `decimal(10,0)` instead of `int` creates a decimal type in Iceberg. The same applies when you specify `decimal(19,0)`. |

Expand

Show lessSee more

#### External catalog

When you create an Iceberg table that uses an external Iceberg catalog, Iceberg numeric types are mapped to Snowflake numeric types according
to the following table.

| Iceberg data type | Snowflake data type |
| --- | --- |
| `int` (32-bit signed integer) | [NUMBER(10,0)](/sql-reference/data-types-numeric#label-data-type-number) |
| `long` (64-bit signed integer) | [NUMBER(19,0)](/sql-reference/data-types-numeric#label-data-type-number) |
| `float` (single-precision 32-bit IEEE 754 floating point) | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) |
| `double` (double-precision 64-bit IEEE 754 floating point) | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) |
| `decimal(P,S)` | [NUMBER(P,S)](/sql-reference/data-types-numeric#label-data-type-number) |

Expand

Show lessSee more

Note

You can’t use `float` or `double` as primary keys (in accordance with the
[Apache Iceberg spec](https://iceberg.apache.org/spec/#identifier-field-ids)).

### Other data types

Note

For non-numeric data types, specify the Snowflake data type in your table DDL when you use Snowflake as the catalog (for example, use a
structured ARRAY instead of the `list` type).
Snowflake automatically maps each Snowflake type to the corresponding Iceberg data type in the
table metadata for interoperability with external Iceberg tools.

| Iceberg data type | Snowflake data type | Notes |
| --- | --- | --- |
| `boolean` | [BOOLEAN](/sql-reference/data-types-logical) |  |
| `date` | [DATE](/sql-reference/data-types-datetime#label-datatypes-date) |  |
| `time` | [TIME(6)](/sql-reference/data-types-datetime#label-datatypes-time) | Microsecond precision per the Apache Iceberg table specification. |
| `timestamp` | [TIMESTAMP\_NTZ(6)](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) | Microsecond precision per the Apache Iceberg table specification.  You can also use the Parquet physical type `int96` for timestamps. Snowflake translates `timestamp` to microseconds (per the Apache Iceberg table specification). |
| `timestamptz` | [TIMESTAMP\_LTZ(6)](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) | Microsecond precision per the Apache Iceberg table specification.  You can also use the Parquet physical type `int96` for timestamps. Snowflake translates `timestamptz` to microseconds (per the Apache Iceberg table specification). |
| `string` | [VARCHAR(134217728)](/sql-reference/data-types-text#label-data-types-text-varchar) | The default size is 128 MB, and the only size that you can specify explicitly is 134217728 (128 MB). |
| `uuid` | [UUID](/sql-reference/data-types-uuid) | You can also store UUID values in Iceberg VARIANT (v3) columns and as the element or value type of Iceberg structured types (`struct`, `list`, and `map`). |
| `fixed(L)` | [BINARY(L)](/sql-reference/data-types-text#label-data-type-binary) | You can create an Iceberg table that uses this type, but you can’t convert a table that has a column of type `fixed(L)`. Inserting a value that doesn’t exactly match L bytes in length results in an error. |
| `binary` | [BINARY(67108864)](/sql-reference/data-types-text#label-data-type-binary) | The default size is 64 MB, and the only size that you can specify explicitly is 67108864 (64 MB). |
| `struct` | [Structured OBJECT](/sql-reference/data-types-structured) | Structured type columns support a maximum of 1000 sub-columns. |
| `list` | [Structured ARRAY](/sql-reference/data-types-structured) | Structured type columns support a maximum of 1000 sub-columns. |
| `map` | [MAP](/sql-reference/data-types-structured) | Structured type columns support a maximum of 1000 sub-columns. |

Expand

Show lessSee more

### Iceberg v3 data types

Important

To use Iceberg v3 data types, you must specify the version of the Apache Iceberg™ specification that your Iceberg table conforms to as
`3`. For instructions on how to specify a version, see [Configure the default Iceberg version](/user-guide/tables-iceberg-v3-specification-support#tables-iceberg-configuring-default-version).

The following table shows the Apache Iceberg™ v3 data types that you can use with Iceberg tables:

| Iceberg data type | Snowflake data type | Notes |
| --- | --- | --- |
| `geography` | `GEOGRAPHY` | Snowflake supports the [GEOGRAPHY data type](/sql-reference/data-types-geospatial#label-data-types-geography) in [Apache Iceberg™ tables](/user-guide/tables-iceberg). You can create a Snowflake-managed or externally managed Iceberg table with a GEOGRAPHY column. To create an Iceberg table with a GEOGRAPHY column, use the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command.  Caution  Iceberg uses the WKB format to store geography data. This format can’t represent all data that can be contained in Snowflake GEOGRAPHY values. The `Feature` and `FeatureCollection` types aren’t supported in WKB format. When inserting GEOGRAPHY values with these types into an Iceberg table, Snowflake converts features to their underlying geography objects and drops all properties. The automatic conversion for Iceberg tables behaves identically to the [ST\_ASWKB](/sql-reference/functions/st_aswkb) function.  For GEOGRAPHY objects, the SRID is always 4326. |
| `geometry` | `GEOMETRY` | Snowflake supports the [GEOMETRY data type](/sql-reference/data-types-geospatial#label-data-types-geometry) in [Apache Iceberg™ tables](/user-guide/tables-iceberg). You can create a Snowflake-managed or externally managed Iceberg table with a GEOMETRY column. To create an Iceberg table with a GEOMETRY column, use the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command.  Note  All GEOMETRY objects in a single column must have the same SRID. |
| `timestamp_ns` | `TIMESTAMP_NTZ(9)` | Nanosecond precision per the Apache Iceberg table specification. No timezone semantics (wall-clock). TIMESTAMP(9) is first mapped to either the TIMESTAMP\_NTZ(9) or the TIMESTAMP\_LTZ(9) Snowflake type, depending on the value of the Snowflake parameter [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping). Then, it is mapped to the appropriate Iceberg data type. |
| `timestamptz_ns` | `TIMESTAMP_LTZ(9)` | Nanosecond precision per the Apache Iceberg table specification. Stored in UTC.  TIMESTAMP(9) is first mapped to either the TIMESTAMP\_NTZ(9) or the TIMESTAMP\_LTZ(9) Snowflake type, depending on the value of the Snowflake parameter [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping). Then, it is mapped to the appropriate Iceberg data type. |
| `variant` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Snowflake initially developed the [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) data type for standard Snowflake tables.  VARIANT provides efficient binary encoding for dynamic semi-structured data such as JSON, Avro, and Protobuf, which makes it easier to work with and operate on data containing other nested data types. For more information, see [Semi-structured data types](/sql-reference/data-types-semistructured) and [Introduction to loading semi-structured data](/user-guide/semistructured-intro).  **Shredding**  Snowflake provides built-in shredding (also called [subcolumnarization](/user-guide/semistructured-considerations#label-semistructured-columnarization)) for the VARIANT data type. Shredding is the process of extracting fields from a VARIANT-type column into separate fields, and storing each field in columnar form (subcolumns) that you can traverse and query by using special notation.  Snowflake tracks metadata and statistics for shredded subcolumns, which enables pruning for faster, more efficient queries.  When you insert semi-structured data into a VARIANT column, Snowflake shreds as much of the data as possible.  For more information, see [Semi-structured data files and subcolumnarization](/user-guide/semistructured-considerations#label-semistructured-columnarization). |

Expand

Show lessSee more

#### Considerations for the Iceberg v3 data types

Consider the following as you use the Iceberg v3 data types:

**Nanosecond timestamps**

- Usage notes for the `nanosecond timestamps` data type:
  - Use TIMESTAMP\_NTZ(9), TIMESTAMP\_LTZ(9), or TIMESTAMP(9) in [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) and
    [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) statements. A scale of `9` specifies a new Iceberg nanosecond type.
    A scale of `6` continues to specify the legacy microsecond type.
  - When a scale is omitted, the session-level parameter [ICEBERG\_TIMESTAMP\_DEFAULT\_PRECISION](/sql-reference/parameters#label-iceberg-timestamp-default-precision) controls the precision.
    The default remains `6` for compatibility. If you want Iceberg timestamp columns to default to nanoseconds, set the
    parameter to `9`.
  - All standard Iceberg partition transforms (for example, identity, bucket, year, month, day, and hour) accept the new nanosecond
    types exactly as they do the microsecond variants.
  - Compatibility
    - **Read/write** - Read and write operations are supported for both Snowflake-managed and externally managed Iceberg tables.
    - **External tools** - No connector changes are required. Nanosecond values are used in read and write operations
      as standard Iceberg `timestamp_ns` and `timestamptz_ns` values.

> **VARIANT**
>
> - Note the following considerations and limitations when you use the `VARIANT` data type with Iceberg tables:
>   - The regular considerations for Iceberg data types apply to the VARIANT data type. For more information, see
>     [Considerations for working with data types for Iceberg tables](#label-tables-iceberg-data-types-considerations).
>   - The keys for objects in VARIANT columns should be of type STRING.
>   - Using Snowpipe or COPY INTO to load data into Iceberg tables with VARIANT columns is supported. However, Snowpipe and COPY INTO cannot
>     be used to load data into OBJECT, ARRAY, or MAP columns that contain a nested VARIANT column.
>   - You can store [UUID](/sql-reference/data-types-uuid) values in a VARIANT column. UUID is also supported as the
>     element or value type of Iceberg structured types (`struct`, `list`, and `map`).
>   - Also see [Considerations for semi-structured data stored in VARIANT](/user-guide/semistructured-considerations).

#### Examples

The following section contains examples for the Iceberg v3 data types.

##### GEOGRAPHY

To insert data into a GEOGRAPHY column, specify the input data. The following example inserts a geospatial
object that is defined as well-known text (WKT) into the `geog` column of the `geog_points` table that
was created in the previous example:

Copy code

```
INSERT INTO geog_points
  SELECT TO_GEOGRAPHY('POINT(-122.3861109 37.61637595)');
```

You can also insert geospatial data without explicitly constructing the GEOGRAPHY value:

Copy code

```
INSERT INTO geog_points
  SELECT 'POINT(-122.3861109 37.61637595)';
```

##### GEOMETRY

The following example creates an empty Iceberg table that contains a single GEOMETRY column named
`geom` with a default SRID of `4326`.

Copy code

```
CREATE ICEBERG TABLE geo_points (geom GEOMETRY)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'us_states'
  ICEBERG_VERSION = 3;
```

You can also set the SRID explicitly in the DDL statement. The following example sets the SRID to
`4269`:

Copy code

```
CREATE ICEBERG TABLE geo_points (geom GEOMETRY(4269))
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'us_states'
  ICEBERG_VERSION = 3;
```

To insert data into a GEOMETRY column, specify the input data. The following example inserts a geospatial
object defined as well-known text (WKT) into the `geom` column of the `geo_points` table that was created
in the previous example.

Copy code

```
INSERT INTO geo_points
  SELECT TO_GEOMETRY('POINT(-122.3861109 37.61637595)');
```

You can also insert geospatial data without explicitly constructing the GEOMETRY value:

Copy code

```
INSERT INTO geo_points
  SELECT 'POINT(-122.3861109 37.61637595)';
```

If the SRID isn’t available as part of the GEOMETRY object, you can set it explicitly using the constructor function:

Copy code

```
INSERT INTO geo_points
  SELECT TO_GEOMETRY('POINT(-122.3861109 37.61637595)', 4326);
```

##### Nanosecond timestamps

The following example creates a managed Iceberg table with nanosecond timestamps:

Copy code

```
CREATE ICEBERG TABLE sensor_readings (
    reading_ntz TIMESTAMP_NTZ(9),
    reading_ltz TIMESTAMP_LTZ(9))
  ICEBERG_VERSION = 3;
```

For this statement, Snowflake performs the following data type mappings:

- The data type of the `reading_ntz` column is mapped to the `timestamp_ns` Iceberg v3 data type.
- The data type of the `reading_ltz` column is mapped to the `timestamptz_ns` Iceberg v3 data type.

##### VARIANT

You can create an Iceberg table with a VARIANT column by using the
[CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command.

The following example creates an empty Snowflake-managed Iceberg table that contains a single VARIANT column named `record`.

Copy code

```
CREATE ICEBERG TABLE car_sales (record VARIANT)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'car_sales'
  ICEBERG_VERSION = 3;
```

Similarly, the following example creates an empty externally managed Iceberg table in a catalog-linked database, to which Snowflake can write.

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA my_namespace;

CREATE ICEBERG TABLE car_sales (record VARIANT)
ICEBERG_VERSION = 3;
```

To insert data into a VARIANT column, you specify the input data format.
The following example uses the [PARSE\_JSON](/sql-reference/functions/parse_json)
function to insert JSON-formatted data into the `record` column of the `car_sales` table (created previously).

Copy code

```
INSERT INTO car_sales SELECT
  PARSE_JSON(
    '{
        "date" : "2017-04-28",
        "dealership" : "Valley View Auto Sales",
        "salesperson" : {
          "id": "55",
          "name": "John Salesperson"
        },
        "customer" : [
          {"name": "Alice Doe", "phone": "14151234567", "address": "San Francisco, CA"},
          {"name": "Bob Doe", "phone": "14151234567", "address": "San Francisco, CA"}
        ],
        "vehicle" : [
          {"make": "Honda", "model": "Civic", "year": "2017", "price": "20275", "extras":["ext warranty", "paint protection"]}
        ]
      }'
    );
```

Running a SELECT \* FROM statement on the table returns the following output:

```
+--------------------------------------------+
| RECORD                                     |
|--------------------------------------------|
| {                                          |
|    "customer": [                           |
|      {                                     |
|        "address": "San Francisco, CA",     |
|        "name": "Alice Doe",                |
|        "phone": "14151234567"              |
|      },                                    |
|      {                                     |
|        "address": "San Francisco, CA",     |
|        "name": "Bob Doe",                  |
|        "phone": "14151234567"              |
|      }                                     |
|    ],                                      |
|    "date": "2017-04-28",                   |
|    "dealership": "Valley View Auto Sales", |
|    "salesperson": {                        |
|      "id": "55",                           |
|      "name": "John Salesperson"            |
|    },                                      |
|    "vehicle": [                            |
|      {                                     |
|        "extras": [                         |
|          "ext warranty",                   |
|          "paint protection"                |
|        ],                                  |
|        "make": "Honda",                    |
|        "model": "Civic",                   |
|        "price": "20275",                   |
|        "year": "2017"                      |
|      }                                     |
|    ]                                       |
|  }                                         |
+--------------------------------------------+
```

To query the data in a VARIANT column, you can use dot or bracket notation to access elements nested in the data.

The following example uses dot notation to get the names of all salespeople who sold cars. Since there’s one row in the table,
the query produces a single result value.

Copy code

```
SELECT record:salesperson.name
  FROM car_sales
  ORDER BY 1;
```

Output:

Copy code

```
+-------------------------+
| RECORD:SALESPERSON.NAME |
|-------------------------|
| "John Salesperson"      |
+-------------------------+
```

For more information about querying semi-structured data, see [Querying Semi-structured Data](/user-guide/querying-semistructured).

Note

- When using Apache Spark to read or write Iceberg tables with VARIANT columns, you must use Apache Spark 4.0 or later which includes
  VARIANT support.

  Variant columns in Snowflake-managed Iceberg tables can be read by engines that support Iceberg Variant, such as Apache Spark. Engines
  can read Snowflake-managed Iceberg v3 tables through the [Horizon Iceberg REST Catalog API](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

  Copy code

  ```
  spark.sql("""
  SELECT
  variant_get(record, '$.customer[0].name', 'string') AS customer_1_name,
  variant_get(record, '$.salesperson.name', 'string') AS name
  FROM CAR_SALES
  ORDER BY name
  """).show()
  ```

  Similarly, Snowflake can read or write to externally managed Iceberg tables containing VARIANT columns.
- Snowflake can write null values to a table, if needed.
  For example:

  Copy code

  ```
  INSERT INTO my_table_new
    SELECT ARRAY_CONSTRUCT(
     OBJECT_CONSTRUCT_KEEP_NULL('field1', NULL, 'field2', 123)
    )::ARRAY(OBJECT(field1 STRING, field2 INT));
  ```

## Delta data types

The following table shows how Delta data types map to Snowflake data types for
[Iceberg tables created from Delta table files (Delta Direct)](/user-guide/tables-iceberg-create#label-tables-iceberg-delta-source-create).

| Delta type | Snowflake data type | Note |
| --- | --- | --- |
| BINARY | BINARY |  |
| BOOLEAN | BOOLEAN |  |
| BYTE | NUMBER(3,0) |  |
| DATE | DATE |  |
| DECIMAL(P,S) | NUMBER(P,S) |  |
| DOUBLE | REAL |  |
| FLOAT | REAL |  |
| INTEGER | NUMBER(10,0) |  |
| LONG | NUMBER(20,0) |  |
| SHORT | NUMBER(5,0) |  |
| STRING | TEXT |  |
| TIMESTAMP | TIMESTAMP\_LTZ(6) | You can also use the Parquet physical type `int96` for TIMESTAMP, but Snowflake doesn’t support `int96` for TIMESTAMP\_NTZ. |
| TIMESTAMP\_NTZ | TIMESTAMP\_NTZ(6) |  |
| VARIANT | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) |  |

Expand

Show lessSee more

The following table shows how Delta nested data types map to Snowflake data types.

| Delta nested type | Snowflake data type |
| --- | --- |
| STRUCT | [Structured OBJECT](/sql-reference/data-types-structured#label-structured-types-specifying-object) |
| ARRAY | [Structured ARRAY](/sql-reference/data-types-structured#label-structured-types-specifying-array) |
| MAP | [MAP](/sql-reference/data-types-structured#label-structured-types-specifying-map) |

Expand

Show lessSee more

## Considerations

Consider the following items when you work with data types for Iceberg tables:

- [Converting a table](/user-guide/tables-iceberg-conversion) with a column that uses the Iceberg `fixed(L)` data type is not supported.
- For Snowflake-managed Iceberg tables, you can specify [collation](/sql-reference/collation#label-collation-iceberg) on string columns.
  To set a default collation for new string columns, use the
  [ICEBERG\_DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-iceberg-default-ddl-collation) parameter.
- For all Iceberg table types:

  - Structured type columns support a maximum of 1000 sub-columns.
  - Iceberg supports microsecond precision for time and timestamp types. As a result, you can’t create an Iceberg table in Snowflake
    that uses another precision like millisecond or nanosecond.
  - You can’t use `float` or `double` as primary keys (in accordance with the
    [Apache Iceberg spec](https://iceberg.apache.org/spec/#identifier-field-ids)).
  - For Parquet files that use the `LIST` logical type, be aware of the following:

    - The three-level annotation structure with the `element` keyword is supported. For more
      information, see [Parquet Logical Type Definitions](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#lists). If your
      Parquet file uses an obsolete format with the `array` keyword, you must regenerate your data based on the supported format.
- For tables created from Delta files, be aware of the following:

  - Parquet files (data files for Delta tables) that use any of the following features or data types aren’t supported:

    - Field IDs.
    - The INTERVAL data type.
    - The DECIMAL data type with precision higher than 38.
    - LIST or MAP types with one-level or two-level representation.
    - Unsigned integer types (INT(signed = false)).
    - The FLOAT16 data type.
  - You can use the Parquet physical type `int96` for TIMESTAMP, but Snowflake doesn’t support `int96` for TIMESTAMP\_NTZ.
