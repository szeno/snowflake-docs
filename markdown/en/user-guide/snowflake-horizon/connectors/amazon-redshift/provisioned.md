# Redshift provisioned cluster

This guide walks through connecting a Redshift provisioned cluster to Horizon Catalog.
The connector uses a customer-owned IAM role to discover the cluster endpoint, read audit logs,
and query Redshift system views for metadata and lineage.

Note

This deployment type uses a **`horizoncatalog` database user** that you create in Step 4. It is
different from Redshift Serverless, which uses an auto-created `IAMR:<role-name>` user instead.

## Prerequisites

- Access to an AWS user with permission to modify IAM, Redshift parameter groups, and the cluster.
- Access to the Redshift cluster as an admin user.
- Open the Horizon Catalog connector wizard in another browser tab: sign in to Snowflake, go to
  **Catalog > Connections**, and select **Redshift**. You’ll need the **IAM Principal** and
  **External ID** values shown in the **Authorize AWS access** step when you create the IAM role in Step 5.

## 1. Create a new data source

In Snowflake, open **Catalog > Connections** and select **Redshift** from the list of connectors.
You will go through a 4-step wizard: **Select a connection → Add data source → Authorize AWS access → Select databases**.

In the **Add data source** step, fill in the following fields:

| Field | Value |
| --- | --- |
| **Connection** | Redshift |
| **Display Name** | A name for this data source (for example, `Redshift`) |
| **Instance type** | Provisioned |
| **Cluster Name** | The AWS cluster identifier (for example, `redshift-cluster-1`) |
| **Database** | The name of the database to ingest |
| **Region** | The region where the cluster runs (for example, `us-east-2`) |
| **Snowflake Database** | The Snowflake database where metadata is stored (for example, `CONNECTORS`) |
| **Snowflake Schema** | The Snowflake schema where metadata is stored (for example, `METADATA`) |

Expand

Show lessSee more

## 2. Enable audit logging

Horizon Catalog reads connection and user activity logs from your cluster’s audit logs. Enable
audit logging on the cluster and choose where Redshift delivers the logs. Horizon Catalog
auto-detects the destination, so you only need to configure one.

1. In the Redshift console, go to **Clusters** and select your cluster.
2. Open the **Properties** tab, scroll to **Database configurations**, select **Edit**, then choose **Edit audit logging** from the dropdown menu.
3. Turn on **Configure audit logging**, then choose a log export type:
   - **CloudWatch**: Redshift delivers audit logs directly to Amazon CloudWatch Logs, with no S3 bucket to manage. AWS recommends this option.
   - **S3 bucket**: Redshift writes audit logs to an S3 bucket you specify. Select an existing bucket or create a new one.
4. Select **Save changes**.

