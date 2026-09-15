# Openflow BYOC - Set up encrypted EBS volumes

Feature — Generally Available

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic describes the steps to set up an Openflow BYOC deployment with encrypted Elastic Block Storage (EBS) volumes using one of the following methods:

- [Provide a specific AWS KMS Key for Encrypted EBS Volumes](#label-openflow-byoc-encrypted-ebs-kms-key)
- [Enable Encrypted EBS Volumes by default for your AWS Account](#label-openflow-byoc-encrypted-ebs-default-encryption)

Both of these solutions provide encrypted EBS volumes that meet the following storage requirements of Openflow BYOC:

- Root volume for the Openflow Agent EC2 instance
- Root volumes for the EC2 instances in each EKS Cluster Node Group
- Persistent volumes for Openflow’s runtimes and supporting components

Note

- `$AWS_ACCOUNT_ID` represents the AWS Account ID of the account where Openflow is deployed.
- `$AWS_REGION` represents the AWS Region of the account, for example `us-west-2`.
- `$AWS_KMS_KEY_ARN` represents the Amazon Resource Name (ARN) of the Amazon Key Management Service (AWS KMS) key that Openflow will use for encrypted EBS volumes.
- `$DEPLOYMENT_KEY` represents the Openflow unique identifier applied to cloud resources created and managed by Openflow for a particular deployment.
  This is in the `DataPlaneKey` parameter of the CloudFormation template, also available in Openflow through the **View Details** menu option for the deployment.

## Prerequisites

This topic assumes that you have completed the prerequisites for setting up Openflow BYOC. For more information, see [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).

You must also have access to an AWS KMS key that Openflow will use for encrypted EBS volumes.

## Provide a specific AWS KMS Key for Encrypted EBS Volumes

When uploading the CloudFormation template for your Openflow BYOC Deployment, you can provide the ARN for the AWS KMS key that Openflow uses for encrypted EBS volumes.

Using this configuration, Openflow makes requests for encrypted EBS volumes, ensuring that all SCP policies are satisfied. Snowflake recommends this approach for most customers.

This allows you to use different KMS keys for different applications, reducing the risk of a single key being compromised.

To ensure that Openflow has the necessary permissions to use this key, perform the following tasks:

1. Ensure that the AWS KMS key grants permissions to the AWS Autoscaling Service Role. The Key Policy must include the following statement:

   Copy code

   ```
   {
   "Sid": "Allow Autoscaling to use the key",
   "Effect": "Allow",
   "Principal": {
    "AWS": "arn:aws:iam::$AWS_ACCOUNT_ID:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
   },
   "Action": [
    "kms:CreateGrant",
    "kms:Decrypt",
    "kms:Encrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:DescribeKey"
   ],
   "Resource": "*"
   }
   ```
2. Enter the ARN of the AWS KMS key in the `EBSKMSKeyArn` parameter of the CloudFormation stack when uploading the template.
   For example, `arn:aws:kms:$AWS_REGION:$AWS_ACCOUNT_ID:key/1a1a11aa-aa1a-aaa1a-a1a1-000000000000`.

   Approximately 20 minutes after uploading the CloudFormation template, the Openflow BYOC Deployment creates a new IAM Role with the name `$DEPLOYMENT_KEY-eks-role`.
3. Add the following statement to the KMS key policy to grant permissions for Openflow to use the key:

   Copy code

   ```
   {
   "Sid": "Allow Openflow Deployment to encrypt EBS volumes",
   "Effect": "Allow",
   "Principal": {
    "AWS": "arn:aws:iam::$AWS_ACCOUNT_ID:role/$DEPLOYMENT_KEY-eks-role"
   },
   "Action": [
    "kms:Decrypt",
    "kms:Encrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:CreateGrant",
    "kms:DescribeKey"
   ],
   "Resource": "*"
   }
   ```

Openflow automatically detects the new permissions for the KMS key and continues the installation process. The Openflow BYOC deployment will become `Active` after approximately 20 minutes.

## Enable Encrypted EBS Volumes by default for your AWS Account

AWS accounts can encrypt new EBS volumes by default by following the [AWS EBS encryption by default documentation](https://docs.aws.amazon.com/ebs/latest/userguide/encryption-by-default.html).

With this configuration, Openflow makes requests for unencrypted EBS volumes, but the AWS API will return an encrypted EBS volume. The following steps ensure that Openflow has permissions to use the KMS key for these encrypted volumes.

Whether you choose to use the AWS managed key `aws/ebs` or your own KMS key, you must attach an IAM Policy to the Openflow IAM Role `$DEPLOYMENT_KEY-eks-role` that grants the necessary permissions to use the key.

1. Create an IAM Policy to allow Openflow to use the KMS key by replacing `$AWS_KMS_KEY_ARN` with the ARN of the KMS key.

   Copy code

   ```
   {
   "Sid": "Allow Openflow EKS Role to encrypt EBS volumes",
   "Effect": "Allow",
   "Action": [
    "kms:Decrypt",
    "kms:Encrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:CreateGrant",
    "kms:DescribeKey"
   ],
   "Resource": "$AWS_KMS_KEY_ARN"
   }
   ```
2. Ensure that the AWS KMS key grants permissions to the AWS Autoscaling Service Role. The Key Policy must include the following statement:

   Copy code

   ```
   {
   "Sid": "Allow Autoscaling to use the key",
   "Effect": "Allow",
   "Principal": {
    "AWS": "arn:aws:iam::$AWS_ACCOUNT_ID:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
   },
   "Action": [
    "kms:CreateGrant",
    "kms:Decrypt",
    "kms:Encrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:DescribeKey"
   ],
   "Resource": "*"
   }
   ```
3. When uploading the Openflow BYOC CloudFormation template:

   - Leave the optional `EBSKMSKeyArn` parameter blank.
   - Set the `AdditionalEksRolePolicyArns` parameter to the ARN of the new IAM Policy created previously. For example, `arn:aws:iam::$AWS_ACCOUNT_ID:policy/openflow-kms-key-access-policy`.

   Approximately 20 minutes after uploading the CloudFormation template, the Openflow BYOC Deployment creates a new IAM Role with the name `$DEPLOYMENT_KEY-eks-role`.
4. Add the following statement to the KMS key policy to grant permissions for Openflow to use the key:

   Copy code

   ```
   {
   "Sid": "Allow Openflow Deployment to encrypt EBS volumes",
   "Effect": "Allow",
   "Principal": {
    "AWS": "arn:aws:iam::$AWS_ACCOUNT_ID:role/$DEPLOYMENT_KEY-eks-role"
   },
   "Action": [
    "kms:Decrypt",
    "kms:Encrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:CreateGrant",
    "kms:DescribeKey"
   ],
   "Resource": "*"
   }
   ```

Openflow automatically detects the new permissions for the KMS key and continues the installation process. The Openflow BYOC deployment will become `Active` after approximately 20 minutes.
