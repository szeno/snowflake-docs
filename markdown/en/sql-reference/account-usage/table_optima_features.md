Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_OPTIMA\_FEATURES view

This Account Usage view displays whether [Snowflake Optima](/user-guide/snowflake-optima) Metadata, Indexing, or Clustering
is applied to each table in the account. Use this dictionary view with
[TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_query_pruning_history) and
[AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history) to report on Optima feature use and query optimization
benefits.

Each row represents a table and indicates which Optima capabilities apply to that table.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| OPTIMA\_METADATA\_APPLIED | BOOLEAN | Indicates whether Snowflake Optima Metadata is applied to the table. |
| OPTIMA\_INDEXING\_APPLIED | BOOLEAN | Indicates whether Snowflake Optima Indexing is applied to the table. |
| OPTIMA\_CLUSTERING\_APPLIED | BOOLEAN | Indicates whether Snowflake Optima Clustering is applied to the table. |

Expand

Show lessSee more

## Usage notes

- Users and roles that have been granted the OBJECT\_VIEWER database role can access this view. For more information, see
  [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
