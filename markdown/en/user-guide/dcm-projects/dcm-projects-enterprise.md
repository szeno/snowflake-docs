# Architectural recommendations for DCM Projects

This topic provides architectural recommendations for organizing DCM Projects definitions into project folders and deployment targets. It also
explains how to work with multiple environments. For collaboration workflows, see
[Collaboration and CI/CD for DCM Projects](/user-guide/dcm-projects/dcm-projects-cicd).

## Project folders and deployment targets

A project folder contains a `manifest.yml` file and a set of definitions under `sources/definitions/`. The manifest maps each target to a
DCM project object in a Snowflake account. Each target specifies the owner role for that object and can select a templating configuration.
The same set of definitions can therefore support several deployments. For more information, see
[Project targets](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-targets).

The following table summarizes how shared definitions and deployment boundaries affect the choice of structure:

| Structure | When it fits | Characteristics | Example |
| --- | --- | --- | --- |
| Option A: One project folder with one target | Most objects share an owner role, and the definitions are evaluated once or repeated for a small set of similar resources. Up to approximately 20 template iterations is a rule of thumb when the generated infrastructure is managed together. | A full `PLAN` or `DEPLOY` operation evaluates all definitions and loop iterations together. `PLAN DELTA` evaluates only changed definitions and their downstream dependencies. DCM Projects resolves dependencies within one deployment. | A platform team uses one template to create the same database structure for 20 regional teams. |
| Option B: One project folder with multiple targets | Deployments share most definitions but need different owner roles or independent deployment operations. | Targets share definitions and select their own templating configurations. Independent targets can be planned and deployed concurrently, with failures handled separately. Template changes are maintained in one place. | A platform team manages 100 or more tenants, each with a coexisting production target that supplies its namespace and other variables. |
| Option C: Separate project folders, each with its own targets | Teams maintain mostly different definitions. Dependencies across deployment boundaries are limited or explicitly coordinated. | Each folder has its own manifest and definitions. Teams maintain and deploy their definitions independently, while coordinating any dependencies across targets. | Marketing and finance maintain separate pipelines and serving layers with different definitions and ownership. |

Expand

Show lessSee more

![Three project structures: Option A uses one project folder with one target, Option B uses one project folder with multiple targets, and Option C uses separate project folders, each with its own targets.](/static/images/dcm-projects/dcm-project-architecture-options.png)

