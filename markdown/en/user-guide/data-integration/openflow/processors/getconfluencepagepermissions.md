# GetConfluencePagePermissions 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Processor downloading Confluence page permissions.

## Tags

Preview, atlassian, confluence, page, permissions

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Confluence Client Service | Controller service for managing connections to Confluence |
| Confluence Page ID | Identifier of the Confluence Page |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to fetch and parse Confluence page permissions. |
| page not found | Confluence page not found |
| restrictions changed | Confluence page restrictions changed since last fetch |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched Confluence page permissions. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| confluence.permissions.users | IDs of users with permissions to the Confluence page |
| confluence.permissions.emails | Emails of users with permissions to the Confluence page |
| confluence.permissions.groups | Groups with permissions to the Confluence page |

Expand

Show lessSee more
