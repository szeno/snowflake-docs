# CREATE CATALOG INTEGRATION (AWS Glue)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def)
in the account or replaces an existing catalog integration for [Apache Iceberg™ tables](/user-guide/tables-iceberg)
that use AWS Glue as the catalog.

Note

When you create a catalog integration for AWS Glue, you must complete additional steps to establish a
trust relationship between Snowflake and the Glue Data Catalog. For information, see [Configure a catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue).

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ]
  <name>
  CATALOG_SOURCE = GLUE
  TABLE_FORMAT = ICEBERG
  [ CATALOG_NAMESPACE = '<catalog-namespace>' ]
  REST_CONFIG = (
    CATALOG_API_TYPE = { AWS_GLUE | AWS_PRIVATE_GLUE }
    CATALOG_NAME = '<glue_catalog_id>'
    [ ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS } ]
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = '<arn-for-AWS-role-to-assume>'
    [ SIGV4_SIGNING_REGION = '<AWS-region-of-the-glue-catalog>' ]
  )
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = GLUE`
:   Specifies that the integration is for AWS Glue.

`TABLE_FORMAT = ICEBERG`
:   Specifies Glue Iceberg tables.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` lets users create new Iceberg tables that reference this integration. Existing Iceberg tables that reference
    >   this integration function normally.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration. Existing Iceberg tables that
    >   reference this integration can’t access the catalog in the table definition.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

`CATALOG_NAMESPACE = 'catalog-namespace'`
:   Specifies your AWS Glue Data Catalog namespace (for example, `my_glue_database`). This is the default namespace for all Iceberg tables
    that you associate with this catalog integration.

    > - If specified, you can override this value by specifying the namespace at the table level when you create a table.
    > - If not specified, you must specify the namespace at the table level when you create a table.

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

### REST configuration parameters (`REST_CONFIG`)

`CATALOG_API_TYPE = { AWS_GLUE | AWS_PRIVATE_GLUE }`
:   Specifies the connection type for the Glue catalog API.

    - `AWS_GLUE` specifies that the AWS Glue catalog is publicly accessible.
    - `AWS_PRIVATE_GLUE` specifies that the AWS Glue catalog is accessible through a private endpoint. For more information, see
      [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).

    Don’t specify `CATALOG_URI`, `PREFIX`, or `WAREHOUSE` in `REST_CONFIG` for `CATALOG_SOURCE = GLUE`. Snowflake derives the Glue
    endpoint from `CATALOG_API_TYPE` and `SIGV4_SIGNING_REGION`.

`CATALOG_NAME = 'glue_catalog_id'`
:   Specifies the ID of your AWS account.

`ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS }`
:   Specifies the access delegation mode to use for accessing Iceberg table files in your external cloud storage.

    - `VENDED_CREDENTIALS` specifies that Snowflake should use vended credentials.
    - `EXTERNAL_VOLUME_CREDENTIALS` specifies that Snowflake should use an external volume.

    Default: `EXTERNAL_VOLUME_CREDENTIALS`

### REST authentication parameters (`REST_AUTHENTICATION`)

`TYPE = SIGV4`
:   Specifies Signature Version 4 as the authentication type for Snowflake to use to connect to AWS Glue.
    `SIGV4` is the only supported authentication type for `CATALOG_SOURCE = GLUE`.

`SIGV4_IAM_ROLE = 'arn-for-AWS-role-to-assume'`
:   Specifies the Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role to assume.

`SIGV4_SIGNING_REGION = 'AWS-region-of-the-glue-catalog'`
:   Optionally specifies the AWS Region of your AWS Glue Data Catalog. You must specify a value for this parameter if
    your Snowflake account isn’t hosted on AWS. Otherwise, the default region is the Snowflake deployment region for the account.

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

- You can’t modify an existing catalog integration; use a CREATE OR REPLACE CATALOG INTEGRATION statement instead.
- `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` isn’t supported with `CATALOG_API_TYPE = AWS_PRIVATE_GLUE`.
  Use `CATALOG_API_TYPE = AWS_GLUE` instead.
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

The following example creates a catalog integration that uses an AWS Glue catalog source.
When you create a catalog integration for Glue, you must complete additional steps to establish a
trust relationship between Snowflake and the Glue Data Catalog. For information, see [Configure a catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue).

> Copy code
>
> ```
> CREATE OR REPLACE CATALOG INTEGRATION glueCatalogInt
>   CATALOG_SOURCE = GLUE
>   TABLE_FORMAT = ICEBERG
>   CATALOG_NAMESPACE = 'myNamespace'
>   REST_CONFIG = (
>     CATALOG_API_TYPE = AWS_GLUE
>     CATALOG_NAME = '123456789012'
>   )
>   REST_AUTHENTICATION = (
>     TYPE = SIGV4
>     SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/myGlueRole'
>     SIGV4_SIGNING_REGION = 'us-east-2'
>   )
>   ENABLED = TRUE;
> ```

The following example creates a Glue catalog integration that uses catalog-vended credentials:

> Copy code
>
> ```
> CREATE OR REPLACE CATALOG INTEGRATION glueCatalogIntVended
>   CATALOG_SOURCE = GLUE
>   TABLE_FORMAT = ICEBERG
>   CATALOG_NAMESPACE = 'myNamespace'
>   REST_CONFIG = (
>     CATALOG_API_TYPE = AWS_GLUE
>     CATALOG_NAME = '123456789012'
>     ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
>   )
>   REST_AUTHENTICATION = (
>     TYPE = SIGV4
>     SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/myGlueRole'
>     SIGV4_SIGNING_REGION = 'us-east-2'
>   )
>   ENABLED = TRUE;
> ```
