Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$START\_OAUTH\_FLOW

Initiates the OAUTH client flow, returning a URL you use in a browser to complete the OAuth consent process.

## Syntax

Copy code

```
SYSTEM$START_OAUTH_FLOW( '<database_name.schema_name.secret_name>' )
```

## Arguments

`'database_name.schema_name.secret_name'`
:   The name of the OAuth2 secret specifying authentication information for the API to access with OAuth.

## Usage notes

Use this function to begin a flow that results in an OAuth refresh token added to the secret you pass to this function as an argument.

As an intermediate step, this function returns an authorization URL you can in a browser to complete the OAuth consent process.

After executing this function and using the URL it returns, immediately execute [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow)
in the same session to have Snowflake add a refresh token to the secret you specified.

The [secret](/sql-reference/sql/create-secret) in this function’s argument must include:

- A TYPE parameter specifying a value of `oauth2`.
- An API\_AUTHENTICATION parameter specifying a [security integration](/sql-reference/sql/create-security-integration-api-auth)
  containing details (such as OAuth client ID, secret, authorization endpoint, and token endpoint) about the service provider for which
  access is being granted.
