# .NET Driver release notes for 2024

This article contains the release notes for the .NET Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for .NET Driver updates.

See [.NET Driver](/developer-guide/dotnet/dotnet-driver) for documentation.

## Version 4.2.0 (November 05, 2024)

### New features and improvements

- Added a [signature on the driver package](https://github.com/snowflakedb/snowflake-connector-net/blob/43924472903467ad741f8d1ea3ee777c02e21829/README.md#verifying-the-package-signature) to verify its authenticity and integrity.
- Added support for reading vector types.
  For more information, see [VectorType.md](https://github.com/snowflakedb/snowflake-connector-net/blob/d69e2cb42ebd0f076476b979dcd249a0470f4e71/doc/VectorType.md).
- Added support for reading structured types for the JSON result format.
  For more information, see [StructuredType.md](https://github.com/snowflakedb/snowflake-connector-net/blob/d69e2cb42ebd0f076476b979dcd249a0470f4e71/doc/StructuredTypes.md).
- Added logging for the client environment configuration.
- Implemented `SnowflakeDbDataReader.GetEnumerator()`.

### Bug fixes

- Changed the `SnowflakeDbConnection` finalizer to be non-blocking.
- Fixed an issue where some disposable objects were not properly disposed.
- Improved memory management for reading large query results.
- Increased the log level of messages for failed HTTP responses.
- Stopped retrying non-recoverable authentication exceptions.
- Fixed a concurrency issue with initializing a connection pool.
- Changed `DateTime.Kind` to `Unspecified` for reading DATE, TIME and TIMESTAMP\_NTZ Snowflake types.
  Version 2.1.3 of the driver introduced an undesired change of setting the `DateTime.Kind` to `Utc`.
- Fixed null response handling for PUT/GET operations in the GCS client.
- Fixed exception handling for PUT/GET operations in the S3 client.
- Fixed very large or very small timestamps handling.
- Improved the logic for calculating when the next retry will happen.
- Fixed the returning rows count for COPY statements from multiple files.
- Fixed support of PUT/GET files without client side encryption.

## Version 4.1.0 (August 05, 2024)

### New features and improvements

- Added log messages about the domain destination to which the driver is connecting.
- Updated `DbCommand.Prepare()` to do nothing instead of throwing an exception.

### Bug fixes

- Fixed a issue where a cancel exception was lost when canceling a `OpenAsync` operation.

## Version 4.0.0 (July 08, 2024)

### BCR (Behavior Change Release) changes

Beginning with version 4.0.0, the .NET driver introduced the following breaking changes:

- Connection pool behavior changes:

  - The driver now uses separate pools for each unique connection string. Previously, the driver use only one pool for all connection strings.
  - The `maxPoolSize` parameter change:

    - Previously, it represented the number of connections to store in the pool. Now it defines the maximum number of connections allowed to open for a given pool (for each unique connection string there is a different pool so you can set it differently for each of them).
    - If `maxPoolSize` is reached, the thread requesting a new connection waits until any connection from the pool is available to reuse without exceeding the limit. An exception is thrown in case of a timeout.
    - You can configure the waiting time in the connection string by setting the `waitingForIdleSessionTimeout` property. The default value for the timeout is 30 seconds. You can change it to 0 to disable waiting.
    - The default value for `maxPoolSize` is 10. Make sure your `maxPoolSize` value is properly set for your needs to avoid hanging your threads or timeout exceptions.
    - The `maxPoolSize` property should be greater than or equal to `minPoolSize`.
  - Added a new `minPoolSize` parameter with a default value of 2 that makes the driver open two connections (the second one in background) when you open the first connection for a given connection string. You can set this value to 0 in the connection string if you want to disable the `minPoolSize` feature.
  - The configuration of the pool has been changed to a connection string driven approach. All properties that control the connection pool behavior can be now passed in the connection string. It is no longer possible to set connection pool properties by `SnowflakeDbConnectionPool` setters, such as `SnowflakeDbConnectionPool.SetTimeout`, `SetPooling`, or `SetMaxPoolSize`. Using `SnowflakeDbConnectionPool` setters now throws exceptions.
  - Previously, connections that altered the database, schema, role, or warehouse (for example, by executing the ALTER SESSION SET command) parameters, were pooled. The new default behavior for such cases destroys altered connections when closing does not return them to the pool. If you want to use altered connections in the pool you need to add `ChangedSession=OriginalPool` to your connection string.
  - Connections with external browser authentication or, some cases of KeyPair/JWT token authentication, are no longer stored in the pool by default. To enable pooling such connections you must add `poolingEnabled=true` to the connection string. For other authentication methods pooling is enabled by default.
  - For more information about using connection pool, see [Using Connection Pools](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/ConnectionPooling.md).
- `NONPROXYHOSTS` parameter behavior change:

  The behavior for `NONPROXYHOSTS` parameter has changed. Previously a host would not be proxied if its name contained the value specified in this parameter. Now the host is not proxied when it is exactly the value specified in the parameter. For instance, previously `NONPROXYHOSTS=c` would match any host containing “c”, such as “your-account.snowflakecomputing.com” as well. After the change, you have to specify the whole host, such as `NONPROXYHOSTS=your-account.snowflakecomputing.com`, to make it non-proxied.

### New features and improvements

- Changed connection pool behavior with multiple pools (one per each unique connection string) and connection string driven configuration. For more information about using connection pool, see [Using Connection Pools](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/ConnectionPooling.md).
- Targeting to .netstandard 2.0.
- Added a strong name signature to the driver assembly.
- Added ability to set the `QueryTag` parameter in the connection string and on the `SnowflakeDbCommand` object to mark the connection and command queries with a tag.
- Bumped the `BouncyCastle.Cryptography` dependency.
- Bumped the `Google.Cloud.Storage.V1` dependency.
- Introduced a new `DISABLE_SAML_URL_CHECK` parameter that disables checking if the SAML postback URL matches the host URL when authenticating with Okta.

### Bug fixes

- Fixed the handling of date and time values passed with bindings for queries with very large amount of bindings (more than `CLIENT_STAGE_ARRAY_BINDING_THRESHOLD`).
- Fixed sending SQL queries to the server by sending original queries instead of trimmed queries that resulted in errors for queries ending with comments.
- Implemented a more reliable way of providing hosts in `NONPROXYHOSTS` parameter.
- Fixed support of double quotes in DB, SCHEMA, WAREHOUSE, ROLE connection string parameters.
- Fixed S3 clients by adding “<https://>” to `ServiceUrl` if it is missing.
- Updated the secret detector to better mask secrets when logging.
- Added setting a proper `SnowflakeDbParameter.DbType` value.
- Fixed the logic of shortening the `connectionTimeout` by `retryTimeout` in case of an infinite `retryTimeout` value.
- Applied the logic of increasing `maxHttpRetries` to the default value for HTTP clients. Previously it was applied only to Okta authentication.

## Version 3.1.0 (March 27, 2024)

### New features and improvements

- Added support for running asynchronous queries.

### Bug fixes

- Improved exceptions thrown from the Okta authenticator.
- Fixed an issue with validating very short (1-2 character) account names.
- Fixed an issue related to retrieving the `WAREHOUSE` property from a connection string with quoted content, such as `"WAREHOUSE=\"two words\""`.

## Version 3.0.0 (February 29, 2024)

### BCR (Behavior Change Release) changes

- To enhance security, the driver no longer searches a temporary directory for easy logging configurations. Additionally, the driver now requires the logging configuration file on Unix-style systems to limit file permissions to allow only the file owner to modify the files (such as `chmod 0600`, `chmod 0644`).
- The driver now throws a `SnowflakeDbException` with a `QueryID` for PUT/GET failures. Previously, the driver returned different types of exceptions, such as `FileNotFound` and `DirectoryNotFound`. If your application checked for any of these exceptions, you must update your code to handle only `SnowflakeDbException` for PUT/GET failures.
- The driver no longer supports older versions, such as V1 and V2, of the chunk parser/downloader. As part of the upgrade to version V3, the driver no longer supports the `SFConfiguration.UseV2JsonParser` or `SFConfiguration.UseV2ChunkDownloader` configuration options. If you used commands similar to the following, you should remove them:
  - `SFConfiguration.Instance().ChunkParserVersion = 1;` or `SFConfiguration.Instance().ChunkParserVersion = 2;`
  - `SFConfiguration.Instance().ChunkDownloaderVersion = 1;` or `SFConfiguration.Instance().ChunkDownloaderVersion = 2;`
  - `SFConfiguration.Instance().UseV2JsonParser`
  - `SFConfiguration.Instance().UseV2ChunkDownloader`

### New features and improvements

- Added support for multiple SAML integrations.

### Bug fixes

- Improved security in the easy logging feature, including:

  - Using a more reliable way of determining which driver directory to use when searching for client configuration files.
  - No longer using a temporary directory for configuration search.
  - Enforcing additional file permissions checks under Unix for increased security.
  - Adding more verbose logging.
- Fixed an Okta retry issue for SSO/SAML endpoints.
- Added fast failing for commands without text execution.
- Fixed exceptions thrown from PUT/GET failed executions to contain `QueryId` if possible.
- Replaced the `Portable.BouncyCastle` library with `BouncyCastle.Cryptography`.

## Version 2.2.0 (January 17, 2024)

### BCR (Behavior Change Release) changes

- Beginning with version 2.2.0, the .NET driver automatically replaces underscores (`_`) in account names with hyphens (`-`) when constructing a host name based on an account name. This change impacts PrivateLink customers whose account names contain underscores. In this situation, you must override the default value by setting `allowUnderscoresInHost` to `true`. You can override this behavior by setting `allowUnderscoresInHost=true` in the `ConnectionString`.

  This change was made to fix the DNS resolution errors that occurred when connecting over the public link with Snowflake accounts that had underscores in their account names.

### New features and updates

- Improved Arrow performance.
- Automatically replaces underscores (`_`) in account names with hyphens (`-`) when constructing a host name based on an account name.
- Added an `allowUnderscoresInHost` configuration parameter to allow underscores (\_) in account names to be maintained in the constructed host name. This parameter lets you override the behavior change associated with this release.

### Bug fixes

- To fix an issue with connection timeouts, the driver now closes expired sessions asynchronously when connecting.
