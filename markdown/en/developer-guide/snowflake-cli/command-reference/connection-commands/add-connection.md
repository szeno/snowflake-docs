# snow connection add

Adds a connection to configuration file.

## Syntax

Copy code

```
snow connection add
  --connection-name <connection_name>
  --account <account>
  --user <user>
  --password <password>
  --role <role>
  --warehouse <warehouse>
  --database <database>
  --schema <schema>
  --host <host>
  --port <port>
  --region <region>
  --authenticator <authenticator>
  --workload-identity-provider <workload_identity_provider>
  --private-key <private_key_file>
  --token-file-path <token_file_path>
  --default
  --no-interactive
  --protocol <protocol>
  --secondary-roles <secondary_roles>
  --server-session-keep-alive
  --client-store-temporary-credential
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

`--connection-name, -n TEXT`
:   Name of the new connection.

`-a, --account, --accountname TEXT`
:   Account name to use when authenticating with Snowflake.

`-u, --user, --username TEXT`
:   Username to connect to Snowflake.

`-p, --password TEXT`
:   Snowflake password.

`-r, --role, --rolename TEXT`
:   Role to use on Snowflake.

`-w, --warehouse TEXT`
:   Warehouse to use on Snowflake.

`-d, --database, --dbname TEXT`
:   Database to use on Snowflake.

`-s, --schema, --schemaname TEXT`
:   Schema to use on Snowflake.

`-h, --host TEXT`
:   Host name the connection attempts to connect to Snowflake.

`-P, --port INTEGER`
:   Port to communicate with on the host.

`--region, -R TEXT`
:   Region name if not the default Snowflake deployment.

`-A, --authenticator TEXT`
:   Chosen authenticator, if other than password-based.

`-W, --workload-identity-provider TEXT`
:   Workload identity provider type.

`--private-key, -k, --private-key-file, --private-key-path TEXT`
:   Path to file containing private key.

`-t, --token-file-path TEXT`
:   Path to file with an OAuth token that should be used when connecting to Snowflake.

`--default`
:   If provided the connection will be configured as default connection. Default: False.

`--no-interactive`
:   Disable prompting. Default: False.

`--protocol TEXT`
:   Protocol to use for the connection, for example `https`.

`--secondary-roles TEXT`
:   Secondary roles mode applied when the session starts. Supported values are `ALL` and `NONE`; pass `NONE` to run the session only with the primary role.

`--server-session-keep-alive`
:   Enable server-side session keep-alive to prevent the session from timing out during long operations.

`--client-store-temporary-credential`
:   Store the temporary credential.

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

The `snow connection add` command adds the connection to your default `config.toml` file.
For more information, see [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).

## Examples

To add a connection, run the following:

Copy code

```
snow connection add
Enter connection name: <connection_name>
Enter account: <account>
Enter user: <user-name>
Enter password: <password>
Enter role: <role-name>
Enter warehouse: <warehouse-name>
Enter database: <database-name>
Enter schema: <schema-name>
Enter host: <host-name>
Enter port: <port-number>
Enter region: <region-name>
Enter authenticator: <authentication-method>
Enter private key file: <path-to-private-key-file>
Enter token file path: <path-to-mfa-token>
Do you want to configure key pair authentication? [y/N]: y
Key length [2048]: <key-length>
Output path [~/.ssh]: <path-to-output-file>
Private key passphrase: <key-description>
Wrote new connection <connection-name> to config.toml
```

```
Wrote new connection my_conn to <user-home>/.snowflake/config.toml
```
