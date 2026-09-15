# snow auth oidc read-token

Reads OIDC token based on the specified type. Use ‘auto’ to auto-detect available providers.

## Syntax

Copy code

```
snow auth oidc read-token
  --type <_type>
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

`--type [auto|github]`
:   Type of OIDC provider to use. Default: auto.

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

The `snow auth read-token` command displays the OIDC token, which can be used for authentication in Snowflake operations. This command is primarily for retrieving the authentication token and must run within the supported CI/CD runner.

## Examples

- Display the OIDC token in the current CI/CD environment:

  Copy code

  ```
  snow auth oidc read-token --type github
  ```
