# Snowflake CLI Azure DevOps Extension

Preview Feature

This feature is in public preview. Inputs and behavior may change between releases.

The Snowflake CLI Azure DevOps Extension ([snowflakedb/snowflake-ado-extension](https://github.com/snowflakedb/snowflake-ado-extension)) installs and configures Snowflake CLI in an Azure Pipelines pipeline. Use it to automate Snowflake deployments (DCM projects, Snowpark applications, Snowflake Native Apps, and SQL scripts) from your Azure DevOps project.

## How it works

The extension publishes a single pipeline task, `ConfigureSnowflakeCLI@1`. Marketplace versions since Public Preview ship Major `1` only — `ConfigureSnowflakeCLI@0` is no longer published. The task performs these steps on the agent:

1. Installs Snowflake CLI in an isolated environment using `pipx` (`pipx install snowflake-cli` or `pipx install snowflake-cli==<version>`).
2. Copies the `snow` executable to a known location and prepends it to the pipeline’s `PATH`.
3. Copies `config.toml` from the repository to `~/.snowflake/config.toml` (`0600` on Linux/macOS). Skipped if the file is absent.
4. When workload identity is enabled, requests an OIDC token from Azure DevOps through the specified service connection and sets Snowflake workload identity pipeline variables. `SNOWFLAKE_TOKEN` is marked as a secret, so later `script:` steps must map it with `env: SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)`.

After the task completes, the `snow` command is available on `PATH` for every subsequent step in the job. On Windows agents, both `snow` and `snow.exe` are available.

## Quick usage example

The following pipeline authenticates with Snowflake using workload identity federation (WIF) through an Azure Resource Manager service connection and runs a connection test:

Copy code

```
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'
      useWorkloadIdentity: true
      connectedServiceName: 'snowflake-wif-connection'
    displayName: Configure Snowflake CLI

  - script: |
      snow --version
      snow connection test -x
    displayName: Verify Snowflake connection
    env:
      SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
      SNOWFLAKE_USER: $(SNOWFLAKE_USER)
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

## Inputs

The task accepts the following inputs, specified under `inputs:` in your pipeline YAML:

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `cliVersion` | Yes | `latest` | Snowflake CLI version to install, for example `3.16.0`, or `latest` for the newest released version. |
| `configFilePath` | No | `./config.toml` | Path to your `config.toml`, relative to the repository root. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| `useWorkloadIdentity` | No | `false` | When `true`, configures OIDC authentication using an Azure service connection. |
| `connectedServiceName` | Conditional | (none) | Name of the Azure Resource Manager service connection. Required and shown in the pipeline editor only when `useWorkloadIdentity` is `true`. |

Expand

Show lessSee more

## Authentication methods

The task supports three ways of authenticating with Snowflake. Snowflake recommends workload identity federation because it avoids storing long-lived secrets in Azure DevOps.

| Method | Security | Notes |
| --- | --- | --- |
| [Workload identity federation (WIF) with OIDC](#label-ado-extension-wif) (recommended) | Secretless, short-lived tokens | Requires an Azure Entra ID App Registration with a federated credential and an Azure Resource Manager service connection. |
| [Key pair authentication](#label-ado-extension-key-pair) | Private key stored in pipeline variables/secrets | Works with any Snowflake CLI version. Combined with `config.toml` or environment variable overrides. |
| [Password authentication](#label-ado-extension-password) | Password stored in pipeline variables/secrets | Legacy option, not recommended for production pipelines. |

Expand

Show lessSee more

### Workload identity federation (WIF) with OIDC

With WIF, Azure DevOps obtains a short-lived OIDC token through the configured Azure Resource Manager service connection, and Snowflake validates the token directly. No private key or password is stored in Azure DevOps.

#### Create the service user

Create a Snowflake service user that trusts Azure DevOps OIDC:

Copy code

```
CREATE USER ado_cicd_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://vstoken.dev.azure.com/<azure-ad-tenant-id>'
    SUBJECT = 'sc://<ado-org>/<ado-project>/<service-connection-name>'
    OIDC_AUDIENCE_LIST = ('api://AzureADTokenExchange')
  );
```

The `ISSUER` incorporates your Azure AD tenant ID, and the `SUBJECT` uses the Azure DevOps service connection identifier format (`sc://<org>/<project>/<connection>`). The `OIDC_AUDIENCE_LIST` must be `api://AzureADTokenExchange`.

#### Configure the task

Create an Azure Resource Manager service connection with a federated credential that trusts Snowflake’s audience (see the Azure documentation on [workload identity federation with Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/connect-to-azure)), then reference the service connection from the task:

Copy code

```
steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'
      useWorkloadIdentity: true
      connectedServiceName: 'snowflake-wif-connection'

  - script: |
      snow connection test -x
      snow dcm deploy --target PROD -x
    env:
      SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
      SNOWFLAKE_USER: $(SNOWFLAKE_USER)
      SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

When `useWorkloadIdentity: true` is set, the task sets these pipeline variables:

- `SNOWFLAKE_AUTHENTICATOR=WORKLOAD_IDENTITY` (available to later steps automatically)
- `SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER=OIDC` (available to later steps automatically)
- `SNOWFLAKE_TOKEN` (the OIDC token, marked as a pipeline secret)

Azure Pipelines does not inject secret variables into later `script:` steps. Map the token on every later step that calls `snow`:

Copy code

```
env:
  SNOWFLAKE_TOKEN: $(SNOWFLAKE_TOKEN)
```

If you keep `-x` (`--temporary-connection`), also map `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_USER`. Prefer a committed `config.toml` plus the token map when you do not want `-x`.

For broader context, see [Workload identity federation](/user-guide/workload-identity-federation).

### Key pair authentication

Store your Snowflake private key as an Azure DevOps secret variable and pass it through the environment. You can use a temporary connection (no `config.toml` required) or a named connection defined in `config.toml`.

Copy code

```
steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: '3.16.0'

  - script: |
      snow connection test -x
      snow dcm deploy --target PROD -x
    env:
      SNOWFLAKE_AUTHENTICATOR: SNOWFLAKE_JWT
      SNOWFLAKE_USER: $(SNOWFLAKE_USER)
      SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
      SNOWFLAKE_PRIVATE_KEY_RAW: $(SNOWFLAKE_PRIVATE_KEY_RAW)
      PRIVATE_KEY_PASSPHRASE: $(PRIVATE_KEY_PASSPHRASE)
```

For connection-file-based authentication, commit a `config.toml` with an empty connection block and supply the credentials through `SNOWFLAKE_CONNECTIONS_<NAME>_*` environment variables. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

### Password authentication

Password authentication is supported for legacy workflows but is not recommended for production CI/CD. Unset `SNOWFLAKE_AUTHENTICATOR` and pass `SNOWFLAKE_PASSWORD`:

Copy code

```
steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'

  - script: snow connection test -x
    env:
      SNOWFLAKE_USER: $(SNOWFLAKE_USER)
      SNOWFLAKE_ACCOUNT: $(SNOWFLAKE_ACCOUNT)
      SNOWFLAKE_PASSWORD: $(SNOWFLAKE_PASSWORD)
```

Note

When using a password and MFA, Snowflake recommends enabling [MFA caching](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-mfa-caching).

## Platform support

The task runs on Linux, macOS, and Windows Azure Pipelines agents. Note the following platform-specific behavior:

- **Linux and macOS**: the copied `config.toml` is set to `0600` permissions. The `snow` executable is available on `PATH`.
- **Windows**: file permissions on `config.toml` are not modified. Both `snow` and `snow.exe` are available on `PATH`.

Task version 1.1.0 and later run on the Node 20 agent runtime (Node 24 is also registered). Marketplace 1.0.0 still used Node 16.

## Using a pre-installed Snowflake CLI

If Snowflake CLI is already installed on a self-hosted agent image (for example, baked into a custom agent pool), set the `DISABLE_SNOW_INSTALLATION_WITH_PIPX` environment variable on the task to skip the pipx installation step:

Copy code

```
steps:
  - task: ConfigureSnowflakeCLI@1
    inputs:
      cliVersion: 'latest'
      useWorkloadIdentity: true
      connectedServiceName: 'snowflake-wif-connection'
    env:
      DISABLE_SNOW_INSTALLATION_WITH_PIPX: 'true'
```

The task still copies your `config.toml` and configures authentication. You are responsible for ensuring `snow` is on `PATH` and that the version matches the one declared in `cliVersion`.

## Related resources

- [snowflake-ado-extension repository](https://github.com/snowflakedb/snowflake-ado-extension). Extension source and release notes.
- [Azure DevOps Marketplace listing](https://marketplace.visualstudio.com/items?itemName=snowflake.build-release-task).
- [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd). Overview of all Snowflake-supported CI/CD integrations.
- [DevOps with Snowflake](/developer-guide/builders/devops-with-snowflake). DevOps with Snowflake concepts and workflow guidance.
- [Workload identity federation](/user-guide/workload-identity-federation). Snowflake workload identity federation reference.
