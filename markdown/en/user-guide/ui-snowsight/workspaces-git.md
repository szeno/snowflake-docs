# Integrate workspaces with a Git repository

Important

Starting in September 2025, Snowflake is gradually upgrading accounts from Worksheets to Workspaces. Workspaces will become the default
SQL editor. For more information, see [Defaulting accounts from Worksheets to Workspaces](/release-notes/bcr-bundles/un-bundled/bcr-2117).

## Overview

Workspaces can be local to Snowflake, or you can sync workspaces in development with a branch in a Git repository. In Workspaces, you can:

- [Create a workspace that is connected to a Git repository](#label-create-a-git-workspace).
- [Create a new branch](#label-create-a-new-branch), [switch branches](#label-switch-branches-workspace), or [fetch a remote branch](#label-fetch-remote-branches-workspace).
- Pull the latest changes from your Git repository into your workspace.
- [Track any added, updated, or deleted files](#label-view-updated-workspace-files).
- [Commit and push updated files](#label-commit-and-push-workspaces-changes) back to your Git repository.
- [View and resolve any conflicts](#label-resolve-workspaces-conflicts) directly in Workspaces.

### Create a Git workspace

To develop and maintain files directly in Snowsight, you can create a workspace connected to a Git repository.

Note

- A Git repository must contain at least one branch; empty repositories aren’t supported.
- Git repositories larger than 2 GB aren’t supported.

For a complete list of limitations, see [Git in Snowflake limitations](/developer-guide/git/git-limitations).

To create a new Git-synced workspace, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the **Workspaces** menu, select **From Git repository**.
4. Copy the URL from your Git repository (for example, `https://www.github.com/my-user/my-repo-name`), and then paste it into the **Repository URL** field.
5. Optional: Rename the new Git-synced workspace.
6. In the **API Integration** menu, select an API integration.

   The API integration must allow access to the Git repository URL you used in step 4. Creating an API integration requires the
   [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) privilege, which is often restricted to admin roles in many
   accounts. If another role created the API integration, the current role must have the USAGE privilege on that API integration.
7. Select an authentication method:

   - **OAuth2** - To use OAuth2 for authentication, you must configure the API integration to support OAuth with your Git provider. For more information,
     see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up). Complete the following steps:

     1. Select **Sign in** to authenticate with your GitHub repository.
     2. Select **Configure** next to the account you want to use, then select **Authorize** next to **Snowflake Computing** to allow the
        `snowflakedb` app to access your repository.
     3. Under **Permissions**, ensure that **Read access to metadata** and **Read and write access to code** permissions are granted to
        allow you to pull and push changes to your repository.
     4. Under **Repository access**, specify the level of access you want to grant to Snowflake.
     5. Select **Save**.

     For more information, see [OAuth app access](https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/authorizing-oauth-apps#oauth-app-access).
     After an authorized admin approves the app, all users in the account can use it.
   - **Personal access token** - Select the database and schema where the object containing your token is stored. To create a new secret,
     select **+ Secret** and enter the required details. The API integration must be configured to allow access to this secret or to all secrets.
   - **Public repository** - Select this option if you are using a public repository that doesn’t require authentication. Note that it isn’t
     possible to commit and push any changes from your workspace to this public repository.
8. Select **Create**.

### Update author details and credentials for a branch

By default, your Snowflake email and username are used for committing changes to your Git repository. You can update these at any time.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **Changes** tab.
4. Select the ellipsis and then select **Edit credentials**.
5. Specify an author name and email.
6. Select **Update**.

### Create a new branch

You can create a new branch from your current branch to work on changes independently.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **Changes** tab.
4. Select the repository dropdown.
5. Select **+ New**.
6. Specify a new branch name, and then select **Create**.

### Switch to a different branch

If you have saved but uncommitted changes, you’ll need to choose how to handle them before switching branches.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the Git workspace view, select **Changes**.
4. From the branch menu, select the branch you want to switch to.

   Tip

   To filter the list, start typing a branch name.

### Fetch remote branches

If a new branch was created outside of Snowsight (for example, one created in your Git provider), you can fetch it into your Git-synced
workspace using the **Fetch All** option. This updates your list of available remote branches.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the Git workspace view, select **Changes**.
4. Select the down arrow next to the **Pull** menu, and then select **Fetch All**.
   When the fetch finishes, newly created remote branches appear in the branch list and are available to check out.

### View updated files

To view all the files that were added, deleted, or modified since your last successful commit and push, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. At the top of the folder view, select **Changes**.
   Modified files are indicated with an **M**, added files are indicated with an **A**, and deleted files are indicated with a **D**.
4. To view a visual diff of the changes in the editor, select a file.

### Commit and push updates

After reviewing your changes, you can commit and push them to your remote Git repository from within the workspace.

To commit and push your updated files to the remote Git repository, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select **Changes** at the top of the folder view.
4. Write a commit message in the **Commit message** field.
5. Select **Push**.
6. Write a commit message and select **Push** to push your updates to the Git repository.

   Note

   If conflicts are detected, you are prompted to pull first. Select **Pull** to review a list of files with conflicts.

### View and resolve conflicts

If a conflict occurs during a push, you can view and resolve it directly in the workspace before committing again.

1. In Workspaces, at the top of the folder view, select **Changes**.
   If one or more files have a conflict, a message is displayed at the top of the view. Files with a conflict are indicated with a red **M**.
2. To view a visual diff of the conflict in the editor, select a file.
   Under **File with conflicts**, differences are highlighted inline.
3. Accept the current change, an incoming change, or both changes.
   The result of the merge is shown.
4. Under **Diff View** you can view the current and remote versions side by side.
5. Select **Accept all current** or **Accept all remote**.
6. After you resolve the conflicts, select **Push**.
7. Write a commit message.
8. Select **Push**.
