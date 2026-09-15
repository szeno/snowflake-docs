# Configure a catalog integration for Apache Iceberg™ REST catalogs

An Apache Iceberg™ REST [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) lets Snowflake access
[Apache Iceberg™ tables](/user-guide/tables-iceberg) managed in a remote catalog that complies with the
open-source [Apache Iceberg REST OpenAPI specification](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml).

Snowflake supports the following additional features when you use an Iceberg REST catalog integration:

- [Catalog-linked databases and automatic table discovery](/user-guide/tables-iceberg-catalog-linked-database)
- [Write support for externally managed Iceberg tables](/user-guide/tables-iceberg-externally-managed-writes)

## Authentication methods

Snowflake supports the following authentication methods for Iceberg REST catalogs:

- OAuth
- Bearer token or personal access token (PAT)
- Signature Version 4 (SigV4)

Supported authentication methods vary by [catalog source](#label-tables-iceberg-configure-catalog-integration-sources).

### Credential rotation

To rotate the credentials for a catalog integration, you can use the [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration)
command to update the credentials that Snowflake uses to authenticate with your remote catalog.

For example:

Copy code

```
ALTER CATALOG INTEGRATION my_cat_int SET
  REST_AUTHENTICATION (
    OAUTH_CLIENT_SECRET = 'myNewSecret'
  );
```

## Connection options

This section describes the connection options for Iceberg REST catalogs.

### Vended credentials

In addition to [External volumes](/user-guide/tables-iceberg-configure-external-volume),
Snowflake supports the following connection options for Iceberg REST catalogs:

- [Vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)

Supported connection options vary by [catalog source](#label-tables-iceberg-configure-catalog-integration-sources).

### Private connectivity

Snowflake supports connecting to Iceberg REST catalogs through [private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).

When you use [vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials), you can configure
[private connectivity to storage](/user-guide/tables-iceberg-vended-credentials-private-connectivity) so Snowflake accesses your cloud storage through a private endpoint.

When you use an [external volume](/user-guide/tables-iceberg-configure-external-volume) instead of vended credentials, configure outbound private connectivity on the external volume.

Supported connection options vary by [catalog source](#label-tables-iceberg-configure-catalog-integration-sources).

## Catalog sources

Snowflake supports any external catalog server that complies with the Iceberg REST specification.

The following topics provide examples for commonly used REST catalogs:

- [Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog). These instructions also apply to
  Apache Polaris™.
- [AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue)
- [Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables)
- [Amazon API Gateway](/user-guide/tables-iceberg-configure-catalog-integration-rest-api-gateway)
- [Tabular](/user-guide/tables-iceberg-configure-catalog-integration-rest-tabular)
- [Unity Catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest-unity)
- [OneLake](/user-guide/tables-iceberg-configure-catalog-integration-rest-onelake)
- [Google Cloud BigLake Metastore](/user-guide/tables-iceberg-configure-catalog-integration-rest-biglake)

## Browsing a remote catalog

After you create a catalog integration for Iceberg REST, you can use the following
Snowflake system functions to browse namespaces and tables in the catalog:

- [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog)
- [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog)

## Migrate a table to an Iceberg REST catalog integration

After you create a catalog integration for Iceberg REST, if needed, you can
replace the catalog integration associated with an externally managed Iceberg table in a standard Snowflake database with the catalog
integration you created. For instructions, see [SYSTEM$SET\_CATALOG\_INTEGRATION](/sql-reference/functions/system_set_catalog_integration).

## Create a catalog-linked database

After you create a catalog integration for Iceberg REST, you can create a catalog-linked database to bring the data from your remote Iceberg REST catalog into Snowflake.
When you create the catalog-linked database, specify the name of the catalog integration you created as the catalog.

A catalog-linked database automatically discovers
and stays in sync with the namespaces and tables in your remote catalog. You can use a catalog-linked database to read and
write to the tables in your remote catalog from Snowflake, while preserving full interoperability with your existing
Iceberg ecosystem. For more information, see the following topics:

- [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
- If your external data is in Unity Catalog, see [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog)
- If your external data is in AWS Glue, see [Build Data Lakes using Apache Iceberg with Snowflake and AWS Glue](https://www.snowflake.com/en/developers/guides/data-lake-using-apache-iceberg-with-snowflake-and-aws-glue/)
