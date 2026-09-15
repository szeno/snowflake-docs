Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEMANTIC\_VIEW\_IMPORTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each import entry in a [semantic view](/user-guide/views-semantic/overview) that uses the IMPORTS clause to compose with another semantic view.

See also:
:   [SEMANTIC\_VIEW\_IMPORTS view](/sql-reference/account-usage/semantic_view_imports)

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| SEMANTIC\_VIEW\_IMPORT\_ID | NUMBER | Internal, Snowflake-generated identifier for the import entry. |
| SEMANTIC\_VIEW\_IMPORT\_NAME | VARCHAR | Name of the import entry (system-generated). |
| SEMANTIC\_VIEW\_ID | NUMBER | Internal, Snowflake-generated identifier for the semantic view that contains the import. |
| SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the semantic view that contains the import. |
| SEMANTIC\_VIEW\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier for the schema of the semantic view. |
| SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema of the semantic view. |
| SEMANTIC\_VIEW\_DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier for the database of the semantic view. |
| SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database of the semantic view. |
| IMPORTED\_SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database of the imported semantic view. |
| IMPORTED\_SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema of the imported semantic view. |
| IMPORTED\_SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the imported semantic view. |
| FACTS\_SELECTION | ARRAY | Facts selected by this import. NULL when the FACTS sub-clause is omitted. |
| DIMENSIONS\_SELECTION | ARRAY | Dimensions selected by this import. NULL when the DIMENSIONS sub-clause is omitted. |
| METRICS\_SELECTION | ARRAY | Metrics selected by this import. NULL when the METRICS sub-clause is omitted. |
| CREATED | TIMESTAMP\_LTZ | Date and time the import entry was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DDL or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time the import entry was deleted. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
