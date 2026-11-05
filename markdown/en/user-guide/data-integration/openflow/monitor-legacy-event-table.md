# Runtime metrics: Event table (deprecated)

Deprecated Feature

The runtime metrics on this page are deprecated and will be removed in a future release. A removal date isn’t
planned yet, and removal won’t happen in the near future. Don’t use these metrics for new monitoring. Use the
metrics described in [Openflow telemetry](/user-guide/data-integration/openflow/monitor) instead. For more information, see
[Oct 28, 2026: Openflow legacy runtime metrics deprecated](/release-notes/2026/other/2026-10-28-openflow-legacy-runtime-metrics-deprecation).

Every minute, Openflow runtimes write metrics describing process groups, processors, and connections to your event table.
They can be queried to gain insight into the current state of the connectors and runtimes.

## Process group metrics

Openflow connectors are represented as process groups, marked with `tree.level` record attribute set to `1`.

| Metric | Reported for | Description |
| --- | --- | --- |
| processgroup.bytes.received | Process groups on the root canvas of the runtime | Total bytes received from external sources in the last five minutes. |
| processgroup.bytes.sent | Process groups on the root canvas of the runtime | Total bytes sent to external destinations in the last five minutes. |
| processgroup.time.processing | All process groups | Total time, in nanoseconds, that components of the process group spent processing data in the last five minutes. |

Expand

Show lessSee more

Process group metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the process group. |
| name | Name of the process group. |
| type | The fixed value *process-group*. |
| tree.level | Depth of the process group, as a string. *1* for process groups on the root canvas of the runtime. |
| processGroupIdPath | Slash-delimited path of process group identifiers, starting at the root process group. |
| processGroupNamePath | Slash-delimited path of process group names, starting at the root process group. |
| flow.identifier | Identifier of the versioned flow. Versioned process groups only. |
| flow.version | Version of the versioned flow. Versioned process groups only. |
| registry.name | Name of the registry of the versioned flow. Versioned process groups only. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

## Processor metrics

