# Streamlit in Snowflake in Workspaces

## Overview

In Snowsight, you can access Streamlit from two places:

- **Projects** » **Streamlit**: Browse and open deployed apps that have been shared with you. From here, you can also select **Edit** on an app to open it in its workspace.
- **Workspaces**: Create and edit apps. This is the recommended starting point when building a new app.

With Streamlit in Snowflake in Workspaces, you can create, edit, and deploy Streamlit in Snowflake apps directly inside
workspaces in Snowsight. Workspaces provide a file-based development environment
that separates editing from publishing, so your changes don’t affect the live app until
you explicitly deploy.

With Streamlit in Snowflake in Workspaces, you can:

- Create a Streamlit app.
- Edit your app privately without breaking the deployed version.
- Multitask between apps, worksheets, and notebooks in a single workspace.
- Collaborate through Git-backed or shared workspaces.
- Deploy a Streamlit app to share with other users.

## Key concepts

### Development app vs. deployed app

When you work on a Streamlit app in a workspace, there are two distinct states:

- **Development app**: A private instance of your app that only you can see while
  you’re working on it.
- **Deployed app**: A Streamlit object in a database and schema, owned by a role. Roles
  that have been granted access to the app can view its output. You create a deployed
  app by clicking **Deploy** in the workspace. Clicking the **Edit** button on the
  deployed app brings you back into your private workspace.

This separation means you can iterate on your code without affecting anyone else’s
experience. Keep in mind:

- Code changes made to the app in the workspace aren’t visible to other users until
  you deploy, even if the development app has been updated.
- Changes to development app settings aren’t immediately propagated to the deployed
  app.
- Changes to the deployed app’s settings aren’t saved across deploy actions.

### Streamlit files

A Streamlit file is any Python file that contains `import streamlit` or
`from streamlit import` in its source code. Workspaces detect Streamlit files and
prompt you to create the necessary configuration files. Once a Streamlit project is
identified, the workspace shows a **Run** button and the folder icon is updated.

## Collaboration models

There are two collaboration models for Streamlit in Snowflake app authoring in workspaces:

- **Git-backed workspaces**: Work well for teams familiar with source control. They allow
  editing app code both in Snowsight and locally on your machine, using Git as the
  syncing mechanism. For setup instructions, see [Sync Streamlit in Snowflake apps with a Git repository](/developer-guide/streamlit/features/git-integration).
- **Shared workspaces**: Support collaborative editing for teams that don’t want to use Git.
  Anyone with access to a shared workspace can run a Streamlit app in it. Only the workspace
  owner role can deploy the app. For more information, see
  [Shared workspaces](/user-guide/ui-snowsight/workspaces-shared).

## Prerequisites

To create a Streamlit app in a workspace, you need access to a role with:

- USAGE privilege on a compute pool. The account must have a default compute pool
  configured, and your user must have a default warehouse selected.

Apps in Workspaces run on a compute pool (container runtime). You are billed for compute
pool usage while an app is running. Compute nodes are released after 3 hours of inactivity.

To deploy a Streamlit app from a workspace, your role also needs:

- USAGE privilege on the target database and schema.
- CREATE STREAMLIT privilege on the target schema.

## Next steps

- [Create and run a Streamlit app in a workspace](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run)
- [Administrator control and cost monitoring](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-admin)
- [Streamlit in Snowflake in Workspaces limitations](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-limitations)
