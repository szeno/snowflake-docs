# Aug 10, 2026: Amazon S3 Tables Iceberg REST catalog integration (*General availability*)

Snowflake can now connect directly to the Amazon S3 Tables Iceberg REST endpoint, so you don’t need
to create an AWS Glue integration. This capability is now generally available. You can use an
Apache Iceberg™ REST catalog integration with Signature Version 4 (SigV4) authentication, then create a
catalog-linked database to discover and query S3 Tables from Snowflake. You can also configure
outbound private connectivity so Snowflake accesses the S3 Tables catalog and storage through
private endpoints.

For more information, see [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).
