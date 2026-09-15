# ConsumeBoxEnterpriseEvents 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Consumes Enterprise Events from Box admin\_logs\_streaming Stream Type. The content of the events is sent to the ‘success’ relationship as a JSON array. The last known position of the Box stream is stored in the processor state and is used to resume the stream from the last known position when the processor is restarted.

## Tags

box, storage

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| Event Types | A comma separated list of Enterprise Events to consume. If not set, all Events are consumed. See Additional Details for more information. |
| Start Event Position | What position to consume the Events from. |
| Start Offset | The offset to start consuming the Events from. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | The last known position of the Box Event stream is stored in the processor state and is used to resume the stream from the last known position when the processor is restarted. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Events received successfully will be sent out this relationship. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.ConsumeBoxEvents](/user-guide/data-integration/openflow/processors/consumeboxevents)
- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
