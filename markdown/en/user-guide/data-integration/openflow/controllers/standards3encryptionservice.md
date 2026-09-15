# StandardS3EncryptionService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Adds configurable encryption to S3 Put and S3 Fetch operations.

## Tags

aws, decrypt, decryption, encrypt, encryption, key, s3, service

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Encryption Strategy \* | Encryption Strategy | NONE | - None - Server-side S3 - Server-side KMS - Server-side Customer Key - Client-side KMS - Client-side Customer Key | Strategy to use for S3 data encryption and decryption. |
| KMS Region | KMS Region | us-west-2 | - AWS GovCloud (US) - AWS GovCloud (US-East) - US East (N. Virginia) - US East (Ohio) - US West (N. California) - US West (Oregon) - EU (Ireland) - EU (London) - EU (Paris) - EU (Frankfurt) - EU (Zurich) - EU (Stockholm) - EU (Milan) - EU (Spain) - Asia Pacific (Hong Kong) - Asia Pacific (Taipei) - Asia Pacific (Mumbai) - Asia Pacific (Hyderabad) - Asia Pacific (Singapore) - Asia Pacific (Sydney) - Asia Pacific (Jakarta) - Asia Pacific (Melbourne) - Asia Pacific (Malaysia) - Asia Pacific (Thailand) - Asia Pacific (Tokyo) - Asia Pacific (Seoul) - Asia Pacific (Osaka) - South America (Sao Paulo) - China (Beijing) - China (Ningxia) - Canada (Central) - Canada West (Calgary) - Middle East (UAE) - Middle East (Bahrain) - Africa (Cape Town) - US ISO East - US ISOB East (Ohio) - US ISO West - US ISOF East1 (California) - US ISOF South1 (Alpine) - Israel (Tel Aviv) - Mexico (Central) - EU ISOE West | The Region of the AWS Key Management Service. Only used in case of Client-side KMS. |
| Key ID or Key Material | Key ID or Key Material |  |  | For None and Server-side S3: not used. For Server-side KMS and Client-side KMS: the KMS Key ID must be configured. For Server-side Customer Key and Client-side Customer Key: the Key Material must be specified in Base64 encoded form. In case of Server-side Customer Key, the key must be an AES-256 key. In case of Client-side Customer Key, it can be an AES-256, AES-192 or AES-128 key. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
