# Query Logs

Available query log sources for Oracle data sources:

- **System tables / views** (`system`): No AWS work required. See
  [Oracle](/user-guide/snowflake-horizon/connectors/oracle) Step 3.
- **Database Activity Streams on Amazon RDS** (`s3`): Full DAS pipeline described below.
- **None**: Metadata only; lineage and popularity disabled.

## Database Activity Streams (DAS) on Amazon RDS

This section builds the DAS pipeline manually. The pipeline captures Oracle audit events via
Kinesis, decrypts them with a Lambda function, and delivers the results to S3 for Horizon Catalog
to read.

Creating IAM roles and inline policies

Several steps below create an IAM role with an inline policy. You can add the inline policy while
creating the role (in the **Add permissions** step of the **Create role** wizard, choose **Create
inline policy**) or afterward from the role’s **Permissions** tab. Either order works, so use
whichever the console puts in front of you.

### 1. Create and enable an audit policy

Create a unified audit policy that captures activity from real users, then enable it. The `WHEN`
clause excludes the RDS-managed accounts (`SYS`, `RDSSEC`, `RDSADMIN`), which run maintenance
statements Horizon Catalog doesn’t need.

Copy code

```
CREATE AUDIT POLICY snowflake_horizon_query_logs
ACTIONS ALL
WHEN 'SYS_CONTEXT(''USERENV'', ''SESSION_USER'') NOT IN (''SYS'', ''RDSSEC'', ''RDSADMIN'')'
EVALUATE PER SESSION;

AUDIT POLICY snowflake_horizon_query_logs;
```

After enabling the policy, **reconnect** your database session (the `WHEN` clause is evaluated once
per session) and run queries as a **non-system user**: activity from `SYS`, `RDSSEC`, and `RDSADMIN`
is excluded on purpose. Confirm the policy is active:

Copy code

```
SELECT * FROM audit_unified_enabled_policies WHERE policy_name = 'SNOWFLAKE_HORIZON_QUERY_LOGS';
```

### 2. Start the Database Activity Stream on the RDS instance

DAS requires a customer-managed KMS key in the same region as the RDS instance. The AWS-managed
`aws/rds` key isn’t accepted. If you don’t already have a suitable customer-managed key, create
one first:

1. In the KMS console, go to **Customer managed keys > Create key**. Same region as the RDS instance.
2. Key type: **Symmetric**. Key usage: **Encrypt and decrypt**.
3. Alias: for example, `snowflake-horizon-oracle-das`.
4. Key administrators: an IAM role/user authorized to rotate or schedule deletion of the key.
5. Key users: include the IAM principal you’ll use to start DAS. RDS needs `kms:CreateGrant` on this key to delegate decryption to the DAS service.
6. Finish. Note the key ARN.

Then start the stream:

