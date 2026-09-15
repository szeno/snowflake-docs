# Differences between sfsql and SnowSQL

Obsoleted Feature

`sfsql` is now obsoleted. Use [SnowSQL](/user-guide/snowsql) instead.

SnowSQL (`snowsql`) provides many improvements and enhancements over the `sfsql` command-line interface, including more intuitive option and command names. This topic lists differences in usage between the two
command-line clients.

## Command-line options

Many of the command-line options in SnowSQL are backward-compatible with the corresponding options in `sfsql`; however, there are key differences, as described in the following table:

| Option | `sfsql` | SnowSQL (`snowsql`) |
| --- | --- | --- |
| Account identifier | `-a` | `-a` , `--accountname` |
| User name | `-u` | `-u` , `--username` |
| Password | `-c` | N/A (use SNOWSQL\_PWD environment variable) |
| Prompt for password | N/A | `-P` |
| Database | `-d` | `-d` , `--dbname` |
| Schema | `-s` | `-s` , `--schemaname` |
| Warehouse | `-w` | `-w` , `--warehouse` |
| Role | `-r` | `-r` , `--rolename` |
| Host name | `-g` | `-h` , `--host` |
| Port number | `-p` | `-p` , `--port` |
| MFA passcode | `-m` | `-m` , `--mfa-passcode` |
| MFA passcode in password | `-n` | `--mfa-passcode-in-password` |
| Explain a SQL | `-e` (not supported) | N/A |
| Explain a SQL in dot form | `-x` (not supported) | N/A |
| Run a SQL file | `-f` | `-f` , `--filename` |
| Stop on error | N/A | `-o stop_on_error=true` |
| Exit on error | `-k` | `-o exit_on_error=true` |
| Authenticator | `-b` | `--authenticator` |
| Use a user-defined connection | N/A | `-c` , `--connection` |
| Trace level | `-t` | `-o log_level=(INFO|DEBUG)` |
| Show CLI version | N/A | `-v` , `--version` |
| Use specified config | N/A | `--config` |
| Set options | N/A | `-o` , `--option` |
| Set variables | N/A | `-D` , `--variable` |
| Help | `-h` | `-?` , `--help` |

Expand

Show lessSee more

## Commands

For commands, the key difference is all commands in SnowSQL must be prefixed with an exclamation point (e.g. `!exit`). In addition, the names of some of the commands have changed.

| Command | `sfsql` | SnowSQL (`snowsql`) |
| --- | --- | --- |
| Load and run a SQL file | `load` , `@` | `!source` , `!load` |
| Print a message | `echo` | `!print` |
| Set an option | N/A | `!set` |
| Show all options | N/A | `!options` |
| Set a variable | `set-var` | `!define` |
| Unset a variable | `unset-var` | N/A |
| Show all variables | N/A | `!variables` |
| Connect and start a new session | `connect` | `!connect` |
| Exit the current session | N/A | `!exit` , `!disconnect` (see also `!quit`) |
| Spool output into a file | `spool` | `!spool` |
| Quit the CLI | `exit` , `quit` | `!quit` |
| Executes a system command | `system` | `!system` |
| Help | `help` | `!help` |

Expand

Show lessSee more

## Special characters

The following characters have special meaning in the two clients:

| Usage | `sfsql` | SnowSQL (`snowsql`) |
| --- | --- | --- |
| Prefix for variable names | `$` | `&&` |
| Setting off comments in code | `#` | `--` and `/* ... */` |

Expand

Show lessSee more
