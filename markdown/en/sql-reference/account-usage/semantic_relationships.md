Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_RELATIONSHIPS view

This ACCOUNT\_USAGE view displays a row for each relationship defined in a
[semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_RELATIONSHIPS view (Information Schema)](/sql-reference/info-schema/semantic_relationships)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_relationship_id` | NUMBER | Internal, Snowflake-generated identifier for the relationship in the semantic view. |
| `semantic_relationship_name` | VARCHAR | Name of the relationship in the semantic view. |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view in which the relationship is defined. |
| `semantic_view_name` | VARCHAR | Name of the semantic view in which the relationship is defined. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| `semantic_view_schema_name` | VARCHAR | Schema that the semantic view belongs to. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| `semantic_view_database_name` | VARCHAR | Database that the semantic view belongs to. |
| `semantic_table_id` | NUMBER | Internal, Snowflake-generated identifier for the logical table being referenced. |
| `semantic_table_name` | VARCHAR | Name of the logical table referencing the other table. |
| `foreign_keys` | ARRAY(VARCHAR) | List of the names of the columns referring to the columns of the other table. |
| `ref_semantic_table_id` | NUMBER | Internal, Snowflake-generated identifier for the logical table referencing the other table. |
| `ref_semantic_table_name` | VARCHAR | Name of the logical table being referenced. |
| `ref_keys` | ARRAY(VARCHAR) | One of the following values:  - For relationships that represent [range joins](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins), an array that contains   JSON-formatted strings for objects with the following keys:    - The `start_column` key specifies the name of the column that represents the start of the range.   - The `end_column` key specifies the name of the column that represents the end of the range.   - The `type` key is `RANGE`. - For relationships that represent [ASOF joins](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof), an array that contains the   following elements:    - The name of the column in the first table.   - A JSON object with the following fields:     - `column`: Name of the column in the second table.     - `type`: `ASOF`.   - For other types of relationships, an array containing the name of the column in the other logical table in the relationship. |
| `created` | TIMESTAMP\_LTZ | Creation time of the relationship. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| `deleted` | TIMESTAMP\_LTZ | Date and time when the relationship was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the list of all relationships for the semantic view `O_TPCH_SEMANTIC_VIEW` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_RELATIONSHIPS
  WHERE semantic_view_name = 'O_TPCH_SEMANTIC_VIEW'
    AND semantic_view_database_name = 'MY_DB';
```

```
+--------------------------+-------------------------------------------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------------+---------------------+-----------------+-----------------------+-------------------------+-----------------+-------------------------------+-------------------------------+---------+
| SEMANTIC_RELATIONSHIP_ID | SEMANTIC_RELATIONSHIP_NAME                            | SEMANTIC_VIEW_ID | SEMANTIC_VIEW_NAME   | SEMANTIC_VIEW_SCHEMA_ID | SEMANTIC_VIEW_SCHEMA_NAME | SEMANTIC_VIEW_DATABASE_ID | SEMANTIC_VIEW_DATABASE_NAME | SEMANTIC_TABLE_ID | SEMANTIC_TABLE_NAME | FOREIGN_KEYS    | REF_SEMANTIC_TABLE_ID | REF_SEMANTIC_TABLE_NAME | REF_KEYS        | CREATED                       | LAST_ALTERED                  | DELETED |
|--------------------------+-------------------------------------------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------------+---------------------+-----------------+-----------------------+-------------------------+-----------------+-------------------------------+-------------------------------+---------|
|                       99 | SYS_RELATIONSHIP_67ae9bb4-652a-4985-8dc5-c99fdf7f4276 |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       |               100 | ORDERS              | [               |                    99 | CUSTOMER                | [               | 2025-02-28 16:16:04.321 -0800 | 2025-02-28 16:16:04.321 -0800 | NULL    |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     |   "O_CUSTKEY"   |                       |                         |   "C_CUSTKEY"   |                               |                               |         |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     | ]               |                       |                         | ]               |                               |                               |         |
|                      100 | SYS_RELATIONSHIP_906b4d92-582a-4bef-b2c1-9a69e8f61af1 |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       |               101 | LINEITEM            | [               |                   100 | ORDERS                  | [               | 2025-02-28 16:16:04.363 -0800 | 2025-02-28 16:16:04.363 -0800 | NULL    |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     |   "L_ORDERKEY"  |                       |                         |   "O_ORDERKEY"  |                               |                               |         |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     | ]               |                       |                         | ]               |                               |                               |         |
|                      101 | SYS_RELATIONSHIP_fadc2c0f-db3a-48e4-b96a-53ea2767a2b0 |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       |               102 | SUPPLIER            | [               |                    98 | NATION                  | [               | 2025-02-28 16:16:04.376 -0800 | 2025-02-28 16:16:04.376 -0800 | NULL    |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     |   "S_NATIONKEY" |                       |                         |   "N_NATIONKEY" |                               |                               |         |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     | ]               |                       |                         | ]               |                               |                               |         |
|                       98 | SYS_RELATIONSHIP_8c9ad09e-0ba4-489f-aabb-0503ef80e11b |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       |                99 | CUSTOMER            | [               |                    98 | NATION                  | [               | 2025-02-28 16:16:04.309 -0800 | 2025-02-28 16:16:04.309 -0800 | NULL    |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     |   "C_NATIONKEY" |                       |                         |   "N_NATIONKEY" |                               |                               |         |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     | ]               |                       |                         | ]               |                               |                               |         |
|                       97 | SYS_RELATIONSHIP_8529b4a7-eaff-4c36-888f-d9e1ad2683de |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       |                98 | NATION              | [               |                    97 | REGION                  | [               | 2025-02-28 16:16:04.294 -0800 | 2025-02-28 16:16:04.294 -0800 | NULL    |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     |   "N_REGIONKEY" |                       |                         |   "R_REGIONKEY" |                               |                               |         |
|                          |                                                       |                  |                      |                         |                           |                           |                             |                   |                     | ]               |                       |                         | ]               |                               |                               |         |
+--------------------------+-------------------------------------------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------------+---------------------+-----------------+-----------------------+-------------------------+-----------------+-------------------------------+-------------------------------+---------+
```
