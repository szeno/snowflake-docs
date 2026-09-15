# Alter command behavior using templates

You can use templates to alter the definition using environment variables. For example, the following project definition templates the schema for a Streamlit dashboard:

Copy code

```
definition_version: "1.1"
env:
  schema: "test"
streamlit:
  name: "MY_APP"
  schema: <% ctx.env.schema %>
```

This feature lets you to alter the behavior of the `snow streamlit deploy` command by setting a `schema` environment variable. Using this approach, you can deploy the same dashboard to multiple different schemas by entering the following commands to deploy different schemas:

Copy code

```
schema="staging"; snow streamlit deploy
schema="prod"; snow streamlit deploy
```

Note

The variables and environment variables are case-sensitive.

You can also use the template feature without defining variables in the `env` section. If a variable is not present in `env` section, Snowflake CLI looks for corresponding environment variables. For example, if you define a Streamlit application similar to the following, you can still alter the behavior of `snow streamlit deploy` by specifying a `schema` environment variable.

Copy code

```
definition_version: "1.1"
streamlit:
  name: "MY_APP"
  schema: <% ctx.env.schema %>
```
