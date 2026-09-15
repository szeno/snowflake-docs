# SEMANTIC\_METRICS view

This Information Schema view displays a row for each metric in a semantic view in the specified (or current) database.

See also:
:   [SEMANTIC\_METRICS view (Account Usage)](/sql-reference/account-usage/semantic_metrics)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_catalog` | VARCHAR | Database to which the semantic view belongs. |
| `semantic_view_schema` | VARCHAR | Schema to which the semantic view belongs. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `table_name` | VARCHAR | Name of the semantic table the metric belongs to. |
| `name` | VARCHAR | Name of the metric. |
| `data_type` | VARCHAR | Data type of the metric expression. |
| `expression` | VARCHAR | The SQL expression used to calculate the metric. |
| `synonyms` | ARRAY(VARCHAR) | List of the synonyms for the metric. |
| `comment` | VARCHAR | Description of the metric. |

Expand

Show lessSee more

## Access control requirements

[Private metrics](/user-guide/views-semantic/sql#label-semantic-views-private) are included only if you are using a role that has been
[granted the REFERENCES or OWNERSHIP privilege on the semantic view](/user-guide/views-semantic/sql#label-semantic-views-privileges).

Otherwise, the view lists only the public metrics.
