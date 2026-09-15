# SEMANTIC\_DIMENSIONS view

This Information Schema view displays a row for each dimension in a semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_DIMENSIONS view (Account Usage)](/sql-reference/account-usage/semantic_dimensions)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_catalog` | VARCHAR | Database to which the semantic view belongs. |
| `semantic_view_schema` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `table_name` | VARCHAR | Name of the semantic table the dimension belongs to. |
| `name` | VARCHAR | Name of the dimension. |
| `data_type` | VARCHAR | Data type of the dimension expression. |
| `expression` | VARCHAR | The SQL expression used to calculate the dimension. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the dimension. |
| `comment` | VARCHAR | Description of the dimension. |
| `cortex_search_service_database_name` | VARCHAR | Name of the database containing the [Cortex Search Service that the dimension uses](/user-guide/views-semantic/sql#label-semantic-views-create-cortex-search-service-dimension). |
| `cortex_search_service_schema_name` | VARCHAR | Name of the schema containing the Cortex Search Service that the dimension uses. |
| `cortex_search_service_name` | VARCHAR | Name of the Cortex Search Service that the dimension uses. |
| `cortex_search_service_column_name` | VARCHAR | Name of the column that the Cortex Search Service allows you to search on, if the dimension uses a Cortex Search Service. |

Expand

Show lessSee more
