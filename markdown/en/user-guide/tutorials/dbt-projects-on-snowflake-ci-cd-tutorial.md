# Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake

## Introduction

This tutorial is a continuation of the
[Getting started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) tutorial.
It assumes you’ve already completed that tutorial and have a working Snowflake environment with your database, schemas, warehouse, and source
data set up.

This tutorial guides you through building a secure CI/CD pipeline for dbt Projects on Snowflake using OIDC authentication, Snowflake CLI, and
dbt project objects to automate testing, deployment, and orchestration with minimal overhead.

This is the introductory path: its CI job runs a full `dbt build` for thorough validation of the project. For a CI/CD workflow that creates
an isolated database for each pull request or merge request and uses Slim CI to run and test only changed models and their downstream
dependencies, see [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

The tutorial supports three CI/CD platforms: GitHub Actions, GitLab CI/CD, and Azure DevOps. Choose your platform in the tabbed
sections below and follow along.

For more information, see [Understand CI/CD for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-ci-cd).

### Overview

This tutorial walks you through the following steps:

1. Setting up your Snowflake environment:

   - You choose one of three ways to prepare dev and prod targets (full database clone, partial clone, or brand-new databases).
   - Your dbt project must include a [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file. This file refers to these dev and prod targets.
2. Setting up an OIDC service user for secure authentication: Instead of passwords or long-lived tokens, you create a Snowflake service user
   that trusts your CI/CD platform through [OpenID Connect](/user-guide/workload-identity-federation#label-wif-oidc-authentication-custom). This enables secure, short-lived, per-run
   authentication.
3. Setting up network policies: (Optional) If your Snowflake account restricts inbound IPs, you can add your CI/CD platform’s runner IPs to your service user’s network policy
   (using [Snowflake-managed network rules](/user-guide/network-rules#label-network-rules-working-with) where available). Otherwise, you can skip this step.
4. Storing secrets and variables in your CI/CD platform to configure Snowflake CLI in your workflows:

   - Your Snowflake account identifier
   - (Optionally) the Snowflake username
   - The target database and schema where dbt project objects will be deployed
5. Creating CI/CD pipeline workflows:

> - CI workflow that triggers on pull requests, deploys a tester dbt project object, and runs `dbt build` to build models and test them in DAG order.
>   If anything breaks, the pull request fails.
> - CD workflow that triggers on merges to main, deploys the production dbt project object, and optionally applies scheduling.

At the end of the tutorial, you will have:

- A fully automated, CI/CD-driven dbt workflow
- Secure OIDC authentication
- Consistent, tested deployments into Snowflake
- Version-controlled orchestration (optional)
- A repeatable template for scaling dbt workflows across teams

### Prerequisites

- **CI/CD platform** (one of the following):

  - **GitHub**: A repository with GitHub Actions enabled.
  - **GitLab**: A project with CI/CD pipelines enabled.
  - **Azure DevOps**: A project with Azure Pipelines enabled.
- **Snowflake**

  - Completion of the
    [Getting started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) tutorial,
    which sets up the `tasty_bytes_dbt_db` database, `dev`/`prod` schemas, `TASTY_BYTES_DBT_WH` warehouse, and source data.
  - Basic understanding of dbt Projects on Snowflake. For more information, see [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake).
  - A Snowflake account and user with privileges as described in [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).
  - Privileges or administrator assistance to create and edit the following:
    - CI/CD platform secrets or variables to specify the Snowflake account and (optional) username
    - A Snowflake service user
    - Network policy

Platform-specific reference guides

For detailed configuration options beyond what this tutorial covers, see the dedicated Snowflake CLI CI/CD guides:

- [Snowflake CLI CI/CD integration overview](/developer-guide/snowflake-cli/cicd/integrate-ci-cd)
- [GitLab CI/CD component](/developer-guide/snowflake-cli/cicd/gitlab-component)
- [Azure DevOps extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension)

## Set up your environment

Set up where your dbt project will read and write in Snowflake, then update your `profiles.yml` file.

### Create a warehouse, database, and schemas

Note

If you’ve already completed the
[Getting started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) tutorial
and run the `tasty_bytes_setup.sql` file, your warehouse (`TASTY_BYTES_DBT_WH`), database (`tasty_bytes_dbt_db`), and schemas (`dev`, `prod`)
already exist. You can skip this step. For details, see
[Run the SQL commands in tasty\_bytes\_setup.sql to set up source data](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial#label-dbt-get-started-set-up-tasty-bytes).

If you didn’t complete the getting-started tutorial, run the following SQL commands to create the warehouse, database, and schemas this
tutorial uses:

Copy code

```
CREATE WAREHOUSE IF NOT EXISTS TASTY_BYTES_DBT_WH;
CREATE DATABASE IF NOT EXISTS tasty_bytes_dbt_db;
CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.dev;
CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.prod;
```

Tip

If you already have a production database that you want to test against, you can use [zero-copy cloning](/sql-reference/sql/create-clone) to create a high-fidelity dev database without duplicating storage costs. Zero-copy cloning is cost-effective because you only pay for storage on rows that change during dbt runs.

- **Clone the full database** — gives you a complete replica of production:

  Copy code

  ```
  CREATE DATABASE IF NOT EXISTS tasty_bytes_dbt_db CLONE <your_production_db>;
  ```
- **Clone only specific schemas** — useful when you only need certain schemas for testing:

  Copy code

  ```
  CREATE DATABASE IF NOT EXISTS tasty_bytes_dbt_db;
  CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.dev CLONE <your_production_db>.dev;
  CREATE SCHEMA IF NOT EXISTS tasty_bytes_dbt_db.prod CLONE <your_production_db>.prod;
  ```

For either option, replace `<your_production_db>` with the name of your existing production database.

### Update your profile file

To manage CI/CD for a dbt project object, you must include `dbt_projects_profiles.yml` or `profiles.yml` inside your dbt project folder. The selected file defines your dev and prod targets and uses placeholder values that your CI/CD platform’s secrets or variables will later replace.

This tutorial uses `profiles.yml`. Alternatively, use `dbt_projects_profiles.yml`, which takes precedence if both files are present. For more information, see [Use dbt\_projects\_profiles.yml for a unified development-to-production experience](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file).

Edit `profiles.yml` to reference the dev and prod databases and schemas you created, as shown below:

Copy code

```
tasty_bytes:
  target: dev
  outputs:
    dev:
      account: '_' # Put any value here, it will be overwritten by a CI/CD platform secret or variable
      database: tasty_bytes_dbt_db
      schema: dev
      role: ACCOUNTADMIN # Use whichever role has USAGE on the database and schema
      type: snowflake
      warehouse: TASTY_BYTES_DBT_WH
      user: '_' # Put any value here, it will be overwritten by a CI/CD platform secret or variable
      threads: 8 # Snowflake recommends 8 threads
    prod:
      account: '_' # Put any value here, it will be overwritten by a CI/CD platform secret or variable
      database: tasty_bytes_dbt_db
      schema: prod
      role: ACCOUNTADMIN # Use whichever role has USAGE on the database and schema
      type: snowflake
      warehouse: TASTY_BYTES_DBT_WH
      user: '_' # Put any value here, it will be overwritten by a CI/CD platform secret or variable
      threads: 8 # Snowflake recommends 8 threads
```

Key points from the example:

- `target: dev` sets the default target of the dbt project. This value can be overridden by Snowflake CLI or a dbt project object.
- `dev` and `prod` both use `type: snowflake`.
- Database and schema point to the databases and schemas you created in the previous step (or already set up from the getting-started tutorial).
- Warehouse is the warehouse created in the getting-started tutorial (`TASTY_BYTES_DBT_WH`).
- Account and user are set to dummy values like ‘\_’ because they’ll be replaced by your CI/CD platform’s secrets or variables later.
- `threads: 8` sets the number of concurrent threads dbt uses. Snowflake recommends 8 threads.

## Create a CI/CD service user in Snowflake (recommended)

CI/CD pipelines run using the Snowflake user specified in your Snowflake CLI commands. To keep things clean and secure, create a dedicated
Snowflake user for all CI/CD workflows and grant it the required privileges.

### Recommended: OIDC-based service user

This approach uses OpenID Connect (OIDC) rather than long-lived credentials. The service user trusts your CI/CD platform as an identity
provider, allowing pipelines to request short-lived tokens for each run. For more information, see [Workload identity federation](/user-guide/workload-identity-federation).

Create an OIDC-based service user for your platform:

GitHub ActionsGitLab CI/CDAzure DevOps

Each OIDC service user must have a unique subject. Use a repo path and an environment name, for example
`repo:<org>/<repo>:environment:<environment_name>`. The environment name must match exactly in your GitHub Action YAML file.

Copy code

```
CREATE USER IF NOT EXISTS github_actions_service_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://token.actions.githubusercontent.com',
    SUBJECT = 'repo:your_repo_org/your_dbt_repo:environment:prod'
  )
  DEFAULT_ROLE = ACCOUNTADMIN
  COMMENT = 'Service user for GitHub Actions';
```

The subject uses GitLab’s project path format. Restrict it to a specific branch for tighter security.

Copy code

```
CREATE USER IF NOT EXISTS gitlab_cicd_service_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://gitlab.com'
    SUBJECT = 'project_path:your_group/your_dbt_repo:ref_type:branch:ref:main'
  )
  DEFAULT_ROLE = ACCOUNTADMIN
  COMMENT = 'Service user for GitLab CI/CD';
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
  DEFAULT_ROLE = ACCOUNTADMIN
  COMMENT = 'Service user for Azure DevOps';
```

For more information, see [Azure DevOps extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension).

After you create your user, explicitly grant the default role for the service user to assume that role. The DEFAULT\_ROLE parameter only sets the
user’s default role and doesn’t grant it. Then set a default warehouse.

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
GRANT ROLE ACCOUNTADMIN TO USER github_actions_service_user;

ALTER USER github_actions_service_user SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

Copy code

```
GRANT ROLE ACCOUNTADMIN TO USER gitlab_cicd_service_user;

ALTER USER gitlab_cicd_service_user SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

Copy code

```
GRANT ROLE ACCOUNTADMIN TO USER ado_cicd_service_user;

ALTER USER ado_cicd_service_user SET DEFAULT_WAREHOUSE = 'TASTY_BYTES_DBT_WH';
```

### Alternative: PAT-based authentication (less secure)

If you prefer to use one Snowflake user across multiple repositories, or cannot use OIDC, you can create the user with a personal access
token (PAT) instead.

This method is easier to reuse across repositories but less secure because it relies on long-lived credentials and requires manual rotation.

Copy code

```
CREATE USER IF NOT EXISTS github_actions_service_user
TYPE = SERVICE
COMMENT = 'Service user for GitHub Actions';

-- Grant the level of access to your user that can create network, auth policies,
-- and objects such as DBs and schemas
GRANT ROLE ACCOUNTADMIN TO USER github_actions_service_user;

-- Setting up databases and schemas to store policies and network rules
CREATE DATABASE IF NOT EXISTS github_actions_access_management;
CREATE SCHEMA IF NOT EXISTS github_actions_access_management.NETWORKS;
CREATE SCHEMA IF NOT EXISTS github_actions_access_management.POLICIES;

CREATE AUTHENTICATION POLICY github_actions_access_management.POLICIES.github_auth_policy
authentication_methods = ('PROGRAMMATIC_ACCESS_TOKEN')
pat_policy = (
default_expiry_in_days = 15, -- default value
max_expiry_in_days = 365, -- default value
network_policy_evaluation = ENFORCED_NOT_REQUIRED -- this is needed to ensure you can generate a PAT on Snowsight
);

ALTER USER github_actions_service_user SET AUTHENTICATION POLICY github_actions_access_management.POLICIES.github_auth_policy;
```

Note

This example uses GitHub-oriented names. If you’re on GitLab or Azure DevOps, substitute a service user name that matches your platform (for
example, `gitlab_cicd_service_user` or `ado_cicd_service_user`).

## (Optional) Set up a network policy for your CI/CD platform

Now that you’ve created the service user that Snowflake CLI will use, configure this user to connect to your Snowflake account from within your CI/CD platform.

Note

Creating or modifying network policies requires ACCOUNTADMIN or an equivalent role.

### Determine whether you need a network policy

- If your account restricts inbound access, you must create or update a network policy to add your CI/CD platform’s runner IPs to your allowlist. Snowflake
  simplifies this with Snowflake-managed network rules for some platforms. For more information, see [Network rules](/user-guide/network-rules).
- If your account does *not* restrict inbound access, no network policy changes are required.

If you’re unsure, skip this step for now and return only if you see an error like: `Incoming request with IP/Token <IP> is not allowed to access Snowflake.`

To create and apply a network policy to a user, choose one of the following options:

- Create a new network policy and assign it to the service user, or
- Add a network rule to an existing network policy that the user already uses.

Note

Before doing this, consult your Snowflake account admin. They must ensure the policy includes not only the CI/CD platform network rule but
also any other IP ranges your organization requires.

Once a network policy is applied, Snowflake restricts user access based on its allowed and blocked IP ranges. Your account admin might need
to adjust the policy or apply it account wide to avoid unintentionally blocking essential access.

#### Option 1: Create a new network policy and apply it to the user

A Snowflake user can have only one network policy at a time. If the user doesn’t have one or you want to replace the existing policy, complete
the following steps:

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
CREATE NETWORK POLICY github_actions_policy
  ALLOWED_NETWORK_RULE_LIST = ('SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL', <other required rules>)
  BLOCKED_NETWORK_RULE_LIST = ();

ALTER USER github_actions_service_user
  SET NETWORK_POLICY = github_actions_policy;
```

GitLab doesn’t have a Snowflake-managed network rule. GitLab.com hosted (shared) runners don’t have static, allowlistable IP addresses:
they run as ephemeral VMs drawn from large Google Cloud and AWS ranges, and [GitLab recommends against allowlisting those ranges](https://docs.gitlab.com/user/gitlab_com/#ip-range).
If your Snowflake account restricts inbound IPs, run your pipelines on a self-hosted GitLab Runner (or route runner egress through a proxy
with a fixed IP) and add that static IP to a network rule.

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

Azure DevOps doesn’t have a Snowflake-managed network rule. If you use Microsoft-hosted agents, allow the
[Azure DevOps service IP ranges](https://learn.microsoft.com/en-us/azure/devops/organizations/security/allow-list-ip-url). If you use
self-hosted agents, add your agent’s static IP.

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

#### Option 2: Add a network rule to an existing network policy

If the user already has a network policy, you can add the appropriate rule to it. First, check the user’s current network policy:

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
-- Check the user's current network policy:
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER github_actions_service_user;
```

Copy code

```
-- Check the user's current network policy:
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER gitlab_cicd_service_user;
```

Copy code

```
-- Check the user's current network policy:
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER ado_cicd_service_user;
```

Note

If the network policy is applied at the account level or shared by many users, updating it will affect everyone.

GitHub ActionsGitLab CI/CDAzure DevOps

Copy code

```
-- Add the new rule:
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL');
```

Copy code

```
-- Add the new rule:
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('gitlab_runner_rule');
```

Copy code

```
-- Add the new rule:
ALTER NETWORK POLICY <name>
  ADD ALLOWED_NETWORK_RULE_LIST = ('ado_agent_rule');
```

The user inherits the update automatically since they’re already assigned to this policy.

## Configure CI/CD secrets and variables

Your CI/CD pipelines use Snowflake CLI to connect to your Snowflake account, so you must configure platform secrets and variables
first. This is how the CI/CD integration passes Snowflake account info into Snowflake CLI inside pipeline workflows.

### Configure secrets

Add secrets to securely store the information Snowflake CLI needs to identify your Snowflake account and, if required, the user it should
authenticate as.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Settings**.
2. From the left-hand side navigation, select **Secrets and variables** » **Actions**.
3. Under **Secrets**, select **New repository secret**.
4. Add a secret to connect your Snowflake account:

   - **Name**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier (for example, `org_name-account_name`). This value tells Snowflake CLI which
     account you want to connect to.
5. Select **Add secret**.
6. (Optional) If you aren’t using OIDC, select **New repository secret** to specify the Snowflake username the CLI should use when connecting. It specifies which
   user credentials to run commands under.

   - **Name**: `SNOWFLAKE_USER`
   - **Value**: Optional if you’re using OIDC or credential-less authentication.
     - With OIDC, Snowflake CLI automatically matches the GitHub Action’s subject to the OIDC service user (created in Step 3), so this is
       not required.
     - Without OIDC, you must specify a user (and supply password or key credentials). As a recommended best practice, you should create
       a personal access token in Snowsight. For more information, see [Generating a programmatic access token](/user-guide/programmatic-access-tokens#label-pat-generate).
7. Select **Add secret**.
8. (Optional) If you aren’t using OIDC, select **New repository secret** to specify the service user’s personal access token that the CLI should use when connecting.

   - **Name**: `SNOWFLAKE_PAT`
   - **Value**: Optional if you’re using OIDC or credential-less authentication.

1. In your GitLab project, go to **Settings** » **CI/CD**.
2. Expand the **Variables** section.
3. Select **Add variable**.
4. Add a variable for your Snowflake account:

   - **Key**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier (for example, `org_name-account_name`).
   - Enable **Mask variable** to keep it hidden in job logs.
5. Select **Add variable**.
6. Add a variable for your Snowflake user:

   - **Key**: `SNOWFLAKE_USER`
   - **Value**: The service user you created (for example, `gitlab_cicd_service_user`).
   - Enable **Mask variable**.
7. Select **Add variable**.
8. (Optional) If you aren’t using OIDC, add a variable for the PAT:

   - **Key**: `SNOWFLAKE_PASSWORD`
   - **Value**: The personal access token.
   - Enable **Mask variable** and **Protect variable**.

1. In your Azure DevOps project, go to **Pipelines** » **Library**.
2. Select **+ Variable group** or open an existing variable group.
3. Add a variable for your Snowflake account:

   - **Name**: `SNOWFLAKE_ACCOUNT`
   - **Value**: Your Snowflake account identifier (for example, `org_name-account_name`).
   - Select the lock icon to mark it as secret.
4. Add a variable for your Snowflake user:

   - **Name**: `SNOWFLAKE_USER`
   - **Value**: The service user you created (for example, `ado_cicd_service_user`).
   - Select the lock icon to mark it as secret.
5. (Optional) If you aren’t using OIDC, add a variable for the PAT:

   - **Name**: `SNOWFLAKE_PASSWORD`
   - **Value**: The personal access token.
   - Select the lock icon to mark it as secret.
6. Select **Save**.
7. Link this variable group to your pipeline in the pipeline YAML or pipeline settings.

### Configure variables

These help Snowflake CLI connect to the right database and schema.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Settings**.
2. From the left-hand side navigation, select **Secrets and variables** » **Actions**.
3. Under **Variables**, select **New repository variable**.
4. Add a database variable:

   - **Name**: `SNOWFLAKE_DATABASE`
   - **Value**: Enter an existing database where the dbt project object will be created.
5. Select **Add variable**.
6. Add a schema variable:

   - **Name**: `SNOWFLAKE_SCHEMA`
   - **Value**: Enter an existing schema where the dbt project object will be created.
7. Select **Add variable**.

1. In your GitLab project, go to **Settings** » **CI/CD**.
2. Expand the **Variables** section.
3. Add a variable for your database:

   - **Key**: `SNOWFLAKE_DATABASE`
   - **Value**: Enter an existing database where the dbt project object will be created.
4. Add a variable for your schema:

   - **Key**: `SNOWFLAKE_SCHEMA`
   - **Value**: Enter an existing schema where the dbt project object will be created.

Add these to the same variable group you created for secrets, or define them as pipeline variables:

1. Add a database variable:

   - **Name**: `SNOWFLAKE_DATABASE`
   - **Value**: Enter an existing database where the dbt project object will be created.
2. Add a schema variable:

   - **Name**: `SNOWFLAKE_SCHEMA`
   - **Value**: Enter an existing schema where the dbt project object will be created.
3. Select **Save**.

## Create your Continuous Integration (CI) pipeline

This step is where automation starts. This CI workflow runs whenever a pull request (or merge request) targets main. It:

1. Creates a tester dbt project object in Snowflake
2. Runs `dbt build` against your dev target, which builds all models and runs tests in DAG order, failing early if any test fails
3. Fails the pull request (or merge request) if the dbt execution fails

### Create your CI workflow file

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Actions**.
2. From the left-hand side navigation, select **New workflow**.
3. Select **set up a workflow yourself** to create an empty workflow.
4. Name the file `incoming_pr.yml`.
5. Copy and paste the following into the file:

   Copy code

   ```
   name: Incoming PR
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
       name: "Run on Incoming PR"
       runs-on: ubuntu-latest
       environment: prod # Must match the OIDC subject's environment
       env:
         SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
         # SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }} # Required if you aren't using OIDC
         # SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PAT }} # Snowflake password is required if you aren't using OIDC
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

         # You can remove the "--source" flag if your dbt_project.yml is at root of your repo
         - name: Create a new tester dbt project object in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: snow dbt deploy tester_tasty_bytes_dbt_project_object_gh_action --source ./tasty_bytes --dbt-version 1.11.11 -x

         - name: List all of the snowflake dbt project objects in your account
           run: snow dbt list -x

         # Builds all models and runs tests in DAG order, failing early if any upstream test breaks
         - name: Build and test dbt project in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: snow dbt execute -x tester_tasty_bytes_dbt_project_object_gh_action build --target dev
   ```
6. Select **Commit changes**.
7. Select **Create a new branch for this commit and start a pull request**.
8. Select **Propose changes**.
9. After you finish submitting the pull request, you should see your `incoming_pr.yml` action start to run.
10. After it’s merged, the file will be saved to `.github/workflows/incoming_pr.yml`.

Create a `.gitlab-ci.yml` file at the root of your repository (or add the following to your existing one):

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      use-oidc: true
      template-only: true

stages:
  - test
  - deploy

ci-test-dbt:
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
    # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
    - >-
      snow dbt deploy tester_tasty_bytes_dbt_project_object_gitlab
      --source ./tasty_bytes
      --dbt-version 1.11.11
      --git-url "${CI_PROJECT_URL}"
      --git-commit "${CI_COMMIT_SHA}"
      --git-branch "${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME}"
      -x
    - snow dbt list -x
    # Builds all models and runs tests in DAG order, failing early if any upstream test breaks
    - snow dbt execute -x tester_tasty_bytes_dbt_project_object_gitlab build --target dev
```

Commit this file to a branch and open a merge request to see the pipeline run.

Create a file named `azure-pipelines-ci.yml` at the root of your repository:

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

  # You can remove the "--source" flag if your dbt_project.yml is at the root of your repo
  - script: |
      snow dbt deploy tester_tasty_bytes_dbt_project_object_ado \
        --source ./tasty_bytes \
        --dbt-version 1.11.11 \
        --git-url "$(Build.Repository.Uri)" \
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

  # Builds all models and runs tests in DAG order, failing early if any upstream test breaks
  - script: snow dbt execute -x tester_tasty_bytes_dbt_project_object_ado build --target dev
    displayName: 'Build and test dbt project'
    env:
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

In Azure DevOps, go to **Pipelines** » **New pipeline**, select your repository, and point it to this YAML file.

When `snow dbt deploy` runs in GitHub Actions, Snowflake CLI automatically captures the repository URL, commit, and branch. The GitLab and
Azure DevOps workflows must explicitly pass `--git-url`, `--git-commit`, and `--git-branch`. These flags record the source repository, commit,
and branch in the dbt project object’s deployment metadata.

Use these CI-provided values for the repository URL:

- **GitLab CI/CD:** Use `$CI_PROJECT_URL`, for example, `https://gitlab.com/acme/my-dbt-project`. Don’t use `$CI_REPOSITORY_URL`, which can
  contain a temporary job token.
- **Azure DevOps:** Use `$(Build.Repository.Uri)`, for example, `https://dev.azure.com/acme/data/_git/my-dbt-project`.

### Key pieces from the workflow file

Regardless of which platform you chose, the pipeline follows the same pattern:

- **Trigger**: Runs on incoming pull requests (or merge requests) targeting `main`.
- **OIDC authentication**: Each platform requests a short-lived token that Snowflake validates against your service user’s WORKLOAD\_IDENTITY configuration.
- **Snowflake CLI with `-x` flag**: The `-x` flag (`--temporary-connection`) tells Snowflake CLI to build the connection from environment variables
  (such as `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_DATABASE`) rather than reading a named profile from `config.toml`, which isn’t available in a CI/CD runner.
- **Steps in the job**:

  1. Check out repository code.
  2. Install Snowflake CLI with OIDC enabled.
  3. Verify the connection with `snow connection test -x`.
  4. Deploy a tester dbt project object using `snow dbt deploy ... -x` (with `--source` if the dbt project is in a subfolder).
  5. Build and test the dbt project in DAG order:

     `snow dbt execute -x tester_tasty_bytes_dbt_project_object build --target dev`

     Using `build` instead of separate `run` and `test` commands ensures that tests execute immediately after each model is built, in
     dependency order. If an upstream model’s test fails, downstream models aren’t built, providing faster feedback and preventing invalid
     data from propagating.
- Once you commit this new workflow on a branch and open a pull request (or merge request), the pipeline will run. If the dbt project object fails to build a model
  or any test fails, the CI check fails and the change can’t be merged.

## Create your Continuous Deployment (CD) pipeline

The CD workflow runs after code is merged to main (or any direct push to main), ensuring the dbt project object in Snowflake reflects the
latest code.

### Create your CD workflow file

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

GitHub ActionsGitLab CI/CDAzure DevOps

1. In your GitHub repository, go to **Actions**.
2. From the left-hand side navigation, select **New workflow**.
3. Select **set up a workflow yourself** to create an empty workflow.
4. Name the file `pr_merged.yml`.
5. Copy and paste the following into the file:

   Copy code

   ```
   name: PR Accepted Deployment
   run-name: PR from ${{ github.actor }} accepted - triggered a ${{ github.event_name }}
   on:
     push:
       branches: [ main ]

   permissions:
     contents: read
     id-token: write

   jobs:
     run-snowflake-dbt-job:
       name: "Run on Accepted PR"
       runs-on: ubuntu-latest
       environment: prod # Must match the OIDC subject's environment
       env:
         SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
         # SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }} # Required if you aren't using OIDC
         # SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PAT }} # Snowflake password is required if you aren't using OIDC
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
         # The --default-target flag ensures the dbt project object compiles and executes with your prod target
         - name: Create a new dbt project object in ${{ vars.SNOWFLAKE_DATABASE }}.${{ vars.SNOWFLAKE_SCHEMA }}
           run: snow dbt deploy tasty_bytes_dbt_object_gh_action --source ./tasty_bytes --default-target prod --dbt-version 1.11.11 -x

         - name: List all of the snowflake dbt project objects on your account
           run: snow dbt list -x

         # (optional) Uncomment the lines below and follow Step 7 if you want to manage Task orchestration via source control
         # - name: Run schedules.sql to create or alter tasks for tasty_bytes_dbt_object_gh_action
         #   run: snow sql -f ${{ github.workspace }}/tasty_bytes/schedules.sql -x
   ```
6. Select **Commit changes** to save the file to `.github/workflows/pr_merged.yml`.
7. Navigate to the **Actions** tab of your repository to see your `pr_merged.yml` action start to run.

Add the following deploy job to your `.gitlab-ci.yml` file (after the CI test job you created earlier):

Copy code

```
cd-deploy-dbt:
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
    # The --default-target flag ensures the dbt project object compiles and executes with your prod target
    - >-
      snow dbt deploy tasty_bytes_dbt_object_gitlab
      --source ./tasty_bytes
      --default-target prod
      --dbt-version 1.11.11
      --git-url "${CI_PROJECT_URL}"
      --git-commit "${CI_COMMIT_SHA}"
      --git-branch "${CI_COMMIT_REF_NAME}"
      -x
    - snow dbt list -x
    # (optional) Uncomment to manage Task orchestration via source control
    # - snow sql -f ./tasty_bytes/schedules.sql -x
```

Commit and push to `main` to trigger the deployment.

Create a file named `azure-pipelines-cd.yml` at the root of your repository:

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
  # The --default-target flag ensures the dbt project object compiles and executes with your prod target
  - script: |
      snow dbt deploy tasty_bytes_dbt_object_ado \
        --source ./tasty_bytes \
        --default-target prod \
        --dbt-version 1.11.11 \
        --git-url "$(Build.Repository.Uri)" \
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

Create a second pipeline in Azure DevOps pointing to this YAML file.

### Key pieces from the workflow file

- **Trigger**: Runs on pushes to `main` (after a merge).
- **Same OIDC authentication and `-x` flag** as the CI pipeline.
- **Steps**:

  1. Check out the repository code.
  2. Install Snowflake CLI with OIDC.
  3. Verify the connection with `snow connection test -x`.
  4. Deploy/update the production dbt project object with `snow dbt deploy ... --default-target prod -x`.
  5. (Optional) Run a `schedules.sql` file to manage tasks (see next section).
- Once this workflow is in place, every successful merge to main updates the dbt project object in Snowflake.

## (Optional) Add orchestration with Snowflake tasks

Orchestrate executions of your dbt project object using a `schedules.sql` file and Snowflake tasks (triggered from the CD workflow):

1. In your repository, navigate to your dbt project (for example, `tasty_bytes/`).
2. Create a file named `schedules.sql` and copy and paste the following into the file.

   This file:

   - Suspends any existing tasks
   - Creates or alters tasks to:

     - Run a subset of the DAG on a schedule, failing early if any test fails
     - Run the full project, failing early if any test fails
   - Resumes tasks in the correct order (child → root)

   GitHub ActionsGitLab CI/CDAzure DevOps

   Copy code

   ```
   -- To avoid issues with CREATE OR ALTER, suspend all of the tasks from root to child
   -- ALTER TASK IF EXISTS ensures this file can execute on first run each time a task is added
   ALTER TASK IF EXISTS run_tasty_bytes_subset SUSPEND;
   ALTER TASK IF EXISTS run_tasty_bytes_full SUSPEND;

   -- Example of a subset that needs to be available early for business needs.
   -- If tests fail here, the next task won't run
   CREATE OR ALTER TASK run_tasty_bytes_subset
     WAREHOUSE = TASTY_BYTES_DBT_WH
     SCHEDULE = '12 hours'
     AS
      execute dbt project tasty_bytes_dbt_object_gh_action args='build --select raw_customers stg_customers customers --target prod';

   -- Builds all models and runs tests in DAG order, failing early if any upstream test breaks
   CREATE OR ALTER TASK run_tasty_bytes_full
     WAREHOUSE = TASTY_BYTES_DBT_WH
     AFTER run_tasty_bytes_subset
     AS
      execute dbt project tasty_bytes_dbt_object_gh_action args='build --target prod';

   -- When a task is first created or if an existing task is paused, it MUST BE RESUMED to be activated
   -- The tasks must be enabled in REVERSE ORDER from child to root
   ALTER TASK IF EXISTS run_tasty_bytes_full RESUME;
   ALTER TASK IF EXISTS run_tasty_bytes_subset RESUME;
   ```

   Copy code

   ```
   -- To avoid issues with CREATE OR ALTER, suspend all of the tasks from root to child
   -- ALTER TASK IF EXISTS ensures this file can execute on first run each time a task is added
   ALTER TASK IF EXISTS run_tasty_bytes_subset SUSPEND;
   ALTER TASK IF EXISTS run_tasty_bytes_full SUSPEND;

   -- Example of a subset that needs to be available early for business needs.
   -- If tests fail here, the next task won't run
   CREATE OR ALTER TASK run_tasty_bytes_subset
     WAREHOUSE = TASTY_BYTES_DBT_WH
     SCHEDULE = '12 hours'
     AS
      execute dbt project tasty_bytes_dbt_object_gitlab args='build --select raw_customers stg_customers customers --target prod';

   -- Builds all models and runs tests in DAG order, failing early if any upstream test breaks
   CREATE OR ALTER TASK run_tasty_bytes_full
     WAREHOUSE = TASTY_BYTES_DBT_WH
     AFTER run_tasty_bytes_subset
     AS
      execute dbt project tasty_bytes_dbt_object_gitlab args='build --target prod';

   -- When a task is first created or if an existing task is paused, it MUST BE RESUMED to be activated
   -- The tasks must be enabled in REVERSE ORDER from child to root
   ALTER TASK IF EXISTS run_tasty_bytes_full RESUME;
   ALTER TASK IF EXISTS run_tasty_bytes_subset RESUME;
   ```

   Copy code

   ```
   -- To avoid issues with CREATE OR ALTER, suspend all of the tasks from root to child
   -- ALTER TASK IF EXISTS ensures this file can execute on first run each time a task is added
   ALTER TASK IF EXISTS run_tasty_bytes_subset SUSPEND;
   ALTER TASK IF EXISTS run_tasty_bytes_full SUSPEND;

   -- Example of a subset that needs to be available early for business needs.
   -- If tests fail here, the next task won't run
   CREATE OR ALTER TASK run_tasty_bytes_subset
     WAREHOUSE = TASTY_BYTES_DBT_WH
     SCHEDULE = '12 hours'
     AS
      execute dbt project tasty_bytes_dbt_object_ado args='build --select raw_customers stg_customers customers --target prod';

   -- Builds all models and runs tests in DAG order, failing early if any upstream test breaks
   CREATE OR ALTER TASK run_tasty_bytes_full
     WAREHOUSE = TASTY_BYTES_DBT_WH
     AFTER run_tasty_bytes_subset
     AS
      execute dbt project tasty_bytes_dbt_object_ado args='build --target prod';

   -- When a task is first created or if an existing task is paused, it MUST BE RESUMED to be activated
   -- The tasks must be enabled in REVERSE ORDER from child to root
   ALTER TASK IF EXISTS run_tasty_bytes_full RESUME;
   ALTER TASK IF EXISTS run_tasty_bytes_subset RESUME;
   ```
3. Commit the file to your repository.
4. In the CD workflow file you created earlier, uncomment the step that runs `schedules.sql` (see the commented `schedules.sql` line in your CD pipeline).
5. Commit the change.

## Next steps

Next steps to improve your workflow:

- Add a Slim CI workflow that uses per-pull-request zero-copy clone databases:

  Follow the [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial) to import recent production state, process only changed models and their downstream dependencies, and clean up pull-request resources.

  That workflow uses a [zero-copy clone](/sql-reference/sql/create-clone) when CI needs a realistic database it can modify. A clone is an isolation choice, not a requirement for Slim CI.
- Add alerting:

  Configure Slack or email notifications in your CI/CD platform, or use Snowflake task error notifications.

  For more information, see [Configure a task to send error notifications](/user-guide/tasks-errors-integrate).
- Explore the platform-specific Snowflake CLI CI/CD reference guides for advanced configuration:

  - [Snowflake CLI CI/CD integration overview](/developer-guide/snowflake-cli/cicd/integrate-ci-cd)
  - [GitLab CI/CD component](/developer-guide/snowflake-cli/cicd/gitlab-component)
  - [Azure DevOps extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension)
- Explore [Managing dbt Projects on Snowflake using Snowflake CLI](/developer-guide/snowflake-cli/data-pipelines/dbt-projects).