1. In the RDS console, go to **Databases**, then select the Oracle instance.
2. Verify the DB instance class is in the [AWS-supported list for DAS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/DBActivityStreams.html#DBActivityStreams.Overview.requirements.classes).
3. Open the **Actions** dropdown (top-right) and select **Start activity stream**.
4. Configure:
   - **AWS KMS key**: Pick the customer-managed key from above.
   - **Database activity events**: Tick **Enable engine-native audit fields**.
   - **Apply**: Choose **Immediately** (triggers an RDS reboot) or **During the next maintenance window**.
5. Select **Start database activity stream** and wait for the instance to return to Available.

Enable engine-native audit fields is required

If you don’t tick **Enable engine-native audit fields**, the stream carries only heartbeats: the
Lambda drops every batch and nothing reaches S3.

### 3. Capture the Kinesis stream ARN and KMS key ARN

After the stream is running:

1. In the RDS console, go to **Databases**, select your instance, then open the **Configuration** tab and find the **Database activity stream** section.
2. Copy:
   - **Kinesis data stream**: Full ARN, for example `arn:aws:kinesis:us-east-2:000000000000:stream/aws-rds-das-db-ZQO7M43PGGUXJEZVYSALTO76KA`
   - **AWS KMS key**: Full ARN, for example `arn:aws:kms:us-east-2:000000000000:key/f319545f-a0d4-4bfc-896f-5d37fe921ffb`
   - **RDS resource ID**: The `db-…` identifier shown on the same page. You’ll need this as a Lambda environment variable.

Everything from Step 4 onward must go in the region where the stream was created.

### 4. Create the destination S3 bucket

1. In the S3 console, select **Create bucket**. Choose any bucket name (for example, `snowflake-horizon-oracle-das-<instance>-<acct>`). Same region as the instance.
2. Object Ownership: **Bucket owner enforced**.
3. Block Public Access: leave all four blocks on.
4. Enable SSE-S3 or SSE-KMS encryption per your policy.
5. (Optional) Set a lifecycle rule to expire `errors/` and old `processed/` objects after your retention requirement.

Note the bucket ARN and name.

### 5. Upload the DAS processor Lambda deployment package

The processor decrypts DAS records and writes JSON lines back to Firehose for S3 delivery.

Download [deployment-package.zip](/static/samples/horizon-catalog/deployment-package.zip) and
upload it to your S3 bucket under `deployment-package.zip`. The Lambda runs on arm64.

### 6. Create the Lambda execution role

IAM > Roles > Create role > AWS service > Lambda. Attach these AWS-managed policies:

- `AWSLambdaBasicExecutionRole`
- `AWSXRayDaemonWriteAccess`

Add the following inline policy. Replace `<BUCKET_ARN>` (Step 4) and `<KMS_KEY_ARN>` (Step 3):

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadDeploymentPackage",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "<BUCKET_ARN>/deployment-package.zip"
    },
    {
      "Sid": "DecryptDasBatchKeys",
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "<KMS_KEY_ARN>"
    }
  ]
}
```

Name the inline policy (for example, `snowflake-horizon-oracle-das-lambda-policy`) and the role (for
example, `snowflake-horizon-oracle-das-lambda-exec`). You need the role ARN in Step 7.

### 7. Create the DAS processor Lambda

Go to **Lambda > Create function > Author from scratch** and set:

- **Function name**: `snowflake-horizon-oracle-das-processor` (or similar).
- **Runtime**: Python 3.12.

Expand **Additional settings** and, under **General**:

- Enable **ARM64 architecture** (the deployment package is built for arm64).
- Enable **Custom execution role** and select the role from Step 6.

Select **Create function**. Lambda creates the function with placeholder code; the remaining fields
(code, handler, timeout, and environment variables) are configured on the function’s own page after
it’s created:

1. **Code** tab > **Update** > **Update from a file in Amazon S3**. Leave **Code storage mode** as
   **Copy mode** (default), and for **Amazon S3 link** paste the HTTPS URL of the package you
   uploaded in Step 5 (for example,
   `https://<bucket>.s3.<region>.amazonaws.com/deployment-package.zip`). Select **Update**.
2. **Code** tab > **Runtime settings** > **Edit**. Set **Handler** to
   `snowflake_horizon_das_processor.handler.lambda_handler` and select **Save**. (The architecture was
   already set to arm64 when you created the function.)
3. **Configuration** tab > **General configuration** > **Edit**. Set **Timeout** to 1 min and select
   **Save**.
4. **Configuration** tab > **Environment variables** > **Edit**. Add:
   - `rds_resource_id` = the `db-…` ID from Step 3.
   - `kms_key_arn` = the KMS key ARN from Step 3.

Use the same KMS key everywhere

The KMS key ARN from Step 3 must match in all three places: the DAS stream, the Lambda execution
role’s `kms:Decrypt` statement (Step 6), and this `kms_key_arn` variable. A mismatch fails with
`AccessDeniedException` on `kms:Decrypt` and nothing reaches S3.

**Verify:** In the function’s CloudWatch logs you’ll see `Received N records`. `Dropping record set with no valid events (only heartbeat)` isn’t a failure: it means no audited queries have flowed yet.

### 8. Create the Firehose stream IAM role

First create the log group the Firehose stream logs to, so you have its ARN for the policy below:

- CloudWatch > Log groups > Create log group, name it `/aws/kinesisfirehose/snowflake-horizon-oracle-das/DeliveryStream` (or similar).
- Inside it, create a log stream named `delivery`.
- Open the log group and copy its ARN. It looks like `arn:aws:logs:<region>:<account-id>:log-group:/aws/kinesisfirehose/snowflake-horizon-oracle-das/DeliveryStream:*`. This is `<LOG_GROUP_ARN>` in the policy below.

