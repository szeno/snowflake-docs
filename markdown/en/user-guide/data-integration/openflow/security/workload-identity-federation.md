# Use Workload Identity Federation with Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

[Workload Identity Federation](/user-guide/workload-identity-federation-outbound) (WIF) lets an Openflow runtime
authenticate to external cloud services on Amazon Web Services (AWS), Microsoft Azure, and Google Cloud without storing
long-lived credentials such as access keys, client secrets, or service account keys. Snowflake acts as the
[OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html) (OIDC) provider: the runtime obtains a
short-lived, signed token from Snowflake and exchanges it for temporary, scoped credentials in your cloud account.

This is especially valuable when Openflow runs on Snowpark Container Services (SPCS), where the compute runs in
Snowflake’s cloud account rather than in your own. Traditional cloud authentication mechanisms that rely on attaching
an identity to the compute (for example, AWS instance profiles or IAM roles for service accounts) aren’t available,
which would otherwise leave static credentials as the only option. Because Snowflake itself issues the identity token,
the runtime can federate into your cloud account regardless of where the compute runs, so you never have to store a
static secret.

Note

This topic describes how to configure Openflow to consume Workload Identity Federation. For the Snowflake concepts
behind the feature — the secret object, the trust relationship, and token issuance — see
[Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound).

## How it works

1. You create a Snowflake secret of type `WORKLOAD_IDENTITY_FEDERATION`. Snowflake becomes an OIDC provider with a
   unique issuer URL, and the secret becomes an OIDC client with a unique subject identifier.
2. You establish a trust relationship on the cloud provider side using the issuer URL and subject identifier.
3. In Openflow, the `SnowflakeWorkloadIdentityTokenProvider` controller service obtains a signed token from Snowflake
   for a configured audience.
4. A cloud-specific credentials controller service exchanges that token for temporary cloud credentials, which the
   Openflow processors and parameter providers then use to access cloud resources.

## Prerequisites

- A Snowflake Deployment (SPCS) of Openflow with a runtime. See [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs).
- Privileges to create secrets, network rules, and external access integrations in Snowflake.
- Administrative access to the target cloud provider to configure the trust relationship (AWS IAM, Microsoft Entra ID,
  or Google Cloud IAM).

## Create the Snowflake secret

Create a secret of type `WORKLOAD_IDENTITY_FEDERATION`. Secrets are schema-level objects, so the secret is created in a
specific database and schema.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS wif_demo;
CREATE SCHEMA IF NOT EXISTS wif_demo.secrets_schema;

CREATE SECRET wif_demo.secrets_schema.my_demo
    TYPE = WORKLOAD_IDENTITY_FEDERATION;
```

For more information, see [CREATE SECRET](/sql-reference/sql/create-secret).

Describe the secret to retrieve the two values required to configure the trust relationship on the cloud provider side:

Copy code

```
DESC SECRET wif_demo.secrets_schema.my_demo;
```

Record the following values from the output:

| Column | Description |
| --- | --- |
| `workload_identity_federation_issuer` | Issuer URL of Snowflake as the OIDC provider. Compared to the `iss` claim of the token. |
| `workload_identity_federation_subject` | Identifier of the workload as the OIDC client. Compared to the `sub` claim of the token. |

Expand

Show lessSee more

Note

The issuer is unique to a Snowflake account and is the same for every secret created in that account. The subject is
unique to each secret.

Grant `USAGE` on the database, schema, and secret to the execute-as role assigned to the Openflow runtime:

Copy code

```
GRANT USAGE ON DATABASE wif_demo TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
GRANT USAGE ON SCHEMA wif_demo.secrets_schema TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
GRANT USAGE ON SECRET wif_demo.secrets_schema.my_demo TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

## Set up the common Openflow controller services

The following controller services are required for all cloud providers.

### Snowflake Connection Service

If you don’t already have one (Snowflake-provided connectors include one by default), create an instance of the
[SnowflakeConnectionService](/user-guide/data-integration/openflow/controllers/snowflakeconnectionservice) controller
service and set **Authentication Strategy** to `Snowflake Managed Token`. Enable the controller service.

Note

From the configuration view of a controller service, you can select **Verify** to confirm the configuration is correct
before you enable it.

### Snowflake Workload Identity Token Provider

Create an instance of the `SnowflakeWorkloadIdentityTokenProvider` controller service with the following configuration:

- **Connection Pooling Service**: reference the Snowflake Connection Service.
- **Snowflake Secret Name**: the fully qualified name of the secret, for example `wif_demo.secrets_schema.my_demo`.
- **Audience**: the audience value configured for the identity provider on the cloud provider side (see the per-cloud
  sections below).

