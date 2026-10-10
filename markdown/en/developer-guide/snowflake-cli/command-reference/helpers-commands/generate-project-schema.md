# snow helpers generate-project-schema

Generate a JSON Schema for the Snowflake CLI project definition file (snowflake.yml).

## Syntax

Copy code

```
snow helpers generate-project-schema
  --definition-version <version>
  --output-file <output_file>
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

`--definition-version [1|1.1|2]`
:   Project definition version to generate the schema for. Default: ProjectDefinitionVersion.V2.

`--output-file, -o FILE`
:   Write the JSON Schema to this file. When omitted, schema is printed to stdout.

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

The generated schema describes the structure of the `snowflake.yml` project definition file for the selected definition version. Use the `--definition-version` option to choose the version (`1`, `1.1`, or `2`; the default is `2`), and the `--output-file` (or `-o`) option to write the schema to a file instead of printing it to standard output.

Because the schema is derived from the CLI’s own models, it validates the structure of the file, for example unknown keys, incorrect types, and missing required fields. Some cross-field and semantic checks are applied only when the project is loaded or deployed, so a file that matches the schema can still fail at deploy time.

## Examples

- Print the schema for the default (version 2) project definition to standard output:

  Copy code

  ```
  snow helpers generate-project-schema
  ```
- Write the schema to a file that your editor or CI pipeline can reference:

  Copy code

  ```
  snow helpers generate-project-schema --output-file snowflake-schema.json
  ```
- Generate the schema for a version 1.1 project definition:

  Copy code

  ```
  snow helpers generate-project-schema --definition-version 1.1
  ```
