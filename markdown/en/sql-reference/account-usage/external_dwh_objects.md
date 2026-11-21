Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# EXTERNAL\_DWH\_OBJECTS view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This Account Usage view displays a row for each object that [Horizon Catalog metadata connectors](/user-guide/snowflake-horizon/connectors)
collect from external databases, data warehouses, and data pipeline tools, such as BigQuery, PostgreSQL, and dbt. The view includes
both leaf objects, such as tables and views, and the containers that hold them, such as databases and schemas.

For objects collected from BI tools, see the [EXTERNAL\_BI\_OBJECTS view](/sql-reference/account-usage/external_bi_objects).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| REFERENCE\_ID | TEXT | Snowflake-generated identifier of the object. This value is always present and uniquely identifies the object. |
| EXTERNAL\_ID | TEXT | Identifier of the object in the source system, when known. Otherwise, NULL. |
| NAME | TEXT | Name of the object in the source system. |
| OBJECT\_TYPE | TEXT | Type of the object. Rows for containers have one of the following values: `DATABASE`, `SCHEMA`, `FOLDER`, or `PROJECT`. Rows for other objects have one of the following values: `TABLE`, `VIEW`, `MATERIALIZED_VIEW`, `EXTERNAL_TABLE`, `DYNAMIC_TABLE`, `SNAPSHOT`, `SOURCE`, `SEED`, or `MODEL`.  For dbt, incremental, ephemeral, dynamic table, and legacy model rows all have the value `MODEL`. The `materialization` key in the `PROPERTIES` column identifies the materialization. |
| PARENT\_REFERENCE\_ID | TEXT | `REFERENCE_ID` of the object’s immediate parent in this view. NULL for top-level objects, such as databases. |
| CONNECTOR | TEXT | Display name of the metadata connector that collected the object. This is the connector’s name only, not a fully qualified name. |
| CONNECTOR\_TYPE | TEXT | Vendor or type of the source system, such as `BIGQUERY` or `DBT`. |
| COMMENT | TEXT | Description of the object. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the object was created in the source system. Only rows for tables have a value. For all other object types, NULL. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the object was last updated in the source system. Only rows for tables have a value. For all other object types, NULL. |
| DELETED | TIMESTAMP\_LTZ | Date and time when Snowflake observed that the object was removed from the source system. NULL if the object still exists. |
| PROPERTIES | VARIANT | Additional properties of the object, as an OBJECT. The following keys can be present:   - `last_refreshed_on`: Date and time when the object was last refreshed in the source system. - `business_owner`: Business owner of the object in the source system. - `technical_owner`: Technical owner of the object in the source system. - `materialization`: Materialization of the object, for dbt objects. - `package_name`: Name of the dbt package that contains the object. - `original_file_path`: Path of the file that defines the object in the dbt project. - `relation_name`: Name of the relation that the object is built as in the target database. - `project_reference_id`: `REFERENCE_ID` of the dbt project that contains the object. |
| DATABASE\_NAME | TEXT | Name of the source database. For a database row, this is the database’s own name. For descendants, it’s the name of the database that contains the object. NULL if unknown. |
| SCHEMA\_NAME | TEXT | Name of the source schema. For a schema row, this is the schema’s own name. For tables and views, it’s the name of the schema that contains the object. NULL for database rows. |
| ROW\_COUNT | NUMBER | Number of rows in the object, when known. NULL for containers. |
| BYTES | NUMBER | Size of the object in bytes, when known. NULL for containers. |
| COLUMNS | VARIANT | For table-like objects, an ARRAY of OBJECTs that describe the object’s columns. Each element has the following keys:   - `name`: Name of the column. - `data_type`: Data type of the column in the source system. - `description`: Description of the column. - `is_nullable`: Whether the column accepts NULL values. - `is_primary_key`: Whether the column is part of the primary key.   NULL for containers. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The view includes objects that were removed from the source system. The `DELETED` column is non-NULL for those objects, and
  their rows remain in the view; no retention limit currently applies. To list only current objects, filter on `DELETED IS NULL`.
- Columns that apply only to some object types are NULL for the other types. For example, `ROW_COUNT`, `BYTES`, and `COLUMNS` are NULL
  for databases and schemas.
- To walk the hierarchy, join `PARENT_REFERENCE_ID` to `REFERENCE_ID`. Joining on these columns is more reliable than joining on
  names, because names can collide across containers or change when a container is renamed. The hierarchy for most connectors is
  database, then schema, then table-like object.
- Users and roles that have been granted the OBJECT\_VIEWER database role can access this view. For more information, see
  [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
- Access to this view isn’t controlled by privileges on metadata connectors. A role that can query the view sees the objects
  from every connector in the account, including connectors it has no `USAGE` or `READ EXTERNAL METADATA` privilege on.

## Examples

List the largest current tables and views that a BigQuery connector collected:

Copy code

```
SELECT name, object_type, database_name, schema_name, row_count, bytes, last_altered
  FROM snowflake.account_usage.external_dwh_objects
  WHERE connector_type = 'BIGQUERY'
    AND object_type IN ('TABLE', 'VIEW')
    AND deleted IS NULL
  ORDER BY bytes DESC;
```

Find schemas that contain no current objects:

Copy code

```
SELECT s.reference_id, s.database_name, s.name AS schema_name, s.connector
  FROM snowflake.account_usage.external_dwh_objects s
  WHERE s.object_type = 'SCHEMA'
    AND s.deleted IS NULL
    AND NOT EXISTS (
      SELECT 1
        FROM snowflake.account_usage.external_dwh_objects t
        WHERE t.parent_reference_id = s.reference_id
          AND t.deleted IS NULL
    );
```

List the columns of one object:

Copy code

```
SELECT c.value:name::STRING AS column_name,
       c.value:data_type::STRING AS data_type,
       c.value:is_nullable::BOOLEAN AS is_nullable
  FROM snowflake.account_usage.external_dwh_objects t,
    LATERAL FLATTEN(input => t.columns) c
  WHERE t.reference_id = '<reference_id>';
```
