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
:   SnowSQL configuration file to merge after the default locations. This doesn’t replace the default file list. Repeat to merge several files. `/usr/lib64/snowflake/snowsql/config` is still read last. Each path must already exist. A missing path fails the command and writes nothing. A file that exists but can’t be read also fails before anything is written.

`--default-connection-name TEXT`
:   Specifies the name which will be given in Snowflake CLI to the default connection imported from SnowSQL. Default: default.

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

Run `snow helpers import-snowsql-connections` once. It copies connection sections into your Snowflake CLI configuration and stops. It doesn’t copy `[variables]`, `[connection_options]`, or environment variables, and it doesn’t watch SnowSQL afterward. From `[options]`, it copies only `login_timeout`, `client_session_keep_alive`, `ocsp_fail_open`, `insecure_mode`, and `client_store_temporary_credential`, and only when a connection omits that key. Other `[options]` settings stay unimported. Two runs of this command on the same files agree, aside from the prompts. An overwrite answer changes whether that connection is replaced. If the unnamed section’s name is already taken, the name you type also changes what is saved. A connection saved by an older version of the command can differ: a named connection no longer receives keys from the unnamed `[connections]` section. The import command isn’t part of normal startup.

### Files the command reads

By default, the command reads the following SnowSQL configuration files, in order, and skips a file that is missing:

- `/etc/snowsql.cnf`
- `/etc/snowflake/snowsql.cnf`
- `/usr/local/etc/snowsql.cnf`
- `~/.snowsql.cnf`
- `~/.snowsql/config`

It doesn’t read SnowSQL’s packaged `snowsql.cnf` template.
`/usr/lib64/snowflake/snowsql/config` is read last, when that file exists, and overrides the same keys.
It processes every non-empty `[connections]` and `[connections.*]` section. When the same connection appears in more than one file, keys are merged. A key in a later file replaces that key from an earlier file. A key that appears only in an earlier file is kept.
You can pass `--snowsql-config-file` more than once to merge files after those five default files. The option doesn’t replace that list. Each path must already exist. A missing custom path fails the command and writes nothing. `/usr/lib64/snowflake/snowsql/config` is still read after the custom files and overrides the same keys.
When `WORKSPACE` is set to a non-empty value, `~/.snowsql.cnf` and `~/.snowsql/config` are read from that directory instead of the home directory. An empty value, or a value that is only whitespace, is unset, so the home directory is used. The `/etc` paths, a custom `--snowsql-config-file`, and `/usr/lib64/snowflake/snowsql/config` don’t move.
On Windows, `~/.snowsql.cnf` and `~/.snowsql/config` still use the user profile unless `WORKSPACE` is set. The command doesn’t add a program-data directory. If the SnowSQL file is somewhere else, pass `--snowsql-config-file`.
A file that exists but can’t be read fails the import before anything is written. Each file is read as UTF-8, and a file larger than 128 MB is rejected. An unreadable file, a file that can’t be decoded, or a file that isn’t valid configuration raises an error that names the path. A permission error includes the operating-system reason, such as `Permission denied`. A file that can’t be decoded says that the file could not be read. A parse error says that the file could not be parsed. Neither message repeats the file contents. A missing default file, or a missing `/usr/lib64/snowflake/snowsql/config`, is still skipped.

To illustrate, assume the same `[connections.example]` connection is defined with different parameters in the following locations:

| Location of the configuration file | Connection definition |
| --- | --- |
| `/etc/snowsql.cnf` | Copy code  ``` [connections]  [connections.example] username=user1 ``` |
| `<HOME_DIR>/.snowsql/config` | Copy code  ``` [connections]  [connections.example] username=user2 accountname=myorg-myaccount databasename=mydatabase private_key_path=/path/to/rsa_key.p8 password=<my-pwd> ``` |

Expand

Show lessSee more

After you run the command, `config.toml` contains the remapped `[connections.example]` definition. Keys from `<HOME_DIR>/.snowsql/config` replace the same keys from `/etc/snowsql.cnf`:

Copy code

```
[connections.example]
user = "user2"
account = "myorg-myaccount"
database = "mydatabase"
private_key_file = "/path/to/rsa_key.p8"
authenticator = "SNOWFLAKE_JWT"
password = "<my-pwd>"
```

If `connections.toml` exists, the command writes the same values to a top-level `[example]` section in that file. It doesn’t write `[connections.example]` in that file. `default_connection_name` is still written to `config.toml`.

### How keys are renamed

The command renames these SnowSQL keys: `accountname` to `account`, `username` to `user`, `dbname` to `database`, `schemaname` to `schema`, `warehousename` to `warehouse`, `rolename` to `role`, `pwd` to `password`, `private_key_path` to `private_key_file`, `private_key_file_pwd` to `private_key_passphrase`, and `proxy_pwd` to `proxy_password`. `databasename` is a last-resort alias for `database`, not a SnowSQL key.
Aliases are resolved once, after the raw merge of every file. The Snowflake CLI name wins over the SnowSQL alias across files, not only inside one section, when that name isn’t blank. The exception is `private_key_path`, which wins over `private_key_file` when it has a value, and is saved as `private_key_file`. A blank or whitespace-only value is skipped, so the next name is used. `user=` with `username=alice` imports `alice`. The same rule applies to every alias pair, including `password` or `pwd` and `private_key_path` or `private_key_file`. The pairs are `account` over `accountname`, `user` over `username`, `password` over `pwd`, `database` over `dbname` over `databasename`, `schema` over `schemaname`, `warehouse` over `warehousename`, `role` over `rolename`, `private_key_passphrase` over `private_key_file_pwd`, and `proxy_password` over `proxy_pwd`. An earlier non-blank `account` isn’t replaced by a later `accountname`.
A named connection is only the keys in its `[connections.<name>]` section. Keys from the unnamed `[connections]` section aren’t copied onto it. SnowSQL often puts the account only on that unnamed section. Put the account on the named connection, or use the imported default connection, which is that unnamed section. An empty `[connections.name]` header is skipped for that file only. It doesn’t erase keys that another file set for the same name.
A blank value is left unset before the `[options]` copy. `password=` doesn’t save `""`, so Snowflake CLI can prompt or `SNOWFLAKE_PASSWORD` can fill the gap. A later blank on the same raw key still clears the earlier value. After coercion, Boolean `false` and integer `0` stay. They aren’t deleted as blanks. A section with nothing left isn’t saved, and it doesn’t pick up settings from `[options]`.

