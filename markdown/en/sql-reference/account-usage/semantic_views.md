Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_VIEWS view

This ACCOUNT\_USAGE view displays a row for each [semantic view](/user-guide/views-semantic/overview) in the account.

See also:
:   [SEMANTIC\_VIEWS view (Information Schema)](/sql-reference/info-schema/semantic_views)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| `semantic_view_schema_name` | VARCHAR | Schema that the semantic view belongs to. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| `semantic_view_database_name` | VARCHAR | Database that the semantic view belongs to. |
| `owner` | VARCHAR | Name of the role that owns the semantic view. |
| `created` | TIMESTAMP\_LTZ | Creation time of the semantic view. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. |
| `deleted` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| `comment` | VARCHAR | Comment for the semantic view. |
| `max_stalesness_sec` | NUMBER | Maximum staleness in seconds allowed for the semantic view materialization. NULL if no materialization target lag is set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the semantic view `O_TPCH_SEMANTIC_VIEW` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_VIEWS
  WHERE semantic_view_name = 'O_TPCH_SEMANTIC_VIEW'
    AND semantic_view_database_name = 'MY_DB';
```

```
+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-----------------+-------------------------------+-------------------------------+---------+---------+
| SEMANTIC_VIEW_ID | SEMANTIC_VIEW_NAME   | SEMANTIC_VIEW_SCHEMA_ID | SEMANTIC_VIEW_SCHEMA_NAME | SEMANTIC_VIEW_DATABASE_ID | SEMANTIC_VIEW_DATABASE_NAME | OWNER           | CREATED                       | LAST_ALTERED                  | DELETED | COMMENT |
|------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-----------------+-------------------------------+-------------------------------+---------+---------|
|               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | DYOSHINAGA_ROLE | 2025-02-28 16:16:04.002 -0800 | 2025-02-28 16:16:04.589 -0800 | NULL    | NULL    |
+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-----------------+-------------------------------+-------------------------------+---------+---------+
```
