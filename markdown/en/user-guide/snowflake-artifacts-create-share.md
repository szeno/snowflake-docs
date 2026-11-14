# Create and share a dashboard or HTML report

Publish a `.dash` or `.html` file from [Workspaces](/user-guide/ui-snowsight/workspaces) as an artifact that others can open in Snowsight or Snowflake CoWork. You can also publish an HTML report from CoCo Desktop or one generated in Snowflake CoWork. Recipients access the artifact, not the source file. For artifact types, ownership, and access privileges, see [Snowflake Artifacts](/user-guide/snowflake-artifacts).

## Before you begin

Dashboard or HTML report authoring must be available in your account. To share the artifact, your current role needs the privilege for its type:

- Dashboards: `MANAGE ACCESS ON DASHBOARD ARTIFACTS`.
- HTML reports: `MANAGE ACCESS ON REPORT ARTIFACTS`.

For how these privileges interact with artifact grants and account-wide settings, see [Sharing privileges](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

The source file must be valid. For dashboards, each chart or table tile must have a query before you publish the artifact.

### Dashboard limitations

Use Workspaces to create, edit, preview, and publish dashboards. CoCo Desktop doesn’t support creating, editing, previewing, or publishing dashboards. Snowflake CoWork doesn’t support editing or publishing dashboards.

## Create and share from Workspaces

To publish or share a file from Workspaces:

1. Open the `.dash` or `.html` file in Workspaces. Select **Publish artifact**, or **Share** if you’ve already published it. The sharing dialog opens.
2. Under **Who has access**, add the roles or users who should have access. By default, only the owner has access.
3. Choose an access level for each recipient:
   - **Can view** (`READ`): Open the artifact.
   - **Can publish** (HTML reports) or **Can edit** (dashboards) (`WRITE`): Open the artifact and publish changes after editing its source file. This permission alone doesn’t grant access to the source workspace file.
4. If you’re publishing for the first time, select **Create** to create the artifact and copy its link. For an existing artifact, use the sharing dialog to publish an update or change access.
5. Send the link to your recipients. Granting access and sending the link are separate actions.

## Create and share an artifact from CoCo Desktop

[Preview Feature](/release-notes/preview-features)  — Open

Artifacts in [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/index) is available in accounts where artifacts are available in Snowsight.

CoCo Desktop can publish the HTML and Markdown files that the agent writes as artifacts in your Snowflake account. Dashboard creation, editing, preview, and publication aren’t supported in CoCo Desktop.

To publish a file, find it in the chat’s files card and select **Publish artifact**. Choose the users or roles who can access it.

To manage access, open the **Share** dialog. Add roles or users, and choose an access level for each recipient:

- **Can view** (`READ`): Open the artifact.
- **Can publish** (`WRITE`): Open the artifact, edit it in a CoCo Desktop session, and select **Publish changes** to update the same artifact.

Select **Save** to apply your changes, or **Cancel** to discard them. The owner can also delete the artifact from the **Share** dialog.

The **Artifacts** page in the Agent view sidebar lists your artifacts. **All** shows the artifacts that you own and the ones shared with you, and **Favorites** shows the ones that you marked. Favorites are stored in Snowflake, so they appear on every device and in Snowsight. **Copy link** offers **Copy CoWork link** and **Copy Snowsight link**. When Snowflake CoWork isn’t available in your account, **Copy link** copies the Snowsight link.

To turn off Artifacts in CoCo Desktop, disable the `chat.artifacts.enabled` setting.

## Publish an HTML report from Snowflake CoWork

If your agent has the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool), ask Snowflake CoWork to generate an HTML report. Review the generated report, then select **Publish artifact** on its chat result to choose the users or roles who can access it. A generated file in a conversation isn’t a shared Report artifact until you publish it. For more information about generating HTML, see [Document generation in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation).

## Open a shared artifact

Open the link to the shared artifact, or go to **Projects** > **Artifacts** and select it from the list.

The link doesn’t grant access. Recipients must sign in to the same Snowflake account and have access through a role or an individual user grant. For source-data requirements, see [Artifacts and source data](/user-guide/snowflake-artifacts#label-snowflake-artifacts-source-data).

## Publish updates and manage access

Publish updates to Dashboard artifacts from Workspaces. Publish updates to Report artifacts from their supported source workflow in Workspaces, CoCo Desktop, or CoCo CLI. A report’s data doesn’t refresh when someone opens it; update the HTML and publish it again to show newer data. For an HTML report generated in CoWork, generate updated content and publish it again to update the shared artifact.

Publishing updates to an existing artifact keeps its link unchanged. Recipients use the same link to view the latest published version.

In the **Share** dialog, only the artifact owner can view or change who has access. Other users see a message that they don’t have permission to manage sharing. This restriction on the dialog doesn’t replace the [SQL grant administration rules](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

For ownership transfer and deletion, see [Artifact owner capabilities](/user-guide/snowflake-artifacts#label-snowflake-artifacts-owner-capabilities).
