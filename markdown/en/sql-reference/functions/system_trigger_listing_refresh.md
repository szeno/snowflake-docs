Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$TRIGGER\_LISTING\_REFRESH

Triggers a one-time, on-demand data refresh for a provider’s databases or listings, accessible to all consumers. The refresh job begins immediately upon triggering and can be tracked using the [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history) function. Consumers can track the refresh using the [AVAILABLE\_LISTING\_REFRESH\_HISTORY](/sql-reference/functions/available_listing_refresh_history) function. You can trigger a listing refresh even if you have already set up a scheduled refresh or interval-based refresh.

Note

A completed trigger listing refresh will skip the next interval-based refresh.

For details on the refresh types available for your listings, see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

See also:
:   [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history)

## Syntax

Copy code

```
SYSTEM$TRIGGER_LISTING_REFRESH( '<type>' , '<name>' )
```

## Arguments

**Required:**

`'type'`
:   Type of dataset to refresh (`LISTING` or `DATABASE`). Note that the dataset type must be enclosed in single quotes.

`'name'`
:   Name of the listing or database. Note that the entire name must be enclosed in single quotes.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE LISTING AUTO FULFILLMENT | Account | This privilege grants the ability to publish listings to remote regions. |
| USAGE | Listing or database |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For share-based data product listings, the database associated with the listing is replicated and refreshed across all regions managed by
  auto-fulfillment.
- Application and application package data product listings refresh according to the value of the [LISTING\_AUTO\_FULFILLMENT\_REPLICATION\_REFRESH\_SCHEDULE](/sql-reference/parameters#label-listing-auto-fulfillment-replication-refresh-schedule)
  parameter set on the account. All listings using this schedule are refreshed simultaneously.

## Examples

Copy code

```
SELECT SYSTEM$TRIGGER_LISTING_REFRESH('DATABASE', 'MY_DATABASE');
```
