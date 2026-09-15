# FetchDistributedMapCache 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Computes cache key(s) from FlowFile attributes, for each incoming FlowFile, and fetches the value(s) from the Distributed Map Cache associated with each key. If configured without a destination attribute, the incoming FlowFile ‘s content is replaced with the binary data received by the Distributed Map Cache. If there is no value stored under that key then the flow file will be routed to’ not-found ‘. Note that the processor will always attempt to read the entire cached value into memory before placing it in it’s destination. This could be potentially problematic if the cached value is very large.

## Tags

cache, distributed, fetch, map

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Cache Entry Identifier | A comma-delimited list of FlowFile attributes, or the results of Attribute Expression Language statements, which will be evaluated against a FlowFile in order to determine the value(s) used to identify duplicates; it is these values that are cached. NOTE: Only a single Cache Entry Identifier is allowed unless Put Cache Value In Attribute is specified. Multiple cache lookups are only supported when the destination is a set of attributes (see the documentation for ‘Put Cache Value In Attribute’ for more details including naming convention. |
| Character Set | The Character Set in which the cached value is encoded. This will only be used when routing to an attribute. |
| Distributed Cache Service | The Controller Service that is used to get the cached values. |
| Max Length To Put In Attribute | If routing the cache value to an attribute of the FlowFile (by setting the “Put Cache Value in attribute” property), the number of characters put to the attribute value will be at most this amount. This is important because attributes are held in memory and large attributes will quickly cause out of memory issues. If the output goes longer than this value, it will be truncated to fit. Consider making this smaller if able. |
| Put Cache Value In Attribute | If set, the cache value received will be put into an attribute of the FlowFile instead of a the content of theFlowFile. The attribute key to put to is determined by evaluating value of this property. If multiple Cache Entry Identifiers are selected, multiple attributes will be written, using the evaluated value of this property, appended by a period (.) and the name of the cache entry identifier. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If unable to communicate with the cache or if the cache entry is evaluated to be blank, the FlowFile will be penalized and routed to this relationship |
| not-found | If a FlowFile’s Cache Entry Identifier was not found in the cache, it will be routed to this relationship |
| success | If the cache was successfully communicated with it will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| user-defined | If the ‘Put Cache Value In Attribute’ property is set then whatever it is set to will become the attribute key and the value would be whatever the response was from the Distributed Map Cache. If multiple cache entry identifiers are selected, multiple attributes will be written, using the evaluated value of this property, appended by a period (.) and the name of the cache entry identifier. For example, if the Cache Entry Identifier property is set to ‘id,name’, and the user-defined property is named ‘fetched’, then two attributes will be written, fetched.id and fetched.name, containing their respective values. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.PutDistributedMapCache](/user-guide/data-integration/openflow/processors/putdistributedmapcache)
