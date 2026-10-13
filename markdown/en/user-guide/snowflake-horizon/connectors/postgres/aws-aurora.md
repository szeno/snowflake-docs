# AWS Aurora PostgreSQL

Aurora flavor

This guide applies to Aurora PostgreSQL-compatible.

## Overview

Horizon Catalog ingests Aurora PostgreSQL metadata and query logs. Metadata comes from a
direct database connection using a dedicated read-only service account; query logs are fetched
from Amazon CloudWatch via a cross-account IAM role that Horizon Catalog assumes.

By the time you finish this guide you’ll have:

1. A read-only PostgreSQL user dedicated to Horizon Catalog.
2. Network connectivity between your Aurora cluster and the Horizon Catalog service.
3. PostgreSQL query logs exported from the Aurora cluster to CloudWatch.
4. A cross-account IAM role Horizon Catalog can assume with permission to describe the cluster and read its log group.
5. An active connector in the Horizon Catalog UI that uses all of the above.

Steps 1–4 happen in AWS and are covered in detail below. Step 5 is the UI wrap-up described
at the end.

## Prerequisites

- Access to an AWS user with permission to modify IAM, Aurora cluster parameter groups,
  Aurora instance parameter groups, and the Aurora cluster/instances themselves.
- Access to the Aurora cluster’s writer endpoint as a superuser (typically the `postgres`
  user you set at cluster-creation time).
- Open Horizon Catalog connector in another browser tab. To reach it, sign in
  to Snowflake, open **Catalog > Connections**, pick **PostgreSQL** from the list
  (the same connector is used for Aurora PostgreSQL-compatible).
  There are two values you’ll need to paste into the IAM role in Step 4:
  - **IAM Principal**: The ARN of the Horizon Catalog service role that will assume
    your role. Copy it verbatim.
  - **External ID**: A per-connector secret starting with `sf_horizon_` (for example,
    `sf_horizon_Abc123…`). Horizon Catalog rejects External IDs that don’t match
    this prefix. Don’t regenerate or rewrite it.

## 1. Create a PostgreSQL user for Horizon Catalog

Connect to the cluster writer endpoint as a superuser and create a dedicated service account.
Replace the password with a strong secret; store it in your secrets manager and paste it into the
Horizon Catalog wizard when prompted.

Copy code

```
CREATE USER snowflake_horizon WITH ENCRYPTED PASSWORD '<password>';
```

For each database you want Horizon Catalog to crawl, connect as a superuser and grant the
service account access:

Copy code

```
GRANT CONNECT ON DATABASE <database_name> TO snowflake_horizon;
```

Then connect to that database (`\c <database_name>` in psql) and grant access to each
schema:

Copy code

```
GRANT USAGE ON SCHEMA <schema_name> TO snowflake_horizon;
ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO snowflake_horizon;
```

Repeat per database and per schema. Horizon Catalog won’t read metadata from schemas
the service account can’t access.

## 2. Ensure network connectivity

Horizon Catalog connects to your Aurora cluster over the public internet. The Aurora cluster writer
endpoint must be publicly reachable — either with **Publicly accessible = Yes** on the cluster,
or by fronting it with an internet-facing load balancer or proxy you control. Open the security
group (or firewall) on that path to allow inbound TCP on the PostgreSQL port (default 5432).

Allowlisting specific IPs

Horizon Catalog doesn’t guarantee stable egress IP addresses. The egress IPs it connects from
can change at any time without notice. If your security posture requires pinning the ingress
rule to Horizon Catalog’s egress IPs instead of allowing `0.0.0.0/0` on the PostgreSQL port,
contact Snowflake support for the egress IPs currently in use, and expect to update that
allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 3. Enable query logging to CloudWatch

Aurora exports logs to CloudWatch at the cluster level, but the logging parameters themselves
are usually tuned at the instance parameter group level. Both pieces have to be configured.

### 3a. Enable log export on the cluster

1. In the RDS console, go to **Databases**, select the DB cluster
   (not a writer/reader instance), then select **Modify**.
2. Scroll to **Log exports** and tick **PostgreSQL log**.
3. Scroll to the bottom, choose **Apply immediately**, review, and save.

Note

Enabling log export creates the log group shell but the group stays
empty until the logging parameters in Steps 3b–3d are applied and the instances
start writing statements. Don’t be alarmed if the log group is missing or
empty before Step 3e.

### 3b. Create a custom DB parameter group (if needed)

Default parameter groups are read-only. If the cluster’s writer/reader instances currently use
`default.aurora-postgresql*`, create a custom instance-level parameter group.

