# AWS RDS PostgreSQL

## Overview

Horizon Catalog ingests PostgreSQL metadata and query logs. Metadata comes from a direct
database connection using a dedicated read-only service account; query logs are fetched from
Amazon CloudWatch via a cross-account IAM role that Horizon Catalog assumes. By the time
you finish this guide you’ll have:

1. A read-only PostgreSQL user dedicated to Horizon Catalog.
2. Network connectivity between your RDS instance and the Horizon Catalog service.
3. PostgreSQL query logs exported to CloudWatch.
4. A cross-account IAM role Horizon Catalog can assume with permission to describe the instance and read its log group.
5. An active connector in the Horizon Catalog UI that uses all of the above.

Steps 1–4 happen in AWS and are covered in detail below. Step 5 is the UI wrap-up described
at the end.

## Prerequisites

- Access to an AWS user with permission to modify IAM, RDS parameter groups, and the
  RDS instance itself.
- Access to the RDS instance as an admin or superuser (the account you use to connect
  via `psql`).
- Open Horizon Catalog connector in another browser tab. To reach it, sign in
  to Snowflake, open **Catalog > Connections**, pick **PostgreSQL** from the list.
  There are two values you’ll need to paste into the IAM role in Step 4:
  - **IAM Principal**: The ARN of the Horizon Catalog service role that will assume
    your role. Copy it verbatim.
  - **External ID**: A per-connector secret starting with `sf_horizon_` (for example,
    `sf_horizon_Abc123…`). Horizon Catalog rejects External IDs that don’t match
    this prefix. Don’t regenerate or rewrite it.

## 1. Create a PostgreSQL user for Horizon Catalog

Connect to the instance with an administrative user and create a dedicated,
password-authenticated service account. Replace the password with a strong secret; store it in
your secrets manager and paste it into the Horizon Catalog wizard when prompted.

Copy code

```
CREATE USER snowflake_horizon WITH ENCRYPTED PASSWORD '<password>';
```

For each database you want Horizon Catalog to crawl, connect as an admin and grant the
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

Why the grants are narrow

Horizon Catalog’s PostgreSQL crawler uses `information_schema` and `pg_catalog` for structure.
Standard PostgreSQL exposes those to every role without explicit grants. The statements above are the
minimum needed on top of that to let Horizon Catalog see user-created schemas.

## 2. Ensure network connectivity

Horizon Catalog connects to your RDS instance over the public internet. The instance must be
publicly reachable — either with **Publicly accessible = Yes** on the RDS instance itself, or sitting
behind an internet-facing load balancer or proxy you control. Open the security group (or firewall)
attached to the RDS instance (or the proxy in front of it) and allow inbound TCP on the
PostgreSQL port (default 5432) from the internet.

About egress IPs

Horizon Catalog doesn’t guarantee stable egress IPs. The egress IPs it connects from can change
at any time without notice. If you’d rather allowlist specific CIDRs on the PostgreSQL port
instead of allowing `0.0.0.0/0`, contact Snowflake support for the egress IPs currently in use,
and expect to update that allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 3. Enable query logging to CloudWatch

Query logs drive lineage and popularity in Horizon Catalog. RDS for PostgreSQL doesn’t log
statements by default, and even when it does, it only ships them to CloudWatch once you
explicitly enable the PostgreSQL log export. Both pieces have to be turned on.

### 3a. Create a custom parameter group (if needed)

Default parameter groups are read-only. If the instance currently uses
`default.postgres*`, create a custom group first.

1. In the RDS console, go to **Parameter groups > Create parameter group**.
2. Give it a name (for example, `snowflake_horizon-postgres`), pick the parameter
   group family matching your PostgreSQL major version (for example, `postgres15`), and select
   **Create**.

### 3b. Set logging parameters

1. Open the parameter group from Step 3a (or the existing custom group
   if you already have one).
2. Select **Edit parameters** and set:

   | Parameter | Value | Notes |
   | --- | --- | --- |
   | `log_statement` | `all` | Log every SQL statement. |
   | `log_min_duration_statement` | `0` | Log duration for every statement, regardless of length. |

   Expand

   Show lessSee more
3. **Save changes**. These parameters are dynamic, so no reboot is needed
   if the group is already attached to the instance.

### 3c. Attach the parameter group and enable log export

1. In the RDS console, go to **Databases**, select your instance, then select **Modify**.
2. Under **Database options > DB parameter group**, select the
   custom group from Step 3a. Skip this if the group was already attached.
3. Scroll to **Log exports** and tick **PostgreSQL log**. (Also tick
   **Upgrade log** if you want upgrade events captured.)
4. Scroll to the bottom, choose **Apply immediately** (otherwise the
   change waits for the next maintenance window), review, and save.

