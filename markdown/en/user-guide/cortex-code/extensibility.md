# CoCo CLI extensibility

CoCo CLI can be extended with custom behaviors, specialized agents, lifecycle hooks, and external tool integrations. This topic covers the four main extensibility mechanisms:

[Skills](#label-extensibility-skills)
:   Markdown files that inject domain-specific knowledge and instructions into conversations. Use skills to teach CoCo about your organization’s best practices, coding standards, or specialized workflows.

[Subagents](#extensibility-subagents)
:   Autonomous, specialized AI agents that handle specific tasks independently. Subagents enable parallel execution, focused expertise, and complex multi-step workflows.

[Hooks](#extensibility-hooks)
:   Scripts that intercept and customize CoCo’s behavior at key lifecycle points. Use hooks to validate tool inputs, log operations, or enforce policies.

[MCP (Model Context Protocol)](#extensibility-mcp)
:   An open standard for connecting CoCo to external tools and data sources such as GitHub, Jira, and databases.

## Skills

Skills extend CoCo with domain-specific knowledge and capabilities by injecting specialized instructions and enabling additional tools.

You can also share skills and plugins with your team or your entire account. For details, see [Share skills and plugins](/user-guide/cortex-code/cortex-code-skill-plugin-sharing).

### What are skills?

Skills are markdown files containing:

- Domain-specific instructions and best practices
- When to use the skill
- Example workflows
- Optional tool configurations

When you invoke a skill, its instructions are injected into the conversation context.

### Using skills

Run `/skill list` to list available skills, and invoke them by name to load the skill into the conversation.

### Skill locations

Skills are loaded from multiple locations, listed below from highest to lowest priority:

| Location | Path | Scope |
| --- | --- | --- |
| Project | `.cortex/skills/` or `.claude/skills/` | Project |
| User | `~/.snowflake/cortex/skills/` or `~/.claude/skills/` | User |
| Global | `~/.snowflake/cortex/skills/` | System |
| Session | Added temporarily | Session |
| Remote | Cloned from git | Cache |
| Bundled | Built into CoCo | System |

Expand

Show lessSee more

For a complete reference of all bundled skills and how to use them, see [CoCo CLI bundled skills](/user-guide/cortex-code/bundled-skills).

### Creating custom skills

Skills are directories containing a `SKILL.md` file with skill instructions, and optional examples and templates.
You can create skills in one of the following locations:

| Scope | Path |
| --- | --- |
| Project | `.cortex/skills/` or `.claude/skills/` in the project directory |
| Global | `~/.snowflake/cortex/skills/` |
| User | `~/.claude/skills/` |

Expand

Show lessSee more

To start building a custom skill:

1. Create the skill directory. This example creates a skill directory named “my-skill” in the project location:

   Copy code

   ```
   mkdir -p .cortex/skills/my-skill
   ```
2. Create `SKILL.md` in this directory and add skill instructions. This example shows the basic structure:

   Copy code

   ```
   ---
   name: my-skill
   description: Brief description of what this skill does
   tools:
   - optional_tool_name
   ---

   # When to Use

   - Describe when this skill should be invoked
   - List specific user intents or scenarios

   # What This Skill Provides

   Explain the capabilities and knowledge this skill adds.

   # Instructions

   Step-by-step guidance for the AI when this skill is active.

   ## Best Practices

   - Best practice 1
   - Best practice 2

   ## Common Patterns

   ### Pattern 1

   Description and example.

   ### Pattern 2

   Description and example.

   # Examples

   ## Example 1: Basic Usage

   User: $my-skill Do something Assistant: [Expected behavior]

   ## Example 2: Advanced Usage

   User: $my-skill Complex task with @file.txt Assistant: [Expected behavior]
   ```
3. Verify that your skill appears in the listing using the `$$` command:

   ```
   > $$
   ```

   If your skill is listed, it was loaded correctly and is available for use.
4. Use your skill in a conversation:

   ```
   > $my-skill Test it out
   ```

#### Custom skill settings

Each skill’s options are defined in the YAML frontmatter at the top of `SKILL.md`.
The following options are supported:

This example shows a skill that uses two tools:

Copy code

```
---
name: database-admin
description: Database administration tasks
tools:
- sql_execute
- snowflake_object_search
---
```

The SQL execution tool has a different name on each surface. CoCo CLI names it `sql_execute` (renamed
from `snowflake_sql_execute` in CLI 1.1.8), while CoCo Desktop still names it
`snowflake_sql_execute`. If a skill has to work on both surfaces, list both names.

Tool names in a skill’s `tools:` list are runtime tool IDs and are
case-sensitive. Built-in tools such as `bash`, `read`, and `write` are lowercase.

#### Skill best practices

To write effective skills, follow these guidelines:

- Be specific: Clear instructions produce better results
- Provide examples: Show expected inputs and outputs
- Include edge cases: Handle common errors and exceptions
- Keep focused: One skill equals one domain or capability

### Managing skills

| Slash command | Description |
| --- | --- |
| `/skill` | Interactive skill manager |
| `/skill list` | List all skills |
| `/skill sync <name>` | Sync to global location |
| `/skill add <path>` | Add a skill from a local path, Git repository, tarball, or Snowflake stage |

Expand

Show lessSee more

#### Skill conflicts

When the same skill exists in multiple supported locations, and the contents differ, a conflict occurs, and a conflict
indicator appears in the skill listing. Use `/skill sync` to resolve conflicts by syncing the local scope to the
global scope.

### Composing skills

Custom skills can reference other skills, or combine skills with file context:

```
> $code-review Review @src/auth.py following $security-guidelines
```

### Recommended skill sharing

Snowflake recommends sharing skills through the Snowflake catalog, a Git repository, or a Snowflake stage.

#### Snowflake catalog

Use the Snowflake catalog to share skills and plugins across your account with built-in governance and discoverability. Skills and plugins shared this way appear on the **Skills and plugins** page under **AI & ML** in Snowsight. For details, see [Share skills and plugins](/user-guide/cortex-code/cortex-code-skill-plugin-sharing).

#### Git repositories

Use a Git repository when your team already stores versioned skills in Git. A repository can contain any number of
skills. The layout should match the local skill structure.

```
/skill add https://github.com/org/my-skills.git
```

Git-based skills are cached locally.

#### Snowflake stages

Use a Snowflake stage when you want to distribute skills through Snowflake and control access with Snowflake roles.
Publish one or more local skills to a stage, let users add skills directly from that stage, or publish a profile that
references the same shared stage.

Copy code

```
cortex skill publish ./my-skills --to-stage @MY_DB.MY_SCHEMA.MY_STAGE/skills/
cortex skill add @MY_DB.MY_SCHEMA.MY_STAGE/skills/
cortex profile publish data-analyst --skill-stage @MY_DB.MY_SCHEMA.MY_STAGE/skills/
```

For internal stages, grant `READ` to users who load skills and `WRITE` to users who publish them. To grant
`WRITE`, grant `READ` first. For more information, see [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) and
[Managing Snowflake stages](/developer-guide/snowflake-cli/stages/manage-stages).

#### Snowflake Git repositories

To mirror an external Git repository into Snowflake, create a Snowflake Git repository and then add skills from the
repository branch path that contains the skill files.

Copy code

```
cortex skill publish --from-git https://github.com/org/my-skills.git \
  --to-repo MY_DB.MY_SCHEMA.MY_SKILLS_REPO
cortex skill add @MY_DB.MY_SCHEMA.MY_SKILLS_REPO/branches/main/
```

For setup requirements, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up) and
[CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository).

### Skill command reference

CLI commands:

Copy code

```
cortex skill list
cortex skill add <path>
cortex skill update <source>
cortex skill publish [path] --to-stage <stage>
cortex skill publish --from-git <url> --to-repo <repo>
cortex skill remove <path>
```

For a full list of skill CLI commands and options, run `cortex skill --help`. For plugin CLI commands, run `cortex plugin --help`.

Slash commands:

```
/skill list
/skill add <path>
```

### Skill troubleshooting

Skill not activating
:   - Use specific language related to the skill’s purpose
    - Mention the skill explicitly: “Use semantic-view-optimization”
    - Check availability: `/skill list`

Unexpected behavior
:   - Provide more context about your goal
    - Try a more specific request
    - Submit feedback: `/feedback`

## Subagents

Subagents are autonomous, specialized AI agents that handle specific tasks independently. They enable parallel
execution, focused expertise, and complex multi-step workflows.

Subagents:

- Execute independently from the main conversation
- Have their own context and tool access
- Can run in the foreground or background
- Specialize in specific domains or tasks

### Built-in subagent types

#### `general-purpose`

All-purpose agent with access to all tools. It’s best for:

- Complex research tasks
- Multi-step code changes
- Tasks requiring multiple tools

#### `explore`

Fast codebase exploration specialist. Best for:

- Finding files by patterns
- Searching code for keywords
- Understanding codebase structure
- Quick reconnaissance

You can specify how thoroughly the Explore agent searches:

- `"quick"`: Basic search
- `"medium"`: Moderate exploration
- `"very thorough"`: Comprehensive analysis

#### `plan`

Designs and outlines complex implementation plans. Best for:

- Designing implementation strategies
- Identifying critical files
- Evaluating architectural trade-offs
- Creating step-by-step plans

#### `feedback`

Structured feedback collection. Best for:

- Gathering user input
- Structured questions
- Session feedback

### Running subagents

CoCo automatically delegates to subagents when appropriate. For example, this query delegates to an Explore agent:

```
> Find all files that import the authentication module
```

You can also explicitly request specific subagent types by name:

```
> Use an Explore agent to find all database query definitions
> Use the Explore agent to find all API endpoint definitions
> Launch a Plan agent to design the authentication refactor
```

You can also request that multiple subagents run in parallel to tackle different aspects of a task:

```
> In parallel, search for all test files and all config files
```

Agents can run in the background while you continue working:

```
> Run a background agent to refactor all the test files
```

The agent starts immediately and returns an agent ID for tracking. When the agent completes, you can retrieve its output using its ID:

```
> Get the output from agent abc1234
```

To monitor the status of all running subagents, use the `/agents` command (or press Ctrl-B) to open the background
process viewer. You can stop a running agent using its ID, or with the `/agents` interface:

```
> kill agent abc1234
```

Killed agents stop running, but retain their context indefinitely. You can resume a killed agent using its ID:

```
> Resume agent abc1234 and continue from where it left off
```

### Agent types

Autonomous
:   An autonomous agent runs without user interaction. The agent:

    - Completes independently
    - Never blocks for questions
    - Is suited for well-defined tasks

Non-Autonomous
:   A non-autonomous agent can pause execution to ask the user questions. The agent:

    - May ask clarifying questions
    - Can request permissions interactively
    - Is suited for tasks needing guidance

Custom
:   Custom agents are user-defined subagents with specialized prompts and configurations. You create agents tailored
    to specific domains or workflows in Markdown files, similar to custom skills.

### Creating custom subagents

Custom subagents are defined in Markdown files with YAML front matter. The front matter specifies the agent’s name, description, tool access, and model.
The body contains the system prompt that guides the agent’s behavior.

You can store custom agent Markdown files in one of three locations:

| Scope | Path |
| --- | --- |
| Project | .cortex/agents/ or .claude/agents/ |
| Global | ~/.snowflake/cortex/agents/ |
| User | ~/.claude/agents/ |

Expand

Show lessSee more

The format of an agent definition is shown below:

Copy code

```
---
name: my-agent
description: What this agent specializes in
tools:

- bash
- read
- write

model: claude-sonnet-4-5
---

# System Prompt

You are a specialized agent for [domain].

## Your Responsibilities

1. Task 1
2. Task 2

## Guidelines

- Guideline 1
- Guideline 2

## Output Format

Describe expected output format.
```

#### Example: Test Runner agent

The following Markdown file defines a custom Test Runner agent that runs tests and summarizes results:

Copy code

```
---
name: test-runner
description: Runs tests and reports results
tools:
- bash
- read
- grep
---

# Test Runner Agent

You run tests and provide clear reports of the results.

## Process

1. Identify the test framework (pytest, jest, go test, etc.)
2. Run appropriate test command
3. Parse and summarize results
4. Highlight failures with relevant code context

## Output Format

## Test Results Summary

- Total: X
- Passed: Y
- Failed: Z

## Failures

### Test Name

- File: path/to/file.py
- Error: Description
- Relevant code snippet
```

#### Agent configuration

A custom agent’s configuration is specified in the Markdown file’s YAML front matter.

Tool access
:   Agents can specify which tools they have access to:

    Copy code

    ```
    tools:
    - "*"           # All tools
    - bash          # Specific tools
    - read
    - write
    ```

    Tool names in a `tools:` list are the runtime tool IDs, which are lowercase, such as `bash`, `read`,
    `write`, `grep`, and `glob`. Capitalized names such as `Bash` don’t resolve. An unrecognized entry is
    skipped silently, so an agent whose whole list is capitalized starts with no tools at all and reports
    no error. If your agent behaves as though it can’t read files or run commands, check the casing in its
    `tools:` list first.

Model selection
:   You can choose a model for a specific agent. This overrides the session’s default model.

    Copy code

    ```
    model: claude-sonnet-4-5   # Specific model
    model: auto                # Cost-optimized
    ```

### Worktree isolation

Agents can be run in isolated git worktrees, or branches. When you request worktree isolation, CoCo CLI creates a separate git
worktree for the agent to operate in. This allows multiple agents to run in parallel without conflicting changes, and is easy to clean up afterward.
Isolated worktrees are particularly useful for exploration and experimentation. The git branch created by the agent is named `agent/<agentId>`.

To use worktree isolation, simply include it in your prompt:

```
> Run a background agent with worktree isolation to implement feature X
```

### Swarm pattern

You can launch a swarm of agents to tackle different aspects of a complex task in parallel. Each agent works
independently, and results are aggregated when all agents finish. All types of agents can participate in a swarm.

Use cases for swarms include:

- Code Analysis: Multiple agents analyze different aspects
- Refactoring: Parallel agents handle different files
- Testing: Agents run different test suites
- Documentation: Agents document different components

To create a swarm, simply describe the different agents you want to launch:

```
> Launch a swarm of agents:
> 1. Explore agent to find all database queries
> 2. Explore agent to find all API endpoints
> 3. Explore agent to find all test files
```

### Subagent best practices

Use subagents for:

- Complex tasks: Break into subtasks for parallel execution
- Exploration: Use Explore agent for codebase searches
- Planning: Use Plan agent before major changes
- Background work: Long-running tasks that don’t need attention

Subagents may not be ideal for:

- Simple queries: Direct tools are faster
- Single-file edits: Main agent is more efficient
- Interactive work: When you need immediate feedback

Detailed prompts are generally more effective:

| Good | Find all Python files that contain database queries and list them with line numbers |
| --- | --- |
| Better | Use the Explore agent (very thorough) to find all Python files containing database queries. For each file, extract the query patterns and identify potential SQL injection risks. |

Expand

Show lessSee more

### Viewing active subagents

`/agents` command
:   Issue the `/agents` command in a CoCo session to open the interactive agent viewer.
    This interface shows all running agents, their types, statuses, and output previews.

Background process viewer
:   In a CoCo CLI session, press Ctrl-B to view:

    - All background processes
    - Agent sessions
    - Bash processes

### Agent limits

The following limits apply to subagents in CoCo CLI:

- Maximum 50 concurrent background agents
- Agents inherit session permissions
- Background agents cannot spawn other background agents

## Hooks

Hooks allow you to intercept and customize CoCo’s behavior at key lifecycle points. A hook is a prompt or shell script that executes in response to an event:

- Before tool use: Validate or modify tool inputs
- After tool use: Add context or log results
- On user input: Inject session context
- On session events: Initialize or cleanup

### Hook events

The following events can trigger hooks:

| Event | Description | Can block |
| --- | --- | --- |
| PreToolUse | Before tool execution | Yes |
| PostToolUse | After tool execution | No |
| PermissionRequest | When permission is needed | Yes |
| UserPromptSubmit | When user submits prompt | No |
| SessionStart | When session starts | No |
| SessionEnd | When session ends | No |
| PreCompact | Before context compaction | No |
| Stop | When user stops Claude | No |
| SubagentStop | When subagent stops | No |
| Notification | On system notifications | No |
| Setup | During initialization | No |

Expand

Show lessSee more

### Configuring hooks

Hooks are configured in settings files, which can be in any configuration directory (listed below from highest to lowest priority):

| Location | Path |
| --- | --- |
| Local | `.claude/settings.local.json` or `.cortex/settings.local.json` |
| Project | `.claude/settings.json` or `.cortex/settings.json` |
| User | `~/.claude/settings.json` |
| Global | `~/.snowflake/cortex/hooks.json` |

Expand

Show lessSee more

Hooks are defined in JSON format, specifying the event, tool matcher, and hook actions. A simple example of a pre-tool-use hook is shown below:

Copy code

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/validate-bash.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Two hook types are supported: command hooks and prompt hooks.

- Command hooks run shell commands or scripts.

  Copy code

  ```
  {
    "type": "command",
    "command": "bash /path/to/script.sh",
    "timeout": 60,
    "enabled": true
  }
  ```
- Prompt hooks are evaluated as natural language prompts for a language model.

  Copy code

  ```
  {
    "type": "prompt",
    "prompt": "Is this command safe? $ARGUMENTS",
    "timeout": 30
  }
  ```

To execute your hook only on specific tools, place tool names or patterns in the `matcher` field. For example, to
match all SQL tools, use `"matcher": ".*sql.*"`. You can use regular expressions to match multiple tools.

The pattern is matched against the runtime tool name, which is case-sensitive. Built-in tool names are
lowercase, so `bash` matches and `Bash` doesn’t.

| Pattern | Matches |
| --- | --- |
| `*` | All tools |
| `bash` | Only `bash` |
| `edit|write` | `edit` or `write` |
| `mcp__.*` | All MCP tools |
| `notebook.*` | `notebook_edit_cell`, `notebook_run_cell` |

Expand

Show lessSee more

### Writing hook scripts

Hook scripts accept JSON input via standard input and return JSON output via standard output.
The output contains a field indicating whether the operation is allowed or denied. Optionally,
the hook script can pass back a modified version of the tool input.

Sample input:

Copy code

```
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "bash",
  "tool_input": {
    "command": "ls -la"
  }
}
```

Sample output:

Copy code

```
{
  "decision": "allow",
  "systemMessage": "Note: This operation was validated.",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "updatedInput": {
      "command": "ls -la --color=never"
    }
  }
}
```

The return code indicates whether to block the operation:

- 0: Do not block
- 2: Block

This information can also be returned as part of the JSON output as shown below.

Copy code

```
{
  "decision": "block",
  "reason": "Operation not allowed"
}
```

The following environment variables are available in hook scripts:

| Variable | Description |
| --- | --- |
| `CORTEX_PROJECT_DIR` | Project directory path |
| `CORTEX_CODE_REMOTE` | `"true"` if web context |
| `CORTEX_ENV_FILE` | Persistent env file path |

Expand

Show lessSee more

### Hook examples

The following examples illustrate possible output for common hook use cases.

#### Modify Tool Input

Copy code

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "updatedInput": {
      "command": "modified command"
    }
  }
}
```

#### Add Context

Copy code

```
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Note: File was recently modified."
  }
}
```

#### Show System Messages

Copy code

```
{
  "systemMessage": "Warning: This operation may take a while."
}
```

#### Permission Decisions

Copy code

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved by policy"
  }
}
```

