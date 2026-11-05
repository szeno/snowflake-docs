# Create and share a dashboard or HTML report

Create an artifact from a `.dash` or `.html` file in [Workspaces](/user-guide/ui-snowsight/workspaces) to share it with recipients and make it accessible in Snowflake CoWork. Recipients access the artifact, not the source file. For artifact types, ownership, and access privileges, see [Snowflake Artifacts](/user-guide/snowflake-artifacts).

## Before you begin

Dashboard or HTML report authoring must be available in your account. To share the artifact, your current role needs the privilege for its type:

- Dashboards: `MANAGE ACCESS ON DASHBOARD ARTIFACTS`.
- HTML reports: `MANAGE ACCESS ON REPORT ARTIFACTS`.

For how these privileges interact with artifact grants and account-wide settings, see [Sharing privileges](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

The source file must be valid. For dashboards, each chart or table tile must have a query; otherwise, **Create** isn’t available.

## Create and share from Workspaces

1. Open the `.dash` or `.html` file in Workspaces and select **Share**. The **Create artifact** dialog opens.
2. Under **Who has access**, add the roles or users who should have access. By default, only the owner has access.
3. Choose an access level for each recipient:
   - **Can view**: Open the artifact in Snowsight and Snowflake CoWork.
   - **Can edit**: Open the artifact and publish changes to it, for example after changing the source file in Workspaces.
4. Select **Create**. The artifact link is copied to your clipboard.
5. Send the link to your recipients.

Note

To find a user, search by Snowflake username. When the `2026_08` behavior change bundle is enabled and the account permits access to protected user data, you can also search by name or email address. For the account setting and rollout details, see [User lookup behavior change](/release-notes/bcr-bundles/2026_08/bcr-2429).

## Create and share an artifact from CoCo Desktop

[Preview Feature](/release-notes/preview-features)  — Open

Artifacts in [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/index) is available in accounts where artifacts are available in Snowsight.

CoCo Desktop can publish the HTML and Markdown files that the agent writes as artifacts in your Snowflake account. Creating and sharing a dashboard artifact from CoCo Desktop isn’t supported.

To publish a file, do one of the following:

- In the chat, find the file in the files card that lists the HTML and Markdown files the agent wrote, then select **Publish artifact**.
- Ask CoCo to create an artifact from the file and grant access to the roles you specify. For example:

  > Create a Report artifact from this HTML file and share it with the analytics\_team role.

To manage access, open the **Share** dialog. Add roles or users, and choose an access level for each recipient:

- **Can view**: Open the artifact.
- **Can publish**: Open the artifact, edit it in a CoCo Desktop session, and select **Publish changes** to update the same artifact. This level grants the `WRITE` privilege on the artifact.

Select **Save** to apply your changes, or **Cancel** to discard them. The owner can also delete the artifact from the **Share** dialog.

The **Artifacts** page in the Agent view sidebar lists your artifacts. **All** shows the artifacts that you own and the ones shared with you, and **Favorites** shows the ones that you marked. Favorites are stored in Snowflake, so they appear on every device and in Snowsight. **Copy link** offers **Copy CoWork link** and **Copy Snowsight link**. When Snowflake CoWork isn’t available in your account, **Copy link** copies the Snowsight link.

To turn off Artifacts in CoCo Desktop, disable the `chat.artifacts.enabled` setting.

## Open a shared artifact

The copied link opens the artifact in Snowflake CoWork. To open it in Snowsight, go to **Projects** > **Artifacts** and select it from the list. The same role and user grants apply in both places.

The link doesn’t grant access. Recipients must sign in to the same Snowflake account and have access through a role or a grant to their personal role. For source-data requirements, see [Artifacts and source data](/user-guide/snowflake-artifacts#label-snowflake-artifacts-source-data).

## Publish updates and manage access

Publish updates to Dashboard artifacts through Workspaces. CoCo can author dashboard files, but its sandbox environment doesn’t publish Dashboard artifacts. Publish updates to Report artifacts through Workspaces, CoCo Desktop, or CoCo CLI.

Publishing updates to an existing artifact keeps its link unchanged. Recipients use the same link to view the latest published version.

In the **Share** dialog, only the artifact owner can view or change who has access. Other users see a message that they don’t have permission to manage sharing. This restriction on the dialog doesn’t replace the [SQL grant administration rules](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

For ownership transfer and deletion, see [Artifact owner capabilities](/user-guide/snowflake-artifacts#label-snowflake-artifacts-owner-capabilities).
