# Understand CI/CD for dbt Projects on Snowflake

dbt project objects support using Snowflake CLI commands to integrate deployment and execution into your CI/CD workflows. For a
straightforward full-build workflow, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial). For a Slim CI workflow that
uses per-pull-request zero-copy clone databases, see
[Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

This topic explains how to use CI/CD platforms (GitHub Actions, GitLab CI/CD, or Azure DevOps) to automatically test and deploy your dbt Projects on Snowflake whenever you open a pull request or merge to
main.

Continuous Integration (CI) runs your dbt project against a dev schema on each pull request. In other words, whenever someone opens or
updates a pull request in your code repository, you automatically run tests and builds on the new code. This helps catch problems early
before merging.

Continuous Deployment (CD) keeps a dbt project object in Snowflake up to date after your commits are merged. In other words, whenever code
gets merged into a branch, you automatically deploy the updated code to production. This ensures that your production environment stays
up-to-date, reliably and reproducibly.

CI/CD helps avoid manual, error-prone deployments, ensures changes are validated before being merged, and enables consistent, repeatable
deployments.

## Why use CI/CD to update dbt project objects

dbt projects define all your data transformations in code, so frequent updates can easily introduce errors. CI catches these issues early by
testing every change in a separate dev environment before merging.

After changes are merged, CD automatically updates the official dbt project object in your Snowflake production environment. This removes
manual steps, reduces risk, keeps everything version-controlled, and supports a reliable, collaborative workflow.

For more information on CI/CD best practices, see [Continuous integration and continuous deployment (CI/CD)](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-best-practices-ci-cd).

## Choose a CI validation path

Choose between these two paths based on the breadth of validation that each pull request needs:

- **Full build:** Run `dbt build` against an isolated dev target to validate every model and test in the project. This introductory path is thorough and simple, but it compiles, runs, and tests the entire project even when a pull request changes only a few models. The extra work becomes more significant as the project grows. For the tutorial, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).
- **Slim CI:** Import state from the latest successful production execution, run and test only `state:modified+`, and defer unchanged upstream references to production. This path usually provides faster, more cost-efficient pull-request validation. For the tutorial, see [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

For more information about using dbt artifacts for state, defer, Slim CI, and failed-execution recovery, see [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

## High-level prerequisites for using CI/CD on dbt Projects

- A dbt project stored in a Git repository (for example, GitHub, GitLab, or Azure Repos).
- A Snowflake account and user with privileges as described in [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).
- Privileges to create and edit the following objects or access to an administrator who can create each of them on your behalf:

  - CI/CD platform secrets and variables to hold Snowflake account, database and schema values, and workflow files that define CI and CD jobs.
  - Snowflake service account to communicate with your CI/CD platform
- A separation between dev environment (for CI) and prod environment (for CD) in Snowflake (for example, separate databases or schemas for each
  environment).
- A way to permit your CI/CD runner (for example, GitHub Actions, GitLab Runner, or Azure DevOps agents) to connect to Snowflake, such as OIDC or PAT. For more information, see
  [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd).
- In your code repository, a [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file configured to point to dev and prod targets (for example, databases/schemas, warehouse).
- A network policy that allows inbound access from your Git provider into Snowflake.

## CI/CD workflow overview

The following steps outline the typical workflow with CI/CD.

1. Developer writes or modifies dbt code (models, tests, etc.) in a branch.
2. Developer opens a pull request.
3. CI kicks in: a tester instance of the dbt project object is deployed to the Snowflake dev environment. The workflow either runs a full
   `dbt build` or uses Slim CI to run and test the changed portion of the DAG.

   - If an operation fails, the pull request fails. The developer must fix and update, then rerun.
   - If all operations pass, the pull request is eligible for merge.
4. Pull request is merged to main.
5. CD kicks in: the production dbt project object in Snowflake is updated to reflect the latest code.
6. Optionally, automated scheduling (for example, via Snowflake tasks) can be deployed, so data pipelines run on a schedule without manual
   intervention.
