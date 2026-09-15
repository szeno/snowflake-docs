# GeoEnrichIPRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-enrich-nar

## Description

Looks up geolocation information for an IP address and adds the geo information to FlowFile attributes. The geo data is provided as a MaxMind database. This version uses the NiFi Record API to allow large scale enrichment of record-oriented data sets. Each field provided by the MaxMind database can be directed to a field of the user’s choosing by providing a record path for that field configuration.

## Tags

enrich, geo, ip, maxmind, record

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| City Record Path | Record path for putting the city identified for the IP address |
| Country ISO Code Record Path | Record path for putting the ISO Code for the country identified |
| Country Postal Code Record Path | Record path for putting the postal code for the country identified |
| Country Record Path | Record path for putting the country identified for this IP address |
| IP Address Record Path | The record path to retrieve the IP address for doing the lookup. |
| Latitude Record Path | Record path for putting the latitude identified for this IP address |
| Log Level | The Log Level to use when an IP is not found in the database. Accepted values: INFO, DEBUG, WARN, ERROR. |
| Longitude Record Path | Record path for putting the longitude identified for this IP address |
| MaxMind Database File | Path to Maxmind IP Enrichment Database File |
| Record Reader | Record reader service to use for reading the flowfile contents. |
| Record Writer | Record writer service to use for enriching the flowfile contents. |
| Separate Enriched From Not Enriched | Separate records that have been enriched from ones that have not. Default behavior is to send everything to the found relationship if even one record is enriched. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| found | Where to route flow files after successfully enriching attributes with data provided by database |
| not found | Where to route flow files after unsuccessfully enriching attributes because no data was found |
| original | The original input flowfile goes to this relationship regardless of whether the content was enriched or not. |

Expand

Show lessSee more
