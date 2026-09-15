# FindConfluencePages 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Processor for finding Confluence pages using space name and page name.

## Tags

Preview, atlassian, confluence, fetch, pages

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Confluence Client Service | Controller service for managing connections to Confluence |
| Confluence Page Name | Name of the Confluence Page. If not provided, all pages in the space will be retrieved. |
| Confluence Space Name | Name of the Confluence Space |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to find Confluence pages |
| not found | Pages for given space name and page name not found |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully found Confluence pages |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| confluence.page.name | Unique identifier of the Confluence page. |
| confluence.page.change.type | Informs about status change for the searched page. |
| confluence.page.url | Confluence page url. |
| confluence.page.title | Confluence page title. |
| confluence.page.last.modification.date | Last modification date of the Confluence page. |
| confluence.space.name | Name of the Confluence space. |

Expand

Show lessSee more
