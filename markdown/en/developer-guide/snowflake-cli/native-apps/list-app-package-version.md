# Listing all versions defined in an application package

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your Snowflake Native App project.

## How to list all versions defined in an application package

The [snow app version list](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-list) command lists all versions defined in an application package. This command uses the resolved project definition to determine the name of the application package for which the versions will be listed.

To list the versions of an application package, do the following:

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Execute the `snow app version list` command from within your project, similar to the following:

   Copy code

   ```
   snow app version list --connection="dev"
   ```

When successful, the command displays a list of existing versions in the default format or in the format specified by you through the command line.
For more information about listing the versions of an application package, see the [snow app version list](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-list) command.
