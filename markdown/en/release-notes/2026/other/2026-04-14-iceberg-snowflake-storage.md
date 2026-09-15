# Apr 14, 2026: Snowflake storage for Apache Iceberg™ tables (*Preview*)

With this preview release, you can create Apache Iceberg™ tables that use Snowflake storage.
This option lets Snowflake store and manage the Iceberg table files for you, so you don’t
need to set up access to external cloud storage.

Just like standard Snowflake tables, Iceberg tables with Snowflake storage support Fail-safe
data protection for permanent tables and can be transient to reduce storage costs. You can also
use an external query engine through the Snowflake Horizon Catalog to access these tables.

For more information, see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).
