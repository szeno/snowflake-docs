# SEMANTIC\_FACTS view

This Information Schema view displays a row for each fact in a semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_FACTS view (Account Usage)](/sql-reference/account-usage/semantic_facts)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_catalog` | VARCHAR | Database to which the semantic view belongs. |
| `semantic_view_schema` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `table_name` | VARCHAR | Name of the semantic table the fact belongs to. |
| `name` | VARCHAR | Name of the fact. |
| `data_type` | VARCHAR | Data type of the fact expression. |
| `expression` | VARCHAR | The SQL expression used to calculate the fact. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the fact. |
| `comment` | VARCHAR | Description of the fact. |

Expand

Show lessSee more

## Access control requirements

[Private facts](/user-guide/views-semantic/sql#label-semantic-views-private) are included only if you are using a role that has been
[granted the REFERENCES or OWNERSHIP privilege on the semantic view](/user-guide/views-semantic/sql#label-semantic-views-privileges).

Otherwise, the view lists only the public facts.
