Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEMANTIC\_TABLES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each table reference defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_TABLES view](/sql-reference/account-usage/semantic_tables)

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
| SEMANTIC\_TABLE\_ID | NUMBER | Internal, Snowflake-generated identifier for the table in the semantic view. |
| SEMANTIC\_TABLE\_NAME | VARCHAR | Name of the table in the semantic view. |
| SEMANTIC\_VIEW\_ID | NUMBER | Internal, Snowflake-generated identifier for the semantic view in which the table is defined. |
| SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the semantic view in which the table is defined. |
| SEMANTIC\_VIEW\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database that the semantic view belongs to. |
| BASE\_TABLE\_NAME | VARCHAR | Name of the base table. |
| BASE\_TABLE\_SCHEMA\_NAME | VARCHAR | Schema that the base table belongs to. |
| BASE\_TABLE\_DATABASE\_NAME | VARCHAR | Database that the base table belongs to. |
| PRIMARY\_KEYS | ARRAY | List of the primary key columns of the table. |
| UNIQUE\_KEYS | ARRAY | List of the unique key column groups of the table. |
| SYNONYMS | ARRAY | List of the synonyms for the table. |
| DISTINCT\_RANGES | ARRAY | List of distinct range specifications for the table. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the table. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DDL or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the table was dropped. |
| COMMENT | VARCHAR | Comment for the table. |
| DEFINITION | VARCHAR | The SQL query that defines the logical table, if defined as a SQL query rather than a physical table. NULL if the table uses a physical base table. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
