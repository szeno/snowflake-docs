# Managing dbt Projects on Snowflake using Snowflake CLI

Note

The dbt Projects on Snowflake features in Snowflake CLI are available only in version 3.13.0 or later.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

You can use Snowflake CLI to manage dbt project objects with the following operations:

- [Deploying a dbt project object](#label-snowcli-snow-dbt-deploy)
- [Listing all available dbt project objects](#label-snowcli-snow-dbt-list)
- [Executing a dbt project object command](#label-snowcli-snow-dbt-execute)
- [Describing a dbt project object](#label-snowcli-snow-dbt-describe)
- [Dropping a dbt project object](#label-snowcli-snow-dbt-drop)
- [Copying dbt project files](#label-snowcli-snow-dbt-copy)

## Deploying a dbt project object

The [snow dbt deploy](/developer-guide/snowflake-cli/command-reference/dbt-commands/deploy) command uploads local files to a temporary stage and creates a new dbt project object or updates it by
replacing its live version in a single operation. A valid dbt project must contain `dbt_project.yml` and one of the supported profile files:

- `dbt_project.yml`: A standard dbt configuration file that specifies the profile to use.
- [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`: A dbt connection profile definition referenced in `dbt_project.yml`. The selected profile file must define the database, role, schema, and type. If both files are present, Snowflake uses `dbt_projects_profiles.yml` and ignores `profiles.yml` during deployment, compilation, and subsequent commands.

  - By default, dbt Projects on Snowflake uses your target schema (`target.schema`) specified from your dbt environment or profile. When you execute a dbt project object, dbt attempts to create the target schema specified in `dbt_projects_profiles.yml` or `profiles.yml` if it doesn’t already exist. For more information, see [Understand schema generation and customization](/user-guide/data-engineering/dbt-projects-on-snowflake-schema-customization).

  Copy code

  ```
  <profile_name>:
    target: dev
    outputs:
      dev:
        database: <database_name>
        role: <role_name>
        schema: <schema_name>
        warehouse: <warehouse_name>
        type: snowflake
  ```

The following examples illustrate how to use the `snow dbt deploy` command:

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

- Deploy a dbt project object named `jaffle_shop`:

  Copy code

  ```
  snow dbt deploy jaffle_shop
  ```
- Deploy a project named `jaffle_shop` from a specified directory, using a profile file from a separate directory. The CLI looks for `dbt_projects_profiles.yml` first and uses `profiles.yml` only if `dbt_projects_profiles.yml` isn’t present. The CLI copies the file into the root of the deployed project object with the same filename, overwriting a file with the same name in this location:

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory --profiles-dir ~/my_profiles/
  ```
- Deploy a project named `jaffle_shop` from a specified directory, supplying a profile file from outside the project, setting a default target, pinning a dbt version, and enabling [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access):

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory \
    --profiles-dir ~/my_profiles/ \
    --default-target prod \
    --dbt-version 1.11.11 \
    --external-access-integration dbthub-integration \
    --external-access-integration github-integration
  ```
- Deploy a project named `jaffle_shop` and set a specific dbt runtime version:

  Copy code

  ```
  snow dbt deploy jaffle_shop --dbt-version '1.11.11'
  ```
- Deploy a project named `jaffle_shop`, pull in an `env.yml` file from a separate directory, and set the default environment for compilation and later executions:

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory \
    --env-file-dir /path/to/env/directory \
    --default-env prod
  ```

  The `--env-file-dir` flag points the CLI at an `env.yml` file elsewhere in your repo (similar to `--profiles-dir`) and pulls it into the deployed object, overwriting the object’s root `env.yml` if one already exists. The `--default-env` flag sets the environment used for compilation and subsequent executions. These flags require Snowflake CLI 3.21 or later. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Listing all available dbt project objects

The [snow dbt list](/developer-guide/snowflake-cli/command-reference/dbt-commands/list) command lists all available dbt project objects on Snowflake.

The following examples illustrate how to use the `snow dbt list` command:

- List all available dbt project objects:

  Copy code

  ```
  snow dbt list
  ```
- List dbt project objects in the `product` database whose names begin with `JAFFLE`:

  Copy code

  ```
  snow dbt list --like JAFFLE% --in database product
  ```

## Executing a dbt project object command

The [snow dbt execute](/developer-guide/snowflake-cli/command-reference/dbt-commands/execute/overview) command executes one of the following [dbt commands](https://docs.getdbt.com/reference/dbt-commands) on a Snowflake dbt project object:

- [build](https://docs.getdbt.com/reference/commands/build)
- [clean](https://docs.getdbt.com/reference/commands/clean)
- [compile](https://docs.getdbt.com/reference/commands/compile)
- [deps](https://docs.getdbt.com/reference/commands/deps)
- [list](https://docs.getdbt.com/reference/commands/list)
- [parse](https://docs.getdbt.com/reference/commands/parse)
- [retry](https://docs.getdbt.com/reference/commands/retry)
- [run](https://docs.getdbt.com/reference/commands/run)
- [run-operation](https://docs.getdbt.com/reference/commands/run-operation)
- [seed](https://docs.getdbt.com/reference/commands/seed)
- [show](https://docs.getdbt.com/reference/commands/show)
- [snapshot](https://docs.getdbt.com/reference/commands/snapshot)
- [source freshness](https://docs.getdbt.com/reference/commands/source)
- [test](https://docs.getdbt.com/reference/commands/test)

For more information about using dbt commands, see the [dbt Command reference](https://docs.getdbt.com/reference/dbt-commands).

The following examples illustrate how to use the `snow dbt execute` command:

- Execute the dbt `test` command:

  Copy code

  ```
  snow dbt execute jaffle_shop test
  ```
- Execute the `run` dbt command asynchronously:

  Copy code

  ```
  snow dbt execute --run-async jaffle_shop run
  ```
- Execute the `run` dbt command with a specific dbt version:

  Copy code

  ```
  snow dbt execute --dbt-version '1.9.4' jaffle_shop run
  ```
- Execute the `run` dbt command against a selected environment, overriding individual variables for this run:

  Copy code

  ```
  snow dbt execute --env staging \
    --env-vars '{"DBT_DATABASE": "tasty_bytes_staging_db"}' jaffle_shop run
  ```

  The `--env` flag selects the environment defined in the project’s `env.yml` file, and `--env-vars` applies inline key/value overrides for this execution. Use `--use-shell-env-vars` to pull `DBT_`-prefixed shell variables (excluding `DBT_ENV_SECRET_*` variables) into the run. These flags require Snowflake CLI 3.21 or later. For more information, see [Use the Snowflake CLI](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables#label-dbt-env-vars-cli).

## Describing a dbt project object

The [snow dbt describe](/developer-guide/snowflake-cli/command-reference/dbt-commands/describe) command describes a dbt project object on Snowflake.

The following example describes the dbt project object named `my_dbt_project` on Snowflake:

Copy code

```
snow dbt describe my_dbt_project
```

## Dropping a dbt project object

The [snow dbt drop](/developer-guide/snowflake-cli/command-reference/dbt-commands/drop) command deletes a dbt project object on Snowflake.

The following example deletes the dbt project object named `my_dbt_project` on Snowflake:

Copy code

```
snow dbt drop my_dbt_project
```

## Copying dbt project files

The [snow dbt copy](/developer-guide/snowflake-cli/command-reference/dbt-commands/copy) command copies files between local directories,
stages, and a dbt project object’s live version. Use `snow dbt execute --import` instead when files only need to be mounted under `./imports`
for one execution.

## Use `snow dbt` commands in a CI/CD workflow

Note

When building CI/CD workflows, you only need your Git server, such as GitHub, and Snowflake CLI. A Git repository object is not required.

You can run dbt commands with Snowflake CLI to test pull requests and update the production dbt project object after changes merge. Choose a workflow based on the amount of the project that CI needs to validate:

- **Basic CI workflow:** Deploy a tester dbt project object and run `dbt build` across the project. Start with [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).
- **Advanced Slim CI:** Deploy with automatic compilation disabled, import dbt artifacts from the last successful production execution, and use state
  selection with defer to process only changed models and their downstream dependencies. For a complete per-pull-request CI workflow, see
  [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

To build a CI/CD workflow with `snow dbt` commands, follow these steps:

1. Prepare your dbt project:

   1. Download your dbt project or start a new one.
      - Ensure that the main project directory contains `dbt_project.yml` and either [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`.
      - Verify that the profile name referenced in `dbt_project.yml` is defined in `dbt_projects_profiles.yml` or `profiles.yml`. If both files are present, Snowflake uses `dbt_projects_profiles.yml`.

        Note

        Ensure that credentials are excluded from the profile file. Leave `account` and `user` as placeholder strings and let your CI/CD platform supply the connection through secrets or environment variables.
2. Set up Snowflake CLI GitHub Action.

   Follow the guidelines for [setting up GitHub Action for Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd) and [verify your connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-test-connection) to Snowflake.
3. Define your workflow.

   The following example illustrates a CI workflow that replaces the live version of the dbt project object named `product_pipeline` in a
   single operation, then builds models and runs tests in DAG order:

   Copy code

   ```
   - name: Execute Snowflake CLI command
     run: |
       snow dbt deploy product_pipeline
       snow dbt execute product_pipeline build
   ```
