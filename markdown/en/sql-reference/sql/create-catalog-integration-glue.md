# CREATE CATALOG INTEGRATION (AWS Glue)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def)
in the account or replaces an existing catalog integration for [Apache Iceberg™ tables](/user-guide/tables-iceberg)
that use AWS Glue as the catalog.

Important

To integrate with AWS Glue, we recommend that you instead create a catalog integration for the
[AWS Glue Iceberg REST endpoint](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html),
which supports additional Iceberg table features such as catalog-vended credentials.

For instructions, see [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest).

Note

When you create a catalog integration for AWS Glue, you must complete additional steps to establish a
trust relationship between Snowflake and the Glue Data Catalog. For information, see [Configure a catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue).

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [IF NOT EXISTS]
  <name>
  CATALOG_SOURCE = GLUE
  TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = '<arn-for-AWS-role-to-assume>'
  GLUE_CATALOG_ID = '<glue-catalog-id>'
  [ GLUE_REGION = '<AWS-region-of-the-glue-catalog>' ]
  [ CATALOG_NAMESPACE = '<catalog-namespace>' ]
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = GLUE`
:   Specifies that the integration is for AWS Glue.

`TABLE_FORMAT = ICEBERG`
:   Specifies Glue Iceberg tables.

`GLUE_AWS_ROLE_ARN = 'arn-for-AWS-role-to-assume'`
:   Specifies the Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role to assume.

`GLUE_CATALOG_ID = 'glue-catalog-id'`
:   Specifies the ID of your AWS account.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` lets users create new Iceberg tables that reference this integration. Existing Iceberg tables that reference
    >   this integration function normally.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration. Existing Iceberg tables that
    >   reference this integration cannot access the catalog in the table definition.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

`[ GLUE_REGION = 'AWS-region-of-the-glue-catalog' ]`
:   Specifies the AWS Region of your AWS Glue Data Catalog. You must specify a value for this parameter if
    your Snowflake account is not hosted on AWS. Otherwise, the default region is the Snowflake deployment region for the account.

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

- You cannot modify an existing catalog integration; use a CREATE OR REPLACE CATALOG INTEGRATION statement instead.
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
> CREATE CATALOG INTEGRATION glueCatalogInt
>   CATALOG_SOURCE = GLUE
>   CATALOG_NAMESPACE = 'myNamespace'
>   TABLE_FORMAT = ICEBERG
>   GLUE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myGlueRole'
>   GLUE_CATALOG_ID = '123456789012'
>   GLUE_REGION = 'us-east-2'
>   ENABLED = TRUE;
> ```
