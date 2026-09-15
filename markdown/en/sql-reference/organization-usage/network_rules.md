Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# NETWORK\_RULES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns one row for each network rule in an account.

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
| `id` | NUMBER | Internal system-generated identifier for network rule. |
| `name` | VARCHAR | Network rule name. |
| `schema_id` | NUMBER | Internal system-generated identifier for the schema that contains the network rule. |
| `schema_name` | VARCHAR | Name of the schema that contains the network rule. |
| `database_id` | NUMBER | Internal system-generated identifier for the database that contains the network rule. |
| `database_name` | VARCHAR | Name of the database that contains the network rule. |
| `owner` | VARCHAR | Name of role that owns the network rule. |
| `owner_role_type` | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| `comment` | VARCHAR | Comment for the network rule (if any). |
| `created` | TIMESTAMP\_LTZ | Date and time that the network rule was created. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time that the network rule was last altered. |
| `deleted` | TIMESTAMP\_LTZ | Date and time the network rule was dropped. |
| `mode` | VARCHAR | Mode of the network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |
| `type` | VARCHAR | Type of network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |
| `value_list` | VARCHAR | List of values for the network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.

- The view only displays objects for which the current role for the session has been granted access privileges.

## Example

To see current Snowflake-managed rules, *including* IP addresses, query the [NETWORK\_RULES view](/sql-reference/organization-usage/network_rules) view and filter on rows where the database is SNOWFLAKE and the schema is NETWORK\_SECURITY:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.NETWORK_RULES
  WHERE DATABASE_NAME = 'SNOWFLAKE' AND SCHEMA_NAME = 'NETWORK_SECURITY';
```