Now create the role. IAM > Roles > Create role > Custom trust policy:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "firehose.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

Name the role (for example, `snowflake-horizon-oracle-das-firehose`).

Attach this inline policy (replace `<KINESIS_STREAM_ARN>`, `<LAMBDA_ARN>`, `<BUCKET_ARN>`, and
`<LOG_GROUP_ARN>` with the log group ARN you copied above):

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadDasKinesis",
      "Effect": "Allow",
      "Action": [
        "kinesis:GetRecords",
        "kinesis:GetShardIterator",
        "kinesis:DescribeStream",
        "kinesis:ListStreams"
      ],
      "Resource": [
        "<KINESIS_STREAM_ARN>",
        "<KINESIS_STREAM_ARN>/*"
      ]
    },
    {
      "Sid": "InvokeProcessorLambda",
      "Effect": "Allow",
      "Action": [
        "lambda:InvokeFunction",
        "lambda:GetFunctionConfiguration"
      ],
      "Resource": [
        "<LAMBDA_ARN>",
        "<LAMBDA_ARN>:$LATEST"
      ]
    },
    {
      "Sid": "WriteS3",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:PutObject"
      ],
      "Resource": [
        "<BUCKET_ARN>",
        "<BUCKET_ARN>/*"
      ]
    },
    {
      "Sid": "WriteFirehoseLogs",
      "Effect": "Allow",
      "Action": "logs:PutLogEvents",
      "Resource": [
        "<LOG_GROUP_ARN>",
        "<LOG_GROUP_ARN>/*"
      ]
    }
  ]
}
```

Name the inline policy (for example, `snowflake-horizon-oracle-das-firehose-policy`).

### 9. Create the Firehose stream

In the [Amazon Data Firehose](https://console.aws.amazon.com/firehose/) console (formerly Kinesis
Data Firehose, and delivery streams are now called Firehose streams), select **Create Firehose
stream** and configure:

- **Source**: **Amazon Kinesis Data Streams**. **Destination**: **Amazon S3**. (You can’t change the source or destination after the stream is created.)
- **Firehose stream name**: for example, `snowflake-horizon-oracle-das-firehose-stream`.
- **Source settings > Kinesis data stream**: browse to, or paste the ARN of, the DAS Kinesis stream from Step 3.
- **Transform and convert records > Transform source records with AWS Lambda**: turn on data transformation and choose the `snowflake-horizon-oracle-das-processor` function. Set the transform **Buffer size** to 1 MB and **Buffer interval** to 900 seconds (15 min; the AWS minimum is 60 s, lower it for faster ingest).
- **Destination settings > S3 bucket**: the bucket from Step 4.
- **New line delimiter**: **Enabled**. Without this, Firehose concatenates records without newlines and Horizon Catalog’s JSON parser fails.
- **Dynamic partitioning**: leave **Not enabled**.
- **S3 bucket prefix**: `processed/!{timestamp:yyyy}/!{timestamp:MM}/!{timestamp:dd}/!{timestamp:HH}/`
- **S3 bucket error output prefix**: `errors/`
- Under **Buffer hints, compression, file extension and encryption**, keep **Compression** disabled (the Lambda plus new-line delimiter already produce NDJSON, which Horizon Catalog reads directly).
- **Backup settings**: leave **Source record backup in Amazon S3** not enabled.
- **Advanced settings > Service access**: select **Choose existing IAM role** and pick the Firehose role from Step 8 (not the default **Create or update IAM role**). Keep **Amazon CloudWatch error logging** set to **Enabled**.

Create the Firehose stream and wait for it to become Active.

Restarting DAS makes this stream inoperable

Stopping and starting the activity stream creates a new Kinesis stream, so this Firehose stream
becomes inoperable (its source can’t be changed after creation). If you restart DAS, delete and
recreate the Firehose stream against the new Kinesis stream.

### 10. Create the cross-account IAM role for Horizon Catalog

This is the role Horizon Catalog’s service role assumes to read the S3 bucket.

**Naming rules** (same as the other connectors):

| Form | Example | When to use |
| --- | --- | --- |
| Role name prefix | `SnowflakeHorizon-oracle-das-prod` | AWS Console: the console doesn’t expose the Path field. |
| Path-based | path `/SnowflakeHorizon/`, name `oracle-das-prod` | API, CLI, or Terraform. |

Expand

Show lessSee more

Anything else (`SnowflakeHorizonOther`, `SnowflakeHorizon_foo`, a bare name) is rejected by
Horizon Catalog even if the AWS role exists.

**Trust policy**: Paste the IAM Principal and External ID from the Horizon Catalog wizard:

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
the JSON above > **Next**. On the **Add permissions** step, either add the access policy below now
(**Create inline policy > JSON**) or skip it and add it afterward. Name the role
`SnowflakeHorizon-<suffix>` and create it.

**Inline access policy**: Replace `<BUCKET_ARN>` with the bucket ARN from Step 4:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadDasLogsBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": [
        "<BUCKET_ARN>",
        "<BUCKET_ARN>/*"
      ]
    }
  ]
}
```

