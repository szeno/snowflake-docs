# Viewing metrics data

You can view metrics data for analysis in the following ways:

- Use Snowsight or Grafana.
- Execute a SELECT command on the event table.

Note

Before you can begin using metrics data, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).

## Visualize on Snowsight

You can use Snowsight to view metrics data captured in the event table.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Query History**.
3. In the **Query History** page, select the query for which you want to view metrics data.
4. Select the **Query Telemetry** tab.
5. Select the span for which you want to view data, then select the **Related Metrics** tab.
6. View the time series metrics over the course of the query and metrics over time.

## Visualize on Grafana

You can also use free partner tools, such as Grafana Cloud, to visualize the metrics data.

For Snowflake dashboard templates and installation instructions for Grafana Cloud, see [Snowflake Telemetry Dashboard Templates](https://github.com/snowflakedb/snowflake-telemetry-dashboard-templates).

## Query with SELECT statement

When querying for data, you can select attribute values within a column by using
[bracket notation](/user-guide/querying-semistructured#label-bracket-notation-when-querying-semistructured-data), as in the following form:

Code in the following example queries the preceding table with the intention of isolating data related to the `DIGITS_OF_NUMBER`
function.

Copy code

```
SET EVENT_TABLE_NAME='my_db.public.my_events';

SELECT TIMESTAMP, RESOURCE_ATTRIBUTES['snow.executable.name'] AS FUNCTION_NAME, RECORD['METRIC']['NAME']AS METRIC_NAME, VALUE
FROM EVENT_TABLE_NAME
WHERE
  RESOURCE_ATTRIBUTES['snow.query.id']  = <INSERT YOUR QUERY ID>
  AND RECORD_TYPE = 'METRIC'
ORDER BY TIMESTAMP DESC;
```
