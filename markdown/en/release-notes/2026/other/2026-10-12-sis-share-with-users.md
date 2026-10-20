# Oct 12, 2026: Share Streamlit in Snowflake apps with individual users (*General availability*)

You can now share a Streamlit in Snowflake app directly with a user, not only with a role. In the **Share Streamlit app** window,
search by username and select a permission level. If the user lacks USAGE on the app’s database and schema, you can
grant it from the same window. The user is notified in Snowsight, and by email if their email address is
verified.

You can also share with users from a workspace’s deploy dialog, or with `GRANT USAGE ON STREAMLIT ... TO USER`.

For more information, see [Share an app with a user](/developer-guide/streamlit/features/sharing-streamlit-apps#label-streamlit-sharing-users).
