# Jul 23, 2026: SERVICE\_AGENT user type (*General availability*)

With this release, the `SERVICE_AGENT` user type is generally available. Use this user type for automated AI agents that interact with Snowflake using their own identity and privileges.

`SERVICE_AGENT` users share the non-interactive authentication characteristics of `SERVICE` users and include the following capabilities:

- Every session opened by a `SERVICE_AGENT` user is automatically agent-active, so [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated)
  returns `'TRUE'` for the session.
- Support for [workload identity federation](/user-guide/workload-identity-federation), including SPIFFE/SPIRE authentication.

You can create and manage `SERVICE_AGENT` users using SQL or the [SCIM API](/user-guide/scim-user-api-reference).

For more information, see the following topics:

- [Workload identity federation](/user-guide/workload-identity-federation)
- [Types of users](/user-guide/admin-user-management#label-user-management-types)
- [CREATE USER](/sql-reference/sql/create-user)
- [ALTER USER](/sql-reference/sql/alter-user)
