# Enterprise use cases for DCM Projects

This topic covers how to use DCM Projects in enterprise environments, such as managing multiple projects, working with multiple environments, and
collaborating on projects.

## When to use multiple DCM projects

When deciding if and how to split a DCM project into multiple projects, consider ownership and templating.

### Ownership

Each project has one owner role that can deploy all defined objects. Grants allow granular access management for individual objects inside
the project. However, if different groups of users are responsible for deploying changes to a project, it generally makes sense to
split a DCM project accordingly.

The following is an example scenario:

- The platform administrator deploys a database and a warehouse, creates the team administrator role, and
  grants CREATE privileges to the team administrator for a defined set of object types inside that database, as well as access to a defined
  set of account-level integrations.
- The team administrator can now decide how to organize schemas and dynamic tables inside that database, fine-tune refresh frequencies, and grant more
  granular read access to individual team members.

The following is a solution:

- The platform administrator deploys the high-level infrastructure for the team and grants the team administrator the privilege to create DCM project projects
  inside their database.
- The team administrator can now also benefit from DCM Projects by creating one or more projects inside the team database to manage tables and grants to team members.

### Template variables

If a DCM project defines a range of objects that are and should remain mostly similar, it is generally more convenient to define them once
as a parameterized template.

The following is an example scenario:

- The platform team deploys a database for each regional team in the organization.
- New regions are expected to be added over time.
- All regions require mostly the same setup of schema, landing tables, roles, and warehouse.
- Changes in this database template should be applied to all teams, for example, adding a read-only role.

The following is a solution:

- You can execute a single set of definitions in a loop for each regional team listed in the manifest profile.

When more elements of this template start to diverge and the number of templating conditions increases, it can become easier to read and
maintain separate DCM projects with their individual object definitions.

## Use DCM Projects with multiple environments

The following diagram shows a typical workflow for deploying a DCM project to multiple environments.

![Reviewing and merging changes](/static/images/dcm-projects/dcm-project-deployment-multi-environments.png)

### Separate accounts compared with separate databases

Snowflake generally recommends setting up each environment as a separate Snowflake account. This ensures complete separation of production
infrastructure from any experimental development and guarantees restricted developer access to production data.

However, with careful access management, you can successfully manage multiple environments on one Snowflake account. This is easier when the
databases are clearly separated and can become more challenging when account-level objects and integrations are involved.

The benefit of a single-account setup is the ability to easily clone production infrastructure and data for testing alterations before
deploying those changes to production. However, copying parts of production data and infrastructure to a different account, for example,
through org-internal data shares, can be more costly.

### Impact on DCM project templating

Distinct object names for each environment are a requirement for single-account setups, for example, to keep `EMEA_DB` and `EMEA_ADMIN`
separate from `EMEA_DB_DEV` and `EMEA_ADMIN_DEV`. Snowflake also recommends this practice for multi-account setups. Templated names
allow for multiple instances of entities like `EMEA_DB_DEV_JOHN` and `EMEA_DB_DEV_MARY` to coexist for independent development and to
quickly create and destroy sandbox environments to test different solutions.

This applies to all account-level objects, such as databases, roles, and warehouses. You then need to apply these templated names to all
fully qualified names of nested objects.

## Collaborate on DCM Projects

### Shared development environment

Multiple developers commonly share the same development account to build and iterate on data products in parallel. However, if multiple
users work on the same project in parallel, their PLAN and DEPLOY operations can cause conflicts if they don’t use templating to create
unique names.

The following is an example scenario:

- Users A and B are both testing changes to different parts of project `TASTYBYTES`, which already runs on production.
- Each user creates their own feature branch of `prod-main` and starts editing the entity definitions.
- Each user creates their own DCM project (`TASTYBYTES_DEV_A` and `TASTYBYTES_DEV_B`).
- If both users deploy with the same `DEV` templating configuration to the same Snowflake account, then:

  - User A deploys the new `_DEV` instance of all entities first including the `TB_WAREHOUSE_DEV`, so they are managed by their project `TASTYBYTES_DEV_A`.
  - Once user B tries to deploy one or more of the same object names (for example, `TB_WAREHOUSE_DEV`), the deployment for
    `TASTYBYTES_DEV_B` fails because the warehouse is already managed by `TASTYBYTES_DEV_A`.
- Alternatively, both users could own and deploy from the same project `TASTYBYTES_DEV`, each pointing at their different branch folders.
  This would lead to user B overwriting all deployed entity versions of user A and vice versa.

The following is a solution:

- When working on the same development environment in parallel, Snowflake recommends always using distinct entity names to avoid conflicting
  object names. You can achieve this by templating database, warehouse, and role names with unique suffixes. For example, `DEFINE DATABASE DCM_PROJECT_{{db}};`
- When using configuration profiles like the following example, multiple developers can all use the `DEV` configuration to set their warehouses
  to `X-SMALL`.
- To avoid conflicting database names, developers should overwrite the `db` variable with a unique string. This could be based on
  user names, feature names, ticket numbers, or branch names.

  For example, `snow dcm deploy --variable "db='DEV_JS'"` would resolve to a unique `DEFINE DATABASE DCM_PROJECT_DEV_JS;` operation.

  Copy code

  ```
  templating:
    defaults:
   wh_size: "X-SMALL"

    configurations:
   DEV:
     db: "DEV"

   TEST:
     db: "TEST"

   PROD:
     db: "PROD"
     wh_size: "LARGE"
  ```
- You can apply the same templating solution when one developer works on multiple projects.
- The following is an example of a scalable project setup for teams.

  When you start a new Jira ticket, complete the following steps:

  1. `CREATE GIT BRANCH {{ticket_number}} FROM REPO`
  2. `CREATE DCM PROJECT {{ticket_number}}`
  3. `EXECUTE DCM PROJECT {{ticket_number}} PLAN USING CONFIGURATION "DEV" (db => '{{ticket_number}}') FROM @REPO/BRANCHES/{{ticket_number}}/DCM_PROJECT/`
