Schema:
:   [Data Sharing Usage](/sql-reference/data-sharing-usage)

# MARKETPLACE\_PROVIDER\_SPCS\_USAGE View

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The MARKETPLACE\_PROVIDER\_SPCS\_USAGE view in the [Data Sharing Usage](/sql-reference/data-sharing-usage) schema lets providers review their daily [Snowpark Container Services (SPCS) usage](/developer-guide/snowpark-container-services/provider-pricing-surcharges). In this view, providers can see the number of compute pool hours and credits consumed by applications that the consumers purchased from the provider.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | DATETIME | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | DATETIME | The date and end of the hour (in the local time zone) in which the usage took place. |
| LISTING\_NAME | VARCHAR | Identifier for the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. |
| IDENTIFIER | VARCHAR | The compute pool name. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account locator of the consumer account. For more information about account identifiers, see [Account identifiers](/user-guide/admin-account-identifier). |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer account. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Organization name for the consumer. |
| CREDITS | VARCHAR | Credits consumed by the compute pool. |
| COMPUTE\_HOURS | VARCHAR | The number of hours consumed by the compute pool. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 48 hours (2 days).
- The data is retained for 365 days (1 year).

## Examples

Retrieve the total number of SPCS compute pool hours consumed by each of your consumers.

Copy code

```
SELECT
  start_time,
  end_time,
  listing_name,
  listing_display_name,
  listing_global_name,
  identifier,
  consumer_account_name,
  consumer_account_locator,
  consumer_organization_name,
  credits,
  compute_hours,
FROM snowflake.data_sharing_usage.marketplace_provider_spcs_usage;
```
