# Opening an app in a browser

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your Snowflake Native App project.

## How to open a Snowflake Native App application in your default browser

The `snow app open` command opens the app specified in the resolved project definition of your Snowflake Native App project.

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Execute the `snow app open` command from within your project, similar to the following:

   Copy code

   ```
   snow app open --connection="dev"
   ```

   When successful, the command returns the following message:

   ```
   Application opened in browser.
   ```

   If you have not yet installed an application as part of the `snow app run`, the following error message is displayed:

   ```
   Application not yet deployed! Please run "snow app run" first.
   ```

For more information about opening a Snowflake Native App in a browser, see the CLI [snow app open](/developer-guide/snowflake-cli/command-reference/native-apps-commands/open-app) command.
