# ApicurioSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a Schema Registry that interacts with the Apicurio Schema Registry so that those Schemas that are stored in the Apicurio Schema Registry can be used in NiFi. When a Schema is looked up by name by this registry, it will find a Schema in the Apicurio Schema Registry with their artifact identifiers.

## Tags

apicurio, avro, registry, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Cache Expiration \* | Cache Expiration | 1 hour |  | Specifies how long a Schema that is cached should remain in the cache. Once this time period elapses, a cached version of a schema will no longer be used, and the service will have to communicate with the Schema Registry again in order to obtain the schema. |
| Cache Size \* | Cache Size | 1000 |  | Specifies how many Schemas should be cached from the Schema Registry. The cache size must be a non-negative integer. When it is set to 0, the cache is effectively disabled. |
| Schema Group ID \* | Schema Group ID | default |  | The artifact Group ID for the schemas |
| Schema Registry URL \* | Schema Registry URL |  |  | The URL of the Schema Registry e.g. <http://localhost:8080> |
| Web Client Service Provider \* | Web Client Service Provider |  |  | Controller service for HTTP client operations |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
