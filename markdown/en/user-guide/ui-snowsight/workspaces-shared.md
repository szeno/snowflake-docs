# Shared workspaces

## Overview

A standard Snowflake workspace provides an environment for individual development and can be created as a private workspace or connected to
a Git repository.

You can also create a *shared workspace* to share with specific roles. Shared workspaces introduce a new model for team-based
collaboration directly within Snowflake. Instead of sharing individual files, users can create dedicated spaces where work is organized, versioned,
and shared with roles that represent teams or groups.

| Workspace type | Purpose | Storage location |
| --- | --- | --- |
| Private | Default mode for individual development. Ideal for ad-hoc exploratory data analysis (EDA), administration tasks, and private projects. | User’s Personal Database (PDB) |
| Git-synced | Private workspace connected to a Git repository. Ideal for production workloads and complex multi-file projects. | User’s PDB, synced to an external Git repository |
| Shared | Multi-user collaboration using wiki-style drafts and a publish model. Shared as RBAC schema objects in databases and schemas. | Standard database and schema |

Expand

Show lessSee more

## Shared workspace functionality

Shared workspaces are created within a specific database and schema. The privileges granted to a user’s role determine what the user can do:

| Workspace privilege | Capabilities |
| --- | --- |
| `READ` | View the workspace and its files without changing their contents. |
| `WRITE` | Create, edit, and delete files. Includes `READ`, so a separate `READ` grant isn’t required. |
| `OWNERSHIP` | Full control over the workspace. Only one role owns a workspace at a time. |

Expand

Show lessSee more

Access to workspace files doesn’t grant access to the data or compute used by their code. Users run queries with their own execution privileges.
For privilege definitions, see [Workspace privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-workspace).

