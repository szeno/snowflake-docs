# snow app bundle

Copies resolved artifacts into `output/bundle` so you can inspect what a deploy
would upload. No Snowflake connection is required because this command operates
entirely locally. `snow app bundle` doesn’t take `--target`; all
targets share one source tree.

## Syntax

Copy code

```
snow app bundle
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
```

## Arguments

None

## Options

`--verbose, -v`
:   Displays log entries for log levels `info` and higher. Default: False.

`--debug`
:   Displays log entries for log levels `debug` and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--help`
:   Displays the help text for this command.

## Usage notes

Use `snow app bundle` to preview exactly which files would be uploaded during a
deploy. The output directory is `output/bundle` relative to your project root.
This is useful for debugging artifact resolution or verifying that your
`app.yml` `ignore` list and source layout include the correct files.

## Examples

Bundle the project artifacts locally:

Copy code

```
snow app bundle
```

Then inspect the output:

Copy code

```
ls output/bundle/
```
