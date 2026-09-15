Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# NETWORK\_RULE\_REFERENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns one row for each network rule that is associated with an external access integration or a network policy.

The view is complementary to the Information Schema table function [NETWORK\_RULE\_REFERENCES](/sql-reference/functions/network_rule_references).

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
| `network_rule_db` | VARCHAR | Database name that contains the network rule. |
| `network_rule_schema` | VARCHAR | Schema that contains the network rule. |
| `network_rule_id` | NUMBER | Internal system-generated identifier for the network rule. |
| `network_rule_mode` | VARCHAR | Either: `ingress` or `egress`. |
| `network_rule_type` | VARCHAR | Either: `AWSLinkId`, `AzureLinkId`, `HOST_PORT`, or `IPV4`. |
| `network_rule_name` | VARCHAR | Name of the network rule. |
| `container_id` | NUMBER | Internal system-defined identifier for the container. |
| `container_name` | VARCHAR | Name of the external access integration or network policy with which the network rule is associated. |
| `container_type` | VARCHAR | Either: `INTEGRATION` or `NETWORK_POLICY`. |
| `action_type` | VARCHAR | Either: `ALLOW` or `BLOCK`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.

- The view only displays objects for which the current role for the session has been granted access privileges.
