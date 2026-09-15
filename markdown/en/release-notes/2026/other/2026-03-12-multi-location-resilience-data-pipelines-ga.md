# Mar 12, 2026: Multi-Location Resilience for Data Pipelines (General availability)

Multi-location resilience for data pipelines helps you safeguard your data
pipelines against potential region-wide cloud provider outages. It ensures that,
upon failing over to a secondary location, file-based data ingestion
(specifically Snowpipe and COPY INTO) resumes processing new data without
interruption.

Key use cases include the following:

- **Business continuity and disaster recovery:** Maintain uninterrupted data
  flows and ensure critical dashboards and machine learning models are fed with
  fresh data during region-wide cloud provider outages.
- **Regulatory compliance:** Satisfy regulatory mandates that require
  multi-region resilience without building complex, custom infrastructure.
- **Cross-cloud flexibility:** Fail over data ingestion pipelines across cloud
  providers, eliminating single-vendor infrastructure lock-in for your disaster
  recovery architecture.
- **Zero-engineering overhead:** Get exactly-once ingestion semantics upon
  failover or failback without requiring manual reconciliation or custom
  deduplication scripts.

You can enable this feature by configuring a Multi-Location Storage Integration
(MLSI) and a Multi-Queue Notification Integration (MQNI) to transition your
active storage and message queues during failover, combined with routing your
files through a dual-write architecture.

For more information, see [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines).
