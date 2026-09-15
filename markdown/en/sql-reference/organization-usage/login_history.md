Schemas:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# LOGIN\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query login attempts by Snowflake users.

Details about the error codes/messages for login attempts that were unsuccessful can be found in the following documentation:

- [Federated authentication & SSO error codes](/user-guide/errors-saml)
- [Multi-factor authentication (MFA) error codes](/user-guide/security-mfa-duo#label-mfa-error-codes)
- [OAuth error codes](/user-guide/oauth-snowflake-overview#label-oauth-snowflake-error-codes)

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
| READER\_ACCOUNT\_NAME | VARCHAR | Name of the reader account for the user authentication event. This column is only included in the view in the READER\_ACCOUNT\_USAGE schema. |
| EVENT\_ID | NUMBER | Internal/system-generated identifier for the login attempt. |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Time (in the UTC time zone) of the event occurrence. |
| EVENT\_TYPE | VARCHAR | Event type, such as LOGIN for authentication events. |
| USER\_NAME | VARCHAR | User associated with this event. |
| CLIENT\_IP | VARCHAR | IP address where the request originated. This value can be an IPv4 or IPv6 address. |
| REPORTED\_CLIENT\_TYPE | VARCHAR | Reported type of the client software, such as JDBC\_DRIVER, ODBC\_DRIVER, and so on. This information is not authenticated. |
| REPORTED\_CLIENT\_VERSION | VARCHAR | Reported version of the client software. This information is not authenticated. |
| FIRST\_AUTHENTICATION\_FACTOR | VARCHAR | Method used to authenticate the user (the first factor in multi factor authentication, if used). |
| SECOND\_AUTHENTICATION\_FACTOR | VARCHAR | The second factor in multi factor authentication. If the user did not use multi-factor authentication, this value is NULL. |
| IS\_SUCCESS | VARCHAR | Whether the user’s request was successful or not. |
| ERROR\_CODE | NUMBER | Error code, if the request was not successful. |
| ERROR\_MESSAGE | VARCHAR | Error message returned to the user, if the request was not successful. |
| RELATED\_EVENT\_ID | NUMBER | Reserved for future use. |
| CONNECTION | VARCHAR | Name of the connection used by the client, or NULL if the client is not using a connection URL. A connection is a Snowflake object that is part of [Client Redirect](/user-guide/client-redirect). It represents a connection URL that you can use to fail over to another account for business continuity and disaster recovery.     NOTE: If a client authenticates through an identity provider (IdP) that is configured with the account URL rather than the connection URL, the IdP directs the client to the account URL after authentication is complete. The CONNECTION column for this login event is NULL. See [Authentication and Client Redirect](/user-guide/client-redirect#label-authentication-and-client-redirect). |
| CLIENT\_PRIVATE\_LINK\_ID | VARCHAR | If the user logged in using [private connectivity](/user-guide/private-connectivity-inbound), specifies the identifier of the endpoint from which the request originated. |
| FIRST\_AUTHENTICATION\_FACTOR\_ID | VARCHAR | ID of the [credential](/sql-reference/account-usage/credentials) used to authenticate the user (the first factor in multi-factor authentication, if used). |
| SECOND\_AUTHENTICATION\_FACTOR\_ID | VARCHAR | ID of the [credential](/sql-reference/account-usage/credentials) used for the second factor in multi-factor authentication. If the user did not use multi-factor authentication, this value is NULL. |
| LOGIN\_DETAILS | VARCHAR | Displays details for each login event, including malicious IP protection category name, risk category, and blocking status. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- `INTERNAL_SNOWFLAKE_IP/0.0.0.0` appears as the client IP for login events triggered by internal Snowflake operations that support
  your usage. For example:

  - Because worksheets exist as unique sessions, when a user accesses a worksheet in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in),
    Snowflake creates a login event that originates from `INTERNAL_SNOWFLAKE_IP/0.0.0.0`.
  - When a Snowpark Container Services [service](/developer-guide/snowpark-container-services/overview) logs into Snowflake, the client
    IP is masked to `INTERNAL_SNOWFLAKE_IP/0.0.0.0`.
- This view doesn’t record the activity of internal users the system defines to perform various operations, such as maintaining
  Snowsight worksheets.
- Failed authentication attempts where the user could not be identified appear with a NULL USER\_NAME. These events
  occur when authentication fails before the user can be resolved, such as when OAuth client credentials are invalid or
  when a key pair authentication attempt references an unrecognized user.
- To see the blocking status of potentially malicious IP addresses, examine the LOGIN\_DETAILS column output. For examples, see [View network login details](/user-guide/malicious-ip-protection#label-malicious-ip-view-login-details).
