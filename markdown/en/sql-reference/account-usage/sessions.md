Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SESSIONS view

This Account Usage view provides information on the session, including information on the authentication method to Snowflake and the
Snowflake login event. Snowflake returns one row for each session created over the last year.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SESSION\_ID | Number | The unique identifier for the current session. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the session was created. |
| USER\_NAME | String | The user name of the user. |
| AUTHENTICATION\_METHOD | String | The authentication method used to access Snowflake. |
| LOGIN\_EVENT\_ID | Number | The unique identifier for the login event. |
| CLIENT\_APPLICATION\_VERSION | String | The version number (e.g. 3.8.7) of the Snowflake-provided client application used to create the remote session to Snowflake. |
| CLIENT\_APPLICATION\_ID | String | The identifier for the Snowflake-provided client application used to create the remote session to Snowflake (e.g. JDBC 3.8.7) |
| CLIENT\_ENVIRONMENT | String | The environment variables (e.g. operating system, OCSP mode) of the client used to create a remote session to Snowflake. |
| CLIENT\_BUILD\_ID | String | The build number (e.g. 41897) of the third-party client application used to create a remote session to Snowflake, if available. For example, a third-party Java application that uses the JDBC driver to connect to Snowflake. |
| CLIENT\_VERSION | String | The version number (e.g. 47154) of the third-party client application that uses a Snowflake-provided client to create a remote session to Snowflake, if available. |
| ACCESS\_TIME | TIMESTAMP\_LTZ | Date and time when the session was last used. |
| IS\_OPEN | BOOLEAN | Whether the session is currently open (TRUE) or closed (FALSE). |
| CLOSED\_REASON | String | The reason why a Snowflake session closed. NULL for sessions that are currently open. For closed sessions, one of the values described in [CLOSED\_REASON values](#label-sessions-closed-reason-values). |

Expand

Show lessSee more

### CLOSED\_REASON values

| Value | Description |
| --- | --- |
| UNKNOWN | Session closed for an unspecified or unclassified reason. |
| DROP\_USER | Session closed because the user was dropped. |
| LOGOUT | Session closed because the user signed out. |
| FORCED\_LOGOUT | An account administrator in your Snowflake account forced the user to log out. |
| ABANDONED | Session closed after it was left unused (for example, after a session timeout). |
| OAUTH\_CRITICAL\_CHANGE\_INTEGRATION | Session closed after a critical change to the OAuth security integration associated with the session. |
| DROP\_ACCOUNT | Session closed because the account was dropped. |
| OAUTH\_CONSENT\_REVOKED | Session closed because OAuth consent was revoked. |
| TASK\_COMPLETED | Session closed when the task that owned the session completed. |
| SFC\_FORCED\_LOGOUT | A Snowflake administrator (for example, a Support engineer) forced the user to log out. |
| OAUTH\_RESOURCE\_NOT\_AUTHORIZED | Session closed because the role in the session doesn’t have access to certain resources. |
| PAT\_DELETED | Session closed because the programmatic access token (PAT) was deleted. |
| PAT\_COMPROMISED | Session closed because the programmatic access token (PAT) was compromised. |
| WORKLOAD\_IDENTITY\_DELETED | Session closed because the workload identity (WIF authenticator) was deleted. |
| SPROC\_COMPLETED | Session closed when the stored procedure that owned the session completed (for example, when using multiple sessions with native dbt). |
| WEB\_SESSION\_LIMIT\_REACHED | Session closed because the web session limit was reached. |
| WEB\_SESSION\_EXPIRED | Session closed because the web session expired. |
| MAX\_LIFESPAN\_EXCEEDED | Session closed because the session exceeded its maximum lifespan. |
| INTEGRATION\_DISABLED | Session closed because the integration that backed the session was disabled or deleted. |

Expand

Show lessSee more

`FORCED_LOGOUT` and `SFC_FORCED_LOGOUT` match the definitions in [SESSIONS View (Account Usage): New Column in View](/release-notes/bcr-bundles/2023_03/bcr-991).

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- The view displays data starting from July 20-21, 2020.

- The SESSIONS view does not currently track SQL API transient sessions.
- This view does not record the activity of internal users the system defines to perform various operations
  (e.g. maintain Snowsight worksheets).
