# Row access policies in Streamlit in Snowflake

This topic describes using context functions and row access policies in Streamlit in Snowflake warehouse runtimes.

In container runtimes, context functions on owner’s rights connections will return values from the owner role’s context
and so are not appropriate for user-targeted row access policies. However, restricted caller’s rights connections
return the viewer’s context. For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Context functions and row access policies in Streamlit in Snowflake

To use [context functions](/sql-reference/functions-context) such as [CURRENT\_USER](/sql-reference/functions/current_user)
and data from tables with [row access policies](/user-guide/security-row-intro) in a Streamlit in Snowflake app, a user with the
ACCOUNTADMIN role must grant the global READ SESSION privilege to the Streamlit app owner role, as shown in the following example:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT READ SESSION ON ACCOUNT TO ROLE streamlit_owner_role;
```

Note

In a Streamlit in Snowflake app, you can’t use row access policies that use CURRENT\_ROLE. Streamlit in Snowflake apps run with owner’s rights,
so using CURRENT\_ROLE inside a Streamlit app always returns the app owner role.
For more information, see [Understanding owner’s rights and Streamlit in Snowflake apps](/developer-guide/streamlit/object-management/owners-rights).

### Example: Access data in a table with row access policy using CURRENT\_USER

You can use a Streamlit in Snowflake app to govern access to rows in a table protected by a row access policy.
Specify the CURRENT\_USER function in the body of the row access policy and add the row access policy to the table.

The following example demonstrates how to govern access to a table that is protected by a row access policy in a Streamlit in Snowflake app.

1. Create a table and insert data:

   Copy code

   ```
   CREATE TABLE row_access_policy_test_table (
    id INT,
    some_data VARCHAR(100),
    the_owner VARCHAR(50)
   );

   INSERT INTO row_access_policy_test_table (id, some_data, the_owner)
   VALUES
    (4, 'Some information 4', 'ALICE'),
    (5, 'Some information 5', 'FRANK'),
    (6, 'Some information 6', 'ALICE');
   ```
2. Create a row access policy:

   Copy code

   ```
   CREATE OR REPLACE ROW ACCESS POLICY st_schema.row_access_policy
   AS (the_owner VARCHAR) RETURNS BOOLEAN ->
    the_owner = CURRENT_USER();
   ```
3. Add the row access policy to the table:

   Copy code

   ```
   ALTER TABLE row_access_policy_test_table ADD ROW ACCESS POLICY st_schema.row_access_policy ON (the_owner);
   ```
4. Create a Streamlit app.
5. Grant the global READ SESSION privilege to the Streamlit app owner role:

   Copy code

   ```
   GRANT READ SESSION ON ACCOUNT TO ROLE streamlit_owner_role;
   ```
6. Add the following code to your Streamlit app:

   Copy code

   ```
   # Import Python packages
   import streamlit as st
   from snowflake.snowpark.context import get_active_session

   st.title("CURRENT_USER() + Row Access Policy in SiS Demo :balloon:")
   st.write(
        """You can access `CURRENT_USER()` and data from tables with row access policies
        in Streamlit in Snowflake apps
        """)

   # Get the current credentials
   session = get_active_session()

   st.header('Demo')

   st.subheader('Credentials')
   sql = "SELECT CURRENT_USER();"
   df = session.sql(sql).collect()
   st.write(df)

   st.subheader('Row Access on a Table')
   sql = "SELECT * FROM st_db.st_schema.row_access_policy_test_table;"
   df = session.sql(sql).collect()

   st.write(df)
   ```
