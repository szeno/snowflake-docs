# Creating a Snowflake Native App project

You can use the `snow init` command to bootstrap a Snowflake Native App project, and get the project up and running quickly.

To create a Snowflake Native App project from a Snowflake provided Snowflake Native App template:

- Enter a `snow init` command, similar to the following:

  Copy code

  ```
  snow init --template app_basic my_app
  ```

  When successful, the command returns a confirmation message similar to the following:

  ```
  Initialized the new project in my_app
  ```

Caution

Files inside a project directory are processed by Snowflake CLI and could be uploaded to Snowflake when executing other `snow app` commands. You should use caution when putting any sensitive information inside files in a project directory.

For more information about creating a Snowflake Native App project, see the snow init command as well as the [Snowflake CLI templates](https://github.com/snowflakedb/snowflake-cli-templates) repository.
