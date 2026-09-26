# Configuring Snowflake CLI

Snowflake CLI uses a global configuration file called `config.toml` to configure connections and logs for Snowflake CLI.
If the file does not exist, running any `snow` command for the first time automatically creates an
empty `config.toml` file that you can then populate with the desired connections.
For more information about `toml` file formats, see [TOML (Tom’s Obvious Minimal Language)](https://toml.io/en/).
Snowflake Python libraries currently support TOML version 1.0.0.

The `config.toml` supports the following sections:

- `[connections]` for defining and managing connections
- `[logs]` for configuring which types of messages are saved to log files

A Snowflake CLI configuration file has the following structure:

Copy code

```
default_connection_name = "myconnection"

[connections]
[connections.myconnection]
account = "myorganization-myaccount"
user = "jdoe"
...

[connections.testingconnection]
account = "myorganization-myaccount"
user = "jdoe"
...

[cli.logs]
save_logs = true
level = "info"
path = "/home/<username>/.snowflake/logs"
```

You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
[Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

Note

Other Snowflake tools (VS Code Extension, Cortex Code, SnowConvert) also read `connections.toml`. If it exists, Snowflake CLI uses connections from it instead of `config.toml`.

## Location of the `.toml` configuration file

By default Snowflake CLI looks for the `config.toml` file in the `~/.snowflake` directory or, in case this directory does not exist, in a system-specific location, as listed below.
You can also specify which configuration file should be used with the `--config-file` flag or `SNOWFLAKE_HOME` environment variable.

- If you specify the `--config-file` option (such as `snow --config-file ./my-config-file-path`), Snowflake CLI uses the specified configuration file.
- If the `SNOWFLAKE_HOME` environment variable is set, Snowflake CLI uses the location specified by this variable.
- If a `~/.snowflake` directory exists on your machine, Snowflake CLI uses the `~/.snowflake/config.toml` file.
- Otherwise, Snowflake CLI uses the `config.toml` file in one of the following locations, based on your operating system:
  - Linux: `~/.config/snowflake/config.toml`, but you can update it with XDG vars
  - Windows: `%USERPROFILE%\AppData\Local\snowflake\config.toml`
  - Mac: `~/Library/Application Support/snowflake/config.toml`

Note

For macOS and Linux systems, Snowflake CLI requires the `config.toml` file to limit its file permissions to read and write for the file owner only. To set the required file permissions, execute the following commands:

Copy code

```
chown $USER config.toml
chmod 0600 config.toml
```

### Choose a different configuration file

In some situations, such as continuous integration and continuous deployment (CI/CD) environments, you might prefer to create dedicated configuration files for testing and deployment pipelines instead of defining all of the possible configurations in a single Snowflake default configuration file.

To use a different configuration file than your default file, you can use the `--config-file` option for the `snow` command, as shown:

Copy code

```
snow --config-file="my_config.toml" connection test
```

### Support for system environment variables

Snowflake CLI supports using system environment variables to override parameter values defined in your `config.toml` file, using the following format:

Copy code

```
SNOWFLAKE_<config-section>_<variable>=<value>
```

where:

- `<config-section>` is the name of a section in the configuration file with periods (`.`) replaced with underscores (`_`), such as `CLI_LOGS`.
- `<variable>` is the name of a variable defined in that section, such as `path`.

Some examples include:

- Override the `path` parameter in the `[cli.logs]` section in the `config.toml` file:

  Copy code

  ```
  export SNOWFLAKE_CLI_LOGS_PATH="/Users/jondoe/snowcli_logs"
  ```
- Set the password for the `myconnection` connection:

  Copy code

  ```
  export SNOWFLAKE_CONNECTIONS_MYCONNECTION_PASSWORD="*******"
  ```
- Set the default connection name:

  Copy code

  ```
  export SNOWFLAKE_DEFAULT_CONNECTION_NAME="myconnection"
  ```

## Add an authentication policy that limits access to Snowflake CLI only

Users can create an [authentication policy](/user-guide/authentication-policies) that limits access permission to drivers, as well as Snowflake CLI.
If you want to allow access to Snowflake CLI only (and exclude the drivers), you can do the following:

- Create a new authentication policy that limits access strictly to Snowflake CLI.
- Enable the policy in the `config.toml` file.

### Create an authentication policy limited to Snowflake CLI

To create a new authentication policy for only Snowflake CLI, follow these steps:

1. Execute the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) SQL command, setting the CLIENT\_TYPES parameter to include `'SNOWFLAKE_CLI'`.

   Copy code

   ```
   CREATE AUTHENTICATION POLICY snowflake_cli_only
     CLIENT_TYPES = ('SNOWFLAKE_CLI');
   ```
2. Add the policy to the user, as shown:

   Copy code

   ```
   ALTER USER user1
     SET AUTHENTICATION POLICY snowflake_cli_only;
   ```

### Enable the policy in the Snowflake CLI configuration

The `enable_separate_authentication_policy_id` configuration parameter lets you enable access to Snowflake CLI separately from the drivers.
When this access is enabled, specified users can access Snowflake CLI but not the other Snowflake drivers.

Warning

If you already have an authentication policy that allows access only to drivers and don’t have one that allows access to Snowflake CLI only, enabling the `enable_separate_authentication_policy_id` parameter will cause the users to lose access to Snowflake CLI if you don’t create the new policy first. Make sure to add SNOWFLAKE\_CLI to your authentication policy before enabling the configuration parameter.

To enable the SNOWFLAKE\_CLI policy, add the `enable_separate_authentication_policy_id` parameter to the `[cli.features]` section in the `config.toml` file, as shown:

Copy code

```
[cli.features]
enable_separate_authentication_policy_id = true
```

Note

Enabling this parameter affects all connections made by Snowflake CLI.

## Use a proxy server

To use a proxy server, configure the following environment variables:

- HTTP\_PROXY
- HTTPS\_PROXY
- NO\_PROXY

For example:

Linux or macOS:
:   Copy code

    ```
    export HTTP_PROXY='http://username:password@proxyserver.example.com:80'
    export HTTPS_PROXY='http://username:password@proxyserver.example.com:80'
    ```

Windows:
:   Copy code

    ```
    set HTTP_PROXY=http://username:password@proxyserver.example.com:80
    set HTTPS_PROXY=http://username:password@proxyserver.example.com:80
    ```

Tip

Snowflake’s security model does not allow Secure Sockets Layer (SSL) proxies (using an HTTPS certificate). Your proxy server must use a publicly available Certificate Authority (CA), reducing potential security risks such as a MITM (Man In The Middle) attack through a compromised proxy.

If you must use your SSL proxy, we strongly recommend that you update the server policy to pass through the Snowflake certificate such that no certificate is altered in the middle of
communications.

Optionally `NO_PROXY` can be used to bypass the proxy for specific communications. For example, access to Amazon S3 can bypass the proxy server by specifying `NO_PROXY=".amazonaws.com"`.

`NO_PROXY` does not support wildcards. Each value specified should be one of the following:

- The end of a hostname (or a complete hostname), for example:

  - .amazonaws.com
  - myorganization-myaccount.snowflakecomputing.com
- An IP address, for example:

  - 192.196.1.15

If more than one value is specified, values should be separated by commas, for example:

> Copy code
>
> ```
> localhost,.example.com,.snowflakecomputing.com,192.168.1.15,192.168.1.16
> ```

## Configure logging

By default, Snowflake CLI automatically saves `INFO`, `WARNING`, and `ERROR` level messages to log files. To disable or customize logging, create a `[cli.logs]` section in your `config.toml` file:

Copy code

```
[cli.logs]
save_logs = true
level = "info"
path = "/home/<username>/.snowflake/logs"
```

where:

- `save_logs` indicates whether to save logs to files. Default: `true`.
- `level` specifies which levels of messages to save to log files. Choose from the following levels, which include all levels below the selected one:

  - `debug`

    Warning

    Switching to the `debug` logging level can expose sensitive information, such as executed SQL queries. Use caution when enabling this level.
  - `info`
  - `warning`
  - `error`

  Default: `info`
- `path` specifies the absolute path to save the log files. The format of the path varies based on your operating system, as shown:

  - Linux: `path = "/home/<your_username>/.config/snowflake/logs"`
  - macOS: `path = "/Users/<your_username>/Library/Application Support/snowflake/logs"`
  - Windows: `path = "C:\\Users\\<your_username>\\AppData\\Local\\snowflake\\logs"`

  If not specified, the command creates a `logs` directory in the default `config.toml` file location.

If your `config.toml` was created automatically, the `config.toml` file contains the `[cli.logs]` section filled with default values.

Logs from a single day are appended to file `snowflake-cli.log`, which is later renamed to `snowflake-cli.log.YYYY-MM-DD`, as shown.

Copy code

```
ls logs/
```

```
snowflake-cli.log            snowflake-cli.log.2024-10-22
```

For troubleshooting purposes, you’ll typically also need to configure logging for the Snowflake Connector for Python by adding a `[log]` section to the `config.toml` file, as shown in the following example:

Copy code

```
[log]
save_logs = true
path = "/home/<username>/.snowflake/logs"
level = "DEBUG"
```

For more information about logging for the Snowflake Connector for Python, see [Logging configuration file](/developer-guide/python-connector/python-connector-example#label-python-easy-logging) in the Snowflake Connector for Python documentation.

## Configure encoding

By default, Snowflake CLI uses your operating system’s default text encoding when reading files, decoding output from external processes, and writing to standard output. On modern Linux and macOS systems, this default is UTF-8 and no configuration is needed. To confirm, run `locale` and check that it reports `UTF-8`. On Windows, the default is a legacy code page (such as `cp1252` on Western European systems or `cp932` on Japanese systems), which can silently corrupt non-ASCII characters in:

- SQL files containing Unicode identifiers or string literals.
- Query results redirected to a file with `>`.
- Output captured from external processes such as `pip` or `docker`.

To avoid these issues on Windows, choose **one** of the following options.

Note

If you run Snowflake CLI inside the Windows Subsystem for Linux (WSL), you already have a UTF-8 environment and don’t need any of the configuration below.

### Option 1: Enable Python UTF-8 mode

Set the `PYTHONUTF8` environment variable to `1` before running Snowflake CLI. This applies UTF-8 to all of Python’s input and output, so it’s the broadest fix.

- PowerShell (add to your `$PROFILE` to make it permanent):

  Copy code

  ```
  $env:PYTHONUTF8=1
  ```
- Command Prompt:

  Copy code

  ```
  set PYTHONUTF8=1
  ```
- Git Bash:

  Copy code

  ```
  export PYTHONUTF8=1
  ```

### Option 2: Set encodings in `config.toml`

Add a `[cli.encoding]` section to your `config.toml` file:

Copy code

```
[cli.encoding]
file_io = "utf-8"
subprocess = "utf-8"
stdout = "utf-8"
```

where:

- `file_io` is the encoding Snowflake CLI uses to read and write project files such as SQL scripts and `snowflake.yml`.
- `subprocess` is the encoding Snowflake CLI uses to decode output of external processes such as `pip` or `docker`.
- `stdout` is the encoding Snowflake CLI uses when writing output to standard output.

### Option 3: Set encodings using environment variables

Set the matching environment variables instead of editing `config.toml`. For example, in PowerShell:

Copy code

```
$env:SNOWFLAKE_CLI_ENCODING_FILE_IO='utf-8'
$env:SNOWFLAKE_CLI_ENCODING_SUBPROCESS='utf-8'
$env:SNOWFLAKE_CLI_ENCODING_STDOUT='utf-8'
```

### Additional step for Windows PowerShell 5.x

Note

This applies to Windows PowerShell 5.x only. Skip this section if you use PowerShell 7 or later, which defaults to UTF-8 without a byte order mark (BOM).

Windows PowerShell has encoding settings of its own that Snowflake CLI configuration doesn’t reach. `[Console]::OutputEncoding`
controls what the console passes to and from native executables, `$OutputEncoding` controls what PowerShell sends through
the pipeline, and `$PSDefaultParameterValues['Out-File:Encoding']` controls which text encoding `Out-File` and the `>` operator use to write their output to disk.
If any of these is left on a legacy code page, non-ASCII characters are silently corrupted even when Snowflake CLI emits UTF-8.
This issue can occur in the following scenarios:

- Saving the output of a Snowflake CLI command to a file using the `>` operator.
- Storing the output of a Snowflake CLI command in a variable for further processing in a script.
- Passing the output of a Snowflake CLI command to another native command using the `|` operator.

To prevent these issues, apart from applying one of the three options described earlier, you need to force PowerShell to use UTF-8
by adding the following to your PowerShell session or profile (`$PROFILE`):

Copy code

```
[Console]::OutputEncoding = [Text.UTF8Encoding]::new()
$OutputEncoding = [Text.UTF8Encoding]::new()
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
```

The `Out-File:Encoding` setting above applies to files you create to capture or read Snowflake CLI output. It does not
make it safe to use `>` or `Out-File` to create files you feed *into* a Snowflake CLI command because in Windows PowerShell 5.x
the `utf8` encoding always writes a BOM at the start of the file, which Snowflake CLI does not strip.
To create BOM-free UTF-8 files in Windows PowerShell 5.x we recommend using `[System.IO.File]::WriteAllLines`:

Copy code

```
$Path = "C:\Users\<your_username>\<path_to_your_file>\<file_name>"
[System.IO.File]::WriteAllLines($Path, "SELECT 1;")
```

If a file in UTF-8 encoding already has a byte order mark, for example from `Out-File -Encoding utf8`, you can strip it to get BOM-free UTF-8:

Copy code

```
$Path = "C:\Users\<your_username>\<path_to_your_file>\<file_name>"
$Content = Get-Content -Raw $Path
[System.IO.File]::WriteAllText($Path, $Content)
```

For files created under a different encoding entirely, for example cp932, use a third-party tool (like Notepad++)
to convert to BOM-free UTF-8 instead.

## Set a default output format

By default, Snowflake CLI prints command results as a table. You can change the default to `TABLE`, `JSON`, `JSON_EXT`, or `CSV`. `--format` on a command still overrides the default.

- Add the `output_format` setting to the `config.toml` file:

  Copy code

  ```
  [cli]
  output_format = "JSON"
  ```
- Set the `SNOWFLAKE_CLI_OUTPUT_FORMAT` environment variable:

  Copy code

  ```
  export SNOWFLAKE_CLI_OUTPUT_FORMAT=JSON
  ```

## Suppress version update notifications

By default, Snowflake CLI checks for newer versions and displays a notification message when a newer version is available. You can suppress these notifications using either a configuration file setting or an environment variable, as follows:

- Add the `ignore_new_version_warning` setting to the `config.toml` file:

  Copy code

  ```
  [cli]
  ignore_new_version_warning = true
  ```
- Set the `SNOWFLAKE_CLI_IGNORE_NEW_VERSION_WARNING` environment variable:

  Copy code

  ```
  export SNOWFLAKE_CLI_IGNORE_NEW_VERSION_WARNING=true
  ```
