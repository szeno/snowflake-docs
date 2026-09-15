# Migrating from JDBC Driver 3.x to JDBC Driver 4.x

The JDBC Driver 4.x introduces several new features and improvements over the JDBC Driver 3.x. This topic provides an overview of the public API changes and new features and also provides information about how to migrate from JDBC Driver 3.x to JDBC Driver 4.x.

## Public API overview

The Snowflake JDBC driver public API is located under the `net.snowflake.client.api` package (see [API Reference](https://docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/index.html)). The changes to the public API between JDBC Driver 3.x and JDBC Driver 4.x are listed in the following table:

| Package | Description |
| --- | --- |
| [api.driver](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/driver/package-summary.html) | JDBC driver registration and entry point |
| [api.connection](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/connection/package-summary.html) | Snowflake-specific connection and database metadata interfaces, stream transfer configuration |
| [api.datasource](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/datasource/package-summary.html) | DataSource implementation for creating and managing connections |
| [api.pooling](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/pooling/package-summary.html) | Connection pool data source for applications requiring pooled connections |
| [api.resultset](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/resultset/package-summary.html) | Result set interfaces, field metadata, Snowflake data types, and async query status |
| [api.auth](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/auth/package-summary.html) | Authentication method definitions |
| [api.loader](https://staging.docs.snowflake.com/developer-guide/jdbc/reference/java/v4.0/net/snowflake/client/api/loader/package-summary.html) | Bulk data loading API for high-volume ingestion with progress callbacks |

Expand

Show lessSee more

Additionally, the driver includes classes in the `net.snowflake.client.internal` package that are not part of the public API. These classes are used internally by the driver and are not intended for use by application developers. Use the internal APIs at your own risk: They are subject to change without notice and without backward compatibility guarantees.

## Code changes from JDBC Driver 3.x to JDBC Driver 4.x

### Driver class name changes

The driver class name has changed.

| Before (3.x) | After (4.x) |
| --- | --- |
| `com.snowflake.client.jdbc.SnowflakeDriver` | `net.snowflake.client.api.driver.SnowflakeDriver` |

Expand

Show lessSee more

### Data source creation changes

`SnowflakeDataSource` and `SnowflakeConnectionPoolDataSource` are now interfaces. Use factory classes instead of direct instantiation.

| Component | Factory method |
| --- | --- |
| `SnowflakeDataSource` | `SnowflakeDataSourceFactory.createDataSource()` |
| `SnowflakeConnectionPoolDataSource` | `SnowflakeConnectionPoolDataSourceFactory.createConnectionPoolDataSource()` |

Expand

Show lessSee more

### Stream upload and download changes

The `SnowflakeConnection` interface simplified overloads for stream operations:

- Upload:

  - `uploadStream(stageName, destFileName, inputStream)`
  - `uploadStream(stageName, destFileName, inputStream, UploadStreamConfig)`
  - `UploadStreamConfig` options: `destPrefix`, `compressData` (default: `true`)
- Download:

  - `downloadStream(stageName, sourceFileName)`
  - `downloadStream(stageName, sourceFileName, DownloadStreamConfig)`
  - `DownloadStreamConfig` options: `decompress` (default: `false`)

### `SnowflakeType` changes

The `SnowflakeType` enum has been removed. Type values remain the same, but the enum is no longer supported.

### `QueryStatus` and `SnowflakeAsyncResultSet` changes

Version 4.0.0 made the following changes regarding queries and result sets:

- The `QueryStatus` enum was replaced with DTO (previously known as `QueryStatusV2`). It carries the same data, but in a thread-safe manner. To retrieve query status, unwrap your result set to `SnowflakeAsyncResultSet` and call `getStatus`.
- The `getQueryErrorMessage` on a result set is removed, but it can be retrieved directly from `getErrorMessage` on `QueryStatus`.

If you need an enum value representing the status, call `getStatus` on `QueryStatus`.
