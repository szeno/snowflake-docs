# Apr 14, 2026: Monitor Cortex Search requests (*Preview*)

Cortex Search request monitoring is now available in public preview.

You can enable request logging on a Cortex Search Service to collect detailed
information about search requests for monitoring and debugging purposes. With
request logging enabled, you can review query patterns, response times, and
request details for a Cortex Search Service.

Request logs are stored in the `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` event
table and are accessible using the `snowflake.local.get_ai_observability_events`
function or by querying the event table directly as ACCOUNTADMIN.

For more information, see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor).
