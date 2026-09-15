# Understand dependencies for dbt Projects on Snowflake

In dbt Projects on Snowflake, dbt dependencies are the packages that you declare in your *packages.yml* file (for example, `dbt-labs/dbt_utils` from the
[Getting started tutorial](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial)). They get installed into a
`dbt_packages` folder when you run `dbt deps`, just like in dbt Core.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

You can execute `dbt deps` in a Snowflake workspace, on your local machine or Git orchestrator before deployment, or against a deployed dbt
project object’s mutable `live` version. When you execute it against a deployed object, use `WRITEBACK = TRUE` to persist installed or updated
packages. For details, see [About executing the dbt deps command](#label-dbt-key-concepts-execute-deps).

## About executing the dbt deps command

You can execute the `dbt deps` command in one of the following ways:

- **In a Snowflake Workspace:** (Recommended for dev environments.) You can execute the `dbt deps` command inside your workspace in
  Snowsight to populate `dbt_packages` before you deploy your dbt Project as a DBT PROJECT object.

  This requires external network access so Snowflake can access the repositories for the dependencies. For more information, see
  [Create an external access integration in Snowflake for dbt dependencies](#label-dbt-key-concepts-external-access-config).
- **Outside Snowflake:** (For example, in the build step of your deployment pipeline.) You can execute the `dbt deps` command on your
  local machine or in your continuous integration (CI), which downloads packages into `dbt_packages`, then deploy the whole project
  (including that folder) into Snowflake.

  This doesn’t require an external network access integration because all dependencies are already included in the dbt project.
- **On a deployed dbt project object:** You can execute the `deps` command against the mutable `live` version. Set `WRITEBACK = TRUE` so that
  the generated `dbt_packages` folder and `package-lock.yml` persist on the live version:

  Copy code

  ```
  EXECUTE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
    ARGS = 'deps'
    WRITEBACK = TRUE;
  ```

  External packages require an external access integration. For more information, see
  [Create an external access integration in Snowflake for dbt dependencies](#label-dbt-key-concepts-external-access-config) and [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

If you’re using the dbt Fusion engine, note that Fusion automatically runs `dbt deps` when `packages.yml` lists dependencies
but no `dbt_packages` folder is present. This happens implicitly during commands like `dbt compile` and `dbt run`. If no
external access integration is configured, this implicit run will fail with a network access error. To resolve this: if
you’re working in a workspace, run `dbt deps` manually first to populate `dbt_packages`. If you’re deploying a project,
set an external access integration on the project object so that `dbt deps` runs automatically during compilation.
For more information, see [Create an external access integration in Snowflake for dbt dependencies](#label-dbt-key-concepts-external-access-config).

## Cross dbt project dependencies

In order to reference another dbt project within your dbt project, the dbt project being referenced must be copied into the root of your dbt
project. Snowflake only supports references in the same folder. For example, `:local: ../some_other_project` isn’t supported.

Although local dependencies don’t require an external access integration, if you need a mix of local packages and remote packages (for example, from dbt Packages hub or Git), you must configure a real external access integration.

Take, for example, the following two dbt projects. You want `core_project` to include `metrics_project` locally so that everything
is self-contained when you deploy to Snowflake (no external access needed).

```
/Projects
├─ core_project/
│   ├─ dbt_project.yml
│   ├─ packages.yml
│   ├─ models/
│   └─ ...
└─ metrics_project/
    ├─ dbt_project.yml
    ├─ models/
    └─ ...
```

- `core_project`: This is your main project (the one that you’ll deploy).
- `metrics_project`: This is the project you want to use as a local dependency.

To reference `metrics_project` inside `core_project`, complete the following steps:

1. Inside of `core_project`, create a folder named `local_packages`. Copy `metrics_project` into this folder.

   Make sure that `metrics_project` has a different name in its `dbt_project.yml` than `core_project`. They must be unique.

   Copy code

   ```
   cd /Projects/core_project
   mkdir local_packages
   cp -R ../metrics_project ./local_packages/metrics_project
   ```

   Now, your layout looks like this:

   ```
   core_project/
     ├─ dbt_project.yml
     ├─ packages.yml
     ├─ models/
     ├─ local_packages/
     │   └─ metrics_project/
     │       ├─ dbt_project.yml
     │       ├─ models/
     │       └─ ...
   ```
2. In `core_project/packages.yml`, declare the local dependency using the relative path.

   Copy code

   ```
   packages:
     - local: local_packages/metrics_project
   ```
3. From inside `core_project`, run `dbt deps`.

   dbt will now treat `metrics_project` as a package and macros from `metrics_project` are available to `core_project`.

## Run dbt deps automatically during deployment

When you deploy or update a dbt project object and give it an external access integration, Snowflake automatically runs `dbt deps`
during deployment (before `dbt compile`) so that dependencies are installed as part of that step. This means you no longer need to include `/dbt_packages`
when deploying projects with external dependencies.

SnowsightSQLSnowflake CLI

When you deploy your dbt project object from the workspace to a Snowflake database and schema, you can create or update an object that
you previously created.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In the **Workspaces** menu, select the workspace that contains your dbt project.
4. On the right side of the workspace editor, select **Connect** » **Deploy dbt project**.
5. In the **Deploy dbt project** popup window, select the following:

   - Under **Select location**, select your database and schema.
   - Under **Select or Create dbt project**, select **Create dbt project**.
   - Enter a name and description.
   - Optionally, enter a default target to choose which profile will be used for compilation and subsequent runs (for example, prod). The
     target of a dbt project object execution can still be overridden with `--target` in `ARGS`.
   - Optionally, select **Run dbt deps**, then select your external access integration to execute `dbt deps` automatically during
     deployment.
6. Select **Deploy**.

The **Output** tab displays the command that runs on Snowflake, which is similar to the following example:

Copy code

```
CREATE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  FROM 'snow://workspace/user$.public."my_workspace_name"/versions/live'
  DEFAULT_TARGET = 'prod'
  EXTERNAL_ACCESS_INTEGRATIONS = (my_dbt_ext_access);
```

```
my_dbt_project successfully created.
```

The **Connect** menu now displays the name of the dbt project object that you created, with the following options:

- **Redeploy dbt project**: Updates the dbt project object with the current workspace version of the project by using
  `ALTER DBT PROJECT ... DEPLOY`. This
  replaces the object’s mutable `live` version in a single operation. For more information, see
  [How dbt project objects get updated](/user-guide/data-engineering/dbt-projects-on-snowflake-understanding-dbt-project-objects#label-dbt-key-concepts-dbt-project-updating).
- **Disconnect**: Disconnects the workspace from the dbt project object, but doesn’t delete the dbt project object.
- **Edit project**: Update the comment, default target, and external access integration for the dbt project object.
- **View project**: Opens the dbt project object in the object explorer, where you can view the CREATE DBT PROJECT command for the dbt
  project object and run history for the project.
- **Create schedule**: Provides options for you to create a task that runs the dbt project object on a schedule. For more information,
  see [Schedule execution of dbt project objects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).
- **View schedules**: Opens a list of schedules (tasks) that run the dbt project object, with the option to view task details in the
  object explorer.

To automatically run `dbt deps` during deployment, run the CREATE DBT PROJECT or ALTER DBT PROJECT command with the
EXTERNAL\_ACCESS\_INTEGRATIONS parameter, as shown in the following example.

With `AUTO_COMPILE = TRUE`, Snowflake runs `dbt compile` during deployment. If an external access integration is configured, Snowflake first
runs `dbt deps`, then `dbt compile`. Setting `AUTO_COMPILE = FALSE` skips both commands.

You can pass an empty array into the EXTERNAL\_ACCESS\_INTEGRATIONS parameter or you can specify one or more external access integrations,
depending on your use case. Local dependencies don’t require an external access integration, but if you need a mix of local packages and
remote packages (for example, from dbt Packages hub or Git), you must configure a real external access integration.

Copy code

```
-- Create a dbt project object that runs dbt deps during deployment for remote packages
CREATE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  FROM 'snow://workspace/user$.public."my_workspace_name"/versions/live'
  EXTERNAL_ACCESS_INTEGRATIONS = (my_dbt_ext_access);

-- Create a dbt project object that runs dbt deps during deployment for only local dependencies
CREATE DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  FROM 'snow://workspace/user$.public."my_workspace_name"/versions/live'
  EXTERNAL_ACCESS_INTEGRATIONS = ();
```

Copy code

```
-- Update the Git repository object to fetch the latest code
ALTER GIT REPOSITORY mydb.dev_schema.my_dbt_git_stage FETCH;

-- Set external access integrations
ALTER DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  SET EXTERNAL_ACCESS_INTEGRATIONS = (my_dbt_ext_access);

-- Deploy the updated Git repository files to the live version
-- After an external access integration is set, deployment runs dbt deps, then dbt compile
ALTER DBT PROJECT mydb.my_dbt_projects_schema.my_dbt_project
  DEPLOY FROM '@mydb.dev_schema.my_dbt_git_stage/branches/main/sales_dbt_project';
```

To automatically run `dbt deps` during deployment, run the [snow dbt deploy](/developer-guide/snowflake-cli/command-reference/dbt-commands/deploy)
command with either the `--external-access-integration` or `--install-local-deps` flag, as shown in the following example.

By default, Snowflake runs `dbt compile` during deployment. If an external access integration is configured, Snowflake first runs `dbt deps`,
then `dbt compile`. Pass `--no-auto-compile` to skip both commands.

The `--install-local-deps` flag creates an object that has an empty external access integration. During deployment, it runs
`dbt deps` and replaces the previous state of the `dbt_packages` folder.

The `--external-access-integration` flag adds an external access integration, which takes precedence over the
`--install-local-deps` flag.

Copy code

```
snow dbt deploy my_dbt_project --install-local-deps;
```

## Create an external access integration in Snowflake for dbt dependencies

When you run dbt commands in a workspace, dbt might need to access remote URLs to download dependencies. For example, dbt might need to
download packages from the dbt Package hub or from GitHub.

Most dbt projects specify dependencies in their `packages.yml` file. You can install those dependencies in a workspace, locally, or in CI
before you deploy.

To get dbt packages from remote URLs, Snowflake needs an external access integration that relies on a network rule, as shown in the
following example. Creating the network rule and external access integration is a **one-time admin
operation**. After that, grant `USAGE` on the integration to the roles that run dbt. Engineers can
then select it whenever they need it.

Copy code

```
-- Create NETWORK RULE for external access integration

CREATE OR REPLACE NETWORK RULE my_dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  -- Minimal URL allowlist that is required for dbt deps
  VALUE_LIST = (
    'hub.getdbt.com',
    'codeload.github.com'
    );

-- Create EXTERNAL ACCESS INTEGRATION for dbt access to external dbt package locations

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_dbt_ext_access
  ALLOWED_NETWORK_RULES = (my_dbt_network_rule)
  ENABLED = TRUE;

-- Grant USAGE so data engineers can select and use the integration
GRANT USAGE ON INTEGRATION my_dbt_ext_access TO ROLE data_engineer;
```

For more information about external access integrations in Snowflake, see [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

## Limitations, requirements, and considerations for dbt dependencies

The following requirements, considerations, and limitations apply to dbt dependencies for dbt projects in dbt Projects on Snowflake:

- You can specify public [Git packages](https://docs.getdbt.com/docs/build/packages#git-packages) in the `packages.yml` file. As a best practice, Snowflake recommends using private Git packages
  only if they are stored securely. We don’t recommend embedding unencrypted Git tokens. To authenticate private Git packages securely, store the token in a Snowflake secret and reference it from an `env.yml` file as a `DBT_ENV_SECRET_` variable. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).
- A network rule and external access integration are required to allow Snowflake to access the repositories for the dependencies. For more
  information, see [Create an external access integration in Snowflake for dbt dependencies](#label-dbt-key-concepts-external-access-config).
- With `AUTO_COMPILE = TRUE`, Snowflake runs `dbt compile` during deployment. If an external access integration is configured, Snowflake first
  runs `dbt deps`, then `dbt compile`. During automatic compilation, the generated `dbt_packages` folder, `package-lock.yml`, and compiled
  artifacts persist to the live version regardless of the `WRITEBACK` setting. On a later `deps` execution, `WRITEBACK` controls whether the
  updated dependency files persist to the live version.
- Snowflake only supports referencing another dbt project in the same folder. For example, `:local: ../some_other_project` isn’t
  supported. For a workaround, see [Cross dbt project dependencies](#label-dbt-key-concepts-cross-project-deps).
- **dbt Fusion and implicit `dbt deps`:** When using the dbt Fusion engine, if `packages.yml` lists dependencies but no `dbt_packages` folder exists, Fusion automatically runs `dbt deps`
  during commands like `dbt compile` or `dbt run`. This is why Snowflake surfaces an external access integration option for
  every dbt command. If you receive an unexpected network access error: in a workspace, run `dbt deps` manually first to
  pre-populate `dbt_packages`. When deploying, set an external access integration on the project object so that
  `dbt deps` runs automatically during compilation.
