# Git in Snowflake limitations

This topic describes limitations for using Git repositories from within Snowflake.

- Currently, only the following Snowflake features can write to the repository:

  - [Workspaces](/user-guide/ui-snowsight/workspaces-git#label-integrate-a-git-repository)
  - [Streamlit applications](/developer-guide/streamlit/features/git-integration)
  - [Notebooks](/user-guide/ui-snowsight/notebooks-snowgit)

  For other Snowflake code, access to the repository is read-only.
- When you connect to a Git repository using a workspace, the following limitation applies:

  - The Git repository can’t be empty. It must have at least one commit.
- Creating a local Git repository in Snowflake is supported only when using the Workspaces user interface to create it. It isn’t
  supported when you create the repository by using [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository) in a workspace. This is because
  when using the SQL command, the flow does not include presenting a user interface with which to sign in.
- Sharing Snowflake Git repository clones is not supported through data sharing or apps built on the Snowflake Native App Framework.
- Creating Snowflake Git repository clones inside application packages is not supported and might be blocked in the future.
- Creating Snowflake Git repository clones inside native applications on the consumer side is not supported.
- Snowflake doesn’t currently support submodules, so you won’t be able to see submodule files. Snowflake won’t download those files
  from the remote repository nor upload them to the remote repository.
- Git repositories larger than 2 GB aren’t supported.
