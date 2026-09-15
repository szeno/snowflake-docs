# Code mode

Code mode runs the Cortex Code CLI (CoCo) with a lean tool set focused on software engineering. It restricts the agent to file, shell, and code-search tools and turns off Snowflake data tools, Model Context Protocol (MCP) servers, skills, and team and scheduling features.

Because code mode ships a smaller tool set and a system prompt tuned for coding, it sends fewer tokens per turn than the default mode. On coding-heavy work — writing, refactoring, and debugging application code and dbt projects — this lowers token cost, with comparable task quality on software-engineering work.

Code mode is off by default; the CLI starts in standard mode.

## Enable code mode

Start a session in code mode with the `--mode` flag:

Copy code

```
cortex --mode code
```

`--mode` accepts `standard` (the default) or `code`. It works the same in interactive and headless (`--print`) sessions.

To make code mode the default for every session, set `agentMode` in `~/.snowflake/cortex/settings.json`:

Copy code

```
{
  "agentMode": "code"
}
```

Setting `agentMode` to `standard` (or omitting it) keeps the default mode. See [Settings](/user-guide/cortex-code/settings).

## What changes in code mode

Code mode changes the tools available to the agent. Your Snowflake connection is still used for authentication and model access — only the tools the agent can call are restricted.

| Available in code mode | Disabled in code mode |
| --- | --- |
| File editing (`read`, `write`, `edit`, `apply_patch`) | Snowflake data tools (`sql_execute`, dbt, data diff, notebooks) |
| Shell (`bash`, background shells) | MCP servers and their tools |
| Code search (`grep`, `glob`) | Skills (bundled and custom) and the skill curator |
| Web search and fetch | Teams, inter-agent messaging, and cron scheduling |
| Subagents (`task`) | Plan mode and goal mode tools |
| Programmatic tool calling (`python_repl`) | Semantic code search — use `grep` and `glob` instead |

Expand

Show lessSee more

Because Snowflake data tools are turned off, code mode is not suited to tasks that query or modify Snowflake data. Use the default (standard) mode for data work, and code mode for software-engineering tasks.

## When to use each mode

- **Code mode** — writing or editing application code, refactors, bug fixes, running tests, and building or fixing dbt projects. Best when the work is primarily files and shell, and you want lower token cost.
- **Standard mode** (default) — anything that needs Snowflake data access (`sql_execute`, dbt tooling against your account), MCP connectors, skills, teams, or plan and goal modes.
