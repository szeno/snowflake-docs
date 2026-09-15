Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SET\_ROW\_TIMESTAMP\_ON\_ALL\_SUPPORTED\_TABLES

Use this system function to bulk enable row timestamps on existing tables.

This function adds the row timestamp column to all existing eligible tables within the container and ensures newly created tables automatically
have row timestamp enabled.

To successfully execute the function, you need MODIFY privileges on the container you’re invoking the function on.

After row timestamps are enabled, tables expose the METADATA$ROW\_LAST\_COMMIT\_TIME column, which returns the timestamp when each row was last
modified. This enables change tracking, incremental processing, and time-travel queries based on row modification time. For more information, see
[Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).

## Syntax

Copy code

```
SELECT SYSTEM$SET_ROW_TIMESTAMP_ON_ALL_SUPPORTED_TABLES('<level>', '<qualified_name>')

- The first argument is level: one of :code:`schema`, :code:`database`, or :code:`account`.
- The second argument is the fully qualified name of the container.
```

## Arguments

**Required**

`'level'`
:   Container level. Can be one of the following: `account`, `database`, `schema`.

`'qualified_name'`
:   The fully qualified name of the container. For example, `my_db.myschema` for schema level.

## Examples

The following example demonstrates how to bulk-enable row timestamps for all supported tables within a specific schema using a system function. It
also verifies that the feature is applied to existing tables and sets the schema-level default to ensure all future tables automatically include
the METADATA$ROW\_LAST\_COMMIT\_TIME column.

Copy code

```
CREATE OR REPLACE DATABASE my_db;
CREATE OR REPLACE SCHEMA my_schema;
USE DATABASE my_db;
USE SCHEMA my_schema;

CREATE OR REPLACE TABLE my_table (id INT, v STRING);
CREATE OR REPLACE TRANSIENT TABLE my_transient_table (id INT, v STRING);
CREATE OR REPLACE TEMP TABLE my_temp_table (id INT, v STRING);

SELECT SYSTEM$SET_ROW_TIMESTAMP_ON_ALL_SUPPORTED_TABLES(
  'schema',
  'my_db.my_schema'
);

-- System function sets the container default so that new tables will get row timestamp going forward
SHOW PARAMETERS LIKE 'ROW_TIMESTAMP_DEFAULT' IN SCHEMA my_db.my_schema;

INSERT INTO my_table VALUES (1, 'a'), (2, 'b');
INSERT INTO my_transient_table VALUES (10, 'x');
INSERT INTO my_temp_table VALUES (100, 'tmp');

SELECT ID, METADATA$ROW_LAST_COMMIT_TIME FROM my_table ORDER BY ID;

SELECT ID, METADATA$ROW_LAST_COMMIT_TIME FROM my_transient_table ORDER BY ID;

SELECT ID, METADATA$ROW_LAST_COMMIT_TIME FROM my_temp_table ORDER BY ID;
```
