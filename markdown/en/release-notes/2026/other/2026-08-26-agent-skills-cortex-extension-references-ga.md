# Aug 26, 2026: Cortex Extension references in agent skills (*General availability*)

Referencing a Cortex Extension from an agent skill is now generally available. Set the skill source `type` to `CORTEX_EXTENSION` and `path` to the extension’s fully qualified name, and Snowflake expands the reference into the extension’s member skills at request time, so you don’t list each skill individually. Updates to the extension flow to every agent that references it, and access is controlled by the `READ` privilege on the extension object.

For more information, see [Agent skills](/user-guide/snowflake-cortex/cortex-agents-skills).
