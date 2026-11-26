# Git in Snowflake limitations

This topic describes limitations for using Git repositories from within Snowflake.

- Only [Git workspaces](/user-guide/ui-snowsight/workspaces-git#label-integrate-a-git-repository) can push changes to the remote repository. To edit and push changes to
  files such as Streamlit app files or notebook files, work with them in a Git workspace. Access to a Git repository clone is
  read-only.
- When you connect to a Git repository using a workspace, the following limitation applies:

  - The Git repository can’t be empty. It must have at least one commit.
- OAuth sign-in is available when you create a Git workspace or a Git repository clone in Snowsight. It isn’t available
  when you create a Git repository clone by running the [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository) SQL command, because the SQL
  command doesn’t present a user interface with which to sign in.
- Sharing Snowflake Git repository clones is not supported through data sharing or apps built on the Snowflake Native App Framework.
- Creating Snowflake Git repository clones inside application packages is not supported and might be blocked in the future.
- Creating Snowflake Git repository clones inside native applications on the consumer side is not supported.
- Snowflake doesn’t currently support submodules, so you won’t be able to see submodule files. Snowflake won’t download those files
  from the remote repository.
- Git repositories larger than 2 GB aren’t supported.
