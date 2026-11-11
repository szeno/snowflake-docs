# DESCRIBE CATALOG INTEGRATION

Describes the properties of a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration) , [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations)

## Syntax

Copy code

```
DESC[RIBE] CATALOG INTEGRATION <name>
```

## Parameters

`name`
:   Specifies the identifier for the catalog integration to describe. If the identifier contains spaces or special characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `property` | The name of the property. This column can include the properties listed in the following table. |
| `property_type` | The property type. |
| `property_value` | The value assigned to the property. |
| `property_default` | The default property value. |

Expand

Show lessSee more

For AWS Glue, the output includes `REST_CONFIG` and `REST_AUTHENTICATION` property maps, which contain the
catalog ID (`CATALOG_NAME`), IAM role (`SIGV4_IAM_ROLE`), Region (`SIGV4_SIGNING_REGION`), and external ID
(`SIGV4_EXTERNAL_ID`).

The `property` column can include the following properties of catalog integration object:

| Property | Description |
| --- | --- |
| `enabled` | Specifies whether the catalog integration is available to use for Apache Iceberg™ tables. |
| `catalog_source` | The type of catalog source; for example, `ICEBERG_REST`, `POLARIS`, `OBJECT_STORE`, or `GLUE`. |
| `refresh_interval_seconds` | Specifies the number of seconds that Snowflake waits between attempts to poll the external Iceberg catalog for metadata updates for [automated refresh](/user-guide/tables-iceberg-auto-refresh). |
| `rest_authentication` | Specifies the REST authentication parameters for the catalog integration. |
| `rest_config` | Specifies the REST configuration parameters for the catalog integration. |
| `catalog_namespace` | The output for this column is as follows:   - If the catalog integration is for externally managed Iceberg tables, specifies the namespace of the external Iceberg catalog. If the   namespace is specified at the table level only, this column has no value in the function output. - If the catalog integration is for [syncing a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync)   , this column has no value in the function output because this field is   not required. |
| `table_format` | The table format supplied by the catalog; for example, `ICEBERG`. |
| `glue_aws_iam_user_arn` | (AWS Glue) The ARN of the AWS IAM user created for your Snowflake account when you created the catalog integration. |
| `workload_identity_federation_issuer` | (Workload identity federation) The issuer URL of Snowflake as the OIDC provider for the catalog integration. Give this value to the remote service so that it can verify the `iss` claim of the ID tokens that Snowflake issues for the catalog integration. For example, see [Access Apache Iceberg™ tables in another Snowflake account](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon). |
| `workload_identity_federation_subject` | (Workload identity federation) The identifier of the catalog integration as an OIDC client. Give this value to the remote service so that it can verify the `sub` claim of the ID tokens that Snowflake issues for the catalog integration. |
| `comment` | The comment for the catalog integration. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration (catalog) |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Describe a catalog integration:

Copy code

```
DESC CATALOG INTEGRATION my_catalog_integration;
```

The following shows the output of DESCRIBE CATALOG INTEGRATION for an AWS Glue catalog integration.
The IAM role, catalog ID, Region, and external ID appear inside the `REST_CONFIG` and
`REST_AUTHENTICATION` property maps.

```
+--------------------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------+------------------+
|         property         | property_type |                                                                property_value                                                               | property_default |
+--------------------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------+------------------+
| ENABLED                  | Boolean       | true                                                                                                                                        | true             |
| CATALOG_SOURCE           | String        | GLUE                                                                                                                                        |                  |
| CATALOG_NAMESPACE        | String        | dbname                                                                                                                                      |                  |
| TABLE_FORMAT             | String        | ICEBERG                                                                                                                                     |                  |
| REFRESH_INTERVAL_SECONDS | Integer       | 30                                                                                                                                          | 30               |
| GLUE_AWS_IAM_USER_ARN    | String        | arn:aws:iam::123456789012:user/example                                                                                                      |                  |
| REST_CONFIG              | EnumMap       | {CATALOG_API_TYPE=AWS_GLUE, CATALOG_NAME=123456789012}                                                                                      |                  |
| REST_AUTHENTICATION      | EnumMap       | {TYPE=SIGV4, SIGV4_IAM_ROLE=arn:aws:iam::123456789012:role/myGlueRole, SIGV4_SIGNING_REGION=us-east-2, SIGV4_EXTERNAL_ID=exampleExternalId} |                  |
| COMMENT                  | String        |                                                                                                                                             |                  |
+--------------------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------+------------------+
```
