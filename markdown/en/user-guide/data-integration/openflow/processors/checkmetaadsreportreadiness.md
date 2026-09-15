# CheckMetaAdsReportReadiness 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-meta-ads-processors-nar

## Description

Processor checking if the Meta Ads report is ready for download.

## Tags

Facebook, Meta, Meta Ads, report

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | Token required to request Meta Ads Marketing API. It must match pattern ‘Bearer <Access Token Value>’. |
| Meta Ads API Version | Version of Meta Ads API which is used for report generation. |
| Report ID | ID of the generated report. |
| Web Client Service Provider | Service providing client for REST request execution. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Error FlowFiles transferred when receiving error response from Meta Ads Marketing API or when an error occurred during response processing. |
| ready | Response FlowFiles transferred when receiving Job Completed response from Meta Ads Marketing API. |
| retry | Response FlowFiles transferred when report prepared by Meta Ads Marketing API is not yet ready to be downloaded. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| meta.ads.report.status | Current state of the processed report. |

Expand

Show lessSee more
