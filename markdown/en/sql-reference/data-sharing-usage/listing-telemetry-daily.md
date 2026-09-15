Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# LISTING\_TELEMETRY\_DAILY view

The LISTING\_TELEMETRY\_DAILY view in the DATA\_SHARING\_USAGE schema displays daily telemetry data by data exchange and region.
The view returns a row for each data exchange in your organization and each region where that data exchange is available.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| EXCHANGE\_NAME | VARCHAR | Name of the data exchange the listing belongs to, such as the Snowflake Marketplace. |
| EVENT\_DATE | DATE | Date of the event. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the event occurred. If `NONE`, the event occurred for a user that is not signed in to a Snowflake account. |
| LISTING\_NAME | VARCHAR | Identifier of the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. Unique for each listing and is used to create the listing URL. |
| EVENT\_TYPE | VARCHAR | Event that occurred for the listing. Use in combination with the ACTION column. This can be one of the following:   - GET: Consumer creates a database for a free, paid, or limited trial listing, or installs a Snowflake Native App, depending on the value   of the ACTION column. - REQUEST: Consumer requests a limited trial listing or a free listing in a region where the data is not yet available. - LISTING CLICK: A user clicks the tile for a listing, such as from search or the Snowflake Marketplace page. - LISTING VIEW: A user visits the listing detail page. - UNINSTALL: Consumer uninstalls a Snowflake Native App or drops an imported database. |
| ACTION | VARCHAR | Action that was taken for the event. This can be one of the following:   - STARTED: The consumer selected **Get** or **Request** for a listing on the listing details page. - COMPLETED: can be one of the following, depending on the EVENT\_TYPE:    - For an EVENT\_TYPE of GET, indicates that a consumer installed a Snowflake Native App or created a database from the data product. For     paid and limited trial listings, this indicates that a consumer started a trial or purchased a data product.   - For an EVENT\_TYPE of REQUEST, indicates that the provider received a listing request from the consumer.   - For an EVENT\_TYPE of UNINSTALL, indicates that the consumer successfully uninstalled a Snowflake Native App or dropped an imported database. - CLICK: For a LISTING CLICK event, indicates that a consumer clicked the tile for a listing, such as from search or   the Snowflake Marketplace homepage. - VIEW: For a LISTING VIEW event, records a listing view. |
| EVENT\_COUNT | INTEGER | The total number of times this event action occurred on the event date. |
| CONSUMER\_ACCOUNTS\_DAILY | INTEGER | The count of distinct accounts that performed the given event action above. |
| CONSUMER\_ACCOUNTS\_28D | INTEGER | The count of distinct consumer accounts that performed the given event action in the past 28 days. |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account of the consumer is located. If `NONE`, the event occurred for a user that is not signed in to a Snowflake account. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).
- The view contains data for all data products, whether your data product is a Snowflake Native App or a share.

## Examples

To review the click-through rates for each listing, run the following:

Copy code

```
SELECT
  listing_name,
  listing_display_name,
  event_date,
  SUM(IFF(event_type = 'LISTING CLICK', consumer_accounts_daily, 0)) AS listing_clicks,
  SUM(IFF(event_type IN ('GET', 'REQUEST') and action = 'STARTED', consumer_accounts_daily, 0)) AS get_request_started,
  SUM(IFF(event_type IN ('GET', 'REQUEST') and action = 'COMPLETED', consumer_accounts_daily, 0)) AS get_request_completed,
  get_request_completed / NULLIFZERO(listing_clicks) AS ctr
FROM snowflake.data_sharing_usage.LISTING_TELEMETRY_DAILY
GROUP BY 1,2,3
ORDER BY 1,2,3;
```

To get a clearer sense of how many listing views are from immediate potential customers, you can use the REGION\_GROUP field to split
the total count of listing views per day by whether the view was performed by a user signed in to a Snowflake account or not:

Copy code

```
SELECT
  listing_name,
  listing_display_name,
  event_date,
  COUNT_IF(event_type= 'listing_view' AND region_group='NONE') as unknown_user_view_count,
  COUNT_IF(event_type= 'listing_view' AND region_group!='NONE') as known_user_view_count
FROM snowflake.data_sharing_usage.LISTING_TELEMETRY_DAILY
GROUP BY 1,2,3
ORDER BY 1,2,3;
```
