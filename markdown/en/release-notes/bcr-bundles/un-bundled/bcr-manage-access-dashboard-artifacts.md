# MANAGE ACCESS privileges on Artifacts granted to the PUBLIC role

Note

This change will be rolled out gradually beginning in late September 2026. Please note dates are subject to change.

To share Artifacts, a user needs a role with the MANAGE ACCESS privilege for that Artifact type.
This change grants the following privileges to the PUBLIC role by default:

- MANAGE ACCESS ON CHART ARTIFACTS
- MANAGE ACCESS ON DASHBOARD ARTIFACTS
- MANAGE ACCESS ON FILE ARTIFACTS
- MANAGE ACCESS ON REPORT ARTIFACTS
- MANAGE ACCESS ON THREAD ARTIFACTS

Before the change:
:   The MANAGE ACCESS privileges on Artifacts are not granted to any role by default. Account
    administrators must explicitly grant the privilege for each Artifact type to roles before users can
    share the Artifacts of that type that they own.

After the change:
:   The PUBLIC role is granted the MANAGE ACCESS privileges on all five Artifact types, which means a
    user can use any role to grant and revoke access to Artifacts.

    These are account-level privileges, scoped by Artifact type. They control whether a role can manage
    sharing for Artifacts of that type at all. For users beyond the owner role to work with an Artifact,
    the owner must still grant other roles access to each individual Artifact.

    If you do not publish Artifacts, these privileges will still be granted but will not have any
    observable effect.

What viewers see depends on the Artifact type:

- Dashboard Artifacts and Chart Artifacts run with caller’s rights, so each viewer sees only the data
  that their own roles can access.
- Report Artifacts (HTML reports), File Artifacts (such as PDF and PPT files), and Thread Artifacts
  (Snowflake CoWork conversations) are static snapshots that don’t run SQL. Viewers see the text
  and visualizations directly.

After the change, if you want to restrict who can share Artifacts, revoke the MANAGE ACCESS
privileges from the PUBLIC role, then grant the privileges to specific roles. You can do this for
each Artifact type independently:

Copy code

```
-- Revoke from PUBLIC to centralize access management
REVOKE MANAGE ACCESS ON CHART ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON DASHBOARD ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON FILE ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON REPORT ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON THREAD ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;

-- Optionally grant to specific roles
GRANT MANAGE ACCESS ON CHART ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON DASHBOARD ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON FILE ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON REPORT ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON THREAD ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
```

Ref: 2462
