# snow notebook commands

Deprecated

The `snow notebook` commands create and run [Legacy Notebooks](/user-guide/ui-snowsight/notebooks), which are
deprecated. Starting September 1, 2026, new Legacy Notebooks can’t be created. Starting November 2026, Legacy
Notebooks can no longer be run or edited. For the full timeline, see
[Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks).

Use [Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
instead. To migrate existing notebooks, see
[Migrating legacy notebooks to Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).

Snowflake CLI supports the following commands for managing Snowflake notebooks:

- [snow notebook create](/developer-guide/snowflake-cli/command-reference/notebook-commands/create)
- [snow notebook deploy](/developer-guide/snowflake-cli/command-reference/notebook-commands/deploy)
- [snow notebook execute](/developer-guide/snowflake-cli/command-reference/notebook-commands/execute)
- [snow notebook get-url](/developer-guide/snowflake-cli/command-reference/notebook-commands/get-url)
- [snow notebook open](/developer-guide/snowflake-cli/command-reference/notebook-commands/open)

You can get a list of all available notebooks by running the `snow object list notebook` command. For more information, see [snow object list](/developer-guide/snowflake-cli/command-reference/object-commands/list).
