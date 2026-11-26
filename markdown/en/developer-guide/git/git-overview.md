# Using a Git repository in Snowflake

You can connect your Snowflake account to a remote Git repository in the following ways:

- **Git workspaces (recommended):** Create a [workspace connected to a Git repository](/user-guide/ui-snowsight/workspaces-git)
  to develop directly in Snowsight. In a Git workspace, you can create and edit files, create and switch branches, pull
  changes, commit and push to the remote repository, and resolve conflicts. Each Git workspace belongs to the user who creates it
  and can’t be shared. For more information, see [Git workspace ownership](/user-guide/ui-snowsight/workspaces-git#label-git-workspace-ownership).
- **Git repository clone:** Create a Git repository clone with [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository) so that files from the
  remote repository are synchronized to Snowflake. The clone includes all branches, tags, and commits from the remote repository.
  Access to the clone is read-only. Use a clone when Snowflake code such as tasks or stored procedures needs to reference
  repository files.

Snowflake recommends Git workspaces for working with a Git repository from Snowflake.

Note

A Git repository in Snowflake is not required for CI/CD. In a typical [CI/CD pipeline](/developer-guide/cicd/index), the CI runner checks out the repository and deploys directly to Snowflake. Use a Git workspace to develop with repository files in Snowsight, and a Git repository clone when Snowflake code needs to reference repository files.

Both options use an API integration to access the remote repository. To configure it, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).
For a complete list of limitations, see [Git in Snowflake limitations](/developer-guide/git/git-limitations).

## Supported platforms

You can integrate Git repositories that use the following platforms. This includes repositories based on these platforms but
available at custom URLs. For example, a repository based on GitHub does not need to be at github.com.

- GitHub
- GitLab
- BitBucket
- Azure DevOps
- AWS CodeCommit

## How a Git repository clone works

A Git repository clone is a schema-level object that’s owned by a role. When you
[fetch from the remote repository](/developer-guide/git/git-operations#label-git-integration-refreshing-stage), Snowflake synchronizes the clone with the branches, tags,
and commits in the remote repository. The clone is read-only: you can’t create, edit, commit, or push files through it.

Because the clone is owned by a role rather than by an individual user, Snowflake objects and code can reference files in it. For
example, stored procedures, UDFs, and tasks can use repository files as handler code, and you can run `.sql` files with
[EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from). Code that references a file in the clone uses the version of the
file from the most recent fetch. Changes pushed to the remote repository after that fetch aren’t visible in Snowflake until you fetch
again. For more information about using repository files, see [Use a Git repository file as a stored procedure handler](/developer-guide/git/git-examples#label-integrating-git-repository-using-procedure).

To create, edit, commit, and push files, including Streamlit app and notebook files, use a
[Git workspace](/user-guide/ui-snowsight/workspaces-git) instead.

![Diagram showing Git repository exchanging files with development tools and Snowflake.](/static/images/git-architecture.png)

After you create a Git repository clone, you can continue using your development tools and local repository as before.
Through the Git repository clone, Snowflake becomes another client of your repository that reads from it, separate from your local
repository.

With a Git repository clone in Snowflake, you can do the following:

- Fetch the latest version of branches, tags, and commits from the remote repository.
- Browse folders, search for files, and select branches or tags.
- Copy file paths for referencing in Snowflake code (such as handler code for functions, tasks, or procedures).
- [Execute immediate from](/sql-reference/sql/execute-immediate-from) `.sql` files.
- Import files from the repository clone into code you run in Snowflake, such as procedures and UDFs.

## Next steps

- [Integrate workspaces with a Git repository](/user-guide/ui-snowsight/workspaces-git)
- [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up)
- [Working with Git repositories](/developer-guide/git/git-operations)
- [Examples of using Git with Snowflake](/developer-guide/git/git-examples)
- [Troubleshooting Git in Snowflake](/developer-guide/git/git-troubleshooting)
- [Git in Snowflake limitations](/developer-guide/git/git-limitations)
