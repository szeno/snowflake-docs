Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEMANTIC\_VIEW\_IMPORTS view

This ACCOUNT\_USAGE view displays a row for each import entry in a [semantic view](/user-guide/views-semantic/overview) that uses the `IMPORTS` clause to compose with another semantic view.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `semantic_view_import_id` | NUMBER | Internal, Snowflake-generated identifier for the import entry. |
| `semantic_view_import_name` | VARCHAR | Name of the import entry (system-generated, format: SYS\_IMPORT\_<uuid>). |
| `semantic_view_id` | NUMBER | Internal, Snowflake-generated identifier for the semantic view that contains the import. |
| `semantic_view_name` | VARCHAR | Name of the semantic view that contains the import. |
| `semantic_view_schema_id` | NUMBER | Internal, Snowflake-generated identifier for the schema of the semantic view. |
| `semantic_view_schema_name` | VARCHAR | Schema of the semantic view. |
| `semantic_view_database_id` | NUMBER | Internal, Snowflake-generated identifier for the database of the semantic view. |
| `semantic_view_database_name` | VARCHAR | Database of the semantic view. |
| `imported_semantic_view_database_name` | VARCHAR | Database of the imported semantic view. |
| `imported_semantic_view_schema_name` | VARCHAR | Schema of the imported semantic view. |
| `imported_semantic_view_name` | VARCHAR | Name of the imported semantic view. |
| `facts_selection` | ARRAY | Facts selected by this import. NULL when the FACTS sub-clause is omitted. |
| `dimensions_selection` | ARRAY | Dimensions selected by this import. NULL when the DIMENSIONS sub-clause is omitted. |
| `metrics_selection` | ARRAY | Metrics selected by this import. NULL when the METRICS sub-clause is omitted. |
| `created` | TIMESTAMP\_LTZ | Date and time the import entry was created. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. |
| `deleted` | TIMESTAMP\_LTZ | Date and time the import entry was deleted. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the import entries for the semantic view `COMPOSED_SALES` in the database `MY_DB`:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_VIEW_IMPORTS
  WHERE semantic_view_name = 'COMPOSED_SALES'
    AND semantic_view_database_name = 'MY_DB';
```
