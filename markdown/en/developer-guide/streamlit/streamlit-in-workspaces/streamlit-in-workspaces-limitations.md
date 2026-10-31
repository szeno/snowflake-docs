# Streamlit in Snowflake in Workspaces limitations

The following limitations apply to Streamlit in Snowflake in Workspaces:

- Only container runtimes are supported for Streamlit in Snowflake in Workspaces.
- Development apps (private apps) cannot be shared with other users. To share a
  Streamlit app, it must be deployed first.
- `snowflake.yml` must use project definition version 2 (`definition_version: 2`).
- Deploy targets with a templated `identifier` can’t be edited or deployed from
  Workspaces.
- A project must have at least one deploy target.
