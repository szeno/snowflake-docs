# Nov 1, 2026: Apache Iceberg™ tables: Read and write across Snowflake accounts with Snowflake Horizon Catalog, now without managing secrets (*General availability*)

With this release, you can read and write Apache Iceberg™ tables managed by another Snowflake account without creating, storing, or rotating
secrets. This capability is generally available through catalog integrations for Snowflake Horizon Catalog. The accounts access the same
table data without copying it.

With this feature, you can do the following:

- Read and write tables across accounts, including accounts in different regions, while the provider account retains ownership of the tables.
- Create individual Iceberg tables or a catalog-linked database that connects to the tables in another account.
- Use vended credentials from Horizon Catalog, the recommended option, so you don’t need to configure an external volume.
- Restrict ID tokens to one account with a custom audience.
- Connect over private connectivity.

Snowflake handles authentication through workload identity federation, using short-lived identities and access tokens that refresh
automatically.

This feature is available in all commercial regions.

For more information, see [Access Apache Iceberg™ tables in another Snowflake account](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon).
