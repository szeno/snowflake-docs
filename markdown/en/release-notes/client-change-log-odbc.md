# ODBC Driver Change Log (Prior to January 2022)

This topic lists the fixes, enhancements, and other changes introduced across all released, production versions of the Snowflake [ODBC Driver](/developer-guide/odbc/odbc) prior to January 2022.

See the  [release notes](/release-notes/clients-drivers/odbc) for current release note and change log information from January 2022 and later.

Note that this list does not include all changes made to the driver; it only lists significant changes or changes that may impact your usage.

In addition, this list is updated independently from the ODBC driver releases and, therefore, may not include the most recently-released version. To
see all available versions, go to the [ODBC Download](https://developers.snowflake.com/odbc/) page.

| Version | Change | Description |
| --- | --- | --- |
| **ODBC Driver 2.24.4** |  |  |
|  |  | Fixed an issue with arrow that occurred when using ODBC\_TREAT\_DECIMAL\_AS\_INT. |
|  |  |  |
| **ODBC Driver 2.24.3** |  |  |
|  |  | Added the MapToLongVarchar property. |
|  |  | Updated the OpenSSL version from 1.1.1k to 1.1.1l. |
|  |  | Updated the curl version from 7.74.0 to 7.78.0 |
|  | SNOW-30433 | Fixed a issue to add retry on invalid arrow chunks. |
|  |  | Fixed an issue to remove retry on HTTP 403 errors. |
|  |  |  |
| **ODBC Driver 2.24.2** |  |  |
|  |  | Added the UseCurrentCatalog connection parameter. |
|  | SNOW-464077 | Fixed a bug in stage binding related to timestamps. |
|  | SNOW-452624 | Fixed installer registry issues. |
|  |  | Performance improvement. |
|  | SNOW-452032 | Replaced invalid UTF-8 characters returned from the server. |
|  | SNOW-366898 | Added additional checks to prevent potential crash issues. |
|  | SNOW-279670 | Add test button on DSN dialog. |
|  |  |  |
| **ODBC Driver 2.24.1** |  |  |
|  |  | Added fast fail and maximum retry support to the GET command for ODBC. |
|  | SNOW-395216 | Added telemetry for unsupported APIs. |
|  |  | Fixed a bug with empty binary data in JSON format. |
|  |  | Added a warning message when an invalid key is passed to a connection string. |
|  |  | Fixed an issue with the default location of the CA Bundle file on Windows. |
|  |  | Fixed a bug where multiple statements beginning with a CALL stored procedure caused a crash. |
|  |  |  |
| **ODBC Driver 2.24.0** |  |  |
|  |  | Updated the minimum supported version of MacOS from 10.13 to 10.14. |
|  |  | Fixed an issue where Arrow crashed when calling the ValueOrDie() function. |
|  |  | Fixed an issue related to parameter array binding. |
|  | SNOW-373871 | Added PUT/GET support when connecting to a FIPS enabled endpoint. |
|  | SNOW-227282 | Added the ability for Telemetry to record the number of result rows consumed by an application. |
|  |  |  |
| **ODBC Driver 2.23.3** |  |  |
|  | SNOW-293206 | Added ability to return argument names from SQLProcedureColumns(). |
|  |  | Added option to set PUT\_COMPRESSLV as a connection / configuration parameter. |
|  |  | Fixed an issue with the UPDATE/DELETE/INSERT statements where parameter array binding failed in some cases. |
|  |  | Fixed an issue where DEFAULT\_VARCHAR\_SIZE and DEFAULT\_BINARY\_SIZE did not work with SQLColumn(). |
|  |  | Added support for streaming values for the bind variables SQLParamData() and SQLPutData(). |
|  | SNOW-355132 | Added feature to make CURLOPT\_MAXAGE\_CONN configurable. |
|  |  | Fixed an issue where arrow chunk downloading caused a crash. |
|  |  | Upgraded OpenSSL from 1.1.1i to 1.1.1k. |
|  | SNOW-350996 | Changed behavior so that the PUT command does not retry when the file being processed already exists in the stage. |
|  |  | Fixed an issue where AWS logging caused a crash when using multiple threads. |
|  |  |  |
| **ODBC Driver 2.23.2** |  |  |
|  | SNOW-293206 | Added support for SQLProcedureColumns. |
|  |  | Fixed a bug with SQLColumns() and the GEOGRAPHY data type. |
|  | SNOW-291407 | Added connection / configuration parameters for specifying the default sizes of BINARY and VARCHAR columns when the column size is undetermined. |
|  |  | Improved performance when using TRACING=6. |
|  |  | Improved the performance of the secret detector. |
|  |  | Improvements for log settings. |
|  |  | When the ODBC version is 3 or higher, the ODBC Driver now uses SQL\_TYPE\_DATE, SQL\_TYPE\_TIME and SQL\_TYPE\_TIMESTAMP as the data types of date, time and timestamp. |
|  | SNOW-334403 | ODBC now generates regional url for aws us-east-1. |
|  |  |  |
| **ODBC Driver 2.23.1** |  |  |
|  | SNOW-249530 | Updated the driver to send only supported statements in SQLPrepare (including SELECT, DML, and SHOW statements). Prior to this change, if a statement was not supported in SQLPrepare (e.g. BEGIN, SET, or COMMIT), the driver would send the statement in SQLPrepare, and the server would return an error. |
|  | SNOW-269456 | Fixed a null pointer issue with timestamps. |
|  |  | Escaped unsafe characters in parameters in the connection string. |
|  |  | Added a configuration / connection parameter for specifying the temporary directory for PUT commands. |
|  |  | Captured the use of the session context in the telemetry. |
|  | SNOW-282587 | Without a sqlfetch the query is canceled. |
|  |  |  |
| **ODBC Driver 2.23.0** |  |  |
|  | SNOW 194654 | Added support for caching MFA tokens. |
|  | SNOW-239674 | Updated the driver to capture escape characters in telemetry. |
|  |  | Set a default value for the CA certificate bundle file name. |
|  |  | Update the driver to free up memory when downloading chunks of results in Arrow format . |
|  | SNOW-274791 | Updated the driver to prevent overscoping when listing foreign keys. |
|  | SNOW-295726 | Added a secret detector and masking module. |
|  | SNOW-278585 | Added support for using the Arrow data format for transferring data to Snowflake. |
|  |  |  |
| **ODBC Driver 2.22.5** |  |  |
|  | SNOW-219403 | Added support for specifying the PUT\_FASTFAIL and PUT\_MAXRETRIES parameters in the simba.ini file. |
|  | SNOW-215983 | Added support for unicode in folder names in PUT / GET statements. |
|  | SNOW-275777 | Updated the driver to use JSON format for Win32 applications when exchanging data with Snowflake. |
|  | SNOW-269456 | Upgraded the version of Arrow to 0.17.0. |
|  | SNOW-78018 | Updated the driver to return the query Id for a successful ODBC call that executes the PUT/GET command. |
|  |  |  |
| **ODBC Driver 2.22.4** |  |  |
|  | SNOW-218025 | Caught exception during the heartbeat sync, which prevents crashes during large (10G) uploads. |
|  | SNOW-240901 | Added Security Verification for Query Texts. |
|  | SNOW-218019 | Updated the telemetry payloads. |
|  | SNOW-195691 | Added support for the ODBC SQLProcedures() function. |
|  | SNOW-231762 | Fixed error with recognizing multi-statements. |
|  |  |  |
| **ODBC Driver 2.22.3** |  |  |
|  | SNOW-219403 | Added support for configurable parameters to enable fast fail and specify the maximum number of retries for PUT command failures. |
|  | SNOW-197194 | Improved the error message for ODBC SSL Certificate failures. |
|  | SNOW-201816 | Reverted a change that overwrote proxy configurations that were set in environment variables. |
| **ODBC Driver 2.22.2** |  |  |
|  | SNOW-199839 | Added inband telemetry when the PUT command fails. |
|  | SNOW-200183 | Added the EnablePidLogFileNames configuration parameter, which causes different processes to generate separate log files. |
|  | SNOW-201047 | Added exceptions for unsupported features to inband telemetry. |
|  | SNOW-201816 | Fixed a problem where the proxy details could not be cleared after being set in the ODBC driver. |
|  | SNOW-204142 | When enabled, SQL\_DESC\_TYPE\_NAME returns the GEOGRAPHY type when GEOGRAPHY\_OUTPUT\_TYPE is GeoJSON (not (E)WKT or (E)WKB). |
|  | SNOW-209045 | Fixed a problem where a crash occurred with concurrent connections. |
|  | SNOW-213639 | Fixed ODBC bulk array binding errors that occurred when parsing data in DATE format. |
| **ODBC Driver 2.22.1** |  |  |
|  | SNOW-170804 | Addressed a security vulnerability finding for util-linux-v2.33.1. |
|  | SNOW-170805 | Addressed a security vulnerability finding for openssl-OpenSSL\_1\_1\_1b. |
|  | SNOW-177073 | Send inband telemetry objects for metadata API calls. |
|  | SNOW-178485 | Addressed a security vulnerability finding for openssl-1.1.1b-v1.1.1b. |
|  | SNOW-197540 | Added metadata to the telemetry for derived ODBC Show commands. |
| **ODBC Driver 2.22.0** |  |  |
|  | SNOW-170120 | Added the configuration parameter EnableAutoIpdByDefault to override the default value of SQL\_ATTR\_ENABLE\_AUTO\_IPD. |
|  | SNOW-181235 | Addressed a connection glitch introduced in version 2.21.8. |
|  | SNOW-183721 | Updated the CACert Bundle in ODBC Drivers. |
|  | SNOW-184163 | Improved PUT performance by using /dev/urandom as the default device. |
|  | SNOW-187198 | Fixed support for the CLIENT\_MEMORY\_LIMIT parameter, which is used as a max memory limit for Chunk downloading. |
|  | SNOW-187534 | Masked signatures in GCP URLs in logs. |
| **ODBC Driver 2.21.8** |  |  |
|  | SNOW-160149 | set Min version of ODBC to receive Arrow result set. |
|  | SNOW-170279 | Add usage stats of SqlPrepare Defer execution stats to CLIENT\_ENVIRONMENT. |
|  | SNOW-175663 | Enable MULTI STATEMENT Support for ODBC on server side. |
|  | SNOW-175667 | Increase the PUT threshold value on the server side to 200MB |
|  | SNOW-177137 | Added new parameter named UseURandomDevice that changes the driver to use /dev/urandom instead of /dev/random. |
| **ODBC Driver 2.21.7** |  |  |
|  | SNOW-101559 | Fixed issue where PUT command with slashes did not work as documented. |
|  | SNOW-156582 | Fixed the following error that occurred when uploading a file into AWS S3 internal stage using PUT command:`AwsSdk::AWSClient::: No response body. Response code: 404`. |
|  | SNOW-159839 | Fixed issue with reading and writing data containing an em-dash when using the latest Snowflake ODBC driver with Informatica Cloud Services. |
|  | SNOW-162610 | Performance improvements for using PUT commands with internal stages. |
|  | SNOW-163154 | Fixed issue where PUT commands failed when no file extension was specified. |
|  | SNOW-163664 | Fixed issue for Private Preview feature. |
|  | SNOW-165820 | Fixed issue where PUT commands did not upload files without returning errors. |
|  | SNOW-168900 | Fixed issue where the driver continued to open connections to localhost when successive PUT commands were issued; this caused excessive TCP connections (in 3rd-party connectors for Attunity and Razorsql). |
|  | SNOW-169965 | Added Logging level to client environment telemetry. |
|  | SNOW-170115 | For Windows, fixed issue where PUT commands failed even when an escape character was provided and delimited using single quotes. |
|  | SNOW-170233 | Fixed issue where PUT / GET commands fail when paths use forward slashes. |
| **ODBC Driver 2.21.6** |  |  |
|  | SNOW-135244 | For Windows, fixed issue where `externalbrowser` authentication was not working properly. |
|  | SNOW-143536 | Added the `NoExecuteInSQLPrepare` parameter to enable controlling how DDL statements are handled in `SQLPrepare` and `SQLExecute`. |
|  | SNOW-158500 | Fixed issue where queries executed with the driver showed failing DESCRIBE\_QUERY results; related to the fix for SNOW-143536. |
|  | SNOW-160829 | Fixed performance issue caused by driver not picking up schema/database. |
| **ODBC Driver 2.21.5** |  |  |
|  | SNOW-45633,   SNOW-144591 | Support added for bulk array binding. |
|  | SNOW-75496 | For Snowflake accounts hosted on GCP, support added for PUT and GET commands. |
|  | SNOW-165067 | Security fix. |
| **ODBC Driver 2.21.4** |  |  |
|  | N/A | Version is not available for download; all fixes are available in 2.21.5 (and higher). |
| **ODBC Driver 2.21.3** |  |  |
|  | SNOW-136211 | Implemented Arrow Bulk fetch. |
|  | SNOW-157756 | Notarized mac package. |
| **ODBC Driver 2.21.2** |  |  |
|  | SNOW-52894,   SNOW-152727,   SNOW-152768,   SNOW-153310 | Fixed issues related to GA of secure SSO ID tokens to support browser-based SSO (for Windows and macOS only). |
|  | SNOW-140235 | Fixed issue where using `yum` to upgrade the driver to a new version deleted the driver RPM, which caused the upgrade to fail. |
|  | SNOW-147376 | Fixed issue where OOB (Out Of Band) Telemetry did not capture connections if curl code was not set to `CURL_OK`. |
|  | SNOW-150687 | Fixed the following session expiration error for long running queries: `"GS error code=390112, GS error message=Your session has expired. Please login again"` |
|  | SNOW-151169 | Upgraded curl to 7.68.0. |
| **ODBC Driver 2.21.1** |  |  |
|  | SNOW-139254 | Internal enhancement. |
|  | SNOW-147190 | Removed unnecessary `{"message":"Limit Exceeded"}` error message from displaying in output buffer. |
|  | SNOW-147420 | Fixed issue that caused a driver failure when a property in the connection string was too long. |
|  | SNOW-148261 | Fixed issue with incorrect Heartbeat endpoint that caused the CLIENT\_SESSION\_KEEP\_ALIVE parameter to fail if set to true; this was a regression introduced in version 2.20.5. |
| **ODBC Driver 2.21.0** |  |  |
|  | SNOW-75961 | Set ODBC SQL\_ATTR\_ENABLE\_AUTO\_IPD default value to true, which reverts the default value change introduced in version 2.20.0 of the driver. |
|  | SNOW-120324 | For macOS and Windows, implemented additional updates to support secure SSO ID tokens (preview feature). |
|  | SNOW-137581 | For Linux, implemented guarding of `getaddrinfo()` with `mutex` in `libcurl`; also introduced `ForceLockGetaddrinfo` parameter in ODBC configuration settings to fix segmentation fault when application is not pthread compatible. |
|  | SNOW-139281 | For Linux, disabled SSO ID token cache. |
|  | SNOW-141543 | Fixed issue with rendering of results for LIST and REMOVE commands. |
|  | SNOW-141622 | Updated SSO ID token secure storage to make it ODBC-specific, rending it inaccessible to other drivers. |
| **ODBC Driver 2.20.5** |  |  |
|  | SNOW-120324 | For macOS and Windows, added support for secure SSO ID tokens (preview feature); this enables applications to use browser-based SSO while minimizing the number of authentication popups when connecting to Snowflake. |
|  | SNOW-123641 | Added support for multi-threading in the driver to implement thread-safety in Snowflake native objects. |
|  | SNOW-134689 | Increased multi-part upload threshold to 64MB for PUT commands. |
|  | SNOW-139112 | Fixed potential security issue due to raw message logging. |
| **ODBC Driver 2.20.4** |  |  |
|  | SNOW-121054 | Reduced unnecessary calls to `ALTER SESSION SET AUTOCOMMIT=TRUE`. |
| **ODBC Driver 2.20.3** |  |  |
|  | SNOW-124921 | Merged partner code changes to implement partner requests and fix reported issues. |
|  | SNOW-126811 | Changed the behavior of the PUT command that skips file upload if the file exists in the stage and no overwrite option is set. |
| **ODBC Driver 2.20.2** |  |  |
|  | SNOW-91853 | Fixed issue where system locale takes precedence over any locale settings in the driver. |
|  | SNOW-110240 | For Linux and Snowflake accounts hosted on Azure, fixed segmentation violation error that occurred when using PUT with SAS. |
|  | SNOW-115888 | For Windows and Snowflake accounts on Azure, fixed issue that occurred with large file uploads when using PUT. |
|  | SNOW-121236 | (Corrected: it appears that this was a false alarm, and is no longer an issue for the customer.) Fixed issue where CLIENT\_METADATA\_REQUEST\_USE\_CONNECTION\_CTX and CLIENT\_SESSION\_KEEP\_ALIVE parameters could not be set in the ODBC connect string. |
| **ODBC Driver 2.20.1** |  |  |
|  | SNOW-115888 | For Windows, fixed issue with uploading/downloading large files to/from stages in Azure (using PUT/GET). |
|  | SNOW-110240 | Fixed issue that resulted in a segmentation fault on Redhat when uploading files to stages in Azure (using PUT). |
| **ODBC Driver 2.20.0** |  |  |
|  | SNOW-97263 | Implemented the following fixes from Simba, some of which introduced behavior changes:   1. Fix issue with setting DSI\_CONN\_CURRENT\_CATALOG to non-null value; also, implement `SFSemantics` and change the default behavior for it.   2. Set SQL\_DESC\_CASE\_SENSITIVE to false for non-character data types.   3. When using non-existent name or invalid character (e.g. `"`) in filters for catalog functions, return empty result instead of error.   4. Set SQL\_ATTR\_ENABLE\_AUTO\_IPD to false by default to match ODBC specification.   5. Add support for binding SQL\_BIT parameter.   6. Fix incorrect value when binding SQL\_REAL parameter.   7. Support Inf/Nan values when binding SQL\_REAL/SQL\_DOUBLE parameters.   8. Return truncation warning when data retrieval buffer size is smaller than actual data.   9. Support binding parameter with custom data types (SQL\_SF\_TIMESTAMP\_LTZ, SQL\_SF\_TIMESTAMP\_NTZ, SQL\_SF\_TIMESTAMP\_TZ).   10. Provide correct information from `SQLGetInfo(SQL_DATABASE_NAME)` and `SQLGetInfo(SQL_USERNAME)`. |
|  | SNOW-97669 | Fixed issue with SOURCE\_COMPRESSION = GZIP by matching the value case-insensitively. |
|  | SNOW-98456 | Internal enhancement. |
|  | SNOW-100023 | Fixed issue where Azure SDK fails to upload large files from Mac/Windows. |
|  | SNOW-101569 | Replaced `int128` and `uint128` libraries. |
| **ODBC Driver 2.19.16** |  |  |
|  | SNOW-14287 | Fixed Wrong Column Size error for `string` data type in the result set metadata. |
|  | SNOW-86742 | Added client information to the USER-AGENT HTTP header. |
|  | SNOW-90398 | Improved handling of Cache Directory creation errors. |
|  | SNOW-90427 | Fixed issue where `ensureCacheDir` failure was not properly handled in `readOCSPCacheFile()`. |
|  | SNOW-98251 | Fixed performance degradation by removing `CURLOPT_FORBID_REUSE` from `curl` option. |
| **ODBC Driver 2.19.15** |  |  |
|  | SNOW-98251 | Fixed a performance regression introduced in v2.19.10 of the driver. Due to this fix, versions 2.19.10 to 2.19.14 have been removed from distribution and are no longer available for download. |
| **ODBC Driver 2.19.14**   (removed from distribution due to fix in 2.19.15) |  |  |
|  | SNOW-81418 | Added support for `OVERWRITE` option in PUT and GET commands. |
|  | SNOW-91145 | Implemented behavior change for values returned by `SQLTable()` function, based on the table type (`TABLE`, `VIEW`, or `TABLE,VIEW`). |
| **ODBC Driver 2.19.13**   (removed from distribution due to fix in 2.19.15) |  |  |
|  | SNOW-92671 | Fixed issue with duplicate row being inserted by ensuring `requestID` is consistent with expired session. |
| **ODBC Driver 2.19.12**   (removed from distribution due to fix in 2.19.15) |  |  |
|  | SNOW-76184 | Fixed extra space in end-of-timestamp output by introducing `ODBC_USE_STANDARD_TIMESTAMP_COLUMNSIZE=true` where the output size is estimated to be 29 instead of 35. |
|  | SNOW-76710 | Implemented Out-of-Band Telemetry. |
|  | SNOW-90409 | Fixed support for OCSP Fail-open. |
| **ODBC Driver 2.19.11**   (removed from distribution due to fix in 2.19.15) |  |  |
|  | SNOW-80091 | Driver now sends `clientStartTime` and `retryCount` with each `/queries/v1/query-request`. |
|  | SNOW-88346 | Internal change for pending feature. |
|  | SNOW-82846 | Fixed issue where inserting a TIMESTAMP into a STRING data type field via Parameterized insert left-trims the month, day, and time using MS ODBC TEST Tool (`odbcte32.exe`). |
|  | SNOW-90640 | Fixed issue with `CABundleFile` parameter for PUT and GET support. |
|  | SNOW-90246 | Fixed issue with `OCSP_FAIL_OPEN` parameter normalization. |
| **ODBC Driver 2.19.10**   (removed from distribution due to fix in 2.19.15) |  |  |
|  | SNOW-88730 | In Windows, fixed AWS PrivateLink connection issue by adding support for the `CABundleFile` parameter to the connect string. |
|  | SNOW-88853 | Added support for optionally setting application name through the `.ini` file or connect string. |
| **ODBC Driver 2.19.9** |  |  |
|  | SNOW-82352 | Enhanced prepared statements to support queries that start with an open parenthesis. |
|  | SNOW-84995 | Driver now checks the OCSP Response Cert Status before checking the time validity for the cert; this prevents expired REVOKED OCSP responses from failing open. |
|  | SNOW-86966 | Driver now sets empty SERVICE\_NAME if passed from the services layer. |
|  | SNOW-86970 | Replaced insecure CRT functions with secure functions. |
| **ODBC Driver 2.19.8** |  |  |
|  | SNOW-85722 | Driver now checks on the return value for `TlsAlloc()` and calls `TlsFree()` as needed. |
| **ODBC Driver 2.19.7** |  |  |
|  | SNOW-85249 | Fixed an issue where SERVICE\_NAME was not propagated to the services layer. |
|  | SNOW-85264 | Fixed a critical stability issue in OCSP fail-open handling that was introduced in version 2.19.0. Due to this fix, versions 2.19.0 to 2.19.6 have been removed from distribution and are no longer available for download. |
| **ODBC Driver 2.19.6**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-81831 | Driver now uses standard connection fields for global URLs. |
| **ODBC Driver 2.19.5**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-80433 | Fixed issue with PUT commands encountering a data error (e.g. `'LOAD00000001.csv.gz',compression type used: 'GZIP', cause: 'data error'`) due to files with the same name being uploaded in separate, but concurrent sessions. |
| **ODBC Driver 2.19.4**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-67606 | Internal change. |
|  | SNOW-70889 | Updated OCSP hostname/URL for AWS PrivateLink. |
| **ODBC Driver 2.19.3**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-79225 | Internal change for pending feature. |
| **ODBC Driver 2.19.2**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-78624 | Fixed issue with Linux dependency on gcc and g++. |
| **ODBC Driver 2.19.1**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-74552 | For Windows, driver now returns the query ID for a successful ODBC call. |
|  | SNOW-77593 | Improved logging for OCSP fail-open, as well as updated configuration naming from Soft Fail to Fail Open. |
|  | SNOW-77750 | To facilitate downloading the driver automatically/programmatically, the Client Driver Repository now includes a `Latest` directory for each supported OS. The directory is a symlink to the latest version directory. |
|  | SNOW-77781 | Implemented various fixes for issues caused by OCSP fail-open. |
| **ODBC Driver 2.19.0**   (removed from distribution due to fix in 2.19.7) |  |  |
|  | SNOW-73827 | Driver upgraded from SimbaSDK 10.1.11 to 10.1.15. |
|  | SNOW-76151 | Implemented support for OCSP fail-open. |
|  | SNOW-76979 | Updated priority of ways to configure OCSP fail-open. |
|  | SNOW-77160 | Added OCSP\_MODE metric. |
| **ODBC Driver 2.18.4** |  |  |
|  | SNOW-66128 | Driver now supports SERVICE\_NAME. |
|  | SNOW-73120 | Fixed issue with PUT command failing to load file to internal stage. |
|  | SNOW-73304 | Fixed the TIMESTAMP\_LTZ behavior for the driver. |
| **ODBC Driver 2.18.3** |  |  |
|  | SNOW-63521 | Driver upgraded to OpenSSL 1.1.1b. |
| **ODBC Driver 2.18.2** |  |  |
|  | SNOW-39055 | Documented support for defining custom C data types. |
|  | SNOW-60376 | For Windows, fixed issue that prevented changing the installation location from the default. |
| **ODBC Driver 2.18.1** |  |  |
|  | SNOW-56250 | Fixed issue where cancel does not record `requestId`. |
|  | SNOW-64779 | Added BIGINT support to ODBC Data Type table. |
| **ODBC Driver 2.18.0** |  |  |
|  | SNOW-65165 | Driver upgraded to SimbaSDK 10.1. |
| **ODBC Driver 2.17.6** |  |  |
|  | SNOW-60066 | For Mac OS, fixed key pair segfault when extracting public key. |
|  | SNOW-60617 | Added support for setting `APPLICATION` property. |
|  | SNOW-63031 | Driver now invalidates outdated OCSP responses when checking cache hit. |
|  | SNOW-63305 | Improvements for future use. |
| **ODBC Driver 2.17.5** |  |  |
|  | SNOW-62431 | For Snowflake accounts hosted on AWS, support added for PUT and GET commands. |
|  | SNOW-62880 | Support added for loading private key file for key-pair authentication. |
|  | SNOW-62922 | Fixed issue with driver crashing when DB2 ODBC library is also used. |
| **ODBC Driver 2.17.4** |  |  |
|  | SNOW-61962 | Improved the precision for floating point numbers to mitigate precision loss. |
|  | SNOW-62077 | Driver now checks HTTP Response Codes for OCSP Cache Download. |
| **ODBC Driver 2.17.3** |  |  |
|  | SNOW-55056 | Fixed issue caused by including region and cloud platform in `account` parameter in `odbc.ini`. |
| **ODBC Driver 2.17.2** |  |  |
|  | SNOW-52535 | Internal change for pending feature. |
|  | SNOW-58250 | Driver now filters client application names to pass only alphanumeric characters and underscore characters (`_`); all other characters in client application names are ignored. |
|  | SNOW-60207 | Fixed an issue where the warehouse specified in the connection parameters is not set when a session is created by an ID token. |
| **ODBC Driver 2.17.1** |  |  |
|  | SNOW-55036 | Added `request_guid` to all HTTP requests to support better tracing. |
| **ODBC Driver 2.17.0** |  |  |
|  | SNOW-55095 | Internal change for pending feature. |
|  | SNOW-56912 | Changed mapping for BOOLEAN data type from SQL\_INTEGER to SQL\_BIT. |
| **ODBC Driver 2.16.11** |  |  |
|  | SNOW-55003 | For Windows ODBC configuration, changed UID parameter from required to optional, enabling creation of system DSNs without a username. |
| **ODBC Driver 2.16.10** |  |  |
|  | SNOW-45298 | Driver no longer generates incidents for errors caused by user environment. |
| **ODBC Driver 2.16.9** |  |  |
|  | SNOW-40171 | Fixed a memory leak when setting the `autocommit` attribute. |
|  | SNOW-53452 | Internal change for pending feature. |
|  | SNOW-53650 | Internal change for pending feature. |
|  | SNOW-53955 | Fixed the following error: `failed to create a id token cache` |
| **ODBC Driver 2.16.8** |  |  |
|  | SNOW-50766 | Updated driver to enforce virtual host style for S3 URLs. |
|  | SNOW-51436 | Fixed issue with underflow of INTEGER values. |
| **ODBC Driver 2.16.7** |  |  |
|  | SNOW-50618 | Internal change for pending feature. |
|  | SNOW-51002 | Fixed issue introduced in v2.16.4 of the driver, in which numeric values fetched as the FLOAT/DOUBLE data type using the bulk fetch API could return wrong results. |
| **ODBC Driver 2.16.6** |  |  |
|  | SNOW-42835 | For Mac OS, added version number to package file metadata. |
|  | SNOW-49898 | Driver now returns Okta-specific error code when Okta authentication fails. |
| **ODBC Driver 2.16.5** |  |  |
|  | SNOW-49793 | Driver now deletes the OCSP response cache from the memory cache if validity check fails. |
|  | SNOW-49860 | For Mac OS, fixed the default driver manager encoding. |
| **ODBC Driver 2.16.4** |  |  |
|  | SNOW-48678 | Internal change for pending feature. |
| **ODBC Driver 2.16.3** |  |  |
|  | SNOW-44911 | For Windows, fixed issue with non-ASCII character binding. |
| **ODBC Driver 2.16.2** |  |  |
|  | SNOW-44075 | Removed login name requirement when authenticating with an OAuth access token. |
| **ODBC Driver 2.16.1** |  |  |
|  | SNOW-42987 | Added support for WCHAR and WVARCHAR data types to the converter to address Power BI failures in Direct Query mode due to non-ASCII characters. |
|  | SNOW-43215 | Added support for OCSP dynamic cache server for AWS PrivateLink. |
| **ODBC Driver 2.16.0** |  |  |
|  | SNOW-42632 | Enabled the OCSP Cache Server by default. |
|  | SNOW-43021 | Added support for using the DSN proxy parameters and `simba.ini` parameters to override the HTTP\_PROXY, HTTPS\_PROXY, and NO\_PROXY environment variables. |
| **ODBC Driver 2.15.0** |  |  |
|  | SNOW-38487 | For Windows, driver now uses OCSP via OpenSSL instead of WinSSL. |
| **ODBC Driver 2.14.0** |  |  |
|  | SNOW-38487 | For Mac OS, driver now uses cURL 7.58.0 and OpenSSL 1.1.0g to support OCSP revocation check instead of using the preinstalled cURL and SecureTransport. |
|  | SNOW-38487 | For Linux, upgraded cURL 7.54.0 and OpenSSL 1.1.0e to 7.58.0 and 1.1.0g, respectively. |
| **ODBC Driver 2.13.21** |  |  |
|  | SNOW-34055 | Added OS and OS\_VERSION to the session info. |
|  | SNOW-39429 | Added filtering of primary key and foreign keys by connection database and schema if CLIENT\_METADATA\_REQUEST\_USE\_CONNECTION\_CTX session parameter is enabled. |
|  | SNOW-40307 | Fixed incorrect formatting of trailing and leading zeros for numeric data type. |
| **ODBC Driver 2.13.20** |  |  |
|  | SNOW-38487 | For Linux, added OCSP cache server support. |
| **ODBC Driver 2.13.19** |  |  |
|  | SNOW-39883 | Fixed SIGSEGV caused by null pointer reference in base64 encoding. |
| **ODBC Driver 2.13.18** |  |  |
|  | SNOW-39049 | Driver now uses cURL library to retrieve OCSP responses to honor `proxy` config set by environment variable. |
|  | SNOW-39305 | Fixed a segmentation fault that occurred when converting TIMESTAMP to STRING for custom SQL data types (pending feature; not currently enabled). |
| **ODBC Driver 2.13.17** |  |  |
|  | SNOW-38353 | Fixed bulk converter and decimal digits for custom timestamps (pending feature; not currently enabled). |
|  | SNOW-38772 | Driver now honors output format for individual timestamp type. Also returns the value length after conversion. |
| **ODBC Driver 2.13.16** |  |  |
|  | SNOW-36102 | Added a parameter to allow the driver to treat big numbers (i.e. precision over 19) as a string. |
|  | SNOW-37994 | Fixed issue caused by wrong column byte size for VARCHAR type in result set metadata. |
| **ODBC Driver 2.13.15** |  |  |
|  | SNOW-23881 | Added support for custom timestamp formatter (pending feature; not currently enabled). |
| **ODBC Driver 2.13.14** |  |  |
|  | SNOW-34096 | Added support for custom SQL data types (pending feature; not enabled by default) in result set metadata. |
| **ODBC Driver 2.13.13** |  |  |
|  | SNOW-32391 | Fixed an issue that caused large inserts to overflow `rowCount`. |
| **ODBC Driver 2.13.12** |  |  |
|  | SNOW-31347 | Fixed an issue where `SQLDescribeCol` always returned 6 decimal digits (i.e. microseconds) as the precision for TIME and TIMESTAMP data types, regardless of whether the precision was set to a different value. Now, the driver returns the precision, from 0 (seconds) to 9 (nanoseconds), defined for the data type. |
| **ODBC Driver 2.13.11** |  |  |
|  | SNOW-31998 | Added support for SAML 2.0-compliant services/applications for federated authentication by adding the `externalbrowser` option to the `authenticator` connection parameter. |
| **ODBC Driver 2.13.10** |  |  |
|  | SNOW-29705 | Fixed issue where ODBC sessions were not closing properly; now the driver tries to close sessions in the destructor for the ODBC Connection object. |
|  | SNOW-33074 | Added support for `timezone` as a session parameter that can be set in `odbc.ini` for connecting to Snowflake. |
| **ODBC Driver 2.13.9** |  |  |
|  | SNOW-25562 | If `metadata_request_use_connection_ctx` is set to true, the driver now applies the database name to the ODBC API call if the schema name is not null. |
|  | SNOW-31998 | Added support for federated authentication/SSO/ADFS. |
| **ODBC Driver 2.13.8** |  |  |
|  | SNOW-31847 | For Windows, fixed an issue with a `curl failed initialization` error. |
| **ODBC Driver 2.13.7** |  |  |
|  | SNOW-30968 | Added an ODBC driver property to support `noproxy`. |
| **ODBC Driver 2.13.6** |  |  |
|  | SNOW-31211 | For Windows, applied fix for timestamps older than 1970 to dates. |
| **ODBC Driver 2.13.5** |  |  |
|  | SNOW-31211 | For Windows, added internal flag that enables an exception when TIMESTAMP\_LTZ is out of range. By default, 1970-01-01 is quietly used in the event of an error. Previously, 1969-12-31 was returned. |
| **ODBC Driver 2.13.4** |  |  |
|  | SNOW-31211 | For Windows, fixed issue with timestamps older than 1970 not being supported. |
| **ODBC Driver 2.13.3** |  |  |
|  | SNOW-26793 | Added the version number to ODBC packages. |
|  | SNOW-28379 | For Mac OS, changed the namespace used to identify the installation package for the operating system from `com.snowflake.odbc` to `net.snowflake.odbc`. |
|  | SNOW-29592 | For Linux, changed the underlying SSL library from NSS to OpenSSL. No change to ODBC for Mac OS and Windows. |
| **ODBC Driver 2.12.99** |  |  |
|  | SNOW-22240 | Fixed an issue with merge count not adding up. |
|  | SNOW-30586 | Fixed an issue with number conversion in the driver. |
| **ODBC Driver 2.12.98** |  |  |
|  | SNOW-25562 | Added CLIENT\_METADATA\_REQUEST\_USE\_CONNECTION\_CTX session parameter (to filter object names by the current database and schema if not specified). |
| **ODBC Driver 2.12.97** |  |  |
|  | SNOW-28617 | Client package signed with new GPG key (and secret). |
| **ODBC Driver 2.12.96** |  |  |
|  | SNOW-24601 | Implemented security patch for federated authentication. |
| **ODBC Driver 2.12.95** |  |  |
|  | SNOW-28234 | Added CLIENT\_TIMESTAMP\_TYPE\_MAPPING to the list of parameters that can be set in connection properties. |
| **ODBC Driver 2.12.94** |  |  |
|  | SNOW-25540 | Added support for binding timestamp variables as timestamp\_ntz for applications that use the bind API to load data into datetime columns (which are equivalent to the timestamp\_ntz data type). |
|  | SNOW-26451 | Implemented CLIENT\_SESSION\_KEEP\_ALIVE session parameter as a supported connection option. |
| **ODBC Driver 2.12.93** |  |  |
|  | SNOW-26953 | Fixed an issue which caused network disruptions to return an exception. Now, disruptions return a user error instead of an exception. |
| **ODBC Driver 2.12.92** |  |  |
|  | SNOW-26215,   SNOW-26227 | If the client tries to send a delete request to the server for a session that has already expired, the request is ignored. |
| **ODBC Driver 2.12.91** |  |  |
|  | SNOW-25999 | Driver processes SQL\_DECIMAL as SQL\_BIGINT if the scale is set to 0. |
| **ODBC Driver 2.12.90** |  |  |
|  | SNOW-11970 | Improved the resiliency for intermittent network errors when receiving query results. |
| **ODBC Driver 2.12.89** |  |  |
|  | SNOW-22102 | Fixed a potential deadlock when the main application thread waiting for a result chunk, being downloaded by an asynchronous thread, times out. |
|  | SNOW-22351 | Improved memory management for downloading large result sets. |
|  | SNOW-21795,   SNOW-24366,   SNOW-24519,   SNOW-24589 | Improved handling of connection failures and re-establishing a connection. |
| **ODBC Driver 2.12.88** |  |  |
|  | SNOW-22865 | The BulkFetch API is now supported. |
|  | SNOW-23884 | Improved performance on ODBC initial connection. |
| **ODBC Driver 2.12.87** |  |  |
|  | SNOW-18996 | Added support for BINARY data type. |
|  | SNOW-22697 | Improved performance when fetching large result sets. |

Expand

Show lessSee more
