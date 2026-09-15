# Validate your BYOC deployment

Feature — Generally Available

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic describes how to use BYOC Pre-flight Validation to verify your AWS
network configuration for Openflow deployments.

## About BYOC Pre-flight Validation

BYOC Pre-flight Validation is a script that verifies your AWS network
environment is ready for an Openflow deployment. It checks that required
networking, connectivity, and access settings are in place.

Use this tool to identify and resolve network or access misconfigurations
before deployment. This helps prevent failures and ensures a smoother rollout
by providing specific feedback and actionable guidance for any issues found.

There are two versions of this script:

`byoc-validator.sh`:
:   Verifies that your AWS environment is ready for a new Openflow deployment.

`byo-vpc-validator.sh`:
:   Verifies that your existing VPC is configured correctly for Openflow.

## What does BYOC Pre-flight Validation review?

BYOC Pre-flight Validation performs a pre-deployment review that verifies your
existing AWS setup, identifies issues, and explains what needs to be corrected.

BYOC Pre-flight Validation checks the following:

- Prerequisites (applies only to existing VPCs)

  - VPC components such as subnets, gateways, and routing
  - Network sizing and placement across availability zones
  - Required resource tags
- Network connectivity

  - Access to Openflow services and endpoints
  - Image registry access for required containers
  - Connectivity to core AWS services
- Permissions

  - Security group rules
  - Required IAM permissions
  - Encryption key access when needed

BYOC Pre-flight Validation checks the resource tags that are required for deployment readiness, such
as the subnet tags needed by Openflow. It does not validate your organization’s complete cost
allocation, governance, or compliance tagging policy.

## When to use BYOC Pre-flight Validation?

Use BYOC Pre-flight Validation:

- Before your initial Openflow deployment
- After AWS networking changes that might impact connectivity
- During troubleshooting to confirm your setup
- When migrating Openflow to a new VPC or AWS account

## Download the CloudFormation template for BYOC Pre-flight Validation

Follow these steps to set up BYOC Pre-flight Validation in your AWS environment:

1. Create a new BYOC deployment in the Openflow Control Plane.
2. Download the CloudFormation template for BYOC Pre-flight Validation.

   To download the CloudFormation template for BYOC Pre-flight Validation, click
   **Download Validator** in the confirmation dialog that appears after
   creating the deployment.
3. Apply the BYOC Pre-flight Validation CloudFormation template in AWS.
4. Access the EC2 instance where BYOC Pre-flight Validation is installed.

## Configure the CloudFormation template for BYOC Pre-flight Validation

The CloudFormation template for the BYOC validator includes defaults for all
parameters, and those defaults should not be changed.

The CloudFormation template for the BYO-VPC validator includes defaults for most
parameters, and those defaults should not be changed. However, the following
parameters do not have defaults and must be provided, using the inputs you plan
to use for the actual deployment:

`InfraVPC`
:   Select an existing VPC.

`PrivateSubnet1`
:   The first private subnet for Openflow runtimes.

`PrivateSubnet2`
:   The second private subnet for the EKS control plane.

`PrivateSecurityGroup`
:   Security group for the agent instance, EC2 Instance Connect endpoint, and EKS
    cluster.

`EBSKMSKeyArn`
:   Optional KMS key ARN for encrypted EBS volumes.

## Run BYOC Pre-flight Validation and view results

Follow these steps to run BYOC Pre-flight Validation:

1. Connect to the EC2 instance where BYOC Pre-flight Validation is installed.
2. Run the BYOC Pre-flight Validation script from the home directory:

   Copy code

   ```
   /home/ec2-user/byoc-validator.sh
   ```

   You can run BYOC Pre-flight Validation as many times as needed.
3. Review the output file in the `home` directory:

   Each run produces a new, timestamped results file, for example:
   `/home/ec2-user/byoc-validation-results-YYYYMMDDHHMMSS.txt`
4. Open and inspect the results:

   Use a tool of your preference to read the output and review pass/fail
   messages.

Follow these steps to run BYOC Pre-flight Validation for an existing VPC:

1. Connect to the EC2 instance where BYOC Pre-flight Validation is installed.
2. Run the BYOC Pre-flight Validation script in the home directory:

   Copy code

   ```
   /home/ec2-user/byo-vpc-validator.sh
   ```

   You can run BYOC Pre-flight Validation as many times as needed.
3. Review the output file in the `home` directory:

   Each run produces a new, timestamped results file, for example:
   `/home/ec2-user/byo-vpc-validation-results-YYYYMMDDHHMMSS.txt`
4. Open and inspect the results:

   Use a tool of your preference to read the output and review pass/fail
   messages.

## Example output

The following example shows a successful validation output:

```
2026-01-15 11:43:37,599 - INFO - Starting BYO-VPC validation suite...
2026-01-15 11:43:37,599 - INFO - ============================================================
...
2026-01-15 11:43:37,599 - INFO - Starting Prerequisites validation...
2026-01-15 11:43:37,704 - INFO - Running validation rule: internet_gateway
2026-01-15 11:43:38,538 - INFO - ✅ internet_gateway: Internet Gateway validation passed
...
2026-01-15 11:43:39,769 - INFO - Prerequisites Summary: 4/4 rules passed
2026-01-15 11:43:39,769 - INFO - --------------------------------------------------
2026-01-15 11:43:39,769 - INFO - Starting Network validation...
2026-01-15 11:43:39,780 - INFO - Running validation rule: snowflake_authentication
2026-01-15 11:43:41,130 - INFO - ✅ snowflake_authentication: Snowflake OAuth authentication successful
...
2026-01-15 11:43:55,920 - INFO - Network Summary: 7/7 rules passed
2026-01-15 11:43:55,920 - INFO - --------------------------------------------------
2026-01-15 11:43:55,920 - INFO - Starting Permissions validation...
2026-01-15 11:43:55,946 - INFO - Running validation rule: private_security_group
2026-01-15 11:43:56,766 - INFO - ✅ private_security_group: Private security group validation passed
...
2026-01-15 11:43:57,560 - INFO - Permissions Summary: 2/2 rules passed
2026-01-15 11:43:57,560 - INFO - ============================================================
2026-01-15 11:43:57,560 - INFO - 🎉 Openflow compatibility checker completed successfully!
```

The output highlights each check with a status icon:

- ✅ - The requirement is met.
- ❌ - The requirement is not met, and action is needed.

## AWS permissions required

The CloudFormation template creates an IAM role with the necessary permissions
for the EC2 instance where BYOC Pre-flight Validation is installed. If your
organization uses custom IAM controls, ensure the instance role includes the
following permissions:

- Required to access the Snowflake OAuth secret created by the template:

  - `secretsmanager:GetSecretValue`
- Required to inspect network resources:

  - `ec2:DescribeInternetGateways`
  - `ec2:DescribeSubnets`
  - `ec2:DescribeRouteTables`
  - `ec2:DescribeNATGateways`
  - `ec2:DescribeSecurityGroups`
- Required only when validating an optional EBS KMS key:

  - `kms:DescribeKey`
  - `kms:GetKeyPolicy`

The Secrets Manager permission is scoped to the BYOC Pre-flight Validation
secret created by the template. The EC2 and KMS actions can be scoped to `*`
(read-only metadata).

## Cleanup

After validation is complete, you can delete BYOC Pre-flight Validation to
avoid ongoing AWS costs. To delete BYOC Pre-flight Validation, delete the
CloudFormation stack used to create it. This automatically removes the EC2
instance, the IAM role, and the Secrets Manager secret.
