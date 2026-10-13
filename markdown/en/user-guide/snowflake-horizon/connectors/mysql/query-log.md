# Query Logs

Available query log sources for MySQL data sources:

- **None**: Metadata only; lineage and popularity disabled.
- **CloudWatch Logs** (`cloudwatch`): The MySQL general query log exported to CloudWatch Logs on
  Amazon RDS, read by Horizon Catalog through a cross-account IAM role. Described below.

Why there's no system log source for MySQL

Unlike the SQL Server and Oracle connectors, MySQL offers only `none` and `cloudwatch`. There’s no
`system` option that reads query history directly from the database: MySQL doesn’t retain a durable,
queryable history of executed statements (the `performance_schema` statement tables are ring buffers
that rotate quickly). To capture lineage and popularity, export the general query log to CloudWatch
as described here.

## CloudWatch Logs on Amazon RDS

Horizon Catalog reads the MySQL general query log from CloudWatch. RDS doesn’t enable the general
log by default, so you enable it, export it to CloudWatch, and grant Horizon Catalog read access
through a cross-account IAM role. By the time you finish this guide you’ll have:

1. The MySQL general query log enabled through a custom parameter group.
2. The log exported to a CloudWatch log group.
3. A cross-account IAM role that Horizon Catalog can assume to read that log group.
4. The role ARN ready to paste into the Horizon Catalog wizard.

Every step below happens in AWS except the last, which returns to the Horizon Catalog UI.

Creating the IAM role and its inline policy

You can add the inline policy while creating the role (in the **Add permissions** step of the
**Create role** wizard, choose **Create inline policy**) or afterward from the role’s own
**Permissions** tab. Either order works, so use whichever the console puts in front of you.

### 1. Enable the general query log

The general log is controlled by parameters that only a custom parameter group can change.

1. In the RDS console, go to **Parameter groups**. If your instance uses a `default.*` group,
   select **Create parameter group**, give it a name (for example, `snowflake-horizon-mysql`), pick
   the parameter group family that matches your MySQL major version (for example, `mysql8.0`), and
   select **Create**.
2. Open the custom group, select **Edit**, and set:

   | Parameter | Value | Notes |
   | --- | --- | --- |
   | `general_log` | `1` | Enable the general query log. |
   | `log_output` | `FILE` | Required to export the log to CloudWatch Logs. |

   Expand

   Show lessSee more
3. Save the changes.

### 2. Export the general log to CloudWatch

1. In the RDS console, go to **Databases** and select your MySQL instance.
2. Select **Modify**. Under **Database options > DB parameter group**, attach the custom group
   from Step 1 if it isn’t already attached.
3. Under **Log exports**, tick **General log**.
4. Choose **Apply immediately**, review, and save. Attaching a new parameter group triggers a
   reboot; changing only parameters on an already-attached group does not.

### 3. Verify

Run a query against the database, then confirm the log group
`/aws/rds/instance/<DB_IDENTIFIER>/general` exists in CloudWatch Logs in the same region as the
instance and that recent streams contain entries. Horizon Catalog refuses the connector during the
UI authorization step if it can’t find a populated log group.

### 4. Create the cross-account IAM role

Horizon Catalog’s service role assumes a customer-owned IAM role in your account to read the log
group.

#### 4a. Trust policy

Paste the **IAM Principal** and **External ID** values from the Horizon Catalog wizard into this
trust policy.

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

**AWS Console**: IAM > Roles > Create role > Trusted entity type: **Custom trust policy** > paste
the JSON above > **Next**.

#### 4b. Access policy

On the **Add permissions** step, either add this inline policy now (**Create inline policy >
JSON**) or skip it and add it afterward from the role’s **Permissions** tab. It grants read access
to the CloudWatch log groups that match your prefix. Replace `<AWS_REGION>`, `<AWS_ACCOUNT_ID>`,
and `<LOG_GROUP_NAME_PREFIX>` (for example, `/aws/rds/instance/<DB_IDENTIFIER>/general`) with your
values.

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadLogGroup",
      "Effect": "Allow",
      "Action": [
        "logs:Get*",
        "logs:List*",
        "logs:StartQuery",
        "logs:StopQuery",
        "logs:Describe*",
        "logs:FilterLogEvents",
        "logs:Unmask"
      ],
      "Resource": "arn:aws:logs:<AWS_REGION>:<AWS_ACCOUNT_ID>:log-group:<LOG_GROUP_NAME_PREFIX>*:*"
    },
    {
      "Sid": "QueryResultsAndLogGroupDiscovery",
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

**AWS Console** (if you skipped it above): Open the role > **Add permissions > Create inline
policy** > **JSON** tab > paste the policy above > name it `EnableSnowflakeHorizon` > **Create
policy**.

#### 4c. Name the role

On the **Name, review, and create** step, name the role. The name must match one of the two forms
Horizon Catalog’s validator accepts.

| Form | Example | When to use |
| --- | --- | --- |
| Role name prefix | `SnowflakeHorizon-rds-mysql-prod` | AWS Console: the console doesn’t expose the Path field. |
| Path-based | path `/SnowflakeHorizon/`, name `rds-mysql-prod` | API, CLI, or Terraform. |

Expand

Show lessSee more

Anything else (`SnowflakeHorizonOther`, `SnowflakeHorizon_foo`, a bare name) is rejected by
Horizon Catalog even if the AWS role exists. Select **Create role**.

#### 4d. Copy the role ARN

Note the role ARN from the IAM console (for example,
`arn:aws:iam::123456789012:role/SnowflakeHorizon-rds-mysql-prod`). You’ll paste it into the Horizon
Catalog UI in the next step.

### 5. Confirm authorization in Horizon Catalog

In the **Connect query log** step, set **Source type** to **CloudWatch Logs** and fill in:

- **AWS Region**: The region where your MySQL instance is hosted (for example, `us-east-2`).
- **Role ARN**: The ARN of the IAM role from Step 4d.
- **Log Group Name Prefix**: The general log group, for example
  `/aws/rds/instance/<DB_IDENTIFIER>/general`.

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| UI rejects Role ARN | Role name doesn’t match `SnowflakeHorizon-*` or `/SnowflakeHorizon/` | Step 4c |
| `AccessDenied` on `sts:AssumeRole` | Trust-policy principal or External ID mismatch | Step 4a |
| UI says “no query log found” | General log not enabled or not exported to CloudWatch | Steps 1–3 |

Expand

Show lessSee more

## Sensitive data in logs

The general query log records statement text, including literal values that may contain sensitive
data. Treat the CloudWatch log group accordingly: restrict access, and apply a retention policy
that matches your organization’s requirements.
