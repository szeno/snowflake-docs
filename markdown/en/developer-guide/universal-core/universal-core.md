# Universal Core

Preview Feature

This feature is in public preview. Inputs and behavior may change between releases.

The Snowflake **Universal Core** is a shared Rust library (`sf_core`) that contains the networking, authentication, data-transfer, and protocol logic that every Snowflake driver needs. Each driver is built as a thin, language-specific wrapper around this shared core; the Rust layer is not visible to application code.

Before the Universal Core, each Snowflake driver maintained its own independent implementation of these capabilities. A security fix or protocol update had to be applied separately to every driver. The Universal Core resolves this by implementing each capability once, in a single place, and making it available to all drivers.

This page describes the Universal Core architecture:

- [Architecture](#label-universal-core-architecture)
- [Benefits](#label-universal-core-benefits)
- [What sf\_core handles](#label-universal-core-capabilities)
- [Driver adoption](#label-universal-core-driver-adoption)

## Architecture

The Universal Core splits Snowflake driver work into two well-defined layers:

**`sf_core` (Rust):** The shared library. It handles all protocol-level work: forming and validating requests, managing TLS connections, executing authentication flows, fetching and decoding result sets, transferring files to and from stages, and reporting telemetry. The Rust implementation is compiled into each driver package as a native extension.

**Language wrapper:** A thin layer that exposes the driver’s public API in the target language, for example the PEP 249 `Connection` and `Cursor` objects for Python. The wrapper translates between the language’s conventions and the `sf_core` C API, handles language-runtime lifecycle concerns such as the GIL or async event loops, and surfaces driver-specific ergonomics. It contains no protocol logic of its own.

Copy code

```
Application code
       │
       ▼
 Language wrapper            Python / JDBC / ODBC / Node.js / ...
  (thin, per-driver)
       │  C API
       ▼
    sf_core                  Rust, shared across all drivers
  (Rust library)
       │
       ▼
  Snowflake service
```

This split means that any change to `sf_core`, whether a security fix, a protocol update, or a new authentication flow, becomes available to every driver that wraps it as soon as it is released, without each driver team needing to implement the change independently.

## Benefits

**Consistent behavior across drivers:** Because protocol and authentication logic lives in `sf_core`, the same query, the same authentication flow, and the same error condition produce the same outcome across drivers built on it.

**Faster security response:** Security fixes in areas such as TLS configuration, OAuth validation, and certificate revocation checking reach every driver simultaneously through a single `sf_core` release. Driver teams do not need to separately backport the fix to each language implementation.

**Performance:** Result-set decoding and concurrent chunk downloads are implemented once in Rust, so an optimization there applies to every driver built on the core without per-driver work.

**Smaller wrapper surface:** Because `sf_core` handles the protocol, each language wrapper contains no protocol logic of its own. This reduces the per-driver maintenance burden, the number of places where bugs can be introduced, and the size of what you install.

## What sf\_core handles

### Networking and TLS

`sf_core` owns the HTTP client and all TLS configuration. It negotiates TLS versions, manages certificate validation, applies connection timeouts and retry logic with exponential backoff, and handles proxy configuration. Certificate revocation checking uses certificate revocation lists (CRLs) rather than the Online Certificate Status Protocol (OCSP), and is off by default; see the driver pages for how to enable it and what it requires of your network. All drivers that use `sf_core` get the same TLS policy and the same network resilience behavior.

### Authentication

All authentication flows are implemented in `sf_core`: username/password, username/password with multi-factor authentication (MFA), key pair, programmatic access tokens, external browser, native Okta, OAuth client credentials, OAuth authorization code, OAuth with a pre-acquired token, and workload identity federation on AWS, Azure, Google Cloud, and OpenID Connect (OIDC). MFA token caching is handled there too. The wrapper passes the configured credentials to `sf_core` at connection time and receives a session token in return; the wrapper itself has no knowledge of the authentication protocol.

### Result-set fetching and decoding

After a query completes, Snowflake returns either a JSON or Arrow-encoded result set, potentially spread across multiple chunks hosted in cloud storage. `sf_core` downloads and decodes these chunks, including decompression and Arrow IPC deserialization, and makes the rows available to the wrapper through a typed iterator interface.

### Stage file transfers

PUT and GET operations (uploading files to and downloading files from Snowflake internal stages) are handled by `sf_core`. This includes multipart upload, chunk-level retry, cloud-provider-specific signing (S3, Azure Blob Storage, Google Cloud Storage), and compression negotiation.

### Session and token management

`sf_core` manages session lifetime, including token refresh, heartbeat keep-alives, and multi-factor-authentication token caching. Token-refresh races across concurrent requests are serialized inside the Rust layer; wrapper code does not need to coordinate them.

### Telemetry and diagnostics

`sf_core` collects structured telemetry about driver operations, errors, and performance, and sends it to Snowflake’s telemetry service. The diagnostic service, which validates connectivity and configuration without requiring a full Snowflake login, is also implemented in `sf_core` and exposed through each driver’s diagnostic command.

## Driver adoption

The Universal Core changes how a driver is built, not the interface your application targets. A driver built on it implements the same standard API, accepts the same connection parameters except where its own page notes differences, and the existing documentation for that driver still applies.

How you obtain a Universal Core driver differs by language. See the driver’s own page for what to install.

The Universal Core is being rolled out across Snowflake drivers progressively. The table below reflects the current status.

| Driver | Universal Core status | How it ships |
| --- | --- | --- |
| Python (`snowflake-connector-python` 5.x) | Public preview | New major version, 5.x, of the same package |
| ODBC (Snowflake ODBC Driver 4.x) | Public preview | New major version, 4.x; replaces 3.x on the machine |
| JDBC | Private preview | New Maven artifacts, `snowflake-jdbc-native` and `snowflake-jdbc-native-all` |
| Node.js | Planned |  |
| .NET | Planned |  |
| Go | Planned |  |
| PHP | Planned |  |

Expand

Show lessSee more

Each driver’s own documentation page notes its Universal Core status. For drivers currently in preview, see the driver-specific Universal Core page for installation instructions, known behavior differences, and migration guidance.
