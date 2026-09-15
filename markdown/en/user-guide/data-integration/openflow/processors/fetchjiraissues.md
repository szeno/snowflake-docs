# FetchJiraIssues 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Fetches issues from Jira Cloud using REST API v3 with configurable search options. Provides two search modes: 1. Simple Search - Filter by project name, status category, created/updated dates 2. Advanced Search - Use custom JQL (Jira Query Language) expressions Key features: - Smart pagination handling with automatic state management - Incremental sync capability using timestamps between processor runs - Timezone-aware date handling using Jira user’s timezone - Configurable issue fields retrieval - Adds metadata to FlowFiles: source URL (jira.source.url), query (jira.query.jql), statement type (statement.type) - Adds insert,upsert attributes for downstream processing The processor maintains cluster state to resume operations after restarts Authentication is handled via basic auth using Jira email/API token credentials. Currently that is the only supported method. LIMITATIONS: - Jira issue deletes are not detected.

## Tags

api, atlassian, fetch, jira, rest

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| API Token | Jira API token for authorization |
| Authorization Method | Authorization method for Jira Cloud API |
| Created After | Filter issues created after specified date/time (optional, format: yyyy-MM-dd) |
| Environment URL | URL to the Atlassian Jira Environment |
| Issue Fields | A list of fields to return for each issue. This property accepts a comma-separated list. |
| JQL Query | JQL query string (required when using JQL query type) |
| Jira Email | Email address associated with Jira account |
| Maximum Page Size | The Maximum Page Size value must be between 50 and 1000 |
| Project Names | Comma-separated list of project names for simple search |
| Request Rate Manager | Controller service for keeping track of rate limits for Atlassian APIs |
| Search Type | Type of search to perform |
| Status Category | Status category filter for simple search (optional) |
| Updated After | Filter issues updated after specified date/time (optional, format: yyyy-MM-dd) |
| Web Client Service | Controller service for managing HTTP connections to Jira |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores pagination state to maintain position between restarts. Resets when ingestion configuration changes. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched Jira issues |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | application/json |
| jira.query.jql | The JQL query used for this fetch |
| jira.source.url | URL of the Jira source |
| statement.type | Statement type INSERT, UPSERT |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.atlassian.jira.processors.FetchJiraFields](/user-guide/data-integration/openflow/processors/fetchjirafields)
