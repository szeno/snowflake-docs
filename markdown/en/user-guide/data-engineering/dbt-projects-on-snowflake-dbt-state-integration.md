# Integrating dbt State with dbt Projects on Snowflake

Important

dbt State is a service operated by dbt Labs under your own dbt Labs agreement. Snowflake does not control its availability or the accuracy of its skip, clone, and rebuild decisions, and it is not covered by the Snowflake Service Level Agreement. For State availability or billing issues, contact dbt Labs support.

dbt State, a dbt Labs service, decides which models need to be rebuilt and which models can be reused during an execution. It skips models that don’t need to run, which aims to reduce execution runtime and warehouse compute. You can use dbt State with dbt project objects and Workspaces by connecting your project to your dbt Platform account through an `env.yml` secret and an external access integration.

For how dbt State decides what to rebuild, see [How dbt State works](https://docs.getdbt.com/docs/deploy/dbt-state-about?version=2#how-dbt-state-works) in the dbt Labs documentation.

## Supported dbt versions

dbt State is supported only on the following dbt version in dbt Projects on Snowflake:

| Supported dbt version | dbt State support |
| --- | --- |
| dbt Fusion 2.0.0-preview.210 | Supported |

Expand

Show lessSee more

Support for dbt v1 versions and dbt 2.0.0 and later is coming soon. To run with dbt State today, set `DBT_VERSION = '2.0.0-preview.210'` on your dbt project object or Workspace execution. For all versions that dbt Projects on Snowflake supports, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).

## Prerequisites

Before you start, make sure you have:

