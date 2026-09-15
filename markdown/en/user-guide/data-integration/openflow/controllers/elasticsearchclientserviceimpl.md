# ElasticSearchClientServiceImpl

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A controller service for accessing an Elasticsearch client, using the Elasticsearch (low-level) REST Client.

## Tags

client, elasticsearch, elasticsearch6, elasticsearch7, elasticsearch8

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| API Key \* | API Key |  |  | Encoded API key. |
| API Key ID \* | API Key ID |  |  | Unique identifier of the API key. |
| Authorization Scheme \* | Authorization Scheme | BASIC | - None - PKI - Basic - API Key - JWT | Authorization Scheme used for optional authentication to Elasticsearch. |
| Character Set \* | Character Set | UTF-8 |  | The charset to use for interpreting the response from Elasticsearch. |
| Connect timeout \* | Connect timeout | 5000 |  | Controls the amount of time, in milliseconds, before a timeout occurs when trying to connect. |
| Enable Compression \* | Enable Compression | false | - true - false | Whether the REST client should compress requests using gzip content encoding and add the “Accept-Encoding: gzip” header to receive compressed responses |
| HTTP Hosts \* | HTTP Hosts |  |  | A comma-separated list of HTTP hosts that host Elasticsearch query nodes.The HTTP Hosts should be valid URIs including protocol, domain and port for each entry.For example “<https://elasticsearch1:9200>, <https://elasticsearch2:9200>”.Note that the Host is included in requests as a header (typically including domain and port, e.g. elasticsearch:9200). |
| JWT Shared Secret \* | JWT Shared Secret |  |  | JWT realm Shared Secret. |
| Node Selector \* | Node Selector | ANY | - Any - Skip Dedicated Masters | Selects Elasticsearch nodes that can receive requests. Used to keep requests away from dedicated Elasticsearch master nodes |
| OAuth2 Access Token Provider \* | OAuth2 Access Token Provider |  |  | The OAuth2 Access Token Provider used to provide JWTs for Bearer Token Authorization with Elasticsearch. |
| Password \* | Password |  |  | The password to use with XPack security. |
| Path Prefix | Path Prefix |  |  | Sets the path’s prefix for every request used by the http client. For example, if this is set to “/my/path”, then any client request will become “/my/path/” + endpoint. In essence, every request’s endpoint is prefixed by this pathPrefix. The path prefix is useful for when Elasticsearch is behind a proxy that provides a base path or a proxy that requires all paths to start with ‘/’; it is not intended for other purposes and it should not be supplied in other scenarios |
| Read Timeout \* | Read Timeout | 60000 |  | Controls the amount of time, in milliseconds, before a timeout occurs when waiting for a response. |
| Run As User | Run As User |  |  | The username to impersonate within Elasticsearch. |
| SSL Context Service | SSL Context Service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections. This service only applies if the Elasticsearch endpoint(s) have been secured with TLS/SSL. |
| Send Meta Header \* | Send Meta Header | true | - true - false | Whether to send a “X-Elastic-Client-Meta” header that describes the runtime environment. It contains information that is similar to what could be found in User-Agent. Using a separate header allows applications to use User-Agent for their own needs, e.g. to identify application version or other environment information |
| Sniff Cluster Nodes \* | Sniff Cluster Nodes | false | - true - false | Periodically sniff for nodes within the Elasticsearch cluster via the Elasticsearch Node Info API. If Elasticsearch security features are enabled (default to “true” for 8.x+), the Elasticsearch user must have the “monitor” or “manage” cluster privilege to use this API.Note that all HTTP Hosts (and those that may be discovered within the cluster using the Sniffer) must use the same protocol, e.g. http or https, and be contactable using the same client settings. Finally the Elasticsearch “network.publish\_host” must match one of the “network.bind\_host” list entries see <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html> for more information |
| Sniff on Failure \* | Sniff on Failure | false | - true - false | Enable sniffing on failure, meaning that after each failure the Elasticsearch nodes list gets updated straight away rather than at the following ordinary sniffing round |
| Sniffer Failure Delay \* | Sniffer Failure Delay | 1 min |  | Delay between an Elasticsearch request failure and updating available Cluster nodes using the Sniffer |
| Sniffer Interval \* | Sniffer Interval | 5 mins |  | Interval between Cluster sniffer operations |
| Sniffer Request Timeout \* | Sniffer Request Timeout | 1 sec |  | Cluster sniffer timeout for node info requests |
| Strict Deprecation \* | Strict Deprecation | false | - true - false | Whether the REST client should return any response containing at least one warning header as a failure |
| Suppress Null and Empty Values \* | Suppress Null and Empty Values | always-suppress | - Never Suppress - Always Suppress | Specifies how the writer should handle null and empty fields (including objects and arrays) |
| Username \* | Username |  |  | The username to use with XPack security. |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
