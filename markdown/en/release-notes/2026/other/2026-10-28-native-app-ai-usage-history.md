# Oct 28, 2026: Cortex AI usage in Native App usage history

You can now use the `SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_DAILY_USAGE_HISTORY` view to track supported Cortex AI
credits attributed to a Snowflake Native App. This includes Cortex Agent token usage, Cortex Search serving and
embedding usage, and Cortex AI Function token usage on application-owned warehouses.

The `CREDITS_USED_BREAKDOWN` array reports these credits under `CORTEX_AGENTS`, `CORTEX_SEARCH`, and
`AI_FUNCTIONS`. Because the existing `CREDITS_USED` total now includes these credits, `CREDITS_USED` values for
applications that use Cortex AI can increase. The view name and columns haven’t changed.

For more information, see [APPLICATION\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/application_daily_usage_history).
