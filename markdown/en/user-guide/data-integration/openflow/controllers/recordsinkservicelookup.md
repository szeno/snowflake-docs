# RecordSinkServiceLookup

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a RecordSinkService that can be used to dynamically select another RecordSinkService. This service requires an attribute named ‘record.sink.name’ to be passed in when asking for a connection, and will throw an exception if the attribute is missing. The value of ‘record.sink.name’ will be used to select the RecordSinkService that has been registered with that name. This will allow multiple RecordSinkServices to be defined and registered, and then selected dynamically at runtime by tagging flow files with the appropriate ‘record.sink.name’ attribute. Note that this controller service is not intended for use in reporting tasks that employ RecordSinkService instances, such as QueryNiFiReportingTask.

## Tags

lookup, record, sink

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
