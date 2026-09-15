# Maintain Openflow Connector for Amazon Kinesis Data Streams

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to maintain the Openflow Connector for Amazon Kinesis Data Streams connector, including how to manage and reset the connector state.

## Manage connector state

The Openflow Connector for Amazon Kinesis Data Streams connector uses DynamoDB to store the consumer application state.

### DynamoDB table created by the connector

The connector creates a DynamoDB table with the name specified in `AWS Kinesis Application Name`.
The table stores the checkpointed sequence number for each shard in the stream. This tracks which records have been processed.

If multiple processors use the same application name, they cooperate to consume data from the stream
and share this table. If processors have different application names, each creates its own table
to independently track consumed records.

## Reset the connector state

If the connector state in DynamoDB becomes corrupted or inconsistent, you may need to reset it.
There are two approaches to reset the connector state.

### Reset by changing the application name

The simplest way to reset the connector state is to change the AWS Kinesis Application Name parameter:

1. Stop the connector.
2. Navigate to the connector’s parameter context.
3. Change the `AWS Kinesis Application Name` parameter value to a new value.
4. Start the connector.

The connector creates a new DynamoDB table with the new application name and begins consuming
records from the position specified by the [AWS Kinesis Initial Stream Position](/user-guide/data-integration/openflow/connectors/kinesis/setup#label-kinesis-json-source-parameters) parameter.

Note

- When you change the application name, the connector doesn’t delete the old DynamoDB table.
  You must manually delete it through the AWS Console or the AWS CLI.
- If your IAM policy restricts DynamoDB access to a specific table name, you must update the policy
  to allow access to the new table name. For more information on configuring IAM permissions,
  see [Set up Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/setup).

### Reset by deleting the DynamoDB table

Alternatively, you can delete the existing DynamoDB table to reset the state:

1. Stop the connector.
2. In the AWS Console or using the AWS CLI, delete the DynamoDB table associated with the application name.
3. Start the connector.

The connector recreates the table and begins consuming records from the position specified by the [AWS Kinesis Initial Stream Position](/user-guide/data-integration/openflow/connectors/kinesis/setup#label-kinesis-json-source-parameters) parameter.

Warning

Resetting the connector state causes the connector to reprocess records from the position specified by the
initial stream position. Depending on your [AWS Kinesis Initial Stream Position](/user-guide/data-integration/openflow/connectors/kinesis/setup#label-kinesis-json-source-parameters) setting,
this may result in duplicate data being ingested into Snowflake or data not being ingested at all.
