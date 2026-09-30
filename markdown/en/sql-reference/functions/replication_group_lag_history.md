Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_GROUP\_LAG\_HISTORY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the replication lag history for a secondary failover group over a time
window. The results show how the replication lag for the group changed over time, returned as a step
function that you can plot.

The lag at a point in time is the difference between that time and the primary snapshot timestamp of
the most recent completed refresh. Between refreshes, the lag increases as time passes. When a
refresh completes, the lag drops because a newer snapshot becomes available.

By default (when no date-range arguments are provided), the function returns data for the last 24 hours.

See also:
:   [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) , [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/account-usage/replication_group_refresh_history)

## Syntax

Copy code

```
REPLICATION_GROUP_LAG_HISTORY(
      REPLICATION_GROUP_NAME => '<string>'
      [ , START_TIME => <constant_expr> ]
      [ , END_TIME => <constant_expr> ] )
```

## Arguments

`REPLICATION_GROUP_NAME => 'string'`
:   Name of the secondary failover group to report on. The value must be a non-NULL
    constant and enclosed in single quotes. This argument is required.

The following arguments are optional.

`START_TIME => constant_expr` , `END_TIME => constant_expr`
:   The `TIMESTAMP_LTZ` time window (inclusive) for which to return the lag history:

    - If neither `START_TIME` nor `END_TIME` is specified, the default is the last 24 hours.
    - If `START_TIME` is omitted, it defaults to 24 hours before the current timestamp.
    - If `END_TIME` is omitted, it defaults to the current timestamp.

    Both arguments must be constant values.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| TIMESTAMP | TIMESTAMP\_LTZ | Point in time for the lag measurement. |
| LAG\_SECONDS | NUMBER | Replication lag, in seconds, at that timestamp. This is the difference between `TIMESTAMP` and `PRIMARY_SNAPSHOT_TIMESTAMP`. |
| PRIMARY\_SNAPSHOT\_TIMESTAMP | TIMESTAMP\_LTZ | Primary snapshot timestamp from the most recent completed refresh in effect at that timestamp. |

Expand

Show lessSee more

## Usage notes

- When no `START_TIME` or `END_TIME` arguments are provided, the function returns data for the last
  24 hours. To retrieve data beyond the last 24 hours, specify the time window explicitly.
- The function returns two rows for each refresh interval so that the lag history renders as a
  step (sawtooth) function: one row at the moment a refresh completes (the start of the step), and
  one row just before the next refresh, or before the window’s end time for the final interval (the
  end of the step). Rows are ordered by `TIMESTAMP`, and then by `LAG_SECONDS`.
- Only returns rows for a secondary replication or failover group in the current account.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the replication lag history for the last 24 hours (default) for secondary group `myrg`:

Copy code

```
SELECT TIMESTAMP, LAG_SECONDS, PRIMARY_SNAPSHOT_TIMESTAMP
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_LAG_HISTORY(
          REPLICATION_GROUP_NAME => 'myrg')
  );
```

Retrieve the replication lag history for a specific time window for secondary group `myrg`:

Copy code

```
SELECT TIMESTAMP, LAG_SECONDS, PRIMARY_SNAPSHOT_TIMESTAMP
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_LAG_HISTORY(
          REPLICATION_GROUP_NAME => 'myrg',
          START_TIME => '2024-01-01'::TIMESTAMP_LTZ,
          END_TIME => '2024-01-31'::TIMESTAMP_LTZ)
  );
```
