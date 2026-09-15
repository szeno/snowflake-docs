# Setting up a Git repository

You can integrate your remote Git repository with Snowflake so that files from the repository are synchronized to a special kind of stage called a *repository stage*. The repository stage acts as a local Git repository with a full clone of the remote repository, including branches, tags, and commits.

For more information, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).

## Before you start

Before setting a Git repository, you need the following information:

- URL for the remote repository (also called the `origin` in Git).
- Optional credentials for connecting to Git, including a secret, username, and password.
- Optional API integration ID.
- Role or user with privileges to create API integrations, if you do not already have an API integration.

For more information, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

## Set up a Git repository

To clone a Git repository into Git repository stage, use the `snow git setup` command, as shown:

Copy code

```
snow git setup <REPO_NAME>
```

where:

- `<REPO_NAME>` is the ID of the repository stage you want to create. Note that if the repository stage already exists, the command fails.

The `snow git setup` command provides a series of prompts to collect the necessary information, as shown in the following examples:

- Create a repository that requires a secret and credentials:

  Copy code

  ```
  $ snow git setup snowcli_git
  Origin url: https://github.com/snowflakedb/snowflake-cli.git
  Use secret for authentication? [y/N]: y
  Secret identifier (will be created if not exists) [snowcli_git_secret]: new_secret
  Secret 'new_secret' will be created
  username: john_doe
  password/token: ****
  API integration identifier (will be created if not exists) [snowcli_git_api_integration]:
  ```

  ```
  Secret 'new_secret' successfully created.
  API integration snowcli_git_api_integration successfully created.
  +------------------------------------------------------+
  | status                                               |
  |------------------------------------------------------|
  | Git Repository SNOWCLI_GIT was successfully created. |
  +------------------------------------------------------+
  ```
- Create a repository without a secret and an existing API integration ID:

  Copy code

  ```
  $ snow git setup snowcli_git
  Origin url: https://github.com/snowflakedb/snowflake-cli.git
  Use secret for authentication [y/N]: n
  API integration identifier (will be created if not exists) [snowcli_git_api_integration]: EXISTING_INTEGRATION
  ```

  ```
  Using existing API integration 'EXISTING_INTEGRATION'.
  +------------------------------------------------------+
  | status                                               |
  |------------------------------------------------------|
  | Git Repository SNOWCLI_GIT was successfully created. |
  +------------------------------------------------------+
  ```

If the role or user specified in your [connection](/developer-guide/snowflake-cli/connecting/configure-connections) has not been granted, executing this command generates an error similar to the following:

Copy code

```
003001 (42501): 01b2f095-0508-c66d-0001-c1be009a66ee: SQL access control error: Insufficient privileges to operate on account XXX
```

In this situation, you should check your connection configuration or ask your account administrator to give you the necessary privileges or to create the integration for you. For more information, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up)
