Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# REPLICATION\_GROUP\_USAGE\_HISTORY view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query the replication history for a specified
[replication or failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

The returned results include the replication or
failover group name, credits consumed, and bytes transferred for replication. Usage data is retained for 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the replication usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the replication usage took place. |
| REPLICATION\_GROUP\_NAME | VARCHAR | Name of the secondary replication or failover group. |
| REPLICATION\_GROUP\_ID | NUMBER | Internal/system-generated identifier for the replication or failover group. |
| CREDITS\_USED | NUMBER | Total number of credits used for replication during the START\_TIME and END\_TIME window. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for replication during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- Results are only returned for secondary failover or replication groups in the target account.
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
