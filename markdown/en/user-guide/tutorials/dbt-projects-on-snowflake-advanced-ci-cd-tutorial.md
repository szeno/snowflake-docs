# Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake

## Introduction

This tutorial is a continuation of the
[Getting started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) tutorial.
It assumes you have a dbt project in a Git repository and a working Snowflake environment with your database, schemas, warehouse, and source
data set up. You can use the Tasty Bytes objects from the getting-started tutorial or substitute your own objects.

This tutorial provides all of the additional environment, authentication, repository, and workflow setup needed to implement advanced CI/CD
with GitHub Actions, GitLab CI/CD, or Azure DevOps. You don’t need to complete the
[introductory CI/CD tutorial](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial) first. If you already completed it, you can reuse
its service user, network policy, secrets, and variables.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

For the underlying artifact comparison and defer concepts, and for a SQL alternative, see
[Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

### Overview

This tutorial walks you through the following steps:

1. Set up the Snowflake environment and configure the dbt profile to accept a per-pull-request database override.
2. Create a CI/CD service user that uses OpenID Connect (OIDC) authentication.
3. Configure an optional network policy.
4. Store the required secrets and variables in your CI/CD platform.
5. Create an incoming-pull-request workflow that:
   - Creates a zero-copy clone for the pull request. Cloning is optional unless tests need a realistic, writable copy of existing production
     data and objects; this tutorial includes it.
   - Deploys a tester dbt project object with `--no-auto-compile`.
   - Imports state from the latest qualifying successful production execution.
   - Uses `dbt build` to run and test only changed models and their downstream dependencies in DAG order.
   - Defers unchanged upstream references to production relations.
6. Create a production deployment workflow that:
   - Deploys code pushed to `main` to the production dbt project object.
   - Optionally recreates or updates scheduled Snowflake tasks.
7. Remove the tester object and per-pull-request database after validation or when the pull request closes, depending on the CI/CD platform.

At the end of the tutorial, you’ll have a repeatable workflow that isolates each pull request or merge request, processes only the affected
portion of the dbt DAG, and keeps production state available for future Slim CI runs.

### Prerequisites

- An existing production dbt project object.
- A CI role with the `MONITOR` privilege on the production dbt project object.
- At least one successful execution of the production dbt project object within the previous 7 days.

## Set up your environment

Set up where your dbt project reads and writes in Snowflake, then configure `env.yml` and your profile file so the incoming-pull-request
workflow can override the target database.

### Create a warehouse, database, and schemas

Note

If you completed the
[Getting started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) tutorial
and ran `tasty_bytes_setup.sql`, the `tasty_bytes_dbt_db` database, `dev` and `prod` schemas, and `TASTY_BYTES_DBT_WH` warehouse already
exist. You can skip this step.

If you use the Tasty Bytes project but haven’t created its warehouse, database, and schemas, run the following commands:

Copy code

```
CREATE WAREHOUSE IF NOT EXISTS TASTY_BYTES_DBT_WH;
CREATE DATABASE IF NOT EXISTS tasty_bytes_dbt_db;
CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.dev;
CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.prod;
```

If you use your own project, substitute the production database, schemas, and warehouse that your production dbt project object uses.

### Configure environment and profile files

The `env.yml` file defines named execution environments for a dbt project. In this workflow, CI selects the `staging` environment and
overrides `DBT_DATABASE` so that selected models write to the zero-copy clone for the pull request or merge request. The production workflow
uses the default `prod` environment and database.

Create `env.yml` in the root of your dbt project, next to `dbt_project.yml`:

Copy code

```
env_config:
  default_environment: prod
  environments:
    - name: staging
      env:
        DBT_DATABASE: tasty_bytes_dbt_db
    - name: prod
      env:
        DBT_DATABASE: tasty_bytes_dbt_db
```

To manage CI/CD for a dbt project object, include `dbt_projects_profiles.yml` or `profiles.yml` in the root directory of your dbt project.
Snowflake uses `dbt_projects_profiles.yml` if both files are present.

This tutorial uses `profiles.yml`. Configure its `database` fields to read the `DBT_DATABASE` environment variable:

Copy code

```
tasty_bytes:
  target: dev
  outputs:
    dev:
      account: '_'
      database: "{{ env_var('DBT_DATABASE') }}"
      schema: dev
      role: DBT_CI_ROLE
      type: snowflake
      warehouse: TASTY_BYTES_DBT_WH
      user: '_'
      threads: 8
    prod:
      account: '_'
      database: "{{ env_var('DBT_DATABASE') }}"
      schema: prod
      role: DBT_CI_ROLE
      type: snowflake
      warehouse: TASTY_BYTES_DBT_WH
      user: '_'
      threads: 8
```

The account and user values are placeholders because the CI/CD platform variables configure the temporary Snowflake CLI connection. Replace
the role, warehouse, database, and schema names with the objects for your project.

For more information about `env.yml`, including value precedence, see
[Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

### Configure CI role access

Grant the CI role monitoring access to the production dbt project object:

Copy code

```
GRANT MONITOR ON DBT PROJECT <database>.<schema>.<production_project>
  TO ROLE <ci_role>;
```

Grant the role the account-level privilege required to create the per-pull-request database:

Copy code

```
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <ci_role>;
```

The CI role also needs the following access:

- `USAGE` on the database and schema that contain the production dbt project object.
- The privileges required to clone the source database. For more information, see
  [Access control requirements](/sql-reference/sql/create-clone#label-create-clone-access-control-reqs).
- Access to the warehouse and production relations that deferred references resolve to.
- The privileges required to create, execute, and drop the tester dbt project object.

For dbt project object privileges, see [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).

## Create a CI/CD service user in Snowflake (recommended)

Your CI/CD platform runs Snowflake CLI commands as a Snowflake service user. OIDC authentication is recommended because it uses a short-lived
token for each workflow run instead of a long-lived credential.

### Recommended: OIDC-based service user

Create an OIDC-based service user for your platform. Replace `DBT_CI_ROLE`, the warehouse, and the platform identifiers with your values.

GitHub ActionsGitLab CI/CDAzure DevOps

The GitHub environment in the subject must match the `environment` value in both workflow files:

Copy code

```
CREATE USER IF NOT EXISTS github_actions_service_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://token.actions.githubusercontent.com',
    SUBJECT = 'repo:your_repo_org/your_dbt_repo:environment:prod'
  )
  DEFAULT_ROLE = DBT_CI_ROLE
  COMMENT = 'Service user for GitHub Actions';

GRANT ROLE DBT_CI_ROLE TO USER github_actions_service_user;

ALTER USER github_actions_service_user
  SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

By default, GitLab includes the branch in the OIDC subject. To use one service user for merge-request and `main` pipelines, customize the
GitLab `sub` claim so it remains the same across branches, then use that value for `<gitlab_custom_subject>`. For details, see
.

Copy code

```
CREATE USER IF NOT EXISTS gitlab_cicd_service_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://gitlab.com'
    SUBJECT = '<gitlab_custom_subject>'
  )
  DEFAULT_ROLE = DBT_CI_ROLE
  COMMENT = 'Service user for GitLab CI/CD';

GRANT ROLE DBT_CI_ROLE TO USER gitlab_cicd_service_user;

ALTER USER gitlab_cicd_service_user
  SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

For more information, see [GitLab CI/CD component](/developer-guide/snowflake-cli/cicd/gitlab-component).

The subject uses an Azure DevOps service connection identifier. Replace `<azure-ad-tenant-id>` with your Microsoft Entra tenant ID.

Copy code

```
CREATE USER IF NOT EXISTS ado_cicd_service_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://vstoken.dev.azure.com/<azure-ad-tenant-id>'
    SUBJECT = 'sc://<ado-org>/<ado-project>/<service-connection-name>'
    OIDC_AUDIENCE_LIST = ('api://AzureADTokenExchange')
  )
  DEFAULT_ROLE = DBT_CI_ROLE
  COMMENT = 'Service user for Azure DevOps';

GRANT ROLE DBT_CI_ROLE TO USER ado_cicd_service_user;

ALTER USER ado_cicd_service_user
  SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

For more information, see [Azure DevOps extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension).

The `DEFAULT_ROLE` property selects a default role but doesn’t grant it, so each example includes a separate `GRANT ROLE` command.

For more information, see [Workload identity federation](/user-guide/workload-identity-federation).

### Alternative: Use PAT-based authentication (less secure)

If you can’t use OIDC, you can authenticate the service user with a programmatic access token (PAT). This alternative is less secure because
it relies on a long-lived credential that requires manual rotation.

Create a service user and an authentication policy that permits PAT authentication. Replace `<service_user>` with a platform-specific name,
such as `github_actions_service_user`, `gitlab_cicd_service_user`, or `ado_cicd_service_user`:

Copy code

```
CREATE USER IF NOT EXISTS <service_user>
  TYPE = SERVICE
  DEFAULT_ROLE = DBT_CI_ROLE
  COMMENT = 'Service user for CI/CD';

GRANT ROLE DBT_CI_ROLE TO USER <service_user>;

ALTER USER <service_user>
  SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';

CREATE DATABASE IF NOT EXISTS cicd_access_management;
CREATE SCHEMA IF NOT EXISTS cicd_access_management.policies;

CREATE AUTHENTICATION POLICY cicd_access_management.policies.cicd_auth_policy
  AUTHENTICATION_METHODS = ('PROGRAMMATIC_ACCESS_TOKEN')
  PAT_POLICY = (
    DEFAULT_EXPIRY_IN_DAYS = 15,
    MAX_EXPIRY_IN_DAYS = 365,
    NETWORK_POLICY_EVALUATION = ENFORCED_NOT_REQUIRED
  );

ALTER USER <service_user>
  SET AUTHENTICATION POLICY cicd_access_management.policies.cicd_auth_policy;
```

Generate a PAT for the service user and store it in your CI/CD platform as described later. For more information, see
[Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

## (Optional) Set up a network policy for your CI/CD platform

Now that you’ve created the service user that Snowflake CLI uses, configure this user to connect to your Snowflake account from within your
CI/CD platform.

Note

Creating or modifying network policies requires `ACCOUNTADMIN` or an equivalent role.

### Determine whether you need a network policy

- If your account restricts inbound access, you must create or update a network policy to add your CI/CD platform’s runner IPs to your
  allowlist. Snowflake provides managed network rules for some platforms. For more information, see [Network rules](/user-guide/network-rules).
- If your account doesn’t restrict inbound access, no network policy changes are required.

If you’re unsure, skip this step for now and return only if you see an error like:
`Incoming request with IP/Token <IP> is not allowed to access Snowflake.`

To create and apply a network policy to a user, choose one of the following options:

- Create a new network policy and assign it to the service user.
- Add a network rule to an existing network policy that the user already uses.

Note

Before doing this, consult your Snowflake account administrator. They must ensure that the policy includes the CI/CD platform network rule and
any other IP ranges your organization requires.

After a network policy is applied, Snowflake restricts user access based on its allowed and blocked IP ranges. Your account administrator
might need to adjust the policy or apply it account-wide to avoid unintentionally blocking essential access.

### Option 1: Create a new network policy and apply it to the user

A Snowflake user can have only one network policy at a time. If the user doesn’t have one or you want to replace the existing policy, complete
the following steps:

GitHub ActionsGitLab CI/CDAzure DevOps

Snowflake provides a managed network rule for GitHub-hosted runners:

Copy code

```
CREATE NETWORK POLICY github_actions_policy
  ALLOWED_NETWORK_RULE_LIST = ('SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL', <other required rules>)
  BLOCKED_NETWORK_RULE_LIST = ();

ALTER USER github_actions_service_user
  SET NETWORK_POLICY = github_actions_policy;
```

GitLab doesn’t have a Snowflake-managed network rule. GitLab.com hosted runners don’t have static, allowlistable IP addresses. If your
Snowflake account restricts inbound IPs, use a self-hosted GitLab Runner or route runner traffic through a fixed egress IP:

Copy code

```
CREATE NETWORK RULE gitlab_runner_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('<your_gitlab_runner_ip_range>');

CREATE NETWORK POLICY gitlab_cicd_policy
  ALLOWED_NETWORK_RULE_LIST = ('gitlab_runner_rule', <other required rules>)
  BLOCKED_NETWORK_RULE_LIST = ();

ALTER USER gitlab_cicd_service_user
  SET NETWORK_POLICY = gitlab_cicd_policy;
```

Azure DevOps doesn’t have a Snowflake-managed network rule. For Microsoft-hosted agents, allow the
[Azure DevOps service IP ranges](https://learn.microsoft.com/en-us/azure/devops/organizations/security/allow-list-ip-url). For self-hosted
agents, add the agent’s static egress IP:

Copy code

```
CREATE NETWORK RULE ado_agent_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('<your_ado_agent_ip_range>');

CREATE NETWORK POLICY ado_cicd_policy
  ALLOWED_NETWORK_RULE_LIST = ('ado_agent_rule', <other required rules>)
  BLOCKED_NETWORK_RULE_LIST = ();

ALTER USER ado_cicd_service_user
  SET NETWORK_POLICY = ado_cicd_policy;
```

### Option 2: Add a network rule to an existing network policy

If the user already has a network policy, add the appropriate rule to it. First, check the user’s current network policy:

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER github_actions_service_user;
```

Copy code

```
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER gitlab_cicd_service_user;
```

Copy code

```
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER ado_cicd_service_user;
```

Note

If the network policy is applied at the account level or shared by many users, updating it affects everyone.

Add the platform’s network rule to the existing policy:

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL');
```

Copy code

```
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('gitlab_runner_rule');
```

Copy code

```
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('ado_agent_rule');
```

The user inherits the update automatically because they’re already assigned to this policy.

For more information, see [Network rules](/user-guide/network-rules).

## Configure CI/CD secrets and variables

Your CI/CD pipelines use Snowflake CLI to connect to your Snowflake account, so you must configure platform secrets and variables first.
Secrets identify the account and, when required, the user credentials. Variables supply Snowflake object names and the dbt project path.

### Configure secrets

Add secrets to securely store the information that Snowflake CLI needs to identify your Snowflake account and, if required, the user it
should authenticate as.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Settings**.
2. From the left-hand navigation, select **Secrets and variables** » **Actions**.
3. Under **Secrets**, select **New repository secret**.
4. Add a secret to connect to your Snowflake account:
   - **Name**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier, for example, `org_name-account_name`.
5. Select **Add secret**.
6. If you use PAT authentication instead of OIDC, add these repository secrets:
   - **Name**: `SNOWFLAKE_USER`
     - **Value**: `github_actions_service_user`, or the name of your service user.
   - **Name**: `SNOWFLAKE_PAT`
     - **Value**: The PAT generated for the service user.

Don’t add `SNOWFLAKE_USER` or `SNOWFLAKE_PAT` when you use OIDC. Snowflake automatically matches the GitHub Actions subject to the OIDC
service user.

1. In your GitLab project, go to **Settings** » **CI/CD**.
2. Expand **Variables**, then select **Add variable**.
3. Add a variable for your Snowflake account:
   - **Key**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier, for example, `org_name-account_name`.
   - Enable **Mask variable**.
4. Add a variable for your Snowflake user:
   - **Key**: `SNOWFLAKE_USER`
   - **Value**: The service user you created, for example, `gitlab_cicd_service_user`.
   - Enable **Mask variable**.
5. If you use PAT authentication instead of OIDC, add a variable for the PAT:
   - **Key**: `SNOWFLAKE_PASSWORD`
   - **Value**: The PAT generated for the service user.
   - Enable **Mask variable**. Enable **Protect variable** only if the merge-request branches are protected and the pipeline can access
     protected variables.

1. In your Azure DevOps project, go to **Pipelines** » **Library**.
2. Select **+ Variable group** or open an existing variable group named `dbt-cicd-variables`.
3. Add a variable for your Snowflake account:
   - **Name**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier, for example, `org_name-account_name`.
   - Select the lock icon to mark it as secret.
4. Add a variable for your Snowflake user:
   - **Name**: `SNOWFLAKE_USER`
   - **Value**: The service user you created, for example, `ado_cicd_service_user`.
   - Select the lock icon to mark it as secret.
5. If you use PAT authentication instead of OIDC, add a variable for the PAT:
   - **Name**: `SNOWFLAKE_PASSWORD`
   - **Value**: The PAT generated for the service user.
   - Select the lock icon to mark it as secret.
6. Select **Save**, then authorize both pipelines to use the variable group.

### Configure variables

| Variable | Description | Example |
| --- | --- | --- |
| `SNOWFLAKE_DATABASE` | Database that contains the production and tester dbt project objects. | `TASTY_BYTES_DBT_DB` |
| `SNOWFLAKE_SCHEMA` | Schema that contains the production and tester dbt project objects. | `PROJECTS` |

Expand

Show lessSee more

Add these values to your platform:

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Settings**.
2. From the left-hand navigation, select **Secrets and variables** » **Actions**.
3. Under **Variables**, select **New repository variable**.
4. Add each value from the table as a repository variable, selecting **Add variable** after each one.

1. In your GitLab project, go to **Settings** » **CI/CD**.
2. Expand **Variables**, then add each value from the table as a project variable.

These object names and paths don’t need to be masked unless your organization treats them as sensitive.

1. In your Azure DevOps project, go to **Pipelines** » **Library**.
2. Open the variable group used by your pipelines.
3. Add each value from the table, then select **Save**.

## Create your Continuous Integration (CI) pipeline

This step is where automation starts. The CI pipeline runs whenever a pull request or merge request targets `main`. It creates isolated
resources for the request, imports artifacts from production, and uses `dbt build` to run and test changed models and their downstream
dependencies in DAG order.

### Create your CI workflow file

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Actions**.
2. From the left-hand side navigation, select **New workflow**.
3. Select **set up a workflow yourself** to create an empty workflow.
4. Name the file `incoming_pr_slim_ci.yml`.
5. Copy and paste the following into the file:

   Copy code

   ```
   name: Incoming PR - Slim CI
   run-name: PR opened by ${{ github.actor }}
   on:
     pull_request:
       types: [opened, synchronize, reopened, ready_for_review]
       branches: [main]

   permissions:
     contents: read
     id-token: write

   jobs:
     run-snowflake-test-dbt-job:
       name: "Run on Incoming PR - Slim CI"
       runs-on: ubuntu-latest
       environment: prod # Must match the OIDC subject's environment
       env:
         SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
         # SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }} # Required for PAT authentication
         # SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PAT }} # Required for PAT authentication
         SNOWFLAKE_DATABASE: ${{ vars.SNOWFLAKE_DATABASE }}
         SNOWFLAKE_SCHEMA: ${{ vars.SNOWFLAKE_SCHEMA }}

       steps:
         # Check out repository code
         # Gets the latest code from the incoming pull request
         - name: Check out repository code
           uses: actions/checkout@v4

         - name: Install Snowflake CLI
           uses: snowflakedb/snowflake-actions@v3
           with: # Ensures Snowflake CLI will search for OIDC users matching this subject
             use-oidc: true

         - name: Check Snowflake CLI Version
           run: snow --version

         # The -x is shorthand for --temporary-connection
         - run: snow connection test -x

         - name: Create a staging database using the PR number
           run: snow sql -x -q "CREATE OR REPLACE DATABASE tasty_bytes_dbt_db_staging_pr_${{ github.event.number }} CLONE tasty_bytes_dbt_db"

         # You can remove the "--source" flag if your dbt_project.yml is at root of your repo
         - name: Create a new tester dbt project object in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: |
             snow dbt deploy tester_tasty_bytes_dbt_project_object_gh_action_pr_${{ github.event.number }} \
               --source ./tasty_bytes \
               --no-auto-compile \
               --dbt-version 1.11.11 \
               -x

         - name: List all of the snowflake dbt project objects in your account
           run: snow dbt list -x

         # Builds changed models and runs their tests in DAG order, failing early if any upstream test breaks
         - name: Build and test dbt project in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: |
             snow dbt execute -x \
               --import "SYSTEM\$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}.tasty_bytes_dbt_object_gh_action') as state" \
               --env staging \
               --env-vars '{"DBT_DATABASE": "tasty_bytes_dbt_db_staging_pr_${{ github.event.number }}"}' \
               tester_tasty_bytes_dbt_project_object_gh_action_pr_${{ github.event.number }} \
               build --target dev --state ./imports/state --defer --select state:modified+
   ```
6. Select **Commit changes**.
7. Select **Create a new branch for this commit and start a pull request**.
8. Select **Propose changes**.
9. After you finish submitting the pull request, you should see your `incoming_pr_slim_ci.yml` action start to run.
10. After it’s merged, the file will be saved to `.github/workflows/incoming_pr_slim_ci.yml`.

If you use PAT authentication, remove the `with` block that contains `use-oidc: true`, and uncomment the `SNOWFLAKE_USER` and
`SNOWFLAKE_PASSWORD` lines in the workflow.

Create a `.gitlab-ci.yml` file at the root of your repository (or add the following to your existing one):

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      use-oidc: true
      cli-version: "3.16"
      template-only: true

stages:
  - test
  - cleanup
  - deploy

ci-test-dbt-slim-ci:
  extends: .configure-snowflake-cli
  stage: test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  variables:
    SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER: $SNOWFLAKE_USER
    SNOWFLAKE_DATABASE: $SNOWFLAKE_DATABASE
    SNOWFLAKE_SCHEMA: $SNOWFLAKE_SCHEMA
  script:
    - snow --version
    # The -x is shorthand for --temporary-connection
    - snow connection test -x
    - snow sql -x -q "CREATE OR REPLACE DATABASE tasty_bytes_dbt_db_staging_mr_${CI_MERGE_REQUEST_IID} CLONE tasty_bytes_dbt_db"
    # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
    - >-
      snow dbt deploy tester_tasty_bytes_dbt_project_object_gitlab_mr_${CI_MERGE_REQUEST_IID}
      --source ./tasty_bytes
      --no-auto-compile
      --dbt-version 1.11.11
      --git-commit "${CI_COMMIT_SHA}"
      --git-branch "${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME}"
      -x
    - snow dbt list -x
    # Builds changed models and runs their tests in DAG order, failing early if any upstream test breaks
    - >-
      snow dbt execute -x
      --import "SYSTEM\$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.tasty_bytes_dbt_object_gitlab') as state"
      --env staging
      --env-vars '{"DBT_DATABASE": "tasty_bytes_dbt_db_staging_mr_${CI_MERGE_REQUEST_IID}"}'
      tester_tasty_bytes_dbt_project_object_gitlab_mr_${CI_MERGE_REQUEST_IID}
      build --target dev --state ./imports/state --defer --select state:modified+

cleanup-slim-ci:
  extends: .configure-snowflake-cli
  stage: cleanup
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  when: always
  variables:
    SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER: $SNOWFLAKE_USER
    SNOWFLAKE_DATABASE: $SNOWFLAKE_DATABASE
    SNOWFLAKE_SCHEMA: $SNOWFLAKE_SCHEMA
  script:
    - snow --version
    # The -x is shorthand for --temporary-connection
    - snow connection test -x
    - snow sql -x -q "DROP DBT PROJECT IF EXISTS tester_tasty_bytes_dbt_project_object_gitlab_mr_${CI_MERGE_REQUEST_IID}"
    - snow sql -x -q "DROP DATABASE IF EXISTS tasty_bytes_dbt_db_staging_mr_${CI_MERGE_REQUEST_IID}"
    - snow dbt list -x
```

Commit the file to a branch and open a merge request targeting `main`. The cleanup job runs after validation, including when validation
fails.

If you use PAT authentication, set the component’s `use-oidc` input to `false` and configure `SNOWFLAKE_USER` and `SNOWFLAKE_PASSWORD`.

Create `azure-pipelines-ci-slim-ci.yml` at the root of your repository:

Copy code

```
trigger: none

pr:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
  SNOWFLAKE_USER: $(SNOWFLAKE_USER)
  SNOWFLAKE_DATABASE: $(SNOWFLAKE_DATABASE)
  SNOWFLAKE_SCHEMA: $(SNOWFLAKE_SCHEMA)

steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'
      useWorkloadIdentity: true
      connectedServiceName: 'snowflake-wif-connection'

  - script: snow --version
    displayName: 'Check Snowflake CLI Version'

  # The -x is shorthand for --temporary-connection.
  # SNOWFLAKE_TOKEN is a pipeline secret — map it on every later snow step.
  - script: snow connection test -x
    displayName: 'Test Snowflake connection'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow sql -x -q "CREATE OR REPLACE DATABASE tasty_bytes_dbt_db_staging_pr_$(System.PullRequest.PullRequestId) CLONE tasty_bytes_dbt_db"
    displayName: 'Create a staging database using the PR number'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
  - script: |
      snow dbt deploy tester_tasty_bytes_dbt_project_object_ado_pr_$(System.PullRequest.PullRequestId) \
        --source ./tasty_bytes \
        --no-auto-compile \
        --dbt-version 1.11.11 \
        --git-commit "$(Build.SourceVersion)" \
        --git-branch "$(System.PullRequest.SourceBranch)" \
        -x
    displayName: 'Create tester dbt project object'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow dbt list -x
    displayName: 'List dbt project objects'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  # Builds changed models and runs their tests in DAG order, failing early if any upstream test breaks
  - script: |
      snow dbt execute -x \
        --import "SYSTEM\$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('$(SNOWFLAKE_DATABASE).$(SNOWFLAKE_SCHEMA).tasty_bytes_dbt_object_ado') as state" \
        --env staging \
        --env-vars '{"DBT_DATABASE": "tasty_bytes_dbt_db_staging_pr_$(System.PullRequest.PullRequestId)"}' \
        tester_tasty_bytes_dbt_project_object_ado_pr_$(System.PullRequest.PullRequestId) \
        build --target dev --state ./imports/state --defer --select state:modified+
    displayName: 'Build and test dbt project - Slim CI'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow sql -x -q "DROP DBT PROJECT IF EXISTS tester_tasty_bytes_dbt_project_object_ado_pr_$(System.PullRequest.PullRequestId)"
    displayName: 'Drop the tester dbt project object'
    condition: always()
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow sql -x -q "DROP DATABASE IF EXISTS tasty_bytes_dbt_db_staging_pr_$(System.PullRequest.PullRequestId)"
    displayName: 'Drop the per-PR database'
    condition: always()
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow dbt list -x
    displayName: 'List dbt project objects after cleanup'
    condition: always()
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

In Azure DevOps, create a pipeline named `Incoming PR - Slim CI` that uses this YAML file and configure it as a build-validation policy for
pull requests targeting `main`. The cleanup steps remove the CI resources after each validation run.

If you use PAT authentication, set `useWorkloadIdentity` to `false` and add `SNOWFLAKE_USER` and `SNOWFLAKE_PASSWORD` to each script’s `env`
mapping. For workload identity, keep the `SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)` map on every later `script:` step — the task stores the token
as a secret, so Azure Pipelines does not inject it automatically.

When `snow dbt deploy` runs in GitHub Actions, Snowflake CLI automatically captures the commit and branch. The GitLab and
Azure DevOps workflows must explicitly pass `--git-commit` and `--git-branch`. These flags record the source commit and
branch in the dbt project object’s deployment metadata.

### Key pieces from the workflow file

Regardless of which platform you chose, the pipeline follows the same pattern:

- **Trigger**: Runs on incoming pull requests (or merge requests) targeting `main`.
- **OIDC authentication**: Each platform requests a short-lived token that Snowflake validates against your service user’s WORKLOAD\_IDENTITY
  configuration.
- **Snowflake CLI with `-x` flag**: The `-x` flag (`--temporary-connection`) tells Snowflake CLI to build the connection from environment
  variables (such as `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_DATABASE`) rather than reading a named profile from `config.toml`, which isn’t
  available in a CI/CD runner.
- **Steps in the job**:
  1. Check out repository code.
  2. Install Snowflake CLI with OIDC enabled.
  3. Check the Snowflake CLI version and verify the connection with `snow connection test -x`.
  4. Create a zero-copy clone whose name includes the pull-request or merge-request number.
  5. Deploy a tester dbt project object using `snow dbt deploy ... --no-auto-compile -x` (with `--source` if the dbt project is in a
     subfolder).
  6. List the dbt project objects with `snow dbt list -x`.
  7. Build and test the changed portion of the dbt project in DAG order with production state, defer, and `state:modified+`.
  8. Remove the tester object and clone when the platform’s cleanup workflow runs.

This workflow creates a zero-copy clone for each pull request or merge request so that CI has a realistic database it can modify without
changing production. The clone is an isolation choice, not a prerequisite for Slim CI. You don’t need to clone production for every CI
workflow unless your tests need a realistic, writable copy of existing production data and objects. With defer to production, CI can read
unchanged upstream tables from production and write changed models to a separate test database or schema.

Artifact comparison and database cloning serve different purposes. The `state:modified+` selector identifies which nodes to execute, and
`--defer` resolves references to unchanged production relations. The per-pull-request clone determines where CI writes and provides an
independently writable snapshot when tests depend on existing data or database state.

When Snowflake creates a zero-copy clone, the clone initially shares the source database’s existing micro-partitions instead of physically
copying all table data. The source and clone consume additional storage as their data changes.

The incoming workflow combines the Slim CI operations in one selective `dbt build` command. This runs models and tests in DAG order:

- `--no-auto-compile` skips `dbt deps` and `dbt compile` during deployment. The project compiles later, during execution, with the
  environment override.
- `SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET` retrieves artifacts from a recent successful execution of the production dbt project object.
- `--import "... as state"` mounts those artifacts at `./imports/state`.
- `--state ./imports/state --select state:modified+` selects changed nodes and their downstream dependencies.
- `--defer` resolves unselected upstream references to existing production relations.
- `--env staging --env-vars ...` overrides `DBT_DATABASE` so selected models write to the per-pull-request database.

## Create your Continuous Deployment (CD) pipeline

The production workflow deploys code pushed to `main` and optionally recreates or updates scheduled tasks. Resource cleanup differs by
platform:

- GitHub Actions uses a second event in the production workflow to clean up when a pull request closes.
- The GitLab and Azure incoming workflows clean up after each validation run.

### Create your CD workflow file

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Actions**.
2. From the left-hand side navigation, select **New workflow**.
3. Select **set up a workflow yourself** to create an empty workflow.
4. Name the file `pr_merged_slim_ci.yml`.
5. Copy and paste the following into the file:

   Copy code

   ```
   name: PR Accepted Deployment - Slim CI
   run-name: PR from ${{ github.actor }} accepted - triggered a ${{ github.event_name }}
   on:
     push:
       branches: [ main ]
     pull_request:
       types: [closed]
       branches: [main]

   permissions:
     contents: read
     id-token: write

   jobs:
     run-snowflake-dbt-job:
       if: github.event_name == 'push'
       name: "Run on Accepted PR - Slim CI"
       runs-on: ubuntu-latest
       environment: prod # Must match the OIDC subject's environment
       env:
         SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
         # SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }} # Required for PAT authentication
         # SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PAT }} # Required for PAT authentication
         SNOWFLAKE_DATABASE: ${{ vars.SNOWFLAKE_DATABASE }}
         SNOWFLAKE_SCHEMA: ${{ vars.SNOWFLAKE_SCHEMA }}

       steps:
         # Check out repository code
         # Gets the latest code from the pull request branch
         - name: Check out repository code
           uses: actions/checkout@v4

         - name: Install Snowflake CLI
           uses: snowflakedb/snowflake-actions@v3
           with: # Ensures Snowflake CLI will search for OIDC users matching this subject
             use-oidc: true

         - name: Check Snowflake CLI Version
           run: snow --version

         # The -x is shorthand for --temporary-connection
         - run: snow connection test -x

         # You can remove the "--source" flag if your dbt_project.yml is at root of your repo
         # The --default-target flag ensures the dbt project object executes with your prod target
         - name: Create a new dbt project object in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: |
             snow dbt deploy tasty_bytes_dbt_object_gh_action \
               --source ./tasty_bytes \
               --default-target prod \
               --no-auto-compile \
               --dbt-version 1.11.11 \
               -x

         - name: List all of the snowflake dbt project objects on your account
           run: snow dbt list -x

         # (optional) Uncomment the lines below and follow Step 7 if you want to manage Task orchestration via source control
         # - name: Run schedules.sql to create or alter tasks for tasty_bytes_dbt_object_gh_action
         #   run: snow sql -f ${{ github.workspace }}/tasty_bytes/schedules.sql -x

     clean-up-pull-request:
       if: github.event_name == 'pull_request'
       name: Clean up pull-request resources - Slim CI
       runs-on: ubuntu-latest
       environment: prod # Must match the OIDC subject's environment
       env:
         SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
         # SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }} # Required for PAT authentication
         # SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PAT }} # Required for PAT authentication
         SNOWFLAKE_DATABASE: ${{ vars.SNOWFLAKE_DATABASE }}
         SNOWFLAKE_SCHEMA: ${{ vars.SNOWFLAKE_SCHEMA }}

       steps:
         - name: Install Snowflake CLI
           uses: snowflakedb/snowflake-actions@v3
           with: # Ensures Snowflake CLI will search for OIDC users matching this subject
             use-oidc: true

         - name: Check Snowflake CLI Version
           run: snow --version

         # The -x is shorthand for --temporary-connection
         - run: snow connection test -x

         - name: Drop the tester dbt project object
           run: snow sql -x -q "DROP DBT PROJECT IF EXISTS tester_tasty_bytes_dbt_project_object_gh_action_pr_${{ github.event.pull_request.number }}"

         - name: Drop the per-PR database
           if: always()
           run: snow sql -x -q "DROP DATABASE IF EXISTS tasty_bytes_dbt_db_staging_pr_${{ github.event.pull_request.number }}"

         - name: List all of the snowflake dbt project objects in your account
           if: always()
           run: snow dbt list -x
   ```
6. Select **Commit changes** to save the file to `.github/workflows/pr_merged_slim_ci.yml`.
7. Navigate to the **Actions** tab of your repository to see your `pr_merged_slim_ci.yml` action start to run.

If you use PAT authentication, remove each `with` block that contains `use-oidc: true`, and uncomment the `SNOWFLAKE_USER` and
`SNOWFLAKE_PASSWORD` lines in both jobs.

Pull-request cleanup runs from the separate `closed` event, so it doesn’t depend on the production deployment job succeeding.

Add the following deploy job to your `.gitlab-ci.yml` file (after the CI test and cleanup jobs you created earlier):

Copy code

```
cd-deploy-dbt-slim-ci:
  extends: .configure-snowflake-cli
  stage: deploy
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  variables:
    SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER: $SNOWFLAKE_USER
    SNOWFLAKE_DATABASE: $SNOWFLAKE_DATABASE
    SNOWFLAKE_SCHEMA: $SNOWFLAKE_SCHEMA
  script:
    - snow --version
    # The -x is shorthand for --temporary-connection
    - snow connection test -x
    # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
    # The --default-target flag ensures the dbt project object executes with your prod target
    - >-
      snow dbt deploy tasty_bytes_dbt_object_gitlab
      --source ./tasty_bytes
      --default-target prod
      --no-auto-compile
      --dbt-version 1.11.11
      --git-commit "${CI_COMMIT_SHA}"
      --git-branch "${CI_COMMIT_REF_NAME}"
      -x
    - snow dbt list -x
    # (optional) Uncomment to manage Task orchestration via source control
    # - snow sql -f ./tasty_bytes/schedules.sql -x
```

Commit and push to `main` to trigger the deployment.

Create a file named `azure-pipelines-cd-slim-ci.yml` at the root of your repository:

Copy code

```
trigger:
  branches:
    include:
      - main

pr: none

pool:
  vmImage: 'ubuntu-latest'

variables:
  SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
  SNOWFLAKE_USER: $(SNOWFLAKE_USER)
  SNOWFLAKE_DATABASE: $(SNOWFLAKE_DATABASE)
  SNOWFLAKE_SCHEMA: $(SNOWFLAKE_SCHEMA)

steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'
      useWorkloadIdentity: true
      connectedServiceName: 'snowflake-wif-connection'

  - script: snow --version
    displayName: 'Check Snowflake CLI Version'

  # The -x is shorthand for --temporary-connection.
  # SNOWFLAKE_TOKEN is a pipeline secret — map it on every later snow step.
  - script: snow connection test -x
    displayName: 'Test Snowflake connection'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
  # The --default-target flag ensures the dbt project object executes with your prod target
  - script: |
      snow dbt deploy tasty_bytes_dbt_object_ado \
        --source ./tasty_bytes \
        --default-target prod \
        --no-auto-compile \
        --dbt-version 1.11.11 \
        --git-commit "$(Build.SourceVersion)" \
        --git-branch "$(Build.SourceBranchName)" \
        -x
    displayName: 'Deploy production dbt project object'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  - script: snow dbt list -x
    displayName: 'List dbt project objects'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)

  # (optional) Uncomment to manage Task orchestration via source control
  # - script: snow sql -f ./tasty_bytes/schedules.sql -x
  #   displayName: 'Run schedules.sql'
  #   env:
  #     SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

