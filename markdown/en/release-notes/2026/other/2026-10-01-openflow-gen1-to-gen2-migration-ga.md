# Oct 1, 2026: Migration of gen 1 Openflow deployments and runtimes to gen 2 (*General availability*)

Migration of gen 1 Openflow deployments and runtimes to gen 2 is now generally available. From the
Openflow UI, you can convert an existing gen 1 deployment
(`OPENFLOW DATA PLANE INTEGRATION`) and all of its runtimes (`OPENFLOW RUNTIME INTEGRATION`) into
gen 2 `OPENFLOW DEPLOYMENT` and `OPENFLOW RUNTIME` objects, with standard Snowflake RBAC on the
resulting schema-scoped objects. Migration no longer requires separate account enablement.

Migrating a gen 1 **connector** to a gen 2 connector object is also available to all accounts. The
gen 2 connector you migrate to keeps its own release stage: the gen 2 PostgreSQL CDC and
MySQL/MariaDB CDC connectors are in [Public Preview](/release-notes/preview-features), so a
connector you migrate to gen 2 today runs as a preview feature. Check the **Preview** badge on the
gen 2 connector card in the **Connector library** tab before you migrate.

Gen 1 deployments that you don’t migrate continue to work unchanged. A deployment and all of its
runtimes are migrated together; you can’t leave individual runtimes as gen 1. After that
migration, gen 1 connectors keep running on the gen 2 runtime until you migrate those connectors
separately.

For more information, see [Migrate a gen 1 deployment and runtimes to gen 2](/user-guide/data-integration/openflow/gen2/migrate-deployment-runtime)
and [Migrate a gen 1 connector to gen 2](/user-guide/data-integration/openflow/gen2/migrate-connector).
