# Sep 08, 2026: Second generation Openflow deployments and runtimes (*General availability*)

Second generation (gen 2) Openflow **deployment** and **runtime** SQL objects are now generally
available on AWS and Azure. Create, modify, and remove gen 2 deployments and runtimes with
`CREATE`, `ALTER`, `DROP`, `SHOW`, and `DESCRIBE` commands, or through the Openflow UI, with
standard Snowflake RBAC on schema-scoped objects.

Gen 2 **connector** configuration — the setup wizard, SQL/stage-based configuration, and
supported connectors (PostgreSQL CDC, MySQL/MariaDB CDC) — remains in
[Public Preview](/release-notes/preview-features).

GCP support isn’t available yet.

Gen 1 Openflow resources continue to work unchanged. Gen 1 and gen 2 resources can coexist in the
same account. Migration from gen 1 to gen 2 is available separately in Private Preview; contact
your Snowflake account representative to be included.

For more information, see [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index).
