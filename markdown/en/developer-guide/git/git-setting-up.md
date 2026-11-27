# Setting up Snowflake to use Git

To connect your Snowflake account to a remote Git repository, you configure an API integration (and, if needed, a secret) that
specifies how Snowflake reaches and authenticates with the Git repository server. After that, Snowflake recommends that you
[create a workspace connected to the Git repository](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace), where you can create and edit files, manage
branches, and commit and push changes. You can also create a Git repository clone, which synchronizes files from the remote
repository to Snowflake so that Snowflake code can read them.

Setting up requires two decisions: which **network path** to use (public or private) and which **authentication method** to use.

## Choose your use case

The following use cases can help you pick the right authentication method:

- **Interactive development** (pulling, pushing, and creating files): configure
  [OAuth authentication](/developer-guide/git/git-setting-up-public#label-git-setup-oauth) to simplify sign-in for [Workspaces](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace) users.
- **Automated pipelines or ML projects**: configure [token-based authentication](/developer-guide/git/git-setting-up-public#label-git-setup-token) so that scripted
  processes can access the repository without manual sign-in.
- **Quick start with a public repository** (including Snowflake Labs): use
  [no authentication](/developer-guide/git/git-setting-up-public#label-git-setup-no-auth) to clone a public repository and run SQL scripts, notebook files, or Python
  files in [Workspaces](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace).

## Choose your network path

After you know which authentication method you need, choose how Snowflake connects to your Git server:

| Access over a public network | Access over a private network |
| --- | --- |
| [Access over a public network](/developer-guide/git/git-setting-up-public) allows you to authenticate to your remote Git repository server over the public internet. If your Git server uses IP-based allowlisting, Snowflake can route Git traffic through stable egress IP addresses on supported cloud providers. For details, see [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress).   1. Configure Snowflake for access to the repository.   Choose one of the following authentication methods:   - [No authentication](/developer-guide/git/git-setting-up-public#label-git-setup-no-auth).   Configure an API integration with details about the Git repository server. You don’t provide credentials.   - [Authenticate with a token](/developer-guide/git/git-setting-up-public#label-git-setup-token), such as a personal access token.   Configure a secret containing the username and token to use, then configure an API integration that allows Snowflake to use the secret when authenticating.   - [Authenticate through an OAuth flow](/developer-guide/git/git-setting-up-public#label-git-setup-oauth).   Configure an API integration to support OAuth2 authentication. In this case, you don’t need to create a secret.   2. [Create a Git workspace](/developer-guide/git/git-setting-up-public#label-git-create-workspace-public) (recommended) or a    [Git repository clone](/developer-guide/git/git-setting-up-public#label-git-create-clone-public) to which you can synchronize files from the remote repository. | [Access over a private network](/developer-guide/git/git-setting-up-private) routes Git traffic through a dedicated outbound private link connection instead of the public internet. Use this when your organization requires full network isolation between Snowflake and your Git server.   1. [Configure the private link connection](/developer-guide/git/git-setting-up-private#label-git-setup-private-link-connection).   Before you can configure Snowflake for access to the remote Git repository, you’ll need to set up a private link between Snowflake and your cloud service provider.   2. [Configure Snowflake access to the remote Git repository](/developer-guide/git/git-setting-up-private#label-git-setup-private-link-snowflake-access).   After you’ve set up private link between Snowflake and your cloud service provider, you can configure Snowflake access to the remote Git repository.   3. [Create a Git workspace](/developer-guide/git/git-setting-up-private#label-git-create-workspace-private) (recommended) or a    [Git repository clone](/developer-guide/git/git-setting-up-private#label-git-create-clone-private) to which you can synchronize files from the remote repository. |

Expand

Show lessSee more
