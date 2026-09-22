# CoCo Desktop

Feature — Generally Available

Available to all Commercial (non-Gov, VPS, Sovereign) accounts with [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled.

CoCo Desktop is a native macOS/Windows desktop application that brings CoCo’s full
agentic capabilities into an IDE-like surface: file editor, integrated terminal, agentic AI
loop, agentic browser, agentic notebook, and deep Snowflake awareness.

Get CoCo Desktop

**[Download the latest version](https://www.snowflake.com/en/product/snowflake-coco/downloads/)**. Available for macOS and Windows.

[![CoCo Desktop in Agent view showing the chat interface, session sidebar, and tool bar](/static/images/user-guide/cortex-code/cortex-code-desktop/agent-mode-overview.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/agent-mode-overview.png)

## Access control requirements

The user’s active role must have one of the following database roles granted to use CoCo Desktop:

| Database role | Notes |
| --- | --- |
| SNOWFLAKE.CORTEX\_USER **or** SNOWFLAKE.CORTEX\_AGENT\_USER | At least one of these database roles is required. SNOWFLAKE.CORTEX\_AGENT\_USER grants access to Cortex Agents and agentic surfaces, including CoCo Desktop and Snowflake Intelligence. |

Expand

Show lessSee more

By default, SNOWFLAKE.CORTEX\_USER is granted to the PUBLIC role,
so all users in the account have access to CoCo Desktop without additional configuration.
SNOWFLAKE.CORTEX\_AGENT\_USER is not granted to PUBLIC by default and must be explicitly granted
to roles that need it. To restrict access, revoke SNOWFLAKE.CORTEX\_USER from PUBLIC and grant it
only to specific roles. For details, see
[Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

Important

Revoking SNOWFLAKE.CORTEX\_USER from PUBLIC also removes access to other Covered AI Features,
including Cortex AI functions (AI\_COMPLETE, AI\_TRANSLATE, AI\_CLASSIFY, and others). If you
need finer-grained control, use the daily credit usage limit parameter to block
Desktop access without affecting other AI features.

Account administrators can additionally control access by setting per-user daily credit limits.
Setting the account-level `CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER` parameter to `0`
blocks all users, and you can then selectively allow access for individual users by assigning
them a positive value. See [Daily credit usage limits for CoCo](/user-guide/cortex-code/credit-usage-limit).

Note

On self-service [trial accounts](/user-guide/admin-trial-account), AI features are disabled by default.
To enable them, an account administrator must
[add a credit card to the account](/user-guide/admin-trial-account#label-trial-account-ai-features).
Adding a credit card doesn’t upgrade the trial to a paid account or end the trial period.

## What’s new

See [Release notes](/user-guide/cortex-code/cortex-code-desktop/release-notes) for the latest features,
improvements, and fixes in each version.

## Supported models

CoCo can use the Cortex large language models your role has access to, including Claude,
OpenAI GPT, Gemini, and Grok models. New models are added as they’re released, so instead of a
fixed list, CoCo shows you the models that are currently available to you. That in-product list is
authoritative.

You can pick a specific model, or one of these Auto options that choose a model for you:

- **Auto**: Snowflake selects the model.
- **Auto Intelligent**: Favors the most capable models. Highest quality, highest cost.
- **Auto Efficient**: Optimizes for cost. Lowest cost, and might reduce quality on hard tasks.

Two things determine which models you can choose:

- **Model access:** the models granted to your active role. Snowflake Cortex controls model access
  with role-based access control (RBAC). A user with the `ACCOUNTADMIN` role grants a per-model
  application role, or `CORTEX-MODEL-ROLE-ALL` for all current and future models, to each role that
  needs it. By default, users inherit access to all models through the
  [`SNOWFLAKE.PUBLIC` bootstrap grant](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-model-role-all-bootstrap).
  To list the models your active role can use, run
  `SHOW CORTEX BASE MODELS IN SCHEMA SNOWFLAKE.MODELS`. For more information, see
  [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models). For how to restrict model access, see
  [Control model access](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-access-control).
- **Regional availability:** whether the model runs in your account’s region, or is reachable
  through cross-region inference. For per-model regions, see
  [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability). If a
  model isn’t available in your region, a user with the
  `ACCOUNTADMIN` role must enable [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

To see which model CoCo Desktop is using or to switch models, use the **model picker** in the chat
input.

## Get started

| Topic | Description |
| --- | --- |
| [Installation, onboarding, and authentication](/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication) | Download, install, and sign in |
| [Navigation](/user-guide/cortex-code/cortex-code-desktop/navigation) | Agent view, Editor view, and layout controls |
| [Agent view and Editor view](/user-guide/cortex-code/cortex-code-desktop/agent-view-and-editor-view) | When to use each view |
| [Agent mode and Plan mode](/user-guide/cortex-code/cortex-code-desktop/agent-mode-and-plan-mode) | Planning before implementing |

Expand

Show lessSee more

## Features

| Topic | Description |
| --- | --- |
| [Agents](/user-guide/cortex-code/cortex-code-desktop/agents) | Subagents for parallel, specialized tasks |
| [Building apps](/user-guide/cortex-code/cortex-code-desktop/building-apps) | Scaffold and deploy Streamlit and Snowflake App Runtime apps |
| [Context management](/user-guide/cortex-code/cortex-code-desktop/context-management) | Track and free up the conversation context window |
| [Data visualization](/user-guide/cortex-code/cortex-code-desktop/data-visualization) | Inline charts from query results |
| [Semantic code search](/user-guide/cortex-code/cortex-code-desktop/semantic-code-search) | Search your codebase in plain English with tgrep |
| [SQL Playground](/user-guide/cortex-code/cortex-code-desktop/sql-playground) | Run and explore SQL interactively |
| [dbt integration](/user-guide/cortex-code/cortex-code-desktop/dbt-integration) | Build, test, and deploy dbt models |
| [Agentic browser](/user-guide/cortex-code/cortex-code-desktop/agentic-browser) | Browse and interact with web content |
| [Agentic notebook](/user-guide/cortex-code/cortex-code-desktop/agentic-notebook) | Jupyter notebooks with AI assistance |
| [Automations](/user-guide/cortex-code/cortex-code-desktop/automations) | Automate recurring agent workflows |

Expand

Show lessSee more

## Customization and extensibility

| Topic | Description |
| --- | --- |
| [Plugins](/user-guide/cortex-code/cortex-code-desktop/plugins) | Install or create plugin packages |
| [Skills](/user-guide/cortex-code/cortex-code-desktop/skills) | Custom instructions the agent follows |
| [Hooks](/user-guide/cortex-code/cortex-code-desktop/hooks) | Scripts that run on events like session start |
| [MCP support](/user-guide/cortex-code/cortex-code-desktop/mcp-support) | Connect external tools via Model Context Protocol |
| [Instruction files](/user-guide/cortex-code/cortex-code-desktop/instruction-files) | Project-level agent instructions |
| [Personalization](/user-guide/cortex-code/cortex-code-desktop/personalization) | Custom instructions and built-in tool toggles |
| [Memory](/user-guide/cortex-code/cortex-code-desktop/memory) | Remember context across conversations |
| [Permission modes](/user-guide/cortex-code/cortex-code-desktop/permission-modes) | Control what the agent can do without asking |

Expand

Show lessSee more

## Monitoring and history

| Topic | Description |
| --- | --- |
| [Usage history view](/sql-reference/account-usage/cortex_code_desktop_usage_history) | Monitor usage and token consumption |

Expand

Show lessSee more

## Security

| Topic | Description |
| --- | --- |
| [Security](/user-guide/cortex-code/cortex-code-desktop/security) | Trust model, recommended baseline, and limits |
| [Managed settings](/user-guide/cortex-code/cortex-code-desktop/managed-settings) | Centrally configure the app for your organization |
| [FAQ](/user-guide/cortex-code/cortex-code-desktop/faq) | Answers to common setup and platform questions |

Expand

Show lessSee more

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
