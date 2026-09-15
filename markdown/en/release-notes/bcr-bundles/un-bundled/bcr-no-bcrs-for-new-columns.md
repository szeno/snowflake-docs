# New columns in views and SHOW command output are no longer treated as behavior changes

Beginning with the 2026\_04 behavior change bundle (May 8-14, 2026), new columns in Snowflake
views (such as views in the [SNOWFLAKE.ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views),
[SNOWFLAKE.ORGANIZATION\_USAGE](/sql-reference/organization-usage#label-organization-usage-views), and
[INFORMATION\_SCHEMA](/sql-reference/info-schema#label-information-schema-views) schemas) and in the output of SHOW commands are no longer treated as
behavior changes.

When a new column is added to a Snowflake view or to the output of a SHOW command, the change will no longer be included in a
[behavior change bundle](/release-notes/intro-bcr-releases), and the change will no longer be
[announced with the other behavior changes](/release-notes/behavior-changes). These types of changes will be introduced
in [server releases and feature updates](/release-notes/new-features).

If the introduction of a new column causes an unexpected problem:

- In the short term, you can [temporarily exclude that column](/release-notes/behavior-changes-new-columns) from queries
  of the view and from the output of SHOW commands.
- As a long term solution, update your scripts to select specific columns from the query or SHOW command output.

  To select specific columns from the output of SHOW commands, you can use the
  [pipe operator](/sql-reference/operators-flow). See the example in [Select a list of columns for the output of a SHOW command](/sql-reference/operators-flow#label-pipe-operator-example-show).
