# Cortex Agent code execution tool

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Cortex Agent code execution tool is a built-in tool that enables an agent to execute code during a conversation. With access to a code execution tool enabled, your agents can execute scripts to process data, perform calculations, and produce visualizations. By default, the code execution tool runs in a sandboxed, isolated environment that can only access data in the current agent session.

You enable the code execution tool by configuring it in an agent specification. The agent then decides during orchestration when to generate and run code based on the user’s query. The code execution tool is also used when executing Python scripts as part of an agent skill.

There are two tool types that provide code execution capabilities:

- **`code_execution`**: A single code execution tool for running Python in a sandbox. Use this when you want basic code execution alongside other agent tools (Cortex Analyst, Cortex Search, etc.). This tool type is documented on this page.
- **`code_toolset_all`**: The full Cortex Code sandbox toolset, which includes bash, file read/write/edit, grep, glob, web search, SQL execution, and skills. Use this when you want an autonomous coding agent with the full suite of development tools. See [Coding Agent](/user-guide/snowflake-cortex/cortex-agents-coding-agent).

These two tool types are **mutually exclusive** — you cannot include both in a single request. Specifying both returns an error.

## How the code execution tool works

The agent uses the code execution tool alongside other configured tools and skills. During orchestration, the agent evaluates the user’s query and determines whether code execution is the best approach. If so, the agent invokes the code execution tool.

The agent then generates code and executes it in a secure sandbox. By default, the code execution tool environment is isolated and can only access data passed into the session, plus the workspace stage mounted into the sandbox.

The sandbox doesn’t query your data. When the agent needs data from Snowflake, it runs the query with its SQL tools, outside the sandbox, and the sandbox works with the results.

### Default access scope

The sandbox has read and write access to the workspace stage location mounted into it, which is your default user workspace. The agent sees that workspace as a regular directory. Stages mounted for skills are read-only. Beyond those mounts, the sandbox can’t reach data that wasn’t passed into the session.

Because the workspace is backed by a stage, files the agent writes there outlive the sandbox. The sandbox itself is scoped to a conversation thread and is reused across requests on that thread, but it isn’t shared between threads, and it suspends after a period of inactivity. Don’t rely on in-memory state, such as imported modules or variables, surviving between separate code executions: persist anything you need to reuse as a file in the workspace.

## Enabling the code execution tool

To use the code execution tool with a Cortex Agent, the agent must have the code execution tool specified in its tools.

Important

Calls to agents that use owner’s rights don’t support code execution. When an agent is invoked from an owner’s rights stored procedure, the code execution tools are removed from the request and no sandbox is created, even when the tool is enabled in the agent specification. The response includes a warning saying so. Invoke the agent with caller’s rights if it needs code execution.

### Required Cortex Agent permissions

The following permissions on a Cortex Agent affect both your ability to configure and query the agent:

| Privilege | Required for |
| --- | --- |
| USAGE | Allows invoking the agent, including code execution tool use |
| MODIFY | Changing an agent specification to enable or configure the code execution tool |
| OWNERSHIP | Full control over agent configuration and use |

Expand

Show lessSee more

### Agent specification

You enable the code execution tool by adding the resources and configuration for it to an agent specification.

The tool definition to add in the `tools` section of your agent specification is:

Copy code

```
tools:
  - tool_spec:
    type: code_execution
    name: code_execution
```

Enable the tool by adding a `code_execution` section to `tool_resources` in your agent specification:

Copy code

```
tool_resources:
  code_execution:
```

If configuring an agent through the UI, the Code Execution tool toggle for an agent adds the required fields specified previously. New agents created through the UI have this toggle switched on by default.

For full information on the agent specification format and instructions on how to modify an existing agent’s specification, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Sandbox permission policy

By default, tools that modify state require user approval before execution. You can control this behavior using the `permission_policy` field in `tool_resources` under the tool’s name. The policy applies to both the `code_execution` and `code_toolset_all` tool types.

| Policy value | Behavior |
| --- | --- |
| `always_ask` | Always prompt the user for approval before executing state-modifying tools (default) |
| `always_allow` | Skip permission checks and execute all tools without user approval |

Expand

Show lessSee more

Copy code

```
{
  "tools": [
    {
      "tool_spec": {
        "type": "code_execution",
        "name": "code_execution"
      }
    }
  ],
  "tool_resources": {
    "code_execution": {
      "permission_policy": {
        "type": "always_ask"
      }
    }
  }
}
```

Important

Setting `permission_policy` to `always_allow` means the tool can execute code without user confirmation. Only use this setting in trusted, automated workflows where human-in-the-loop approval is not needed.

For the `permission_policy` as it applies to the full Cortex Code toolset, see [Sandbox permission policy](/user-guide/snowflake-cortex/cortex-agents-coding-agent#sandbox-permission-policy).

## Coding Agent (full toolset)

The `code_toolset_all` tool type provides the full Cortex Code sandbox toolset — bash, file read/write/edit, grep, glob, web search, SQL execution, and skills — as a managed coding agent backed by the same runtime that powers Snowflake CoCo. Unlike `code_execution`, which provides a single Python execution tool, `code_toolset_all` routes the request through the Cortex Code orchestration path and automatically provisions the complete set of sandbox tools.

For the full toolset, workspace mounts, skill attachment (bundled, workspace, and stage-based), disabled skills, and orchestration instructions, see [Coding Agent](/user-guide/snowflake-cortex/cortex-agents-coding-agent).

## Default available libraries

The default execution environment for the code execution tool uses Python 3.12, with the Python standard library available. Common data-processing and plotting libraries are also preinstalled, including `numpy`, `pandas`, `scipy`, `pyarrow`, `matplotlib`, and `plotly`. To use additional packages, retrieve them from PyPI through the Artifact Repository, as described in the following section.

## Adding libraries through Artifact Repository

You can use Snowflake’s default PyPI [Artifact Repository](/developer-guide/udf/python/udf-python-packages) to install PyPI packages in the code execution tool environment with support for package policies. Add the `artifact_repositories` key to the `code_execution` resources in your agent specification, as a list containing an entry for `SNOWFLAKE.SNOWPARK.PYPI_SHARED_REPOSITORY`:

Copy code

```
tool_resources:
  code_execution:
    artifact_repositories:
      - SNOWFLAKE.SNOWPARK.PYPI_SHARED_REPOSITORY
```

To access the PyPI repository, you must also assign the role `SNOWFLAKE.PYPI_REPOSITORY_USER` to the owner of the Cortex Agent.

Important

This gives the code execution tool access to retrieve any package published on PyPI. Use caution when granting this level of access.

## Known limitations

Cortex Agent code execution tool is subject to the following known limitations:

- **Thread-scoped sandbox**: A sandbox is scoped to a single conversation thread. It isn’t shared across threads, and in-memory state isn’t preserved between separate code executions. Files written to the mounted workspace do persist, because the workspace is backed by a stage.
- **No owner’s rights support**: Calls to agents that use owner’s rights don’t support code execution. See [Enabling the code execution tool](#enabling-the-code-execution-tool).
- **No SQL in the sandbox**: The sandbox doesn’t query your data. The agent runs SQL with its SQL tools instead, outside the sandbox.
- **Limited stage access**: The sandbox can only read and write the workspace stage mounted into it, not arbitrary stages in your account.
