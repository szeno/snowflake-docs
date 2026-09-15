Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_VERSION

Returns the current Snowflake version.

See also:
:   [CURRENT\_CLIENT](/sql-reference/functions/current_client)

## Syntax

Copy code

```
CURRENT_VERSION()
```

## Arguments

None.

## Returns

The data type of the returned value is VARCHAR.

The returned value contains four fields:

> Copy code
>
> ```
> <major_version>.<minor_version>.<patch_version>  <internal_identifier>
> ```
>
> `major_version`
> :   Major version numbers change annually. For example, the major version for all releases in 2026 is 10. For all releases in 2025, the major version is 9.
>
> `minor_version`
> :   Minor version numbers change for each weekly release.
>
> `patch_version`
> :   Patch version numbers represent minor changes within a weekly release. It can be 1x or 10x based on the Early Adopter release and Weekly release respectively.
>
> `internal_identifier`
> :   This field is for internal use only.
>
> For example, for version 10.15.10, the major version is 10, the minor version is 15, and the patch version is 10. (Early Adopter Release)
>
> For example, for version 10.15.100, the major version is 10, the minor version is 15, and the patch version is 100. (Weekly Release - All accounts)

## Usage notes

- This function returns version number information for Snowflake. To retrieve information about client versions,
  see [CURRENT\_CLIENT](/sql-reference/functions/current_client).

## Examples

This shows the version of Snowflake on which the query is run:

> Copy code
>
> ```
> SELECT CURRENT_VERSION();
> ```
>
> Output:
>
> Copy code
>
> ```
> +-------------------+
> | CURRENT_VERSION() |
> |-------------------|
> | 10.15.100         |
> +-------------------+
> ```
