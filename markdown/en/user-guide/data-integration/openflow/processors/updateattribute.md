# UpdateAttribute 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-update-attribute-nar

## Description

Updates the Attributes for a FlowFile by using the Attribute Expression Language and/or deletes the attributes based on a regular expression

## Tags

Attribute Expression Language, attributes, delete, modification, state, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Delete Attributes Expression | Regular expression for attributes to be deleted from FlowFiles. Existing attributes that match will be deleted regardless of whether they are updated by this processor. |
| Stateful Variables Initial Value | If using state to set/reference variables then this value is used to set the initial value of the stateful variable. This will only be used in the @OnScheduled method when state does not contain a value for the variable. This is required if running statefully but can be empty if needed. |
| Store State | Select whether or not state will be stored. Selecting ‘Stateless’ will offer the default functionality of purely updating the attributes on a FlowFile in a stateless manner. Selecting a stateful option will not only store the attributes on the FlowFile but also in the Processors state. See the ‘Stateful Usage’ topic of the ‘Additional Details’section of this processor’s documentation for more information |
| canonical-value-lookup-cache-size | Specifies how many canonical lookup values should be stored in the cache |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | Gives the option to store values not only on the FlowFile but as stateful variables to be referenced in a recursive manner. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All successful FlowFiles are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| See additional details | This processor may write or remove zero or more attributes as described in additional details |

Expand

Show lessSee more

## Use cases

| Add a new FlowFile attribute |
| --- |
| Overwrite a FlowFile attribute with a new value |
| Rename a file |

Expand

Show lessSee more
