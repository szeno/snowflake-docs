# snow helpers clean-installer-path

Remove PATH entries that older macOS installers left in shell startup files, which can keep an outdated `snow` ahead of the current one.

## Syntax

Copy code

```
snow helpers clean-installer-path
  --apply
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

`--apply`
:   Remove historical installer PATH entries. The default is a dry run. Default: False.

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

The command reports what it would remove by default. `--apply` removes the entries and backs up every file it changes.

## Examples

- Preview the PATH entries that older macOS installers left behind:

  Copy code

  ```
  snow helpers clean-installer-path
  ```
- Remove those entries and back up the edited files:

  Copy code

  ```
  snow helpers clean-installer-path --apply
  ```
