Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# LOGIN\_HISTORY , LOGIN\_HISTORY\_BY\_USER

The LOGIN\_HISTORY family of table functions can be used to query login attempts by Snowflake users along various dimensions:

- LOGIN\_HISTORY returns login events within a specified time range.
- LOGIN\_HISTORY\_BY\_USER returns login events of a specified user within a specified time range.

Each function is optimized for querying along the specified dimension. The results can be further filtered using SQL predicates.

Note

These functions return login activity within the last 7 days.

## Syntax

Copy code

```
LOGIN_HISTORY(
      [  TIME_RANGE_START => <constant_expr> ]
      [, TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <num> ] )

LOGIN_HISTORY_BY_USER(
      [  USER_NAME => '<string>' ]
      [, TIME_RANGE_START => <constant_expr> ]
      [, TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <num> ] )
```

## Arguments

All the arguments are optional.

`TIME_RANGE_START => constant_expr` , `TIME_RANGE_END => constant_expr`
:   Time range (in TIMESTAMP\_LTZ format), within the last 7 days, in which the login event occurred.

    If `TIME_RANGE_END` is not specified, the function returns the most recent login events.

    If the time range does not fall within the last 7 days, an error is returned.

`USER_NAME => 'string'`
:   Applies only to LOGIN\_HISTORY\_BY\_USER

    A string specifying a user name or [CURRENT\_USER](/sql-reference/functions/current_user). Only login events for the specified user are returned. Note that the login name must be enclosed in single quotes. Also, if the
    login name contains any spaces, mixed-case characters, or special characters, the name must be double-quoted within the single quotes (e.g. `'"User 1"'` vs `'user1'`).

    Default: [CURRENT\_USER](/sql-reference/functions/current_user)

`RESULT_LIMIT => num`
:   A number specifying the maximum number of rows returned by the function.

    If the number of matching rows is greater than this limit, the login events with the most recent timestamp are returned, up to the specified limit.

    Range: `1` to `10000`

    Default: `100`.

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Time of the event occurrence. |
| EVENT\_ID | NUMBER | Event’s unique id. |
| EVENT\_TYPE | VARCHAR | Event type, such as LOGIN for authentication events. |
| USER\_NAME | VARCHAR | User associated with this event. If the user could not be identified during a failed authentication attempt, this value is NULL. |
| CLIENT\_IP | VARCHAR | IP address where the request originated from. |
| REPORTED\_CLIENT\_TYPE | VARCHAR | Reported type of the client software, such as JDBC\_DRIVER, ODBC\_DRIVER, etc. This information is not authenticated. |
| REPORTED\_CLIENT\_VERSION | VARCHAR | Reported version of the client software. This information is not authenticated. |
| FIRST\_AUTHENTICATION\_FACTOR | VARCHAR | Method used to authenticate the user (the first factor in multi factor authentication, if used). |
| SECOND\_AUTHENTICATION\_FACTOR | VARCHAR | The second factor in multi factor authentication. If the user did not use multi-factor authentication, this value is NULL. |
| IS\_SUCCESS | VARCHAR | Whether the user’s request was successful or not. |
| ERROR\_CODE | NUMBER | Error code, if the request was not successful. |
| ERROR\_MESSAGE | VARCHAR | Error message returned to the user, if the request was not successful. |
| RELATED\_EVENT\_ID | NUMBER | Reserved for future use. |
| CONNECTION | VARCHAR | Name of the connection used by the client, or NULL if the client is not using a connection URL. Connection is a Snowflake object that is a part of [Client Redirect](/user-guide/client-redirect). It represents a connection URL that you can use to fail over to another account for business continuity and disaster recovery.     NOTE: If a client authenticates through an identity provider (IdP) that is configured with the account URL rather than the connection URL, the IdP directs the client to the account URL after authentication is complete. The CONNECTION column for this login event is NULL. See [Authentication and Client Redirect](/user-guide/client-redirect#label-authentication-and-client-redirect). |
| CLIENT\_PRIVATE\_LINK\_ID | VARCHAR | If the user logged in using [private connectivity](/user-guide/private-connectivity-inbound), specifies the identifier of the endpoint from which the request originated. |
| FIRST\_AUTHENTICATION\_FACTOR\_ID | VARCHAR | ID of the [credential](/sql-reference/account-usage/credentials) used to authenticate the user (the first factor in multi-factor authentication, if used). |
| SECOND\_AUTHENTICATION\_FACTOR\_ID | VARCHAR | ID of the [credential](/sql-reference/account-usage/credentials) used for the second factor in multi-factor authentication. If the user did not use multi-factor authentication, this value is NULL. |
| LOGIN\_DETAILS | VARCHAR | A JSON object containing details for each login event, including the malicious IP protection category name, the risk category, and the blocking status. For failed authentication attempts with validation errors, the object also includes `authn_validation_error`, a JSON array of strings describing the validation errors. For example, `["Audience mismatch: expected 'https://account.snowflakecomputing.com', got 'https://other.example.com'"]`. |
| AUTHORIZING\_INTEGRATION\_NAME | VARCHAR | Name of the security integration that authorized the login. For OAuth logins, this is the security integration used to grant access. If no security integration authorized the login, this value is NULL. |
| AUTHENTICATING\_INTEGRATION\_NAME | VARCHAR | Name of the security integration used for authentication. For federated logins, this is the SAML or OIDC security integration. If no security integration was used for authentication, this value is NULL. |

Expand

Show lessSee more

For details about the error codes/messages for login attempts that were unsuccessful due to invalid SAML responses, see [Federated authentication and SSO troubleshooting](/user-guide/errors-saml).

## Examples

Retrieve up to the last 100 login events of the current user:

> Copy code
>
> ```
> select *
> from table(information_schema.login_history_by_user())
> order by event_timestamp;
> ```

Retrieve up to the last 1000 login events of the specified user:

> Copy code
>
> ```
> select *
> from table(information_schema.login_history_by_user(USER_NAME => 'USER1', result_limit => 1000))
> order by event_timestamp;
> ```

Retrieve up to 100 login events of every user your current role is allowed to monitor in the last hour:

> Copy code
>
> ```
> select *
> from table(information_schema.login_history(TIME_RANGE_START => dateadd('hours',-1,current_timestamp()),current_timestamp()))
> order by event_timestamp;
> ```