1. In the RDS console, go to **Parameter groups > Create parameter group**.
2. Type: **DB parameter group** (not “DB cluster parameter group”:
   `log_statement` and `log_min_duration_statement` apply per-instance for Aurora PostgreSQL).
3. Family: `aurora-postgresql<version>`.
4. Name: for example, `snowflake_horizon-aurora-pg`. Select **Create**.

### 3c. Set logging parameters

1. Open the parameter group from Step 3b (or the existing custom group
   if you already have one).
2. Select **Edit parameters** and set:

   | Parameter | Value | Notes |
   | --- | --- | --- |
   | `log_statement` | `all` | Log every SQL statement. |
   | `log_min_duration_statement` | `0` | Log duration for every statement, regardless of length. |

   Expand

   Show lessSee more
3. **Save changes**.

### 3d. Attach the parameter group

1. In the RDS console, go to **Databases**, select each writer/reader instance
   in the cluster (not the cluster itself).
2. Select **Modify** for the instance.
3. Under **Additional configuration > DB parameter group**, pick
   the custom group from Step 3b.
4. Choose **Apply immediately**, review, and save. This triggers an
   instance reboot. Repeat for each instance in the cluster.

Subsequent changes to parameters within the group are dynamic and take effect without
another reboot.

### 3e. Verify

Once the instances are back, run any query against the cluster and check that the log group
`/aws/rds/cluster/<CLUSTER_IDENTIFIER>/postgresql` exists in CloudWatch Logs in
the same region, and that recent streams contain messages. Horizon Catalog will refuse the
connector during the UI authorization step if it can’t find a populated log group.

## 4. Create the cross-account IAM role

Horizon Catalog’s service role assumes a customer-owned IAM role in your account to describe
the Aurora cluster and read its CloudWatch log group. This step creates that role and its access
policy.

### 4a. Decide the role name

The role name must match one of the two forms Horizon Catalog’s validator accepts. Pick the
one that fits how you’re creating the role.

| Form | Example | When to use |
| --- | --- | --- |
| Role name prefix | `SnowflakeHorizon-aurora-pg-prod` | AWS Console: the console doesn’t expose the Path field. |
| Path-based | path `/SnowflakeHorizon/`, name `aurora-pg-prod` | API, CLI, or Terraform. |

Expand

Show lessSee more

Anything else (`SnowflakeHorizonOther`, `SnowflakeHorizon_foo`, a bare name) is
rejected by Horizon Catalog during Step 5 even if the AWS role exists.

### 4b. Trust policy

Create the role with this trust policy. Paste the **IAM Principal** and **External ID** values from the
Horizon Catalog wizard.

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "<IAM_PRINCIPAL_FROM_UI>" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "sts:ExternalId": "<EXTERNAL_ID_FROM_UI>" }
      }
    }
  ]
}
```

**AWS Console**: IAM > Roles > Create role > Trusted entity: Custom trust policy > paste
the JSON > skip permissions (attached in Step 4c) > Name: `SnowflakeHorizon-<suffix>`

> Create role.

**AWS CLI**:

Copy code

```
aws iam create-role \
  --role-name aurora-pg-test-instance \
  --path /SnowflakeHorizon/ \
  --assume-role-policy-document file://trust-policy.json
```

### 4c. Access policy

Attach the following policy inline to the role. Replace the placeholders:

- `<AWS_REGION>`: Region of the Aurora cluster.
- `<AWS_ACCOUNT_ID>`: Your 12-digit AWS account ID.
- `<CLUSTER_IDENTIFIER>`: The Aurora DB cluster identifier.

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DescribeAuroraCluster",
      "Effect": "Allow",
      "Action": [
        "rds:List*",
        "rds:Describe*",
        "rds:Get*"
      ],
      "Resource": "arn:aws:rds:<AWS_REGION>:<AWS_ACCOUNT_ID>:db:<CLUSTER_IDENTIFIER>"
    },
    {
      "Sid": "ReadClusterLogs",
      "Effect": "Allow",
      "Action": [
        "logs:Get*",
        "logs:List*",
        "logs:StartQuery",
        "logs:StopQuery",
        "logs:Describe*",
        "logs:FilterLogEvents"
      ],
      "Resource": "arn:aws:logs:<AWS_REGION>:<AWS_ACCOUNT_ID>:log-group:/aws/rds/cluster/<CLUSTER_IDENTIFIER>/*:*"
    },
    {
      "Sid": "QueryResultAndLogGroupDiscovery",
      "Effect": "Allow",
      "Action": [
        "logs:GetQueryResults",
        "logs:DescribeLogGroups"
      ],
      "Resource": "arn:aws:logs:*:*:log-group::log-stream:"
    }
  ]
}
```

