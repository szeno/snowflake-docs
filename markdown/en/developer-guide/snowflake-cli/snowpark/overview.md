# Using Snowpark in Snowflake CLI

The [Snowpark API](/developer-guide/snowpark/index) provides an intuitive library for querying and processing data at scale
in Snowflake, without using SQL. Using a library for any of three languages, you can build applications that process data in Snowflake—without moving
data to the system where your application code runs—and process at scale as part of the elastic and serverless Snowflake engine.

Snowflake CLI gives developers convenient tooling for developing and managing their Snowpark functions and procedures.
To create and maintain Snowpark functions and procedures, use the following process:

- [Initialize](/developer-guide/snowflake-cli/snowpark/initialize) — create a boilerplate

  The `snow init <project-name> --template example_snowpark` command creates a boilerplate project that you can customize.
- [Create](/developer-guide/snowflake-cli/snowpark/create) — create a project definition

  You edit the `snowflake.yml` file with the project details.
- [Build](/developer-guide/snowflake-cli/snowpark/build) — create artifacts

  The `snow snowpark build` command builds the Snowpark project as a `.zip` archive that can be used by the `snow snowpark deploy` command. The archive is built using only the `src` directory specified in the `snowflake.yml` file.
- [Deploy](/developer-guide/snowflake-cli/snowpark/deploy) — create Snowflake objects

  The `snow snowpark deploy` command uploads local files to the specified stage and creates procedure and function objects defined in the project.
- [Execute](/developer-guide/snowflake-cli/snowpark/execute) — use deployed procedures and functions

  The `snow snowpark execute` command executes deployed procedures and functions.
- [Upload](/developer-guide/snowflake-cli/snowpark/upload) — upload already implemented Snowpark functions, procedures, and custom packages, such as from PyPi, in your projects.

  The `snow snowpark package` commands let you reuse existing packages.
- [Manage](/developer-guide/snowflake-cli/snowpark/manage) — manage your Snowpark functions and procedures

  The `snow snowpark` and `snow object` commands let you create, list, execute, and delete Snowpark functions and procedures.
