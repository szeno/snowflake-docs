Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$ISSUE\_WORKLOAD\_IDENTITY\_FEDERATION\_TOKEN

Returns an ID token that a Snowflake workload can send to an external service for authentication purposes.

For more information about using this function, see [Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound).

## Syntax

Copy code

```
SYSTEM$ISSUE_WORKLOAD_IDENTITY_FEDERATION_TOKEN(
  '<workload_identity_secret>',
  '<audience>' )
```

## Arguments

`'workload_identity_secret'`
:   Fully qualified name of the [secret](/sql-reference/sql/create-secret) that was created for the Snowflake workload that is
    authenticating with workload identity federation.

    The type of the secret must be `WORKLOAD_IDENTITY_FEDERATION`.

`'audience'`
:   Specifies the audience of the ID token in JSON format. The function uses this value to set the `aud` claim of the ID token.

    The audience is specified in the following format:

    Copy code

    ```
    { "aud": "<audience_identifier>" }
    ```

## Returns

Returns an encoded ID token that conforms to the [OIDC specification](https://openid.net/specs/openid-connect-core-1_0.html#IDToken).

## Examples

Generate an ID token for the workload that created the `my_workload` secret so it can authenticate with workload identity federation.
The workload intends to send the ID token to the service identified by `example-cloud-service.com`.

Copy code

```
SELECT SYSTEM$ISSUE_WORKLOAD_IDENTITY_FEDERATION_TOKEN(
  'my_db.auth.my_workload',
  '{
    "aud": "example-cloud-service.com"
    }'
  );
```
