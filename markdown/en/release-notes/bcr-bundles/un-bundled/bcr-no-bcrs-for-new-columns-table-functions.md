# New columns in built-in table function output are no longer treated as behavior changes

Beginning September 4, 2026, new columns in the output of the built-in table functions in the
[INFORMATION\_SCHEMA](/sql-reference/info-schema), [ACCOUNT\_USAGE](/sql-reference/account-usage),
[ORGANIZATION\_USAGE](/sql-reference/organization-usage), and [READER\_ACCOUNT\_USAGE](/sql-reference/account-usage) schemas are no
longer treated as behavior changes.

This change applies only to the built-in table functions in these schemas. It doesn’t apply to other built-in table functions,
such as [FLATTEN](/sql-reference/functions/flatten), [RESULT\_SCAN](/sql-reference/functions/result_scan), and
[SPLIT\_TO\_TABLE](/sql-reference/functions/split_to_table).

When a new column is added to the output of a built-in table function, the change will no longer be included in a
[behavior change bundle](/release-notes/intro-bcr-releases), and the change will no longer be
[announced with the other behavior changes](/release-notes/behavior-changes). These types of changes will be introduced
in [server releases and feature updates](/release-notes/new-features).

If you depend on an exact column list, introducing a new column may cause unexpected problems. In this scenario, consider one of
these approaches:

- As a workaround, you can [temporarily exclude that column](/release-notes/behavior-changes-new-columns) from the output of
  the table function.
- As a long term solution, update your scripts to select specific columns from the table function output.
