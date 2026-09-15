# Overview of Snowflake CoCo

Snowflake CoCo is an AI-driven intelligent agent integrated into the Snowflake platform, optimized for complex data
engineering, analytics, machine learning, and agent-building tasks. It uses an autonomous agent framework to interact
directly with your Snowflake environment, with deep understanding of Snowflake’s role-based access control (RBAC),
schemas, and best practices.

CoCo supports data analysis, machine learning, and data engineering workflows. It provides a consistent, context-aware interface for users
performing data exploration or developing complex data pipelines.

## Core experiences

CoCo is delivered through three experiences: in Snowsight, as a standalone desktop IDE, and as a command line interface (CLI) that runs in a local shell.
This availability ensures access to AI agentic experiences wherever you work.

### CoCo in Snowsight

Feature — Generally Available

Available to all Commercial (non-Gov), FedRAMP (Moderate and High), DoD, and KSA sovereign accounts with [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled.

CoCo is the persistent, web-based entry point for AI in Snowflake. It is deeply integrated into Workspaces and
Snowsight Admin pages.

Key capabilities:

- **SQL and Python Notebook authoring:** Generate code from natural language or explain and optimize existing queries.
- **Account administration:** Take actions and answer questions about credit consumption, query performance, governance, and user permissions.
- **Within Workspaces:**
  - **Context awareness:** CoCo knows which SQL file or notebook you are currently viewing and uses that as background context for its answers.
  - **Change review:** A visual “diff view” allows you to review and accept AI-suggested changes before they are applied.

### CoCo Desktop

Feature — Generally Available

Available to all Commercial (non-Gov, VPS, Sovereign) accounts with [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled.

CoCo Desktop is a standalone AI-powered IDE for macOS and Windows, deeply integrated with Snowflake. It
provides the full CoCo agent experience in a native desktop application.

Key capabilities:

- **Agent and Editor modes:** Switch between an autonomous agent that completes multi-step tasks and a focused editor
  mode for reviewing and applying AI suggestions.
- **Local file access:** Read and write local repositories, making it ideal for managing `dbt` projects, Streamlit apps,
  and other local codebases.
- **Plugins, skills, and hooks:** Extend the agent with custom tools, skills, subagents, and hooks to fit your workflows.
- **MCP support:** Connect to external tools and data sources through the Model Context Protocol.
- **Agentic browser and notebooks:** Interact with web pages and Snowflake notebooks directly from the IDE.

Get CoCo Desktop

**[Download the latest version](https://www.snowflake.com/en/product/snowflake-coco/downloads/)**. Available for macOS and Windows.

For details about the Desktop experience, see [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop).

### CoCo CLI

Feature — Generally Available

Available to all Commercial (non-Gov, VPS, Sovereign) accounts with [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled.

For power users and developers, the CoCo CLI provides an agentic shell for Snowflake that bridges the gap between your local development environment
(for example, VS Code or Cursor) and your Snowflake account.

For details about the CLI experience, see [CoCo CLI](/user-guide/cortex-code/cortex-code-cli).

#### Key features of the CLI

- **Snowflake integration:** The CLI connects directly to your Snowflake account using your existing authentication methods. You can execute SQL commands,
  view tables, validate [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst) semantic models, and manage multiple connections.
- **Local file access:** Unlike the Snowsight UI, the CLI can read and write to your local repositories, making
  it ideal for managing `dbt` projects or Streamlit apps.
- **Tool orchestration:** The CLI can invoke local `bash` commands, run `git` operations, and execute SQL directly against your Snowflake warehouse.
- **Agent customization:** Support for `AGENTS.md` files and Agent Skills allows you to define custom behaviors for the agent within
  specific projects.
- **Security:** Full support for Snowflake role-based access control (RBAC), OS-level sandboxing, a three-tier approval
  system, and automatic risk assessment help ensure secure operation within your environment.
- **Built-in Snowflake skills:** CoCo includes built-in skills that support key Snowflake workflows such as agent creation, machine
  learning, data engineering, and data governance.
- **Extensibility:** The CLI can be extended with custom tools, skills, subagents, hooks, and profiles to fit your organization’s workflows.
- **Developer friendly:** Developers, data engineers, and data scientists will find the CoCo CLI pleasant to work
  with, thanks to features like session persistence, `git` worktree support, a choice of compact and expanded display
  modes, multiple color themes, and support for `vim`-style keyboard navigation.

### CoCo Agent SDK

Feature — Preview

This feature is in preview.

The CoCo Agent SDK lets you build agentic AI applications using Python and TypeScript. Your agents can read
files, run commands, search codebases, execute SQL, and edit code, using the same tools and agent loop that power
CoCo.

For details about the Agent SDK, see [CoCo Agent SDK](/user-guide/cortex-code-agent-sdk/cortex-code-agent-sdk).

### Model Context Protocol (MCP)

Feature — Preview

This feature is in preview.

CoCo CLI implements the Model Context Protocol (MCP), an open standard for connecting AI agents to external
tools and data sources such as GitHub, Jira, internal APIs, and databases. Add an MCP server once, and its tools
become available to the agent in every CoCo session.

For details about MCP support, see [CoCo CLI Model Context Protocol (MCP) support](/user-guide/cortex-code/cortex-code-mcp).

### Agent Client Protocol (ACP)

Feature — Preview

This feature is in preview.

CoCo CLI implements the Agent Client Protocol (ACP), an open standard that lets editors and IDEs such as Zed,
JetBrains, VS Code, and Neovim embed CoCo as a local agent backend. Editors drive the session while CoCo
streams responses, tool calls, and file diffs back to the editor.

For details about ACP support, see [CoCo CLI Agent Client Protocol (ACP) support](/user-guide/cortex-code/cortex-code-acp).

### Plugins

Feature — Preview

This feature is in preview.

A CoCo CLI plugin is a self-contained package that bundles skills, subagents, slash commands, hooks, and MCP
servers under a single manifest. Share plugins across a team from a Git repository, install them from the official
marketplace, or ship them as part of a Snowflake connection profile.

For details about plugins, see [CoCo CLI plugins](/user-guide/cortex-code/cortex-code-plugins).

## More information

For detailed setup instructions, release history, troubleshooting, and advanced use cases, see the following topics:

- [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight)
- [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop)
- [CoCo Desktop release notes](/user-guide/cortex-code/cortex-code-desktop/release-notes)
- [CoCo CLI](/user-guide/cortex-code/cortex-code-cli)
- [CoCo automations in CLI and Snowsight](/user-guide/cortex-code/cortex-code-automations)
- [CoCo changelog](/user-guide/cortex-code/changelog)
- [Observability](/user-guide/cortex-code/observability)
- [CoCo Agent SDK](/user-guide/cortex-code-agent-sdk/cortex-code-agent-sdk)
- [CoCo CLI Model Context Protocol (MCP) support](/user-guide/cortex-code/cortex-code-mcp)
- [CoCo CLI Agent Client Protocol (ACP) support](/user-guide/cortex-code/cortex-code-acp)
- [CoCo CLI plugins](/user-guide/cortex-code/cortex-code-plugins)
- [Share skills and plugins](/user-guide/cortex-code/cortex-code-skill-plugin-sharing)

## Cost

CoCo is billed based on token consumption. Pricing details are provided in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### CoCo CLI billing

CoCo CLI supports two billing models depending on how you access the product:

- **Subscription:** Individual developers who sign up at [signup.snowflake.com/cortex-code](https://signup.snowflake.com/cortex-code)
  start with a free trial that includes a fixed amount of CoCo CLI usage. The trial is valid for 30 days from
  the date of sign-up. After the trial period ends, the account converts to a paid subscription unless canceled. The
  subscription includes a fixed monthly amount of CoCo CLI usage. If you exceed the included usage, CoCo
  CLI is unavailable until the next billing period.
- **Pay-as-you-go:** Companies with an existing Snowflake account (on-demand or capacity customers) are billed based
  on token consumption.

Any Snowflake compute or storage consumed separately from CoCo CLI usage (for example, virtual warehouse or
storage costs) is billed at standard Snowflake on-demand rates, as described in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

To manage CoCo spend, see
[Cost controls for CoCo](/user-guide/cortex-code/cost-controls).

### CoCo Desktop billing

CoCo Desktop supports two billing models depending on how you access the product:

- **Subscription:** Individual developers who sign up at [signup.snowflake.com/cortex-code](https://signup.snowflake.com/cortex-code)
  start with a free trial that includes a fixed amount of CoCo Desktop usage. The trial is valid for 30 days from
  the date of sign-up. After the trial period ends, the account converts to a paid subscription unless canceled. The
  subscription includes a fixed monthly amount of CoCo Desktop usage. If you exceed the included usage, CoCo
  Desktop is unavailable until the next billing period.
- **Pay-as-you-go:** Companies with an existing Snowflake account (on-demand or capacity customers) are billed based
  on token consumption.

Any Snowflake compute or storage consumed separately from CoCo Desktop usage (for example, virtual warehouse or
storage costs) is billed at standard Snowflake on-demand rates, as described in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

To manage CoCo spend, see
[Cost controls for CoCo](/user-guide/cortex-code/cost-controls).

### CoCo in Snowsight billing

CoCo in Snowsight is billed based on token consumption for customers with an existing
Snowflake account.

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
