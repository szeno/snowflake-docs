# October 21, 2026: Declarative Feature Store (*General availability*)

The Declarative Feature Store workflow is now generally available. Define your
feature store resources (entities, data sources, feature views, and feature groups) as
version-controlled YAML or Python specs, then preview and deploy them with the
`snow feature` CLI using a plan-and-apply workflow.

Documentation in the developer guide covers the following topics:

- [Declarative feature store overview](/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle)
  for the end-to-end plan-and-apply workflow.
- [Declarative project configuration](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-projects)
  for project layout, deployment targets, and templating.
- [Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring)
  for authoring each object kind in YAML or Python.
- [Declarative API (snow feature CLI) references](/developer-guide/snowflake-ml/feature-store/feature-store-cli-reference)
  for shared flags, per-command flags, and exit statuses.
- [Migrating to declarative](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-migration)
  for pulling an imperatively registered feature store into declarative specs with
  `snow feature sync`.
