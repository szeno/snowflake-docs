# snow helpers detect-encoding

Show the encoding configuration for the current environment.

## Syntax

Copy code

```
snow helpers detect-encoding
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

Use `snow helpers detect-encoding` to inspect the text encoding Snowflake CLI uses in the current environment and to diagnose encoding warnings. The command reports the encodings applied to reading and writing project files, decoding subprocess output, and writing output to standard output, and it highlights settings that can corrupt files when projects are shared across platforms, for example between Windows and macOS or Linux.

To change these encodings, configure the `[cli.encoding]` section of `config.toml` or set the corresponding `SNOWFLAKE_CLI_ENCODING_*` environment variables. For more information, see [Configuring Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli).

## Examples

- Show the encoding configuration for the current environment:

  Copy code

  ```
  snow helpers detect-encoding
  ```
- Emit the encoding details as JSON for scripting:

  Copy code

  ```
  snow helpers detect-encoding --format json
  ```
