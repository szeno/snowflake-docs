# snow connection list

Lists configured connections.

## Syntax

Copy code

```
snow connection list
  --all
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

`--all, -a`
:   Include connections from all sources (environment variables, SnowSQL config). By default, only shows connections from configuration files. Default: False.

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

The `snow connection list` command lists the connections in your default `config.toml` file.
For more information, see [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).

## Examples

Copy code

```
snow connection list
```

```
+--------------------------------------------------------------------------------------------------------------------------------+
| connection_name | parameters                                                                                                   |
|-----------------+--------------------------------------------------------------------------------------------------------------|
| my-prod         | {'account': 'po52878', 'user': 'JDOE', 'password': '****', 'role': 'integration_tests', 'database':          |
|                 | 'SNOWFLAKE'}                                                                                                 |
|-----------------+--------------------------------------------------------------------------------------------------------------|
| my-test         | {'account': 'po52878', 'user': 'SSMITH', 'password': '****', 'role': 'integration_tests', 'database':        |
|                 | 'SNOWFLAKE'}                                                                                                 |
+--------------------------------------------------------------------------------------------------------------------------------+
```
