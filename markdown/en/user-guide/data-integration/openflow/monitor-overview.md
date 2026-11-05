# Monitor Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow provides the following ways to monitor your data integration pipelines:

[Monitor connectors using the Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard)
:   Use the Openflow Connectors Dashboard in Snowsight to get a high-level view of connector health, throughput,
    and data ingestion. The dashboard provides filtering, error distribution, and per-connector detail pages.

[Set up alerts for Openflow](/user-guide/data-integration/openflow/alerts)
:   Create alerts from templates to be notified about replication issues. Predefined templates cover connector-specific
    failure modes and generic issues such as errors, back pressure, and resource utilization.

[Openflow telemetry](/user-guide/data-integration/openflow/monitor)
:   Query the logs and metrics that Openflow writes to your event table, such as connector throughput, back pressure,
    errors, resource usage, and connector-specific metrics, and build custom queries tailored to your environment.
