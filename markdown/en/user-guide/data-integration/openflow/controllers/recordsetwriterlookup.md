# RecordSetWriterLookup

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a RecordSetWriterFactory that can be used to dynamically select another RecordSetWriterFactory. This will allow multiple RecordSetWriterFactory’s to be defined and registered, and then selected dynamically at runtime by tagging FlowFiles with the attributes and referencing those attributes in the Service to Use property.

## Tags

lookup, record, recordset, result, row, serializer, set, writer

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Service to Use \* | Service to Use | ${recordsetwriter.name} |  | Specifies the name of the user-defined property whose associated Controller Service should be used. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
