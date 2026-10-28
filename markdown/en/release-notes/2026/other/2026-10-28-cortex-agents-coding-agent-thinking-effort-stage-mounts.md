# October 28, 2026: Cortex Agents Coding Agent thinking effort, system instructions, and stage mounts

The Cortex Agents Coding Agent `agent:run` API now accepts three additional public controls on a request that includes the `code_toolset_all` tool:

- `thinking_effort` sets the orchestration model’s reasoning effort. Accepted values are `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`. Each model uses a subset of those values, and a request above that subset is lowered to the highest level the model accepts. Omit the field to keep the default for the model.
- `instructions.system` appends extra system instructions to the managed coding-agent prompt. The text does not replace the sandbox, tool, or skill instructions.
- `stage_mounts`, on the `code_toolset_all` entry in `tool_resources`, mounts a Snowflake stage or versioned stage into the sandbox. Versioned stages include notebooks, Streamlit apps, workspaces, and agents. `workspace_mounts` is unchanged and still mounts a persistent, writable workspace at version `live`.

For more information, see [Coding Agent](/user-guide/snowflake-cortex/cortex-agents-coding-agent).
