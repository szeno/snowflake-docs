# Manage your Streamlit app

This topic describes how to view, rename, and modify properties of a deployed Streamlit in Snowflake app.

## Rename a Streamlit app

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to rename.
4. Select **Edit**.
5. Select the name of the app in the upper-left corner.
6. Enter the new name in the text box.
7. Click outside the text box to commit the change.

Use the RENAME TO clause of the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command:

Copy code

```
ALTER STREAMLIT my_app RENAME TO my_new_app;
```

Snowflake CLI does not support renaming a deployed app directly. Use SQL or Snowsight
instead.

## Change the query warehouse

You might want to switch to a warehouse with more capacity to handle the queries run by
your app.

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app whose warehouse you want to change.
4. Select the name of the app in the upper-left corner.
5. Select the new warehouse from the dropdown list.

Use the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command to set the QUERY\_WAREHOUSE
property:

Copy code

```
ALTER STREAMLIT my_app SET QUERY_WAREHOUSE = my_new_warehouse;
```

Update the `query_warehouse` value in your `snowflake.yml` file and redeploy:

Copy code

```
snow streamlit deploy --replace
```

## Change the compute pool

You can change the compute pool for a container-runtime Streamlit app after it’s created.
This has no effect on warehouse-runtime apps.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app whose compute pool you want to change.
4. Select the three-dots button in the upper-right corner, then select **App Settings**.
5. Select a new compute pool from the dropdown.
6. Select **Save**.

Use the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command to set the COMPUTE\_POOL
property:

Copy code

```
ALTER STREAMLIT my_app SET COMPUTE_POOL = my_new_pool;
```

## Change the stage or main file

SnowsightSQLSnowflake CLI

Changing the stage or main file is not available from Snowsight. Use SQL
instead.

Use the [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) command:

To change the stage:

Copy code

```
ALTER STREAMLIT my_app SET ROOT_LOCATION = '@my_db.my_schema.new_stage';
```

To change the main file:

Copy code

```
ALTER STREAMLIT my_app SET MAIN_FILE = 'new_main.py';
```

Update the `main_file` or artifact paths in your `snowflake.yml` and redeploy:

Copy code

```
snow streamlit deploy --replace
```

## List Streamlit apps

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.

Snowsight displays all Streamlit apps available to your current role.

Use the [SHOW STREAMLITS](/sql-reference/sql/show-streamlits) command:

Copy code

```
SHOW STREAMLITS;
```

List deployed Streamlit apps:

Copy code

```
snow streamlit list
```

## View app details

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app.

The app details panel shows the app’s database, schema, warehouse, and other properties.

Use the [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit) command:

Copy code

```
DESC STREAMLIT my_app;
```

Use the `describe` command:

Copy code

```
snow streamlit describe my_app
```

## Share a Streamlit app

You can share your Streamlit app with other Snowflake users by granting USAGE privilege
to a role. For more information about sharing options, see
[Sharing Streamlit in Snowflake apps](/developer-guide/streamlit/features/sharing-streamlit-apps).

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to share.
4. Select **Share**.
5. Begin typing the name of the role you want to share your app with, and then select it.
6. Optional: Select **Copy to clipboard** to copy the app URL.
7. Select **Done**.

Grant USAGE privilege on the Streamlit object:

Copy code

```
GRANT USAGE ON STREAMLIT my_app TO ROLE viewer_role;
```

Share the app with a role:

Copy code

```
snow streamlit share my_app viewer_role
```
