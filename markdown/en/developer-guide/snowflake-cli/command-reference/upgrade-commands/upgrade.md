# snow upgrade

Upgrade a direct install of Snowflake CLI.

## Syntax

Copy code

```
snow upgrade
  --revert
  --dry-run
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

`--revert`
:   Point the shim at the previous direct install version. Default: False.

`--dry-run`
:   Show what would change without downloading or retargeting the shim. Default: False.

`--format [TABLE|JSON|JSON_EXT|CSV|PLAIN]`
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

`snow upgrade` updates a direct install of Snowflake CLI to the latest same-major version. It writes a new version directory, verifies the signed manifest and tarball checksum, and retargets the shim. The next `snow` in the same session is the new version.

The command works only when `snow --info` reports `installation_source` as `direct-install`. Other channels refuse and print the direct-install command. Those installs are not modified:

- `pypi` (pip, pipx, uv, and the Homebrew formula) refuses.
- `binary` (macOS pkg, Homebrew cask, Windows MSI, and Linux deb or rpm) refuses.

A newer major version is reported and not installed. If the install is already on the latest same-major version, the command reports that and does nothing.

`--dry-run` shows what would change without downloading or retargeting the shim. `--revert` points the shim at the previous direct-install version. Revert is available only after a successful upgrade, does not download a new version, and does not change configuration in `~/.snowflake`.

Upgrades are disabled when `cli.air_gapped` is set in the configuration file or `SNOWFLAKE_CLI_AIR_GAPPED` is set.

## Examples

- Upgrade a direct install:

  Copy code

  ```
  snow upgrade
  ```

  ```
  Upgraded 3.12.0 → 3.13.1.
  ```
- Show the upgrade without downloading or retargeting the shim:

  Copy code

  ```
  snow upgrade --dry-run
  ```
- Point the shim at the previous direct-install version:

  Copy code

  ```
  snow upgrade --revert
  ```