#### Remote Hooks

You can reference scripts in git repositories as shown below:

Copy code

```
{
  "type": "command",
  "command": "bash",
  "source": {
    "source": "github:org/hooks-repo/scripts/validate.sh",
    "ref": "main"
  }
}
```

### Hook best practices

- Keep hooks fast: Timeouts default to 60 seconds
- Handle errors gracefully: Return exit 0 if uncertain
- Log for debugging: Write to files for troubleshooting
- Use matchers: Target specific tools, not all
- Test thoroughly: Use hooks manager to verify behavior

## Model Context Protocol (MCP)

You can connect CoCo CLI to external tools and data sources with Model Context Protocol (MCP). MCP is an open
standard for connecting AI agents to external tools such as GitHub, Jira, and databases. Once configured, MCP servers
give CoCo access to hosted tools beyond built-in capabilities.

### Transport types

CoCo supports three MCP transport types:

| Type | Use Case | Connection |
| --- | --- | --- |
| stdio | Local tools, CLI wrappers | Subprocess with stdin/stdout |
| http | Web services, APIs | HTTP requests |
| sse | Real-time services | Server-Sent Events |

Expand

Show lessSee more

You can use OAuth to authenticate to HTTP MCP servers. The first time you connect to a server configured for OAuth,
CoCo CLI opens a browser window, where the user authenticates. The resulting token is stored in
`~/.snowflake/cortex/mcp_oauth/` and automatically refreshed as needed. The following is a sample OAuth configuration:

