# CreateMetaAdsReport 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-meta-ads-processors-nar

## Description

Processor which creates report configuration for Meta Ads connector. By default it runs once a day.

## Tags

Facebook, Meta, Meta Ads, report

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | Token required to request Meta Ads Marketing API. It must match pattern ‘Bearer <Access Token Value>’. |
| Action Report Time | Determine the report time of action stats. |
| Click Attribution Window | Attribution window for the click action. |
| Meta Ads API Version | Version of Meta Ads API which is used for report generation. |
| Report Breakdowns | List of values which determine how to break down the result. Multiple breakdowns can be picked, but only some combinations work. |
| Report Fields | List of fields fetched from Marketing API. If non are selected most used fields will be downloaded. |
| Report Ingestion Strategy | Configuration of the report ingestion. |
| Report Level | Granularity of the report. |
| Report Name | Unique name of the report. |
| Report Object ID | ID of the object from which data will be fetched. It can be Account, Campaign, Ad or Ad Set ID. |
| Report Start Date | Start date from which the ingestion should happen. |
| Report Time Increment | Value of aggregation in days. |
| View Attribution Window | Attribution window for the view action. |
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
| success | Response FlowFiles transferred when receiving success response from Meta Ads Marketing API. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| meta.ads.report.id | Unique identifier of the currently prepared job. |
| meta.ads.report.name | Unique name of the report. |
| meta.ads.report.ingestion.strategy | Strategy which defines if the report will be downloaded as a SNAPSHOT or INCREMENTALLY. |
| meta.ads.run.id | Unique identifier of the current ingestion process. |
| meta.ads.ingestion.start.date | Date from which data is downloaded from Meta Ads (including given date). |
| meta.ads.ingestion.end.date | Date to which data is downloaded from Meta Ads (including given date). |
| meta.ads.report.schema.changed | Flag meaning if the report schema has changed between processor executions. |
| avro.schema | Avro schema containing set of all configured fields. |

Expand

Show lessSee more
