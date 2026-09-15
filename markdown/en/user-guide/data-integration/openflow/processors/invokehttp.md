# InvokeHTTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

An HTTP client processor which can interact with a configurable HTTP Endpoint. The destination URL and HTTP Method are configurable. When the HTTP Method is PUT, POST or PATCH, the FlowFile contents are included as the body of the request and FlowFile attributes are converted to HTTP headers, optionally, based on configuration properties.

## Tags

client, http, https, rest

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| Connection Timeout | Maximum time to wait for initial socket connection to the HTTP URL. |
| HTTP Method | HTTP request method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS). Arbitrary methods are also supported. Methods other than POST, PUT and PATCH will be sent without a message body. |
| HTTP URL | HTTP remote URL including a scheme of http or https, as well as a hostname or IP address with optional port and path elements. Any encoding of the URL must be done by the user. |
| HTTP/2 Disabled | Disable negotiation of HTTP/2 protocol. HTTP/2 requires TLS. HTTP/1.1 protocol supported is required when HTTP/2 is disabled. |
| OAuth2 Access Token Refresh Strategy | Specifies which strategy should be used to refresh the OAuth2 Access Token. |
| Request Body Enabled | Enable sending HTTP request body for PATCH, POST, or PUT methods. |
| Request Chunked Transfer-Encoding Enabled | Enable sending HTTP requests with the Transfer-Encoding Header set to chunked, and disable sending the Content-Length Header. Transfer-Encoding applies to the body in HTTP/1.1 requests as described in RFC 7230 Section 3.3.1 |
| Request Content-Encoding | HTTP Content-Encoding applied to request body during transmission. The receiving server must support the selected encoding to avoid request failures. |
| Request Content-Type | HTTP Content-Type Header applied to when sending an HTTP request body for PATCH, POST, or PUT methods. The Content-Type defaults to application/octet-stream when not configured. |
| Request Date Header Enabled | Enable sending HTTP Date Header on HTTP requests as described in RFC 7231 Section 7.1.1.2. |
| Request Digest Authentication Enabled | Enable Digest Authentication on HTTP requests with Username and Password credentials as described in RFC 7616. |
| Request Failure Penalization Enabled | Enable penalization of request FlowFiles when receiving HTTP response with a status code between 400 and 499. |
| Request Header Attributes Pattern | Regular expression that defines which FlowFile attributes to send as HTTP headers in the request. If not defined, no attributes are sent as headers. Dynamic properties will be always be sent as headers. The dynamic property name will be the header key and the dynamic property value, interpreted as Expression Language, will be the header value. Attributes and their values are limited to ASCII characters due to the requirement of the HTTP protocol. |
| Request Multipart Form-Data Filename Enabled | Enable sending the FlowFile filename attribute as the filename parameter in the Content-Disposition Header for multipart/form-data HTTP requests. |
| Request Multipart Form-Data Name | Enable sending HTTP request body formatted using multipart/form-data and using the form name configured. |
| Request OAuth2 Access Token Provider | Enables managed retrieval of OAuth2 Bearer Token applied to HTTP requests using the Authorization Header. |
| Request Password | The password provided for authentication of HTTP requests. Encoded using Base64 for HTTP Basic Authentication as described in RFC 7617. |
| Request User-Agent | HTTP User-Agent Header applied to requests. RFC 7231 Section 5.5.3 describes recommend formatting. |
| Request Username | The username provided for authentication of HTTP requests. Encoded using Base64 for HTTP Basic Authentication as described in RFC 7617. |
| Response Body Attribute Name | FlowFile attribute name used to write an HTTP response body for FlowFiles transferred to the Original relationship. |
| Response Body Attribute Size | Maximum size in bytes applied when writing an HTTP response body to a FlowFile attribute. Attributes exceeding the maximum will be truncated. |
| Response Body Ignored | Disable writing HTTP response FlowFiles to Response relationship |
| Response Cache Enabled | Enable HTTP response caching described in RFC 7234. Caching responses considers ETag and other headers. |
| Response Cache Size | Maximum size of HTTP response cache in bytes. Caching responses considers ETag and other headers. |
| Response Cookie Strategy | Strategy for accepting and persisting HTTP cookies. Accepting cookies enables persistence across multiple requests. |
| Response FlowFile Naming Strategy | Determines the strategy used for setting the filename attribute of FlowFiles transferred to the Response relationship. |
| Response Generation Required | Enable generation and transfer of a FlowFile to the Response relationship regardless of HTTP response status code received. |
| Response Header Request Attributes Enabled | Enable adding HTTP response headers as attributes to FlowFiles transferred to the Original, Retry or No Retry relationships. |
| Response Header Request Attributes Prefix | Prefix to HTTP response headers when included as attributes to FlowFiles transferred to the Original, Retry or No Retry relationships. It is recommended to end with a separator character like ‘.’ or ‘-’. |
| Response Redirects Enabled | Enable following HTTP redirects sent with HTTP 300 series responses as described in RFC 7231 Section 6.4. |
| SSL Context Service | SSL Context Service provides trusted certificates and client certificates for TLS communication. |
| Socket Idle Connections | Maximum number of idle connections to the HTTP URL. |
| Socket Idle Timeout | Maximum time to wait before closing idle connections to the HTTP URL. |
| Socket Read Timeout | Maximum time to wait for receiving responses from a socket connection to the HTTP URL. |
| Socket Write Timeout | Maximum time to wait for write operations while sending requests from a socket connection to the HTTP URL. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| Failure | Request FlowFiles transferred when receiving socket communication errors. |
| No Retry | Request FlowFiles transferred when receiving HTTP responses with a status code between 400 an 499. |
| Original | Request FlowFiles transferred when receiving HTTP responses with a status code between 200 and 299. |
| Response | Response FlowFiles transferred when receiving HTTP responses with a status code between 200 and 299. Enabling [Response Generation Required] changes routing behavior, sending unsuccessful responses to their corresponding relationships and also sending FlowFiles to the Response relationship as well, regardless of status code received. |
| Retry | Request FlowFiles transferred when receiving HTTP responses with a status code between 500 and 599. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| invokehttp.status.code | The status code that is returned |
| invokehttp.status.message | The status message that is returned |
| invokehttp.response.body | In the instance where the status code received is not a success (2xx) then the response body will be put to the ‘invokehttp.response.body’ attribute of the request FlowFile. |
| invokehttp.request.url | The original request URL |
| invokehttp.request.duration | Duration (in milliseconds) of the HTTP call to the external endpoint |
| invokehttp.response.url | The URL that was ultimately requested after any redirects were followed |
| invokehttp.tx.id | The transaction ID that is returned after reading the response |
| invokehttp.remote.dn | The DN of the remote server |
| invokehttp.java.exception.class | The Java exception class raised when the processor fails |
| invokehttp.java.exception.message | The Java exception message raised when the processor fails |
| user-defined | If the ‘Put Response Body In Attribute’ property is set then whatever it is set to will become the attribute key and the value would be the body of the HTTP response. |

Expand

Show lessSee more
