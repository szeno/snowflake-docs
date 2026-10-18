# Migrating from SnowSQL to Snowflake CLI

Caution

[Snowflake CLI](/developer-guide/snowflake-cli/index) is the preferred command-line client for new installs and new work. SnowSQL is a
legacy command-line client. Snowflake will only add new features and enhancements to Snowflake CLI. Snowflake supports SnowSQL 1.5.x through
April 16, 2028. Earlier minor versions have earlier support end dates.

If you’re starting a new project, [install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). If you already use
SnowSQL, follow the steps in this topic.

## Choose your path

- **New to Snowflake:** [Install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) and start with
  [Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes). You don’t need SnowSQL.
- **Already using SnowSQL:** Follow the migration steps in this topic.

This guide helps you move existing SnowSQL connections, configuration, and SQL workflows to Snowflake CLI.

- [Migration steps](#label-snowsql-migration-migrate-connections)
- [Migrate your configurations](#label-snowsql-migration-migrate-configurations)
- [Connect to Snowflake](#label-snowsql-migration-connect-to-snowflake)
- [Run SQL queries](#label-snowsql-migration-execute-sql)

## Migration steps

To migrate from SnowSQL to Snowflake CLI, follow these steps:

1. [Install Snowflake CLI](#label-cli-migration-install) with your preferred method.
2. [Import your connections](#label-cli-migration-connections).
3. Optionally check for suggested changes for your environment variables.
4. Optionally create an alias that maps the `snowsql` shell command to the `snow sql` shell command.

### Install the Snowflake CLI software

For supported platforms and install methods (package installers, Homebrew, and PyPI), see
[Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). Binaries are also available from the
[Snowflake CLI binaries repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html).

### Migrate your SnowSQL connections and settings

Snowflake CLI provides a [snow helpers](/developer-guide/snowflake-cli/command-reference/helpers-commands/overview) command group to simplify the transition from SnowSQL to Snowflake CLI.
These helpers are shipped with Snowflake CLI. Use them as follows:

- Run [snow helpers import-snowsql-connections](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections) once. It copies connection sections into the Snowflake CLI configuration and stops. It doesn’t copy `[variables]`, `[connection_options]`, or environment variables, and it doesn’t watch SnowSQL afterward. A named connection doesn’t receive keys from the unnamed `[connections]` section. For the files the command reads, key renaming, the `[options]` copy, blank values, and the default connection name, see the [snow helpers import-snowsql-connections](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections) command reference.
- Run [snow helpers check-snowsql-env-vars](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-snowsql-env-vars) to print suggested mappings for SnowSQL environment variables that are set.
  It doesn’t change the environment. Some suggestions aren’t connection variables that the default Snowflake CLI connection behavior reads. Use the [environment-variable table](#label-snowsql-migration-env-var-mappings) on this page.

To keep existing scripts, map the `snowsql` command to `snow sql`.

On Unix-like systems:

Copy code

```
alias snowsql='snow sql'
```

In PowerShell:

Copy code

```
function snowsql { snow sql @args }
```

Scripts keep working when they use these Snowflake CLI forms:

- `-q` or `--query`, and `-f` or `--filename`. You can pass `-f` more than once.
- `-c` or `--connection`, and `-D` or `--variable`.
- `--account` or `--accountname`, `--user` or `--username`, `--database` or `--dbname`, `--schema` or `--schemaname`, `--role` or `--rolename`, `--warehouse`, `--host`, `--port`, `--protocol`, and `--private-key-file` or `--private-key-path`.

These SnowSQL forms aren’t accepted:

- `-o` options, including `output_format`, `exit_on_error`, and `variable_substitution`.
- `--config`. The Snowflake CLI flag is `--config-file`.
- `--warehousename`. Use `--warehouse`. `warehousename` is a SnowSQL configuration key.

### Roll back to SnowSQL

Snowflake CLI uses its own configuration files, so you can continue to use SnowSQL unchanged.
You can install both SnowSQL and Snowflake CLI and run them independently.
If you set the alias in [Migrate your SnowSQL connections and settings](#label-cli-migration-connections), remove it to use the `snowsql` command for SnowSQL.

## Migrate your configurations

Tip

Useful links:

- [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect) documentation

### Differences in the configuration files

- SnowSQL

  SnowSQL is configured by its [configuration file](/user-guide/snowsql-config#label-configuring-snowsql), which is an INI-style file that contains connection configurations, various settings of the tool, and variables that can be used in SQL queries.
  Configurations can be split across several locations, which lets you define system-wide defaults and override them for different users.
  You can also specify configurations from custom locations with the `--config` command-line option.
  For more information, see [Connection parameters reference](/user-guide/snowsql-start#label-snowsql-connection-parameters).
- Snowflake CLI

  Snowflake CLI uses TOML [configuration files](/developer-guide/snowflake-cli/connecting/configure-cli) for connections and tool settings.
  By default, the configuration has no SQL `[variables]` section. For variables, use `-D` or `--variable` on `snow sql`, or define an `env` section in a `snowflake.yml` [project definition file](/developer-guide/snowflake-cli/project-definitions/use-sql-variables).
  `config.toml` lives in the directory described in [Location of the `.toml` configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations). That directory is `$SNOWFLAKE_HOME` when the variable is set and the directory exists. When `SNOWFLAKE_HOME` isn’t set, the directory is `~/.snowflake` if that directory exists. Otherwise it is a system directory: `~/.config/snowflake` on Linux, `~/Library/Application Support/snowflake` on macOS, or `%USERPROFILE%\AppData\Local\snowflake` on Windows.
  A `SNOWFLAKE_HOME` value that points at a missing directory is ignored, and Snowflake CLI doesn’t then use `~/.snowflake`. Create the directory first.
  If `connections.toml` exists in that directory, connections are read from it and connection entries in `config.toml` are ignored. `default_connection_name` is still read from `config.toml`.
  `--config-file` selects a specific `config.toml`. It doesn’t move `connections.toml`.
  Run `snow --info` and read `default_config_file_path` to see the file this installation uses.
  For more information, see [Location of the `.toml` configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations) and the [snow](/developer-guide/snowflake-cli/command-reference/snow) command reference.

### Find the Snowflake CLI default configuration file

The location of the default Snowflake CLI configuration depends on your system and is determined by the order specified in [Location of the `.toml` configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations).

- To find the value of the `default_config_file_path` parameter for your Snowflake CLI installation, run the `snow --info` command as shown:

  Copy code

  ```
  snow --info
  ```

  ```
  [
    ...

    {
     "key": "default_config_file_path",
     "value": "/<user_home>/.snowflake/config.toml"
    },

    ...
  ]
  ```

### Import connections from SnowSQL

Tip

Useful links:

- [Import connections from SnowSQL](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-import-connections-snowsql) documentation

You can import all of your SnowSQL connections with the `snow helpers import-snowsql-connections` command.
For more information, see [Import connections from SnowSQL](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-import-connections-snowsql) and the [snow helpers import-snowsql-connections](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections) command reference.

### Manually migrate the default connection configuration

If you choose not to import connections using the `snow helpers import-snowsql-connections` command, you can migrate the default connection manually.

Differences in specifying the default connection include the following:

- SnowSQL

  The default connection is configured in the SnowSQL [configuration file](/user-guide/snowsql-config#label-configuring-snowsql), and connection settings are defined directly in the [[connections]](/user-guide/snowsql-start#label-connecting-default-connection-settings) section.
- Snowflake CLI

  Named connections live under `[connections.<name>]` in the Snowflake CLI [configuration file](/developer-guide/snowflake-cli/connecting/configure-cli).
  Choose which one is default with the top-level `default_connection_name` setting, or run `snow connection set-default` (see [Set the default connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection)).

By default both SnowSQL and Snowflake CLI use the default connection configuration to connect to Snowflake. If you have it configured in SnowSQL, migrate it as follows.
If `connections.toml` exists, add the connection there as a top-level `[your_connection_name]` section. Connection entries you add under `[connections]` in `config.toml` are ignored while `connections.toml` exists. Set `default_connection_name` in `config.toml` either way.

1. Open the SnowSQL configuration file and find the default connection parameters in the `[connections]` section. You need the values of the connection parameters when adding the connection to Snowflake CLI.
2. To add the connection to Snowflake CLI, use one of the following methods:
   - Manually edit the configuration, as follows:

     1. Open `connections.toml` when that file exists. Otherwise open `config.toml`.
     2. Add the connection. In `connections.toml`, use a top-level `[your_connection_name]` section. In `config.toml`, use `[connections.your_connection_name]`. Copy the SnowSQL `[connections]` values into that section.
        The import also copies `login_timeout`, `client_session_keep_alive`, `ocsp_fail_open`, `insecure_mode`, and `client_store_temporary_credential` from `[options]` when `[connections]` omits them. Copying the connection yourself doesn’t include those values, so add them when you want them.
     3. Change the names of the following parameters, as shown:

        - `accountname` to `account`
        - `username` to `user`
        - `dbname` to `database`. `databasename` is a last-resort alias, not a SnowSQL key. Use it only when `database` and `dbname` aren’t set.
        - `schemaname` to `schema`
        - `warehousename` to `warehouse`
        - `rolename` to `role`
        - `pwd` to `password`
        - `private_key_path` to `private_key_file`
        - `private_key_file_pwd` to `private_key_passphrase`
        - `proxy_pwd` to `proxy_password`

        When both spellings are present, keep the Snowflake CLI name when it isn’t blank. A blank or whitespace-only value is skipped, so the next name is used. For example, `user=` with `username=alice` is saved as `user = "alice"`. The same rule applies to every pair in those bullets, including `password` or `pwd` and `private_key_path` or `private_key_file`. `private_key_path` wins over `private_key_file` when it has a value, and is saved as `private_key_file`. An `account` value isn’t replaced by `accountname`. For how the import command resolves a later blank across files, see [How keys are renamed](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections#label-snowcli-import-snowsql-keys).
        If you copy a private key and `authenticator` is absent, set `authenticator = "SNOWFLAKE_JWT"`. If `authenticator` is present and isn’t JWT, don’t copy `private_key_file` or `private_key_passphrase`. The comparison ignores case, so `snowflake_jwt` keeps the private key.
        Write integers and Booleans as described in [Values saved on the connection](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections#label-snowcli-import-snowsql-saved-values). If the value is left as the string `"false"`, the connector treats it as true.
     4. Add or set `default_connection_name = "your_connection_name"` at the top level of `config.toml`, including when the connection itself was written to `connections.toml` (see [Set the default connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection)).
   - Use the `snow connection add` and `snow connection set-default` commands.
     For more information, see [Manage or add your connections to Snowflake with the `snow connection` commands](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command).

### Manually migrate your named connection configurations

If you don’t use the `snow helpers import-snowsql-connections` command to import your connections, you can migrate them manually.

Differences in specifying named connections include the following:

- SnowSQL

  Named connections are configured in the SnowSQL [configuration file](/user-guide/snowsql-start#label-connecting-named-connection). Each named connection has its own `[connections.your_connection_name]` section.
- Snowflake CLI

  Snowflake CLI uses almost the same format to [configure named connections](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-define-connections). You can copy them from the SnowSQL configuration and rename the parameters as specified in the default connection.

Copy each named SnowSQL connection into Snowflake CLI.
If `connections.toml` exists, add each connection there as a top-level `[your_connection_name]` section. While `connections.toml` exists, Snowflake CLI ignores a `[connections.your_connection_name]` entry in `config.toml`.

1. Open the SnowSQL configuration file and locate the `[connections.your_connection_name]` sections. You need the values of the connection parameters when adding the [connections](#label-snowsql-migration-migrate-connections) to Snowflake CLI.
2. To add the connection to Snowflake CLI, use one of the following methods:
   - Manually edit the configuration, as follows:

     1. Open `connections.toml` when that file exists. Otherwise open `config.toml`.
     2. Add the connection. In `connections.toml`, use a top-level `[your_connection_name]` section. In `config.toml`, use `[connections.your_connection_name]`. Copy the SnowSQL `[connections.your_connection_name]` values into that section.
        Copying only `[connections.dev]` doesn’t include the account that lived on `[connections]`. The import doesn’t copy those unnamed keys onto a named connection either. Include the account and any other keys that lived only on the unnamed section. The import copies `login_timeout`, `client_session_keep_alive`, `ocsp_fail_open`, `insecure_mode`, and `client_store_temporary_credential` from `[options]` when the connection omits them. Copying the connection yourself doesn’t include those values, so add them when you want them.
     3. Rename the parameters as described in [Manually migrate the default connection configuration](#label-snowsql-migration-set-default-config).
   - Use the `snow connection add` command.
     For more information, see [Manage or add your connections to Snowflake with the `snow connection` commands](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command).

### Configure logs

Tip

Useful links:

- [Configure logging](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-configure-logging) documentation

To manually configure logging for Snowflake CLI, see [Configure logging](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-configure-logging).

### Migrate your variables

Tip

Useful links:

- [About project definition files](/developer-guide/snowflake-cli/project-definitions/about) documentation
- [Use variables in SQL](/developer-guide/snowflake-cli/project-definitions/use-sql-variables) documentation
- [Using variables for SQL templates](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-templating)

The default Snowflake CLI configuration file has no SQL `[variables]` section. Instead, pass variables on the command line with `-D` or `--variable` `key=value`, or define an `env` section in a `snowflake.yml` [project definition file](/developer-guide/snowflake-cli/project-definitions/about).

- Command-line variables such as `-D x=1` are referenced as `<% x %>`.
- Project `env` values are referenced as `<% ctx.env.name %>`. The `ctx.env` prefix applies only to project definition `env` values, not to `-D` variables.
- SnowSQL built-in variables aren’t supported.

The following example defines two project variables: `database` and `role`:

Copy code

```
definition_version: 2
env:
  database: "dev"
  role: "eng_rl"
```

### Manually migrate your environment variables

Tip

Useful links:

- [Use environment variables for Snowflake credentials](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-environment-creds) documentation
- [Support for system environment variables](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-env-var-support) documentation

In SnowSQL, you can use environment variables (like `$SNOWSQL_ACCOUNT` and `$SNOWSQL_DATABASE`) instead of specifying command-line parameters when starting a connection.
The default Snowflake CLI connection behavior doesn’t read `SNOWSQL_*` variables while connecting, including `SNOWSQL_REGION`. It also doesn’t read `SNOWFLAKE_REGION`.
`snow helpers check-snowsql-env-vars` only prints suggestions and doesn’t change the environment. Treat that output as a checklist. Some suggestions aren’t connection variables that the default Snowflake CLI connection behavior reads. For how the checker treats names, region, and proxy variables, see [snow helpers check-snowsql-env-vars](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-snowsql-env-vars). `SNOWFLAKE_ENHANCED_EXIT_CODES=1` enables `--enhanced-exit-codes` for Snowflake CLI commands. That variable isn’t a connection variable, and it isn’t SnowSQL `EXIT_ON_ERROR`. Use the following table for connection variables the default Snowflake CLI connection behavior reads. See also [Use environment variables for Snowflake credentials](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-environment-creds) and [Support for system environment variables](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-env-var-support).
A generic `SNOWFLAKE_*` variable in the table fills a parameter only when that parameter isn’t already set by a command-line flag or by the selected connection. With `--temporary-connection` (`-x`), no saved connection is loaded, so those variables supply the parameters.
To replace one key of a saved connection, set `SNOWFLAKE_CONNECTIONS_<NAME>_<KEY>`. `<NAME>` is the connection name in uppercase. `<KEY>` is the Snowflake CLI key, such as `ACCOUNT` or `PRIVATE_KEY_FILE`, rather than the SnowSQL name `ACCOUNTNAME`. The connection must already exist. This variable replaces that key from the file.
`PRIVATE_KEY_PASSPHRASE` is separate from the `SNOWFLAKE_*` variables. For an encrypted private key, it takes precedence over the passphrase stored on the connection.
A passphrase saved from the SnowSQL configuration file is used. `PRIVATE_KEY_PASSPHRASE` wins when it is set. `SNOWSQL_PRIVATE_KEY_PASSPHRASE` isn’t read.
SnowSQL stores the private key path in the configuration key `private_key_path`, not in a `SNOWSQL_*` environment variable. For that rename, see [How keys are renamed](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections#label-snowcli-import-snowsql-keys).

For the default Snowflake CLI behavior, migrate the following environment variables:

| SnowSQL | Snowflake CLI |
| --- | --- |
| `SNOWSQL_ACCOUNT` | `SNOWFLAKE_ACCOUNT` |
| `SNOWSQL_USER` | `SNOWFLAKE_USER` |
| `SNOWSQL_PWD` | `SNOWFLAKE_PASSWORD` |
| `SNOWSQL_DATABASE` | `SNOWFLAKE_DATABASE` |
| `SNOWSQL_SCHEMA` | `SNOWFLAKE_SCHEMA` |
| `SNOWSQL_WAREHOUSE` | `SNOWFLAKE_WAREHOUSE` |
| `SNOWSQL_ROLE` | `SNOWFLAKE_ROLE` |
| `SNOWSQL_HOST` | `SNOWFLAKE_HOST` |
| `SNOWSQL_PORT` | `SNOWFLAKE_PORT` |
| `SNOWSQL_PROTOCOL` | `SNOWFLAKE_PROTOCOL` |
| `SNOWSQL_REGION` | `SNOWFLAKE_ACCOUNT` (account identifier, not the region value) |
| `SNOWSQL_PRIVATE_KEY_PASSPHRASE` | `PRIVATE_KEY_PASSPHRASE` |

Expand

Show lessSee more

For `SNOWSQL_REGION`, put the [account identifier](/user-guide/admin-account-identifier) in `SNOWFLAKE_ACCOUNT` or on the imported connection’s `account`. Don’t copy the region name into the account. A region value already in the SnowSQL file is imported as `region`. The default Snowflake CLI doesn’t read `SNOWSQL_REGION` or `SNOWFLAKE_REGION` while connecting.

## Connect to Snowflake

Tip

Useful links:

- [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections) documentation
- [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) documentation

Assuming that you have migrated your configuration, you can connect to Snowflake from Snowflake CLI using methods similar to those used by SnowSQL, including the following:

- [Use the default connection](#label-snowsql-migration-default-connection).
- [Use a connection with command-line options](#label-snowsql-migration-default-and-options).
- [Use a named configuration](#label-snowsql-migration-named-connection).
- [Use only command-line options](#label-snowsql-migration-command-options-only).
- [Use environment variables](#label-snowsql-migration-connect-env-vars).
- [Use a mixture of connections, environment variables, and command-line options](#label-snowsql-migration-connection-mixed).

### Use the default connection

- To connect using the default configuration defined in your configuration file:
  - SnowSQL

    Copy code

    ```
    snowsql -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql -q "select 1"
    ```

### Use a connection with command-line options

- To connect using the default configuration defined in your configuration file and override parameters with command-line options:
  - SnowSQL

    Copy code

    ```
    snowsql --username myname -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql --username myname -q "select 1"
    ```

    For a list of possible command-line options, see [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql).
    Runtime connection flags override a connection for that command; they don’t save a connection the way `snow connection add` does.
    Some options have different names than in SnowSQL (for example, `--config-file` instead of `--config`).
    Both clients use `--warehouse`; Snowflake CLI doesn’t accept `--warehousename`.

### Use a named configuration

- To connect using a named configuration defined in your configuration file:
  - SnowSQL

    Copy code

    ```
    snowsql -c dev -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql -c dev -q "select 1"
    ```

### Use only command-line options

- To connect using only command-line options instead of a configured connection:
  - SnowSQL

    Copy code

    ```
    snowsql \
      --accountname myaccount \
      --username myuser \
      --authenticator SNOWFLAKE_JWT \
      --private-key-path "path_to_my_key" \
      -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql \
      --temporary-connection \
      --accountname myaccount \
      --username myuser \
      --authenticator SNOWFLAKE_JWT \
      --private-key-path "path_to_my_key" \
      -q "select 1"
    ```

    Note that Snowflake CLI requires the `--temporary-connection` (`-x`) option for this method.

### Use environment variables

- To connect using the default connection, passing some parameters as environment variables:
  - SnowSQL

    Copy code

    ```
    export SNOWSQL_USER=myuser
    snowsql -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    export SNOWFLAKE_USER=myuser
    snow sql -q "select 1"
    ```

    Note that the names of environment variables differ. For more information, see [Use environment variables for Snowflake credentials](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-environment-creds).

### Use a mixture of connections, environment variables, and command-line options

- To connect using a mixed approach with a named connection, environment variables, and command-line options:
  - SnowSQL

    Copy code

    ```
    export SNOWSQL_USER=myuser
    snowsql -c dev --accountname myaccount -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    export SNOWFLAKE_USER=myuser
    snow sql -c dev --accountname myaccount -q "select 1"
    ```

    You can use this method with both the default and named connections.

## Run SQL queries

Tip

Useful links:

- [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) documentation
- [Executing SQL statements](/developer-guide/snowflake-cli/sql/execute-sql) documentation

You can run [PUT](/sql-reference/sql/put) and [GET](/sql-reference/sql/get) with `snow sql` the same way you run other SQL
statements. For interactive SQL, enter `snow sql` with no `-q` or `-f` option. For details, see
[Entering SQL commands in interactive mode](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-interactive-mode).

### Run SQL queries from various inputs

Snowflake CLI lets you run SQL queries using inputs similar to those handled by SnowSQL. The following examples run SQL queries using various inputs.

- Run queries using command-line parameters:

  - SnowSQL

    Copy code

    ```
    snowsql -q "select 1"
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql -q "select 1"
    ```
- Run queries from a file (`-f` is repeatable in Snowflake CLI):

  - SnowSQL

    Copy code

    ```
    snowsql -f test.sql
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql -f test.sql
    ```
- Run queries from standard input:

  - SnowSQL

    Copy code

    ```
    cat test.sql | snowsql
    ```
  - Snowflake CLI

    Copy code

    ```
    cat test.sql | snow sql --stdin
    ```

Note

`--stdin` (`-i`) is required. `cat test.sql | snow sql` doesn’t run the file. With no `-q`, `-f`, or `--stdin`, the command reads standard input and then still enters the REPL. That decision is made before the read, so the piped text is discarded. The REPL sees an empty standard input, and the session ends when it reaches the end of that input. The SQL isn’t executed. The `snowsql` alias in [Migrate your SnowSQL connections and settings](#label-cli-migration-connections) doesn’t make `cat test.sql | snowsql` run the file either.

### Save query results to a file

Snowflake CLI doesn’t support every [SnowSQL output formatting option](/user-guide/snowsql-use#label-snowsql-export-data).
Supported `--format` values are `TABLE`, `JSON`, `JSON_EXT`, and `CSV`. There is no `-o output_file` equivalent; use shell redirection.

- SnowSQL

  Copy code

  ```
  snowsql \
    -f test.sql \
    -o "output_format=json" \
    -o "output_file=result.json"
  ```
- Snowflake CLI

  Copy code

  ```
  snow sql -f test.sql --format json > result.json
  snow sql -f test.sql --format csv > result.csv
  ```

### Run queries using variables

Both SnowSQL and Snowflake CLI let you use variables in queries. SnowSQL lets you use variables from command-line options, from its configuration file, and using a few [built-in variables](/user-guide/snowsql-use#label-snowsql-variables).
Snowflake CLI doesn’t support variables in its configuration file or SnowSQL built-in variables. It does support `-D` or `--variable` on the command line and `env` values in project definition files. For information about migrating your SnowSQL configuration file variables, see [Migrate your variables](#label-snowsql-migration-variables).

After migrating your variables from SnowSQL’s configuration, you can run Snowflake CLI queries using variables from both command-line options and project definitions.

When using variables, note the following important differences between SnowSQL and Snowflake CLI:

- They use different syntaxes for variable substitutions. SnowSQL uses the `&variable` or `&{variable}` syntax while Snowflake CLI uses `<% variable %>`. The SnowSQL syntax remains accepted by default, but is deprecated.
- Snowflake CLI automatically enables variable substitution, so you don’t need to explicitly enable it as with SnowSQL.
- Project definition `env` values must be prefixed with `ctx.env`, as shown. Command-line `-D` variables aren’t under `ctx.env`.

The following examples show the differences when running SQL queries with variables:

- Run a query using variables in command-line options, where `x` is the variable name:

  - SnowSQL

    Copy code

    ```
    snowsql \
      -o variable_substitution=true \
      -q "select &x" \
      -D x=1
    ```
  - Snowflake CLI

    Copy code

    ```
    snow sql \
      -q "select <% x %>" \
      -D x=1
    ```
  - Snowflake CLI (using deprecated syntax to facilitate quick migrations)

    Copy code

    ```
    snow sql \
      -q "select &x" \
      -D x=1
    ```
- Run a query using variables in a SnowSQL configuration versus a Snowflake CLI project definition file:

  - SnowSQL

    Copy code

    ```
    # save variables to config
    echo "[variables]
    xyz=Hello World" > custom_config

    # run query
    snowsql \
      --config custom_config \
      -o variable_substitution=true \
      -q "select '&{xyz}'"
    ```
  - Snowflake CLI

    Copy code

    ```
    # save variables to project definition
    echo "definition_version: 2
    env:
      xyz: Hello World" > snowflake.yml

    # run query
    snow sql -q "select '<% ctx.env.xyz %>'"
    ```
  - Snowflake CLI (using deprecated syntax to facilitate quick migrations)

    Copy code

    ```
    # save variables to project definition
    echo "definition_version: 2
    env:
      xyz: Hello World" > snowflake.yml

    # run query
    snow sql -q "select '&{ctx.env.xyz}'"
    ```

### Run queries asynchronously

End a statement with `;>` instead of `;` to schedule it without waiting. This works in the REPL and in noninteractive input (`-q`, `-f`, or `--stdin`). Snowflake CLI prints a `scheduled query ID`. After the query finishes, retrieve the result with `!result <query_id>` or [RESULT\_SCAN](/sql-reference/functions/result_scan).
`!queries`, `!result`, and `!abort` work in the REPL and in `snow sql` input (`-q`, `-f`, and `--stdin`). `!edit` fails outside the REPL. The command prints `The edit command can only be used in interactive mode.`
For details, see [Executing SQL queries asynchronously](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-async).

Copy code

```
snow sql -q "select 'async example';>"
snow sql -q '!result <query_id>'
```

## SnowSQL and Snowflake CLI feature parity

The following table shows how SnowSQL features are integrated into Snowflake CLI.

**SnowSQL and Snowflake CLI feature parity**

| SnowSQL feature | Snowflake CLI implementation |
| --- | --- |
| Global configuration file (`~/.snowsql/config`) in an INI-style format. | Configuration uses TOML. For the directory, `connections.toml`, and `--config-file`, see [Location of the `.toml` configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations). |
| Connection configuration through command-line options supports everything the Snowflake Connector for Python supports. | Runtime connection flags on commands such as `snow sql` override the connection for that run; they don’t save a connection. To save a connection, use [snow connection add](/developer-guide/snowflake-cli/command-reference/connection-commands/add-connection). |
| Connection testing via the `--probe-connection` command-line option. This option is mainly used to print out the TLS/SSL certificate chain. | `snow connection test` tests whether a session can be created. `--enable-diag` writes a diagnostic report; `--print-diag` prints that diagnostic. This isn’t a drop-in TLS chain dump. For more information, see [snow connection test](/developer-guide/snowflake-cli/command-reference/connection-commands/test-connection). |
| Ability to generate and display a JWT token based on the `user`, `account`, and `private-key-path` parameters. | Use the `snow connection generate-jwt` command. For more information, see [snow connection generate-jwt](/developer-guide/snowflake-cli/command-reference/connection-commands/generate-jwt). |
| Execute a query from a file using the `-f` or `--filename FILE` options. | Use `snow sql -f` or `--filename`. The option is repeatable. |
| Execute a query from command-line input using the `-q` or `--query TEXT` options. | Use `snow sql -q` or `--query`; for example, `snow sql -q "select emp_id FROM employees"`. |
| Query templating with the option to provide variables using the `--variable` command-line option, such as `--variable db_key=$DB_KEY`. | Snowflake CLI supports `-D` or `--variable` and `snowflake.yml` `env` values (`<% ctx.env.name %>`). For more information, see [Using variables for SQL templates](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-templating) and [Storing variables in the `snowflake.yml` project definition file](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-env-vars). |
| [Interactive SQL shell mode](/user-guide/snowsql-use#label-using-commands). | Use [interactive mode](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-interactive-mode). The REPL and noninteractive `snow sql` both accept `;>` to schedule a query and print its query ID. `!queries`, `!result`, and `!abort` work in the REPL and in noninteractive input. `!edit` fails outside the REPL. The command prints `The edit command can only be used in interactive mode.` |
| Include, or source, one or more SQL files from another SQL file:  Copy code  ``` !source file1.sql; !source file2.sql; !source http://example.com/my.sql ``` | `!source` and `!load` are supported. Snowflake CLI fetches `https://` URLs. A plaintext `http://` URL is rejected before any fetch, and the command prints `Plaintext http:// sources are not allowed`. An `https://` URL that redirects to `http://` is rejected too. Local-only mode (`--local-only`, `SNOWFLAKE_CLI_SQL_LOCAL_ONLY`, or `cli.sql_local_only`) blocks `https://` URLs, and the command prints `Loading SQL from URLs is disabled (--local-only)`. For more information, see [Working with SQL query commands](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-query-commands). |
| Stop after a SQL error (`-o exit_on_error=true`). | In noninteractive `snow sql`, a failed SQL statement stops the command and returns a nonzero exit code. There is no continue-on-error switch. For exit codes, see [Enhanced error codes](/developer-guide/snowflake-cli/command-reference/sql-commands/sql#label-snowcli-enhanced-error-codes). |

Expand

Show lessSee more
