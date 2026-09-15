# Managing Git repositories

You can integrate your remote Git repository with Snowflake so that files from the repository are synchronized to a special kind of stage called a *repository stage*. The repository stage acts as a local Git repository with a full clone of the remote repository, including branches, tags, and commits.

For more information, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).

Snowflake CLI supports the following git operations:

- [Setting up a Git repository](/developer-guide/snowflake-cli/git/setup-git)
- [Refreshing a repository](/developer-guide/snowflake-cli/git/refresh-repo)
- [Listing the contents of a repository](/developer-guide/snowflake-cli/git/list-contents)
- [Copying files in Git](/developer-guide/snowflake-cli/git/copy-files)
- [Executing files from a repository](/developer-guide/snowflake-cli/git/execute-sql)
