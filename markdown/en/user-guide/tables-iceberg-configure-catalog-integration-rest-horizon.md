# Access Apache Iceberg™ tables in another Snowflake account

Regional availability

Available on Amazon Web Services (AWS), Google Cloud, or Microsoft Azure in all commercial regions. Not available on government deployments.

Create a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in one Snowflake account that connects to the
[Horizon Iceberg REST Catalog API](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) of another
Snowflake account. You can then read and write Apache Iceberg™ tables in the other account from your account, without creating, storing,
or rotating a secret.

This topic uses the following terms:

- **Consumer account**: The Snowflake account where you create the catalog integration and query the tables.
- **Provider account**: The Snowflake account that contains the Iceberg tables and exposes them through Horizon Catalog.

The catalog integration authenticates with [workload identity federation](/user-guide/workload-identity-federation) (WIF). Snowflake
issues a workload identity for the catalog integration, and the provider account trusts that identity through a service user.

## How the connection works

When the catalog integration connects to the provider account, the following happens:

1. Snowflake issues a short-lived ID token for the catalog integration.
2. Snowflake exchanges the ID token at the token endpoint of the provider account for an access token that is scoped to a role in the
   provider account.
3. The catalog integration calls the Horizon Iceberg REST Catalog API with the access token. Snowflake refreshes the access token
   automatically before it expires.

You don’t manage any credentials for this connection.

## Before you begin

### Account requirements and privileges

- In the provider account, the database that you want to access must be available through the Horizon Iceberg REST Catalog API. For more
  information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
- In the provider account, choose a role that has the privileges that you need on the database. For example, to read tables, the role needs
  the `USAGE` privilege on the database and schemas and the `SELECT` privilege on the tables. To write to tables, the role also needs the
  write privileges on those tables. For more information, see
  [Configure read access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-horizon-configure-read-access) and
  [Configure write access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-configure-write-access).

  The steps in this topic refer to this role as `<role_name>`.
