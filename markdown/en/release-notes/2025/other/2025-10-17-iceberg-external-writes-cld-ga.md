# Oct 17, 2025: Write support for externally managed Apache Iceberg™ tables and catalog-linked databases (*General availability*)

The following Apache Iceberg™ table features are now generally available and are no longer in
[Preview](/release-notes/preview-features):

- Write operations for externally managed Iceberg tables.
- Catalog-linked databases that connect to external Iceberg REST catalogs.

Key capabilities:

- Create new Iceberg tables directly in your remote catalog using Snowflake.
- Perform full DML operations — for example, INSERT, UPDATE, DELETE, MERGE — on externally managed tables.
- Create a Snowflake database that’s linked to your remote Iceberg REST catalog; for example, AWS Glue, Snowflake Open Catalog, and others.
- Modify the properties of a catalog-linked database, including suspending or resuming automatic table discovery.
- Discover and access multiple remote Iceberg tables without individually defining them in Snowflake.
- Use vended credentials with external writes.

  Note

  CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT isn’t supported with vended credentials.

For more information, see the following topics:

- [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
- [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
- [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked)

Note

Update: Billing for catalog-linked databases started on December 15, 2025.
