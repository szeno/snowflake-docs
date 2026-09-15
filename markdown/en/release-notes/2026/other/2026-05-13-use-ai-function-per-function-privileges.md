# May 13, 2026: Per-function privileges for Cortex AI Functions — *General Availability*

You can now grant per-function privileges for Snowflake Cortex AI Functions using `USE AI FUNCTION <name>`.
This gives account administrators finer-grained control over which AI functions individual roles can call,
instead of granting blanket access to all AI functions with the existing USE AI FUNCTIONS privilege.

Key capabilities include:

- **Per-function access control:** Grant access to individual Cortex AI functions such as AI\_COMPLETE,
  AI\_CLASSIFY, AI\_FILTER, or AI\_EMBED, rather than all functions at once.
- **OR relationship with USE AI FUNCTIONS:** The blanket USE AI FUNCTIONS privilege and per-function
  USE AI FUNCTION <name> privileges work together. A role with either privilege can call the corresponding
  functions.
- **Revoke-then-grant workflow:** Revoke USE AI FUNCTIONS from PUBLIC, then grant only the specific
  per-function privileges that each role needs.

For more information, see [USE AI FUNCTION <name> — per-function privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-ai-function-per-function-privileges).
