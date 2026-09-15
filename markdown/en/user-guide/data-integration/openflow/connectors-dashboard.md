# Monitor connectors using the Openflow Connectors Dashboard

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

The Openflow Connectors Dashboard provides a high-level view of all installed connectors, health snapshots,
and key performance indicators, such as the aggregated average throughput and total data ingested by all connectors matching
the filter criteria.

## Prerequisites

To use the Openflow Connectors Dashboard, the following prerequisites must be met:

- You need at least read-only permissions on the event table.
- You must have the following minimum Openflow versions:

  - BYOC deployment: 1.36.0
  - Snowflake deployment: 1.26.0
  - Runtime: 2026.3.17.13
- You must have the following minimum connector versions. These versions apply to Database connectors only.
  Other connector types don’t have a minimum version requirement for dashboard support.

  | Connector | Minimum version |
  | --- | --- |
  | MySQL | 0.33.0 |
  | PostgreSQL | 0.39.0 |
  | MongoDB | 0.17.0 |
  | SQL Server | 0.27.0 |
  | Oracle Embedded License | 0.25.0 |
  | Oracle Independent License | 0.24.0 |

  Expand

  Show lessSee more

See [Snowflake Openflow version history](/user-guide/data-integration/openflow/version-history) for more information.

## Access the Openflow Connectors Dashboard

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow** and navigate to the **Connector Observability** tab.

   The Openflow Connectors Dashboard appears.

## The Openflow Connectors Dashboard overview

The Openflow Connectors Dashboard displays the following information:

**Status**
:   Shows the number of connectors with the following statuses:

    - **Healthy**: Didn’t encounter any errors during the selected time period.
    - **Unhealthy**: Logged errors in the event table during the selected time period or has one or more tables in
      **Failed** state (Database connectors only).
    - **Upgrade required**: Openflow deployment, runtime, or connector aren’t running the minimum required versions
      to display health and performance metrics. Review the version prerequisites and upgrade as needed.

**Average throughput**
:   Measures the rate at which data is read from source systems and sent to Snowflake across all connectors.

    - The **Average throughput** » **Ingested** metric measures how fast data is sent to Snowflake across all connectors that match
      the primary filter criteria (time frame and event table).
    - The **Average throughput** » **Read** metric measures how fast Openflow reads data from source systems across all connectors that match
      the primary filter criteria (time frame and event table).

**Total data ingested**
:   Shows how much data all connectors that match the primary filter criteria for time frame and event table have sent to Snowflake during the selected time period.
    Use this metric to quickly identify ingestion anomalies over a specific time period.

For custom telemetry queries beyond the dashboard, see [Monitor Openflow using telemetry data](/user-guide/data-integration/openflow/monitor).

Note

- **Total data ingested** and **Average throughput** metrics include both raw payload and structural overhead such as JSON keys, braces,
  and delimiters. Because these metrics track the total transmitted volume, these figures might be higher than the uncompressed data reported
  by Snowpipe Streaming or the final storage volume in your destination table.
- The connectors appear in the list if they match the selected filter criteria and have recorded telemetry events during the selected time frame.
- If you examine longer time frames, the list might show connectors that were previously deleted.

  For example, you deployed a connector six days ago, and then deleted that connector two days ago. If you set the time frame to **Last 7 days**,
  the connector appears in the list because it recorded telemetry events in the last 7 days.

### Filtering connectors

The Openflow Connectors Dashboard supports the following filters:

**Event table**
:   The Openflow connectors event table you want to monitor. This filter displays event tables that are associated with at least one Openflow deployment,
    as well as the default event table and the account event table. You can select only one event table at a time. Event table views are also supported.

    The event table is set when you set up Openflow.

    Tip

    To view the event table associated with an Openflow deployment, use the [DESCRIBE OPENFLOW DATA PLANE INTEGRATION](/sql-reference/sql/desc-oflow-data-plane-integration) command.
    See [Set up Openflow - Snowflake Deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment) or
    [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) for more information on configuring event tables.

Time frame
:   Use this filter to identify relevant connectors in a specific time frame.

    Tip

    To get the most up-to-date results about the connector health, select the **Last Hour** time period.

**Status**
:   Enables filtering for **Healthy**, **Unhealthy**, or **All** connectors.

**Source**
:   Enables filtering by the source system based on known deployed connectors. The filter only shows sources that are used by your connectors.

