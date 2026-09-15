# S3FileResourceService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides an Amazon Web Services (AWS) S3 file resource for other components.

## Tags

AWS, Amazon, S3, file, resource

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| AWS Credentials Provider service \* | AWS Credentials Provider service |  |  | The Controller Service that is used to obtain AWS credentials provider |
| Bucket \* | Bucket | ${s3.bucket} |  | The S3 Bucket to interact with |
| Object Key \* | Object Key | ${filename} |  | The S3 Object Key to use. This is analogous to a filename for traditional file systems. |
| Region \* | Region | us-west-2 | - AWS GovCloud (US) - AWS GovCloud (US-East) - US East (N. Virginia) - US East (Ohio) - US West (N. California) - US West (Oregon) - EU (Ireland) - EU (London) - EU (Paris) - EU (Frankfurt) - EU (Zurich) - EU (Stockholm) - EU (Milan) - EU (Spain) - Asia Pacific (Hong Kong) - Asia Pacific (Taipei) - Asia Pacific (Mumbai) - Asia Pacific (Hyderabad) - Asia Pacific (Singapore) - Asia Pacific (Sydney) - Asia Pacific (Jakarta) - Asia Pacific (Melbourne) - Asia Pacific (Malaysia) - Asia Pacific (Thailand) - Asia Pacific (Tokyo) - Asia Pacific (Seoul) - Asia Pacific (Osaka) - South America (Sao Paulo) - China (Beijing) - China (Ningxia) - Canada (Central) - Canada West (Calgary) - Middle East (UAE) - Middle East (Bahrain) - Africa (Cape Town) - US ISO East - US ISOB East (Ohio) - US ISO West - US ISOF East1 (California) - US ISOF South1 (Alpine) - Israel (Tel Aviv) - Mexico (Central) - EU ISOE West - Use ‘s3.region’ Attribute | The AWS Region to connect to. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
