# snow helpers v1-to-v2

Migrates the Snowpark, Streamlit, and Native App project definition files from V1 to V2.

## Syntax

Copy code

```
snow helpers v1-to-v2
  --accept-templates
  --migrate-local-overrides / --no-migrate-local-overrides
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

`-t, --accept-templates`
:   Allows the migration of templates. Default: False.

`-l, --migrate-local-overrides / --no-migrate-local-overrides`
:   Merge values in snowflake.local.yml into the main project definition. The snowflake.local.yml file will not be migrated, instead its values will be reflected in the output snowflake.yml file. If unset and snowflake.local.yml is present, an error will be raised.

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

Snowflake CLI 3.0 introduced support for V2 project definition files. If you have existing V1.x project definition files, you can use the `snow helpers v1-to-v2` command to convert the files to the V2 version. The command preserves the original version in a `snowflake_V1.yml` file.

You must run this command in the same directory as the `snowflake.yml` file.

Attention

With the change in how Snowflake CLI 3.0 handles project definition templates, Snowflake cannot guarantee that project definition files using
[templates](/developer-guide/snowflake-cli/project-definitions/create-templates) will work correctly after conversion. By default, this command generates an error if you try convert a 1.x file that contains templates. You can force the command to convert these types of files by using the `--accept-templates` option. Then you
must manually update any templates to their V2 equivalents.

## Examples

- Convert a version 1.x project definition file.

  Copy code

  ```
  cd <project-directory>
  snow helpers v1-to-v2
  ```

  ```
  Project definition migrated to version 2.
  ```
- Convert a version 2 project definition file.

  Copy code

  ```
  cd <project-directory>
  snow helpers v1-to-v2
  ```

  ```
  Project definition is already at version 2.
  ```
- Convert a version 1 project definition that contains templates without the `--accept-templates` option.

  Copy code

  ```
  cd <project-directory>
  snow helpers v1-to-v2
  ```

  ```
  +- Error---------------------------------------------------------------------+
  | Project definition contains templates. They may not be migrated correctly, |
  | and require manual migration.You can try again with --accept-templates     |
  | option, to attempt automatic migration.                                    |
  +----------------------------------------------------------------------------+
  ```
- Convert a version 1 project definition with the `--accept-templates` option.

  Copy code

  ```
  cd <project-directory>
  snow helpers v1-to-v2
  ```

  ```
  WARNING  snowflake.cli._plugins.workspace.commands:commands.py:60 Your V1 definition contains templates. We cannot guarantee the correctness of the migration.
  Project definition migrated to version 2
  ```
