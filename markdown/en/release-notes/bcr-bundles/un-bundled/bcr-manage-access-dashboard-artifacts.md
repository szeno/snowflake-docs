# Snowflake CoWork: MANAGE ACCESS privileges on Artifacts granted to the PUBLIC role

Note

This change will be rolled out gradually beginning in late September 2026. Please note dates are subject to change.

Users must use a role that has the MANAGE ACCESS privilege for an Artifact type to grant or revoke
access to Artifacts of that type. This change affects which roles have the following privileges by
default:

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

    Granting these privileges to PUBLIC does not by itself give every role control over every Artifact.
    Each privilege is granted at the account level and scoped by Artifact type: it governs whether a
    role may manage sharing for Artifacts of that type at all, not which Artifacts it may manage.
    Artifact-level authority is also evaluated when access grants are changed. The privileges on their
    own confer no access to Artifact content or to the data behind it.

    If you do not publish Artifacts, these privileges will still be granted but will not have any
    observable effect.

Granting someone access to an Artifact does not grant access to the data behind it. Dashboard
Artifacts and Report Artifacts run with caller’s rights, so each viewer sees only the data that
their own role is authorized to access. Chart Artifacts, File Artifacts, and Thread Artifacts are
static snapshots that don’t execute SQL, so caller’s rights don’t apply to them.

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
