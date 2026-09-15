# Query a table in Snowflake Open Catalog using Snowflake

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

To query a table registered in [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) using Snowflake,
you can create an [externally managed](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration) Apache Iceberg™ table and a catalog integration.

The table represents the Iceberg table in Snowflake Open Catalog and provides read-only access.

Note

This topic covers how to create a single externally managed Iceberg table. Alternatively,
use a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) to automatically discover multiple tables in Open Catalog.

## Prerequisites

Before you start, you need the following:

- An Iceberg table registered with Open Catalog.
- A service connection that Snowflake can use to connect to Open Catalog.
  You can use an existing service connection that you’ve set up roles and privileges for,
  or [Configure a service connection](https://other-docs.snowflake.com/en/opencatalog/configure-service-connection#configure-a-service-connection) for Snowflake. If you configure a new service connection, you must also configure access control for it.

## Step 1: Create an external volume in Snowflake

If you don’t have one already, start by creating an external volume in Snowflake that provides access to the
cloud storage location where you store your table data and metadata.

Complete the instructions for your cloud storage service:

- [Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3)
- [Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
- [Azure Storage](/user-guide/tables-iceberg-configure-external-volume-azure)

## Step 2: Create a catalog integration for Open Catalog

Next, use the [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration-open-catalog) command to
create a catalog integration in Snowflake that uses OAuth to connect to Open Catalog using your service connection credentials. The
CATALOG\_NAMESPACE parameter is optional. However, if you don’t specify it with the catalog integration, you must specify it when you create
an externally managed table. This section includes the following examples:

- If you don’t use private connectivity for inbound network traffic in Open Catalog, see the
  [example Snowflake catalog integration that uses the public internet](#label-example-catalog-integration-public-internet).
- If you use [private connectivity for inbound network traffic in Open Catalog](https://other-docs.snowflake.com/en/opencatalog/private-connectivity-inbound),
  see the [example Snowflake catalog integration that uses a private IP address](#label-example-catalog-integration-private-ip-address).

### Example: Catalog integration that uses the public internet

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE= 'myOpenCatalogNamespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = 'myOpenCatalogName'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = 'my-client-id'
    OAUTH_CLIENT_SECRET = 'my-client-secret'
    OAUTH_ALLOWED_SCOPES = ( 'PRINCIPAL_ROLE:ALL' )
  )
  ENABLED = TRUE;
```

Note

- To find your Snowflake organization name (`orgname`), follow the steps in [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find `<my-snowflake-open-catalog-account-name`,
  see [Find the account name for a Snowflake Open Catalog account](https://other-docs.snowflake.com/en/opencatalog/find-account-name) in
  the Snowflake Open Catalog documentation.

### Example: Catalog integration that uses a private IP address

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE= 'myOpenCatalogNamespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://<open_catalog_privatelink_account_url>/polaris/api/catalog'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = 'myOpenCatalogName'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = 'my-client-id'
    OAUTH_CLIENT_SECRET = 'my-client-secret'
    OAUTH_ALLOWED_SCOPES = ( 'PRINCIPAL_ROLE:ALL' )
  )
  ENABLED = TRUE;
```

Note

For `open_catalog_privatelink_account_url`, enter one of the following values:

- **PrivateLink Account URL**
- **Regionless PrivateLink Account URL**

To obtain these values, retrieve your Open Catalog account settings for private connectivity. For details, see the instructions for the
cloud platform where your Open Catalog account is hosted:

- [AWS](http://docs.snowflake.com/user-guide/opencatalog/private-connectivity-inbound-configure-aws#step-3-retrieve-your-open-catalog-account-settings)
- [Azure](http://docs.snowflake.com/user-guide/opencatalog/private-connectivity-inbound-configure-azure#step-1-retrieve-your-open-catalog-account-settings)

## Step 3: Create an externally managed table

Create an Iceberg table in Snowflake using the external volume and catalog integration that you previously configured.

For CATALOG\_TABLE\_NAME, specify the table name as it appears in Open Catalog.

Copy code

```
CREATE ICEBERG TABLE open_catalog_iceberg_table
  CATALOG = 'open_catalog_int'
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG_TABLE_NAME = 'my_iceberg_table';
```

You can optionally enable automated refreshes of the table metadata by specifying `AUTO_REFRESH = TRUE`.
For more information, see [Automatically refresh Apache Iceberg™ tables](/user-guide/tables-iceberg-auto-refresh). If you didn’t specify a CATALOG\_NAMESPACE with the catalog integration
you created in the previous step, you must specify this parameter to set a catalog namespace for the table.

Note

To retrieve a list of tables or namespaces in your remote catalog, you can use the following functions:

- [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog)
- [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog)
- [SYSTEM$EXECUTE\_CATALOG\_OPERATION](/sql-reference/functions/system_execute_catalog_operation)

## Step 4: Query the table using Snowflake

You can now use Snowflake to query the table in Open Catalog. You can also join the query results with other Snowflake tables.

Copy code

```
SELECT id, date
  FROM open_catalog_iceberg_table
  LIMIT 10;
```
