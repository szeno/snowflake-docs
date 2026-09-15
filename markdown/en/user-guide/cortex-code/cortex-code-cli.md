# CoCo CLI

This topic helps you get started with CoCo CLI, including installation, connection setup, and validation.

Before you begin, ensure you have a Snowflake account with access to the required Cortex models. See [Prerequisites](#label-cortex-code-cli-prerequisites) for full details.

Note

If you don’t have a Snowflake account, you can [sign up for a free CoCo CLI trial](https://signup.snowflake.com/cortex-code).

CoCo CLI is not available on standard Snowflake trial accounts (for example, accounts created at [trial.snowflake.com](https://trial.snowflake.com)). To use CoCo CLI, you need either a paid Snowflake account or the dedicated CoCo CLI trial linked above.

## Install CoCo CLI

CoCo CLI is available for macOS, Linux, and Windows (both WSL and native). Use the instructions below to install CoCo CLI on your platform.

### macOS and Linux (including WSL)

To install CoCo CLI on macOS, Linux, or WSL, issue the following command in a shell:

Copy code

```
curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh
```

This command downloads and runs the installation script, which installs the latest version of CoCo CLI.
The `cortex` executable is installed in `~/.local/bin` by default. The installation script adds this directory
to your PATH by modifying your shell profile.

Tip

If the curl command fails due to `~/.curlrc`, try the command below instead.

Copy code

```
curl -qLsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh
```

The `-q` flag prevents `curl` from reading your `~/.curlrc` file. If you have custom options in `.curlrc`
(such as `--verbose`), they can interfere with the installation script. Always include `-q` when piping
`curl` output to a shell.

### Windows native

To install CoCo CLI on Windows, issue the following command in PowerShell:

Copy code

```
irm https://ai.snowflake.com/static/cc-scripts/install.ps1 | iex
```

This command downloads and runs the installation script, which installs the latest version of CoCo CLI.
The `cortex` executable is installed in `%LOCALAPPDATA%\cortex` by default. The installation script adds
this directory to your PATH.

After installation, invoke CoCo CLI from the Run dialog (Win+R), Command Prompt (`cmd.exe`), or PowerShell.

## Connect to Snowflake

After installing the CoCo CLI, issue the `cortex` command. A setup wizard guides you through the
initial configuration steps, including choosing or setting up a connection to Snowflake.

The first prompt asks you to choose a connection from the existing connections in the `~/.snowflake/connections.toml` file
or to create a new connection.

- To use an existing connection, choose the connection from the list using the up and down arrow keys, then press Enter.
- To create a new connection, choose **More options** by pressing the down arrow key until it is highlighted, then press Enter.
  Follow the prompts to enter your Snowflake account details.

Note

The `connections.toml` is also used by the [Snowflake CLI](/developer-guide/snowflake-cli/index) (`snow` command). If you have already set up a connection
for use with the Snowflake CLI, you can use that connection with the CoCo CLI.

## Start using CoCo

Once connected, try your first request:

```
What can I do with Cortex Code?
```

Type natural-language requests (such as “find tables with PII tags” or “generate a Streamlit app for
SALES\_MART.REVENUE”) and CoCo attempts to fulfill the request by orchestrating Snowflake-native skills and any
MCP tools you have configured. For more information on configuring MCP tools, see [MCP (Model Context Protocol)](extensibility#extensibility-mcp).

As it works on your request, CoCo CLI displays its reasoning steps and actions in the terminal. From time to
time, it may ask you for information that it needs. If you’re in plan mode, it will ask you to confirm each action.

### Example requests

#### Discover your catalog

```
What databases do I have access to?
List every table tagged PII = TRUE in ANALYTICS_DB
Show the lineage from RAW_DB.ORDERS to downstream dashboards
```

#### Generate and run SQL commands

```
Write a query for top 10 customers by revenue
Add a 7-day moving average and show me the results
Explain why this query is slow and optimize it
```

#### Build applications

```
Build a Streamlit dashboard on SALES_MART.REVENUE with filters for date and region
Create a dbt project to transform raw sales data
```

#### Work with Cortex Analyst

```
Use the @models/revenue.yaml semantic model to answer "What was revenue last month?"
Debug my semantic model at @models/revenue.yaml
```

## Prerequisites

To use CoCo CLI, you need the following:

- A Snowflake user account with the necessary permissions to access the data you intend to use with CoCo CLI and to perform operations on it.
  This user must also have the SNOWFLAKE.CORTEX\_USER or SNOWFLAKE.CORTEX\_AGENT\_USER database role. By default, SNOWFLAKE.CORTEX\_USER is granted to all
  users through the PUBLIC role, but your organization may have explicitly revoked it to implement stricter access control.
- Network access to your Snowflake server.
- [Snowflake CLI](/developer-guide/snowflake-cli/index) installed on your workstation.
- One of the following supported platforms:

  - macOS on Apple Silicon or Intel
  - Linux on Intel or ARM
  - Windows Subsystem for Linux (WSL) on Intel
  - Windows Native on Intel

  Note

  Snowflake may add support for other platforms from time to time. Please let your Snowflake representative know if you
  have a specific platform requirement.
- Local terminal access to the `bash`, `zsh`, or `fish` shell on your platform.

For additional configuration options, troubleshooting, and advanced setup, see [CoCo CLI reference](/user-guide/cortex-code/cli-reference).

## Supported platforms

CoCo CLI currently supports the following platforms:

| Platform | Architecture |
| --- | --- |
| macOS | arm64, x64 |
| Linux | x64, arm64 |
| Windows | WSL on x64/amd64; Native on x64 |

Expand

Show lessSee more

Note

Snowflake may add support for other platforms from time to time. Please contact your Snowflake representative if you
have a specific platform requirement.

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

To list the models available to your role or to switch models, use the `/model` command inside
a CoCo CLI session. To set the model for a single invocation, pass `--model`, as in
`cortex --model auto`.

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
