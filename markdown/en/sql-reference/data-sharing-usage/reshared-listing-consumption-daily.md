Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# RESHARED\_LISTING\_CONSUMPTION\_DAILY view

This view in the DATA\_SHARING\_USAGE schema can be used to track resharing activity for listings published in a data exchange or the
Snowflake Marketplace. The view returns a record for each resharer account that has active reshares of a listing for a given date.

Use this view to:

- Identify which accounts are resharing your listings.
- Monitor the number of active reshares per listing over time.
- Understand the geographic distribution of resharing activity by region and region group.

## Columns

**RESHARED\_LISTING\_CONSUMPTION\_DAILY**

| Field | Type | Description |
| --- | --- | --- |
| EVENT\_DATE | DATE | Date of the reshared listing consumption. |
| EXCHANGE\_NAME | VARCHAR | Name of the data exchange or the Snowflake Marketplace to which the listing belongs. |
| LISTING\_NAME | VARCHAR | Identifier for the listing that was reshared. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. Unique for each listing and is used to create the listing URL. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the data product owner (the provider). |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Account name of the data product owner (the provider). |
| RESHARER\_REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the resharer account is located. |
| RESHARER\_SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the resharer account is located. |
| RESHARER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the account that reshared the listing. |
| RESHARER\_ACCOUNT\_NAME | VARCHAR | Account name of the account that reshared the listing. |
| RESHARER\_ORGANIZATION\_NAME | VARCHAR | Organization name of the account that reshared the listing. |
| NUMBER\_OF\_ACTIVE\_RESHARES | NUMBER | Total number of active reshares of the listing by the resharer on the given date. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).
- The view only returns data for listings owned by the current account.
- Internal Snowflake organization accounts are excluded from the results unless the querying account belongs to an internal organization.

## Examples

Shows the total number of active reshares per listing for a given time period:

Copy code

```
SELECT
  listing_name,
  listing_display_name,
  SUM(number_of_active_reshares) AS total_active_reshares
FROM snowflake.data_sharing_usage.reshared_listing_consumption_daily
WHERE event_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY ALL
ORDER BY total_active_reshares DESC;
```

Shows the top resharers by listing:

Copy code

```
SELECT
  listing_name,
  listing_display_name,
  resharer_account_name,
  resharer_organization_name,
  SUM(number_of_active_reshares) AS total_active_reshares
FROM snowflake.data_sharing_usage.reshared_listing_consumption_daily
WHERE event_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY ALL
ORDER BY listing_name, total_active_reshares DESC;
```

Shows resharing activity by region:

Copy code

```
SELECT
  resharer_snowflake_region,
  resharer_region_group,
  COUNT(DISTINCT resharer_account_locator) AS unique_resharers,
  SUM(number_of_active_reshares) AS total_active_reshares
FROM snowflake.data_sharing_usage.reshared_listing_consumption_daily
WHERE event_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY ALL
ORDER BY total_active_reshares DESC;
```
