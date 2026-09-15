# CURRENT\_PACKAGES\_POLICY view

This Information Schema view displays a row for each Snowpark packages policy created on the current account by the
[CREATE PACKAGES POLICY](/sql-reference/sql/create-packages-policy) command. For details, see
[Packages policies](/developer-guide/udf/python/packages-policy).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | The name of the package policy |
| LANGUAGE | VARCHAR | The programming language the packages policy applies to |
| ALLOWLIST | VARCHAR | The list of package specs that are allowed |
| BLOCKLIST | VARCHAR | The list of package specs that are blocked |
| ADDITIONAL\_CREATION\_BLOCKLIST | VARCHAR | The list of package specs that are blocked at creation time |
| COMMENT | VARCHAR | A comment about the packages policy |

Expand

Show lessSee more

## Usage notes

Currently, package policies are supported for Python.
