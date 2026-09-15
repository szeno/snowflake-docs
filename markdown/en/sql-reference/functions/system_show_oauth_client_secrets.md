Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS

Returns the client secrets in a string. The client ID and a client secret must be included in the authorization header to the OAuth token endpoint.

## Syntax

Copy code

```
SYSTEM$SHOW_OAUTH_CLIENT_SECRETS( '<integration_name>' )
```

## Arguments

`integration_name`
:   Name of the integration. Note that the integration name is case-sensitive and must be uppercase and enclosed in single quotes.

## Output

The function returns the following elements in a JSON object:

| Column Name | Data Type | Description |
| --- | --- | --- |
| oauth\_client\_secret\_2 | BASE64 | Secondary client secret for the specified integration. Snowflake supports two client secrets to allow for uninterrupted rotation. |
| oauth\_client\_secret | BASE64 | Client secret for the specified integration |
| oauth\_client\_id | STRING | Client ID in Snowflake |

Expand

Show lessSee more

## Examples

The following example retrieves the client secret for the specified integration:

> Copy code
>
> ```
> select system$show_oauth_client_secrets('MYINT');
> ```
