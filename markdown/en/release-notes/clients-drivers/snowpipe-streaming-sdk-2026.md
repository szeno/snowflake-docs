# Snowpipe Streaming SDK release notes for 2026

This article contains the release notes for the Snowpipe Streaming SDK, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowpipe Streaming SDK updates.

## Version 1.7.0 (July 23, 2026)

### Behavior changes

- The SDK now trusts the operating system certificate store for TLS instead of a compiled-in Mozilla root bundle. This enables connections through TLS-inspecting corporate proxies (for example, Cloudflare WARP) when the inspection CA is installed in the OS trust store, with no client configuration. Minimal container images must include CA certificates (or set `SSL_CERT_FILE` / `SSL_CERT_DIR`).

### Bug fixes

- Updated Jackson databind in the Java SDK to address known security vulnerabilities.

## Version 1.6.2 (July 09, 2026)

### New features and updates

- Added elastic channels and table mode to the Snowpipe Streaming SDK for Node.js, bringing Node.js parity with the Java and Python SDKs for elastic ingestion. Elastic channels require SDK version 1.6.2 or later. For more information, see [Elastic Channels](/LIMITEDACCESS/snowpipe-streaming-elastic-channels).
- Elastic channels that upload in file mode now stage data under the durable stage location when the server provides it, so elastic file-mode uploads receive the durable TTL. Non-elastic channels are unchanged.

## Version 1.6.1 (June 29, 2026)

### New features and updates

- Added support for sending the `oauth_scope` parameter on IdP token requests when using OAuth, with role fallback behavior for compatibility.

### Bug fixes

- Fixed transitive Rust dependencies to resolve CVEs.

## Version 1.6.0 (June 18, 2026)

### New features and updates

- The Snowpipe Streaming SDK for Node.js `appendRow` and `appendRows` methods are now synchronous, aligning the Node.js API with the Java and Python SDKs. This is a breaking change for Node.js applications. For more information, see the [Node.js API reference](/user-guide/snowpipe-streaming-sdk/reference/nodejs/index.html).
- Added the `SS_LOG_TARGET` environment variable to redirect SDK logs to `stderr`.
- The SDK now logs a warning when concurrent `appendRow` or `appendRows` calls are detected on the same channel, helping surface incorrect single-writer usage.
- On Windows, the SDK now uses the mimalloc memory allocator to reduce memory fragmentation under sustained streaming workloads, matching the jemalloc-based approach on Linux and macOS.

## Version 1.5.0 (May 20, 2026)

### New features and updates

- Added the `application` client property and `SS_APPLICATION` environment variable for partner CSID attribution. Partners and integrators can now identify their application to Snowflake for usage tracking and support. For more information, see [Configurations for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations).
- The SDK now uses the jemalloc memory allocator on Linux and macOS to reduce memory fragmentation under sustained streaming workloads. The change is automatic; no configuration is required. Windows builds continue to use the system allocator. For more information, see [Best practices for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-best-practices).
- Enabled FIPS 140-3 validated cryptography for TLS and data encryption. The SDK now uses AWS-LC as its cryptographic provider and enforces HTTPS-only connections to Snowflake. For more information, see [Configurations for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations).
- Added support for running the SDK inside Snowpark Container Services (SPCS). The SDK reads the SPCS workload identity token automatically and authenticates without long-lived credentials in the container. For more information, see [Run the Snowpipe Streaming SDK in Snowpark Container Services](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-spcs).
- Released the Snowpipe Streaming SDK for Node.js v1.5.0 on [npm](https://www.npmjs.com/package/snowpipe-streaming) with the same updates as the Java and Python SDKs.

For links to the official SDK packages for each supported language, see [How to connect](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview#how-to-connect).

## Version 1.4.0 (May 08, 2026)

### New features and updates

- The Snowpipe Streaming SDK for Node.js is now generally available. The SDK brings the Snowpipe Streaming high-performance architecture to JavaScript and TypeScript applications, and shares the same Rust-based client core as the Java and Python SDKs. Install from [npm](https://www.npmjs.com/package/snowpipe-streaming), and see the [Node.js API reference](/user-guide/snowpipe-streaming-sdk/reference/nodejs/index.html). The Node.js SDK requires Node.js 20 or later and runs on ARM64 Mac, Windows, ARM64-Linux, and x86\_64-Linux (glibc 2.26 or later).
- Added support for OAuth authentication. You can now set `authorization_type` to `OAUTH` and connect to Snowflake using OAuth (Snowflake OAuth or External OAuth, including the refresh-token and client-credentials flows). For configuration details, see [Configurations for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations).
- Added support for programmatic access token (PAT) authentication. You can now set `authorization_type` to `PAT` and provide a `personal_access_token` to connect to Snowflake using a long-lived programmatic access token.
- Binary column encoding now follows the effective `BINARY_INPUT_FORMAT` parameter for custom pipes. The SDK fetches the effective format through the pipe-info API at client creation and encodes byte arrays accordingly. Default pipes always use `BASE64` for binary columns, independent of account-level or session-level parameters. If the effective `BINARY_INPUT_FORMAT` changes during a session, the SDK invalidates the client and you must close and reopen it. For more information, see [The PIPE object](/user-guide/snowpipe-streaming/snowpipe-streaming-pipe-object).
- The `appendRows` method now accepts a `startOffsetToken` in addition to the existing end offset token, letting you record the offset range covered by each batch. For single-row appends, the SDK uses the same token for both bounds. The start offset is recorded as `offset_token_lower_bound` in error-table metadata, making it easier to locate the source range that produced an erroneous row. For more information, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
- When reopening a channel that has uncommitted in-flight data, the SDK now requests the server to reject the reopen until that data commits, retrying for up to 120 seconds before falling back to a force-reopen. To get the same protection when calling the REST API directly, pass `fail_on_uncommitted_rows=true`. For more information, see [Snowpipe Streaming REST API endpoints](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api).

## Version 1.3.0 (March 12, 2026)

### New features and updates

- Maintenance and stability release. Updates to release tooling and minor internal improvements. See the [Maven Central release page](https://repo1.maven.org/maven2/com/snowflake/snowpipe-streaming/) for the artifact.

## Version 1.2.0 (February 16, 2026)

### New features and updates

- Added support for encrypted key-pair authentication. You can now connect to your instances by using both encrypted and unencrypted private keys, providing greater flexibility for your security workflows.

## Version 1.1.2 (January 20, 2026)

### Behavior changes

- Fixed a race condition in the channel status cache to improve multi-threaded stability.
- Reduced log flooding by removing redundant messages for cleaner monitoring.

### New features and updates

- Added support for account locators with region suffixes.

### Bug fixes

- Removed unused configuration parameters and addressed minor internal logic issues to improve reliability.
