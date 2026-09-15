# Refresh directory tables automatically for Amazon S3

This topic provides instructions for creating a directory table on an external stage and refreshing the directory table metadata automatically using [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket. This operation synchronizes the metadata with the
latest set of associated files in the external stage and path when the following occur:

> - New files in the path are added to the table metadata.
> - Changes to files in the path are updated in the table metadata.
> - Files no longer in the path are removed from the table metadata.

Note

- To perform the tasks described in this topic, you must use a role that has the CREATE STAGE privilege on a schema.

  In addition, you must have administrative access to AWS. If you are not an AWS administrator, ask your AWS administrator to complete
  the steps required to configure AWS event notifications.
- Snowflake recommends that you only send supported events for directory tables to reduce costs, event noise, and latency.

## Limitations of automatic refreshing of directory tables using Amazon SQS

- [Virtual Private Snowflake (VPS)](/user-guide/intro-editions) and [AWS PrivateLink](/user-guide/admin-security-privatelink)
  customers: Although AWS services within a VPC (including VPS) can communicate with SQS, this traffic is not within the VPC, and therefore is not protected by the VPC.
- SQS notifications notify Snowflake when new files arrive in monitored S3 buckets and are ready to load. SQS notifications contain the S3
  event and a list of the file names. They do not include the actual data in the files.

## Cloud platform support

Triggering automated refreshes using S3 event messages is supported for Snowflake accounts hosted on any of the
[supported cloud platforms](/user-guide/intro-cloud-platforms).

## Configure secure access to cloud storage

Note

If you have already configured secure access to the S3 bucket that stores your data files, you can skip this section.

This section describes how to configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage
to a Snowflake identity and access management (IAM) entity.

Note

We highly recommend this option, which avoids the need to supply IAM credentials when accessing cloud storage. See
[Configuring secure access to Amazon S3](/user-guide/data-load-s3-config) for additional storage access options.

This section describes how to use storage integrations to allow Snowflake to read data from and write data to an Amazon S3 bucket referenced in an external (i.e. S3) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as secret keys or access tokens. Integration objects store an AWS identity and access management (IAM) user ID. An administrator in your organization grants the integration IAM user permissions in the AWS account.

An integration can also list buckets (and optional paths) that limit the locations users can specify when creating external stages that use the integration.

Note

- Completing the instructions in this section requires permissions in AWS to create and manage IAM policies and roles. If you are not an AWS administrator, ask your AWS administrator to perform these tasks.
- Note that currently, accessing S3 storage in [government regions](/user-guide/intro-regions#label-us-gov-regions)
  using a storage integration is limited to Snowflake accounts hosted on AWS in the same government
  region. Accessing your S3 storage from an account hosted outside of the government region using
  direct credentials is supported.

The following diagram shows the integration flow for a S3 stage:

![Amazon S3 Stage Integration Flow](/static/images/storage-integration-s3.png)

1. An external (i.e. S3) stage references a storage integration object in its definition.
2. Snowflake automatically associates the storage integration with a S3 IAM user created for your account. Snowflake creates a single IAM user that is referenced by all S3 storage integrations in your Snowflake account.
3. An AWS administrator in your organization grants permissions to the IAM user to access the bucket referenced in the stage definition. Note that many external stage objects can reference different buckets and paths and use the same storage integration for authentication.

When a user loads or unloads data from or to a stage, Snowflake verifies the permissions granted to the IAM user on the bucket before allowing or denying access.

### Step 1: Configure access permissions for the S3 bucket

#### AWS access control requirements

Snowflake requires the following permissions on an S3 bucket and folder to be able to access files in the folder (and sub-folders):

- `s3:GetBucketLocation`
- `s3:GetObject`
- `s3:GetObjectVersion`
- `s3:ListBucket`

As a best practice, Snowflake recommends creating an IAM policy for Snowflake access to the S3 bucket. You can then attach the policy to
the role and use the security credentials generated by AWS for the role to access files in the bucket.

#### Create an IAM policy

The following step-by-step instructions describe how to configure access permissions for Snowflake in your AWS Management Console to access
your S3 bucket.

1. Log into the AWS Management Console.
2. From the home dashboard, search for and select **IAM**.
3. From the left-hand navigation pane, select **Account settings**.
4. Under **Security Token Service (STS)** in the **Endpoints** list, find the Snowflake
   [region](/user-guide/intro-regions) where your account is located. If the **STS status** is inactive,
   move the toggle to **Active**.
5. From the left-hand navigation pane, select **Policies**.
6. Select **Create Policy**.
7. For **Policy editor**, select **JSON**.
8. Add a policy document that will allow Snowflake to access the S3 bucket and folder.

   The following policy (in JSON format) provides Snowflake with the required permissions to load or unload data using a single bucket and
   folder path.

   Copy and paste the text into the policy editor:

   Note

   - Make sure to replace `bucket` and `prefix` with your actual bucket name and folder path prefix.
   - The Amazon Resource Names (ARN) for buckets in
     [government regions](/user-guide/intro-regions#label-us-gov-regions) have a `arn:aws-us-gov:s3:::` prefix.

   Copy code

   ```
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "s3:GetObject",
              "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::<bucket>/<prefix>/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::<bucket>",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "<prefix>/*"
                    ]
                }
            }
        }
    ]
   }
   ```

   Note

   Setting the `"s3:prefix":` condition to either `["*"]` or `["<path>/*"]` grants access to all prefixes in the
   specified bucket or path in the bucket, respectively.

   Note that AWS policies support a variety of different security use cases.
9. Select **Next**.
10. Enter a **Policy name** (for example, `snowflake_access`) and an optional **Description**.
11. Select **Create policy**.

# Step 2: Create the IAM role in AWS

To configure access permissions for Snowflake in the AWS Management Console, do the following:

1. From the left-hand navigation pane in the Identity and Access Management (IAM) Dashboard, select **Roles**.
2. Select **Create role**.
3. Select **AWS account** as the trusted entity type.
4. Select **Another AWS account**

> ![Select trusted entity page in AWS Management Console](/static/images/screens/iam-role-select-trusted-entity.png)

5. In the **Account ID** field, enter your own AWS account ID temporarily. Later, you modify the trust relationship and grant
   access to Snowflake.
6. Select the **Require external ID** option. An external ID is used to grant access to your AWS resources
   (such as S3 buckets) to a third party like Snowflake.

   Enter a placeholder ID such as `0000`.
   In a later step, you will modify the trust relationship for your IAM role and specify the external ID for your storage integration.
7. Select **Next**.
8. Select the policy you created in `Step 1: Configure access permissions for the S3 bucket`\_ (in this topic).
9. Select **Next**.

> ![Review Page in AWS Management Console](/static/images/screens/iam-role-review.png)

10. Enter a name and description for the role, then select **Create role**.

You have now created an IAM policy for a bucket, created an IAM role, and attached the policy to the role.

11. On the role summary page, locate and record the **Role ARN** value. In the next step, you will create a Snowflake integration that
    references this role.

Note

Snowflake caches the temporary credentials for a period that cannot exceed the 60-minute expiration time. If you revoke access from
Snowflake, users might be able to list files and access data from the cloud storage location until the cache expires.

## Step 3: Create a cloud storage integration in Snowflake

Create a storage integration using the [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) command. A storage integration is a Snowflake
object that stores a generated identity and access management (IAM) user for your S3 cloud storage, along with an optional set of allowed
or blocked storage locations (that is, buckets). Cloud provider administrators in your organization grant permissions on the storage locations
to the generated user. This option allows users to avoid supplying credentials when creating stages or loading data.

A single storage integration can support multiple external (that is, S3) stages. The URL in the stage definition must align with the S3
buckets (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this
SQL command.

Copy code

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<iam_role>'
  STORAGE_ALLOWED_LOCATIONS = ('<protocol>://<bucket>/<path>/', '<protocol>://<bucket>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('<protocol>://<bucket>/<path>/', '<protocol>://<bucket>/<path>/') ]
```

Where:

- `integration_name` is the name of the new integration.
- `iam_role` is the Amazon Resource Name (ARN) of the role you created in [Step 2: Create the IAM role in AWS](#step-2-create-the-iam-role-in-aws) (in this topic).
- `protocol` is one of the following:

  - `s3` refers to S3 storage in public AWS regions outside of China.
  - `s3china` refers to S3 storage in public AWS regions in China.
  - `s3gov` refers to S3 storage in [government regions](/user-guide/intro-regions#label-us-gov-regions).
- `bucket` is the name of a S3 bucket that stores your data files (for example, `mybucket`). The required STORAGE\_ALLOWED\_LOCATIONS
  parameter and optional STORAGE\_BLOCKED\_LOCATIONS parameter restrict or block access to these buckets, respectively, when stages that
  reference this integration are created or modified.
- `path` is an optional path that can be used to provide granular control over objects in the bucket.

The following example creates an integration that allows access to all buckets in the account but blocks access to the defined `sensitivedata` folders.

Additional external stages that also use this integration can reference the allowed buckets and paths:

Copy code

```
CREATE STORAGE INTEGRATION s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
  STORAGE_ALLOWED_LOCATIONS = ('*')
  STORAGE_BLOCKED_LOCATIONS = ('s3://mybucket1/mypath1/sensitivedata/', 's3://mybucket2/mypath2/sensitivedata/');
```

Note

Optionally, use the [STORAGE\_AWS\_EXTERNAL\_ID](/sql-reference/sql/create-storage-integration#label-create-storage-integration-aws-ext-id) parameter to specify
your own external ID. You might choose this option
to use the same external ID across multiple external volumes and/or storage integrations.

## Step 4: Retrieve the AWS IAM user for your Snowflake account

1. To retrieve the ARN for the IAM user that was created automatically for your Snowflake account, use the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration).

   Copy code

   ```
   DESC INTEGRATION <integration_name>;
   ```

   Where:

   - `integration_name` is the name of the integration you created in [Step 3: Create a Cloud Storage Integration in Snowflake](#step-3-create-a-cloud-storage-integration-in-snowflake)
     (in this topic).

   For example:

   Copy code

   ```
   DESC INTEGRATION s3_int;
   ```

   ```
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------+
   | property                  | property_type | property_value                                                                 | property_default |
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------|
   | ENABLED                   | Boolean       | true                                                                           | false            |
   | STORAGE_ALLOWED_LOCATIONS | List          | s3://mybucket1/mypath1/,s3://mybucket2/mypath2/                                | []               |
   | STORAGE_BLOCKED_LOCATIONS | List          | s3://mybucket1/mypath1/sensitivedata/,s3://mybucket2/mypath2/sensitivedata/    | []               |
   | STORAGE_AWS_IAM_USER_ARN  | String        | arn:aws:iam::123456789001:user/abc1-b-self1234                                 |                  |
   | STORAGE_AWS_ROLE_ARN      | String        | arn:aws:iam::001234567890:role/myrole                                          |                  |
   | STORAGE_AWS_EXTERNAL_ID   | String        | MYACCOUNT_SFCRole=2_a123456/s0aBCDEfGHIJklmNoPq=                               |                  |
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------+
   ```
2. Record the values for the following properties:

| Property | Description |
| --- | --- |
| `STORAGE_AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account; for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. All S3 storage integrations in your account use that IAM user. |
| `STORAGE_AWS_EXTERNAL_ID` | The external ID that Snowflake uses to establish a trust relationship with AWS. If you didn’t specify an external ID (`STORAGE_AWS_EXTERNAL_ID`) when you created the storage integration, Snowflake generates an ID for you to use. |

Expand

Show lessSee more

You provide these values in the next section.

## Step 5: Grant the IAM user permissions to access bucket objects

The following step-by-step instructions describe how to configure IAM access permissions for Snowflake in your AWS Management Console so that you can use a S3 bucket to load and unload data:

1. Sign in to the AWS Management Console.
2. Select **IAM**.
3. From the left-hand navigation pane, select **Roles**.
4. Select the role you created in [Step 2: Create the IAM role in AWS](#step-2-create-the-iam-role-in-aws) (in this topic).
5. Select the **Trust relationships** tab.
6. Select **Edit trust policy**.
7. Modify the policy document with the DESC STORAGE INTEGRATION output values you recorded in
   [Step 4: Retrieve the AWS IAM user for your Snowflake account](#step-4-retrieve-the-aws-iam-user-for-your-snowflake-account) (in this topic):

   **Policy document for IAM role**

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<snowflake_user_arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<snowflake_external_id>"
        }
      }
    }
     ]
   }
   ```

   Where:

> - `snowflake_user_arn` is the STORAGE\_AWS\_IAM\_USER\_ARN value you recorded.
> - `snowflake_external_id` is the STORAGE\_AWS\_EXTERNAL\_ID value you recorded.
>
> In this example, the `snowflake_external_id` value is `MYACCOUNT_SFCRole=2_a123456/s0aBCDEfGHIJklmNoPq=`.
>
> Note
>
> For security reasons, if you create a new storage integration (or recreate an existing storage integration using the CREATE OR
> REPLACE STORAGE INTEGRATION syntax) without specifying an external ID, the new integration has a *different* external ID and
> can’t resolve the trust relationship unless you update the trust policy.

8. Select **Update policy** to save your changes.

Note

Snowflake caches the temporary credentials for a period that cannot exceed the 60-minute expiration time. If you revoke access from
Snowflake, users might be able to list files and load data from the cloud storage location until the cache expires.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

## Determine the correct option

Before proceeding, determine whether an S3 event notification exists for the target path (or “prefix,” in AWS terminology) in your S3
bucket where your data files are located. AWS rules prohibit creating conflicting notifications for the same path.

The following options for automating the refreshing of directory table metadata using Amazon SQS are supported:

- **Option 1. New S3 event notification:** Create an event notification for the target path in your S3 bucket. The event notification
  informs Snowflake via an SQS queue when new, removed, or modified files in the path require a refresh of the directory table metadata.

  Important

  If a conflicting event notification exists for your S3 bucket, use Option 2 instead.
- **Option 2. Existing event notification:** Configure [Amazon Simple Notification Service (SNS)](https://aws.amazon.com/sns/) as a
  broadcaster to share notifications for a given path with multiple endpoints (or “subscribers,” e.g. SQS queues or AWS Lambda workloads),
  including the Snowflake SQS queue for directory table refresh automation. An S3 event notification published by SNS informs Snowflake of
  file changes in the path via an SQS queue.

  Note

  We recommend this option if you plan to use [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history). You can also migrate from option 1 to
  option 2 after you create a replication or failover group. For more information, see [Migrate to Amazon Simple Notification Service (SNS)](/user-guide/account-replication-stages-pipes-load-history#label-account-replication-stages-pipes-load-history-migrate-to-sns).

## Option 1: Create a new S3 event notification

This section describes the most common option for automatically refreshing directory table metadata using [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket. The steps explain how to create an event notification for the
target path (or “prefix,” in AWS terminology) in your S3 bucket where your data files are stored.

> Important
>
> If a conflicting event notification exists for your S3 bucket, use [Option 2: Configure Amazon SNS](#option-2-configure-amazon-sns) (in this topic) instead. AWS
> rules prohibit creating conflicting notifications for the same target path.

### Step 1: Create a stage with an included directory table

Create an external stage that references your S3 bucket using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads
your staged data files into the directory table metadata. Alternatively, you can use an existing external stage.

Note

- To configure secure access to the cloud storage location, see [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage) (in this topic).
- To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration
  object.

Copy code

```
-- External stage
CREATE [ OR REPLACE ] [ TEMPORARY ] STAGE [ IF NOT EXISTS ] <external_stage_name>
      <cloud_storage_access_settings>
    [ FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } [ formatTypeOptions ] } ) ]
    [ directoryTable ]
    [ COPY_OPTIONS = ( copyOptions ) ]
    [ COMMENT = '<string_literal>' ]
