# Configure a catalog integration for Delta Sharing

Use the [CREATE CATALOG INTEGRATION (Delta Sharing)](/sql-reference/sql/create-catalog-integration-delta-sharing) command to create a catalog integration
that uses the [Delta Sharing](https://delta.io/sharing/) protocol to read Delta tables from a remote Delta Sharing server.
After you create the catalog integration, you can create a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
to query the shared Delta tables from Snowflake.

Note

To configure a catalog integration that uses the Apache Iceberg™ REST protocol to connect to Databricks Unity Catalog,
see [Configure a catalog integration for Unity Catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest-unity) instead.

You can configure a Delta Sharing catalog integration that uses any of the following authentication methods:

- [Configure a catalog integration with bearer-token authentication](#label-tables-iceberg-configure-catalog-integration-delta-sharing-bearer): the provider issues a long-lived bearer token
  to the recipient, and Snowflake uses that token to authenticate.
- [Configure a catalog integration with OIDC authentication](#label-tables-iceberg-configure-catalog-integration-delta-sharing-oidc): Snowflake authenticates to the Delta Sharing
  server by using [OpenID Connect](https://openid.net/connect/) federation, exchanging short-lived JWT tokens. OIDC avoids the
  need to share or rotate long-lived bearer tokens.
- [Configure a catalog integration with OAuth authentication](#label-tables-iceberg-configure-catalog-integration-delta-sharing-oauth): Snowflake exchanges an OAuth2 client ID and
  secret with a token endpoint for an access token, then uses that token to authenticate to the Delta Sharing server.

## Considerations

Consider the following when you use a Delta Sharing catalog integration:

- **Tables are read-only in Snowflake.** A catalog-linked database that uses a Delta Sharing catalog integration supports only
  read operations. You can’t insert into, update, or create tables in the catalog-linked database from Snowflake.
- **Table format must be Delta.** A Delta Sharing catalog integration supports only Delta tables (`TABLE_FORMAT = DELTA`).
- **Table data access requires vended credentials or an external volume.** By default, Snowflake uses vended credentials
  returned by the Delta Sharing server to access the underlying table data in cloud storage. If the Delta Sharing server
  doesn’t support vended credentials, you can configure an external volume that grants Snowflake direct access to the
  storage instead. See [Use an external volume when the provider doesn’t support credential vending](#label-tables-iceberg-configure-catalog-integration-delta-sharing-external-volume).

## Prerequisites

Before you begin, make sure that you have:

- A Snowflake account where you can create a catalog integration. You must use the ACCOUNTADMIN role, or a role that has the
  CREATE INTEGRATION privilege on the account.
- Access to a Delta Sharing server (the provider) that has:

  - A *share* configured for an open recipient.
  - The recipient configured for bearer-token, OIDC federation, or OAuth client-credentials authentication.

  For Databricks Unity Catalog, see [Delta Sharing](https://docs.databricks.com/aws/en/delta-sharing/) in the Databricks
  documentation for instructions on enabling Delta Sharing, creating a share, and creating a recipient.

## Configure a catalog integration with bearer-token authentication

With bearer-token authentication, the Delta Sharing provider issues a long-lived bearer token to the recipient. Snowflake uses
that token to authenticate to the Delta Sharing server.

### About the recipient credential file

The Delta share credential file is a JSON file from the Delta Sharing provider that contains
the endpoint URL and the bearer token Snowflake uses to authenticate. The file contains content like the following:

Copy code

```
{
  "shareCredentialsVersion": 1,
  "bearerToken": "...",
  "endpoint": "https://<delta-sharing-server>/api/2.0/delta-sharing/metastores/<metastore-id>",
  "expirationTime": "2027-03-25T20:08:11.118Z"
}
```

When you create the catalog integration, you specify the `endpoint` and `bearerToken` values from this file.

Important

The bearer token grants access to the share. Treat it like a password and don’t commit it to source control.

### Create the catalog integration

Use the [CREATE CATALOG INTEGRATION (Delta Sharing)](/sql-reference/sql/create-catalog-integration-delta-sharing) command to create a Delta Sharing catalog integration
in Snowflake. Use the `endpoint` and `bearerToken` values from the recipient credential file.

The following example creates a Delta Sharing catalog integration with bearer-token authentication:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<endpoint_from_credential>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = BEARER
    BEARER_TOKEN = '<bearer_token_from_credential>'
  )
  ENABLED = TRUE;
```

Where:

- `CATALOG_URI` is the `endpoint` value from the recipient credential file.
- `CATALOG_NAME` is `shares/` followed by the name of the Delta Sharing share. For example, if your share is named
  `sales_share`, specify `CATALOG_NAME = 'shares/sales_share'`. You can also specify just the share name without the
  `shares/` prefix, for example `CATALOG_NAME = 'sales_share'`.
- `BEARER_TOKEN` is the `bearerToken` value from the recipient credential file.

After you create the catalog integration, verify it by following [Verify the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-verify).

## Configure a catalog integration with OIDC authentication

With OIDC authentication, Snowflake authenticates to the Delta Sharing server by using
[OpenID Connect](https://openid.net/connect/) federation. Snowflake acts as the workload identity provider, and the Delta
Sharing server validates the short-lived JWT tokens that Snowflake presents.

OIDC authentication avoids sharing or rotating long-lived bearer tokens. Setup requires a handshake: you create the catalog
integration in Snowflake, retrieve the workload identity values, and then provide those values to the Delta Sharing provider
to configure the OIDC recipient policy.

Note

For Databricks Unity Catalog, see
[Read shared data using Open ID Connect (OIDC) token federation in an M2M flow](https://docs.databricks.com/aws/en/delta-sharing/sharing-over-oidc-m2m)
in the Databricks documentation for the provider-side steps to enable OIDC federation and configure the recipient policy.

### Step 1: Create the catalog integration

Use the [CREATE CATALOG INTEGRATION (Delta Sharing)](/sql-reference/sql/create-catalog-integration-delta-sharing) command to create a Delta Sharing catalog integration
that uses OIDC authentication. Specify `TYPE = OIDC` and provide the `OIDC_AUDIENCE` value that the Delta Sharing provider’s
recipient policy expects.

The following example creates a Delta Sharing catalog integration with OIDC authentication:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int_oidc
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<recipient_endpoint>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OIDC
    OIDC_AUDIENCE = '<audience>'
  )
  ENABLED = TRUE;
```

Where:

- `CATALOG_URI` is the endpoint URL for the Delta Sharing recipient that the provider gave you.
- `CATALOG_NAME` is `shares/` followed by the name of the Delta Sharing share. You can also specify just the share name
  without the `shares/` prefix.
- `OIDC_AUDIENCE` is the audience value that the Delta Sharing server’s OIDC recipient policy expects.

### Step 2: Retrieve the workload identity values

After you create the catalog integration, run [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) to retrieve the workload identity
issuer and subject values that Snowflake uses to identify itself to the Delta Sharing provider:

Copy code

```
DESC CATALOG INTEGRATION my_delta_sharing_int_oidc;
```

In the output, note the values for the following properties:

- `WORKLOAD_IDENTITY_FEDERATION_ISSUER`
- `WORKLOAD_IDENTITY_FEDERATION_SUBJECT`

You provide these values to the Delta Sharing provider in the next step.

[![Snowsight output of DESC CATALOG INTEGRATION showing the WORKLOAD_IDENTITY_FEDERATION_ISSUER and WORKLOAD_IDENTITY_FEDERATION_SUBJECT values.](/static/images/iceberg/delta-sharing/oidc-desc-output.png)](/static/images/iceberg/delta-sharing/oidc-desc-output.png)

### Step 3: Configure the OIDC recipient policy on the provider

On the Delta Sharing provider, configure the OIDC recipient policy with the `issuer` and `subject` values that you retrieved
in the previous step, plus the `audience` value that you specified for `OIDC_AUDIENCE` when you created the catalog
integration. All three values must match exactly.

For Databricks Unity Catalog, see
[Read shared data using Open ID Connect (OIDC) token federation in an M2M flow](https://docs.databricks.com/aws/en/delta-sharing/sharing-over-oidc-m2m)
in the Databricks documentation for the provider-side configuration steps.

### Step 4: Verify the catalog integration

After the provider’s OIDC recipient policy is configured, verify the catalog integration by following
[Verify the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-verify).

## Configure a catalog integration with OAuth authentication

With OAuth client-credentials authentication, Snowflake exchanges a long-lived OAuth2 client ID and secret with the
identity provider’s token endpoint for a short-lived access token, then uses that access token to authenticate to the
Delta Sharing server. The Delta Sharing provider configures the recipient policy to trust tokens issued by the identity
provider.

### Step 1: Gather the OAuth credentials from the provider

From the Delta Sharing provider, obtain:

- The OAuth2 **client ID** and **client secret** that the provider issued for your recipient.
- The **token endpoint URL** of the identity provider that issues access tokens for the Delta Sharing server.
- The Delta Sharing **endpoint URL** and **share name**.

Important

Treat the OAuth client secret like a password and don’t commit it to source control.

### Step 2: Create the catalog integration

Use the [CREATE CATALOG INTEGRATION (Delta Sharing)](/sql-reference/sql/create-catalog-integration-delta-sharing) command to create a Delta Sharing catalog
integration that uses OAuth authentication. Specify `TYPE = OAUTH` and provide the client ID, client secret, and token
endpoint URL.

The following example creates a Delta Sharing catalog integration with OAuth authentication:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int_oauth
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<recipient_endpoint>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
    OAUTH_TOKEN_URI = 'https://<token_server_uri>'
  )
  ENABLED = TRUE;
```

Where:

- `CATALOG_URI` is the endpoint URL for the Delta Sharing recipient that the provider gave you.
- `CATALOG_NAME` is `shares/` followed by the name of the Delta Sharing share. You can also specify just the share name
  without the `shares/` prefix.
- `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` are the OAuth2 credentials issued by the provider’s identity provider.
- `OAUTH_TOKEN_URI` is the token endpoint URL of the identity provider.

### Step 3: Verify the catalog integration

Verify the catalog integration by following [Verify the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-verify).

## Verify the catalog integration

Verify that Snowflake can connect to the Delta Sharing server. Substitute the name of your catalog integration in the
following examples.

1. Verify the catalog integration configuration by calling the SYSTEM$VERIFY\_CATALOG\_INTEGRATION function:

   Copy code

   ```
   SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('my_delta_sharing_int');
   ```

   [![Snowsight output showing a successful SYSTEM$VERIFY_CATALOG_INTEGRATION call.](/static/images/iceberg/delta-sharing/catalog-integration-01.png)](/static/images/iceberg/delta-sharing/catalog-integration-01.png)
2. List the namespaces (schemas) in the share by calling the SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG function:

   Copy code

   ```
   SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('my_delta_sharing_int');
   ```

   [![Snowsight output showing the schemas returned by SYSTEM$LIST_NAMESPACES_FROM_CATALOG.](/static/images/iceberg/delta-sharing/catalog-integration-02.png)](/static/images/iceberg/delta-sharing/catalog-integration-02.png)
3. List the tables in a schema by calling the SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG function:

   Copy code

   ```
   SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG(
     'my_delta_sharing_int',
     '<schema_name_in_share>'
   );
   ```

   [![Snowsight output showing the Delta tables returned by SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG.](/static/images/iceberg/delta-sharing/catalog-integration-03.png)](/static/images/iceberg/delta-sharing/catalog-integration-03.png)

## Create a catalog-linked database

After you verify the catalog integration, create a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
that surfaces the Delta tables from the share as queryable tables in Snowflake.

The following example creates a read-only catalog-linked database named `delta_sharing_cld`:

Copy code

```
CREATE OR REPLACE DATABASE delta_sharing_cld
  LINKED_CATALOG = (
    CATALOG = my_delta_sharing_int
    ALLOWED_WRITE_OPERATIONS = 'NONE'
    SYNC_INTERVAL_SECONDS = 30
  );
```

Where:

- `CATALOG` is the name of the catalog integration that you created in
  [Create the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-create-integration),
  [Step 1: Create the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-create-integration-oidc),
  or [Step 2: Create the catalog integration](#label-tables-iceberg-configure-catalog-integration-delta-sharing-create-integration-oauth).
- `ALLOWED_WRITE_OPERATIONS = 'NONE'` makes the database read-only. Write operations against Delta tables shared through
  Delta Sharing aren’t supported.
- `SYNC_INTERVAL_SECONDS` controls how often Snowflake syncs the catalog-linked database with the remote share. Adjust this
  value based on how frequently the tables in the share change.

For more information about catalog-linked databases, including additional parameters, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
and [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked).

## Use an external volume when the provider doesn’t support credential vending

By default, a Delta Sharing catalog integration uses vended credentials (`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`) to
access the shared table data in cloud storage. Some Delta Sharing servers don’t support credential vending. For example,
servers that implement version 1 of the Delta Sharing protocol don’t provide the `/temporary-table-credentials` endpoint.
Against those servers, credential vending fails and the shared tables remain uninitialized placeholders that you can’t query.

In that case, you can grant Snowflake direct access to the underlying cloud storage with an
[external volume](/user-guide/tables-iceberg-configure-external-volume) instead.

1. Create the catalog integration **without** `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`. The following example uses OAuth
   authentication, but you can use any of the supported authentication methods:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int_ext_vol
     CATALOG_SOURCE = DELTA_SHARING
     TABLE_FORMAT = DELTA
     REST_CONFIG = (
       CATALOG_URI = '<recipient_endpoint>'
       CATALOG_NAME = 'shares/<share_name>'
     )
     REST_AUTHENTICATION = (
       TYPE = OAUTH
       OAUTH_CLIENT_ID = '<oauth_client_id>'
       OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
       OAUTH_TOKEN_URI = 'https://<token_server_uri>'
     )
     ENABLED = TRUE;
   ```
2. Configure an external volume that grants Snowflake access to the cloud storage that backs the shared tables. For
   instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume). Because Delta Sharing tables are read-only in
   Snowflake, the external volume doesn’t need write access, so you can set `ALLOW_WRITES = FALSE`.

   The following example creates an external volume for Amazon S3:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL VOLUME iceberg_external_volume
     STORAGE_LOCATIONS = (
       (
         NAME = 'my-s3-us-west-2'
         STORAGE_PROVIDER = 'S3'
         STORAGE_BASE_URL = 's3://<my_bucket>/'
         STORAGE_AWS_ROLE_ARN = '<arn:aws:iam::123456789012:role/myrole>'
         STORAGE_AWS_EXTERNAL_ID = 'external_id'
       )
     )
     ALLOW_WRITES = FALSE;
   ```

   Set `STORAGE_BASE_URL` to the cloud storage location that backs the shared tables. If you don’t know this location, the
   provider can supply it, or you can retrieve it from the base location that the Delta Sharing server returns for the share.
3. Specify the external volume with the `EXTERNAL_VOLUME` parameter when you create the catalog-linked database:

   Copy code

   ```
   CREATE OR REPLACE DATABASE delta_sharing_cld
     LINKED_CATALOG = (
       CATALOG = my_delta_sharing_int_ext_vol
       ALLOWED_WRITE_OPERATIONS = 'NONE'
       SYNC_INTERVAL_SECONDS = 30
     )
     EXTERNAL_VOLUME = 'iceberg_external_volume';
   ```

With this configuration, Snowflake uses the external volume to read the shared table data directly from cloud storage and
doesn’t call the Delta Sharing server’s credential-vending endpoint.

## Query Delta tables

After Snowflake syncs the catalog-linked database, you can query the shared Delta tables like any other table in Snowflake.

For example:

Copy code

```
SELECT *
  FROM delta_sharing_cld.<schema_name>.<table_name>;
```

[![Snowsight showing a SELECT query against a Delta table in the catalog-linked database.](/static/images/iceberg/delta-sharing/query-01.png)](/static/images/iceberg/delta-sharing/query-01.png)
