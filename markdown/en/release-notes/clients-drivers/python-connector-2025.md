# Snowflake Connector for Python release notes for 2025

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 4.1.1 (Dec 02, 2025)

### New features and updates

- None.

### Bug fixes

- Relaxed the pandas dependency requirements for Python below 3.12.
- Changed the CRL cache cleanup background task to a daemon thread to avoid blocking the main thread.
- Fixed NO\_PROXY issues with PUT operations.

## Version 4.1.0 (Nov 13, 2025)

### New features and updates

- Added official support for RHEL9 (Red Hat Enterprise Linux 9).
- Added the `oauth_socket_uri` connection parameter to allow users to specify separate server and redirect URIs for local OAuth server.
- Added the `no_proxy` parameter for proxy configuration without using environmental variables.
- Added the `SNOWFLAKE_AUTH_FORCE_SERVER` environment variable to force the driver to receive SAML tokens even without opening a browser when using the `externalbrowser` authentication method. The variable allows headless environments, such as Docker or Airflow) that run locally to authenticate the connection using a browser URL.

### Bug fixes

- Fixed a compilation error when building from sources with libc++.
- Added `OAUTH_AUTHORIZATION_CODE` and `OAUTH_CLIENT_CREDENTIALS` to the list of authenticators that don’t require users to set the `user` parameter.

## Version 4.0.0 (Oct 9, 2025)

### BCR (Behavior Change Release) changes

- Configuration files writable by a group or others now raise a `ConfigSourceError` with detailed permission information, preventing potential credential tampering.
- Reverted changing the exception type in case of token expired scenario for `Oauth` authenticator back to `DatabaseError`.

### New features and updates

