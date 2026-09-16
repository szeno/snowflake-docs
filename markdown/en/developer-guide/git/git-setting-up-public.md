# Connect to a Git repository over a public network

You can set up Snowflake to access your Git repository over a public network. If your Git server
uses IP-based allowlisting, see [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress) to configure stable
egress IPs for Snowflake Git traffic.

You can have Snowflake authenticate using any of the following strategies:

- [Authenticate through an OAuth flow](#label-git-setup-oauth).

  Configure an API integration to allow for an OAuth2 flow.
- [Authenticate with a token](#label-git-setup-token), such as a personal access token.

  Configure a secret containing the username and token to use, then configure an API integration that allows Snowflake to use the
  secret when authenticating.
- [No authentication](#label-git-setup-no-auth).

  Configure an API integration with details about the Git repository server.

## Configure for authenticating with OAuth

![Diagram showing components needed to configure Git connection requiring no authentication](/static/images/git-components-oauth.png)

You can configure Snowflake to authenticate with the remote Git repository using an OAuth2 flow.

GitHubOAuth2

The [Snowflake GitHub App](https://github.com/apps/snowflakedb) is a pre-configured OAuth2 application that simplifies
authentication. You don’t need to register an OAuth application or a redirect URI.

Note

The Snowflake GitHub App works with github.com, including standard GitHub Enterprise Cloud organizations
hosted there. GitHub Enterprise Cloud with data residency (`*.ghe.com`) and GitHub Enterprise Server
require OAuth2 instead.

1. Create an API integration that specifies the Snowflake GitHub App:

   Copy code

   ```
   CREATE OR REPLACE API INTEGRATION my_git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://github.com')
     API_USER_AUTHENTICATION = (TYPE = SNOWFLAKE_GITHUB_APP)
     ENABLED = TRUE;
   ```
2. Create a workspace connected to a Git repository as described in [Create a Git workspace](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace).

For any repository provider, you can create an API integration that specifies OAuth2 parameters
directly. Before you begin, create an OAuth application with your provider and collect the client ID, client secret,
authorization endpoint, and token endpoint. For end-to-end, provider-specific instructions, see the quickstarts for
[GitLab](https://www.snowflake.com/en/developers/guides/snowflake-git-oauth-gitlab/),
[Azure DevOps](https://www.snowflake.com/en/developers/guides/snowflake-git-oauth-azure-devops/), or
[Bitbucket](https://www.snowflake.com/en/developers/guides/snowflake-git-oauth-bitbucket/).

1. Register the Snowflake redirect URI with your Git provider.

   When you register the OAuth application, the provider asks for a redirect URI (sometimes called a callback URL).
   Set this to the following value, based on the cloud region that hosts your Snowflake account:

   ```
   https://apps-api.c1.<region>.<cloud>.app.snowflake.com/oauth/complete-secret
   ```

   Replace `<region>` and `<cloud>` with the values for your Snowflake deployment. For example, for an account
   in AWS US West (Oregon), the redirect URI is
   `https://apps-api.c1.us-west-2.aws.app.snowflake.com/oauth/complete-secret`.
2. Create an API integration that specifies your OAuth2 parameters.

   For details on each parameter, see
   [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration#label-create-api-integration-git-repo-optional-parameters).

   Copy code

   ```
   CREATE OR REPLACE API INTEGRATION my_git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://example.com/my_account')
     API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_AUTHORIZATION_ENDPOINT = '<your_oauth_authorization_endpoint>'
    OAUTH_TOKEN_ENDPOINT = '<your_oauth_token_endpoint>'
    OAUTH_CLIENT_ID = '<your_oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<your_oauth_client_secret>'
    OAUTH_ACCESS_TOKEN_VALIDITY = 3600
    OAUTH_REFRESH_TOKEN_VALIDITY = 2592000
    OAUTH_ALLOWED_SCOPES = ( 'read_api', 'read_repository', 'write_repository' )
     )
     ENABLED = TRUE;
   ```
3. Create a workspace connected to a Git repository as described in [Create a Git workspace](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace).

## Configure for authenticating with a token

![Diagram showing components needed to configure Git connection requiring no authentication](/static/images/git-components-token-pat.png)

To have Snowflake authenticate with the Git repository by using a username and token such as a personal access token (PAT), follow
these steps:

1. Provide credentials in a [basic authentication secret](/sql-reference/sql/create-secret#label-create-secret-basic-auth-params).

   To provide the credentials that Snowflake uses to authenticate with the repository, create a secret that contains the following:

   - A TYPE value of `password`
   - A username and token, such as a personal access token (PAT)

     If your Git repository is hosted on Bitbucket, specify `x-token-auth` as the username value.

     Note

     For information about creating a personal access token in GitHub, see
     [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
     in the GitHub documentation.

   For more information on the SQL command for creating a secret, see the [CREATE SECRET](/sql-reference/sql/create-secret).

   Code in the following example creates a secret called `my_git_secret` with a username and the user’s personal access token to use as
   credentials:

   Copy code

   ```
   CREATE OR REPLACE SECRET db.schema.my_git_secret
     TYPE = password
     USERNAME = 'gladyskravitz'
     PASSWORD = 'ghp_token';
   ```
2. Create an API integration that supports authenticating with a token.

   To create an API integration for access to a Git repository with a token, specify the following details:

   - `git_https_api` as the value of the API\_PROVIDER parameter
   - HTTPS endpoints to which requests must be limited as values of the API\_ALLOWED\_PREFIXES parameter

   For more information, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

   Copy code

   ```
   CREATE OR REPLACE API INTEGRATION my_git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://github.com/my-account')
     ALLOWED_AUTHENTICATION_SECRETS = (my_git_secret)
     ENABLED = TRUE;
   ```
3. Create a Git repository clone as described in [Create a Snowflake Git repository clone](#label-git-create-clone-public).

## Configure for no authentication

![Diagram showing components needed to configure Git connection requiring no authentication](/static/images/git-components-no-auth.png)

To set up Snowflake to use a Git repository without authenticating, follow these steps:

1. Create an API integration that supports access without authenticating, and specify the following details:

   - `git_https_api` as the value of the API\_PROVIDER parameter
   - HTTPS endpoints to which requests must be limited as values of the API\_ALLOWED\_PREFIXES parameter

   For more information, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

   Copy code

   ```
   CREATE OR REPLACE API INTEGRATION my_git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://example.com/my-account')
     ENABLED = TRUE;
   ```
2. Create a Git repository clone as described in [Create a Snowflake Git repository clone](#label-git-create-clone-public).

## Create a Snowflake Git repository clone

After you configure Snowflake for access to your remote repository, create a Git repository clone in Snowflake to contain files
fetched from the remote repository.

Note

For information on creating a Git workspace in Snowsight, see [Create a Git workspace](/user-guide/ui-snowsight/workspaces-git#label-create-a-git-workspace).

A Git repository clone in Snowflake specifies the following details:

- The remote repository’s origin

  In Git, `origin` is the remote repository’s URL. Use that URL when setting up Snowflake to use a remote Git repository.
  The URL must use HTTPS. For example, you can retrieve the origin URL in the following ways:

  - In the GitHub user interface, you can get the origin URL from the repository home page. Select the **Code** button,
    and then copy the HTTPS URL from the box displayed beneath the button.
  - From the command line, use the `git config` command from within your local repository, as in the following example:

    Copy code

    ```
    $ git config --get remote.origin.url
    ```

    The command produces output such as the following:

    ```
    https://github.com/my-account/snowflake-extensions.git
    ```

    For reference information about `git config`, see the [git documentation](https://git-scm.com/docs/git-config).
- Credentials, if needed, for Snowflake to use when authenticating with the repository

  For the GIT\_CREDENTIALS parameter, specify a Snowflake [secret](/sql-reference/sql/create-secret) you created.
- [An API integration](/sql-reference/sql/create-api-integration) specifying details for Snowflake interaction with the
  repository API

You can create a Git repository clone by using either Snowsight or SQL.

SQLSnowsight

Note

Before creating a Git repository clone, you’ll need to create [a secret](/sql-reference/sql/create-secret) (if the remote
repository requires authentication) and [an API integration](/sql-reference/sql/create-api-integration).

Code in the following example creates a Git repository clone called `snowflake_extensions`. The clone specifies
the `my_git_api_integration` API integration and the `my_git_secret` secret with credentials for authenticating.

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT CREATE GIT REPOSITORY ON SCHEMA myco_db.integrations TO ROLE myco_git_admin;
GRANT USAGE ON INTEGRATION my_git_api_integration TO ROLE myco_git_admin;
GRANT USAGE ON SECRET db.schema.my_git_secret TO ROLE myco_git_admin;

USE ROLE myco_git_admin;

CREATE OR REPLACE GIT REPOSITORY snowflake_extensions
  API_INTEGRATION = my_git_api_integration
  GIT_CREDENTIALS = my_git_secret
  ORIGIN = 'https://github.com/my-account/snowflake-extensions.git';
```

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. In the Horizon Catalog Explorer, select the database and schema that you want to contain the Git repository clone you’re creating.
4. Select **Create** » **Git Repository**.
5. In the **Create Git Repository** dialog, for **Repository Name**, enter a name that will uniquely identify this repository
   clone in the schema.

   For naming guidelines, see [Identifier requirements](/sql-reference/identifiers-syntax).
6. For **Origin**, enter the remote repository’s origin URL.
7. From the **API Integration** drop-down menu, select the API integration to reference when creating the Git repository clone.

   If you don’t have an API integration to use, select **Create new API integration in Worksheets** to use SQL to create one.
   For more information, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).
8. Optional: For the **Comment**, enter text describing this integration for others.
9. Optional: If the remote repository requires authentication, set the **Authentication** toggle to the *on* position.

   - If you turned on the toggle, from the **Secret** menu, select the secret that should be referenced by the Git integration to
     authenticate with the remote repository.

     If you don’t have a secret to use, select **Create new secret in Worksheets** to use SQL to create one. For
     more information, see [CREATE SECRET](/sql-reference/sql/create-secret).
10. Select **Create**.

When you successfully create the integration, the Git repository clone appears beneath the schema, in a **Git Repositories** directory.
You’ll also see a page that lists repository directories, branches, and tags.