- A dbt project that runs on a [supported dbt version](#label-dbt-state-supported-versions).
- A dbt Platform account.
- A role that can create secrets, network rules, and external access integrations, or an administrator who can create them for you.
- An `env.yml` file at the root of your dbt project. For more information, see [Use SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Set up dbt State

### Step 1: Enable dbt State and collect your dbt Platform credentials

Enable dbt State on your dbt Platform account. For instructions, see [Setting up dbt State](https://docs.getdbt.com/docs/deploy/dbt-state-setup) in the dbt Labs documentation.

dbt project objects run without a browser, so dbt State can’t use the interactive `dbt login` flow. Instead, dbt authenticates with a dbt Platform service token. From **Account settings** in your dbt Platform account, collect the following values:

- **Account ID:** Your numeric dbt Platform account ID. You set it as `DBT_CLOUD_ACCOUNT_ID`.
- **Access URL:** The host name of your dbt Platform account, such as `ab123.us1.dbt.com`. Don’t include `https://`. You set it as `DBT_CLOUD_ACCOUNT_HOST` and add it to your network rule.
- **Service token:** A service token that you create under **API tokens** » **Service tokens**. You store it in a Snowflake secret and pass it as `DBT_CLOUD_TOKEN`.

### Step 2: Store the service token in a Snowflake secret

Store your dbt Platform service token in a Snowflake secret, and grant `READ` on it to the role that runs your dbt project:

Copy code

```
CREATE OR REPLACE SECRET tasty_bytes_dbt_db.integrations.dbt_cloud_token_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = '<your_dbt_platform_service_token>';

GRANT READ ON SECRET tasty_bytes_dbt_db.integrations.dbt_cloud_token_secret TO ROLE data_engineer;
```

### Step 3: Allow network traffic to dbt State

dbt State needs network access to the dbt State service and to your dbt Platform account. Add these hosts to the network rule for your dbt external access integration, and allow the secret you created.

If you’re starting from scratch, create a network rule that allows everything a dbt project typically needs: dbt packages, Git, and dbt State. If your project pulls private Git packages from GitLab, Azure DevOps, Bitbucket, or a self-hosted Git server, replace `'github.com'` with your Git provider’s domain.

Copy code

```
CREATE OR REPLACE NETWORK RULE dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'hub.getdbt.com',       -- dbt packages
    'codeload.github.com',  -- dbt packages
    'github.com',           -- Private Git packages (replace with your Git host)
    'auth.state.dbt.com',   -- dbt State
    'api.state.dbt.com',    -- dbt State
    'ab123.us1.dbt.com'     -- Replace with your dbt Platform access URL
  );

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (tasty_bytes_dbt_db.integrations.dbt_cloud_token_secret)
  ENABLED = TRUE;

GRANT USAGE ON INTEGRATION dbt_ext_access TO ROLE data_engineer;
```

If you already have a network rule and external access integration for dbt, add the dbt State hosts and your access URL with `ALTER`. `SET VALUE_LIST` replaces the whole list, so include the hosts that are already in your rule:

Copy code

```
ALTER NETWORK RULE dbt_network_rule SET
  VALUE_LIST = (
    'hub.getdbt.com',
    'codeload.github.com',
    'github.com',           -- Replace with your Git host
    'auth.state.dbt.com',
    'api.state.dbt.com',
    'ab123.us1.dbt.com'     -- Replace with your dbt Platform access URL
  );

ALTER EXTERNAL ACCESS INTEGRATION dbt_ext_access SET
  ALLOWED_AUTHENTICATION_SECRETS = all;
```

Setting `ALLOWED_AUTHENTICATION_SECRETS = all` is a secure, recommended practice. It removes a repetitive administrative bottleneck without weakening access control:

- **It’s a one-time adjustment:** You don’t need to alter the external access integration when your team adds or rotates secrets.
- **`READ` or `OWNERSHIP` is still required:** Allowing a secret in the integration doesn’t grant access to it. The executing role must still hold the `READ` privilege or `OWNERSHIP` on the secret.
- **The network rule still controls where secrets can go:** A secret can only be transmitted to hosts listed in the network rule.

If your organization requires an explicit allowlist, include the dbt Platform service token and every other secret that the integration already allows:

Copy code

```
ALTER EXTERNAL ACCESS INTEGRATION dbt_ext_access SET
  ALLOWED_AUTHENTICATION_SECRETS = (
    tasty_bytes_dbt_db.integrations.dbt_cloud_token_secret,
    tasty_bytes_dbt_db.integrations.tb_dbt_git_secret
  );
```

### Step 4: Configure dbt State in your env.yml file

In `env.yml`, inject the service token as `DBT_CLOUD_TOKEN`, set your dbt Platform account host and ID, and enable dbt State with `DBT_ENGINE_MANAGE_STATE`:

Copy code

```
env_config:
  default_environment: prod
  environments:
    - name: prod
      secrets:
        - snowflake_secret: tasty_bytes_dbt_db.integrations.dbt_cloud_token_secret
          env_var_name: DBT_CLOUD_TOKEN
      env:
        DBT_CLOUD_ACCOUNT_HOST: "ab123.us1.dbt.com"
        DBT_CLOUD_ACCOUNT_ID: "<your_dbt_platform_account_id>"
        DBT_ENGINE_MANAGE_STATE: "true"
```

dbt State reads these variables by name, so use them exactly as shown:

- `DBT_CLOUD_TOKEN`: Your dbt Platform service token, injected from the Snowflake secret.
- `DBT_CLOUD_ACCOUNT_HOST`: Your dbt Platform access URL, without `https://`.
- `DBT_CLOUD_ACCOUNT_ID`: Your dbt Platform account ID.
- `DBT_ENGINE_MANAGE_STATE`: Turns dbt State on (`"true"`) or off (`"false"`). dbt Projects defaults this variable to `"false"`, so set it to `"true"` to use dbt State.

### Step 5: Optional: Configure lag tolerance

The `lag_tolerance` config controls how long dbt State waits before rebuilding a model after its upstream data changes. You can set it for the whole project or for a single model.

To set it for all models, add it under `+state:` in `dbt_project.yml`. The following example allows production models to lag by up to 4 hours and models in other targets by up to 7 days:

Copy code

```
models:
  +state:
    lag_tolerance: "{{ '4h' if target.name == 'prod' else '7d' }}"
```

To set it for a single model, add a `config()` block at the top of the model’s SQL file:

Copy code

```
{{ config(
    state={
        "lag_tolerance": "1h"
    }
) }}

SELECT ...
```

For all dbt State settings, see [dbt State configurations](https://docs.getdbt.com/reference/resource-configs/dbt-state-configs) in the dbt Labs documentation.

### Step 6: Run your project with dbt State

In Workspaces, select dbt Fusion 2.0.0-preview.210, the environment that contains your dbt State settings, and the `dbt_ext_access` external access integration, and then run `dbt run` or `dbt build`.

For a dbt project object, pass the dbt version, the external access integration, and the environment on `EXECUTE DBT PROJECT`:

Copy code

```
EXECUTE DBT PROJECT tasty_bytes_dbt_db.prod.tasty_bytes_dbt_project
  ARGS = 'build --target prod'
  DBT_VERSION = '2.0.0-preview.210'
  EXTERNAL_ACCESS_INTEGRATIONS = (dbt_ext_access)
  ENVIRONMENT = 'prod';
```

To turn off dbt State for a single run, override `DBT_ENGINE_MANAGE_STATE`. In Workspaces, use **Override environment variables** in the run panel. In SQL, use `ENV_VARS`:

Copy code

```
EXECUTE DBT PROJECT tasty_bytes_dbt_db.prod.tasty_bytes_dbt_project
  ARGS = 'build --target prod'
  DBT_VERSION = '2.0.0-preview.210'
  EXTERNAL_ACCESS_INTEGRATIONS = (dbt_ext_access)
  ENVIRONMENT = 'prod'
  ENV_VARS = ('DBT_ENGINE_MANAGE_STATE' = 'false');
```

## Troubleshoot dbt State authentication

After a run, check the dbt log for dbt State messages. If dbt State can’t authenticate, the failure behavior differs by dbt version:

- **dbt v1:** dbt State disables itself, logs an authentication warning, and the execution continues without dbt State.
- **dbt v2 (Fusion):** The execution fails with a dbt State authentication error.

If authentication fails, check that the environment includes the service-token secret, the run uses the external access integration, and the executing role has `READ` on the secret.

## dbt State compared with Slim CI

dbt State and [Slim CI](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod) both help you avoid work that isn’t needed:

- **Slim CI** uses artifacts from an earlier execution and selectors such as `--select state:modified+`, so you choose what runs. It’s built into dbt Projects on Snowflake and doesn’t require a dbt Labs account.
- **dbt State** is a dbt Labs service that decides which selected models need to be rebuilt and which can be reused during an execution. It requires a dbt Platform account and is billed by dbt Labs.

## Billing

dbt State is a separately billed dbt Labs feature. dbt Labs handles all dbt State billing and services through your dbt Platform account.

Executions of your dbt project object still run on your Snowflake warehouse and incur standard Snowflake compute costs. For more information, see [Understanding costs for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-cost).

For more about dbt State, see [About dbt State](https://docs.getdbt.com/docs/deploy/dbt-state-about?version=2) in the dbt Labs documentation.
