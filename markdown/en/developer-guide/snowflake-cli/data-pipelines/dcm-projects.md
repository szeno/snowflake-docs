# Managing DCM projects using Snowflake CLI

You can manage a DCM project using Snowflake CLI. For more information about DCM projects, see [Snowflake DCM Projects](/user-guide/dcm-projects/dcm-projects-overview).

## Install Snowflake CLI with DCM project features

To use the `snow dcm` commands, you must install Snowflake CLI version 3.24.0 or later. For more information, see [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).

## Verify you have a valid connection to Snowflake

Snowflake CLI requires a working connection to interact with Snowflake. For information about managing connections, see [Configuring Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli).

For more information about how targets interact with the active connection and role, see
[Project identifier resolution](/developer-guide/snowflake-cli/command-reference/dcm-commands/overview#label-snowcli-dcm-project-identifier-resolution).

## Initialize a DCM project from a template

- To initialize a DCM project from a template, use the `snow init` command:

  Copy code

  ```
  snow init <project_dir_name> --template dcm_project
  ```

  where `<project_dir_name>` is the directory with the DCM project files. This directory is created by the `snow init` command and is populated with the project files generated from the specified template.

  For example, the following command creates the project files in the `MY_PROJECT` directory:

  Copy code

  ```
  snow init MY_PROJECT --template dcm_project
  ```

## Snowflake CLI commands

To support DCM projects, Snowflake CLI added the following commands:

- [snow dcm create](/developer-guide/snowflake-cli/command-reference/dcm-commands/create)
- [snow dcm deploy](/developer-guide/snowflake-cli/command-reference/dcm-commands/deploy)
- [snow dcm describe](/developer-guide/snowflake-cli/command-reference/dcm-commands/describe)
- [snow dcm drop](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop)
- [snow dcm drop-deployment](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop-deployment)
- [snow dcm list](/developer-guide/snowflake-cli/command-reference/dcm-commands/list)
- [snow dcm list-deployments](/developer-guide/snowflake-cli/command-reference/dcm-commands/list-deployments)
- [snow dcm plan](/developer-guide/snowflake-cli/command-reference/dcm-commands/plan)
- [snow dcm preview](/developer-guide/snowflake-cli/command-reference/dcm-commands/preview)
- [snow dcm purge](/developer-guide/snowflake-cli/command-reference/dcm-commands/purge)
- [snow dcm test](/developer-guide/snowflake-cli/command-reference/dcm-commands/test)

## Create and deploy DCM projects

This section describes how to create, validate, and deploy DCM projects using Snowflake CLI.

### Create a DCM project

Use the `snow dcm create` command to create a new DCM project in Snowflake. The project identifier can be specified directly as an argument or resolved from the `manifest.yml` file.

- Create a project using the identifier from the default target specified in the manifest:

  Copy code

  ```
  snow dcm create
  ```
- Create a project using the identifier from the `dev` target specified in the manifest:

  Copy code

  ```
  snow dcm create --target dev
  ```
- Create a project only if it does not already exist:

  Copy code

  ```
  snow dcm create --if-not-exists
  ```

For more information, see [snow dcm create](/developer-guide/snowflake-cli/command-reference/dcm-commands/create).

### Plan a DCM project

Use the `snow dcm plan` command to validate your project before deploying. This command shows what changes would be applied without actually making any modifications.

- Validate a project:

  Copy code

  ```
  snow dcm plan
  ```
- Validate with variable substitution:

  Copy code

  ```
  snow dcm plan -D "db_name=my_database" -D "schema_name=my_schema"
  ```
- Validate using a specific target profile and save the output:

  Copy code

  ```
  snow dcm plan --target dev --save-output
  ```

  When using `--save-output`, the command saves the response and artifacts to a local `out/` directory.

For more information, see [snow dcm plan](/developer-guide/snowflake-cli/command-reference/dcm-commands/plan).

### Deploy a DCM project

Use the `snow dcm deploy` command to apply changes defined in your DCM project to Snowflake.

- Deploy a project:

  Copy code

  ```
  snow dcm deploy
  ```
- Deploy with variable substitution:

  Copy code

  ```
  snow dcm deploy -D "table_name='MY_DB.PUBLIC.MY_TABLE'"
  ```
- Deploy with an alias for the deployment:

  Copy code

  ```
  snow dcm deploy --alias v1.0
  ```
- Deploy from a specific directory using a target profile:

  Copy code

  ```
  snow dcm deploy --from /path/to/project --target prod
  ```

For more information, see [snow dcm deploy](/developer-guide/snowflake-cli/command-reference/dcm-commands/deploy).

### Preview a DCM project

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use the `snow dcm preview` command to return rows from any table, view, or dynamic table defined in your project. This command is useful for testing your definitions before or after deployment.

- Preview data from a table:

  Copy code

  ```
  snow dcm preview --object MY_DB.PUBLIC.MY_TABLE
  ```
- Preview with a row limit:

  Copy code

  ```
  snow dcm preview --object MY_DB.PUBLIC.MY_VIEW --limit 10
  ```
- Preview with variable substitution:

  Copy code

  ```
  snow dcm preview --object MY_DB.PUBLIC.MY_VIEW -D "filter_date='2024-01-01'"
  ```

For more information, see [snow dcm preview](/developer-guide/snowflake-cli/command-reference/dcm-commands/preview).

### Test a DCM project

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use the `snow dcm test` command to run all expectations (data metric functions) defined in your project. This command validates data quality rules and returns pass/fail results.

- Test a project:

  Copy code

  ```
  snow dcm test
  ```
- Test using a target profile:

  Copy code

  ```
  snow dcm test --target dev
  ```
- Test and save the results:

  Copy code

  ```
  snow dcm test --save-output
  ```

The command returns exit code 0 if all tests pass, or exit code 1 if any test fails.

For more information, see [snow dcm test](/developer-guide/snowflake-cli/command-reference/dcm-commands/test).

### Purge a DCM project

Use the `snow dcm purge` command to drop all entities, revoke all grants, and remove all attachments managed by a DCM project without dropping
the project itself. The operation is recorded in the project’s deployment history.

- Purge a project:

  Copy code

  ```
  snow dcm purge
  ```
- Purge a project using a target profile, tagging the purge deployment with an alias for easier identification in the deployment history. Wrap the alias in single quotes so that any shell-special characters (such as `$`) in the value are preserved literally:

  Copy code

  ```
  snow dcm purge --target dev --alias 'purge_v1.0'
  ```
- Purge a project without the confirmation prompt (for example, in CI/CD pipelines):

  Copy code

  ```
  snow dcm purge --force
  ```

For more information, see [snow dcm purge](/developer-guide/snowflake-cli/command-reference/dcm-commands/purge).

### Drop a DCM project

Use the `snow dcm drop` command to drop a DCM project object and its retained deployment history. Objects, grants, and attachments previously
managed by the project remain in place as unmanaged resources.

- Drop a project:

  Copy code

  ```
  snow dcm drop
  ```
- Drop a project only if it exists:

  Copy code

  ```
  snow dcm drop --if-exists
  ```

For more information, see [snow dcm drop](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop).

## Manage deployed DCM projects

After deploying a DCM project, you can list and manage individual deployments.

### List deployed DCM projects

Use the `snow dcm list-deployments` command to list all deployments of a given DCM project.

- List deployments for a project:

  Copy code

  ```
  snow dcm list-deployments
  ```
- List deployments using a target profile:

  Copy code

  ```
  snow dcm list-deployments --target dev
  ```

The output shows the deployment name and alias (if set) for each deployment.

For more information, see [snow dcm list-deployments](/developer-guide/snowflake-cli/command-reference/dcm-commands/list-deployments).

### Drop deployed DCM projects

Use the `snow dcm drop-deployment` command to drop a specific deployment from a DCM project.

- Drop a deployment by name:

  Copy code

  ```
  snow dcm drop-deployment --deployment 'DEPLOYMENT$1'
  ```

  Note

  For deployment names containing `$`, use single quotes to prevent shell expansion.
- Drop a deployment by alias:

  Copy code

  ```
  snow dcm drop-deployment --deployment v1.0
  ```
- Drop a deployment only if it exists:

  Copy code

  ```
  snow dcm drop-deployment --deployment v1.0 --if-exists
  ```

For more information, see [snow dcm drop-deployment](/developer-guide/snowflake-cli/command-reference/dcm-commands/drop-deployment).