| Metric | Reported for | Description |
| --- | --- | --- |
| processor.run.status.running | All processors | *1* if the processor is running. Otherwise, *0*. |
| processor.bytes.received | [Source processors](#label-openflow-legacy-source-processors) | Total bytes received from external sources in the last five minutes. |
| processor.bytes.sent | [Destination processors](#label-openflow-legacy-destination-processors) | Total bytes sent to external destinations in the last five minutes. |
| processor.output.count | [Processors with output counts](#label-openflow-legacy-output-count-processors) | Total number of FlowFiles the processor output in the last five minutes. |
| processor.time.lineage.average | [Processors with lineage times](#label-openflow-legacy-lineage-processors) | Average time, in nanoseconds, since the FlowFiles that the processor handled in the last five minutes entered the flow. |
| processor.counter | [Processors with counters](#label-openflow-legacy-counter-processors) | Current value of a processor counter. Each counter is a separate row, identified by the *counter* attribute. |

Expand

Show lessSee more

Processor metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the processor. |
| name | Name of the processor. |
| component | Type of the processor, for example *PutSnowpipeStreaming*. |
| type | The fixed value *processor*. For `processor.counter`, the fixed value *counter*. |
| counter | Name of the counter. `processor.counter` only. |
| execution.node | Either *ALL* or *PRIMARY*, depending on how the processor is configured to run. |
| group.id | Unique identifier of the process group that contains the processor. |
| processGroupIdPath | Slash-delimited path of process group identifiers, starting at the root process group. |
| processGroupNamePath | Slash-delimited path of process group names, starting at the root process group. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### Source processors

Openflow writes `processor.bytes.received` for the following processors:

- CaptureChangeMySQL
- CaptureChangeOracle
- CaptureChangePostgreSQL
- CaptureChangeSqlServer
- CaptureGoogleDriveChanges
- CaptureMicrosoft365GroupsChanges
- CaptureSharepointChanges
- ConsumeKafka
- ConsumeKinesis
- ConsumeKinesisStream
- ConsumeSlackConversation
- ConsumeSlackHistory
- ConsumeSnowflakeStream
- FetchBoxFile
- FetchGoogleDrive
- FetchGoogleDriveFileComments
- FetchJiraBoardConfiguration
- FetchJiraBoardProjects
- FetchJiraBoards
- FetchJiraBoardSprints
- FetchJiraChangelogs
- FetchJiraComments
- FetchJiraDeletedIssues
- FetchJiraFields
- FetchJiraFilter
- FetchJiraIssues
- FetchJiraIssueSecuritySchemes
- FetchJiraIssueTypes
- FetchJiraIssueVotes
- FetchJiraIssueWatchers
- FetchJiraPermissions
- FetchJiraPriorities
- FetchJiraProjectComponents
- FetchJiraProjects
- FetchJiraProjectVersions
- FetchJiraRemoteIssueLinks
- FetchJiraResolutions
- FetchJiraStatuses
- FetchJiraUserGroups
- FetchJiraUsers
- FetchJiraWorklogs
- FetchMicrosoftDataverseTable
- FetchS3Object
- FetchSharepointFile
- FetchSharepointMetadata
- FetchSlackConversationInfo
- FetchSlackFile
- FetchSlackMessage
- FetchTableSnapshot
- GetAmazonAdsReport
- GetGoogleAdsReport
- GetGoogleSheets
- GetHubSpotObject
- GetLinkedInAdsReport
- GetQueryJobResult
- GetShopifyBulk
- GetShopifyDeletes
- GetShopifyIncremental
- GetWorkdayReport
- InvokeHTTP
- ListenSlack
- MultiDatabaseCaptureChangeSqlServer
- MultiDatabaseFetchRowsByRowId
- MultiDatabaseFetchTableSnapshot
- SearchJiraJQL

### Destination processors

Openflow writes `processor.bytes.sent` for the following processors:

- PublishChangeDataSnowpipeStreaming
- PublishKafka
- PublishSnowpipeStreaming
- PutDatabaseRecord
- PutKinesisStream
- PutSnowflakeInternalStageFile
- PutSnowpipeStreaming
- PutSnowpipeStreaming2

### Processors with output counts

Openflow writes `processor.output.count` for the following processors:

- CaptureGoogleDriveChanges
- CaptureSharepointChanges

### Processors with lineage times

Openflow writes `processor.time.lineage.average` for the following processors:

- MergeSnowflakeJournalTable
- PublishChangeDataSnowpipeStreaming
- PublishKafka
- PublishSnowpipeStreaming
- PutSnowpipeStreaming
- PutSnowpipeStreaming2

### Processors with counters

Openflow writes `processor.counter` for all counters of the following processors:

- CaptureChangeMySQL
- CaptureChangeOracle
- CaptureChangePostgreSQL
- CaptureChangeSqlServer
- CaptureSharepointChanges
- ConsumeBoxEnterpriseEvents
- ConsumeKafka
- ConsumeKinesis
- ConsumeKinesisStream
- ConsumeSnowflakeStream
- FetchMicrosoftDataverseTable
- FetchTableSnapshot
- GetHubSpotObject
- MultiDatabaseCaptureChangeSqlServer
- MultiDatabaseFetchTableSnapshot
- PublishChangeDataSnowpipeStreaming
- PublishKafka
- PublishSnowpipeStreaming
- PutSnowflakeInternalStageFile
- PutSnowpipeStreaming
- PutSnowpipeStreaming2
- UpdateCounter

## Connection metrics

Openflow writes the following metrics for all connections:

| Metric | Description |
| --- | --- |
| connection.queued.count | Number of FlowFiles queued in the connection. |
| connection.queued.bytes | Size, in bytes, of the FlowFiles queued in the connection. |
| connection.queued.duration.max | Longest time, in milliseconds, that a queued FlowFile has been in the connection. |
| connection.backpressure.threshold.bytes | Size, in bytes, of queued FlowFiles at which the connection applies back pressure. |
| connection.backpressure.threshold.object | Number of queued FlowFiles at which the connection applies back pressure. |

Expand

Show lessSee more

Connection metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the connection. |
| name | Name of the connection. |
| type | The fixed value *connection*. |
| source.id | Unique identifier of the component that sends FlowFiles to the connection. |
| source.name | Name of the component that sends FlowFiles to the connection. |
| destination.id | Unique identifier of the component that receives FlowFiles from the connection. |
| destination.name | Name of the component that receives FlowFiles from the connection. |
| group.id | Unique identifier of the process group that contains the connection. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more
