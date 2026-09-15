# Creating an application package with a version (or patch)

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your native app project.

## How to create an application package with a version (or patch)

The [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) command brings all the different code files together, creates an application package, uploads code to a Snowflake stage in this application package, and creates a version for that application package. If a version already exists, it adds a custom or an auto-incremented patch to it. This command uses the values specified in your resolved project definition to determine the stage to which it uploads files, which files to upload, and the name of the application package to create.

To create an application package and create a version for it, do the following:

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Make relevant changes to your code files, including `snowflake.yml`, `manifest.yml`, adding any setup scripts and extension code files.
3. Execute the `snow app version create` command from within your project, similar to the following:

   Copy code

   ```
   snow app version create V1 --connection="dev"
   ```

   ```
   Version V1 created for application package my_app_pkg.
   Version create is now complete.
   ```

> This command creates a version **V1** and a default patch **0** for application package `my_app_pkg`.

For more information about adding a version definition to an application package, see the [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) command.