**AWS Console** (if you didn’t add it during role creation): Open the role > **Add permissions >
Create inline policy** > **JSON** tab > paste the policy above > name it `EnableSnowflakeHorizon` >
**Create policy**.

Copy the role ARN (for example,
`arn:aws:iam::123456789012:role/SnowflakeHorizon-oracle-das-prod`). You’ll paste it into the
Horizon Catalog UI in Step 12.

### 11. Verify the pipeline end-to-end

1. Run a query as a non-system user (for example, `SELECT 1 FROM dual;`).
2. Wait up to 15 minutes (the Firehose buffer default).
3. Check S3 > your bucket > `processed/YYYY/MM/DD/HH/`. Fresh objects should appear. If `errors/` fills up instead, check the Firehose stream’s CloudWatch log stream `delivery`. The most common causes are Lambda permissions (Step 6) and Lambda handler/runtime misconfiguration (Step 7).

### 12. Confirm authorization in Horizon Catalog

In the **Connect query log** step, set **Source type** to **RDS Database Activity Stream** and
fill in:

- **AWS Region**: The region where your Oracle instance is hosted (for example, `us-east-2`).
- **Role ARN**: The ARN of the IAM role from Step 10.
- **S3 Bucket**: The name of the S3 bucket from Step 4.
- **S3 Object Prefix**: `processed/` (matches the Firehose prefix in Step 9).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| `s3` test fails: AccessDenied on bucket | Cross-account role policy scope or name wrong | Step 10: re-check role name matches `SnowflakeHorizon-*` or `/SnowflakeHorizon/` |
| `s3` test passes but no data | Firehose buffer is 15 min; run a query and wait; check `errors/` prefix and Firehose CloudWatch logs | Step 11 |
| Ingestion fails with `JSONDecodeError: Extra data` | Firehose **New line delimiter** is not enabled, so DAS records are concatenated | Step 9: set New line delimiter to Enabled |
| Firehose log: Decryption failure | Lambda execution role missing `kms:Decrypt` on the right key | Step 6 |
| DAS won’t start: instance class not supported | Instance class not in the AWS-supported DAS list | Step 2 |
| Audit policy created but no records in Kinesis | Audit policy not enabled (`AUDIT POLICY …` not run) | Step 1 |
| Lambda logs only `Dropping … only heartbeat` | Engine-native audit fields off, session not reconnected, or queries run as an excluded system user | Step 2, Step 1 |
| `kms:Decrypt` `AccessDeniedException` in Lambda | KMS key ARN doesn’t match across the DAS stream, the exec role, and `kms_key_arn` | Step 6, Step 7 |
| Firehose stream shows `Inoperable` | DAS was restarted, so the source Kinesis stream was replaced | Step 9: recreate the Firehose stream |

Expand

Show lessSee more

## Sensitive data in DAS

The audit policy in Step 1 captures statement activity, including literal values passed to those
statements. Treat the S3 bucket as a tier-1 data store: KMS-encrypt at rest, scope the
cross-account role narrowly, and apply a lifecycle rule so old batches expire on your
data-retention schedule.
