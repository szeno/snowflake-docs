# Aug 25, 2026: Remote Development with the Snowflake Extension for Visual Studio Code (*Preview*)

Remote Development with the Snowflake Extension for Visual Studio Code is now available in public preview.

Remote Development lets you create a Snowflake-backed development environment and connect to it over
Remote - SSH from Visual Studio Code or Cursor. You can run Python notebooks, SQL,
scripts, terminals, and Cortex Code on Snowflake-managed compute.

## Key features

- Run notebooks with the **Snowflake Kernel (Python + SQL)**, the same kernel that Snowflake Notebooks use
  in Workspaces, so Python and SQL cells run the same way they do in the Snowsight Workspaces UI.
- Select multiple workspaces for a remote environment and change the selection at any time.
- Use Cortex Code in the remote session in Visual Studio Code and Cursor.

Remote Development requires version 1.38 or later of the Snowflake Extension for Visual Studio Code. It’s enabled by default through the
`ENABLE_NOTEBOOK_SERVICE_REMOTE_VS_CODE_ACCESS` account parameter, which an account administrator can disable.

For details, see [Remote Development with the Snowflake Extension for Visual Studio Code](/user-guide/vscode-ext-remote-development).
