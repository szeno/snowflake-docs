Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_METRICS view

This ACCOUNT\_USAGE view displays a row for each metric defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_METRICS view (Information Schema)](/sql-reference/info-schema/semantic_metrics)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_metric_id` | NUMBER | ID of the metric in the semantic view. |
| `semantic_metric_name` | VARCHAR | Name of the metric in the semantic view. |
| `semantic_table_id` | NUMBER | ID of the logical table the metric belongs to. |
| `semantic_table_name` | VARCHAR | Name of the logical table the metric belongs to. |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view in which the metric is defined. |
| `semantic_view_name` | VARCHAR | Name of the semantic view in which the metric is defined. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| `semantic_view_schema_name` | VARCHAR | Schema that the semantic view belongs to. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| `semantic_view_database_name` | VARCHAR | Database that the semantic view belongs to. |
| `data_type` | VARCHAR | Data type of the metric expression. |
| `expression` | VARCHAR | The SQL expression used to calculate the metric. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the metric. |
| `created` | TIMESTAMP\_LTZ | Creation time of the metric. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| `deleted` | TIMESTAMP\_LTZ | Date and time when the metric was dropped. |
| `comment` | VARCHAR | Description of the metric. |
| `additive_dimensions` | ARRAY(VARCHAR) | List of dimensions from the semantic view that the metric can be grouped by. |
| `non_additive_dimensions` | ARRAY(VARCHAR) | List of dimensions from the semantic view that the metric cannot be grouped by. |
| `using_relationships` | ARRAY(VARCHAR) | List of relationship names that the metric uses. |
| `access_modifier` | VARCHAR | Access modifier for the metric. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the list of all metrics for the semantic view `O_TPCH_SEMANTIC_VIEW` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_METRICS
  WHERE semantic_view_name = 'O_TPCH_SEMANTIC_VIEW'
    AND semantic_view_database_name = 'MY_DB';
```

```
i+--------------------+------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+--------------+--------------------------------------+----------+-------------------------------+-------------------------------+---------+---------+
| SEMANTIC_METRIC_ID | SEMANTIC_METRIC_NAME   | SEMANTIC_TABLE_ID | SEMANTIC_TABLE_NAME | SEMANTIC_VIEW_ID | SEMANTIC_VIEW_NAME   | SEMANTIC_VIEW_SCHEMA_ID | SEMANTIC_VIEW_SCHEMA_NAME | SEMANTIC_VIEW_DATABASE_ID | SEMANTIC_VIEW_DATABASE_NAME | DATA_TYPE    | EXPRESSION                           | SYNONYMS | CREATED                       | LAST_ALTERED                  | DELETED | COMMENT |
|--------------------+------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+--------------+--------------------------------------+----------+-------------------------------+-------------------------------+---------+---------|
|                396 | M_CUSTOMER_ORDER_COUNT |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | NUMBER(30,0) | SUM(customer.a_customer_order_count) | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                395 | M_CUSTOMER_COUNT       |                99 | CUSTOMER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | NUMBER(18,0) | COUNT(c_custkey)                     | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                398 | M_SUPPLIER_COUNT       |               102 | SUPPLIER            |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | NUMBER(18,0) | COUNT(s_suppkey)                     | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
|                397 | M_ORDER_COUNT          |               100 | ORDERS              |               49 | O_TPCH_SEMANTIC_VIEW |                      92 | MY_SCHEMA                 |                         7 | MY_DB                       | NUMBER(18,0) | COUNT(o_orderkey)                    | NULL     | 2025-02-28 16:16:04.389 -0800 | 2025-02-28 16:16:04.389 -0800 | NULL    | NULL    |
+--------------------+------------------------+-------------------+---------------------+------------------+----------------------+-------------------------+---------------------------+---------------------------+-----------------------------+--------------+--------------------------------------+----------+-------------------------------+-------------------------------+---------+---------+
```
