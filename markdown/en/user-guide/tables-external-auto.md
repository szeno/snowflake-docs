# Refresh external tables automatically

Event notifications for cloud storage can start refreshes of the external table metadata or add or drop file references.

Important

If you transfer ownership on an external table or its parent database by using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command,
this sets the table’s `AUTO_REFRESH` property to `FALSE`. This blocks automatic refreshes of the table metadata.
To restore automatic refreshes after you transfer ownership, set `AUTO_REFRESH = TRUE`
by using the [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) command.

**Next topics:**

- [Refresh external tables automatically for Amazon S3](/user-guide/tables-external-s3)
- [Refresh external tables automatically for Google Cloud Storage](/user-guide/tables-external-gcs)
- [Refresh external tables automatically for Azure Blob Storage](/user-guide/tables-external-azure)