Copy code

```
{
   "oauth": {
      "client_id": "pre-registered-client-id",
      "client_name": "My Client",
      "redirect_port": 8585,
      "scope": "openid mcp read write",
      "authorization_server_url": "https://auth.example.com"
   }
}
```

### Managing MCP servers

You can issue the `/mcp` command in an interactive CoCo CLI session to open an interactive MCP status viewer.
Use the `cortex mcp` command to manage MCP server configurations from the command line.

| Command | Description |
| --- | --- |
| **Command line** | **Description** |
| cortex mcp add | Add a new server (see below) |
| cortex mcp list | List configured servers |
| cortex mcp get <server> | Get details for a specific server |
| cortex mcp remove <server> | Remove a server |
| cortex mcp start <server> | Check server status and available tools |

Expand

Show lessSee more

#### Adding a server

The `cortex mcp add` command accepts options for configuring servers.

Copy code

```
cortex mcp add <name> <command> [args...]
```

Options:

```
--transport, -t    Transport type (stdio, http, sse)
--type             Alias for --transport
--env, -e          Environment variable (KEY=value)
--header, -H       HTTP header
--timeout          Connection timeout in ms
```

Note

MCP tools are namespaced to avoid conflicts, using the format below:

```
mcp__{server-name}__{tool-name}
```

