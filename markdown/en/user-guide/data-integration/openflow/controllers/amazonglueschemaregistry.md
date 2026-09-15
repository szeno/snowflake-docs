# AmazonGlueSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a Schema Registry that interacts with the AWS Glue Schema Registry so that those Schemas that are stored in the Glue Schema Registry can be used in NiFi. When a Schema is looked up by name by this registry, it will find a Schema in the Glue Schema Registry with their names.

## Tags

avro, aws, glue, registry, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| AWS Credentials Provider Service | AWS Credentials Provider Service |  |  | The Controller Service that is used to obtain AWS credentials provider |
| Cache Expiration \* | Cache Expiration | 1 hour |  | Specifies how long a Schema that is cached should remain in the cache. Once this time period elapses, a cached version of a schema will no longer be used, and the service will have to communicate with the Schema Registry again in order to obtain the schema. |
| Cache Size \* | Cache Size | 1000 |  | Specifies how many Schemas should be cached from the Schema Registry |
| Communications Timeout \* | Communications Timeout | 30 secs |  | Specifies how long to wait to receive data from the Schema Registry before considering the communications a failure |
| Region \* | Region | us-west-2 | - AWS GovCloud (US-East) - AWS GovCloud (US-West) - Africa (Cape Town) - Asia Pacific (Hong Kong) - Asia Pacific (Hyderabad) - Asia Pacific (Jakarta) - Asia Pacific (Malaysia) - Asia Pacific (Melbourne) - Asia Pacific (Mumbai) - Asia Pacific (New Zealand) - Asia Pacific (Osaka) - Asia Pacific (Seoul) - Asia Pacific (Singapore) - Asia Pacific (Sydney) - Asia Pacific (Taipei) - Asia Pacific (Thailand) - Asia Pacific (Tokyo) - Canada (Central) - Canada West (Calgary) - China (Beijing) - China (Ningxia) - EU (Germany) - EU ISOE West - Europe (Frankfurt) - Europe (Ireland) - Europe (London) - Europe (Milan) - Europe (Paris) - Europe (Spain) - Europe (Stockholm) - Europe (Zurich) - Israel (Tel Aviv) - Mexico (Central) - Middle East (Bahrain) - Middle East (UAE) - South America (Sao Paulo) - US East (N. Virginia) - US East (Ohio) - US ISO East - US ISO WEST - US ISOB East (Ohio) - US ISOF EAST - US ISOF SOUTH - US West (N. California) - US West (Oregon) - aws global region - aws-cn global region - aws-iso global region - aws-iso-b global region - aws-iso-e global region - aws-iso-f global region - aws-us-gov global region | The region of the cloud resources |
| SSL Context Service | SSL Context Service |  |  | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Schema Registry Name \* | Schema Registry Name |  |  | The name of the Schema Registry |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
