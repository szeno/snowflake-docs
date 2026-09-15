# Using a Git repository in Snowflake

You can integrate your remote Git repository with Snowflake so that files from the remote repository are synchronized to a
Git repository clone in Snowflake. The clone includes all branches, tags, and commits from the remote repository.

To get started, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).
For a complete list of limitations, see [Git in Snowflake limitations](/developer-guide/git/git-limitations).

## Supported platforms

You can integrate Git repositories that use the following platforms. This includes repositories based on these platforms but
available at custom URLs. For example, a repository based on GitHub does not need to be at github.com.

- GitHub
- GitLab
- BitBucket
- Azure DevOps
- AWS CodeCommit

## How Snowflake works with a remote Git repository

With a remote Git repository integrated with your Snowflake account, you synchronize files from the remote repository to a
Git repository clone in Snowflake. To access a file in Snowflake, you refer to it in the Git repository clone. For more information about
using repository files, see [Use a Git repository file as a stored procedure handler](/developer-guide/git/git-examples#label-integrating-git-repository-using-procedure).

![Diagram showing Git repository exchanging files with development tools and Snowflake.](/static/images/git-architecture.png)

After you integrate your remote repository with Snowflake, you can continue using your development tools and local repository as before.
Through the Git repository clone, Snowflake becomes another client of your repository separate from your local repository.

With a Git repository clone in Snowflake, you can do the following:

- Fetch the latest version of branches, tags, and commits from the remote repository.
- Browse folders, search for files, and select branches or tags.
- Copy file paths for referencing in Snowflake code (such as handler code for functions, tasks, or procedures).
- [Execute immediate from](/sql-reference/sql/execute-immediate-from) `.sql` files.
- Commit and push changes to the remote repository from [Workspaces](/user-guide/ui-snowsight/workspaces-git#label-integrate-a-git-repository),
  [Streamlit apps](/developer-guide/streamlit/features/git-integration), and
  [Snowflake notebooks](/user-guide/ui-snowsight/notebooks-snowgit).
- Import files from the repository clone into code you run in Snowflake, such as procedures and UDFs.

## Next steps

- [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up)
- [Working with Git repositories](/developer-guide/git/git-operations)
- [Examples of using Git with Snowflake](/developer-guide/git/git-examples)
- [Troubleshooting Git in Snowflake](/developer-guide/git/git-troubleshooting)
- [Git in Snowflake limitations](/developer-guide/git/git-limitations)
