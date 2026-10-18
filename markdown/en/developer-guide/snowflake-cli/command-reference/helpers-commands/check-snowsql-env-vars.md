# snow helpers check-snowsql-env-vars

Check if there are any SnowSQL environment variables set.

## Syntax

Copy code

```
snow helpers check-snowsql-env-vars
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

None

## Options

`--format [TABLE|JSON|JSON_EXT|CSV]`
:   Specifies the output format. [env var: SNOWFLAKE\_CLI\_OUTPUT\_FORMAT | config: cli.output\_format]. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels `info` and higher. Default: False.

`--debug`
:   Displays log entries for log levels `debug` and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

This command only prints suggested Snowflake CLI mappings. It doesn’t set or migrate environment variables.
It treats a `snowsql` prefix without regard to case. Only the exact uppercase names in the map get a suggestion. On Windows, the operating system stores environment-variable names in uppercase, so `snowsql_account` is read as `SNOWSQL_ACCOUNT`. The command handles these names as follows:

- `EXIT_ON_ERROR` isn’t printed, because that name doesn’t start with `snowsql`.
- `snowsql_account` is reported unused on Unix-like systems, where the lowercase name is preserved. Only the exact uppercase name `SNOWSQL_ACCOUNT` gets a suggestion. On Windows, that lowercase name is already uppercase, so the command suggests `SNOWFLAKE_ACCOUNT`.
- `SNOWSQL_PASSWORD` is reported unused. The known password name is `SNOWSQL_PWD`.
- `SNOWSQL_ACCOUNTNAME` is reported unused. The documented name is `SNOWSQL_ACCOUNT`.
- `SNOWSQL_REGION` is suggested as `SNOWFLAKE_ACCOUNT` (account identifier, not the region name). Put the [account identifier](/user-guide/admin-account-identifier) in `SNOWFLAKE_ACCOUNT` or on the imported connection’s `account`. Don’t copy the region name into the account. A region value already in the SnowSQL file is imported as `region`. The default Snowflake CLI doesn’t read `SNOWSQL_REGION` or `SNOWFLAKE_REGION` while connecting.
- `SNOWSQL_PROXY_HOST` is suggested as `HTTPS_PROXY or HTTP_PROXY host`. `SNOWSQL_PROXY_PORT`, `SNOWSQL_PROXY_USER`, and `SNOWSQL_PROXY_PWD` are suggested as `HTTPS_PROXY or HTTP_PROXY` followed by `port`, `username`, or `password`. Those SnowSQL proxy variables aren’t read while connecting.

For the connection mappings the default Snowflake CLI connection behavior reads, see [Manually migrate your environment variables](/user-guide/snowsql-migrate#label-snowsql-migration-env-var-mappings).

## Examples

- This example assumes a user has defined the following environment variables:
- `SNOWSQL_USER`: Username for the connection.
- `SNOWSQL_ROLE`: Role for the connection.
- `SNOWSQL_UNUSED`: Variable not used in Snowflake CLI.

  Copy code

  ```
  snow helpers check-snowsql-env-vars
  ```

  ```
  +--------------------------------------------------------------------------------------------------------------------------------------------+
  | Found        | Suggested      | Additional info                                                                                            |
  |--------------+----------------+------------------------------------------------------------------------------------------------------------|
  | SNOWSQL_USER | SNOWFLAKE_USER | https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#use-environme |
  |              |                | nt-variables-for-snowflake-credentials                                                                     |
  | SNOWSQL_ROLE | SNOWFLAKE_ROLE | https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#use-environme |
  |              |                | nt-variables-for-snowflake-credentials                                                                     |
  +--------------------------------------------------------------------------------------------------------------------------------------------+

  +----------------------------------------------+
  | Found          | Suggested | Additional info |
  |----------------+-----------+-----------------|
  | SNOWSQL_UNUSED | n/a       | Unused variable |
  +----------------------------------------------+

  Found 3 SnowSQL environment variables, 2 with replacements, 1 unused.
  ```
