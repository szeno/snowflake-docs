# August 31, 2026: Second generation Openflow (*Preview*)

Second generation (gen 2) Openflow is now in public preview. Gen 2 makes Openflow
deployments, runtimes, and connectors first-class Snowflake SQL objects with standard
RBAC, SQL lifecycle management, and versioned connector configuration.

Key capabilities:

- **SQL-managed objects.** Create, modify, and remove gen 2 deployments, runtimes,
  and connectors with `CREATE`, `ALTER`, `DROP`, `SHOW`, and `DESCRIBE` commands, or
  through the Openflow UI.
- **Versioned configuration.** Gen 2 connectors store configuration as File Based
  Entities (FBEs) with committed versions. Draft changes, commit them, roll back to a
  previous version, and promote configurations across environments with Git workflows.
- **Standard RBAC.** Grant `USAGE`, `OPERATE`, and other Snowflake privileges on
  schema-scoped gen 2 objects.
- **Setup wizard.** Install and configure gen 2 connectors with a step-by-step wizard
  that validates connectivity and configuration before starting.

Supported connectors at public preview: PostgreSQL CDC, MySQL/MariaDB CDC.

Gen 2 Openflow is available on AWS and Azure. GCP support isn’t available yet.

Gen 1 Openflow resources continue to work unchanged. Gen 1 and gen 2 resources can
coexist in the same account. Migration from gen 1 to gen 2 is available separately in
Private Preview; contact your Snowflake account representative to be included.

For more information, see [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index).
