# Amazon Redshift

Horizon Catalog supports both Amazon Redshift deployment types. Select your instance type to get started:

## Supported deployments

- [Provisioned cluster](/user-guide/snowflake-horizon/connectors/amazon-redshift/provisioned)
- [Serverless workgroup](/user-guide/snowflake-horizon/connectors/amazon-redshift/serverless)

## How the connector works

The connector authenticates using IAM role assumption (`sts:AssumeRole` with an external ID
supplied by Horizon Catalog) and then:

1. Auto-discovers the cluster or workgroup endpoint.
2. Auto-detects the audit log destination (S3 or CloudWatch for provisioned; CloudWatch only for serverless).
3. Reads query logs to build popularity and lineage data.
4. Queries Redshift system views for schema and table metadata.

## Choosing between provisioned and serverless

|  | Provisioned | Serverless |
| --- | --- | --- |
| **Identifier** | Cluster identifier | Workgroup name |
| **Audit logging** | S3 or CloudWatch | CloudWatch only |
| **Parameter groups** | Required to enable user activity logging | Not used — configure on the workgroup directly |

Expand

Show lessSee more
