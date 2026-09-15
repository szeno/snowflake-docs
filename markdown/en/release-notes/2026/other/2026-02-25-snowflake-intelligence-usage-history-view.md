# Feb 25, 2026: Account Usage SNOWFLAKE\_INTELLIGENCE\_USAGE\_HISTORY view (*General availability*)

The [SNOWFLAKE\_INTELLIGENCE\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_intelligence_usage_history_view)
view in the ACCOUNT\_USAGE schema is now generally available. This view provides visibility into the usage history of Snowflake CoWork.

The information in the view includes the number of credits consumed each time a user interacts
with Snowflake CoWork. A request results in one or more calls to underlying agents and any
tools (for example, Cortex Analyst and Cortex Search). Each row in the view represents a call to the agent and provides detail about
the aggregated tokens and credits in the call as well as granular detail. The view also includes
relevant metadata, such as the user ID, request ID, Snowflake CoWork ID, and the agent ID.

For more information, see .