Users with write access can collaborate on file edits and move or copy files from their private workspaces into a shared workspace.
For the draft and publish workflow, see [Collaborate in a shared workspace](#label-shared-workspaces-collaborate-in-a-shared-workspace).

## Create a shared workspace

The creation dialog selects your current Snowsight user-menu role as the owner by default.
The owner role menu lists all your roles, so you can select a different role to own the shared workspace.
The execution role selected inside an open SQL file doesn’t determine the workspace’s owner.

Shared workspaces are created within a specific database and schema that the role has access to. To create a shared workspace, the role must either own the destination schema or have sufficient privileges on it:

- **Option 1**: OWNERSHIP on the destination schema.
- **Option 2**: Sufficient privileges on the schema — USAGE on the database, and USAGE and CREATE WORKSPACE on the schema:

  Copy code

  ```
  GRANT USAGE ON DATABASE <database> TO ROLE <role>;
  GRANT USAGE, CREATE WORKSPACE ON SCHEMA <database>.<schema> TO ROLE <role>;
  ```

Shared workspaces can be shared with roles that have the USAGE privilege on the database where the shared workspace is located.

To grant `CREATE WORKSPACE` on a schema, use a role that owns the schema, has the global `MANAGE GRANTS` privilege,
or holds `CREATE WORKSPACE` on that schema with `WITH GRANT OPTION`. Having `CREATE WORKSPACE` alone doesn’t authorize a role to grant it to others.
The accompanying `USAGE` grants also require grant authority on their respective objects. For details, see
[GRANT access control requirements](/sql-reference/sql/grant-privilege#label-grant-privilege-access-control-requirements).

To create a shared workspace, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the **Workspaces** menu, select **Shared workspace** in the **Create** section.
4. Specify a shared workspace name.
5. Review the owner role. Your current role is selected by default; you can choose another of your roles from the menu.
6. Select a shared database and schema for the workspace.
7. Specify the roles to share the workspace with.
8. Select **Create** after you have finished adding roles.

## Access and filter shared workspaces

You can navigate, filter, and search for workspaces using the **Workspaces** menu. Your current role from the
Snowsight user menu determines which shared workspaces you can see and access. To use a different role,
select your name in the lower-left corner » **Switch role**. Changing the role inside a SQL file doesn’t change this list.
For details, see [Roles in Workspaces](/user-guide/ui-snowsight/workspaces#label-workspaces-role-context).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **Workspaces** menu. The menu displays a list of all accessible workspaces.
4. Refine the list of workspaces using the filter buttons at the top of the list:
   :   - **All** - View all workspaces you have access to, including private and shared workspaces.
       - **Private** - Only display the workspaces that are private to you.
       - **Shared** - Only display the workspaces that have been shared with you.
5. To search for a workspace, start typing the workspace name in the **Search field** (indicated by a magnifying glass icon). The list
   dynamically filters to show only the workspaces matching your search query.
6. Select the name of the workspace to open. A checkmark appears next to the currently active workspace.

## Share files and folders in a workspace

There are two ways to share files and folders in a private workspace with other users:

- **Move** or **Copy** a file or folder from the workspace list into a shared workspace.
- Click **Share** to share a single file that is open in the Workspaces editor.

To move or copy files or folders from the workspace list:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the files or folders to move or copy in the workspace list.
4. Select the ellipsis [![More options](/static/images/snowsight/snowsight-worksheets-gs-options.png)](/static/images/snowsight/snowsight-worksheets-gs-options.png) for the selected items.
5. Select **Copy to** or **Move**.
6. In the dialog that appears, select a shared workspace destination for the items.
7. Select **Copy to destination** or **Move**.

> Note
>
> You can also copy and move files to another private workspace.

To share the file currently open in the Workspaces editor:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. From the currently open file in the editor, click **Share** on the upper-right.
4. From the drop-down, you can:
   - **Move file to shared workspace**: Select a destination and select **Move**. Only shared workspaces are displayed.
   - **Copy URL**: Copy the file’s unique URL to your clipboard. This option is only available if the file is in a shared workspace. Any user
     with access to that shared workspace can use this URL to directly open the file and its containing workspace, making it efficient to share
     specific files. If the file is deleted or renamed, the URL will no longer work.
   - **Copy code**: Copy the contents of the file to clipboard.
   - **Download**: Download the file to your computer.

After a move or copy, the file or folder is published in the shared workspace and is immediately visible to all collaborators with access.

### Manage access to a shared workspace

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the ellipsis [![More options](/static/images/snowsight/snowsight-worksheets-gs-options.png)](/static/images/snowsight/snowsight-worksheets-gs-options.png) next to the shared workspace you want to manage.

   ![Select Configure workspace from the ellipsis menu.](/static/images/workspaces/configure-workspace.png)
4. Select **Configure workspace**.
5. Select the **Location & access** tab from the **Configure workspace** dialog. From this tab, you can:

> - Remove a role that was granted to a user by selecting the trash icon.
> - Add a new role to access the shared workspace. To filter the list, start typing a role name.

## Collaborate in a shared workspace

Shared workspaces use a wiki-style collaboration model to manage changes:

| Concept | Description |
| --- | --- |
| Draft State | When you begin editing a file, your changes enter a draft state. The file does not automatically update with changes from other collaborators, and only you can see your edits. |
| Publishing | To make your changes visible to all other collaborators, you must publish the file. This is a per-file action that updates the shared version. |
| Publish history | For any file, you can view the history of published versions by selecting the **Publish changes** drop-down and selecting **View publish history**. |

Expand

Show lessSee more

When you access a shared workspace, you automatically see the latest, published versions of all files. The only exception is any file you
currently have in a draft state.

Note

Certain actions on the file tree do not require a separate publishing action and are immediately visible to all collaborators. These
actions include uploading, renaming, and deleting files and/or folders.

To collaborate within a shared workspace, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Open a workspace and make your updates.
4. Select **Publish**. Your changes are published, and the file is updated for all collaborators.

   > Note
   >
   > If a file with a draft (or one of its parent folders) is deleted by another user, you will be prompted to recreate it (and its folder path) when publishing.

When you are collaborating in a shared workspace, you can take the following actions on files in draft state using the **Publish changes** drop-down:

- **View publish history** - Select **View publish history** to see the history of published versions of the file.
- **Show changes** - Select **Show changes** to compare your current local draft against the latest published version in a side-by-side
  comparison view. Review all changes made between your draft and the latest published version. Select **Hide changes** to return to the editor.
- **Discard changes** - Select **Discard changes** to permanently erase your unpublished draft edits
  and revert the file to the last published version. You are prompted to confirm.

### Resolve conflicts

If another user publishes a version of the file while you’re working on a draft, you will be prompted to take action when you attempt to
publish:

- Select **Overwrite** to overwrite the version published by the other user, making your version the latest published version.
- Select **Cancel** to exit, and then select **Discard**. Your edits are discarded and the other user’s version is now the latest published version.
- Select **Show differences** to view a side-by-side view to resolve the conflict before publishing your changes.

### View publish history

After making updates to a file in a shared workspace, you can revert to a previous version of a file by viewing its publish history.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Open the file you want to check or restore from its publish history.
4. Select the **Publish changes** drop-down and select **View publish history**.
5. In the right-hand panel, browse through the different versions by clicking on the timestamps.
6. Filter the list of versions by selecting **All** (to view every version), **By me** (to view your own updates), or **By others** (to view changes made by collaborators).
7. Select a specific timestamp to preview a version in the left-hand panel.
8. When you find the version you want to revert to, select it and then select **Restore this version**.
9. Select **Restore and publish** to confirm. The file opens in the editor, and you can choose to publish this version or continue editing.
