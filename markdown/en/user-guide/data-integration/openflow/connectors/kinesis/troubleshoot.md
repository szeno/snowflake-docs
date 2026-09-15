# Troubleshooting the Openflow Connector for Amazon Kinesis Data Streams

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to troubleshoot common issues with the
Openflow Connector for Amazon Kinesis Data Streams.

## Common errors

### Error: UnknownHostException

**Error message**

```
java.net.UnknownHostException: dynamodb.eu-west-1.amazonaws.com
```

**Cause**

If the runtime is using a Snowflake Deployment, the network rule is most likely misconfigured.

**Solution**

Make sure the required AWS domains are allowlisted in your network rule.
For the list of required domains, see
[Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

### Error: Connect timed out to DynamoDB

**Error message**

```
software.amazon.awssdk.core.exception.SdkClientException: Unable to execute HTTP request:
Connect to https://dynamodb.us-east-1.amazonaws.com:443 failed: Connect timed out
```

**Cause**

This occurs when the AWS PrivateLink configuration uses `PRIVATE_HOST_PORT` for `dynamodb.us-east-1.amazonaws.com`. DNS resolves to the
PrivateLink endpoint IP, but the TCP connection can’t be established because Amazon DynamoDB doesn’t
support Private DNS for its PrivateLink endpoints.

**Solution**

Use `HOST_PORT` for DynamoDB instead of `PRIVATE_HOST_PORT`. Only checkpoint metadata flows through DynamoDB; stream records continue through the Kinesis PrivateLink endpoints.
For the full PrivateLink configuration, see [(Optional) Configure outbound AWS PrivateLink](/user-guide/data-integration/openflow/connectors/kinesis/setup#label-kinesis-configure-aws-privatelink).
