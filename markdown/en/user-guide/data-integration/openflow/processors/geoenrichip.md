# GeoEnrichIP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-enrich-nar

## Description

Looks up geolocation information for an IP address and adds the geo information to FlowFile attributes. The geo data is provided as a MaxMind database. The attribute that contains the IP address to lookup is provided by the ‘IP Address Attribute’ property. If the name of the attribute provided is ‘X’, then the attributes added by enrichment will take the form X.geo.<fieldName>

## Tags

enrich, geo, ip, maxmind

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| IP Address Attribute | The name of an attribute whose value is a dotted decimal IP address for which enrichment should occur |
| Log Level | The Log Level to use when an IP is not found in the database. Accepted values: INFO, DEBUG, WARN, ERROR. |
| MaxMind Database File | Path to Maxmind IP Enrichment Database File |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| found | Where to route flow files after successfully enriching attributes with data provided by database |
| not found | Where to route flow files after unsuccessfully enriching attributes because no data was found |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| X.geo.lookup.micros | The number of microseconds that the geo lookup took |
| X.geo.city | The city identified for the IP address |
| X.geo.accuracy | The accuracy radius if provided by the database (in Kilometers) |
| X.geo.latitude | The latitude identified for this IP address |
| X.geo.longitude | The longitude identified for this IP address |
| X.geo.subdivision.N | Each subdivision that is identified for this IP address is added with a one-up number appended to the attribute name, starting with 0 |
| X.geo.subdivision.isocode.N | The ISO code for the subdivision that is identified by X.geo.subdivision.N |
| X.geo.country | The country identified for this IP address |
| X.geo.country.isocode | The ISO Code for the country identified |
| X.geo.postalcode | The postal code for the country identified |

Expand

Show lessSee more
