# Deploy dbt project objects

In dbt Projects on Snowflake, deploying a dbt project object means copying your dbt project code into Snowflake to create the object or replace its live version in a single operation. You can deploy with the `snow dbt deploy` command in Snowflake CLI, Snowsight, or the `CREATE DBT PROJECT` and `ALTER DBT PROJECT ... DEPLOY` SQL commands.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Deploy a dbt project object using Snowflake CLI

This is the recommended approach for deploying dbt project objects. Use Snowflake CLI in a CI/CD pipeline. For a full walkthrough from setup to deployment,
see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

The [snow dbt deploy](/developer-guide/snowflake-cli/command-reference/dbt-commands/deploy) command uploads local files to a temporary stage
and creates a new dbt project object or updates the live version of an existing object in a single operation. A valid dbt project must contain
`dbt_project.yml` and one of the supported profile files:

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
- Deploy a project named `jaffle_shop` from a specified directory, supplying a profile file in a folder outside the project, setting a default target, pinning a dbt version, and enabling [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access):

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

## Deploy a dbt project object using Snowsight

Deploying a dbt project object in Snowsight takes the dbt code in your workspace and creates a new dbt project object or updates an existing one.

To deploy a dbt project object in Snowsight, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the **Workspaces** menu, select the workspace that contains your dbt project.
4. Optionally, [run the dbt deps command](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies) to pull in project dependencies.
5. Confirm that your dbt files are in place.

   To verify that things work, run the `dbt compile`, `dbt run`, or **dbt build** command, as follows:

   1. Below the workspace editor, open the **Output** tab so that you can see stdout after you run dbt commands from the workspace.
   2. From the menu bar above the workspace editor, confirm that the correct **Project** and **Profile** are selected.
   3. From the command list, select **dbt compile**, `dbt run`, or **dbt build**, then select the execute button. This step parses
      your project.
6. From the top right of your workspace, select **Connect** then select one of the following:

   - **Deploy dbt project** to connect a new dbt project. On first deploy, this creates a schema-level dbt project object.
   - **Existing dbt deployment** to connect to an existing dbt project. Deploying updates the live version of the existing dbt project object
     in a single operation
     (equivalent to `ALTER DBT PROJECT ... DEPLOY FROM 'snow://workspace/.../versions/live'`).
7. In the **Deploy dbt project** popup window, select the following:

   - Under **Select location**, select your database and schema.
   - Under **Select or Create dbt project**, select **Create dbt project**.
   - Enter a name and description.
   - Optionally, enter a default target to choose which profile will be used for compilation and subsequent runs (for example, prod). The
     target of a dbt project object execution can still be overridden with `--target` in `ARGS`.
   - Optionally, select **Run dbt deps**, then select your external access integration to execute `dbt deps` automatically during deployment. Alternatively, you can run `dbt deps` from inside the workspace before deployment to ensure your `dbt_packages` folder is included without any additional steps.
8. Select **Deploy**.

   The **Output** tab displays the command that runs on Snowflake, which is similar to the following example:

   Copy code

   ```
   CREATE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
     FROM 'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live'
     EXTERNAL_ACCESS_INTEGRATIONS = ();
   ```

   ```
   my_dbt_project successfully created.
   ```

   The **Connect** menu now displays the name of the dbt project object that you created, with the following options:

   - **Redeploy dbt project**: Replaces the live version of the dbt project object with the current workspace contents in a single operation by using `ALTER DBT PROJECT ... DEPLOY`. For more information, see [Live version for dbt project objects and files](/user-guide/data-engineering/dbt-projects-on-snowflake-live-version).
   - **Disconnect**: Disconnects the workspace from the dbt project object, but doesn’t delete the dbt project object.
   - **Edit project**: Update the comment, default target, and external access integration for the dbt project object.
   - **View project**: Opens the dbt project object in the object explorer, where you can view the CREATE DBT PROJECT command for the dbt
     project object and run history for the project.
   - **Create schedule**: Provides options for you to create a task that runs the dbt project object on a schedule. For more information,
     see [Schedule execution of dbt project objects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).
   - **View schedules**: Opens a list of schedules (tasks) that run the dbt project object, with the option to view task details in the
     object explorer.
9. Optionally, confirm your dbt project object exists by running the SHOW DBT PROJECTS command in a worksheet, for example:

   Copy code

   ```
   SHOW DBT PROJECTS IN DATABASE mydb;
   ```

## Deploy a dbt project object using SQL commands

The [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project) and [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project) commands copy the files specified in the FROM
clause of the statement to create a dbt project object or update its live version, respectively.

Caution

Deploying directly from a Git repository stage with SQL commands bypasses CI/CD validation. There’s no pull request review and
no tests run before changes reach production. We recommend using these commands for development and testing only. For a
comprehensive guide on deploying to production, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

The CREATE DBT PROJECT command creates a new object with one mutable version named `live`, as shown below.

Copy code

```
CREATE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  FROM '@sales_db.integrations_schema.sales_dbt_git_stage/branches/main'
  DEFAULT_TARGET = 'prod'
  EXTERNAL_ACCESS_INTEGRATIONS = my_dbt_ext_access
  COMMENT = 'Generates sales data models.';
```

The ALTER DBT PROJECT command replaces the full set of files in the live version in a single operation.

Copy code

```
ALTER DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  DEPLOY
  FROM '@sales_db.integrations_schema.sales_dbt_git_stage/branches/main/sales_dbt_project';
```

## Source file locations

The dbt project object source files can be in any one of the following locations:

> - **An internal named stage**, for example:
>
>   `'@my_db.my_schema.my_internal_named_stage/path/to/dbt_projects_or_projects_parent'`
>
>   Internal user stages and table stages aren’t supported.
> - **A dbt workspace**, for example:
>
>   `'snow://workspace/user$.public."my_workspace_name"/versions/live'`
>
>   Workspace URIs use `versions/live`, which refers to the active working state of the workspace. We recommend enclosing the workspace name in double quotes because workspace names are case-sensitive and can contain special characters.
> - **An existing dbt project stage**, for example:
>
>   `'snow://dbt/my_db.my_schema.my_existing_dbt_project_object/versions/live'`
>
>   The version specifier is required and is `live`.
> - **A Git repository stage**, for example:
>
>   `'@my_db.my_schema.my_git_repository_stage/branches/my_branch/path/to/dbt_project_or_projects_parent'`
>
>   For more information about creating and managing a Git repository object and stage, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview) and [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository).
