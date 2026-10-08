# Oct 7, 2026: Zero-copy integration for Workday Data Cloud (*General availability*)

The zero-copy integration between Workday Data Cloud and Snowflake is now generally available. You can query Workday Data
Cloud tables directly from your existing Snowflake account, without ETL pipelines, data replication, or moving data out of
Workday.

You create a Zerocopy Connector that authenticates outbound to your Workday tenant, then mount the Workday Data Cloud
catalog as a catalog-linked database. Each Workday namespace becomes a schema and each Workday table becomes a table.
Snowflake contacts Workday on each `SELECT`, so queries return fresh data rather than a cached copy, and Workday remains
the system of record.

For more information, see:

- [About Workday Data Cloud and Snowflake](/user-guide/data-integration/zero-copy/about-workday-datacloud)
- [Set up the Workday Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/workday-data-cloud/setup)
- [Workday Data Cloud Zerocopy Connector: Security and privileges](/user-guide/data-integration/zero-copy/workday-data-cloud/security)
- [Explore and query Workday Data Cloud data](/user-guide/data-integration/zero-copy/workday-data-cloud/explore-data)
