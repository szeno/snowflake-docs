Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This view in the ORGANIZATION\_USAGE schema can be used to estimate the costs associated with
[Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment#label-how-auto-fulfillment-works).

When a data product is fulfilled to a region, Snowflake uses a managed account associated with your provider account, called a
*secure share area*, to store the data product in each region with consumer demand. Your provider account incurs costs associated
with the secure share areas in other regions.

For more details, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

Note

Because this view provides estimated values, the usage and currency values might not match the values in the
[USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily) or your usage statement.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| CONTRACT\_NUMBER | VARCHAR | Snowflake contract number for the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the secure share area where the usage occurred. |
| ACCOUNT\_LOCATOR | VARCHAR | Locator for the secure share area where the usage occurred. |
| REGION | VARCHAR | Name of the region where the secure share area is located. |
| SERVICE\_LEVEL | VARCHAR | Service level (edition) of the secure share area. See [Snowflake editions](/user-guide/intro-editions). |
| USAGE\_DATE | DATE | Date (in UTC format) in which the secure share area usage took place. |
| SERVICE\_TYPE | VARCHAR | Can be one of:   - DATA\_TRANSFER - REPLICATION - STORAGE |
| CURRENCY | VARCHAR | Currency of the usage. |
| ESTIMATED\_USAGE | NUMBER (38,9) | Estimated amount of usage to be charged based on SERVICE\_TYPE. Units of USAGE depend on the SERVICE\_TYPE. For example, when the SERVICE\_TYPE is REPLICATION, USAGE is measured in credits. When the SERVICE\_TYPE is DATA\_TRANSFER or STORAGE, USAGE is measured in terabytes. |
| ESTIMATED\_USAGE\_IN\_CURRENCY | NUMBER (38,9) | Estimated amount to be charged for the SERVICE\_TYPE for USAGE on the USAGE\_DATE. |
| PROVIDER\_ACCOUNT\_REGION | VARCHAR | Name of the region where the provider account that shared the data product is located. If NULL, the usage could not be attributed to a specific provider account. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Name of the provider account that shared the data product that incurred the usage in the secure share area. If NULL, the usage could not be attributed to a specific provider account. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Locator for the provider account that shared the data product that incurred the usage in the secure share area. If NULL, the usage could not be attributed to a specific provider account. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
