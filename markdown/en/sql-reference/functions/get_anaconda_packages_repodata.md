Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# GET\_ANACONDA\_PACKAGES\_REPODATA

Returns a list of third-party packages that are available from Anaconda.
For more information, see [Packages policies](/developer-guide/udf/python/packages-policy).

## Syntax

Copy code

```
SNOWFLAKE.SNOWPARK.GET_ANACONDA_PACKAGES_REPODATA( '<architecture>' )
```

## Arguments

`architecture`
:   String specifying the architecture, which can be:
    `linux-64`, `linux-aarch64`, or `noarch`.

## Returns

Returns a JSON string that contains the contents of `repodata.json`, which is an index of the packages in a subdir. A subdir represents a particular architecture. Each subdir will have its own repodata.

For more information, see the [Conda documentation](https://docs.conda.io/projects/conda-build/en/stable/concepts/generating-index.html#repodata-json)

## Access control requirements

You must use the ACCOUNTADMIN role to call this function.

## Examples

The following example gets the list of third-party packages from Anaconda for `linux-64`.

Copy code

```
USE ROLE ACCOUNTADMIN;

select SNOWFLAKE.SNOWPARK.GET_ANACONDA_PACKAGES_REPODATA('linux-64');
```
