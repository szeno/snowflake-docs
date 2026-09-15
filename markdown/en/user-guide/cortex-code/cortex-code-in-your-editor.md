# Cortex Code in your code editor

Cortex Code brings Snowflake-aware AI assistance into the code editors and coding agents you already use. Instead of switching to a separate tool, you can run Cortex Code as the agent backend for an editor, add it to an existing editor extension, or route Snowflake prompts to it from Claude Code.

Each of these paths builds on the [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), which is generally available. The CLI carries Snowflake authentication, role-based access control, and the built-in Snowflake skills, so every integration gets the same Snowflake expertise.

## Ways to use Cortex Code in your editor

### ACP-compatible editors

Cortex Code CLI implements the [Agent Client Protocol (ACP)](https://agentclientprotocol.com/), an open standard that lets editors and IDEs embed an external agent as a local subprocess. Supported ACP clients include Zed, JetBrains IDEs, and Neovim. Your editor drives the session while Cortex Code streams responses, tool calls, and file diffs back to the editor.

For Visual Studio Code, use the [Snowflake extension for Visual Studio Code](/user-guide/vscode-ext#label-cortex-code-vscode-extension) instead of ACP.

For prerequisites, generic configuration, and step-by-step setup for Zed and JetBrains IDEs, see [Cortex Code CLI Agent Client Protocol (ACP) support](/user-guide/cortex-code/cortex-code-acp).

### Snowflake extension for Visual Studio Code

The [Snowflake extension for Visual Studio Code](/user-guide/vscode-ext#label-cortex-code-vscode-extension) includes CoCo chat. After you sign in, select the CoCo icon in the Activity Bar to open the CoCo side panel and start a chat session alongside the extension’s object explorer and SQL features.

For details, see [CoCo in the Snowflake extension for Visual Studio Code](/user-guide/vscode-ext#label-cortex-code-vscode-extension).

### Cortex Code in Claude Code

The Cortex Code in Claude Code plugin detects Snowflake-related prompts in your Claude Code session and routes them to Cortex Code. Non-Snowflake prompts stay in Claude Code.

For details, see [Cortex Code in Claude Code](/user-guide/cortex-code/cortex-code-claude-code).

## Monitor usage

Because all editor integrations build on the Cortex Code CLI, usage from these integrations is recorded in the [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_cli_usage_history) view. To query usage across all Cortex Code surfaces in a single view, use [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history).
