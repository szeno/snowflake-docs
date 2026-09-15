Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# MATERIALIZED\_VIEW\_REFRESH\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Materialized views require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query the [materialized views](/user-guide/views-materialized) refresh history. The information returned by the view includes the view name and credits consumed each time a materialized view is refreshed.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | VARCHAR | Number of credits billed for materialized view maintenance during the START\_TIME and END\_TIME window. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the materialized view. |
| TABLE\_NAME | VARCHAR | Name of the materialized view. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the materialized view. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the materialized view. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the materialized view. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the materialized view. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```

- The history is displayed in increments of 1 hour.
