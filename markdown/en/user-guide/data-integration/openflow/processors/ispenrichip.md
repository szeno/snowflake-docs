# ISPEnrichIP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-enrich-nar

## Description

Looks up ISP information for an IP address and adds the information to FlowFile attributes. The ISP data is provided as a MaxMind ISP database. (Note that this is NOT the same as the GeoLite database utilized by some geo enrichment tools). The attribute that contains the IP address to lookup is provided by the ‘IP Address Attribute’ property. If the name of the attribute provided is ‘X’, then the attributes added by enrichment will take the form X.isp.<fieldName>

## Tags

ISP, enrich, ip, maxmind

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
| X.isp.lookup.micros | The number of microseconds that the geo lookup took |
| X.isp.asn | The Autonomous System Number (ASN) identified for the IP address |
| X.isp.asn.organization | The Organization Associated with the ASN identified |
| X.isp.name | The name of the ISP associated with the IP address provided |
| X.isp.organization | The Organization associated with the IP address provided |

Expand

Show lessSee more
