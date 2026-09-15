# DistributeLoad 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Distributes FlowFiles to downstream processors based on a Distribution Strategy. If using the Round Robin strategy, the default is to assign each destination a weighting of 1 (evenly distributed). However, optional properties can be added to the change this; adding a property with the name ’5’ and value ’10’ means that the relationship with name ’5’ will be receive 10 FlowFiles in each iteration instead of 1.

## Tags

distribute, load balance, round robin, route, weighted

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Distribution Strategy | Determines how the load will be distributed. Relationship weight is in numeric order where ’1’ has the greatest weight. |
| Number of Relationships | Determines the number of Relationships to which the load should be distributed |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| 1 | Where to route flowfiles for this relationship index |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| distribute.load.relationship | The name of the specific relationship the FlowFile has been routed through |

Expand

Show lessSee more