For example, a tool called `search` from server `github` is given the name `mcp__github__search`.

### MCP configuration

MCP server configuration is stored in `~/.snowflake/cortex/mcp.json` under the key `mcpServers`. The following example
shows the structure of a configuration file with a single MCP server:

Copy code

```
{
   "mcpServers": {
      "server-name": {
         "type": "stdio",
         "command": "command-to-run",
         "args": ["arg1", "arg2"]
      }
   }
}
```

#### Environment variables

Use the `${VAR}` or `$VAR` syntax to insert the values of environment variables into the configuration file.

Copy code

```
{
"mcpServers": {
   "my-server": {
      "type": "http",
      "url": "https://api.example.com",
      "headers": {
      "Authorization": "Bearer ${MY_API_TOKEN}"
      }
   }
}
```

Important

It is a best practice to use environment variables for credentials. Never hardcode tokens in `mcp.json`.
Add a line to your shell’s profile, such as `~/.bashrc` or `~/.zshrc`, like the following:

Copy code

```
export GITHUB_TOKEN="your_token_here"
```

#### Configuration from the command line

To add an MCP server from the command line, use the `cortex mcp add` command. For example:

| Action | Command |
| --- | --- |
| Add stdio server | `cortex mcp add git-server uvx mcp-server-git` |
| Add HTTP server | `cortex mcp add api-server https://api.example.com --type http` |
| Add with environment variables | `cortex mcp add my-server npx my-mcp-server -e API_KEY=secret` |
| Add with headers | `cortex mcp add my-server https://api.example.com -H "Authorization: Bearer token"` |

