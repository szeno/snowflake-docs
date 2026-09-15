Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DECODE\_PAT

Returns information about a [programmatic access token](/user-guide/programmatic-access-tokens), given the secret for the
token. This information includes the name of the token, the state of the token, and the user associated with the token.

You can call this function if you need to disable a programmatic access token and you want to know which user is associated with
the token.

## Syntax

Copy code

```
SYSTEM$DECODE_PAT( '<secret_for_programmatic_access_token>' )
```

## Arguments

`'secret_for_programmatic_access_token'`
:   Secret for the programmatic access token.

## Returns

Returns a VARCHAR value containing the token information in a JSON object. The JSON object has the following fields:

| Field | Description |
| --- | --- |
| `STATE` | State of the programmatic access token. This field contains one of the following values:  - `ACTIVE`: The programmatic access token can be used to authenticate and has not expired yet. - `EXPIRED`: The programmatic access token cannot be used to authenticate because the expiration date has passed. - `DISABLED`: The programmatic access token is [disabled](/user-guide/programmatic-access-tokens#label-pat-disabled) because user login access is disabled or   the user is locked out of logging in. |
| `PAT_NAME` | Name of the programmatic access token. |
| `USER_NAME` | Name of the user associated with the programmatic access token. |

Expand

Show lessSee more

## Examples

The following example returns information about the programmatic access token with the secret `abC...Y5Z`:

Copy code

```
SELECT SYSTEM$DECODE_PAT('abC...Y5Z');
```

```
+------------------------------------------------------------------------+
| SYSTEM$DECODE_PAT('☺☺☺...☺☺☺')                                         |
|------------------------------------------------------------------------|
| {"STATE":"ACTIVE","PAT_NAME":"MY_EXAMPLE_TOKEN","USER_NAME":"MY_USER"} |
+------------------------------------------------------------------------+
```
