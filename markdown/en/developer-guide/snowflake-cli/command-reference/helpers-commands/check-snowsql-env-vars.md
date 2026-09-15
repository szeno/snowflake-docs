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

`--format [TABLE%JSON%JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels *info* and higher. Default: False.

`--debug`
:   Displays log entries for log levels *debug* and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

This command helps you migrate from SnowSQL to Snowflake CLI by identifying your SnowSQL environment variables and mapping them to the corresponding Snowflake CLI environment variables. It displays information with suggested changes and links to documentation.

## Examples

This example assumes a user has defined the following environment variables:

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
