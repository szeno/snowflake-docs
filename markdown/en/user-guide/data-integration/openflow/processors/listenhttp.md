# ListenHTTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Starts an HTTP Server and listens on a given base path to transform incoming requests into FlowFiles. The default URI of the Service will be http://{hostname}:{port}/contentListener. Only HEAD and POST requests are supported. GET, PUT, DELETE, OPTIONS and TRACE will result in an error and the HTTP response status code 405; CONNECT will also result in an error and the HTTP response status code 400. GET is supported on <service\_URI>/healthcheck. If the service is available, it returns “200 OK” with the content “OK”. The health check functionality can be configured to be accessible via a different port. For details, see the documentation of the “Listening Port for health check requests” property. A Record Reader and Record Writer property can be enabled on the processor to process incoming requests as records. Record processing is not allowed for multipart requests and request in FlowFileV3 format (minifi). If the incoming request contains a FlowFileV3 package format, the data will be unpacked automatically into individual FlowFile(s) contained within the package; the original FlowFile names are restored.

## Tags

http, https, ingest, listen, rest

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authorized DN Pattern | A Regular Expression to apply against the Subject’s Distinguished Name of incoming connections. If the Pattern does not match the Subject DN, the processor will respond with a status of HTTP 403 Forbidden. |
| Base Path | Base path for incoming connections |
| HTTP Headers to receive as Attributes (Regex) | Specifies the Regular Expression that determines the names of HTTP Headers that should be passed along as FlowFile attributes |
| HTTP Protocols | HTTP Protocols supported for Application Layer Protocol Negotiation with TLS |
| Listening Port | The Port to listen on for incoming connections |
| Max Unconfirmed Flowfile Time | The maximum amount of time to wait for a FlowFile to be confirmed before it is removed from the cache |
| Request Header Maximum Size | The maximum supported size of HTTP headers in requests sent to this processor |
| Return Code | The HTTP return code returned after every HTTP call |
| SSL Context Service | SSL Context Service enables support for HTTPS |
| authorized-issuer-dn-pattern | A Regular Expression to apply against the Issuer’s Distinguished Name of incoming connections. If the Pattern does not match the Issuer DN, the processor will respond with a status of HTTP 403 Forbidden. |
| client-authentication | Client Authentication policy for TLS connections. Required when SSL Context Service configured. |
| health-check-port | The port to listen on for incoming health check requests. If set, it must be different from the Listening Port. Configure this port if the processor is set to use two-way SSL and a load balancer that does not support client authentication for health check requests is used. Only /<base\_path>/healthcheck service is available via this port and only GET and HEAD requests are supported. If the processor is set not to use SSL, SSL will not be used on this port, either. If the processor is set to use one-way SSL, one-way SSL will be used on this port. If the processor is set to use two-way SSL, one-way SSL will be used on this port (client authentication not required). |
| max-thread-pool-size | The maximum number of threads to be used by the embedded Jetty server. The value can be set between 8 and 1000. The value of this property affects the performance of the flows and the operating system, therefore the default value should only be changed in justified cases. A value that is less than the default value may be suitable if only a small number of HTTP clients connect to the server. A greater value may be suitable if a large number of HTTP clients are expected to make requests to the server simultaneously. |
| multipart-read-buffer-size | The threshold size, at which the contents of an incoming file would be written to disk. Only applies for requests with Content-Type: multipart/form-data. It is used to prevent denial of service type of attacks, to prevent filling up the heap or disk space. |
| multipart-request-max-size | The max size of the request. Only applies for requests with Content-Type: multipart/form-data, and is used to prevent denial of service type of attacks, to prevent filling up the heap or disk space |
| record-reader | The Record Reader to use parsing the incoming FlowFile into Records |
| record-writer | The Record Writer to use for serializing Records after they have been transformed |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Relationship for successfully received FlowFiles |

Expand

Show lessSee more

## Use cases

| Unpack FlowFileV3 content received in a POST |
| --- |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Limit the date flow rate that is accepted |
| --- |

Expand

Show lessSee more
