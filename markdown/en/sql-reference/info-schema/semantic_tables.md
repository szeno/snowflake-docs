# SEMANTIC\_TABLES view

This Information Schema view displays a row for each logical table in a semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_TABLES view (Account Usage)](/sql-reference/account-usage/semantic_tables)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_catalog` | VARCHAR | Database to which the semantic view belongs. |
| `semantic_view_schema` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `name` | VARCHAR | Name of the semantic table. |
| `base_table_catalog` | VARCHAR | Database to which the base table belongs. |
| `base_table_schema` | VARCHAR | Schema to which the base table belongs. |
| `base_table_name` | VARCHAR | Name of the base table. |
| `primary_keys` | ARRAY(VARCHAR) | List of the primary key columns of the table. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the table. |
| `distinct_ranges` | ARRAY(OBJECT) | Array of OBJECT values, which describe the [constraints for the logical table containing the range](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins). Each object contains the following key-value pairs:   - `constraint_name`: The name of the constraint. - `end_column`: The name of the column that represents the end of the range. - `start_column`: The name of the column that represents the start of the range. |
| `comment` | VARCHAR | Description of the semantic table. |
| `definition` | VARCHAR | The SQL query that defines the logical table, if the table is defined as a [SQL query](/user-guide/views-semantic/inline-view) rather than a physical table. NULL if the table uses a physical base table. |

Expand

Show lessSee more
