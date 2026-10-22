# Create and deploy DCM Projects

This topic describes how to create and deploy DCM Projects to manage Snowflake environments, including accounts.

The DCM project lifecycle involves the following steps:

1. [Prepare](#label-dcm-projects-prepare) your Snowflake account for a DCM project.
2. [Define](#label-dcm-projects-define) project configuration and objects in project files.
3. [Create](#label-dcm-projects-create-object) a DCM Projects object.
4. [Plan](#label-dcm-projects-plan) to preview proposed changes before deployment.
5. [Deploy](#label-dcm-projects-deploy) the project.
6. [Monitor](/user-guide/dcm-projects/dcm-projects-monitor) deployments and troubleshoot failing plans.
7. [Manage](/user-guide/dcm-projects/dcm-projects-manage) the deployed project and the entities, grants, and attachments it manages.

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
| **Snowsight**  A workspace in Snowsight is a Snowflake native cloud IDE in your account. | - Easily create or upload DCM definition files via the UI. - Connect to a Git repository to pull and push changes. - Review, edit, and debug definition files. - Execute DCM PLAN and DEPLOY commands using the workspace UI. - Browse the database catalog to see DCM project objects and their configuration, managed objects, and deployment history. - Select a target profile to automatically use the linked DCM project and templating configuration. |
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

1. DCM Projects require Snowflake CLI version 3.24.0 or higher for the commands and options documented in this guide. Install or upgrade
   Snowflake CLI as described in [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
2. Configure your connection to your Snowflake account, as described in [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect). Confirm you have a working connection:

   Copy code

   ```
   snow connection test
   ```

   For more information about how the CLI resolves project targets separately from the active connection and role, see
   [Project identifier resolution](/developer-guide/snowflake-cli/command-reference/dcm-commands/overview#label-snowcli-dcm-project-identifier-resolution).
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

snow dcm create --target DEV # uses the named target from the manifest
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
| READ | - Shows if the DCM project object exists. - Lists the objects and grants deployed by the DCM project, which are visible to the user’s role.   This means you need both `READ` on the DCM project and the appropriate privilege to see each managed object. The underlying privilege varies by object type. | - SHOW DCM PROJECTS LIKE ‘%project’ - DESCRIBE DCM PROJECT <project> - SHOW ENTITIES IN DCM PROJECT <project> |
| MONITOR | - Gives access to the complete deployment history, including all artifacts. - Gives the role the ability to analyze, debug, or audit production deployments without the ability to deploy changes directly. | - All READ privileges - DESCRIBE DCM PROJECT <project> (with source and deployment path of latest deployment) - INFORMATION\_SCHEMA.DCM\_DEPLOYMENT\_HISTORY (project\_name => ‘db.schema.project’) - SHOW DEPLOYMENTS IN DCM PROJECT <project> - LIST all files in the deployment - GET any access to files inside the DCM project |
| OWNERSHIP | - The role that is used to create the DCM project object is the owner of that project. - Gives the role the ability to deploy changes. - Gives the role the ability to transfer ownership of the project to another role when the project has not yet been deployed. | - All MONITOR privileges - EXECUTE DCM PROJECT <project> PLAN - EXECUTE DCM PROJECT <project> DEPLOY - EXECUTE DCM PROJECT <project> PREVIEW - EXECUTE DCM PROJECT <project> TEST - DROP DCM PROJECT <project> - ALTER DCM PROJECT <project> - GRANT READ on DCM PROJECT <project> TO ROLE <role2> - GRANT MONITOR on DCM PROJECT <project> TO ROLE <role2> |

Expand

Show lessSee more

### Ownership on DCM-managed objects

The role that deploys a DCM project, by default, has the OWNERSHIP privilege of all deployed objects.

Project definitions can transfer ownership to other roles. To prevent owner lockout, the DCM project owner role must hold the role that
receives ownership. For the complete definition pattern and its limitations, see
[OWNERSHIP grants](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-grant-ownership).

DCM PLAN and DEPLOY actively check for potential owner lockout and fail before making any changes if a `GRANT OWNERSHIP` statement on a
managed object points to a role that the project owner role doesn’t hold. This is a safety check, not a side effect: DCM prevents the
lockout from happening in the first place.

The situation where the project owner is already locked out of a managed object only occurs when a privilege was revoked from the project
owner role manually outside of DCM. In that case, the next PLAN or DEPLOY will fail because the current state no longer matches what DCM
expects. To recover, restore the required ownership or role hierarchy outside of DCM.

For an intentional management handoff, first use the documented
[detach workflow](/user-guide/dcm-projects/dcm-projects-manage#label-dcm-projects-detach-object) with a role that has the required privileges, and then remove the definition before
redeploying. Removing a definition without first detaching the object expresses intent to drop the managed object; it isn’t a recovery
method for owner lockout.

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

An example of a CLI command to plan a DCM project from local files by using a non-default target is:

Copy code

```
snow dcm plan --target PROD_US --save-output
```

An example of a CLI command to plan a DCM project with optional arguments is:

Copy code

```
snow dcm plan \
  --variable "wh_size='MEDIUM'" --variable "teams = ['TEAM_A', 'TEAM_B']" \
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

  If you want to manually run SQL commands in workspaces, you can also refer to that same path inside any of your workspaces.

  **Tip:** The 3-dot menu next to every file in your workspace lets you copy the full path to that file into your SQL code.

  An example of a SQL command to plan a DCM project from a workspace path is:

  Copy code

  ```
  EXECUTE DCM PROJECT DCM_PROJECT_DEV
    PLAN
    USING CONFIGURATION DEV
  FROM
    'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/Quickstarts/DCM_Project_Quickstart_1';
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
  snow dcm plan DCM_PROJECT_DEV \
    --target DEV \
    --from ./Quickstarts/DCM_Project_Quickstart_2/
  ```
- From your remote repository in a workflow

  The same CLI syntax can be used when the DCM commands are executed in a CI/CD workflow. You can call the CLI directly
  or use the [reusable GitHub Actions](/user-guide/dcm-projects/dcm-projects-cicd#label-dcm-github-actions) from the snowflake-labs DCM repository, which
  handle CLI setup, authentication, and DCM commands internally.

  An example using the reusable `dcm-plan` action:

  Copy code

  ```
  jobs:
    plan:
      runs-on: ubuntu-latest
      environment: PROD
      permissions:
        contents: read
        id-token: write
      steps:
        - uses: actions/checkout@v7
        - uses: snowflakedb/snowflake-actions/dcm/plan@v3
          with:
            target: PROD
            project-path: Quickstarts/DCM_Project_Quickstart_1/
            snowflake-user: ${{ env.SNOWFLAKE_USER }}
  ```
- From a Stage or Git repository clone in Snowflake

  If you want to run a PROCEDURE or TASK inside Snowflake that runs DCM commands, this SQL command can reference an absolute
  path to a Snowflake stage or Git repository clone inside the account.

  For Git repository clones, consider first running ALTER GIT REPOSITORY FETCH to get the latest version.

  `'@...'` paths can only be used when executing DCM SQL commands.

  An example of a SQL command to plan a DCM project from a Stage or Git repository clone in Snowflake is:

  Copy code

  ```
  EXECUTE DCM PROJECT DCM_PROJECT_DEV
    PLAN
    USING CONFIGURATION DEV
  FROM
    '@DCM_DEMO.DEPLOY.DCM_DEMO/branches/main/Quickstarts/DCM_Project_Quickstart_1/';
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
snow dcm deploy DCM_PROJECT_DEV \
  --target DEV \
  --variable "suffix='DEV_USER'" \
  --variable "user='JANEDOE'"
```

Each deployment attempt (executing, successful, failed, or canceled) has a deployment number, for example `DEPLOYMENT$1`. Optionally you can
specify a unique string as a deployment *alias* to name individual deployments for better observability in the deployment history.
Think of the deployment *alias* like a commit message for your code change.

Each `DEPLOY` command first runs an internal `COMPILE` and `PLAN` as part of the deployment. If the `PLAN` succeeds, `DEPLOY` is executed
directly afterwards. There is no option to intercept or review this internal plan step. The `PLAN` is executed to further
reduce the risk of failure during the deployment.
`DEPLOY` reconciles the submitted definitions with the current account state and computes a fresh changeset. It doesn’t replay a previously
saved `PLAN` result. Intervening account changes can therefore change the deployment changeset even when the submitted definitions are
unchanged.
If `DEPLOY` fails, you can see in the error message if it failed during the `RENDER`, `COMPILE`, `PLAN` or `DEPLOY` step.
Failure during any step before `DEPLOY` step is similar to `PLAN`: No DDL changes are executed.

Warning

In the rare case of failure during the `DEPLOY` step, the defined changes can be partially executed. This can potentially cause some of the
managed objects to be in an undefined state. In most cases, fixing the root cause and executing DEPLOY again restores the
defined target state. To apply an earlier definition state through a new reconciliation, see
[Recover an earlier defined state](/user-guide/dcm-projects/dcm-projects-monitor#label-dcm-projects-recover-state).

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

### Automate a DCM project deployment

To set up collaboration workflows and automate PLAN and DEPLOY with CI/CD pipelines, see
[Collaboration and CI/CD for DCM Projects](/user-guide/dcm-projects/dcm-projects-cicd).
