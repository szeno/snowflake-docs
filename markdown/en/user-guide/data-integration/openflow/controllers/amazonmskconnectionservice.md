# AmazonMSKConnectionService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides and manages connections to AWS MSK Kafka Brokers for producer or consumer operations.

Important

The component picker might list two controller services named `AmazonMSKConnectionService`. Select the service without
the Snowflake badge. The Snowflake-badged service is deprecated and doesn’t support workload identity federation.

## Tags

aws, kafka, managed, msk, openflow, streaming

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| SSL Context Service | SSL Context Service |  |  | Service supporting SSL communication with Kafka brokers |
| Acknowledgment Wait Time \* | ack.wait.time | 5 sec |  | After sending a message to Kafka, this indicates the amount of time that the service will wait for a response from Kafka.If Kafka does not acknowledge the message within this time period, the service will throw an exception. |
| AWS Profile Name | aws.profile.name |  |  | The Amazon Web Services Profile to select when multiple profiles are available. |
| AWS Role Source \* | AWS Role Source | Default Profile | - Default Profile - Specified Profile - Specified Role - Web Identity Provider | Selects how AWS credentials are sourced for AWS MSK IAM. |
| AWS Assume Role ARN \* | AWS Assume Role ARN |  |  | The AWS role ARN for cross-account access. This property is shown when AWS Role Source is set to Specified Role or Web Identity Provider. |
| AWS Assume Role Session Name \* | AWS Assume Role Session Name |  |  | The AWS role session name for cross-account access. This property is shown when AWS Role Source is set to Specified Role or Web Identity Provider. |
| AWS Web Identity Token Provider \* | AWS Web Identity Token Provider |  |  | Controller service that provides an OAuth2 OpenID Connect token. This property is shown when AWS Role Source is set to Web Identity Provider. |
| AWS Web Identity Session Time \* | AWS Web Identity Session Time | 3600 sec |  | Session time for AWS STS AssumeRoleWithWebIdentity, from 900 through 3600 seconds. This property is shown when AWS Role Source is set to Web Identity Provider. |
| AWS Web Identity STS Region | AWS Web Identity STS Region |  |  | Region identifier used for AWS Security Token Service when exchanging web identity tokens. This property is shown when AWS Role Source is set to Web Identity Provider. |
| AWS Web Identity STS Endpoint | AWS Web Identity STS Endpoint |  |  | Optional endpoint override for AWS Security Token Service. This property is shown when AWS Role Source is set to Web Identity Provider. |
| AWS Web Identity SSL Context Provider | AWS Web Identity SSL Context Provider |  |  | SSL Context Service used to communicate with AWS STS. This property is shown when AWS Role Source is set to Web Identity Provider. |
| Bootstrap Servers \* | bootstrap.servers |  |  | Comma-separated list of Kafka Bootstrap Servers in the format host:port. Corresponds to Kafka bootstrap.servers property |
| Client Timeout \* | default.api.timeout.ms | 60 sec |  | Default timeout for Kafka client operations. Mapped to Kafka default.api.timeout.ms. The Kafka request.timeout.ms property is derived from half of the configured timeout |
| Transaction Isolation Level \* | isolation.level | read\_committed | - Read Committed - Read Uncommitted | Specifies how the service should handle transaction isolation levels when communicating with Kafka.The uncommitted option means that messages will be received as soon as they are written to Kafka but will be pulled, even if the producer cancels the transactions.The committed option configures the service to not receive any messages for which the producer’s transaction was canceled, but this can result in some latency since theconsumer must wait for the producer to finish its entire transaction instead of pulling as the messages become available.Corresponds to Kafka isolation.level property. |
| Max Metadata Wait Time \* | max.block.ms | 5 sec |  | The amount of time publisher will wait to obtain metadata or wait for the buffer to flush during the ‘send’ call before failing theentire ‘send’ call. Corresponds to Kafka max.block.ms property |
| Max Poll Records \* | max.poll.records | 10000 |  | Maximum number of records Kafka should return in a single poll. |
| SASL Mechanism \* | sasl.mechanism | AWS\_MSK\_IAM | - AWS\_MSK\_IAM - SCRAM-SHA-512 | SASL mechanism used for authentication. Corresponds to Kafka Client sasl.mechanism property |
| SASL Password \* | sasl.password |  |  | Password provided with configured username when using PLAIN or SCRAM SASL Mechanisms |
| SASL Username \* | sasl.username |  |  | Username provided with configured password when using PLAIN or SCRAM SASL Mechanisms |
| Security Protocol \* | security.protocol | SSL | - PLAINTEXT - SSL - SASL\_PLAINTEXT - SASL\_SSL | Security protocol used to communicate with brokers. Corresponds to Kafka Client security.protocol property |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