Attaching a newly-associated parameter group triggers a reboot. If the group was already
attached and you only changed the logging parameters, no reboot is needed.

### 3d. Verify

Once the change has applied, run any query against the database and then check that the log
group `/aws/rds/instance/<DB_IDENTIFIER>/postgresql` exists in CloudWatch Logs in
the same region as the instance, and that recent streams contain messages. Horizon Catalog
will refuse the connector during the UI authorization step if it can’t find a populated log group.

## 4. Create the cross-account IAM role

Horizon Catalog’s service role assumes a customer-owned IAM role in your account to read the
CloudWatch log group. This step creates that role and its access policy.

### 4a. Decide the role name

The role name must match one of the two forms Horizon Catalog’s validator accepts. Pick the
one that fits how you’re creating the role.

| Form | Example | When to use |
| --- | --- | --- |
| Role name prefix | `SnowflakeHorizon-rds-postgres-prod` | AWS Console: the console doesn’t expose the Path field, so this is the only form you can set through the UI. |
| Path-based | path `/SnowflakeHorizon/`, name `rds-postgres-prod` | API, CLI, or Terraform: any tool that lets you set Path. |

Expand

Show lessSee more

Anything else (`SnowflakeHorizonOther`, `SnowflakeHorizon_foo`, a bare name) will be
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

**AWS CLI** (supports the path form):

Copy code

```
aws iam create-role \
  --role-name rds-postgres-prod \
  --path /SnowflakeHorizon/ \
  --assume-role-policy-document file://trust-policy.json
```

### 4c. Access policy

Attach the following policy inline to the role. Replace the placeholders with your values:

- `<AWS_REGION>`: Region of the RDS instance (for example, `us-east-2`).
- `<AWS_ACCOUNT_ID>`: Your 12-digit AWS account ID.
- `<DB_IDENTIFIER>`: The RDS DB identifier.

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DescribeRdsInstance",
      "Effect": "Allow",
      "Action": [
        "rds:List*",
        "rds:Describe*",
        "rds:Get*"
      ],
      "Resource": "arn:aws:rds:<AWS_REGION>:<AWS_ACCOUNT_ID>:db:<DB_IDENTIFIER>"
    },
    {
      "Sid": "ReadEngineLogs",
      "Effect": "Allow",
      "Action": [
        "logs:Get*",
        "logs:List*",
        "logs:StartQuery",
        "logs:StopQuery",
        "logs:Describe*",
        "logs:FilterLogEvents"
      ],
      "Resource": "arn:aws:logs:<AWS_REGION>:<AWS_ACCOUNT_ID>:log-group:/aws/rds/instance/<DB_IDENTIFIER>/*:*"
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
`arn:aws:iam::123456789012:role/SnowflakeHorizon-rds-postgres-prod`). You
will paste it into the Horizon Catalog UI in Step 5.

## 5. Finish in the Horizon Catalog UI

Back in the Horizon Catalog connector wizard, complete the connector:

1. **Source type**: PostgreSQL.
2. **Connection details**: hostname, port (5432 unless overridden),
   database name, and the `snowflake_horizon` user + password from Step 1.
3. **Authorization**: paste the Role ARN from Step 4d, the AWS
   Region, and the DB identifier.
4. **Log type**: `rds`.
5. Select **Test connection**, then **Save**, then select the databases
   and schemas you want crawled.

A successful test confirms that Horizon Catalog could (a) assume the IAM role using the
External ID, (b) describe the RDS instance, (c) discover the CloudWatch log group, and (d) log
in as the PostgreSQL user. Failures map back to Step 4, Step 4, Step 3, and Step 1
respectively.

Initial metadata typically appears within a few minutes; popularity and lineage can take 24–48
hours as query log history accumulates.

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| UI rejects Role ARN | Role name doesn’t match `SnowflakeHorizon-*` or `/SnowflakeHorizon/` | Step 4a |
| `AccessDenied` on `sts:AssumeRole` | Trust-policy principal or External ID mismatch | Step 4b: re-copy from the wizard |
| UI says “no query log found” | Log export not enabled or parameter group not applied | Step 3c/3d |
| Authentication failed for user `snowflake_horizon` | Wrong password or user lacks `CONNECT` on the database | Step 1 |
| Connection timeout to DB | Instance not publicly reachable, or IP allowlist out of date | Step 2: confirm with Snowflake support |

Expand

Show lessSee more

## Connection security

Horizon Catalog uses a TLS-capable PostgreSQL client. If your RDS instance is configured to
accept TLS connections, the connection is encrypted automatically. However, if TLS is not
available on the server, the connection proceeds unencrypted.

You are responsible for enabling TLS on your database instance

Snowflake strongly recommends enforcing TLS 1.2 or higher on your RDS instance. For RDS
PostgreSQL, set the following parameters in the DB parameter group:

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