The following sections provide more detail about options A, B, and C. You can also combine these options, for example, to deploy templated
infrastructure for multiple teams within each tenant across production and non-production environments. For a pattern that lets
projects with different definitions share common code, see [Shared code across projects in one folder](#label-dcm-sharing-code-across-projects).

### Option A: One project folder with one target

One target can deploy a set of definitions once or render a parameterized template in a loop. Each full `PLAN` or `DEPLOY` operation
evaluates the definitions and all loop iterations together, allowing DCM Projects to resolve dependencies within that deployment. `PLAN DELTA`
evaluates only changed definitions and their downstream dependencies. For more information, see
[Plan only changed definitions](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-plan-delta).

For example, a platform team provides a database for each regional team:

- Each region requires mostly the same infrastructure, including schemas and landing tables.
- The template also defines roles and a warehouse for each region.
- Additional regions are expected over time.
- Template changes, such as adding a read-only role, apply to all regions.

The platform team can maintain one set of definitions and use a Jinja loop for the regional teams listed in a templating configuration in the
manifest. As a rule of thumb, up to approximately 20 iterations can remain in one target when most objects share an owner role and the
generated infrastructure is managed together. This is an architectural guideline rather than a product limit.

### Option B: One project folder with multiple targets

One project folder can also define multiple coexisting targets. Targets can represent tenants, regional teams, or isolated developer
environments in addition to shared development, staging, or production environments.

For example, a platform team serving 100 or more tenants can maintain one set of definitions and give each tenant its own target. Each target
selects a templating configuration that supplies the tenant’s namespace and other variables. Independent deployments use distinct
DCM project objects and distinct names for the managed objects within the same account.

This structure provides the following capabilities:

- Changes to shared definitions are maintained in one place.
- Each target can specify a different owner role through `project_owner`.
- Each target can be planned and deployed independently, so a failure in one deployment doesn’t require stopping the others.
- Independent targets can be planned and deployed concurrently, which can reduce the total time to apply changes across tenants.

The same structure also lets isolated developer environments coexist with production. The following figure shows one manifest and one set
of definition files in Git. The manifest defines four targets, and each target maps to its own DCM project object:

![One manifest and definitions folder in Git with four targets. Developer A creates the projects DEV_A1 and DEV_A2, and developer B creates DEV_B, all with the DEVELOPER role. A service user with the PROD_DEPLOYER role creates the PROD project. Each project deploys definitions from its own Git branch and manages its own instance of the templated SALES table.](/static/images/dcm-projects/dcm-project-targets-shared-definitions.png)

- Targets `DEV_A1`, `DEV_A2`, and `DEV_B` are development targets. Each references its own DCM project object owned by the
  `DEVELOPER` role, and they all select the `DEV` templating configuration. Developer A creates the projects `DEV_A1` and `DEV_A2`, for
  example, to work on two changes in parallel, and developer B creates `DEV_B`.
- Target `PRODUCTION` references the project `PROD`, which is owned by the `PROD_DEPLOYER` role, and selects the `PROD` templating
  configuration. A service user, such as a CI/CD pipeline, creates and deploys this project. As long as developers aren’t granted the
  `PROD_DEPLOYER` role, they can’t deploy to production through the shared manifest.

All four projects reference the same manifest and the same templated table definition, `DEFINE TABLE SALES{{env_suffix}}`. Each target
deploys the definitions from a different Git branch: the development targets from their own branches and the production target from
`MAIN`. Each project deploys and manages its own instance of the table: `SALES_DEV_A1`, `SALES_DEV_A2`, and `SALES_DEV_B` in
development, and `SALES` in production. Because the development targets share the `DEV` configuration, each developer supplies a distinct
`env_suffix` value as a runtime variable override when running `PLAN` or `DEPLOY`. The asterisk after `DEV` in the figure marks this
override.

Because each instance has a distinct name and is managed by a different project, the instances coexist in the same account, and a
`DEPLOY` operation on one target doesn’t change the objects that another target manages. For more information, see
[Environment isolation and object naming](#label-dcm-multiple-environments) and [Independent development in a shared environment](/user-guide/dcm-projects/dcm-projects-cicd#label-dcm-collaboration).

### Option C: Separate project folders, each with its own targets

Separate project folders let teams maintain different sets of definitions, each with its own manifest and targets. This fits object groups
with limited dependencies between them, such as marketing and finance teams with separate pipelines and serving layers. Splitting a very
large set of definitions along these boundaries can also reduce the scope of each `PLAN` and `DEPLOY` operation.
For an example repository layout, see
[Create a DCM project folder](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-files).

Each DCM project object has one owner role that can deploy its defined objects. Grants allow granular access to individual managed objects.
When different teams are responsible for maintaining and deploying different definitions, separate project folders can reflect those
responsibilities.

For example, a platform administrator provides infrastructure that a team administrator builds on:

- The platform administrator deploys a database and a warehouse, creates a team administrator role, and grants it the required privileges.
- Those privileges allow creation of a defined set of object types in the database and access to a defined set of account-level integrations.
- The platform administrator also grants the team administrator the privilege to create DCM project objects inside the database.
- The team administrator maintains a separate project folder and targets for team-owned definitions. These definitions organize schemas and
  dynamic tables, configure refresh frequencies, and manage granular access for team members.

The platform-managed infrastructure must exist before the team administrator deploys definitions that depend on it. Dependencies across
these targets require explicit coordination of deployment order.

If a separate governance project transfers `OWNERSHIP` of an object, that project must also define the other privilege grants on the
ownership-transfer target. For more information, see
[OWNERSHIP grants](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-grant-ownership).

Separate project folders can also become easier to maintain when instances of a shared template diverge. As differences accumulate and
templating conditions increase, independently maintained definitions can be easier to read than a shared template with many exceptions.

### Shared code across projects in one folder

When several projects maintain mostly different definitions but need some common code, such as macros or a standard set of schemas and
audit tables, it’s possible to keep them in one project folder. This pattern combines options B and C. Each project becomes its own target
in one `manifest.yml` file and references its own DCM project object. Jinja conditions then determine which definitions each target
renders. Shared code is maintained in one place, while each project keeps its own owner role and its own `PLAN` and `DEPLOY` operations.

This pattern relies on templating conditions to separate the projects within one folder, which comes with trade-offs described at the end
of this section. Review them before choosing this pattern over separate project folders as described in Option C.

In this pattern, the definitions are organized into one folder for shared code and one folder for each project:

Copy code

```
sources/
  ├── definitions/
  │   ├── shared/
  │   │   └── base.sql
  │   ├── project_a/
  │   │   └── ingest.sql
  │   └── project_b/
  │       └── reporting.sql
  └── macros/
      └── shared_macros.sql
```

Since the target name is not a templating variable, each templating configuration sets a variable identifying its project:

Copy code

```
manifest_version: 2
type: DCM_PROJECT

targets:
  PROJECT_A:
    account_identifier: MYORG-MYACCOUNT
    project_name: DCM_ADMIN.PROJECTS.PROJECT_A
    project_owner: PROJECT_A_DEPLOYER
    templating_config: PROJECT_A

  PROJECT_B:
    account_identifier: MYORG-MYACCOUNT
    project_name: DCM_ADMIN.PROJECTS.PROJECT_B
    project_owner: PROJECT_B_DEPLOYER
    templating_config: PROJECT_B

templating:
  configurations:
    PROJECT_A:
      project: A
      db: PROJECT_A_DB

    PROJECT_B:
      project: B
      db: PROJECT_B_DB
```

Definitions in `shared/` have no condition, so they render for every target. They can use the variables of the selected configuration and
call shared macros. In the following example, the `audit_table` macro is defined in `sources/macros/shared_macros.sql`:

Copy code

```
DEFINE DATABASE {{ db }};

DEFINE SCHEMA {{ db }}.CORE;

{{ audit_table(db ~ '.CORE.AUDIT_LOG') }}
```

Project-specific definitions can be limited to their own target in one of two ways, described in the following sections.

#### Condition at the top of each project-specific file

With this approach, each definition file that is not shared is wrapped in a condition that renders it only for its own project:

Copy code

```
{% if project == 'A' %}

  DEFINE TABLE {{ db }}.CORE.RAW_ORDERS (
    ORDER_ID INT,
    AMOUNT NUMBER(10,2)
  );

  DEFINE ...

{% endif %}
```

When you plan or deploy target `PROJECT_B`, every file in `project_a/` renders empty, and DCM Projects compiles and plans only the shared
definitions and the definitions for project B. Each file remains a regular definition file, and the condition at the top shows which
project it belongs to.

Note

To check which definitions a target includes, run `PLAN` with output saving enabled and review the rendered definitions in the `out/`
folder. Files that a condition excludes render empty. For how to save the output and where to find it, see
[The `/out/` subfolder](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-out-folder).

#### Project code in macros with one dispatching definition

Instead of a condition in each file, you can define each project’s objects inside macros under `sources/macros/`. A project’s objects can
be split across several macros and macro files. The following example shows one macro for project A:

Copy code

```
{% macro project_a_objects() %}

  DEFINE TABLE {{ db }}.CORE.RAW_ORDERS (
    ORDER_ID INT,
    AMOUNT NUMBER(10,2)
  );

  DEFINE ...

{% endmacro %}
```

A single definition file then calls the macros for the selected project. If a project uses several macros, this file calls each of them,
or one macro calls the others:

Copy code

```
{% if project == 'A' %}
  {{ project_a_objects() }}

{% elif project == 'B' %}
  {{ project_b_objects() }}

{% endif %}
```

All project conditions live in one file, and a macro that isn’t called renders nothing, so project code can’t render for the wrong target
by accident. In exchange, every object definition sits inside a macro, and every new macro must be called from the dispatching definition or from a macro that it calls.

#### Combine shared code with multiple environments

Sharing code across projects is independent of deploying one project to several environments. Each target and its templating
configuration represent one combination of project and environment. If each project needs development and production instances, define a
target and a templating configuration for every combination, for example `PROJECT_A_DEV`, `PROJECT_A_PROD`, `PROJECT_B_DEV`, and
`PROJECT_B_PROD`. Configurations don’t inherit values from each other, so each configuration sets both the project variable and the
environment-specific values. Values that are the same for every combination can go in `defaults`.

The following example shows the targets and configurations for project A and B:

Copy code

```
targets:
  PROJECT_A_DEV:
    account_identifier: MYORG-MYACCOUNT_DEV
    project_name: DCM_ADMIN.PROJECTS.PROJECT_A
    project_owner: PROJECT_A_DEPLOYER
    templating_config: PROJECT_A_DEV

  PROJECT_A_PROD:
    account_identifier: MYORG-MYACCOUNT_PROD
    project_name: DCM_ADMIN.PROJECTS.PROJECT_A
    project_owner: PROJECT_A_DEPLOYER
    templating_config: PROJECT_A_PROD

  PROJECT_B_DEV:
    account_identifier: MYORG-MYACCOUNT_DEV
    project_name: DCM_ADMIN.PROJECTS.PROJECT_B
    project_owner: PROJECT_B_DEPLOYER
    templating_config: PROJECT_B_DEV

  PROJECT_B_PROD:
    account_identifier: MYORG-MYACCOUNT_PROD
    project_name: DCM_ADMIN.PROJECTS.PROJECT_B
    project_owner: PROJECT_B_DEPLOYER
    templating_config: PROJECT_B_PROD

templating:
  configurations:
    PROJECT_A_DEV:
      project: A
      db: PROJECT_A_DB_DEV

    PROJECT_A_PROD:
      project: A
      db: PROJECT_A_DB

    PROJECT_B_DEV:
      project: B
      db: PROJECT_B_DB_DEV

    PROJECT_B_PROD:
      project: B
      db: PROJECT_B_DB
```

#### Every target uploads the files of all projects

Conditions reduce what DCM Projects renders, compiles, and plans for each target. Snowflake CLI still uploads `manifest.yml` and all files under
`sources/` for every target, including the files of other projects. This has the following consequences:

- Each project’s deployment artifacts include the definition files of all other projects in the folder. Users with access to one project’s
  artifacts can therefore read the definitions of the other projects. If projects must keep their definitions confidential from each other,
  use separate project folders as described in Option C.
- A change to a file in `shared/` affects every target. After changing shared definitions, plan each target to review its changes.

Dependencies between projects in a shared folder follow the same rules as Option C: DCM Projects resolves dependencies within one target’s
deployment, and deployment order across targets requires explicit coordination.

## Considerations across architecture options

The following guidance applies across the architecture options:

- Separation of concerns and deployment dependencies are primarily considerations for Option C and for projects that share one folder.
- Environment isolation and object naming apply to all three options.
- [Independent development](/user-guide/dcm-projects/dcm-projects-cicd#label-dcm-collaboration) applies when developers create parallel instances of Option A or B. The object-naming requirements also apply
  when developers independently maintain Option C projects in the same account.

### Separation of concerns and deployment dependencies

One set of definitions can cover both infrastructure and governance definitions, allowing DCM Projects to resolve their dependencies and determine the execution order for `PLAN` and `DEPLOY`.

When business or organizational requirements call for separate ownership or deployment processes, one common scenario is a separate project
folder for grants, policies, and role privileges. Its definitions reference objects managed by the infrastructure definitions, creating a primarily
one-directional dependency. The infrastructure target must be deployed first so that the objects exist, followed by the access-privilege
target that applies grants to those objects.

Dependencies across these targets require manual coordination. Keeping the definitions together under one target avoids this coordination
when separate ownership or deployment isn’t required.

Keep cross-project dependencies acyclic so that the projects have a valid deployment order. A downstream `PLAN` can’t validate references
to upstream changes that haven’t been deployed. For example, separating tables and views from functions and procedures can create a cycle
if each project references objects managed by the other. DCM Projects resolves dependencies within one deployment, but it doesn’t orchestrate
dependencies across projects.

### Environment isolation and object naming

For a diagram of a typical workflow for deploying a DCM project to multiple environments, see
[Collaboration and CI/CD for DCM Projects](/user-guide/dcm-projects/dcm-projects-cicd).

#### Separate accounts compared with separate databases

Snowflake generally recommends setting up each environment as a separate Snowflake account. This ensures complete separation of production
infrastructure from any experimental development and guarantees restricted developer access to production data.

However, with careful access management, you can successfully manage multiple environments on one Snowflake account. This is easier when the
databases are clearly separated and can become more challenging when account-level objects and integrations are involved.

The benefit of a single-account setup is the ability to easily clone production infrastructure and data for testing alterations before
deploying those changes to production. However, copying parts of production data and infrastructure to a different account, for example,
through org-internal data shares, can be more costly.

#### Distinct object names across environments

Distinct object names for each environment are a requirement for single-account setups, for example, to keep `EMEA_DB` and `EMEA_ADMIN`
separate from `EMEA_DB_DEV` and `EMEA_ADMIN_DEV`. Snowflake also recommends this practice for multi-account setups. Templated names
allow for multiple instances of entities like `EMEA_DB_DEV_JOHN` and `EMEA_DB_DEV_MARY` to coexist for independent development and to
quickly create and destroy isolated developer environments to test different solutions.

This applies to all account-level objects, such as databases, roles, and warehouses. You then need to apply these templated names to all
fully qualified names of nested objects.
