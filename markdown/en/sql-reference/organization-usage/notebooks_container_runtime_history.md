[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

You can use the NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view in the ORGANIZATION\_USAGE schema to return the hourly credit usage for notebooks running on Snowpark Container Services across accounts in your organization.

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
| NOTEBOOK\_NAME | VARCHAR | The name of the notebook (running on Snowpark Container Services) that incurred the credit usage. |
| NOTEBOOK\_ID | NUMBER | The ID of the notebook that incurred the credit usage. |
| USER\_NAME | VARCHAR | The name of the user associated with the notebook. NULL if the notebook was not run interactively. |
| USER\_ID | NUMBER | The ID of the user associated with the notebook. NULL if the notebook was not run interactively. |
| COMPUTE\_POOL\_NAME | VARCHAR | The name of the compute pool associated with the notebook. |
| COMPUTE\_POOL\_ID | NUMBER | The ID of the compute pool associated with the notebook. |
| SERVICE\_NAME | VARCHAR | The name of the service associated with the notebook. |
| SERVICE\_ID | NUMBER | The ID of the service associated with the notebook. |
| NOTEBOOK\_EXECUTION\_TIME\_SECS | NUMBER | The run time of the notebook in the given hour. |
| CREDITS | NUMBER(38, 9) | The number of credits that the notebook used in the hour. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
- The view provides hourly container notebook credit usage across accounts in your organization within the last 365 days (1 year).
- The credit rate usage is determined based on the machine type (instance family) of the compute pool, as outlined in the consumption table.
