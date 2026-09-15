# SEMANTIC\_VIEWS view

This Information Schema view displays a row for each semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_VIEWS view (Account Usage)](/sql-reference/account-usage/semantic_views)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `catalog` | VARCHAR | Database to which the semantic view belongs. |
| `schema` | VARCHAR | Schema to which the semantic view belongs. |
| `name` | VARCHAR | Name of the semantic view. |
| `owner` | VARCHAR | Owner of the semantic view. |
| `created` | TIMESTAMP\_LTZ | Creation time of the view. |
| `comment` | VARCHAR | Description of the semantic view. |

Expand

Show lessSee more
