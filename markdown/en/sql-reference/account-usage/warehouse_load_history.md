Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# WAREHOUSE\_LOAD\_HISTORY view

This Account Usage view can be used to analyze the workload on your warehouse within a specified date range.

See also:
:   [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history)

## Columns

Note

For the output columns of this view, the query load value is the ratio of the total execution time (in seconds) of all queries in a specific state in an interval by the total time (in seconds) for that interval.

For example, if 276 seconds was the total time for 4 queries in a 5 minute (300 second) interval, then the query load value is 276 / 300 = 0.92.

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The start of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The end of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| AVG\_RUNNING | NUMBER(38,9) | Query load value for queries executed. |
| AVG\_QUEUED\_LOAD | NUMBER(38,9) | Query load value for queries queued because the warehouse was overloaded. |
| AVG\_QUEUED\_PROVISIONING | NUMBER(38,9) | Query load value for queries queued because the warehouse was being provisioned. |
| AVG\_BLOCKED | NUMBER(38,9) | Query load value for queries blocked by a transaction lock. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- Load history is shown in 5-minute intervals.
