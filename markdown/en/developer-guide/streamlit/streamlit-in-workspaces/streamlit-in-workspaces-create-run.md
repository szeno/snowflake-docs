# Create and run a Streamlit app in a workspace

This topic describes how to create, run, deploy, and configure a Streamlit in Snowflake app in a
workspace.

## Create a Streamlit app

1. Open a workspace in Snowsight.
2. Select **+ Add new** » **Streamlit app**. Alternatively, select the
   **Streamlit app** shortcut from the workspace home screen.

Snowflake creates a folder with the following starter files:

- `streamlit_app.py`: The app source code, pre-populated with a demo app.
- `pyproject.toml`: Where you add Python package dependencies.
- `snowflake.yml`: A declarative file that specifies deployment settings such as
  compute, runtime, and so on.
- `.streamlit/config.toml`: Streamlit configuration settings.

## Run and preview your app

Whenever you open a Streamlit file, an action bar appears at the top of the file. Press
**Run** or use `Cmd+Enter` (Mac) / `Ctrl+Enter` (Windows/Linux) to start or
rerun your app and preview your latest changes.

The running app is a development app: a private instance that only you can see while
you’re working on it. To publish your app to other users, see
[Deploy your app](#label-streamlit-in-workspaces-deploy).

## Deploy your app

Deploying publishes your workspace code to a Streamlit object that other users can
access.

1. In the project pane toolbar, select **Deploy**.
2. In the deploy dialog, review the settings:

   - **App title**: Defaults to the app name in the workspace.
   - **Location**: The database and schema where the Streamlit object is created.
   - **Execution**: The compute pool to run the app and the query warehouse to run
     queries in the app.
   - **Network**: Any External Access Integrations you want to add to the app.
   - **Sharing**: Add roles that will have USAGE privilege on the app.
3. Select **Deploy**.

Snowflake copies your app files into the Streamlit object and makes the app available
to users with the appropriate privileges.

### Redeploy your app

After you make changes to your code, select **Deploy** again in the project pane.
Select the deployment target and confirm. The new code overwrites the existing
Streamlit app.

If you select a different database or schema as the target for the app deployment, the
previous app continues to run in its original location.

### Edit a deployed app

When viewing a deployed Streamlit app in Snowsight, select **Edit** to open
the app’s source code in its workspace. Snowflake opens the workspace and file
associated with the deployed app.

Note

Only the app owner can edit and redeploy a deployed app.

## App settings

The settings dialog lets you configure the following properties for apps in your
workspace:

- **Execution**: The warehouse used to run SQL queries.
- **External network access** via an [External Access Integration](/developer-guide/external-network-access/external-network-access-overview).

For apps in workspaces, settings are stored per app, per user. Changing settings on your
development app doesn’t affect the deployed app.

For deployed apps, settings are stored on the Streamlit object and apply to all
viewers. Settings are also written to `snowflake.yml` so they persist across
deploys.

## Collaboration

There are two collaboration models for Streamlit in Snowflake app authoring in workspaces: Git-backed
workspaces and shared workspaces. For a comparison of both models, see
[Collaboration models](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-overview#label-streamlit-in-workspaces-collaboration-models).

### Git-backed workspaces

Workspaces are private by default: only you can see and edit the code and deploy the app.

To use version control with your Streamlit app, you can sync it with a branch in a Git
repository. To do this, your Snowflake account must already be connected to a Git
repository. For setup instructions, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

Once your account is connected, you can:

- **Create a Git-backed app from a workspace**: In **Workspaces**, select **+** and
  create a new Git workspace. Connect to your repository using OAuth2 or a public
  repository URL, then clone your repo into the workspace and iterate from there.

For full instructions including ongoing sync and pushing changes, see [Sync Streamlit in Snowflake apps with a Git repository](/developer-guide/streamlit/features/git-integration).

### Shared workspaces

In a [shared workspace](/user-guide/ui-snowsight/workspaces-shared), multiple users can
collaborate on a Streamlit app without using Git. Anyone with access to the shared workspace
can run the Streamlit app. Only the workspace owner role can deploy the app.

You can also move a Streamlit app from a private workspace to a shared workspace to make it
available for team collaboration.

To work with a Streamlit app in a shared workspace:

1. Open the shared workspace in Snowsight.
2. Open or create a Streamlit app file in the workspace. You can also move an existing app
   from a private workspace into the shared workspace.
3. Select **Run** to run the app. All users with access to the shared workspace can run
   the app.
4. To publish the app, select **Deploy**. Only the workspace owner role can deploy.

For information about creating and managing shared workspaces, see
[Shared workspaces](/user-guide/ui-snowsight/workspaces-shared).

### Source code mapping

A deployed Streamlit object is connected to one logical source code location: the
workspace and file path it was deployed from.

If you move the location of your application within your workspace, this mapping no
longer works and you need to redeploy from the new source location.
