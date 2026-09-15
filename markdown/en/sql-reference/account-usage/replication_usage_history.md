Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# REPLICATION\_USAGE\_HISTORY view

Deprecated Feature

This view has been deprecated.

- Use [DATABASE\_REPLICATION\_USAGE\_HISTORY view](/sql-reference/account-usage/database_replication_usage_history) for database replication.
- Use [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history) for account replication.

This Account Usage view can be used to query the replication history for a specified database. The returned results include the database name, credits consumed, and bytes transferred for replication. Usage data is retained for 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the replication usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the replication usage took place. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| CREDITS\_USED | NUMBER | Total number of credits used for database replication during the START\_TIME and END\_TIME window. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for database replication during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- The view displays data starting from September 1, 2019.
