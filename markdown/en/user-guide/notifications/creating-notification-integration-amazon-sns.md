# Creating a notification integration to send notifications to an Amazon SNS topic

To send notifications to an Amazon SNS topic, you must create a notification integration for that topic. To do this:

1. [Create an Amazon SNS topic](#label-notification-integration-amazon-sns-topic)
2. [Create the IAM policy that grants permission to publish to this topic](#label-notification-integration-amazon-iam-policy).
3. [Create the IAM role that you attach to this policy](#label-notification-integration-amazon-iam-role).
4. [Create a notification integration](#label-notification-integration-amazon-creating-integration).
5. [Grant Snowflake access to the topic](#label-notification-integration-amazon-granting-access).

Note

Currently, this feature is limited to Snowflake accounts hosted on AWS.

## Create an Amazon SNS topic

Create an SNS topic in your AWS account to handle the notifications. Record the Amazon Resource Name (ARN) for the SNS topic.

Note

Only standard SNS topics are supported. Do not create SNS FIFO (first in, first out) topics for use with error notifications.
Currently, error notifications sent to FIFO topics fail silently.

To reduce latency and avoid [data egress](/user-guide/cost-understanding-data-transfer) charges for sending notifications
across [regions](/user-guide/intro-regions), we recommend creating the SNS topic in the same region as your Snowflake
account.

For instructions, see the [Creating an Amazon SNS topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html) in
the SNS documentation.

## Create the IAM policy

Create an AWS Identity and Access Management (IAM) policy that grants permissions to publish to the SNS topic. The policy defines the following actions:

- `sns:publish`: Publish to the SNS topic.

1. Log into the AWS Management Console.
2. From the home dashboard, choose **Identity & Access Management** (IAM).
3. Choose **Account settings** from the left-hand navigation pane.
4. Expand the **Security Token Service Regions** list, find the AWS region corresponding to the
   [region](/user-guide/intro-regions) where your account is located, and choose **Activate** if the status is
   **Inactive**.
5. Choose **Policies** from the left-hand navigation pane.
6. Select **Create Policy**.
7. Select the **JSON** tab.
8. Add a policy document that defines actions that can be taken on your SNS topic.

   Copy and paste the following text into the policy editor:

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "<sns_topic_arn>"
    }
     ]
   }
   ```

   Replace `sns_topic_arn` with the ARN of the
   [SNS topic that you created earlier](#label-notification-integration-amazon-sns-topic).
9. Select **Review policy**.
10. Enter the policy name (e.g. `snowflake_sns_topic`) and an optional description, and select **Create policy**.

## Create the AWS IAM role

Create an AWS IAM role on which to assign privileges on the SNS topic.

1. Log into the AWS Management Console.
2. From the home dashboard, choose **Identity & Access Management** (IAM):
3. Choose **Roles** from the left-hand navigation pane.
4. Select **Create role**.
5. Select **Another AWS account** as the trusted entity type.
6. In the **Account ID** field, enter your own AWS account ID temporarily.
7. Select the **Require external ID** option. This option enables you to grant permissions on your Amazon account resources
   (i.e. SNS) to a third party (i.e. Snowflake).

   For now, enter a dummy ID such as `0000`. Later, you will modify the trust relationship and replace the dummy ID with the
   external ID for the Snowflake IAM user generated for your account. A condition in the trust policy for your IAM role allows
   your Snowflake users to assume the role using the notification integration object you will create later.
8. Select **Next**.
9. Locate the [policy that you created earlier](#label-notification-integration-amazon-iam-policy), and select this policy.
10. Select **Next**.
11. Enter a name and description for the role, and select **Create role**.
12. Record the **Role ARN** value located on the role summary page. You will specify this value in one or more later steps.

## Create the notification integration

Run the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-outbound-aws) command to
create a notification integration. An integration is a Snowflake object that references the SNS topic you created.

Note

If you plan to use the integration for notifications about errors in [tasks](/user-guide/tasks-errors) or
[pipes](/user-guide/data-load-snowpipe-errors), a single notification integration can support multiple tasks or pipes.

When running the command, set these parameters to the following values:

- Set AWS\_SNS\_TOPIC\_ARN to the [SNS topic ARN you recorded earlier](#label-notification-integration-amazon-sns-topic).
- Set AWS\_SNS\_ROLE\_ARN to the [IAM role ARN you recorded earlier](#label-notification-integration-amazon-iam-role).

  Note

  The value of AWS\_SNS\_ROLE\_ARN is case-sensitive. Use the exact value that is specified in your AWS account.

For example:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  ENABLED = TRUE
  DIRECTION = OUTBOUND
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AWS_SNS
  AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-2:111122223333:sns_topic'
  AWS_SNS_ROLE_ARN = 'arn:aws:iam::111122223333:role/error_sns_role';
```

## Grant Snowflake access to the SNS topic

### Retrieve the IAM user ARN and SNS topic external ID

1. Execute the [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) command to display the properties of the notification
   integration that you just created.

   For example, to display the properties of the notification integration named `my_notification_int`:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION my_notification_int;
   ```

   ```
   +---------------------------+-------------------+------------------------------------------------------+----------------------+
   |   property                |   property_type   |   property_value                                     |   property_default   |
   +---------------------------+-------------------+------------------------------------------------------+----------------------+
   |   ENABLED                 |   Boolean         |   true                                               |   false              |
   |   NOTIFICATION_PROVIDER   |   String          |   AWS_SNS                                            |                      |
   |   DIRECTION               |   String          |   OUTBOUND                                           |   INBOUND            |
   |   AWS_SNS_TOPIC_ARN       |   String          |   arn:aws:sns:us-east-2:111122223333:myaccount       |                      |
   |   AWS_SNS_ROLE_ARN        |   String          |   arn:aws:iam::111122223333:role/myrole              |                      |
   |   SF_AWS_IAM_USER_ARN     |   String          |   arn:aws:iam::123456789001:user/c_myaccount         |                      |
   |   SF_AWS_EXTERNAL_ID      |   String          |   MYACCOUNT_SFCRole=2_a123456/s0aBCDEfGHIJklmNoPq=   |                      |
   +---------------------------+-------------------+------------------------------------------------------+----------------------+
   ```
2. Record the values of the following properties:

   - SF\_AWS\_IAM\_USER\_ARN

     ARN for the Snowflake IAM user created for your account. Users in your Snowflake account will assume the
     [IAM role you created earlier](#label-notification-integration-amazon-iam-role) by submitting the external ID for this
     user using your notification integration.
   - SF\_AWS\_EXTERNAL\_ID

     External ID for the Snowflake IAM user created for your account.

   In the next step, you will update the trust relationship for the IAM role with these values.

Note the DIRECTION property, which indicates the direction of the cloud messaging with respect to Snowflake.

### Modify the trust relationship in the IAM role

1. Log into the AWS Management Console.
2. From the home dashboard, choose **Identity & Access Management** (IAM):
3. Choose **Roles** from the left-hand navigation pane.
4. Select the [role you created earlier](#label-notification-integration-amazon-iam-role).
5. Select the **Trust relationships** tab.
6. Select **Edit trust relationship**.
7. Modify the policy document to use the
   [values of the notification integration properties that you recorded earlier](#label-notification-integration-amazon-granting-access-retrieve).

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
        "AWS": "<sf_aws_iam_user_arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<sf_aws_external_id>"
        }
      }
    }
     ]
   }
   ```

   Where:

   - `sf_aws_iam_user_arn` is the SF\_AWS\_IAM\_USER\_ARN value you recorded.
   - `sf_aws_external_id` is the SF\_AWS\_EXTERNAL\_ID value you recorded.
8. Select **Update Trust Policy**. The changes are saved.
