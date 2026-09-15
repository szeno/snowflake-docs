# Personalize your Streamlit app with user information

The [st.user](https://docs.streamlit.io/develop/api-reference/user/st.user) API lets your Streamlit in Snowflake app access information about the person currently
viewing the app. You can use this to display personalized greetings, filter data by user,
or track who performed an action.

## What st.user provides in Streamlit in Snowflake

In Streamlit in Snowflake, `st.user` provides two attributes for the current viewer:

- `st.user.user_name` – the viewer’s Snowflake username.
- `st.user.email` – the viewer’s email address.

The following example greets the viewer by their Snowflake username:

Copy code

```
import streamlit as st

st.write(f"Hello, {st.user.user_name}!")
```

## Look up the viewer’s display name (optional)

`st.user.user_name` returns the Snowflake username (for example, `JSMITH`). To
show a friendlier name, you can look up the user’s display name with
[DESCRIBE USER](/sql-reference/sql/desc-user). This requires elevated privileges:
the app owner’s role must have the MONITOR privilege on the user object, or be an account
administrator.

The following example greets the viewer by their display name:

Copy code

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()

user_info = session.sql(
    f"DESCRIBE USER {st.user.user_name}"
).collect()
display_name = st.user.user_name
for row in user_info:
    if row["property"] == "DISPLAY_NAME":
        display_name = row["value"]
        break

st.write(f"Hello, {display_name}!")
```

## Personalize data queries

Filter query results so each viewer sees only their own data. This example uses
`session.sql()` instead of `conn.query()` so that the query runs fresh on every
rerun rather than returning cached results:

Copy code

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()
data = session.sql(
    "SELECT * FROM my_table WHERE owner = ?",
    params=[st.user.user_name],
).to_pandas()
st.dataframe(data)
```

## Track who performed an action

Include the viewer’s identity when writing data back to Snowflake:

Copy code

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()

with st.form("entry_form"):
    value = st.text_input("Enter a value")
    submitted = st.form_submit_button("Save")

if submitted:
    session.sql(
        "INSERT INTO my_table (created_by, value) VALUES (?, ?)",
        params=[st.user.user_name, value],
    ).collect()
    st.success("Saved!")
```

## Relationship to CURRENT\_USER()

The SQL function CURRENT\_USER() returns the Snowflake username of the session owner. In
Streamlit in Snowflake apps using owner’s rights, this is the owner of the Streamlit object, not the viewer.
To identify the viewer in your Python code, use `st.user` instead.

If you need the viewer’s identity in SQL queries, consider using restricted caller’s rights (Preview).
With restricted caller’s rights, queries run as the viewer, so CURRENT\_USER() returns the viewer’s
identity. For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Runtime differences

`st.user` is available in both container and warehouse runtimes. The behavior is
the same in both environments: it returns the identity of the person viewing the app,
not the owner of the Streamlit object.
