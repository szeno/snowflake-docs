# Working with the Snowflake Connector for Kafka

This topic describes how the connector works with tables and pipes, and how to configure the connector with these elements.

## How the connector works with tables and pipes

The connector treats each Kafka record as a row to be inserted into a Snowflake table. For example,
if you have a Kafka topic with the content of the message structured like the following JSON:

Copy code

```
{
  "order_id": 12345,
  "customer_name": "John",
  "order_total": 100.00,
  "isPaid": true
}
```

By default you don’t have to create a table or pipe before ingestion begins.
The connector creates a table with columns matching the JSON keys, and relies on the default pipe named `{tableName}-STREAMING`
which will automatically map the record content’s first-level keys to table columns matching by name (case-insensitive).
You can also create your own table with columns matching the JSON keys.
The connector tries to match the record content’s first-level keys to the table columns by name.
If keys from the JSON don’t match the table columns, the connector ignores the keys unless
`ENABLE_SCHEMA_EVOLUTION` is enabled on the table, in which case new columns are added automatically.

Copy code

```
CREATE TABLE ORDERS (
  record_metadata VARIANT,
  order_id NUMBER,
  customer_name VARCHAR,
  order_total NUMBER,
  ispaid BOOLEAN
);
```

If you choose to create your own pipe, you can define the data transformation logic in the pipe’s [COPY INTO](/sql-reference/sql/copy-into-table) statement. You can rename columns as required and cast the data types as needed. For example:

Copy code

```
CREATE TABLE ORDERS (
  order_id VARCHAR,
  customer_name VARCHAR,
  order_total VARCHAR,
  ispaid VARCHAR
);
```

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
  $1:order_id::STRING,
  $1:customer_name,
  $1:order_total::STRING,
  $1:isPaid::STRING
FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

or

Copy code

```
CREATE TABLE ORDERS (
 topic VARCHAR,
 partition VARCHAR,
 order_id VARCHAR,
 customer_name VARCHAR,
 order_total VARCHAR,
 ispaid VARCHAR
);
```

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
  $1:RECORD_METADATA.topic::STRING AS topic,
  $1:RECORD_METADATA.partition::STRING AS partition,
  $1['order_id']::STRING AS order_id,
  $1['customer_name']::STRING as customer_name,
  CONCAT($1['order_total']::STRING, ' USD') AS order_total,
  $1['isPaid']::STRING AS ispaid
FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

When you define your own pipe your destination table columns need not match the JSON keys.
You can rename the columns to your desired names and cast the data types if required.

### Topic names, table names, and pipe names

Depending on the configuration settings, the connector will use different names for the destination table.
The destination table name is always derived from the topic name.

#### How the connector maps topic names to the destination table

The Kafka connector provides two modes for mapping Kafka topic names to Snowflake table names:

- **Static mapping**: The connector derives destination table names using only Kafka topic name.
- **Explicit topic-to-table mapping mode**: You specify custom mappings between topics and tables using the `snowflake.topic2table.map` configuration parameter

#### Static mapping

If you do not configure the `snowflake.topic2table.map` parameter, the connector always derives the table names from the topic name.

**Table name generation:**

The connector derives the destination table name from the topic name using the following rules:

1. If the topic name is a valid [Snowflake identifier](/sql-reference/identifiers-syntax)
   the connector uses the topic name as the destination table name, converted to uppercase).
2. If the topic name contains invalid characters, the connector:
   - Replaces invalid characters with underscores
   - Appends an underscore followed by a hash code to ensure uniqueness
   - For example, the topic `my-topic.data` becomes `MY_TOPIC_DATA_<hash>`

**Pipe name determination:**

The connector determines which pipe to use based on the following logic:

1. The connector checks if a pipe exists with the same name as the destination table name.
2. If a user-created pipe with that name exists, the connector uses that pipe (user-defined pipe mode).
3. If not, the connector uses the default pipe named `{tableName}-STREAMING`

Note

