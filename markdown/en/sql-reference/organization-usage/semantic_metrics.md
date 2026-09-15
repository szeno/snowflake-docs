Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEMANTIC\_METRICS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each metric defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_METRICS view](/sql-reference/account-usage/semantic_metrics)

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
| SEMANTIC\_METRIC\_ID | NUMBER | ID of the metric in the semantic view. |
| SEMANTIC\_METRIC\_NAME | VARCHAR | Name of the metric in the semantic view. |
| SEMANTIC\_TABLE\_ID | NUMBER | ID of the logical table the metric belongs to. |
| SEMANTIC\_TABLE\_NAME | VARCHAR | Name of the logical table the metric belongs to. |
| SEMANTIC\_VIEW\_ID | NUMBER | Internal, Snowflake-generated identifier for the semantic view in which the metric is defined. |
| SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the semantic view in which the metric is defined. |
| SEMANTIC\_VIEW\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database that the semantic view belongs to. |
| DATA\_TYPE | VARCHAR | Data type of the metric expression. |
| EXPRESSION | VARCHAR | The SQL expression used to calculate the metric. |
| SYNONYMS | ARRAY | List of the synonyms for the metric. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the metric. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DDL or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the metric was dropped. |
| COMMENT | VARCHAR | Description of the metric. |
| ADDITIVE\_DIMENSIONS | ARRAY | List of dimensions from the semantic view that the metric can be grouped by. |
| NON\_ADDITIVE\_DIMENSIONS | ARRAY | List of dimensions from the semantic view that the metric cannot be grouped by. |
| USING\_RELATIONSHIPS | ARRAY | List of relationship names that the metric uses. |
| ACCESS\_MODIFIER | VARCHAR | Access modifier for the metric. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
