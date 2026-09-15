# GetConfluencePageIds 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Downloads changed Confluence pages since the last sync and emits each as a FlowFile with metadata.

## Tags

Preview, atlassian, changes, confluence, fetch, pages

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Confluence Client Service | Controller service for managing connections to Confluence |
| Page IDs | Comma separated list of page IDs to filter page by; only pages with these IDs are returned |
| Space IDs | Comma separated list of space IDs to filter pages by; only pages from these spaces are returned |
| Start Date | Start date from which the ingestion should happen (format: yyyy-MM-dd, inclusive) |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores pagination state to maintain position between restarts. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to fetch changed Confluence pages |
| original | The input Flow File is routed to the original relationship. |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched changed Confluence pages |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| confluence.page.id | Unique identifier of the Confluence page. |
| confluence.page.change.type | Informs about status change for the searched page. |
| confluence.page.url | Confluence page url. |
| confluence.page.title | Confluence page title. |
| confluence.page.last.modification.date | Last modification date of the Confluence page. |
| confluence.space.id | Unique identifier of the Confluence space. |
| confluence.continue.fetching | Indicates whether there are more pages to fetch (true/false). |

Expand

Show lessSee more
