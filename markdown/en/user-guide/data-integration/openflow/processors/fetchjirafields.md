# FetchJiraFields 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-atlassian-processors-nar

## Description

Retrieves comprehensive metadata for all fields available in the Jira Cloud instance using the REST API v3 /field endpoint. For each field, returns detailed information including field ID/key, display name, field properties, JQL clause names for queries, and schema details with data types.

## Tags

api, atlassian, fetch, jira, rest

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| API Token | Jira API token for authorization |
| Authorization Method | Authorization method for Jira Cloud API |
| Environment URL | URL to the Atlassian Jira Environment |
| Issue Fields | A list of fields to return for each issue. This property accepts a comma-separated list. |
| Jira Email | Email address associated with Jira account |
| Request Rate Manager | Controller service for keeping track of rate limits for Atlassian APIs |
| Web Client Service | Controller service for managing HTTP connections to Jira |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to fetch Jira fields, e.g., due to connection issues or invalid credentials |
| retry | Retryable failure occurred, e.g. rate limiting |
| success | Successfully fetched Jira fields |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The MIME type of the returned response, always set to ‘application/json’ |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.atlassian.jira.processors.FetchJiraIssues](/user-guide/data-integration/openflow/processors/fetchjiraissues)
