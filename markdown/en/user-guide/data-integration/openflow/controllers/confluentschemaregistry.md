# ConfluentSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a Schema Registry that interacts with the Confluent Schema Registry so that those Schemas that are stored in the Confluent Schema Registry can be used in NiFi. The Confluent Schema Registry has a notion of a “subject” for schemas, which is their terminology for a schema name. When a Schema is looked up by name by this registry, it will find a Schema in the Confluent Schema Registry with that subject.

## Tags

avro, confluent, kafka, registry, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Authentication Type | Authentication Type | NONE | - BASIC - NONE | HTTP Client Authentication Type for Confluent Schema Registry |
| Cache Expiration \* | Cache Expiration | 1 hour |  | Specifies how long a Schema that is cached should remain in the cache. Once this time period elapses, a cached version of a schema will no longer be used, and the service will have to communicate with the Schema Registry again in order to obtain the schema. |
| Cache Size \* | Cache Size | 1000 |  | Specifies how many Schemas should be cached from the Schema Registry |
| Communications Timeout \* | Communications Timeout | 30 secs |  | Specifies how long to wait to receive data from the Schema Registry before considering the communications a failure |
| Password | Password |  |  | Password for authentication to Confluent Schema Registry |
| SSL Context Service | SSL Context Service |  |  | Specifies the SSL Context Service to use for interacting with the Confluent Schema Registry |
| Schema Registry URLs \* | Schema Registry URLs | <http://localhost:8081> |  | A comma-separated list of URLs of the Schema Registry to interact with |
| Username | Username |  |  | Username for authentication to Confluent Schema Registry |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
