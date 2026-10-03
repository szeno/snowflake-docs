# Snowflake CoWork: MANAGE ACCESS ON DASHBOARDARTIFACT privilege granted to the PUBLIC role

Note

This change will be rolled out gradually beginning in late September 2026. Please note dates are subject to change.

Users must use a role that has the MANAGE ACCESS ON DASHBOARDARTIFACT privilege to grant or revoke
access to a dashboard Artifact. This change affects which roles have the MANAGE ACCESS ON
DASHBOARDARTIFACT privilege by default.

Before the change:
:   The MANAGE ACCESS ON DASHBOARDARTIFACT privilege is not granted to any role by default. Account
    administrators must explicitly grant the privilege to roles before users can share the dashboard
    Artifacts they own.

After the change:
:   The PUBLIC role is granted the MANAGE ACCESS ON DASHBOARDARTIFACT privilege, which means a user can
    use any role to grant and revoke access to dashboard Artifacts.

    Granting this privilege to PUBLIC does not by itself give every role control over every dashboard
    Artifact. The privilege is granted at the account level and scoped by Artifact type: it governs
    whether a role may manage dashboard Artifact sharing at all, not which Artifacts it may manage.
    Artifact-level authority is also evaluated when access grants are changed. The privilege on its own
    confers no access to Artifact content or to the data behind it.

    If you do not publish dashboard Artifacts, this privilege will still be granted but will not have any
    observable effect.

Granting someone access to a dashboard Artifact does not grant access to the data behind it. A
dashboard Artifact runs with caller’s rights, so each viewer sees only the data that their own role
is authorized to access.

After the change, if you want to restrict who can share dashboard Artifacts, revoke the MANAGE ACCESS
ON DASHBOARDARTIFACT privilege from the PUBLIC role, then grant the privilege to specific roles:

Copy code

```
-- Revoke from PUBLIC to centralize access management
REVOKE MANAGE ACCESS ON DASHBOARDARTIFACT ON ACCOUNT FROM ROLE PUBLIC;

-- Optionally grant to specific roles
GRANT MANAGE ACCESS ON DASHBOARDARTIFACT ON ACCOUNT TO ROLE dashboard_sharer;
```

Ref: 2462
