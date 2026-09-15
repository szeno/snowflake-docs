# GetLinkedInAdsReport 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-linkedin-ads-processors-nar

## Description

Processor downloading metrics from the LinkedIn Reporting APIs.

## Tags

LinkedIn, LinkedIn Ads, ads, report

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Accounts | List of comma-separated accounts. |
| Campaign Groups | List of comma-separated campaign groups. |
| Campaigns | List of comma-separated campaigns. |
| Companies | List of comma-separated companies. |
| Conversion Window | Timeframe for which data is refreshed during incremental load. |
| Metrics | List of comma-separated metrics. |
| OAuth Token Provider | Service providing OAuth access token. |
| Pivots | List of comma-separated pivots. |
| Report Name | Unique name of the report. |
| Shares | List of comma-separated shares. |
| Start Date | Start date from which ingestion should begin. It must be in the yyyy-MM-dd format. |
| Time Granularity | Time granularity of results. |
| Web Client Service Provider | Service providing client for REST request execution. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores information about last report definition in form of hash to detect schema changes. Incrementally loaded reports persist last ingestion date to define ingestion date ranges after initial load. Additionally start date is saved. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Response FlowFiles transferred when successfully processed a response from the LinkedIn Ads Reporting API. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| linkedin.ads.report.name | Unique name of the report. |
| linkedin.ads.run.id | Unique identifier of the run. |
| avro.schema | Avro schema that contains a set of all configured metrics and pivots. |
| linkedin.ads.ingestion.strategy | Strategy that defines whether the report will be downloaded as SNAPSHOT or INCREMENTAL. |
| linkedin.ads.report.schema.changed | Flag that indicates whether the report schema has changed between processor executions. |
| linkedin.ads.ingestion.start.date | Date from which data is downloaded from LinkedIn Ads (including a given date). |
| linkedin.ads.ingestion.end.date | Date to which data is downloaded from LinkedIn Ads (including a given date). |

Expand

Show lessSee more
