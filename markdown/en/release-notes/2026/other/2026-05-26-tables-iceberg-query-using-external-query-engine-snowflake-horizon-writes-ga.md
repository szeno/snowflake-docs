# May 26, 2026: Apache Iceberg™ tables: Write support by using an external query engine (*General availability*)

With this release, write support for Snowflake-managed Apache Iceberg™ tables by using an external query engine through Snowflake Horizon
Catalog is now generally available. You can read and write to Snowflake-managed Iceberg v2 and v3 tables from any external query engine
that supports the open Iceberg REST protocol, such as Apache Spark™, by using a single Horizon Catalog endpoint and your existing
Snowflake users, roles, policies, and authentication.

This release also adds Workload Identity Federation (WIF) with OpenID Connect (OIDC) as an authentication option for connecting an
external query engine to Iceberg tables through Horizon Catalog.

For more information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
