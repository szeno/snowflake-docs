# Deploy and manage DCM Projects

This topic describes how to create and deploy DCM Projects to manage Snowflake environments, including accounts.

Managing a DCM project involves the following steps:

1. [Prepare](#label-dcm-projects-prepare) your Snowflake account for a DCM project.
2. [Define](#label-dcm-projects-define) project configuration and objects in project files.
3. [Create](#label-dcm-projects-create-object) a DCM Projects object.
4. [Plan](#label-dcm-projects-plan) to preview proposed changes before deployment.
5. [Deploy](#label-dcm-projects-deploy) the project.
6. [Maintain](#label-dcm-projects-manage) the project by monitoring, updating, and repeating the process as needed.

You can continuously deploy incremental changes to your project as well as large-scale account infrastructure changes.

## Prepare for a DCM project

To get started with DCM Projects, your Snowflake account must satisfy the following prerequisites:

- A database and schema where you can create your DCM Projects object
- A role with privileges to create a DCM Projects object and access to run queries on a warehouse
- For Snowflake CLI, a role with privileges to create a temporary stage

This section describes the tasks that you need to complete to prepare for DCM Projects:

- [Install interfaces to use with DCM Projects](#label-dcm-projects-interface-tools) if you want to use Snowflake CLI or Cortex CLI.
- [Configure Git integration](#label-dcm-projects-git-integration) (recommended but not mandatory)

### Interface tools

You have the following interface options available for DCM Projects.

| Interface tool | Best for |
| --- | --- |
| **Snowsight**  A workspace in Snowsight is a Snowflake native cloud IDE in your account. | - Easily create or upload DCM definition files via the UI. - Connect to a Git repository to pull and push changes. - Review, edit, and debug definition files. - Execute DCM PLAN and DEPLOY commands using the workspace UI. - Browse the database catalog to see DCM project objects and their configuration, managed objects and deployment history. - Select a target profile to automatically use the linked DCM project and templating configuration. |
| **Local IDE** with **Snowflake CLI**  The most familiar and personalized interface for software engineers. | - Create and edit definition files locally. - Connect to a Git repository to pull and push changes. - Concise Snowflake CLI commands with directory context and optional flags. - Rich formatted output and an option to save as a `.json` file. - Option to leverage Cortex Code CLI for agentic or assisted development. - See [Snowflake CLI for DCM Projects](#label-dcm-projects-snowflake-cli) for information about installing and running Snowflake CLI in your local IDE. |
| **Cortex Code**  An agentic AI tool for Snowflake. See [Cortex Code for DCM Projects](#label-dcm-projects-cortex-code) for more information. | - AI assisted or agentic authoring of local definition files. - AI assisted or agentic code validation and debugging by running static analysis and DCM PLAN commands. |
| **SQL commands** | - Run SQL commands from the Snowflake CLI REPL, workspaces, notebooks, or worksheets. - Customize commands with additional arguments. - Same commands work across all Snowflake SQL interfaces. |

Expand

Show lessSee more

The following diagram shows how these interfaces fit into a typical development-to-production workflow.

![DCM interfaces across the development-to-production workflow](/static/images/dcm-projects/dcm_interfaces_workflow.png)

#### Cortex Code for DCM Projects

Cortex Code is an agentic AI tool for Snowflake. With the DCM skill enabled, Cortex Code can autonomously create, migrate, debug, and
deploy DCM Projects. It can also work alongside you step by step. The DCM skill is available in any Cortex Code environment, including
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight),
the [Snowflake extension for VS Code](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc), and
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop).

The Cortex Code DCM skill enables the following:

- Scaffold a new DCM project from scratch, including the manifest file, the folder structure, and definition files.
- Author and edit DEFINE statements, Jinja templates, and macros.
- Run PLAN, DEPLOY, TEST, and PREVIEW commands.
- Interpret plan output, diagnose failures, and suggest fixes.
- Download and inspect deployment artifacts.
- Navigate and explain an existing DCM project.

To get started with the Cortex Code DCM skill, use one of the following options:

- **Snowsight Workspaces**: Open Cortex Code in the Workspaces sidebar while editing your project files, as described in
  [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight).
- **Cortex Code CLI**: Install Cortex Code CLI as described in [Installing Cortex Code](/user-guide/cortex-code/cortex-code-cli),
  then start Cortex Code in your terminal.
- **VS Code extension**: Use the [Snowflake extension for VS Code](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc)
  to work with Cortex Code directly from your editor.
- **Cortex Code Desktop**: Run Cortex Code as a standalone desktop application connected to your Snowflake account. See
  [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop).

In any of these interfaces, use the `$dcm` skill reference or the term `DCM` in your natural language prompt.

For example:

- “Create a new DCM project for our analytics pipeline”
- “Plan my project against the PROD target”
- “Why did my last plan fail?”
- “Add a new dynamic table definition for customer spending”

#### Snowflake CLI for DCM Projects

Snowflake CLI is a command-line interface for Snowflake. It is a tool that you can use to interact with your Snowflake account from your local
IDE.

1. DCM Projects require Snowflake CLI version 3.16 or higher. Install or upgrade Snowflake CLI as described in [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
2. Configure your connection to your Snowflake account, as described in [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect). Confirm you have a working connection:

   Copy code

   ```
   snow connection test
   ```
3. Navigate to the local directory of your Git repository clone. For example:

   Copy code

   ```
   cd ./Quickstarts/DCM_Quickstart_1
   ```
4. See the Snowflake CLI DCM commands available to you:

   Copy code

   ```
   snow dcm --help
   ```

### Git integration

Connect to the Git repository where your DCM project definition files are stored.

SnowsightLocal IDE

1. [Create a new workspace from a Git repository](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace).
2. Create or select a Git branch for your planned changes.

   Snowflake clones files from that branch into your workspace editor.
3. Navigate to the folder where you have your DCM project definition files or want to create them.

1. [Install Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation).

   The [Snowflake extension](https://docs.snowflake.com/en/user-guide/vscode-ext) for VS Code is not needed here, but can be helpful.
2. [Connect to Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/connect).
3. Connect to your Git repository.

   1. Connect your local IDE to your remote Git repository.
   2. Create or select a branch for your planned changes.
   3. Clone that branch to your local disk.
   4. Navigate to the folder where you have your DCM Projects definition files or want to create them.

## Create a DCM project

### Required roles and privileges

The role of the user who creates a DCM project object must have the following roles and privileges:

- The CREATE DCM PROJECT ON SCHEMA privilege:

  Copy code

  ```
  GRANT CREATE DCM PROJECT ON SCHEMA <schema_name> TO ROLE <role_name>;
  ```

### Create a DCM project

Create a DCM project object by using one of the following options.

SQLSnowflake CLISnowsight

Copy code

```
CREATE [OR REPLACE] DCM PROJECT [IF NOT EXISTS] <my_project>
[COMMENT = 'my comment'];
```

Copy code

```
snow dcm create <my_project> --if-not-exists
```

To create a project for a non-default target, use one of the following commands:

Copy code

```
snow dcm create <my_project> --if-not-exists

snow dcm create # uses the name specified in the default target from the manifest

snow dcm create --target # uses the named target from the manifest
```

1. In the navigation menu, select **Projects** » **Workspaces**.
2. In the **Workspaces** pane, select **+ Add new** » **DCM Project** to create a new DCM project folder.

   ![Create DCM project dialog with the Define default target environment option selected](/static/images/dcm-projects/dcm-project-create-dialog.png)
3. Select **Define default target environment** to select or create a new DCM project object for the default target in the manifest.

   When running DCM PLAN against a target that has a DCM project object defined in the manifest, but does not yet exist, the UI
   prompts you to confirm creation of that DCM project object based on the defined name and owner role before executing the plan.
4. The status indicator next to **Target** shows whether the specified DCM project object is ready to use. Open the target selector to
   see the status and message for each target.

   - Green: The DCM project object exists and can be used to run PLAN or DEPLOY.
   - Yellow: The object exists, but the `project_owner` role doesn’t have access to this workspace.
   - Red: The object can’t be used yet, because the project name isn’t a valid fully qualified name, `manifest.yml` is missing
     `project_owner`, or the object doesn’t exist or isn’t accessible to the `project_owner` role.
   - Gray: Snowflake is still checking the object’s status.

![Target selector showing a green target and a red target with its error message](/static/images/dcm-projects/dcm-project-target-status.png)

## Access control and role privileges

You can set role-based access control (RBAC) of the schema-level DCM project object to READ, MONITOR, or OWNERSHIP privileges.

These privileges are independent of the access control for definition files stored in a workspace, stage, or repository.

| Privilege | Description | Allowed operations |
| --- | --- | --- |
| READ | - Shows if the DCM project object exists. - Lists the objects and grants deployed by the DCM project, which are visible to the user’s role.   This means you need both READ on the DCM project and READ on the objects themselves. | - SHOW DCM PROJECTS LIKE ‘%project’ - DESCRIBE DCM PROJECT <project> - SHOW ENTITIES IN DCM PROJECT <project> |
| MONITOR | - Gives access to the complete deployment history, including all artifacts. - Gives the role the ability to analyze, debug, or audit production deployments without the ability to deploy changes directly. | - All READ privileges - DESCRIBE DCM PROJECT <project> (with source and deployment path of latest deployment) - INFORMATION\_SCHEMA.DCM\_DEPLOYMENT\_HISTORY (project\_name => ‘db.schema.project’) - SHOW DEPLOYMENTS IN DCM PROJECT <project> - LIST all files in the deployment - GET any access to files inside the DCM project |
| OWNERSHIP | - The role that is used to create the DCM project object is the owner of that project. - Gives the role the ability to deploy changes. - Gives the role the ability to transfer ownership of the project to another role when the project has not yet been deployed. | - All MONITOR privileges - EXECUTE DCM PROJECT <project> PLAN - EXECUTE DCM PROJECT <project> DEPLOY - EXECUTE DCM PROJECT <project> PREVIEW - EXECUTE DCM PROJECT <project> TEST - DROP DCM PROJECT <project> - ALTER DCM PROJECT <project> - GRANT READ on DCM PROJECT <project> TO ROLE <role2> - GRANT MONITOR on DCM PROJECT <project> TO ROLE <role2> |

Expand

Show lessSee more

### Ownership on DCM-managed objects

The role that deploys a DCM project, by default, has the OWNERSHIP privilege of all deployed objects.

The project definitions can include GRANT OWNERSHIP statements to other roles. The DCM project owner role automatically has OWNERSHIP on
all roles it creates inside the project. However, if one of those roles is then granted OWNERSHIP of other deployed entities (such as tables
or schemas), the project owner role no longer has direct OWNERSHIP of those entities. To avoid being locked out of those objects on future
deployments, you must also grant that role to the project owner role:

Copy code

```
-- Define a role inside the project. The project owner role has OWNERSHIP on this role by default.
DEFINE ROLE MY_DB.MY_SCHEMA.DATA_OWNER_ROLE;

-- Define a table inside the project.
DEFINE TABLE MY_DB.MY_SCHEMA.MY_TABLE (ID INT, NAME VARCHAR);

-- Transfer ownership of the table to the role.
GRANT OWNERSHIP ON TABLE MY_DB.MY_SCHEMA.MY_TABLE TO ROLE DATA_OWNER_ROLE;

-- Grant the role to the project owner role so the project owner inherits
-- ownership of MY_TABLE through the role hierarchy.
-- Without this, the project owner is locked out of MY_TABLE on future deployments.
GRANT ROLE DATA_OWNER_ROLE TO ROLE DCM_PROJECT_OWNER_ROLE;
```

DCM PLAN and DEPLOY actively check for potential owner lockout and fail before making any changes if a `GRANT OWNERSHIP` statement on a
managed object points to a role that the project owner role doesn’t hold. This is a safety check, not a side effect: DCM prevents the
lockout from happening in the first place.

The situation where the project owner is already locked out of a managed object only occurs when a privilege was revoked from the project
owner role manually outside of DCM. In that case, the next PLAN or DEPLOY will fail because the current state no longer matches what DCM
expects. To recover, either remove the object’s definition from the project or restore ownership to the project owner role outside of DCM.

If you want to migrate existing objects to be managed by a DCM project, the role that owns the DCM project object also has to have ownership
privileges (direct or inherited through other roles) on the object to be managed by DCM project.

Note

If an object is migrated, we recommend adding the corresponding GRANT OWNERSHIP statement to the project definitions as well to ensure that
the current state and DCM project definitions are in sync.

## Define a DCM project

A DCM project is based on a manifest file and one or more SQL object definition files. These files are typically stored and managed in a
Git repository or your local workspace.

- The manifest file

  - Specifies one or more target environments with corresponding account identifiers, DCM project objects, owner roles for these objects, and optional templating configurations
  - Optionally, specifies templating defaults and one or more configurations with values for [template variables](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-files-configurations).
- The object definition files

  - Define a group of Snowflake objects, grants, and expectations that you want to manage together in this DCM project.

See [Create a DCM project folder to store your definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-files) for how to set up a DCM project folder and the definition files and how to use templates to define your
DCM project.

## Plan a DCM project

Planning a DCM project performs a dry run to preview changes before deployment. Snowflake compares your [project definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-definition-files) to existing objects and shows which objects will be created, altered, or dropped. No changes are made
to your account.

Use planning to review and validate changes before deploying a DCM project.
You can specify options such as a [configuration](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-files-configurations)
or an output path for plan results.

The PLAN mimics the DEPLOY command as much as possible, except it doesn’t actually execute any DDL statements. Because PLAN closely
mirrors DEPLOY, it requires the same OWNERSHIP privilege on the DCM project as DEPLOY, even though no changes are applied. This way,
a dry run surfaces privilege errors before deployment.

Important

Always run the PLAN command on your projects before deployment to help ensure there are no errors from syntax, templating, object
dependency, access privileges, and so on. Review the plan output to debug any errors, preview the rendered Jinja with the provided
variables, and preview the changes that will be made once you deploy.

The plan performs the following steps:

1. Renders all Jinja templating with the selected configuration profile or values provided at runtime.
2. Compares all definitions against the current state of entities that were defined as part of the last deployment.
3. Converts all defined statements into CREATE, ALTER, DROP, GRANT, and REVOKE statements.
4. Sorts all statements based on their interdependencies.
5. Compiles all statements.

Note

Although PLAN catches almost all possible errors that can occur during deployment, it does not guarantee a successful deployment.

### Run the PLAN command

The PLAN command takes the following information as input:

- The path to the manifest file

  The CLI reads the target from the manifest (`default_target` or `--target` flag). For SQL commands, the path to the manifest file and
  the project name must be provided.
- Defined values for Jinja variables (optional).
- The target’s `templating_config` automatically selects the configuration profile. For SQL commands, use the USING CONFIGURATION clause to
  specify the profile.
- One or more values of the configuration profile to overwrite (optional).

The following are examples of how to run the PLAN command.

Snowflake CLISnowsightSQL

Run the `snow dcm plan` command in your local IDE terminal or as part of a Git workflow.

An example of a CLI command to plan a DCM project from a local directory is:

Copy code

```
cd ./Quickstarts/DCM_Project_Quickstart_1/
snow dcm plan
```

An example of a CLI command to plan a DCM project from a Snowflake stage or Git repository clone is:

Copy code

```
snow dcm plan --target PROD_US --save-output
```

An example of a CLI command to plan a DCM project with optional arguments is:

Copy code

```
snow dcm plan
--variable "wh_size='MEDIUM'" --variable "teams = ['TEAM_A', 'TEAM_B']"
--save-output
```

Variables must be enclosed in double quotes, with additional single quotes for string values. Lists of values require
square brackets.

![Snowflake CLI commands](/static/images/dcm-projects/dcm-project-snow-dcm-commands.png)

To open the DCM project pane, select **Show project controls** on your project folder in the file explorer. Then, at the top of the pane:

1. Select your project from the project switcher in the pane tab.

   ![DCM project pane tab with the project switcher chevron next to the project name](/static/images/dcm-projects/dcm-project-pane-tab.png)
2. Select your target (if you have multiple targets).
3. In the operations list, select **Plan**.
4. (optional) To overwrite specific variable values for this run, turn on **Override Variables** in the same list. This option only
   appears when the selected target declares a `templating_config` in `manifest.yml`.
5. (optional) Select **Delta** under **Plan Mode** to only evaluate definitions that changed since the last deployment. See
   [Plan only changed definitions (PLAN DELTA)](#label-dcm-projects-plan-delta) for details.
6. Click the run button to start the plan.
7. The Snowsight UI automatically uses the DCM project object defined in the manifest target. If the project object does not yet
   exist, you can create it from the UI.

When the PLAN is completed, the output opens in a new tab. If you don’t see it, select **View Last Plan** in the operations list. This
option appears once a plan exists, and it opens the existing output without re-running the plan.

If a Plan already exists, you can choose to re-plan if you have changed your definitions.

The plan output is always generated automatically under the project sub-folder `out/`.

![Plan in Snowflake Workspaces](/static/images/dcm-projects/dcm-project-plan-workspace.png)

You can execute a DCM PLAN in SQL from anywhere you can run SQL commands, inside Snowflake or connected to Snowflake. Use the
[EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) command with the `PLAN` mode.

An example of a SQL command to plan a DCM project from a Workspace path is:

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  PLAN
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_9_36';
```

An example of a SQL command to plan a DCM project when using Jinja with configuration profiles but overwriting `wh_size` and `teams` is:

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  PLAN
  USING CONFIGURATION DEV (wh_size => 'MEDIUM', teams => ['TEAM_A', 'TEAM_B'])
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_9_36';
```

An example of a SQL command to plan a DCM project when using Jinja templating without configuration profiles is:

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  PLAN
  USING (wh_size => 'MEDIUM')
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_9_36';
```

### Plan only changed definitions (PLAN DELTA)

PLAN DELTA is a faster variant of PLAN for validating incremental changes to an existing project. Instead of checking
all definitions against the current account state, PLAN DELTA only evaluates the definitions you changed and any
downstream definitions in the project that depend on them.

Use PLAN DELTA during active development to get faster feedback on your edits. Because it skips unchanged
definitions, it doesn’t detect changes that happened outside of DCM Projects on your account since the last deployment (for
example, a view dropped or altered by another user). Always run a full PLAN before deploying to ensure no external
changes will cause a deployment failure.

Snowflake CLISnowsightSQL

Copy code

```
snow dcm plan --delta
```

In the DCM project pane, select **Plan** in the operations list, select **Delta** under **Plan Mode**, then click the run button.

![Operations list showing Plan selected, Delta selected under Plan Mode, and the Override Variables toggle](/static/images/dcm-projects/dcm-project-plan-mode-delta.png)

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  PLAN DELTA
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1';
```

See [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) for the full syntax.

### Definition file path

You have the following options to reference the location of the manifest and definition files.

- From a Workspace path

  The Snowsight user interface automatically lists all DCM project definitions inside the current workspace. You can select one of these
  paths and workspaces will use it to run DCM commands.

  If you want to manually run SQL commands in workspaces you can also refer to that same path inside any of your workspaces.

  **Tip:** The 3-dot menu next to every file in your workspace lets you copy the full path to that file into your SQL code.

  An example of a SQL command to plan a DCM project from a workspace path is:

  Copy code

  ```
  EXECUTE DCM PROJECT DCM_PROJECT_DEV
    PLAN
    USING CONFIGURATION DEV
  FROM
    'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1'
  ```
- From a local Git repository clone on your disk

  Select the directory that contains your `manifest.yml` file before running the CLI command in your local IDE.
  Alternatively, you can specify a different local directory that contains the manifest and definitions you want to use.

  An example of a CLI command to plan a DCM project from the current directory of a local Git repo:

  Copy code

  ```
  cd ./Quickstarts/DCM_Project_Quickstart_1/

  snow dcm plan

  snow dcm plan --target PROD
  ```

  An example of a CLI command to plan a DCM project from a different directory in a local Git repo clone:

  Copy code

  ```
  snow dcm plan DCM_PROJECT_DEV --configuration DEV --from ./Quickstarts/DCM_Project_Quickstart_2/
  ```
- From your remote repository in a workflow

  The same CLI syntax can be used when the DCM commands are executed in a CI/CD workflow. You can call the CLI directly
  or use the [reusable GitHub Actions](#label-dcm-github-actions) from the snowflake-labs DCM repository, which
  handle CLI setup, authentication, and DCM commands internally.

  An example using the reusable `dcm-plan` action:

  Copy code

  ```
  steps:
    - uses: actions/checkout@v4
    - uses: snowflakedb/snowflake-actions/dcm/dcm-plan@v3
      with:
        target: PROD
        project-path: Quickstarts/DCM_Project_Quickstart_1/
        snowflake-user: ${{ env.SNOWFLAKE_USER }}
  ```
- From a Stage or Git repository clone in Snowflake

  If you want to run a PROCEDURE or TASK inside Snowflake that runs DCM commands, this SQL command can reference an absolute
  path to a Snowflake stage or Git repository clone inside the account.

  For Git repository clones, consider first running ALTER GIT REPOSITORY FETCH to have the latest version.

  `'@...'` paths can only be used when executing DCM SQL commands.

  An example of a SQL command to plan a DCM project from a Stage or Git repository clone in Snowflake is:

  Copy code

  ```
  EXECUTE DCM PROJECT DCM_PROJECT_DEV
    PLAN
    USING CONFIGURATION DEV
  FROM
    '@DCM_DEMO.DEPLOY.DCM_DEMO/branches/main/Quickstarts/DCM_Project_Quickstart_1/'
  ```

### Plan output

For the PLAN and DEPLOY output format, including the JSON schema and examples, see the
[PLAN and DEPLOY output](/sql-reference/sql/execute-dcm-project#label-dcm-projects-plan-deploy-output) section of the [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) command reference.

## Deploy a DCM project

When you deploy a DCM project, the following actions are performed:

- Objects that are defined but don’t exist yet are created.
- Objects that already exist but differ from the current definition are altered.
- Objects that already exist as defined are skipped.
- Objects that already exist but are no longer defined are dropped.

The same behavior applies to grants and attached data quality expectations defined in the project.

Important

To avoid any unintended data loss, always run and **review your PLAN** output before running DEPLOY.

Each DCM project can only have one instance deployed at any time. Multiple configuration profiles can’t coexist. Deploying configuration B
with the same DCM project will drop any objects from other previous configurations that are not defined in B.

Create one DCM project for each target environment. The DCM project for each environment can then point to the same definition files, but
deploy independently with different values for each variable, like `suffix => 'DEV_JS'`, so that they can exist
independently side-by-side on the same Snowflake account.

You can overwrite values for selected variables at runtime if you want to use a pre-defined profile with a slight variation.

For example:

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  DEPLOY
  USING CONFIGURATION DEV (suffix=>'DEV_USER', user=>'JANEDOE')
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1';
```

Copy code

```
snow dcm deploy DCM_PROJECT_DEV --configuration DEV --variable "suffix='DEV_USER'" --variable "user='JANEDOE'"
```

Each deployment attempt (executing, successful, failed, or canceled) has a deployment number, for example `DEPLOYMENT$1`. Optionally you can
specify a unique string as a deployment *alias* to name individual deployments for better observability in the deployment history.
Think of the deployment *alias* like a commit message for your code change.

Each DEPLOY command first runs an internal PRE-PLAN as part of the deployment. If the PRE-PLAN succeeds, the DEPLOY is executed
directly afterwards. There is no option to intercept or review this internal plan step. The PRE-PLAN is executed to further
reduce the risk of failure during the deployment.
If a DEPLOY fails, you can see in the error message if it failed during the PRE-PLAN or DEPLOY step.
Failure during the PRE-PLAN step is similar to PLAN - no DDL changes are executed.

Important

Failure during the DEPLOY step can result in partial execution of the defined changes. This can potentially cause some of the
managed objects to be in an undefined state. In most cases, fixing the root cause and executing DEPLOY again restores the
defined target state.

The target path for the DEPLOY output file can’t be customized. Deployment artifacts are always stored inside the DCM project.

### Run the DEPLOY command

To execute the DEPLOY command, provide the following inputs:

- The path to the manifest file.
- A configuration profile must be named if configuration profiles are defined in the manifest.
- Optionally, values for the configuration profile overriding the default values.
- Optionally, a deployment *alias*.

The following are examples of how to run the DEPLOY command.

SQLSnowflake CLISnowsight

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  DEPLOY
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1';
```

An example of a SQL command to deploy a DCM project when using Jinja with configuration profiles but overwriting `wh_size` and `teams` is:

Copy code

```
EXECUTE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  DEPLOY AS "testing 2 teams"
  USING CONFIGURATION DEV (wh_size => 'MEDIUM', teams => ['TEAM_A', 'TEAM_B'])
FROM
  'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1';
```

You can run `snow dcm deploy` either in your local IDE terminal or as part of a Git workflow.

An example of a CLI command to deploy a DCM project from a local directory is:

Copy code

```
cd ./Quickstarts/DCM_Project_Quickstart_1/
snow dcm deploy DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
```

An example of a CLI command to deploy a DCM project targeting a non-default environment is:

Copy code

```
snow dcm deploy --target PROD_US
```

An example of a CLI command to deploy a DCM project with optional arguments is:

Copy code

```
snow dcm deploy DCM_DEMO.PROJECTS.DCM_PROJECT_DEV \
--target DCM_DEV \
--variable "wh_size='MEDIUM'" --variable "teams = ['TEAM_A', 'TEAM_B']" \
--alias 'testing 2 teams'
```

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Select your project from the project switcher in the DCM project pane tab.

   ![DCM project pane tab with the project switcher chevron next to the project name](/static/images/dcm-projects/dcm-project-pane-tab.png)
3. Select your target (if you have multiple targets).
4. In the operations list, select **Plan**, then click the run button.

   The UI will automatically use the DCM project object defined in the manifest target. If the project object does not yet exist, you
   can create it from the UI.
5. Once the PLAN is completed, the output opens in a new tab. If you don’t see it, select **View Last Plan** in the operations list.
   This option appears once a plan exists, and it opens the existing output without re-running the plan.

   If a Plan already exists you can choose to re-plan if you have changed your definitions.
6. Review your PLAN output to ensure it does not contain unintended changes.
7. In the operations list, select **Deploy**, then click the run button to execute the deployment with the same target and values
   from PLAN.

See [PLAN and DEPLOY output](/sql-reference/sql/execute-dcm-project#label-dcm-projects-plan-deploy-output) for the standard plan output structure.

## Manage a DCM project

### Show objects and grants managed by a DCM project

The [SHOW ENTITIES IN DCM PROJECT](/sql-reference/sql/show-entities-in-dcm-project) command allows you to see a list of all Snowflake objects that are currently managed by a specific DCM project.
It provides a list of fully qualified names for all objects. To see the results, you need both READ privilege on the DCM project and privileges to see the managed object itself.

Note

The result does not necessarily match the objects of the most recent deployment. Objects that were manually dropped or detached from the project are not listed in the result.

You can use `LIKE` to search by name or use a flow operator to further process or filter the result set.

Similarly, the [SHOW GRANTS IN DCM PROJECT](/sql-reference/sql/show-grants-in-dcm-project) command lets you list the grants that are defined and deployed with the DCM project.
Use `SHOW GRANTS IN DCM PROJECT` to list grants that are currently deployed and managed by the project, or `SHOW FUTURE GRANTS IN DCM PROJECT` to list grants that will be deployed and managed by the project the next time it’s executed.

Examples to see the objects and grants that are currently managed by a DCM project:

SQLSnowsight

Copy code

```
SHOW ENTITIES LIKE '%DASHBOARD%' IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

SHOW ENTITIES IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  ->> SELECT * FROM $1 WHERE "object_type" = 'DYNAMIC_TABLE';

SHOW GRANTS IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

SHOW FUTURE GRANTS IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;
```

1. In the navigation menu, select **Catalog** » **Database Explorer**.
2. Navigate to the schema that contains the DCM project object.
3. Select the DCM project object to see its details.
4. Select the **Objects** tab to see a list of all Snowflake objects currently managed by this project object, or select the **Grants** tab to see a list of all grants currently managed by this project object.
5. Click the name of an object to open that object’s details page in a new tab.

### Detach objects from a DCM project

Using the [ALTER <object>](/sql-reference/sql/alter) command with the UNSET DCM PROJECT clause, you can detach an object that was deployed and
is now managed by a DCM project. The command removes the association between the object and the DCM project without dropping the object.
You can use this command when you want to start managing an object by a different DCM project.

Make sure to remove the corresponding DEFINE statement from your [project definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-definition-files) before
you deploy it again. Otherwise, the object will be reintegrated into the DCM project.

An example of a SQL command to detach an object from a DCM project:

Copy code

```
ALTER TABLE MY_DB.MY_SCH.MY_TABLE
  UNSET DCM PROJECT;
```

### Detach grants from a DCM project

`ALTER DCM PROJECT ... UNMANAGE GRANT` removes a grant from a project’s management scope without revoking the underlying privilege. The grant remains exactly as it is: only the project’s tracking of it is removed.

Use `UNMANAGE GRANT` when you want to:

- Transfer a grant to a different project or to manual management.
- Clean up stale grant references after an external change: for example, someone outside DCM revoked a privilege.

This is different from removing a grant definition and redeploying. DCM interprets a missing grant definition as intent to revoke, and revokes the grant on the next deployment.

#### Required privileges

The role executing `ALTER DCM PROJECT ... UNMANAGE GRANT` must have `OWNERSHIP` on the DCM Project object.
No `REVOKE` privilege or ownership of the target resource is required: the role only needs to be able to see the grant and the securable object.
This means you can clean up grant references even after another role has removed your access to the managed resources.

#### Syntax

Copy code

```
ALTER DCM PROJECT <project_name>
  UNMANAGE GRANT <grant_specification>;
```

`<grant_specification>` uses the same grammar as a [GRANT <privilege>](/sql-reference/sql/grant-privilege) statement. Write it exactly as you would write the `GRANT` line in your DCM definition files, omitting the leading `GRANT` keyword.

#### Return value

On success, the command returns a message that includes the count of unmanaged grants, for example:

Copy code

```
Unmanaged 3 grants from the project my_project
```

#### Next steps after unmanaging

After running `UNMANAGE GRANT`, remove the corresponding `GRANT` statement from your project definition files before the next deployment. If you leave it in place, DCM reintegrates the grant on the next `EXECUTE DCM PROJECT` run.

#### Error handling

The command returns an error if:

- The referenced grant or securable object doesn’t exist or isn’t resolvable.
- The role doesn’t have `OWNERSHIP` on the DCM Project.
- The role can’t see the referenced securable object.

The command doesn’t fail silently: every error is reported so you can confirm exactly which grants were unmanaged.

### Purge a DCM project

When you create temporary DCM project objects as development sandboxes or for demos, the
[EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) command with the PURGE option lets you clean up the entire project in a single
statement. PURGE runs a deployment without any definitions, which drops all entities, revokes all grants, and removes all
attachments the project currently manages.

Warning

PURGE is destructive by design. Use it only for non-production projects, such as development sandboxes or demos.

To fully tear down a temporary DCM project, run two commands:

1. `EXECUTE DCM PROJECT <name> PURGE` drops all entities, grants, and attachments the project manages.
2. `DROP DCM PROJECT <name>` removes the project object itself.

For example:

Copy code

```
EXECUTE DCM PROJECT my_project PURGE AS "sandbox_cleanup";
DROP DCM PROJECT my_project;
```

The purge execution appears in the deployment history of the DCM project, so you can confirm that it ran successfully. For
more information about dropping the project object, see [Drop a DCM project](#label-dcm-projects-drop).

### Drop a DCM project

When a DCM project object is dropped, all managed entities, grants, and expectations remain in place as “unmanaged”.

Important

Dropping or replacing a DCM project object causes you to lose all deployment history artifacts that the object contains.

SQLSnowflake CLISnowsight

Copy code

```
DROP DCM PROJECT [IF EXISTS] <my_project>;
```

Copy code

```
snow dcm drop my_project
```

1. In the navigation menu, select **Catalog** » **Database Explorer**.
2. Navigate to the schema that contains the DCM project.
3. Select the DCM project to see its details page.
4. Click the 3-dot menu in the top right and select **Drop**.

## Automate a DCM project deployment

### CI/CD best practices

Follow these practices when automating deployments with CI/CD pipelines:

- A DCM project targeting a non-production environment should be owned by a different role than its production counterpart to avoid
  accidental deployments to production.
- A DCM project targeting a production environment should be owned by a dedicated role for production deployments with specifically tailored access
  privileges that are just enough to deploy all objects in the project.
  - Avoid using general administrator roles for DCM project ownership. Grant such roles only to service users, not to individual developers.
  - Grant the dedicated production deployment role only to service users, not to individual developers.
  - Restrict the ownership to the production deployment role to ensure immutability of critical infrastructure or data products.

    If the dedicated production deployment role grants ownership of production objects to other roles, users who are granted those roles can
    still modify or drop the production objects.

### GitHub Actions

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A set of reusable composite GitHub Actions that automate DCM Projects pipelines is available in the
[`snowflakedb/snowflake-actions`](https://github.com/snowflakedb/snowflake-actions) repository on the
[GitHub Marketplace](https://github.com/marketplace/actions/snowflake-actions#github-actions-for-dcm-projects).
Each action handles one step of the lifecycle, and you can compose them to build end-to-end CI/CD pipelines.

Note

These reusable actions are only available for GitHub. The same CI/CD concepts apply to Azure DevOps, GitLab CI/CD,
Bitbucket Pipelines, and other providers. Only the workflow syntax differs. No published actions are available for
those platforms yet. Consider building your own workflows using a coding agent such as Cortex Code.

The following reusable actions are available: `dcm-parse-manifest`, `dcm-connection-test`, `dcm-plan`, and `dcm-deploy`.
For setup instructions, input/output documentation, and sample workflows, see the
[GitHub Marketplace listing](https://github.com/marketplace/actions/snowflake-actions#github-actions-for-dcm-projects).

To use an action in your workflow, reference it with:

Copy code

```
- uses: snowflakedb/snowflake-actions/dcm/<action-name>@v3
```

#### Authentication

OIDC (OpenID Connect) is the recommended authentication method for CI/CD pipelines because it uses GitHub’s built-in identity
tokens and requires no stored secrets. For setup instructions and alternative authentication options, see the
[GitHub Marketplace listing](https://github.com/marketplace/actions/snowflake-actions#authentication).

#### Sample workflows

The [GitHub\_workflows](https://github.com/Snowflake-Labs/snowflake-dcm-projects/tree/main/GitHub_workflows) directory in the
snowflake-labs DCM repository contains ready-to-use workflow files that compose the reusable actions into complete CI/CD pipelines.
You can copy them into your repository’s `.github/workflows/` directory and customize them for your project. For full setup
instructions, see the
[sample workflows README](https://github.com/Snowflake-Labs/snowflake-dcm-projects/blob/main/GitHub_workflows/README.md).

All sample workflows read the Snowflake `account_identifier` and `project_owner` role directly from the manifest targets,
so that environment-specific configuration lives in the version-controlled `manifest.yml` rather than in duplicated
GitHub secrets. Only the service user credentials are stored as secrets.

The sample workflows demonstrate the following patterns applicable to any DCM Projects CI/CD setup:

- **Manifest-driven configuration**: Each workflow reads `account_identifier`, `project_owner`, and `project_name` from the
  manifest targets, keeping environment configuration in one place.
- **Data drop protection**: The deploy workflow detects destructive DROP operations on data-bearing objects
  (databases, schemas, tables, and stages) and blocks the deployment if any are found.
- **Sequential stage-to-production promotion**: Production deployment starts only after staging deployment succeeds and data quality tests pass.
- **Pull request comments**: Plan and deploy summaries are posted as comments on the originating pull request.

The following screenshot shows a sample PLAN summary that a workflow posted as a pull request comment.

![GitHub Actions bot comment on a pull request summarizing a DCM PLAN, including created and altered objects](/static/images/dcm-projects/dcm_github_actions_pr_comment.png)

##### Sample workflow: Test connections

- Workflow configuration file: [DCM\_1\_Test\_Connections.yml](https://github.com/Snowflake-Labs/snowflake-dcm-projects/blob/main/GitHub_workflows/DCM_1_Test_Connections.yml)
- Trigger: Manual with the `workflow_dispatch` event

This workflow validates that the GitHub Actions service user can connect to every target environment defined in the manifest. Use it
when setting up a new repository, onboarding a new account, or debugging authentication issues. The workflow performs the following steps:

- Parses all target names from `manifest.yml` dynamically.
- Uses a GitHub Actions matrix strategy to test each target in parallel.
- For each target, verifies the Snowflake connection, reports the connected account, user, and role, and checks whether the connected
  role matches the DCM project owner.
- Reports whether the DCM project object already exists and whether the service user has deployment privileges.

##### Sample workflow: Test PR to main

- Workflow configuration file: [DCM\_2\_Test\_PR\_to\_main.yml](https://github.com/Snowflake-Labs/snowflake-dcm-projects/blob/main/GitHub_workflows/DCM_2_Test_PR_to_main.yml)
- Trigger: Pull request opened, synchronized, or reopened against the `main` branch

This workflow runs a PLAN against the production target as an integration test for every pull request. It provides reviewers with a
summary of the planned changes directly on the pull request. The workflow performs the following steps:

- Runs `snow dcm plan` against the PROD target.
- Parses `plan_result.json` to summarize CREATE, ALTER, and DROP operations grouped by object domain.
- Uploads plan artifacts for later inspection.
- Posts the plan summary as a comment on the pull request.
- Fails the check if the PLAN fails, blocking the merge.

##### Sample workflow: Deploy to Prod

- Workflow configuration file: [DCM\_3\_Deploy\_to\_Prod.yml](https://github.com/Snowflake-Labs/snowflake-dcm-projects/blob/main/GitHub_workflows/DCM_3_Deploy_to_Prod.yml)
- Trigger: Push to the `main` branch (typically a merged pull request)

This workflow plans and deploys to a single production target. Use it when you don’t need a staging environment or when staging
is handled separately. The workflow performs the following steps:

1. Plan: Runs `snow dcm plan` and summarizes the changeset.
2. Data drop detection: Blocks the pipeline if the plan contains DROP operations for databases, schemas, tables, or stages.
3. Deploy: Runs `snow dcm deploy`.
4. Post scripts (optional): Runs SQL post-hook scripts with Jinja variable injection.
5. Test expectations (optional): Runs `snow dcm test` to validate data quality expectations.

After deployment, the workflow optionally posts a status summary to the originating pull request.

##### Sample workflow: Deploy to Stage then Prod

- Workflow configuration file: [DCM\_4\_Deploy\_to\_Stage\_then\_Prod.yml](https://github.com/Snowflake-Labs/snowflake-dcm-projects/blob/main/GitHub_workflows/DCM_4_Deploy_to_Stage_then_Prod.yml)
- Trigger: Push to the `main` branch (typically a merged pull request)

This workflow implements a sequential promotion pipeline. Changes are first deployed to staging, validated end-to-end, and only then
promoted to production. If any step fails, the pipeline stops and production is not affected.

The deployment sequence for each target (STAGE, then PROD) includes:

1. Plan: Runs `snow dcm plan` and summarizes the changeset.
2. Data drop detection: Blocks the pipeline if the plan contains DROP operations for databases, schemas, tables, or stages.
3. Deploy: Runs `snow dcm deploy`.
4. Post scripts (optional): Runs SQL post-hook scripts with Jinja variable injection.
5. Test expectations (optional): Runs `snow dcm test` to validate data quality expectations.

Production deployment starts only after all staging steps pass. After all jobs complete, the workflow optionally posts a final
status summary to the originating pull request.

## Frequently asked questions (FAQ)

How do I rename an existing object?
:   1. Run an ALTER command outside of the DCM project.
    2. Change the definition.
    3. Run PLAN to verify that the new definition matches the new state (no change in PLAN).
    4. Run DEPLOY to save the new state.

How do I deploy objects that are not yet supported by DEFINE statements?
:   You can run CREATE IF NOT EXISTS or CREATE OR REPLACE statements in a separate SQL script after executing your DCM project plan or
    deployment.

    Both options support Jinja2 templating and dry-run (dry-run renders the Jinja templating but does not verify successful SQL compilation).

    For example:

    SQLSnowflake CLI

    Copy code

    ```
    EXECUTE DCM PROJECT my_project
      PLAN ...
    USING ...
    FROM ...

    EXECUTE IMMEDIATE
    FROM
      'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/head/Quickstarts/DCM_Project_Quickstart_1/hooks/post_hook.sql'
      USING (db => 'DEV')
      dry_run = TRUE      -- shows the rendered Jinja but does not verify successful compilation
    ;
    ```

    Copy code

    ```
    snow dcm deploy --target DEV

    snow sql -f hooks/post_hook.sql --variable "db='DEV'" --enable-templating JINJA
    ```
