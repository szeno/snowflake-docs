# Set up and manage an event table in the provider account

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can set up an event table and manage event sharing for an app.

Tip

For new deployments, we strongly recommend using
[centralized event sharing](/developer-guide/native-apps/event-central) to route events from every region
to a single destination account. Use the per-region event account setup described below only when centralized
event sharing is not an option for your deployment.

## Set up an event table in the provider organization in every region

To collect the log messages and trace events that a consumer shares, a provider must set up an event
table by performing the following:

1. [Set an account as the event account](#label-nativeapps-provider-event-table-set-account).
2. [Create an event table in the event account](#label-nativeapps-provider-event-table-create).
3. [Set the event table as the active event table in event account](#label-nativeapps-provider-event-table-set-active).

Important

If a provider does not have an event account and active event table within the region where the app is
installed before the consumer installs an app, trace events and log messages from that region are dropped
(events access loss for the provider). Consumer event tables continue to capture the data locally; only the
shared copy that would have flowed to the provider is lost.

For multi-region centralization without per-region event accounts, see
[Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

### Set an account as the events account

To store shared logs and events, a provider must select an account to hold an event table. This can be any
account that a provider can access. However, if an organization has multiple providers publishing
application packages, consider using a Snowflake account that is dedicated to storing shared events from the
consumer.

The following restrictions apply to accounts used to store shared events:

- You must use an [organization administrator role](/user-guide/organization-administrators) to set an account as the account used
  to store events.
- The account must have an active event table.
- The specified account cannot be any of the following:
  - A locked or suspended account.
  - A reader account.
  - A trial account.
  - A Snowflake managed account.

Note

A provider can collect logs and shared events only in the same region where a consumer installs an app.
Providers must set up an event account to store shared events in every region where consumers configure event
sharing for an app.

To set an account to be the events account for a region, call the [SYSTEM$SET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_set_event_sharing_account_for_region)
system function as shown in the following example:

Copy code

```
SELECT SYSTEM$SET_EVENT_SHARING_ACCOUNT_FOR_REGION('<snowflake_region>', '<region_group>', '<account_name>')
```

Where:

`snowflake_region`
:   Specifies the region where the account is located, for example: `AWS_US_WEST_2, AWS_US_EAST_1`.

`region_group`
:   Specifies the region group, for example: `PUBLIC`. Refer to
    [Region groups](/user-guide/admin-account-identifier#label-region-groups) for details.

`account_name`
:   Specifies the account name. If another account is already set as the events account in the
    specified region, running this command changes the events account to be the account
    specified here.

### Create an event table in the event account

To create an event table, run the [CREATE EVENT TABLE](/sql-reference/sql/create-event-table) command as shown in the
following example:

Copy code

```
CREATE EVENT TABLE event_db.event_schema.my_event_table;
```

This command specifies the database and schema that contain the event table.

## Set the event table as the active event table

An account can have multiple event tables, but only one can be set as the active event table in a
Snowflake account at a time. Without an active event table, log messages and trace events that the consumer
shares are discarded.

After creating the event table, use [ALTER ACCOUNT … SET EVENT\_TABLE](/sql-reference/sql/alter-account)
to specify that the event table is the active table for the account:

Copy code

```
ALTER ACCOUNT SET EVENT_TABLE=event_db.event_schema.my_event_table;
```

## Unset an account as the events account

To unset an account to be the events account for a region, call the
[SYSTEM$UNSET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_unset_event_sharing_account_for_region) system function:

Copy code

```
SELECT SYSTEM$UNSET_EVENT_SHARING_ACCOUNT_FOR_REGION('<snowflake_region>', '<region_group>', '<account_name>')
```

Where:

`snowflake_region`
:   Specifies the region where the account is located, for example: `AWS_US_WEST_2`.

`region_group`
:   Specifies the region group, for example: `PUBLIC`.

`account_name`
:   Specifies the account name.

## View the event accounts in an organization

To show events accounts in a provider’s organization, call the
[SYSTEM$SHOW\_EVENT\_SHARING\_ACCOUNTS](/sql-reference/functions/system_show_event_sharing_accounts) system function:

Copy code

```
SELECT SYSTEM$SHOW_EVENT_SHARING_ACCOUNTS()
```

Note

You must use an [organization administrator role](/user-guide/organization-administrators) to call this function.

This system function returns a string in JSON format containing a list of event accounts within the organization.
Because the metadata takes some time to propagate to all regions, this function might have a short delay before
showing the most current events account after the user sets or unsets the event account for the organization.

## View the logging and trace event levels defined in an application package

Use the [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) command to view the logging level of the app versions
defined in an application package, as shown in the following example:

Copy code

```
SHOW VERSIONS
  IN APPLICATION PACKAGE HelloSnowflake;
```

## View the logs and events in the event table

To view the logs and events stored in the event table, use the [SELECT](/sql-reference/sql/select) command as shown
in the following example:

Copy code

```
SELECT * FROM EVENT_DB.EVENT_SCHEMA.MY_EVENT_TABLE
```

For more information on querying the event table, see the following:

- [Viewing log messages](/developer-guide/logging-tracing/logging-accessing-messages)
- [Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events)

See [Event table columns](/developer-guide/logging-tracing/event-table-columns) for information on the columns
in the event table.

## Shared event information available to the provider

The following sections describe the information that the Snowflake Native App Framework shares with providers and how sensitive identifiers
are protected before events leave the consumer account.

### App event context shared with the provider

To help providers identify the source of shared events, the following fields are populated into the
`RESOURCE_ATTRIBUTES` column when events are shared with the provider:

- `snow.application.package.name`
- `snow.application.consumer.account_locator`
- `snow.application.consumer.account_name`
- `snow.application.consumer.organization`
- `snow.application.consumer.name` (deprecated)
- `snow.application.consumer.snowflake_region`
- `snow.listing.name`
- `snow.listing.global_name`

### Field categorization for privacy and masking

Fields fall into three categories: shared (visible to the provider), masked (hashed before sharing), and omitted
(never leave the consumer account).

| Field category | Shared, masked, or omitted | Details and examples |
| --- | --- | --- |
| Application info | Shared | `APPLICATION_PROVIDER_ORG`, `APPLICATION_PROVIDER_NAME`. Application name and application instance name are not shared; they are hashed and shared as `snow.application.hash` (see masked row below). |
| Listing info | Shared | `LISTING_NAME`, `LISTING_GLOBAL_NAME` |
| SPCS info | Shared | `DEPLOYMENT_NAME`, `NODE_ID`, `CONTAINER_NAME`, `RUN_ID`, `INSTANCE_FAMILY`, `SERVICE_NAME`, `SERVICE_INSTANCE`, `SERVICE_TYPE` |
| Database and query identifiers | Masked (SHA-1) | `snow.database.hash`, `snow.query.hash`, `snow.application.hash` |
| Sensitive database info | Omitted | `snow.database.id`, `snow.database.name`, `snow.schema.id`, `snow.executable.id` |
| Environment info | Omitted | `snow.warehouse.name`, `snow.warehouse.id`, `snow.query.id`, `snow.session.id` |
| Role and user info | Omitted | `snow.session.role.primary.name`, `snow.session.role.primary.id`, `snow.user.name`, `snow.user.id`, `db.user` |
| SPCS environment | Omitted | Compute pool name, compute pool ID, service UUID. Compute pool fields are shared only when the Snowflake Native App manages the compute pool. |
| Other identifiers | Omitted | `snow.owner.name`, `snow.owner.id` |

Expand

Show lessSee more

Snowflake provides the [SHA-1 function](/sql-reference/functions/sha1) so consumers can derive the same hash
values for `snow.database.name` and `snow.query.id` and use them as reference values when contacting the
provider. The system function [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application)
returns the same hash an installed app’s identifiers map to, so consumers can correlate shared events with their
local queries.

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Same-account event sharing (sharing events back to the same account that owns the application package) is
currently in preview. The same field categorization and masking apply once event sharing is enabled in the
same account.
