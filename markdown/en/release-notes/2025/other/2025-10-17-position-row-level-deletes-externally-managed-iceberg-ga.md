# Oct 17, 2025: Positional deletes for externally managed Apache Iceberg™ tables (*General availability*)

Snowflake support for positional delete files on externally managed Apache Iceberg™ tables is now generally available and is no longer in
[Preview](/release-notes/preview-features). Snowflake can read and write positional deletes for these tables.

Key capabilities:

- Query externally managed Iceberg tables that use positional delete files for row-level deletes.
- Write positional delete files when Snowflake runs UPDATE, DELETE, and MERGE operations on externally managed tables stored on Amazon S3,
  Azure, or Google Cloud.

For more information, see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes) and [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes).
