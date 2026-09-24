# Configuring SnowSQL

Caution

[Snowflake CLI](/developer-guide/snowflake-cli/index) is the preferred command-line client for new installs and new work. SnowSQL is a
legacy command-line client. Snowflake will only add new features and enhancements to Snowflake CLI. Snowflake supports SnowSQL 1.5.x through
April 16, 2028. Earlier minor versions have earlier support end dates.

If you’re starting a new project, [install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). If you already use
SnowSQL, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

This topic describes how to configure SnowSQL using connection parameters, configuration options, and variables.

## About the SnowSQL `config` file

SnowSQL supports multiple configuration files that allow organizations to define base values for connection parameters,
default settings, and variables while allowing individual users to customize their personal settings in their
own `<HOME_DIR>/.snowsql/config` files. When SnowSQL starts, it loads configuration parameter values from the following
configuration file locations in order, overriding values from files loaded previously:

- `/etc/snowsql.cnf`
- `/etc/snowflake/snowsql.cnf`
- `/usr/local/etc/snowsql.cnf`
- `<HOME_DIR>/.snowsql.cnf` (supported only for backward compatibility)
- `<HOME_DIR>/.snowsql/config`

For example, if the `/etc/snowsql.cnf` configuration file sets the `log_level` parameter to `info`, you can override this by setting the parameter to `debug` in your file `<HOME_DIR>/.snowsql/config` file.

The `snowsql` command generates a configuration file similar to the following the first time you execute the command.

Copy code

```
[connections]
# *WARNING* *WARNING* *WARNING* *WARNING* *WARNING* *WARNING*
#
# The Snowflake user password is stored in plain text in this file.
# Pay special attention to the management of this file.
# Thank you.
#
# *WARNING* *WARNING* *WARNING* *WARNING* *WARNING* *WARNING*

#If a connection doesn't specify a value, it will default to these
#
#accountname = defaultaccount
#region = defaultregion
#username = defaultuser
#password = defaultpassword
#dbname = defaultdbname
#schemaname = defaultschema
#warehousename = defaultwarehouse
#rolename = defaultrolename
#proxy_host = defaultproxyhost
#proxy_port = defaultproxyport

[connections.example]
#Can be used in SnowSql as #connect example

accountname = my_organization-my_account
username = username
password = password1234

[variables]
# SnowSQL defines the variables in this section on startup.
# You can use these variables in SQL statements. For details, see
# https://docs.snowflake.com/en/user-guide/snowsql-use.html#using-variables

# example_variable=27

[options]
# If set to false auto-completion will not occur interactive mode.
auto_completion = True

# main log file location. The file includes the log from SnowSQL main
# executable.
log_file = ~/.snowsql/log

# bootstrap log file location. The file includes the log from SnowSQL bootstrap
# executable.
# log_bootstrap_file = ~/.snowsql/log_bootstrap

# Default log level. Possible values: "CRITICAL", "ERROR", "WARNING", "INFO"
# and "DEBUG".
log_level = INFO

# Timing of sql statements and table rendering.
timing = True

# Table format. Possible values: psql, plain, simple, grid, fancy_grid, pipe,
# orgtbl, rst, mediawiki, html, latex, latex_booktabs, tsv.
# Recommended: psql, fancy_grid and grid.
output_format = psql

# Keybindings: Possible values: emacs, vi.
# Emacs mode: Ctrl-A is home, Ctrl-E is end. All emacs keybindings are available in the REPL.
# When Vi mode is enabled you can use modal editing features offered by Vi in the REPL.
key_bindings = emacs

# OCSP Fail Open Mode.
# The only OCSP scenario which will lead to connection failure would be OCSP response with a
# revoked status. Any other errors or in the OCSP module will not raise an error.
# ocsp_fail_open = True

# Enable temporary credential file for Linux users
# For Linux users, since there are no OS-key-store, an unsecure temporary credential for SSO can be enabled by this option. The default value for this option is False.
# client_store_temporary_credential = True

# Select statement split method (default is to use the sql_split method in snowsql, which does not support 'sql_delimiter')
# sql_split = snowflake.connector.util_text # to use connector's statement_split which has legacy support to 'sql_delimiter'.

# Force the result data to be decoded in utf-8. By default the value is set to false for compatibility with legacy data. It is recommended to set the value to true.
# json_result_force_utf8_decoding = False
```

You should create these configuration files using UTF-8 encoding.

## Modify the SnowSQL configuration file

To modify the configuration file:

