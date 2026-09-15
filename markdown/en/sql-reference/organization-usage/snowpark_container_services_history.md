Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view

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

This Organization Usage view can be used to query the hourly
[compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) credit usage across all the accounts in your
organization.

See also:
:   [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view](/sql-reference/account-usage/snowpark_container_services_history) (Account Usage)

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
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the compute pool which incurred the credit usage. |
| COMPUTE\_POOL\_ID | NUMBER | Internal, Snowflake-generated identifier of the compute pool which incurred the credit usage. |
| IS\_EXCLUSIVE | BOOLEAN | TRUE, if the compute pool was created for an [application](/developer-guide/native-apps/native-apps-about). |
| APPLICATION\_NAME | VARCHAR | The name of the application for which the compute pool was created. NULL if the compute pool was not created for an application or if the application no longer exists. |
| APPLICATION\_ID | NUMBER | The ID of the application for which the compute pool was created; otherwise NULL. |
| CREDITS\_USED | NUMBER | Number of credits the compute pool used in the hour. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The credit rate usage is determined based on the machine type (instance family) of the compute pool, as outlined in the consumption table.
- Rows are only included for hours in which a compute pool consumed credits.
