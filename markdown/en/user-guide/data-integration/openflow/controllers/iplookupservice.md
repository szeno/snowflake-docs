# IPLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A lookup service that provides several types of enrichment information for IP addresses. The service is configured by providing a MaxMind Database file and specifying which types of enrichment should be provided for an IP Address or Hostname. Each type of enrichment is a separate lookup, so configuring the service to provide all of the available enrichment data may be slower than returning only a portion of the available enrichments. In order to use this service, a lookup must be performed using key of ‘ip’ and a value that is a valid IP address or hostname. View the Usage of this component and choose to view Additional Details for more information, such as the Schema that pertains to the information that is returned.

## Tags

anonymous, cellular, domain, enrich, geo, ip, ipgeo, isp, lookup, maxmind, tor

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| MaxMind Database File \* | database-file |  |  | Path to Maxmind IP Enrichment Database File |
| Lookup Anonymous IP Information \* | lookup-anonymous-ip | false | - true - false | Specifies whether or not information about whether or not the IP address belongs to an anonymous network should be returned. |
| Lookup Geo Enrichment \* | lookup-city | true | - true - false | Specifies whether or not information about the geographic information, such as cities, corresponding to the IP address should be returned |
| Lookup Connection Type \* | lookup-connection-type | false | - true - false | Specifies whether or not information about the Connection Type corresponding to the IP address should be returned. If true, the lookup will contain a ‘connectionType’ field that (if populated) will contain a value of ‘Dialup’, ‘Cable/DSL’, ‘Corporate’, or ‘Cellular’ |
| Lookup Domain Name \* | lookup-domain | false | - true - false | Specifies whether or not information about the Domain Name corresponding to the IP address should be returned. If true, the lookup will contain second-level domain information, such as foo.com but will not contain bar.foo.com |
| Lookup ISP \* | lookup-isp | false | - true - false | Specifies whether or not information about the Information Service Provider corresponding to the IP address should be returned |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
