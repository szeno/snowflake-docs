# Jul 29, 2026: Data quality monitoring dashboard (*Public preview*)

The data quality monitoring dashboard is now available in public preview for Enterprise Edition accounts.

The dashboard provides an account-wide view of data quality health in Snowsight. Instead of reviewing results one object at a time, you can use the dashboard to assess the overall health of your data, triage open incidents, and understand which schemas are under active monitoring, all from a single page.

Key capabilities include:

- **Account-wide health summary**: View the percentage of healthy tables and monitoring coverage across your entire account at a glance.
- **Incident triage**: See all open data quality incidents (volume anomalies, freshness anomalies, and failed expectations) in a unified list with filtering by database, schema, and metric type.
- **AI-assisted root-cause analysis**: Select **Investigate** on any incident to open Cortex Code with the incident context pre-loaded. Select multiple incidents to investigate correlated issues in a single thread.
- **Schema-level breakdown**: Browse all monitored schemas with per-schema health metrics, and drill into a schema to see its top failing tables and metrics.
- **Automatic monitoring management**: Use **Manage Monitors** to control which schemas are included in automatic freshness and volume anomaly detection. Snowflake proactively recommends schemas that contain popular tables but are not yet in your monitoring scope.

To navigate to the dashboard, select **Governance & security** » **Data quality** in Snowsight.

For more information, see [Using the data quality monitoring dashboard](/user-guide/data-quality-centralized-dashboard).
