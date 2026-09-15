# CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the account or replaces an existing catalog integration
for [Apache Iceberg™ tables](/user-guide/tables-iceberg) managed in a remote catalog that complies with the
open source [Apache Iceberg™ REST OpenAPI specification](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml).

Note

To create an integration for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview), see [CREATE CATALOG INTEGRATION (Snowflake Open Catalog)](/sql-reference/sql/create-catalog-integration-open-catalog) instead.

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ] <name>
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  [ CATALOG_NAMESPACE = '<namespace>' ]
  REST_CONFIG = (
    restConfigParams
  )
  REST_AUTHENTICATION = (
    restAuthenticationParams
  )
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

Where:

Copy code

```
restConfigParams ::=

  CATALOG_URI = '<rest_api_endpoint_url>'
  [ PREFIX = '<prefix>' ]
  [ CATALOG_NAME = '<catalog_name>' ]
  [ CATALOG_API_TYPE = { PUBLIC | PRIVATE | AWS_API_GATEWAY | AWS_PRIVATE_API_GATEWAY
                         | AWS_GLUE | AWS_PRIVATE_GLUE
                         | AWS_S3TABLES | AWS_PRIVATE_S3TABLES } ]
  [ ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS } ]
```

The `restAuthenticationParams` are as follows, depending on your authentication method:

**OAuth**

Copy code

```
restAuthenticationParams (for OAuth) ::=

  TYPE = OAUTH
  [ OAUTH_TOKEN_URI = 'https://<token_server_uri>' ]
  OAUTH_CLIENT_ID = '<oauth_client_id>'
  OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
  OAUTH_ALLOWED_SCOPES = ('<scope_1>', '<scope_2>')
```

**Bearer token**

Copy code

```
restAuthenticationParams (for Bearer token) ::=

  TYPE = BEARER
  BEARER_TOKEN = '<bearer_token>'
```

**SigV4**

Copy code

```
restAuthenticationParams (for SigV4) ::=

  TYPE = SIGV4
  SIGV4_IAM_ROLE = '<iam_role_arn>'
  [ SIGV4_SIGNING_REGION = '<region>' ]
  [ SIGV4_EXTERNAL_ID = '<external_id>' ]
```

## Parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = ICEBERG_REST`
:   Specifies that the catalog source is a REST catalog that’s compliant with the Apache Iceberg REST specification.

`TABLE_FORMAT = ICEBERG`
:   Specifies ICEBERG as the table format supplied by the catalog.