### Settings copied from `[options]`

These settings are copied from `[options]` onto each connection that still has values, and only when that connection omits the key. A key already set on the connection wins, including `0` and `false`:

- `login_timeout`
- `client_session_keep_alive`
- `ocsp_fail_open`
- `insecure_mode`
- `client_store_temporary_credential`

`[variables]` and the other settings in `[options]`, such as `log_level`, `timing`, and `output_format`, stay unimported.

### Values saved on the connection

`private_key_path` with no `authenticator` imports as `private_key_file` plus `authenticator = "SNOWFLAKE_JWT"`. A private key is kept only when the authenticator is absent or JWT. The JWT check ignores case, so `snowflake_jwt` keeps the private key. If an `authenticator` survives the merge and isn’t JWT, that authenticator is kept and `private_key_file` and `private_key_passphrase` are omitted. The command prints which connection dropped the key. Keeping that key with any other authenticator would leave a connection that Snowflake CLI can’t open.
`proxy_host`, `proxy_port`, `proxy_user`, and `proxy_password` are copied. `region` is stored as `region` and isn’t rewritten into `host`.
Every other key in the connection section is copied under the same name. Values are read the way SnowSQL 1.5 reads them. After the aliases are applied, only these keys are coerced. `login_timeout` and `client_prefetch_threads` become integers. `client_session_keep_alive`, `client_store_temporary_credential`, `ocsp_fail_open`, `insecure_mode`, `oauth_disable_pkce`, `oauth_enable_refresh_tokens`, `oauth_enable_single_use_refresh_tokens`, and `disable_request_pooling` become Booleans when the value is `true`, `false`, `yes`, `no`, `on`, `off`, `1`, or `0`. `insecure_mode=yes` is saved as `true`. `oauth_disable_pkce=false` is saved as Boolean `false`. If the value is left as the string `"false"`, the connector treats it as true. A value that isn’t one of those words stays text. `oauth_disable_pkce`, `oauth_enable_refresh_tokens`, `oauth_enable_single_use_refresh_tokens`, and `disable_request_pooling` aren’t copied from `[options]`. They’re coerced only when the connection section sets them. A value that doesn’t parse as an integer, such as `30s`, stays text. `password=123456` stays a string. `port` and `proxy_port` stay strings. `#` starts a comment. An unquoted comma list stays one string, so `token = a, b` stays `a, b`. One matching quote pair is stripped, so `accountname = "acct"` becomes `acct`, and a `#` inside the quotes stays. A `%` stays literal. Backslashes inside the quotes stay as written.
`[connection_options]` isn’t imported.
An imported `proxy_host` is what the connector uses. `HTTPS_PROXY` and `HTTP_PROXY` apply when that saved `proxy_host` is absent.

### Default connection name

The command also imports the unnamed SnowSQL default connection from the `[connections]` section.
Because Snowflake CLI requires named connections, that section is saved under `--default-connection-name` (default: `default`). In `config.toml` that is `[connections.default]`. In `connections.toml` that is a top-level `[default]` section.
If that name is already used by another connection in the same import, including `[connections.default]`, the command prompts for a different name for the unnamed section. A blank name is rejected. After three unsuccessful tries, the command stops with `Could not choose a name for the SnowSQL default connection.` and writes nothing. When a new name is accepted, the existing named connection is kept, and the unnamed section is saved under that new name.
`default_connection_name` is set only from the unnamed `[connections]` section, under the name that section was actually saved with, including a prompted rename. A section that is only `[connections.default]` doesn’t become the CLI default. If you decline the overwrite of that unnamed connection, the existing connection and `default_connection_name` are left unchanged. Declining a named connection still lets the unnamed section set the default when that section is saved.

The command prompts only for that name collision and when an imported name already exists in Snowflake CLI. In the overwrite case, it asks whether to replace the existing Snowflake CLI connection or skip that SnowSQL connection. The default answer is no.

## Examples

The following example imports SnowSQL connections from the standard configuration file locations:

Copy code

```
snow helpers import-snowsql-connections
```

As the command processes the SnowSQL configuration files, it shows the progress and prompts for confirmation when a connection with the same name is already defined in the Snowflake CLI configuration.

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
SnowSQL config file [/usr/lib64/snowflake/snowsql/config] does not exist. Skipping.
Connection 'connection1' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: Y
Connection 'connection2' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Connection 'default' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Saving [connection1] connection in Snowflake CLI's config.
Connections successfully imported from SnowSQL to Snowflake CLI.
```
