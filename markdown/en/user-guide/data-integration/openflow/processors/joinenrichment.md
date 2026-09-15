# JoinEnrichment 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Joins together Records from two different FlowFiles where one FlowFile, the ‘original’ contains arbitrary records and the second FlowFile, the ‘enrichment’ contains additional data that should be used to enrich the first. See Additional Details for more information on how to configure this processor and the different use cases that it aims to accomplish.

## Tags

combine, enrichment, fork, join, merge, record, recordpath, sql, streams, wrap

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Default Decimal Precision | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘precision’ denoting number of available digits is required. Generally, precision is defined by column data type definition or database engines default. However undefined precision (0) can be returned from some database engines. ‘Default Decimal Precision’ is used when writing those undefined precision numbers. |
| Default Decimal Scale | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘scale’ denoting number of available decimal digits is required. Generally, scale is defined by column data type definition or database engines default. However when undefined precision (0) is returned, scale can also be uncertain with some database engines. ‘Default Decimal Scale’ is used when writing those undefined numbers. If a value has more decimals than specified scale, then the value will be rounded-up, e.g. 1.53 becomes 2 with scale 0, and 1.5 with scale 1. |
| Enrichment Record Reader | The Record Reader for reading the ‘enrichment’ FlowFile |
| Insertion Record Path | Specifies where in the ‘original’ Record the ‘enrichment’ Record’s fields should be inserted. Note that if the RecordPath does not point to any existing field in the original Record, the enrichment will not be inserted. |
| Join Strategy | Specifies how to join the two FlowFiles into a single FlowFile |
| Maximum number of Bins | Specifies the maximum number of bins that can be held in memory at any one time |
| Original Record Reader | The Record Reader for reading the ‘original’ FlowFile |
| Record Writer | The Record Writer to use for writing the results. If the Record Writer is configured to inherit the schema from the Record, the schema that it will inherit will be the result of merging both the ‘original’ record schema and the ‘enrichment’ record schema. |
| SQL | The SQL SELECT statement to evaluate. Expression Language may be provided, but doing so may result in poorer performance. Because this Processor is dealing with two FlowFiles at a time, it ‘s also important to understand how attributes will be referenced. If both FlowFiles have an attribute with the same name but different values, the Expression Language will resolve to the value provided by the’ enrichment’ FlowFile. |
| Timeout | Specifies the maximum amount of time to wait for the second FlowFile once the first arrives at the processor, after which point the first FlowFile will be routed to the ‘timeout’ relationship. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If both the ‘original’ and ‘enrichment’ FlowFiles arrive at the processor but there was a failure in joining the records, both of those FlowFiles will be routed to this relationship. |
| joined | The resultant FlowFile with Records joined together from both the original and enrichment FlowFiles will be routed to this relationship |
| original | Both of the incoming FlowFiles (‘original’ and ‘enrichment’) will be routed to this Relationship. I.e., this is the ‘original’ version of both of these FlowFiles. |
| timeout | If one of the incoming FlowFiles (i.e., the ‘original’ FlowFile or the ‘enrichment’ FlowFile) arrives to this Processor but the other does not arrive within the configured Timeout period, the FlowFile that did arrive is routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records in the FlowFile |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ForkEnrichment](/user-guide/data-integration/openflow/processors/forkenrichment)
