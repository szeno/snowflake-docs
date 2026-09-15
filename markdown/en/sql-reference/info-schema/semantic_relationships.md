# SEMANTIC\_RELATIONSHIPS view

This Information Schema view displays a row for each relationship in a semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_RELATIONSHIPS view (Account Usage)](/sql-reference/account-usage/semantic_relationships)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_catalog` | VARCHAR | Database to which the semantic view belongs. |
| `semantic_view_schema` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `name` | VARCHAR | Name of the semantic relationship. |
| `table_name` | VARCHAR | Name of the semantic table referencing the other table. |
| `foreign_keys` | ARRAY(VARCHAR) | List of the names of the columns referring to the columns of the other table. |
| `ref_table_name` | VARCHAR | Name of the semantic table being referenced. |
| `ref_keys` | ARRAY(VARCHAR) | One of the following values:  - For relationships that represent [range joins](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins), an array that contains   JSON-formatted strings for objects with the following keys:    - The `start_column` key specifies the name of the column that represents the start of the range.   - The `end_column` key specifies the name of the column that represents the end of the range.   - The `type` key is `RANGE`. - For relationships that represent [ASOF joins](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof), an array that contains the   following elements:    - The name of the column in the first table.   - A JSON object with the following fields:     - `column`: Name of the column in the second table.     - `type`: `ASOF`.   - For other types of relationships, an array containing the name of the column in the other logical table in the relationship. |

Expand

Show lessSee more
