# Workload identity federation

This document is for the following audiences:

- Developers of in-house cloud services.
- Administrators who manage integrations with internal and external services.
- Developers of multi-tenant SaaS applications who want to issue
  [OpenID Connect (OIDC) Federation](https://openid.net/developers/how-connect-works/) ID tokens to individual workloads that are running
  on their platform so that each customer workload can authenticate to Snowflake as a dedicated user.

Workload identity federation (WIF) is a service-to-service authentication method that lets workloads, such as applications, services, or
containers, authenticate with Snowflake using their cloud provider’s native identity system, such as AWS Identity and Access Management (AWS IAM) roles, Microsoft Entra ID, and
Google Cloud service accounts, to get an attestation that Snowflake can use and validate.

WIF removes the need to manage and store long-lived credentials such as passwords, API keys, key pairs, and
programmatic access tokens for authenticating to Snowflake. WIF also reduces the complexity involved in getting
credentials, where other methods, such as [External OAuth](/user-guide/oauth-ext-overview), can require more effort to set up.
Applications, services, and containers that use Snowflake connectors automatically get short-lived credentials from their platform’s
identity provider (IdP) through each platform’s native mechanisms.

## Benefits

This section describes why you may want to use WIF for authentication:

- **Cost effective**: Using existing IdPs to manage service identities reduces the need for additional tools or licenses, which can be
  cost-effective.
- **Interoperability**: Popular cloud provider services, such as AWS IAM, Entra ID, and Google Cloud, support and
  encourage WIF as an authentication method for external workloads.
- **Convenient auditing and monitoring**:
  - Administrators can use existing cloud provider services, such as
    [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) and [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview), to log and monitor activity.
  - Snowflake administrators can query the LOGIN\_HISTORY and CREDENTIALS views in the
    [ACCOUNT\_USAGE schema](/sql-reference/account-usage) to monitor and audit services that use WIF.

## Workflow for implementing workload identity federation

You can use WIF to authenticate a variety of workloads using different IdPs, but the basic workflow, as shown in
the following steps, remains the same:

1. As a workload administrator, configure your service to use a native identity provider so that the provider can issue an *attestation* of
   your workload’s identity. This attestation is often, but not always, a JSON Web Token (JWT).
2. As a Snowflake administrator, create a Snowflake service user for your workload. You set the properties of this user to values found in
   the attestation sent by the provider. For example, a user property might specify the name of an IAM role or the issuer URL of the
   provider.
3. As a workload developer, configure your workload to use a [Snowflake driver](#label-wif-supported-drivers). Drivers send the
   attestation to Snowflake for verification.

   You can also use workload identity federation to authenticate requests to Snowflake APIs. For more information, see
   [Authenticating requests to Snowflake SQL APIs](/developer-guide/sql-api/authenticating) and
   [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

To view end-to-end examples of this workflow for different types of workloads and IdPs, see [Use cases](#label-wif-getting-started).

## Access control requirements

To configure WIF for a Snowflake service user (that is, a user with their TYPE property set to `SERVICE` or `SERVICE_AGENT`)
you must grant your activated roles one of the following privileges:

- OWNERSHIP on the service user.
- MODIFY PROGRAMMATIC AUTHENTICATION METHODS on the service user.

## Supported Snowflake drivers

A workload uses a Snowflake driver to send an attestation when it connects to Snowflake. The following drivers support workload identity
federation:

| Driver | Minimum version |
| --- | --- |
| [Go](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Authenticator_values) | v1.16.0 |
| [JDBC](/developer-guide/jdbc/jdbc-configure#label-jdbc-auth-wif) | v3.26.0 |
| [.NET](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/Connecting.md) | v4.8.0 |
| [Node.js](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-auth-wif) | v2.2.0 |
| [ODBC](/developer-guide/odbc/odbc-parameters#label-odbc-auth-wif) | v3.11.0 |
| [PHP PDO](https://github.com/snowflakedb/pdo_snowflake/blob/master/README.rst) | v3.6.0 |
| [Python](/developer-guide/python-connector/python-connector-connect#label-python-auth-wif) | v3.17.0 |
| [Spark Connector](/user-guide/spark-connector-use#label-spark-auth-wif) | v3.1.7 |

Expand

Show lessSee more

## Minimizing the number of Snowflake identities

Creating a dedicated Snowflake user for every WIF workload can be challenging at scale. It’s often better to consolidate so that multiple workloads authenticate with a well-defined, limited number of Snowflake service users. This approach reduces identity sprawl in Snowflake, simplifies user lifecycle management, and enables consistent access patterns without tightly coupling Snowflake users to individual workloads or infrastructure.

- [Create a single user for multiple workloads](#create-a-single-user-for-multiple-workloads)
- [Create a single user for multiple GitHub or GitLab environments](#create-a-single-user-for-multiple-github-or-gitlab-environments)

### Create a single user for multiple workloads

Some cloud providers allow the identity that is attached to a workload to impersonate another identity. For example, suppose a workload on
Google Cloud is attached to service account `A`. You can use
[service account impersonation](https://docs.cloud.google.com/iam/docs/service-account-impersonation) so that service account `A`
authenticates as service account `B`. That is, service account `A` impersonates service account `B` so that the workload can
authenticate to Snowflake as user `B`.

Impersonation is especially useful in an environment that has many workloads because creating a one-to-one mapping between each workload
and a Snowflake service user is operationally expensive and difficult to manage. By allowing multiple workloads to impersonate a shared
Snowflake identity, teams can centralize Snowflake access behind a small set of service users while enforcing access controls through the
cloud provider’s IAM.

**Prerequisite**

To use impersonation so that multiple workloads authenticate with a single Snowflake identity, the workload must be on Google Cloud or AWS.
Currently, Microsoft Azure doesn’t support impersonation.

**Workflow**

1. As the workload administrator, configure the workloads so that their attached identities impersonate another identity.
2. As the Snowflake administrator, create a service user that corresponds to the cloud provider identity that is authenticating to
   Snowflake. For example, if workloads are using service account `D` to authenticate, create a service user and set its SUBJECT parameter
   to the unique identifier of service account `D`.
3. As the workload developer, use a connection parameter of the driver to define the
   identity chain for the workloads that use impersonation. The parameter is set to a list of strings, where each string is a cloud
   provider identity (for example, a service account ID).

   The driver follows the identity chain defined in the list in order to obtain the token that is needed to authorize the next cloud
   provider identity. Each identity in the chain needs permissions to impersonate the next identity only. The final identity in the list
   obtains the Snowflake connection token that is used to connect to Snowflake.

   To obtain the syntax of the connection parameter for your driver, see the driver documentation.

**Example**

Suppose a Google Cloud workload is attached to service account `A` but impersonates service account `B`, which then
impersonates service account `D`. To set up the Python driver so that the workload authenticates with WIF using the identity of service
account `D`, define the connection parameter as follows:

Copy code

```
workload_identity_impersonation_path=['service_account_a@my-project.iam.gserviceaccount.com',
                                      'service_account_b@my-project.iam.gserviceaccount.com',
                                      'service_account_d@my-project.iam.gserviceaccount.com']
```

The Snowflake service user created for the workload should contain the identifier of the final identity in the identity chain. Given the
example above, create the service user with the following command:

Copy code

```
CREATE USER <username>
  WORKLOAD_IDENTITY = (
    TYPE = GCP
    SUBJECT = 'service_account_d@my-project.iam.gserviceaccount.com'
  )
  TYPE = SERVICE
  DEFAULT_ROLE = PUBLIC;
```

### Create a single user for multiple GitHub or GitLab environments

If you’re using GitHub actions or GitLab projects, you can use the tool’s OIDC Provider to use WIF to authenticate to Snowflake. By default,
the OIDC token for each GitHub action or GitLab project might have a different subject in the `sub` claim, which would require you to
have multiple Snowflake service users, one for each subject.

However, GitHub and GitLab let you customize the `sub` claim of their OIDC tokens. This lets you configure your tool so that the subject
of OIDC tokens is the same for all of your environments. When you create a Snowflake service user, you specify the subject of the OIDC
tokens it will be receiving from GitHub or GitLab. Because the subject in the tokens will always be the same (that is, the custom value),
you only need one service user for all of your environments.

To learn more about customizing the `sub` claim of a GitHub or GitLab OIDC token, see the following resources:

- **GitHub**: To customize the subject claim for an organization or repository, see the
  [GitHub documentation](https://docs.github.com/en/actions/reference/security/oidc#customizing-the-subject-claims-for-an-organization-or-repository).
- **GitLab**: To use the Project API to customize the `sub` claim of the GitLab OIDC token, see the
  [GitLab documentation](https://docs.gitlab.com/api/projects/). Currently, the claim is customized with the
  `ci_id_token_sub_claim_components` attribute.

After you’ve defined a custom `sub` claim that is the same for all of your GitHub or GitLab environments, configure the SUBJECT
parameter of your Snowflake service user to match the custom `sub` claim.

## Hardening your security posture

You can use an [authentication policy](/user-guide/authentication-policies) to control which Snowflake service users can authenticate
with WIF. You can also create and set the authentication policy so that a workload can authenticate only if it uses
a specified identity provider, or an account within that provider.

For example, the following authentication policy allows a workload to authenticate only if it uses Microsoft Entra ID as its provider and the
issuer of the attestation is a Microsoft Entra ID tenant with tenant ID `https://login.microsoftonline.com/9ebd1ec9-9a78-4429-8f53-5cf870a812d1/v2.0`:

> Copy code
>
> ```
> CREATE AUTHENTICATION POLICY workload_policy
>   WORKLOAD_IDENTITY_POLICY=(
>     ALLOWED_PROVIDERS = (AZURE)
>     ALLOWED_AZURE_ISSUERS = (
>       'https://login.microsoftonline.com/9ebd1ec9-9a78-4429-8f53-5cf870a812d1/v2.0')
>   );
> ```

For more information about the `WORKLOAD_IDENTITY_POLICY` parameter, see [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy).

For more information about setting an authentication policy so it is enforced, see [Setting an authentication policy on an account or user](/user-guide/authentication-policies#label-authentication-policy-set).

## Use cases

The following use cases are examples of implementing WIF for a workload:

- [Authenticate using AWS IAM roles and a Snowflake Python driver](#authenticate-using-aws-iam-roles-and-a-snowflake-python-driver)
- [Authenticate using Microsoft Entra ID and a Snowflake Python driver](#authenticate-using-microsoft-idp-and-a-snowflake-python-driver)
- [Authenticate using Google Cloud service accounts and a Snowflake Python driver](#authenticate-using-google-csp-service-accounts-and-a-snowflake-python-driver)
- [Authenticate using an OpenID Connect (OIDC) issuer from Elastic Kubernetes Service (EKS)](#authenticate-using-an-openid-connect-oidc-issuer-from-aws-kubernetes)
- [Authenticate using an OpenID Connect (OIDC) issuer from Azure Kubernetes Service (AKS)](#authenticate-using-an-openid-connect-oidc-issuer-from-microsoft-azure-kubernetes)
- [Authenticate using an OpenID Connect (OIDC) issuer from Google Kubernetes Engine (GKE)](#authenticate-using-an-openid-connect-oidc-issuer-from-google-kubernetes)
- [Authenticate using SPIFFE/SPIRE](#authenticate-using-spiffespire)
- [Authenticate using a custom OpenID Connect (OIDC) Provider](#authenticate-using-a-custom-openid-connect-oidc-provider)

### Authenticate using AWS IAM roles and a Snowflake Python driver

AWS WIF supports two approaches: the default `GetCallerIdentity`-based approach and a JWT-based approach
using `GetWebIdentityToken`. Snowflake drivers support both. Snowflake recommends the JWT-based method for a
more future-proof approach that aligns with industry-standard token patterns. For instructions, see
[Upgrade to JWT-based authentication (recommended)](#label-wif-aws-upgrade-jwt).

Complete the following tasks to use WIF to authenticate to Snowflake from your AWS service:

- [Configure AWS](#configure-aws)
- [Configure Snowflake](#configure-snowflake)
- [Configure your workload to use a Snowflake driver](#configure-your-workload-to-use-a-snowflake-driver)

#### Configure AWS

To configure your AWS service to use AWS IAM as its identity provider, attach an IAM role. For more information, see the AWS documentation
that corresponds to your workload.

- For Amazon EC2, see [Attach an IAM role to an instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/attach-iam-role.html).
- For AWS Lambda, see [Defining Lambda function permissions with an execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html).

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you must have the Amazon Resource Identifier (ARN) that uniquely identifies the AWS user or
role associated with the instance authenticating to Snowflake. To obtain the ARN of an IAM role, complete the following steps:

1. Sign in to the AWS Console, and then navigate to the IAM Dashboard.
2. In the left-hand navigation, select **Roles**.
3. Select the name of the role that you attached to your AWS instance.
4. In the **Summary** section, find the ARN, and then select the **Copy** icon.

Snowflake accepts the following forms of [IAM identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html):

> - `arn:aws:iam::account:user/user_name_with_path`
> - `arn:aws:iam::account:role/role_name_with_path`
> - `arn:aws:sts::account:assumed-role/role_name/role_session_name`

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER <username>
     WORKLOAD_IDENTITY = (
    TYPE = AWS
    ARN = '<amazon_resource_identifier>'
     )
     TYPE = SERVICE
     DEFAULT_ROLE = PUBLIC;
   ```

   Where `ARN` is the value you obtained before starting these steps. We recommend setting
   `ISSUER` to the account-specific issuer URL from AWS for JWT-based authentication; see
   [Upgrade to JWT-based authentication (recommended)](#label-wif-aws-upgrade-jwt).

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   import os
   import snowflake.connector

   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='AWS'
   )
   ```
3. Run your Python application. It authenticates to Snowflake using WIF.

#### Upgrade to JWT-based authentication (recommended)

By default, the connector authenticates using `GetCallerIdentity`. This upgrade uses `GetWebIdentityToken`
to send a standards-based JWT instead, providing stateless token verification and compatibility with AWS outbound identity federation.

Note

Requires Python connector v4.7.1 or later.

**AWS prerequisites:**

1. Enable outbound identity federation on your AWS account and note the account-specific issuer URL from the API response.
   For more information, see the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_outbound_getting_started.html#enable-outbound-federation).
2. Grant the IAM role `sts:GetWebIdentityToken` permission. See the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_outbound_getting_started.html#configure-iam-permissions) for an example IAM policy.

**To configure a new Snowflake user for JWT-based authentication:**

1. Run a [CREATE USER](/sql-reference/sql/create-user) statement, including both `ARN` and `ISSUER`:

   Copy code

   ```
   CREATE USER <username>
     WORKLOAD_IDENTITY = (
       TYPE = AWS
       ARN = '<amazon_resource_identifier>'
       ISSUER = '<aws_issuer_url>'
     )
     TYPE = SERVICE
     DEFAULT_ROLE = PUBLIC;
   ```

   Where `ARN` is the IAM role ARN and `ISSUER` is the account-specific issuer URL from AWS.
2. In your connection parameters, set `workload_identity_aws_use_outbound_token=True`. This instructs
   the connector to authenticate via JWT from `GetWebIdentityToken` instead of the default authentication method.

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='AWS',
     workload_identity_aws_use_outbound_token=True
   )
   ```

**To upgrade an existing Snowflake user to JWT-based authentication:**

Important

`ISSUER` must be configured on the Snowflake user **before** [setting the connection option](/user-guide/workload-identity-federation#label-wif-aws-set-conn-option). Setting the connection option without `ISSUER` configured causes JWT authentication to fail immediately.

1. Run [ALTER USER](/sql-reference/sql/alter-user) to add `ISSUER`:

   Copy code

   ```
   ALTER USER <user_name> SET WORKLOAD_IDENTITY = (
     TYPE = AWS
     ARN = '<role_arn>'
     ISSUER = '<aws_issuer_url>'
   );
   ```

   Where `ARN` is the IAM role ARN configured when creating the user, and `ISSUER` is the account-specific issuer URL from AWS.

2. In your connection parameters, set `workload_identity_aws_use_outbound_token=True`. This instructs
   the connector to authenticate via JWT from `GetWebIdentityToken` instead of the default authentication method.

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='AWS',
     workload_identity_aws_use_outbound_token=True
   )
   ```

**To revert to the default authentication method:**

Important

Remove `ISSUER` from the Snowflake user **after** [removing the connection option](/user-guide/workload-identity-federation#label-wif-aws-unset-conn-option). Reversing this order
causes JWT authentication to fail for any connections made between the two steps.

1. In your connection parameters, remove `workload_identity_aws_use_outbound_token` or set it to `False`.
   This instructs the connector to resume using the default authentication method.
2. Run [ALTER USER](/sql-reference/sql/alter-user) to remove `ISSUER`, omitting it from the `WORKLOAD_IDENTITY` properties:

   Copy code

   ```
   ALTER USER <user_name> SET WORKLOAD_IDENTITY = (
     TYPE = AWS
     ARN = '<role_arn>'
   );
   ```

   Where `ARN` is the IAM role ARN previously configured on the user.

### Authenticate using Microsoft Entra ID and a Snowflake Python driver

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from Microsoft Entra ID:

- [Configure Microsoft Entra ID](#label-wif-azure-configure-entra)
- [Configure Microsoft Azure](#label-wif-azure-configure-azure)
- [Configure Snowflake](#label-wif-azure-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-azure-set-up-a-snowflake-connector-for-python)

#### Configure Microsoft Entra ID

A Microsoft Entra ID tenant administrator must complete the following steps to allow usage of Snowflake workload identity. These steps only
need to be performed once per Microsoft Entra ID tenant:

1. Log in to the Microsoft Azure portal.
2. Ensure you have Azure tenant admin privileges.
3. Consent to installing the multi-tenant Snowflake EntraID app by visiting [the consent URI](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=fd3f753b-eed3-462c-b6a7-a4b5bb650aad&response_type=none&scope=openid&redirect_uri=https://www.snowflake.com/).

   The multi-tenant Snowflake EntraID app is publisher-verified, and represents Snowflake as a resource. The app is used as the audience for
   the access token when authenticating to Snowflake. This app only requires basic permissions and is non-privileged.
4. Select **Accept** to give permissions to the Snowflake EntraID app.

#### Configure Microsoft Azure

Complete the following steps to configure your Microsoft Azure service to use WIF:

1. Log in to the Microsoft Azure portal.
2. Select your workload, such as a [virtual machine](https://learn.microsoft.com/en-us/azure/virtual-machines/) or an [app service](https://learn.microsoft.com/en-us/azure/app-service).
3. In the sidebar, navigate to **Security** » **Identity**.
4. Enable a managed identity for an
   [Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-configure-managed-identities?pivots=qs-configure-portal-windows-vm#system-assigned-managed-identity)
   or an [Azure Function](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp).
5. Save the **Object (Principal) ID** for a later step.

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- The case-sensitive Object ID (Principal ID) of the managed identity you enabled in the [previous step](#label-wif-azure-configure-azure).
  You can use the Azure Portal to copy this identifier from the **Identity** page for your Azure VM or function.
- Your Microsoft Entra tenant ID. You use this value to construct the Authority URL.
  - To obtain the tenant ID by using the Microsoft Entra Console, see the [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant).
  - To obtain the tenant ID by using PowerShell, run the following commands:

    Copy code

    ```
    Connect-AzAccount
    Get-AzTenant
    ```

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER <username>
     WORKLOAD_IDENTITY = (
    TYPE = AZURE
    ISSUER = 'https://login.microsoftonline.com/<tenant_id>/v2.0'
    SUBJECT = '<managed_identity_object_id>'
     )
     TYPE = SERVICE
     DEFAULT_ROLE = PUBLIC;
   ```

   Where `ISSUER` and `SUBJECT` are the values that you obtained before starting these steps.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   import snowflake.connector

   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='AZURE'
   )
   ```
3. Run your Python application. It authenticates to Snowflake using WIF.

Note

As the workload developer, you might need to set an environment variable related to the managed identity that your workload administrator
enabled. If your administrator enabled a [user-assigned managed identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm#user-assigned-managed-identity) rather than a system-assigned one, you must set the
MANAGED\_IDENTITY\_CLIENT\_ID environment variable to the client ID of the managed identity that you want to use for authenticating to
Snowflake.

### Authenticate using Google Cloud service accounts and a Snowflake Python driver

Complete the following tasks to use WIF to authenticate to Snowflake from your Google Cloud service:

- [Configure Google Cloud](#configure-google-csp)
- [Configure Snowflake](#configure-snowflake-2)
- [Configure your workload to use a Snowflake driver](#configure-your-workload-to-use-a-snowflake-driver-2)

#### Configure Google Cloud

To configure your service to use Google Cloud as its identity provider, [attach a service account to your GCE or Cloud Run instance](https://cloud.google.com/compute/docs/instances/change-service-account).

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you must have the value of the service account’s `uniqueId` property. To obtain this unique ID,
use the Google Cloud CLI to run the following command:

Copy code

```
gcloud iam service-accounts describe "<SERVICE_ACCOUNT_EMAIL_ADDRESS>" --format="value(uniqueId)"
```

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER <username>
     WORKLOAD_IDENTITY = (
    TYPE = GCP
    SUBJECT = '<unique_id_of_service_account>'
     )
     TYPE = SERVICE
     DEFAULT_ROLE = PUBLIC;
   ```

   Where `SUBJECT` is the value that you obtained before starting these steps.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   import snowflake.connector

   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='GCP'
   )
   ```
3. Run your Python application. It authenticates to Snowflake using WIF.

### Authenticate using an OpenID Connect (OIDC) issuer from Elastic Kubernetes Service (EKS)

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from Elastic Kubernetes Service (EKS):

- [Configure EKS](#label-wif-oidc-aws-kubernetes-configure-aws)
- [Configure Snowflake](#label-wif-oidc-aws-kubernetes-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-oidc-aws-kubernetes-set-up-a-snowflake-connector-for-python)

#### Configure EKS

1. Configure EKS to issue ID tokens that are compatible with Snowflake.
   1. [Configure your pod deployment YAML to include a projected ServiceAccount token volume](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#launch-a-pod-using-service-account-token-projection).
   2. Configure the ID tokens to contain an audience claim with `snowflakecomputing.com`.

      The following is an example of a YAML configuration with the proper audience:

      Copy code

      ```
      kind: Pod
      metadata:
        name: nginx
      spec:
        containers:
        - image: nginx
          name: nginx
          volumeMounts:
          - mountPath: /var/run/secrets/tokens
      name: snowflake-token
        serviceAccountName: build-robot
        volumes:
        - name: snowflake-token
          projected:
      sources:
      - serviceAccountToken:
          path: snowflake-token
          expirationSeconds: 7200
          audience: snowflakecomputing.com
      ```

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- The issuer URL of the OIDC provider that is generating the ID token for the Kubernetes service account. To obtain this issuer URL, you
  can perform either of the following tasks:

  - Navigate to the **Overview** tab of your cluster, and copy the value in the **OpenID Connect provider URL** field.
  - Run the following command with access to the API server endpoint:

    Copy code

    ```
    aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
    ```
- The namespace and name of the Kubernetes service account. You use this information to construct the subject of the ID token issued by
  the OIDC provider.

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER my_eks_service
     WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://oidc.eks.<region>.amazonaws.com/id/<issuer_id>'
    SUBJECT = 'system:serviceaccount:<service_account_namespace>:<service_account_name>'
     )
     TYPE = SERVICE;
   ```

   Where `ISSUER` and `SUBJECT` are the values that you obtained before starting these steps.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='OIDC',
     token_file_path='<service_account_token_path>'
   )
   ```

   Where `service_account_token_path` is the one you created in the [Configure EKS](#label-wif-oidc-aws-kubernetes-configure-aws) step. Based
   on the YAML example in that step, the token path would be `/var/run/secrets/tokens/snowflake-token`.
3. Run your Python application. It authenticates to Snowflake using WIF.

### Authenticate using an OpenID Connect (OIDC) issuer from Azure Kubernetes Service (AKS)

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from Azure Kubernetes Service (AKS):

- [Configure AKS](#label-wif-oidc-azure-kubernetes-configure-azure)
- [Configure Snowflake](#label-wif-oidc-azure-kubernetes-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-oidc-azure-kubernetes-set-up-a-snowflake-connector-for-python)

#### Configure AKS

Configure AKS to issue ID tokens that are compatible with Snowflake:

1. [Enable the OIDC issuer on your AKS cluster](https://learn.microsoft.com/en-us/azure/aks/use-oidc-issuer).
2. Configure AKS to issue ID tokens that are compatible with Snowflake.
   1. [Configure your pod deployment YAML to include a projected ServiceAccount token volume](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#launch-a-pod-using-service-account-token-projection).
   2. Configure the ID tokens to contain an audience claim with `snowflakecomputing.com`.

      The following is an example of a YAML configuration with the proper audience:

      Copy code

      ```
      kind: Pod
      metadata:
        name: nginx
      spec:
        containers:
        - image: nginx
          name: nginx
          volumeMounts:
          - mountPath: /var/run/secrets/tokens
      name: snowflake-token
        serviceAccountName: build-robot
        volumes:
        - name: snowflake-token
          projected:
      sources:
      - serviceAccountToken:
          path: snowflake-token
          expirationSeconds: 7200
          audience: snowflakecomputing.com
      ```

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- The issuer URL of the OIDC provider that is generating the ID token for the Kubernetes service account. To obtain this issuer URL, see
  the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/aks/use-oidc-issuer#get-the-oidc-issuer-url).
- The namespace and name of the Kubernetes service account. You use this information to construct the subject of the ID token issued
  by the OIDC provider.

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER my_aks_service
     WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://<region>.oic.prod-aks.azure.com/<tenant_id>/<uuid>/'
    SUBJECT = 'system:serviceaccount:<service_account_namespace>:<service_account_name>'
     )
     TYPE = SERVICE;
   ```

   Where `ISSUER` and `SUBJECT` are the values that you obtained before starting these steps.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='OIDC',
     token_file_path='<service_account_token_path>'
   )
   ```

   Where `service_account_token_path` is the one you created in the [Configure AKS](#label-wif-oidc-azure-kubernetes-configure-azure) step.
   Based on the YAML example in that step, the token path would be `/var/run/secrets/tokens/snowflake-token`.
3. Run your Python application. It authenticates to Snowflake using WIF.

### Authenticate using an OpenID Connect (OIDC) issuer from Google Kubernetes Engine (GKE)

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from Google Kubernetes Engine (GKE):

- [Configure GKE](#label-wif-oidc-google-kubernetes-configure-google)
- [Configure Snowflake](#label-wif-oidc-google-kubernetes-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-oidc-google-kubernetes-set-up-a-snowflake-connector-for-python)

#### Configure GKE

1. Configure GKE to issue ID tokens that are compatible with Snowflake.
   1. [Configure your pod deployment YAML to include a projected ServiceAccount token volume](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#launch-a-pod-using-service-account-token-projection).
   2. Configure the ID tokens to contain an audience claim with `snowflakecomputing.com`.

      The following is an example of a YAML configuration with the proper audience:

      Copy code

      ```
      kind: Pod
      metadata:
        name: nginx
      spec:
        containers:
        - image: nginx
          name: nginx
          volumeMounts:
          - mountPath: /var/run/secrets/tokens
      name: snowflake-token
        serviceAccountName: build-robot
        volumes:
        - name: snowflake-token
          projected:
      sources:
      - serviceAccountToken:
          path: snowflake-token
          expirationSeconds: 7200
          audience: snowflakecomputing.com
      ```

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- The Google Cloud project ID, region of the cluster, and cluster name. You use this information to construct the OIDC issuer.
- The namespace and name of the Kubernetes service account. You use this information to construct the subject of the ID token issued by
  the OIDC provider.

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER my_gke_service
     WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://container.googleapis.com/v1/projects/<project_id>/locations/<region>/clusters/<cluster_name>'
    SUBJECT = 'system:serviceaccount:<service_account_namespace>:<service_account_name>'
     )
     TYPE = SERVICE;
   ```

   Where `ISSUER` and `SUBJECT` are the values that you obtained before starting these steps.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='OIDC',
     token_file_path='<service_account_token_path>'
   )
   ```

   Where `service_account_token_path` is the one you created in the [Configure GKE](#label-wif-oidc-google-kubernetes-configure-google) step.
   Based on the YAML example in that step, the token path would be `/var/run/secrets/tokens/snowflake-token`.
3. Run your Python application. It authenticates to Snowflake using WIF.

### Authenticate using SPIFFE/SPIRE

[SPIFFE](https://spiffe.io) (Secure Production Identity Framework for Everyone) is a set of open source standards for
identifying software workloads across platforms and cloud providers. [SPIRE](https://spiffe.io/docs/latest/spire-about/spire-concepts/)
is a production-ready implementation. Workloads that use SPIRE to manage their identities can authenticate to Snowflake through OIDC-based
workload identity federation.

SPIRE issues JWT-SVIDs (JSON Web Token SPIFFE Verifiable Identity Documents) that are compatible with OIDC validation
when the OIDC Discovery Provider is enabled. Snowflake validates these tokens through that endpoint. Snowflake doesn’t
support X.509-SVIDs for WIF authentication.

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from a SPIFFE/SPIRE workload:

- [Configure SPIRE](#label-wif-spiffe-configure-spire)
- [Configure Snowflake](#label-wif-spiffe-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-spiffe-configure-workload)

#### Configure SPIRE

1. Deploy a [SPIRE Server and Agent](https://spiffe.io/docs/latest/deploying/using_spire/) for your workload environment.
2. Enable the [SPIRE OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md). This component exposes a
   publicly accessible HTTPS endpoint that Snowflake uses to retrieve signing keys for token validation. Both the
   `/.well-known/openid-configuration` endpoint and the `jwks_uri` it references must be publicly accessible.
3. [Register your workload](https://spiffe.io/docs/latest/deploying/registering/) in SPIRE with a SPIFFE ID. For example:

   Copy code

   ```
   spire-server entry create \
     -parentID spiffe://<trust_domain>/agent \
     -spiffeID spiffe://<trust_domain>/workload/<workload_name> \
     -selector <attestor_type>:<selector_value>
   ```
4. Configure the workload registration to issue JWT-SVIDs with an audience value that matches the value you configure
   in Snowflake. See [Configure Snowflake](#label-wif-spiffe-configure-snowflake).

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- **Issuer URL**: The HTTPS URL of your SPIRE OIDC Discovery Provider. For example, `https://spire-oidc.example.com`.
- **Subject**: The SPIFFE ID of your workload. For example, `spiffe://trust-domain/workload/my-service`.

You can verify these values by fetching a JWT-SVID and inspecting its claims:

Copy code

```
spire-agent api fetch jwt \
  -audience <audience> \
  -socketPath /var/run/spire/agent.sock \
  -output json
```

Replace `/var/run/spire/agent.sock` with the socket path configured in your SPIRE Agent deployment.

The `iss` claim is the issuer URL and the `sub` claim is the SPIFFE ID.

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER my_spiffe_workload
     WORKLOAD_IDENTITY = (
       TYPE = OIDC
       ISSUER = '<issuer_url>'
       SUBJECT = '<spiffe_id>'
       OIDC_AUDIENCE_LIST = ('<audience>')
     )
     TYPE = SERVICE;
   ```

   Where:

   - `ISSUER` is the HTTPS URL of your SPIRE OIDC Discovery Provider.
   - `SUBJECT` is the SPIFFE ID of your workload (for example, `spiffe://trust-domain/workload/my-service`).
   - `OIDC_AUDIENCE_LIST` is a list of audience values that the JWT-SVID must contain. Set this to a value scoped to your
     Snowflake account, such as your account URL.

   To mark every session from this workload as agent-active, use `TYPE = SERVICE_AGENT` instead of `TYPE = SERVICE`. For the
   characteristics of `SERVICE_AGENT` users, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

Security: Audience restriction

Always specify `OIDC_AUDIENCE_LIST` with a value scoped to your Snowflake account. If you omit this parameter, the audience
defaults to `snowflakecomputing.com`, which is shared across all Snowflake accounts and can allow cross-account token reuse.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. Install the [SPIFFE Python library](https://github.com/HewlettPackard/py-spiffe): `pip install spiffe`
2. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
3. In your Python application code, add the following source code:

   Copy code

   ```
   from spiffe import WorkloadApiClient
   import snowflake.connector

   # Fetch a JWT-SVID from the local SPIRE Agent
   with WorkloadApiClient() as spiffe_client:
       jwt_svid = spiffe_client.fetch_jwt_svid(
           audience={'<audience>'}
       )

   # Authenticate to Snowflake using the JWT-SVID
   conn = snowflake.connector.connect(
       account='<snowflake_account>',
       authenticator='WORKLOAD_IDENTITY',
       workload_identity_provider='OIDC',
       token=jwt_svid.token,
   )
   ```

   Where:

   - `<audience>` matches the value in your Snowflake user’s `OIDC_AUDIENCE_LIST`.
   - `<snowflake_account>` is your Snowflake account identifier.
4. Run your Python application. It authenticates to Snowflake using WIF.

Note

JWT-SVIDs are short-lived (the default is 5 minutes, but this depends on your SPIRE configuration). The SPIFFE library
provides a fresh token each time you call `fetch_jwt_svid`, so call it before each new connection.

### Authenticate using a custom OpenID Connect (OIDC) Provider

Complete the steps in each section listed below to use WIF to authenticate to Snowflake from a custom OIDC Provider:

- [Configure your OIDC Provider](#label-wif-oidc-custom-configure-custom)
- [Configure Snowflake](#label-wif-oidc-custom-configure-snowflake)
- [Configure your workload to use a Snowflake driver](#label-wif-oidc-custom-set-up-a-snowflake-connector-for-python)

#### Configure your OIDC Provider

1. Ensure that your OIDC Provider supports the [OpenID Configuration](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig)
   as specified within the Discovery specification. Both the configuration and the configuration’s `jwks_uri` endpoint must be publicly accessible.
2. Configure your OpenID Provider to issue ID tokens with an audience claim that is set to `snowflakecomputing.com` or a non-empty custom list.
   If you define a non-empty custom list, you need to specify it when you create a service user in Snowflake.

#### Configure Snowflake

To configure Snowflake, create a Snowflake service user (that is, a user of type `SERVICE`) that uses WIF
to authenticate with Snowflake.

Before you begin

To successfully configure Snowflake, you need the following information:

- The issuer URL of your OIDC Provider.
- The subject claim associated with your workload.

You can obtain both of these values by parsing out the `iss` and `sub` claims from an issued ID token for your workload. For example,
if you have access to a Unix-like environment with `jq`, `cat`, and `echo`, you can save your ID token to a file and run the
following commands.

Copy code

```
ID_TOKEN_PATH=<id_token_path>

JWS_PAYLOAD=$(cat $ID_TOKEN_PATH | jq -R 'split(".") | .[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson')
echo "ISSUER = '$(echo $JWS_PAYLOAD | jq -r .iss)'"
echo "SUBJECT = '$(echo $JWS_PAYLOAD | jq -r .sub)'"
```

To learn how to obtain an ID token, see the documentation for your OIDC Provider.

**To create a service user for your workload:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To open the list of worksheets, in the navigation menu, select **Projects** » **Worksheets**.
3. To open a new SQL worksheet, select **+**.
4. To create a service user that uses WIF to authenticate with Snowflake, run a
   [CREATE USER](/sql-reference/sql/create-user) statement in the worksheet:

   Copy code

   ```
   CREATE USER my_custom_service
     WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = '<issuer>'
    SUBJECT = '<subject>'
    OIDC_AUDIENCE_LIST = ('<custom_audience>')
     )
     TYPE = SERVICE;
   ```

   Where:

   - `ISSUER` and `SUBJECT` are the values that you obtained before starting these steps.
   - `OIDC_AUDIENCE_LIST` is a non-empty superset of the ID token’s audience claim set in [Configure your OIDC Provider](#label-wif-oidc-custom-configure-custom).
     You don’t have to specify `OIDC_AUDIENCE_LIST` if the ID token’s audience claim is `snowflakecomputing.com`.

#### Configure your workload to use a Snowflake driver

Note

You can configure your workload to use any Snowflake driver that supports WIF. For the complete list, see
[Supported Snowflake drivers](#label-wif-supported-drivers).

If your workload needs a Python driver, complete the following steps:

1. [Install the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-install).
2. In your Python application code, add the following source code:

   Copy code

   ```
   conn = snowflake.connector.connect(
     account='<snowflake_account>',
     authenticator='WORKLOAD_IDENTITY',
     workload_identity_provider='OIDC',
     token='<id_token>'
   )
   ```

   Where `id_token` is an unexpired ID token received from your OIDC Provider for your workload. To learn how to obtain
   this token, see the documentation for your OIDC Provider.
3. Run your Python application. It authenticates to Snowflake using WIF.

## View service user settings

Run the [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods) command to view the values of the WORKLOAD\_IDENTITY
parameter for the service user. For example, to view the WIF settings that the service user `my_custom_service`
uses to authenticate to Snowflake, run the following command:

Copy code

```
SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR USER my_custom_service;
```

## Limitations and considerations

- Azure workloads can’t be located in Azure sovereign clouds, such as Azure China and Azure US Gov. This limitation isn’t related to the
  Snowflake region of your account.
- The SUBJECT property in WORKLOAD\_IDENTITY can’t exceed 255 characters.
- The ISSUER property in WORKLOAD\_IDENTITY can’t exceed 2048 characters.
- ID tokens must include the `iat` (issued at) claim. Snowflake rejects tokens that omit this claim.
- Snowflake supports the following JWT signature algorithms: RS256, RS384, RS512, ES256, ES384, and ES512. Tokens signed with other
  algorithms (such as PS256, PS384, or PS512) are rejected.
- Snowflake caches the issuer’s signing keys for up to 60 minutes. If your identity provider rotates signing keys, ensure that old keys
  remain published for at least 60 minutes after new keys are introduced to avoid transient authentication failures.