When using client-side validation (`snowflake.validation=client_side`), only the default pipe
mode is supported. User-defined pipes aren’t available with client-side validation.

Note

Snowflake recommends choosing topic names that follow the rules for Snowflake identifier names to ensure predictable table names.

### Understanding RECORD\_METADATA

The connector populates the `RECORD_METADATA` structure with metadata about the Kafka record. This metadata is sent through the Snowpipe Streaming data source to Snowflake, where it becomes available in pipe transformations using the `$1:RECORD_METADATA` accessor. `RECORD_METADATA` structure is available in both user-defined pipe and default pipe modes. Its content can be saved to the column of type VARIANT, or individual fields can be extracted and saved to separate columns.

**Example pipe with transformations and metadata:**

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS_TABLE
FROM (
  SELECT
    $1:order_id::NUMBER,
    $1:customer_name,
    $1:order_total,
    $1:RECORD_METADATA.topic AS source_topic,
    $1:RECORD_METADATA.offset::NUMBER AS kafka_offset,
    $1:RECORD_METADATA.SnowflakeConnectorPushTime::BIGINT AS ingestion_time
  FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

In this example:

- The pipe extracts specific fields from the Kafka message (order\_id, customer\_name, order\_total)
- It also captures metadata fields (topic, offset, and ingestion timestamp)
- The values can be cast or transformed as needed

### How metadata fields are populated

The connector automatically populates metadata fields based on the Kafka record properties and connector configuration. You can control which metadata fields are included using these configuration parameters:

- `snowflake.metadata.topic` (default: true) - Includes the topic name
- `snowflake.metadata.offset.and.partition` (default: true) - Includes offset and partition
- `snowflake.metadata.createtime` (default: true) - Includes the Kafka record timestamp
- `snowflake.metadata.all` (default: true) - Includes all available metadata

When `snowflake.metadata.all=true` (the default), all metadata fields are populated. Setting individual metadata flags to `false` excludes those specific fields from the RECORD\_METADATA structure.

Note

The `SnowflakeConnectorPushTime` field is always available and represents the time when the connector pushed the record into the ingestion buffer. This is useful for calculating end-to-end ingestion latency.

The RECORD\_METADATA structure contains the following information by default:

| Field | Data Type | Description |
| --- | --- | --- |
| topic | String | The name of the Kafka topic that the record came from. |
| partition | String | The number of the partition within the topic. (Note that this is the Kafka partition, not the Snowflake micro-partition.) |
| offset | number | The offset in that partition. |
| CreateTime /   LogAppendTime | number | This is the timestamp associated with the message in the Kafka topic. The value is milliseconds since midnight January 1, 1970, UTC. For more information, see: [Kafka ProducerRecord documentation](https://kafka.apache.org/0100/javadoc/org/apache/kafka/clients/producer/ProducerRecord.html). |
| SnowflakeConnectorPushTime | number | A timestamp when a record was pushed into an Ingest SDK buffer. The value is the number of milliseconds since midnight January 1, 1970, UTC. For more information, see [Estimating ingestion latency](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka#label-kafka-connector-snowpipe-streaming-latency). |
| key | String | If the message is a Kafka KeyedMessage, this is the key for that message. For the connector to store the key in the RECORD\_METADATA, the `key.converter` parameter in the [connector configuration properties](/user-guide/kafka-connector/setup-kafka#label-kafkahp-connector-configuration-properties) must be set to `org.apache.kafka.connect.storage.StringConverter`; otherwise, the connector ignores keys. |
| headers | Object | A header is a user-defined key-value pair associated with the record. Each record can have 0, 1, or multiple headers. |

Expand

Show lessSee more

The amount of metadata recorded in the RECORD\_METADATA column is configurable using optional Kafka configuration properties.

The field names and values are case-sensitive.

Note

RECORD\_METADATA adds approximately 150 bytes of overhead per record, depending on the topic name
length. For records with small payloads, this overhead can be a significant portion of the total
ingested data and affects
[billing](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-cost).
If you don’t need metadata, you can reduce this overhead by setting
`snowflake.metadata.all=false`.

### How Kafka records are converted before ingestion

Before each row is handed over to Snowpipe Streaming, the connector converts the Kafka Connect record value into a `Map<String, Object>` whose keys must match your target column names (or can be transformed inside a user-defined pipe). Primitive strings, byte arrays, or numbers must be wrapped (for example by using the HoistField SMT) so that the connector receives a structured object. The converter applies the following rules:

- Null values are treated as tombstones. They are skipped when `behavior.on.null.values=IGNORE` or ingested as empty JSON objects otherwise.
- Numeric and boolean fields are passed through as-is. Decimal values whose precision is greater than 38 are serialized as strings to stay within Snowflake’s `NUMBER` limits.
- `byte[]` and `ByteBuffer` payloads are Base64-encoded strings, so store them in `VARIANT` or `VARCHAR` columns.
- Arrays remain arrays, and nested objects remain nested maps. Declare `VARIANT` columns when you rely on the default pipe to land nested data as-is.
- Maps with non-string keys are emitted as arrays of `[key, value]` pairs because Snowflake column names must be text.
- Record headers and keys are copied into `RECORD_METADATA` whenever the relevant metadata flags are enabled.

If you need the entire message body preserved as a single column, wrap it into a new top-level field using SMTs. See [Legacy RECORD\_CONTENT column](#label-kafkahp-connector-legacy-record-content-column) for the transformation pattern.

## User-defined pipe mode vs default pipe mode

The connector supports two modes for managing data ingestion:

- [User-defined pipe mode](#label-kafkahp-connector-user-defined-pipe-mode)
- [Default pipe mode](#label-kafkahp-connector-default-pipe-mode)

### User-defined pipe mode

In this mode, you have full control over data transformation and column mapping.

**When to use this mode:**

- You need custom column names that differ from JSON field names
- You need to apply data transformations (type casting, masking, filtering)
- You want full control over how data is mapped to columns

### Default pipe mode

In this mode, the connector uses a default pipe named `{tableName}-STREAMING` and maps kafka record fields to table columns matching by name (case-insensitive).

**When to use this mode:**

- Your kafka record key names match your desired column names
- You don’t need custom data transformations
- You want a simple configuration

**Mapping kafka record keys to table columns with default pipe mode**

When using default pipe mode, the connector uses default pipe named `{tableName}-STREAMING` and maps content’s first-level keys directly to table columns using case-insensitive matching.

### Using default pipe mode - example

#### Example 1:

Consider the following kafka record content payload:

Copy code

```
{
  "city": "New York",
  "age": 30,
  "married": true,
  "has cat": true,
  "@&$#* includes special characters": true,
  "skills": ["sitting", "standing", "eating"],
  "family": {"son": "Jack", "daughter": "Anna"}
}
```

You create a table with columns matching the JSON keys (case-insensitive, including special characters):

Copy code

```
CREATE TABLE PERSON_DATA (
  record_metadata VARIANT,
  city VARCHAR,
  age NUMBER,
  married BOOLEAN,
  "has cat" BOOLEAN,
  "!@&$#* includes special characters" BOOLEAN,
  skills VARIANT,
  family VARIANT
);
```

**Matching behavior:**

- `"city"` (kafka) → `city` or `CITY` or `City` (column) - case insensitive
- `"has cat"` (kafka) → `"has cat"` (column) - must be quoted due to space
- `"!@&$#* includes special characters"` (kafka) → `"!@&$#* includes special characters"` (column) - special characters preserved
- Nested objects like `skills` and `family` map to VARIANT columns automatically

### Using user-defined pipe mode - examples

This example shows how to configure and use user-defined pipes with custom data transformations.

#### Example 1:

Create a table with your desired schema:

Copy code

```
CREATE TABLE ORDERS (
  order_id NUMBER,
  customer_name VARCHAR,
  order_total NUMBER,
  order_date TIMESTAMP_NTZ,
  source_topic VARCHAR
);
```

Create a pipe that transforms the incoming Kafka records to match your table schema:

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
    $1:order_id::NUMBER,
    $1:customer_name,
    $1:order_total::NUMBER,
    $1:order_date::TIMESTAMP_NTZ,
    $1:RECORD_METADATA.topic
  FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

Note that the pipe name (`ORDERS`) matches the table name (`ORDERS`). The pipe definition extracts fields from the JSON payload using `$1:field_name` syntax and maps them to the table columns.

Note

You can access nested JSON fields and fields with special characters using bracket notation, such as `$1['field name']` or `$1['has cat']`.

Configure topic to table mapping:

Copy code

```
snowflake.topic2table.map=kafka-orders-topic:ORDERS
```

This configuration maps the Kafka topic `kafka-orders-topic` to the pre-existing table and pipe named `ORDERS`.

#### Example 2:

When you need to access keys in the content that do not have conventional names use the following syntax:

- Simple fields: `$1:field_name`
- Fields with spaces or special characters: `$1['field name']` or `$1['has cat']`
- Fields with unicode characters: `$1[' @&$#* has Łułósżź']`
- Nested fields: `$1:parent.child` or `$1:parent['child field']`

Consider this JSON payload from Kafka:

Copy code

```
{
  "city": "New York",
  "age": 30,
  "married": true,
  "has cat": true,
  " @&$#* has Łułósżź": true,
  "skills": ["sitting", "standing", "eating"],
  "family": {"son": "Jack", "daughter": "Anna"}
}
```

You create a destination table with your chosen column names:

Copy code

```
CREATE TABLE PERSON_DATA (
  city VARCHAR,
  age NUMBER,
  married BOOLEAN,
  has_cat BOOLEAN,
  weird_field_name BOOLEAN,
  skills VARIANT,
  family VARIANT
);
```

Then create a pipe with the same name that defines the mapping:

Copy code

```
CREATE PIPE PERSON_DATA AS
COPY INTO PERSON_DATA
FROM (
  SELECT
    $1:city,
    $1:age,
    $1:married,
    $1['has cat'] AS has_cat,
    $1[' @&$#* has Łułósżź'] AS weird_field_name,
    $1:skills,
    $1:family
  FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

**Key points:**

- You control column names (for example, renaming `"has cat"` to `has_cat`)
- You can cast data types as needed (for example, `$1:age::NUMBER`)
- You can include or exclude fields as desired
- You can add metadata fields (for example, `$1:RECORD_METADATA.topic`)
- VARIANT columns automatically handle nested JSON structures

#### Example 3: With interactive tables

Interactive tables are a special type of Snowflake table optimized for low-latency, high-concurrency queries. You can find out more about interactive tables in the [interactive tables documentation](/user-guide/interactive).

1. Create an interactive table:

   Copy code

   ```
   CREATE INTERACTIVE TABLE REALTIME_METRICS (
     metric_name VARCHAR,
     metric_value NUMBER,
     source_topic VARCHAR,
     timestamp TIMESTAMP_NTZ
   ) AS (SELECT
      $1:M_NAME::VARCHAR,
      $1:M_VALUE::NUMBER,
      $1:RECORD_METADATA.topic::VARCHAR,
      $1:RECORD_METADATA.timestamp::TIMESTAMP_NTZ
      from TABLE(DATA_SOURCE(TYPE => 'STREAMING')));
   ```
2. Configure topic to table mapping:

   Copy code

   ```
   snowflake.topic2table.map=metrics-topic:REALTIME_METRICS
   ```

**Important considerations:**

- Interactive tables have specific limitations and query restrictions. Review the
  [interactive tables documentation](/user-guide/interactive) before using them with the connector.
- For interactive tables, any required transformations must be handled in the table definition.
- Interactive warehouses are required to query interactive tables efficiently.

### Explicit topic-to-table mapping

When you configure the `snowflake.topic2table.map` parameter, the connector operates in explicit mapping mode. This mode allows you to:

- Map multiple Kafka topics to a single Snowflake table
- Use custom table names that differ from topic names
- Apply regex patterns to match multiple topics

**Configuration format:**

The `snowflake.topic2table.map` parameter accepts a comma-separated list of topic-to-table mappings in the format:

Copy code

```
topic1:table1,topic2:table2,topic3:table3
```

Both topic and table names can be double-quoted to support special characters (colons, commas,
spaces). Unquoted table names are uppercased. Quoted table names preserve case, allowing you to
target mixed-case or special-character table names. For example:

Copy code

```
snowflake.topic2table.map="topic:one":"table,one","my-topic":"My_Table"
```

**Example configurations:**

Direct topic mapping

Copy code

```
snowflake.topic2table.map=orders:ORDER_TABLE,customers:CUSTOMER_TABLE
```

Regex pattern matching

Copy code

```
snowflake.topic2table.map=.*_cat:CAT_TABLE,.*_dog:DOG_TABLE
```

This configuration maps all topics ending with `_cat` (such as `orange_cat`, `calico_cat`) to the `CAT_TABLE` table, and all topics ending with `_dog` to the `DOG_TABLE` table.

Many topics to one table

Copy code

```
snowflake.topic2table.map=topic1:shared_table,topic2:shared_table,topic3:other_table
```

This configuration maps both `topic1` and `topic2` to `shared_table`, while `topic3` maps to `other_table`.

Important

- Regex patterns in the mapping can’t overlap. Each topic must match at most one pattern.
- Table names in the mapping must be valid Snowflake identifiers with at least 2 characters, starting with a letter or underscore.
- You can map multiple topics to a single table.

### RECORD\_CONTENT column

When schematization is disabled (`snowflake.enable.schematization=false`), the connector creates a
destination table with two columns: RECORD\_CONTENT and RECORD\_METADATA. The RECORD\_CONTENT column
contains the entire Kafka message content in a column of type VARIANT.

When schematization is enabled (the default), the RECORD\_CONTENT column isn’t created and
`$1:RECORD_CONTENT` isn’t available in PIPE transformations. To access the entire message body
when schematization is enabled, use the HoistField SMT to wrap the content into a named field.

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
    $1:RECORD_CONTENT
FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

If you need entire Kafka message content saved to a single column, or you need a handle to the entire Kafka message content in a PIPE transformation, you can use the following SMT transformation that wraps the entire Kafka message content into your desired custom field:

Copy code

```
transforms=wrapKafkaMessageContent
transforms.wrapKafkaMessageContent.type=org.apache.kafka.connect.transforms.HoistField$Value
transforms.wrapKafkaMessageContent.field=your_top_level_field_name
```

This transformation will wrap the entire Kafka message content into a custom field named `your_top_level_field_name`. You can then access the entire Kafka message content using the `$1:your_top_level_field_name` accessor in your PIPE transformation.

Copy code

```
CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
    $1:your_top_level_field_name
FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

Alternatively, if you want to save both the entire metadata and content to a single table using the default pipe, do not create a custom pipe; instead, create only a table with two columns: `RECORD_CONTENT` and `your_top_level_field_name`.

Copy code

```
CREATE TABLE ORDERS (
  record_metadata VARIANT,
  your_top_level_field_name VARIANT
);
```

To read more about the HoistField$Value transformation, see the [Kafka documentation](https://kafka.apache.org/39/documentation.html#connect_transforms).

Warning

Saving the entire Kafka message content and metadata to a table can negatively impact your ingestion cost, pipeline speed and latency. If you need the best possible performance, consider saving only the data you need if it is accessible from the top-level of the Kafka record content, or use SMT transformations to extract the data from deeply nested fields to top-level fields.

### Error handling

For information about how the connector handles ingestion errors, validation modes (server-side
and client-side), Error Tables, and Dead Letter Queues, see [Validation and error handling](/user-guide/kafka-connector/validation-error-handling).

## Schema evolution

For tables with `ENABLE_SCHEMA_EVOLUTION=TRUE`, the connector automatically evolves their schema, based on the incoming Kafka records. All connector created tables default to `ENABLE_SCHEMA_EVOLUTION=TRUE`.

Schema evolution is limited to the following operations:

- Adding new columns. The connector will add new columns to the table if the incoming Kafka records contain new fields that are not present in the table.
- Dropping the NOT NULL constraint from columns that are missing data in the inserted records

## Using the connector with Apache Iceberg™ tables

The connector can ingest data into a Snowflake-managed Apache Iceberg™ table. You must create the Iceberg table manually before running the connector; the connector doesn’t create Iceberg tables automatically. Server-side schema evolution is supported for Iceberg tables; client-side schema evolution isn’t. For more information, see [Validation and error handling](/user-guide/kafka-connector/validation-error-handling).

The Iceberg table can use either of the following storage options:

- [Snowflake storage](/user-guide/tables-iceberg-internal-storage): Snowflake stores and manages the Iceberg table files for you, so you don’t need to create an external volume or grant the connector access to it.
- External cloud storage that you manage, accessed through an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def). You must grant the connector role USAGE on the external volume.

### Grant usage on an external volume

This step applies only when the Iceberg table uses an external volume that you manage. If the table uses [Snowflake storage](/user-guide/tables-iceberg-internal-storage), skip this step.

For example, if your Iceberg table uses the `kafka_external_volume` external volume and the connector uses the role `kafka_connector_role`, run the following statement:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT USAGE ON EXTERNAL VOLUME kafka_external_volume TO ROLE kafka_connector_role;
```

### Create an Apache Iceberg™ table for ingestion

When you create an Iceberg table, you can use Iceberg data types (including VARIANT) or [compatible Snowflake types](/user-guide/tables-iceberg-data-types).

For example, consider the following message:

Copy code

```
{
    "id": 1,
    "name": "Steve",
    "body_temperature": 36.6,
    "approved_coffee_types": ["Espresso", "Doppio", "Ristretto", "Lungo"],
    "animals_possessed":
    {
        "dogs": true,
        "cats": false
    },
    "options":
    {
        "can_walk": true,
        "can_talk": false
    },
    "date_added": "2024-10-15"
}
```

To create an Iceberg table for the example message, use one of the following statements.

To use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` and omit `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
    id number(38,0),
    name varchar,
    body_temperature number(4,2),
    approved_coffee_types array(varchar),
    animals_possessed variant,
    options object(can_walk boolean, can_talk boolean),
    date_added date
  )
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
  CATALOG = 'SNOWFLAKE'
  ICEBERG_VERSION = 3;
```

To use your own external volume, set `EXTERNAL_VOLUME` to the volume name and provide a `BASE_LOCATION`:

> Copy code
>
> ```
> CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
>     id number(38,0),
>     name varchar,
>     body_temperature number(4,2),
>     approved_coffee_types array(varchar),
>     animals_possessed variant,
>     options object(can_walk boolean, can_talk boolean),
>     date_added date
>   )
>   EXTERNAL_VOLUME = 'my_volume'
>   CATALOG = 'SNOWFLAKE'
>   BASE_LOCATION = 'my_location/my_iceberg_table'
>   ICEBERG_VERSION = 3;
> ```
>
> Copy code
>
> ```
> CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
>     id INT,
>     name string,
>     body_temperature float,
>     approved_coffee_types array(string),
>     animals_possessed variant,
>     date_added date,
>     options object(can_walk boolean, can_talk boolean),
>     )
>   EXTERNAL_VOLUME = 'my_volume'
>   CATALOG = 'SNOWFLAKE'
>   BASE_LOCATION = 'my_location/my_iceberg_table'
>   ICEBERG_VERSION = 3;
> ```

Note

Field names inside nested structures such as `dogs` or `cats` are case sensitive.

## Next steps

[Set up tasks](/user-guide/kafka-connector/setup-tasks).
