# Deploying a Streamlit app

The [snow streamlit deploy](/developer-guide/snowflake-cli/command-reference/streamlit-commands/deploy) command creates a new Streamlit object
inside your chosen database and schema. By default, this command looks for a main file called `streamlit_app.py`
in your current working directory.

## Prerequisites

Before deploying a Streamlit app with Snowflake CLI, you should meet the following prerequisites:

- Ensure that you have a local Streamlit app with the correct directory structure and `snowflake.yml` project definition file must exist.
- Ensure that your account has the correct privileges as described in [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).
- Ensure that you can create or have access to a named stage where you can upload your Streamlit app files.

## How to deploy a Streamlit app

Note

With the release of Snowflake CLI 3.14.0, the `snow streamlit deploy` command now uses the updated CREATE STREAMLIT syntax (FROM *source\_location*) instead of the deprecated syntax (ROOT\_LOCATION = ‘<stage\_path\_and\_root\_directory>’). To continue using the deprecated syntax, you can use the `--legacy` option.

The `snow streamlit deploy` command uploads local files to a stage and creates a new Streamlit object inside your chosen database and schema. Your [project definition file](/developer-guide/snowflake-cli/streamlit-apps/manage-apps/initialize-app#label-snowcli-streamlit-project-definition) should specify the main Python file and query warehouse. You can also specify the following options:

- `--replace`: Replaces the specified Streamlit app, if it already exists.
- `--open`: Opens the Streamlit app in your default browser after deploying the app.
- `--prune`: Removes files that exist in the stage, but not files in the local filesystem (by default no files are removed).
- `--legacy`: Uses the deprecated SQLsyntax (ROOT\_LOCATION = ‘<stage\_path\_and\_root\_directory>’).

By default the command automatically deploys the `environment.yml` file and the content of the `pages/`
directory, if any of those exists. You can use different files by using [command-line options](/developer-guide/snowflake-cli/command-reference/streamlit-commands/deploy).

For more information about creating Streamlit apps, see the CLI [snow streamlit deploy](/developer-guide/snowflake-cli/command-reference/streamlit-commands/deploy) and
SQL [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) commands.
