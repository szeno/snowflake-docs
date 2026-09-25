Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Snowflake Openflow Connector for Kafka: Configuring AWS MSK IAM Authentication

AWS MSK IAM authentication allows you to use AWS Identity and Access Management (IAM) to authenticate to Amazon Managed Streaming for Apache Kafka (MSK).

## Prerequisites

- Your Kafka cluster must be Amazon MSK with IAM authentication enabled.
- You need to provide IAM credentials in Openflow with BYOC (bring your own cloud) configurations, deployed in your cloud.
- The IAM role or user must have the necessary MSK permissions.

## Step 1: Create AmazonMSKConnectionService

From the Openflow canvas, access the Controller Services configuration:

1. Double-click on the connector’s processing group.
2. Right-click on the canvas and select Controller Services.

Add a new AmazonMSKConnectionService:

1. Select **+** to add a new controller service.
2. Select **AmazonMSKConnectionService** from the list. If two services with this name appear, select the one without the
   Snowflake badge. The Snowflake-badged service is deprecated and doesn’t support IAM authentication through a web
   identity provider.
3. Select **Add**.

Configure the AmazonMSKConnectionService properties:

| Property | Value |
| --- | --- |
| SASL Mechanism | `AWS_MSK_IAM` |
| Security Protocol | `#{Kafka Security Protocol}` |
| Bootstrap Servers | `#{Kafka Bootstrap Servers}` |

Expand

Show lessSee more

Verify the AmazonMSKConnectionService:

1. Select **Verify** for the service.
2. Confirm that the service status shows as **Verified**.

## Step 2: Configure ConsumeKafka Processor

1. In your Kafka connector locate the ConsumeKafka processor.
2. Configure the processor to use the new connection service:

   Set the **Kafka Connection Service** property to the AmazonMSKConnectionService you created in [Step 1: Create AmazonMSKConnectionService](#label-openflow-kafka-aws-msk-iam-auth-step1).

## Step 3 (Optional): Remove Old Kafka Connection Service

1. In the Controller Services tab, locate the old Kafka3Connection service.
2. Disable and remove the old service:
   1. Select **Disable** for the old service.
   2. After it’s disabled, select **Delete** to remove the old service.
