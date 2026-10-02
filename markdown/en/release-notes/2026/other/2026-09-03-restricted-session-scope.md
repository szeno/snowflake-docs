# Sep 3, 2026: Restricted Session Scope for agents (*General availability*)

With this release, Restricted Session Scope (RSS) is generally available. An RSS is a privilege
ceiling that limits what an agent can do on behalf of a user. It intersects with RBAC and never
grants privileges the user doesn’t already have through their roles.

This announcement covers admin-managed RSS, which administrators apply with session policies. For
the GA announcement for user-managed RSS in CoCo clients, see
[Sep 14, 2026: User-managed Restricted Session Scope in CoCo (General availability)](/release-notes/2026/other/2026-09-14-restricted-session-scope-coco).

To apply an RSS, set `AGENT_RESTRICTED_SESSION_SCOPE` on a session policy, then attach the policy
to the account or to specific users. The property applies only when an agent is active. You can
reference a Snowflake predefined scope, create a restricted session scope object, or embed the RSS
YAML inline in the session policy.

For more information, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope).