- Implemented a new CRL (Certificate Revocation List) checking mechanism.

  Enabling CRLs improves security by checking for revoked certificates during the TLS handshake process. For more information, see the [Replacing OCSP with CRL as the method of certificate revocation checking](https://community.snowflake.com/s/article/Replacing-OCSP-with-CRL-as-the-method-of-certificate-revocation-checking) Knowledge Base article.

  This feature is disabled by default. For information on enabling this feature, see [CertRevocationCheckMode](/developer-guide/python-connector/python-connector-api#label-python-crl-validation-options). We recommend you test this feature in advisory mode before enabling it in production.
- Added the `workload_identity_impersonation_path` parameter to support service account impersonation for Workload Identity Federation. Impersonation is available only for Google Cloud and AWS workloads.
- Added the `oauth_credentials_in_body` parameter to support sending OAuth client credentials in a connection request body.
- Added an option to exclude `botocore` and `boto3` dependencies during installation by setting the `SNOWFLAKE_NO_BOTO` environment variable to `true`. For the full details, see [Installing the Python Connector](/developer-guide/python-connector/python-connector-install).
- Added the `ocsp_root_certs_dict_lock_timeout` connection parameter to set the timeout (in seconds) for acquiring the lock on the OCSP root certs dictionary. The default value is -1, which represents no timeout.

### Bug fixes

- Fixed `get_results_from_sfqid` when using `DictCursor` and executing multiple statements at once.
- Fixed retry behavior for `ECONNRESET` errors.
- Fixed the return type of `SnowflakeConnection.cursor(cursor_class)` to match the type of `cursor_class`.
- Constrained the types of `fetchone`, `fetchmany`, and `fetchall`.
- Fixed the “No AWS region was found” error when AWS region was set in the `AWS_DEFAULT_REGION` variable instead of in `AWS_REGION` for the `WORKLOAD_IDENTITY` authenticator.

## Version 3.18.0 (Oct 6, 2025)

### New features and updates

- Added support for pandas conversion for Day-time and Year-Month Interval types.

### Bug fixes

- None.

## Version 3.17.4 (Sep 22, 2025)

### New features and updates

- Added support for allowing intermediate certificates from the trust store to act as root certificates.
- Updated bundled *urllib3* to version v2.5.0.
- Updated bundled *requests* to version v2.32.5.
- Dropped support for OpenSSL versions older than 1.1.1.

### Bug fixes

- None.

## Version 3.17.3 (Sep 3, 2025)

### New features and updates

- None.

### Bug fixes

- Enhanced configuration file permission warning messages.

  - Improved warning messages for readable permission issues to include clear instructions on how to skip warnings using the `SF_SKIP_WARNING_FOR_READ_PERMISSIONS_ON_CONFIG_FILE` environment variable.
- Fixed the bug with staging pandas dataframes on AWS — the regional endpoint is used when required.

  - This fix addresses the issue with the `create_dataframe` call on Snowpark.

## Version 3.17.2 (August 20, 2025)

### New features and updates

- None.

### Bug fixes

- Added the ability to disable endpoint-based platform detection by setting `platform_detection_timeout_seconds` to zero.
- Fixed a bug where `platform_detection` was retrying failed requests with warnings to non-existent endpoints.

## Version 3.17.1 (August 14, 2025)

### New features and updates

- Added the `infer_schema` parameter to `write_pandas` to perform schema inference on the passed data.

### Bug fixes

- Reverted the `snowflake` namespace back to non-module.

## Version 3.17.0 (August 13, 2025)

### New features and updates

- Added support for workload identity federation in the AWS, Azure, Google Cloud, and Kubernetes platforms.

  - Added the `workload_identity_provider` connection parameter.
  - Added `WORKLOAD_IDENTITY` to the values for the `authenticator` connection parameter.
- Added an `unsafe_skip_file_permissions_check` flag to skip file permission checks on the cache and configuration.
- Added basic JSON support for `Interval` types.
- Added populating of `type_code` in `ResultMetadata` for interval types.
- Relaxed the pyarrow version constraint; versions >= 19 can now be used.
- Introduced the `snowflake_version property` to the connection.
- Added support for the `use_vectorized_scanner` parameter in the `write_pandas` function.
- Added support of proxy setup using connection parameters without emitting environment variables.

### Bug fixes

- Fixed OAuth authenticator values.
- Fixed a bug where a PAT with an external session authenticator was used while `external_session_id` was not provided in `SnowflakeRestful.fetch`.
- Fixed the case-sensitivity of Oauth and `programmatic_access_token` authenticator values.
- Fixed unclear error messages for incorrect authenticator values.
- Fixed GCS staging by ensuring the endpoint has a scheme.
- Fixed a bug where time-zoned timestamps fetched as a `pandas.DataFrame` or `pyarrow.Table` would overflow due to unnecessary precision. A clear error is now raised if an overflow cannot be prevented.

## Version 3.16.0 (July 01, 2025)

### New features and updates

- Added the `client_fetch_use_mp` connection parameter that enables multi-processed fetching of result batches, which usually reduces fetching time.
- Added support for the new Personal Access Token (PAT) authentication mechanism with external session ID.
- Added the `bulk_upload_chunks` parameter to the `write_pandas` function. Setting this parameter to `True` changes the behavior of the `write_pandas` function to first write all the data chunks to the local disk and then perform the wildcard upload of the chunks folder to the stage. When set to `False` (default), the chunks are saved, uploaded, and deleted one by one.
- Added Windows support for Python 3.13.
- Added basic arrow support for `Interval` types.
- Added support for Snowflake OAuth for local applications.

### Bug fixes

- Fixed `write_pandas` special characters usage in the location name.
- Fixed the usage of `use_virtual_url` when building the location for a Google Cloud Storage (GCS) client.

## Version 3.15.0 (April 28, 2025)

### Private Preview (PrPr) features

Added support for workload identity federation in the AWS, Azure, GCP and Kubernetes platforms.

Disclaimer:

- This feature can only be accessed by setting `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use this feature only with non-production data.
- This PrPr feature is not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Added new authentication methods support for OAuth 2.0 Authorization Code Flow, OAuth 2.0 Client Credentials Flow, and OAuth Token caching.
  - For OAuth 2.0 Authorization Code Flow:

    - Added the `oauth_client_id`, `oauth_client_secret`, `oauth_authorization_url`, `oauth_token_request_url`, `oauth_redirect_uri`, `oauth_scope`, `oauth_disable_pkce`, `oauth_enable_refresh_tokens` and `oauth_enable_single_use_refresh_tokens` parameters.
    - Added the `OAUTH_AUTHORIZATION_CODE` value for the parameter authenticator.
  - For OAuth 2.0 Client Credentials Flow:

    - Added the `oauth_client_id`, `oauth_client_secret`, `oauth_token_request_url`, and `oauth_scope` parameters.
    - Added the `OAUTH_CLIENT_CREDENTIALS` value for the parameter authenticator.
  - For OAuth Token caching: Passing a username to driver configuration is required, and the `client_store_temporary_credential property` is to be set to `true`.

### Bug fixes

- Increased the minimum required `boto` and `botocore` versions to 1.24.
- Fixed an issue with OSCP by terminating a certificate’s chain traversal if a trusted certificate was already reached.

## Version 3.14.1 (April 21, 2025)

### Private Preview (PrPr) features

- Added the `client_fetch_threads` experimental parameter to better utilize threads for fetching query results.
- Added new experimental authentication methods:
  - OAuth authorization code and client credentials flows.
  - Workload Identity Federation for AWS, Azure, GCP and Kubernetes platforms.

Disclaimer:

- These features can only be accessed by setting `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use these features only with non-production data.
- These PrPr features are not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Added support for Python 3.13.

  Note

  Windows 64 support is still experimental and should not yet be used for production environments.
- Dropped support for Python 3.8.
- Added support for the basic decimal `floating-point` type.
- Added support for providing a PAT in the `password` field.
- Added support for GCS regional endpoints.
- Added support for GCS virtual URLs. For more information, see [Request endpoints](https://cloud.google.com/storage/docs/request-endpoints#xml-api).
- Added support to allow the connector to inherit a UUID4 generated upstream, provided in statement parameters (field: `requestId`), rather than automatically generate a UUID4 to use for the HTTP Request ID.
- Improved logging in the urllib3, boto3, and botocore libraries to assure data masking even after a future migration to the external owned library.
- Lowered log levels from `info` to `debug` for some of the messages to make the output easier to follow.
- Improved security and robustness for the temporary credentials cache storage.
- Deprecated the `insecure_mode` connection property and replaced it with `disable_ocsp_checks` with the same behavior as the former property.
- Implemented and improved the file-based credentials cache for Linux, including enhanced token caching.

### Bug fixes

- Improved the error message for client-side query cancellations due to timeouts.
- Fixed a bug that caused the driver to fail silently on `TO_DATE` arrow to python conversion when an invalid date was followed by the correct one.
- Added the `check_arrow_conversion_error_on_every_column` connection property that can be set to `False` to restore previous behavior in which driver ignores errors until they occurs in the last column. This option lest you unblock workflows that might be impacted by the bug fix and will be removed in later releases.
- Fixed an issue with expired S3 credentials update and increment retry when expired credentials are found.

## Version 3.14.0 (March 03, 2025)

### New features and updates

- Bumped the pyOpenSSL dependency upper boundary from <25.0.0 to <26.0.0.
- Optimized distribution package lookup to improve import speed.
- Added support for iceberg tables to `write_pandas`.
- Added support for `File` types.

### Bug fixes

- Added a <19.0.0 pin to `pyarrow` as a workaround to a bug affecting Azure Batch.
- Fixed a bug where the privatelink OCSP Cache url could not be determined if the privatelink account name was specified in uppercase.
- Fixed base64 encoded private key tests.
- Fixed a bug with file permission checks on Windows.
- Added the `unsafe_file_write` connection parameter that restores the previous behavior of saving files downloaded with GET with 644 permissions.

## Version 3.13.2 (January 30, 2025)

### New features and updates

- The connector no longer uses scoped temporary objects.

### Bug fixes

- None.

## Version 3.13.1 (January 29, 2025)

### New features and updates

- None.

### Bug fixes

- Hardened the `snowflake.connector.pandas_tools` module against SQL injection. For more information, see [CVE-2025-24793](https://github.com/snowflakedb/snowflake-connector-python/security/advisories/GHSA-2vpq-fh52-j3wv).
- The local OCSP cache has been updated to use the json module instead of pickle to serialize its contents. For more information, see [CVE-2025-24794](https://github.com/snowflakedb/snowflake-connector-python/security/advisories/GHSA-m4f6-vcj4-w5mx).
- The Linux credential cache file permissions have been updated explicitly to be only be owner readable. For more information, see [CVE-2025-24795](https://github.com/snowflakedb/snowflake-connector-python/security/advisories/GHSA-r2x6-cjg7-8r43).
- Updated the file permissions for files downloaded with GET to be readable only by the file owner.

## Version 3.13.0 (January 23, 2025)

### New features and updates

- Added the `iobound_tpe_limit` connection parameter to limit the sizes of IO-bound `ThreadPoolExecutors` during PUT and GET commands. By default, the size is calculated to the lesser of the number of files and the number of CPU cores.
- Added the `Connection.is_valid()` method that verifies whether a connection is stable enough to receive queries.
- Updated the log level for cursor’s chunk `rowcount` from INFO to DEBUG.
- Added support for base64-encoded DER private key strings in the `private_key` authentication type.
- Updated `README.md` to include instructions on how to verify package signatures using `cosign`.

### Bug fixes

- None.
