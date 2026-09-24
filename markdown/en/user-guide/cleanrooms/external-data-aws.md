# Snowflake Data Clean Room: External data from an Amazon S3 bucket

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

Data analyzed in a [Snowflake Data Clean Room](/user-guide/cleanrooms/overview) can be native to Snowflake, reside externally
in cloud provider storage, or both. A *connector* allows collaborators to access external data from a cloud provider from within the clean
room.

The external data connector uses [Snowflake external tables](/user-guide/tables-external-intro) to make data
available. Be aware that there is an increased security risk associated with linking external tables in a clean room. As a result,
the provider must explicitly allow the use of external tables in the clean room before
consumers can use a connector to include external data. If the provider uses the external data connector, the consumer is warned that
external tables are being used so they can decide whether to install the clean room.

This topic describes how to use a connector so that clean room analysts can access external data from an Amazon S3 bucket.

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Prerequisites

To use the connector for external data:

- The provider must explicitly [allow the use of external tables in the clean room](/user-guide/cleanrooms/register-data).
- Files must be in parquet format.

## Connecting to an S3 bucket

The process of allowing clean room collaborators to access data from Amazon S3 storage consists of the following steps:

1. In AWS, complete these procedures:

   1. [Create an IAM policy](#label-cleanrooms-external-data-aws-iam-policy) with specific permissions.
   2. [Create an IAM role](#label-cleanrooms-external-data-aws-iam-role) that references the new IAM policy.
   3. [Copy the identifiers of the S3 bucket and IAM role](#label-cleanrooms-external-data-aws-copy).
2. In the clean room environment, [create the connector](#label-cleanrooms-external-data-aws-create-connector).
3. In AWS, [update the IAM role](#label-cleanrooms-external-data-aws-update-role) with the service account identifiers from the clean
   room environment.
4. In the clean room environment, [authenticate the connector with AWS](#label-cleanrooms-external-data-aws-authenticate).

### Create an IAM policy in AWS

Snowflake recommends that you create a dedicated IAM policy for the connector that includes the necessary permissions to access the S3 bucket. In a
subsequent step, you add this policy to an IAM role that represents the identity of the connector.

To complete this procedure, you need to know the region of the account associated with the clean room environment.

- To find the region of the account associated with the clean room environment, [log in to the clean room](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in), and select **Connectors** » **Cleanrooms** » **Snowflake**.

To create an IAM policy that contains permissions to the S3 bucket:

1. Sign in to the **AWS Management Console**.
2. From the **Console Home** dashboard, select **Identity and Access Management (IAM)**.
3. In the left navigation, select **Account settings**.
4. In the **Security Token Service (STS)** section, find the region of the account associated with the clean room environment, and
   toggle it to **Active**.
5. In the left navigation, select **Policies**.
6. Select **Create policy**.
7. In the **Policy editor** section, select **JSON**.
8. Copy and paste the following policy body into the policy editor, and then edit the JSON to include your bucket name (`<bucket>`) and folder
   path prefix (`<prefix>`):

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

   Be sure to keep the `:::` format. For example, if your S3 bucket URI is `s3://sales/customers/`, the value of the `Resource` JSON field is `arn:aws:s3:::sales/customers/*`.
9. Select **Next**.
10. Enter a policy name (for example, `snowflake_cleanroom_access`), and then select **Create policy**.

### Create an IAM role in AWS

The AWS IAM role represents the identity of the connector. During the creation process, you associate the
role with the new IAM policy that grants permissions needed by the connector to access the S3 bucket.

To create a new IAM role:

1. From the **Console Home** dashboard in AWS, select **Identity and Access Management (IAM)**.
2. In the left navigation, select **Roles**.
3. Select **Create role**.
4. In the **Trusted entity type** section, select **AWS account**.
5. In the **An AWS account** section, select **Another AWS account**.
6. In the **Account ID** field, enter a temporary placeholder value that contains 12 digits (for example, the account identifier of
   the current AWS account). You will replace this value later.
7. Select **Require external id**, and then enter a temporary placeholder value, such as `0000`. You will replace this value later.
8. Select **Next**.
9. In the **Permissions policies** section, find the policy that you created in the previous procedure, and select its check box.
10. Select **Next**.
11. Enter a role name (for example, `snowflake_cleanroom_connector`), and then select **Create role**.

### Copy the S3 bucket and IAM role identifiers

When creating the connector in the clean room environment, you need the identifiers of the S3 bucket and the IAM role. Before creating
the connector, follow these steps to copy and save these identifiers:

To copy the IAM role identifier:

1. From the **Console Home** dashboard in AWS, select **Identity and Access Management (IAM)**.
2. In the left navigation, select **Roles**.
3. Find the role that you created in the previous procedure, and select it to open
   it.
4. In the **Summary** section, find the **ARN** and select the copy icon. Save this role identifier for a later step.

To copy the S3 bucket identifier:

1. From the **Console Home** dashboard in AWS, select **S3**.
2. Find the name of your S3 bucket and select it to open it. The bucket must contain the data that you want to include in the clean room.
3. Navigate into the prefix of the bucket, and then select **Copy S3 URI**. Save this bucket identifier for a later step.

   Don’t try to select the button in the **Objects** section.

### Create a connector and copy the service account details

You are now ready to create the connector in the clean room environment. After you create the connector, copy details about
its service account so it can be associated with the IAM role in AWS.

To create the connector in your clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors**, and then expand the **Amazon Web Services** section.
3. In the **AWS Role ARN** field, enter the identifier of the IAM role that you copied from AWS, such as
   `arn:aws:iam::772412615275:role/mub00002_vhb71832_role`.
4. In the **S3 Bucket URI** field, enter the identifier of the S3 bucket that you copied from AWS, such as
   `s3://sales/customer_data/`.
5. Select **Create**.

   The clean room generates a service account that it uses to access AWS.
6. Use the copy icon to copy the **Principal** and **External ID** identifiers of the connector’s service account, and save them for
   the next procedure.

### Update the IAM role with service account details

You are now ready to update the IAM role with the identifiers associated with the connector’s service account. To update the IAM role:

1. Sign in to the **AWS Management Console**.
2. From the **Console Home** dashboard, select **Identity and Access Management (IAM)**.
3. In the left navigation, select **Roles**.
4. Find the role that you created earlier, and select it to open it.
5. Select the **Trust relationships** tab.
6. Select **Edit trust policy**.
7. Modify the JSON of the trust policy to include the identifiers from the connector’s service account. You copied these identifiers
   earlier. Make the following changes to the JSON:

   - Replace the value of the `AWS` JSON field with the **Principal** value you copied from the clean room environment.

     In the following example, the value of **Principal** in the clean room environment is `arn:aws:iam::115136555074:user/x4gy-s-p2345g38`.
   - Replace the value of the `sts:ExternalId` JSON field with the **External ID** value you copied from the clean room environment.

     In the following example, the value of **External ID** in the clean room environment is `UCA56729_SFCRole=4447_uht2344sdf3mrWLNRM0y3bE=`.

     Copy code

     ```
     {
       "Version": "2012-10-17",
       "Statement": [
         {
     "Sid": "Statement1",
     "Effect": "Allow",
     "Principal": {
       "AWS": "arn:aws:iam::115136555074:user/x4gy-s-p2345g38"
     },
     "Action": "sts:AssumeRole",
     "Condition": {
       "StringEquals": {
         "sts:ExternalId": "UCA56729_SFCRole=4447_uht2344sdf3mrWLNRM0y3bE="
       }
     }
         }
       ]
     }
     ```
8. Select **Update policy**.

### Authenticate the connector

You are now ready to authenticate the connector to make sure it can access the S3 bucket. To authenticate the connector:

1. If you are signed out of the clean room environment, see [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the clean room environment, select **Connectors** and expand the **Amazon Web Services** section.
3. Select the S3 bucket you are connecting to, and then select **Authenticate**.

## Remove access to external data on AWS

To remove access to an S3 bucket from a clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors** and expand the **Amazon Web Services** section.
3. Find the S3 bucket that is currently connected, and then select the trash can icon.