```

Note

The storage location in the URL value must end in a forward slash (`/`).

Where:

> Copy code
>
> ```
> directoryTable (for Amazon S3) ::=
>   [ DIRECTORY = ( ENABLE = { TRUE | FALSE }
>                   [ AUTO_REFRESH = { TRUE | FALSE } ] ) ]
> ```

#### Directory table parameters (`directoryTable`)

`ENABLE = { TRUE | FALSE }`
:   Specifies whether to add a directory table to the stage. When the value is TRUE, a directory table is created with the stage.

    Default: `FALSE`

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable triggering automatic refreshes of the directory table metadata when new or updated data
    files are available in the named external stage specified in the URL value.

    `TRUE`
    :   Snowflake enables triggering automatic refreshes of the directory table metadata.

    `FALSE`
    :   Snowflake does not enable triggering automatic refreshes of the directory table metadata. You must manually refresh the directory
        table metadata periodically using [ALTER STAGE](/sql-reference/sql/alter-stage) … REFRESH to synchronize the metadata with the current list
        of files in the stage path.

    Default: `FALSE`

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`.

> Copy code
>
> ```
> USE SCHEMA mydb.public;
> ```

Copy code

```
CREATE STAGE mystage
  URL='s3://load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (
    ENABLE = true
    AUTO_REFRESH = true
  );
```

