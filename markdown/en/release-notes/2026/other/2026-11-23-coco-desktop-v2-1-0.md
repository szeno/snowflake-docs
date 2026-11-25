# Nov 23, 2026: CoCo Desktop v2.1.0

CoCo Desktop v2.1.0 includes these changes:

- **Plan mode without a confirmation**: The agent switches to Plan mode without asking first. You still approve the plan before any code is written.
- **Model and effort for each subagent**: The agent can choose the model and effort that a subagent runs on, and a subagent’s chat has its own model and effort pickers.
- **Lighter Agentic Browser**: Screenshots are smaller on high-resolution displays, and the agent gets a short summary after each action instead of the whole page.
- **Broader Snowflake object discovery**: A lookup by name without an object type searches every object type in one step.
- **Fixes**: SQL recovers after a Snowflake session expires, requests no longer fail on slow connections while CoCo checks your agent profile, and the dbt **Lineage** panel shows results for runs that finished before you opened it.

For more information, see [CoCo Desktop v2.1.0 release notes](/user-guide/cortex-code/cortex-code-desktop/release-notes/v2-1-0).
