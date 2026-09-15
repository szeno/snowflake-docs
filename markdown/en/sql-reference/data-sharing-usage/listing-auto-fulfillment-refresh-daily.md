Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# LISTING\_AUTO\_FULFILLMENT\_REFRESH\_DAILY view

This view in the DATA\_SHARING\_USAGE schema can be used to determine the data refreshes performed by Cross-Cloud Auto-Fulfillment.
When a listing is fulfilled to another region, the data product is refreshed on a frequency defined by the listing provider. This view
contains details about how much data is refreshed to specific regions, and which listings and databases the data refreshes are
associated with.

You can use this view to help manage the costs associated with Cross-Cloud Auto-Fulfillment.
See [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

## Columns

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
- The data is retained for 365 days (1 year).
- The view only contains data from 2023-04-16 onward.
- In cases where auto-fulfillment is incomplete, the array returned for the LISTINGS column might be empty.
- The view contains data for all data products, whether your data product is a Snowflake Native App or a share.

Important

This view is intended to help you understand the resources used by Cross-Cloud Auto-Fulfillment. It is not intended to
be used for billing reconciliation. Instead, refer to the views in the ORGANIZATION\_USAGE schema. See
[View actual costs](/collaboration/provider-listings-auto-fulfillment-monitor-view-costs#label-listings-ccaf-costs-view).
for more details.

## Examples

Shows the sum of credits used to refresh the data associated with a specific auto-fulfillment group,
including the associated databases and listings:

Copy code

```
 SELECT
   fulfillment_group_name,
   databases,
   listings,
   SUM(credits_used) AS total_credits_used
FROM snowflake.data_sharing_usage.listing_auto_fulfillment_refresh_daily
GROUP BY 1,2,3
ORDER BY 4 DESC;
```

Shows top databases by credit usage for a given time period:

Copy code

```
 SELECT
   databases,
   listings,
   SUM(credits_used) AS total_credits_used
FROM snowflake.data_sharing_usage.listing_auto_fulfillment_refresh_daily
WHERE 1=1
   AND usage_date BETWEEN '2023-04-17' AND '2023-04-30'
GROUP BY 1,2
ORDER BY 3 DESC;
```
