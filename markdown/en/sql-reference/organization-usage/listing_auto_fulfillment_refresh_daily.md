Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# LISTING\_AUTO\_FULFILLMENT\_REFRESH\_DAILY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to determine the data refreshes performed by Cross-Cloud Auto-Fulfillment for the listings owned by the accounts in your organization.
When a listing is fulfilled to another region, the data product is refreshed on a frequency defined by the listing provider. This view
contains details about how much data is refreshed to specific regions, and which listings and databases the data refreshes are
associated with.

This view is the organization-wide counterpart of the [LISTING\_AUTO\_FULFILLMENT\_REFRESH\_DAILY view in the DATA\_SHARING\_USAGE schema](/sql-reference/data-sharing-usage/listing-auto-fulfillment-refresh-daily), which returns the rows for a single provider account.
The columns, other than the common organization columns, and the usage notes are the same.

You can use this view to help manage the costs associated with Cross-Cloud Auto-Fulfillment.
See [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

This view is available only in the [organization account](/user-guide/organization-accounts). Users with the GLOBALORGADMIN role, or users granted the SNOWFLAKE.ORGANIZATION\_SECURITY\_VIEWER application role, can access it. For details, see [Accessing the ORGANIZATION\_USAGE schema](/sql-reference/organization-usage#label-org-usage-access-org-account).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

The ORGANIZATION\_NAME, ACCOUNT\_LOCATOR, and ACCOUNT\_NAME columns identify the provider account that owns the listings.

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the data refresh occurred. |
| SNOWFLAKE\_REGION | VARCHAR | [Snowflake region](/user-guide/admin-account-identifier#label-snowflake-region-ids) where the data refresh occurred. |
| USAGE\_DATE | DATE | Date in UTC when the refresh was performed. |
| FULFILLMENT\_GROUP\_NAME | VARCHAR | Identifier for the auto-fulfillment group used to refresh the data. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for refreshes in this day. |
| CREDITS\_USED | NUMBER | Number of credits used for refreshes in this day. |
| DATABASES | ARRAY | List of databases refreshed in the auto-fulfillment group. Returns an empty array until a listing is successfully fulfilled to a region. |
| LISTINGS | ARRAY | List of listings that reference the databases in this region. Returns an empty array until a listing is successfully fulfilled to a region. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 1 year.
- The view only contains data from 2023-04-16 onward.
- In cases where auto-fulfillment is incomplete, the array returned for the LISTINGS column might be empty.
- The view contains data for all data products, whether your data product is a Snowflake Native App or a share.

Important

This view is intended to help you understand the resources used by Cross-Cloud Auto-Fulfillment. It is not intended to
be used for billing reconciliation. Instead, use the [LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history).

## Examples

### Credits used by provider account

To show the credits used in the last 30 days to refresh data, broken down by provider account, run the following statement:

Copy code

```
select
  account_name,
  sum(credits_used) as total_credits_used,
  sum(bytes_transferred) as total_bytes_transferred
from SNOWFLAKE.ORGANIZATION_USAGE.LISTING_AUTO_FULFILLMENT_REFRESH_DAILY
where usage_date >= dateadd('day', -30, current_date())
group by account_name
order by total_credits_used desc;
```

### Credits used by auto-fulfillment group

To show the credits used in the last 30 days to refresh the data associated with each auto-fulfillment group, including the associated databases and listings, run the following statement:

Copy code

```
select
  account_name,
  fulfillment_group_name,
  databases,
  listings,
  sum(credits_used) as total_credits_used
from SNOWFLAKE.ORGANIZATION_USAGE.LISTING_AUTO_FULFILLMENT_REFRESH_DAILY
where usage_date >= dateadd('day', -30, current_date())
group by 1,2,3,4
order by total_credits_used desc;
```