Create a second pipeline named `PR Accepted Deployment - Slim CI` in Azure DevOps pointing to this YAML file.

### Key pieces from the workflow file

- **Trigger**: Runs on updates to `main` after a merge or direct push.
- **Same OIDC authentication and `-x` flag** as the CI pipeline.
- **Steps**:
  1. Check out the repository code.
  2. Install Snowflake CLI with OIDC.
  3. Check the Snowflake CLI version and verify the connection with `snow connection test -x`.
  4. Deploy or update the production dbt project object with `snow dbt deploy ... --default-target prod --no-auto-compile -x`.
  5. List the dbt project objects with `snow dbt list -x`.
  6. Optionally run a `schedules.sql` file to manage tasks.
- **Cleanup**: GitHub cleans up resources when the pull request closes. GitLab and Azure clean up at the end of their CI pipelines.

The production dbt project object must complete at least one successful scheduled or otherwise initiated execution every 7 days so that
future Slim CI jobs can import its state.

## (Optional) Add orchestration with Snowflake tasks

To manage task orchestration from source control, create `schedules.sql` in the dbt project folder, then uncomment the optional
`schedules.sql` step in the production workflow.

The following example suspends an existing task, recreates or updates it, and resumes it:

Copy code

```
ALTER TASK IF EXISTS run_tasty_bytes_full SUSPEND;

CREATE OR ALTER TASK run_tasty_bytes_full
  WAREHOUSE = TASTY_BYTES_DBT_WH
  SCHEDULE = '12 hours'
  AS
    EXECUTE DBT PROJECT TASTY_BYTES_DBT_PROJECT
      ARGS = 'build --target prod';

ALTER TASK IF EXISTS run_tasty_bytes_full RESUME;
```

