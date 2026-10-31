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

You deploy to a *deploy target*. A deploy target is a deployed copy of your app that
runs outside the workspace. Each target has its own location, compute, execution role,
and list of people who can open it. A project can have more than one target, for
example a `dev` target and a `prod` target. Each target is stored as a `streamlit`
entity in `snowflake.yml`. For more information, see
[Deploy targets in snowflake.yml](#label-streamlit-in-workspaces-snowflake-yml).

### Set up a deploy target

1. In the project pane toolbar, select **Settings**.
2. In the **Targets** tab, select a target under **Deploy targets**, or select
   **Add deploy target**. A new target starts as a copy of the selected target.
3. Review the target settings:
   - **Target name**: The name of the target. It’s also the entity key in `snowflake.yml`.
   - **App title**: Displayed in the top left corner of the app and in the dashboard.
   - **App ID (optional)**: The name of the Streamlit object, used in the app URL. If
     you leave it blank, Snowflake generates one when you first deploy.
   - **Owner role of deployed app**: The role that owns the Streamlit object. The app
     runs as this role. Apps deployed from a shared workspace always use the workspace
     owner role.
   - **App location**: The database and schema where the Streamlit object is created.
   - **Execution**: The query warehouse that runs queries in the app, and the compute
     pool that runs the app.
4. Select **Save settings**.

### Deploy to one or more targets

1. In the project pane toolbar, select **Deploy**.
2. Select one or more targets. Each target shows whether it’s deployed and when.
3. Select **Deploy**. If you selected more than one target, select **Deploy selected**.

Snowflake copies your app files into the Streamlit object for each target and makes the
app available to users with the appropriate privileges. If a target fails to deploy,
select **Details** next to it to see the error.

A target can’t be deployed until it has an app location. If a project has no targets
that are ready to deploy, select **Add deploy target** to open the app settings.

### Share with roles and users

1. In the project pane toolbar, select **Share**.
2. For each deploy target, add roles or users and select **View only** or
   **View and share** for each.
3. Select **Save grants**.

If the target is already deployed, Snowflake grants USAGE on the app right away. If the
target isn’t deployed yet, Snowflake grants USAGE when you deploy it. In both cases, the
list is saved in `snowflake.yml` as `grants`, so later deploys grant the same access.

If a user doesn’t have USAGE on the app’s database and schema, a warning icon appears next to their name. Hover over it
and select **Grant USAGE** to grant it. If that grant fails, the app isn’t shared with that user.

To stop sharing a deployed app with a user, see [Stop sharing an app with a user](/developer-guide/streamlit/features/sharing-streamlit-apps#label-streamlit-sharing-users-remove).

### Redeploy your app

After you make changes to your code, select **Deploy** again in the project pane.
Select the targets and confirm. The new code replaces the existing Streamlit app for
each target, and Snowflake grants the target’s sharing list again.

If you change the app location of a target, the previous app continues to run in its
original location. To run the app in more than one location, add a deploy target
instead.

### Remove a deployed app or delete a target

In the deploy menu, select the actions menu next to a target, and then select one of
the following:

- **Remove deployed app**: Drops the Streamlit object for the target. The target stays in
  `snowflake.yml`, so you can deploy to it again.
- **Delete target**: Drops the Streamlit object for the target and removes the target
  from `snowflake.yml`. You can’t undo this action.

A project needs at least one deploy target, so you can’t delete the last one.

### Edit a deployed app

When viewing a deployed Streamlit app in Snowsight, select **Edit** to open
the app’s source code in its workspace. Snowflake opens the workspace and file
associated with the deployed app.

Note

Only the app owner can edit and redeploy a deployed app.

## App settings

To open the app settings, select **Settings** in the project pane toolbar. The app
settings have the following tabs:

- **Targets**: Settings for **Preview in workspace** and for each deploy target.
  **Preview in workspace** is the development app that runs in your workspace. For deploy
  target settings, see [Set up a deploy target](#label-streamlit-in-workspaces-deploy-target-add).
- **Network**: External network access via an [External Access Integration](/developer-guide/external-network-access/external-network-access-overview).
  This setting applies to the development app and to every deploy target.

Note

The compute pool and the query warehouse are authorized against different roles, because they
are used at different times:

- **Compute pool**: checked when the app starts, as you, using all roles granted to you,
  including secondary roles.
- **Query warehouse**: checked each time the app runs a query, as the app, using only the
  single role the app runs as. Secondary roles are not used.

As a result, the query warehouse list shows only warehouses that the app’s role can use on its
own. If a warehouse you expect is missing, grant USAGE on it to the app’s role.

Saving the app settings restarts the app and reconnects all user sessions.

Development app settings are stored per app, per user. Changing them doesn’t affect
deployed apps.

Deploy target settings are saved in `snowflake.yml`. Changes to a target apply to its
deployed app the next time you deploy that target.

## Deploy targets in snowflake.yml

Workspaces reads and writes `snowflake.yml` as a [Snowflake CLI](/developer-guide/snowflake-cli/project-definitions/about)
project definition, version 2. Each entity with `type: streamlit` is a deploy target, and
the entity key is the target name. You can edit the file directly, and you can deploy
the same project with `snow streamlit deploy`.

When Workspaces saves `snowflake.yml`, it writes settings that are the same for every
target into a [mixin](/developer-guide/snowflake-cli/project-definitions/specify-entities#label-cli-project-mixins) named `streamlit_shared`, and each target uses that mixin. Settings
that differ between targets are written on each target. Sharing is written as USAGE
`grants`. For example:

Copy code

```
definition_version: 2
mixins:
  streamlit_shared:
    main_file: streamlit_app.py
    query_warehouse: my_warehouse
    compute_pool: my_compute_pool
    runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
    artifacts:
      - streamlit_app.py
      - pyproject.toml
entities:
  dev:
    type: streamlit
    identifier:
      name: my_app
      database: dev_db
      schema: apps
    meta:
      use_mixins:
        - streamlit_shared
  prod:
    type: streamlit
    identifier:
      name: my_app
      database: prod_db
      schema: apps
    grants:
      - privilege: USAGE
        role: analyst
    meta:
      use_mixins:
        - streamlit_shared
```

Keep the following in mind:

- The first time Workspaces saves a file that you wrote by hand, it might restructure
  the file in this way. Comments other than those at the top of the file aren’t kept.
- `definition_version` must be `2`.
- Workspaces can’t resolve [templates](/developer-guide/snowflake-cli/project-definitions/create-templates)
  in an `identifier`. A target with a templated identifier can’t be edited or deployed
  from Workspaces. To delete it, edit `snowflake.yml`.

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
