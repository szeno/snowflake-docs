# Edit your Streamlit app

After deploying a Streamlit app in Snowsight, you can edit both the app code and
dependencies using Snowsight or SQL commands. The way your changes take effect
depends on the runtime environment and how the app was created.

Note

Apps created with the ROOT\_LOCATION parameter (legacy apps) have limited editing
capabilities and should be converted to use the FROM parameter for full functionality.
For more information, see [Understanding the different types of Streamlit objects](/developer-guide/streamlit/migrations-and-upgrades/overview).

This page only covers apps created with the FROM parameter.

Both container and warehouse runtime environments are subject to possible race conditions
when multiple people edit the same app simultaneously. See the [Collaborative editing considerations](#label-streamlit-collaborative-editing)
section below for details and best practices.

## Editing methods

You can edit your app through an in-browser editor in Snowsight or by uploading
files using SQL commands.

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then select your Streamlit app.
3. In the upper-right corner, select **Edit**.
4. In the file explorer, select or create a new file to edit:

   - To edit an existing file, select it from the file explorer.
   - To create a new file, select **+** (Add) » **Create new file**, enter
     the filename, and then select **Create**. You can include subdirectories in the filename,
     like `subdir/new_file.py`.
   - To upload a file from your local machine, select **+** (Add) » **Upload file**,
     choose the file to upload, modify the filename and path if needed, and then select
     **Upload**.
5. Make your changes in the editor pane.

   Changes are automatically saved to the app’s source location, after a few seconds.
6. Optional: Select **Run**.

   If you don’t want to wait a few seconds for the changes to be saved, you can select
   **Run** to copy the changes immediately.
7. If your app uses a warehouse runtime, viewers must select **Run** to copy the
   changes to their app instance. If your app uses a container runtime, changes are
   directly saved to the live app’s source and will be visible to all viewers the
   next time they interact with the app.

If you have your edited app files on a stage, you can CREATE OR REPLACE your
app with the following command:

Copy code

```
CREATE OR REPLACE STREAMLIT my_app
FROM '@my_stage/app_folder'
MAIN_FILE = 'streamlit_app.py'
QUERY_WAREHOUSE = my_warehouse
RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
COMPUTE_POOL = my_compute_pool
EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration);
```

Alternatively, if you want to update your app files in place or want to update only
a subset of your app files, you can use the following commands:

1. Get the URI of your app’s source location:

   Copy code

   ```
   DESCRIBE STREAMLIT my_app;
   ```

   The `live_version_location_uri` value is the source location for your app. Copy
   this to use in the next step.
2. Upload one or more updated app files to the source location with PUT or COPY FILES.

   Copy code

   ```
   COPY FILES INTO '<live_version_location_uri>' FROM @my_stage FILES = ('streamlit_app.py');;
   ```

Note

[Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) version 3.14.0
or later is required. Version 3.14+ uses the modern CREATE STREAMLIT syntax by default.

If you have a complete set of edited app files on your local machine (including its
`snowflake.yml` file for Snow CLI), you can redeploy your app with the following
command:

Copy code

```
snow streamlit deploy --replace
```

## Runtime behavior differences

The way your edits take effect depends on your app’s [runtime type](/developer-guide/streamlit/app-development/runtime-environments).

### Container runtime

Feature — Generally Available

Not supported in government regions.

When you edit a container runtime app:

- Changes to your app’s source go directly to the live app.
- Current viewers see updates the next time they interact with the app and trigger a rerun. (The Streamlit
  [configuration option](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#server)
  `server.runOnSave` is disabled by default.)
- The **Run** button is available to viewers but not required to propagate changes to a current viewing or editing session.
- All users see the same app instance with immediate changes.

Even though the live app is shared between viewers, the view of the source code in
Snowsight editors isn’t. Therefore, apps on container runtimes are still
subject to race conditions when multiple people edit the app simultaneously. See the
[Collaborative editing considerations](#label-streamlit-collaborative-editing) section below for details and best practices.

### Warehouse runtime

When you edit a warehouse runtime app:

- App source code is copied when each viewer’s instance starts.
- Current viewers must select **Run** to copy updates made to the source during their session.
- Even the person making edits must click **Run** to see changes in their preview pane.
- Each viewer gets their own isolated app instance.

## Collaborative editing considerations

When multiple people edit the same app, be aware of potential conflicts. Both
container and warehouse runtime apps are subject to the following race condition
if more than one person edits the app simultaneously.

### Race conditions

The Snowsight editor works as follows:

- The current source code is copied into the editor pane when you open it or use the file navigator to open a file.
- If you are viewing a file in the editor pane, it doesn’t update automatically when changes are made by others.
- If you make changes in your editor pane, the automatic save will overwrite any changes made by others after you opened the editor.
- There’s no automatic merging of conflicting edits.

For example, the following sequence can lead to lost changes:

1. Developer A opens the editor at 2:00 PM.
2. Developer B makes and saves changes at 2:15 PM.
3. Developer A saves changes at 2:30 PM.
4. Developer B’s changes are lost (overwritten by Developer A).

### Best practices for team editing

To avoid conflicts when working with a team:

- Communicate with your team members before making edits.
- Keep your source files in a Git repository and deploy your code from there.
- Use separate development apps for testing changes.
- Reload the Snowsight editor to get the latest version immediately before making changes.
