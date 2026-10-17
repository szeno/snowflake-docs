# October 16, 2026: Apache Iceberg™ v3 table upgrades and expression defaults (*General availability*)

The following Apache Iceberg™ v3 features are now generally available.

## Upgrade tables from Iceberg v2 to v3

You can upgrade an existing Apache Iceberg™ table from Iceberg v2 to v3 in place by using
[ALTER ICEBERG TABLE … UPGRADE TO ICEBERG VERSION 3](/sql-reference/sql/alter-iceberg-table). The upgraded table keeps its
name, privileges, and downstream references, so you don’t need to recreate the table to use Iceberg v3 features such as
default values, row lineage, deletion vectors, and v3 data types.

Upgrades are supported for Snowflake-managed tables and for externally managed tables with `CATALOG_SOURCE = ICEBERG_REST`,
including tables in catalog-linked databases. Upgrading to v3 is permanent, but for Snowflake-managed tables you can restore the pre-upgrade v2 table by using
Time Travel within the retention period.

For more information, see [Upgrade an Apache Iceberg™ table from version 2 to version 3](/user-guide/tables-iceberg-upgrade-version).

## Expression defaults for Snowflake-managed Iceberg v3 tables

Snowflake-managed Iceberg v3 tables now support SQL expressions, sequences, and identity columns as column defaults, matching
the behavior of v2 tables. Snowflake writes expressions that it can evaluate to a constant, such as `PI()`, to Iceberg metadata.
Other defaults, such as `CURRENT_DATE()`, sequences, and identity columns, are evaluated only for Snowflake writes and require
the new [ALLOW\_V3\_EXPRESSION\_DEFAULTS](/sql-reference/parameters#label-allow-v3-expression-defaults) parameter.

When you upgrade a v2 table that has expression defaults, Snowflake enables the parameter on the table automatically.

For more information, see [Use default values with Apache Iceberg™ tables](/user-guide/tables-iceberg-default-values).
