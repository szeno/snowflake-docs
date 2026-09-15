# Feb 20, 2026: USE AI FUNCTIONS account privilege for Cortex AI Functions

Snowflake now provides the USE AI FUNCTIONS account privilege to control access to Cortex AI Functions. This privilege allows administrators to manage which roles can use AI Functions across the account.

By default, the USE AI FUNCTIONS privilege is granted to the PUBLIC role, allowing all users to access Cortex AI Functions. Account administrators can revoke this privilege from PUBLIC and grant it to specific roles for more granular access control.

Users need both the USE AI FUNCTIONS account privilege (or a per-function USE AI FUNCTION <name> privilege) and one of the CORTEX\_USER or AI\_FUNCTIONS\_USER database roles to use Snowflake Cortex AI Functions.

For finer-grained control over individual AI functions, see [USE AI FUNCTION <name> — per-function privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-ai-function-per-function-privileges).

For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).
