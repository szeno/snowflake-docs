# Snowflake CoWork: MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege granted to the PUBLIC role

Note

This change will be rolled out gradually beginning in June 2026. Please note dates are subject to change.

Users must use a role that has the MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege to publish or unpublish dashboards to
Snowflake CoWork. This change affects which roles have the MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege by default.

Before the change:
:   The MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege is not granted to any role by default. Account administrators must
    explicitly grant the privilege to roles before users can publish dashboards to Snowflake CoWork.

After the change:
:   The PUBLIC role is granted the MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege, which means a user can use any role to
    publish and unpublish dashboards to Snowflake CoWork.

    This doesn’t mean that all roles and users can publish any dashboard; users must still have the appropriate
    privileges on the dashboard (such as edit access) in order to publish it. If you do not use Snowflake CoWork, this
    privilege will still be granted but will not have any observable effect.

After the change, if you want to restrict who can publish dashboards to Snowflake CoWork, revoke the MANAGE ARTIFACT PUBLICATION
ON ACCOUNT privilege from the PUBLIC role, then grant the privilege to specific roles:

Copy code

```
-- Revoke from PUBLIC to restrict publishing
REVOKE MANAGE ARTIFACT PUBLICATION ON ACCOUNT FROM ROLE PUBLIC;

-- Optionally grant to specific roles (account-level)
GRANT MANAGE ARTIFACT PUBLICATION ON ACCOUNT TO ROLE dashboard_publisher;

-- Or grant for a specific Snowflake CoWork instance only
GRANT MANAGE ARTIFACT PUBLICATION ON SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT TO ROLE dashboard_publisher;
```

Ref: 2335
