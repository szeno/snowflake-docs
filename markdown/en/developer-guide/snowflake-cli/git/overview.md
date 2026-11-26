# Managing Git repositories

You can integrate your remote Git repository with Snowflake so that files from the repository are synchronized to a Git repository clone. The clone includes all branches, tags, and commits from the remote repository. Access to the clone is read-only.

For more information, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).

To create and edit files, manage branches, and commit and push changes from Snowsight, Snowflake recommends
[Git workspaces](/user-guide/ui-snowsight/workspaces-git) instead of a Git repository clone.

Snowflake CLI supports the following git operations:

- [Setting up a Git repository](/developer-guide/snowflake-cli/git/setup-git)
- [Refreshing a repository](/developer-guide/snowflake-cli/git/refresh-repo)
- [Listing the contents of a repository](/developer-guide/snowflake-cli/git/list-contents)
- [Copying files in Git](/developer-guide/snowflake-cli/git/copy-files)
- [Executing files from a repository](/developer-guide/snowflake-cli/git/execute-sql)