When new or updated data files are added to the cloud storage location, the event notification informs Snowflake to scan them into the
directory table metadata.

### Step 2: Configure event notifications

Configure event notifications for your S3 bucket to notify Snowflake when new or updated data is available to read into the directory table
metadata. The auto-refresh feature relies on SQS queues to deliver event notifications from S3 to Snowflake.

For ease of use, these SQS queues are created and managed by Snowflake. The [DESCRIBE STAGE](/sql-reference/sql/desc-stage) command output displays
the Amazon Resource Name (ARN) of your SQS queue.

1. Execute the DESCRIBE STAGE command:

   Copy code

   ```
   DESC STAGE <stage_name>;
   ```

   For example:

   Copy code

   ```
   DESC STAGE mystage;
   ```

   Note the ARN of the SQS queue for the directory table in the `directory_notification_channel` field. Copy the ARN to a convenient location.

   Note

   Following AWS guidelines, Snowflake designates no more than one SQS queue per AWS S3 region. This SQS queue can be shared among multiple
   buckets in the same AWS account. The SQS queue coordinates notifications for all directory tables reading data files from the same S3
   bucket. When a new or modified data file is uploaded into the bucket, all directory table definitions that match the stage directory
   path read the file details into their metadata.
2. Log into the AWS Management Console.
3. Configure an event notification for your S3 bucket using the instructions provided in the
   [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-event-notifications.html). Complete the fields
   as follows:

   - **Name**: Name of the event notification (e.g. `Auto-ingest Snowflake`).
   - **Events**: Select the **ObjectCreate (All)** and **ObjectRemoved** options.
   - **Send to**: Select **SQS Queue** from the dropdown list.
   - **SQS**: Select **Add SQS queue ARN** from the dropdown list.
   - **SQS queue ARN**: Paste the SQS queue name from the DESC STAGE output.

