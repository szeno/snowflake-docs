# Redshift Serverless workgroup

This guide walks through connecting a Redshift Serverless workgroup to Horizon Catalog.
The connector uses a customer-owned IAM role to discover the workgroup endpoint, read CloudWatch
audit logs, and query Redshift system views for metadata and lineage.

Note

This deployment type uses an auto-created **`IAMR:<role-name>` database user** (not a
`horizoncatalog` user). Redshift creates this user when the database list loads in Step 4; you
grant permissions to it in Step 5.

## Prerequisites

- Access to an AWS user with permission to modify IAM and Redshift Serverless workgroups.
- Access to the Redshift workgroup as an admin user.
- Open the Horizon Catalog connector wizard in another browser tab: sign in to Snowflake, go to
  **Catalog > Connections**, and select **Redshift**. You’ll need the **IAM Principal** and
  **External ID** values shown in the **Authorize AWS access** step when you create the IAM role in Step 3.

## 1. Create a new data source

In Snowflake, open **Catalog > Connections** and select **Redshift** from the list of connectors.
You will go through a 4-step wizard: **Select a connection → Add data source → Authorize AWS access → Select databases**.

In the **Add data source** step, fill in the following fields:

| Field | Value |
| --- | --- |
| **Connection** | Redshift |
| **Display Name** | A name for this data source (for example, `My Redshift - Serverless`) |
| **Instance type** | Serverless |
| **Workgroup name** | The name of your Redshift Serverless workgroup (for example, `my-workgroup`) |
| **Database** | The name of the database to ingest |
| **Region** | The region where the workgroup runs (for example, `us-east-2`) |
| **Snowflake Database** | The Snowflake database where metadata is stored (for example, `CONNECTORS`) |
| **Snowflake Schema** | The Snowflake schema where metadata is stored (for example, `METADATA`) |

Expand

Show lessSee more

Note

The connector uses the workgroup name to auto-discover the endpoint. You do not need to provide a
host or port.

## 2. Enable audit logging

Redshift Serverless exports audit logs from the namespace configuration, not the workgroup. Enable
the user log and user activity log so Horizon Catalog can read query history from CloudWatch.

1. Go to **Amazon Redshift Serverless > Namespace configuration** and select your namespace.
2. Open the **Security and encryption** tab. In the **Security and encryption** section, select **Edit**.
3. Select the following log exports, then save:
   - **User log**
   - **User activity log**

After you choose which logs to export, Amazon Redshift Serverless delivers them to Amazon CloudWatch
Logs. A new log group is created for each log type, where `<log_type>` is the exported log (for
example, `useractivitylog`):

Copy code

```
/aws/redshift/<namespace>/<log_type>
```

Note

Horizon Catalog reads query logs exclusively from CloudWatch for Redshift Serverless. S3 audit
logging is not supported.

## 3. Create an IAM role

Horizon Catalog uses a customer-owned IAM role that it assumes to access the workgroup and its
CloudWatch logs. In the AWS IAM console, go to **Roles** and select **Create role**, then add a
custom trust policy and an inline permission policy as follows.

### 3a. Trust policy

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

### 3b. Permission policy

Select **Next**. On the **Add permissions** step, select **Create inline policy**, then open the
**JSON** editor and paste the following. Replace `{region_id}`, `{account_id}`, and
`{workgroup_name}` with your values:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RedshiftServerlessAccess",
      "Effect": "Allow",
      "Action": [
        "redshift-serverless:GetWorkgroup",
        "redshift-serverless:GetCredentials"
      ],
      "Resource": "arn:aws:redshift-serverless:{region_id}:{account_id}:workgroup/*"
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