1. Open the SnowSQL configuration file (named `config`) in a text editor. The default location of the file is:

   Linux/macOS:
   :   `~/.snowsql/`

   Windows:
   :   `%USERPROFILE%\.snowsql\`

   Note

   You can change the default location by specifying the `--config path` command-line flag when starting SnowSQL.
2. Modify settings in the following sections:

   - [Connection Parameters Section](#connection-parameters-section)
   - [Configuration Options Section](#configuration-options-section)
   - [Variables Section](#variables-section)

Attention

- The password is stored in plain text in the `config` file. You must explicitly secure the file to restrict access. For example, in Linux or macOS, you can set the read permissions to you
  alone by running `chmod`:

  Copy code

  ```
  $ chmod 700 ~/.snowsql/config
  ```

Note

- If a value contains special characters (other than single or double quotes), you must enclose it in either single quotes or double quotes, e.g.:

  Copy code

  ```
  password = "my$^pwd"
  ```
- If a value contains quote characters *in addition to* other special characters, escape these quotes using the backslash (`\`) character, e.g.:

  Copy code

  ```
  password = "my$^\"\'pwd"
  ```

  Note that escaping quote characters is optional in unenclosed values (i.e. values that do not contain other special characters).
- Multi-line values must be enclosed in three single or double quotes (`'''` or `"""`), e.g.:

  Copy code

  ```
  prompt_format='''[#FFFF00][user]@[account]
  [#00FF00]> '''
  ```

### Connection parameters section

In the `[connections]` section of the `config` file, optionally set the default connection parameters for SnowSQL,
e.g. account identifier, user login credentials, and the default database and warehouse.
You can also define *named* connections to make multiple simultaneous connections to Snowflake or store different sets of connection configurations.

For more information, see [Connecting through SnowSQL](/user-guide/snowsql-start).

### Configuration options section

Configure the behavior of SnowSQL by adding settings in the `[options]` section of the `config` file:

> Copy code
>
> ```
> [options]
> <option_name> = <option_value>
> ```

Where:

- `<option_name>` is the name of the option (case-insensitive). If an invalid name is specified, SnowSQL displays an error.
- `<option_value>` specifies a supported value (case-insensitive) for the option, as described below.

Copy code

```
+----------------------------+---------------------+------------------------------------------------------------------------------------+
| Name                       | Value               | Help                                                                               |
+----------------------------+---------------------+------------------------------------------------------------------------------------+
| auto_completion            | True                | Displays auto-completion suggestions for commands and Snowflake objects.           |
| client_session_keep_alive  | False               | Keeps the session active indefinitely, even if there is no activity from the user. |
| echo                       | False               | Outputs the SQL command to the terminal when it is executed.                       |
| editor                     | vim                 | Changes the editor to use for the !edit command.                                   |
| empty_for_null_in_tsv      | False               | Outputs an empty string for NULL values in TSV format.                             |
| environment_variables      | ['PATH']            | Specifies the environment variables that can be referenced as SnowSQL variables.   |
|                            |                     | The variable names should be comma separated.                                      |
| execution_only             | False               | Executes queries only.                                                             |
| exit_on_error              | False               | Quits when SnowSQL encounters an error.                                            |
| fix_parameter_precedence   | True                | Controls the precedence of the environment variable and the config file entries    |
|                            |                     | for password, proxy password, and private key phrase.                              |
| force_put_overwrite        | False               | Force PUT command to stage data files without checking whether already exists.     |
| friendly                   | True                | Shows the splash text and goodbye messages.                                        |
| header                     | True                | Outputs the header in query results.                                               |
| insecure_mode              | False               | Turns off OCSP certificate checks.                                                 |
| key_bindings               | emacs               | Changes keybindings for navigating the prompt to emacs or vi.                      |
| log_bootstrap_file         | ~/.snowsql/log_...  | SnowSQL bootstrap log file location.                                               |
| log_file                   | ~/.snowsql/log      | SnowSQL main log file location.                                                    |
| log_level                  | CRITICAL            | Changes the log level (critical, debug, info, error, warning).                     |
| login_timeout              | 120                 | Login timeout in seconds.                                                          |
| noup                       | False               | Turns off auto upgrading SnowSQL.                                                  |
| output_file                | None                | Writes output to the specified file in addition to the terminal.                   |
| output_format              | psql                | Sets the output format for query results.                                          |
| paging                     | False               | Enables paging to pause output per screen height.                                  |
| progress_bar               | True                | Shows progress bar while transferring data.                                        |
| prompt_format              | [user]#[warehou...] | Sets the prompt format. Experimental feature, currently not documented.            |
| sfqid                      | False               | Turns on/off Snowflake query id in the summary.                                    |
| sfqid_in_error             | False               | Turns on/off Snowflake query id in the error message.                              |
| quiet                      | False               | Hides all output.                                                                  |
| remove_comments            | False               | Removes comments before sending query to Snowflake.                                |
| remove_trailing_semicolons | True                | Removes trailing semicolons from SQL text before sending queries to Snowflake.     |
| results                    | True                | If set to off, queries will be sent asynchronously, but no results will be fetched.|
|                            |                     | Use !queries to check the status.                                                  |
| rowset_size                | 1000                | Sets the size of rowsets to fetch from the server.                                 |
|                            |                     | Set the option low for smooth output, high for fast output.                        |
| stop_on_error              | False               | Stops all queries yet to run when SnowSQL encounters an error.                     |
| syntax_style               | default             | Sets the colors for the text of SnowSQL.                                           |
| timing                     | True                | Turns on/off timing for each query.                                                |
| timing_in_output_file      | False               | Includes timing in the output file.                                                |
| variable_substitution      | False               | Substitutes variables (starting with '&') with values.                             |
| version                    | 1.1.70              | Returns SnowSQL version.                                                           |
| wrap                       | True                | Truncates lines at the width of the terminal screen.                               |
+----------------------------+---------------------+------------------------------------------------------------------------------------+
```

See [SnowSQL configuration options reference](#label-snowsql-options) (in this topic) for descriptions of all valid options.

Note

In addition to setting the configuration options in the `config` file, you can set the options using either of the following methods:

- While connecting to Snowflake, you can use the `-o` or `--option` connection parameter to set these options. For more information, see [Connection parameters reference](/user-guide/snowsql-start#label-snowsql-connection-parameters).
- After connecting to Snowflake, you can use the `!set` command to set these options for the session. For more information, see [Commands reference](/user-guide/snowsql-use#label-snowsql-commands).

### Variables section

In the `[variables]` section of the `config` file, you can store values as variables for reuse. This feature enables you to use user-defined and database values in queries.

For more information, see [Using variables](/user-guide/snowsql-use#label-snowsql-variables).

## SnowSQL configuration options reference

Options modify the default SnowSQL behavior. You can set these options using any of the following methods:

- In the [configuration file](#label-configuring-snowsql) (as described in this topic).
- Using the `-o` or `--option` [parameter](/user-guide/snowsql-start#label-snowsql-connection-parameters) when connecting to Snowflake.
- Using the `!set` [command](/user-guide/snowsql-use#label-snowsql-commands) once connected to Snowflake.

Note

The option names and values are case-insensitive.

### `auto_completion`

> Type:
> :   Boolean
>
> Description:
> :   Enables context-sensitive auto-completion. If enabled, functions, table names, and variables stored in SnowSQL are auto-completed in interactive mode.
>
> Default:
> :   `auto_completion=True`

### `client_session_keep_alive`

> Type:
> :   Boolean
>
> Description:
> :   Indicates whether to force a user to log in again after a period of inactivity in a JDBC or ODBC session. When set to `True`, Snowflake keeps the session active indefinitely, even if there is no activity from the user. When set to `False`, the user must log in again after four hours of inactivity.
>
> Default:
> :   `client_session_keep_alive=False`

### `echo`

> Type:
> :   Boolean
>
> Description:
> :   Echoes local input. When set to `True`, echoes to both `stdout` and the output file.
>
> Default:
> :   `echo=False`

### `editor`

> Type:
> :   String (constant)
>
> Description:
> :   Specifies the editor to invoke when the `!edit` command is issued in SnowSQL. Supported values:
>
>     - `emacs`
>     - `vi`
>     - `vim`
>
> Default:
> :   `editor=vim`

### `empty_for_null_in_tsv`

> Type:
> :   Boolean
>
> Description:
> :   If enabled, when `output_format` is set to `TSV`, SnowSQL outputs an empty string for each NULL value.
>
> Example:
> :   `empty_for_null_in_tsv=True`

### `environment_variables`

> Type:
> :   List
>
> Description:
> :   Specifies the environment variables to be set in the SnowSQL variables.
>
> Example:
> :   `environment_variables=PATH,USER,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY`

### `execution_only`

> Type:
> :   Boolean
>
> Description:
> :   If enabled, SnowSQL executes queries without fetching data. This option is useful when you only want to measure execution times. Note that returned values include any network latency and
>     are not pure server-side execution times.
>
> Example:
> :   `execution_only=True`

### `exit_on_error`

> Type:
> :   Boolean
>
> Description:
> :   If enabled, SnowSQL exits when an error occurs. This behavior is useful to stop running queries when an error is encountered.
>
> Example:
> :   `exit_on_error=True`

### `fix_parameter_precedence`

> Type:
> :   Boolean
>
> Description:
> :   Controls the precedence among the possible sources of the password, proxy password, and private key
>     phrase parameters.
>
>     If the value is True, the precedence (from highest to lowest) is:
>
>     - The environment variable or the SnowSQL command-line parameter.
>     - The connection-specific connection parameters, which are the parameters in the config file’s named connection
>       section, e.g. the section `[connections.myconnection]`.
>     - The default connection parameters, which are the parameters in the `[connections]` section of the config file.
>
>     If the value is False, the precedence (from highest to lowest) is:
>
>     - The connection-specific connection parameters, which are the parameters in the config file’s named connection
>       section, e.g. the section `[connections.myconnection]`.
>     - The environment variable or the SnowSQL command-line parameter.
>     - The default connection parameters, which are the parameters in the `[connections]` section of the config file.
>
> Default:
> :   True

### `force_put_overwrite`

> Type:
> :   Boolean
>
> Description:
> :   If enabled, SnowSQL forces the PUT command to upload (i.e. stage) data files from a local directory/folder on a client machine to the specified internal (i.e. Snowflake) stage without checking whether the files already exist in the stage. If the files are already present in the destination stage, the PUT command overwrites the existing files.
>
> Default:
> :   `force_put_overwrite=False`

### `friendly`

> Type:
> :   Boolean
>
> Description:
> :   If disabled, SnowSQL suppresses the startup and exit messages.
>
> Default:
> :   `friendly=True`

### `header`

> Type:
> :   Boolean
>
> Description:
> :   Displays the header in the results table rendered by SnowSQL. Disabling this option is useful when you want to retrieve data-only in the results.
>
>     Can be used with `output_format` and `timing` to produce data-only output.
>
> Default:
> :   `header=True`

### `insecure_mode`

> Type:
> :   Boolean
>
> Description:
> :   Skips the certificate revocation checks using the Online Certificate Status Protocol (OCSP). This option could be used in an emergency situation in which no OCSP service is accessible.
>     Snowflake strongly recommends that you do not enable this option unless directed by Snowflake Support.
>
> Default:
> :   `insecure_mode=False`

### `key_bindings`

> Type:
> :   String (constant)
>
> Description:
> :   Key bindings to use. Possible values:
>
>     - `emacs`: `CTRL` + `a` is home, `CTRL` + `e` is end. All Emacs key bindings for the REPL
>       environment are available.
>     - `vi`: You can use all modal editing features offered by vi in the REPL environment.
>
> Note:
> :   The value cannot be changed by `!set` command during the SnowSQL session. Instead, set the value in the configuration file or on the command line when connecting to Snowflake.
>
> Default:
> :   `key_bindings=vi`

### `log_bootstrap_file`

> Type:
> :   String (path)
>
> Description:
> :   Bootstrap log file location. If not specified, `log_file` is used as the base name followed by `_bootstrap`. For example, by default, the log file name is `log_bootstrap`.
>
> Default:
> :   `log_bootstrap_file=~/.snowsql/bootlog`

### `log_file`

> Type:
> :   String (path)
>
> Description:
> :   log\_file location.
>
> Note
>
> You must have permissions to write to the log file’s parent directory or to modify the location of the log file.
>
> Default:
> :   `log_file=~/.snowsql/log`

### `log_level`

> Type:
> :   String (constant)
>
> Description:
> :   Default log level. Possible values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`.

### `login_timeout`

> Type:
> :   Number
>
> Description:
> :   Login timeout in seconds.
>
> Default:
> :   `login_timeout=120`

### `noup`

> Type:
> :   Boolean
>
> Description:
> :   Prevents SnowSQL from downloading and installing a new version if `True`. By default, SnowSQL auto-upgrades to the latest version if no version is specified.
>
> Default:
> :   `noup=True`

### `output_file`

> Type:
> :   String (path and file name)
>
> Description:
> :   Writes output to the specified file in addition to the terminal output.
>
> Default:
> :   None

### `output_format`

> Type:
> :   String (constant)
>
> Description:
> :   Specifies the format of the results displayed in the terminal. Possible values:
>
>     - `csv`
>     - `expanded`
>     - `fancy_grid`
>     - `grid`
>     - `html`
>     - `json`
>     - `latex`
>     - `latex_booktabs`
>     - `mediawiki`
>     - `orgtbl`
>     - `pipe`
>     - `plain`
>     - `psql`
>     - `rst`
>     - `simple`
>     - `tsv`
>
>     Recommended values for tabular results: `psql` , `grid`, or `fancy_grid`
>
>     Recommended values for data-only results (used in combination with `header`, `timing`, and `friendly` set to `False`): `plain` , `csv`, or `tsv`
>
> Default:
> :   `output_format=psql`

### `paging`

> Type:
> :   Boolean
>
> Description:
> :   When enabled, pauses output per screen height. This feature is useful for browsing large result sets. To scroll down, press the **[ENTER]/[RETURN]** key.
>
> Default:
> :   `paging=False`

### `progress_bar`

> Type:
> :   Boolean
>
> Description:
> :   Shows progress bar while transferring data.
>
> Default:
> :   `progress_bar=True`

### `prompt_format`

> Type:
> :   string
>
> Description:
> :   Changes the SnowSQL prompt format.
>
>     The SnowSQL prompt dynamically displays the current user, warehouse, database, and schema by default. Dynamic tokens are written as [<token>], e.g. [user] or [warehouse]. You can change the Snowflake object order, delimiter,
>     and color. Change the object color by defining a pygments token in brackets.
>
>     For example, change the object order to user, database and schema, then warehouse. Change the delimiter to a period. Change the [user] object name to red, the [database] and [schema] names to green, and the [warehouse] name to blue:
>
>     > Copy code
>     >
>     > ```
>     > prompt_format="[#FF0000][user]@[#00FF00][database][schema][#0000FF][warehouse]"
>     > ```
>
>     Put quotes around the value to prevent “#” characters from being interpreted as the start of a comment.
>
> Default:
> :   `None`

### `quiet`

> Type:
> :   Boolean
>
> Description:
> :   Removes all output data from the terminal, but continues to display error messages and diagnostic data.
>
> Default:
> :   `quiet=True`

### `remove_comments`

> Type:
> :   Boolean
>
> Description:
> :   Removes comments from the output.
>
> Default:
> :   `remove_comments=False`

### `remove_trailing_semicolons`

> Type:
> :   Boolean
>
> Description:
> :   Removes trailing semicolons from SQL text before sending queries to Snowflake. Note that removing the semicolons can prevent Snowflake from using cached results from different clients when
>     the [USE\_CACHED\_RESULT](/sql-reference/parameters#label-use-cached-result) session parameter is enabled.
>
> Default:
> :   `remove_trailing_semicolons=True`

### `results`

> Type:
> :   Boolean
>
> Description:
> :   Returns the query results. If `False`,the query is executed asynchronously, no result including any error messages is returned.
>
> Default:
> :   `results=True`

### `rowset_size`

> Type:
> :   Number
>
> Description:
> :   Number of rows to fetch at once in interactive mode. Results are then fetched for output one rowset at a time.
>
> Default:
> :   `rowset_size=1000`

### `sfqid`

> Type:
> :   Boolean
>
> Description:
> :   Includes the Snowflake query ID in the result summary.
>
>     **Note**: You must also set `timing_in_output_file=True` to add `sqfid` to the spool file.
>
> Default:
> :   `sfqid=False`

### `sfqid_in_error`

> Type:
> :   Boolean
>
> Description:
> :   Includes the Snowflake query ID in error messages.
>
> Default:
> :   `sfqid_in_error=False`

### `stop_on_error`

> Type:
> :   Boolean
>
> Description:
> :   When an error is encountered, stops query execution, but does not exit.
>
> Default:
> :   `stop_on_error=False`

### `syntax_style`

> Type:
> :   String (constant)
>
> Description:
> :   Sets the text colors for SnowSQL. Currently, the only supported value is `default`.
>
> Default:
> :   `syntax_style=default`

### `timing`

> Type:
> :   Boolean
>
> Description:
> :   Specifies whether to display the number of rows produced and elapsed time for SQL statements that have executed. This information is displayed as a line of text under the results table rendered by SnowSQL. If set to `False`, the line of text under the results table is not displayed.
>
>     Can be used in conjunction with `header` and `output_format` to produce data-only output.
>
> Default:
> :   `timing=True`

### `timing_in_output_file`

> Type:
> :   Boolean
>
> Description:
> :   Specifies whether to include the execution time details in the output file, if the `output_file` option is configured. Requires also setting the `timing` option to `True`.
>
>     If set to `False`, the line of text under the results table is not included in the output file.
>
> Default:
> :   `timing_in_output_file=False`

### `variable_substitution`

> Type:
> :   Boolean
>
> Description:
> :   Substitutes variables with the values. See [Using variables](/user-guide/snowsql-use#label-snowsql-variables).
>
> Default:
> :   `variable_substitution=False`

### `wrap`

> Type:
> :   Boolean
>
> Description:
> :   Wraps the output by the terminal width. If `False`, the outputs are truncated.
>
> Default:
> :   `wrap=True`
