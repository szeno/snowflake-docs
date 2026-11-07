# Configure default model settings

Snowflake account administrators can set a default model for all Cortex Code users by creating a settings agent: a schema-level object in `CORTEX_CODE.CONFIG` that Cortex Code reads at session startup to apply account-wide model settings.

This topic describes how to create the settings agent, configure the default model, and grant access to users.

## Prerequisites

Before configuring default model settings, ensure the following:

- You have the ACCOUNTADMIN role. This is required to create and modify agent objects in the `CORTEX_CODE` database.
- Cross-region inference is enabled on your account. See [Enable cross-region inference](#enable-cross-region-inference).

## Create the database and schema

The `CORTEX_CODE` database is not created automatically. Create it once per account using the
`ACCOUNTADMIN` role:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS CORTEX_CODE;
CREATE SCHEMA IF NOT EXISTS CORTEX_CODE.CONFIG;
```

If the `CORTEX_CODE` database already exists in your account, skip this step.

If you skip this step, creating the settings agent in the next section fails with the following error:

Copy code

```
002003 (42S02): SQL compilation error:
Database 'CORTEX_CODE' does not exist or not authorized.
```

## Create the settings agent

The settings agent is an AGENT object in the `CORTEX_CODE.CONFIG` schema. Cortex Code reads this object at session startup and applies the configured settings. This topic covers the `models.orchestration` key. The `CORTEX_CODE.CONFIG.DEFAULT` agent is also the account’s default profile, so it can set instructions and skills as well. You can also create it on the **Profiles** tab of the CoCo Admin page by selecting **Create default profile**. For more information, see [The default profile](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-default).

:::note
The settings agent can’t set session behaviors such as plan mode. Those are controlled per session. To enable plan mode, use the `/plan` command or press Ctrl-P. For more information, see [Agent mode and Plan mode](/user-guide/cortex-code/cortex-code-desktop/agent-mode-and-plan-mode).
:::

If `CORTEX_CODE.CONFIG.DEFAULT` already exists, for example because it was created on the CoCo Admin page, update it with `ALTER AGENT` as described in [Update agent settings](#label-cortex-code-default-model-update) instead. `CREATE OR REPLACE AGENT` replaces the whole object, including its instructions and skills, and removes its grants unless you specify `COPY GRANTS`.

To create the default settings agent, run the following as ACCOUNTADMIN:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE AGENT CORTEX_CODE.CONFIG.DEFAULT
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;
```

This creates a settings agent using `auto`, the recommended model setting. With `auto`, Snowflake selects a default model automatically. Currently this maps to a fixed default model; dynamic model selection is under active development.

To pin a specific model instead, replace `auto` with a model identifier:

Copy code

```
models:
  orchestration: claude-opus-4-7
```

## Grant access to users

Grant USAGE on the settings agent to each role whose users should receive these settings:

Copy code

```
GRANT USAGE ON DATABASE CORTEX_CODE TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CORTEX_CODE.CONFIG TO ROLE <role_name>;
GRANT USAGE ON AGENT CORTEX_CODE.CONFIG.DEFAULT TO ROLE <role_name>;
```

Cortex Code applies the settings from the agent object to any user whose active role has USAGE on that agent.

To apply the settings to all users in the account, grant USAGE to the PUBLIC role, which is automatically granted to every user:

Copy code

```
GRANT USAGE ON DATABASE CORTEX_CODE TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA CORTEX_CODE.CONFIG TO ROLE PUBLIC;
GRANT USAGE ON AGENT CORTEX_CODE.CONFIG.DEFAULT TO ROLE PUBLIC;
```

## Update agent settings

To change the default model after the initial setup:

Copy code

```
ALTER AGENT CORTEX_CODE.CONFIG.DEFAULT
  MODIFY LIVE VERSION SET SPECIFICATION =
  $$
  models:
    orchestration: claude-opus-4-7
  $$;
```

This statement replaces the whole specification. If the agent also sets instructions or skills, include them in the new specification.

Note

Settings are applied at session startup. Exact behavior may vary across surfaces and is subject to change.

## Available models

Set `orchestration` to a supported Cortex model identifier. Use `auto` (recommended) to let Snowflake select an appropriate model automatically.

Auto options depend on your account configuration. If one of the following options appears in your account’s model picker, you can set `orchestration` to its corresponding value:

- `auto-intelligent` (**Auto Intelligent**): Favors the most capable models.
- `auto-efficient` (**Auto Efficient**): Optimizes for cost.

For available model identifiers, context windows, and per-region availability, see [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

## Enable cross-region inference

Cross-region inference is required for Cortex Code to function. It routes model requests to a region where the necessary model is available.

Cross-region inference is disabled by default. An ACCOUNTADMIN must enable it:

Copy code

```
-- Requires ACCOUNTADMIN role
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

When `orchestration` is set to `auto`, Snowflake uses cross-region inference to automatically select an available model.
