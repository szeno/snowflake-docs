# Aug 4, 2026: Gateway Monitoring & A/B Testing (*General availability*)

Gateway Monitoring & A/B Testing is now generally available. Use gateway model monitors to track
drift and performance for inference services behind a Snowflake Gateway, compare baseline and
challenger services during live traffic splits, and evaluate results in Snowsight or with SQL.

With this release, you can:

- Create gateway model monitors with [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor) and query drift, performance, and statistical metrics with [monitor metric functions](/sql-reference/functions-model-monitors).
- Compare services during A/B tests using traffic-split gateways and designate a baseline service for drift comparisons.
- Review gateway operational metrics and monitor dashboards in Snowsight, including confidence intervals when supported.

For more information, see [Gateway monitoring & A/B testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing).