Expand

Show lessSee more

### Using MCP tools

Once configured, MCP tools are available automatically in CoCo CLI sessions. You invoke them via natural
language commands:

```
Show me recent GitHub pull requests
Create a Jira ticket for this bug
Query the PostgreSQL database for user activity
```

Permissions are requested on first use. Configure defaults in `~/.snowflake/cortex/permissions.json`:

Copy code

```
{
  "allow": ["mcp__github__read_file", "mcp__github__list_repos"],
  "deny": ["mcp__github__delete_repo"]
}
```

### Sample MCP configurations

The following examples illustrate MCP server configurations for common use cases.

#### Git Server (stdio)

Copy code

```
{
  "mcpServers": {
    "git": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

#### HTTP API with OAuth

Copy code

```
{
  "mcpServers": {
    "my-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "oauth": {
        "client_id": "my-client-id",
        "redirect_port": 8585,
        "scope": "openid mcp"
      }
    }
  }
}
```

#### SSE Server with Headers

Copy code

```
{
  "mcpServers": {
    "realtime": {
      "type": "sse",
      "url": "https://realtime.example.com/events",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-Custom-Header": "value"
      },
      "timeout": 30000
    }
  }
}
```

#### Sourcegraph Integration

Copy code

```
{
  "mcpServers": {
    "sourcegraph": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@sourcegraph/mcp-server"],
      "env": {
        "SRC_ACCESS_TOKEN": "${SOURCEGRAPH_TOKEN}",
        "SRC_ENDPOINT": "https://sourcegraph.company.com"
      }
    }
  }
}
```

### MCP troubleshooting

Server not connecting
:   - Check `/mcp` during a session to make sure it is listed
    - Use `cortex mcp start <server>` to test connectivity
    - Ensure credentials are correctly set in environment variables
    - `cat ~/.snowflake/cortex/logs/mcp.log` to review the log for clues

Tools not appearing
:   - Run `cortex mcp list` to verify configuration
    - Make sure tool names are valid (contain only alphanumeric characters, underscores, and hyphens)
    - Check that tool names are shorter than 64 characters

OAuth issues
:   - Clear cached tokens: `rm ~/.snowflake/cortex/mcp_oauth/{server}*`
    - Reconnect to trigger new OAuth flow
    - Check redirect port is available (default 8585)

Environment variables not expanding
:   - Use `${VAR}` syntax (with braces) rather than `$VAR`
    - Ensure variable is set in your shell (`echo $VAR`)
    - Check for typos in variable names

### MCP best practices

- Use descriptive server names: Makes tool namespacing clear
- Set appropriate timeouts: Default is 10 minutes for tool listing
- Secure credentials: Use environment variables, not hardcoded secrets
- Test connections: Use `cortex mcp start` before relying on a server