| Permission | Purpose |
| --- | --- |
| `redshift-serverless:GetWorkgroup` | Required on every connection to discover the workgroup endpoint and the namespace that backs it. The namespace determines the CloudWatch log group (`/aws/redshift/<namespace>/useractivitylog`) that Horizon Catalog reads query history from. |
| `redshift-serverless:GetCredentials` | Obtains temporary database credentials |
| `logs:DescribeLogGroups`, `logs:StartQuery`, `logs:GetQueryResults` | Reads the CloudWatch user activity log group |

Expand

Show lessSee more

Enter a name and description for the role, then select **Create role**. For example:

- **Role name:** `SnowflakeHorizon-Redshift`
- **Description:** `IAM role used to connect Horizon Catalog to Amazon Redshift`

Caution

The role name must start with the `SnowflakeHorizon-` prefix, or the role must be created under the
`SnowflakeHorizon/` path — Horizon Catalog rejects role ARNs that don’t meet this requirement. Valid
ARNs look like `arn:aws:iam::123456789012:role/SnowflakeHorizon-Redshift` or
`arn:aws:iam::123456789012:role/SnowflakeHorizon/Redshift`.

Open the role’s summary page and copy the role ARN — you paste it into the wizard in Step 4.

## 4. Confirm authorization and choose databases

Return to the **Authorize AWS access** step in the Horizon Catalog wizard. The **External ID**
and **IAM Principal** fields are already pre-filled. Paste the Role ARN from Step 3 into the
**Role ARN** field and select **Next**.

The **Select databases** step will open and load the list of available databases. When the list
appears, Redshift has automatically created the `IAMR:<role-name>` database user for the first
time. **Pause here — do not select Done yet.** Continue to Step 5 to run the grants before
ingestion fires.

Caution

You must complete Step 5 (grant `SELECT` on system views to `IAMR:<role-name>` in every database)
**before** selecting **Done** in the wizard. If you finish the wizard first, ingestion can start
before the grants are in place and metadata ingestion will fail.

## 5. Grant permissions to the connector’s database user

With the wizard still open on the **Select databases** step, open Redshift Query Editor v2 in
another browser tab. Connect to each database you plan to select as an admin user (for example,
`awsuser`) and run:

Copy code

```
GRANT SELECT ON SVV_TABLE_INFO TO "IAMR:<role-name>";
GRANT SELECT ON SVV_TABLES TO "IAMR:<role-name>";
GRANT SELECT ON SVV_COLUMNS TO "IAMR:<role-name>";
```

Replace `<role-name>` with the name of the IAM role created in Step 3 (for example,
`SnowflakeHorizon-Redshift`). The double quotes are required because of the colon in the username.

Note

Unlike provisioned clusters, Redshift Serverless does not use a `horizoncatalog` database user.
The `IAMR:<role-name>` user is auto-created by Redshift when the database list loads in Step 4,
and is the user that must receive the grants.

Repeat in **every database** you plan to select in the wizard. The grants are database-scoped —
running them in one database does not apply to others.

Once all grants are applied, return to the wizard, select the databases and schemas you want
Horizon Catalog to crawl, and select **Done**. The connector is saved and the first ingestion
starts automatically.

Initial metadata typically appears within a few minutes. Popularity and lineage can take 24–48 hours
as query log history accumulates.

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| `AccessDenied` on `sts:AssumeRole` | Trust-policy principal or External ID mismatch | Step 3a — re-copy from the wizard |
| `AccessDenied` on `redshift-serverless:GetWorkgroup` | Permission policy missing or wrong workgroup ARN | Step 3b |
| No query logs appearing | User log or user activity log not enabled on the namespace | Step 2 |
| CloudWatch log group not found | Logging enabled but no queries run yet, or wrong namespace | Verify the log group `/aws/redshift/<namespace>/useractivitylog` exists in CloudWatch |
| Access denied to `svv_table_info` on a database | `GRANT` statements from Step 5 were not run in every selected database, or the `IAMR:<role-name>` user has not been auto-created yet (connector not saved) | Complete Step 4 first, then re-run the `GRANT SELECT` statements from Step 5 in each database |

Expand

Show lessSee more
