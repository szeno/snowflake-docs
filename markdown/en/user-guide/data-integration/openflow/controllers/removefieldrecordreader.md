# RemoveFieldRecordReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A wrapper for a RecordReaderFactory that supports filtering out specified fields from NiFi Records. It allows users to specify a list of field names that should be ignored when reading records from the record reader returned from the wrapped RecordReaderFactory. The ignored record fields are specified as dynamic properties. At least one dynamic property must be set. The dynamic property name is used as a description of the field to remove, and the dynamic property value is a RecordPath that identifies the field to be removed. Nested paths are supported. Record paths targeting the root path (“/”) are not allowed and will result in a validation error. This service should be used when all of the following criteria are met: - your delegate RecordReaderFactory is configured to infer the schema from the data - you do not have or do not want to define a static schema for the data you ‘re reading - the fields you set to be ignored should not be serialized to the NiFi content repository for security or performance reasons If any of the above criteria are not met, consider using the RecordFieldRemover processor instead. NOTE: The RecordReader returned by this implementation is hardcoded to drop unknown fields rather than ignoring them. Even when the RecordReader’s nextRecord(coerceTypes, dropUnknownFields) method is called with dropUnknownFields set to false, the RecordReader will still drop unknown fields.

## Tags

delete, field, filter, reader, record, remove

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Record Reader \* | Record Reader |  |  | The underlying RecordReaderFactory service that will be used to read records before filtering is applied. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
