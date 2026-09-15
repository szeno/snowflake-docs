# Integrating CI/CD with Snowflake CLI

Snowflake CLI integrates with popular CI/CD (continuous integration and continuous delivery) platforms so that you can automate Snowflake deployments for DCM projects, Snowpark applications, Snowflake Native Apps, and standalone SQL scripts. Snowflake publishes and maintains first-party integrations for the most widely used CI/CD systems; for any platform that can run a shell command, you can also install Snowflake CLI directly.

For broader DevOps concepts including declarative object management and environment strategy, see [DevOps with Snowflake](/developer-guide/builders/devops-with-snowflake).

## Supported CI/CD integrations

Snowflake maintains the following first-party CI/CD integrations. Each integration installs Snowflake CLI on the runner and configures authentication to Snowflake.

| Integration | Status | Authentication (recommended) | Reference |
| --- | --- | --- | --- |
| GitHub Action | Generally available | Workload identity federation (OIDC) | [Snowflake CLI GitHub Action](/developer-guide/snowflake-cli/cicd/github-action) |
| GitLab CI/CD Component | Public preview | Workload identity federation (OIDC) | [Snowflake CI/CD Component for GitLab](/developer-guide/snowflake-cli/cicd/gitlab-component) |
| Azure DevOps Extension | Public preview | Workload identity federation (OIDC through Azure service connection) | [Snowflake CLI Azure DevOps Extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension) |

Expand

Show lessSee more

Note

If you use Jenkins, Bitbucket Pipelines, CircleCI, or another CI system that is not listed in the preceding table, you can install Snowflake CLI with a single shell command in your pipeline. See [Installing Snowflake CLI on other CI systems](#label-other-ci-systems).

## Common Snowflake-side setup

All first-party CI/CD integrations follow the same pattern on the Snowflake side:

1. Create a [service user](/user-guide/admin-user-management) that the pipeline authenticates as.
2. Configure the service user’s authentication method. Snowflake recommends workload identity federation (WIF) with OpenID Connect (OIDC) so that no long-lived secrets are stored in the CI system.
3. Grant the service user the roles it needs to deploy your objects.

### Authenticate with workload identity federation (OIDC)

With OIDC, the CI runner obtains a short-lived identity token that Snowflake validates directly. Each CI platform publishes tokens from a different issuer with a different subject claim format; the integration reference pages document the exact values to use.

A minimal service user definition looks like the following. Replace the `ISSUER` and `SUBJECT` values with the ones required by your CI platform (see the corresponding integration reference page).

Copy code

```
CREATE USER <username>
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = '<ci-platform-issuer>'
    SUBJECT = '<ci-platform-subject>'
  );
```

For background on Snowflake WIF, see [Workload identity federation](/user-guide/workload-identity-federation).

### Authenticate with a key pair or password

When OIDC is not available (for example, when you need to support older Snowflake CLI versions or on-premises CI runners), use key pair authentication. Store the private key as a CI secret and pass it through the environment using `SNOWFLAKE_PRIVATE_KEY_RAW` (for a temporary connection) or `SNOWFLAKE_CONNECTIONS_<NAME>_PRIVATE_KEY_RAW` (for a named connection).

Password authentication is supported for legacy workflows but is not recommended for production CI/CD. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections) for the full list of authentication parameters.

## Configuration files and environment variables

Most CI/CD workflows combine a committed `config.toml` with secrets injected through environment variables. The following precedence rules apply:

- Command-line parameters override everything.
- Environment variables that target a specific connection parameter (for example, `SNOWFLAKE_CONNECTIONS_MYCONNECTION_PASSWORD`) override `config.toml`.
- Values defined in `config.toml` are used when no override is provided.
- Generic environment variables such as `SNOWFLAKE_USER` apply last.

For details, including a full parameter reference, see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

## Installing Snowflake CLI on other CI systems

You can run Snowflake CLI on any CI runner that can execute a shell command. The canonical single-line installation uses `uv`:

Copy code

```
uv tool install snowflake-cli
snow --version
```

For installation options on specific operating systems, see [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). For connection management (including using environment variables to avoid storing credentials on the runner), see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

## Typical pipeline stages

A Snowflake CI/CD pipeline typically progresses through three stages: validate proposed changes on a pull request, deploy them on merge, and verify the result. The same pattern works on every CI platform; only the syntax changes.

| Stage | What it does | Example tools |
| --- | --- | --- |
| Validate | Computes the changes that would be applied to the target environment without modifying anything. Post the output as a PR comment so reviewers can confirm intent before merging. | `snow dcm plan` for DCM Projects. |
| Deploy | Applies the validated changes to the target environment. Typically runs after a pull request is merged to the main branch. | `snow dcm deploy` for DCM Projects; `snow sql -f <file>` for standalone SQL scripts; `snow snowpark deploy` for Snowpark applications; `snow git execute` to run SQL files from a Snowflake Git integration. |
| Verify | Refreshes derived data and runs expectation checks to confirm the deployment produced the expected results. | `snow dcm test` to run expectation checks. |

Expand

Show lessSee more

## Security recommendations

- Use workload identity federation (OIDC) wherever your CI system supports it. Avoid storing long-lived credentials in CI secrets.
- Create a dedicated service user for each pipeline environment (for example, one user per repository or per environment). Grant only the roles required for that pipeline.
- Use [Controlling network traffic with network policies](/user-guide/network-policies) to restrict which source IPs can authenticate as the service user when possible.
- Do not commit `config.toml` files that contain credentials. Commit only the connection skeleton and supply secrets through environment variables.
- Rotate private keys and passwords on a regular schedule if you can’t adopt OIDC.

## Related resources

- [Configure CI/CD Integrations with Snowflake](https://www.snowflake.com/en/developers/guides/configure-cicd-integrations-with-snowflake/). CI/CD quickstart.
- [Snowflake CLI GitHub Action](/developer-guide/snowflake-cli/cicd/github-action). Snowflake CLI GitHub Action reference.
- [Snowflake CI/CD Component for GitLab](/developer-guide/snowflake-cli/cicd/gitlab-component). Snowflake CLI CI/CD Component for GitLab reference.
- [Snowflake CLI Azure DevOps Extension](/developer-guide/snowflake-cli/cicd/azure-devops-extension). Snowflake CLI Azure DevOps Extension reference.
- [DevOps with Snowflake](/developer-guide/builders/devops-with-snowflake). DevOps with Snowflake concepts and end-to-end guidance.
- [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). Connection parameter reference.
- [Workload identity federation](/user-guide/workload-identity-federation). Snowflake workload identity federation reference.
