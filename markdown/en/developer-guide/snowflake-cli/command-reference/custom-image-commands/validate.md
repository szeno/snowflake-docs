# snow custom-image validate

Validates a Docker image against Snowflake custom image requirements.

## Syntax

Copy code

```
snow custom-image validate
  <image>
  --scan-vulnerabilities
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`image`
:   Local Docker image to validate. Accepts image name (e.g., ‘myimage:latest’) or image ID/hash.

## Options

`--scan-vulnerabilities`
:   Run vulnerability scan using Grype. Requires Grype to be installed. Default: False.

`--format [TABLE|JSON|JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

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

The `snow custom-image validate` command validates a custom Docker image against the configured rules before you register it for use with Snowflake container services. The command checks the entrypoint configuration, required environment variables, installed Python packages, and dependency health.

Pass the `--scan-vulnerabilities` flag to run Grype vulnerability scanning against the image as part of validation.

## Examples

- Validate a local Docker image:

  Copy code

  ```
  snow custom-image validate my-image:latest
  ```
- Validate a local Docker image and scan it for vulnerabilities:

  Copy code

  ```
  snow custom-image validate my-image:latest --scan-vulnerabilities
  ```
