# Snowflake sessions and session policies

This topic describes Snowflake sessions and session policies and provides instructions for configuring session policies at the account or
user level.

## Snowflake sessions

A session begins when a user connects to Snowflake and authenticates successfully using a Snowflake programmatic client or [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
A session is independent of an identity provider (IdP) session. If the Snowflake session expires but the IdP session remains active,
a user can log in to Snowflake without entering their login credentials again (i.e. silent authentication).

By default, a session is maintained indefinitely with continued user activity. After a period of inactivity in the session, known as the
idle session timeout, the user must authenticate to Snowflake again. The default idle session timeout is four hours for non-UI (programmatic)
sessions and 18 hours for UI sessions. The session policy can modify
the idle session timeout period from a minimum of 5 minutes to a maximum of 24 hours.

A session policy can also enforce a maximum session lifespan, which ends the session after a set duration regardless
of activity. The configurable range is 0 minutes to 30 days, where a value of 0 means no maximum lifespan is enforced. By default, no maximum lifespan is enforced.
These session timeouts apply to the following:

- [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
- [Snowflake CLI](/developer-guide/snowflake-cli/index).
- [SnowSQL (CLI client)](/user-guide/snowsql).
- Supported [connectors and drivers](/guides-overview-connecting).
- Third-party clients that connect to Snowflake using a supported connector or driver.

Snowflake recommends reusing existing sessions when possible and to close the connection to Snowflake when a session is no longer needed.

### Snowsight session expiration and logout behavior

- A Snowsight session remains active as long as the user is interacting with the application, has not exceeded the configured idle
  session timeout, and has not reached the maximum session lifespan (if configured).
- The session idle timeout is controlled by your organization’s session policy. The default idle timeout is 18 hours.
  If there is no activity for longer than this period, the session will expire and you will be logged out automatically.
- A session policy can also enforce a maximum session lifespan. If configured, the session expires after the specified duration regardless
  of activity. By default, no maximum lifespan is enforced.
- In addition to idle timeout and maximum lifespan, session persistence is also affected by authentication cookies:

  - In most cases, closing and reopening your browser will end your Snowsight session, regardless of your idle time.
  - If your authentication cookie expires (typically after 24 hours), you will be required to log in again, even if you have not been idle
    for longer than the session timeout.
- If your network connection is lost or you attempt to access Snowsight from a disallowed network, your session may be closed and you will be logged out.
- When a session is closed for any reason, any running queries or jobs associated with that session will be terminated after a short delay
  (usually within a few minutes).

Note

Session expiration can occur due to idle timeout, maximum session lifespan, cookie expiration, browser restarts, or network policy
violations. Closing your browser or being inactive for an extended period may require you to log in again, even if you have not
reached the configured idle timeout.

### Monitor session usage

You can monitor active sessions and session usage using Snowsight or a SQL view. You can view your own sessions,
or use a role with access to view the SESSIONS view to view sessions for your account. See [ACCOUNT\_USAGE schema SNOWFLAKE database roles](/sql-reference/account-usage#label-account-usage-snowflake-db-roles).

SQL:
:   Query the [SESSIONS](/sql-reference/account-usage/sessions) view in the ACCOUNT USAGE schema
    of the shared SNOWFLAKE database to monitor session usage.

Snowsight:
:   In the navigation menu, select **Governance & security** » **Network policies**, and then select the **Sessions** tab.
    You can review the session ID, user name, start time, client driver in use for the session, client net address, and authentication method.
    Hover over the start time to view the exact date and time that the session started, in your local time zone.

## Session policies

A session policy defines the idle session timeout period in minutes and provides the option to override the default idle timeout
value. The timeout period begins upon a successful authentication to Snowflake. The minimum configurable idle timeout value for a session
policy is `5` minutes.

If a session policy is not set, Snowflake uses a default value of `240` minutes (four hours) for non-UI (programmatic)
sessions. For Snowsight sessions, the default is `1080` minutes (18 hours).

When the session expires, the user must authenticate to Snowflake again. However, Snowflake does not enforce any setting defined by the
[Custom logout endpoint](/user-guide/admin-security-fed-auth-security-integration#label-sso-custom-logout-endpoint).

The session policy can be set for an account or user with configurable idle timeout and maximum session lifespan values to address compliance requirements. If a user
is associated with both an account and user-level session policy, the user-level session policy takes precedence. After the session policy
is set on the account or user, Snowflake enforces the session policy.

There are two properties that govern the idle timeout behavior:

- `SESSION_IDLE_TIMEOUT_MINS` for programmatic and Snowflake clients.
- `SESSION_UI_IDLE_TIMEOUT_MINS` for Snowsight.

A session policy can also define the maximum session lifespan, regardless of activity. When the maximum lifespan is reached, the user must
authenticate again even if the session is still active. The configurable range is `0` to `43200` minutes (30 days).

> If a session policy is set but a session lifespan is not defined, Snowflake uses a default value of `0`, which means no maximum lifespan is enforced.

There are two properties that govern the maximum lifespan behavior:

- `SESSION_MAX_LIFESPAN_MINS` for programmatic and Snowflake clients.
- `SESSION_UI_MAX_LIFESPAN_MINS` for Snowsight.

For more information, see [Managing session policies](/sql-reference/ddl-user-security#label-session-policy-ddl).

### Secondary roles in a session policy

When a user connects to Snowflake and the session begins, the user can activate
[secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) with a [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) command. However, as a
security administrator, you might want to manage the secondary roles that are available to an individual user, groups of users, or the
entire account. Managing secondary roles helps to scope the set of privileges available to a user for the duration of the session.

To meet these management needs, you can set the `ALLOWED_SECONDARY_ROLES` property in a session policy and set the session policy on
the account or a user in the account. This property controls the secondary roles that can be activated in a session. Setting this property
to an empty list `ALLOWED_SECONDARY_ROLES=()` disables secondary roles in a session.

For examples, see [Specifying secondary roles in a session policy](/user-guide/session-policies-using#label-session-policy-secondary-roles-examples).

Note

When you set the `ALLOWED_SECONDARY_ROLES` property in a session policy, the enforcement of the secondary roles begins immediately,
including existing sessions.

Prior to updating the session policy to limit secondary roles, consider your workload schedule and the access control for each
workload to avoid unnecessary workload disruption.

### Restricted Session Scope for agents

A session policy can set `AGENT_RESTRICTED_SESSION_SCOPE`, a privilege ceiling that Snowflake
applies when an agent is active in the session. The ceiling intersects with the user’s RBAC
privileges and never grants additional access. When no agent is active, the property is ignored.

For YAML structure, predefined scopes, and examples, see
[Restricted Session Scope for agents](/user-guide/restricted-session-scope).

### Considerations

- If a client supports the CLIENT\_SESSION\_KEEP\_ALIVE option and the option is set to `TRUE`, the client preserves the Snowflake
  session as long as the connection to Snowflake is active. However, if a session policy with a maximum session lifespan is configured,
  the session still ends when that lifespan is reached, regardless of activity. If the option is set to `FALSE`, the session ends
  after the idle session timeout (four hours by default for programmatic sessions). When possible, avoid using this option since it can
  result in many open sessions and place a greater demand on resources, which can lead to a performance degradation.
- You can use the [CLIENT\_SESSION\_KEEP\_ALIVE\_HEARTBEAT\_FREQUENCY](/sql-reference/parameters#label-client-session-keep-alive-heartbeat-frequency) parameter to specify the number of seconds
  between client attempts to update the token for the session. The web interface session can be refreshed as Snowflake objects continue to
  be used, such as executing DDL and DML statements. Snowflake checks for this behavior every 30 seconds.
- Creating a new worksheet or opening an existing worksheet continues to use the established user session but with its idle session timeout
  reset to 0.

### Limitations

Future grants:
:   [Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) of privileges on session policies are not supported.

    As a workaround, grant the APPLY SESSION POLICY privilege to a custom role to allow that role to apply session policies on a user or the
    Snowflake account.
