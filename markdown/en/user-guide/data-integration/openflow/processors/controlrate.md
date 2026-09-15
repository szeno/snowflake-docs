# ControlRate 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Controls the rate at which data is transferred to follow-on processors. If you configure a very small Time Duration, then the accuracy of the throttle gets worse. You can improve this accuracy by decreasing the Yield Duration, at the expense of more Tasks given to the processor.

## Tags

rate, rate control, throttle, throughput

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Grouping Attribute | By default, a single “throttle” is used for all FlowFiles. If this value is specified, a separate throttle is used for each value specified by the attribute with this name. Changing this value resets the rate counters. |
| Maximum Data Rate | The maximum rate at which data should pass through this processor. The format of this property is expected to be a Data Size (such as ’1 MB’) representing bytes per Time Duration. |
| Maximum FlowFile Rate | The maximum rate at which FlowFiles should pass through this processor. The format of this property is expected to be a positive integer representing FlowFiles count per Time Duration |
| Maximum Rate | The maximum rate at which data should pass through this processor. The format of this property is expected to be a positive integer, or a Data Size (such as ’1 MB’) if Rate Control Criteria is set to ‘data rate’. |
| Rate Control Criteria | Indicates the criteria that is used to control the throughput rate. Changing this value resets the rate counters. |
| Rate Controlled Attribute | The name of an attribute whose values build toward the rate limit if Rate Control Criteria is set to ‘attribute value’. The value of the attribute referenced by this property must be a positive long, or the FlowFile will be routed to failure. This value is ignored if Rate Control Criteria is not set to ‘attribute value’. Changing this value resets the rate counters. |
| Rate Exceeded Strategy | Specifies how to handle an incoming FlowFile when the maximum data rate has been exceeded. |
| Time Duration | The amount of time to which the Maximum Rate pertains. Changing this value resets the rate counters. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles will be routed to this relationship if they are missing a necessary Rate Controlled Attribute or the attribute is not in the expected format |
| success | FlowFiles are transferred to this relationship under normal conditions |

Expand

Show lessSee more

## Use cases

| Limit the rate at which data is sent to a downstream system with little to no bursts |
| --- |
| Limit the rate at which FlowFiles are sent to a downstream system with little to no bursts |
| Reject requests that exceed a specific rate with little to no bursts |
| Reject requests that exceed a specific rate, allowing for bursts |

Expand

Show lessSee more
