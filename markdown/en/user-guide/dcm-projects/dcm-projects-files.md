# DCM Projects files and templates

A DCM project requires a manifest file and one or more SQL object definition files. These files are typically stored and managed in a
Git repository or your local workspace.

- The manifest file

  - Defines deployment targets and configurations for different environments with
    [template variables](#label-dcm-projects-files-configurations).
- The object definition files

  - Define a group of Snowflake objects that you want to manage together in the DCM project.

The high-level workflow to create DCM project files is:

1. [Create a DCM project folder to store your definition files](#label-dcm-projects-files)
2. [Create a manifest file](#label-dcm-projects-manifest-file)
3. [Create object definition files](#label-dcm-projects-definition-files)

## Create a DCM project folder to store your definition files

To create a new DCM project, create a folder to store your manifest file (`manifest.yml`) and SQL object definition files.

Snowflake CLISnowsight

Copy code

```
snow init <project_name> --template dcm_project
```

The `snow init` command with the `dcm_project` template creates example definition files in your project directory. You can open and
edit these files to define your DCM project.

1. In the navigation menu, select **Projects** » **Workspaces**.
2. In the **Workspaces** pane, select **+ Add new**.
3. Select **DCM Project**.

![Add new DCM Project](/static/images/dcm-projects/dcm-project-add-new-workspace.png)

DCM Projects follows the standardized folder structure:

- DCM Projects object definition files must be placed under `sources/definitions/`.
- The optional global macro files can be placed under `sources/macros/`.
- File naming and nesting inside these project directories are flexible.
- Snowflake CLI and Workspaces save local command output under `out/`. SQL commands can use interface-specific output locations.
- If you have additional scripts that you want to use with DCM commands, you can add them under `sources`.
- If you have other custom scripts that you want to store within the project folder that should not be used by DCM Projects commands and not
  uploaded from local, add them in a folder outside of the `sources` folder.
- Snowflake CLI uploads `manifest.yml` and the files under `sources`.

Note

If you are using Git, add `out/` to your `.gitignore` file to avoid pushing local output files to Git.

An example of a DCM project folder structure is:

Copy code

```
my_dcm_project/
  ├── manifest.yml
  ├── sources/
  │   ├── definitions/
  │   │   ├── bronze.sql
  │   │   └── silver.sql
  │   ├── macros/
  │   │   └── global_macro.sql
  ├── my_post_scripts/
  └── out/
      └── plan/
```

You can also keep multiple projects in one repository. Keep each project in a separate, non-overlapping folder with its own `manifest.yml`
and `sources/definitions/` directory:

Copy code

```
repository/
  ├── customer_data/
  │   ├── manifest.yml
  │   └── sources/
  │       └── definitions/
  │           └── customer_data.sql
  └── reporting/
      ├── manifest.yml
      └── sources/
          └── definitions/
              └── reporting.sql
```

Run a command for a specific project by passing its directory:

Copy code

```
snow dcm plan --from ./customer_data/
```

Each project’s DCM configuration belongs in its `manifest.yml` file, not in `snowflake.yml`.

## The `/out/` subfolder

The `/out/` folder in your project directory contains the rendered project definitions after you run `PLAN` with one of the following:

- The `--save-output` flag in the CLI.
- The Workspace UI.
- An `OUTPUT_PATH` pointed at this folder in an `EXECUTE DCM PROJECT ... PLAN` statement.

Each CLI command that uses `--save-output` recreates the local `/out/` folder. Copy any local output that you need to retain before running
another command with this option. Workspaces and SQL `OUTPUT_PATH` destinations have their own overwrite behavior.

For `PLAN`, the local `/out/` folder also contains the response JSON as `plan_result.json` and the rendered definitions. The Workspace UI
uses the response file to render the `PLAN` changeset, and you can also process it with agents or automations. These local outputs are
distinct from the deployment artifacts retained inside the DCM project after `DEPLOY`.

Consider the following:

- You can ignore the `/out/` folder if you don’t need the rendered output or changeset. To prevent it from being committed to your Git
  repository, add `/out/` to your project’s `.gitignore` file.
- You can safely delete the `/out/` folder at any time. It’s recreated the next time you run `PLAN` with output saving enabled.

## Create a manifest file

Each DCM project requires a `manifest.yml` file. It holds the essential configuration details of the project and allows the project folder to be
identified as a DCM project.

You use the manifest file to control which DCM project objects and roles to use when deploying to different target environments and to
manage sets of templating values.

The manifest file is a YAML file that contains the following properties:

Copy code

```
manifest_version: 2
type: DCM_PROJECT
default_target:
targets:
templating:
```

| Property | Required | Description |
| --- | --- | --- |
| `manifest_version` | Required | Version of the manifest schema. The current version is 2. |
| `type` | Required | Type of the project. Set to `DCM_PROJECT`. |
| `default_target` | Optional | If you have more than one target, specify the default target. The Snowflake CLI and Workspaces use the default target if you do not specify a target using the `--target` flag. |
| `targets` | Required | The `targets` section maps each deployment target to a specific Snowflake account, DCM project object, owner role, and optionally a templating configuration. This mapping eliminates the need to pass fully qualified project names and configuration flags in every CLI command. See [Project targets](#label-dcm-projects-targets) for more details. |
| `templating` | Optional | The `templating` section defines the templating configurations to use for the project. See [Project templating configurations](#label-dcm-projects-files-configurations) for more details. |

Expand

Show lessSee more

### Project targets

Each target in the manifest file contains the following properties:

Copy code

```
targets:
  <target_name>:
    account_identifier:
    project_name:
    project_owner:
    templating_config:
```

| Property | Description |
| --- | --- |
| `account_identifier` | The Snowflake account identifier for this target.  See [Finding the region and locator for an account](/user-guide/admin-account-identifier#label-account-locator-identifier-find). |
| `project_name` | The fully qualified name of the DCM project object, for example, `DCM_DEMO.PROJECTS.DCM_PROJECT_DEV`.  Use the [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects) SQL command to find it. |
| `project_owner` | The role with OWNERSHIP on this project object.  Use the [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects) or [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) SQL command to find it. |
| `templating_config` (optional) | The name of the templating configuration defined in the `templating` section, to use for this target. |

Expand

Show lessSee more

Targets select a project object and templating configuration, not the authenticated Snowflake CLI connection or active role. For CLI precedence,
mismatch warnings, and examples, see
[Project identifier resolution](/developer-guide/snowflake-cli/command-reference/dcm-commands/overview#label-snowcli-dcm-project-identifier-resolution).

#### Map between project definitions and project objects

DCM Projects definition files aren’t strictly tied to a specific DCM project object. You can use the same set of definitions to deploy to multiple
projects, either on different Snowflake accounts or by referencing different configuration profiles. For example, the same definition files
on a repository branch can be deployed to both DEV and PROD accounts as shown in the following figure.

![DCM definitions to DCM Project objects](/static/images/dcm-projects/dcm-project-to-definitions-mapping.png)

Similarly, you can execute a DCM Projects object by referencing definition files from different paths. For example, your CI/CD automation can deploy
definitions from your main branch, and you can manually run a PLAN from your local definition files against the same project to check
how your definitions diverge from the latest deployment. You can also use this approach for ad-hoc manual deployments from other branches or
local paths.

### Project templating configurations

Following is the high-level structure of the templating configuration in the manifest file. You can set only `defaults`, or only
`configurations`, or both.

Copy code

```
templating:
  defaults:
    <variable_name>: <value>
  configurations:
    <configuration_name>:
      <variable_name>: <value>
```

| Property | Description |
| --- | --- |
| `defaults` | The shared variable values, in key-value pairs, that apply across all configurations to avoid repetition. |
| `configurations` | The templating configurations to use for the project.  Individual configurations can override defaults with configuration-specific values. For details on how variables are resolved, see [Configurations](#label-dcm-projects-configurations). |
| `<configuration_name>` | The name of the templating configuration.  Configuration names are case-insensitive. |
| `<variable_name>` | The name of the variable.  Variable names should follow [Python variable naming rules](https://www.w3schools.com/python/python_variables_names.asp).  All variables in project definitions must be declared either in defaults, the selected configuration, or at runtime.  If you want string variables to resolve empty, specify them as `""`. |
| `<value>` | The value of the variable.  Values can be strings, numbers, booleans, lists, or dictionaries.  Dictionaries can be defined in the manifest but cannot be overwritten at runtime. |

Expand

Show lessSee more

### Example: manifest.yml

This is an example of a DCM project manifest file (`manifest.yml`) that includes three [configurations](#label-dcm-projects-files-configurations),
DEV, STAGE, and PROD, with template variables and their default values:

Copy code

```
manifest_version: 2

type: DCM_PROJECT

default_target: DCM_DEV

targets:
  DCM_DEV:
    account_identifier: MYORG-MYACCOUNT_DEV
    project_name: DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
    project_owner: DCM_DEVELOPER
    templating_config: DEV

  DCM_STAGE:
    account_identifier: MYORG-MYACCOUNT_STAGE
    project_name: DCM_DEMO.PROJECTS.DCM_PROJECT_STG
    project_owner: DCM_STAGE_DEPLOYER
    templating_config: STAGE

  DCM_PROD:
    account_identifier: MYORG-MYACCOUNT_PROD
    project_name: DCM_DEMO.PROJECTS.DCM_PROJECT_PROD
    project_owner: DCM_PROD_DEPLOYER
    templating_config: PROD

templating:
  defaults:
    user: "GITHUB_ACTIONS_SERVICE_USER"
    wh_size: "SMALL"

  configurations:
    DEV:
      env_suffix: "_DEV"
      user: "INSERT_YOUR_USER"
      wh_size: "X-SMALL"
      teams:
        - name: "DEV_TEAM"
          write_access: TRUE

    STAGE:
      env_suffix: "_STG"
      teams:
        - name: "TEST_TEAM_A"
          write_access: TRUE
        - name: "TEST_TEAM_B"
          write_access: FALSE

    PROD:
      env_suffix: ""
      teams:
        - name: "Marketing"
          write_access: FALSE
        - name: "Finance"
          write_access: FALSE
          wh_size: "LARGE"
        - name: "HR"
          write_access: FALSE
        - name: "IT"
          write_access: TRUE
```

## Create object definition files

A DCM project definition file is a template that resolves to valid SQL statements for managing Snowflake objects. Each DCM project
requires at least one definition file.

You can organize your object definitions and grants across multiple files and folders. Snowflake recommends choosing a structure that
represents the business logic of the project (for example, bronze, silver, and gold) rather than grouping by object type.

Definition files can only contain DEFINE, GRANT, or ATTACH statements. Other SQL commands are not supported.

To get started quickly with DCM Projects, you can convert your existing SQL deployment scripts by using the DEFINE keyword for your existing DDLs
(*for supported object types*).

The DEFINE statement works like the [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter) command, but with the following key
differences:

- The order and location of DEFINE statements don’t matter. Snowflake collects and sorts all statements from all definition
  files during project execution.
- If you remove a DEFINE statement, Snowflake drops the corresponding object the next time you deploy the project.
- Only a subset of Snowflake objects is supported. For details, see [Supported object types in DCM Projects](/user-guide/dcm-projects/dcm-projects-supported-entities).
- Qualify object names according to the object’s scope. Account-level objects use account-level identifiers, database-level objects use
  the appropriate two-part form, and schema-level objects use fully qualified three-part names in the format
  `database.schema.object_name`.

Definition files can contain various [Jinja2 templating](#label-dcm-projects-templating) options and support advanced templating features, which allow you to
do the following:

- Customize file content at runtime using template variables.
- Use Jinja2 syntax for logic such as loops and conditionals.
- Make definition files reusable and adaptable for different scenarios.

### Object definition templating

DCM Projects supports the Jinja2 framework for templating SQL statements. You can declare variables and assign values using the Jinja2 syntax either
from configuration profiles, in the [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) command, or within Jinja. You can also construct
loops through lists of values, case statements, reusable functions, and more. For more information, see the [Jinja2 documentation](https://jinja.palletsprojects.com/en/stable/).

Supported Jinja2 functionality includes:

- String replacements
- Lists
- Dictionaries and nested dictionaries
- Conditions (IF statements)
- Looping
- Global and in-file macros
  - Macros defined in the `sources/macros` folder can be used across all definition files.
  - Macros defined in a file can be used within the file.

Unsupported Jinja2 functionality includes:

- Using the following tags:
  - [import](https://jinja.palletsprojects.com/en/stable/templates/#import)
  - [extends](https://jinja.palletsprojects.com/en/stable/templates/#extends)
  - [include](https://jinja.palletsprojects.com/en/stable/templates/#include)

Note

The `_snow` identifier is reserved for future use, and can’t be used as a variable or macro name.

Important

Do not use DCM Projects templating variables for object definitions that contain sensitive information or credentials.
The rendered SQL definitions do not redact any values inserted by environment variables.

Similarly, do not enter any personal data, sensitive data, export-controlled data, or other regulated data as metadata, for example, file
names, configuration and variable names, when using the Snowflake service. For more information, see [Metadata fields in Snowflake](https://docs.snowflake.com/en/sql-reference/metadata).

The following is an example DCM project definition file that uses Jinja2 templating:

Copy code

```
DEFINE WAREHOUSE DCM_PROJECT_WH_{{db}}
  WITH
    warehouse_size = '{{wh_size}}'
    auto_suspend = 300;
```

The following is an example of a DCM project manifest file (`manifest.yml`) that defines two configurations: DEV and PROD.

Copy code

```
templating:
  configurations:
    DEV:
      db: "DEV_2"
      wh_size: "X-SMALL"
    PROD:
      db: "PROD"
      wh_size: "LARGE"
```

Rendering this warehouse definition with the DEV configuration (selected automatically through the target’s `templating_config` or at runtime)
resolves to:

Copy code

```
DEFINE WAREHOUSE DCM_PROJECT_WH_DEV_2
  WITH
    warehouse_size = 'X-SMALL'
    auto_suspend = 300;
```

#### Macros

Macro files are any SQL files located in the `macros` folder and its sub-folders. They can only contain macros.

An example of a directory structure of a DCM project with macro files is:

Copy code

```
My_dcm_project
 |_ manifest.yml
 |_ sources
    |_ definitions
       |_ my_definitions.sql
    |_ macros
       |_ my_global_macros.sql
```

Similar to functions in regular programming languages, macros help organize often-used pieces of code into reusable functions, thereby
avoiding repetition and following the DRY (Don’t Repeat Yourself) principle. Macros in DCM Projects work in the same way as [Jinja2 macros](https://jinja.palletsprojects.com/en/stable/templates/#macros) with the following exceptions:

- Dedicated location for macro files in the `macros` folder.
- Macros defined in macro files are automatically visible in other source files.
  The [import](https://jinja.palletsprojects.com/en/stable/templates/#import) Jinja tag is not permitted.
- Duplicate definition of a macro with the same name is detected and rejected.

##### Automatic import of global macros

During the definition file rendering process, source files are scanned for potential macro calls. If a called macro is defined in a macro
file, the implicit [from […] import tag](https://jinja.palletsprojects.com/en/stable/templates/#import) is added automatically, so
no explicit import is needed.

Similar to [Jinja2 macros](https://jinja.palletsprojects.com/en/stable/templates/#macros), you can define a local macro
by prefixing it with an underscore. A local macro can be used only in the file where it’s declared and isn’t visible to
other files.

#### Template comments

In SQL commands, you can add `--` before your code to comment out the line. Jinja still processes variables within the SQL code but leaves the SQL
comments.

For example, the following Jinja code:

Copy code

```
-- hello {{ project_owner_role }}
```

Renders as:

Copy code

```
-- hello DCM_DEVELOPER
```

Commented out commands do not execute in SQL. You can use template comments to debug Jinja templating without affecting your SQL code.

To ignore Jinja code during rendering, add `#` inside opening and closing brackets as shown in the following example:

Copy code

```
{# This Jinja comment will not appear in the rendered output. #}
```

#### Configurations

When using templates in your object definitions, you have the following options:

- Assign values to variables at runtime.
- Define different configuration profiles under `templating: configurations:` in the `manifest.yml`. Each target can reference a
  configuration through `templating_config`. See [Project templating configurations](#label-dcm-projects-files-configurations) for more details.

  If configuration profiles are defined and a target references one through `templating_config`, the configuration is automatically applied
  when using that target. For examples, see [Plan a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-plan).

  The primary use case for configuration profiles in DCM Projects is to target different environments. Configuration profiles allow you to do the following:

  - Deploy the same code to multiple environments.
  - Test production code on a non-prod environment at a reduced scale.
  - Maintain multiple isolated environments on the same account.

  Not all templating configurations have to be referenced by a target profile. You can keep unused configurations to switch the templating
  config for your target from one to another.

  Warning

  A DCM project has only one deployed configuration at a time. Switching a target to another configuration can drop objects from the
  previous configuration when those objects aren’t present in the newly rendered definitions. For coexisting deployments, use distinct
  DCM project objects and non-overlapping managed object names. For more information, see
  [Deploy a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-deploy).
- Define shared default values under `templating: defaults:` to avoid repeating common variables across configurations. See
  [Project templating configurations](#label-dcm-projects-files-configurations) for more details.
- Overwrite specific variables with one-time values at runtime using the `--variable` flag in CLI.

Variables are resolved with a three-tier hierarchy: global defaults < configuration variables < runtime execution variables.

#### Dictionaries

DCM Projects templating supports dictionaries as variable values, enabling structured configuration for complex multi-tenant or multi-resource
deployments.

By grouping related configuration details into dictionaries, you get:

- Granular control: Apply specific settings, such as warehouse sizes, retention policies, and grants, to individual resources without writing
  unique logic for every variation.
- Cleaner code bases: Replace repetitive hard-coded scripts with dynamic loops that adapt based on the configuration.
- Scalability: Onboard new teams or resources by adding entries to your configuration, rather than refactoring deployment pipelines.

Note

Dictionaries can be defined in the manifest but can’t be overwritten at runtime with the `--variable` flag or SQL
`USING CONFIGURATION (...)` overrides. Only scalar values and lists can be overwritten at runtime.

##### Example use case for dictionaries: Multi-tenant environment provisioning

Consider a platform shared by multiple departments, such as Marketing, Finance, and HR, each with different compliance and compute
requirements. With dictionaries, you define a single configuration that captures each team’s needs.

Manifest example:

Copy code

```
templating:
  defaults:
    user: "GITHUB_ACTIONS_SERVICE_USER"
    wh_size: "X-SMALL"
  configurations:
    PROD:
      env_suffix: ""
      project_owner_role: "DCM_PROD_DEPLOYER"
      teams:
        - name: "Marketing"
          wh_size: "MEDIUM"
          data_retention_days: 14
          needs_sandbox_schema: true
        - name: "Finance"
          wh_size: "X-LARGE"
          data_retention_days: 90
          needs_sandbox_schema: false
        - name: "HR"
          data_retention_days: 30
          needs_sandbox_schema: false
```

Definition example:

Your SQL template loops through this dictionary. It automatically creates schemas, assigns the correct retention policy, and conditionally
creates extra resources only for the teams that request them.

Copy code

```
-- loop through team dictionaries
{% for team in teams %}
    {% set team_name = team.name | upper %}

    -- inject dictionary values directly into object properties
    define schema DCM_DEMO_1{{env_suffix}}.{{team_name}}
        comment = 'using JINJA dictionary values'
        data_retention_time_in_days = {{ team.data_retention_days }};

    -- pass the name to your macro
    {{ create_team_roles(team_name) }}

    define table DCM_DEMO_1{{env_suffix}}.{{team_name}}.PRODUCTS(
        ITEM_NAME varchar,
        ITEM_ID varchar,
        ITEM_CATEGORY array
    )
    data_metric_schedule = 'TRIGGER_ON_CHANGES';

    {% if team_name == 'HR' %}
        define table DCM_DEMO_1{{env_suffix}}.{{team_name}}.EMPLOYEES(
            NAME varchar,
            ID int
        )
        comment = 'This table is only created in HR';
    {% endif %}

    -- use dictionary booleans to deploy optional infrastructure
    {% if team.needs_sandbox_schema | default(false) %}
        define schema DCM_DEMO_1{{env_suffix}}.{{team_name}}_SANDBOX
            comment = 'Sandbox schema defined via dictionary flag'
            data_retention_time_in_days = 1;
    {% endif %}

{% endfor %}
```
