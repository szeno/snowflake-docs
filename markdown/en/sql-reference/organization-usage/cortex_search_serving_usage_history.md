Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

This Organization Usage view can be used to query the hourly serving usage history of [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) across all the accounts in your organization.
The information in this view includes the number of serving credits consumed per hour for a Cortex Search Service. This view
only contains credits consumed for serving, not the other costs associated with a Cortex Search Service. For more information, see
[Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

See also:
:   [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_serving_usage_history) (Account Usage)

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
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the Cortex Search serving usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the Cortex Search usage took place. |
| DATABASE\_NAME | VARCHAR | Name of the database in which the Cortex Search Service resides. |
| SCHEMA\_NAME | VARCHAR | Name of the schema in which the Cortex Search Service resides. |
| SERVICE\_NAME | VARCHAR | Name of the Cortex Search Service. |
| SERVICE\_ID | NUMBER | ID of the Cortex Search Service. |
| CREDITS | NUMBER | Number of credits billed for Cortex Search serving usage based on the size of indexed data during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- Serving credits are incurred per GB-mo of indexed data, metered at the second-level. One may get an estimate of
  the indexed data size for a given service using the credit rate defined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- This view may show small discrepancies in incurred cost from hour-to-hour based on the second-level metering.
