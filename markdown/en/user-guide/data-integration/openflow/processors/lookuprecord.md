# LookupRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Extracts one or more fields from a Record and looks up a value for those fields in a LookupService. If a result is returned by the LookupService, that result is optionally added to the Record. In this case, the processor functions as an Enrichment processor. Regardless, the Record is then routed to either the ‘matched’ relationship or ‘unmatched’ relationship (if the ‘Routing Strategy’ property is configured to do so), indicating whether or not a result was returned by the LookupService, allowing the processor to also function as a Routing processor. The “coordinates” to use for looking up a value in the Lookup Service are defined by adding a user-defined property. Each property that is added will have an entry added to a Map, where the name of the property becomes the Map Key and the value returned by the RecordPath becomes the value for that key. If multiple values are returned by the RecordPath, then the Record will be routed to the ‘unmatched’ relationship (or ‘success’, depending on the ‘Routing Strategy’ property’s configuration). If one or more fields match the Result RecordPath, all fields that match will be updated. If there is no match in the configured LookupService, then no fields will be updated. I.e., it will not overwrite an existing value in the Record with a null value. Please note, however, that if the results returned by the LookupService are not accounted for in your schema (specifically, the schema that is configured for your Record Writer) then the fields will not be written out to the FlowFile.

## Tags

avro, convert, csv, database, db, enrichment, filter, json, logs, lookup, record, route

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Root Record Path | A RecordPath that points to a child Record within each of the top-level Records in the FlowFile. If specified, the additional RecordPath properties will be evaluated against this child Record instead of the top-level Record. This allows for performing enrichment against multiple child Records within a single top-level Record. |
| lookup-service | The Lookup Service to use in order to lookup a value in each Record |
| record-path-lookup-miss-result-cache-size | Specifies how many lookup values/records should be cached. Setting this property to zero means no caching will be done and the table will be queried for each lookup value in each record. If the lookup table changes often or the most recent data must be retrieved, do not use the cache. |
| record-reader | Specifies the Controller Service to use for reading incoming data |
| record-update-strategy | This property defines the strategy to use when updating the record with the value returned by the Lookup Service. |
| record-writer | Specifies the Controller Service to use for writing out the records |
| result-contents | When a result is obtained that contains a Record, this property determines whether the Record itself is inserted at the configured path or if the contents of the Record (i.e., the sub-fields) will be inserted at the configured path. |
| result-record-path | A RecordPath that points to the field whose value should be updated with whatever value is returned from the Lookup Service. If not specified, the value that is returned from the Lookup Service will be ignored, except for determining whether the FlowFile should be routed to the ‘matched’ or ‘unmatched’ Relationship. |
| routing-strategy | Specifies how to route records after a Lookup has completed |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile cannot be enriched, the unchanged FlowFile will be routed to this relationship |
| success | All records will be sent to this Relationship if configured to do so, unless a failure occurs |

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

- [org.apache.nifi.processors.standard.ConvertRecord](/user-guide/data-integration/openflow/processors/convertrecord)
- [org.apache.nifi.processors.standard.SplitRecord](/user-guide/data-integration/openflow/processors/splitrecord)