Note

These instructions create a single event notification that monitors activity for the entire S3 bucket. This is the simplest approach.
This notification handles all directory tables configured at a more granular level in the S3 bucket directory.

Alternatively, in the above steps, configure one or more paths and/or file extensions (or *prefixes* and *suffixes*, in AWS terminology)
to filter event activity. For instructions, see the object key name filtering information in the relevant
[AWS documentation topic](https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html). Repeat these steps for each
additional path or file extension you want the notification to monitor.

Note that AWS limits the number of these notification *queue configurations* to a maximum of 100 per S3 bucket.

Also note that AWS does not allow overlapping queue configurations (across event notifications) for the same S3 bucket. For example, if
an existing notification is configured for `s3://mybucket/files/path1`, then you cannot create another notification at a higher
level, such as `s3://mybucket/files`, or vice-versa.

The external stage with auto-refresh is now configured!

When new or updated data files are added to the S3 bucket, the event notification informs Snowflake to scan them into the directory table
metadata.

### Step 3: Manually refresh directory table metadata

Refresh the metadata in a directory table manually using the [ALTER STAGE](/sql-reference/sql/alter-stage) command.

Copy code

```
ALTER STAGE [ IF EXISTS ] <name> REFRESH [ SUBPATH = '<relative-path>' ]
```

