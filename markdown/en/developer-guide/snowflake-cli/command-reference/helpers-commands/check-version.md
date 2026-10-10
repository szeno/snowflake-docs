# snow helpers check-version

Check whether a newer version of the Snowflake CLI is available.

## Syntax

Copy code

```
snow helpers check-version
  --refresh
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

`--refresh`
:   Query PyPI and Homebrew for the latest version instead of using the local cache. Default: False.

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

`snow helpers check-version` doesn’t require a Snowflake connection. It checks locally cached version information by default. Use `--refresh` to query PyPI and Homebrew directly, bypassing the cache.

## Examples

- Check whether a newer version is available using the local cache:

  Copy code

  ```
  snow helpers check-version
  ```
- Query PyPI and Homebrew directly for the latest version:

  Copy code

  ```
  snow helpers check-version --refresh
  ```