Replace the warehouse, task, and dbt project object names with your objects. Keep the optional `schedules.sql` step after deployment so that
tasks are updated only after deployment succeeds. A successful scheduled build also keeps production state available for future pull
requests.

## Verify the workflows

Open a pull request or merge request that changes a model. In the CI run, verify that:

1. The incoming workflow creates a database whose name contains the pull-request or merge-request number.
2. Snowflake CLI deploys a tester dbt project object with `--no-auto-compile`.
3. The workflow lists the tester dbt project object with `snow dbt list -x`.
4. The build step imports production state.
5. dbt selects changed models and their downstream dependencies.
6. Selected models write to the per-pull-request database.

Merge the pull request or merge request and verify that:

1. The pipeline triggered by the update to `main` deploys the production dbt project object.
2. The workflow lists the production dbt project object with `snow dbt list -x`.
3. If task deployment is enabled, the workflow recreates or updates the tasks.

Verify cleanup for your platform:

GitHub ActionsGitLab CI/CDAzure DevOps

Verify that the pull-request `closed` workflow run removes the tester object and per-pull-request database. Also close an unmerged test pull
request and verify that cleanup and the final `snow dbt list -x` step run without starting a production deployment.

Verify that the `cleanup-slim-ci` job removes the tester object and per-merge-request database after validation, including when a validation
command fails, and that the final list command runs.

Verify that the cleanup steps remove the tester object and per-pull-request database after validation, including when a validation command
fails, and that the final list step runs.

In Snowflake, use `SHOW DBT PROJECTS` and dbt project execution history to confirm the tester and production deployments. Deployment metadata
should identify the repository, branch, and commit.

## Adapt the cloning decision

Keep the per-pull-request clone when CI needs an independently writable snapshot of existing database state, such as when you test:

- DDL, migrations, or destructive operations.
- Incremental models against realistic existing target data.

For ordinary transformation changes, you can omit the clone and use an empty isolated database or schema as the CI write target. State
selection and defer continue to work as long as the CI role can read the required production relations.

## Clean up manually

The CI/CD workflows normally remove CI resources. If a workflow was disabled or interrupted, remove the resources manually:

Copy code

```
DROP DBT PROJECT IF EXISTS <database>.<schema>.<tester_project>;
DROP DATABASE IF EXISTS <per_pull_request_database>;
```

## Next steps

- [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod)
- [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables)
- [Best practices for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices)
- [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability)
