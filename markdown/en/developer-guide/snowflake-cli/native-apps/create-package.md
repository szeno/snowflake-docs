# Creating and installing your application

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your native app project.

## How to create an application package and an application object together

The [snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app) command brings all the different code files together, creates an application package, uploads code to a Snowflake stage in this application package, [validates the setup script SQL](/developer-guide/snowflake-cli/command-reference/native-apps-commands/validate-app), and also installs or upgrades an application in the same account from this application package. This command is driven by the values specified in your resolved project definition for determining which stage to upload files to, which files to upload, and the names of the objects to be created.

To create an application object, do the following:

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Make relevant changes to your code files, including `snowflake.yml`, `manifest.yml`, any setup scripts and extension code files.
3. Execute the `snow app run` command from within your project, similar to the following:

   Copy code

   ```
   snow app run --connection="dev"
   ```

> When successful, the command displays a message similar to the following:
>
> ```
> Your application ("my_app_admin") is now live:
> https://app.snowflake.com/data_org/data_acct/#/apps/application/my_app_admin
> ```

Using the `snow app run --connection="dev"` command creates an application using the files on a named stage that is automatically managed by Snowflake CLI. You can also use the command to create or update your application even if your application package already exists. In this case, the command issues an UPGRADE on your application object, which will execute your setup script. For information about how to avoid re-running the setup script, see the next section.

To create an application using a version (and patch) of an existing application package, execute the following:

Copy code

```
snow app run --version v1 --patch 12 --connection="dev"
```

Here, version `V1` and patch `12` are used as an example only.
For more information about creating Snowflake Native App objects, see the [snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app) command.

## How to create an application package

The `snow app deploy` command performs a subset of the steps `snow app run` takes to deploy your
code to Snowflake. While it still brings all the different code files together, creates an application
package, and uploads code to a named stage in this application package, and [validates the setup script SQL](/developer-guide/snowflake-cli/command-reference/native-apps-commands/validate-app), the `snow app deploy` command does not attempt to create or upgrade an application object.

The `snow app deploy` command is particularly useful in the following situations:

- Deploying only the application package and stage files, for situations where an application object is not required (such as part of a Continuous Delivery pipeline).
- Updating the stage files linked to the application object. For example, if you only changed python code files, you do not need to re-create the PROCEDURE, FUNCTION, and STREAMLIT objects that point to it when using stage development mode. This approach saves time and reduces cost, as you do not need to use a warehouse to re-execute the setup script to use the updated python code.

To create an application package without a corresponding application object, do the following:

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Make relevant changes to your code files, including `snowflake.yml`, `manifest.yml`, any setup scripts, and extension code files.
3. Execute the `snow app deploy` command from within your project, similar to the following:

   Copy code

   ```
   snow app deploy --connection="dev"
   ```

> When successful, the command displays a message similar to the following:
>
> ```
> Checking if stage exists, or creating a new one if none exists.
> Performing a diff between the Snowflake stage and your local deploy_root
> ...
> Deployed successfully. Application package and stage are up-to-date.
> ```

You can also use the `snow app deploy` command to restrict which files it synchronizes to
a stage by listing paths as positional arguments after the `snow app deploy` command. For more information about this and other advanced functionality, see the [snow app deploy](/developer-guide/snowflake-cli/command-reference/native-apps-commands/deploy-app) command.
