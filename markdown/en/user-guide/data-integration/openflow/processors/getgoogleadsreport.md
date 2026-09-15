# GetGoogleAdsReport 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-ads-nar

## Description

A processor which can interact with Google Ads Reporting API. By default it fetches data once a day

## Tags

Google, Google Ads, report

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Client Account ID | ID of the Google Ads account for which the report should be fetched |
| GCP Credentials Service | Controller Service used to obtain Google Cloud Platform credentials. |
| Google Ads Resource Name | Name of the resource that should be used in ‘FROM’ clause of the query |
| Google Developer Token | Developer token required to access Google APIs |
| Report Attributes | List of comma-separated report attributes |
| Report Metrics | List of comma-separated report metrics |
| Report Segments | List of comma-separated report segments |
| Report Start Date | Start date from which the ingestion should happen. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores information about last report definition in form of hash to detect schema changes. In incremental ingestion (when the ‘segments.date’ segment is selected) it keeps track of latest ingested date to download only new data chunks. Additionally start date is saved. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Error FlowFiles transferred when receiving error response from Google Ads Reporting API or when an error occurred during response processing. |
| success | Response FlowFiles transferred when receiving success response from Google Ads Reporting API. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| google.ads.client.account.id | ID of the account in Google Ads for which given report should be ingested |
| google.ads.resource.name | Name of the resource in Google Ads that is a source for the report |
| google.ads.query | Query used to fetch data from Google Ads StreamSearch API |
| google.ads.attributes | Attributes of the selected resource |
| google.ads.metrics | Metrics collected in the context of a given resource |
| google.ads.segments | Buckets in which metrics should be grouped |
| google.ads.ingestion.strategy | The strategy used for ingestion. Can be ‘SNAPSHOT’ or ‘INCREMENTAL’ |
| google.ads.start.date | Date from which data is downloaded from Google Ads (including given date) |
| google.ads.end.date | Date to which data is downloaded from Google Ads (including given date) |
| google.ads.report.schema.changed | Flag meaning if the report schema has changed between processor executions |
| google.ads.report.conversion.window | Number of days which are fetched from Google Ads during incremental load. Based on Conversion Window values |
| fragment.identifier | A unique ID of each ingestion run. Lets you identify all flow files generated during a single run. |
| fragment.index | Number representing unique identifier in batch of flowfiles generated during one ingestion run |
| fragment.count | Amount of flowfiles generated during processor execution |
| avro.schema | Avro schema representing fetched data |
| mime.type | Mime type of the returned report. |

Expand

Show lessSee more
