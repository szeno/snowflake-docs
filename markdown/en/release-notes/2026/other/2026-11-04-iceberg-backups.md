# Nov 4, 2026: Backups for Snowflake Storage for Apache Iceberg™ tables (*General availability*)

With this release, we’re pleased to announce the general availability of backups for Snowflake Storage
for Apache Iceberg™ tables and dynamic Apache Iceberg™ tables that use Snowflake Storage on
Amazon Web Services (AWS).

You can now:

- Create backup sets for Snowflake Storage for Apache Iceberg™ tables with
  [`CREATE BACKUP SET ... FOR ICEBERG TABLE`](/sql-reference/sql/create-backup-set).
- Create backup sets for dynamic Apache Iceberg™ tables that use Snowflake Storage with
  [`CREATE BACKUP SET ... FOR DYNAMIC ICEBERG TABLE`](/sql-reference/sql/create-backup-set).
- Restore Snowflake Storage for Apache Iceberg™ tables with
  [`CREATE ICEBERG TABLE ... FROM BACKUP SET`](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-from-backup-set-syntax).
- Restore dynamic Apache Iceberg™ tables that use Snowflake Storage with
  [`CREATE DYNAMIC ICEBERG TABLE ... FROM BACKUP SET`](/sql-reference/sql/create-dynamic-table#label-create-dit-backup-syntax).
- Include eligible Snowflake Storage for Apache Iceberg™ tables and dynamic
  Apache Iceberg™ tables that use Snowflake Storage in schema and database backups.

For more information, see [Backups for disaster recovery and immutable storage](/user-guide/backups).
