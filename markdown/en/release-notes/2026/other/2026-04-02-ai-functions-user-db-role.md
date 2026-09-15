# Apr 02, 2026: AI\_FUNCTIONS\_USER database role (*General availability*)

Snowflake has added an AI\_FUNCTIONS\_USER database role in the SNOWFLAKE database to more granularly manage access
to Cortex AI functions. With this role, you can independently control access to AI functions without requiring
the CORTEX\_USER database role. For example, an account administrator can disable CORTEX\_USER for a role but still
allow that role to use AI functions by doing the following:

1. Revoke SNOWFLAKE.CORTEX\_USER from the role.
2. Grant SNOWFLAKE.AI\_FUNCTIONS\_USER to the role.
3. Verify that the role also has the USE AI FUNCTIONS account-level privilege, which is granted to PUBLIC by default.

For more information about this role, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).
