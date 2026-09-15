Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_DIMENSIONS view

This ACCOUNT\_USAGE view displays a row for each dimension defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_DIMENSIONS view (Information Schema)](/sql-reference/info-schema/semantic_dimensions)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_dimension_id` | NUMBER | ID of the dimension in the semantic view. |
| `semantic_dimension_name` | VARCHAR | Name of the dimension in the semantic view. |
| `semantic_table_id` | NUMBER | ID of the semantic table the dimension belongs to. |
| `semantic_table_name` | VARCHAR | Name of the semantic table the dimension belongs to. |
| `semantic_view_id` | NUMBER | ID of the semantic view. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `semantic_view_schema_id` | NUMBER | ID of the schema to which the semantic view belongs. |
| `semantic_view_schema_name` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_database_id` | NUMBER | ID of the database to which the semantic view belongs. |
| `semantic_view_database_name` | VARCHAR | Database to which the semantic view belongs. |
| `data_type` | VARCHAR | Data type of the dimension expression. |
| `expression` | VARCHAR | The SQL expression used to calculate the dimension. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the dimension. |
| `created` | TIMESTAMP\_LTZ | Creation time of the dimension. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| `deleted` | TIMESTAMP\_LTZ | Date and time when the dimension was dropped. |
| `comment` | VARCHAR | Description of the dimension. |
| `cortex_search_service_database` | VARCHAR | Name of the database containing the [Cortex Search Service that the dimension uses](/user-guide/views-semantic/sql#label-semantic-views-create-cortex-search-service-dimension). |
| `cortex_search_service_schema` | VARCHAR | Name of the schema containing the Cortex Search Service that the dimension uses. |
| `cortex_search_service` | VARCHAR | Name of the Cortex Search Service that the dimension uses. |
| `cortex_search_service_column` | VARCHAR | Name of the column that the Cortex Search Service allows you to search on, if the dimension uses a Cortex Search Service. |
| `labels` | ARRAY(VARCHAR) | List of labels associated with the dimension. |
| `lod_dimensions` | ARRAY(VARCHAR) | List of dimensions that define the level of detail for the dimension. |
| `lod_dimension_type` | VARCHAR | Type of level-of-detail dimension applied to the dimension. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the list of all dimensions for the semantic view `O_TPCH_SEMANTIC_VIEW` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_DIMENSIONS
  WHERE semantic_view_name = 'O_TPCH_SEMANTIC_VIEW'
    AND semantic_view_database_name = 'MY_DB';
```

```
+-----------------------+------------------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------+----------------------+----------+-------------------------------+-------------------------------+---------+---------+
| SEMANTIC_DIMENSION_ID | SEMANTIC_DIMENSION_NAME            | SEMANTIC_TABLE_ID | SEMANTIC_TABLE_NAME | SEMANTIC_VIEW_ID | SEMANTIC_VIEW_NAME   | SEMANTIC_VIEW_SCHEMA_ID | SEMANTIC_VIEW_SCHEMA_NAME | SEMANTIC_VIEW_DATABASE_ID | SEMANTIC_VIEW_DATABASE_NAME | DATA_TYPE   | EXPRESSION           | SYNONYMS | CREATED                       | LAST_ALTERED                  | DELETED | COMMENT |
|-----------------------+------------------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------+----------------------+----------+-------------------------------+-------------------------------+---------+---------|
|                   391 | D_CUSTOMER_REGION_NAME_FROM_REGION |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | region.d_region_name | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   392 | D_CUSTOMER_NATION_NAME             |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | nation.d_nation_name | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   393 | D_CUSTOMER_MARKET_SEGMENT          |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(10) | c_mktsegment         | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   387 | D_NATION_NAME                      |                98 | NATION              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | n_name               | NULL     | 2025-02-28 16:16:04.388 -0800 | 2025-02-28 16:16:04.388 -0800 | NULL    | NULL    |
|                   389 | D_REGION_NAME                      |                97 | REGION              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | r_name               | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   394 | D_CUSTOMER_COUNTRY_CODE            |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(15) | LEFT(c_phone, 2)     | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   390 | D_CUSTOMER_REGION_NAME             |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | nation.d_region_name | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                   388 | D_REGION_NAME                      |                98 | NATION              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | VARCHAR(25) | region.d_region_name | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
+-----------------------+------------------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+-------------+----------------------+----------+-------------------------------+-------------------------------+---------+---------+
```
