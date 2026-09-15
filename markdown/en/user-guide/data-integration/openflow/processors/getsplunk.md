# GetSplunk 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-splunk-nar

## Description

Retrieves data from Splunk Enterprise.

## Tags

get, logs, splunk

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| API Version | Select which version of the Splunk Search API to use for search operations. Version 2 is recommended for newer Splunk instances. |
| Application | The Splunk Application to query. |
| Connection Timeout | Max wait time for connection to the Splunk server. |
| Earliest Time | The value to use for the earliest time when querying. Only used with a Time Range Strategy of Provided. See Splunk’s documentation on Search Time Modifiers for guidance in populating this field. |
| Hostname | The ip address or hostname of the Splunk server. |
| Latest Time | The value to use for the latest time when querying. Only used with a Time Range Strategy of Provided. See Splunk’s documentation on Search Time Modifiers for guidance in populating this field. |
| Output Mode | The output mode for the results. |
| Owner | The owner to pass to Splunk. |
| Password | The password to authenticate to Splunk. |
| Port | The port of the Splunk server. |
| Query | The query to execute. Typically beginning with a <search> command followed by a search clause, such as <search source=”<tcp:7689>”> to search for messages received on TCP port 7689. |
| Read Timeout | Max wait time for response from the Splunk server. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Scheme | The scheme for connecting to Splunk. |
| Security Protocol | The security protocol to use for communicating with Splunk. |
| Time Field Strategy | Indicates whether to search by the time attached to the event, or by the time the event was indexed in Splunk. |
| Time Range Strategy | Indicates how to apply time ranges to each execution of the query. Selecting a managed option allows the processor to apply a time range from the last execution time to the current execution time. When using <Managed from Beginning>, an earliest time will not be applied on the first execution, and thus all records searched. When using <Managed from Current> the earliest time of the first execution will be the initial execution time. When using <Provided>, the time range will come from the Earliest Time and Latest Time properties, or no time range will be applied if these properties are left blank. |
| Time Zone | The Time Zone to use for formatting dates when performing a search. Only used with Managed time strategies. |
| Token | The token to pass to Splunk. |
| Username | The username to authenticate to Splunk. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | If using one of the managed Time Range Strategies, this processor will store the values of the latest and earliest times from the previous execution so that the next execution of the can pick up where the last execution left off. The state will be cleared and start over if the query is changed. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Results retrieved from Splunk are sent out this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| splunk.query | The query that performed to produce the FlowFile. |
| splunk.earliest.time | The value of the earliest time that was used when performing the query. |
| splunk.latest.time | The value of the latest time that was used when performing the query. |

Expand

Show lessSee more
