# SnowSQL Change Log (Prior to January 2022)

This topic lists the fixes, enhancements, and other changes introduced across all released, production versions of [SnowSQL](/user-guide/snowsql),
the Snowflake CLI (command-line interface) client prior to January 2022.

See the [Snowflake connector, driver, and library monthly releases](/release-notes/clients-drivers/monthly-releases) for current release note and change log information from January 2022 and later.

Note that this list does not include all changes made to SnowSQL; it only lists significant changes or changes that may impact your usage.

In addition, this list is updated independently from the SnowSQL releases and, therefore, may not include the most recently-released version; to see
all available versions, go to the [SnowSQL Download](https://developers.snowflake.com/snowsql/) page.

| Version | Change | Description |
| --- | --- | --- |
| **SnowSQL 1.2.21** |  |  |
|  | SNOW-480963 | Fixes Python connector bug that Updated URL escaping when uploading to AWS S3 to match how S3 escapes URLs. |
|  |  |  |
| **SnowSQL 1.2.20** |  |  |
|  | SNOW-475359 | Upgrade sqlparse library version from 0.2.3 to 0.4.2. |
|  |  |  |
| **SnowSQL 1.2.19** |  |  |
|  | SNOW-467701 | Added ability to set arbitrary connection parameters in Snowflake connections. |
|  | SNOW-276705 | Make the use of encrypted private key for Key Pair authentication optional. |
|  |  |  |
| **SnowSQL 1.2.18** |  |  |
|  | SNOW-377123 | Added the ability to accept and substitute empty variables, this new behavior is protected by the environmental variable SNOWSQL\_ALLOW\_EMPTY\_ENV\_VARS. |
|  | SNOW-407614 | Changed the behavior of printing unicode characters instead of their escape sequences when using csv format, this new behavior is protected by the environmental variable SNOWSQL\_OUTPUT\_AS\_UNICODE. |
|  |  |  |
| **SnowSQL 1.2.17** |  |  |
|  | SNOW-378268 | Fixes Python Connector bug that prevents the connector from using AWS S3 Regional URL. The driver currently overrides the regional URL information with the default S3 URL causing failure in PUT. |
|  |  |  |
| **SnowSQL 1.2.16** |  |  |
|  | SNOW-365900 | Fix for incorrect JWT token invalidity when an account alias with a dash in it is used for regionless account URL. |
|  |  |  |
| **SnowSQL 1.2.15** |  |  |
|  | SNOW-303944 | Added command-line flags to generate JSON Web Tokens (JWT) in SnowSQL. |
|  |  |  |
| **SnowSQL 1.2.14** |  |  |
|  | SNOW-298813 | Fix for Progress percentage computation to handle the case when file size is zero. |
|  |  |  |
| **SnowSQL 1.2.13** |  |  |
|  | SNOW-270946 | Fix a zero division error while computing progress percentage which gets triggered when the size of file to upload/download is 0. |
|  |  |  |
| **SnowSQL 1.2.12** |  |  |
|  | SNOW-293541 | Released Mac package with renewed Developer Installer Certificate. |
|  |  |  |
| **SnowSQL 1.2.11** |  |  |
|  | SNOW-232777 | The fix to add proper proxy CONNECT headers for connections made over proxies. |
|  |  |  |
| **SnowSQL 1.2.10** |  |  |
|  | SNOW-170647 | Removed an unnecessary dependency. |
| **SnowSQL 1.2.9** |  |  |
|  | SNOW-181011 | Fixed missing dependency for keyring package, which caused issues when connecting using `authenticator = externalbrowser`. |
| **SnowSQL 1.2.8** |  |  |
|  | SNOW-123267 | Support added for forcing quit by pressing **[CTRL]-c** twice. Note that, if you use this option, SnowSQL does not verify previously-started queries were successfully canceled. |
|  | SNOW-159538 | Internal improvement for masking logs for sensitive information. |
| **SnowSQL 1.2.7** |  |  |
|  | SNOW-150710 | Added new custom `sql_delimiter` variable to enable specifying a character other than a semicolon as the delimiter for SQL statements. |
|  | SNOW-170458 | Fixed an issue where SnowSQL failed on multi-line queries, which was caused by a regression introduced in the SnowSQL 1.2.6 internal release. |
| **SnowSQL 1.2.6** |  |  |
|  | N/A | Version is not available for download. |
| **SnowSQL 1.2.5** |  |  |
|  | SNOW-135171 | Updated the SnowSQL distribution to allow specifying the install location. |
|  | SNOW-136164 | Fixed issue where SnowSQL could not be installed if `~/.snowsql` doesn’t exist. |
| **SnowSQL 1.2.4** |  |  |
|  | SNOW-126786 | For Snowflake accounts hosted on GCP, fixed exception when using PUT to upload a file to a stage with `auto_compress=false`. |
|  | SNOW-134305 | Increased threshold to 64MB for multi-part upload to S3. |
| **SnowSQL 1.2.3** |  |  |
|  | SNOW-93304 | Full/main SnowSQL module included in the bootstrap distribution to facilitate offline/hosted installation. |
|  | SNOW-120329 | Added support for OAuth token authentication method. |
| **SnowSQL 1.2.2** |  |  |
|  | SNOW-75495 | Internal change for pending feature. |
|  | SNOW-121787 | Pinned the keyring version to 19.2.0. |
|  | SNOW-122376 | Fixed issue with no content cache for downloading newer version of SnowSQL. |
|  | SNOW-122797 | For MacOS Catalina 10.15.1, fixed `oscrypto` and OpenSSL conflict. |
| **SnowSQL 1.2.1** |  |  |
|  | SNOW-106130 | Added Cask Installer for SnowSQL 1.2.0. |
|  | SNOW-110191 | Enabled `fix_parameter_precedence` connection parameter to `true` for SnowSQL. |
|  | SNOW-118881 | Added .zprofile support to SnowSQL installer. |
| **SnowSQL 1.2.0** |  |  |
|  | SNOW-110647 | Moved upgrade repository from S3 to sfc-repo; original S3 repository is still available for earlier versions. |
| **SnowSQL 1.1.86** |  |  |
|  | SNOW-64718 | Internal change for pending feature. |
|  | SNOW-92738 | Improved SnowSQL installation through `brew cask` for `zshell` users. |
| **SnowSQL 1.1.85** |  |  |
|  | SNOW-94184 | Fixed issue related to Arrow format (internal enhancement). |
| **SnowSQL 1.1.84** |  |  |
|  | SNOW-66323 | Driver now suppresses echo of sensitive data output. |
|  | SNOW-82276 | Removed support for old OCSP URL for AWS PrivateLink. |
| **SnowSQL 1.1.83** |  |  |
|  | SNOW-88844 | Fixed grammatical issues in SnowSQL error message. |
|  | SNOW-89190 | For Snowflake accounts in the US Gov Virginia region (Azure), fixed issue with PUT and GET commands. |
| **SnowSQL 1.1.82** |  |  |
|  | SNOW-82268 | This version of SnowSQL does not use the new OCSP hostname/URL for AWS PrivateLink; the new hostname/URL will be implemented in a future version. |
| **SnowSQL 1.1.81** |  |  |
|  | SNOW-80440 | Fixed an issue where extra linefeed characters were generated when `output_format` was set to `tsv` and a DESCRIBE SCHEMA command was executed on an empty schema. |
| **SnowSQL 1.1.80** |  |  |
|  | SNOW-57024 | Fixed an issue where casting a timestamp earlier than UNIX epoch time added 0.100 seconds to the output. |
| **SnowSQL 1.1.79** |  |  |
|  | SNOW-75465 | Fixed issue with `!SET` indent with comment. |
|  | SNOW-76043 | Added option to skip request pooling. |
|  | SNOW-76797 | Implemented support for OCSP fail-open. |
|  | SNOW-77160 | Added OCSP\_MODE metric. |
| **SnowSQL 1.1.78** |  |  |
|  | SNOW-74395 | Fixed issue with Azure token renewal for long running jobs. |
|  | SNOW-75372 | Enhanced SQL syntax highlighting in the SnowSQL editor. |
| **SnowSQL 1.1.77** |  |  |
|  | SNOW-74042 | Implemented the custom OCSP Cache Server URL in the Python Connector used by SnowSQL. |
| **SnowSQL 1.1.76** |  |  |
|  | SNOW-66025 | Added support for FORCE\_PUT\_OVERWRITE option. |
| **SnowSQL 1.1.75** |  |  |
|  | SNOW-66722 | For Windows, fixed regression for DATE format. |
| **SnowSQL 1.1.74** |  |  |
|  | SNOW-64148 | Upgraded Python version to 3.6. |
| **SnowSQL 1.1.73** |  |  |
|  | SNOW-57001 | Driver now ignores exceptions from Heartbeat. |
|  | SNOW-63422 | Added support for negative values for year. |
|  | SNOW-63839 | Fixed out-of-range error for year values. |
|  | SNOW-64053 | Added an option to automatically print query ids. |
| **SnowSQL 1.1.72** |  |  |
|  | SNOW-37156 | Added new SQL functions to the keyword list for auto-completion and syntax highlighting. |
|  | SNOW-54514 | Fixed issue with explicitly-specified default region causing SnowSQL to hanging indefinitely. |
| **SnowSQL 1.1.71** |  |  |
|  | SNOW-36812 | Added the `!pause` command to pause and continue running queries. |
|  | SNOW-56234 | For Snowflake accounts hosted on Azure, fixed the PUT/GET progress bar. |
|  | SNOW-59077 | Added the `timing_in_output_file` option to store the query timing in the output file. |
|  | SNOW-60603 | Added the `progress_bar` option to suppress displaying the progress of PUT and GET commands. |
|  | SNOW-61860 | Adjusted the log level to mitigate confusion. |
| **SnowSQL 1.1.70** |  |  |
|  | SNOW-60580 | For Snowflake accounts in the EU region, fixed 403 error. |
| **SnowSQL 1.1.69** |  |  |
|  | SNOW-58838 | Added service name support for multi-GS clustering (internal feature). |
|  | SNOW-58845 | Added SNOWSQL\_DOWNLOAD\_DIR environment variable to set the download directory. |
|  | SNOW-60056 | For Windows, fixed issue with Python connector failing to convert pre-epoch TIMESTAMP\_NTZ data. |
| **SnowSQL 1.1.68** |  |  |
|  | SNOW-58177 | SnowSQL now raises a more user-friendly error if `localhost` is not found. |
| **SnowSQL 1.1.67** |  |  |
|  | SNOW-56812 | Fixed an issue where `exit_on_error=true` didn’t work if an error occurred for a PUT or GET command. |
|  | SNOW-56882 | Fixed an issue caused by using a backslash followed by a single quote in a literal (e.g. `'text\'s string'`). |
| **SnowSQL 1.1.66** |  |  |
|  | SNOW-55034 | Added `request_guid` to each HTTP request for tracing. |
|  | SNOW-56079 | Fixed an issue with setting a single right angle bracket (`>`) as the command-line prompt. |
| **SnowSQL 1.1.65** |  |  |
|  | SNOW-55027 | Added support for binding the `datetime` object with the Snowflake TEXT data type. |
|  | SNOW-55093 | Internal change for pending feature. |
|  | SNOW-55253 | Added the `--client-session-keep-alive` option. |
| **SnowSQL 1.1.64** |  |  |
|  | SNOW-31060 | Adjusted log levels by changing most `INFO` logs to `DEBUG`. |
|  | SNOW-54322 | Fixed a misspelling in an error message for SSO. |
|  | SNOW-54714 | SnowSQL now retries if HTTP 405 error is encountered. |
| **SnowSQL 1.1.63** |  |  |
|  | SNOW-52668 | Added `-U` and `--upgrade` options to enable forcing upgrading to the latest version of SnowSQL. |
|  | SNOW-53452 | Internal change for pending feature. |
|  | SNOW-53650 | Internal change for pending feature. |
|  | SNOW-53890 | Fixed the incorrect description in the SnowSQL help for the `friendly` option. |
|  | SNOW-53891 | Fixed issue which incorrectly displayed the following message when **[Ctrl]+[D]** was used to exit SnowSQL: `If the error message is not clear, enable the logging using -o log_level=DEBUG...`; the message is no longer displayed. |
| **SnowSQL 1.1.62** |  |  |
|  | SNOW-53405 | Deprecated the `region` parameter; instead, region information is specified (if needed) in the `account` parameter. |
|  | SNOW-53629 | Removed hardcoded `testaccount` names. |
| **SnowSQL 1.1.61** |  |  |
|  | SNOW-50629 | SnowSQL now uses UTC timestamp for logging. |
|  | SNOW-50766 | Updated SnowSQL to enforce virtual host style for S3 URLs. |
| **SnowSQL 1.1.60** |  |  |
|  | SNOW-50514 | Internal change for pending feature. |
|  | SNOW-51669 | Internal change for pending feature. |
| **SnowSQL 1.1.59** |  |  |
|  | SNOW-48675 | Added support for client-side job telemetry (for internal use). |
|  | SNOW-48678 | Internal change for pending feature. |
| **SnowSQL 1.1.58** |  |  |
|  | SNOW-45021 | Removed login name requirement when authenticating with an OAuth access token. |
| **SnowSQL 1.1.57** |  |  |
|  | SNOW-43215 | SnowSQL now uses OCSP dynamic server if OCSP response doesn’t exist in the cache. This is currently only for AWS PrivateLink. |
| **SnowSQL 1.1.56** |  |  |
|  | SNOW-28419 | SnowSQL now dumps the TLS/SSL Certificate to `stdout` if the handshake fails; provided primarily for troubleshooting connection issues. |
|  | SNOW-39938 | Fixed issue where the `key_bindings` configuration parameter did not work correctly when set to `vi` mode. |
| **SnowSQL 1.1.55** |  |  |
|  | SNOW-41707 | Internal change for pending feature. |
| **SnowSQL 1.1.54** |  |  |
|  | SNOW-42833 | Internal change for pending feature. |
| **SnowSQL 1.1.53** |  |  |
|  | SNOW-41694 | Added support for key pair authentication. |
| **SnowSQL 1.1.52** |  |  |
|  | SNOW-40919 | Added `login_timeout` option. |
|  | SNOW-41377 | Fixed TypeError that occurred when using PUT or GET command to upload/download extremely large numbers of small files. |
| **SnowSQL 1.1.51** |  |  |
|  | SNOW-34467 | Internal change for pending feature. |
| **SnowSQL 1.1.50** |  |  |
|  | SNOW-28376 | SnowSQL now uses the shared OCSP response cache file in `~/.cache/snowflake/ocsp_response_cache.json`. |
|  | SNOW-38618 | SnowSQL now handles cases where `stdin/stdout/stderr` is closed. |
| **SnowSQL 1.1.49** |  |  |
|  | SNOW-21492 | Added flag for OCSP response cache server. |
| **SnowSQL 1.1.48** |  |  |
|  | SNOW-37395 | Added support for the `authenticator` option in the configuration file. |
| **SnowSQL 1.1.47** |  |  |
|  | SNOW-37262 | Fixed `string index out of range` error, which occurred when a string, ending with an escape sequence, was truncated. |
| **SnowSQL 1.1.46** |  |  |
|  | SNOW-24653 | Fixed issue that generated an error stack if the specified log file was not accessible; now, the error stack is suppressed. |
|  | SNOW-24710 | Added connection parameter to support single transactions. |
|  | SNOW-28482 | Added option to support paging output. |
|  | SNOW-32282 | Internal change for pending feature. |
| **SnowSQL 1.1.45** |  |  |
|  | SNOW-32806 | Internal change for pending feature. |
|  | SNOW-34176 | Upgraded underlying PyInstaller to 3.3 along with the base Python version to 3.5. |
|  | SNOW-34418 | Fixed performance issue with SHOW COLUMN IN ACCOUNT command. |
|  | SNOW-36332 | Windows: Fixed an issue where the output was truncated. |
| **SnowSQL 1.1.44** |  |  |
|  | SNOW-35404 | Fixed issue where fractions of seconds in timestamps were reported incorrectly. |
| **SnowSQL 1.1.43** |  |  |
|  | SNOW-30483 | Added support for SAML 2.0-compliant services/applications for federated authentication by adding the `externalbrowser` value to the `authenticator` connection option. |
|  | SNOW-32139 | Added correct verification of the proof key, login name, and request ID in support of SAML 2.0-compliant services/applications for federated authentication. |
| **SnowSQL 1.1.42** |  |  |
|  | SNOW-33973 | SnowSQL now retries all HTTP 5xx errors returned by the Python Connector. |
|  | SNOW-34027 | To prevent AWS token expiration issues, SnowSQL now renews the AWS token if a `S3UploadFailedError` error occurs. |
|  | SNOW-34123 | Fixed a minor issue where an error was generated with no error message. |
| **SnowSQL 1.1.41** |  |  |
|  | SNOW-29826 | Error message details improved for connection errors caused by an invalid SSL certificate. |
|  | SNOW-31859 | SnowSQL now assigns a `__rowcount` variable to the number of rows updated/selected by the previous statement, which can then be called using the SnowSQL variables syntax (e.g. `&__rowcount`). |
|  | SNOW-33405 | SnowSQL now monitors the status of queries when running in asynchronous mode and waits for the queries to finish before disconnecting from Snowflake. |
| **SnowSQL 1.1.40** |  |  |
|  | SNOW-33112 | SnowSQL now retries queries indefinitely to mitigate HTTP 500 errors. |
| **SnowSQL 1.1.39** |  |  |
|  | SNOW-30483 | Fixed a security issue for SAML integration. |
|  | SNOW-31153 | Implemented support for using **Ctrl+C** to exit when prompted for a password (during re-authentication). |
|  | SNOW-32445 | Fixed an issue with fetching large result sets for Azure BLOB. |
| **SnowSQL 1.1.38** |  |  |
|  | SNOW-29144 | SnowSQL now flushes output to a file on each write. |
| **SnowSQL 1.1.37** |  |  |
|  | SNOW-30483 | Added support for web-based SAML authentication. |
| **SnowSQL 1.1.36** |  |  |
|  | SNOW-32074 | Fixed issue introduced in previous rolled-back version of SnowSQL. |
| **SnowSQL 1.1.35** |  |  |
|  | SNOW-30483 | Internal fix (rolled back). |
| **SnowSQL 1.1.34** |  |  |
|  | SNOW-31790 | Minor improvements to SnowSQL help text. |
| **SnowSQL 1.1.33** |  |  |
|  | SNOW-31712 | Fixed regression introduced in 1.1.32: missing parameter, `src_file_size`, resulted in GET commands returning errors. |
| **SnowSQL 1.1.32** |  |  |
|  | SNOW-31396 | Removed scanning of all existing files in a stage before executing a PUT command. Now, each individual upload operation checks the target file, and if the file digests are identical, the file is not uploaded. This reduces overhead on the PUT command. |
| **SnowSQL 1.1.31** |  |  |
|  | SNOW-18939 | Added support for ORC file format in PUT command. |
|  | SNOW-30785 | Added support for the current role in the SnowSQL prompt. |
| **SnowSQL 1.1.30** |  |  |
|  | SNOW-30376 | Set AUTOCOMMIT and ABORT\_DETACHED\_QUERY session parameter in authentication time instead of separate command executions. |
|  | SNOW-30422 | Changed the log levels for OCSP and some network related messages from INFO to DEBUG. |
|  | SNOW-30428 | Added region parameter to S3 connection so that PUT and GET can support cross-region stages. |
| **SnowSQL 1.1.29** |  |  |
|  | SNOW-29714 | Added check to make sure file isn’t empty when checking to see if compression type is zstd. |
|  | SNOW-29933 | Driver suppresses ‘No data returned’ message when no data is returned and `friendly=false`. |
| **SnowSQL 1.1.28** |  |  |
|  | SNOW-27327 | Added support for brotli and zstd in PUT statements for the python connector. |
|  | SNOW-29584 | Implemented timeout OCSP server requests to mitigate hang. |
| **SnowSQL 1.1.27** |  |  |
|  | SNOW-29146 | Fixed issue with the bootstrap process that may cause invalid literal for `int()` with base 10. |
|  | SNOW-29283 | Fixed issue with Python3.5 DLL that fails to get loaded on Windows. |
| **SnowSQL 1.1.26** |  |  |
|  | SNOW-29023 | Added `remove_trailing_semicolons` option. |
|  | SNOW-29098 | Fixed issue for undeleted sessions by explicitly closing a session at the end of an event loop. |
| **SnowSQL 1.1.25** |  |  |
|  | SNOW-28883 | Fixed issue where auto-completion caused a non-fatal exception when typing the AS keyword in a SQL statement, e.g. when defining a view. |
| **SnowSQL 1.1.24** |  |  |
|  | SNOW-17790 | Fixed how the fractional seconds (FF) timestamp format is handled. |
|  | SNOW-28596 | Fixed issue with SnowSQL not closing sessions correctly. |
|  | SNOW-28810 | Fixed issue with `!edit` command not returning the edited text to the prompt. |
|  | SNOW-28812 | Improved user experience for `!exit` and `!quit` commands by allowing SnowSQL to quit without deleting the session connection. |
| **SnowSQL 1.1.23** |  |  |
|  | SNOW-28202 | Improved retry of the PUT command on `OpenSSL.SSL.SysCallError 10053` with lower concurrency to mitigate connection saturation. |
|  | SNOW-28345 | Improved OKTA authentication by securing the hostname matching. |
|  | SNOW-28380 | Added `query_id_in_error` option to show or hide the query ID in the error message. |
|  | SNOW-28570 | Fixed issue where command (string beginning with an exclamation point) could not be executed if it contained a tailing semi-colon; driver now ignores the semi-colon. |
| **SnowSQL 1.1.22** |  |  |
|  | SNOW-18260 | Added support for executing multiple SQL files. |
|  | SNOW-24118 | Added SnowSQL installation files to the Amazon S3 artifact repository, in addition to the Snowflake web interface |
|  | SNOW-28224 | Fixed issue in which SnowSQL exited before asynchronous queries could complete execution. |
|  | SNOW-28266 | Fixed issue in which the `!quit` command caused the following exception: `AttributeError: 'Statement' object has no attribute 'to_unicode'`. |
|  | SNOW-28247 | Fixed issue in which a non-SQL command producing empty results failed. |
| **SnowSQL 1.1.21** |  |  |
|  | SNOW-22313 | Changed the transaction completion behavior to roll back in-progress transactions when SnowSQL exits or quits a session. |
|  | SNOW-28072 | Fixed a conversion failure issue that caused a `collections.defaultdict` exception. |
|  | SNOW-28220 | Fixed an issue in which autocomplete raised an exception if the previous token had a comparison type. |
| **SnowSQL 1.1.20** |  |  |
|  | SNOW-21252 | Fixed an issue with inconsistent behavior for account, username, and password inputs with MFA and new password. |
|  | SNOW-23904 | Improved auto-completion support for warehouses and stages; also includes various fixes for auto-completion. |
|  | SNOW-27292 | Changed auto-upgrade check to run once per hour after startup, rather than after every restart. This change requires a manual reinstall of SnowSQL. |
| **SnowSQL 1.1.19** |  |  |
|  | SNOW-25342 | Added support for version as a configuration parameter, in addition to the `-v , --version` connection parameters that are already supported. |
|  | SNOW-27620 | Implemented general performance improvements. |
|  | SNOW-27647 | Fixed internal issue with elapsed time. |
|  | SNOW-27657 | Added support for proxy parameter for OCSP validation. |
|  | SNOW-27671 | Extended the token retry period for PUT and GET to 2 hours; if all retries fail, an error is returned. |
|  | SNOW-27710 | Fixed issue where, in interactive mode, SnowSQL executed commands that were not properly started with an exclamation point or ended with a semi-colon; this issue was caused by an issue introduced in v1.1.17. |
|  | SNOW-27715 | Added support for proxy parameter for PUT and GET commands. |
|  | SNOW-27732 | SnowSQL now ignores/removes the protocol prefix, i.e. `http://` or `https://`, if included in the `--proxy-host` connection parameter. |
| **SnowSQL 1.1.18** |  |  |
|  | SNOW-25251 | Fixed issue with semi-colons in comments stopping parsing of the rest of the statement. |
|  | SNOW-27443 | Fixed issue where specifying an invalid account name returned irrelevant exception. |
| **SnowSQL 1.1.17** |  |  |
|  | SNOW-21299 | Fixed the `reauth` failure that occurs when a session expires and the password is wrong. |
|  | SNOW-27328 | Fixed issue with the `--region` connection option that caused one character to be truncated from the end of the account name. |
|  | SNOW-27345 | Implemented performance improvements when parsing SQL scripts. |
|  | SNOW-27356 | Fixed issue with the `New Password` prompt not displaying in non-interactive mode; this was caused by an issue introduced in v1.1.15. |
|  | SNOW-27374 | Added `execution_only` option for executing queries without fetching data. |
| **SnowSQL 1.1.16** |  |  |
|  | SNOW-27308 | Fixed an issue with converting DATE columns to Python data. |
| **SnowSQL 1.1.15** |  |  |
|  | SNOW-22443 | Added support for MFA passcode input. |
|  | SNOW-26262 | Implemented performance improvements for fetching numeric and timestamp data types. |
|  | SNOW-27094 | Added the `--region` connection option to support specifying the Snowflake deployment region for the account. |
| **SnowSQL 1.1.14** |  |  |
|  | SNOW-26990 | Fixed issue with OCSP access retries when a non-200 HTTP response code is returned. |
| **SnowSQL 1.1.13** |  |  |
|  | SNOW-26802 | Fixed issue in Windows environment where the bootstrap process and main executable caused conflicts writing to the same log file. Issue fixed by writing the bootstrap log to a separate file. |
| **SnowSQL 1.1.12** |  |  |
|  | SNOW-26586 | Fixed issue where the client failed to decode JSON output due to invalid UTF-8 byte sequence. |
| **SnowSQL 1.1.11** |  |  |
|  | SNOW-26352 | Fixed issue with VARIABLE not found; this was caused by an issue introduced in v1.1.10. |
| **SnowSQL 1.1.10** |  |  |
|  | SNOW-26081 | Increased the validity date acceptance window to prevent OCSP returning invalid responses due to out-of-scope validity dates for certificates; also enabled OCSP response cache file by default. |
|  | SNOW-26246 | Fixed issue where the value of variables in SnowSQL cannot include the equal character (`=`). |
|  | SNOW-26264 | Fixed issue with results command that dumped error stack. |
|  | SNOW-26265 | Fixed issue where the `!result` and `!abort` commands hang if no variable substitution is enabled. |
| **SnowSQL 1.1.9** |  |  |
|  | SNOW-25189 | Fixed issue with SnowSQL unexpectedly converting strings to numbers. |
| **SnowSQL 1.1.8** |  |  |
|  | SNOW-25368 | Fixed issue with return timing for results with 0 rows. |
| **SnowSQL 1.1.7** |  |  |
|  | SNOW-25260 | Added `noup=true` configuration option so that users can skip auto-upgrade by adding the option directly to the config file. SnowSQL already has the `--noup` connection option to prevent auto-upgrade when connecting to Snowflake. |
| **SnowSQL 1.1.6** |  |  |
|  | SNOW-24965 | Fixed issue where empty results return the following error: `max() arg is an empty sequence when specify -o output_format=expanded`. |
| **SnowSQL 1.1.5** |  |  |
|  | SNOW-17258 | Fixed issues with how AUTO handled Parquet file compression: COMPRESSION parameter for CREATE / ALTER FILE FORMAT commands and AUTO\_COMPRESS parameter for PUT command. |
|  | SNOW-21492 | SnowSQL now uses the OCSP response cache file located in `~/.snowsql/ocsp_response_cache`. This file is used to store OCSP responses up to 24 hours. |
| **SnowSQL 1.1.4** |  |  |
|  | SNOW-24548 | Set the signature version for AWS client to v3 (no change in functionality). |
| **SnowSQL 1.1.3** |  |  |
|  | SNOW-23198 | Fixed a problem that caused output spanning multiple lines to sometimes result in a misaligned table format. |
| **SnowSQL 1.1.2** |  |  |
|  | SNOW-20418 | Added support for PUT command. |
|  | SNOW-23840 | Added command-line options `--proxy-user` and `--proxy-password` to support proxy authentication. |
| **SnowSQL 1.1.0** |  |  |
|  | Feature | Various minor enhancements. |
|  | Bug fix | Command-line options are now passed through to the main SnowSQL executable. |
|  | Bug fix | SnowSQL online upgrade is now transactional. |
|  | Bug fix | Option names are now case-insensitive. |
|  | Bug fix | Various minor bug fixes. |
| **SnowSQL 1.0.0** |  |  |
|  | Initial release |  |

Expand

Show lessSee more
