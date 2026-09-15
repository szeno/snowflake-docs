# Feb 25, 2026: Account Usage CORTEX\_AGENT\_USAGE\_HISTORY view (*General availability*)

The [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history)
view in the ACCOUNT\_USAGE schema is now generally available. This view provides visibility into the usage history of Cortex Agents.

The information in the view includes the number of credits consumed each time a user interacts
with Cortex Agents. A request results in one or more calls to underlying tools (for example, Cortex Analyst and Cortex Search). Each row in the view represents a call to the agent and provides detail about
the aggregated tokens and credits in the call as well as granular detail. The view also includes
relevant metadata, such as the user ID, request ID, and the agent ID.

For more information, see [CORTEX\_AGENT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_agent_usage_history).
