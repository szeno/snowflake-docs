# UUID data type

The UUID data type stores universally unique identifiers (UUIDs). A UUID is a 128-bit binary value that
uniquely identifies information. Each UUID value is designed to be globally unique, which means that
there is a very low probability that two different systems will generate the exact same UUID independently.
However, uniqueness depends on how the UUID values are generated, and the Snowflake UUID data type
itself doesn’t guarantee uniqueness. For example, a user can insert the same UUID value multiple
times without errors.

UUID values are in UUID format, which is a 36-character string of hexadecimal digits, separated by
hyphens, in the pattern 8-4-4-4-12. For example, `f353ca91-4fc5-49f2-9b9e-304f83d11914` is a string
in UUID format.

For more information about the UUID data type, see the
[Universally unique identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier) Wikipedia
article.

The following considerations apply to the UUID data type:

- [Snowflake drivers](/developer-guide/drivers) treat UUID values as text strings.
- The ANSI literal form of UUID is supported as input.
- UUID values of any version can be inserted into tables.
- UUID values are case-insensitive.
- You can store UUID values in [semi-structured data types](/sql-reference/data-types-semistructured) (such as VARIANT)
  and [structured data types](/sql-reference/data-types-structured) (such as ARRAY, OBJECT, and MAP).
- Apache Iceberg™ tables support UUID as a column type. You can also store UUID values in Iceberg VARIANT (v3) columns
  and as the element or value type of Iceberg structured types (ARRAY, OBJECT, and MAP). For more information, see
  [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

## Specify a UUID data type

- To specify a UUID type, use the following syntax:

  Copy code

  ```
  <column_name> UUID
  ```

  Where:

  - `column_name` is the name of a column in a table.

## Limitations for the UUID data type

The following limitations apply to the UUID data type:

- The UUID data type isn’t supported in stored procedures or user-defined functions (UDFs) written in a
  language other than SQL, such as Python or Java.
- The UUID data type isn’t supported in [hybrid tables](/user-guide/tables-hybrid).
- The UUID data type isn’t supported in Snowpark.
- The following features don’t support the UUID data type:
  - [Differential privacy](/user-guide/diff-privacy/differential-privacy-sql-reference)
  - [Sensitive data classification](/user-guide/classify-intro)

## Examples for the UUID data type

The following examples insert UUID values into tables:

- [Insert a UUID value into a table](#label-uuid-example-inserting)
- [Automatically generate UUID values when you insert rows into a table](#label-uuid-example-generating)
- [Store a UUID value in a semi-structured or structured type](#label-uuid-example-semi-structured)

### Insert a UUID value into a table

- Create a table with a column of UUID type and insert a UUID value:

  Copy code

  ```
  CREATE TABLE sample_uuid_table(uuid_col UUID);

  INSERT INTO sample_uuid_table VALUES ('c73d9175-0a1d-48c6-8d30-df165461328b');
  ```

### Automatically generate UUID values when you insert rows into a table

The following example shows you how to automatically generate UUID values when you insert rows into a table:

1. Create a table that uses the [UUID\_STRING](/sql-reference/functions/uuid_string) function to
   generate a UUID value for each row inserted into the table:

   Copy code

   ```
   CREATE OR REPLACE TABLE sample_generate_uuid (
     id UUID DEFAULT UUID_STRING() NOT NULL,
     sample_column VARCHAR);
   ```
2. Insert values into the table and omit the `id` column so that a UUID value is generated and
   inserted automatically:

   Copy code

   ```
   INSERT INTO sample_generate_uuid (sample_column) VALUES
     ('value_a'),
     ('value_b');
   ```
3. Query the table to view the generated UUID values:

   Copy code

   ```
   SELECT * FROM sample_generate_uuid;
   ```

   ```
   +--------------------------------------+---------------+
   | ID                                   | SAMPLE_COLUMN |
   |--------------------------------------+---------------|
   | f353ca91-4fc5-49f2-9b9e-304f83d11914 | value_a       |
   | da563283-e201-4744-b158-221dd204a61f | value_b       |
   +--------------------------------------+---------------+
   ```

### Store a UUID value in a semi-structured or structured type

You can store UUID values inside semi-structured types (such as VARIANT) and structured types (such as ARRAY, OBJECT, and MAP).

1. Create a table with a VARIANT column and a structured ARRAY column of UUID elements:

   Copy code

   ```
   CREATE OR REPLACE TABLE uuid_container_table (
     v VARIANT,
     uuid_array ARRAY(UUID));
   ```
2. Insert a row that stores a UUID value in the VARIANT column and in the structured ARRAY column:

   Copy code

   ```
   INSERT INTO uuid_container_table
     SELECT
       OBJECT_CONSTRUCT('id', '5f4d3c2b-1a09-4e8f-8c7b-6a5d4e3f2b1a'::UUID),
       [
         'c73d9175-0a1d-48c6-8d30-df165461328b'::UUID,
         'da563283-e201-4744-b158-221dd204a61f'::UUID
       ]::ARRAY(UUID);
   ```
3. Query the table to view the stored values:

   Copy code

   ```
   SELECT * FROM uuid_container_table;
   ```

   ```
   +--------------------------------------------------+------------------------------------------+
   | V                                                | UUID_ARRAY                               |
   |--------------------------------------------------+------------------------------------------|
   | {                                                | [                                        |
   |   "id": "5f4d3c2b-1a09-4e8f-8c7b-6a5d4e3f2b1a"   |   "c73d9175-0a1d-48c6-8d30-df165461328b", |
   | }                                                |   "da563283-e201-4744-b158-221dd204a61f"  |
   |                                                  | ]                                        |
   +--------------------------------------------------+------------------------------------------+
   ```
4. To read a UUID value back out of a VARIANT, cast it with the `::` operator, [CAST](/sql-reference/functions/cast), or
   [TO\_UUID](/sql-reference/functions/to_uuid):

   Copy code

   ```
   SELECT v:id::UUID AS id FROM uuid_container_table;
   ```

   ```
   +--------------------------------------+
   | ID                                   |
   |--------------------------------------|
   | 5f4d3c2b-1a09-4e8f-8c7b-6a5d4e3f2b1a |
   +--------------------------------------+
   ```
