# MANAGE ACCESS privileges on Artifacts granted to the PUBLIC role

Note

This change will be rolled out gradually beginning in late September 2026. Please note dates are subject to change.

This change introduces the following privileges, which let account administrators control which
roles can share Artifacts of each type:

- MANAGE ACCESS ON CHART ARTIFACTS
- MANAGE ACCESS ON DASHBOARD ARTIFACTS
- MANAGE ACCESS ON FILE ARTIFACTS
- MANAGE ACCESS ON REPORT ARTIFACTS
- MANAGE ACCESS ON THREAD ARTIFACTS

To preserve existing behavior, these privileges are granted to the PUBLIC role by default. Users can
continue to share Artifacts as they do today, and the existing account-wide sharing setting
continues to work as before.

Before the change:
:   Users can share the Artifacts that they own. Account administrators can turn off sharing for the
    entire account, but they can’t control which roles can share Artifacts.

After the change:
:   Users can continue to share the Artifacts that they own, because the MANAGE ACCESS privileges on all
    five Artifact types are granted to the PUBLIC role. This grant doesn’t give users any ability that
    they didn’t already have before the change.

    Account administrators can still turn off sharing for the entire account. They can now also control
    which roles can share each Artifact type.

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

## Account-wide sharing setting

The **Sharing artifacts and chats** setting turns Artifact sharing on or off for the entire account.
It’s on by default. To change it, use the ACCOUNTADMIN role and open the Snowflake CoWork settings
in Snowsight. Under **Data controls**, turn **Sharing artifacts and chats** on or off.

You can also change the setting with the ENABLE\_SNOWFLAKE\_INTELLIGENCE\_ARTIFACT\_SHARING account
parameter. For example, to turn off sharing:

Copy code

```
ALTER ACCOUNT SET ENABLE_SNOWFLAKE_INTELLIGENCE_ARTIFACT_SHARING = FALSE;
```

When sharing is turned off, users can’t share Artifacts, and only owners can open Artifacts, even
if other roles have been granted access. The MANAGE ACCESS privileges don’t override this setting.
For more information, see
[Control sharing for the account](/user-guide/snowflake-artifacts#label-snowflake-artifacts-control-sharing).

## Actions required

What you need to do depends on how sharing is configured in your account:

- **Sharing is turned on, and you want all users to keep sharing:** No action is required.
- **Sharing is turned off, and you want to keep it off:** No action is required. Granting the
  MANAGE ACCESS privileges to the PUBLIC role doesn’t turn sharing back on.
- **You want to allow only specific roles to share:** Complete the following steps. You can do this
  for each Artifact type independently.

  1. Revoke the MANAGE ACCESS privileges from the PUBLIC role.
  2. Grant the MANAGE ACCESS privileges to the roles that should be able to share.
  3. If sharing is turned off for the account, turn it on.

  If sharing is turned off, revoke the privileges from the PUBLIC role before you turn sharing on,
  so that all users don’t regain the ability to share.

For example:

Copy code

```
-- Revoke from PUBLIC to centralize access management
REVOKE MANAGE ACCESS ON CHART ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON DASHBOARD ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON FILE ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON REPORT ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;
REVOKE MANAGE ACCESS ON THREAD ARTIFACTS ON ACCOUNT FROM ROLE PUBLIC;

-- Grant to specific roles
GRANT MANAGE ACCESS ON CHART ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON DASHBOARD ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON FILE ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON REPORT ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
GRANT MANAGE ACCESS ON THREAD ARTIFACTS ON ACCOUNT TO ROLE artifact_sharer;
```

After you revoke a privilege from the PUBLIC role, only roles that have the privilege can share
Artifacts of that type. Revoking a privilege doesn’t remove access that users have already been
granted to individual Artifacts.

Ref: 2462
