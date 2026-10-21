# Snowflake Artifacts

An artifact is a [securable object](/user-guide/security-access-control-overview#label-access-control-securable-objects) in Snowflake that stores analytical content for viewing and sharing within an account. Each artifact has a unique identifier and access privileges managed through [role-based access control (RBAC)](/user-guide/security-access-control-overview#label-access-control-framework).

## Overview

Artifacts include the following types:

- **Dashboard** (`DASHBOARD`): A dashboard that runs with caller’s rights.
- **Chart** (`CHART`): A chart or table that runs with caller’s rights.
- **Report** (`REPORT`): An HTML report containing a static snapshot of text and visualizations.
- **File** (`FILE`): A static file, such as a PDF or PowerPoint file.
- **Thread** (`THREAD`): A static snapshot of a Snowflake CoWork conversation.

Artifact types share a common model for ownership, access, and visibility. Authoring, refresh, and interaction behavior depend on the type. For type-specific instructions, see [Related topics](#label-snowflake-artifacts-related-topics).

## How artifacts work

An artifact is separate from the file or conversation used to create it. Sharing the artifact doesn’t grant access to its source file, source conversation, or underlying tables and views. Recipients must sign in to the same Snowflake account and have access to the artifact through a role or a grant to their personal role.

### Access control

The following privileges control access to an individual artifact:

- `OWNERSHIP` grants control of the artifact, including deletion and the ability to transfer ownership. Each artifact has one owner role. By default, the owner is the personal role of the user who created it.
- `READ` allows viewing the artifact’s content.
- `WRITE` allows viewing and modifying the artifact. It also permits inspecting the artifact with `DESCRIBE ARTIFACT` and `SHOW ARTIFACTS` when those SQL commands are available.

### Sharing privileges

Sharing requires the account-level `MANAGE ACCESS` privilege for the corresponding artifact type:

- `MANAGE ACCESS ON CHART ARTIFACTS`
- `MANAGE ACCESS ON DASHBOARD ARTIFACTS`
- `MANAGE ACCESS ON FILE ARTIFACTS`
- `MANAGE ACCESS ON REPORT ARTIFACTS`
- `MANAGE ACCESS ON THREAD ARTIFACTS`

These privileges control whether a role can manage sharing for that artifact type. They don’t grant access to individual artifacts or source data. Authority to manage grants on the individual artifact is also required. A role with account-level `MANAGE GRANTS` can administer artifact grants.

In accounts where the [artifact sharing behavior change](/release-notes/bcr-bundles/un-bundled/bcr-manage-access-dashboard-artifacts) is enabled, all five privileges are granted to `PUBLIC` by default. Administrators can restrict sharing independently for each type by revoking its `MANAGE ACCESS` privilege from `PUBLIC` and granting it to designated roles. Existing artifact grants remain unchanged.

For example, restrict dashboard sharing to the `artifact_sharer` role:

Copy code

```
REVOKE MANAGE ACCESS ON DASHBOARD ARTIFACTS
  ON ACCOUNT FROM ROLE PUBLIC;

GRANT MANAGE ACCESS ON DASHBOARD ARTIFACTS
  ON ACCOUNT TO ROLE artifact_sharer;
```

For general grant and revoke syntax, see [GRANT privileges to a role](/sql-reference/sql/grant-privilege) and [REVOKE privileges from a role](/sql-reference/sql/revoke-privilege).

### Artifacts and source data

Sharing an artifact doesn’t grant privileges on its source tables or views. Data access depends on how the artifact supplies its content:

- **Query-backed artifacts:** Snowflake evaluates the viewer’s data privileges when queries run. This applies to Dashboard and Chart artifacts.
- **Artifacts with saved content:** Viewers read the saved content without rerunning its source queries. This applies to Report, File, and Thread artifacts.

Important

Recipients can view saved content even without source-data access. Changes to source data or source-data privileges don’t update existing saved content. Review the content before sharing it.

For chart refresh and cached-snapshot behavior, see [Find and refresh saved artifacts](/user-guide/snowflake-cortex/snowflake-cowork/artifacts#label-chart-artifacts-refresh).

## Artifact owner capabilities

Owners can manage access to artifacts and transfer ownership. For dashboard and report creation, publication, and sharing procedures, see [Create and share a dashboard or HTML report](/user-guide/snowflake-artifacts-create-share).

### Ownership transfer

Ownership can be transferred to another role or to a user’s personal role through the artifact’s **Share** dialog. When you transfer ownership through the dialog, all current grants remain active.

Coming soon: SQL ownership transfer

SQL ownership transfer with `GRANT OWNERSHIP ON ARTIFACT` isn’t yet available. The following example describes the upcoming syntax; don’t run it before this capability is available in your account.

Replace the example UUID and role name with your artifact identifier and receiving role:

Copy code

```
GRANT OWNERSHIP ON ARTIFACT "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
  TO ROLE analytics_team COPY CURRENT GRANTS;
```

For artifact ownership transfer, `COPY CURRENT GRANTS` is the default and preserves existing `READ` and `WRITE` grants and any enabled link-sharing setting. The owner can instead replace `COPY CURRENT GRANTS` with `REVOKE CURRENT GRANTS` to remove existing `READ` and `WRITE` grants and disable that setting. The new owner receives `OWNERSHIP`. Link-sharing settings don’t bypass account-wide controls or source-data access checks.

### Deletion

Deletion requires `OWNERSHIP`. Dropped artifacts can’t be restored with `UNDROP`, including by administrators. For the lifecycle of saved charts and shared conversations, see [Lifecycle and access changes](/user-guide/snowflake-cortex/snowflake-cowork/artifacts#label-artifact-lifecycle).

## Administrative capabilities

Administrators can control sharing for the account and inspect artifact metadata and grants.

### Control sharing for the account

The **Sharing artifacts and chats** setting is an account-wide control for artifact sharing. To change it, use the `ACCOUNTADMIN` role and open the Snowflake CoWork settings in Snowsight. Under **Data controls**, turn **Sharing artifacts and chats** on or off.

Turning the setting off blocks new sharing and prevents non-owners from accessing shared artifacts, even if they have existing grants. Owners retain access, and authorized users can still revoke sharing for cleanup.

This setting is separate from artifact privileges:

- `MANAGE ACCESS` controls who can administer sharing for each artifact type. It doesn’t bypass the account-wide setting.
- `READ` and `WRITE` grants control access to individual artifacts when sharing is enabled, subject to other applicable access checks.

Turning sharing off blocks access; it isn’t a substitute for revoking the grants on an artifact.

### Inspect artifacts and grants

Coming soon: SQL administration

The artifact-specific SQL commands and function in this section aren’t yet available. SQL administration has a separate rollout from the artifact authoring and sharing workflows.

Administrators can use the following SQL interfaces when they become available:

- `SHOW ARTIFACTS` lists artifacts and their identifiers.
- `DESCRIBE ARTIFACT` inspects an artifact’s properties.
- `SYSTEM$SHOW_ARTIFACT_GRANTS` inspects the `OWNERSHIP`, `READ`, and `WRITE` grants recorded on an artifact. It returns JSON containing each grant’s privilege, grantee role, grantor role, grant option, and creation timestamp.

The grant output lists role grants, not every user with effective access, and doesn’t include source-data permissions or link-sharing settings. Artifact grants aren’t included in [SHOW GRANTS](/sql-reference/sql/show-grants) output.

These interfaces return metadata, not content. Reference artifacts by their unique identifier, not their display title. The identifier is the UUID after `/artifacts/` in the artifact URL; it is also available through `SHOW ARTIFACTS` when that command is available.

## Limitations and considerations

- Artifact administration SQL manages existing artifacts; it doesn’t create artifacts or edit their content.
- Possessing an artifact link doesn’t replace the applicable access checks.
- Availability and supported authoring surfaces depend on the artifact type.

## Related topics

- [Create and share a dashboard or HTML report](/user-guide/snowflake-artifacts-create-share).
- [Chart and Thread artifacts](/user-guide/snowflake-cortex/snowflake-cowork/artifacts).
- [Generate PDF, Word, PowerPoint, and HTML files in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation).
- [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code).
- [Overview of access control](/user-guide/security-access-control-overview).
