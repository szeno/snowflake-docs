Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_TABLES view

This ACCOUNT\_USAGE view displays a row for each logical table defined in a
[semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_TABLES view (Information Schema)](/sql-reference/info-schema/semantic_tables)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_table_id` | NUMBER | Internal, Snowflake-generated identifier for the table in the semantic view. |
| `semantic_table_name` | VARCHAR | Name of the table in the semantic view. |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view in which the table is defined. |
| `semantic_view_name` | VARCHAR | Name of the semantic view in which the table is defined. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| `semantic_view_schema_name` | VARCHAR | Schema that the semantic view belongs to. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| `semantic_view_database_name` | VARCHAR | Database that the semantic view belongs to. |
| `base_table_name` | VARCHAR | Name of the base table. |
| `base_table_schema_name` | VARCHAR | Schema that the base table belongs to. |
| `base_table_database_name` | VARCHAR | Database that the base table belongs to. |
| `primary_keys` | ARRAY(VARCHAR) | List of the primary key columns of the table. |
| `unique_keys` | ARRAY(ARRAY) | List of the unique key column groups of the table. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the table. |
| `distinct_ranges` | ARRAY(OBJECT) | Array of OBJECT values, which describe the [constraints for the logical table containing the range](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins). Each object contains the following key-value pairs:   - `constraint_name`: The name of the constraint. - `end_column`: The name of the column that represents the end of the range. - `start_column`: The name of the column that represents the start of the range. |
| `created` | TIMESTAMP\_LTZ | Creation time of the table. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| `deleted` | TIMESTAMP\_LTZ | Date and time when the table was dropped. |
| `comment` | VARCHAR | Comment for the table. |
| `definition` | VARCHAR | The SQL query that defines the logical table, if the table is defined as a [SQL query](/user-guide/views-semantic/inline-view) rather than a physical table. NULL if the table uses a physical base table. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the list of all logical tables for the semantic view `O_TPCH_SEMANTIC_VIEW` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_TABLES
  WHERE semantic_view_name = 'O_TPCH_SEMANTIC_VIEW'
    AND semantic_view_database_name = 'MY_DB';
```

```
+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+------------------+----------+-------------------------------+-------------------------------+---------+---------+
| SEMANTIC_TABLE_ID | SEMANTIC_TABLE_NAME | SEMANTIC_VIEW_ID | SEMANTIC_VIEW_NAME   | SEMANTIC_VIEW_SCHEMA_ID | SEMANTIC_VIEW_SCHEMA_NAME | SEMANTIC_VIEW_DATABASE_ID | SEMANTIC_VIEW_DATABASE_NAME | PRIMARY_KEYS     | SYNONYMS | CREATED                       | LAST_ALTERED                  | DELETED | COMMENT |
|-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+------------------+----------+-------------------------------+-------------------------------+---------+---------|
|               101 | LINEITEM            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.363 -0800 | 2025-02-28 16:16:04.363 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "L_ORDERKEY",  |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             |   "L_LINENUMBER" |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
|                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.309 -0800 | 2025-02-28 16:16:04.309 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "C_CUSTKEY"    |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
|               100 | ORDERS              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.321 -0800 | 2025-02-28 16:16:04.321 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "O_ORDERKEY"   |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
|               102 | SUPPLIER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.376 -0800 | 2025-02-28 16:16:04.376 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "S_SUPPKEY"    |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
|                98 | NATION              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.294 -0800 | 2025-02-28 16:16:04.294 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "N_NATIONKEY"  |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
|                97 | REGION              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | [                | NULL     | 2025-02-28 16:16:04.249 -0800 | 2025-02-28 16:16:04.249 -0800 | NULL    | NULL    |
|                   |                     |                  |                      |                         |                           |                           |                             |   "R_REGIONKEY"  |          |                               |                               |         |         |
|                   |                     |                  |                      |                         |                           |                           |                             | ]                |          |                               |                               |         |         |
+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+------------------+----------+-------------------------------+-------------------------------+---------+---------+
```
