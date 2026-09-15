# RetryFlowFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

FlowFiles passed to this Processor have a ‘Retry Attribute’ value checked against a configured ‘Maximum Retries’ value. If the current attribute value is below the configured maximum, the FlowFile is passed to a retry relationship. The FlowFile may or may not be penalized in that condition. If the FlowFile ‘s attribute value exceeds the configured maximum, the FlowFile will be passed to a’ retries\_exceeded ‘relationship. WARNING: If the incoming FlowFile has a non-numeric value in the configured’Retry Attribute ‘attribute, it will be reset to’1 ‘. You may choose to fail the FlowFile instead of performing the reset. Additional dynamic properties can be defined for any attributes you wish to add to the FlowFiles transferred to’ retries\_exceeded’. These attributes support attribute expression language.

## Tags

FlowFile, Retry

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Fail on Non-numerical Overwrite | If the FlowFile already has the attribute defined in ‘Retry Attribute’ that is *not* a number, fail the FlowFile instead of resetting that value to ’1’ |
| maximum-retries | The maximum number of times a FlowFile can be retried before being passed to the ‘retries\_exceeded’ relationship |
| penalize-retries | If set to ‘true’, this Processor will penalize input FlowFiles before passing them to the ‘retry’ relationship. This does not apply to the ‘retries\_exceeded’ relationship. |
| retry-attribute | The name of the attribute that contains the current retry count for the FlowFile. WARNING: If the name matches an attribute already on the FlowFile that does not contain a numerical value, the processor will either overwrite that attribute with ’1’ or fail based on configuration. |
| reuse-mode | Defines how the Processor behaves if the retry FlowFile has a different retry UUID than the instance that received the FlowFile. This generally means that the attribute was not reset after being successfully retried by a previous instance of this processor. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The processor is configured such that a non-numerical value on ‘Retry Attribute’ results in a failure instead of resetting that value to ’1’. This will immediately terminate the limited feedback loop. Might also include when ‘Maximum Retries’ contains attribute expression language that does not resolve to an Integer. |
| retries\_exceeded | Input FlowFile has exceeded the configured maximum retry count, do not pass this relationship back to the input Processor to terminate the limited feedback loop. |
| retry | Input FlowFile has not exceeded the configured maximum retry count, pass this relationship back to the input Processor to create a limited feedback loop. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| Retry Attribute | User defined retry attribute is updated with the current retry count |
| Retry Attribute .uuid | User defined retry attribute with .uuid that determines what processor retried the FlowFile last |

Expand

Show lessSee more
