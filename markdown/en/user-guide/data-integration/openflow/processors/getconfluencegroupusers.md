# GetConfluenceGroupUsers 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Processor that downloads information about users belonging to a given Confluence group

## Tags

Preview, atlassian, confluence, groups, users

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Confluence Client Service | Controller service for managing connections to Confluence |
| Confluence Group ID | Identifier of the Confluence Group |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to fetch Confluence group users |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched Confluence group users |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| confluence.group.user.ids | Identifiers of the Confluence group users. |
| confluence.group.user.emails | Emails of the Confluence group users. |

Expand

Show lessSee more
