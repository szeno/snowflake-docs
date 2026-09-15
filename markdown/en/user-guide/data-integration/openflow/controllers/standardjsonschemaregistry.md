# StandardJsonSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a service for registering and accessing JSON schemas. One can register a schema as a dynamic property where ‘name’ represents the schema name and ‘value’ represents the textual representation of the actual schema following the syntax and semantics of the JSON Schema format. Empty schemas and schemas only consisting of whitespace are not acceptable schemas. The registry is heterogeneous registry as it can store schemas of different schema draft versions. By default the registry is configured to store schemas of Draft 2020-12. When a schema is added, the version which is currently is set, is what the schema is saved as.

## Tags

json, registry, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| JSON Schema Version \* | JSON Schema Version | DRAFT\_2020\_12 | - Draft 4 - Draft 6 - Draft 7 - Draft 2019-09 - Draft 2020-12 | The JSON schema specification |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
