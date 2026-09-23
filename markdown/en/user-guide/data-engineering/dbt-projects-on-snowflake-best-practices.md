# Best practices for dbt Projects on Snowflake

This guide provides opinionated best practices for data engineering teams running dbt at scale on Snowflake. Each section is self-contained, so you can jump to the topic that matters most to your team.

dbt Projects on Snowflake eliminates infrastructure you’d otherwise manage yourself. There’s no Python environment to maintain, no Airflow cluster to scale, no dbt CLI version drift across developer machines. Snowflake handles the runtime, orchestration (through [tasks](/user-guide/tasks-intro)), and dbt version management natively. This lets your team focus on transformation logic and data quality rather than infrastructure operations.

## Cost optimization

Reducing warehouse compute time is one of the highest-impact best practices for teams running dbt at scale. The following patterns help you avoid unnecessary processing.

### Use incremental models for large, frequently updated tables

If your source table is large and receives regular updates, use the `incremental` materialization instead of a full table rebuild. Incremental models scan only the rows that changed since the last run, which drastically reduces the time window processed before transformation occurs.

If no new rows exist since the last run, dbt still runs the filter query to check, but the transformation itself is effectively skipped because there’s nothing to merge or insert. This consumes a fraction of the warehouse time because only the lightweight filter query runs, not the full transformation. This makes incremental models especially cost-effective for event-driven pipelines or tables with append-only patterns.

For small tables that update infrequently, a full `table` materialization is simpler and often just as fast. Use incremental models where the scan reduction provides a measurable benefit.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

### Use defer to production during development

When you run only part of your DAG during development, dbt still needs relations for any unbuilt upstream models. Use `--defer` with production state so that dbt resolves these upstream references to existing production relations instead of rebuilding the upstream models in the development target.

Snowflake Workspaces provides native defer to production controls under **Advanced options** in the execution pane. To configure this behavior, see [Defer to production during development](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-workspace-defer-production).

### Use Slim CI

When a pull request changes only a few models, deploying a tester dbt project object with automatic compilation enabled compiles the entire project. Also, running a full `dbt build` in the pipeline then compiles, runs, and tests the entire project again. Together, this extra work uses more warehouse compute as the project grows. Use Slim CI to limit validation to changed nodes and their downstream dependencies:

- Deploy the tester dbt project object with `snow dbt deploy --no-auto-compile` to skip automatic compilation during deployment.
- Pass `--state` with `--select state:modified+` to process only nodes that changed relative to prior production artifacts and their downstream dependencies. Unchanged nodes don’t consume warehouse time.
- Pass `--defer` so that references to unbuilt upstream nodes resolve to existing production relations.

Use a full `dbt build` only when you need the most thorough validation of every model and test in the project. Incremental models and Slim CI optimize different work: incremental models skip unchanged rows within a selected model, while Slim CI skips unchanged nodes in the project DAG.

