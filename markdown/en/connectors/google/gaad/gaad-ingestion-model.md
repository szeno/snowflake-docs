# ingestion model

This topic describes how the ingests data from the [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1) and how sampling may affect ingested data.

## Ingestion strategy

The connector uses two ingestion modes:

- The *initial load* of data occurs directly after configuring the report. Successful *initial load* finishes with data ingested from a chosen start data up to today.
- The *ongoing load* of data begins after completing the *initial load*. Incremental updates occur on a chosen, regular schedule.

The ingestion of each report is an independent process. Ingestion processes may be performed in parallel.

See [Set up data ingestion for your instance](/connectors/google/gaad/gaad-connector-setting-up-data) to learn how to configure a report or choose a *sync schedule* and a *start date*.

### Choosing interval length

The [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1) requires specifying each request’s date range (*startDate* and *endDate*). The connector may make multiple requests during one ingestion load and adjust an interval length as required.
The default interval is 31 days. The interval may be shortened automatically in the following situations:

- The API responded with an error, which the connector may mitigate by retrying the request with a shorter interval.
- The API responded with sampled data (only if the *avoid sampling* option was chosen during report configuration).
- The report contains a large amount of data. In this case, the interval is shortened to reduce the risk of an API error when retrieving subsequent result pages.

The user cannot set the interval length.

## Monitoring ingestion

Ingestion metadata is available in the `CONNECTOR_STATS` view. See more: [Monitoring the](/connectors/google/gaad/gaad-connector-monitoring) .

Copy code

```
SELECT * FROM PUBLIC.CONNECTOR_STATS ORDER BY COMPLETED_AT DESC;
```

The `METADATA` column contains, among other things, the request body that was sent in a request to the [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1). The request body contains information about *startDate* and *endDate*.

The `STATUS` column may be equal to one of the following values:
:   - `COMPLETED` - a successful ingestion.
    - `CANCELED` - the interval length was shortened and the ingestion will continue with adjusted date ranges.
    - `FAILED` - ingestion failed and was not continued.

Note

`FAILED` ingestion doesn’t necessarily mean that the data was lost. The connector may recover from some errors by attempting to download all missing data during the next scheduled report update.
If succeeding ingestion runs were successful, the connector ingested all missing data.

To receive email notifications about failed ingestion runs, set up alerting. See more: [Manage the](/connectors/google/gaad/gaad-connector-managing) .

## About sampling

Sampling is the process of selecting and analyzing a subset of data from a larger dataset in order to extrapolate the result. This means that sampling lowers data quality.
Data quality depends on number of samples used in the process. For more information see [Google Analytics sampling](https://support.google.com/analytics/answer/13331292?hl=en).

Note

By default, the connector doesn’t try to avoid sampling. This setting can be changed only during the initial report configuration.

### Obtaining sampling metadata

The `METADATA` column from the `CONNECTOR_STATS` view contains also sampling metadata. It can be joined with the data saved in a destination table.

Use the following statement to obtain information about the data that is sampled:

Copy code

```
SELECT d.date, d.raw, d.last_update_date, cs.metadata:samplingMetadata:samplesReadCount::INTEGER as samplesReadCount, cs.metadata:samplingMetadata:samplingSpaceSize::INTEGER as samplingSpaceSize, samplesReadCount/samplingSpaceSize as ratio
FROM <destination_table> as d
LEFT JOIN <connector_stats_view> as cs
ON d.ingestion_run_id = cs.run_id
WHERE cs.metadata:samplingMetadata:samplingOccurred::BOOLEAN = true;
```

Replace the placeholders with the actual values, as in the following example for a report named `REPORT_1`.

Copy code

```
SELECT d.date, d.raw, d.last_update_date, cs.metadata:samplingMetadata:samplesReadCount::INTEGER as samplesReadCount, cs.metadata:samplingMetadata:samplingSpaceSize::INTEGER as samplingSpaceSize, samplesReadCount/samplingSpaceSize as ratio
FROM google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema.report_1__raw as d
LEFT JOIN snowflake_connector_for_google_analytics_aggregate_data.public.connector_stats as cs
ON d.ingestion_run_id = cs.run_id
WHERE cs.metadata:samplingMetadata:samplingOccurred::BOOLEAN = true;
```

The result contains the following information related to sampling.

| Name | Description |
| --- | --- |
| `samplesReadCount` | The total number of events read in this sampled report for a date range. |
| `samplingSpaceSize` | The total number of events present in this property’s data that could have been analyzed in this report for a date range. |
| `ratio` | The number of analyzed events to the number of events that could have been analyzed. |

Expand

Show lessSee more

The [Google Analytics sampling metadata documentation](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/ResponseMetaData#SamplingMetadata) provides more information about the meaning of the sampling metadata values.

Note

Metadata about ingestion performed before the upgrade to the 1.4.0 version doesn’t contain information about the occurrence of sampling. It is certain that the data is not sampled only if the *samplingOccurred* flag is equal to false.