Enable the controller service.

## AWS

### Create the IAM identity provider

Note

Create the IAM identity provider only once per Snowflake account.

1. In the AWS console, go to **IAM** » **Identity providers** and select **Add provider**.
2. For **Provider type**, select **OpenID Connect**.
3. For **Provider URL**, enter the `workload_identity_federation_issuer` value.
4. For **Audience**, enter a value of your choice, for example `snowflake`. Use this same value as the **Audience** on
   the Snowflake Workload Identity Token Provider controller service.
5. Select **Add provider**.

### Create the IAM role and policy

1. In the AWS console, go to **IAM** » **Roles** and select **Create role**.
2. For **Trusted entity type**, select **Web identity**.
3. For **Identity provider**, select the identity provider you created, and select the audience you defined.
4. Add a condition where the key ends with `:sub`, the condition is `StringEquals`, and the value is the
   `workload_identity_federation_subject` value. This creates a one-to-one relationship between the Snowflake secret and
   the IAM role.
5. Attach the policies required for the resources the Openflow runtime needs to access, name the role, and create it.

Save the Amazon Resource Name (ARN) of the role for the Openflow configuration.

Note

You can create a one-to-many mapping between a single secret and multiple IAM roles. For example, to give read-only
access to one Snowflake role and read-write access to another, edit the role’s trust policy to add a condition on the
`sf_rnm` claim, which equals the name of the execute-as role assigned to the Openflow runtime:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/identity.snowflake.com/oauth2/<PATH>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "identity.snowflake.com/oauth2/<PATH>:sub": "<SUBJECT>",
          "identity.snowflake.com/oauth2/<PATH>:aud": "snowflake",
          "identity.snowflake.com/oauth2/<PATH>:sf_rnm": "AWS_RO"
        }
      }
    }
  ]
}
```

### Configure the external access integration

In addition to a network rule for the resource itself, add a network rule that allows access to the AWS Security Token
Service (STS) endpoint used to exchange the token. The following example allows access to STS and Amazon SQS:

Copy code

```
USE ROLE SECURITYADMIN;

USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE NETWORK RULE openflow_sqs_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('sts.eu-central-1.amazonaws.com:443', 'sqs.eu-central-1.amazonaws.com:443');

CREATE EXTERNAL ACCESS INTEGRATION openflow_sqs_eai
    ALLOWED_NETWORK_RULES = (openflow_sqs_network_rule)
    ENABLED = TRUE;

GRANT USAGE ON INTEGRATION openflow_sqs_eai TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

For Amazon S3 (for example, the `ListS3` or `FetchS3Object` processors), allow STS plus both the regional and global
S3 endpoints. The AWS SDK might connect using either the regional or the global S3 endpoint. Snowflake network
rules require an exact hostname match, so allow both forms, plus the wildcard variants used by virtual-hosted bucket URLs.
In the following example, replace `us-east-1` with your bucket region in each of the regional entries:

Copy code

