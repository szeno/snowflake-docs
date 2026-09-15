Categories:
:   [Table functions](/sql-reference/functions-table)

# REST\_EVENT\_HISTORY

Returns a list of SCIM REST API requests made to Snowflake over a specified time interval.

## Syntax

Copy code

```
REST_EVENT_HISTORY(
      REST_SERVICE_TYPE => 'scim'
      [, TIME_RANGE_START => <constant_expr> ]
      [, TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ] )
```

## Arguments

**Required:**

`REST_SERVICE_TYPE => 'scim'`
:   The type of REST API service. Currently, Snowflake only supports `SCIM`.

**Optional:**

`TIME_RANGE_START => <constant_expr>`, `TIME_RANGE_END => <constant_expr>`
:   Time range (in TIMESTAMP\_LTZ format), within the last 7 days, in which the login event occurred.

    - If `TIME_RANGE_START` is not specified, all logs from the last seven days are returned.
    - If `TIME_RANGE_END` is not specified, all logs are returned.

    If the time range does not fall within the last 7 days, an error is returned.

    For more information on functions that you can use, see [Date & time functions](/sql-reference/functions-date-time).

`RESULT_LIMIT => <integer>`
:   A number specifying the maximum number of rows returned by the function.

    If the number of matching rows is greater than this limit, the queries with the most recent end time (or those that are still executing) are returned, up to the specified limit.

    Range: `1` to `10000`

    Default: `100`.

## Usage notes

- Currently, the REST\_EVENT\_HISTORY table function can only be used with [SCIM](/user-guide/scim-intro).
- Only account administrators (i.e. users with the ACCOUNTADMIN role) can obtain query results.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Time of the event occurrence. |
| EVENT\_ID | NUMBER | The unique identifier for the request. |
| EVENT\_TYPE | TEXT | The REST API event category. Currently, `SCIM` is the only possible value. |
| ENDPOINT | TEXT | The endpoint in the API request (e.g. `scim/v2/Users/<id>`). |
| METHOD | TEXT | The HTTP method used in the request. |
| STATUS | TEXT | The HTTP status result of the request. |
| ERROR\_CODE | TEXT | Error code, if the request was not successful. |
| DETAILS | TEXT | A description of the result of the API request in JSON format. |
| CLIENT\_IP | TEXT | The IP address where the request originated from. This value can be an IPv4 or IPv6 address. |
| ACTOR\_NAME | TEXT | The name of the actor making the request. |
| ACTOR\_DOMAIN | TEXT | The domain (i.e. security integration) in which the request was made. |
| RESOURCE\_NAME | TEXT | The name of the object making the request. |
| RESOURCE\_DOMAIN | TEXT | The object type (e.g. user) making the request. |

Expand

Show lessSee more

## Examples

Return the SCIM REST API requests made in the last five minutes, up to 200 requests.

> Copy code
>
> ```
> use role accountadmin;
> use database my_db;
> use schema information_schema;
> select *
>   from table(rest_event_history(
>       rest_service_type => 'scim',
>       time_range_start => dateadd('minutes',-5,current_timestamp()),
>       time_range_end => current_timestamp(),
>       200))
>   order by event_timestamp;
> ```
