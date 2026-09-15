# August 20, 2026: Cortex Agent code execution tool (*Preview*)

The Cortex Agent code execution tool is now in public preview. When you enable the tool on an agent, the agent
can generate and run Python in a secure, isolated sandbox to process data, perform calculations, and produce
visualizations. The sandbox includes the Python standard library along with preinstalled data-processing and
plotting libraries such as `numpy`, `pandas`, `scipy`, `pyarrow`, `matplotlib`, and `plotly`. You can install
additional PyPI packages through the Artifact Repository.

Note the following behavior:

- The sandbox doesn’t query your data. When the agent needs data from Snowflake, it runs the query with its SQL
  tools outside the sandbox, and the sandbox works with the results.
- A sandbox is scoped to a single conversation thread. Files written to the mounted workspace persist because
  the workspace is backed by a stage, but in-memory state doesn’t carry over between separate code executions.
- Calls to agents that use owner’s rights don’t support code execution. Invoke the agent with caller’s rights if
  it needs the tool.

For more information, see [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool).