**AWS Console**: Open the role > Add permissions > Create inline policy > JSON tab >
paste > Review > name it `EnableSnowflakeHorizon` > Create policy.

**AWS CLI**:

Copy code

```
aws iam put-role-policy \
  --role-name <role-name> \
  --policy-name EnableSnowflakeHorizon \
  --policy-document file://access-policy.json
```

### 4d. Copy the role ARN

Note the role ARN from the IAM console (for example,
`arn:aws:iam::123456789012:role/SnowflakeHorizon-aurora-pg-prod`). You will
paste it into the Horizon Catalog UI in Step 5.

## 5. Finish in the Horizon Catalog UI

Back in the Horizon Catalog connector wizard, complete the connector:

1. **Source type**: PostgreSQL (the same connector is used for Aurora
   PostgreSQL-compatible).
2. **Connection details**: Use the cluster writer endpoint as the
   hostname, port (5432 unless overridden), database name, and the `snowflake_horizon` user
   - password from Step 1.
3. **Authorization**: Paste the Role ARN from Step 4d, the AWS
   Region, and the Cluster identifier (shown as “instance/cluster name” in some UI
   versions).
4. **Log type**: `aurora` (not `rds`). This selects the
   `/aws/rds/cluster/…` log group layout on the Horizon Catalog side.
5. Select **Test connection**, then **Save**, then select the databases
   and schemas you want crawled.

A successful test confirms that Horizon Catalog could (a) assume the IAM role using the
External ID, (b) describe the Aurora cluster, (c) read the CloudWatch log group, and (d) log in as
the PostgreSQL user. Failures map back to Step 4, Step 4, Step 3, and Step 1 respectively.

Initial metadata typically appears within a few minutes; popularity and lineage can take 24–48
hours as query log history accumulates.

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| UI rejects Role ARN | Role name doesn’t match `SnowflakeHorizon-*` or `/SnowflakeHorizon/` | Step 4a |
| `AccessDenied` on `sts:AssumeRole` | Trust-policy principal or External ID mismatch | Step 4b: re-copy from the wizard |
| UI says “no query log found” | Log export not enabled on the cluster or parameter group not applied on instances | Step 3a/3d/3e |
| Authentication failed for user `snowflake_horizon` | Wrong password, or user lacks `CONNECT` on the database | Step 1 |
| Connection timeout to cluster writer | Cluster writer endpoint not publicly reachable, or IP allowlist out of date | Step 2: confirm with Snowflake support |

Expand

Show lessSee more

## Differences from RDS for PostgreSQL

| Concern | RDS for PostgreSQL | Aurora PostgreSQL |
| --- | --- | --- |
| Log group path | `/aws/rds/instance/<DB_ID>/*` | `/aws/rds/cluster/<CLUSTER_ID>/*` |
| Where to enable log export | DB instance Modify page | DB cluster Modify page |
| Where to set log parameters | DB parameter group (on the instance) | DB parameter group (on each Aurora instance in the cluster) |
| Host used by the connector | Instance endpoint | Cluster writer endpoint |
| Horizon Catalog `log_type` | `rds` | `aurora` |

Expand

Show lessSee more

## Connection security

Horizon Catalog uses a TLS-capable PostgreSQL client. If your Aurora cluster is configured to
accept TLS connections, the connection is encrypted automatically. However, if TLS is not
available on the cluster, the connection proceeds unencrypted.

You are responsible for enabling TLS on your database cluster

Snowflake strongly recommends enforcing TLS 1.2 or higher on your Aurora PostgreSQL cluster.
Set the following parameters in the DB cluster parameter group:

| Parameter | Recommended value | Effect |
| --- | --- | --- |
| `rds.force_ssl` | `1` | Reject any connection that does not use TLS. |
| `ssl_min_protocol_version` | `TLSv1.2` | Refuse TLS versions older than 1.2. |

Expand

Show lessSee more

After applying these settings, Horizon Catalog connects over TLS without any changes on the
connector side.

For more details on the shared-responsibility model for Horizon Catalog connectors,
see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Sensitive data in logs

The logging setup above may record statement text, including literal values that could contain
sensitive data. Review AWS’s guidance on [PostgreSQL cleartext logging](https://aws.amazon.com/premiumsupport/knowledge-center/rds-postgresql-cleartext-logging/) to assess impact and
apply redaction or filtering that matches your organization’s policies.