```
USE ROLE SECURITYADMIN;
USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE NETWORK RULE openflow_s3_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = (
      'sts.us-east-1.amazonaws.com:443',
      's3.us-east-1.amazonaws.com:443',
      's3.amazonaws.com:443',
      '*.s3.us-east-1.amazonaws.com:443',
      '*.s3.amazonaws.com:443'
    );

CREATE EXTERNAL ACCESS INTEGRATION openflow_s3_eai
    ALLOWED_NETWORK_RULES = (openflow_s3_network_rule)
    ENABLED = TRUE;

GRANT USAGE ON INTEGRATION openflow_s3_eai TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

After you create the external access integration, associate it with your runtime. See
[Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

### Configure the AWS Credentials Provider Service

For most components to interact with AWS services, configure an
[AWSCredentialsProviderControllerService](/user-guide/data-integration/openflow/controllers/awscredentialsprovidercontrollerservice)
controller service:

- **Assume Role ARN**: the ARN of the IAM role you created.
- **Assume Role Session Name**: any descriptive string that identifies the session.
- **Assume Role STS Region**: the region for the STS endpoint (the same region as the resources being accessed).
- **OAuth2 Access Token Provider**: reference the Snowflake Workload Identity Token Provider controller service.

Enable the controller service.

### Configure AWS components

Configure the AWS components (for example, `ListS3` or `ConsumeKinesis`) to reference the credentials controller
service you created.

This also applies to the AWS Secrets Manager parameter provider. However, parameter providers aren’t flow-level
components: create the controller services at the flow controller level (**Controller Settings** »
**Management controller services**) so that the parameter provider can reference them.

### AWS MSK with IAM authentication

In the `ConsumeKafka` processor, set the **Kafka Connection Service** property to reference an
[AmazonMSKConnectionService](/user-guide/data-integration/openflow/controllers/amazonmskconnectionservice) controller
service. In that controller service:

- Set **SASL Mechanism** to `AWS_MSK_IAM`.
- Set **AWS Role Source** to `Web Identity Provider`, which reveals the following properties:
  - **AWS Assume Role ARN**: the ARN of the IAM role you created.
  - **AWS Assume Role Session Name**: any descriptive string that identifies the session.
  - **AWS Web Identity Token Provider**: reference the Snowflake Workload Identity Token Provider controller service.
  - **AWS Web Identity STS Region**: the region for the STS endpoint (the same region as the MSK instance).

### AWS RDS for PostgreSQL with IAM authentication

1. Create an `AWSCredentialsProviderControllerService` as described in
   [Configure the AWS Credentials Provider Service](#label-openflow-wif-aws-creds), using the STS region of the RDS instance.
2. Create an `AwsRdsIamDatabasePasswordProvider` controller service:
   - **AWS Credentials Provider Service**: reference the credentials controller service from the previous step.
   - **Region**: the same region as the RDS instance.
3. In the `DBCPConnectionPool` controller service, set **Password Source** to `Password Provider`, then set
   **Database Password Provider** to reference the `AwsRdsIamDatabasePasswordProvider`.

## Azure

### Register an application in Microsoft Entra ID

1. In Microsoft Entra ID, register a new application and give it a name.
2. Record the application’s **Tenant ID** and **Client ID**.
3. Go to **Certificates & secrets** » **Federated credentials** and select **Add credential**.
4. For the scenario, select **Other issuer**.
5. For **Issuer**, enter the `workload_identity_federation_issuer` value. For **Value** (the subject identifier), enter
   the `workload_identity_federation_subject` value. Give the credential a name, and note the **Audience** — you set this
   same value as the **Audience** on the Snowflake Workload Identity Token Provider controller service.

### Configure the external access integration

In addition to a network rule for the resource itself, add a network rule that allows access to the Microsoft login
endpoint (`login.microsoftonline.com`) used to exchange the token. The following example also allows access to an Azure
Key Vault:

Copy code

```
USE ROLE SECURITYADMIN;

USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE NETWORK RULE openflow_azure_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('login.microsoftonline.com:443', 'myvault.vault.azure.net:443');

CREATE EXTERNAL ACCESS INTEGRATION openflow_azure_eai
    ALLOWED_NETWORK_RULES = (openflow_azure_network_rule)
    ENABLED = TRUE;

GRANT USAGE ON INTEGRATION openflow_azure_eai TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

Note

The endpoint required for the token exchange is `login.microsoftonline.com`. Add other endpoints based on the service
you access; `myvault.vault.azure.net` is only an example for the Key Vault service.

