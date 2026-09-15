# HttpRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Format and send Records to a configured uri using HTTP post. The Record Writer formats the records which are sent as the body of the HTTP post request. JsonRecordSetWriter is often used with this processor because many HTTP posts require a JSON body.

## Tags

http, post, record, sink

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| API URL \* | API URL |  |  | The URL which receives the HTTP requests. |
| Maximum Batch Size \* | Maximum Batch Size | 0 |  | Specifies the maximum number of records to send in the body of each HTTP request. Zero means the batch size is not limited, and all records are sent together in a single HTTP request. |
| OAuth2 Access Token Provider | OAuth2 Access Token Provider |  |  | OAuth2 service that provides the access tokens for the HTTP requests. |
| Web Service Client Provider \* | Web Service Client Provider |  |  | Controller service to provide the HTTP client for sending the HTTP requests. |
| Record Writer \* | record-sink-record-writer |  |  | Specifies the Controller Service to use for writing out the records. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