For details, see [Database audit logging](https://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html) in the AWS documentation.

## 3. Enable user activity logging

The user activity log is where Redshift records the SQL statements that Horizon Catalog uses to
build popularity and lineage. Enabling audit logging in Step 2 captures the connection log and user
log, but the user activity log is produced only when you also set the `enable_user_activity_logging`
parameter to `true` in the cluster’s parameter group.

Note

This step uses a Redshift parameter group. Default parameter groups are read-only — if your cluster
uses `default.redshift-*`, create a custom one first.

1. In the Redshift console, go to **Parameter groups** and create a custom group if needed:

   - Base it on the same family as the existing group.
   - Apply the new group to your cluster under **Clusters > Modify > Parameter group**.
2. Open the custom parameter group and set:

   | Parameter | Value |
   | --- | --- |
   | `enable_user_activity_logging` | `true` |

   Expand

   Show lessSee more
3. Reboot the cluster if the parameter group change requires it.

For details, see [Managing parameter groups](https://docs.aws.amazon.com/redshift/latest/mgmt/managing-parameter-groups-console.html) in the AWS documentation.

## 4. Create the Horizon Catalog database user

Connect to each database you want to ingest and run:

Copy code

```
CREATE USER horizoncatalog WITH PASSWORD DISABLE syslog ACCESS UNRESTRICTED;
GRANT SELECT ON SVV_TABLE_INFO TO horizoncatalog;
GRANT SELECT ON SVV_TABLES TO horizoncatalog;
GRANT SELECT ON SVV_COLUMNS TO horizoncatalog;
GRANT SELECT ON STL_QUERYTEXT TO horizoncatalog;
GRANT SELECT ON STL_DDLTEXT TO horizoncatalog;
GRANT SELECT ON STL_QUERY TO horizoncatalog;
```

Note

`syslog ACCESS UNRESTRICTED` is required so Horizon Catalog can read `SYS_QUERY_HISTORY` and
`SYS_PROCEDURE_CALL`, which are used to build lineage for queries executed inside stored procedures.

Repeat in **every database** you select in the wizard. The grants are database-scoped — running them in one database does not apply to others.

## 5. Create an IAM role

Horizon Catalog uses a customer-owned IAM role that it assumes to access the cluster and its logs.
In the AWS IAM console, go to **Roles** and select **Create role**, then add a custom trust policy
and an inline permission policy as follows.

### 5a. Trust policy

In the Horizon Catalog wizard, go to the **Authorize AWS access** step. Horizon Catalog
pre-generates two values you must copy into the trust policy:

- **External ID** — a unique token generated per data source
- **IAM Principal** — the Horizon Catalog AWS principal that will assume your role

For **Trusted entity type**, select **Custom trust policy** and paste the following, substituting the
**IAM Principal** and **External ID** values from the wizard:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "<IAM Principal from wizard>" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "sts:ExternalId": "<External ID from wizard>" }
      }
    }
  ]
}
```

Caution

The **External ID is unique per data source** — it is regenerated each time a new connection is
created. If you recreate the data source in another environment, copy the new External ID from the
wizard and update the trust policy to match.

### 5b. Permission policy

Select **Next**. On the **Add permissions** step, select **Create inline policy**, then open the
**JSON** editor and paste the following. Replace `{region_id}`, `{account_id}`, `{cluster_name}`,
and `{bucket}` with your values:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RedshiftClusterAccess",
      "Effect": "Allow",
      "Action": [
        "redshift:DescribeClusters",
        "redshift:DescribeLoggingStatus",
        "redshift:GetClusterCredentials"
      ],
      "Resource": [
        "arn:aws:redshift:{region_id}:{account_id}:cluster:{cluster_name}",
        "arn:aws:redshift:{region_id}:{account_id}:dbuser:{cluster_name}/horizoncatalog",
        "arn:aws:redshift:{region_id}:{account_id}:dbname:{cluster_name}/*"
      ]
    },
    {
      "Sid": "S3AuditLogAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:GetBucketLogging",
        "s3:GetBucketAcl",
        "s3:GetBucketPolicy",
        "s3:GetBucketVersioning",
        "s3:GetBucketPublicAccessBlock",
        "s3:GetBucketTagging",
        "s3:GetObjectVersion",
        "s3:GetObjectVersionTagging",
        "s3:ListBucketVersions",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:GetInventoryConfiguration",
        "s3:GetLifecycleConfiguration",
        "s3:GetBucketOwnershipControls",
        "s3:GetBucketPolicyStatus"
      ],
      "Resource": ["arn:aws:s3:::{bucket}", "arn:aws:s3:::{bucket}/*"]
    },
    {
      "Sid": "CloudWatchLogsAccess",
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogGroups",
        "logs:StartQuery",
        "logs:GetQueryResults"
      ],
      "Resource": "*"
    }
  ]
}
```

Note

The `S3AuditLogAccess` block is only needed if you chose **S3 bucket** as the log export type in
Step 2. If you chose **CloudWatch**, omit the S3 block and keep only `RedshiftClusterAccess` and
`CloudWatchLogsAccess`.

Enter a name and description for the role, then select **Create role**. For example:

- **Role name:** `SnowflakeHorizon-Redshift`
- **Description:** `IAM role used to connect Horizon Catalog to Amazon Redshift`

Caution

The role name must start with the `SnowflakeHorizon-` prefix, or the role must be created under the
`SnowflakeHorizon/` path — Horizon Catalog rejects role ARNs that don’t meet this requirement. Valid
ARNs look like `arn:aws:iam::123456789012:role/SnowflakeHorizon-Redshift` or
`arn:aws:iam::123456789012:role/SnowflakeHorizon/Redshift`.

Open the role’s summary page and copy the role ARN — you paste it into the wizard in Step 6.

## 6. Confirm authorization and choose databases

Return to the **Authorize AWS access** step in the Horizon Catalog wizard. The **External ID**
and **IAM Principal** fields are already pre-filled. Paste the Role ARN from Step 5 into the
**Role ARN** field and select **Next**.

In the **Select databases** step, choose the databases and schemas you want Horizon Catalog to
crawl, then select **Done**.

Initial metadata typically appears within a few minutes. Popularity and lineage can take 24–48 hours
as query log history accumulates.

## 7. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| `AccessDenied` on `sts:AssumeRole` | Trust-policy principal or External ID mismatch | Step 5a — re-copy from the wizard |
| `AccessDenied` on `redshift:DescribeClusters` | Permission policy missing or wrong cluster ARN | Step 5b |
| No query logs appearing | Audit logging not enabled or user activity logging off | Steps 2 and 3 |
| `No database found` | `horizoncatalog` user lacks `CONNECT` on the database | Step 4 |
| Access denied to `svv_table_info` on a database | `GRANT` statements from Step 4 were not run in every selected database; grants are database-scoped | Re-connect to each affected database and re-run the `GRANT SELECT` statements from Step 4 |

Expand

Show lessSee more