After you create the external access integration, associate it with your runtime. See
[Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

### Configure the Azure Identity Federation Token Provider

In Openflow, go to **Controller Settings** » **Management controller services** (where you added the Snowflake
Connection Service and the Snowflake Workload Identity Token Provider) and add an instance of
`StandardAzureIdentityFederationTokenProvider`:

- Reference the Snowflake Workload Identity Token Provider controller service.
- Set the **Tenant ID** and **Client ID** of your registered Entra application.

Select **Verify** to confirm that tokens can be exchanged before you continue.

### Configure the Azure Credentials Controller Service

Add a
[StandardAzureCredentialsControllerService](/user-guide/data-integration/openflow/controllers/standardazurecredentialscontrollerservice)
controller service, select `Identity Federation` for the strategy, and reference the Azure Identity Federation Token
Provider controller service. Enable all of the controller services.

### Access secrets with the Azure Key Vault parameter provider

1. Create a Key Vault in Azure and add the secrets you want to use as parameters in Openflow.
2. In the Key Vault, go to **Access control (IAM)** and add a role assignment. Assign the **Key Vault Secrets User**
   role to your Entra application (a service principal), then review and approve the assignment.
3. In Openflow, go to **Parameter Providers** and add an `AzureKeyVaultSecretsParameterProvider`:
   - **Credentials Service**: reference the Azure Credentials Controller Service you created.
   - **Vault URI**: the URI shown on the overview page of your Key Vault.
4. Select **Verify** to confirm access to the secrets.

## GCP

### Create the workload identity pool and provider

Note

The workload identity pool and its OIDC provider can be created once and reused across secrets for the Snowflake
account.

In Google Cloud, create a workload identity pool and add an OpenID Connect (OIDC) provider to that pool. Configure the
provider with the following values:

- **Issuer (URL)**: the `workload_identity_federation_issuer` value.
- **Allowed audiences**: an audience value of your choice. This value must be identical to the **Audience** on the
  Snowflake Workload Identity Token Provider controller service and the **Audience** on the GCP Credentials Controller
  Service. A common choice is the provider resource name itself.
- **Attribute mapping**: map `google.subject` to `assertion.sub`. This maps the subject claim of the Snowflake token to
  the principal identity used in IAM bindings.

For example, using the gcloud CLI:

Copy code

```
gcloud iam workload-identity-pools create openflow-pool \
    --location="global" \
    --display-name="Openflow WIF pool"

gcloud iam workload-identity-pools providers create-oidc snowflake-provider \
    --location="global" \
    --workload-identity-pool="openflow-pool" \
    --issuer-uri="<WORKLOAD_IDENTITY_FEDERATION_ISSUER>" \
    --attribute-mapping="google.subject=assertion.sub" \
    --allowed-audiences="//iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/openflow-pool/providers/snowflake-provider"
```

Record the provider resource name (used as the audience above), because it’s required in the Openflow configuration:

```
//iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/openflow-pool/providers/snowflake-provider
```

### Grant access to the workload identity principal

Note

Service account impersonation isn’t currently supported. Grant roles directly to the workload identity principal.

Grant the required IAM roles directly to the principal that corresponds to the Snowflake secret. The principal is
derived from the `workload_identity_federation_subject` value:

```
principal://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/openflow-pool/subject/<SUBJECT>
```

For example, to grant read-only access to a Cloud Storage bucket:

Copy code

```
gcloud storage buckets add-iam-policy-binding gs://<BUCKET_NAME> \
    --role="roles/storage.objectViewer" \
    --member="principal://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/openflow-pool/subject/<SUBJECT>"
```

Adapt the role and resource to what the Openflow runtime needs to access.

### Configure the external access integration

In addition to a network rule for the resource itself, add a network rule that allows access to the Google Security
Token Service (STS) endpoint (`sts.googleapis.com`) used to exchange the token. The following example also allows access
to Cloud Storage:

Copy code

```
USE ROLE SECURITYADMIN;

USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE NETWORK RULE openflow_gcs_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('sts.googleapis.com:443', 'storage.googleapis.com:443');

CREATE EXTERNAL ACCESS INTEGRATION openflow_gcs_eai
    ALLOWED_NETWORK_RULES = (openflow_gcs_network_rule)
    ENABLED = TRUE;

GRANT USAGE ON INTEGRATION openflow_gcs_eai TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

Note

`iamcredentials.googleapis.com` isn’t required, because service account impersonation isn’t used.

After you create the external access integration, associate it with your runtime. See
[Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

### Configure the GCP Credentials Controller Service

Unlike AWS and Azure, GCP uses a single credentials controller service that consumes the Snowflake token directly
through its Workload Identity Federation strategy. Add a
[GCPCredentialsControllerService](/user-guide/data-integration/openflow/controllers/gcpcredentialscontrollerservice)
controller service:

- **Authentication Strategy**: `Workload Identity Federation`.
- **Audience**: the provider resource name. It must match the allowed audiences configured on the GCP OIDC provider and
  the **Audience** on the Snowflake Workload Identity Token Provider, for example
  `//iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/openflow-pool/providers/snowflake-provider`.
- **Subject Token Provider**: reference the Snowflake Workload Identity Token Provider controller service.
- **Subject Token Type**: leave the default (`urn:ietf:params:oauth:token-type:jwt`).
- **Scope**: leave the default (`https://www.googleapis.com/auth/cloud-platform`) unless a narrower scope is required.
- **STS Token Endpoint**: leave the default (`https://sts.googleapis.com/v1/token`).

Enable the controller service. Select **Verify** to confirm that tokens can be exchanged.

### Configure GCP components

Configure the GCP components (for example, the Cloud Storage or BigQuery processors) to reference the GCP Credentials
Controller Service you created.

As with the other cloud providers, if you use a parameter provider that requires GCP credentials (parameter providers
aren’t flow-level components), create the GCP Credentials Controller Service and the Snowflake controller services it
depends on at the flow controller level (**Controller Settings** » **Management controller services**), so that the
parameter provider can reference them.

## Next steps

- [Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
- [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors)
