# Share a Streamlit app

## Prerequisites

Before sharing a Streamlit app with Snowflake CLI, you should meet the following prerequisites:

- Ensure that your account has the correct privileges as described in [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).
- Ensure that the app is already deployed in your connection.
- Ensure that your connection has the right ROLE and that the connection uses the correct database and schema.

## How to share a Streamlit app

To share a Streamlit app from the stage, enter the following command:

Copy code

```
snow streamlit share my-app some-role
```

For more information about sharing Streamlit apps, see the CLI [snow streamlit share](/developer-guide/snowflake-cli/command-reference/streamlit-commands/share) command.
