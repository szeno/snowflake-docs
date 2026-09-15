Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# EVENT\_ROUTING\_TABLES view

Use this view to query the event routing tables in the current organization.
Event routing tables are used to route telemetry data (logs and traces) from Snowflake Native Apps
deployed across multiple regions to a centralized destination account.

For more information, see [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal identifier for the event routing table. |
| NAME | TEXT | Name of the event routing table. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the event routing table was created. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | Date and time when the event routing table was last modified. NULL if the table has never been modified. |

Expand

Show lessSee more

## Usage notes

- Latency for the view might be up to 120 minutes (2 hours).
- The view displays only event routing tables that belong to the organization of the current account.
- Dropped event routing tables don’t appear in this view.
