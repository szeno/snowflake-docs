# Data Sharing Usage

In the SNOWFLAKE database, the DATA\_SHARING\_USAGE schema includes views that display information about listings published in the
Snowflake Marketplace or a data exchange. This includes telemetry data (number of clicks), as well as consumption data (queries
run by consumers).

Note

This data is available only to the account that published the individual listing. By default, only account administrators (users with
the ACCOUNTADMIN role) in the account can access the SNOWFLAKE database and schemas within the database, or perform queries on the
views; however, privileges on the database can be granted to other roles in your account to allow other users to access the objects.
For more details, see [Enabling other roles to use schemas in the SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles).

## DATA\_SHARING\_USAGE views

The DATA\_SHARING\_USAGE schema contains the following views:

| View | Type | Latency [1] | Retention duration | View audience |
| --- | --- | --- | --- | --- |
| [APPLICATION\_STATE](/sql-reference/data-sharing-usage/application-state-view) | Current state | up to 10 minutes | Not applicable. | Provider |
| [LISTING\_ACCESS\_HISTORY](/sql-reference/data-sharing-usage/listing-access-history) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [LISTING\_AUTO\_FULFILLMENT\_DATABASE\_STORAGE\_DAILY](/sql-reference/data-sharing-usage/listing-auto-fulfillment-database-storage-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [LISTING\_AUTO\_FULFILLMENT\_REFRESH\_DAILY](/sql-reference/data-sharing-usage/listing-auto-fulfillment-refresh-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [LISTING\_CONSUMPTION\_DAILY](/sql-reference/data-sharing-usage/listing-consumption-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [LISTING\_EVENTS\_DAILY](/sql-reference/data-sharing-usage/listing-events-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [LISTING\_TELEMETRY\_DAILY](/sql-reference/data-sharing-usage/listing-telemetry-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [MARKETPLACE\_DISBURSEMENT\_REPORT](/collaboration/views/marketplace-disbursement-report-ds) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [MARKETPLACE\_LISTING\_INVOICE\_STATUS](/collaboration/views/marketplace_listing_invoice_status) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [MARKETPLACE\_PAID\_USAGE\_DAILY](/collaboration/views/marketplace-paid-usage-daily-ds) | Historical | up to 2 days | Data retained for 1 year. | Consumer |
| [MARKETPLACE\_PROVIDER\_SPCS\_USAGE](/collaboration/views/marketplace-provider-spcs-usage-ds) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [MONETIZED\_USAGE\_DAILY](/collaboration/views/monetized-usage-daily-ds) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [PAID\_LISTING\_ACCESS\_AND\_CHANGE\_LOG](/sql-reference/data-sharing-usage/paid-listing-access-change-log) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [PROVIDER\_APPLICATION\_DAILY\_USAGE\_HISTORY](/sql-reference/data-sharing-usage/provider-application-daily-usage-history) | Historical | up to 2 days | Data retained for 1 year. | Provider |
| [RESHARED\_LISTING\_CONSUMPTION\_DAILY](/sql-reference/data-sharing-usage/reshared-listing-consumption-daily) | Historical | up to 2 days | Data retained for 1 year. | Provider |

Expand

Show lessSee more

[1] All latency times are approximate; in some instances, the actual latency may be lower.

## General usage notes

The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.
