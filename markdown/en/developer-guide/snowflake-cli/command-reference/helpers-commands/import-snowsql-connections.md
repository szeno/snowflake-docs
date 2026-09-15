# snow helpers import-snowsql-connections

Import your existing connections from your SnowSQL configuration.

## Syntax

Copy code

```
snow helpers import-snowsql-connections
  --snowsql-config-file <custom_snowsql_config_files>
  --default-connection-name <default_cli_connection_name>
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

`--snowsql-config-file FILE`
:   Specifies file paths to custom SnowSQL configuration. The option can be used multiple times to specify more than 1 file.

`--default-connection-name TEXT`
:   Specifies the name which will be given in Snowflake CLI to the default connection imported from SnowSQL. Default: default.

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

The `snow helpers import-snowsql-connections` command imports existing connection definitions from SnowSQL into your `config.toml` configuration file.

By default, the command reads the SnowSQL configuration files in the order described in the [Configuring SnowSQL](/user-guide/snowsql-config#label-configuring-snowsql) topic.
If more than one of these configurations define the same connection, this command overwrites the previously imported connection definition with the most recent one.
To illustrate, assume the same `[connections.example]` connection is defined with different parameters in the following locations:

| Location of the configuration file | Connection definition |
| --- | --- |
| `/etc/snowsql.cnf` | Copy code  ``` [connections]  [connections.example] username=user1 ``` |
| `<HOME_DIR>/.snowsql/config` | Copy code  ``` [connections]  [connections.example] username=user2 password=<my-pwd> ``` |

Expand

Show lessSee more

After you run the command, your Snowflake CLI `config.toml` file contains the following `[connections.example]` definition (from the file with the higher precedence):

Copy code

```
[connections]

[connections.example]
username=user2
password=<my-pwd>
```

You can use the `--snowsql-config-file` option to override this default behavior and import from one or more specific SnowSQL configuration files instead.

The `snow helpers import-snowsql-connections` command also imports the default connection from SnowSQL, which is not a named connection.
It is defined directly in the `[connections]` section of the configuration file.
Because Snowflake CLI requires all connections to be named, the command defines a connection named `[default]`.
If you want to use another name for the default connection, you can specify it with the `--default-connection-name` option.

If a SnowSQL connection matches the name of an existing Snowflake CLI connection, the command prompt asks whether you want to overwrite the existing connection or skip importing that SnowSQL connection.

## Examples

The following example imports SnowSQL connections from the standard configuration file locations:

Copy code

```
snow helpers import-snowsql-connections
```

As the command processes the SnowSQL configuration files, it shows the progress and prompts for confirmation when a connection with the same name is already defined in the Snowflake CLI `config.toml` file.

```
SnowSQL config file [/etc/snowsql.cnf] does not exist. Skipping.
SnowSQL config file [/etc/snowflake/snowsql.cnf] does not exist. Skipping.
SnowSQL config file [/usr/local/etc/snowsql.cnf] does not exist. Skipping.
Trying to read connections from [/Users/<user>/.snowsql.cnf].
Reading SnowSQL's connection configuration [connections.connection1] from [/Users/<user>/.snowsql.cnf]
Trying to read connections from [/Users/<user>/.snowsql/config].
Reading SnowSQL's default connection configuration from [/Users/<user>/.snowsql/config]
Reading SnowSQL's connection configuration [connections.connection1] from [/Users/<user>/.snowsql/config]
Reading SnowSQL's connection configuration [connections.connection2] from [/Users/<user>/.snowsql/config]
Connection 'connection1' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: Y
Connection 'connection2' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Connection 'default' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Saving [connection1] connection in Snowflake CLI's config.
Connections successfully imported from SnowSQL to Snowflake CLI.
```
