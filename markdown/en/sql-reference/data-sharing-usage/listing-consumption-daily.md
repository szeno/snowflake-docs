Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# LISTING\_CONSUMPTION\_DAILY view

This view in the DATA\_SHARING\_USAGE schema can be used to analyze consumption of a Snowflake Native App or shared data associated with listings
in a data exchange, such as the Snowflake Marketplace. The view returns a record for each consumer account that queried data for a given date.

## Columns

**LISTING\_CONSUMPTION\_DAILY**

| Field | Type | Description |
| --- | --- | --- |
| EVENT\_DATE | DATETIME | Date of the consumption. |
| EXCHANGE\_NAME | VARCHAR | Name of the data exchange or the Snowflake Marketplace to which the listing belongs. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the consumption occurred. |
| LISTING\_NAME | VARCHAR | Identifier for the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. Unique for each listing and is used to create the listing URL. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the data product owner. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Account name of the data product owner. |
| SHARE\_NAME | VARCHAR | Share name. If your data product is a Snowflake Native App, this is NULL. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator name of the consumer. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account name of the consumer. |
| CONSUMER\_ORGANIZATION | VARCHAR | Organization name of the consumer. |
| JOBS | NUMBER | Total jobs run that day on the data product. A job is recorded when a consumer query resolves objects included in the data share or Snowflake Native App attached to the listing. |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account of the consumer is located. |
| CONSUMER\_NAME | VARCHAR | Contains the company name of the consumer account that accessed, used, or requested a listing. If no name is available, such as for trial accounts, the value is NULL. |
| UNIQUE\_USERS\_1D | NUMBER | Count of unique users (within the consumer account) who had jobs running on the date of consumption (EVENT\_DATE). |
| UNIQUE\_USERS\_7D | NUMBER | Count of unique users (within the consumer account) who had jobs running within the 7-day period ending on the date of consumption (EVENT\_DATE). |
| UNIQUE\_USERS\_28D | NUMBER | Count of unique users (within the consumer account) who had jobs running within the 28-day period ending on the date of consumption (EVENT\_DATE). |
| CONSUMER\_MCD\_STATUS | VARCHAR | The Marketplace Capacity Drawdown (MCD) status of the consumer account. One of:   - `ENROLLED`: The consumer account is enrolled in the MCD program. - `ELIGIBLE`: The consumer account is eligible to enroll in the MCD program but isn’t currently enrolled. - `NOT ELIGIBLE`: The consumer account isn’t eligible for the MCD program. |
| CONSUMER\_MCD\_OPT\_IN\_RANGE | VARCHAR | The number of days since the consumer account enrolled in the Marketplace Capacity Drawdown (MCD) program, expressed as a range. One of:   - `< 30 days` - `30-60 days` - `60-90 days` - `90-120 days` - `> 120 days`   The upper bound of each range is exclusive. If the consumer account isn’t enrolled in the MCD program, the value is NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).
- The view contains data for all data products, whether your data product is a Snowflake Native App or a share.

## Examples

Shows top listings by consumption for a given time period:

Copy code

```
 SELECT
   listing_name,
   listing_display_name,
   SUM(jobs) AS jobs
FROM snowflake.data_sharing_usage.listing_consumption_daily
WHERE 1=1
   AND event_date BETWEEN '2021-01-01' AND '2021-01-31'
GROUP BY 1,2
ORDER BY 3 DESC
```

Shows top consumers by listing:

Copy code

```
SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY listing_name, listing_display_name ORDER BY jobs DESC) AS rank
FROM (
  SELECT
    listing_name,
    listing_display_name,
    consumer_account_locator,
    SUM(jobs) AS jobs
  FROM snowflake.data_sharing_usage.listing_consumption_daily
  WHERE 1=1
    AND event_date BETWEEN '2021-01-01' AND '2021-01-31'
  GROUP BY 1,2,3
)
ORDER BY
  listing_name,
  listing_display_name,
  rank
```
