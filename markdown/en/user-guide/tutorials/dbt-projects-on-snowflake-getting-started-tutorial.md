# Tutorial: Get started with dbt Projects on Snowflake

## Introduction

This tutorial guides you through creating a workspace for [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake) that is connected to a GitHub repository that you fork from our [getting-started-with-dbt-on-snowflake repository](https://github.com/Snowflake-Labs/getting-started-with-dbt-on-snowflake) in Snowflake Labs. You then use the workspace to update dbt project files, and test and run the dbt project, which materializes the data model output of the dbt project in target Snowflake databases and schemas. You deploy the project to create a dbt project object on Snowflake. Finally, you set up a task to execute the project on a schedule that you define.

If you would like to get started with running an existing dbt Core project on dbt Projects on Snowflake, see [Migrate from dbt Core to dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-migrate-from-dbt-core).

Note

GitHub isn’t a requirement of dbt Projects on Snowflake. Snowflake connects to any Git platform listed in [Using a Git repository in Snowflake](/developer-guide/git/git-overview),
including GitLab, Bitbucket, and Azure DevOps. This tutorial uses GitHub only because the sample project is hosted there.

To follow the tutorial with another provider, import the sample repository into your own GitLab, Azure DevOps, or Bitbucket repository, and then
use your own repository URL in the setup steps. For provider-specific API integration examples, see
[Step 3: Connect your Git repository with OAuth2](/user-guide/data-engineering/dbt-projects-on-snowflake-migrate-from-dbt-core#label-dbt-migrate-step3).

### Prerequisites

- **Git provider**

  - An account with a [supported Git platform](/developer-guide/git/git-overview) that can create a repository and manage access to that repository. The steps in this tutorial use GitHub.
  - Git on the command line. For more information about installation, see [Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git).
- **Snowflake**

  - A Snowflake account and user with privileges as described in [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).
  - Privileges to create and edit the following objects or access to an administrator who can create each of them on your behalf:
    - An API integration
    - If your repository is private, a secret
    - A network rule
    - (Optional) An external access integration that references the network rule (a one-time admin setup, followed by a `USAGE` grant on the integration to the role that runs dbt)
    - Your user object

## Set up your environment

Complete the following steps to set up your environment for this tutorial:

1. [Fork and clone the dbt Projects on Snowflake getting started repository](#label-dbt-get-started-fork-and-clone)
2. [(Optional) Create a warehouse for executing workspace actions](#label-dbt-get-started-create-warehouse)
3. [Create a database and schema for integrations and model materializations](#label-dbt-get-started-create-database-and-schema)
4. [Create an API integration in Snowflake for connecting to GitHub](#label-dbt-get-started-create-api-integration)
5. [(Optional) Create an external access integration in Snowflake for dbt dependencies](#label-dbt-get-started-create-external-access-integration)

### Fork and clone the dbt Projects on Snowflake getting started repository

1. Go to <https://github.com/Snowflake-Labs/getting-started-with-dbt-on-snowflake>, select the down arrow next to **Fork**, and then select **Create a new fork**.
2. Specify the owner and name of your forked repository and other details. Later in the tutorial, we use the following URL to represent your forked repository:

   Copy code

   ```
   https://github.com/my-github-account/getting-started-with-dbt-on-snowflake.git
   ```

### (Optional) Create a warehouse for executing workspace actions

A dedicated warehouse assigned to your workspace can help you log, trace, and identify actions initiated from within that workspace. In this tutorial, we use a warehouse named TASTY\_BYTES\_DBT\_WH. Alternatively, you can use an existing warehouse in your account. For more information about creating a warehouse, see [Creating a warehouse](/user-guide/warehouses-tasks#label-warehouse-create).

The Tasty Bytes data model that you create for source data is fairly large, so we recommend using an XL warehouse for that one-time setup. Snowflake warehouses bill for the time they are running, including idle time before auto-suspend. After you finish creating the source data, you can resize the warehouse to SMALL for compiling, running, and scheduling the dbt project.

To create a warehouse, run the following SQL command:

Copy code

```
CREATE WAREHOUSE tasty_bytes_dbt_wh WAREHOUSE_SIZE = XLARGE AUTO_SUSPEND = 60;
```

### Create a database and schema for integrations and model materializations

This tutorial uses a database named TASTY\_BYTES\_DBT\_DB. Within that database, you create a schema named INTEGRATIONS to store the objects that Snowflake needs for GitHub integration. You create schemas named DEV and PROD to store materialized objects that your dbt project creates.

To create the database and schemas, run the following SQL commands:

Copy code

```
CREATE DATABASE tasty_bytes_dbt_db;
CREATE SCHEMA tasty_bytes_dbt_db.dev;
CREATE SCHEMA tasty_bytes_dbt_db.prod;
CREATE SCHEMA tasty_bytes_dbt_db.integrations;
```

### Create an API integration in Snowflake for connecting to GitHub

Snowflake needs an API integration to interact with GitHub.

If your repository is private, you must also create a secret in Snowflake to store GitHub credentials for your repository. You then specify the secret in the API integration definition as one of the ALLOWED\_AUTHENTICATION\_SECRETS. You also specify this secret when you create the workspace for your dbt project later in this tutorial.

Creating a secret requires a personal access token for your repository. For more information about creating a token, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in GitHub documentation.

This tutorial uses a secret named TB\_DBT\_GIT\_SECRET. For more information about creating a secret, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

To create a secret for GitHub, run the following SQL commands:

Copy code

```
USE tasty_bytes_dbt_db.integrations;
CREATE OR REPLACE SECRET tasty_bytes_dbt_db.integrations.tb_dbt_git_secret
  TYPE = password
  USERNAME = 'your-gh-username'
  PASSWORD = 'YOUR_PERSONAL_ACCESS_TOKEN';
```

To create an API integration for GitHub that uses the secret you just created, run the following SQL command. Replace `https://github.com/my-github-account` with the HTTPS URL of the GitHub account for your forked repository:

Copy code

```
CREATE OR REPLACE API INTEGRATION tb_dbt_git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/my-github-account')
  -- Comment out the following line if your forked repository is public
  ALLOWED_AUTHENTICATION_SECRETS = (tasty_bytes_dbt_db.integrations.tb_dbt_git_secret)
  ENABLED = TRUE;
```

### (Optional) Create an external access integration in Snowflake for dbt dependencies

When you run dbt commands in a workspace, dbt might need to access remote URLs to download dependencies. For example, dbt might need to download packages from the dbt Package hub or from GitHub.

Most dbt projects specify dependencies in their `packages.yml` file. You must install these dependencies in the dbt project workspace. You can’t update a deployed dbt project object with dependencies.

To get dependency files from remote URLs, Snowflake needs an external access integration that relies on a network rule. Creating the network rule and external access integration is a **one-time admin operation**. After that, an admin grants `USAGE` on the integration to the role that runs dbt (for example, a data engineering role), and engineers select the integration when they run `dbt deps` without ever recreating it.

For more information about external access integrations in Snowflake, see [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

To create a network rule and an external access integration, and to grant `USAGE` to a data engineering role, run the following SQL commands as an admin:

Copy code

```
-- Create NETWORK RULE for external access integration

CREATE OR REPLACE NETWORK RULE dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  -- Minimal URL allowlist that is required for dbt deps
  VALUE_LIST = (
    'hub.getdbt.com',
    'codeload.github.com'
    );

-- Create EXTERNAL ACCESS INTEGRATION for dbt access to external dbt package locations

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ENABLED = TRUE;

-- Grant USAGE so the role that runs dbt can select and use the integration
GRANT USAGE ON INTEGRATION dbt_ext_access TO ROLE data_engineer;
```

If you run this tutorial with a role other than `data_engineer`, replace that role name with yours, or grant `USAGE` to the role you use in Workspaces.

## Create a workspace connected to your Git repository

In this step, you create a workspace in Snowsight that is connected to your GitHub repository. For more information about workspaces, see [Workspaces](/user-guide/ui-snowsight/workspaces).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. From the Workspaces list above the workspace files area, under **Create Workspace**, select **From Git repository**. (The Workspaces list has a default selection of **My Workspace**.)
4. For **Repository URL**, enter the HTTPS URL of your forked GitHub repository; for example, *<https://github.com/my-github-account/getting-started-with-dbt-on-snowflake.git>*
5. For **Workspace name**, enter a name. Later in this tutorial, we use *tasty\_bytes\_dbt*.
6. Under **API integration**, select the name of the API integration that you created earlier; for example, *TB\_DBT\_GIT\_API\_INTEGRATION*.
7. If your GitHub repository is public, select **Public repository**, and then select **Create**.

   Note

   Workspaces don’t support committing and pushing changes from a workspace to a public repository.
8. If your GitHub repository is private, and you created a secret for your API integration during setup, do the following:

   1. Select **Personal access token**.
   2. Under **Credentials secret**, select **Select database and schema**.
   3. Select the database from the list (for example, **TASTY\_BYTES\_DBT\_DB**), and then select the schema from the list (for example, **INTEGRATIONS**) where you stored the API integration.
   4. Select **Select secret**, and then select your secret from the list; for example, **tb\_dbt\_git\_secret**.
9. Select **Create**.

   Snowflake connects to the GitHub repository that you specified and opens your new workspace. A single folder in the workspace named `tasty_bytes_dbt_demo` contains the dbt project that you will work with.

### Verify the contents of the profiles.yml file in your dbt project root

Each dbt project folder in your Snowflake workspace must contain a `dbt_projects_profiles.yml` or `profiles.yml` file that specifies a target `warehouse`, `database`, `schema`, and `role` in Snowflake for the project. The `type` must be set to `snowflake`. dbt requires an `account` and `user`, but these can be left with an empty or arbitrary string because the dbt project runs in Snowflake under the current account and user context.

This tutorial uses `profiles.yml`. Alternatively, hybrid teams can use [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file), which takes precedence if both files are present.

When you run dbt commands, your workspace reads `dbt_projects_profiles.yml` if it’s present. Otherwise, it reads `profiles.yml`. Each target is listed in the **Profile** dropdown. When you run a dbt command, the workspace uses the selected profile (`target`) to run the command.

Open the `tasty_bytes_dbt_demo/profiles.yml` file, and then verify that your contents match the following example. If you specified different database or warehouse names earlier, replace them with your own.

Copy code

```
tasty_bytes:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: 'not needed'
      user: 'not needed'
      role: accountadmin
      database: tasty_bytes_dbt_db
      schema: dev
      warehouse: tasty_bytes_dbt_wh
      threads: 8
    prod:
      type: snowflake
      account: 'not needed'
      user: 'not needed'
      role: accountadmin
      database: tasty_bytes_dbt_db
      schema: prod
      warehouse: tasty_bytes_dbt_wh
      threads: 8
```

## Run the SQL commands in tasty\_bytes\_setup.sql to set up source data

As source data for its transformations, the dbt project in your repository uses the foundational data model for the fictitious Tasty Bytes food truck brand. The SQL script to create the data model is in the workspace.

1. In your workspace, navigate to the `tasty_bytes_dbt_demo/setup/tasty_bytes_setup.sql` file, and then open it.
2. From the context selector in the upper right of the workspace editor, select the warehouse you created earlier; for example, **TASTY\_BYTES\_DBT\_WH**.
3. The SQL file contains commands that you already ran in this tutorial. Near the beginning of the file, find the following commands, and then comment them out so that you don’t run them again and create duplicate resources:

   Copy code

   ```
   CREATE OR REPLACE WAREHOUSE ...;
   CREATE OR REPLACE API INTEGRATION ...;
   CREATE OR REPLACE NETWORK RULE ...;
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION ...;
   ```
4. Run the uncommented SQL commands in the file.

   Tip

   Use `cmd` + `Shift` + `Enter` to run all uncommented commands.

   The **Output** tab displays the following message:

   `tasty_bytes_dbt_db setup is now complete`
5. After the source data is created, resize the warehouse to SMALL:

   Copy code

   ```
   ALTER WAREHOUSE tasty_bytes_dbt_wh SET WAREHOUSE_SIZE = SMALL;
   ```

### Enable logging, tracing, and metrics

You can capture logging and tracing events for a dbt project object and for the task that runs it on a schedule, if applicable. For more information, see [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability).

To enable this feature, you must set logging, tracing, and metrics on the schema where the dbt project object and task are deployed.

The following commands in the `tasty_bytes_setup.sql` file enable logging, tracing, and metrics for the DEV and PROD schemas in the TASTY\_BYTES\_DBT\_DB database. You ran these in the previous step. They are shown here for reference so that you can enable logging, tracing, and metrics for your own projects.

Copy code

```
ALTER SCHEMA tasty_bytes_dbt_db.dev SET LOG_LEVEL = 'INFO';
ALTER SCHEMA tasty_bytes_dbt_db.dev SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA tasty_bytes_dbt_db.dev SET METRIC_LEVEL = 'ALL';

ALTER SCHEMA tasty_bytes_dbt_db.prod SET LOG_LEVEL = 'INFO';
ALTER SCHEMA tasty_bytes_dbt_db.prod SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA tasty_bytes_dbt_db.prod SET METRIC_LEVEL = 'ALL';
```

## (Optional) Execute the dbt deps command for your project

You can use the workspace to execute common dbt commands for a project. For a list of available commands, see [Supported dbt commands and flags](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands). To run a command, you select the dbt **Project**, **Profile**, and dbt command from the lists above the workspace editor. You then select the execute button. Use the down arrow next to the execute button to specify additional arguments that the dbt command supports.

When you execute any dbt command within the workspace, the **Output** tab shows the command that executes on Snowflake (in green) and the stdout for that command so that you can monitor command success or failure.

The first command you must execute for any dbt project is `deps`, which updates the dependencies for your project specified in your project’s `packages.yml` file. Other commands will fail unless you have updated dependencies. For more information, see [Limitations, requirements, and considerations for dbt dependencies](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies#label-dbt-requirements-deps).

1. In the workspace, open `tasty_bytes_dbt_demo/packages.yml`. This file contains a `packages:` block that’s commented out by default. Uncomment the block before continuing.
2. Below the workspace editor, open the **Output** tab so that you can see stdout after you run dbt commands from the workspace.
3. From the menu bar above the workspace editor, confirm that the default **Project** (**tasty\_bytes\_dbt\_demo**) is selected. You can have any **Profile** selected. This project has the profiles `dev` and `prod` defined in the `profiles.yml` file.
4. From the command list, select **Deps**.
5. Next to the execute button, select the down arrow.
6. In the dbt Deps window, do the following:

   - Select **Run with defaults**.
   - Enter the name of the **External Access Integration** you created during setup in the space provided; for example, *dbt\_ext\_access*.
7. To run the command, select **Deps**.

   The **Output** tab displays the SQL command that runs on Snowflake, which is similar to the following:

   Copy code

   ```
   execute dbt project from workspace "USER$"."PUBLIC"."tasty_bytes_dbt" project_root='tasty_bytes_dbt_demo' args='deps --target dev' external_access_integrations = (dbt_ext_access)
   ```

   When the command finishes, stdout messages appear that are similar to the following:

   ```
   14:47:19  Running with dbt=1.8.9
   14:47:19  Updating lock file in file path: /tmp/dbt/package-lock.yml
   14:47:19  Installing dbt-labs/dbt_utils
   14:47:19  Installed from version 1.3.0
   14:47:19  Up to date!
   Uploading /tmp/dbt/package-lock.yml to snow://workspace/USER$ADMIN.PUBLIC."tasty_bytes_dbt"/versions/live/dbt//package-lock.yml
   ```

   The `package_lock.yml` file is created and appears in your list of workspace files with an **A** next to it. This indicates that the file was added in the workspace for your dbt project, with contents that are similar to the following example:

   Copy code

   ```
   packages:
     - package: dbt-labs/dbt_utils
    version: 1.3.0
   ```

## Compile the dbt project, view the DAG, and view compiled SQL

Compiling a project in dbt creates executable SQL from modeled SQL files and a visual representation of the directed acyclic graph (DAG) for the project in the workspace. For more information about dbt project compilation, see [compile](https://docs.getdbt.com/reference/commands/compile) in dbt documentation.

After you compile the project in the workspace, you can view the DAG. You also can open any SQL file in the `models` folder to see the model SQL and the compiled SQL in side-by-side tabs.

1. Select the project and target that you want to compile.
2. From the command list, select **Compile**, and then select the execute button (optionally, you can select the down arrow and specify compile command arguments).
3. In the area below the workspace editor, select the **DAG** tab.

   You can use the DAG pane to visualize your dbt project transformations from source files to materialized data model objects in Snowflake.

   - Click and drag anywhere in the pane to pan the view.
   - Use the **+** and **–** buttons to zoom in and out.
4. To view the contents of an object’s source file in the editor, select a tile for any object.
5. To see compiled SQL in a split-pane view in the workspace editor:

   1. In the DAG, select the tile for a dbt SQL model file; for example, **orders**.

      –OR–

      From the workspace file listing, select any file in the `models` subdirectory of your dbt project to open it in the workspace editor.
   2. Choose **View Compiled SQL** in the upper-right of the workspace editor to see the compiled SQL in a split-pane view.

## Run the dbt dev project and verify the materialized Snowflake objects

Executing the dbt `run` command executes your compiled SQL against the target database and schema using the Snowflake warehouse and role that are specified in the `profiles.yml` file of the project. In this step, you’ll materialize the output of the `Dev` target in your dbt demo project. You then create a SQL worksheet named `dbt_sandbox.sql` in the workspace where you can run SQL to verify object creation.

Important

Choosing the dbt **Run** or **Build** command for a project from within a workspace materializes target output using the `role` defined in the project’s [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file. Both the user and the role specified must have the required privileges to use the `warehouse`, perform operations on the `database` and `schema` that are specified in the profile file, and perform operations on any other Snowflake objects that the dbt model specifies. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

1. From the **Profile** list, select **Dev**.
2. From the command list, select **Run**, and then select the execute button.

   The output pane shows the completion status of the run.
3. In your **tasty\_bytes\_dbt\_demo** project, navigate to the `examples` folder, select the **+** next to the folder name, and then select **SQL File**.
4. Enter *dbt\_sandbox.sql*, and then press `Enter`.
5. In the workspace tab for `dbt_sandbox.sql`, run the following query:

   Copy code

   ```
   SHOW TABLES IN DATABASE tasty_bytes_dbt_db;
   ```

   In the **Status and Results** pane, you should see the tables CUSTOMER\_LOYALTY\_METRICS, ORDERS, and SALES\_METRICS\_BY\_LOCATION.
6. To see the views that your dbt project run created, run the following command:

   Copy code

   ```
   SHOW VIEWS IN DATABASE tasty_bytes_dbt_db;
   ```

## Push your file updates from the workspace to your repository

Now that you have updated your workspace and compiled, tested, run, and deployed your project as a dbt project object, you can push the changes you made in the workspace to your private GitHub repository. This step isn’t supported for public repositories.

1. With your workspace open, select **Changes**.

   The workspace file listing is filtered to show only files that have changed since you synchronized with the Git repository.

   - **A** indicates a file added in the workspace and not to the Git repository.
   - **M** indicates a modified file.
   - **D** indicates a deleted file.
2. Select a file to view its diff with GitHub since the last pull (in this case, when the workspace was created).
3. On the menu bar above the workspace file listing, verify that the branch selector is set to **main** for this tutorial.
4. Select the **Push** button, and then type a commit message in the box provided; for example, *Updating project with initial changes from dbt on Snowflake*.
5. Select **Push**.

   A push to your repository might take several minutes.

## Deploy the dbt project object from the workspace

Deploying your dbt project from a workspace creates a dbt project object. You can use the object to schedule, execute, and monitor a dbt project object in Snowflake outside of the workspace.

When you deploy your dbt project object from the workspace to a Snowflake database and schema, you can create or overwrite an object that you previously created.

1. On the right side of the workspace editor, select **Connect** » **Deploy dbt project**.
2. Select **Select database and schema**, and then select the **TASTY\_BYTES\_DBT\_DB** database and the **DEV** schema.
3. Under **Select or Create dbt Object**, select **Create dbt Object**.
4. Under **Enter Name**, type *TASTY\_BYTES\_DBT\_PROJECT*, and then select **Deploy**.

   The **Output** tab displays the command that runs on Snowflake, which is similar to the following example:

   Copy code

   ```
   create or replace DBT PROJECT "TASTY_BYTES_DBT_DB"."DEV"."TASTY_BYTES_DBT_PROJECT" from snow://workspace/USER$MYUSER.PUBLIC."tasty_bytes_dbt_demo"/versions/live/dbt

   tasty_bytes_dbt_project successfully created.
   ```

   The Connect menu now displays the name of the dbt project object that you created, with the following options:

   - **Redeploy dbt project** - Updates the dbt project object’s mutable `live` version with the current workspace contents by using ALTER. For more information, see [How dbt project objects get updated](/user-guide/data-engineering/dbt-projects-on-snowflake-understanding-dbt-project-objects#label-dbt-key-concepts-dbt-project-updating).
   - **Disconnect** - Disconnects the workspace from the dbt project object, but doesn’t delete the dbt project object.
   - **View project** - Opens the dbt project object in the object explorer, where you can view the CREATE DBT PROJECT command for the dbt project object and run history for the project.
   - **Create schedule** - Provides options for you to create a task that executes the dbt project object on a schedule. For more information, see [Create a task to schedule dbt project execution](#label-dbt-get-started-create-task).
   - **View schedules** - Opens a list of schedules (tasks) that execute the dbt project object, with the option to view task details in the object explorer.
5. To verify the creation of the project, do one or both of the following tasks:

   - From the menu for the dbt project, select **View project** to open the dbt project object in the object explorer.

     –OR–
   - From the `dbt_sandbox.sql` file worksheet that you created earlier, run the following command:

     Copy code

     ```
     SHOW DBT PROJECTS LIKE 'tasty%';
     ```

## Create a task to schedule dbt project execution

Now that you have deployed your dbt project object, you can use the workspace or SQL to set up a task that executes a dbt command on your dbt project object.

The following steps set up a schedule to execute the dbt project object every 12 hours at one minute after the hour. The task executes the dbt `run` command with the `--select` option to run the `customer_loyalty_metrics` model in the dbt project.

1. From the dbt project menu on the right side of the project pane, choose **Create schedule**.
2. In the **Schedule a dbt run** dialog box, do the following:

   - For **Schedule name**, enter a name for the task; for example, *run\_prepped\_data\_dbt*.
   - For **Frequency**, select **Custom**, and then enter the Cron expression `1 */12 * * *` for your time zone selected.
   - Under **dbt properties**:
     - For **Operation**, select **run**.
     - For **Profile**, select **dev**.
     - For **Additional flags**, enter `--select customer_loyalty_metrics`.
3. Choose **Create**.

   Snowflake creates a task that executes an EXECUTE DBT PROJECT command using these parameters. For more information about tasks and task options, see [Introduction to tasks](/user-guide/tasks-intro) and [CREATE TASK](/sql-reference/sql/create-task).
4. From the dbt project menu, select **View schedules**, and then choose your schedule from the list.

   The object explorer opens to your database with the **Task Details** pane opened for the task. The **Task Definition** shows a [CREATE TASK](/sql-reference/sql/create-task) command similar to the following:

   Copy code

   ```
   CREATE OR REPLACE TASK tasty_bytes_dbt_db.dev.run_prepped_data_dbt
     WAREHOUSE=tasty_bytes_dbt_wh
     SCHEDULE ='USING CRON 1 */12 * * * America/Los_Angeles'
   AS
     EXECUTE DBT PROJECT tasty_bytes_dbt_project ARGS='run --select customer_loyalty_metrics --target dev';
   ```

## Clean up

To minimize credit consumption, you can delete the task, databases, workspaces, and warehouse that you created.

Run the following SQL commands from your `dbt_sandbox.sql` worksheet to suspend and remove the task, and to remove the warehouse, the TASTY\_BYTES\_DBT\_DB and TB\_101 databases that you created, and all schemas and objects created in the databases:

Copy code

```
-- If you want to keep this setup, suspend the task to stop scheduled runs:
ALTER TASK IF EXISTS tasty_bytes_dbt_db.dev.run_prepped_data_dbt SUSPEND;

-- If you want to remove this setup, drop the task, warehouse, and databases:
DROP TASK IF EXISTS tasty_bytes_dbt_db.dev.run_prepped_data_dbt;
DROP WAREHOUSE IF EXISTS tasty_bytes_dbt_wh;
DROP DATABASE IF EXISTS tasty_bytes_dbt_db;
DROP DATABASE IF EXISTS tb_101;
```

**To delete your tasty\_bytes\_dbt\_demo workspace:**

- From the vertical ellipsis menu [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) next to the workspace menu at the top of the workspace explorer, select **Delete**, and then confirm the deletion when you’re prompted.

## What’s next

Now that you’ve seen how dbt Projects on Snowflake works end to end, you’re ready to bring your real project over. [Migrate from dbt Core to dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-migrate-from-dbt-core) walks you through moving an existing dbt Core project (your actual `models/`, `seeds/`, and `packages.yml`) into Snowflake with step-by-step SQL.

You can also continue with the [Tutorial: Set up CI/CD integrations on dbt Projects](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial) to automate full-build validation and deployment. For a Slim CI workflow that uses per-pull-request zero-copy clone databases, follow the [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial), or learn the underlying state and defer concepts in [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).
