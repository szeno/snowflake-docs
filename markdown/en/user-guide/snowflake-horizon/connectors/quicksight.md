# Amazon QuickSight

Horizon Catalog collects users, data sources as connections, dashboards, analyses, and the
visuals inside them from Amazon QuickSight. It also ingests dataset, table, custom SQL, and column
metadata for lineage. Catalog Explorer groups the browsable objects by type (Dashboards and
Analyses), not by Amazon QuickSight folders. It builds column-level lineage to warehouse columns when that warehouse is also connected in the same
Horizon Catalog organization, and only when exactly one warehouse of that type is connected.
Otherwise warehouse lineage stays empty. It derives dashboard and analysis popularity from AWS
CloudTrail events. The connector uses a customer-owned IAM role that Horizon Catalog assumes with an
external ID.

Note

AWS now presents QuickSight within Amazon Quick, so the AWS console might show Quick branding.
Snowsight, the AWS APIs, IAM actions, and ARNs still use the QuickSight name, so this guide uses
Amazon QuickSight throughout.

## Prerequisites

To connect Amazon QuickSight to Horizon Catalog, you need the following:

- A Snowflake account hosted on AWS. Snowsight lists this connector only on AWS-hosted accounts,
  because Horizon Catalog assumes an AWS IAM role.
- Access to an AWS user with permission to create IAM roles in the account that owns the QuickSight
  subscription.
- At least one dataset, and at least one user in the QuickSight `default` namespace. Horizon Catalog
  verifies both before it accepts the data source.
- Optional: permission to create a CloudTrail trail and an S3 bucket, including
  `s3:PutEncryptionConfiguration`, if you want popularity data. CloudTrail enables server-side
  encryption on a bucket it creates.

Complete the following steps to connect Amazon QuickSight to Horizon Catalog:

