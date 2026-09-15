# snow auth oidc commands

The `snow auth oidc` commands enable secure, password-less authentication to Snowflake. It leverages OpenID Connect (OIDC) tokens from CI/CD environments like GitHub Actions. This feature supports workload identity federation (WIF), enabling automated systems to access Snowflake without static credentials, which aligns with security best practices.

The following Snowflake CLI `snow auth oidc` commands let you manage authentication for your Snowflake projects:

- [snow auth oidc read-token](/developer-guide/snowflake-cli/command-reference/auth-commands/read-token)

Note the following:

- The `snow auth oidc` commands are currently limited to GitHub Actions as the provider.
- The OIDC token is only available when running inside a supported CI/CD environment, such as a GitHub Actions runner.
- Short-lived OIDC tokens are detected dynamically; Snowflake CLI does not store any OIDC tokens.
