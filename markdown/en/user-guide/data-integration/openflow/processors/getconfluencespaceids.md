# GetConfluenceSpaceIds 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Processor for retrieving Confluence space ids.

## Tags

atlassian, confluence, preview, spaces

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Confluence Client Service | Controller service for managing connections to Confluence |
| Space Keys | Comma-separated list of space keys to filter. If not specified, all spaces will be retrieved. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched Confluence spaces |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| confluence.space.ids | List of identifiers of the Confluence spaces. |

Expand

Show lessSee more
