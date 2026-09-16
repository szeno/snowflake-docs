# Connect to a Git repository over a private network

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can configure Snowflake to establish connectivity through an outbound private link connection between Snowflake and your cloud
infrastructure. Snowflake routes Git traffic through this connection to the Git repository server.

With a private link connection, Snowflake routes Git traffic through a dedicated private
network connection, avoiding the public internet entirely. This section describes the steps at a high level.

1. [Configure the private link connection](#label-git-setup-private-link-connection).

   You’ll apply configuration changes to both Snowflake and your cloud service infrastructure. This topic describes the steps on the
   Snowflake side. For details about all the steps, including about configuring your cloud service provider, see the knowledge base article
   [Configuring Git Integration with Snowflake over Private Link](https://community.snowflake.com/s/article/Configuring-Git-Integration-with-Snowflake-over-Private-Link).
2. [Configure Snowflake access to the remote Git repository](#label-git-setup-private-link-snowflake-access).

Note

Snowflake supports only connections within the same cloud and region. For example, if your Snowflake deployment is on AWS in the
us-west-2 region, then your other components must also be in that region.

## Configure the private link connection

Before you can configure Snowflake for access to the remote Git repository, you must set up a private link between Snowflake and
your cloud service provider.

To apply configuration changes to both Snowflake and your infrastructure, follow these steps:

1. In your cloud service provider, create a private link service to receive requests from the Snowflake private endpoint service.

   For details, see the knowledge base article
   [Configuring Git Integration with Snowflake over Private Link](https://community.snowflake.com/s/article/Configuring-Git-Integration-with-Snowflake-over-Private-Link).
2. In Snowflake, provision a private endpoint that will reach your infrastructure through a private IP.

   To provision the endpoint, use the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) function with the following
   two arguments:

   - Your cloud provider’s private link service ID
   - Your Git server’s domain name

AWSAzureGoogle Cloud

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.vpce.us-west-2.vpce-svc-xxx', // VPC Endpoint Service Name
  'git_address.com' // Git server domain
);
```

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
'/subscriptions/9217bbdd-434e-4dbb-97c2-0825c627a277/resourceGroups/git-server_group/providers/Microsoft.Network/privateLinkServices/git-server-pl-service', // Private Service ID
  'git_address.com' // Git server domain
);
```

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'projects/my-google-project/regions/us-east4/serviceAttachments/gitservice', // Service attachement field
  'git_address.com' // Git server domain
);
```

3. In your cloud service provider, accept the Snowflake private endpoint setup to finish setting up the private link connection.
4. To check status of the provisioning, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info)
   system function.

## Configure Snowflake access to the remote Git repository

After you set up a private link between Snowflake and your cloud service provider, you can configure Snowflake access to the remote
Git repository.

1. Create an API integration that supports authenticating with a certificate.

   Because Snowflake will reach your Git server using the HTTPS protocol, the domain name needs to have a valid certificate. The
   configuration you use differs depending on whether you use a self-signed certificate or a certificate signed by a certificate authority.

   - Using a self-signed certificate:

     ![Diagram showing components needed to configure Git connection requiring no authentication](/static/images/git-components-cert-self-signed.png)
     1. Provide credentials in a [generic string secret](/sql-reference/sql/create-secret#label-create-secret-generic-string).

        This should be a public key of a self-signed domain to establish an HTTPS connection. To provide to Snowflake the credentials
        it will use to authenticate with the server, create a secret that contains the following details:

        - A TYPE parameter value of `GENERIC_STRING`
        - A public certificate string as the value of the SECRET\_STRING parameter

          For the parameter’s value, specify a secret string, such as a public certificate body.

        Copy code

        ```
        CREATE OR REPLACE SECRET my_public_certificate
          TYPE = GENERIC_STRING
          SECRET_STRING = '-----BEGIN CERTIFICATE-----
           <certificate_body>
           -----END CERTIFICATE-----';
        ```
     2. Create an API integration to integrate with the Git API, and specify the following details:

        - An API\_PROVIDER parameter set to `git_https_api`
        - An API\_ALLOWED\_PREFIXES set to the base URL beneath which access is allowed
        - A USE\_PRIVATELINK\_ENDPOINT parameter set to `TRUE`
        - A TLS\_TRUSTED\_CERTIFICATES parameter set to the name of the secret you created, which contains the certificate

        For more information, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

        Copy code

        ```
        CREATE OR REPLACE API INTEGRATION my_git_api_integration
          API_PROVIDER = git_https_api
          API_ALLOWED_PREFIXES = ('https://example.com/my-account')
          ALLOWED_AUTHENTICATION_SECRETS = ALL
          USE_PRIVATELINK_ENDPOINT = TRUE
          TLS_TRUSTED_CERTIFICATES = (my_public_certificate)
          ENABLED = TRUE;
        ```
   - Using a certificate signed by a certificate authority:

     ![Diagram showing components needed to configure Git connection requiring no authentication](/static/images/git-components-cert-ca-signed.png)
     1. Create an API integration to integrate with the Git API, and specify the following details:

        - An API\_PROVIDER parameter set to `git_https_api`
        - An API\_ALLOWED\_PREFIXES set to the base URL beneath which access is allowed
        - A USE\_PRIVATELINK\_ENDPOINT parameter set to `TRUE`
        - A TLS\_TRUSTED\_CERTIFICATES parameter set to the name of the secret you created, which contains the certificate

        For more information, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

        Copy code

        ```
        CREATE OR REPLACE API INTEGRATION my_git_api_integration
          API_PROVIDER = git_https_api
          API_ALLOWED_PREFIXES = ('https://example.com/my-account')
          ALLOWED_AUTHENTICATION_SECRETS = ALL
          USE_PRIVATELINK_ENDPOINT = TRUE
          ENABLED = TRUE;
        ```
2. Provide credentials in a [basic authentication secret](/sql-reference/sql/create-secret#label-create-secret-basic-auth-params).

   After successfully connecting to the Git server over private link, you must still authenticate with the repository by creating
   another secret that provides credentials for the repository.

   To provide the credentials that Snowflake uses to authenticate with the repository, create a secret that contains the following:

   - A TYPE value of `password`
   - A username and token, such as a personal access token (PAT)

     Note

     For information about creating a personal access token in GitHub, see
     [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
     in the GitHub documentation.

   For more information on the SQL command for creating a secret, see the [CREATE SECRET](/sql-reference/sql/create-secret).
3. Create a Git repository clone as described in [Create a Snowflake Git repository clone](#label-git-create-clone-private).

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
