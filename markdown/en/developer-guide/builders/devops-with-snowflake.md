# DevOps with Snowflake

Snowflake provides tools and practices for managing your Snowflake environments as code, validating changes before they reach
production, and automating deployments through CI/CD pipelines.

## What is DevOps with Snowflake?

DevOps with Snowflake brings software engineering best practices to data infrastructure management. The core principles are:

- **Define as code.** Declare the desired state of your Snowflake objects in version-controlled files. The tool you choose compares
  those definitions against the current state and applies the necessary changes (create, alter, or drop) to reach it.
- **Validate before you deploy.** Preview proposed changes in a plan step before applying them to your account. Review creates, alters,
  and drops, then deploy when you’re confident the changes are correct.
- **Automate with CI/CD.** Integrate Snowflake into your existing CI/CD pipelines so that deployments are triggered by pull requests,
  merges, or scheduled runs rather than manual steps.

Snowflake supports two declarative tools for managing objects as code, and they cover different layers:

- [DCM Projects](/user-guide/dcm-projects/dcm-projects-overview) (Database Change Management Projects) are the Snowflake-native
  option for the objects inside your databases. They unify declarative object management, plan-then-deploy validation,
  multi-environment targeting, and CI/CD automation into a single workflow.
- The [Snowflake Terraform provider](/user-guide/terraform) covers account-level objects and any infrastructure you manage outside
  Snowflake, alongside your other Terraform providers.

