# MonitorActivity 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Monitors the flow for activity and sends out an indicator when the flow has not had any data for some specified amount of time and again when the flow’s activity is restored

## Tags

active, activity, detection, flow, inactive, monitor

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Activity Restored Message | The message that will be the content of FlowFiles that are sent to ‘activity.restored’ relationship |
| Continually Send Messages | If true, will send inactivity indicator continually every Threshold Duration amount of time until activity is restored; if false, will send an indicator only when the flow first becomes inactive |
| Copy Attributes | If true, will copy all flow file attributes from the flow file that resumed activity to the newly created indicator flow file |
| Inactivity Message | The message that will be the content of FlowFiles that are sent to the ‘inactive’ relationship |
| Monitoring Scope | Specify how to determine activeness of the flow. ‘node’ means that activeness is examined at individual node separately. It can be useful if DFM expects each node should receive flow files in a distributed manner. With ‘cluster’, it defines the flow is active while at least one node receives flow files actively. If NiFi is running as standalone mode, this should be set as ‘node’, if it ‘s’ cluster ‘, NiFi logs a warning message and act as’ node’scope. |
| Reporting Node | Specify which node should send notification flow-files to inactive and activity.restored relationships. With ‘all’, every node in this cluster send notification flow-files. ‘primary’ means flow-files will be sent only from a primary node. If NiFi is running as standalone mode, this should be set as ‘all’, even if it ‘s’ primary ‘, NiFi act as’ all’. |
| Reset State on Restart | When the processor gets started or restarted, if set to true, the initial state will always be active. Otherwise, the last reported flow state will be preserved. |
| Threshold Duration | Determines how much time must elapse before considering the flow to be inactive |
| Wait for Activity | When the processor gets started or restarted, if set to true, only send an inactive indicator if there had been activity beforehand. Otherwise send an inactive indicator even if there had not been activity beforehand. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | MonitorActivity stores the last timestamp at each node as state, so that it can examine activity at cluster wide. If ‘Copy Attribute’ is set to true, then flow file attributes are also persisted. In local scope, it stores last known activity timestamp if the flow is inactive. |
| CLUSTER | MonitorActivity stores the last timestamp at each node as state, so that it can examine activity at cluster wide. If ‘Copy Attribute’ is set to true, then flow file attributes are also persisted. In local scope, it stores last known activity timestamp if the flow is inactive. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| activity.restored | This relationship is used to transfer an Activity Restored indicator when FlowFiles are routing to ‘success’ following a period of inactivity |
| inactive | This relationship is used to transfer an Inactivity indicator when no FlowFiles are routed to ‘success’ for Threshold Duration amount of time |
| success | All incoming FlowFiles are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| inactivityStartMillis | The time at which Inactivity began, in the form of milliseconds since Epoch |
| inactivityDurationMillis | The number of milliseconds that the inactivity has spanned |

Expand

Show lessSee more
