# CreateAmazonAdsReport 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-amazon-ads-processors-nar

## Description

Processor which creates report configuration for Amazon Ads connector. By default it runs once a day.

## Tags

Amazon, Amazon Ads, report

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token Provider | Service providing OAuth access token. |
| Amazon Advertising Client ID | Client ID of the Amazon Advertising user. |
| Region | Environment from which advertising data will be downloaded. |
| Report Ad Product | Type of advertising product being reported. |
| Report Columns | List of columns fetched from Reporting API. |
| Report Filters | Set of filters used to trim returned data. |
| Report Group By | Level of granularity of the report. |
| Report Ingestion Strategy | Configuration of the report ingestion. |
| Report Ingestion Window | How many days from the past should be downloaded during incremental ingestion. |
| Report Name | Unique name of the report. |
| Report Profile ID | The profile ID associated with an advertising account in a specific marketplace. |
| Report Start Date | Start date from which the ingestion should happen. |
| Report Time Unit | Date aggregation. |
| Report Type | Data type contained in the report. |
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
| success | Response FlowFiles transferred when receiving success response from Amazon Ads Reporting API. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| amazon.ads.report.id | Unique identifier of the currently prepared job. |
| amazon.ads.report.name | Unique name of the report. |
| amazon.ads.ingestion.strategy | Strategy which defines if the report will be downloaded as a SNAPSHOT or INCREMENTALLY. |
| amazon.ads.run.id | Unique identifier of the current ingestion process. |
| amazon.ads.ingestion.start.date | Date from which data is downloaded from Amazon Ads (including given date). |
| amazon.ads.ingestion.end.date | Date to which data is downloaded from Amazon Ads (including given date). |
| amazon.ads.report.schema.changed | Flag meaning if the report schema has changed between processor executions. |
| avro.schema | Avro schema containing set of all configured fields. |
| fragment.identifier | A unique ID of each ingestion run. Lets you identify all flow files generated during a single run. |
| fragment.index | Number representing unique identifier in batch of flowfiles generated during one ingestion run. |
| fragment.count | Amount of flowfiles generated during processor execution. |

Expand

Show lessSee more