The two are complementary, and many organizations use both. For guidance on which to use where, see
[Choosing between DCM Projects and Terraform](#label-builder-devops-dcm-vs-terraform).

## Define your Snowflake objects as code

### DCM Projects

[DCM Projects](/user-guide/dcm-projects/dcm-projects-overview) (Database Change Management Projects) provide a declarative,
infrastructure-as-code approach to managing your Snowflake environment, and are the recommended option for the objects inside your
databases. Instead of writing imperative scripts that specify each step, you define the desired target state of your objects.
Snowflake compares those definitions against the current state and determines the necessary changes.

A DCM project consists of:

- A **manifest file** (`manifest.yml`) that specifies deployment targets, owner roles, and templating configurations for each
  environment.
- **Definition files** (SQL files under `sources/definitions/`) that contain DEFINE statements for your Snowflake objects, GRANT
  statements for access control, and ATTACH statements for data quality expectations.

The following example shows a definition file that creates infrastructure for multiple teams using Jinja2 templating:

Copy code

```
{% for team in teams %}

  DEFINE DATABASE {{team.name}}_DB;

  DEFINE WAREHOUSE {{team.name}}_WH
    WITH
      warehouse_size = '{{team.wh_size}}'
      auto_suspend = 300;

  DEFINE ROLE {{team.name}}_ADMIN;

  GRANT OWNERSHIP ON DATABASE {{team.name}}_DB TO ROLE {{team.name}}_ADMIN;
  GRANT OWNERSHIP ON WAREHOUSE {{team.name}}_WH TO ROLE {{team.name}}_ADMIN;

{% endfor %}
```

For complete documentation on DCM Projects, including how to set up your project files, manage multiple environments, and automate
deployments, see [Snowflake DCM Projects](/user-guide/dcm-projects/dcm-projects-overview).

### Snowflake Terraform provider

The [Snowflake Terraform provider](/user-guide/terraform) lets you manage Snowflake objects with
[HashiCorp Terraform](https://www.terraform.io/), the tool many teams already use for their cloud infrastructure. You declare
resources in Terraform configuration files, run a plan to preview the changes, and then apply them to converge your account to
the declared state.

The provider runs outside Snowflake and manages objects by issuing SQL statements, so the changes it makes appear in your
account’s [query history](/user-guide/ui-snowsight-activity). Because it’s one of many Terraform providers, you can manage
Snowflake objects and non-Snowflake resources in the same configuration: for example, a cloud storage bucket and the Snowflake
storage integration that reads from it.

For installation, versioning, preview features, and support boundaries, see [Snowflake Terraform provider](/user-guide/terraform).

### Choosing between DCM Projects and Terraform

DCM Projects and Terraform solve the same problem at different layers, and many organizations use both: Terraform for the
account-level layer that platform teams own, and DCM Projects for the objects inside databases that data engineers own. Both
manage roles and grants, so at that layer the choice depends on which team owns them.

The following table compares the two tools:

| Consideration | DCM Projects | Snowflake Terraform provider |
| --- | --- | --- |
| Typical scope | Objects inside a database, such as schemas, tables, views, dynamic tables, and tasks, plus databases, warehouses, and roles | Account-level objects, such as users, integrations, and policies |
| Resources outside Snowflake | Not supported; Snowflake objects only | Supported through other Terraform providers in the same configuration |
| Authoring language | SQL `DEFINE` statements, with Jinja2 templating built in | Terraform configuration language (HCL), with modules for reuse |
| Where it runs | Inside Snowflake, executed by your account | Outside Snowflake, wherever you run Terraform |
| Multiple environments | Deployment targets and configuration profiles in `manifest.yml` | Terraform modules and per-environment pipelines |

Expand

Show lessSee more

Whichever tool you choose, confirm that it covers the object types you need. See
[Supported object types in DCM Projects](/user-guide/dcm-projects/dcm-projects-supported-entities) for DCM Projects and the
[provider documentation](https://registry.terraform.io/providers/snowflakedb/snowflake/latest/docs) for Terraform.

Note

If you already have a Terraform setup that works, you don’t need to replace it. You can adopt DCM Projects alongside it for
schema-level objects. Manage each object with only one tool, so that the two don’t compete to reconcile the same state.

### dbt Projects on Snowflake

dbt Projects do a different job from DCM Projects and Terraform: they manage SQL transformations rather than the declared state of
your objects, so you typically use them alongside one of the tools above.

[dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake) let you deploy and run
[dbt Core](https://www.getdbt.com/) projects as native Snowflake objects. You define SQL transformations in dbt models, deploy them
as a versioned DBT PROJECT object, and execute them with Snowflake SQL or the Snowflake CLI. You can schedule runs with Snowflake tasks
and integrate deployment into CI/CD pipelines.

For more information, see [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake).

### Alternative: CREATE OR ALTER with versioned scripts

For individual object changes outside of a DCM project or a Terraform configuration, you can use the
[CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter) command, which creates the object or alters it to match the definition specified by the
command. By using this command from a versioned file in a remote repository, you can roll back changes to a previous version by
executing a previous version of the file.

SQLPython

Copy code

```
CREATE OR ALTER TABLE vacation_spots (
  city VARCHAR,
  airport VARCHAR,
  avg_temperature_air_f FLOAT,
  avg_relative_humidity_pct FLOAT,
  avg_cloud_cover_pct FLOAT,
  precipitation_probability_pct FLOAT
) data_retention_time_in_days = 1;
```

Copy code

```
from snowflake.core import Root
from snowflake.core.table import PrimaryKey, Table, TableColumn

my_table = root.databases["my_db"].schemas["my_schema"].tables["vacation_spots"].fetch()
my_table.columns.append(TableColumn(name="city", datatype="varchar", nullable=False))
my_table.columns.append(TableColumn(name="airport", datatype="varchar", nullable=False))
my_table.columns.append(TableColumn(name="avg_temperature_air_f", datatype="float", nullable=False))
my_table.columns.append(TableColumn(name="avg_relative_humidity_pct", datatype="float", nullable=False))
my_table.columns.append(TableColumn(name="avg_cloud_cover_pct", datatype="float", nullable=False))
my_table.columns.append(TableColumn(name="precipitation_probability_pct", datatype="float", nullable=False))

my_table_res = root.databases["my_db"].schemas["my_schema"].tables["vacation_spots"]
my_table_res.create_or_alter(my_table)
```

Note

You can also use the [Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview) and
[Snowflake CLI](/developer-guide/snowflake-cli/index) to manage Snowflake resources. If you prefer to do your data engineering work
in Python, Snowflake’s first-class Python API enables you to do the same resource management in the language you are most productive in.

## Validate and preview changes

Before deploying changes to your Snowflake account, you can preview the proposed modifications to verify they match your intent.

### Plan with DCM Projects

DCM Projects use a plan-then-deploy model. The PLAN command compares your definition files against the current state of your account
and produces a list of proposed changes without modifying anything.

You can run a plan using the Snowflake CLI:

Copy code

```
snow dcm plan --target PROD
```

Or using SQL:

Copy code

```
EXECUTE DCM PROJECT my_db.my_schema.my_project
  PLAN
  USING CONFIGURATION PROD
FROM
  '@my_stage/my_project/';
```

Review the output to confirm the expected creates, alters, and drops before proceeding to deploy.

### Plan with Terraform

Terraform follows the same plan-then-apply model: a plan reports the intended creates, changes, and destroys, and you apply them in
a separate step.

For objects both tools manage, a DCM plan detects more. DCM plans against internal object state inside Snowflake, while Terraform
reads object state through public SQL, so a change to an attribute that SHOW and DESCRIBE don’t return won’t appear in its plan. In
return, every statement Terraform runs lands in your query history.

For more information, see [Snowflake Terraform provider](/user-guide/terraform).

## Automate deployment with CI/CD

You can integrate Snowflake into your CI/CD pipelines so that deployments are triggered automatically by events such as
pull request merges, branch pushes, or scheduled runs. A typical Snowflake pipeline progresses through three stages:

- **Validate on pull request.** Compute the proposed changes against the target environment without modifying anything,
  and post the output for reviewers to confirm intent before merging.
- **Deploy on merge.** Apply the validated changes to the target environment. Use a separate service user and target
  per environment so that promotion from dev to prod is a configuration change, not a code change.
- **Verify after deployment.** Refresh derived data and run expectation checks to confirm the deployment produced the
  results you expect.

Snowflake publishes and maintains first-party integrations for the following CI/CD platforms. Each integration installs
Snowflake CLI on the runner and configures authentication, with workload identity federation (OIDC) recommended so that no
long-lived secrets are stored in your CI system.

| Integration | Status | Reference |
| --- | --- | --- |
| GitHub Action | Generally available | [Snowflake CLI GitHub Action](/developer-guide/snowflake-cli/cicd/github-action) |
| GitLab CI/CD Component | Public preview | [Snowflake CI/CD Component for GitLab](/developer-guide/snowflake-cli/cicd/gitlab-component) |
| Azure DevOps Extension | Public preview | [Snowflake CLI Azure DevOps Extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension) |

Expand

Show lessSee more

For any CI platform that can run a shell command, you can also install Snowflake CLI directly. For setup instructions and the
common Snowflake-side configuration, see [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd).

Because these integrations install Snowflake CLI, they cover the `snow` commands that drive DCM Projects. If you manage objects with the
Terraform provider, run your plan and apply steps with your existing Terraform tooling. The three stages above are the same either
way, and both tools can run in the same pipeline as long as each object is managed by only one of them.

## Manage environments

By maintaining separate environments for development, test, and production, your teams can isolate development activities from the
production environment, which reduces the chance of unintended consequences and data corruption.

Both tools support this, with different mechanics. DCM Projects use deployment targets and configuration profiles in the manifest
file. Terraform packages resources into modules and supplies per-environment values from a separate pipeline for each environment;
for more information, see [Snowflake Terraform provider](/user-guide/terraform).

### Connection profiles for environment targeting

With DCM Projects, you can define multiple deployment targets in your `manifest.yml` file. Each target maps to a specific Snowflake
account (or database), project object, owner role, and templating configuration. The same definition files can deploy to all environments
with environment-specific settings applied through configuration profiles.

Copy code

```
targets:
  DEV:
    account_identifier: MYORG-MYACCOUNT_DEV
    project_name: MY_DB.MY_SCHEMA.MY_PROJECT_DEV
    project_owner: DEV_DEPLOYER
    templating_config: DEV

  PROD:
    account_identifier: MYORG-MYACCOUNT_PROD
    project_name: MY_DB.MY_SCHEMA.MY_PROJECT_PROD
    project_owner: PROD_DEPLOYER
    templating_config: PROD

templating:
  configurations:
    DEV:
      wh_size: "X-SMALL"
    PROD:
      wh_size: "LARGE"
```

For enterprise patterns such as multi-project setups and team collaboration, see
[Enterprise use cases for DCM Projects](/user-guide/dcm-projects/dcm-projects-enterprise).

### Advanced: Jinja parameterization for custom scripts

DCM Projects natively support Jinja2 templating in definition files. You can use template variables, loops, conditions, macros, and
dictionaries to make your definitions reusable across environments. Variable values come from configuration profiles in the
`manifest.yml` or from runtime overrides.

For details on DCM templating, see [DCM Projects files and templates](/user-guide/dcm-projects/dcm-projects-files).

You can also parameterize standalone SQL scripts (outside of DCM Projects) using Jinja2 with
[EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from). The Snowflake CLI allows you to pass environment variables to Python
scripts as well.

To change a deployment target, for example, you replace the name of the target database with a Jinja variable such as
`{{ environment }}` in SQL scripts, or an environment variable in Python scripts. This technique is shown in the following SQL
and Python code examples:

SQLPython

Copy code

```
CREATE OR ALTER TASK {{ environment }}.my_schema.my_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '60 minute'
  AS select pi();
```

Copy code

```
import os
from snowflake.core import Root, CreateMode
from datetime import timedelta
from snowflake.core.task import Task

my_task = Task(
    name="my_task",
    warehouse="my_warehouse",
    definition="select pi()",
    schedule=timedelta(minutes=60)
)
root = Root(Session.builder.getOrCreate())
tasks = root.databases[os.environ["environment"]].schemas["my_schema"].tasks
tasks.create(my_task, mode=CreateMode.or_replace)
```

## Getting started

To get started with DCM Projects, see [Snowflake DCM Projects](/user-guide/dcm-projects/dcm-projects-overview) for a complete overview of the feature,
including how to set up your project files, configure environments, and deploy changes.

For sample projects, CI/CD templates, and quickstarts, see the
[snowflake-labs DCM repository](https://github.com/Snowflake-Labs/snowflake_dcm_projects).

To follow a step-by-step tutorial, try the
[Getting Started with Snowflake DCM Projects](https://www.snowflake.com/en/developers/guides/get-started-snowflake-dcm-projects/)
quickstart, or the
[Configure CI/CD Integrations with Snowflake](https://www.snowflake.com/en/developers/guides/configure-cicd-integrations-with-snowflake/)
CI/CD quickstart.

To get started with the Terraform provider, see [Snowflake Terraform provider](/user-guide/terraform) for installation, versioning, and support details, or try
the [Terraforming Snowflake](https://quickstarts.snowflake.com/guide/terraforming_snowflake/#0) quickstart.
