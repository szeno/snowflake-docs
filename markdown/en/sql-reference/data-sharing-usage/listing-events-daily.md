Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# LISTING\_EVENTS\_DAILY view

The LISTING\_EVENTS\_DAILY view in the [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage) schema lets you query the daily history of
consumer activity on listings for the Snowflake Marketplace and data exchanges, including:

- Consumer installs a database from a listing.
- Consumer installs a Snowflake Native App.
- Consumer requests unlimited access to a limited trial listing or a free listing where data is not yet available.
- Consumer installs the trial data product for a paid listing or limited trial listing.
- Consumer buys a paid listing from the Snowflake Marketplace.
- Consumer decides to no longer use the paid data for a paid listing.
- Consumer uninstalls a Snowflake Native App or drops an imported database.

The view includes the history of consumer activity for a specific listing.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_DATE | DATE | Date of the event. |
| EXCHANGE\_NAME | VARCHAR | Name of the data exchange the listing belongs to, such as the Snowflake Marketplace. |
| EVENT\_TYPE | VARCHAR | One of:   - `GET`: Consumer creates a database for a free listing, or installs a Snowflake Native App. - `REQUEST`: Consumer requests a “by request” (personalized) listing, a limited trial listing, or a free listing that’s in a region where the data isn’t yet available. - `TRIAL`: Consumer creates a trial database or installs a trial Snowflake Native App. - `PURCHASE`: Consumer agrees to be invoiced when paid data in a paid listing is queried. - `CANCEL PURCHASE`: Consumer decides to stop using the paid data in a paid listing. - `UNINSTALL`: Consumer uninstalls a Snowflake Native App or drops an imported database. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the `REQUEST` or `GET` event occurred. |
| LISTING\_NAME | VARCHAR | Identifier of the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. Unique for each listing and is used to create the listing URL. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer account. For more information about account identifiers, see [account identifier](/user-guide/admin-account-identifier). |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Name of the consumer account. |
| CONSUMER\_ORGANIZATION | VARCHAR | Organization name of the consumer account. |
| CONSUMER\_EMAIL | VARCHAR | Email address for the consumer account (if available). |
| TERMS\_ACCEPTED\_DATE | DATETIME | Timestamp when the consumer accepted the listing terms. |
| CONSUMER\_METADATA | VARIANT | Other information included by the consumer when the event happened, such as their name or the reason for using a free email address. |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account of the consumer is located. |
| CONSUMER\_NAME | VARCHAR | Contains the company name of the consumer account that accessed, used, or requested a listing. If a name is unavailable, such as for trial accounts, the value is NULL. |
| ACCESS\_TYPE | VARCHAR | The listing access type. The access type is also called the monetization type. |
| EVENT\_TIMESTAMP | DATETIME | The date and time that a listing-related event occurred. |
| CONSUMER\_MCD\_STATUS | VARCHAR | The Marketplace Capacity Drawdown (MCD) status of the consumer account. One of:   - `ENROLLED`: The consumer account is enrolled in the MCD program. - `ELIGIBLE`: The consumer account is eligible to enroll in the MCD program but isn’t currently enrolled. - `NOT ELIGIBLE`: The consumer account isn’t eligible for the MCD program. |
| CONSUMER\_MCD\_OPT\_IN\_RANGE | VARCHAR | The number of days since the consumer account enrolled in the Marketplace Capacity Drawdown (MCD) program, expressed as a range. One of:   - `< 30 days` - `30-60 days` - `60-90 days` - `90-120 days` - `> 120 days`   The upper bound of each range is exclusive. If the consumer account isn’t enrolled in the MCD program, the value is NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).
- The view contains data for all data products, whether your data product is a Snowflake Native App or a share.

## Examples

Shows daily count of gets and requests by listing:

Copy code

```
SELECT
  listing_name,
  listing_display_name,
  event_date,
  event_type,
  SUM(1) AS count_gets_requests
FROM snowflake.data_sharing_usage.listing_events_daily
GROUP BY 1,2,3,4
```
