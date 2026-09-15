# HandleHttpRequest 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Starts an HTTP Server and listens for HTTP Requests. For each request, creates a FlowFile and transfers to ‘success’. This Processor is designed to be used in conjunction with the HandleHttpResponse Processor in order to create a Web Service. In case of a multipart request, one FlowFile is generated for each part.

## Tags

http, https, ingress, listen, request, web service

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Additional HTTP Methods | A comma-separated list of non-standard HTTP Methods that should be allowed |
| Allow DELETE | Allow HTTP DELETE Method |
| Allow GET | Allow HTTP GET Method |
| Allow HEAD | Allow HTTP HEAD Method |
| Allow OPTIONS | Allow HTTP OPTIONS Method |
| Allow POST | Allow HTTP POST Method |
| Allow PUT | Allow HTTP PUT Method |
| Allowed Paths | A Regular Expression that specifies the valid HTTP Paths that are allowed in the incoming URL Requests. If this value is specified and the path of the HTTP Requests does not match this Regular Expression, the Processor will respond with a 404: NotFound |
| Client Authentication | Specifies whether or not the Processor should authenticate clients. This value is ignored if the <SSL Context Service> Property is not specified or the SSL Context provided uses only a KeyStore and not a TrustStore. |
| Default URL Character Set | The character set to use for decoding URL parameters if the HTTP Request does not supply one |
| HTTP Context Map | The HTTP Context Map Controller Service to use for caching the HTTP Request Information |
| HTTP Protocols | HTTP Protocols supported for Application Layer Protocol Negotiation with TLS |
| Hostname | The Hostname to bind to. If not specified, will bind to all hosts |
| Listening Port | The Port to listen on for incoming HTTP requests |
| Maximum Threads | The maximum number of threads that the embedded HTTP server will use for handling requests. |
| Request Header Maximum Size | The maximum supported size of HTTP headers in requests sent to this processor |
| SSL Context Service | The SSL Context Service to use in order to secure the server. If specified, the server will accept only HTTPS requests; otherwise, the server will accept only HTTP requests |
| container-queue-size | The size of the queue for Http Request Containers |
| multipart-read-buffer-size | The threshold size, at which the contents of an incoming file would be written to disk. Only applies for requests with Content-Type: multipart/form-data. It is used to prevent denial of service type of attacks, to prevent filling up the heap or disk space. |
| multipart-request-max-size | The max size of the request. Only applies for requests with Content-Type: multipart/form-data, and is used to prevent denial of service type of attacks, to prevent filling up the heap or disk space |
| parameters-to-attributes | A comma-separated list of HTTP parameters or form data to output as attributes |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All content that is received is routed to the ‘success’ relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| http.context.identifier | An identifier that allows the HandleHttpRequest and HandleHttpResponse to coordinate which FlowFile belongs to which HTTP Request/Response. |
| mime.type | The MIME Type of the data, according to the HTTP Header “Content-Type” |
| http.servlet.path | The part of the request URL that is considered the Servlet Path |
| http.context.path | The part of the request URL that is considered to be the Context Path |
| http.method | The HTTP Method that was used for the request, such as GET or POST |
| http.local.name | IP address/hostname of the server |
| http.server.port | Listening port of the server |
| http.query.string | The query string portion of the Request URL |
| http.remote.host | The hostname of the requestor |
| http.remote.addr | The hostname:port combination of the requestor |
| http.remote.user | The username of the requestor |
| http.protocol | The protocol used to communicate |
| http.request.uri | The full Request URL |
| http.auth.type | The type of HTTP Authorization used |
| http.principal.name | The name of the authenticated user making the request |
| http.query.param.XXX | Each of query parameters in the request will be added as an attribute, prefixed with “http.query.param.” |
| http.param.XXX | Form parameters in the request that are configured by “Parameters to Attributes List” will be added as an attribute, prefixed with “http.param.”. Putting form parameters of large size is not recommended. |
| http.subject.dn | The Distinguished Name of the requestor. This value will not be populated unless the Processor is configured to use an SSLContext Service |
| http.issuer.dn | The Distinguished Name of the entity that issued the Subject’s certificate. This value will not be populated unless the Processor is configured to use an SSLContext Service |
| http.certificate.sans.N.name | X.509 Client Certificate Subject Alternative Name value from mutual TLS authentication. The attribute name has a zero-based index ordered according to the content of Client Certificate |
| http.certificate.sans.N.nameType | X.509 Client Certificate Subject Alternative Name type from mutual TLS authentication. The attribute name has a zero-based index ordered according to the content of Client Certificate. The attribute value is one of the General Names from RFC 3280 Section 4.1.2.7 |
| http.headers.XXX | Each of the HTTP Headers that is received in the request will be added as an attribute, prefixed with “http.headers.” For example, if the request contains an HTTP Header named “x-my-header”, then the value will be added to an attribute named “http.headers.x-my-header” |
| http.headers.multipart.XXX | Each of the HTTP Headers that is received in the multipart request will be added as an attribute, prefixed with “http.headers.multipart.” For example, if the multipart request contains an HTTP Header named “content-disposition”, then the value will be added to an attribute named “http.headers.multipart.content-disposition” |
| http.multipart.size | For requests with Content-Type “multipart/form-data”, the part’s content size is recorded into this attribute |
| http.multipart.content.type | For requests with Content-Type “multipart/form-data”, the part’s content type is recorded into this attribute |
| http.multipart.name | For requests with Content-Type “multipart/form-data”, the part’s name is recorded into this attribute |
| http.multipart.filename | For requests with Content-Type “multipart/form-data”, when the part contains an uploaded file, the name of the file is recorded into this attribute. Files are stored temporarily at the default temporary-file directory specified in “java.io.File” Java Docs) |
| http.multipart.fragments.sequence.number | For requests with Content-Type “multipart/form-data”, the part’s index is recorded into this attribute. The index starts with 1. |
| http.multipart.fragments.total.number | For requests with Content-Type “multipart/form-data”, the count of all parts is recorded into this attribute. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.HandleHttpResponse](/user-guide/data-integration/openflow/processors/handlehttpresponse)
