# Using SQL environment variables in dbt Projects on Snowflake

Environment variables have been part of dbt Core for years, but managing them at scale has always meant stitching together `.env` files across a growing team of engineers. These files live on individual machines, drift out of sync, and can’t be reviewed or audited. The dbt Projects on Snowflake `env.yml` is a single, Git-versioned file that provides SQL in YAML capabilities alongside Snowflake secrets support to let admins manage per-developer schemas, dynamic runtime values, secrets, and CI/CD configurations in one place, unlocking workflows dbt Core can’t offer on its own.

This guide covers:

- **[Concepts](#concepts):** How the `env.yml` file works, the `env:` and `secrets:` sections, environments and value precedence, and the naming and casing rules.
- **[Admin setup](#admin-setup):** Importing private Git packages (shared macros, sub-projects in a monorepo, or another team’s dbt project) by configuring a Snowflake secret, network rule, and external access integration. This is how cross-project references work at the dbt Core level.
- **[Using environment variables](#start-using-environment-variables):** Authoring an `env.yml` file to define one or more environments (for example, dev and prod), configuring [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` to read them, writing a model that consumes them, and running your project in Workspaces and as a dbt project object with SQL.
- **[Use the Snowflake CLI](#label-dbt-env-vars-cli):** Wiring environment variables into CI/CD workflows.
- **[Observability](#observability):** Seeing which environment and variable overrides each run used.
- **[Reference](#reference):** Supported context functions and Jinja helpers, environment selection and value precedence tables, and naming rules.

Administrators set up the shared building blocks (Snowflake secrets, the network rule, and the external access integration) in [Admin setup](#admin-setup). Data engineers author the project files (`env.yml`, `dbt_projects_profiles.yml` or `profiles.yml`, `packages.yml`, and models) and run the project, starting with [Start using environment variables](#start-using-environment-variables).

The `env.yml` file works across Workspaces, deployed dbt project objects (through SQL and the Snowflake CLI), and CoCo Desktop in Snowflake-managed mode. For how it works in CoCo Desktop, see [SQL environment variables and private Git package support](/user-guide/cortex-code/cortex-code-desktop/dbt-integration#label-coco-desktop-dbt-env-vars).

## Concepts

### What is the env.yml file?

The `env.yml` file is a project-level configuration file that defines the environment variables and secrets for your dbt project. A few things make it different from a dbt Core `.env` file:

- **Runs before dbt Core or dbt Fusion execution begins:** When you run your project, Snowflake resolves the `env.yml` file first and injects the resulting environment variables into the run. Only then does dbt Core start. This is why values can come from live SQL (for example, the current timestamp) and from Snowflake secrets: they’re computed at the start of the run, before your models execute.
- **Uses your Snowflake execution context, not your profile file:** Context functions like `CURRENT_ROLE()`, `CURRENT_USER()`, and `CURRENT_WAREHOUSE()` resolve based on the role, user, and warehouse of the outer session that runs `EXECUTE DBT PROJECT` (whether that’s a Workspaces session, a Snowflake Task, or a Snowflake CLI call), not the role defined in `dbt_projects_profiles.yml` or `profiles.yml`. The same applies to every Snowflake secret resolution and SELECT query.
- **Lives at the root of your dbt project:** Place `env.yml` in the same folder as your `dbt_project.yml`. During execution, Workspaces and the dbt project object expect to find it there.
- **Git-versioned and auditable:** Unlike `.env` files that live on a developer’s machine, `env.yml` is version-controlled. An admin can adjust the set of env vars a team needs and commit the change so the whole team benefits from this unified configuration.
- **Flexible:** Developers can override individual env vars within Workspaces or during dbt project object execution.
- **Supports multiple environments:** One file can define dev, prod, staging, and any other environments you need.

The file has a 2 MB size limit, which supports roughly 12,000 lines.

### Structure of the file

Copy code

```
env_config: # Top-level key. Required.
  default_environment: my_env_dev # The environment used when not specified at run time.
  environments: # The list of available environments.
    - name: my_env_dev # You name each environment.
      secrets: # Snowflake secrets injected as masked env vars.
        - snowflake_secret: my_db.my_schema.my_token
          env_var_name: DBT_ENV_SECRET_GIT_CREDENTIAL
      env: # Plain environment variables (text or SQL that returns VARCHAR).
        DBT_CURRENT_ROLE: "{{ select CURRENT_ROLE() }}"
        DBT_HARDCODED: VALUE
```

### The env: and secrets: sections

Each environment entry has two optional sections that serve different purposes.

**`env:` values** dynamically configure a dbt execution. You can use env vars to create per-developer schemas. This allows large eng teams to avoid collisions during development. Also, Snowflake’s SQL in YAML capabilities can compute Airflow-style data-window timestamps at run time without an orchestrator or wire up CI/CD pipelines to dynamically create and run against a database named after a pull request number, all without changing a single line in your dbt models.

Values can be plain text or any SQL query that returns one row and one column of type `VARCHAR`, including full table queries like `SELECT column FROM your_control_table` and stored procedures called with `SELECT * FROM TABLE(...)`. Wrap any SQL query in double quotes so Jinja parses it correctly. For start-of-day and end-of-day time-window examples, see [Author your env.yml file](#label-dbt-env-vars-author-envyml). For stored procedure examples, see [Call stored procedures from env.yml](#call-stored-procedures-from-envyml).

**`secrets:` values** pull Snowflake-managed credentials into a run. The primary use is authenticating `dbt deps` calls: pulling in private Git packages from another team’s repository, or, if your team uses a monorepo, referencing sub-projects within the same Git repository. Once injected, the secret value is available as a `DBT_ENV_SECRET_` prefixed variable. This uses dbt Core best practices to mask the value to `****` in all logs. The supported context variables are `{{ current_user }}`, `{{ current_account }}`, `{{ current_account_name }}`, and `{{ current_organization_name }}`. We recommend using `{{ current_user }}` inside the `snowflake_secret` reference to provide each engineer their own personal secret. We recommend using secrets only in `packages.yml` to authenticate `dbt deps` calls to private Git repositories. Avoid referencing `DBT_ENV_SECRET_` variables in models, macros, or other dbt artifacts.

Macros aren’t allowed anywhere in the `env.yml` file. Since standard dbt Core env vars must resolve before a macro can use them, allowing macros inside the env.yml would create a circular dependency.

### Environments and the default environment

Each entry under `environments:` is a named environment that defines a set of variable keys and their values. There are two separate kinds of precedence to keep straight.

Exactly one environment is active per execution. It’s chosen in this order, highest priority first (see [Environment selection](#environment-selection-highest-to-lowest)):

1. `ENVIRONMENT = '...'` on `EXECUTE DBT PROJECT` (highest).
2. `DEFAULT_ENVIRONMENT` set on the dbt project object.
3. `default_environment` in `env.yml`.

In Workspaces, you choose the environment using the environment selector in the run panel before starting a run. See [Run your project in Workspaces](#run-your-project-in-workspaces).

After the active environment is chosen, individual variable values are resolved in this order, highest priority first (see [Value precedence](#value-precedence-highest-to-lowest)):

1. `--env-vars` / `EXECUTE ... ENV_VARS` (highest). Merges into the selected environment and takes final precedence.
2. Shell environment variables. Only when using `--use-shell-env-vars`. All shell variables prefixed with `DBT_` are used (excluding `DBT_ENV_SECRET_*` variables), including those not defined in `env.yml`.
3. `env.yml` selected `default_environment:`. The default configuration in the file. This takes lowest precedence.

To run with no environment at all, use the reserved name `NO_ENV`. See [Run without an environment (NO\_ENV)](#run-without-an-environment-no_env).

### Naming and casing rules

These rules are enforced on every run. If you break them, the run fails.

- Every key in `env:` and in any override must be prefixed with `DBT_` (this includes `DBT_ENV_CUSTOM_ENV_` and `DBT_ENV_SECRET_`).
- Every key must be UPPERCASE.
- Every key in the `secrets:` section must be prefixed with `DBT_ENV_SECRET_`. dbt masks the value of any `DBT_ENV_SECRET_` variable to `****` in logs and error messages.
- Key names (the left-hand side) must be plain text. They can’t be SQL.

Environment names are case sensitive and can contain English letters, numbers, and underscores, up to 256 characters.

## Admin setup

Skip this section unless your dbt project pulls in private Git packages. This section covers two common scenarios:

- **Monorepo pattern:** Your team maintains multiple dbt projects in a single private Git repository. You import a subfolder of that repo as a package using the `subdirectory:` key in `packages.yml`.
- **Separate repo pattern:** Another team owns a private Git repository with a dbt project you depend on. You import the entire repo (or a subfolder of it) as a package.

Both patterns use the same mechanism: a Snowflake secret holding a Git access token, a network rule allowing traffic to the Git host, and an external access integration that ties them together. Once set up, `dbt deps` authenticates with your Git provider and pulls in the package. You then reference its models using dbt Core’s two-argument `ref()`, which is how cross-project references work at the dbt Core level.

Here’s what the end result looks like in your `packages.yml`:

Copy code

```
packages:
  # ...other packages
  - git: "https://{{env_var('DBT_ENV_SECRET_GIT_TOKEN')}}@github.com/my-github-account/jaffle-shop-demo.git"
    subdirectory: "jaffle-shop"
    revision: a47561234f73937cf58589ca2247475b40341237
```

The rest of this section walks you through each piece needed to get there.

Tip

Including a `secrets:` section in your environment requires you to select an external access integration each time you run a command. If you aren’t running `dbt deps` (or a command that needs a secret), comment out the `secrets:` block in your `env.yml` to skip this requirement.

### Create a Snowflake secret

Store sensitive values, such as Git access tokens, as Snowflake secret objects rather than hardcoding them. You reference the secret from `env.yml`, and Snowflake injects it as a masked environment variable at run time.

The simplest approach is a single team-wide secret that your dbt project references across all environments. When you create the Git access token for this secret, scope it to read-only access (for example, GitHub’s “Contents: Read-only” repository permission). This matches the access your team members already have to the repository itself, so a shared token doesn’t grant broader access than they’d have individually.

First create the token in your Git provider. For GitHub, follow [Creating a personal access token](https://docs.github.com/en/enterprise-server@3.1/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token). Then store the value in a Snowflake secret and grant `READ` to your team’s shared role:

Copy code

```
CREATE OR REPLACE SECRET tasty_bytes_dbt_db.integrations.tb_dbt_git_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = 'ghp_...<your read-only token>';

GRANT READ ON SECRET tasty_bytes_dbt_db.integrations.tb_dbt_git_secret TO ROLE data_engineer;
```

For more granular control, create individual secrets per developer so each token is independently revocable. The `env.yml` resolves `{{ current_user }}` at run time, so name each engineer’s secret with their user name:

Copy code

```
CREATE OR REPLACE SECRET tasty_bytes_dbt_db.integrations.jdoe_personal_git_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = 'ghp_...<your token>';

GRANT READ ON SECRET tasty_bytes_dbt_db.integrations.jdoe_personal_git_secret TO USER jdoe;
```

Privileges granted directly to a user are only effective when that user has all secondary roles enabled. For more information, see [GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user).

For CI/CD pipelines, create a separate secret for the service account and grant `READ` to the service account user (for example, the `github_actions_service_user` created in the CI/CD tutorial). Skip this step if your repository already includes a complete `dbt_packages` folder with all dependencies checked in. In that case, you can deploy the project object directly without running `dbt deps`.

Copy code

```
CREATE OR REPLACE SECRET tasty_bytes_dbt_db.integrations.tb_dbt_github_actions_git_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = 'ghp_...<your token>';

GRANT READ ON SECRET tasty_bytes_dbt_db.integrations.tb_dbt_github_actions_git_secret TO USER github_actions_service_user;
```

If you already have a secret object and need to rotate the value, use `ALTER SECRET` instead of `CREATE OR REPLACE` to avoid accidentally resetting other properties.

Copy code

```
ALTER SECRET tasty_bytes_dbt_db.integrations.tb_dbt_github_actions_git_secret SET SECRET_STRING = 'ghp_...<new token>';
```

If you connect Workspaces to a private Git repository, authorize the secret in your Git API integration too, the same `tb_dbt_git_api_integration` you use to deploy dbt projects.

Copy code

```
CREATE OR REPLACE API INTEGRATION tb_dbt_git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/my-github-account')
  ALLOWED_AUTHENTICATION_SECRETS = (
    tasty_bytes_dbt_db.integrations.tb_dbt_git_secret,
    tasty_bytes_dbt_db.integrations.tb_dbt_github_actions_git_secret
  )
  ENABLED = TRUE;
```

The executing role needs `READ` or `OWNERSHIP` on the secret to use it in a run.

### Allow private Git traffic (update the network rule)

To pull in private Git packages, an administrator updates the network rule to allow traffic to your Git host. If you’re going to use private Git packages, you must add `github.com` (or your Git host) to the allowlist.

If you’re starting from scratch, create the network rule with the full allowlist.

Copy code

```
CREATE OR REPLACE NETWORK RULE dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  -- Minimal allowlist required for dbt deps
  VALUE_LIST = (
    'hub.getdbt.com',
    'codeload.github.com',
    'github.com',          -- GitHub
    -- 'gitlab.com',       -- GitLab
    -- 'dev.azure.com',    -- Azure DevOps
    -- 'bitbucket.org'     -- Bitbucket
  );
```

Some organizations run self-hosted instances of these providers. For example, GitLab self-managed, Bitbucket Data Center, Azure DevOps Server, or GitHub Enterprise Server. If your team does, replace the commented-out host with your instance’s custom domain (for example, `'gitlab.mycompany.com'`).

If you already have a network rule for dbt, add your Git provider (for example, `github.com`) to the existing `VALUE_LIST` with `ALTER`.

Copy code

```
ALTER NETWORK RULE dbt_network_rule SET
  VALUE_LIST = ('hub.getdbt.com', 'codeload.github.com', 'github.com');
```

#### Network rules don’t support paths

Add the host only. A `HOST_PORT` network rule entry must resolve to a valid domain, with an optional port. It can’t include a URL path, so an entry like `github.com/my-repo` isn’t supported.

Copy code

```
-- This doesn't work. HOST_PORT network rules don't support paths, such as /my-repo.
-- ALTER NETWORK RULE dbt_network_rule SET
--   VALUE_LIST = ('hub.getdbt.com', 'codeload.github.com', 'github.com/my-repo');
```

For the full rules on valid values, see [CREATE NETWORK RULE](https://docs.snowflake.com/en/sql-reference/sql/create-network-rule).

### Update the external access integration

Next, the administrator updates the external access integration (EAI) so engineers can reference secrets from their `env.yml` files without an administrator editing the EAI each time. Set `ALLOWED_AUTHENTICATION_SECRETS` to `all`.

To see what your EAI currently allows, describe it first.

Copy code

```
DESCRIBE EXTERNAL ACCESS INTEGRATION dbt_ext_access;
```

If you’re starting from scratch, create the EAI with `ALLOWED_AUTHENTICATION_SECRETS = all`.

Copy code

```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = all   -- Recommended if you expect your repos or access tokens changes over time, or you enable many personal access tokens.
  -- ALLOWED_AUTHENTICATION_SECRETS = (tasty_bytes_dbt_db.integrations.tb_dbt_git_secret) -- Use this if your org has a single admin secret for repo access or want to list out each secret for your team.
  ENABLED = TRUE;
```

Grant `USAGE` on the integration to the roles that need it.

Copy code

```
GRANT USAGE ON INTEGRATION dbt_ext_access TO ROLE accountadmin;
GRANT USAGE ON INTEGRATION dbt_ext_access TO ROLE data_engineer;
```

If you already have an EAI, switch it to allow all secrets with `ALTER`. Use `UNSET` to revert.

Copy code

```
ALTER EXTERNAL ACCESS INTEGRATION dbt_ext_access SET ALLOWED_AUTHENTICATION_SECRETS = all;
-- ALTER EXTERNAL ACCESS INTEGRATION dbt_ext_access UNSET ALLOWED_AUTHENTICATION_SECRETS;
```

If you already granted `USAGE` on `dbt_ext_access` when you first created it, you don’t need to grant it again here. You’re only updating the integration’s `ALLOWED_AUTHENTICATION_SECRETS` setting.

#### Why ALLOWED\_AUTHENTICATION\_SECRETS = all is still safe

Setting `ALLOWED_AUTHENTICATION_SECRETS = all` is a secure, recommended practice. It’s similar to granting a privilege on all future schemas: it removes a repetitive administrative bottleneck without weakening access control. Here’s why it stays safe:

- **It’s a one-time adjustment:** Once set to `all`, you won’t need to alter the EAI again when your team adds or rotates secrets. The alternative below (listing individual secrets) requires an `ALTER` every time you add one.
- **`READ` or `OWNERSHIP` is still required:** Allowing a secret in the EAI doesn’t grant access to it. The executing role must still hold the `READ` privilege (or OWNERSHIP) on the specified secret object. A user can only use the secrets they’ve been granted.
- **The network rule still controls where secrets can go:** `all` means any secret can be *used*, but a secret can only be transmitted to hosts listed in the network rule. Any attempt to reach an unlisted host is denied, regardless of what `ALLOWED_AUTHENTICATION_SECRETS` is set to.
- **dbt masks secret values:** Because every secret is referenced through a `DBT_ENV_SECRET_` variable, dbt replaces the value with `****` in all logs and error messages.

The benefit is that engineers can add and manage their own secrets in `env.yml` and work freely, while an administrator keeps control through provisioning `READ` grants on the secret objects.

#### Alternative: list individual secrets

If you’d rather not allow all secrets, list each one explicitly. Use this when you want the EAI itself to constrain exactly which secrets a project can use.

Copy code

```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (
    tasty_bytes_dbt_db.integrations.tb_dbt_git_secret,
    tasty_bytes_dbt_db.integrations.tb_dbt_github_actions_git_secret,
    tasty_bytes_dbt_db.integrations.jdoe_tb_dbt_git_secret,
    tasty_bytes_dbt_db.integrations.msmith_tb_dbt_git_secret
    -- Add each secret your projects reference.
  )
  ENABLED = TRUE;
```

If a dbt project object uses more than one EAI, such as `EXTERNAL_ACCESS_INTEGRATIONS = ('EAI_1', 'EAI_2')`, and even one of them has `ALLOWED_AUTHENTICATION_SECRETS = all`, then every secret referenced in the selected environment passes the EAI’s secret allowlist. Passing the allowlist isn’t the same as being granted access: the executing role must still hold `READ` or `OWNERSHIP` on a secret object in order to use it.

### Update your packages.yml to use private Git packages

With the network rule and EAI in place, reference your private Git package in `packages.yml`. Inject the Git credential securely using the `DBT_ENV_SECRET_` variable from your `env.yml`, then run `dbt deps` to pull the package.

Copy code

```
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: Snowflake-Labs/dbt_semantic_view
    version: [">=1.0.0", "<2.0.0"]
  - git: "https://{{env_var('DBT_ENV_SECRET_GIT_TOKEN')}}@github.com/my-github-account/jaffle-shop-demo.git"
    subdirectory: "jaffle-shop"
    revision: a47561234f73937cf58589ca2247475b40341237 # you can get this from the URL of any commit on the repo, using shorthand commit ID does not work
  - git: "https://{{env_var('DBT_ENV_SECRET_GIT_TOKEN')}}@github.com/my-github-account/jaffle-shop-demo.git"
    subdirectory: "flower-shop" # Cross-project deps. Referencing the same repo, but a different subfolder.
    revision: b9831234f73937cf58589ca2247475b40341298
```

Using the latest main branch (`revision: main`) is also supported, but not recommended as it could introduce breaking changes when dbt deps is called.

### Reference the imported package

After `dbt deps` pulls in the package, you reference its models from your own project with a **two-argument `ref()`**: `{{ ref('package_name', 'model_name') }}`. The package name comes first.

Two things to know:

- **One argument versus two:** A one-argument `ref('model_name')` resolves to a model in your own project. A two-argument `ref('package_name', 'model_name')` resolves to a model in an imported package. dbt recommends the two-argument form whenever you reference a model from another package, so the reference stays unambiguous even if a model name exists in more than one project.
- **Where the package name comes from:** The first argument is the dbt project `name:` declared in the imported package’s `dbt_project.yml`. It isn’t the Git repository name (`jaffle-shop-demo`) or the `subdirectory` value (`jaffle-shop`). For this package, that project name is `jaffle_shop`.

The example below is a model in our `tasty_bytes` project. It joins two of its own models, `simple_customers` and `combined_bookings` (one-argument `ref()`), and enriches them with a model from the imported `jaffle_shop` package (two-argument `ref()`).

Copy code

```
-- A model in the tasty_bytes project.
-- ref('simple_customers') and ref('combined_bookings') are models in THIS project.
-- ref('jaffle_shop', 'stg_customers') is a model from the imported jaffle_shop package.
SELECT
    A.ID,
    FIRST_NAME,
    LAST_NAME,
    birthdate,
    BOOKING_REFERENCE,
    HOTEL,
    BOOKING_DATE,
    COST,
    COST as cost_1,
    COST as cost_2,
    BOOKING_DATE as BOOKING_DATE_1,
    C.customer_id as jaffle_shop_customer_id
FROM {{ ref('simple_customers') }}  A
JOIN {{ ref('combined_bookings') }} B
  ON A.ID = B.ID
LEFT JOIN {{ ref('jaffle_shop', 'stg_customers') }} C
  ON A.ID = C.customer_id
```

The columns you select from a package model (here, `customer_id`) depend on that package’s schema. Check the imported package’s models for the exact column names.

## Start using environment variables

### Prerequisites

Before you start, make sure you have:

- Access to dbt Projects on Snowflake and Workspaces.
- A warehouse you can use to run the project. This warehouse runs the `env.yml` file at the start of the run.
- A role with the `READ` privilege or `OWNERSHIP` on any Snowflake secret you reference in `env.yml`.
- A dbt project (this guide uses a `tasty_bytes` dbt project and imports a private `jaffle_shop` package as a dependency).
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) version 3.21 or later, if you’re using the CLI for CI/CD workflows.

### If your project already uses environment variables

If you already call `env_var()` in your models or `profiles.yml`, you need to rename your variables to meet the `DBT_` prefix requirement before they’ll work with `env.yml`. We recommend using CoCo to do the heavy lifting by copying and pasting in these steps:

1. **Scan your project for all `env_var()` calls:** Ask CoCo to list every unique environment variable referenced across your models, macros, and `profiles.yml`.
2. **Add variables to your `env.yml` file:** Use the `env.yml` syntax from [Author your env.yml file](#label-dbt-env-vars-author-envyml). Set values to `""` as a placeholder while you decide which ones to hardcode.
3. **Rename each variable to UPPERCASE with the `DBT_` prefix:** For example, `my_schema` becomes `DBT_MY_SCHEMA`. Your values stay the same.
4. **Update the references in your project files:** Ask CoCo to replace every `env_var('OLD_NAME')` call with `env_var('DBT_OLD_NAME')` across your models, macros, and `profiles.yml` in one pass.

### Author your env.yml file

Create a file named `env.yml` in the root of your dbt project, next to `dbt_project.yml`. The example below defines four environments: `dev`, `staging`, `prod`, and `prod_complex`. The `default_environment` is `dev`. The dev and staging environments use metadata functions, such as `CURRENT_USER()`, to give each engineer an isolated schema so team members don’t collide while developing. The production environments use date and time functions to compute an incremental data window at run time.

The `env:` section supports any SQL query as long as it resolves into a single row and one column of type VARCHAR. You can query control tables, dbt execution history tables, task history tables, or any other table you set up.

Copy code

```
env_config: # Top-level: name is required for YAML - currently "env_config:"
  default_environment: dev
  environments: # The list of available environments
    - name: dev # User defines environment names
      # Uncomment if using private Git packages. See "Import private Git packages" above.
      # secrets:
      # - snowflake_secret: tasty_bytes_dbt_db.integrations.tb_dbt_git_secret  # Shared team secret
      #   # Must be prepended with DBT_ENV_SECRET_
      #   env_var_name: DBT_ENV_SECRET_GIT_TOKEN
      env:
        # Metadata function support, requires quotes for Jinja parsing
        DBT_CURRENT_WH: "{{ select CURRENT_WAREHOUSE() }}"
        DBT_CURRENT_DB: tasty_bytes_dbt_db
        DBT_CURRENT_SCHEMA: "{{ select CURRENT_USER() }}"
        DBT_CURRENT_ROLE: "{{ select CURRENT_ROLE() }}"
        DBT_CURRENT_USER: "{{ select CURRENT_USER() }}"
        DBT_FEATURE_FLAG_X_Y_Z: VALUE
        DBT_DATA_INTERVAL_START: "2020-01-01 00:00:00"
        DBT_DATA_INTERVAL_END: "2099-12-31 23:59:59"
    - name: staging # User defines environment names
      # secrets:
      # - snowflake_secret: tasty_bytes_dbt_db.integrations.tb_dbt_git_secret  # Shared team secret
      #   # Must be prepended with DBT_ENV_SECRET_
      #   env_var_name: DBT_ENV_SECRET_GIT_TOKEN
      env:
        # Metadata function support, requires quotes for Jinja parsing
        DBT_CURRENT_WH: tasty_bytes_dbt_wh
        DBT_CURRENT_DB: "{{ select CURRENT_USER() }}_tasty_bytes_dbt_db"
        DBT_CURRENT_SCHEMA: "{{ select CURRENT_USER() }}"
        DBT_CURRENT_ROLE: "{{ select CURRENT_ROLE() }}"
        DBT_CURRENT_USER: "{{ select CURRENT_USER() }}"
        DBT_DATA_INTERVAL_START: "2020-01-01 00:00:00"
        DBT_DATA_INTERVAL_END: "2099-12-31 23:59:59"
    - name: prod # User defines environment names
      # secrets:
      # - snowflake_secret: tasty_bytes_dbt_db.integrations.tb_dbt_git_secret  # Shared team secret
      #   # Must be prepended with DBT_ENV_SECRET_
      #   env_var_name: DBT_ENV_SECRET_GIT_TOKEN
      env:
        DBT_CURRENT_WH: tasty_bytes_dbt_wh
        DBT_CURRENT_DB: tasty_bytes_dbt_db
        DBT_CURRENT_SCHEMA: "{{ select CURRENT_USER() }}"
        DBT_CURRENT_ROLE: accountadmin
        # Start of day query, requires quotes for Jinja parsing
        DBT_DATA_INTERVAL_START: "{{ select (DATE_TRUNC('DAY', CURRENT_TIMESTAMP()) - INTERVAL '1 DAY')::string }}"
        DBT_DATA_INTERVAL_END: "{{ select (DATE_TRUNC('DAY', CURRENT_TIMESTAMP()) - INTERVAL '1 SECOND')::string }}"
    - name: prod_complex # User defines environment names
      # secrets:
      # - snowflake_secret: tasty_bytes_dbt_db.integrations.tb_dbt_git_secret  # Shared team secret
      #   # Must be prepended with DBT_ENV_SECRET_
      #   env_var_name: DBT_ENV_SECRET_GIT_TOKEN
      env:
        DBT_CURRENT_WH: tasty_bytes_dbt_wh
        DBT_CURRENT_DB: tasty_bytes_dbt_db
        DBT_CURRENT_ROLE: accountadmin
        # Completion time of the last successful run
        DBT_DATA_INTERVAL_START: "{{ select COALESCE((SELECT COMPLETED_TIME::STRING FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(TASK_NAME => 'RUN_TASTY_BYTES_DBT_OBJECT', RESULT_LIMIT => 100)) WHERE STATE = 'SUCCEEDED' ORDER BY COMPLETED_TIME DESC LIMIT 1), (DATE_TRUNC('DAY', CURRENT_TIMESTAMP()) - INTERVAL '1 DAY')::STRING) }}"
        # Start time of the current execution
        DBT_DATA_INTERVAL_END: "{{ select CURRENT_TIMESTAMP()::STRING }}"
```

### Configure your profile file

Your `dbt_projects_profiles.yml` or `profiles.yml` file reads the environment variables you defined in `env.yml` using `env_var()`. Wrap each `env_var()` call in double quotes so Jinja parses it correctly. With this setup, the same profile file produces a different connection target for each engineer in dev, because the values come from their injected environment. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

Copy code

```
tasty_bytes:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "not needed"
      user: "not needed"
      role: "{{ env_var('DBT_CURRENT_ROLE') }}"
      database: "{{ env_var('DBT_CURRENT_DB') }}"
      schema: "{{ env_var('DBT_CURRENT_SCHEMA') }}"
      warehouse: "{{ env_var('DBT_CURRENT_WH') }}"
      threads: 8
```

Note

Workspaces pre-validates the `role` and `warehouse` fields in the editor. Dynamic expressions that wrap those functions (for example, `"{{ select REPLACE(STRTOK(CURRENT_WAREHOUSE(), '_', 1)) }}"`) fail validation in Workspaces with the error `env.yml value contains Jinja that is not a supported Snowflake context function.` The `env.yml` values that feed these two connection fields must be a simple context function: `"{{ select CURRENT_ROLE() }}"` or `"{{ select CURRENT_WAREHOUSE() }}"`.

The `database` and `schema` fields don’t have this restriction: they accept any supported SQL, including string manipulation, table queries, and stored procedures.

This restriction applies only to Workspaces. In a deployed dbt project object (for example, in CI/CD with `EXECUTE DBT PROJECT` or the Snowflake CLI), `role` and `warehouse` accept complex SQL too.

### Write a model that consumes environment variables

Use `env_var()` in your models to read the injected values. The example below joins two upstream models and filters on the injected time window, so the same model processes a different date range depending on the environment you run it in.

Copy code

```
SELECT
  a.BOOKING_DATE,
  a.HOTEL,
  a.COST,
  a."30_DAY_AVG_COST",
  a."DIFF_BTW_ACTUAL_AVG",
  b.count_bookings
FROM {{ ref('thirty_day_avg_cost') }} a
JOIN {{ ref('hotel_count_by_day') }} b
  ON a.BOOKING_DATE = b.BOOKING_DATE
  AND a.HOTEL = b.HOTEL
WHERE a.BOOKING_DATE >= '{{ env_var("DBT_DATA_INTERVAL_START") }}'::TIMESTAMP
  AND a.BOOKING_DATE <= '{{ env_var("DBT_DATA_INTERVAL_END") }}'::TIMESTAMP
```

### Run your project in Workspaces

Note

If your `env.yml` includes a `secrets:` block, running the project requires you to select an external access integration each time you run a command, and the executing role needs `READ` or `OWNERSHIP` on the secret to use it in a run.

In Workspaces, you run your project on a selected environment. Snowflake resolves your `env.yml` first to inject environment variables and secrets. `CURRENT_WAREHOUSE()` uses your current session and resolves without needing a running warehouse. The resolved values then flow into `dbt_projects_profiles.yml` or `profiles.yml`, and the project runs on the warehouse that the file specifies.

Use the environment selector in the run panel to choose your active environment before running. You can also set or override the environment using `DEFAULT_ENVIRONMENT` on the dbt project object or `ENVIRONMENT` on `EXECUTE DBT PROJECT`. See [Create and execute the dbt project object](#create-and-execute-the-dbt-project-object).

### Create and execute the dbt project object

When you’re ready to deploy, create a dbt project object and select a default environment. Snowflake expects an `env.yml` file in the root of your dbt project.

Copy code

```
CREATE DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project
  FROM '@tasty_bytes_dbt_db.integrations.tasty_bytes_dbt_git_stage/branches/main'
  DEFAULT_TARGET = 'prod'
  DEFAULT_ENVIRONMENT = 'prod'   -- Optional.
  EXTERNAL_ACCESS_INTEGRATIONS = 'dbt_ext_access';
```

Change or clear the default environment later with `ALTER`.

Copy code

```
ALTER DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project SET DEFAULT_ENVIRONMENT = 'staging';
ALTER DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project UNSET DEFAULT_ENVIRONMENT;
```

#### Run without an environment (NO\_ENV)

`NO_ENV` is a reserved environment name (always uppercase). Use it when you want to run without selecting any environment from `env.yml`, while still passing overrides through `ENV_VARS`. You can set it as the default at creation or pass it on execute.

Copy code

```
CREATE OR REPLACE DBT PROJECT tasty_bytes_dbt_db.dev.dbt_no_env_valid
  FROM '@tasty_bytes_dbt_db.integrations.tasty_bytes_dbt_git_stage/branches/main'
  DEFAULT_ENVIRONMENT = 'NO_ENV';

EXECUTE DBT PROJECT tasty_bytes_dbt_db.dev.dbt_no_env_valid
  ARGS = 'run --target prod'
  ENVIRONMENT = 'NO_ENV'
  ENV_VARS = ('DBT_KEY' = 'some_value');
```

#### Execute with an environment override

Override the default environment for a single run with the `ENVIRONMENT` argument, which accepts one environment name.

Copy code

```
EXECUTE DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project
  ARGS = 'run --target prod'
  DBT_VERSION = '1.11.11'
  ENVIRONMENT = 'prod';   -- Optional.
```

#### Execute with specific variable overrides

Snowflake secrets can’t be referenced directly in `ENV_VARS` overrides (for example, `'DBT_KEY1' = 'db.schema.my_secret'`). This is by design: `EXECUTE DBT PROJECT` statements are recorded in Query History, so allowing raw secret references there would expose credentials to anyone who can query that history. Manage secrets through the `env.yml` file instead.

You can override individual env vars for a single execution with `ENV_VARS`. These overrides merge into the selected environment and take final precedence. Values can be SQL that resolves to VARCHAR, string literals, session variables (`$var`), or bind placeholders (`?`). `NULL` values and non-`VARCHAR`/`CHAR` types are rejected. SQL queries must be passed in with single quotes and all inner single quotes must be escaped.

Copy code

```
EXECUTE DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project
  ARGS = 'run --target prod'
  DBT_VERSION = '1.11.11'
  ENV_VARS = ('DBT_KEY1' = 'VALUE1', 'DBT_KEY2' = '{{ select (DATE_TRUNC(\'DAY\', CURRENT_TIMESTAMP()) - INTERVAL \'1 SECOND\')::string }}');   -- Optional. Override keys must be DBT_-prefixed and uppercase.
```

You can also pass a session variable as an `ENV_VARS` value. Set the session variable first, then reference it with `$`.

Copy code

```
SET my_user_var = (SELECT CURRENT_USER());

EXECUTE DBT PROJECT tasty_bytes_dbt_db.dev.tasty_bytes_dbt_project
  ARGS = 'run --target prod'
  ENV_VARS = ('DBT_CURRENT_USER' = $my_user_var);
```

### Call stored procedures from env.yml

You can call stored procedures from `env:` values using the `SELECT * FROM TABLE(...)` syntax. The CALL syntax is not supported. This is useful when your logic is too complex for inline SQL or when you want to reuse the same transformation across multiple environments.

Because `env.yml` values must resolve to a single row and one VARCHAR column, the stored procedure must return a table with one row and one column. Use the `SELECT * FROM TABLE(procedure_name(...))` pattern inside `"{{ select ... }}"`.

For more information about calling stored procedures with SELECT, see [Calling a stored procedure with SELECT](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-selecting-from).

#### Example: per-developer schema from a stored procedure

This stored procedure takes an email or username string, strips everything at and after the `@`, and replaces `.` with `_`. The result is a clean schema name for each developer.

Copy code

```
CREATE OR REPLACE PROCEDURE tasty_bytes_dbt_db.public.clean_username(email_input VARCHAR)
RETURNS TABLE (cleaned_username VARCHAR)
LANGUAGE SQL
AS
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT REPLACE(SPLIT_PART(:email_input, '@', 1), '.', '_') AS cleaned_username);
  RETURN TABLE(res);
END;

-- Example 1: Passing 'john.doe@company.com'
SELECT * FROM TABLE(tasty_bytes_dbt_db.public.clean_username('john.doe@company.com'));
-- Result: john_doe

-- Example 2: Passing 'johndoe@company.com'
SELECT * FROM TABLE(tasty_bytes_dbt_db.public.clean_username('johndoe@company.com'));
-- Result: johndoe
```

#### Call the stored procedure in env.yml

In your `env.yml`, call the stored procedure with `CURRENT_USER()` as the input so each engineer gets their own schema automatically:

Copy code

```
env:
  # Example for per-developer schema using a stored procedure
  DBT_SCHEMA: "{{ select * FROM TABLE(tasty_bytes_dbt_db.public.clean_username(CURRENT_USER())) }}"
  # Alternative in raw SQL (no stored procedure needed):
  # DBT_SCHEMA: "{{ select REPLACE(SPLIT_PART(CURRENT_USER(), '@', 1), '.', '_') }}"
```

Both approaches produce the same result. The stored procedure is useful when the logic is more complex or shared across teams.

## Use the Snowflake CLI

The Snowflake CLI is how you wire environment variables into CI/CD and external orchestrators. The flags in this section require Snowflake CLI 3.21 or later.

### Deploy flags

- `--env-file-dir`: Points the CLI at a directory containing an `env.yml` file elsewhere in your repo, similar to `--profiles-dir`. The file is pulled into the deployed object, overwriting the object’s `env.yml` at the project root (next to `dbt_project.yml`) if one already exists.
- `--default-env`: Sets the default environment for compilation and later executions of the dbt project object.
- `--external-access-integration`: Attaches an external access integration to the dbt project object. Required when your project pulls in private Git packages or remote dependencies via `dbt deps`. Pass the flag once per integration. See [Admin setup](#admin-setup).

Copy code

```
snow dbt deploy tester_tasty_bytes_dbt_project --source ./tasty_bytes
snow dbt deploy tester_tasty_bytes_dbt_project --source ./tasty_bytes --env-file-dir ./some/path
snow dbt deploy tester_tasty_bytes_dbt_project --default-env prod

# Deploy with a default target and an external access integration (required for private Git packages).
snow dbt deploy tasty_bytes_dbt_project --source ./tasty_bytes \
  --default-target prod \
  --external-access-integration dbt_ext_access
```

### Execute flags

- `--env`: Selects the environment within the `env.yml` file at execution time.
- `--env-vars`: Applies inline key/value overrides at execution time without modifying the file. Secret injection through Snowflake-managed secrets isn’t supported here.
- `--use-shell-env-vars`: Pulls shell environment variables into the run, overriding `env.yml`. All shell variables prefixed with `DBT_` are used (excluding `DBT_ENV_SECRET_*` variables), including those not defined in `env.yml`. When this flag is set, only `--env-vars` can override the shell values.

Copy code

```
snow dbt execute --dbt-version '1.11.11' --env staging \
  --env-vars '{"DBT_DATABASE": "tasty_bytes_staging_db", "DBT_OTHER_KEY": "value"}' tester_tasty_bytes_dbt_project run
```

At deploy time, `--env-file-dir` determines which `env.yml` is stored at the root of the deployed dbt project object; without it, the CLI deploys the `env.yml` from your project root. At execution time, the run reads that root `env.yml`. Adding `--use-shell-env-vars` overrides those values with `DBT_`-prefixed shell variables wherever keys collide, and `--env-vars` overrides everything, including the shell values.

### Spin up an isolated per-PR database for CI testing (GitHub Actions)

This example uses a pull request number to create an isolated staging database, run transformations on it, and clean it up. GitHub Actions replaces `${{ github.event.number }}` with the pull request number before the shell runs.

The example chooses a zero-copy clone so that CI gets a realistic, independently writable snapshot of existing data. A clone initially shares the source database’s existing micro-partitions instead of physically copying all table data. The source and clone consume additional storage as their data changes.

You don’t need to clone production for every CI workflow unless your tests need a realistic, writable copy of existing production data and objects. With defer to production, CI can read unchanged upstream tables from production and write changed models to a separate test database or schema. For a complete workflow that imports production state, runs Slim CI against a per-pull-request clone, and cleans up its resources, see [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

Copy code

```
# Deploy a tester object.
snow dbt deploy tester_tasty_bytes_dbt_project --source ./tasty_bytes

# Create a staging database using the PR number.
snow sql -q "CREATE DATABASE tasty_bytes_staging_pr_${{ github.event.number }}_db CLONE tasty_bytes_dbt_db"

# Execute against the staging database with overrides.
snow dbt execute --env staging \
  --env-vars '{"DBT_DATABASE": "tasty_bytes_staging_pr_${{ github.event.number }}_db"}' tester_tasty_bytes_dbt_project run

# After the PR merges, deploy to the production object and select the environment for compilation and subsequent runs.
snow dbt deploy tasty_bytes_dbt_project --default-env prod

# In a workflow triggered when the pull request closes, clean up using the same PR number.
snow sql -q "DROP DATABASE IF EXISTS tasty_bytes_staging_pr_${{ github.event.pull_request.number }}_db"
```

## Observability

You can see environment information through several Snowflake surfaces:

- `SHOW DBT PROJECTS` and `GET_DDL` reflect the dbt project object’s `DEFAULT_ENVIRONMENT` attribute. This is an attribute the user must set on the object via CREATE or via ALTER commands. This isn’t derived from the `default_environment:` section in the `env.yml` file.
- The `ENVIRONMENT` column in the ACCOUNT\_USAGE [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/account-usage/dbt_project_execution_history) view shows which environment was used for each execution.
- Query History shows the `ENVIRONMENT` override for a specific `EXECUTE DBT PROJECT` statement.
- Query History also shows the `ENV_VARS` overrides (the overridden environment variables) for a specific `EXECUTE DBT PROJECT` statement.

## Reference

### Supported context functions and Jinja helpers

The `env:` and `secrets:` sections support different syntax. The tables below list what works in each.

#### Jinja context variable helpers (secrets: name interpolation)

Use these inside `secrets:` to interpolate the secret name, for example `"snowflake_secret: {{ current_user }}_git_secret"`. `select` statements, parentheses, and concatenation aren’t allowed in this section.

| Helper | Supported |
| --- | --- |
| `{{ current_user }}` | Yes |
| `{{ current_account }}` | Yes |
| `{{ current_account_name }}` | Yes |
| `{{ current_organization_name }}` | Yes |

Expand

Show lessSee more

#### SQL context functions (env: values via `{{ select ... }}` syntax)

Use these inside `env:` values wrapped in `"{{ select ... }}"`. Any SQL query that returns a single row and one VARCHAR column is supported, including full table queries (for example, `SELECT column FROM your_control_table`).

| Function | Supported | Notes |
| --- | --- | --- |
| CURRENT\_USER() | Yes |  |
| CURRENT\_ROLE() | Yes |  |
| CURRENT\_DATABASE() | Yes |  |
| CURRENT\_SCHEMA() | Yes |  |
| CURRENT\_WAREHOUSE() | Yes |  |
| CURRENT\_DATE() / CURRENT\_TIME() / CURRENT\_TIMESTAMP() and aliases (GETDATE, SYSDATE, SYSTIMESTAMP, LOCALTIME, LOCALTIMESTAMP) | Yes |  |
| Date and time math (DATEADD, DATEDIFF, DATE\_TRUNC, ADD\_MONTHS, and similar) | Yes |  |
| CURRENT\_SESSION() | No | dbt runs across multiple threads; there’s no single consistent session ID. |
| CURRENT\_CLIENT() | No |  |
| CURRENT\_IP\_ADDRESS() | No |  |
| CURRENT\_VERSION() | No |  |
| ALL\_USER\_NAMES() | No |  |
| LAST\_QUERY\_ID() | No |  |
| INVOKER\_ROLE() | No |  |
| IS\_ROLE\_IN\_SESSION() | No |  |
| SYS\_CONTEXT() | No |  |

Expand

Show lessSee more

When a value feeds the `role` or `warehouse` field of the profile file, Workspaces accepts only a bare `"{{ select CURRENT_ROLE() }}"` or `"{{ select CURRENT_WAREHOUSE() }}"`, not expressions that wrap them. The `database` and `schema` fields accept the full set of SQL behaviors including stored procedures. This restriction applies to Workspaces only. Deployed dbt project objects accept complex SQL for all four fields.

#### dbt macros

Macros (for example, `{{ ref(...) }}`, `{{ source(...) }}`) aren’t allowed anywhere in `env.yml`. Since standard dbt Core env vars must resolve before a macro can use them, allowing macros inside `env.yml` would create a circular dependency.

#### Limited Jinja in env: values

In `env:` values, only the `{{ select (query) }}` Jinja pattern is supported. Other Jinja constructs, such as loops, conditionals, and filters, aren’t allowed. For example, this isn’t valid:

Copy code

```
env:
  # Not supported: Jinja loops aren't allowed in env: values.
  DBT_SCHEMA: "{% for schema in schemas %}{{ schema }}{% endfor %}"
```

Use SQL inside `{{ select ... }}` instead. For example, `"{{ select CURRENT_USER() }}"`, `"{{ select COALESCE(...) }}"`, or `"{{ select * from TABLE(my_stored_proc()) }}"`.

### Environment selection (highest to lowest)

One environment is active per execution, chosen in this order:

| Priority | Source |
| --- | --- |
| 1 (highest) | `ENVIRONMENT = '...'` on `EXECUTE DBT PROJECT` |
| 2 | `DEFAULT_ENVIRONMENT` on the dbt project object |
| 3 | `default_environment` in `env.yml` |

Expand

Show lessSee more

Use the reserved name `NO_ENV` to run without any environment.

### Value precedence (highest to lowest)

| Priority | Source | Notes |
| --- | --- | --- |
| 1 (highest) | `--env-vars` / `EXECUTE ... ENV_VARS` | Final precedence. Merges into the selected environment. |
| 2 | Shell environment variables | Only when using `--use-shell-env-vars`. All shell variables prefixed with `DBT_` are used (excluding `DBT_ENV_SECRET_*` variables), including those not defined in `env.yml`. |
| 3 (lowest) | `env.yml` selected environment | The committed default configuration. |

Expand

Show lessSee more

### Naming and casing rules

| Rule | Applies to |
| --- | --- |
| Prefix with `DBT_` (includes `DBT_ENV_CUSTOM_ENV_`, `DBT_ENV_SECRET_`) | All keys in `env:` and `secrets:`, and all overrides |
| UPPERCASE keys | All keys in `env:` and `secrets:`, and all overrides |
| Prefix with `DBT_ENV_SECRET_` | All keys in `secrets:` (value masked to `****`) |
| Must be plain text, not SQL | All environment names, keys in `env:` and `secrets:`, and secret values |
| Must be English letters, numbers, and underscores, up to 256 characters. | All keys in `env:` and `secrets:` and environment names |
| Case sensitive | Environment names |

Expand

Show lessSee more

### env: versus secrets: capabilities

| Capability | `env:` | `secrets:` |
| --- | --- | --- |
| Plain text values | Yes | n/a (references a secret object) |
| SQL query `"{{ select ... }}"` (one row, one VARCHAR column, including table queries) | Yes | No |
| Limited context vars (for example `{{ current_user }}`, no `select`, no `()`) | No | Yes |
| Concatenation operators (for example, `"{{ select CURRENT_USER() || '_schema' }}"`) | Yes | No |
| Macros | No | No |
| Secret type | n/a | `GENERIC_STRING` only |
| Validated against the external access integration before use | n/a | Yes |

Expand

Show lessSee more

### Why the DBT\_ prefix is required

The `DBT_` prefix is an intentional design decision.

- **Namespace isolation:** CI/CD pipelines, Airflow DAGs, and container hosts already hold system-level variables and potentially sensitive credentials. The `DBT_` prefix prevents name collisions with infrastructure variables that happen to share a name.
- **Built-in security:** dbt Core uses the prefix to route variables through different security pipelines. `DBT_ENV_SECRET_` variables are automatically masked to `****` in all logs and excluded from metadata artifacts. Without the prefix, the compiler has no way to distinguish sensitive from non-sensitive values at runtime.
- **Scoped discovery:** When you use `--use-shell-env-vars`, the Snowflake CLI only reads shell variables prefixed with `DBT_` (excluding `DBT_ENV_SECRET_*` variables). This constrains the values read in your Airflow DAG, local machine, or container host to only variables intended for dbt.

### File location and size

- Place `env.yml` in the root of your dbt project, in the same folder as `dbt_project.yml`.
- 2 MB limit (roughly 12,000 lines).