**Deployment**
:   Enables filtering by Snowflake Openflow deployments.

    This filter displays data plane integration names, which are composed of the prefix `OPENFLOW_DATAPLANE_` followed by the deployment ID.
    To find the deployment ID, navigate to Openflow, select the **Deployments** tab, then select **View Details**.

**Runtime**
:   Enables filtering by Snowflake Openflow runtimes.

    This filter displays the runtime keys. To match runtime keys with Openflow runtime names in the UI, navigate to Openflow, select the **Runtimes** tab, then
    select **View Details**, and find the corresponding key.

**Type**
:   Enables filtering by connector type: Databases, SaaS, Streaming, Unstructured, Other.

Note

- Primary filters (event table and time frame) are applied before secondary filters (status, source, deployment, runtime, or type).
- The secondary filters (status, source, deployment, runtime, type) don’t apply to the throughput and data ingested visuals.

## Monitoring Openflow connectors

To monitor the connector details, select [![Vertical more icon](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **View Details**.

### Database connectors

The details page shows the following information for each table that is part of the Database connector configuration:

**Table replication status**
:   Tables can either be in **Active** or **Failed** replication status. The replication status is based on the most recent telemetry event
    that is available for the table. Events that cause replication to fail for a table immediately result in a **Failed** replication
    status in the dashboard. Use the **Failure Reason** message to identify the issue.

**Error distribution**
:   Helps you understand when the connector experienced issues, so that you can identify any potential problems with source systems,
    connector configuration, or the Snowflake destination.

**Table name**
:   Shows the schema and table names for all tables that are configured to be replicated by the connector. The list matches the
    **Included Table Names** or **Included Table Regex** configuration parameters of the connector.

**Replication status**
:   Shows whether each table is in **Active** or **Failed** replication status.

**Replication phase**
:   Shows the current table replication phase. After configuration in the connector, tables enter the **New** replication
    phase, progress to the **Snapshot Load** phase, perform the initial load, and ultimately enter the **Incremental Replication** phase
    when individual change data capture events are processed.

**Last Ingested**
:   Shows the timestamp of the last inserted record into the destination table during the selected time frame. When looking at this
    metric, consider a short delay between the records being ingested and events being logged and available to query.

    The connector updates this timestamp after each merge query and continues to emit the last known value every minute, even when
    no new data is being ingested. If no merge query has occurred for more than 3 days, the connector stops emitting the metric
    entirely and the dashboard shows **More than 3 days ago** instead of a timestamp. If the last ingestion timestamp falls outside
    the selected time frame, switch to a longer window such as **Last 24 hours** or **Last 7 days** to retrieve it.

You can use the **Replication status**, **Replication phase**, and time frame filters to narrow down the table list.

### All connectors

**Connector status**
:   Shows the connector health status: **Healthy** if no error messages were encountered during the selected time frame,
    or **Unhealthy** if any error messages were encountered.

**Error distribution**
:   Shows a count of how many errors this connector encountered during the selected time period.

**Average throughput**
:   Measures the rate at which data is read from source systems and ingested into Snowflake for the selected connector.

    - The **Average throughput** » **Ingested** metric measures how fast the selected connector ingests data into Snowflake.
    - The **Average throughput** » **Read** metric measures how fast the selected connector reads data from source systems.

**Total data ingested**
:   Shows how much data the selected connector has ingested into Snowflake during the selected time period.
    Use this metric to quickly identify ingestion anomalies over a specific time period.

### Custom flows

Custom flows built on the Openflow canvas can also be monitored on the dashboard, but only if they are represented
as process groups on the root canvas and are actively version-controlled in a customer Git repository using the
Openflow Git integration. Custom flows that don’t meet these criteria don’t appear in the dashboard.

For more information, see [Version control for custom flows](/user-guide/data-integration/openflow/version-control-custom-flows).

## Debugging Openflow connectors

The Openflow Connectors Dashboard serves as an entry point for debugging connector-specific issues and makes all connector logs easily accessible to users.

### Troubleshoot connectors with AI

Use AI-assisted troubleshooting to get root cause analysis and remediation steps for unhealthy connectors directly from the dashboard,
without writing a prompt or switching tools. The AI assistant combines event table logs, connector metrics, and built-in runbooks
to identify the issue and recommend next steps. It can also surface source system or Snowflake destination configuration problems
that contribute to the failure.

You can start AI-assisted troubleshooting at two scopes:

**Troubleshoot a whole connector**
:   Use this option to investigate everything affecting a connector. The AI assistant looks at all errors and metrics for the connector
    during the selected time frame and reports back with the most impactful issues and how to address them.

    To troubleshoot a whole connector, do one of the following:

    - In the connectors list, select the troubleshoot icon next to the status on the row of an **Unhealthy** connector. In the list, the
      control is an icon only, without a text label.
    - On the connector details page, select the **Troubleshoot** button in the page header.

**Troubleshoot a specific issue**
:   Use this option to focus on a single error. The AI assistant scopes its analysis to that error and returns targeted root cause analysis
    and remediation steps.

    To troubleshoot a specific issue, navigate to the connector details page, select the **Issues** tab, locate the error
    you want to investigate, and select the **Troubleshoot** button on that error.

Note

The troubleshoot control, shown as an icon in the connectors list and as a **Troubleshoot** button elsewhere, only appears for
connectors or issues in an **Unhealthy** state.

### Viewing the connector errors

To view all errors that a connector encountered in the selected time frame, first navigate to the connector details page by
selecting [![Vertical more icon](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **View Details**, and then select the **Issues** tab.

The error headline tells you what type of error the connector encountered, and the content provides the entire stacktrace of the error.

### Viewing the connector logs

You might also want to look at additional connector logs to understand the context around an error message. To view all logs for the selected connector,
select [![Vertical more icon](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **View logs**.

After you open the log explorer, you can also change the filters to view logs for different connectors or for entire
runtimes or deployments. The log explorer supports Openflow-specific filters like the dataplane ID, the runtime key, and the process group ID.

### Accessing the Openflow canvas

When you identify a connector issue, you probably need to navigate to the Openflow canvas to fix it; for example, adjust some configuration parameters or
upgrade to a newer connector version.

To navigate to the selected connector in the Openflow canvas, select [![Vertical more icon](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **Go to canvas**.

## Optimizing performance

### Select a larger warehouse

Use the warehouse selector in the top right section of the screen to choose a different warehouse to run the queries.

Note

While larger warehouses run queries faster, they take longer to resume, which might increase the initial page load time.

### Set up clustering on the Openflow event table

By using clustering keys, you can avoid unnecessary scanning of micro-partitions during querying, significantly accelerating
the performance of queries that reference these columns. For more information, see
[What is Data Clustering?](/user-guide/tables-clustering-micropartitions#label-data-clustering).

Run the following query, replacing the placeholders with your Openflow event table:

Copy code

```
ALTER TABLE <database>.<schema>.<event_table_name>
  CLUSTER BY (
    DATE_TRUNC('HOUR', timestamp),
    RECORD_TYPE,
    CAST(record_attributes:"metricNameHash" AS STRING)
  );
```

Note

- Automatic clustering consumes Snowflake credits using serverless compute resources. To learn how many credits
  per compute-hour are consumed, refer to the “Serverless Feature Credit Table” in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- After you enable clustering on your event table, a background process starts that takes some time to complete.
  After the process is complete, you should see improved performance when using the dashboard.

### Reduce the queried time frame

Selecting a smaller time frame in the filter scans less data and leads to faster query performance.
Use the **Last Hour** filter for the best performance and the most up-to-date view of your connector health and performance.

## Limitations

- The Openflow Connectors Dashboard uses data stored in event tables to provide insight into Openflow connectors. Depending on the selected time period and event table,
  information provided on the dashboard might not reflect the current status of a connector.
- Detailed health monitoring is currently only available for Database connectors.
- The connector details page for Database connectors displays up to 75,000 tables.
- The **Deployment** and **Runtime** filters use internal names that differ from the display names in the Openflow UI.
  For details on matching these names, see [Filtering connectors](#label-openflow-dashboard-filtering).
- The **Last Ingested** column for Database connector tables shows **More than 3 days ago** when the connector hasn’t performed
  a merge query in more than 3 days, because the connector stops emitting the last-ingestion metric after that period.
  If the last ingestion timestamp falls outside the selected time frame, switch to a longer window such as **Last 24 hours**
  or **Last 7 days** to retrieve it.

## Known issues

- After upgrading the deployment, runtime, and connector to the versions mentioned in the prerequisites, the error count metric is only accurate
  for errors encountered after the upgrade.
