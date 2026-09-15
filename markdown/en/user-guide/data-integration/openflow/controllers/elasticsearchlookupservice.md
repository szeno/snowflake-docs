# ElasticSearchLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Lookup a record from Elasticsearch Server associated with the specified document ID. The coordinates that are passed to the lookup must contain the key ‘id’.

## Tags

elasticsearch, enrich, lookup, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Client Service \* | Client Service |  |  | An ElasticSearch client service to use for running queries. |
| Index \* | Index |  |  | The name of the index to read from |
| Schema Access Strategy \* | Schema Access Strategy | infer | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Infer from Result | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Type | Type |  |  | The type of this document (used by Elasticsearch for indexing and searching) |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
