Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_VARIABLES view

This ACCOUNT\_USAGE view displays a row for each variable defined in a [semantic view](/user-guide/views-semantic/overview).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_variable_id` | NUMBER | Internal, Snowflake-generated identifier for the variable. |
| `semantic_variable_name` | VARCHAR | Name of the variable. |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view. |
| `semantic_view_name` | VARCHAR | Name of the semantic view. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| `semantic_view_schema_name` | VARCHAR | Schema that the semantic view belongs to. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| `semantic_view_database_name` | VARCHAR | Database that the semantic view belongs to. |
| `data_type` | VARCHAR | Data type of the variable. |
| `default_value` | VARCHAR | Default value of the variable, if specified. |
| `created` | TIMESTAMP\_LTZ | Date and time the variable was created. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. |
| `deleted` | TIMESTAMP\_LTZ | Date and time the variable was deleted. |
| `comment` | VARCHAR | Description of the variable. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the variables for the semantic view `SALES_ANALYTICS` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_VARIABLES
  WHERE semantic_view_name = 'SALES_ANALYTICS'
    AND semantic_view_database_name = 'MY_DB';
```
