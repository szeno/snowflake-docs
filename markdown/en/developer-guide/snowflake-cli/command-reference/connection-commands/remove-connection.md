# snow connection remove

Removes a connection from configuration file.

## Syntax

Copy code

```
snow connection remove
  <connection_name>
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`connection_name`
:   Name of the connection to remove.

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

None.

## Examples

To remove a connection, execute a `snow connection remove` command similar to the following:

Copy code

```
snow connection remove bad_connection
```

```
Removed connection bad_connection from /Users/jdoe/.snowflake/config.toml.
```
