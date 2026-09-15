# CORTEX\_SEARCH\_SERVICES view

This view shows existing Cortex Search Services in the current or specified database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_CATALOG | VARCHAR | Database that the service belongs to. |
| SERVICE\_SCHEMA | VARCHAR | Schema that the service belongs to. |
| SERVICE\_NAME | VARCHAR | Name of the service. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the service. |
| DEFINITION | VARCHAR | SQL query used to create the service. |
| SEARCH\_COLUMN | VARCHAR | Name of the search column. |
| ATTRIBUTE\_COLUMNS | VARCHAR | Comma-separated list of attribute columns in the service. |
| COLUMNS | VARCHAR | Comma-separated list of all columns included in the service. |
| TARGET\_LAG | VARCHAR | Target lag for refreshing the service. |
| WAREHOUSE | VARCHAR | Name of the warehouse used for refreshing the service. |
| COMMENT | VARCHAR | Comment for this service. |
| SERVICE\_QUERY\_URL | VARCHAR | URL for querying the service. |
| OWNER | VARCHAR | Role that owns the service. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role of the service owner (one of DATABASE\_ROLE or ROLE). |
| DATA\_TIMESTAMP | TIMESTAMP\_LTZ | Time at which the source data was checked for changes resulting in the currently serving index. |
| SOURCE\_DATA\_BYTES | NUMBER | Current size, in bytes, of the materialized source data. |
| SOURCE\_DATA\_NUM\_ROWS | NUMBER | Current number of rows in the materialized source data. |
| INDEXING\_STATE | VARCHAR | Indexing state of the service (one of SUSPENDED or RUNNING). |
| INDEXING\_ERROR | VARCHAR | Error encountered in the last indexing pipeline, if one exists. |
| SERVING\_STATE | VARCHAR | Serving state of the service (one of SUSPENDED or RUNNING). |
| SERVING\_DATA\_BYTES | NUMBER | Size of the billable serving data, in bytes. |
| EMBEDDING\_MODEL | VARCHAR | The vector embedding model used by the service. |
| PRIMARY\_KEY\_COLUMNS | VARCHAR | Comma-separated list of primary key column names defined on the service. Empty if no primary key is set. |

Expand

Show lessSee more

## Example

Copy code

```
SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.CORTEX_SEARCH_SERVICES;
```