For setup and examples, see [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

### Increase parallelism with threads

Configure the `threads` parameter in [`dbt_projects_profiles.yml`](#label-dbt-projects-profiles-file) or `profiles.yml` to control how many models dbt runs concurrently within a single execution. To be compatible with most Snowflake warehouses, Snowflake recommends setting your threads to 8. A higher thread count than 1 allows independent models to execute in parallel, reducing total wall-clock time for a given run.

Copy code

```
my_target:
  type: snowflake
  threads: 8
  # ...
```

Choose a thread count that matches your warehouse’s available compute capacity without causing queuing.

For more details about costs, see [Understanding costs for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-cost).

## Choosing a dbt version

Snowflake supports both dbt Core (Python-based, versions 1.x) and dbt Fusion (Rust-based, versions 2.x). For most teams, start with the latest supported dbt Core version in dbt Projects on Snowflake (1.11.x). It has the broadest Snowflake materialization and dbt package support.

If your project becomes very large (more than 5,000 models) or your team wants to future-proof for performance improvements, consider moving to dbt Fusion. Keep in mind:

- Some migration is required when moving from Core to Fusion.
- Not all dbt packages are compatible with Fusion today. Check the [dbt package hub](https://hub.getdbt.com/) for Fusion-compatible badges before upgrading.
- The most popular dbt package hub packages (`dbt_utils`, `dbt_expectations`, `dbt_project_evaluator`) are already compatible.

For the full list of supported versions and how to set account-level defaults, see [Migrate to dbt Fusion](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-fusion-migration). For Fusion migration guidance, see [Upgrading to v2.0](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v2).

## Orchestration

Snowflake [tasks](/user-guide/tasks-intro) provide native scheduling for dbt project execution without requiring external orchestrators like Airflow. Understanding the permission model is critical to setting up orchestration correctly.

### Understand the two-role model of execution

Every `EXECUTE DBT PROJECT` statement involves two roles:

1. **The calling role**: the active role of the session (or task owner role) that issues the `EXECUTE DBT PROJECT` statement. This role must have the `USAGE` privilege on the dbt project object.
2. **The profile role**: the role specified in the target in your project’s `dbt_projects_profiles.yml` or `profiles.yml`. The profile role defines what the dbt run can actually access (databases, schemas, tables, warehouses) during execution.

Both roles must have USAGE on the warehouse. The calling role must also be able to use the profile role. Operations during execution are restricted to the privileges that both roles have in common.

This two-role model applies whether you run dbt interactively (a human running `EXECUTE DBT PROJECT` in a worksheet) or through a scheduled task. The difference is:

- **Interactive execution:** Your active session role is the calling role.
- **Task execution:** The task runs as a system service with the privileges of the **task owner role** (the role that has OWNERSHIP on the task). No specific user is associated with the run.

You can simplify this setup with an `env.yml` file instead of hardcoding a role in `dbt_projects_profiles.yml` or `profiles.yml`. Define a variable such as `DBT_CURRENT_ROLE: "{{ select CURRENT_ROLE() }}"` in `env.yml`, then reference it from the profile file with `role: "{{ env_var('DBT_CURRENT_ROLE') }}"`. The profile role then resolves to the calling role on every run. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

### Use a dedicated service account

Create a dedicated service account (for example, `github_actions_service_user`), assign them narrow privileges, and use this user to create and own your tasks. This ensures:

- Task privileges are governed and auditable in one place.
- The service account role can be granted only the minimum permissions needed.
- Departing team members don’t break production scheduling.

### Align your warehouse configuration

Use the same warehouse in both your task definition and the target in `dbt_projects_profiles.yml` or `profiles.yml` to avoid waking two warehouses for a single orchestration run:

Copy code

```
-- Task warehouse matches profiles.yml warehouse
CREATE OR ALTER TASK my_db.my_schema.run_dbt_daily
  WAREHOUSE = transform_wh
  SCHEDULE = '360 minutes'
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project args='build --target prod';
```

Copy code

```
# profiles.yml
prod:
  type: snowflake
  warehouse: transform_wh
  # ...
```

If the task uses `warehouse_a` but your profile file specifies `warehouse_b`, both warehouses wake up for one run.

To keep them aligned automatically, use an `env.yml` file instead of hardcoding the warehouse. Define a variable such as `DBT_CURRENT_WH: "{{ select CURRENT_WAREHOUSE() }}"` in `env.yml`, then reference it from the profile file with `warehouse: "{{ env_var('DBT_CURRENT_WH') }}"`. The profile warehouse then matches the calling task warehouse on every run.

### Use task graphs for multi-step pipelines

Use the `AFTER` clause to chain tasks into a graph. For example, run tests after your models complete:

Copy code

```
CREATE OR ALTER TASK my_db.my_schema.test_dbt_daily
  WAREHOUSE = transform_wh
  AFTER my_db.my_schema.run_dbt_daily
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project args='test --target prod';
```

To create and manage scheduled tasks from Snowsight or SQL, see [Schedule execution of dbt project objects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).

For a comprehensive overview of orchestration options including Apache Airflow integration, see
[Understanding orchestration for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-orchestration).

## Recover from a failed execution

When a `run` or `build` fails partway through, rerunning the complete command repeats work that already succeeded. `dbt retry` can avoid a complete rerun, but it replays the previous invocation with its original arguments and selection, so you can’t review or change which resources dbt reruns.

For more control, import the failed execution’s state with [SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target), then use an explicit result selector:

Copy code

```
EXECUTE DBT PROJECT prod_database.dbt_projects.production_project
  ARGS = 'run --state ./imports/state --select result:error+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET(
      'prod_database.dbt_projects.production_project',
      'run,build'
    ) AS 'state'
  );
```

The `result:error+` selector reruns resources that errored and their downstream dependencies. For failed tests, use `1+result:fail+` to rerun the failed tests, their parent models, and downstream resources.

Use `dbt retry` when you want to replay the previous invocation without changing its arguments or selection. For production orchestration, use explicit result selectors for greater control over which resources dbt reruns. For more examples, see [Recover from a failed execution](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-failed-execution-recovery).

## Continuous integration and continuous deployment (CI/CD)

CI/CD pipelines ensure that every change to your dbt project is validated before reaching production. This is essential for teams working collaboratively on shared pipelines.

### Use CI/CD to deploy to production

Teams sometimes bypass CI/CD validation by deploying directly to a production dbt project object. Common anti-patterns include:

- Using the Git stage as a shortcut to deploy changes without creating a pull request.
- Deploying from Workspaces by doing a `git pull` and then deploying via the Workspaces UI.

These approaches should be used when deploying and testing a **dev/staging** dbt project object. But for production, always deploy through a CI/CD pipeline. Without CI validation:

- Broken models reach production undetected.
- Tests never run until after data is already corrupted.
- There’s no review gate for teammates to catch errors.

### The recommended CI/CD pattern

Use the Snowflake CLI within a CI orchestrator (such as GitHub Actions) to gate every deployment behind validation:

1. A developer opens a pull request.
2. The CI pipeline triggers and creates a **tester** dbt project object using `snow dbt deploy --no-auto-compile`.
3. The pipeline imports dbt artifacts from the latest successful production execution and runs the changed models and tests with `--state`, `--defer`, and `--select state:modified+` against an isolated dev or staging target.
4. If all selected models run successfully and all selected tests pass, the PR is mergeable.
5. On merge to main, a separate pipeline deploys to the **production** dbt project object.

This ensures that no change reaches production without CI validation. For the complete Slim CI workflow, see [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial). For a simpler workflow that runs a full build, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

### Multi-account setups

For teams with separate staging and production Snowflake accounts, CI/CD is the best pattern to manage different deployment destinations:

- **On pull request:** Deploy and test against your staging account.
- **On merge to main:** Deploy to your production account.

The Snowflake CLI supports inline connection overrides, making it straightforward to target different accounts:

Copy code

```
# During a CI job, deploy to your staging account
snow dbt deploy my_project \
  --account my_org-staging \
  --database analytics_staging \
  --role svc_dbt_role \
  --warehouse transform_wh \
  --default-target staging

# Later, in a CD job, deploy to your production account
snow dbt deploy my_project \
  --account my_org-production \
  --database analytics_prod \
  --role svc_dbt_role \
  --warehouse transform_wh \
  --default-target prod
```

### Enforce quality at the PR level

Set up branch protection rules so that pull requests can’t merge into main until all CI checks pass. This guarantees quality regardless of where the commit originated (Workspaces, local IDE, or Cortex Code Desktop).

## Environment variables

Environment variables have been part of dbt Core for years, but managing them at scale has always meant wrangling `.env` files that live on individual machines, drift out of sync, and can’t be audited. The `env.yml` file is a single, Git-versioned configuration file that Snowflake resolves before each dbt Projects on Snowflake run.

### Why env.yml matters

The `env.yml` file gives admins one place to manage configuration for the entire team:

- **Per-developer schemas:** Use `CURRENT_USER()` to automatically isolate each engineer’s work into their own schema during development.
- **Production time windows:** Use SQL functions to compute start and end timestamps at run time without an external orchestrator.
- **Secrets for private packages:** Inject Snowflake-managed secrets to authenticate against private Git repositories during `dbt deps`.
- **Multiple environments in one file:** Define dev, staging, and prod configurations together. Choose which environment is active at execution time.

### How it works

The `env.yml` file runs before dbt Core execution begins. Snowflake resolves all values (including SQL queries and secrets) first, then injects the resulting environment variables into the dbt run. Values come from your Snowflake execution context (the role, user, and warehouse of the outer session running `EXECUTE DBT PROJECT`).

Copy code

```
env_config:
  default_environment: dev
  environments:
    - name: dev
      env:
        DBT_CURRENT_SCHEMA: "{{ select CURRENT_USER() }}"
        DBT_CURRENT_ROLE: "{{ select CURRENT_ROLE() }}"
    - name: prod
      env:
        DBT_DATA_INTERVAL_START: "{{ select (DATE_TRUNC('DAY', CURRENT_TIMESTAMP()) - INTERVAL '1 DAY')::string }}"
        DBT_DATA_INTERVAL_END: "{{ select (DATE_TRUNC('DAY', CURRENT_TIMESTAMP()) - INTERVAL '1 SECOND')::string }}"
```

Values resolve highest priority first: `ENV_VARS` on `EXECUTE DBT PROJECT` (or `--env-vars` in the CLI), then shell variables (with `--use-shell-env-vars`), then the active environment in `env.yml`.

For env.yml authoring, environment selection, private Git packages, and the full reference, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Cross-project references and shared macros

As your dbt practice grows, teams often need to share macros, models, or utilities across multiple projects. Private Git packages provide the Snowflake-native solution for this.

### Why teams use cross-project references

Teams import other repositories to share code across projects instead of duplicating it, most often to:

- **Reuse utility macros:** Maintain custom materializations, audit and logging macros, and schema or naming helpers in one place instead of copying them into every project.
- **Reuse model, source, or seed definitions:** Share canonical source definitions, standard staging models, or reference data that multiple projects build on rather than redefine.
- **Build on another team’s models:** Depend on models that a different team owns and maintains.

dbt Core supports importing from either a single monorepo or separate repositories.

### How it works

Private Git packages use a Snowflake secret to authenticate against your private Git repository during `dbt deps`. The admin sets up a secret, network rule, and external access integration. Data engineers reference the private package in their `packages.yml`:

Copy code

```
packages:
  - git: "https://{{env_var('DBT_ENV_SECRET_GIT_TOKEN')}}@github.com/your-org/dbt-shared-utils.git"
    subdirectory: "macros"
    # Pin to a commit ID; a branch like main isn't recommended.
    revision: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

The `env.yml` file injects the secret as a `DBT_ENV_SECRET_` variable, which dbt uses to authenticate during package installation.

## Permissions and privileges

Understanding the separation between dbt project object permissions and data access is critical for teams operating dbt at scale.

### Separate deployment and execution roles

Some teams require the CI/CD service user that manages the dbt project object to be limited to deployment and unable to transform production data. For this separation-of-duties model, use a deploy-only role in the CI/CD pipeline. Grant it only the privileges needed to create the dbt project object and replace its live version. Deploy with `snow dbt deploy --no-auto-compile` so that the deployment doesn’t attempt to run `dbt deps` or `dbt compile`.

Use a separate production execution role for transformations. Configure it as the role in the production target in `dbt_projects_profiles.yml` or `profiles.yml`, and use the same role as the calling role for external orchestration or the task owner role for Snowflake tasks. Grant this role `USAGE` on the dbt project object and the required warehouse and data privileges. For detailed role and privilege setup, see [Optionally separate deployment from execution](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control#label-dbt-project-separate-deployment-execution).

### MONITOR privilege doesn’t grant data access

The MONITOR privilege on a dbt project object gives a user access to the dbt project object’s manifest, run history, and artifacts. It does **not** grant access to query the tables and views that the dbt project object creates.

This means a data engineer with MONITOR can:

- View model definitions, schemas, and lineage in the dbt DAG.
- Review execution logs and run history.
- Access dbt artifacts (`manifest.json`, `run_results.json`, `dbt.log`) from each execution using [system functions](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
- Use CoCo to inspect the files of a deployed dbt project object and debug production failures.

But they **cannot** query the production tables unless they have SELECT privileges granted separately.

### Separate data engineering from data querying

The permissions for running a dbt pipeline are separate from the permissions for querying its output:

- **Data engineering permissions:** USAGE on the dbt project object, ownership or access to source tables in dev, and the ability to deploy updates.
- **Data querying permissions:** SELECT on the production tables and views created by the pipeline.

This separation is intentional. A data engineer might only have access to run operations in their dev schema or staging environment, while a dedicated service account runs the production pipeline. Analysts then receive access to the production output through standard role grants, not through the dbt project object itself.

### Artifacts describe schema, not data

dbt artifacts such as `manifest.json`, `run_results.json`, only describe the **schema** of models (column names, types, relationships). They don’t grant query access to the tables and views that the project creates. Granting MONITOR on a dbt project object grants access to those artifacts, but it doesn’t grant SELECT privileges on production data.
For the full permissions reference, see [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).

## Security

Security best practices for dbt Projects on Snowflake center on minimizing credential exposure and maintaining strict access boundaries.

### Use OIDC ephemeral tokens for CI/CD

For GitHub Actions and other CI/CD platforms, use [OpenID Connect (OIDC)](/user-guide/workload-identity-federation) authentication instead of long-lived service account credentials. With OIDC:

- Tokens are ephemeral and scoped to the specific workflow run.
- No secrets to store, rotate, or risk leaking.
- The OIDC user has only the permissions needed to deploy and execute the tester or production dbt project object.

This is a significant security improvement over storing Snowflake credentials as repository secrets. For setup details, see the OIDC section in the [CI/CD tutorial](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

### Require multi-factor authentication for human users

For any human user who can deploy or execute dbt project objects, require multi-factor authentication (MFA) or personal access tokens (PATs). This protects against credential compromise and ensures that only authorized engineers can modify production pipelines.

### Output tables don’t auto-grant access

When a dbt pipeline creates or updates tables, those tables don’t automatically become accessible to the user or role that ran the pipeline. Access to production output requires explicit GRANT statements from an administrator.

This means:

- Running a pipeline doesn’t give you SELECT on the results.
- Analysts need separate grants to query production tables.
- Your data engineering permissions and your data querying permissions remain isolated.

This design keeps your security boundary clean: the ability to build a pipeline is separate from the ability to read its output.

### Use Snowflake secrets for private Git packages

Teams that depend on private dbt packages (shared macros, internal utilities) can use Snowflake secrets to authenticate against private Git repositories during `dbt deps`. This eliminates the need to store Git tokens in credential managers or developer environments. An admin creates a Snowflake secret containing a read-only Git personal access token, then references it in the `env.yml` file as a `DBT_ENV_SECRET_` variable. dbt uses this variable to authenticate when installing packages from `packages.yml`, and masks the value wherever it appears. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Hybrid development

Large engineering teams have developers with different skill levels and tool preferences. dbt Projects on Snowflake supports multiple development workflows so teams can choose what works best for each member.

### Development environment options

| Environment | Best for | Key benefit |
| --- | --- | --- |
| Cortex Code Desktop (Snowflake-managed mode) | Experienced developers who prefer a full IDE | Local IDE experience with Snowflake-native dbt execution |
| Snowflake Workspaces | Teams that want browser-based development with no local setup | Zero installation, collaborative, Git-integrated |
| Local IDE + Snowflake CLI | Teams with established local dbt Core workflows | Familiar tools, deploy to Snowflake via CI/CD |

Expand

Show lessSee more

All three environments support standard dbt Core and produce the same results when deployed.

### Use dbt\_projects\_profiles.yml for a unified development-to-production experience

Teams migrating from self-hosted dbt Core often already have a `~/.dbt/profiles.yml` that their entire local workflow depends on. Previously, dbt Projects on Snowflake required a `profiles.yml` in the project root, and because dbt Core checks the project directory before `~/.dbt/`, that file silently took over for local runs too. Your team was stuck overwriting personal profiles, passing `--profiles-dir` by hand on every local command, or forcing everyone onto the same workflow.

The `dbt_projects_profiles.yml` file solves this:

- It works the same way as `profiles.yml` but is specifically for dbt Projects on Snowflake.
- dbt Projects on Snowflake supports both file names. If both files are present, Snowflake uses `dbt_projects_profiles.yml` and ignores `profiles.yml` during deployment, compilation, and subsequent commands. If `dbt_projects_profiles.yml` isn’t present, Snowflake uses `profiles.yml` as before.
- Standard dbt doesn’t recognize `dbt_projects_profiles.yml`. The local dbt CLI reads only `profiles.yml`, so adding `dbt_projects_profiles.yml` never disrupts anyone’s existing local dbt workflow, including a personal `~/.dbt/profiles.yml`.
- It works across Workspaces, Cortex Code Desktop (Snowflake-managed mode), and deployed dbt project objects. In Workspaces and Cortex Code Desktop, the profile picker displays targets from `dbt_projects_profiles.yml` when present.

Hybrid teams can maintain both workflows side by side: some engineers can use the local dbt CLI with their personal `~/.dbt/profiles.yml`, while others use Workspaces or Cortex Code Desktop with the in-project `dbt_projects_profiles.yml`. Both groups can share one Git-versioned project without reconfiguring connections and can switch between local and Snowflake-managed development. The deployed dbt project object also uses `dbt_projects_profiles.yml`, so admins can configure production connection settings in a single version-controlled file.

After your team deploys with `dbt_projects_profiles.yml`, pair it with `env.yml` to take advantage of Snowflake’s SQL in YAML capability, which standard dbt Core doesn’t offer on its own. Use SQL functions to compute time intervals for incremental processing, query control tables for orchestration metadata, or call stored procedures to retrieve runtime parameters. Both files remain version controlled, and Snowflake resolves the values dynamically at execution time without external tooling. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

For more information about developing in Workspaces, see [Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces). For Cortex Code Desktop, see [dbt integration](/user-guide/cortex-code/cortex-code-desktop/dbt-integration).

## Documenting sources and models

Well-documented dbt projects are easier to onboard new engineers, debug failures, and audit for compliance. dbt provides three key documentation surfaces that integrate with Snowflake’s tooling, and CoCo can accelerate all of them by reading the Snowflake Horizon Catalog to generate accurate documentation from existing metadata.

### Document your sources (sources.yml)

A `sources.yml` file declares the raw tables your dbt project depends on and provides metadata that flows directly into the Snowsight dbt project object details page. Key properties to define:

- **Source descriptions** explaining where the data comes from and what the source system is.
- **Table descriptions** documenting what each table contains and its business context.
- **Column descriptions** defining the meaning of each column for downstream consumers.

CoCo can scan the Snowflake Horizon Catalog (table comments, column comments, and tags) and generate a `sources.yml` with accurate descriptions already populated. This saves manual discovery work and ensures your documentation stays in sync with what’s actually in your Snowflake account.

### Document your models (models.yml)

A `models.yml` file (sometimes called `schema.yml`) describes the models your project produces. Define these properties alongside your model SQL:

- **Model descriptions** explaining what the model does and who consumes it.
- **Column descriptions** with business definitions and expected data types.
- **Meta fields** for ownership, SLA expectations, domain tagging, or any team-specific conventions.

CoCo can read the Snowflake objects that your models produce and generate model documentation from the catalog metadata, keeping your `models.yml` files accurate as your pipeline evolves.

### Maintain a project overview

The dbt project object details page in Snowsight renders your project’s [overview docs block](https://docs.getdbt.com/docs/build/documentation#setting-a-custom-overview): a `{% docs __overview__ %}` block you define in any `.md` file dbt parses. Use it as a living README for your data project:

- Project purpose and scope.
- Key models, their relationships, and data flow summary.
- Team ownership and contact information.
- Data refresh cadence and pipeline schedules.

When large structural changes are made to the pipeline (new domains, deprecated models, schema reorganizations), ask CoCo to regenerate or update your overview docs block to keep it fresh. This ensures anyone browsing the project in Snowsight gets an accurate, up-to-date picture of what the pipeline does and how it’s organized.

## Concurrent execution and large projects

As your dbt practice matures, understanding how to structure projects for efficiency and maintainability becomes important.

### Why teams start with a single dbt project object

Keeping your pipeline in a single dbt project object preserves end-to-end lineage across all models. This means your dbt DAG in Snowsight shows the complete dependency graph, making impact analysis and debugging straightforward. You can still run specific slices of the pipeline using `--select` on different task schedules while maintaining that unified view.

For example, you might schedule hourly runs for time-sensitive models while running the full pipeline daily:

Copy code

```
-- Hourly: only the time-sensitive slice
CREATE OR ALTER TASK my_db.my_schema.hourly_slice
  WAREHOUSE = transform_wh
  SCHEDULE = '1 hour'
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project
    args='run --target prod --select my_model_a my_model_b';

-- Daily: the full pipeline
CREATE OR ALTER TASK my_db.my_schema.daily_full
  WAREHOUSE = transform_wh
  SCHEDULE = '24 hours'
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project
    args='build --target prod';
```

### When teams outgrow a single project

As teams grow, they may split their pipeline into logical units for efficiency (separate domains, teams, or cadences). When this happens, maintaining dependencies across project boundaries becomes important.

### Run one project concurrently

Data teams often need to run independent slices of a pipeline at different cadences. Run the same dbt project object concurrently so that each slice can stay fresh without waiting for unrelated work or requiring duplicate deployed objects.

With the default writeback behavior, concurrent executions can write target and log artifacts to the same directories on the live version, which can cause an execution to fail. To prevent those writes from conflicting, use one of these isolation patterns:

- **Recommended:** Set `WRITEBACK = FALSE` for executions that don’t need to persist target and log artifacts to the live version.
- If writeback is required, set distinct, non-overlapping `--target-path` and `--log-path` values for each execution.

Snowflake stores the per-query result artifacts and archive regardless of this setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

Concurrent object executions are different from the `threads` profile setting. Concurrent executions run multiple dbt commands using one deployed object, while `threads` control parallel model work within one execution. For details, see [Run a dbt project object concurrently](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-concurrent-executions).

### File limit considerations

A dbt project object supports up to 100,000 files. For very large projects approaching this limit, consider splitting into logical sub-projects. If your project still requires more capacity, contact your Snowflake account representative.

For more details on current limitations, see [Limitations, requirements, and considerations for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations).

## Data quality testing

Data quality checks should be built into your dbt pipeline, not bolted on as an afterthought. dbt’s testing framework runs alongside your models and fails the pipeline when quality checks don’t pass.

### Built-in dbt tests

Every dbt project should use the standard test types for basic data integrity:

- `not_null`: Ensures critical columns never contain null values.
- `unique`: Validates that primary keys and business keys are unique.
- `accepted_values`: Confirms categorical columns contain only expected values.
- `relationships`: Verifies referential integrity between models.

Ask CoCo to define these in your `schema.yml` files alongside your model definitions.

### Use dbt-expectations for advanced testing

For teams that need expressive, verbose data quality assertions, the [dbt-expectations](https://hub.getdbt.com/metaplane/dbt_expectations/latest/) package extends dbt’s testing capabilities significantly. It supports patterns like:

- Row count comparisons between tables.
- Distribution checks (values within expected ranges).
- Pattern matching and regex validation.
- Cross-column consistency checks.

dbt Projects on Snowflake has full `dbt deps` support, which means you can install and use any package from the dbt package hub, including dbt-expectations.

### Enforce test gates in CI/CD

Configure your CI/CD pipeline to run both models and tests. Use a full `dbt build` for complete-project validation, or run and test the selected `state:modified+` graph in a Slim CI workflow. This ensures that:

- Tests run after every model build in CI.
- A failing test blocks the pull request from merging.
- Data quality is validated before changes reach production.

Tests are part of `dbt build`, so no separate step is needed.

## Third-party packages

dbt Projects on Snowflake has full `dbt deps` support, so you can install and use any package from the [dbt package hub](https://hub.getdbt.com/). This includes popular packages like `dbt_utils`, `dbt_expectations`, and `dbt_project_evaluator`.

If you run `dbt deps` inside a Snowflake workspace or during dbt project object execution, Snowflake needs network access to download packages from the internet. Configure an external access integration on your dbt project object to allow this. Alternatively, run `dbt deps` locally or in your CI/CD pipeline and deploy the project with `dbt_packages/` already included.

For details on installing and managing packages, see [Understand dependencies for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).

## Semantic views

Codifying your semantic views within a dbt pipeline ensures they’re version-controlled, testable, and reproducible across environments.

### Use the Snowflake Semantic Views dbt package

The [Snowflake Semantic View dbt Package](https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/) is the recommended approach for managing semantic views in dbt rather than creating them manually through the Snowflake UI. This package lets you define semantic views as dbt models, which means:

- Semantic view definitions are stored in your Git repository alongside your transformation logic.
- Changes to semantic views go through the same CI/CD and review process as your models.
- You get reproducibility across environments (dev, staging, prod) and a clear audit trail of who changed what and when.

Snowflake semantic views don’t support the Open Semantic Interface (OSI) and don’t integrate directly with the dbt Labs MetricFlow semantic layer. The Snowflake Semantic View dbt Package is the recommended path for codifying semantic views within your dbt pipeline on the Snowflake platform.

### SQL pass-through for latest features

The Snowflake Semantic View dbt Package uses SQL pass-through, which means it supports the latest Snowflake SQL features regardless of the package’s version on the dbt package hub. You don’t need to wait for a package update to use new Snowflake capabilities in your semantic view definitions.

For best practices on developing and maintaining semantic views, see [Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev).
