# About Openflow Connector for Google Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for
Google Ads, steps to set it up, and limitations.

Google Ads is an online advertising platform where advertisers can
create and run ads to promote their products or services. Through Google
Ads, you can create online ads to reach people exactly when they’re
interested in offered products and services.

The Openflow Connector for Google Ads:

- Automatically ingests Google Ads data into your Snowflake account.
- Downloads data using the [Google Ads API](https://cloud.google.com/endpoints/docs/openapi/enable-api).
- Lets you configure custom reports with chosen attributes,
  [metrics](https://developers.google.com/google-ads/api/fields/v17/metrics),
  and
  [segments](https://support.google.com/google-ads/answer/2454072).

Use this connector if you’re looking to do the following:

- Import metrics from Google Ads for performance tracking and optimization

## Use cases

### Run the connector in different ingestion modes

There are two ways of ingesting data incrementally and as a snapshot.
Snapshot mode is a default one and is on as long as **segments.date**
segment is not selected. It creates a table in the provided destination
schema and appends on each schedule the newest data from Google Ads.

To configure incremental ingestion user has to fill Report Segments
parameter with segment named **segments.date**, other segments can be
still preset. Then data will be overlapped between the one we fetched
previously and the date range of the current run. The overlap is caused
by the conversion window as we need to ask for the historical data for
the number of days that’s equal to the conversion window, for example, if the
conversion window is set to 14 days and the ingestion happens every day,
there is 13 days of overlap.

### Reconfigure currently running connector

The report configuration can be changed when the processor is running.
To do so go to GetGoogleAdsReportContext and change your desired
parameters. Upon changing only Report Attributes, Metrics or Segments
parameters, the current destination table will be removed and a new one
with updated schema will be created, so before updating them please be
aware that already downloaded data will be deleted.

When the Resource Name or Account Client ID will be changed a new table
will be created. The old destination table will not be dropped.

Modifying the Schedule and Conversion window will not affect in any way
the data already fetched in the destination table.

When the Start Date will be changed, the connector will perform a single
ingestion from that date to the current date and then proceed as
normally in incremental mode. If there is data downloaded from the
period between new Start Date and current date it will be replaced after
change. Data before the new Start Date will not be affected.

#### Rate Limiting Restrictions

[Google Ads API limits](https://developers.google.com/google-ads/api/docs/access-levels) govern how many requests can be made within a given time frame. If your flow exceeds the allowed quota, syncs may slow down or fail with an error. This mostly occurs when your access token makes higher number of requests than the source typically allows. In such cases, we recommend applying for higher access quota (wherever appliable) or reducing the sync frequency.

## Limitations

- Filtering is not supported. Instead, data can be filtered after
  ingestion.
- Custom column ingestion is not supported.
- When segmenting reports, if all selected metrics are zero, they are
  always excluded.
- Attributed resource ingestion is not supported. Instead, multiple
  reports can be joined after ingestion.
- There can be only one report for selected resource name and client id
  pair.
- Modification of report definition when processors are running may lead
  to data inconsistencies. To ensure consistency, before updating
  configuration stop processors and clear queues.

## Next steps

[Set up the Openflow Connector for Google Ads](/user-guide/data-integration/openflow/connectors/google-ads/setup)
