# Snowflake CLI GitHub Action

The Snowflake CLI GitHub Action ([snowflakedb/snowflake-actions](https://github.com/snowflakedb/snowflake-actions)) installs and configures Snowflake CLI in a GitHub Actions workflow. Use it to automate Snowflake deployments (DCM projects, Snowpark applications, Snowflake Native Apps, and SQL scripts) from your GitHub repository.

## How it works

The action performs these steps on the runner:

1. Installs Python 3.11 and the `uv` package manager using [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv).
2. Installs Snowflake CLI in an isolated environment (`uv tool install snowflake-cli`).
3. Copies `config.toml` from the repository to `~/.snowflake/config.toml` (`0600` on Linux/macOS). Skipped if the file is absent.
4. When OIDC authentication is enabled, obtains a GitHub-issued OIDC token and sets the Snowflake workload identity environment variables for subsequent steps.

After the action completes, the `snow` command is available on `PATH` for every subsequent step in the job.

## Quick usage example

The following workflow authenticates with Snowflake using OIDC and runs a connection test:

Copy code

```
name: Deploy to Snowflake
on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false

      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.16"

      - name: Deploy
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
        run: |
          snow connection test -x
          snow dcm deploy --target PROD -x
```

For other authentication methods, see [Authentication methods](#label-github-action-authentication).

## Version pinning

The action supports three pin styles:

- **Commit SHA** (`@a1b2c3d...`): pins to a specific commit.
- **Patch version tag** (`@v3.0.0`): pins to a specific release.
- **Floating major tag** (`@v3`): follows the latest release in that major version.

Copy code

```
# Pinned commit SHA.
- uses: snowflakedb/snowflake-actions@a1b2c3d4e5f67890abcdef1234567890abcdef12

# Patch version tag.
- uses: snowflakedb/snowflake-actions@v3.0.0

# Floating major tag.
- uses: snowflakedb/snowflake-actions@v3
```

## Inputs

The action accepts the following inputs, specified under `with:` in your workflow YAML:

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `cli-version` | No | (latest) | Snowflake CLI version to install, for example `3.16.0` or `3.16`. When omitted, the latest released version is installed. |
| `custom-github-ref` | No | (none) | GitHub branch, tag, or commit to install Snowflake CLI from. Use this to test unreleased features or a fork. Mutually exclusive with `cli-version`. |
| `default-config-file-path` | No | `./config.toml` | Path to your `config.toml`, relative to the repository root. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| `use-oidc` | No | `false` | When `true`, configures OIDC authentication by obtaining a GitHub OIDC token and setting the Snowflake workload identity environment variables. |
| `oidc-token-name` | No | `SNOWFLAKE_TOKEN` | Name of the environment variable the OIDC token is exported as. Set this to `SNOWFLAKE_CONNECTIONS_<NAME>_TOKEN` when you use a named connection, where `<NAME>` is the uppercased connection name from your `config.toml` (for example, for `[connections.myconnection]`, set `SNOWFLAKE_CONNECTIONS_MYCONNECTION_TOKEN`). The variable name is uppercased internally before being exported. |

Expand

Show lessSee more

Note

Specify only one of `cli-version` or `custom-github-ref`; using both at the same time results in an error.

## Authentication methods

The action supports three ways of authenticating with Snowflake. Snowflake recommends OIDC because it avoids storing long-lived secrets in GitHub.

| Method | Security | Secrets required | Snowflake CLI version |
| --- | --- | --- | --- |
| [Workload identity federation (WIF) with OIDC](#label-github-action-oidc) (recommended) | Secretless, short-lived tokens | Snowflake account only | 3.11 or later |
| [Key pair authentication](#label-github-action-key-pair) | Private key stored in GitHub Secrets | Private key, account, user | Any |
| [Password authentication](#label-github-action-password) | Password stored in GitHub Secrets | Password, account, user | Any |

Expand

Show lessSee more

### Workload identity federation (WIF) with OIDC

Note

OIDC authentication requires Snowflake CLI version 3.11.0 or later.

With OIDC, GitHub issues a short-lived OpenID Connect token that Snowflake validates directly. No private key or password is stored in GitHub.

#### Create the service user

Create a Snowflake service user that trusts GitHub’s OIDC provider:

Copy code

```
CREATE USER <username>
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://token.actions.githubusercontent.com'
    SUBJECT = '<your_subject>'
  );
```

The `SUBJECT` must match the claim GitHub emits for the workflow. Use one of the following formats:

| Subject format | Matches | Workflow requirement |
| --- | --- | --- |
| `repo:<owner>/<repo>:ref:refs/heads/<branch>` | Push to the specified branch | `on: push`, without `environment:` on the job |
| `repo:<owner>/<repo>:pull_request` | Any pull request event | `on: pull_request`, without `environment:` on the job |
| `repo:<owner>/<repo>:environment:<name>` | Job targets a named GitHub environment | Job sets `environment: <name>` (the environment must exist in repository settings) |

Expand

Show lessSee more

When a job sets `environment:`, GitHub uses the environment form regardless of the trigger.

To customize the subject to include a broader claim such as `repository_owner`, see the GitHub [OpenID Connect reference](https://docs.github.com/en/actions/reference/security/oidc).

#### Configure the action

Grant `id-token: write` permission to the job and set `use-oidc: true` on the action:

Copy code

```
name: Snowflake OIDC
on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  oidc-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.16"
      - name: Test connection
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
        run: snow connection test -x
```

When `use-oidc: true` is set, the action exports the following environment variables for subsequent steps:

- `SNOWFLAKE_AUTHENTICATOR=WORKLOAD_IDENTITY`
- `SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER=OIDC`
- `SNOWFLAKE_AUDIENCE=snowflakecomputing.com`
- `SNOWFLAKE_TOKEN=<token>` (or the variable named by `oidc-token-name`)

For broader context, see [Workload identity federation](/user-guide/workload-identity-federation).

### Key pair authentication

Store your Snowflake private key as a GitHub secret and pass it through the environment. You can use a temporary connection (no `config.toml` required) or a named connection defined in `config.toml`.

**Temporary connection:**

Copy code

```
- uses: snowflakedb/snowflake-actions@v3
  with:
    cli-version: "3.16.0"
- name: Deploy
  env:
    SNOWFLAKE_AUTHENTICATOR: SNOWFLAKE_JWT
    SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
    SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
    SNOWFLAKE_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
    PRIVATE_KEY_PASSPHRASE: ${{ secrets.PRIVATE_KEY_PASSPHRASE }}
  run: |
    snow connection test -x
    snow dcm deploy --target PROD -x
```

**Named connection:** commit a `config.toml` with an empty connection block and override the fields through environment variables:

Copy code

```
default_connection_name = "myconnection"

[connections.myconnection]
```

Copy code

```
- uses: actions/checkout@v4
  with:
    persist-credentials: false
- uses: snowflakedb/snowflake-actions@v3
  with:
    default-config-file-path: "config.toml"
- name: Deploy
  env:
    SNOWFLAKE_CONNECTIONS_MYCONNECTION_AUTHENTICATOR: SNOWFLAKE_JWT
    SNOWFLAKE_CONNECTIONS_MYCONNECTION_USER: ${{ secrets.SNOWFLAKE_USER }}
    SNOWFLAKE_CONNECTIONS_MYCONNECTION_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
    SNOWFLAKE_CONNECTIONS_MYCONNECTION_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
    PRIVATE_KEY_PASSPHRASE: ${{ secrets.PRIVATE_KEY_PASSPHRASE }}
  run: snow connection test
```

For more information about connections, see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

### Password authentication

Password authentication is supported for legacy workflows but is not recommended for production CI/CD. To use it, omit `SNOWFLAKE_AUTHENTICATOR` (the CLI defaults to password authentication) and pass `SNOWFLAKE_PASSWORD`:

Copy code

```
- uses: snowflakedb/snowflake-actions@v3
- name: Deploy
  env:
    SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
    SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
    SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
  run: snow connection test -x
```

Note

When using a password and MFA, Snowflake recommends enabling [MFA caching](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-mfa-caching).

## Installing from a branch, tag, or commit

To test an unreleased Snowflake CLI change or a fork, use `custom-github-ref`:

Copy code

```
- uses: snowflakedb/snowflake-actions@v3
  with:
    custom-github-ref: "feature/my-branch"  # or a tag/commit hash
```

## Platform support

The action runs on Ubuntu, macOS, and Windows GitHub-hosted runners and is tested against Python 3.10 and 3.13. Note the following platform-specific behavior:

- **Linux and macOS**: the copied `config.toml` is set to `0600` permissions.
- **Windows**: file permissions on `config.toml` are not modified. Use GitHub Secrets for credentials; avoid committing secrets to `config.toml` regardless of the runner.

## Related resources

- [Configure CI/CD Integrations with Snowflake](https://www.snowflake.com/en/developers/guides/configure-cicd-integrations-with-snowflake). Step-by-step walkthrough for setting up Snowflake CLI in a GitHub Actions pipeline.
- [snowflake-actions repository](https://github.com/snowflakedb/snowflake-actions). Action source and release notes.
- [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd). Overview of all Snowflake-supported CI/CD integrations.
- [DevOps with Snowflake](/developer-guide/builders/devops-with-snowflake). DevOps with Snowflake concepts and workflow guidance.
- [Workload identity federation](/user-guide/workload-identity-federation). Snowflake workload identity federation reference.
