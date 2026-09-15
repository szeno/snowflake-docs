# Restricted caller’s rights and Streamlit in Snowflake

By default, all Streamlit in Snowflake apps [run with the privileges of the owner](/developer-guide/streamlit/object-management/owners-rights),
not the privileges of the caller. The Streamlit app developer can define whether a
container-runtime app runs with owner’s rights or restricted caller’s rights. Restricted caller’s rights
aren’t supported in warehouse runtimes. Restricted caller’s rights require Streamlit version 1.53.1 or later.

Restricted caller’s rights allow a Streamlit app to run with caller’s rights, but restrict which of the caller’s
privileges the app runs with. With restricted caller’s rights, a Streamlit app can’t run with a specific privilege
unless an administrator expressly allows it. Administrators use [caller grants](#label-streamlit-restricted-callers-rights-required-caller-grants)
to define which of the caller’s privileges an app can run with. This way, Streamlit apps only access data (on behalf
of the viewer) that they are authorized to access.

For more information, see [Restricted caller’s rights](/developer-guide/restricted-callers-rights).

## Required caller grants

To access any tables, stored procedures, or warehouses on behalf of the viewer, the Streamlit app developer must have
the caller grants granted by a user with the MANAGE CALLER GRANTS privilege.

### Example workflow

1. The administrator grants the MANAGE CALLER GRANTS privilege to the `data_science_manager` role:

   Copy code

   ```
   GRANT MANAGE CALLER GRANTS ON ACCOUNT TO ROLE data_science_manager;
   ```
2. A user with the `data_science_manager` role grants the following privileges to the `streamlit_app_developer` role:

   - Caller usage privileges on the database and schema, and caller select privileges on the table, to the
     `streamlit_app_developer` role so that Streamlit apps owned by that role can access
     the `streamlit_db.streamlit_schema.streamlit_table` table with the SELECT privilege:

     Copy code

     ```
     GRANT CALLER USAGE ON DATABASE streamlit_db TO ROLE streamlit_app_developer;
     GRANT CALLER USAGE ON SCHEMA streamlit_db.streamlit_schema TO ROLE streamlit_app_developer;
     GRANT CALLER SELECT ON TABLE streamlit_db.streamlit_schema.streamlit_table TO ROLE streamlit_app_developer;
     ```
   - Usage privileges to the `streamlit_app_developer` role to use the `streamlit_wh` warehouse:

     Copy code

     ```
     GRANT USAGE ON WAREHOUSE streamlit_wh TO ROLE streamlit_app_developer;
     ```

For more information about caller grants, see [About caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants)
and [GRANT CALLER](/sql-reference/sql/grant-caller).

## Use cases for restricted caller’s rights in Streamlit in Snowflake

Restricted caller’s rights in Streamlit in Snowflake let you control the following:

- Which pages of a Streamlit app are available
- Which data in the Streamlit app is available
- Which data with row access policies the CURRENT\_ROLE can access
- Which warehouses are accessible
- Which stored procedures can be called in a Streamlit app

## Restricted caller’s rights in container runtimes

In container runtimes, you can combine owner’s rights and restricted caller’s rights in the same app.

- To create a connection that uses owner’s rights, use `st.connection("snowflake")`.
- To create a connection that uses restricted caller’s rights, use `st.connection("snowflake-callers-rights")`.

For more information, see [st.connection](https://docs.streamlit.io/develop/api-reference/connections/st.connections.snowflakeconnection) and `SnowflakeConnection` in the Streamlit documentation.

The following example shows how to create a caller’s rights connection:

Copy code

```
import streamlit as st

conn = st.connection("snowflake-callers-rights")
df = conn.query("SELECT CURRENT_USER()")
st.write(f"Running as: {df[0][0]}")
```

Specifying secondary roles is supported in restricted caller’s rights sessions. After establishing a restricted caller’s rights session, run [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) to activate secondary roles.

### Tips and limitations for using restricted caller’s rights in container runtimes

- The token provided in the `Sf-Context-Current-User-Token` header is only valid for two minutes and
  is created at the start of the app session. Create any caller’s rights connections at the top of your app script
  and not behind if-else blocks or pages.
- Restricted caller’s rights connections use the viewer’s default role and not the role they have selected in Snowsight.
- You can use both restricted caller’s rights connections and regular owner’s rights connections in the same app by creating multiple connections.
- Restricted caller’s rights connections only work when your app is using a container runtime. If you try to use a restricted caller’s rights
  connection in a local development environment or in a warehouse-runtime environment, you will get an error.

Important

Restricted caller’s rights connections are session-scoped. If you need to cache data returned from a restricted caller’s rights
connection, you must use session-scoping in the cache decorator. This prevents data from being shared between sessions.
To use session-scoping with caching, set `scope="session"` in the caching decorator. For more information, see
[st.cache\_data](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data) in the Streamlit documentation.
