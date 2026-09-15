# dbt Projects on Snowflake

[dbt Core](https://github.com/dbt-labs/dbt-core) is an open-source framework for defining, testing, and deploying SQL transformations.
dbt Projects on Snowflake brings the full dbt lifecycle into Snowflake: develop, deploy, orchestrate, and observe your transformations in the same place your data already lives.

## Why dbt Projects on Snowflake

- **No infrastructure to manage:** Snowflake provides managed dbt Core and dbt Fusion runtimes. Pin a version or set an account-level default.
- **Hybrid development:** dbt Projects on Snowflake is supported across Snowflake Workspaces and Snowflake-managed mode in CoCo Desktop, giving you a true pre-production runtime environment with no installs.
- **Governed configuration:** Manage per-developer setups, production environment variables, and secrets in a single, Git-versioned `env.yml` file.
- **CI/CD:** Bring software development best practices to your data pipelines. Use Snowflake CLI with GitHub Actions, GitLab, Azure DevOps, or another CI platform to validate every pull request in an isolated environment and deploy to production after merge.
- **Slim CI:** Import the latest successful state directly from a production dbt project object without managing a separate artifact store. Run only changed models and their downstream dependencies to reduce validation time and warehouse use.
- **Native defer to production:** Build changed models in an isolated CI target while resolving unchanged upstream references to existing production relations, avoiding unnecessary rebuilds.
- **Native orchestration:** Schedule executions with Snowflake tasks or integrate with Apache Airflow. No external orchestrator required.
- **Concurrent executions:** Run the same deployed dbt project object concurrently to keep independent data slices in your pipeline fresh.
- **Built-in observability:** Inspect run history, logs, and artifacts, with column-level lineage in Snowsight.
- **AI-assisted development:** CoCo is integrated with the Snowflake Horizon Catalog, so it can inspect the files of a deployed dbt project object to debug production runs, generate `sources.yml` and `models.yml` documentation from catalog metadata, and scaffold dbt data quality tests in your `schema.yml`.
- **No extra fees:** Executions use a virtual warehouse and incur standard compute costs, with no licensing or per-user fees.

## Get started

- **New to dbt Projects on Snowflake?** Follow the [Tutorial: Get started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial).
- **Migrating an existing dbt Core project?** See the [Migrate from dbt Core to dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-migrate-from-dbt-core).
- **Running dbt at scale?** See [Best practices for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices).

## Workflow

1. **Start with a valid dbt project.** Your project needs a `dbt_project.yml`, a [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file, and model files, stored in a workspace or a connected Git repository. If both files are present, Snowflake uses `dbt_projects_profiles.yml`.
2. **Install dependencies** by running `dbt deps` to populate the `dbt_packages` folder. See [Understand dependencies for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).
3. **Deploy a dbt project object** with `CREATE DBT PROJECT ... FROM <source>` or `snow dbt deploy`. See [Deploy dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-deploy).
4. **Execute the object** with `EXECUTE DBT PROJECT` or `snow dbt execute`. See [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).
5. **Schedule and orchestrate** with Snowflake tasks or Apache Airflow. See [Schedule execution of dbt project objects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).
6. **Set up CI/CD integrations** with Snowflake CLI. Start with the [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial), or use the [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial) for a Slim CI workflow that uses per-pull-request zero-copy clone databases.
7. **Monitor executions,** logs, and artifacts. See [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability).

## Learn more

| Topic | Description |
| --- | --- |
| [Understand dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-understanding-dbt-project-objects) | Start here to learn what dbt project objects are and how they work. |
| [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod) | Use artifacts from earlier dbt runs to identify and run changed models, defer to production, and recover from a failed execution. |
| [Use SQL environment variables and private Git packages](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables) | Manage environment variables, secrets, and multiple environments with a Git-versioned `env.yml` file. |
| [Understand CI/CD](/user-guide/data-engineering/dbt-projects-on-snowflake-ci-cd) | Automate testing and deployment with the Snowflake CLI and OIDC. |
| [Deploy dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-deploy) | Create and update dbt project objects from Snowsight, SQL, or the Snowflake CLI. |
| [Understand orchestration](/user-guide/data-engineering/dbt-projects-on-snowflake-orchestration) | Integrate dbt project object executions with Snowflake tasks, Apache Airflow, or other external orchestrators. |
| [Schedule executions](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution) | Run dbt project objects on a schedule with Snowflake tasks. |
| [Monitor and observe](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability) | Inspect run history, logs, artifacts, and column-level lineage. |
| [Understand costs](/user-guide/data-engineering/dbt-projects-on-snowflake-cost) | How compute costs work when you execute dbt project objects. |
| [Access control](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control) | Privileges for creating, executing, and managing dbt project objects. |
| [Supported commands and flags](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands) | The dbt commands and flags supported on Snowflake. |
| [Limitations](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations) | Requirements and considerations to plan for. |

Expand

Show lessSee more
