# PACKAGES view

This Information Schema view displays a row for each Snowpark package version supported for use in the PACKAGES clause in the
[CREATE FUNCTION](/sql-reference/sql/create-function) and [CREATE PROCEDURE](/sql-reference/sql/create-procedure) commands. For Python, this view also displays a
row for each version of a third-party package that you can install. For details, see
[Using third-party packages](/developer-guide/udf/python/udf-python-packages).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PACKAGE\_NAME | VARCHAR | The name of the package |
| VERSION | VARCHAR | The version number of the package |
| LANGUAGE | VARCHAR | The programming language for the package |

Expand

Show lessSee more

## Usage notes

Currently, the package versions with the following are supported:

- `language = java`
- `language = python`
- `language = scala`

## Examples

List all available versions of the pandas package for Python:

> Copy code
>
> ```
> SELECT package_name, version
>   FROM information_schema.packages
>   WHERE language = 'python'
>     AND package_name = 'pandas'
>   ORDER BY version;
> ```