Where:

`REFRESH`
:   Accesses the staged data files referenced in the directory table definition and updates the table metadata:

    - New files in the path are added to the table metadata.
    - Changes to files in the path are updated in the table metadata.
    - Files no longer in the path are removed from the table metadata.

    Currently, it is necessary to execute this command each time files are added to the stage, updated, or dropped. This step synchronizes
    the metadata with the latest set of associated files in the stage definition for the directory table.

`SUBPATH = '<relative-path>'`
:   Optionally specify a relative path to refresh the metadata for a specific subset of the data files.

For example, manually refresh the directory table metadata in a stage named `mystage`:

Copy code

```
ALTER STAGE mystage REFRESH;
```

Important

If this step is not completed successfully at least once after the directory table is created, querying the directory table returns no
results until a notification event triggers the directory table metadata to refresh automatically for the first time.

### Step 4: Configure security

For each additional role that will be used to query the directory table, grant sufficient access control privileges on the various objects
(i.e. the database(s), schema(s), stage, and table) using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE |  |

Expand

Show lessSee more

## Option 2: Configure Amazon SNS

This section describes how to trigger directory table metadata refreshing automatically using
[Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket. The steps explain how to configure
[Amazon Simple Notification Service (SNS)](https://aws.amazon.com/sns/) as a broadcaster to publish event notifications for your S3
bucket to multiple subscribers (e.g. SQS queues or AWS Lambda workloads), including the Snowflake SQS queue for directory table refresh
automation.

> Note
>
> These instructions assume an event notification exists for the target path in your S3 bucket where your data files are located. If no
> event notification exists, either:
>
> - Follow [Option 1: Create a new S3 event notification](#option-1-create-a-new-s3-event-notification) (in this topic) instead.
> - Create an event notification for your S3 bucket, then proceed with the instructions in this topic. For information, see the
>   [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-event-notifications.html).

# Prerequisite: Create an Amazon SNS Topic and Subscription

1. Create an SNS topic in your AWS account to handle all messages for the Snowflake stage location on your S3 bucket.
2. Subscribe your target destinations for the S3 event notifications (for example, other SQS queues or AWS Lambda workloads) to this topic. SNS publishes event notifications for your bucket to all subscribers to the topic.

For instructions, see the [SNS documentation](https://aws.amazon.com/documentation/sns/).

## Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic

1. Sign in to the AWS Management Console.
2. From the home dashboard, choose **Simple Notification Service** (SNS).
3. Choose **Topics** from the left-hand navigation pane.
4. Locate the topic for your S3 bucket. Note the topic ARN.
5. Using a Snowflake client, query the [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) system function with your SNS topic ARN:

   > Copy code
   >
   > ```
   > select system$get_aws_sns_iam_policy('<sns_topic_arn>');
   > ```

   The function returns an IAM policy that grants a Snowflake SQS queue permission to subscribe to the SNS topic.

   For example:

   > Copy code
   >
   > ```
   > select system$get_aws_sns_iam_policy('arn:aws:sns:us-west-2:001234567890:s3_mybucket');
   >
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > | SYSTEM$GET_AWS_SNS_IAM_POLICY('ARN:AWS:SNS:US-WEST-2:001234567890:S3_MYBUCKET')                                                                                                                                                                   |
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > | {"Version":"2012-10-17","Statement":[{"Sid":"1","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"},"Action":["sns:Subscribe"],"Resource":["arn:aws:sns:us-west-2:001234567890:s3_mybucket"]}]}                 |
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > ```
6. Return to the AWS Management Console. Choose **Topics** from the left-hand navigation pane.
7. Select the topic for your S3 bucket, and click the **Edit** button. The **Edit** page opens.
8. Click **Access policy - Optional** to expand this area of the page.
9. Merge the IAM policy addition from the SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY function results into the JSON document.

   For example:

   **Original IAM policy (abbreviated):**

   > Copy code
   >
   > ```
   > {
   >   "Version":"2008-10-17",
   >   "Id":"__default_policy_ID",
   >   "Statement":[
   >   {
   >      "Sid":"__default_statement_ID",
   >      "Effect":"Allow",
   >      "Principal":{
   >         "AWS":"*"
   >      }
   >      ..
   >   }
   > ]
   >  }
   > ```

   **Merged IAM policy:**

   > Copy code
   >
   > ```
   > {
   >   "Version":"2008-10-17",
   >   "Id":"__default_policy_ID",
   >   "Statement":[
   >   {
   >      "Sid":"__default_statement_ID",
   >      "Effect":"Allow",
   >      "Principal":{
   >         "AWS":"*"
   >      }
   >      ..
   >   },
   >   {
   >      "Sid":"1",
   >      "Effect":"Allow",
   >      "Principal":{
   >        "AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
   >       },
   >       "Action":[
   >         "sns:Subscribe"
   >       ],
   >       "Resource":[
   >         "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
   >       ]
   >   }
   > ]
   >  }
   > ```
10. Add an additional policy grant to allow S3 to publish event notifications for the bucket to the SNS topic.

For example (using the SNS topic ARN and S3 bucket used throughout these instructions):

> Copy code
>
> ```
> {
>  "Sid":"s3-event-notifier",
>  "Effect":"Allow",
>  "Principal":{
>     "Service":"s3.amazonaws.com"
>  },
>  "Action":"SNS:Publish",
>  "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
>  "Condition":{
>     "ArnLike":{
>        "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
>     }
>  }
>  }
> ```

**Merged IAM policy:**

> Copy code
>
> ```
> {
>   "Version":"2008-10-17",
>   "Id":"__default_policy_ID",
>   "Statement":[
>   {
>      "Sid":"__default_statement_ID",
>      "Effect":"Allow",
>      "Principal":{
>         "AWS":"*"
>      }
>      ..
>   },
>   {
>      "Sid":"1",
>      "Effect":"Allow",
>      "Principal":{
>        "AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
>       },
>       "Action":[
>         "sns:Subscribe"
>       ],
>       "Resource":[
>         "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
>       ]
>   },
>   {
>      "Sid":"s3-event-notifier",
>      "Effect":"Allow",
>      "Principal":{
>         "Service":"s3.amazonaws.com"
>      },
>      "Action":"SNS:Publish",
>      "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
>      "Condition":{
>         "ArnLike":{
>            "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
>         }
>      }
>    }
> ]
>  }
> ```

11. Click **Save changes**.

### Step 2: Create a stage with an included directory table

Create an external stage that references your S3 bucket using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads
your staged data files into the directory table metadata. Alternatively, you can use an existing external stage.

Note

- To configure secure access to the cloud storage location, see [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage) (in this topic).
- To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration
  object.

Copy code

```
-- External stage
CREATE [ OR REPLACE ] [ TEMPORARY ] STAGE [ IF NOT EXISTS ] <external_stage_name>
      <cloud_storage_access_settings>
    [ FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } [ formatTypeOptions ] } ) ]
    [ directoryTable ]
    [ COPY_OPTIONS = ( copyOptions ) ]
    [ COMMENT = '<string_literal>' ]
```

Where:

> Copy code
>
> ```
> directoryTable (for Amazon S3) ::=
>   [ DIRECTORY = ( ENABLE = { TRUE | FALSE }
>                   [ AUTO_REFRESH = { TRUE | FALSE } ]
>                   [ AWS_SNS_TOPIC = '<sns_topic_arn>' ] ) ]
> ```

#### Directory table parameters (`directoryTable`)

`ENABLE = { TRUE | FALSE }`
:   Specifies whether to add a directory table to the stage. When the value is TRUE, a directory table is created with the stage.

    Default: `FALSE`

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable triggering automatic refreshes of the directory table metadata when new or updated data
    files are available in the named external stage specified in the URL value.

    `TRUE`
    :   Snowflake enables triggering automatic refreshes of the directory table metadata.

    `FALSE`
    :   Snowflake does not enable triggering automatic refreshes of the directory table metadata. You must manually refresh the directory table
        metadata periodically using [ALTER STAGE](/sql-reference/sql/alter-stage) … REFRESH to synchronize the metadata with the current list of
        files in the stage path.

    Default: `FALSE`

**Amazon S3**

> `AWS_SNS_TOPIC = '<sns_topic_arn>'`
> :   Specifies the ARN for the SNS topic for your S3 bucket. The CREATE directory table statement subscribes the Snowflake SQS queue to the
>     specified SNS topic.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`.

> Copy code
>
> ```
> USE SCHEMA mydb.public;
> ```

Copy code

```
CREATE STAGE mystage
  URL='s3://load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (
    ENABLE = true
    AUTO_REFRESH = true
    AWS_SNS_TOPIC = 'arn:aws:sns:us-west-2:001234567890:s3_mybucket'
  );
```

When new or updated data files are added to the cloud storage location, the event notification informs Snowflake to scan them into the
directory table metadata.

### Step 3: Manually refresh the directory table metadata

Refresh the metadata in a directory table manually using the [ALTER STAGE](/sql-reference/sql/alter-stage) command.

Copy code

```
ALTER STAGE [ IF EXISTS ] <name> REFRESH [ SUBPATH = '<relative-path>' ]
```

Where:

`REFRESH`
:   Accesses the staged data files referenced in the directory table definition and updates the table metadata:

    - New files in the path are added to the table metadata.
    - Changes to files in the path are updated in the table metadata.
    - Files no longer in the path are removed from the table metadata.

    Currently, it is necessary to execute this command each time files are added to the stage, updated, or dropped. This step synchronizes
    the metadata with the latest set of associated files in the stage definition for the directory table.

`SUBPATH = '<relative-path>'`
:   Optionally specify a relative path to refresh the metadata for a specific subset of the data files.

For example, manually refresh the directory table metadata in a stage named `mystage`:

Copy code

```
ALTER STAGE mystage REFRESH;
```

Important

If this step is not completed successfully at least once after the directory table is created, querying the directory table returns no
results until a notification event triggers the directory table metadata to refresh automatically for the first time.

### Step 4: Configure security

For each additional role that will be used to query the directory table, grant sufficient access control privileges on the various objects
(i.e. the database(s), schema(s), stage, and table) using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE |  |

Expand

Show lessSee more
