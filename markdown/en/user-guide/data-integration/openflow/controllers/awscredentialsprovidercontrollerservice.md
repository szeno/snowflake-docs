# AWSCredentialsProviderControllerService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Defines credentials for Amazon Web Services processors. Uses default credentials without configuration. Default credentials support EC2 instance profile/role, default user profile, environment variables, etc. Additional options include access key / secret key pairs, credentials file, named profile, and assume role credentials.

## Tags

aws, credentials, provider

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Access Key ID | Access Key ID |  |  |  |
| Assume Role ARN | Assume Role ARN |  |  | The AWS Role ARN for cross account access. This is used in conjunction with Assume Role Session Name and other Assume Role properties. |
| Assume Role External ID | Assume Role External ID |  |  | External ID for cross-account access. This is used in conjunction with Assume Role ARN. |
| Assume Role Proxy Configuration Service | Assume Role Proxy Configuration Service |  |  | Proxy configuration for cross-account access, if needed within your environment. This will configure a proxy to request for temporary access keys into another AWS account. |
| Assume Role SSL Context Service | Assume Role SSL Context Service |  |  | SSL Context Service used when connecting to the STS Endpoint. |
| Assume Role STS Endpoint Override | Assume Role STS Endpoint Override |  |  | The default AWS Security Token Service (STS) endpoint (“sts.amazonaws.com”) works for all accounts that are not for China (Beijing) region or GovCloud. You only need to set this property to “sts.cn-north-1.amazonaws.com.cn” when you are requesting session credentials for services in China(Beijing) region or to “sts.us-gov-west-1.amazonaws.com” for GovCloud. |
| Assume Role STS Region | Assume Role STS Region | us-west-2 | - Middle East (UAE) - US ISOF SOUTH - Asia Pacific (Taipei) - US West (N. California) - US West (Oregon) - Africa (Cape Town) - Asia Pacific (Osaka) - Asia Pacific (Seoul) - Asia Pacific (Tokyo) - Middle East (Bahrain) - South America (Sao Paulo) - China (Beijing) - Asia Pacific (Singapore) - Asia Pacific (Sydney) - Asia Pacific (Jakarta) - Asia Pacific (Melbourne) - Asia Pacific (Malaysia) - US East (N. Virginia) - Asia Pacific (New Zealand) - US East (Ohio) - Asia Pacific (Thailand) - China (Ningxia) - Asia Pacific (Hyderabad) - Asia Pacific (Mumbai) - Europe (Milan) - Europe (Spain) - AWS GovCloud (US-East) - Israel (Tel Aviv) - Canada (Central) - Mexico (Central) - Europe (Frankfurt) - EU (Germany) - US ISO WEST - Europe (Zurich) - EU ISOE West - Europe (Stockholm) - Europe (Paris) - Europe (London) - Europe (Ireland) - Asia Pacific (Hong Kong) - Canada West (Calgary) - AWS GovCloud (US-West) - US ISO East - US ISOB East (Ohio) - US ISOF EAST | The AWS Security Token Service (STS) region |
| Assume Role STS Signer Override | Assume Role STS Signer Override | Default Signature | - Default Signature - Signature Version 4 - Custom Signature | The AWS STS library uses Signature Version 4 by default. This property allows you to plug in your own custom signer implementation. |
| Assume Role Session Name \* | Assume Role Session Name |  |  | The AWS Role Session Name for cross account access. This is used in conjunction with Assume Role ARN. |
| Assume Role Session Time | Assume Role Session Time | 3600 |  | Session time for role based session (between 900 and 3600 seconds). This is used in conjunction with Assume Role ARN. |
| Credentials File | Credentials File |  |  | Path to a file containing AWS access key and secret key in properties file format. |
| Custom Signer Class Name \* | Custom Signer Class Name |  |  | Fully qualified class name of the custom signer class. The signer must implement com.amazonaws.auth.Signer interface. |
| Custom Signer Module Location | Custom Signer Module Location |  |  | Comma-separated list of paths to files and/or directories which contain the custom signer’s JAR file and its dependencies (if any). |
| Profile Name | Profile Name |  |  | The AWS profile name for credentials from the profile configuration file. |
| Secret Access Key | Secret Access Key |  |  |  |
| Use Anonymous Credentials | Use Anonymous Credentials | false | - true - false | If true, uses Anonymous credentials |
| Use Default Credentials | Use Default Credentials | false | - true - false | If true, uses the Default Credential chain, including EC2 instance profiles or roles, environment variables, default user credentials, etc. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| access environment credentials | The default configuration can read environment variables and system properties for credentials |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
