# October 18, 2024 —Apache Iceberg™ tables: Support for Snowflake Open Catalog — *General Availability*

With this release, Snowflake is pleased to announce the general availability of support for integrating Apache Iceberg™ tables in Snowflake
with Snowflake Open Catalog, which was previously named Polaris Catalog. With general availability, we’ve made the following updates:

- When syncing a Snowflake-managed table with Snowflake Open Catalog, Snowflake performs validation when you attempt to create the following objects:

  - A catalog integration
  - An Iceberg table that you’re syncing to Open Catalog

  This validation checks whether the configuration for the catalog integration or table will successfully sync the Iceberg table to
  Open Catalog.
- When you modify the properties for an existing Apache Iceberg™ table by specifying the name of a catalog integration for Open Catalog,
  validation now checks whether the configuration for the table will successfully sync the Iceberg table to Open Catalog.

For more information about the updates available with Snowflake Open Catalog general availability in Open Catalog, see the
[Snowflake Open Catalog release notes](https://other-docs.snowflake.com/en/opencatalog/release-notes)
