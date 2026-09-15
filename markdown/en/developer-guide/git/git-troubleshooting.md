# Troubleshooting Git in Snowflake

Use the tips described in this topic to resolve issues when using a Git repository in Snowflake.

## Error message: “Failed to access the Git repository. Operation ‘clone’ is not authorized”

You might see this message for one of multiple reasons, but it’s typically due to a misconfiguration in Snowflake integration with the
remote Git repository. To eliminate common misconfiguration issues, confirm the following:

- You’re using correct credentials for authenticating with the remote Git repository, such as a correct username-and-password combination or
  correct personal access token.

  For more on authenticating from Snowflake, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).
- You’ve correctly configured the Git repository URL, including the allowed prefixes in the API configuration.

  Read more about specifying an allowed prefix and origin URL in [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).
- You aren’t experiencing a connectivity issue, such as when the repository is in a private network that hasn’t been configured
  for private link access.

  For more information about connecting over a private network, see [Connect to a Git repository over a private network](/developer-guide/git/git-setting-up-private).

If you continue to have this issue after verifying that your configuration is correct, try the following:

- If you’re using a fine-grained token for authorization (not the Classic token), confirm that you’ve set the proper permissions on the
  token. For read-only access, setting the “Content” to “read-only” should be enough.

  For information about managing a personal access token in GitHub, see
  [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  in the GitHub documentation.
- Outside of Snowflake, clone the repository with the command-line Git client using the same URL and TOKEN values that are resulting in the
  error in Snowflake.

  This should generate more verbose output, including messages indicating what the issue might be. For example, cloning might fail from the
  command line because SSO authorization is required for the operation, and this authorization was not available for the fine-grained token.
  Switching to a Classic token might resolve this issue.

## Error message: “Processing aborted due to error” when using the `SHOW GIT BRANCHES` or `SHOW GIT TAGS` commands

You might see this message if you used Git from Snowflake during an early preview of the feature. An optimization in reading from a remote
Git repository, added in a later release, might be complicating access to remote repositories for which you configured access in that early preview.

To ensure that you’re benefitting from the optimization — and to stop receiving this error — re-create your Git repository clone using
[REPLACE GIT REPOSITORY](/sql-reference/sql/create-git-repository).

## Error message: “Private endpoint corresponding to service name xxx does not exist.”

You might see this message if you didn’t create a Private Endpoint for the domain (service) that you’re trying to reach.

Ensure that you’ve provisioned a Private Endpoint in Snowflake and approved it on the cloud provider side. For more information, see
[Configure the private link connection](/developer-guide/git/git-setting-up-private#label-git-setup-private-link-connection).

## Error message: “Failed to perform operation ‘clone’. SSL problems when connect to Git server”

You might see this message when there’s a problem with an HTTPS certificate. For example, the domain’s certificate is not signed by a
certificate authority or it does not contain the Git server domain in the chain.

## Error message: “Failed to connect to the Git Repository via Private Link. Please check your network configuration and ensure Private Link traffic is correctly routed.”

You might see this message when HTTPS traffic was not routed properly to the Git server.

Ensure that you’re routing traffic correctly in your cloud service provider. For more information, see
[Configuring Git Integration with Snowflake over Private Link](https://community.snowflake.com/s/article/Configuring-Git-Integration-with-Snowflake-over-Private-Link).