1. [Create a new data source](#1-create-a-new-data-source).
2. [Configure AWS CloudTrail event logs](#2-configure-aws-cloudtrail-event-logs), which is optional.
3. [Create an IAM role](#3-create-an-iam-role).
4. [Confirm authorization and start the sync](#4-confirm-authorization-and-start-the-sync).
5. [Set up metadata access](#5-set-up-metadata-access).

Steps 1 and 4 take place in the Horizon Catalog wizard, and Steps 2 and 3 take place in the AWS
console. The wizard’s own steps are named rather than numbered, so a numbered step in this guide
always refers to this page.

## 1. Create a new data source

In Snowflake, open **Catalog > Connections** and select **Amazon QuickSight** from the list of
connectors. You go through a 3-step wizard: **Add data source → Authorize AWS access → Load
data**.

In the **Add data source** step, fill in the following fields, then select **Next** to open
**Authorize AWS access** before you leave Snowsight for AWS:

| Field | Value |
| --- | --- |
| **Connection** | Amazon QuickSight |
| **Display Name** | The default is `Amazon QuickSight`, but you can override it. |
| **Region** | The region in the QuickSight console URL, `https://<region>.quicksight.aws.amazon.com/`, for example `us-east-2`. If you enter the wrong region, edit the connection and replace this value. Horizon Catalog calls QuickSight APIs in the region you enter, including `ListDataSets`, and retries `ListUsers` in the identity region when AWS reports a mismatch. |
| **Snowflake Database** | The Snowflake database where Horizon Catalog stores the metadata. The default is `CONNECTORS`. |
| **Snowflake Schema** | The Snowflake schema where Horizon Catalog stores the metadata. The default is `METADATA`. |

Expand

Show lessSee more

Note

QuickSight assets are regional. In QuickSight, switch to the region that contains the datasets,
dashboards, and analyses to ingest. The console URL starts with that region, in the form
`https://<region>.quicksight.aws.amazon.com/`. Create a separate Horizon Catalog connection for
assets in another QuickSight region.

Leave **Authorize AWS access** open. That step shows the **IAM Principal** and **External ID** that
Step 3 copies into the IAM trust policy.

## 2. Configure AWS CloudTrail event logs

This step is optional. Horizon Catalog derives dashboard and analysis popularity, and the top users
of each object, exclusively from AWS CloudTrail management events delivered to an S3 bucket. Skip
this step if you don’t want popularity data.

If a trail already delivers management **Read** events to an S3 bucket that the Horizon Catalog role
can read, skip to [Step 2c](#2c-find-the-bucket-and-prefix) and note whether the trail uses
**Log file SSE-KMS encryption**. Otherwise, create a trail in [Step 2a](#2a-create-the-trail).

Note

A second trail that records the same management events can incur CloudTrail charges. For details,
see [AWS CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing/).

### 2a. Create the trail

In the CloudTrail console, open **Trails**, select **Create trail**, and fill in the following:

- **Trail name**: A name for the trail, for example, `snowflake-horizon-quicksight-logs`.
- **Storage location**: Select **Create new S3 bucket**. CloudTrail then creates the bucket together
  with the bucket policy that lets it write logs there, and names it
  `aws-cloudtrail-logs-<account-id>-<suffix>`. Save that bucket name; Steps 3c and 4 need it. Leave
  **Prefix** empty.
- **Log file SSE-KMS encryption**: Clear this option. It’s enabled by default and requires an AWS KMS
  key and alias. With it cleared, CloudTrail still encrypts the log files with SSE-S3, and the IAM
  role in Step 3 needs no key permissions.
- If you see **Apply trail to my organization**, leave it cleared. Leave **CloudWatch Logs** and
  **SNS notification delivery** cleared.

Then select **Next**.

Using an existing bucket or a KMS key

An existing bucket rejects the trail with `InsufficientS3BucketPolicyException` until you attach the
CloudTrail bucket policy yourself. See [Amazon S3 bucket policy for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html)
in the AWS documentation.

If your organization requires a customer-managed key, keep **Log file SSE-KMS encryption** enabled
and enter an **AWS KMS Alias**, for example, `alias/snowflake-horizon-quicksight-logs`. A key that
CloudTrail creates carries a key policy that lets principals in your account decrypt CloudTrail
logs, so the role in Step 3 works unchanged. For an existing key, follow
[Configure AWS KMS key policies for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-kms-key-policy-for-cloudtrail.html),
and add the `kms:Decrypt` statement from [Step 3c](#3c-permission-policy) to the role’s permission
policy.

### 2b. Choose log events

On the **Choose log events** page, set the following:

- **Event type**: Select **Management events** only. Leave **Data events**, **Insights events**, and
  **Network activity events** cleared.
- **Management events**: Select **Read** and **Exclude AWS KMS events**. Clear **Write**; CloudTrail
  enables it by default. Leave **Exclude Amazon RDS Data API events** cleared.

QuickSight records dashboard and analysis views as management read events, so Horizon Catalog needs
neither write events nor data events. AWS KMS events add a large share of the log volume without
contributing to popularity.

Select **Next**, review the settings, and select **Create trail**. Then open a QuickSight dashboard
or analysis to generate events. For details, see [Creating a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html)
in the AWS documentation.

### 2c. Find the bucket and prefix

Steps 3c and 4 need two values: the bucket name, and the path to the log files for the **Event Logs
Bucket Prefix** field.

A console trail covers every AWS region, so the bucket holds one folder per region. Use the same
region you entered in Step 1. CloudTrail writes QuickSight events under the following prefixes:

| Trail type | Prefix |
| --- | --- |
| Account trail | `AWSLogs/<account-id>/CloudTrail/<region>/` |
| Organization trail | `AWSLogs/<organization-id>/<account-id>/CloudTrail/<region>/` |
| Trail with its own prefix | `<trail-prefix>/AWSLogs/<account-id>/CloudTrail/<region>/` |

Expand

Show lessSee more

For example, account `123456789012` with Step 1 region `us-east-2` uses
`AWSLogs/123456789012/CloudTrail/us-east-2/`. Confirm the path in the S3 console, where CloudTrail
delivers `.json.gz` objects a few minutes after the events occur.

Caution

Copy the prefix the way CloudTrail writes it, including the trailing slash and with no leading
slash. Paste that same value into the IAM policy in Step 3c and into the wizard in Step 4. A
leading slash in the IAM policy doesn’t match the objects in the bucket. Horizon Catalog verifies
during setup that it can read at least one CloudTrail log, and rejects the data source if it can’t.

## 3. Create an IAM role

Horizon Catalog uses a customer-owned IAM role that it assumes to read QuickSight metadata. In the
AWS IAM console, go to **Roles**, select **Create role**, and create the role as follows.

### 3a. Trust policy

In the Horizon Catalog wizard, go to the **Authorize AWS access** step. Horizon Catalog pre-generates
two read-only values you must copy into the trust policy:

- **External ID**: a unique token generated per data source
- **IAM Principal**: the Horizon Catalog AWS principal that assumes your role

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

The **External ID is unique per data source**. It is regenerated each time a new connection is
created. If you recreate the data source in another environment, copy the new External ID from the
wizard and update the trust policy to match.

Select **Next**. On the **Add permissions** page, select **Next** without adding a managed policy.

### 3b. Name and create the role

On the **Name, review, and create** page, name the role. The name must match one of the two forms
Horizon Catalog’s validator accepts.

| Form | Example | When to use |
| --- | --- | --- |
| Role name prefix | `SnowflakeHorizon-QuickSight` | AWS Console: The console doesn’t expose the Path field. |
| Path-based | Path `/SnowflakeHorizon/`, name `QuickSight` | API, CLI, or Terraform. |

Expand

Show lessSee more

Caution

The role name must start with the `SnowflakeHorizon-` prefix, or the role must be created under the
`SnowflakeHorizon/` path. Horizon Catalog rejects role ARNs that don’t meet this requirement. Valid
ARNs look like `arn:aws:iam::123456789012:role/SnowflakeHorizon-QuickSight` or
`arn:aws:iam::123456789012:role/SnowflakeHorizon/QuickSight`.

Add a description, for example `IAM role used to connect Horizon Catalog to Amazon QuickSight`, then
select **Create role**.

### 3c. Permission policy

Open the role, open the **Permissions** tab, select **Add permissions > Create inline policy**, and
open the **JSON** editor. Paste the following policy:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "QuickSightMetadataAccess",
      "Effect": "Allow",
      "Action": [
        "quicksight:List*",
        "quicksight:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```

Name the inline policy, for example, `SnowflakeHorizonQuickSight`, and select **Create policy**.

Horizon Catalog only reads QuickSight metadata. The wildcards cover the list and describe
operations it calls. AWS authorizes some QuickSight APIs under a different IAM action than the API
name: `DescribeAnalysisDefinition` requires `quicksight:DescribeAnalysis`, and
`DescribeDashboardDefinition` requires `quicksight:DescribeDashboard`. An explicit list of API names
is therefore wrong. These are account-scoped read operations, so they use a `"*"` resource rather
than per-object ARNs.

If you configured CloudTrail in Step 2, create another inline policy with the following JSON.
Replace `REPLACE_WITH_EVENT_LOG_BUCKET` with the bucket name and
`REPLACE_WITH_EVENT_LOG_PREFIX` with the path from Step 2c, including the trailing slash and with no
leading slash:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListEventLogBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::REPLACE_WITH_EVENT_LOG_BUCKET",
      "Condition": {
        "StringLike": {
          "s3:prefix": "REPLACE_WITH_EVENT_LOG_PREFIX*"
        }
      }
    },
    {
      "Sid": "ReadEventLogObjects",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::REPLACE_WITH_EVENT_LOG_BUCKET/REPLACE_WITH_EVENT_LOG_PREFIX*"
    }
  ]
}
```

Name this policy, for example, `SnowflakeHorizonQuickSightEventLogs`, and select **Create policy**.
This policy is all the access the role needs for logs encrypted with SSE-S3 or with a key that
CloudTrail created.

If you use an existing KMS key, create one more inline policy. Replace the placeholders with the
key’s region, account ID, and key ID:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DecryptEventLogs",
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:REPLACE_WITH_REGION:REPLACE_WITH_ACCOUNT_ID:key/REPLACE_WITH_KEY_ID"
    }
  ]
}
```

Horizon Catalog also calls `sts:GetCallerIdentity` to resolve your AWS account ID. That call
requires no IAM permission, so don’t add it to a policy.

### 3d. Copy the role ARN

Note the role ARN from the role’s summary page (for example,
`arn:aws:iam::123456789012:role/SnowflakeHorizon-QuickSight`). Paste it into the Horizon Catalog
wizard in Step 4.

## 4. Confirm authorization and start the sync

Return to the **Authorize AWS access** step in the Horizon Catalog wizard. The **External ID** and
**IAM Principal** fields are already filled in and read-only. Paste the role ARN from Step 3 into the
**Role ARN** field.

If you configured CloudTrail, fill in both **Event Logs Bucket** and **Event Logs Bucket Prefix**, or
leave both empty. In **Event Logs Bucket Prefix**, enter the same path you put in the IAM policy, for example
`AWSLogs/123456789012/CloudTrail/us-east-2/`, with no leading slash. If CloudTrail hasn’t delivered
an object yet, open a QuickSight dashboard or analysis and wait a few minutes before you continue.
Then select **Next**.

The **Load data** step starts the first sync. When the call succeeds, the wizard shows **Connection
added**, and the sync continues in the background. You can select **Done** and close the wizard.
Horizon Catalog ingests every dashboard, analysis, and dataset in the QuickSight region
you entered in Step 1. Datasets support lineage but aren’t browsable objects in Catalog
Explorer.

Catalog Explorer shows Amazon QuickSight under a **Dashboards and Analyses** type bucket, with
separate **Dashboards** and **Analyses** groups. Native QuickSight folders are not Catalog roots.

Popularity and top users appear after Horizon Catalog processes the first CloudTrail logs it can
read.

## 5. Set up metadata access

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
| `Unable to assume AWS IAM role` | Trust-policy principal or External ID mismatch. | Step 3a: Copy both values from the wizard again. |
| `Unable to connect to QuickSight` | The selected region has no dataset, or the `default` namespace has no user. | Step 1: Confirm the region, dataset, and user. |
| `Unable to access QuickSight usage logs` | The prefix doesn’t match the CloudTrail path, most often because the trail prefix is missing. | Step 4: Compare the value with the path that contains the `.json.gz` objects. |
| `InsufficientS3BucketPolicyException` when you create the trail | The bucket existed before the trail and has no CloudTrail bucket policy. | Step 2: Let CloudTrail create the bucket, or attach the policy to the existing bucket. |
| `AccessDenied` on `kms:Decrypt` while loading event logs | The existing KMS key policy or role policy doesn’t allow the role to decrypt. | Steps 2 and 3c: Update the key policy and the role policy. |
| No popularity data or top users | The event log fields are empty, or the trail doesn’t log management **Read** events. | Step 2: Confirm that the trail logs management **Read** events to the bucket you specified. |
| Horizon Catalog rejects the **Role ARN** | The role name doesn’t use the `SnowflakeHorizon-` prefix or the `/SnowflakeHorizon/` path. | Step 3b. |

Expand

Show lessSee more

Note

QuickSight serves the user list from a single identity region, which can differ from the region you
entered in Step 1. If an `AccessDenied` error names an identity region, Horizon Catalog retries in
that region automatically, so the fix is the permission policy, not the **Region** field.

## Connection security

All communication between Horizon Catalog and Amazon QuickSight uses the AWS SDK over HTTPS (TLS 1.2
or higher). Horizon
Catalog stores no QuickSight credentials: it reads your account through the customer-owned IAM role
you create in Step 3, which it can assume only with the External ID generated for this data source.
You can revoke that access at any time by deleting the role or removing Horizon Catalog from its
trust policy.

For more details, see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Sensitive data in event logs

The trail you configure in Step 2 records which dashboard or analysis each user opened, together
with the identity that made the call. Treat the S3 bucket accordingly: restrict access to it, and
apply a lifecycle rule so old logs expire on your organization’s data-retention schedule.
