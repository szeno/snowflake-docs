# Cortex Code in Claude Code

The Cortex Code in Claude Code plugin detects Snowflake-related prompts in your Claude Code session and routes them to the [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), where Snowflake-specific skills handle the request. Prompts that aren’t related to Snowflake stay in Claude Code, so you can keep one workflow for both general coding and Snowflake tasks.

## How it works

When you enter a prompt in Claude Code, the plugin runs a lightweight keyword filter to decide whether the prompt is Snowflake-related. If it is, the plugin starts a Cortex Code CLI session, runs the request with the CLI’s built-in Snowflake skills, and returns the result to your Claude Code session. If the prompt isn’t Snowflake-related, Claude Code handles it normally.

You can also route a prompt to Cortex Code explicitly, bypassing the automatic detection:

```
$cortex-run show me my warehouses and their current state
```

## Prerequisites

Before you install the plugin, make sure that:

- [Claude Code](https://www.claude.com/product/claude-code) is installed.
- The [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) (`cortex`) is installed and available on your `PATH`.
- You have a Snowflake connection configured in `~/.snowflake/connections.toml`. To add one, run `snow connection add`.

## Install the plugin

Install the plugin from the [Claude plugin marketplace](https://claude.com/plugins/snowflake-cortex-code). In Claude Code, run:

```
claude plugin install snowflake-cortex-code@claude-plugins-official
```

## Use the plugin

After the plugin is installed, ask Snowflake questions naturally in Claude Code. The plugin detects Snowflake intent and routes those prompts to Cortex Code. For example:

```
Show me my Snowflake warehouses
What databases do I have access to?
List all tables in my current schema
Create a dynamic table that refreshes hourly
```

Prompts that aren’t related to Snowflake, such as “fix the bug in auth.py” or “write a unit test,” stay in your Claude Code session.
