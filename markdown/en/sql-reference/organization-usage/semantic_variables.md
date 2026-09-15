Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEMANTIC\_VARIABLES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each variable defined in a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SEMANTIC\_VARIABLES view](/sql-reference/account-usage/semantic_variables)

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
| SEMANTIC\_VARIABLE\_ID | NUMBER | Internal, Snowflake-generated identifier for the variable. |
| SEMANTIC\_VARIABLE\_NAME | VARCHAR | Name of the variable. |
| SEMANTIC\_VIEW\_ID | NUMBER | Internal, Snowflake-generated identifier for the semantic view. |
| SEMANTIC\_VIEW\_NAME | VARCHAR | Name of the semantic view. |
| SEMANTIC\_VIEW\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier for the schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_SCHEMA\_NAME | VARCHAR | Schema that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier for the database that the semantic view belongs to. |
| SEMANTIC\_VIEW\_DATABASE\_NAME | VARCHAR | Database that the semantic view belongs to. |
| DATA\_TYPE | VARCHAR | Data type of the variable. |
| DEFAULT\_VALUE | VARCHAR | Default value of the variable, if specified. |
| CREATED | TIMESTAMP\_LTZ | Date and time the variable was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DDL or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time the variable was deleted. |
| COMMENT | VARCHAR | Description of the variable. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
