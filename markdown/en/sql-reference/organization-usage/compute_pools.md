Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# COMPUTE\_POOLS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool)
across all the accounts in your organization, including compute pools that have been dropped.

See also:
:   [COMPUTE\_POOLS view](/sql-reference/account-usage/compute_pools) (Account Usage)

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
| NAME | VARCHAR | Compute pool name. |
| ID | NUMBER | Internal, Snowflake-generated identifier for the compute pool. |
| IS\_SUSPENDED | BOOLEAN | Whether the pool is currently suspended. |
| MIN\_NODES | NUMBER | Minimum number of nodes in the compute pool. |
| MAX\_NODES | NUMBER | Maximum number of nodes in the compute pool. |
| INSTANCE\_FAMILY | VARCHAR | Machine type of nodes in the compute pool. |
| AUTO\_SUSPEND\_SECS | NUMBER | Number of seconds of inactivity after which the compute pool is automatically suspended. |
| AUTO\_RESUME | BOOLEAN | Whether the compute pool is automatically resumed when Snowflake attempts to start a service or job. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the compute pool was created. |
| LAST\_RESUMED | TIMESTAMP\_LTZ | Date and time when the suspended compute pool was last resumed. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the compute pool was last updated. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the compute pool was deleted. |
| OWNER | VARCHAR | Role name that owns the compute pool. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of the role that owns the compute pool. |
| IS\_EXCLUSIVE | BOOLEAN | Whether the compute pool was created for an application. |
| APPLICATION\_NAME | VARCHAR | Application name for which the compute pool was created. Null if the compute pool was not created for an application or if the application no longer exists. |
| APPLICATION\_ID | NUMBER | Application ID for which the compute pool was created. Null if the compute pool was not created for an application. |
| COMMENT | VARCHAR | A comment. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
