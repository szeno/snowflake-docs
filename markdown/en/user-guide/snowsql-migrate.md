# Migrating from SnowSQL to Snowflake CLI

Note

Snowflake CLI migration support is still in development. In the meantime, Snowflake encourages you to migrate from SnowSQL using these instructions.

This guide provides instructions for migrating from SnowSQL to Snowflake CLI to help you seamlessly move your existing SnowSQL connections and environment variables.

- [Migration steps](#label-snowsql-migration-migrate-connections)
- [Migrate your configurations](#label-snowsql-migration-migrate-configurations)
- [Connect to Snowflake](#label-snowsql-migration-connect-to-snowflake)
- [Executing SQL queries](#label-snowsql-migration-execute-sql)

## Migration steps

To migrate from SnowSQL to Snowflake CLI, follow these steps:

1. [Install Snowflake CLI](#label-cli-migration-install) with your preferred method.
2. [Import your connections](#label-cli-migration-connections).
3. Optionally check for suggested changes for your environment variables.
4. Optionally create an alias that maps the `snowsql` shell command to the `snow sql` shell command.

### Install the Snowflake CLI software

Tip

Useful links:

- [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) documentation
- [Snowflake CLI binaries repository](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html)

Similarly to SnowSQL, Snowflake CLI provides [binary installers](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-package-managers). Additionally, it also lets you install the software using [homebrew](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-homebrew) and [pip](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-pip).

Currently, Snowflake CLI supports the following platforms:

- macOS (arm)

  - [Package installer](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-macos-installer)
  - [Homebrew](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-homebrew)
  - [PyPi (pip)](/developer-guide/snowflake-cli/installation/installation#label-snowcli-advanced-install)
- macOS (x86\_64):

  - [Package installer](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-macos-installer)
  - [Homebrew](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-homebrew)
  - [PyPi (pip)](/developer-guide/snowflake-cli/installation/installation#label-snowcli-advanced-install)
- Linux (x86\_64 & aarch64):

  - [deb package installer](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-linux-package-managers)
  - [rpm package installer](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-linux-package-managers)
  - [PyPi (pip)](/developer-guide/snowflake-cli/installation/installation#label-snowcli-advanced-install)
- Windows (64bit):

  - [Installer](/developer-guide/snowflake-cli/installation/installation#label-snowcli-install-windows-installer)
  - [PyPi (pip)](/developer-guide/snowflake-cli/installation/installation#label-snowcli-advanced-install)

Currently, Snowflake CLI does not support the following platform:

- Linux bash installer

For more information about installing Snowflake CLI, see [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).

### Migrate your SnowSQL connections and settings

Snowflake CLI provides a [snow helpers](/developer-guide/snowflake-cli/command-reference/helpers-commands/overview) command group to simplify the process of transitioning from SnowSQL to Snowflake CLI.
Use these commands to easily import your existing connections and your environment variables:

- The [snow helpers import-snowsql-connections](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections) command uses an interactive menu to let you choose which SnowSQL connections you want to import.
  For more information, see [Import connections from SnowSQL](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-import-connections-snowsql).
- The [snow helpers check-snowsql-env-vars](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-snowsql-env-vars) command helps you diagnose which environment variables are set in your SnowSQL environment and displays their corresponding Snowflake CLI equivalents.
  For more information, see [Use variables in SQL](/developer-guide/snowflake-cli/project-definitions/use-sql-variables).

If you use SnowSQL to execute inline SQL statements or execute files but do not want to edit all your scripts, consider creating an alias that maps `snowsql` to the `snow sql` command. For example, on Unix-like systems, use the following command:

Copy code

```
alias snowsql='snow sql'
```

With this alias, you can use your existing scripts with Snowflake CLI.

Note that if you are a more advanced SnowSQL user, you might occasionally encounter incompatibility messages, which typically relate to options used for configuring SnowSQL.
Because Snowflake CLI doesn’t use all of the SnowSQL configuration options, you might need to make copies of your scripts and remove those incompatible options.

### Roll back to SnowSQL

Snowflake CLI uses its own configuration files, so you can continue to use SnowSQL.
You can install both SnowSQL and Snowflake CLI and run them independently.
If you set an alias, as described above, you must remove the alias to use the `snowsql` command for SnowSQL.

## Migrate your configurations

Tip

Useful links:

- [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect) documentation

### Differences in the configuration files

- SnowSQL

  SnowSQL is configured by its [configuration file](/user-guide/snowsql-config#label-configuring-snowsql), which is a file in TOML format that contains connection configurations, various settings of the tool, and variables that can be used in SQL queries.
  Configurations can be split into several locations, which lets you define system-wide defaults and override them for different users.
  You can also specify configurations from custom locations by specifying the `--config` command-line option.
  For more information, see [Connection parameters reference](/user-guide/snowsql-start#label-snowsql-connection-parameters).
- Snowflake CLI

  Snowflake CLI also has its own TOML [configuration file](/developer-guide/snowflake-cli/connecting/configure-cli) that specifies connection configurations and settings of the tool.
  It does not allow you to define variables for later use in SQL queries. Variables in Snowflake CLI are defined at the project level in [project definition files](/developer-guide/snowflake-cli/project-definitions/use-sql-variables).
  Snowflake CLI uses only one configuration file that, by default, is located in the user’s home directory.
  You can also specify configurations from custom locations by specifying the `--config` command-line option.
  For more information, see the [snow](/developer-guide/snowflake-cli/command-reference/snow) command reference.

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

  The default connection is configured in the Snowflake CLI [configuration file](/developer-guide/snowflake-cli/connecting/configure-cli) as a named connection with the name `default_connection_name`, set at the top level of configuration (see [Set the default connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection)).
  You can change the default connection by using the `snow connection set-default` command.

By default both SnowSQL and Snowflake CLI use the default connection configuration to connect to Snowflake. If you have it configured in SnowSQL, you should migrate this configuration to the Snowflake CLI configuration file, as follows:

1. Open the SnowSQL configuration file and find the default connection parameters in the `[connections]` section. You need the values of the connection parameters when adding the connection to Snowflake CLI.
2. To add the connection to Snowflake CLI, use one of the following methods:
   - Manually edit the Snowflake CLI configuration file, as follows:

     1. Open the Snowflake CLI configuration file.
     2. Add a `[connections.your_connection_name]` section and copy/paste the default configuration details from the SnowSQL configuration file.
     3. Change the names of the following parameters, as shown:

        - `accountname` to `account`
        - `username` to `user`
        - `dbname` to `database`
        - `schemaname` to `schema`
        - `warehousename` to `warehouse`
        - `rolename` to `role`
     4. Add or set `default_connection_name = "your_connection_name"` setting at the top level of the configuration file (see [Set the default connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection)).
   - Use the `snow connection add` and `snow connection set-default` commands.
     For more information, see [Manage or add your connections to Snowflake with the `snow connection` commands](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command).

### Manually migrate your named connection configurations

If you don’t use the `snow helpers import-snowsql-connections` command to import your connections, you can migrate them manually.

Differences in specifying named connections include the following:

- SnowSQL

  Named connections are configured in the SnowSQL [configuration file](/user-guide/snowsql-start#label-connecting-named-connection). Each named connection has its own `[connections.your_connection_name]` section.
- Snowflake CLI

  Snowflake CLI uses almost the same format to [configure named connections](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-define-connections). You can copy them from the SnowSQL configuration and rename the parameters as specified in the default connection.

By default both SnowSQL and Snowflake CLI let you use a named connection to connect to Snowflake. If you want to continue using those named connections in SnowSQL, you should migrate them to the Snowflake CLI configuration file:

1. Open the SnowSQL configuration file and locate the `[connections.your_connection_name]` sections. You need the values of the connection parameters when adding the [connections](#label-snowsql-migration-migrate-connections) to Snowflake CLI.
2. To add the connection to Snowflake CLI, use one of the following methods:
   - Manually edit the Snowflake CLI configuration file, as follows:

     1. Open the Snowflake CLI configuration file.
     2. Add a `[connections.your_connection_name]` section and copy/paste the default configuration details from the SnowSQL configuration file.
     3. Change the names of the following parameters, as shown:
        - `accountname` to `account`
        - `username` to `user`
        - `dbname` to `database`
        - `schemaname` to `schema`
        - `warehousename` to `warehouse`
        - `rolename` to `role`
   - Use the `snow connection add` command.
     For more information, see [Manage or add your connections to Snowflake with the `snow connection` commands](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command).

### Configure logs

Tip

Useful links:

- [Configure logging](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-configure-logging) documentation

To manually configure logging for Snowflake CLI, see the [Configure logging](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-configure-logging) documentation.

### Migrate your variables

Tip

Useful links:

- [About project definition files](/developer-guide/snowflake-cli/project-definitions/about) documentation
- [Use variables in SQL](/developer-guide/snowflake-cli/project-definitions/use-sql-variables) documentation

Snowflake CLI doesn’t support specifying variables in its configuration file. Instead, it uses a more project-focused approach that associates variables with specific projects. Snowflake CLI lets you define variables in `snowflake.yml` [project definition files](/developer-guide/snowflake-cli/project-definitions/about). You can then use these variables in SQL queries as described in [About project definition files](/developer-guide/snowflake-cli/project-definitions/about).

- To define variables for your project, add an `env` section to the project’s `snowflake.yml` file and include any variables you want to use in your queries.

The following example defines two variables: `database` and `role`:

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
- [Use variables in SQL](/developer-guide/snowflake-cli/project-definitions/use-sql-variables) documentation

In SnowSQL, you can use environment variables (like `$SNOWSQL_ACCOUNT` and `$SNOWSQL_DATABASE`) instead of specifying command-line parameters when starting a connection.
This approach provides another way to specify default connection configurations. Snowflake CLI offers the same functionality but uses different names for these parameters and allows you to override many more configuration parameters via environment variables.
If you’re using environment variables to connect to Snowflake, for more information, see [connecting to Snowflake with environment variables](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-environment-creds). Also, see information about possibilities for [configuring environment variables](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-env-var-support) in the Snowflake CLI documentation.

## Connect to Snowflake

Tip

Useful links:

- [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections) documentation
- [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) documentation

Assuming that you have migrated your configuration, you can connect to Snowflake from Snowflake CLI using similar methods to these used by SnowSQL, including the following:

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

    For a list of possible command-line options, see [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql). Note that some options have different names than in SnowSQL.

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

    Note that Snowflake CLI requires the `--temporary-connection` option for this method.

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

    Note that the names of environment variables might differ. For more information, see [Use environment variables for Snowflake credentials](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-environment-creds).

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

## Executing SQL queries

Tip

Useful links:

- [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) documentation
- [Executing SQL statements](/developer-guide/snowflake-cli/sql/execute-sql) documentation

### Execute SQL queries from various inputs

Snowflake CLI lets you execute SQL queries using inputs similar to these handled by SnowSQL. The following examples execute SQL queries using various inputs.

- Execute queries using command-line parameters:

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
- Execute queries from a file:

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
- Execute queries from standard input:

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

### Save query results to a JSON file

Snowflake CLI currently does not support all of the [SnowSQL output formatting options](/user-guide/snowsql-use#label-snowsql-export-data). Snowflake CLI does let you save query results as either a formatted table or as JSON. Although CSV and other formats are not yet available, you can use external tools, such as [jq](https://jqlang.org/), to convert data from JSON other formats.

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
  ```

### Execute queries using variables

Both SnowSQL and Snowflake CLI let you use variables in queries. SnowSQL lets you use variables from command-line options, from its configuration file, and using a few [built-in variables](/user-guide/snowsql-use#label-snowsql-variables). Although Snowflake CLI does not support variables in its configuration file or using built-in variables, it does support specifying parameters with command-line options and specifying variables in project definition files. For information about migrating your SnowSQL configuration file variables, see [Migrate your variables](#label-snowsql-migration-variables).

After migrating your variables from SnowSQL’s configuration, you can run Snowflake CLI queries using variables from both command-line options and project definitions.

When using variables, note the following important differences between SnowSQL and Snowflake CLI:

- They use different syntaxes for variable substitutions. SnowSQL uses the `&variable` or `&{variable}` syntax while Snowflake CLI uses `<% variable %>`. The syntax from SnowSQL is currently supported, but has been deprecated.
- Snowflake CLI automatically enables variable substitution, so you do not need to explicitly enable it as with SnowSQL.
- Variable names in Snowflake CLI project definition files must be prefixed with `ctx.env`, as shown:

The following examples show the differences when executing SQL queries with variables:

- Execute a query using variables in command-line options, where `x` is the variable name:

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
- Execute a query using variables in a SnowSQL configuration versus a Snowflake CLI project definition file:

  - SnowSQL

    Copy code

    ```
    # save variables to config
    echo "[variables]
    xyz=Hello World" > custom_config

    # execute query
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

    # execute query
    snow sql -q "select '<% ctx.env.xyz %>'"
    ```
  - Snowflake CLI (using deprecated syntax to facilitate quick migrations)

    Copy code

    ```
    # save variables to project definition
    echo "definition_version: 2
    env:
      xyz: Hello World" > snowflake.yml

    # execute query
    snow sql -q "select '&{ctx.env.xyz}'"
    ```

## SnowSQL and Snowflake CLI feature parity

The following table shows how SnowSQL features are integrated into Snowflake CLI.

**SnowSQL and Snowflake CLI feature parity**

| SnowSQL feature | Snowflake CLI implementation |
| --- | --- |
| Global configuration file (`~/.snowsql/config`) in a `.ini` format. | Configuration and connection files use a TOML format and are stored in the `~/.snowflake` directory (Linux) or in another subdirectory in the user’s HOME directory (other OS systems). For more information, see [Location of the `.toml` configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations). |
| Connection configuration through command-line options supports everything the Snowflake Connector for Python supports. | Snowflake CLI supports the command-line options as described in the [snow connection add](/developer-guide/snowflake-cli/command-reference/connection-commands/add-connection) command reference. |
| Connection testing via the `--probe-connection` command-line option. This option is mainly used to print out the TLS/SSL certificate chain. | Currently, the `snow connection test` command does the connection probe but does not print the TLS/SSL certificate chain. You can generate connection diagnostic data for Snowflake Support. |
| Ability to generate and display a JWT token based on the `user`, `account`, and `private-key-path` parameters. | Use the `snow connection generate-jwt` command. For more information, see [Use a private key file for authentication](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-private-key). |
| Execute a query from a file using the `-f` or `--filename FILE` options. | Use the `snow sql [-f/--filename] file.sql` command. |
| Execute a query from command-line input using the `-q` or `--query TEXT` options. | Use the `snow sql [-q/--query] "<query-text>"` command; for example, `snow sql -q "select emp_id FROM employees"`. |
| Query templating with the option to provide variables using the `--variable` command-line option, such as `--variable db_key=$DB_KEY`. | Snowflake CLI supports SQL variables in SQL templates and in snowflake.yml project definition files. For more information, see [Using variables for SQL templates](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-templating) and [Storing variables in the `snowflake.yml` project definition file](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-env-vars). |
| [Interactive SQL shell mode](/user-guide/snowsql-use#label-using-commands). | Use [interactive mode](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-interactive-mode). Support for asynchronous queries will be added at a later date. |
| Include, or source, one or more SQL files from another SQL file:  Copy code  ``` !source file1.sql; !source file2.sql; !source http://example.com/my.sql ``` | Snowflake CLI supports nesting SQL scripts with template support. For more information, see [Working with SQL query commands](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-query-commands). |
| Display EXIT\_ON\_ERROR error codes. | Use the `--enhanced-exit-codes` command-line option, or set the `SNOWFLAKE_ENHANCED_EXIT_CODES` environment variable to `1` to send the enhanced return codes for all `snow sql` commands. For more information, see [Enhanced error codes](/developer-guide/snowflake-cli/command-reference/sql-commands/sql#label-snowcli-enhanced-error-codes). |

Expand

Show lessSee more
