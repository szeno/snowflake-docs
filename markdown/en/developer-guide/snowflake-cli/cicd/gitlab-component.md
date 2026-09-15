# Snowflake CI/CD Component for GitLab

Preview Feature

This feature is in public preview. Inputs and behavior may change between releases.

The Snowflake CI/CD Component for GitLab ([snowflake-dev/snowflake-cicd-component](https://gitlab.com/snowflake-dev/snowflake-cicd-component)) installs and configures Snowflake CLI in a GitLab CI/CD pipeline. Use it to automate Snowflake deployments (DCM projects, Snowpark applications, Snowflake Native Apps, and SQL scripts) from your GitLab project.

## How it works

The component publishes two surfaces, both supplied by the same setup logic:

- A published job that installs Snowflake CLI, deploys `config.toml`, and configures OIDC, then runs the commands you pass via `inputs.script:`. This is the simplest way to use the component (single-job pipelines). You can rename the job via `inputs.job-name:`.
- A hidden job template (`.configure-snowflake-cli`) that you `extends:` from your own jobs when you need `snow` in more than one job. Set `inputs.template-only: true` to suppress the published job. See [Multiple snow-using jobs](#label-gitlab-component-multi-job).

The shared `before_script:`:

1. Installs the `uv` Python package manager.
2. Installs Snowflake CLI in an isolated environment (`uv tool install snowflake-cli`).
3. Copies `config.toml` from the repository to `~/.snowflake/config.toml` with `0600` permissions. Skipped if the file is absent.
4. When OIDC authentication is enabled, instructs GitLab to generate a short-lived ID token and exports the Snowflake workload identity environment variables.

Note

Each GitLab CI job runs in its own container, so the Snowflake CLI install does not travel between jobs. To run `snow` in a job, either pass your commands through `inputs.script:` (single-job pipelines) or `extends: .configure-snowflake-cli` from your own job (multi-job pipelines).

## Quick usage example

Include the component and pass your `snow` commands through `inputs.script:`. The component installs Snowflake CLI and runs your commands in the same container, so `snow` is on `PATH` for everything you pass.

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      use-oidc: true
      cli-version: "3.16"
      job-name: deploy-prod
      script:
        - snow connection test -x
        - snow dcm deploy --target PROD -x

variables:
  SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
  SNOWFLAKE_USER: gitlab_cicd_user
```

## Inputs

The component accepts the following inputs, specified under `inputs:` in your `include:` block:

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `cli-version` | No | (latest) | Snowflake CLI version to install, for example `3.11.0`. When omitted, the latest released version is installed. |
| `default-config-file-path` | No | `./config.toml` | Path to your `config.toml`, relative to the repository root. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| `use-oidc` | No | `false` | When `true`, configures OIDC authentication using GitLab ID tokens. |
| `oidc-audience` | No | `snowflakecomputing.com` | Audience claim to request for the GitLab ID token. |
| `stage` | No | `build` | Pipeline stage in which the published job runs. Override if your pipeline declares custom `stages:` without `build`. |
| `job-name` | No | `configure-snowflake-cli` | Name of the published job. Override to give the job a meaningful name in pipeline output (for example, `deploy-prod`). |
| `script` | No | (no-op echo) | Commands the published job runs after Snowflake CLI is installed. Pass your `snow` commands here for the simple single-job pattern. Ignored when `template-only: true`. |
| `template-only` | No | `false` | When `true`, suppresses the published job. Set `true` when you only need the hidden template (multi-job pattern) and don’t want a phantom job in your pipeline. |

Expand

Show lessSee more

## Authentication methods

The component supports three ways of authenticating with Snowflake. Snowflake recommends OIDC because it avoids storing long-lived secrets in GitLab.

| Method | Security | Notes |
| --- | --- | --- |
| [Workload identity federation (WIF) with OIDC](#label-gitlab-component-oidc) (recommended) | Secretless, short-lived tokens | Requires Snowflake CLI 3.11 or later. |
| [Key pair authentication](#label-gitlab-component-key-pair) | Private key stored in GitLab CI/CD variables | Works with any Snowflake CLI version. Combined with `config.toml` or environment variable overrides. |
| [Password authentication](#label-gitlab-component-password) | Password stored in GitLab CI/CD variables | Legacy option, not recommended for production pipelines. |

Expand

Show lessSee more

### Workload identity federation (WIF) with OIDC

Note

OIDC authentication requires Snowflake CLI version 3.11.0 or later.

With WIF OIDC, GitLab issues a short-lived ID token that Snowflake validates directly. No private key or password is stored in GitLab.

#### Create the service user

Create a Snowflake service user that trusts GitLab’s OIDC provider:

Copy code

```
CREATE USER gitlab_cicd_user
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://gitlab.com'
    SUBJECT = 'project_path:<group>/<project>:ref_type:branch:ref:<branch>'
  );
```

The `SUBJECT` must match the claim GitLab emits for the pipeline job. Common formats:

| Subject format | Matches |
| --- | --- |
| `project_path:<group>/<project>:ref_type:branch:ref:<branch>` | Pipeline run on the specified branch |
| `project_path:<group>/<project>:ref_type:tag:ref:<tag>` | Pipeline triggered by the specified tag |

Expand

Show lessSee more

By default, the subject includes the mutable project path. If your project is renamed or moved, the `sub` claim changes and the service user stops matching. To use the immutable project ID instead, set `ci_id_token_sub_claim_components` to `["project_id", "ref_type", "ref"]` via the [GitLab Projects API](https://docs.gitlab.com/api/projects/). The subject then becomes `project_id:<id>:ref_type:<type>:ref:<name>`.

For the full list of ID token claims and how to configure conditional role access with OIDC claims, see [GitLab Cloud Services: configure a conditional role with OIDC claims](https://docs.gitlab.com/ci/cloud_services/#configure-a-conditional-role-with-oidc-claims).

#### Configure the component

Store your Snowflake account identifier as a GitLab CI/CD variable (see the GitLab documentation on [defining CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)), then set `use-oidc: true` on the component:

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      use-oidc: true
      cli-version: "3.16"
      job-name: deploy-prod
      script:
        - snow connection test -x

variables:
  SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
  SNOWFLAKE_USER: gitlab_cicd_user
```

When `use-oidc: true` is set, the component exports the following environment variables in the same container as your `inputs.script:`:

- `SNOWFLAKE_AUTHENTICATOR=WORKLOAD_IDENTITY`
- `SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER=OIDC`
- `SNOWFLAKE_TOKEN=<id-token>`

For broader context, see [Workload identity federation](/user-guide/workload-identity-federation).

### Key pair authentication

Store your Snowflake private key as a GitLab CI/CD variable (preferably masked and file-typed) and pass it through the environment. You can use a temporary connection (no `config.toml` required) or a named connection defined in `config.toml`.

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      cli-version: "3.16"
      job-name: deploy-prod
      script:
        - snow connection test -x
        - snow dcm deploy --target PROD -x

variables:
  SNOWFLAKE_AUTHENTICATOR: SNOWFLAKE_JWT
  SNOWFLAKE_USER: $SNOWFLAKE_USER
  SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
  SNOWFLAKE_PRIVATE_KEY_RAW: $SNOWFLAKE_PRIVATE_KEY_RAW
  PRIVATE_KEY_PASSPHRASE: $PRIVATE_KEY_PASSPHRASE
```

For connection-file-based authentication, commit a `config.toml` with an empty connection block and supply the credentials through `SNOWFLAKE_CONNECTIONS_<NAME>_*` variables. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

### Password authentication

Password authentication is supported for legacy workflows but is not recommended for production CI/CD. Unset `SNOWFLAKE_AUTHENTICATOR` and pass `SNOWFLAKE_PASSWORD`:

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      job-name: deploy-prod
      script:
        - snow connection test -x

variables:
  SNOWFLAKE_USER: $SNOWFLAKE_USER
  SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
  SNOWFLAKE_PASSWORD: $SNOWFLAKE_PASSWORD
```

Note

When using a password and MFA, Snowflake recommends enabling [MFA caching](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-mfa-caching).

## Multiple snow-using jobs

For pipelines that run `snow` from more than one job (for example, a build/test stage that validates your project, then a separate deploy stage), include the component once with `template-only: true` and `extends: .configure-snowflake-cli` from each job that needs `snow`. The hidden template’s `before_script:` runs in each extending job’s container, so each job gets its own Snowflake CLI install, `config.toml`, and (when `use-oidc: true`) a fresh ID token. Setting `template-only: true` suppresses the published job so you don’t get a phantom in your pipeline.

Copy code

```
include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      use-oidc: true
      template-only: true

stages: [build, deploy]

build-check:
  extends: .configure-snowflake-cli
  stage: build
  script:
    - snow connection test -x
    - snow dcm plan --target PROD
  variables:
    SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER: gitlab_cicd_user

deploy:
  extends: .configure-snowflake-cli
  stage: deploy
  needs: [build-check]
  script:
    - snow dcm deploy --target PROD -x
  variables:
    SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER: gitlab_cicd_user
```

## Pipeline stage configuration

The component runs the published job in the stage named by the `stage` input (default `build`). The stage must exist in your pipeline’s `stages:` list. To run the job in a different stage, declare the stage and set the input:

Copy code

```
stages: [setup, deploy]

include:
  - component: $CI_SERVER_FQDN/snowflake-dev/snowflake-cicd-component/configure-snowflake-cli@1.1.0
    inputs:
      stage: deploy
      use-oidc: true
      script:
        - snow connection test -x
```

## Related resources

- [snowflake-cicd-component repository](https://gitlab.com/snowflake-dev/snowflake-cicd-component). Component source and release notes.
- [GitLab CI/CD Components documentation](https://docs.gitlab.com/ci/components/).
- [GitLab OIDC ID token authentication](https://docs.gitlab.com/ci/secrets/id_token_authentication/).
- [GitLab Cloud Services: configure a conditional role with OIDC claims](https://docs.gitlab.com/ci/cloud_services/#configure-a-conditional-role-with-oidc-claims).
- [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd). Overview of all Snowflake-supported CI/CD integrations.
- [DevOps with Snowflake](/developer-guide/builders/devops-with-snowflake). DevOps with Snowflake concepts and workflow guidance.
- [Workload identity federation](/user-guide/workload-identity-federation). Snowflake workload identity federation reference.
