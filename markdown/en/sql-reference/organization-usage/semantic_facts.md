Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEMANTIC\_FACTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each fact defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_FACTS view](/sql-reference/account-usage/semantic_facts)

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
| SEMANTIC\_FACT\_ID | NUMBER | ID of the fact in the semantic view. |
| SEMANTIC\_FACT\_NAME | VARCHAR | Name of the fact in the semantic view. |
| SEMANTIC\_TABLE\_ID | NUMBER | ID of the semantic table the fact belongs to. |
| SEMANTIC\_TABLE\_NAME | VARCHAR | Name of the semantic table the fact belongs to. |
| SEMANTIC\_VIEW\_ID | NUMBER | ID of the semantic view. |
| SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the semantic view. |
| SEMANTIC\_VIEW\_SCHEMA\_ID | NUMBER | ID of the schema to which the semantic view belongs. |
| SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema to which the semantic view belongs. |
| SEMANTIC\_VIEW\_DATABASE\_ID | NUMBER | ID of the database to which the semantic view belongs. |
| SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database to which the semantic view belongs. |
| DATA\_TYPE | VARCHAR | Data type of the fact expression. |
| EXPRESSION | VARCHAR | The SQL expression used to calculate the fact. |
| SYNONYMS | ARRAY | List of the synonyms for the fact. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the fact. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DDL or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the fact was dropped. |
| COMMENT | VARCHAR | Description of the fact. |
| LABELS | ARRAY | List of labels associated with the fact. |
| ACCESS\_MODIFIER | VARCHAR | Access modifier for the fact. |
| LOD\_DIMENSIONS | ARRAY | List of dimensions that define the level of detail for the fact. |
| LOD\_DIMENSION\_TYPE | VARCHAR | Type of level-of-detail dimension applied to the fact. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
