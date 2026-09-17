# New columns in DESCRIBE command output are no longer treated as behavior changes

Beginning October 19, 2026, new columns in the output of [DESCRIBE <object>](/sql-reference/sql/desc) commands are no longer treated as
behavior changes.

When a new column is added to the output of a DESCRIBE command, the change will no longer be included in a
[behavior change bundle](/release-notes/intro-bcr-releases), and the change will no longer be
[announced with the other behavior changes](/release-notes/behavior-changes). These types of changes will be introduced
in [server releases and feature updates](/release-notes/new-features).

If you depend on an exact column list, introducing a new column may cause unexpected problems. To avoid this, update your
scripts to select specific columns from the DESCRIBE command output instead of relying on all columns.

To select specific columns from the output of a DESCRIBE command, you can use the
[pipe operator](/sql-reference/operators-flow). See the example in [Select a list of columns for the output of a SHOW command](/sql-reference/operators-flow#label-pipe-operator-example-show).
