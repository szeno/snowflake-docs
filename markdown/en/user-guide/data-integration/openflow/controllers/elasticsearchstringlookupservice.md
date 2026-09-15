# ElasticSearchStringLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Lookup a string value from Elasticsearch Server associated with the specified document ID. The coordinates that are passed to the lookup must contain the key ‘id’.

## Tags

elasticsearch, enrich, key, lookup, value

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Client Service \* | Client Service |  |  | An ElasticSearch client service to use for running queries. |
| Index \* | Index |  |  | The name of the index to read from |
| Type | Type |  |  | The type of this document (used by Elasticsearch for indexing and searching) |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
