# ForkEnrichment 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Used in conjunction with the JoinEnrichment processor, this processor is responsible for adding the attributes that are necessary for the JoinEnrichment processor to perform its function. Each incoming FlowFile will be cloned. The original FlowFile will have appropriate attributes added and then be transferred to the ‘original’ relationship. The clone will have appropriate attributes added and then be routed to the ‘enrichment’ relationship. See the documentation for the JoinEnrichment processor (and especially its Additional Details) for more information on how these Processors work together and how to perform enrichment tasks in NiFi by using these Processors.

## Tags

enrich, fork, join, record

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Relationships

| Name | Description |
| --- | --- |
| enrichment | A clone of the incoming FlowFile will be routed to this relationship, after adding appropriate attributes. |
| original | The incoming FlowFile will be routed to this relationship, after adding appropriate attributes. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| enrichment.group.id | The Group ID to use in order to correlate the ‘original’ FlowFile with the ‘enrichment’ FlowFile. |
| enrichment.role | The role to use for enrichment. This will either be ORIGINAL or ENRICHMENT. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.JoinEnrichment](/user-guide/data-integration/openflow/processors/joinenrichment)