`CATALOG_NAMESPACE = 'namespace'`
:   Optionally specifies the namespace in the external catalog. Snowflake uses this namespace for all Iceberg tables that you associate with
    this catalog integration.

    If specified, you can override this value by specifying a namespace at the table level using the
    [CATALOG\_NAMESPACE](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-namespace) parameter for [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest).
    If not specified, you must set it at the table level by using the CATALOG\_NAMESPACE parameter for
    CREATE ICEBERG TABLE (Iceberg REST catalog).

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` allows users to create new Iceberg tables that reference this integration.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration.

    The value is case-insensitive.

    The default is `TRUE`.

`REFRESH_INTERVAL_SECONDS = value`
:   Specifies the number of seconds that Snowflake waits between attempts to poll the external Iceberg catalog for metadata updates
    for [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    For Delta-based tables, specifies the number of seconds that Snowflake waits between attempts to poll your external cloud storage for
    new metadata.

    Values: 30 to 86400, inclusive

    Default: 30 seconds

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

### REST configuration parameters (restConfigParams)

`CATALOG_URI = 'rest_api_endpoint_url'`
:   The endpoint URL for your catalog REST API. For AWS Glue REST, specify the
    [service endpoint for the AWS Glue Iceberg REST catalog](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html).

`PREFIX`
:   Optionally specifies a prefix to append to all API routes.

`CATALOG_API_TYPE = { PUBLIC | PRIVATE | AWS_API_GATEWAY | AWS_PRIVATE_API_GATEWAY | AWS_GLUE | AWS_PRIVATE_GLUE | AWS_S3TABLES | AWS_PRIVATE_S3TABLES }`
:   Specifies the connection type for the catalog API. Required for SigV4 authentication; otherwise, this parameter is optional.

    - `PUBLIC` specifies an API that is publicly accessible and isn’t managed using Amazon API Gateway; used for non-SigV4 APIs.
    - `PRIVATE` specifies that the catalog, such as Databricks Unity Catalog or a generic Iceberg REST catalog, is accessible
      through a private endpoint. For more information, see [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).
    - `AWS_API_GATEWAY` specifies a public API managed using Amazon API Gateway.
    - `AWS_PRIVATE_API_GATEWAY` specifies a private API managed using Amazon API Gateway.
    - `AWS_GLUE` specifies that the AWS Glue REST catalog is publicly accessible. With this option, you must also specify a value
      for `CATALOG_NAME`.
    - `AWS_PRIVATE_GLUE` specifies that the AWS Glue REST catalog is accessible through a private endpoint. With this option, you must
      also specify a value for `CATALOG_NAME`. For more information, see [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).
    - `AWS_S3TABLES` specifies that the Amazon S3 Tables Iceberg REST endpoint is publicly accessible. With this option, you must also
      specify a value for `CATALOG_NAME` (the S3 Tables bucket ARN) and set `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`.
      For more information, see [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).
    - `AWS_PRIVATE_S3TABLES` specifies that the Amazon S3 Tables Iceberg REST endpoint is accessible through a private endpoint. With this
      option, you must also specify a value for `CATALOG_NAME` (the S3 Tables bucket ARN) and set
      `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`. For more information, see
      [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

    Default: `PUBLIC`

`CATALOG_NAME`
:   Specifies the catalog or identifier to request from your remote catalog service.

    When you use `CATALOG_API_TYPE = AWS_GLUE`, specify the ID of your AWS account for this parameter.

    When you use `CATALOG_API_TYPE = AWS_S3TABLES` or `CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES`, specify the ARN of your S3 Tables
    bucket (for example, `arn:aws:s3tables:us-west-2:123456789012:bucket/my_table_bucket`).

    This parameter is required by some
    third-party catalog services. Check with your catalog provider to determine whether you must specify a catalog name.

    Note

    Before Snowflake version 9.6, this parameter was called `WAREHOUSE`. Snowflake still recognizes `WAREHOUSE` if specified,
    but we recommend that you use `CATALOG_NAME`.

`ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS }`
:   Specifies the access delegation mode to use for accessing Iceberg table files in your external cloud storage.

    - `VENDED_CREDENTIALS` specifies that Snowflake should use vended credentials.
    - `EXTERNAL_VOLUME_CREDENTIALS` specifies that Snowflake should use an external volume.

    Default: `EXTERNAL_VOLUME_CREDENTIALS`

### REST authentication parameters (restAuthenticationParams)

**OAuth**

> `TYPE = OAUTH`
> :   Specifies OAuth as the authentication type for Snowflake to use to connect to your Iceberg REST catalog.
>
> `OAUTH_TOKEN_URI = token_server_uri`
> :   Optional URL for your third-party identity provider. If not specified, Snowflake assumes that the remote catalog provider is the OAuth identity provider.
>
> `OAUTH_CLIENT_ID = oauth_client_id`
> :   Your OAuth2 client ID.
>
> `OAUTH_CLIENT_SECRET = oauth_client_secret`
> :   Your OAuth2 client secret.
>
> `OAUTH_ALLOWED_SCOPES = ( 'scope_1', 'scope_2' )`
> :   The scope of the OAuth token. The Iceberg REST API specification includes only one scope,
>     but catalogs can support more than one scope in their implementation.

**Bearer token**

> `TYPE = BEARER`
> :   Specifies a bearer token as the authentication type for Snowflake to use to connect to your Iceberg REST catalog.
>
> `BEARER_TOKEN = bearer_token`
> :   The bearer token for your identity provider. You can alternatively specify a personal access token (PAT).

**SigV4**

> `TYPE = SIGV4`
> :   Specifies Signature Version 4 as the authentication type for Snowflake to use to connect to your Iceberg REST catalog.
>
> `SIGV4_IAM_ROLE = 'iam_role_arn'`
> :   Specifies the Amazon Resource Name (ARN) for an IAM role that has permission to access your REST API in API Gateway.
>
> `SIGV4_SIGNING_REGION = 'region'`
> :   Optionally specifies the AWS Region associated with your API in API Gateway. If you don’t specify this parameter, Snowflake uses the region
>     in which your Snowflake account is deployed.

`SIGV4_EXTERNAL_ID = 'external_id'`
:   Optionally specifies an external ID that Snowflake uses to establish a trust relationship with AWS.
    You must specify the same external ID in the trust policy of the IAM role
    that you configured for this catalog integration.

    If you don’t specify a value for this parameter, Snowflake automatically generates a unique external ID when you create (or replace) a catalog integration.

    For more information about external IDs,
    see
    [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Catalog integrations provide read-only access to external Iceberg catalogs.
- You can’t modify an existing catalog integration; use a CREATE OR REPLACE CATALOG INTEGRATION statement instead.
- You can’t drop or replace a catalog integration if one or more Apache Iceberg™ tables
  are associated with the catalog integration.

  To view the tables that depend on a catalog integration,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `catalog_name` column.

  Note

  The column identifier (`catalog_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "catalog_name" = 'my_catalog_integration_1';
  ```
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

The following example creates a REST catalog integration that uses OAuth to connect
to Tabular. It sets a default namespace using the `CATALOG_NAMESPACE` parameter.

To override the default namespace at the table level,
use the [CATALOG\_NAMESPACE](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-namespace) parameter for CREATE ICEBERG TABLE.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION tabular_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'default'
  REST_CONFIG = (
    CATALOG_URI = 'https://api.tabular.io/ws'
    CATALOG_NAME = '<tabular_warehouse_name>'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = 'https://api.tabular.io/ws/v1/oauth/tokens'
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
    OAUTH_ALLOWED_SCOPES = ('catalog')
  )
  ENABLED = TRUE;
```

Create a catalog integration for AWS Glue REST with SigV4 authentication:

Copy code

```
CREATE CATALOG INTEGRATION glue_rest_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'rest_catalog_integration'
  REST_CONFIG = (
    CATALOG_URI = 'https://glue.us-west-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_GLUE
    CATALOG_NAME = '123456789012'
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my-role'
    SIGV4_SIGNING_REGION = 'us-west-2'
  )
  ENABLED = TRUE;
```

Create a catalog integration for an Amazon S3 Tables Iceberg REST endpoint with SigV4 authentication and catalog-vended
credentials. `CATALOG_NAME` is the ARN of your S3 Tables bucket, and `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`
is required:

Copy code

```
CREATE CATALOG INTEGRATION s3tables_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://s3tables.us-west-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_S3TABLES
    CATALOG_NAME = 'arn:aws:s3tables:us-west-2:123456789012:bucket/my_table_bucket'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my-role'
    SIGV4_SIGNING_REGION = 'us-west-2'
  )
  ENABLED = TRUE;
```

To use `AWS_PRIVATE_S3TABLES` for outbound private connectivity, see
[Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

For examples that cover the other authentication options, see [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest).