- In the consumer account, you must use a role that has the `CREATE INTEGRATION` privilege on the account.
- To create the service user in the provider account, you must use a role that has the `CREATE USER` privilege on the account, such as
  `USERADMIN`. For more information, see [Access control requirements](/sql-reference/sql/create-user#access-control-requirements).
- To grant the access role to the service user in the provider account, you must use a role that has `OWNERSHIP` on the role being granted,
  or the global `MANAGE GRANTS` privilege, such as `SECURITYADMIN`. For more information, see
  [Access control requirements](/sql-reference/sql/grant-role#access-control-requirements).

### Supported operations

You can use the catalog integration for the following operations:

- Read tables through individual Iceberg tables or a catalog-linked database, with support for automated refresh and vended credentials.
- Write to existing tables with `INSERT`, `UPDATE`, and `DELETE`, through an individual Iceberg table or a catalog-linked database.
- Run `CREATE SCHEMA`, `DROP SCHEMA`, and `DROP ICEBERG TABLE` in a catalog-linked database. `CREATE ICEBERG TABLE` isn’t supported.
  To add a table, create it in the provider account; the catalog-linked database discovers it automatically.

### Limitations

This catalog integration doesn’t support fine-grained access control on tables in the provider account, including
[masking policies](/user-guide/security-column-intro) and [row access policies](/user-guide/security-row-intro). You can’t use the
integration to read or write provider tables that require policy-based filtering or masking.

The Snowflake consumer doesn’t currently support the Iceberg REST Catalog Scan Plan API. For supported ways to query policy-protected
tables with external engines, see [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

### Provider responsibilities and data ownership

The provider is responsible for granting the consumer access to its tables. The provider creates a service user in its account
and grants a role to that user. The privileges of the role determine which databases, schemas, and tables the consumer can access
and which operations it can perform. Grant only the privileges that the consumer needs, and scope the catalog integration to that role.

Data that a consumer writes to tables in the provider account belongs to the provider. Granting write access lets the consumer modify the
provider’s tables; it doesn’t transfer ownership of those tables or the data that the consumer writes.

### Billing

When a consumer accesses tables in a provider account through this catalog integration:

- The consumer account pays for the compute used to query and write to the tables.
- The provider account pays for requests to its Horizon Iceberg REST Catalog API. For API pricing and applicable cross-region data egress
  charges, see [Billing](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-billing).
- The provider is responsible for the storage costs of its tables, including data written by the consumer.

## Connect the accounts

Complete the following steps in the provider and consumer accounts.

### Step 1: Get the Horizon Catalog endpoint (provider account)

Use the endpoint format documented in the
[Horizon Catalog connection guide](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine).
In the provider account, retrieve the account identifier:

Copy code

```
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() AS account_identifier;
```

Use the returned identifier in the Horizon Iceberg REST Catalog API URL:

```
https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog
```

For example, if the account identifier is `myorg-provider_account`, the URL is
`https://myorg-provider_account.snowflakecomputing.com/polaris/api/catalog`.

Use this URL as `CATALOG_URI` when you create the catalog integration in the consumer account.

If you need private connectivity, retrieve the private URL instead. For instructions, see
[Use private connectivity for the catalog API](#label-tables-iceberg-catalog-integration-horizon-private).

### Step 2: Create the catalog integration (consumer account)

In the consumer account, use the [CREATE CATALOG INTEGRATION (Snowflake Horizon Catalog)](/sql-reference/sql/create-catalog-integration-horizon)
command to create a catalog integration. Set `CATALOG_SOURCE = POLARIS` and `OAUTH_GRANT_TYPE = TOKEN_EXCHANGE`, and scope the access
token to a role in the provider account. You don’t configure a secret.

Snowflake recommends that you use [vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials),
so that Horizon Catalog provides the storage credentials and you don’t configure an external volume in the consumer account. For private
connectivity to that storage, see [Use private connectivity for storage with vended credentials](#label-tables-iceberg-catalog-integration-horizon-private-storage).

Copy code

```
CREATE CATALOG INTEGRATION horizon_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = '<database_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
    -- OAUTH_AUDIENCE = '<audience>'   -- Optional; defaults to snowflakecomputing.com
  )
  ENABLED = TRUE;
```

Where:

`CATALOG_URI = 'https://account_identifier.snowflakecomputing.com/polaris/api/catalog'`
:   The URL that you retrieved in [Step 1](#label-tables-iceberg-catalog-integration-horizon-get-url).

    For more information about account URL formats, see [Account identifiers](/user-guide/admin-account-identifier).

`CATALOG_NAME = 'database_name'`
:   The name of the database in the provider account that contains the Iceberg tables.

`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`
:   Specifies that Horizon Catalog vends the storage credentials for the tables. Recommended. To use an external volume instead, see
    [Use an external volume instead of vended credentials](#label-tables-iceberg-catalog-integration-horizon-external-volume).

`OAUTH_GRANT_TYPE = TOKEN_EXCHANGE`
:   Specifies that Snowflake obtains access tokens by exchanging an ID token that Snowflake issues for the catalog integration.

`OAUTH_ALLOWED_SCOPES = ( 'session:role:role_name' )`
:   The role in the provider account that the access token is scoped to.

`OAUTH_AUDIENCE = 'audience'`
:   Optional audience for the ID token that Snowflake issues for the catalog integration. Defaults to `snowflakecomputing.com`.
    To restrict token use to the provider account, see [Restrict token use to the provider account](#label-tables-iceberg-catalog-integration-horizon-audience).

You don’t specify `OAUTH_TOKEN_URI`, `OAUTH_CLIENT_ID`, or `OAUTH_CLIENT_SECRET`.

Don’t set `CATALOG_NAMESPACE` on the catalog integration. Instead, specify the schema when you
[create an Iceberg table](#label-tables-iceberg-catalog-integration-horizon-create-table), or use a
[catalog-linked database](#label-tables-iceberg-catalog-integration-horizon-create-cld) to discover all schemas.

### Step 3: Retrieve the catalog integration identity (consumer account)

In the consumer account, run the [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) command:

Copy code

```
DESC CATALOG INTEGRATION horizon_catalog_int;
```

From the output, record the values of the following properties:

| Property | Example value |
| --- | --- |
| `WORKLOAD_IDENTITY_FEDERATION_ISSUER` | `https://identity.snowflake.com/oauth2/...` |
| `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` | `identity_catalog_integration_...` |

Expand

Show lessSee more

The `REST_AUTHENTICATION` property shows `OAUTH_AUDIENCE=snowflakecomputing.com`. If you don’t specify `OAUTH_AUDIENCE`, the audience
defaults to `snowflakecomputing.com`, which is the audience that a Snowflake service user accepts by default.

### Step 4: Create and authorize a service user (provider account)

In the provider account, create a service user that trusts the identity of the catalog integration, and then grant the role to the user.
Replace the `ISSUER` and `SUBJECT` values with the values that you recorded in the previous step.

Use roles with the [required privileges](#label-tables-iceberg-catalog-integration-horizon-prerequisites) for each command. Setting
`DEFAULT_ROLE` doesn’t grant the role to the user; you must also run `GRANT ROLE`.

Copy code

```
CREATE USER horizon_catalog_svc
  TYPE = SERVICE
  DEFAULT_ROLE = <role_name>
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = '<workload_identity_federation_issuer>'
    SUBJECT = '<workload_identity_federation_subject>'
  );

GRANT ROLE <role_name> TO USER horizon_catalog_svc;
```

You don’t need to create a security integration in the provider account.

For more information, see [CREATE USER](/sql-reference/sql/create-user).

### Step 5: Verify the connection (consumer account)

In the consumer account, verify that the catalog integration can connect to the provider account, and then browse the namespaces and tables
in the catalog:

Copy code

```
SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('horizon_catalog_int');

SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('horizon_catalog_int', '', 1);

SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('horizon_catalog_int', '<schema_name>');
```

If verification fails, see [Troubleshooting](#label-tables-iceberg-catalog-integration-horizon-troubleshoot).

## Access tables from the consumer account

In the consumer account, you can access the tables in the provider account by creating individual Iceberg tables or by creating a
catalog-linked database.

### Access an individual table

To access one table, create an Iceberg table in any database that references the table in the provider account. For example:

Copy code

```
CREATE ICEBERG TABLE my_db.public.orders
  CATALOG = 'horizon_catalog_int'
  CATALOG_NAMESPACE = '<schema_name>'
  CATALOG_TABLE_NAME = '<table_name>'
  AUTO_REFRESH = TRUE;
```

You can then query the table and write to it. Writes are committed to Horizon Catalog in the provider account.

Copy code

```
SELECT * FROM my_db.public.orders;

INSERT INTO my_db.public.orders VALUES (...);
```

### Access tables with a catalog-linked database

To discover and sync all schemas and tables in the database, create a
[catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database). For example:

Copy code

```
CREATE DATABASE horizon_linked_db
  LINKED_CATALOG = (
    CATALOG = 'horizon_catalog_int'
    ALLOWED_NAMESPACES = ('<schema_name>')
  );
```

The `ALLOWED_NAMESPACES` parameter is optional. Schemas and tables that you create later in the provider account appear in the
catalog-linked database automatically.

Copy code

```
SELECT * FROM horizon_linked_db.<schema_name>.<table_name>;
```

## Optional configurations

Use the following examples to configure the catalog integration in
[Step 2](#label-tables-iceberg-catalog-integration-horizon-create). After creating the integration, continue with
[Step 3](#label-tables-iceberg-catalog-integration-horizon-get-identity) to retrieve its identity and authorize access in the provider
account.

### Use an external volume instead of vended credentials

Snowflake recommends vended credentials. If you must use an
[external volume](/user-guide/tables-iceberg-configure-external-volume) in the consumer account to access the table storage, set
`ACCESS_DELEGATION_MODE = EXTERNAL_VOLUME_CREDENTIALS` in `REST_CONFIG` (or omit the parameter):

Copy code

```
CREATE CATALOG INTEGRATION horizon_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = '<database_name>'
    ACCESS_DELEGATION_MODE = EXTERNAL_VOLUME_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
  )
  ENABLED = TRUE;
```

Specify `EXTERNAL_VOLUME` when you create Iceberg tables or a catalog-linked database:

Copy code

```
CREATE ICEBERG TABLE my_db.public.orders
  EXTERNAL_VOLUME = '<external_volume_name>'
  CATALOG = 'horizon_catalog_int'
  CATALOG_NAMESPACE = '<schema_name>'
  CATALOG_TABLE_NAME = '<table_name>'
  AUTO_REFRESH = TRUE;

CREATE DATABASE horizon_linked_db
  LINKED_CATALOG = (
    CATALOG = 'horizon_catalog_int'
  )
  EXTERNAL_VOLUME = '<external_volume_name>';
```

### Restrict token use to the provider account

By default, ID tokens use the audience `snowflakecomputing.com`. To limit the tokens of a catalog integration to one provider account, set
the same custom audience in both accounts:

- In the consumer account, set `OAUTH_AUDIENCE` in `REST_AUTHENTICATION`:

  Copy code

  ```
  CREATE CATALOG INTEGRATION horizon_catalog_int
    CATALOG_SOURCE = POLARIS
    TABLE_FORMAT = ICEBERG
    REST_CONFIG = (
      CATALOG_URI = 'https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog'
      CATALOG_NAME = '<database_name>'
      ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
    )
    REST_AUTHENTICATION = (
      TYPE = OAUTH
      OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
      OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
      OAUTH_AUDIENCE = '<audience>'
    )
    ENABLED = TRUE;
  ```
- In the provider account, set `OIDC_AUDIENCE_LIST` in `WORKLOAD_IDENTITY` for the service user:

  Copy code

  ```
  ALTER USER horizon_catalog_svc
    SET WORKLOAD_IDENTITY = (
      TYPE = OIDC
      ISSUER = '<workload_identity_federation_issuer>'
      SUBJECT = '<workload_identity_federation_subject>'
      OIDC_AUDIENCE_LIST = ('<audience>')
    );
  ```

If the audiences don’t match, the provider account rejects the token request.

### Use private connectivity for the catalog API

This configuration controls the connection from the consumer account to the provider’s Horizon Catalog API. To also use private
connectivity when accessing table storage with vended credentials, configure
[Use private connectivity for storage with vended credentials](#label-tables-iceberg-catalog-integration-horizon-private-storage).

For accounts in different Snowflake regions, private endpoint provisioning is supported on AWS and Azure. Both accounts must be hosted
on the same cloud provider.

To retrieve the private connectivity URL, run [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) with the `ACCOUNTADMIN` role
in the provider account:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT 'https://'
  || PARSE_JSON(SYSTEM$GET_PRIVATELINK_CONFIG()):"regionless-privatelink-account-url"::VARCHAR
  || '/polaris/api/catalog' AS catalog_uri;
```

The query uses `regionless-privatelink-account-url`, which contains the organization name and account name. You can also use
`privatelink-account-url` for the account locator form.

In the consumer account, use the returned URL as `CATALOG_URI` and set `CATALOG_API_TYPE = PRIVATE`:

Copy code

```
CREATE CATALOG INTEGRATION horizon_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<orgname>-<provider_account_name>.privatelink.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = '<database_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
  )
  ENABLED = TRUE;
```

Consider the following:

- With `CATALOG_API_TYPE = PRIVATE`, if the provider and consumer accounts are in the same region, Snowflake routes catalog API requests
  internally. You don’t need to provision a catalog endpoint in the consumer account. Private access to table storage with vended
  credentials requires its own configuration; see [Use private connectivity for storage with vended credentials](#label-tables-iceberg-catalog-integration-horizon-private-storage).
- If the provider account is in a different region, you must provision a private endpoint for the PrivateLink host of the provider account in
  the consumer account. On AWS, Snowflake approves the connection automatically without a PrivateLink authorization call. On Azure,
  you must authorize the endpoint after provisioning; the connection isn’t approved automatically. For instructions, see
  [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).
- Use the PrivateLink account URL only with `CATALOG_API_TYPE = PRIVATE`. Use the regular account URL only with
  `CATALOG_API_TYPE = PUBLIC`, which is the default.

### Use private connectivity for storage with vended credentials

To access the provider’s table storage over private connectivity from the consumer account, keep
`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` and set `USE_PRIVATELINK_ENDPOINT = TRUE` in the catalog integration’s
`DEFAULT_STORAGE_CONFIG`. You can configure private connectivity to storage independently of private connectivity to the catalog API.

Private connectivity to storage requires Business Critical (or higher) and is supported on AWS and Azure. On AWS, the consumer account
and S3 bucket must be in the same region.

1. In the consumer account, provision a private endpoint for the table storage. For instructions, see
   [Provision a private connectivity endpoint for storage](/user-guide/tables-iceberg-vended-credentials-private-connectivity#label-vended-creds-pl-provision-storage).
2. On the storage side, allow access from the consumer account’s private endpoint and verify that the endpoint is ready. For instructions,
   see [Allowlist Snowflake’s access on the storage side](/user-guide/tables-iceberg-vended-credentials-private-connectivity#label-vended-creds-pl-allowlist-snowflake) and
   [Verify the endpoint status](/user-guide/tables-iceberg-vended-credentials-private-connectivity#label-vended-creds-pl-step7). Preserve the provider account’s storage access when updating storage policies.
3. In the consumer account, create the catalog integration with private storage access. When you complete
   [Step 2](#label-tables-iceberg-catalog-integration-horizon-create), you can use the following example, which configures private
   connectivity for both the catalog API and storage:

   Copy code

   ```
   CREATE CATALOG INTEGRATION horizon_catalog_int
     CATALOG_SOURCE = POLARIS
     TABLE_FORMAT = ICEBERG
     REST_CONFIG = (
       CATALOG_URI = 'https://<orgname>-<provider_account_name>.privatelink.snowflakecomputing.com/polaris/api/catalog'
       CATALOG_API_TYPE = PRIVATE
       CATALOG_NAME = '<database_name>'
       ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
     )
     REST_AUTHENTICATION = (
       TYPE = OAUTH
       OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
       OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
     )
     DEFAULT_STORAGE_CONFIG = (
       USE_PRIVATELINK_ENDPOINT = TRUE
     )
     ENABLED = TRUE;
   ```

   For private connectivity to the catalog API, complete the setup in
   [Use private connectivity for the catalog API](#label-tables-iceberg-catalog-integration-horizon-private). To use private connectivity for storage with the regular catalog URL,
   use the endpoint from [Step 1](#label-tables-iceberg-catalog-integration-horizon-get-url) and omit `CATALOG_API_TYPE = PRIVATE`.

   After creating the integration, continue with
   [Step 3](#label-tables-iceberg-catalog-integration-horizon-get-identity) to retrieve its identity and authorize access in the provider
   account.

   To enable private storage access on an existing catalog integration, run:

   Copy code

   ```
   ALTER CATALOG INTEGRATION horizon_catalog_int
     SET DEFAULT_STORAGE_CONFIG = (
       USE_PRIVATELINK_ENDPOINT = TRUE
     );
   ```

For the complete storage workflow, see [Configure private connectivity to storage for catalog-vended credentials](/user-guide/tables-iceberg-vended-credentials-private-connectivity).

## Troubleshooting

| Error | Resolution |
| --- | --- |
| `User provided authentication credentials or scopes are invalid for catalog integration ... unauthorized_client: The client is not authorized.` | Check the following:   - The provider account has a service user whose `ISSUER` and `SUBJECT` values exactly match the   `WORKLOAD_IDENTITY_FEDERATION_ISSUER` and `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` values in the output of `DESC CATALOG INTEGRATION`. - The role in `OAUTH_ALLOWED_SCOPES` is granted to the service user. - If you set a custom `OAUTH_AUDIENCE`, the `OIDC_AUDIENCE_LIST` of the service user contains that audience. If you use the default   audience, the service user doesn’t have an `OIDC_AUDIENCE_LIST`. |
| `Missing option(s): REST_AUTHENTICATION.OAUTH_AUDIENCE` | Check the following:   - The catalog integration uses `CATALOG_SOURCE = POLARIS`. - The feature is available for the consumer account. It’s available in commercial regions only. If the error persists, contact   [Snowflake Support](https://community.snowflake.com/s/article/How-To-Submit-a-Support-Case-in-Snowflake-Lodge). |
| `Regular account URL ... is not allowed ... with PRIVATE API type` | When `CATALOG_API_TYPE = PRIVATE`, use the PrivateLink account URL of the provider account for `CATALOG_URI`. |
| `Private link account url ... is not allowed ... use normal account url instead` | When `CATALOG_API_TYPE = PUBLIC`, which is the default, use the regular account URL of the provider account for `CATALOG_URI`. |
| `Private endpoint corresponding to service name ... does not exist` | The provider account is in a different region. Provision a private endpoint for the PrivateLink host of the provider account. |
| `Setting table location is not allowed` | `CREATE ICEBERG TABLE` isn’t supported in a catalog-linked database that uses this catalog integration. Create the table in the provider account; the catalog-linked database discovers it automatically. |

Expand

Show lessSee more
