Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUERY\_ACCELERATION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

The [query acceleration service](/user-guide/query-acceleration-service) requires Enterprise Edition (or higher).
To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query the history of queries accelerated by the
[query acceleration service](/user-guide/query-acceleration-service). The information returned by the view includes the warehouse name
and the credits consumed by the query acceleration service.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for the query acceleration service during the START\_TIME and END\_TIME window. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |

Expand

Show lessSee more

## Usage notes

- Billing history is not necessarily updated immediately. Latency for the view may be up to 180 minutes (3 hours).

- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```

## Examples

This query returns the total number of credits used by each warehouse in your account for the query acceleration service
(month-to-date):

Copy code

```
SELECT warehouse_name,
       SUM(credits_used) AS total_credits_used
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
  WHERE start_time >= DATE_TRUNC(month, CURRENT_DATE)
  GROUP BY 1
  ORDER BY 2 DESC;
```
