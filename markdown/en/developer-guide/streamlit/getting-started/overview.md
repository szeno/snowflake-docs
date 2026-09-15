# Getting started with Streamlit in Snowflake

This topic walks you through deploying your first Streamlit in Snowflake app in under five minutes using
a container runtime. After that, two hands-on examples show you how to build real apps
that query data, personalize the experience for each viewer, and write back to Snowflake.

## Prerequisites

Before you can create a Streamlit app, ensure that your administrator has completed the
[essential security setup](/developer-guide/streamlit/object-management/security#label-streamlit-essential-security-setup) for Streamlit apps.

Your role must have the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Database where you create the Streamlit app |  |
| CREATE STREAMLIT, USAGE | Schema where you create the Streamlit app |  |
| USAGE | Compute pool that runs the Streamlit app | For all accounts, Snowflake configures a general-purpose compute pool that typical users will have access to. For more information, see [Configuring your own preferred compute pools for Streamlit apps](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-streamlit). |
| USAGE | Warehouse that runs queries in the Streamlit app |  |

Expand

Show lessSee more

For more information, see [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).

## Deploy your first Streamlit in Snowflake app

The fastest way to get started is to create a Streamlit app using the default starter code.
When you create an app without specifying source files, Snowflake provides example code
automatically.

Note

In Snowsight, you can access Streamlit from two places:

- **Projects** » **Streamlit**: Browse and open deployed apps that have been shared with you.
- **Workspaces**: Create and edit apps. This is the recommended starting point for new apps.

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Workspaces**, then open a workspace.
3. Select **+ Add new** » **Streamlit app**.

Snowflake creates a folder with starter files and opens the app editor. Select **Run** to
preview the example app. Your app runs on a compute pool. No database or schema
selection is needed at this step.

To deploy the app and share it with other users, see
[Create and run a Streamlit app in a workspace](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run).

Run the following SQL commands in a SQL session:

Copy code

```
CREATE STREAMLIT my_first_app
   RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
   COMPUTE_POOL = my_compute_pool
   QUERY_WAREHOUSE = my_warehouse;

ALTER STREAMLIT my_first_app ADD LIVE VERSION FROM LAST;
```

To view your app, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), then In the navigation menu, select **Projects** » **Streamlit**, and select your app.

Note

[Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) version 3.14.0
or later is required. Version 3.14+ uses the modern CREATE STREAMLIT syntax by default.

1. Initialize a new Streamlit project:

   Copy code

   ```
   snow init my_first_app --template example_streamlit
   ```
2. Navigate to the project directory:

   Copy code

   ```
   cd my_first_app
   ```
3. Edit the `snowflake.yml` file to use a container runtime:

   Copy code

   ```
   definition_version: 2
   entities:
   my_streamlit:
      type: streamlit
      identifier: my_first_app
      query_warehouse: my_warehouse
      compute_pool: my_compute_pool
      runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
      main_file: streamlit_app.py
      artifacts:
      - streamlit_app.py
   ```
4. Deploy the app and open it in your browser:

   Copy code

   ```
   snow streamlit deploy --open
   ```

### Edit your app

After deploying, you can edit the app code to customize it. For a quick test:

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then select your app.
3. Select **Edit**.
4. Modify the code in `streamlit_app.py`.
5. Select **Run** to see your changes.

1. Get your app’s source location:

   Copy code

   ```
   DESCRIBE STREAMLIT my_first_app;
   ```
2. Copy an updated file to that location:

   Copy code

   ```
   COPY FILES INTO '<live_version_location_uri>' FROM @my_stage FILES = ('streamlit_app.py');
   ```

1. Edit `streamlit_app.py` in your local project directory.
2. Redeploy:

   Copy code

   ```
   snow streamlit deploy --replace
   ```

For more information, see [Edit your Streamlit app](/developer-guide/streamlit/app-development/editing-your-app).

## What’s next?

Now that you have a running app, try one of these hands-on examples:

- [Example: Build a personalized data dashboard](/developer-guide/streamlit/getting-started/example-data-dashboard): Build a dashboard that queries Snowflake data and personalizes
  the display for each viewer using `st.connection` and `st.user`.
- [Example: Build a form that writes to Snowflake](/developer-guide/streamlit/getting-started/example-crud-app): Build a form that writes user input back to a Snowflake table,
  demonstrating `st.form`, dependency management, and `st.user`.

To learn more about specific topics:

- [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app): Detailed instructions
  for creating apps from Snowsight, SQL, or the CLI.
- [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management): Add Python packages
  to your app.
- [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments): Understand container
  and warehouse runtimes.
- [External network access in Streamlit in Snowflake](/developer-guide/streamlit/features/external-access): Connect your app to external services.
