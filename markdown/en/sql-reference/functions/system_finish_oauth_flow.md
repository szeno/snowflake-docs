Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$FINISH\_OAUTH\_FLOW

Sets the OAUTH\_REFRESH\_TOKEN parameter value of the secret passed as an argument in the [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow)
call that began the OAuth flow.

This function completes the OAuth client flow begun with SYSTEM$START\_OAUTH\_FLOW.

## Syntax

Copy code

```
SYSTEM$FINISH_OAUTH_FLOW( '<query_string>' )
```

## Arguments

`'query_string'`
:   Query string from the URL in the browser after completing user authentication and providing OAuth consent.

## Usage notes

Use this function to set the refresh token of an OAuth2 secret you’re using to authenticate with a service provider. This function finishes an
OAuth flow that must begin with your call to [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow).

You must execute this function immediately after – and in the same session as – SYSTEM$START\_OAUTH\_FLOW. This ensures that the user who is
finishing the flow is the same as the user who started it.

## Examples

Copy code

```
SELECT SYSTEM$FINISH_OAUTH_FLOW('state=252462476&authz_code=54264262');
```
