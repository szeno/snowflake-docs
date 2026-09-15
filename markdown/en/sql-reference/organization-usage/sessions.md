Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SESSIONS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides information on the session, including information on the authentication method to Snowflake and the
Snowflake login event. Snowflake returns one row for each session created over the last year.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

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
| CLOSED\_REASON | String | The reason why a Snowflake session closed. NULL for sessions that are currently open. One of the following for closed sessions: DROP\_USER, LOGOUT, FORCED\_LOGOUT, ABANDONED, OAUTH\_CRITICAL\_CHANGE\_INTEGRATION, DROP\_ACCOUNT, OAUTH\_CONSENT\_REVOKED, TASK\_COMPLETED, SFC\_FORCED\_LOGOUT. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The SESSIONS view does not currently track SQL API transient sessions.
- This view does not record the activity of internal users the system defines to perform various operations
  (e.g. maintain Snowsight worksheets).
