# Delete your Streamlit app

Deleting a Streamlit app permanently removes it from Snowflake. Any users with whom you
have shared the app will no longer be able to view or interact with it. Before deleting an
app, ensure that you have saved your application code outside of Snowflake.

## Delete a Streamlit app

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to delete.
4. Select **Edit**.
5. Select the name of the app in the upper-left corner.
6. Select **Delete**, and then select **Delete App**.

Snowflake deletes the Streamlit app and displays the updated list of available apps.

Use the [DROP STREAMLIT](/sql-reference/sql/drop-streamlit) command:

Copy code

```
DROP STREAMLIT my_app;
```

Drop the Streamlit app:

Copy code

```
snow streamlit drop my_app
```
