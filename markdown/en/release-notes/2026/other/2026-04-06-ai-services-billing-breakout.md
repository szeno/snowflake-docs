# Apr 6, 2026: AI\_SERVICES billing breakout for implemented AI Credits services

Snowflake introduces **more granular billing service types** for a subset of services currently
billed under AI\_SERVICES as part of the transition to **AI Credits**. These changes will impact
both the [METERING\_HISTORY](/sql-reference/account-usage/metering_history) and
[METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) views.
This change **improves customer clarity** and supports more flexible pricing and packaging over time.

The following services are now being broken out of AI\_SERVICES as separate service types:

| Feature | Previous SERVICE\_TYPE | Future SERVICE\_TYPE |
| --- | --- | --- |
| Cortex Agents | AI\_SERVICES | CORTEX\_AGENTS |
| Cortex Code CLI | AI\_SERVICES | CORTEX\_CODE\_CLI |
| Cortex Code UI | AI\_SERVICES | CORTEX\_CODE\_SNOWSIGHT |
| Snowflake CoWork | AI\_SERVICES | SNOWFLAKE\_INTELLIGENCE |

Expand

Show lessSee more

**AI Functions**, **Search Serving**, **Batch Search Serving**, **Cortex Analyst**, **Cortex Fine Tuning**, and
**Provisioned Throughput** remain in AI\_SERVICES.
