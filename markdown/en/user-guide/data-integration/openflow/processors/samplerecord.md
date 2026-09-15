# SampleRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Samples the records of a FlowFile based on a specified sampling strategy (such as Reservoir Sampling). The resulting FlowFile may be of a fixed number of records (in the case of reservoir-based algorithms) or some subset of the total number of records (in the case of probabilistic sampling), or a deterministic number of records (in the case of interval sampling).

## Tags

interval, range, record, reservoir, sample

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |
| record-writer | Specifies the Controller Service to use for writing results to a FlowFile |
| sample-record-interval | Specifies the number of records to skip before writing a record to the outgoing FlowFile. This property is only used if Sampling Strategy is set to Interval Sampling. A value of zero (0) will cause no records to be included in theoutgoing FlowFile, a value of one (1) will cause all records to be included, and a value of two (2) will cause half the records to be included, and so on. |
| sample-record-probability | Specifies the probability (as a percent from 0-100) of a record being included in the outgoing FlowFile. This property is only used if Sampling Strategy is set to Probabilistic Sampling. A value of zero (0) will cause no records to be included in theoutgoing FlowFile, and a value of 100 will cause all records to be included in the outgoing FlowFile.. |
| sample-record-random-seed | Specifies a particular number to use as the seed for the random number generator (used by probabilistic strategies). Setting this property will ensure the same records are selected even when using probabilistic strategies. |
| sample-record-range | Specifies the range of records to include in the sample, from 1 to the total number of records. An example is ’3,6-8,20-’ which includes the third record, the sixth, seventh and eighth records, and all records from the twentieth record on. Commas separate intervals that don’t overlap, and an interval can be between two numbers (i.e. 6-8) or up to a given number (i.e. -5), or from a number to the number of the last record (i.e. 20-). If this property is unset, all records will be included. |
| sample-record-reservoir | Specifies the number of records to write to the outgoing FlowFile. This property is only used if Sampling Strategy is set to reservoir-based strategies such as Reservoir Sampling. |
| sample-record-sampling-strategy | Specifies which method to use for sampling records from the incoming FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, any record is not valid), the original FlowFile will be routed to this relationship |
| original | The original FlowFile is routed to this relationship if sampling is successful |
| success | The FlowFile is routed to this relationship if the sampling completed successfully |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The MIME type indicated by the record writer |
| record.count | The number of records in the resulting flow file |

Expand

Show lessSee more
